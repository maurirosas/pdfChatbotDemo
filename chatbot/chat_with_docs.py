import os

from langchain.chains import ConversationalRetrievalChain
from langchain.chains.base import Chain
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.schema import BaseRetriever
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import DocArrayInMemorySearch

from .utils import load_document, MEMORY

open_ai_api_key = "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"

#Specify Model
LLM = ChatOpenAI(
    model_name="gpt-3.5-turbo",temperature=0,streaming=True,
    openai_api_key = open_ai_api_key
)

#Split text into chunks
def configure_retriever(docs):
    #First modification: Adjusting chunk size and chunk overlap
        # Previous value: 1000, 200 -> Gives shorter answers
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
    splits = text_splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(openai_api_key=open_ai_api_key)

    vectordb = DocArrayInMemorySearch.from_documents(splits,embeddings)

    retriever = vectordb.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k":5,
            "fetch_k":7,
            "include_metadata":True
        }
    )
    return retriever

#Chain params
def configure_chain(retriever):
    params = dict(
        llm = LLM,
        retriever = retriever,
        memory = MEMORY,
        verbose = True,
        max_tokens_limit=4000
    )
    return ConversationalRetrievalChain.from_llm(**params)

#Store the doc
def configure_retrieval_chain(pdf_file):
    if not pdf_file.endswith(".pdf"):
        raise ValueError("File is not a PDF.")
    
    docs = load_document(pdf_file)
    retriever = configure_retriever(docs)
    chain = configure_chain(retriever)

    return chain