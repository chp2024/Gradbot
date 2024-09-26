import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

import chainlit as cl

# Load environment variables from history.env file
load_dotenv("history.env")


client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Authentication callback function
# @cl.password_auth_callback
# def auth_callback(username: str, password: str):
#     if (username, password) == ("admin", "admin"):
#         return cl.User(identifier="admin", metadata={"role": "admin", "provider": "credentials"})
#     else:
#         return None

# @cl.on_chat_start
# async def on_chat_start():
#     app_user = cl.user_session.get("user")
#     await cl.Message(f"Hello {app_user.identifier}").send()

# Main message handling function
@cl.on_message
async def main(message: cl.Message):
    user_input = message.content.lower()

    responses = {
        "hello": "Hi Cameron",
        "what is my classification?": "You are a Senior!",
        "how many credits do i have?": "You have 90 credits!",
        "what semester is this?": "It is currently the Spring 2024 semester!",
        "what classes am i taking this semester?": "You are taking: \n \n Senior Project I \n Database Systems \n Structures of a programming language \n Intro to Machine Learning \n Technical Writing",
        "what classes should i take next semester?": "Currently, you have it set to no more than 18 credits a semester. With that in mind the courses you should take are: \n \n Senior Project II \n Large Scale Programming \n Applied Data Science \n Technical Elective"
    }

    response = responses.get(user_input, "Sorry, I didn't understand that.")

    if user_input == "what is my API key?":
        api_key = os.getenv("LITERAL_API_KEY")
        if api_key:
            response = f"Your API key is: {api_key}"
        else:
            response = "Sorry, I couldn't find your API key."

    # Send the response back to the user
    await cl.Message(
        content=response,
        author="Gradbot",
    ).send()
