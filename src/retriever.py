import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

class HistoricalRetriever:
    def __init__(self, dataset_path='data/processed/retrieval_dataset.csv'):
        self.dataset_path = dataset_path
        self.df = None
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=10000)
        self.tfidf_matrix = None
        
    def clean_text(self, text):
        if not isinstance(text, str):
            return ""
        text = text.lower()
        # remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # remove @mentions/usernames
        text = re.sub(r'@[a-z0-9_]+', '', text)
        # normalize obvious punctuation noise (replace with space to avoid word joining)
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Keep meaningful short words, remove other short noise (e.g., 'wth')
        whitelist = {'ios', 'app', 'mac', 'pc', 'tv', 'id', 'bug', 'fix', 'pay', 'sim', 'lte', '5g', '4g', 'os', 'x', 'xr', 'xs', 'se', 'pro', 'max', 'usb', 'pad', 'pod'}
        
        words = text.split()
        cleaned_words = []
        for w in words:
            if len(w) >= 4 or w in whitelist or w.isdigit():
                cleaned_words.append(w)
                
        text = ' '.join(cleaned_words)
        
        # normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def load_and_fit(self):
        print(f"Loading retrieval dataset from {self.dataset_path}...")
        self.df = pd.read_csv(self.dataset_path)
        
        # Basic cleaning of customer text for vectorization
        self.df['customer_text_clean'] = self.df['customer_text'].apply(self.clean_text)
        
        print("Fitting TF-IDF vectorizer...")
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['customer_text_clean'])
        print(f"Fitted TF-IDF on {self.df.shape[0]} documents.")

    def retrieve(self, query, top_k=3, exclude_conversation_id=None, exclude_text=None, min_score=0.15):
        if self.df is None or self.tfidf_matrix is None:
            self.load_and_fit()
            
        # Clean query
        query_clean = self.clean_text(query)
        
        query_vec = self.vectorizer.transform([query_clean])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        
        if exclude_conversation_id is not None:
            mask = self.df['conversation_id'] == exclude_conversation_id
            similarities[mask] = -1.0
            
        if exclude_text is not None:
            mask = self.df['customer_text'] == exclude_text
            similarities[mask] = -1.0
            
        # Get top_k indices
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            score = similarities[idx]
            if score >= min_score:
                results.append({
                    'score': score,
                    'customer_text': self.df.iloc[idx]['customer_text'],
                    'support_response': self.df.iloc[idx]['support_response'],
                    'conversation_id': self.df.iloc[idx]['conversation_id']
                })
            
        return results

if __name__ == '__main__':
    retriever = HistoricalRetriever()
    retriever.load_and_fit()
    res = retriever.retrieve("My iPhone battery is draining too fast after the update", top_k=2)
    print("Test retrieval:")
    for r in res:
        print(f"Score: {r['score']:.4f}")
        print(f"Customer: {r['customer_text']}")
        print(f"Support: {r['support_response']}")
        print("---")
