import time

from fastapi import FastAPI
from schemas import ClaimRequest
from agents.truthseeker import truthseekers

app = FastAPI()

@app.post("/verify")
async def verify_claim(request: ClaimRequest):

    start = time.time()

    # result = truthseekers(request.claim)
    result= "Processing..."
    latency = (time.time() - start) * 1000
    # tạm thời bỏ qua phần tính latency để tập trung vào logic chính
    # result["latency_ms"] = round(latency, 2)

    return result