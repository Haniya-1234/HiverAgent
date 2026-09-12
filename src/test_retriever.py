import pandas as pd
from retriever import HistoricalRetriever
import sys

def safe_print(text):
    print(str(text).encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding))

def run_test():
    print("Loading Golden Set...")
    golden_df = pd.read_csv('data/processed/golden_set.csv')
    
    # Select 5 interesting examples
    test_examples = golden_df.head(5)
    
    retriever = HistoricalRetriever()
    retriever.load_and_fit()
    
    print("\n" + "="*50)
    print("TESTING RETRIEVAL")
    print("="*50)
    
    for _, row in test_examples.iterrows():
        query = row['customer_text']
        intent = row['intent']
        
        safe_print(f"\nQUERY (Intent: {intent}):")
        safe_print(query)
        print("-" * 30)
        
        results = retriever.retrieve(query, top_k=1)
        
        for idx, res in enumerate(results):
            print(f"RETRIEVED {idx+1} (Score: {res['score']:.4f})")
            safe_print(f"Historical Customer: {res['customer_text']}")
            safe_print(f"Historical Support: {res['support_response']}")
        print("="*50)

if __name__ == '__main__':
    run_test()
