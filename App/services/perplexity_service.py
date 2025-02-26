import os
from dotenv import load_dotenv
from openai import OpenAI
import json

# Load environment variables from .env file
load_dotenv()

# Access the API key from the environment
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

def get_news_for_topic(interest):
    """
    Get the latest news articles for a specific interest/topic
    
    Args:
        interest (str): The topic to search for news about
        
    Returns:
        list: A list of dictionaries containing news article information
    """
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
                - Your output should be in the form of a list of dictionaries, where each dictionary contains the title, date, link, and summary of the article.
                - Format your response as valid JSON that can be parsed.
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
    
    response_content = response.choices[0].message.content
    
    # Try to parse the JSON response
    try:
        # Find JSON in the response (in case there's text before or after)
        start_idx = response_content.find('[')
        end_idx = response_content.rfind(']') + 1
        
        if start_idx >= 0 and end_idx > start_idx:
            json_str = response_content[start_idx:end_idx]
            news_results = json.loads(json_str)
            return news_results
        else:
            # If we can't find JSON brackets, try parsing the whole response
            news_results = json.loads(response_content)
            return news_results
    except json.JSONDecodeError:
        # If parsing fails, create a fallback response
        print("Failed to parse JSON response from Perplexity API")
        print("Raw response:", response_content)
        
        # Return a fallback response
        return [
            {
                "title": f"Latest Updates on {interest}",
                "date": "Current",
                "link": "https://example.com",
                "summary": f"We're gathering the latest information on {interest}. Check back soon for updates."
            }
        ]