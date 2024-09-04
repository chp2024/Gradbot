import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Print the JWT secret to verify it's loaded
print("JWT Secret:", os.getenv("JWT_SECRET"))
