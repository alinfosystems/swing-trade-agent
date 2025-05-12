from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.agent.strategy_chain import suggest_swing_trade
from app.utils.formatter import save_response
from app.utils.formatter import list_saved_suggestions


app = FastAPI(title="Swing Trade AI Agent")

# CORS settings (you can tighten this in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Swing Trade AI Agent is running."}

@app.get("/suggest_old")
def get_suggestion():
    result = suggest_swing_trade()
    return result

@app.get("/suggest")
def get_suggestion():
    result = suggest_swing_trade()
    save_response(result["result"])
    return result

@app.get("/history")
def get_all_suggestions():
    return list_saved_suggestions()
