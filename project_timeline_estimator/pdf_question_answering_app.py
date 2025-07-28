import streamlit as st
from transformers import pipeline
from pypdf import PdfReader

def run():
    st.header("PDF Question Answering App")

    st.markdown("""
    Upload a PDF and ask a question. The model will extract text and attempt to answer your query.
    """)

    pdf_file = st.file_uploader("Upload a PDF", type="pdf")
    question = st.text_input("Ask a question about the PDF")

    if pdf_file and question:
        reader = PdfReader(pdf_file)
        document_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                document_text += text

        if not document_text.strip():
            st.warning("No extractable text found in PDF.")
            return

        with st.spinner("Loading model and finding the answer..."):
            try:
                qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
            except Exception as e:
                st.error(f"Error loading model: {e}")
                return

            try:
                result = qa_pipeline(question=question, context=document_text)
                st.success("Answer:")
                st.write(result['answer'])
            except Exception as e:
                st.error(f"Error during question answering: {e}")
