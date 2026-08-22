import calendar
from typing import List, Optional
from uuid import UUID
from datetime import date
from decimal import Decimal
from sqlalchemy.orm import Session
from backend.app.repositories.analytics_repository import AnalyticsRepository
from backend.app.schemas.analytics import (
    DashboardResponse,
    CategoryBreakdown,
    MonthlyTrend,
    TopMerchant,
    MonthComparisonResponse,
    CategoryComparison
)

class AnalyticsService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = AnalyticsRepository(session)

    def _calc_percentage_change(self, old_val: float, new_val: float) -> Optional[Decimal]:
        if old_val == 0:
            return None if new_val == 0 else Decimal('100.0') if new_val > 0 else Decimal('-100.0')
        change = ((new_val - old_val) / abs(old_val)) * 100
        return Decimal(str(round(change, 2)))

    def get_dashboard(self, user_id: UUID, year: int, month: int) -> DashboardResponse:
        total_balance = self.repo.get_total_balance(user_id)
        current_inc, current_exp = self.repo.get_monthly_totals(user_id, year, month)
        
        # Previous month
        prev_month = month - 1 if month > 1 else 12
        prev_year = year if month > 1 else year - 1
        prev_inc, prev_exp = self.repo.get_monthly_totals(user_id, prev_year, prev_month)
        
        current_net = current_inc - current_exp
        prev_net = prev_inc - prev_exp
        
        savings_rate = 0.0
        if current_inc > 0:
            savings_rate = ((current_inc - current_exp) / current_inc) * 100
            
        return DashboardResponse(
            total_balance=Decimal(str(round(total_balance, 2))),
            total_income=Decimal(str(round(current_inc, 2))),
            total_expenses=Decimal(str(round(current_exp, 2))),
            net_cash_flow=Decimal(str(round(current_net, 2))),
            savings_rate=Decimal(str(round(savings_rate, 2))),
            income_change_percentage=self._calc_percentage_change(prev_inc, current_inc),
            expense_change_percentage=self._calc_percentage_change(prev_exp, current_exp),
            cash_flow_change_percentage=self._calc_percentage_change(prev_net, current_net)
        )

    def get_category_breakdown(self, user_id: UUID, start_date: date, end_date: date) -> List[CategoryBreakdown]:
        raw_data = self.repo.get_category_breakdown(user_id, start_date, end_date)
        total_expenses = sum(item["total_amount"] for item in raw_data)
        
        result = []
        for item in raw_data:
            pct = (item["total_amount"] / total_expenses * 100) if total_expenses > 0 else 0
            result.append(CategoryBreakdown(
                category=item["category"],
                total_amount=Decimal(str(round(item["total_amount"], 2))),
                transaction_count=item["transaction_count"],
                percentage_of_total_expenses=Decimal(str(round(pct, 2)))
            ))
        # Sort by amount descending
        result.sort(key=lambda x: x.total_amount, reverse=True)
        return result

    def get_monthly_trends(self, user_id: UUID) -> List[MonthlyTrend]:
        raw_data = self.repo.get_monthly_trends(user_id)
        return [MonthlyTrend(
            month=item["month"],
            income=Decimal(str(round(item["income"], 2))),
            expenses=Decimal(str(round(item["expenses"], 2))),
            net_cash_flow=Decimal(str(round(item["net_cash_flow"], 2)))
        ) for item in raw_data]

    def get_top_merchants(self, user_id: UUID, start_date: date, end_date: date, limit: int = 10) -> List[TopMerchant]:
        raw_data = self.repo.get_top_merchants(user_id, start_date, end_date, limit)
        return [TopMerchant(
            merchant=item["merchant"],
            total_spent=Decimal(str(round(item["total_spent"], 2))),
            transaction_count=item["transaction_count"]
        ) for item in raw_data]

    def get_month_comparison(self, user_id: UUID, year: int, month: int) -> MonthComparisonResponse:
        current_inc, current_exp = self.repo.get_monthly_totals(user_id, year, month)
        prev_month = month - 1 if month > 1 else 12
        prev_year = year if month > 1 else year - 1
        prev_inc, prev_exp = self.repo.get_monthly_totals(user_id, prev_year, prev_month)
        
        # Get start/end dates for category breakdown
        _, current_last_day = calendar.monthrange(year, month)
        current_start = date(year, month, 1)
        current_end = date(year, month, current_last_day)
        
        _, prev_last_day = calendar.monthrange(prev_year, prev_month)
        prev_start = date(prev_year, prev_month, 1)
        prev_end = date(prev_year, prev_month, prev_last_day)
        
        current_cats = {item["category"]: item["total_amount"] for item in self.repo.get_category_breakdown(user_id, current_start, current_end)}
        prev_cats = {item["category"]: item["total_amount"] for item in self.repo.get_category_breakdown(user_id, prev_start, prev_end)}
        
        all_categories = set(current_cats.keys()).union(set(prev_cats.keys()))
        category_comparisons = []
        for cat in all_categories:
            c_amt = current_cats.get(cat, 0.0)
            p_amt = prev_cats.get(cat, 0.0)
            if c_amt > 0 or p_amt > 0:
                category_comparisons.append(CategoryComparison(
                    category=cat,
                    previous_amount=Decimal(str(round(p_amt, 2))),
                    current_amount=Decimal(str(round(c_amt, 2))),
                    change_percentage=self._calc_percentage_change(p_amt, c_amt)
                ))
                
        category_comparisons.sort(key=lambda x: x.current_amount, reverse=True)
        
        return MonthComparisonResponse(
            income_previous_month=Decimal(str(round(prev_inc, 2))),
            income_current_month=Decimal(str(round(current_inc, 2))),
            income_change_percentage=self._calc_percentage_change(prev_inc, current_inc),
            expenses_previous_month=Decimal(str(round(prev_exp, 2))),
            expenses_current_month=Decimal(str(round(current_exp, 2))),
            expense_change_percentage=self._calc_percentage_change(prev_exp, current_exp),
            category_comparisons=category_comparisons
        )
