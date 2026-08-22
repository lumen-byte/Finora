from typing import List, Optional, Tuple
from uuid import UUID
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from backend.app.models.transaction import Transaction
from backend.app.models.category import TransactionType, Category
from backend.app.models.account import Account

class AnalyticsRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_total_balance(self, user_id: UUID) -> float:
        result = self.session.query(func.sum(Account.current_balance)).filter(Account.user_id == user_id).scalar()
        return float(result) if result else 0.0

    def get_monthly_totals(self, user_id: UUID, year: int, month: int) -> Tuple[float, float]:
        """Returns (total_income, total_expenses) for a given month."""
        result = self.session.query(
            Transaction.type,
            func.sum(Transaction.amount)
        ).filter(
            Transaction.user_id == user_id,
            extract('year', Transaction.transaction_date) == year,
            extract('month', Transaction.transaction_date) == month
        ).group_by(Transaction.type).all()

        income, expenses = 0.0, 0.0
        for tx_type, total in result:
            if tx_type == TransactionType.INCOME:
                income = float(total)
            elif tx_type == TransactionType.EXPENSE:
                expenses = float(total)
        return income, expenses

    def get_category_breakdown(self, user_id: UUID, start_date: date, end_date: date) -> List[dict]:
        results = self.session.query(
            Category.name,
            func.sum(Transaction.amount).label("total_amount"),
            func.count(Transaction.id).label("transaction_count")
        ).join(Category, Transaction.category_id == Category.id)\
         .filter(
            Transaction.user_id == user_id,
            Transaction.type == TransactionType.EXPENSE,
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
         ).group_by(Category.name).all()
        
        return [{"category": r.name, "total_amount": float(r.total_amount), "transaction_count": r.transaction_count} for r in results]

    def get_monthly_trends(self, user_id: UUID) -> List[dict]:
        # Uses TO_CHAR for PostgreSQL
        results = self.session.query(
            func.to_char(Transaction.transaction_date, 'YYYY-MM').label("month"),
            Transaction.type,
            func.sum(Transaction.amount).label("total")
        ).filter(Transaction.user_id == user_id)\
         .group_by("month", Transaction.type)\
         .order_by("month").all()

        trends = {}
        for r in results:
            month = r.month
            if month not in trends:
                trends[month] = {"month": month, "income": 0.0, "expenses": 0.0}
            if r.type == TransactionType.INCOME:
                trends[month]["income"] += float(r.total)
            elif r.type == TransactionType.EXPENSE:
                trends[month]["expenses"] += float(r.total)
                
        # Calculate net
        final_trends = []
        for v in trends.values():
            v["net_cash_flow"] = v["income"] - v["expenses"]
            final_trends.append(v)
            
        return final_trends

    def get_top_merchants(self, user_id: UUID, start_date: date, end_date: date, limit: int = 10) -> List[dict]:
        results = self.session.query(
            Transaction.merchant,
            func.sum(Transaction.amount).label("total_spent"),
            func.count(Transaction.id).label("transaction_count")
        ).filter(
            Transaction.user_id == user_id,
            Transaction.type == TransactionType.EXPENSE,
            Transaction.merchant.isnot(None),
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        ).group_by(Transaction.merchant)\
         .order_by(func.sum(Transaction.amount).desc())\
         .limit(limit).all()
         
        return [{"merchant": r.merchant, "total_spent": float(r.total_spent), "transaction_count": r.transaction_count} for r in results]
