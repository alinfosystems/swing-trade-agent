#from langchain.chat_models import ChatOpenAI
#from langchain_community.chat_models import ChatOpenAI
# NEW
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.config import settings

from app.agent.stock_fetcher import get_stock_summary
from app.agent.sentiment_analysis import get_stock_sentiment



# Initialize LLM
llm = ChatOpenAI(
    temperature=0.5,
    model="gpt-3.5-turbo",
    openai_api_key=settings.OPENAI_API_KEY
)

# Define prompt template
template = """
You're a financial swing trading analyst. Given the following stocks and their basic info,
suggest the best one to swing trade over the next 7 days.

For the best one, also give:
1. Entry (buy) price range
2. Exit (sell) price range
3. Risk level (Low, Medium, High)
4. 2-line company description
5. Reason for your suggestion

Stocks:
{stock_data}
"""

prompt = ChatPromptTemplate.from_template(template)

# Dummy stock data (replace with live later)
#sample_data = """
#1. TCS - CMP: ₹3650, 7d Change: +3.2%
#2. Infosys - CMP: ₹1420, 7d Change: -1.4%
#3. Reliance - CMP: ₹2750, 7d Change: +1.8%
#4. HDFC Bank - CMP: ₹1570, 7d Change: -0.8%
#"""

#tickers = ["TCS.NS", "INFY.NS", "RELIANCE.NS", "HDFCBANK.NS"]
#sample_data = get_stock_summary(tickers)

tickers = ["TCS.NS", "INFY.NS", "RELIANCE.NS", "HDFCBANK.NS"]
formatted_lines = []

for ticker in tickers:
    summary = get_stock_summary([ticker])
    risk = get_stock_sentiment(ticker)
    formatted_lines.append(f"{summary} | Risk: {risk}")

sample_data = "\n".join(formatted_lines)


def suggest_swing_trade():
    filled_prompt = prompt.format_messages(stock_data=sample_data)
    response = llm.invoke(filled_prompt)
    return {"result": response.content}
