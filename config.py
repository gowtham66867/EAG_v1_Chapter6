import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access your API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Maximum number of iterations for the agent
MAX_ITERATIONS = 3
