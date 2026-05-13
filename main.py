from fastapi import FastAPI, UploadFile, HTTPException
from models import UploadResponse

from services.csv_parser import (
    parse_csv,
    calculate_metrics,
    analyze_data,
    calculate_ccc_trend,
)

from services.tally_parser import parse_tally_xml
from services.ai_service import generate_financial_insights


app = FastAPI(
    title="MecTURING Finance API",
    version="1.0.0",
    description="CSV analysis, CCC trend, Tally parsing and AI insights"
)

# In-memory storage (as required)
stored_data = []


@app.post("/upload-csv", response_model=UploadResponse)
async def upload_csv(file: UploadFile):
    """
    Upload CSV, validate, parse and calculate key metrics.
    """
    global stored_data

    content = await file.read()

    try:
        parsed_rows = parse_csv(content.decode())
        stored_data = parsed_rows

        margin, runway, wc = calculate_metrics(parsed_rows)

        return {
            "data": parsed_rows,
            "gross_margin_pct": margin,
            "cash_runway_days": runway,
            "working_capital": wc,
        }

    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.get("/analysis")
def get_analysis():
    """
    Return financial analysis from last uploaded CSV.
    """
    if not stored_data:
        raise HTTPException(status_code=400, detail="No data uploaded yet")

    return analyze_data(stored_data)


@app.get("/ccc-trend")
def get_ccc_trend():
    """
    Return CCC per month and trend (requires >= 3 months).
    """
    if not stored_data:
        raise HTTPException(status_code=400, detail="No data uploaded yet")

    try:
        return calculate_ccc_trend(stored_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "ok",
        "service": "mct-fo-api",
        "version": "1.0.0",
    }


@app.post("/ai-insight")
def ai_insight():
    """
    Generate AI financial insights from last uploaded CSV.
    """
    if not stored_data:
        raise HTTPException(status_code=400, detail="No data uploaded yet")

    try:
        return generate_financial_insights(stored_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/parse-tally")
async def parse_tally(file: UploadFile):
    """
    Parse uploaded Tally XML file and return structured JSON.
    """
    content = await file.read()

    try:
        return parse_tally_xml(content.decode("utf-8-sig"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))