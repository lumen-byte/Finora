from fastapi import APIRouter
from backend.app.api.routers.auth import router as auth_router
from backend.app.api.routers.health import router as health_router
from backend.app.api.routers.accounts import router as accounts_router
from backend.app.api.routers.categories import router as categories_router
from backend.app.api.routers.transactions import router as transactions_router
from backend.app.api.routers.analytics import router as analytics_router
from backend.app.api.routers.insights import router as insights_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(accounts_router, prefix="/accounts")
api_router.include_router(categories_router, prefix="/categories")
api_router.include_router(transactions_router, prefix="/transactions")
api_router.include_router(analytics_router, prefix="/analytics")
api_router.include_router(insights_router, prefix="/insights")
