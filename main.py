#Importing Packages
import streamlit as st#For UI
from dotenv import load_dotenv#For loading APIkey
from PyPDF2 import PdfReader#To read PDFs
from langchain.text_splitter import CharacterTextSplitter#Splitting the document
from langchain.embeddings import OpenAIEmbeddings#Embedding model
from langchain.vectorstores import FAISS#Vector DB
from langchain.chat_models import ChatOpenAI#Chat Model
from htmlTemplates import css, bot_template, user_template#Custom package for Visual Effects

from langchain.memory import ConversationBufferMemory#To write and retrive the previous chats in that session
from langchain.chains import ConversationalRetrievalChain
import os#To access env variables
import textract#For handling doc and docx files
from docx import Document
# Load OpenAI API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

def extract_text_from_docx(docx_path):
    """
    Extracts text from a Microsoft Word document (.docx).
    """
    doc = Document(docx_path)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text


def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.
    """
    pdf_reader = PdfReader(pdf_path)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text



def extract_text_from_files(file_uploads):
    """
    Extracts text from a list of file uploads, handling PDF and DOCX formats.
    """
    text = ""
    for file_upload in file_uploads:
        file_path = file_upload.name
        if file_path.lower().endswith(('.pdf')):
            text += extract_text_from_pdf(file_upload)
        elif file_path.lower().endswith(('.doc', '.docx')):
            text += extract_text_from_docx(file_upload)
    return text

def get_pdf_text(pdf_docs):
    """
    Gets text from PDF documents.
    """
    text = extract_text_from_files(pdf_docs)
    return text

def get_text_chunks(text):
    """
    Splits text into chunks for embedding.
    """
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    """
    Creates a vector store from text chunks using OpenAI embeddings.
    """
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    """
    Creates a conversational retrieval chain using OpenAI language model.
    """
    llm = ChatOpenAI()

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_userinput(user_question):
    """
    Handles user input, triggers conversation, and displays chat history.
    """
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:#If true, than it's user message
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)

def main():
    # Load environment variables
    load_dotenv()
    
    # Configure Streamlit page
    st.set_page_config(page_title="Chat with multiple Files", page_icon=":moyai:")

    # Initialize session state variables
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    # Streamlit UI header
    st.header("Chat with multiple Files :speaking_head_in_silhouette::")

    # User input for asking questions
    user_question = st.text_input("Ask a question about your documents:arrow_down::")

    # Process user input and display chat history
    if user_question:
        handle_userinput(user_question)

    # Sidebar for file uploads
    with st.sidebar:
        st.subheader("Your documents")

        # File uploader for  documents
        pdf_docs = st.file_uploader(
            "Upload your Files here and click on 'Process':fire:", accept_multiple_files=True)

        # Button to trigger document processing
        if st.button("Process"):
            with st.spinner("Processing"):
                # Get text from uploaded PDFs
                raw_text = get_pdf_text(pdf_docs)

                # Split text into chunks
                text_chunks = get_text_chunks(raw_text)

                # Create vector store from text chunks
                vectorstore = get_vectorstore(text_chunks)

                # Create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)


if __name__ == '__main__':
    main()