import streamlit as st
from src.helper import get_pdf_data, get_split_chunks, get_embeddings, get_conversation_chain

def  main():
    st.set_page_config(page_title="Information Retrieval")
    st.header("Information Retrieval System")
    user_input = st.text_input("Ask any question about the PDF..")

    def user_query(user_input):
        response = st.session_state.conversation({'question': user_input})
        st.session_state.chatHistory = response['chat_history']
        for i, message in enumerate(st.session_state.chatHistory):
            if i % 2 == 0:
                st.write("User:", message.content)
            else:
                st.write("Reply:",message.content)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    if user_input:
        user_query(user_input)
    
    with st.sidebar:
        st.title("Menu")
        pdf_data = st.file_uploader("Upload PDF", type=["pdf"])
        
        
        if st.button("Submit & Process"):
           with st.spinner("Processing..."):
                
                text = get_pdf_data(pdf_data)
                chunks = get_split_chunks(text)
                embeddings = get_embeddings(chunks)
                st.session_state.conversation = get_conversation_chain(embeddings)
                
                st.success("Done!")


if __name__ == "__main__":
    main()