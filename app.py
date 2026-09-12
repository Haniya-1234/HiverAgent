import streamlit as st
from src.support_agent import SupportAgent, clean_fallback_response

# Set page config for a professional look
st.set_page_config(
    page_title="AI Support Agent",
    page_icon="🤖",
    layout="centered"
)

# Initialize the SupportAgent only once using Streamlit caching
@st.cache_resource
def load_agent():
    return SupportAgent()

agent = load_agent()

# 1. Title
st.title("🤖 AI Customer Support Assistant")

# 2. Description
st.markdown("Describe your customer support issue and let the AI analyze the problem, find similar past cases, and decide whether automated support is appropriate or human assistance is needed.")

# 9. How it works
with st.expander("ℹ️ How this assistant works"):
    st.markdown("""
    1. Understands your issue
    2. Identifies the type of problem
    3. Finds similar customer-support cases from the past
    4. Checks how confident the AI is
    5. Provides an automated response or recommends human assistance
    """)

# 3. Text Area
st.markdown("### 💬 Describe Your Issue")
st.markdown("Tell us what went wrong with your device, app, account, or service.")
customer_message = st.text_area(
    label="Customer Message",
    label_visibility="collapsed",
    placeholder="Example: My iPhone battery is draining very quickly while charging.",
    height=150
)

# 4. Button
if st.button("🔍 Analyze My Issue", use_container_width=True):
    if not customer_message.strip():
        st.warning("Please enter a message to analyze.")
    else:
        with st.spinner("Analyzing issue..."):
            result = agent.process_message(customer_message)
            
            pred_intent = result.get("predicted_intent", "Unknown")
            intent_conf = result.get("intent_confidence", 0.0)
            retrieved_cases = result.get("retrieved_cases", [])
            draft_response = result.get("draft_response", "")
            should_escalate = result.get("should_escalate", False)
            escalation_reason = result.get("escalation_reason", "")
            
            top_retrieval_score = retrieved_cases[0]['score'] if retrieved_cases else 0.0
            
            st.divider()
            st.markdown("### 📊 Analysis Results")
            
            if should_escalate:
                st.error("🚨 **Human Support Recommended**")
                st.markdown("The AI cannot confidently resolve this issue automatically, so human assistance is recommended.")
                if escalation_reason:
                    st.warning(f"**Reason for escalation:** {escalation_reason}")
            else:
                st.success("🟢 **Automated Support Available**")
                
            col1, col2, col3 = st.columns(3)
            col1.metric("Issue Category", pred_intent)
            col2.metric("AI Confidence", f"{intent_conf:.2f}")
            col3.metric("Similar Case Match", f"{top_retrieval_score:.2f}")
            
            if should_escalate:
                st.markdown("### 📝 Recommended next step")
            else:
                st.markdown("### 📝 Recommended Response")
            st.info(draft_response)
            
            if retrieved_cases:
                with st.expander("🔎 Similar Historical Cases"):
                    st.markdown("These are previous support cases that were found to be similar.")
                    for i, case in enumerate(retrieved_cases):
                        st.markdown(f"**Case {i+1}** (Similarity score: {case['score']:.2f})")
                        st.markdown(f"**Previous customer issue:** {clean_fallback_response(case['customer_text'])}")
                        st.markdown(f"**Previous support response:** {clean_fallback_response(case['support_response'])}")
                        if i < len(retrieved_cases) - 1:
                            st.divider()

st.divider()

