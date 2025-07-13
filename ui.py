import streamlit as st
import requests
import os

# Get available companies from the documents folder
DOCS_DIR = "documents"
companies = [f.replace(".pdf", "") for f in os.listdir(DOCS_DIR) if f.endswith(".pdf")]

# Five common example questions
EXAMPLE_QUESTIONS = [
    "What personal data does the company collect?",
    "How can I delete my account and data?",
    "Does the company share my data with third parties?",
    "What are the rules for posting content?",
    "How does the company handle data breaches?",
]

st.title("Legal Policy Q&A (RAG)")

company = st.selectbox("Select a company:", companies)

# --- Example Question Boxes ---
st.markdown("<b>Common Questions:</b>", unsafe_allow_html=True)
cols = st.columns(len(EXAMPLE_QUESTIONS))

if 'question' not in st.session_state:
    st.session_state['question'] = ''
if 'auto_ask' not in st.session_state:
    st.session_state['auto_ask'] = False

for i, q in enumerate(EXAMPLE_QUESTIONS):
    with cols[i]:
        if st.button(q, key=f"exq_{i}",
            help="Click to use this question",
            use_container_width=True):
            st.session_state['question'] = q
            st.session_state['auto_ask'] = True
    # Custom CSS for thick border
    st.markdown(f"""
        <style>
        div[data-testid="column"] div[data-testid="stButton"] button {{
            border: 12px solid #4F8BF9;
            border-radius: 8px;
            margin-bottom: 8px;
            font-weight: bold;
            font-size: 1rem;
            background: #f7fafd;
        }}
        </style>
    """, unsafe_allow_html=True)

# --- Main Question Input ---
question = st.text_area("Enter your legal question:", value=st.session_state['question'], key="main_question")

# If an example was clicked, auto-ask
if st.session_state.get('auto_ask', False):
    st.session_state['auto_ask'] = False
    ask_now = True
else:
    ask_now = st.button("Ask")

if ask_now:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Getting answer..."):
            try:
                response = requests.post(
                    "http://localhost:8000/ask",
                    json={"question": question, "company": company}
                )
                data = response.json()
                if "answer" in data:
                    st.success(data["answer"])
                else:
                    st.error(data.get("error", "Unknown error"))
            except Exception as e:
                st.error(f"Request failed: {e}") 