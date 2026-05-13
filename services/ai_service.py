
import os
import requests

from dotenv import load_dotenv

from services.csv_parser import (
    calculate_metrics,
    analyze_data,
)

load_dotenv()


def generate_financial_insights(data):

    api_key = os.getenv(
        "OPENROUTER_API_KEY"
    )

    if not api_key:
        raise Exception(
            "OPENROUTER_API_KEY not configured"
        )

    latest = data[-1]

    margin, runway, wc = calculate_metrics(data)

    analysis = analyze_data(data)

    risk_months = ", ".join(
        analysis["cash_risk_months"]
    )

    prompt = f"""
You are MecTURING, a virtual finance analyser for Indian small businesses.

You analyse financial data and give clear actionable advice.

Reply in English first and then Hindi.

Latest month revenue: {latest["revenue"]}

Cash balance: {latest["cash_balance"]}

Cash runway: {runway} days

Gross margin: {margin}%

Total debtors outstanding: {latest["debtors"]}

GST payable: {latest["gst_payable"]}

Cash risk months identified: {risk_months}
"""

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",

        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },

        json={
            "model": "openai/gpt-3.5-turbo",

            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    )

    result = response.json()

    return {
        "insight":
        result["choices"][0]["message"]["content"],

        "model_used":
        "openai/gpt-3.5-turbo"
    }




