#!/usr/bin/env python3

from pathlib import Path
from langchain.callbacks.base import BaseCallbackHandler
from langchain.indexes import SQLRecordManager, index
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough, RunnableConfig
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import chainlit as cl
import os
from dotenv import load_dotenv

# Load environment variables from the `history.env` file explicitly
load_dotenv('history.env')

# Verify that the API key is loaded correctly
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment. Make sure it is set correctly in history.env.")

# Model setup with OpenAI API key from environment variables
model = ChatOpenAI(model="gpt-4", streaming=True, openai_api_key=api_key)
embeddings = OpenAIEmbeddings()

# Function to process a single PDF
def process_single_pdf(file_path):
    p = Path(file_path)

    # Check if the file exists and is a valid PDF
    if not p.is_file() or p.suffix != ".pdf":
        raise ValueError(f"The file {file_path} is not a valid PDF.")

    docs = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    try:
        print(f"Processing file: {p}")
        loader = PyMuPDFLoader(str(p))
        content = loader.load()
        docs += splitter.split_documents(content)
    except Exception as e:
        raise ValueError(f"Failed to process {file_path}: {e}")

    if not docs:
        raise ValueError(f"No valid content found in {file_path}.")

    # Create a Chroma vector store and store the processed documents
    store = Chroma.from_documents(docs, embeddings)
    ns = "chromadb/docs"
    record_manager = SQLRecordManager(ns, db_url="sqlite:///cache.db")
    record_manager.create_schema()

    # Index the documents for retrieval
    result = index(
        docs, record_manager, store, cleanup="incremental", source_id_key="source"
    )
    print("Indexing Stats")
    print("--------------")
    print(result)

    return store

# Function to format documents into a readable string
def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])

# Process the single PDF
pdf_path = "/Users/cam/Downloads/handbook.pdf"  # Update with your PDF path
documents = process_single_pdf(pdf_path)

# On chat start, initialize the retriever and runnable chain
@cl.on_chat_start
async def on_chat_start():
    # Define the template for question answering based on context
    template = """Answer the question based only on the following context:
    {context}
    Question: {question}"""
    prompt = ChatPromptTemplate.from_template(template)

    # Initialize the retriever from the processed documents
    retriever = documents.as_retriever()

    # Create a runnable chain: retrieve context, use model, and parse output
    runnable = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | model
        | StrOutputParser()
    )

    # Save the runnable chain in the user session
    cl.user_session.set("runnable", runnable)

# On message, process the user's input and stream a response
@cl.on_message
async def on_message(message):
    msg = cl.Message(content="")
    runnable = cl.user_session.get("runnable")
    assert runnable is not None

    # Callback handler to track and show sources
    class PostMessageHandler(BaseCallbackHandler):
        def __init__(self, msg):
            super().__init__()
            self.msg = msg
            self.sources = set()

        # Track documents retrieved by the AI
        def on_retriever_end(self, documents, *, run_id, parent_run_id, **kwargs):
            _ = run_id, parent_run_id, kwargs
            for doc in documents:
                self.sources.add((doc.metadata["source"], doc.metadata.get("page", "unknown")))

        # Track model's response and append sources
        def on_llm_end(self, response, *, run_id, parent_run_id, **kwargs):
            _ = response, run_id, parent_run_id, kwargs
            if self.sources:
                content = "\n".join(
                    [f"{source} - Page {page}" for source, page in self.sources]
                )
                self.msg.elements.append(
                    cl.Text(name="Sources", content=content, display="inline")
                )

    # Stream response to the user
    async for chunk in runnable.astream(
        message.content,
        config=RunnableConfig(
            callbacks=[cl.LangchainCallbackHandler(), PostMessageHandler(msg)]
        ),
    ):
        await msg.stream_token(chunk)

    # Send the final message
    await msg.send()
