import pandas as pd
import os
import json
import time
from src.support_agent import SupportAgent

def setup_llm():
    if 'GEMINI_API_KEY' in os.environ:
        try:
            from google import genai
            client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])
            return "gemini", client
        except ImportError:
            pass
    if 'OPENAI_API_KEY' in os.environ:
        try:
            from openai import OpenAI
            return "openai", OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        except ImportError:
            pass
    return None, None

def evaluate_with_gemini(client, prompt):
    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=prompt
    )
    return response.text

def evaluate_with_openai(client, prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
    return response.choices[0].message.content

def parse_score(text):
    try:
        # Expecting JSON response with integer scores 1-5
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:-3]
        elif text.startswith("```"):
            text = text[3:-3]
        return json.loads(text.strip())
    except Exception as e:
        raise ValueError(f"Failed to parse LLM response: {text}") from e

def main():
    llm_type, llm_client = setup_llm()
    if not llm_type:
        print("Error: No LLM API key configured (GEMINI_API_KEY or OPENAI_API_KEY) or libraries missing.")
        print("Please set an API key to run LLM-as-judge evaluation.")
        return

    print("Initializing Support Agent...")
    agent = SupportAgent()
    
    df = pd.read_csv('data/processed/golden_set.csv')
    df = df.dropna(subset=['customer_text', 'intent']).sample(n=10, random_state=42)
    
    results = []
    hit_429 = False
    print("Evaluating 10 samples (Max 20 requests)...")
    
    for idx, row in df.iterrows():
        customer_msg = row['customer_text']
        true_intent = row['intent']
        
        try:
            print(f"Waiting 13 seconds before SupportAgent call for example {idx} to respect 5 RPM limit...")
            time.sleep(13)
            
            agent_result = agent.process_message(customer_msg)
            predicted_intent = agent_result['predicted_intent']
            agent_response = agent_result['draft_response']
            retrieved_evidence = json.dumps([f"Customer: {c.get('customer_text', '')} | Response: {c.get('support_response', '')}" for c in agent_result.get('retrieved_cases', [])])
            
            print(f"Waiting 13 seconds before LLM judge call for example {idx} to respect 5 RPM limit...")
            time.sleep(13)
            
            prompt = f"""
        You are an expert customer support evaluator.
        Please evaluate the following AI support agent response.
        
        Customer Message: {customer_msg}
        Predicted Intent: {predicted_intent}
        Retrieved Evidence: {retrieved_evidence}
        Agent Response: {agent_response}
        
        Rate the response on a scale of 1 to 5 for the following dimensions:
        1. Relevance: Does the response address the customer's issue?
        2. Helpfulness: Does it provide useful next steps or assistance?
        3. Grounding: Is the response supported by the retrieved historical evidence?
        4. Appropriateness: Is automated response vs escalation appropriate?
        5. Overall: Overall quality.
        
        Return ONLY a JSON object with the keys "Relevance", "Helpfulness", "Grounding", "Appropriateness", "Overall" and integer values 1-5. Do not include any other text.
        """
            
            if llm_type == "gemini":
                eval_text = evaluate_with_gemini(llm_client, prompt)
            else:
                eval_text = evaluate_with_openai(llm_client, prompt)
                
            scores = parse_score(eval_text)
            status = "success"
            error_msg = ""
        except Exception as e:
            print(f"Error evaluating row {idx}: {e}")
            scores = {}
            status = "failed"
            error_msg = str(e)
            
            if "429" in str(e) or "exhausted" in str(e).lower() or "quota" in str(e).lower():
                print("Quota reached (429). Stopping early.")
                hit_429 = True
                results.append({
                    "example_id": row.get('conversation_id', idx),
                    "customer_message": customer_msg,
                    "predicted_intent": locals().get('predicted_intent', None),
                    "retrieved_evidence": locals().get('retrieved_evidence', None),
                    "agent_response": locals().get('agent_response', None),
                    "llm_relevance": None,
                    "llm_helpfulness": None,
                    "llm_grounding": None,
                    "llm_appropriateness": None,
                    "llm_overall": None,
                    "status": "failed",
                    "error": error_msg
                })
                break
                
        results.append({
            "example_id": row.get('conversation_id', idx),
            "customer_message": customer_msg,
            "predicted_intent": locals().get('predicted_intent', None),
            "retrieved_evidence": locals().get('retrieved_evidence', None),
            "agent_response": locals().get('agent_response', None),
            "llm_relevance": scores.get("Relevance", None),
            "llm_helpfulness": scores.get("Helpfulness", None),
            "llm_grounding": scores.get("Grounding", None),
            "llm_appropriateness": scores.get("Appropriateness", None),
            "llm_overall": scores.get("Overall", None),
            "status": status,
            "error": error_msg
        })

    if results:
        results_df = pd.DataFrame(results)
        os.makedirs('evaluation', exist_ok=True)
        results_df.to_csv('evaluation/llm_judge_scores_10.csv', index=False)
        
        # Calculate averages, omitting None values (failed runs)
        avg_scores = {}
        for col in ['llm_relevance', 'llm_helpfulness', 'llm_grounding', 'llm_appropriateness', 'llm_overall']:
            if col in results_df.columns:
                avg_scores[col.replace('llm_', '').capitalize()] = results_df[col].mean()
        
        success_count = len(results_df[results_df['status'] == 'success'])
        failed_count = len(results_df[results_df['status'] == 'failed'])
        
        summary = {
            "sample_size": 10,
            "model": "gemini-3.6-flash" if llm_type == "gemini" else "gpt-3.5-turbo",
            "maximum_possible_requests": 20,
            "successful_requests": success_count * 2,  # 2 requests per successful eval
            "failed_requests": failed_count, # At least 1 request failed if it's in failed state
            "429_occurred": hit_429,
            "RPM_limit": 5,
            "RPD_limit": 20,
            "total_attempted": len(results_df),
            "successful_evaluations": success_count,
            "failed_evaluations": failed_count,
            "average_scores": avg_scores
        }
        
        with open('evaluation/llm_judge_summary_10.json', 'w') as f:
            json.dump(summary, f, indent=4)
            
        print(f"\nEvaluation complete: {success_count} succeeded, {failed_count} failed.")
        print("Results saved to evaluation/llm_judge_scores_10.csv and evaluation/llm_judge_summary_10.json")
    else:
        print("No results to save.")

if __name__ == '__main__':
    main()
