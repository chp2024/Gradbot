from pathlib import Path

import chainlit as cl
import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig
from langchain_community.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.callbacks.base import BaseCallbackHandler
from langchain.indexes import SQLRecordManager, index
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough, RunnableConfig
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Load environment variables
load_dotenv(".env")

model = ChatOpenAI(model="gpt-4", streaming=True)
embeddings = OpenAIEmbeddings()

def process_pdf(directory):
    p = Path(directory)
    docs = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    for pdf in p.glob("*.pdf"):
        loader = PyMuPDFLoader(str(pdf))
        content = loader.load()
        docs += splitter.split_documents(content)

    store = Chroma.from_documents(docs, embeddings)
    ns = "chromadb/docs"
    record_manager = SQLRecordManager(ns, db_url="sqlite:///cache.db")
    record_manager.create_schema()

    result = index(
        docs, record_manager, store, cleanup="incremental", source_id_key="source"
    )

    print("Indexing Stats")
    print("--------------")
    print(result)
    print(store)
    return docs, store  # Return docs first, then store

documents, store = process_pdf("pdfs")

# Authentication callback function
@cl.password_auth_callback
def auth_callback(username: str, password: str):
    if (username, password) == ("admin", "admin"):
        return cl.User(
            identifier="admin", metadata={"role": "admin", "provider": "credentials"}
        )
    return None

documents, store = process_pdf("pdfs")

@cl.on_chat_start
async def on_chat_start():
    # Initialize model
    model = ChatOpenAI(streaming=True)
    
    template =         [
            (
                "system",
                "You're a very knowledgeable assistance on Howard University graduation requirements who provides accurate and eloquent answers to questions.",
            ),
            ("human", "{question}"),
        ]
    
    prompt = ChatPromptTemplate.from_messages(template)
    retriever = store.as_retriever()  # Use the store as the retriever

        # Debugging output to verify documents
    print("Documents loaded:", documents)
    context_runnable = retriever

    runnable = (
        context_runnable
        | prompt
        | model
        | StrOutputParser()
    )
   
    # Store runnable and documents in user session
    cl.user_session.set("runnable", runnable)
    cl.user_session.set("docs", documents)  # Store docs here


@cl.on_message
async def on_message(message: cl.Message):
    runnable = cl.user_session.get("runnable")  # type: Runnable

    # Initialize an empty message to collect response chunks
    msg = cl.Message(content="")

    # Stream the response from the runnable
    async for chunk in runnable.astream(
        message.content,  # Pass the complete input string
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        # Append each chunk to the message content
        msg.content += chunk

    # Send the full response back to the user
    await msg.send()
