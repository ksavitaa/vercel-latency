from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import json
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # allow all websites
    allow_credentials=True,
    allow_methods=["*"],        # allow POST, GET, etc.
    allow_headers=["*"],        # allow any headers
)
@app.post("/analytics")
async def analytics(request: Request):
    body = await request.json()
    regions = body["regions"]
    threshold = body["threshold_ms"]

    # Load telemetry data
    with open("q-vercel-latency.json") as f:
        data = json.load(f)

    results = {}
    for region in regions:
        latencies = [d["latency_ms"] for d in data if d["region"] == region]
        uptimes = [d["uptime"] for d in data if d["region"] == region]

        avg_latency = float(np.mean(latencies))
        p95_latency = float(np.percentile(latencies, 95))
        avg_uptime = float(np.mean(uptimes))
        breaches = sum(1 for l in latencies if l > threshold)

        results[region] = {
            "avg_latency": avg_latency,
            "p95_latency": p95_latency,
            "avg_uptime": avg_uptime,
            "breaches": breaches,
        }

    return results
