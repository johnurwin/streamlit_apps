import streamlit as st
from transformers import pipeline
from pypdf import PdfReader

def run():
    st.set_page_config(page_title="PDF Question Answering", layout="wide")
    st.title("📄 PDF Question Answering App")

    st.markdown("""
    Upload a PDF and ask a natural language question.  
    This app uses a transformer model (`distilbert-base-cased-distilled-squad`) to find answers directly from the text.
    """)

    # Upload PDF file
    pdf_file = st.file_uploader("Upload a PDF", type="pdf")

    # Ask question
    question = st.text_input("Ask a question about the PDF")

    if pdf_file and question:
        reader = PdfReader(pdf_file)
        document_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                document_text += text

        if len(document_text.strip()) == 0:
            st.warning("❗ No extractable text found in the PDF.")
            return

        with st.spinner("Finding the answer..."):
            try:
                qa_pipeline = pipeline(
                    task="question-answering",
                    model="distilbert-base-cased-distilled-squad"
                )

                result = qa_pipeline(question=question, context=document_text)
                st.success("Answer:")
                st.write(result['answer'])

            except Exception as e:
                st.error(f"Error running model: {str(e)}")
