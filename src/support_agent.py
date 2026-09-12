import pandas as pd
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from src.retriever import HistoricalRetriever

def clean_fallback_response(text):
    if not isinstance(text, str):
        return str(text)
    # Remove URLs
    text = re.sub(r'http[s]?://\S+|www\.\S+', '', text)
    # Remove @mentions
    text = re.sub(r'@\w+', '', text)
    # Normalize whitespace
    text = ' '.join(text.split())
    return text

class SupportAgent:
    def __init__(self, golden_set_path='data/processed/golden_set.csv', confidence_threshold=0.4, retrieval_score_threshold=0.15):
        self.retriever = HistoricalRetriever()
        self.confidence_threshold = confidence_threshold
        self.retrieval_score_threshold = retrieval_score_threshold
        self.classifier = None
        self.classes = None
        self._train_classifier(golden_set_path)
        
        self.llm_provider = None
        self.model = None
        
        # Check for GEMINI
        gemini_key = os.environ.get('GEMINI_API_KEY')
        openai_key = os.environ.get('OPENAI_API_KEY')
        
        if gemini_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=gemini_key)
                self.llm_provider = 'gemini'
            except ImportError:
                pass
                
        elif openai_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=openai_key)
                self.llm_provider = 'openai'
            except ImportError:
                pass

    def _train_classifier(self, golden_set_path):
        # Train baseline classification model on the entire golden set
        df = pd.read_csv(golden_set_path)
        df = df.dropna(subset=['customer_text', 'intent'])
        X = df['customer_text']
        y = df['intent']
        
        self.classifier = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2))),
            ('clf', LogisticRegression(class_weight='balanced', random_state=42, max_iter=1000))
        ])
        self.classifier.fit(X, y)
        self.classes = self.classifier.classes_
        
    def generate_response(self, customer_message, retrieved_cases, should_escalate):
        if should_escalate:
            if not retrieved_cases:
                return "I apologize, but I couldn't find a similar issue to help you. Let me connect you with a human agent."
            else:
                return "Could you provide more details about the issue? Otherwise, let me connect you with a human agent."
            
        if not self.llm_provider:
            # Deterministic fallback
            top_case = retrieved_cases[0]
            if top_case['score'] >= self.retrieval_score_threshold and pd.notna(top_case['support_response']) and str(top_case['support_response']).strip():
                return clean_fallback_response(top_case['support_response'])
            else:
                return "Could you provide more details about the issue? Otherwise, let me connect you with a human agent."
            
        # Using LLM
        context = ""
        for i, case in enumerate(retrieved_cases):
            context += f"Historical Case {i+1}:\nCustomer: {case['customer_text']}\nSupport Response: {case['support_response']}\n\n"
            
        prompt = f"""You are an Apple Support AI Agent. Based on the following historical customer interactions, draft a concise and helpful response for the new customer message. Do not make up Apple policies or URLs. If the historical cases don't contain enough information to solve the problem, suggest standard troubleshooting or ask clarifying questions, but do not hallucinate fixes.

Historical Context:
{context}

New Customer Message:
{customer_message}

Draft Response:"""

        try:
            if self.llm_provider == 'gemini':
                response = self.client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=prompt
                )
                return response.text.strip()
            elif self.llm_provider == 'openai':
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content.strip()
        except Exception as e:
            # Fallback if API fails
            print(f"LLM API failed: {e}. Falling back to deterministic.")
            return clean_fallback_response(retrieved_cases[0]['support_response']) if retrieved_cases else "I'm having trouble right now, let me connect you to a human."

    def process_message(self, customer_message, conversation_id=None):
        # 1. Intent Classification
        pred_intent = self.classifier.predict([customer_message])[0]
        probs = self.classifier.predict_proba([customer_message])[0]
        intent_conf = max(probs)
        
        # 2. Retrieval with Leakage Prevention
        retrieved_cases = self.retriever.retrieve(
            query=customer_message, 
            top_k=3, 
            exclude_conversation_id=conversation_id,
            exclude_text=customer_message,
            min_score=self.retrieval_score_threshold
        )
        
        # 3. Escalation Decision
        should_escalate = False
        escalation_reason = None
        
        top_retrieval_score = retrieved_cases[0]['score'] if retrieved_cases else 0.0

        if not retrieved_cases:
            should_escalate = True
            escalation_reason = "No sufficiently similar historical case was found."
        elif pred_intent == 'OTHER_UNCLEAR':
            should_escalate = True
            escalation_reason = "Intent is unclear and requires human clarification."
        elif pred_intent in ['APPLE_ID_ICLOUD']:
            should_escalate = True
            escalation_reason = f"Intent {pred_intent} usually requires human intervention."
        elif intent_conf < 0.20:
            should_escalate = True
            escalation_reason = f"Intent confidence is very low ({intent_conf:.2f})."
        elif intent_conf < self.confidence_threshold and top_retrieval_score < 0.50:
            should_escalate = True
            escalation_reason = f"Low intent confidence ({intent_conf:.2f}) and weak retrieval evidence ({top_retrieval_score:.2f})."
            
        # 4. Generate Response
        draft_response = self.generate_response(customer_message, retrieved_cases, should_escalate)
        
        return {
            "customer_message": customer_message,
            "predicted_intent": pred_intent,
            "intent_confidence": float(intent_conf),
            "retrieved_cases": retrieved_cases,
            "draft_response": draft_response,
            "should_escalate": should_escalate,
            "escalation_reason": escalation_reason
        }
