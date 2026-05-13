from pydantic import BaseModel
from typing import List


class CSVRow(BaseModel):
    month: str
    revenue: int
    expenses: int
    cash_balance: int
    debtors: int
    creditors: int
    gst_payable: int


class UploadResponse(BaseModel):
    data: List[CSVRow]
    gross_margin_pct: float
    cash_runway_days: int
    working_capital: int