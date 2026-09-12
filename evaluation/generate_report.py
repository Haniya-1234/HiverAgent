import json
import os

def load_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return None

def main():
    report = {}
    
    # Load Baselines
    baselines = load_json('evaluation/baseline_results.json')
    if baselines:
        report['baselines'] = baselines
        
    # Load Agent metrics
    agent_results = load_json('evaluation/agent_results.json')
    if agent_results:
        report['support_agent_metrics'] = agent_results['support_agent']
        
    # Load LLM Judge Summary
    llm_summary = load_json('evaluation/llm_judge_summary.json')
    if llm_summary:
        report['llm_judge_scores'] = llm_summary
        
    # Load Human Agreement
    agreement = load_json('evaluation/agreement_report.json')
    if agreement:
        report['human_agreement'] = agreement
        
    # Write full report
    with open('evaluation/evaluation_report.json', 'w') as f:
        json.dump(report, f, indent=4)
        
    print("\n" + "="*50)
    print("EVALUATION REPORT SUMMARY")
    print("="*50)
    
    if 'baselines' in report:
        print("\nBaselines:")
        for k, v in report['baselines'].items():
            print(f"  {k} - Accuracy: {v.get('accuracy', 0):.2%}, Macro F1: {v.get('macro_f1', 0):.4f}")
            
    if 'support_agent_metrics' in report:
        print("\nSupport Agent Metrics:")
        metrics = report['support_agent_metrics']
        print(f"  Intent Accuracy: {metrics.get('intent_accuracy', 0):.2%}")
        if 'f1_score' in metrics:
            print(f"  Escalation F1: {metrics.get('f1_score', 0):.4f}")
            
    if 'llm_judge_scores' in report:
        print("\nLLM-as-Judge Average Scores (1-5):")
        for k, v in report['llm_judge_scores'].items():
            print(f"  {k}: {v:.2f}")
    else:
        print("\nLLM-as-Judge: Not run (no API key configured or script not executed).")
        
    if 'human_agreement' in report:
        print("\nHuman-LLM Agreement:")
        for k, v in report['human_agreement'].items():
            if v.get('exact_agreement') is not None:
                print(f"  {k} - Exact Agreement: {v.get('exact_agreement'):.2%}, Mean Abs Diff: {v.get('mean_absolute_difference'):.2f}")
    else:
        print("\nHuman Agreement: No annotations available yet.")
        
    print("\nDetailed report saved to evaluation/evaluation_report.json")
    print("="*50 + "\n")

if __name__ == '__main__':
    main()
