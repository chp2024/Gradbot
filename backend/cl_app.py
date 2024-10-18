import chainlit as cl
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI  # Update the import
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig

# Load environment variables from history.env file
load_dotenv("history.env")

@cl.on_chat_start
async def on_chat_start():
    model = ChatOpenAI(streaming=True)  # No need to change the usage here
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an AI named Gradbot that helps students create their schedule. You are knowledgeable about different classes.",
            ),
            ("human", "{question}"),
        ]
    )
    runnable = prompt | model | StrOutputParser()
    cl.user_session.set("runnable", runnable)

@cl.on_message
async def on_message(message: cl.Message):
    runnable = cl.user_session.get("runnable")  # Retrieve the Runnable instance

    response = ""  # Initialize an empty string to accumulate the chunks

    # Stream the result chunks
    async for chunk in runnable.astream(
        {"question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        response += chunk  # Accumulate each chunk into the response

    # Send the final full response back to the user
    await cl.Message(
        content=response,
        author="Gradbot"
    ).send()
