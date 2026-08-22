from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from backend.app.api.deps import get_current_user, get_db
from backend.app.schemas.user import UserResponse
from backend.app.schemas.analytics import (
    DashboardResponse,
    CategoryBreakdown,
    MonthlyTrend,
    TopMerchant,
    MonthComparisonResponse,
    RecurringTransactionResponse,
    AnomalyResponse
)
from backend.app.services.analytics_service import AnalyticsService
from backend.app.services.recurring_detection_service import RecurringDetectionService
from backend.app.services.anomaly_detection_service import AnomalyDetectionService

router = APIRouter(tags=["analytics"])

@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard(
    year: Optional[int] = Query(None, description="Year (defaults to current)"),
    month: Optional[int] = Query(None, description="Month (defaults to current)"),
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not year or not month:
        today = date.today()
        year = year or today.year
        month = month or today.month
        
    service = AnalyticsService(db)
    return service.get_dashboard(current_user.id, year, month)

@router.get("/category-breakdown", response_model=List[CategoryBreakdown])
def get_category_breakdown(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not start_date or not end_date:
        today = date.today()
        start_date = date(today.year, today.month, 1)
        end_date = today
        
    service = AnalyticsService(db)
    return service.get_category_breakdown(current_user.id, start_date, end_date)

@router.get("/monthly-trends", response_model=List[MonthlyTrend])
def get_monthly_trends(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = AnalyticsService(db)
    return service.get_monthly_trends(current_user.id)

@router.get("/top-merchants", response_model=List[TopMerchant])
def get_top_merchants(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    limit: int = Query(10, ge=1, le=50),
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not start_date or not end_date:
        today = date.today()
        start_date = date(today.year, today.month, 1)
        end_date = today
        
    service = AnalyticsService(db)
    return service.get_top_merchants(current_user.id, start_date, end_date, limit)

@router.get("/month-comparison", response_model=MonthComparisonResponse)
def get_month_comparison(
    year: Optional[int] = Query(None),
    month: Optional[int] = Query(None),
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not year or not month:
        today = date.today()
        year = year or today.year
        month = month or today.month
        
    service = AnalyticsService(db)
    return service.get_month_comparison(current_user.id, year, month)

@router.get("/recurring-transactions", response_model=List[RecurringTransactionResponse])
def get_recurring_transactions(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = RecurringDetectionService(db)
    return service.detect_recurring(current_user.id)

@router.get("/anomalies", response_model=List[AnomalyResponse])
def get_anomalies(
    days_lookback: int = Query(30, ge=7, le=365),
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = AnomalyDetectionService(db)
    return service.detect_anomalies(current_user.id, days_lookback)
