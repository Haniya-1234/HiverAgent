import pandas as pd
import numpy as np
import os
import json

def main():
    template_path = 'evaluation/human_review_template.csv'
    llm_path = 'evaluation/llm_judge_scores.csv'
    
    if not os.path.exists(template_path):
        print(f"Error: {template_path} not found.")
        return
        
    df_human = pd.read_csv(template_path)
    df_llm = pd.read_csv(llm_path)
    
    # Check if human ratings are actually filled out
    if 'human_overall_1_5' not in df_human.columns:
        print("Human overall column not found")
        return

    if df_human['human_overall_1_5'].isnull().all() or (df_human['human_overall_1_5'] == "").all():
        print("Human review template has not been filled out yet.")
        print("Please fill out the human_* columns in the CSV before calculating agreement.")
        return
        
    print("Calculating Human-LLM Agreement...")
    
    df = pd.merge(df_human, df_llm, on='example_id')
    
    # Drop rows where human rating is missing
    df = df.dropna(subset=['human_overall_1_5'])
    
    metrics = ['relevance', 'helpfulness', 'grounding', 'appropriateness', 'overall']
    results = {}
    
    for metric in metrics:
        llm_col = f"llm_{metric}"
        human_col = f"human_{metric}_1_5"
        
        try:
            llm_scores = pd.to_numeric(df[llm_col], errors='coerce')
            human_scores = pd.to_numeric(df[human_col], errors='coerce')
            
            # Mask out NaNs for pairwise comparison
            mask = ~np.isnan(llm_scores) & ~np.isnan(human_scores)
            
            if not mask.any():
                results[metric] = {"exact_agreement": None, "mean_absolute_difference": None}
                continue
                
            llm_clean = llm_scores[mask]
            human_clean = human_scores[mask]
            
            exact_match = (llm_clean == human_clean).mean()
            mad = np.abs(llm_clean - human_clean).mean()
            
            results[metric] = {
                "exact_agreement": float(exact_match),
                "mean_absolute_difference": float(mad),
                "examples_compared": int(mask.sum())
            }
            
            print(f"\nMetric: {metric.capitalize()}")
            print(f"Exact Agreement: {exact_match:.2%}")
            print(f"Mean Absolute Difference: {mad:.2f}")
            print(f"Examples compared: {int(mask.sum())}")
            
        except Exception as e:
            print(f"Error calculating agreement for {metric}: {e}")
            
    # Save agreement report
    os.makedirs('evaluation', exist_ok=True)
    with open('evaluation/agreement_report.json', 'w') as f:
        json.dump(results, f, indent=4)
    print("\nReport saved to evaluation/agreement_report.json")
        
if __name__ == '__main__':
    main()
