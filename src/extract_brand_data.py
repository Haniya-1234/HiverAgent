import pandas as pd
import numpy as np
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

def main():
    print("Starting Phase 1: Extract AppleSupport interactions...")
    chunksize = 100000
    file_path = 'data/twcs.csv'
    
    # Ensure processed directory exists
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('report', exist_ok=True)
    
    # Pass 1: Extract AppleSupport tweets
    apple_tweets_list = []
    for chunk in pd.read_csv(file_path, chunksize=chunksize, dtype=str):
        apple_chunk = chunk[chunk['author_id'] == 'AppleSupport']
        apple_tweets_list.append(apple_chunk)
    
    df_apple = pd.concat(apple_tweets_list)
    apple_tweet_ids = set(df_apple['tweet_id'].dropna())
    apple_in_response_to = set(df_apple['in_response_to_tweet_id'].dropna())
    
    print(f"Found {len(df_apple)} AppleSupport tweets.")
    
    # Pass 2: Extract related customer tweets
    customer_tweets_list = []
    for chunk in pd.read_csv(file_path, chunksize=chunksize, dtype=str):
        chunk['tweet_id'] = chunk['tweet_id'].fillna('')
        chunk['in_response_to_tweet_id'] = chunk['in_response_to_tweet_id'].fillna('')
        
        mask = (chunk['author_id'] != 'AppleSupport') & (
            chunk['tweet_id'].isin(apple_in_response_to) |
            chunk['in_response_to_tweet_id'].isin(apple_tweet_ids)
        )
        customer_tweets_list.append(chunk[mask])
        
    df_customer = pd.concat(customer_tweets_list)
    print(f"Found {len(df_customer)} related customer tweets.")
    
    # Combine and build conversation threads
    df_all = pd.concat([df_apple, df_customer]).drop_duplicates(subset=['tweet_id'])
    df_all['in_response_to_tweet_id'] = df_all['in_response_to_tweet_id'].fillna('')
    
    parent_map = dict(zip(df_all['tweet_id'], df_all['in_response_to_tweet_id']))
    
    def get_root(tid):
        seen = set()
        curr = str(tid)
        while curr in parent_map and parent_map[curr] != '':
            if curr in seen:
                break
            seen.add(curr)
            next_tid = parent_map[curr]
            if next_tid not in parent_map:
                break
            curr = next_tid
        return curr

    df_all['conversation_root'] = df_all['tweet_id'].apply(get_root)
    
    print("Grouping into conversations...")
    convs = []
    response_pairs_count = 0
    for root, group in df_all.groupby('conversation_root'):
        group = group.sort_values('created_at')
        cust_tweets = group[group['author_id'] != 'AppleSupport']
        supp_tweets = group[group['author_id'] == 'AppleSupport']
        
        if len(cust_tweets) == 0 or len(supp_tweets) == 0:
            continue
            
        response_pairs_count += min(len(cust_tweets), len(supp_tweets))
            
        convs.append({
            'conversation_id': root,
            'customer_tweet_id': ','.join(cust_tweets['tweet_id']),
            'customer_author_id': cust_tweets.iloc[0]['author_id'],
            'customer_text': ' | '.join(cust_tweets['text'].fillna('')),
            'customer_created_at': cust_tweets.iloc[0]['created_at'],
            'support_tweet_id': ','.join(supp_tweets['tweet_id']),
            'support_text': ' | '.join(supp_tweets['text'].fillna('')),
            'support_created_at': supp_tweets.iloc[0]['created_at'],
            'turn_count': len(group)
        })
    
    df_convs = pd.DataFrame(convs)
    print(f"Built {len(df_convs)} multi-turn conversations.")
    
    print("Phase 2: Filtering (Flagging)...")
    df_convs['is_short'] = (df_convs['customer_text'].str.len() < 20) | (df_convs['support_text'].str.len() < 20)
    
    def is_closure(text):
        text = str(text).lower()
        return bool(re.search(r'\b(thank|thanks|resolved|appreciate it)\b', text)) and len(text) < 50

    df_convs['is_closure'] = df_convs['customer_text'].apply(is_closure) | df_convs['support_text'].apply(is_closure)
    
    def is_dm_request(text):
        text = str(text).lower()
        return bool(re.search(r'\b(dm|direct message)\b', text))

    df_convs['is_dm_request'] = df_convs['support_text'].apply(is_dm_request)
    
    def is_link_heavy(text):
        words = str(text).split()
        links = [w for w in words if w.startswith('http')]
        return len(links) > 0 and (len(links) / len(words)) > 0.3 if words else False

    df_convs['is_link_heavy'] = df_convs['support_text'].apply(is_link_heavy)
    
    top_responses = df_convs['support_text'].value_counts().head(10).index
    df_convs['is_generic_response'] = df_convs['support_text'].isin(top_responses)
    
    print("Phase 3: Candidate conversation quality...")
    is_candidate = (
        (~df_convs['is_short']) &
        (~df_convs['is_closure']) &
        (~df_convs['is_generic_response']) &
        (df_convs['customer_text'].str.len() >= 30)
    )
    df_candidates = df_convs[is_candidate].copy()
    print(f"Selected {len(df_candidates)} candidate conversations.")
    
    print("Phase 4: Intent discovery...")
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 3), max_df=0.8, min_df=5, max_features=2000)
    X = vectorizer.fit_transform(df_candidates['customer_text'])
    
    n_components = 12
    nmf = NMF(n_components=n_components, random_state=42)
    W = nmf.fit_transform(X)
    
    df_candidates['theme_id'] = W.argmax(axis=1)
    terms = vectorizer.get_feature_names_out()
    
    theme_names = {}
    theme_keywords = {}
    for i in range(n_components):
        top_indices = nmf.components_[i].argsort()[-5:][::-1]
        t_name = " | ".join([terms[ind] for ind in top_indices])
        theme_names[i] = t_name
        theme_keywords[i] = [terms[ind] for ind in top_indices[:10]]
        
    df_candidates['candidate_theme'] = df_candidates['theme_id'].map(theme_names)
    
    theme_counts = df_candidates['candidate_theme'].value_counts()
    print("\nDiscovered Candidate Themes:")
    for theme, count in theme_counts.items():
        print(f" - {theme}: {count}")
        
    print("\nPhase 5: Sampling...")
    # Sample ~400 total
    samples_per_theme = max(1, 400 // n_components)
    golden_candidates = df_candidates.groupby('theme_id', group_keys=False).apply(
        lambda x: x.sample(min(len(x), samples_per_theme), random_state=42)
    )
    if len(golden_candidates) < 400:
        remaining = 400 - len(golden_candidates)
        pool = df_candidates[~df_candidates.index.isin(golden_candidates.index)]
        extra = pool.sample(min(len(pool), remaining), random_state=42)
        golden_candidates = pd.concat([golden_candidates, extra])
        
    df_candidates.to_csv('data/processed/apple_support_candidates.csv', index=False)
    golden_candidates.to_csv('data/processed/golden_set_candidates.csv', index=False)
    
    print("\nPhase 6: Documentation...")
    with open('report/intent_discovery.md', 'w', encoding='utf-8') as f:
        f.write("# AppleSupport Intent Discovery Report\n\n")
        f.write("## 1. Data Extraction\n")
        f.write("Conversations were extracted by finding AppleSupport tweets and identifying the root tweet in the `in_response_to_tweet_id` chain. ")
        f.write(f"A total of {len(df_convs)} conversations were formed.\n\n")
        
        f.write("## 2. Filtering Signals\n")
        f.write("Flags were added for short messages, closures, DM requests, and generic templates. Data was not deleted.\n\n")
        
        f.write("## 3. Candidate Selection\n")
        f.write(f"Using length and non-generic patterns, {len(df_candidates)} candidate conversations were selected.\n\n")
        
        f.write("## 4. Theme Discovery\n")
        f.write("TF-IDF and NMF (Non-negative Matrix Factorization) were used to discover candidate themes.\n\n")
        
        f.write("## 5. Candidate Theme Frequencies\n")
        for theme, count in theme_counts.items():
            f.write(f"- **{theme}**: {count} candidates\n")
            
        f.write("\n## 6. Representative Examples\n")
        for i in range(n_components):
            theme = theme_names[i]
            sample = df_candidates[df_candidates['theme_id'] == i].head(1)
            if not sample.empty:
                f.write(f"### {theme}\n")
                f.write(f"**Customer**: {sample['customer_text'].values[0]}\n\n")
                f.write(f"**Support**: {sample['support_text'].values[0]}\n\n")
                
        f.write("## 7. Limitations\n")
        f.write("These are automated candidate themes. Some themes may overlap or capture formatting rather than intent. ")
        f.write("Manual review is required to define the final golden intents.\n")

    print("\n--- FINAL METRICS ---")
    print(f"Number of AppleSupport response pairs (approx): {response_pairs_count}")
    print(f"Number of conversations: {len(df_convs)}")
    print(f"Number of candidate conversations: {len(df_candidates)}")
    print(f"Number of candidate golden examples: {len(golden_candidates)}")
    print("Candidate theme names and counts:")
    for theme, count in theme_counts.items():
        print(f"  {theme}: {count}")
    print("Output file paths:")
    print("  - data/processed/apple_support_candidates.csv")
    print("  - data/processed/golden_set_candidates.csv")
    print("  - report/intent_discovery.md")

if __name__ == '__main__':
    main()
