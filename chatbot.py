import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
os.environ["GOOGLE_API_KEY"] = "AIzaSyA5_a3BnFaFRxLb4CvIqP446NvYtNyyCwo"
llm = ChatGoogleGenerativeAI(model="gemini-pro")
st.title("Chat with Google Generative AI")
query = st.text_input("Enter a term you'd like to learn about:")
if query:
    result = llm.invoke(query)
    st.text("Chat History:")
    st.write(result.content)
    with open("chat_history.txt", "a") as file:
        file.write(f"User: {query}\n")
        file.write(f"AI: {result.content}\n\n")