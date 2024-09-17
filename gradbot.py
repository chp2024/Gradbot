import chainlit as cl
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings

# Load environment variables
load_dotenv(".env")

# Load and split documents
loader = PyPDFLoader("handbook.pdf")
docs = loader.load_and_split()

# Authentication callback function
@cl.password_auth_callback
def auth_callback(username: str, password: str):
    if (username, password) == ("admin", "admin"):
        return cl.User(
            identifier="admin", metadata={"role": "admin", "provider": "credentials"}
        )
    return None

@cl.on_chat_start
async def on_chat_start():
    # Initialize model
    model = ChatOpenAI(streaming=True)
    
    # Create prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You're a very knowledgeable historian who provides accurate and eloquent answers to historical questions.",
            ),
            ("human", "{question}"),
        ]
    )
    
    # Define runnable
    runnable = prompt | model | StrOutputParser()
    
    # Store runnable in user session
    cl.user_session.set("runnable", runnable)

@cl.on_message
async def on_message(message: cl.Message):
    runnable = cl.user_session.get("runnable")  # type: Runnable

    # Initialize an empty message to collect response chunks
    msg = cl.Message(content="")

    # Stream the response from the runnable
    async for chunk in runnable.astream(
        {"question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        # Append each chunk to the message content
        msg.content += chunk

    # Send the full response back to the user
    await msg.send()
