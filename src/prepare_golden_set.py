import pandas as pd
import numpy as np
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min

def assign_sampling_stratum(text):
    text = str(text).lower()
    # These are NOT labels, just sampling strata to ensure coverage
    if re.search(r'\b(update|install|ios 11|ios 10|software)\b', text): return 'updates_installation'
    if re.search(r'\b(freeze|frozen|unresponsive|stuck|reboot|restart)\b', text): return 'freezing_performance'
    if re.search(r'\b(battery|drain|power|charge|health)\b', text): return 'battery'
    if re.search(r'\b(autocorrect|keyboard|type|typing)\b', text): return 'autocorrect_keyboard'
    if re.search(r'\b(activate|activation|setup)\b', text): return 'activation'
    if re.search(r'\b(music|library|playlist|song|itunes)\b', text): return 'apple_music_itunes'
    if re.search(r'\b(apple id|icloud|password|login)\b', text): return 'apple_id_icloud'
    if re.search(r'\b(wifi|wi-fi|bluetooth|connection)\b', text): return 'wifi_bluetooth'
    if re.search(r'\b(app crash|crash|closes itself|crashing)\b', text): return 'app_crashes'
    if re.search(r'\b(screen|broken|drop|crack|damage|button)\b', text): return 'hardware_physical_damage'
    return 'other_unclear'

def sample_diverse(df, n_samples):
    if len(df) <= n_samples:
        return df
    
    # TF-IDF features based on unigrams and bigrams
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000, ngram_range=(1,2))
    X = vectorizer.fit_transform(df['customer_text'])
    
    # KMeans clustering to ensure we select diverse examples in the stratum
    kmeans = KMeans(n_clusters=n_samples, random_state=42, n_init=10)
    kmeans.fit(X)
    
    closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_, X)
    return df.iloc[closest]

def main():
    # Load the full candidate dataset
    df = pd.read_csv('data/processed/apple_support_candidates.csv')
    
    # Apply filtering to prefer substantive customer problems
    df = df[df['is_short'] == False]
    df = df[df['is_generic_response'] == False]
    
    # Filter out text that is too short after removing URLs (e.g. pure thanks with URL)
    df['text_no_urls'] = df['customer_text'].str.replace(r'http\S+', '', regex=True).str.strip()
    df = df[df['text_no_urls'].str.len() > 20]
    
    # Deduplicate
    df['normalized_text'] = df['text_no_urls'].str.lower().str.replace(r'[^a-z0-9]', '', regex=True)
    df = df.drop_duplicates(subset=['normalized_text'])
    
    # Assign proxy stratum for coverage (NOT final labels)
    df['sampling_stratum'] = df['customer_text'].apply(assign_sampling_stratum)
    
    strata_counts = df['sampling_stratum'].value_counts()
    
    target_total = 200
    n_strata = df['sampling_stratum'].nunique()
    
    # Attempt equal distribution among strata
    base_per_stratum = target_total // n_strata
    remainder = target_total % n_strata
    
    counts = {s: base_per_stratum for s in df['sampling_stratum'].unique()}
    for s in strata_counts.head(remainder).index:
        counts[s] += 1
        
    sampled_dfs = []
    
    for stratum, group_df in df.groupby('sampling_stratum'):
        n_req = counts[stratum]
        sampled_group = sample_diverse(group_df, n_req)
        sampled_dfs.append(sampled_group)
        
    final_df = pd.concat(sampled_dfs)
    
    # If exactly 200 is not reached, sample from remainder
    if len(final_df) < target_total:
        deficit = target_total - len(final_df)
        remaining = df[~df.index.isin(final_df.index)]
        if len(remaining) > 0:
            extra = sample_diverse(remaining, min(deficit, len(remaining)))
            final_df = pd.concat([final_df, extra])
            
    final_df = final_df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Format the output strictly as requested
    final_df['example_id'] = ['EX_' + str(i).zfill(4) for i in range(len(final_df))]
    final_df['intent'] = ""
    final_df['label_notes'] = ""
    
    final_cols = ['example_id', 'conversation_id', 'customer_tweet_id', 'customer_text', 'support_text', 'intent', 'label_notes']
    output_df = final_df[final_cols]
    
    os.makedirs('data/processed', exist_ok=True)
    output_path = 'data/processed/golden_set.csv'
    output_df.to_csv(output_path, index=False)
    
    print(f"Total selected = {len(output_df)}")
    print(f"\nSampling methodology: Diversity-oriented pre-annotation sampling using stratified KMeans clustering on TF-IDF unigram/bigram features.")
    print(f"\nDiversity/topic coverage statistics (sampling strata, NOT labels):")
    print(final_df['sampling_stratum'].value_counts())
    print(f"\nOutput path: {output_path}")

if __name__ == '__main__':
    main()
