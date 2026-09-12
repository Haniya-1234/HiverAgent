import pandas as pd
from src.support_agent import SupportAgent

def main():
    print("Initializing Support Agent...")
    # Using thresholds: intent 0.4, retrieval 0.15
    agent = SupportAgent(confidence_threshold=0.4, retrieval_score_threshold=0.15)
    
    test_cases = [
        {"customer_text": "My phone is loosing battery while on the charger wth @115858", "intent": "BATTERY_DRAIN_HEALTH", "conversation_id": "test1"},
        {"customer_text": "@AppleSupport apps keep crashing after updating ios", "intent": "APP_CRASHING", "conversation_id": "test2"},
        {"customer_text": "Is there another way to unlock an iCloud account? Email isn't working and forgot answers to questions.", "intent": "APPLE_ID_ICLOUD", "conversation_id": "test3"},
        {"customer_text": "Cracked my iPhone 8 screen", "intent": "HARDWARE_PHYSICAL_DAMAGE", "conversation_id": "test4"},
        {"customer_text": "My device is doing that weird thing again.", "intent": "OTHER_UNCLEAR", "conversation_id": "test5"}
    ]

    print("\n" + "="*60)
    print("RUNNING SUPPORT AGENT TESTS")
    print(f"LLM Provider Configured: {agent.llm_provider if agent.llm_provider else 'None (Using deterministic fallback)'}")
    print("="*60 + "\n")
    
    for i, case in enumerate(test_cases):
        msg = case['customer_text']
        conv_id = case['conversation_id']
        true_intent = case['intent']
        
        print(f"--- Test Case {i+1} ---")
        
        result = agent.process_message(msg, conversation_id=conv_id)
        
        print(f"Customer Message: {result['customer_message'].encode('ascii', 'replace').decode('ascii')}")
        print(f"Predicted Intent: {result['predicted_intent']} (Confidence: {result['intent_confidence']:.2f})")
        print(f"Escalate: {result['should_escalate']} | Reason: {result['escalation_reason']}")
        
        print("\nTop Retrieved Cases (Leakage Prevented):")
        if result['retrieved_cases']:
            for j, c in enumerate(result['retrieved_cases']):
                # Print without line breaks for cleaner output
                c_text = c['customer_text'].replace('\n', ' ').encode('ascii', 'replace').decode('ascii')
                print(f"  [{j+1}] Score: {c['score']:.2f} | Customer: {c_text[:80]}...")
        else:
            print("  No cases retrieved above threshold.")
            
        draft_resp = result['draft_response'].encode('ascii', 'replace').decode('ascii')
        print(f"\nDraft Response:\n{draft_resp}")
        print("\n" + "-"*60 + "\n")

if __name__ == '__main__':
    main()
