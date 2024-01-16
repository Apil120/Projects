import os
import gradio as gr
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.llms import OpenAI
import pinecone

os.environ['OPENAI_API_KEY'] = "sk-...yourAPI"

pdf_loader = DirectoryLoader('path to your file contains the PDFs', glob="**/*.pdf")
loaders = [pdf_loader]

documents = []
for loader in loaders:
    documents.extend(loader.load())

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=40)
documents = text_splitter.split_documents(documents)

# Creating embeddings
embeddings = OpenAIEmbeddings()

# Initializing Pinecone with the correct API key and environment
pinecone.init(api_key='PineconeAPI', environment='PineconeENV')
index_name = "chatbot-application"

# Create vector store using Pinecone
vectorstore = Pinecone.from_documents(documents, embeddings, index_name=index_name)

# Set up QA chain
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 2})

# Initialize the OpenAI language model
openai_model = ChatOpenAI(api_key="sk-..YourAPI")

# Create the conversational retrieval chain
qa = ConversationalRetrievalChain.from_llm(openai_model, retriever)

# Gradio chat UI
chat_history = []

def chat_interface(user_input):
    global chat_history
    result = qa({"question": user_input, "chat_history": chat_history})
    chat_history.append((user_input, result['answer']))
    return result['answer']

iface = gr.Interface(
    fn=chat_interface,
    inputs="text",
    outputs="text",
    live=False
)
iface.launch(share=True)
