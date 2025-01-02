import os
import json
import aiohttp
import asyncio
from dotenv import load_dotenv

load_dotenv()

# Using a smaller, faster model
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"}

async def get_ai_response(question: str) -> str:
    max_retries = 3
    retry_delay = 5  # seconds

    for attempt in range(max_retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(API_URL, headers=headers, json={
                    "inputs": question,
                    "parameters": {
                        "max_length": 100,
                        "temperature": 0.7
                    }
                }) as response:
                    if response.status == 503:  # Model is loading
                        error_data = await response.json()
                        estimated_time = error_data.get("estimated_time", retry_delay)
                        print(f"Model is loading, waiting {estimated_time} seconds...")
                        await asyncio.sleep(min(estimated_time, retry_delay))
                        continue

                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"API request failed: {error_text}")
                    
                    result = await response.json()
                    return result.get("generated_text", "I'm sorry, I couldn't generate a response.")

        except Exception as e:
            if attempt == max_retries - 1:  # Last attempt
                print(f"Failed after {max_retries} attempts: {str(e)}")
                raise
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            await asyncio.sleep(retry_delay)

    raise Exception("Failed to get response after multiple attempts") 