import csv
from io import StringIO

REQUIRED_COLUMNS = [
    "month",
    "revenue",
    "expenses",
    "cash_balance",
    "debtors",
    "creditors",
    "gst_payable",
]


def clean_number(value: str) -> int:
    """Remove commas/spaces and convert to int."""
    return int(value.replace(",", "").strip())


def parse_csv(file_content: str):
    """
    Validate columns and convert CSV text into list of dicts
    with proper integer values.
    """
    reader = csv.DictReader(StringIO(file_content))

    # Check required columns
    if not all(col in reader.fieldnames for col in REQUIRED_COLUMNS):
        missing = set(REQUIRED_COLUMNS) - set(reader.fieldnames)
        raise ValueError(f"Missing columns: {missing}")

    data = []

    for row in reader:
        parsed_row = {
            "month": row["month"],
            "revenue": clean_number(row["revenue"]),
            "expenses": clean_number(row["expenses"]),
            "cash_balance": clean_number(row["cash_balance"]),
            "debtors": clean_number(row["debtors"]),
            "creditors": clean_number(row["creditors"]),
            "gst_payable": clean_number(row["gst_payable"]),
        }
        data.append(parsed_row)

    return data


def calculate_metrics(data: list):
    """
    Calculate:
    - Gross margin %
    - Cash runway (days)
    - Working capital
    """
    avg_expenses = sum(d["expenses"] for d in data) / len(data)
    latest = data[-1]

    gross_margin = (
        (latest["revenue"] - latest["expenses"]) / latest["revenue"]
    ) * 100

    cash_runway_days = (latest["cash_balance"] / avg_expenses) * 30

    working_capital = latest["debtors"] - latest["creditors"]

    return round(gross_margin, 2), int(cash_runway_days), working_capital

def analyze_data(data: list):
    """
    Perform financial analysis required for /analysis endpoint.
    """
    highest_rev = max(data, key=lambda x: x["revenue"])
    lowest_cash = min(data, key=lambda x: x["cash_balance"])

    avg_debtors = sum(d["debtors"] for d in data) / len(data)
    avg_creditors = sum(d["creditors"] for d in data) / len(data)
    avg_revenue = sum(d["revenue"] for d in data) / len(data)
    avg_expenses = sum(d["expenses"] for d in data) / len(data)

    dio = (avg_debtors / avg_revenue) * 30
    dso = (avg_debtors / avg_revenue) * 30
    dpo = (avg_creditors / avg_expenses) * 30

    ccc = round(dio + dso - dpo, 2)

    risk_months = [
        d["month"]
        for d in data
        if d["cash_balance"] < 0.2 * d["revenue"]
    ]

    return {
        "highest_revenue_month": highest_rev["month"],
        "lowest_cash_month": lowest_cash["month"],
        "cash_conversion_cycle": ccc,
        "cash_risk_months": risk_months,
    }

def ccc_trend(data: list):
    """
    Calculate CCC for each month and detect trend.
    """
    ccc_values = []

    for d in data:
        dio = (d["debtors"] / d["revenue"]) * 30
        dso = (d["debtors"] / d["revenue"]) * 30
        dpo = (d["creditors"] / d["expenses"]) * 30

        ccc = round(dio + dso - dpo, 2)

        ccc_values.append({
            "month": d["month"],
            "ccc": ccc
        })

    if len(ccc_values) < 3:
        return {"message": "Not enough data for trend"}

    last_three = [v["ccc"] for v in ccc_values[-3:]]

    if last_three[0] > last_three[1] > last_three[2]:
        trend = "improving"
    elif last_three[0] < last_three[1] < last_three[2]:
        trend = "worsening"
    else:
        trend = "stable"

    return {
        "ccc_by_month": ccc_values,
        "trend": trend
    }

from typing import List, Dict

def calculate_ccc_trend(rows: List[Dict]):
    if len(rows) < 3:
        raise ValueError("At least 3 months data required for CCC trend")

    ccc_by_month = []

    for r in rows:
        dio = (r["debtors"] / r["revenue"]) * 30
        dso = dio
        dpo = (r["creditors"] / r["expenses"]) * 30
        ccc = round(dio + dso - dpo, 2)

        ccc_by_month.append({
            "month": r["month"],
            "ccc": ccc
        })

    last = [x["ccc"] for x in ccc_by_month[-3:]]

    diff1 = last[1] - last[0]
    diff2 = last[2] - last[1]
    tol = 0.01

    if diff1 < -tol and diff2 < -tol:
        trend = "improving"
    elif diff1 > tol and diff2 > tol:
        trend = "worsening"
    else:
        trend = "stable"

    return {
        "ccc_by_month": ccc_by_month,
        "trend": trend
    }