#Importing the necessary Packages:
import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI


#Setting up API key and choosing a LLM
os.environ["GOOGLE_API_KEY"] = "AI-..YourAPI"
llm = ChatGoogleGenerativeAI(model="gemini-pro")


#UI using Streamlit:
st.title("Chat with Google Generative AI")
query = st.text_input("Enter a term you'd like to learn about:")
if query:
    result = llm.invoke(query)
    st.text("Chat History:")
    st.write(result.content)
    #Saving the conversation to a .txt file.
    with open("chat_history.txt", "a") as file:
        file.write(f"User: {query}\n")
        file.write(f"AI: {result.content}\n\n")
