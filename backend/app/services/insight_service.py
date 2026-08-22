from typing import List
from uuid import UUID
import uuid
from datetime import date
from sqlalchemy.orm import Session
from backend.app.schemas.insight import InsightResponse
from backend.app.services.analytics_service import AnalyticsService
from backend.app.services.recurring_detection_service import RecurringDetectionService
from backend.app.services.anomaly_detection_service import AnomalyDetectionService

class InsightService:
    def __init__(self, session: Session):
        self.session = session
        self.analytics = AnalyticsService(session)
        self.recurring = RecurringDetectionService(session)
        self.anomaly = AnomalyDetectionService(session)

    def generate_insights(self, user_id: UUID) -> List[InsightResponse]:
        insights = []
        today = date.today()
        
        # 1. Dashboard Insights
        dashboard = self.analytics.get_dashboard(user_id, today.year, today.month)
        
        if dashboard.savings_rate < 10:
            insights.append(InsightResponse(
                id=str(uuid.uuid4()),
                title="Low Savings Rate",
                message=f"Your savings rate this month is {dashboard.savings_rate}%, which is quite low. Consider reviewing your discretionary expenses.",
                severity="WARNING"
            ))
            
        if dashboard.expense_change_percentage and dashboard.expense_change_percentage > 20:
            insights.append(InsightResponse(
                id=str(uuid.uuid4()),
                title="High Spending Increase",
                message=f"Your expenses have increased by {dashboard.expense_change_percentage}% compared to last month.",
                severity="IMPORTANT"
            ))

        # 2. Category Insights (Top Category)
        month_comp = self.analytics.get_month_comparison(user_id, today.year, today.month)
        if month_comp.category_comparisons:
            top_cat = month_comp.category_comparisons[0]
            insights.append(InsightResponse(
                id=str(uuid.uuid4()),
                title="Top Expense Category",
                message=f"{top_cat.category} is your largest expense category this month, totaling {top_cat.current_amount}.",
                severity="INFO",
                related_category=top_cat.category
            ))
            
            # Check for specific category spikes
            for cat in month_comp.category_comparisons:
                if cat.change_percentage and cat.change_percentage > 30 and cat.current_amount > 100:
                    insights.append(InsightResponse(
                        id=str(uuid.uuid4()),
                        title="Category Spending Spike",
                        message=f"Your {cat.category} spending increased by {cat.change_percentage}% compared to last month.",
                        severity="WARNING",
                        related_category=cat.category
                    ))

        # 3. Recurring Transactions Insight
        recurring = self.recurring.detect_recurring(user_id)
        if recurring:
            total_recurring = sum(r.average_amount for r in recurring if r.frequency == "MONTHLY")
            insights.append(InsightResponse(
                id=str(uuid.uuid4()),
                title="Recurring Expenses",
                message=f"You have {len(recurring)} active subscriptions/recurring expenses costing approximately {total_recurring:.2f} per month.",
                severity="INFO"
            ))

        # 4. Anomaly Insights
        anomalies = self.anomaly.detect_anomalies(user_id, days_lookback=30)
        for anomaly in anomalies:
            if anomaly.anomaly_score > 3.0:
                insights.append(InsightResponse(
                    id=str(uuid.uuid4()),
                    title="Large Unusual Transaction Detected",
                    message=anomaly.reason,
                    severity="IMPORTANT",
                    related_transaction_id=anomaly.transaction.id
                ))

        return insights
