from pydantic import BaseModel
from decimal import Decimal
from typing import List, Optional
from datetime import date
from backend.app.schemas.transaction import TransactionResponse

class DashboardResponse(BaseModel):
    total_balance: Decimal
    total_income: Decimal
    total_expenses: Decimal
    net_cash_flow: Decimal
    savings_rate: Decimal
    income_change_percentage: Optional[Decimal] = None
    expense_change_percentage: Optional[Decimal] = None
    cash_flow_change_percentage: Optional[Decimal] = None

class CategoryBreakdown(BaseModel):
    category: str
    total_amount: Decimal
    transaction_count: int
    percentage_of_total_expenses: Decimal

class MonthlyTrend(BaseModel):
    month: str # YYYY-MM
    income: Decimal
    expenses: Decimal
    net_cash_flow: Decimal

class TopMerchant(BaseModel):
    merchant: str
    total_spent: Decimal
    transaction_count: int

class CategoryComparison(BaseModel):
    category: str
    previous_amount: Decimal
    current_amount: Decimal
    change_percentage: Optional[Decimal] = None

class MonthComparisonResponse(BaseModel):
    income_previous_month: Decimal
    income_current_month: Decimal
    income_change_percentage: Optional[Decimal] = None
    expenses_previous_month: Decimal
    expenses_current_month: Decimal
    expense_change_percentage: Optional[Decimal] = None
    category_comparisons: List[CategoryComparison]

class RecurringTransactionResponse(BaseModel):
    merchant: str
    average_amount: Decimal
    frequency: str
    estimated_next_date: Optional[date] = None
    transaction_count: int
    confidence_score: Decimal

class AnomalyResponse(BaseModel):
    transaction: TransactionResponse
    expected_range_min: Decimal
    expected_range_max: Decimal
    anomaly_score: Decimal
    reason: str
