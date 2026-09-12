import pandas as pd
import json
import os
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix

def main():
    # 1. Load data
    data_path = 'data/processed/golden_set.csv'
    df = pd.read_csv(data_path)
    
    # 2. Verify required columns
    required_cols = ['customer_text', 'intent']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' not found in the dataset.")
            
    # Drop any rows with missing intent or customer_text
    df = df.dropna(subset=required_cols)
    
    # 3. Create reproducible train/test split
    # Since some classes are very small (e.g., 2), we'll try to stratify. If it fails, fallback.
    try:
        X_train, X_test, y_train, y_test = train_test_split(
            df['customer_text'], df['intent'], 
            test_size=0.25, 
            random_state=42, 
            stratify=df['intent']
        )
        print("Train/test split completed with stratification.")
    except ValueError:
        print("Warning: Stratification failed (likely due to classes with very few samples). Falling back to non-stratified split.")
        X_train, X_test, y_train, y_test = train_test_split(
            df['customer_text'], df['intent'], 
            test_size=0.25, 
            random_state=42
        )
        
    print(f"Training set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    
    # 4. Implement Baseline 1: Majority-class classifier
    print("\nTraining Baseline 1: Majority Class...")
    dummy_clf = DummyClassifier(strategy='most_frequent', random_state=42)
    dummy_clf.fit(X_train, y_train)
    y_pred_dummy = dummy_clf.predict(X_test)
    
    # 5. Implement Baseline 2: TF-IDF + Logistic Regression
    print("Training Baseline 2: TF-IDF + Logistic Regression...")
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1, 2))),
        ('clf', LogisticRegression(class_weight='balanced', random_state=42, max_iter=1000))
    ])
    pipeline.fit(X_train, y_train)
    y_pred_tfidf = pipeline.predict(X_test)
    
    # 6. Evaluate both baselines
    results = {}
    
    # Eval Baseline 1
    results['baseline_1_majority'] = {
        'accuracy': accuracy_score(y_test, y_pred_dummy),
        'macro_f1': f1_score(y_test, y_pred_dummy, average='macro', zero_division=0),
        'classification_report': classification_report(y_test, y_pred_dummy, output_dict=True, zero_division=0)
    }
    
    # Eval Baseline 2
    results['baseline_2_tfidf_logreg'] = {
        'accuracy': accuracy_score(y_test, y_pred_tfidf),
        'macro_f1': f1_score(y_test, y_pred_tfidf, average='macro', zero_division=0),
        'classification_report': classification_report(y_test, y_pred_tfidf, output_dict=True, zero_division=0)
    }
    
    # 7. Save outputs
    os.makedirs('evaluation', exist_ok=True)
    
    # Save results json
    with open('evaluation/baseline_results.json', 'w') as f:
        json.dump(results, f, indent=4)
        
    # Save test predictions
    test_results_df = pd.DataFrame({
        'customer_text': X_test,
        'true_intent': y_test,
        'pred_baseline_1': y_pred_dummy,
        'pred_baseline_2': y_pred_tfidf
    })
    test_results_df.to_csv('evaluation/baseline_test_predictions.csv', index=False)
    
    # Save confusion matrix for Baseline 2
    labels = sorted(df['intent'].unique())
    cm = confusion_matrix(y_test, y_pred_tfidf, labels=labels)
    cm_df = pd.DataFrame(cm, index=labels, columns=labels)
    cm_df.to_csv('evaluation/tfidf_logreg_confusion_matrix.csv')
    
    print("\nEvaluation outputs saved to evaluation/ directory:")
    print("- baseline_results.json")
    print("- baseline_test_predictions.csv")
    print("- tfidf_logreg_confusion_matrix.csv")
    
    print("\nBaseline 2 (TF-IDF + LogReg) Overall Metrics:")
    print(f"Accuracy: {results['baseline_2_tfidf_logreg']['accuracy']:.4f}")
    print(f"Macro F1: {results['baseline_2_tfidf_logreg']['macro_f1']:.4f}")
    
    print("\nNote: IOS_UPDATE_INSTALLATION has very limited evaluation support (only 2 total samples in the golden set).")

if __name__ == '__main__':
    main()
