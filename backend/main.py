from fastapi import FastAPI
import json
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # autorise toutes les origines
    allow_methods=["*"],
    allow_headers=["*"]
)
@app.get("/actions")
def get_actions():
    with open("data/mock_actions.json") as f:
        return json.load(f)
