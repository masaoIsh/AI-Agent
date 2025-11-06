from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Literal, Optional
import asyncio

from interactive_cli import InteractiveFinancialInterface


class SectorAnalysisRequest(BaseModel):
    symbols: List[str] = Field(..., description="List of tickers in the same sector")
    start: str = Field(..., description="YYYY-MM-DD")
    end: str = Field(..., description="YYYY-MM-DD")
    strategy: Literal["equal", "invvol", "mpt"] = "mpt"
    rebalance: Literal["D", "W", "M", "Q"] = "M"
    use_oos: bool = True


app = FastAPI(title="AI Sector Portfolio API", version="1.0.0")

# Add CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your Vercel domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/sector-analysis")
async def sector_analysis(req: SectorAnalysisRequest):
    iface = InteractiveFinancialInterface()
    try:
        result = await iface.run_sector_portfolio_analysis_api(
            symbols=[s.upper().strip() for s in req.symbols if s and s.strip()],
            start=req.start,
            end=req.end,
            strategy=req.strategy,
            freq=req.rebalance,
            use_oos=req.use_oos,
        )
        if not result or result.get("status") not in ("ok",):
            raise HTTPException(status_code=400, detail=result)
        return result
    finally:
        await iface.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=True)


