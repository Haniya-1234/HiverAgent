import pandas as pd
import os
from src.support_agent import SupportAgent
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_fscore_support

def main():
    # Force deterministic fallback by removing API keys from env
    if 'GEMINI_API_KEY' in os.environ:
        del os.environ['GEMINI_API_KEY']
    if 'OPENAI_API_KEY' in os.environ:
        del os.environ['OPENAI_API_KEY']

    print("Initializing Support Agent for Evaluation...")
    agent = SupportAgent(confidence_threshold=0.40, retrieval_score_threshold=0.15)
    
    golden_set_path = 'data/processed/golden_set.csv'
    print(f"Loading golden set from {golden_set_path}...")
    try:
        df = pd.read_csv(golden_set_path)
    except FileNotFoundError:
        print(f"Error: Could not find {golden_set_path}")
        return

    total_cases = 0
    correct_intents = 0
    escalated_cases = 0
    no_retrieval_cases = 0
    sum_intent_confidence = 0.0
    sum_top_retrieval_score = 0.0

    has_expected_escalation = 'expected_escalation' in df.columns
    true_positives = 0
    false_positives = 0
    false_negatives = 0

    y_true = []
    y_pred = []

    print("Running evaluation...")
    for index, row in df.iterrows():
        customer_text = row.get('customer_text')
        true_intent = row.get('intent')
        conversation_id = row.get('conversation_id', None)
        
        # Skip rows with missing text or intent
        if pd.isna(customer_text) or pd.isna(true_intent):
            continue

        y_true.append(true_intent)

        result = agent.process_message(customer_text, conversation_id=conversation_id)
        
        y_pred.append(result['predicted_intent'])
        
        total_cases += 1
        
        if result['predicted_intent'] == true_intent:
            correct_intents += 1
            
        sum_intent_confidence += result['intent_confidence']
        
        if result['should_escalate']:
            escalated_cases += 1
            
        if result['retrieved_cases']:
            sum_top_retrieval_score += result['retrieved_cases'][0]['score']
        else:
            no_retrieval_cases += 1
            
        if has_expected_escalation:
            expected_escalation = bool(row['expected_escalation'])
            predicted_escalation = result['should_escalate']
            if expected_escalation and predicted_escalation:
                true_positives += 1
            elif not expected_escalation and predicted_escalation:
                false_positives += 1
            elif expected_escalation and not predicted_escalation:
                false_negatives += 1

    if total_cases == 0:
        print("No valid cases found in golden set.")
        return

    intent_accuracy = correct_intents / total_cases
    escalation_rate = escalated_cases / total_cases
    non_escalated_cases = total_cases - escalated_cases
    avg_intent_confidence = sum_intent_confidence / total_cases
    avg_top_retrieval_score = sum_top_retrieval_score / total_cases
    
    print("\n" + "="*40)
    print("EVALUATION RESULTS")
    print("="*40)
    print(f"Total test cases: {total_cases}")
    print(f"Intent classification accuracy: {intent_accuracy:.2%}")
    print(f"Number of escalated cases: {escalated_cases}")
    print(f"Number of non-escalated cases: {non_escalated_cases}")
    print(f"Escalation rate: {escalation_rate:.2%}")
    print(f"Average intent confidence: {avg_intent_confidence:.4f}")
    print(f"Average top retrieval score: {avg_top_retrieval_score:.4f}")
    print(f"Number of cases with no retrieved result: {no_retrieval_cases}")

    # Calculate Intent Metrics
    labels = sorted(list(set(y_true) | set(y_pred)))
    report = classification_report(y_true, y_pred, output_dict=True, zero_division=0)
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    
    macro_precision, macro_recall, macro_f1, _ = precision_recall_fscore_support(y_true, y_pred, average='macro', zero_division=0)
    _, _, weighted_f1, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted', zero_division=0)
    
    print(f"Macro Precision: {macro_precision:.4f}")
    print(f"Macro Recall: {macro_recall:.4f}")
    print(f"Macro F1 Score: {macro_f1:.4f}")
    print(f"Weighted F1 Score: {weighted_f1:.4f}")

    cm_df = pd.DataFrame(cm, index=labels, columns=labels)
    os.makedirs('evaluation', exist_ok=True)
    cm_df.to_csv('evaluation/support_agent_confusion_matrix.csv')
    
    if has_expected_escalation:
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        
        print(f"\nEscalation Metrics:")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1 Score: {f1:.4f}")
    else:
        print("\nEscalation precision/recall/F1 cannot be calculated from the available data (missing 'expected_escalation' column).")

    # Save to json
    results = {
        "support_agent": {
            "total_cases": total_cases,
            "intent_accuracy": intent_accuracy,
            "escalated_cases": escalated_cases,
            "non_escalated_cases": non_escalated_cases,
            "escalation_rate": escalation_rate,
            "avg_intent_confidence": avg_intent_confidence,
            "avg_top_retrieval_score": avg_top_retrieval_score,
            "no_retrieval_cases": no_retrieval_cases,
            "macro_precision": macro_precision,
            "macro_recall": macro_recall,
            "macro_f1": macro_f1,
            "weighted_f1": weighted_f1,
            "classification_report": report
        }
    }
    
    if has_expected_escalation:
        results["support_agent"].update({
            "precision": precision,
            "recall": recall,
            "f1_score": f1
        })
        
    os.makedirs('evaluation', exist_ok=True)
    import json
    with open('evaluation/agent_results.json', 'w') as f:
        json.dump(results, f, indent=4)
        
    print("\nSaved evaluation results to evaluation/agent_results.json")

if __name__ == '__main__':
    main()
