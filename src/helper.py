import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings, ChatMistralAI
from pdfreader import SimplePDFViewer, PDFDocument
from PyPDF2 import PdfReader
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
from langchain.schema import Document

load_dotenv()

def get_pdf_data(file):
    """Read and extract text from a PDF file."""
    pdf_viewer = PdfReader(file)
    text = ""
    for page in pdf_viewer.pages:
        text += page.extract_text()
    return text


def get_split_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)
    return chunks

def get_embeddings(chunks):
    embeddings = MistralAIEmbeddings(api_key=os.getenv("MISTRALAI_API_KEY"))
    document_chunks = [Document(page_content=text) for text in chunks]
    vector_store = FAISS.from_documents(document_chunks, embeddings)
    return vector_store

def get_conversation_chain(vector_store):
    llm = ChatMistralAI(api_key=os.getenv("MISTRALAI_API_KEY"))
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    chain = ConversationalRetrievalChain.from_llm(llm, vector_store.as_retriever(), memory=memory)
    return chain