from datetime import datetime, date
import sys
import os

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from unittest.mock import patch


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.analytics import AnalyticsRepository, AnalyticsService
from controllers.analytics_controller import router
from seed import execute_sql_file


def test_fetch_comments_analytics():
    repo = AnalyticsRepository()
    execute_sql_file()

    analytics_data = repo.fetch_comments_analytics(date(2024, 9, 17), date(2024, 9, 24))

    assert len(analytics_data) == 8 
    assert analytics_data[0].total_comments == 2
    assert analytics_data[0].banned_comments == 1
    assert analytics_data[1].total_comments == 1
    assert analytics_data[1].banned_comments == 0
    assert analytics_data[2].total_comments == 2
    assert analytics_data[2].banned_comments == 1
    assert analytics_data[3].total_comments == 2
    assert analytics_data[3].banned_comments == 0
    assert analytics_data[4].total_comments == 2
    assert analytics_data[4].banned_comments == 0
    assert analytics_data[5].total_comments == 2
    assert analytics_data[5].banned_comments == 1
    assert analytics_data[6].total_comments == 1
    assert analytics_data[6].banned_comments == 1
    assert analytics_data[7].total_comments == 1
    assert analytics_data[7].banned_comments == 0


def test_get_comments_daily_breakdown():
    mock_repo = MagicMock(spec=AnalyticsRepository)
    
    expected_data = [
        MagicMock(day=date(2024, 9, 17), total_comments=2, banned_comments=1),
        MagicMock(day=date(2024, 9, 18), total_comments=1, banned_comments=0),
        MagicMock(day=date(2024, 9, 19), total_comments=2, banned_comments=1),
        MagicMock(day=date(2024, 9, 20), total_comments=2, banned_comments=0),
        MagicMock(day=date(2024, 9, 21), total_comments=2, banned_comments=0),
        MagicMock(day=date(2024, 9, 22), total_comments=2, banned_comments=1),
        MagicMock(day=date(2024, 9, 23), total_comments=1, banned_comments=1),
        MagicMock(day=date(2024, 9, 24), total_comments=1, banned_comments=0)
    ]
    
    mock_repo.fetch_comments_analytics.return_value = expected_data

    analytics_service = AnalyticsService(mock_repo)

    result = analytics_service.get_comments_daily_breakdown(date(2024, 9, 17), date(2024, 9, 24))

    expected_result = [
        {"day": date(2024, 9, 17), "total_comments": 2, "banned_comments": 1},
        {"day": date(2024, 9, 18), "total_comments": 1, "banned_comments": 0},
        {"day": date(2024, 9, 19), "total_comments": 2, "banned_comments": 1},
        {"day": date(2024, 9, 20), "total_comments": 2, "banned_comments": 0},
        {"day": date(2024, 9, 21), "total_comments": 2, "banned_comments": 0},
        {"day": date(2024, 9, 22), "total_comments": 2, "banned_comments": 1},
        {"day": date(2024, 9, 23), "total_comments": 1, "banned_comments": 1},
        {"day": date(2024, 9, 24), "total_comments": 1, "banned_comments": 0}
    ]

    assert result == expected_result


app = FastAPI()


app.include_router(router)

client = TestClient(app)

expected_data = [
    {"day": "2024-09-17", "total_comments": 2, "banned_comments": 1},
    {"day": "2024-09-18", "total_comments": 1, "banned_comments": 0},
    {"day": "2024-09-19", "total_comments": 2, "banned_comments": 1},
    {"day": "2024-09-20", "total_comments": 2, "banned_comments": 0},
    {"day": "2024-09-21", "total_comments": 2, "banned_comments": 0},
    {"day": "2024-09-22", "total_comments": 2, "banned_comments": 1},
    {"day": "2024-09-23", "total_comments": 1, "banned_comments": 1},
    {"day": "2024-09-24", "total_comments": 1, "banned_comments": 0}
]

def test_comments_daily_breakdown():
    with patch('controllers.analytics_controller.analytics_service') as mock_service:
        mock_service.get_comments_daily_breakdown.return_value = expected_data
        
        response = client.get("/comments-daily-breakdown", params={"date_from": "2024-09-17", "date_to": "2024-09-24"})

        assert response.status_code == 200
        assert response.json() == expected_data


def test_comments_daily_breakdown_invalid_date_range():
    response = client.get("/comments-daily-breakdown", params={"date_from": "2024-09-24", "date_to": "2024-09-17"})
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid date range"}
