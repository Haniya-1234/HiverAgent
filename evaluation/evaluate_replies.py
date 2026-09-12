import pandas as pd
import os
import json
import time
from src.support_agent import SupportAgent
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split
from groq import Groq

def parse_score(text):
    try:
        # Extract json structure
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:-3]
        elif text.startswith("```"):
            text = text[3:-3]
        
        parsed = json.loads(text.strip())
        return {k.lower(): v for k, v in parsed.items()}
    except Exception as e:
        raise ValueError(f"Failed to parse LLM response: {text}") from e

def main():
    load_dotenv()
    if 'GROQ_API_KEY' not in os.environ:
        print("Error: No GROQ_API_KEY found.")
        return

    client = Groq(api_key=os.environ['GROQ_API_KEY'])
    print("Initializing Support Agent (using Groq for generation)...")
    agent = SupportAgent()
    if agent.llm_provider != 'groq':
        print(f"Warning: Support Agent provider is {agent.llm_provider}, not groq.")
    
    # Generate the exact 50 test cases used by baseline evaluation
    df = pd.read_csv('data/processed/golden_set.csv')
    df = df.dropna(subset=['customer_text', 'intent'])
    
    try:
        X_train, X_test, y_train, y_test = train_test_split(
            df['customer_text'], df['intent'], 
            test_size=0.25, 
            random_state=42, 
            stratify=df['intent']
        )
    except ValueError:
        X_train, X_test, y_train, y_test = train_test_split(
            df['customer_text'], df['intent'], 
            test_size=0.25, 
            random_state=42
        )
    
    test_df = df.loc[X_test.index]
    
    results = []
    print(f"Evaluating {len(test_df)} samples...")
    
    for idx, row in test_df.iterrows():
        customer_msg = row['customer_text']
        true_intent = row['intent']
        conv_id = row.get('conversation_id', None)
        
        print(f"Processing row {idx}...")
        
        # 1. Get Agent Response
        try:
            # We strictly raise failures so we don't fall back to deterministic response silently
            agent_result = agent.process_message(customer_msg, conversation_id=conv_id, raise_on_llm_failure=True)
            predicted_intent = agent_result['predicted_intent']
            intent_conf = agent_result['intent_confidence']
            agent_response = agent_result['draft_response']
            should_escalate = agent_result['should_escalate']
            retrieved_cases = agent_result.get('retrieved_cases', [])
            retrieved_evidence = json.dumps([f"Customer: {c.get('customer_text', '')} | Response: {c.get('support_response', '')}" for c in retrieved_cases])
            agent_error = None
            
        except Exception as e:
            print(f"Agent failed to generate response: {e}")
            agent_result = {}
            predicted_intent = None
            intent_conf = None
            agent_response = None
            should_escalate = None
            retrieved_evidence = None
            agent_error = str(e)
            
        # 2. Call Judge
        scores = {}
        status = "failed"
        judge_error = None
        
        if not agent_error and agent_response:
            prompt = f"""You are an expert customer support evaluator.
Please evaluate the following AI support agent response.

Customer Message: {customer_msg}
Predicted Intent: {predicted_intent}
Escalation Decision: {should_escalate}
Retrieved Evidence: {retrieved_evidence}
Agent Response: {agent_response}

Rate the response on a scale of 1 to 5 for the following dimensions:
1. Relevance: Does the response address the customer's actual issue?
2. Helpfulness: Does it provide useful next steps?
3. Grounding: Is the response supported by the retrieved historical evidence rather than invented?
4. Appropriateness: Is the tone and escalation decision appropriate for customer support?
5. Overall: Overall quality of the proposed support response.

Return a JSON object matching this schema exactly:
{{
  "relevance": 1,
  "helpfulness": 1,
  "grounding": 1,
  "appropriateness": 1,
  "overall": 1,
  "short_reason": "string"
}}
Do NOT output anything except the valid JSON object.
"""
            for attempt in range(3):
                try:
                    response = client.chat.completions.create(
                        model="openai/gpt-oss-20b",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.0,
                        max_tokens=1200
                    )
                    eval_text = response.choices[0].message.content
                    scores = parse_score(eval_text)
                    status = "success"
                    break
                except Exception as e:
                    print(f"Judge failed attempt {attempt+1}: {e}")
                    judge_error = str(e)
                    time.sleep(2)
        else:
            status = "failed"
            judge_error = "Agent response generation failed"

        # 3. Save result
        results.append({
            "example_id": conv_id if pd.notna(conv_id) else idx,
            "customer_text": customer_msg,
            "true_intent": true_intent,
            "predicted_intent": predicted_intent,
            "predicted_confidence": intent_conf,
            "retrieved_evidence": retrieved_evidence,
            "agent_response": agent_response,
            "escalation_decision": should_escalate,
            "llm_relevance": scores.get("relevance"),
            "llm_helpfulness": scores.get("helpfulness"),
            "llm_grounding": scores.get("grounding"),
            "llm_appropriateness": scores.get("appropriateness"),
            "llm_overall": scores.get("overall"),
            "judge_reason": scores.get("short_reason"),
            "status": status,
            "agent_error": agent_error,
            "judge_error": judge_error
        })
        time.sleep(1) # brief pause to respect rate limits

    # 4. Summarize and save
    if results:
        results_df = pd.DataFrame(results)
        os.makedirs('evaluation', exist_ok=True)
        results_df.to_csv('evaluation/llm_judge_scores.csv', index=False)
        
        avg_scores = {}
        for col in ['llm_relevance', 'llm_helpfulness', 'llm_grounding', 'llm_appropriateness', 'llm_overall']:
            avg_scores[col.replace('llm_', '').capitalize()] = results_df[col].mean()
        
        success_count = len(results_df[results_df['status'] == 'success'])
        failed_count = len(results_df[results_df['status'] == 'failed'])
        
        summary = {
            "sample_size": len(results_df),
            "model": "openai/gpt-oss-20b",
            "successful_evaluations": success_count,
            "failed_evaluations": failed_count,
            "average_scores": avg_scores
        }
        
        with open('evaluation/llm_judge_summary.json', 'w') as f:
            json.dump(summary, f, indent=4)
            
        print(f"\nEvaluation complete: {success_count} succeeded, {failed_count} failed.")
        print("Results saved to evaluation/llm_judge_scores.csv and evaluation/llm_judge_summary.json")

if __name__ == '__main__':
    main()
