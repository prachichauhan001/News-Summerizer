import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults


st.set_page_config(
    page_title="AI News Summarizer",
    page_icon="📰",
    layout="wide"
)

st.title("📰 AI News Summarizer")
st.write("Get the latest AI news summarized into easy-to-read bullet points.")

search_tool = TavilySearchResults(max_results=5)

llm = ChatMistralAI(model="mistral-small-2506")

prompt = ChatPromptTemplate.from_template(
    """
You are a helpful assistant.

Summarize the following news into clear bullet points.

{news}
"""
)

chain = prompt | llm | StrOutputParser()

query = st.text_input(
    "Enter your news topic",
    value="Latest AI news of 2026"
)

if st.button("Get News Summary"):

    with st.spinner("Searching latest news..."):

        news_result = search_tool.run(query)

    with st.spinner("Summarizing..."):

        result = chain.invoke({"news": news_result})

    st.success("Summary Generated!")

    st.subheader("📌 Summary")
    st.write(result)

    with st.expander("📰 Retrieved News"):
        st.write(news_result)