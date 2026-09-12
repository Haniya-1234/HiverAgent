import pandas as pd
import os

def main():
    judge_scores_path = 'evaluation/llm_judge_scores.csv'
    template_path = 'evaluation/human_review_template.csv'
    
    if not os.path.exists(judge_scores_path):
        print(f"Error: {judge_scores_path} not found. Please run evaluate_replies.py first.")
        return
        
    df = pd.read_csv(judge_scores_path)
    
    # Sample 20 for human review
    sample_size = min(20, len(df))
    sample_df = df.sample(n=sample_size, random_state=42).copy()
    
    # Add human columns (blank)
    sample_df['human_relevance_1_5'] = ""
    sample_df['human_helpfulness_1_5'] = ""
    sample_df['human_grounding_1_5'] = ""
    sample_df['human_appropriateness_1_5'] = ""
    sample_df['human_overall_1_5'] = ""
    sample_df['human_notes'] = ""
    
    cols = [
        "example_id", "customer_text", "true_intent", "predicted_intent", 
        "retrieved_evidence", "agent_response", "escalation_decision",
        "human_relevance_1_5", "human_helpfulness_1_5", "human_grounding_1_5", 
        "human_appropriateness_1_5", "human_overall_1_5",
        "human_notes"
    ]
    
    # Keep only available columns
    actual_cols = [c for c in cols if c in sample_df.columns]
    # Add any missing expected columns as blank
    for c in cols:
        if c not in actual_cols:
            sample_df[c] = ""
            actual_cols.append(c)
            
    sample_df = sample_df[actual_cols]
    
    sample_df.to_csv(template_path, index=False)
    print(f"Generated human review template with {sample_size} examples at {template_path}")

if __name__ == '__main__':
    main()

