from fastapi import APIRouter, HTTPException
from datetime import date
from utils.analytics import AnalyticsService, AnalyticsRepository

router = APIRouter()

analytics_repository = AnalyticsRepository()
analytics_service = AnalyticsService(analytics_repository)

@router.get("/comments-daily-breakdown")
def comments_daily_breakdown(date_from: date, date_to: date):
    if date_from > date_to:
        raise HTTPException(status_code=400, detail="Invalid date range")
    
    analytics_data = analytics_service.get_comments_daily_breakdown(date_from, date_to)
    return analytics_data
