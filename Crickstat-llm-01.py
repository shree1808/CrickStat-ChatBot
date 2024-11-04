import streamlit as st
from langchain_community.llms import Ollama
from langchain_ollama import ChatOllama


ollama_url = "http://localhost:11434/"

llm = ChatOllama(
    base_url = ollama_url,
    model = "llama3.2",
    temperature = 0.8,
    num_predict = 256,
    stream = False
)

messages = [
    ("system", "Act as my Buddy"),
    ("human", "How are you doing today?"),
]

response = llm.invoke(messages)

response.content