import chainlit as cl
import os
from dotenv import load_dotenv

# Load environment variables from history.env file
load_dotenv("history.env")

# Authentication callback function
@cl.password_auth_callback
def auth_callback(username: str, password: str):
    # Verify the credentials against your authentication service or database
    if (username, password) == ("admin", "admin"):
        # If credentials match, return a User object with appropriate metadata
        return cl.User(
            identifier="admin", metadata={"role": "admin", "provider": "credentials"}
        )
    else:
        # If credentials don't match, return None to fail authentication
        return None
    
@cl.on_chat_start
async def on_chat_start():
    app_user = cl.user_session.get("user")
    await cl.Message(f"Hello {app_user.identifier}").send()


# Main message handling function
@cl.on_message
async def main(message: cl.Message):
    # Get user input
    user_input = message.content.lower()

    # Define responses based on user input
    responses = {
        "hello": "Hi Cameron",
        "what is my classification?": "You are a Senior!",
        "how many credits do i have?": "You have 90 credits!",
        "what semester is this?": "It is currently the Spring 2024 semester!",
        "what classes am i taking this semester?": "You are taking: \n \n Senior Project I \n Database Systems \n Structures of a programming language \n Intro to Machine Learning \n Technical Writing",
        "what classes should i take next semester?": "Currently, you have it set to no more than 18 credits a semester. With that in mind the courses you should take are: \n \n Senior Project II \n Large Scale Programming \n Applied Data Science \n Technical Elective"

    }

    # Check if user input matches any predefined responses
    response = responses.get(user_input, "Sorry, I didn't understand that.")

    # If the user asked for their API key, provide it
    if user_input == "what is my API key?":
        api_key = os.getenv("LITERAL_API_KEY")
        if api_key:
            response = f"Your API key is: {api_key}"
        else:
            response = "Sorry, I couldn't find your API key."

    # Send the response back to the user
    await cl.Message(
        content=response,
    ).send()
