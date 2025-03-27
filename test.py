import streamlit as st
from PyPDF2 import PdfReader


def read_pdf(file):
    """Read and extract text from a PDF file."""
    pdf_viewer = PdfReader(file)
    text = ""
    for page in pdf_viewer.pages:
        text += page.extract_text()
    return text


def main():
# Streamlit UI
    st.title("PDF Reader with Streamlit")
    st.write("Upload a PDF file to extract its content.")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        try:
            # Extract text from the uploaded PDF
            text_content = read_pdf(uploaded_file)
            st.write("### Extracted Text:")
            st.text_area("Content", text_content, height=300)
        except Exception as e:
            st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()