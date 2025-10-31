import os
import asyncio
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")
genai.configure(api_key=GEMINI_API_KEY)

async def get_wellness_plan(prompt: str, timeout: int = 120) -> str:
    """Calls the Gemini API to generate the wellness plan."""
    try:
        model = genai.GenerativeModel('gemini-pro-latest')
        # Create a partial function for the blocking call
        blocking_call = asyncio.to_thread(model.generate_content, prompt)
        # Run the blocking call with a timeout
        response = await asyncio.wait_for(blocking_call, timeout=timeout)
        # Clean up the response to get raw JSON
        raw_json = response.text.strip().replace("```json", "").replace("```", "")
        return raw_json
    except asyncio.TimeoutError:
        print("API call timed out.")
        return None
    except Exception as e:
        print(f"An error occurred during API call: {e}")
        return None
