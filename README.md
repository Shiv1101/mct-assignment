# MecTURING Financial Operations API

A FastAPI-based backend assignment project for processing SME financial data.

This project supports:

* CSV financial uploads
* Financial KPI calculations
* Cash Conversion Cycle (CCC) trend analysis
* AI-generated business insights
* Tally XML parsing

---

# Tech Stack

* Python 3.12
* FastAPI
* Uvicorn
* OpenRouter API
* XML Parsing
* CSV Processing

---

# Project Structure

```text
project-folder/
│
├── main.py
├── models.py
├── requirements.txt
├── .env
├── .gitignore
│
├── services/
│   ├── ai_service.py
│   ├── csv_parser.py
│   └── tally_parser.py
│
├── sample_data/
│   ├── sample.csv
│   └── sample_tally.xml
│
└── README.md
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone <your-repo-url>
cd <repo-name>
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 4. Configure Environment Variables

Create a `.env` file in project root.

Example:

```env
OPENROUTER_API_KEY=your_api_key_here
```

---

# 5. Run Application

```bash
uvicorn main:app --reload
```

Server will start at:

```text
http://127.0.0.1:8000
```

Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

---

# API Endpoints

## 1. Health Check

### GET `/health`

Returns API health status.

Example Response:

```json
{
  "status": "ok",
  "service": "mct-fo-api",
  "version": "1.0.0"
}
```

---

## 2. Upload CSV

### POST `/upload-csv`

Uploads SME financial CSV data.

Expected CSV format:

```csv
month,revenue,expenses,cash_balance,debtors,creditors,gst_payable
April 2026,4830000,3960000,1420000,3170000,1840000,257000
```

Returns:

* Gross Margin
* Cash Runway
* Working Capital

---

## 3. Financial Analysis

### GET `/analysis`

Returns:

* Highest revenue month
* Lowest cash month
* Cash risk months
* Financial summary

---

## 4. CCC Trend

### GET `/ccc-trend`

Returns monthly Cash Conversion Cycle trend.

---

## 5. AI Insight

### POST `/ai-insight`

Generates AI-powered financial insights using OpenRouter API.

Returns:

* Business insights
* Financial recommendations

---

## 6. Parse Tally XML

### POST `/parse-tally`

Uploads and parses Tally XML export.

Returns:

* Company name
* Cash balance
* Top debtors
* Gross margin
* Net margin

---

# Assumptions

* CSV columns are correctly formatted.
* Financial values are numeric.
* Uploaded XML follows standard Tally export structure.
* AI responses may vary slightly depending on model output.

---

# Improvements Possible

* Add database integration
* Add authentication
* Add async background processing
* Add dashboard frontend
* Add advanced forecasting
* Add Docker support
* Add unit and integration tests

---

# Security Notes

* `.env` file is excluded using `.gitignore`
* API keys should never be committed to GitHub

---

# Author

Shivam Baghel
