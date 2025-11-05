from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Literal, Optional

from interactive_cli import InteractiveFinancialInterface


class RunRequest(BaseModel):
    symbols: List[str] = Field(..., description="Exactly 10 tickers preferred")
    start: Optional[str] = Field(None, description="YYYY-MM-DD")
    end: Optional[str] = Field(None, description="YYYY-MM-DD")
    strategy: Literal["equal", "invvol", "mpt"] = "mpt"
    rebalance: Literal["D", "W", "M", "Q"] = "M"
    use_oos: bool = True


app = FastAPI(title="AI Sector Portfolio API", version="1.0.0")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/sector-analysis")
async def sector_analysis(req: RunRequest):
    symbols = [s.upper().strip() for s in req.symbols if s and s.strip()]
    if len(symbols) < 2:
        raise HTTPException(status_code=400, detail={"error": "Provide at least 2 symbols"})

    iface = InteractiveFinancialInterface()
    try:
        result = await iface.run_sector_portfolio_analysis_api(
            symbols=symbols,
            start=req.start or "",
            end=req.end or "",
            strategy=req.strategy,
            freq=req.rebalance,
            use_oos=req.use_oos,
        )
        if not result or result.get("status") not in ("ok",):
            raise HTTPException(status_code=400, detail=result)
        return result
    finally:
        await iface.close()


