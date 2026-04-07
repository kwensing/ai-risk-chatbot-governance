import streamlit as st
from chatbot import get_response
from risk_evaluator import check_toxicity, check_bias, check_hallucination, check_privacy
from risk_scoring import calculate_risk
from logging_utils import log_interaction

st.title("AI Chatbot with Risk Assessment")

st.write(
    "This demo shows an AI assitant plus a simple risk assessment layer."
)

user_input = st.text_input("Ask a question:")

if user_input:
    response = get_response(user_input)

    # Combine user input and model response for safety checks
    combined_text = user_input + "\n\n" + response

    tox = check_toxicity(combined_text)
    bias = check_bias(combined_text)
    hall = check_hallucination(response)
    priv = check_privacy(combined_text)

    score, level, details = calculate_risk(tox, bias, hall, priv)

    # Show output
    st.subheader("Response")
    st.write(response)

    st.subheader("Risk Assessment")
    st.write(f"Risk Level: {level}")
    st.write(f"Score: {score}")

    if details:
        st.write("Details:")
        for d in details:
            st.write(f"- {d}")
    else:
        st.write("Details: No specific risks detected by the simple heuristics.")

    # Log to CSV (for governance / audit trail)
    log_interaction(user_input, response, score, level)

    with st.expander("Ethics & Limitations"):
        st.write(
            "This is a simplified demo of AI Risk Assessment. "
            "It uses basic keyword and pattern checkers that may miss many real risks. "
            "Do not rely on it for production decisions."
        )