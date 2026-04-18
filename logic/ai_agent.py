import os
import json
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from logic.rag_system import get_relevant_strategies
import streamlit as st

def get_groq_api_key():
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    # Try getting key from environment
    key = os.environ.get("GROQ_API_KEY")
    if key:
        return key
    
    # Try getting key from Streamlit secrets
    try:
        key = st.secrets.get("GROQ_API_KEY")
        if key:
            return key
    except Exception:
        pass
    
    return None

def get_historical_feedback():
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_path = os.path.join(ROOT_DIR, "data", "agent_feedback_log.json")
    if not os.path.exists(log_path):
        return "No historical feedback available."
    try:
        with open(log_path, 'r') as f:
            logs = json.load(f)
            if not logs:
                return "No historical feedback available."
            
            # Formulate string for prompt
            feedback_str = "Critical Previous Campaign Feedback to Internalize:\n"
            # Get last 5 relevant logs
            for entry in logs[-5:]:
                feedback_str += f"- Profile: Plan {entry.get('plan')} | Action Taken: {entry.get('action')} | Outcome: {entry.get('status')} | Human Feedback: {entry.get('feedback')}\n"
            return feedback_str
    except Exception:
        return "No historical feedback available."


def analyze_churn_and_strategize(customer_profile: dict, prediction_metrics: dict, feature_importances: dict = None):
    """
    Combines ML prediction, RAG pipeline, and previous RL feedback to generate a churn reduction strategy.
    """
    api_key = get_groq_api_key()
    if not api_key:
        return {"error": "GROQ_API_KEY not found."}
        
    try:
        profile_str = ", ".join([f"{k}: {v}" for k, v in customer_profile.items()])
        
        churn_reason = ""
        if feature_importances:
            top_features = list(feature_importances.keys())[:3]
            churn_reason = f"Top contributing factors according to model: {', '.join(top_features)}"
        else:
            if customer_profile.get("watch_hours", 20) < 10:
                churn_reason = "Low engagement / watch hours"
            elif customer_profile.get("monthly_fee", 0) > 15:
                churn_reason = "High price sensitivity"
        
        rag_context = get_relevant_strategies(profile_str, churn_reason)
        feedback_context = get_historical_feedback()
        
        llm = ChatGroq(
            temperature=0.7, 
            model_name="llama-3.3-70b-versatile", 
            api_key=api_key,
            model_kwargs={"response_format": {"type": "json_object"}}
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an elite Netflix Churn Retention Specialist. Always output your response in valid JSON format. "
                       "You will be given a customer profile, the reason they might churn, strategies from our knowledge base, and a log of past successes/failures. "
                       "Adjust your strategy away from previously failed approaches and mimic successful ones.\n\n"
                       "Your output MUST be a JSON object with EXACTLY four keys:\n"
                       "1. 'reasoning': A brief 2-sentence explanation of why the user is at risk.\n"
                       "2. 'recommended_action': A SINGLE STRING containing a markdown-formatted bulleted list of strategic actions (use '\\n- ' for bullets). DO NOT output a JSON array or Python list.\n"
                       "3. 'email_draft': A highly professional, corporate B2C email drafted to the user. MUST include a 'Subject:' line that is creative, sophisticated, and does NOT sound like genetic spam (e.g., do not use 'We missed you'). Use proper greetings/sign-offs, and use 'XYZ' for ANY placeholders (e.g., 'Dear XYZ', 'in the XYZ region').\n"
                       "4. 'promo_code': Generate a realistic looking custom dynamic execution promo code for Stripe API (e.g. 'SAVE20-XYZ', 'PREMIUM-TRIAL-ABC', or 'NONE' if not applicable)."),
            ("human", "Customer Profile: {profile}\n\nChurn Reason: {reason}\n\nKnowledge Base Strategies:\n{context}\n\n{feedback}\n\nRespond in JSON format:")
        ])
        chain = prompt | llm
        
        response = chain.invoke({
            "profile": profile_str,
            "reason": churn_reason,
            "context": rag_context,
            "feedback": feedback_context
        })
        
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            return {"error": "Failed to parse LLM output as JSON.", "raw": response.content}
            
    except Exception as e:
        return {"error": f"Agent error: {str(e)}"}

def analyze_upsell_and_strategize(customer_profile: dict):
    """
    Expansion Agent: Designed for SAFE users with high engagement. Focuses on Upselling and increasing LTV.
    """
    api_key = get_groq_api_key()
    if not api_key:
        return {"error": "GROQ_API_KEY not found."}
        
    try:
        profile_str = ", ".join([f"{k}: {v}" for k, v in customer_profile.items()])
        rag_context = get_relevant_strategies(profile_str, "Highly engaged. Upsell to Premium or suggest add-ons.")
        feedback_context = get_historical_feedback()
        
        llm = ChatGroq(
            temperature=0.8, 
            model_name="llama-3.3-70b-versatile", 
            api_key=api_key,
            model_kwargs={"response_format": {"type": "json_object"}}
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an elite Netflix Expansion & Cross-Selling Specialist. Always output your response in valid JSON format. "
                       "This customer is NOT churning. They are highly engaged. Your job is to increase their Lifetime Value (LTV) by upselling them to a higher tier plan, moving them to an annual subscription, or cross-selling ad-free packages.\n\n"
                       "Your output MUST be a JSON object with EXACTLY four keys:\n"
                       "1. 'reasoning': Explain why this user is a prime target for an upsell based on their profile.\n"
                       "2. 'recommended_action': A SINGLE STRING containing a markdown-formatted bulleted list of upsell actions (use '\\n- ' for bullets). DO NOT output a JSON array or Python list.\n"
                       "3. 'email_draft': A highly professional, celebratory corporate B2C email drafted to the user. MUST include a 'Subject:' line that is creative, sophisticated, and does NOT sound like genetic spam. Use proper greetings/sign-offs, and use 'XYZ' for ANY placeholders (e.g., 'Dear XYZ', 'in the XYZ region').\n"
                       "4. 'promo_code': Generate a realistic looking custom dynamic execution promo code for Stripe API (e.g. 'UPGRADE-XYZ', 'VIP-MONTH-ABC')."),
            ("human", "Customer Profile: {profile}\n\nKnowledge Base Strategies:\n{context}\n\n{feedback}\n\nRespond in JSON format:")
        ])
        chain = prompt | llm
        
        response = chain.invoke({
            "profile": profile_str,
            "context": rag_context,
            "feedback": feedback_context
        })
        
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            return {"error": "Failed to parse LLM output as JSON.", "raw": response.content}
            
    except Exception as e:
        return {"error": f"Agent error: {str(e)}"}

if __name__ == "__main__":
    # Mock testing execution
    dummy_profile = {
        "age": 25,
        "subscription_type": "Premium",
        "watch_hours": 3.5,
        "device": "Mobile",
        "monthly_fee": 19.99
    }
    print("Testing Agent Analysis...")
    result = analyze_churn_and_strategize(dummy_profile, {"churn_risk": 0.85})
    print(json.dumps(result, indent=2))
