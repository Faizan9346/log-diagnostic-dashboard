from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from parser import parse_logs
from rule_engine import analyze_with_rules
from aggregator import aggregate_results
from ai_engine import analyze_with_ai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LogRequest(BaseModel):
    logs: str

@app.get("/")
def home():
    return {"message": "Backend running"}

@app.post("/analyze")
def analyze(request: LogRequest):
    parsed_logs = parse_logs(request.logs)

    rule_results = analyze_with_rules(parsed_logs)

    final_result = aggregate_results(rule_results)

    ai_suggestion = analyze_with_ai(request.logs, final_result)

    return {
        "summary": {
            "total_lines": len(parsed_logs),
            "matched_issues": final_result.get("total_matches", 0)
        },
        "final_result": final_result,
        "ai_suggestion": ai_suggestion
    }