import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Golden Set Annotation Tool", layout="wide")

DATA_PATH = "data/processed/golden_set.csv"

# Label options
LABELS = [
    "IOS_UPDATE_INSTALLATION",
    "DEVICE_FREEZING_UNRESPONSIVE",
    "BATTERY_DRAIN_HEALTH",
    "IOS_AUTOCORRECT_BUG",
    "DEVICE_ACTIVATION",
    "APPLE_MUSIC_LIBRARY",
    "APPLE_ID_ICLOUD",
    "WIFI_BLUETOOTH",
    "APP_CRASHING",
    "HARDWARE_PHYSICAL_DAMAGE",
    "OTHER_UNCLEAR"
]

@st.cache_data(ttl=0)
def load_data():
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        
        # Ensure necessary columns exist
        if 'intent' not in df.columns:
            df['intent'] = None
        if 'label_notes' not in df.columns:
            df['label_notes'] = ""
            
        return df
    else:
        st.error(f"Data file not found at {DATA_PATH}")
        return pd.DataFrame()

def save_data(df):
    df.to_csv(DATA_PATH, index=False)
    st.success("Progress saved successfully!")

def main():
    df = load_data()
    
    if df.empty:
        return

    # Initialize session state for current index if not exists
    if 'current_idx' not in st.session_state:
        # Find first unlabeled row
        unlabeled_indices = df[df['intent'].isna() | (df['intent'] == '')].index
        if len(unlabeled_indices) > 0:
            st.session_state.current_idx = int(unlabeled_indices[0])
        else:
            st.session_state.current_idx = 0

    total_examples = len(df)
    labeled_count = len(df[df['intent'].notna() & (df['intent'] != '')])
    current_idx = st.session_state.current_idx
    
    # Check if index is valid
    if current_idx >= total_examples:
        st.session_state.current_idx = total_examples - 1
        current_idx = st.session_state.current_idx

    current_row = df.iloc[current_idx]

    # Sidebar: Instructions & Rules
    with st.sidebar:
        st.title("Annotation Rules")
        st.markdown("""
        1. Label the customer's **ROOT** problem.
        2. Do not classify based on sentiment/profanity.
        3. If battery + another issue appear, choose the primary/blocking issue.
        4. Hardware damage takes priority when physical damage is clearly the cause.
        5. Distinguish whole-device freezing from a specific app crashing.
        6. Use `OTHER_UNCLEAR` when there is insufficient information to confidently select an intent.
        7. **Do not guess.**
        """)
        
        st.divider()
        st.metric("Progress", f"{labeled_count} / {total_examples} labeled")
        progress_pct = labeled_count / total_examples if total_examples > 0 else 0
        st.progress(progress_pct)

    # Main content
    st.title("Golden Set Annotation Tool")
    
    st.subheader(f"Example {current_idx + 1} of {total_examples}")
    st.write(f"**Current Status:** {'✅ Labeled' if pd.notna(current_row['intent']) and current_row['intent'] != '' else '⏳ Unlabeled'}")
    
    # Display IDs
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"**Example ID:** {current_row.get('example_id', 'N/A')}")
    with col2:
        st.info(f"**Tweet ID:** {current_row.get('tweet_id', 'N/A')}")
    with col3:
        st.info(f"**Conversation ID:** {current_row.get('conversation_id', 'N/A')}")

    # Display Text
    st.markdown("### Customer Message")
    st.success(current_row.get('customer_text', 'N/A'))
    
    st.markdown("### AppleSupport Response")
    st.info(current_row.get('support_text', 'N/A'))

    # Annotation form
    st.markdown("### Annotation")
    
    # Pre-select radio button if already labeled
    current_intent = current_row.get('intent')
    default_index = LABELS.index(current_intent) if pd.notna(current_intent) and current_intent in LABELS else None
    
    selected_label = st.radio(
        "Select the primary intent:",
        LABELS,
        index=default_index,
        key=f"radio_{current_idx}"
    )

    current_notes = current_row.get('label_notes')
    if pd.isna(current_notes):
        current_notes = ""
        
    notes = st.text_area("Optional Notes:", value=current_notes, key=f"notes_{current_idx}")

    # Navigation and Save logic
    col1, col2, col3, col4 = st.columns(4)

    def update_dataframe():
        df.at[current_idx, 'intent'] = selected_label
        df.at[current_idx, 'label_notes'] = notes

    with col1:
        if st.button("⬅️ Previous", disabled=(current_idx == 0)):
            update_dataframe()
            save_data(df)
            st.session_state.current_idx -= 1
            st.rerun()

    with col2:
        if st.button("💾 Save"):
            update_dataframe()
            save_data(df)
            st.rerun()

    with col3:
        if st.button("💾 Save & Next ➡️", disabled=(current_idx == total_examples - 1)):
            update_dataframe()
            save_data(df)
            st.session_state.current_idx += 1
            st.rerun()
            
    with col4:
        if st.button("Next ➡️", disabled=(current_idx == total_examples - 1)):
            update_dataframe()
            save_data(df)
            st.session_state.current_idx += 1
            st.rerun()

if __name__ == "__main__":
    main()
