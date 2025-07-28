import streamlit as st
import project_timelines_monte_carlo
import pdf_question_answering_app

st.set_page_config(page_title="Streamlit Apps Hub", layout="wide")

st.title("📊 Streamlit Apps Hub")

# Make sidebar always visible and expanded
st.sidebar.title("Navigate Apps")
app = st.sidebar.radio(
    "Select an app",
    ("Home", "Project Timeline Estimator", "PDF Question Answering"),
    index=0,
)

if app == "Home":
    st.subheader("Welcome to the App Hub!")
    st.markdown("""
    - 📈 **Project Timeline Estimator**: Run a Monte Carlo simulation to estimate project timelines.
    - 📄 **PDF Question Answering**: Upload a PDF and ask natural language questions.
    """)

elif app == "Project Timeline Estimator":
    project_timelines_monte_carlo.run()

elif app == "PDF Question Answering":
    pdf_question_answering_app.run()
