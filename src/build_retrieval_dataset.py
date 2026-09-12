import pandas as pd

def build_retrieval_dataset(input_path, output_path):
    print(f"Loading candidates from {input_path}...")
    df = pd.read_csv(input_path)
    print(f"Original shape: {df.shape}")
    
    # Filter out empty responses
    df = df.dropna(subset=['customer_text', 'support_text'])
    
    # Filter out extremely short support responses (e.g., less than 15 chars)
    df = df[df['support_text'].str.len() >= 15]
    
    # Filter out pure greetings/DM requests based on heuristics
    if 'is_dm_request' in df.columns:
        # Some responses contain troubleshooting links AND dm links.
        # Let's count how many links are in the text.
        # If it's a DM request and only has 1 link (which is the DM link), it's likely a pure DM request.
        # But for simplicity, we drop all is_dm_request == True unless they also have is_link_heavy
        # Actually is_link_heavy is False for all DM requests as per check.
        # Let's just drop all pure dm_requests to be safe and ensure high quality
        # But we don't want to lose all data. 
        # Let's use a simpler check: if it's a DM request and has no support article link
        # Support links usually look like https://support.apple.com/ or https://apple.co/ or just typical shortlinks.
        
        # We will filter out obvious DM requests: those with is_dm_request == True.
        # We'll also allow those that have "steps" or "article" in the text, indicating a resolution is provided before asking for DM.
        has_resolution = df['support_text'].str.contains(r'step|article|update|restart|here is|here\'s|try this', case=False, na=False)
        obvious_dm = (df['is_dm_request'] == True) & (~has_resolution)
        df = df[~obvious_dm]
        
    if 'is_generic_response' in df.columns:
        df = df[df['is_generic_response'] == False]
    
    # We can filter out duplicates
    df = df.drop_duplicates(subset=['support_text'])
    
    # Select columns
    retrieval_df = df[['conversation_id', 'customer_text', 'support_text']].rename(columns={'support_text': 'support_response'})
    
    print(f"Filtered shape: {retrieval_df.shape}")
    
    retrieval_df.to_csv(output_path, index=False)
    print(f"Saved retrieval dataset to {output_path}")

if __name__ == "__main__":
    build_retrieval_dataset('data/processed/apple_support_candidates.csv', 'data/processed/retrieval_dataset.csv')
