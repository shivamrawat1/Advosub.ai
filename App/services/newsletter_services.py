from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)


def generate_newsletter(news_results):
    """
    Generates an engaging newsletter from Perplexity API search results on animal rights advocacy.
    :param news_results: List of dictionaries containing search results with 'title', 'link', 'date', and 'summary'.
    :return: A formatted newsletter string.
    """
    
    # Format the news results into a structured prompt
    prompt = """
    Create an engaging, easy-to-read newsletter summarizing the latest updates on animal rights advocacy. 
    The newsletter should be concise, around a 2-minute read, with categorized sections:
    - **TL;DR**: A short, bullet-point summary of key takeaways.
    - **Legislation Updates**: Recent laws and policies affecting animal rights.
    - **Industry News**: Corporate and industry-related changes regarding animal welfare.
    - **Activism Highlights**: Grassroots movements, protests, and advocacy campaigns making an impact.
    - **Ways to Take Action**: How readers can contribute, sign petitions, or engage in advocacy.
    
    Here are the latest search results:
    """
    
    for news in news_results:
        prompt += f"\n- **{news['title']}** ({news['date']})\n  {news['summary']}\n  [Read more]({news['link']})"
    
    prompt += "\nNow, craft a compelling and structured newsletter following the above format. Make sure that each section is concise yet comprehensive and relevant. Do not fabricate events or facts beyond given news."
    
    # Use OpenAI API to generate the newsletter
    completion = client. chat. completions.create(
        model="gpt-4o-mini",
        messages =[{"role": "system", "content": "You are an expert newsletter writer. You have to inform readers about the latest updates concisely and comprehensively."},
                  {"role": "user", "content": prompt}]
    )
    
    return completion.choices[0].message

