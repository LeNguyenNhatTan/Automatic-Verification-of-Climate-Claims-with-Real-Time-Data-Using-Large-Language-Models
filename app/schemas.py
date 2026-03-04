from pydantic import BaseModel

class ClaimRequest(BaseModel):
    claim: str

class ClaimResponse(BaseModel):
    statement: str
    final_verdict: str
    confidence: str
    risk_level: str
    debate_rounds: int
    latency_ms: float