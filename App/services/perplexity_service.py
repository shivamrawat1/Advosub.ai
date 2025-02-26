import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Access the API key from the environment
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")


interest = "animal rights advocacy"
messages = [
        {
            "role": "system",
            "content": (
                """
                You are an AI agent tasked with giving the top 10 most recent news articles (from the last month) related to the interest shared with you.

                NOTE:
                - Include the title of the article.
                - Include the date of the article.
                - Include a link to the article (should be an actual link in https format).
                - Include a summary of the article.
                - Your output should be in the form of a single dictionary, where dictionary contains the title, date, link, and summary of the article.
                """
            ),
        },
        {
            "role": "user",
            "content": f"Latest News on {interest}",
        },
    ]

# Initialize the OpenAI client
client = OpenAI(api_key=PERPLEXITY_API_KEY, base_url="https://api.perplexity.ai")

# chat completion without streaming
response = client.chat.completions.create(
    model="llama-3.1-sonar-large-128k-online",
    messages=messages,
)
print(response.choices[0].message.content)