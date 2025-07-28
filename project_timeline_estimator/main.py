import streamlit as st
import project_timelines_monte_carlo
import pdf_question_answering_app

st.set_page_config(page_title="Streamlit Apps Hub", layout="wide")

st.title("📊 Streamlit Apps Hub")

app = st.sidebar.selectbox(
    "Choose an app",
    ("Home", "Project Timeline Estimator", "PDF Question Answering"),
)

if app == "Home":
    st.subheader("Welcome to the App Hub!")
    st.markdown("""
    - 📈 **Project Timeline Estimator**: Run a Monte Carlo simulation to estimate project timelines.
    - 📄 **PDF Question Answering**: Ask questions about uploaded PDFs using AI.
    """)

elif app == "Project Timeline Estimator":
    project_timelines_monte_carlo.run()

elif app == "PDF Question Answering":
    pdf_question_answering_app.run()
