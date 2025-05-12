from transformers import pipeline
from huggingface_hub import login
import requests
from bs4 import BeautifulSoup

from app.config import settings

# Login to HuggingFace (if needed)
login(token=settings.HUGGINGFACE_API_TOKEN)

# Load sentiment analysis pipeline
#sentiment = pipeline("sentiment-analysis")

sentiment = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)


# # Dummy stock-specific headlines (can replace with scraped headlines later)
# stock_news = {
#     "TCS.NS": ["TCS launches new AI platform for BFSI", "Strong Q4 results beat expectations"],
#     "INFY.NS": ["Infosys sees margin pressure", "Client attrition rises in North America"],
#     "RELIANCE.NS": ["Reliance Retail expands aggressively", "Jio shows stable ARPU"],
#     "HDFCBANK.NS": ["HDFC Bank maintains steady NIMs", "HDFC merger impact unclear"]
# }


# def get_stock_sentiment(symbol):
#     headlines = stock_news.get(symbol, [])
#     if not headlines:
#         return "Unknown"

#     results = sentiment(headlines)
#     score = sum(1 if r['label'] == 'POSITIVE' else -1 for r in results)

#     if score >= 2:
#         return "Low"
#     elif score >= 0:
#         return "Medium"
#     else:
#         return "High"



def fetch_news_headlines(query: str, limit=5):
    url = f"https://news.google.com/search?q={query}+stock&hl=en-IN&gl=IN&ceid=IN:en"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    headlines = []

    for article in soup.select("article h3")[:limit]:
        title = article.get_text(strip=True)
        headlines.append(title)

    return headlines

def get_stock_sentiment(symbol):
    name_map = {
        "TCS.NS": "TCS",
        "INFY.NS": "Infosys",
        "RELIANCE.NS": "Reliance Industries",
        "HDFCBANK.NS": "HDFC Bank"
    }

    query = name_map.get(symbol, symbol)
    headlines = fetch_news_headlines(query)

    if not headlines:
        return "Unknown"

    results = sentiment(headlines)
    score = sum(1 if r['label'] == 'POSITIVE' else -1 for r in results)

    if score >= 2:
        return "Low"
    elif score >= 0:
        return "Medium"
    else:
        return "High"
