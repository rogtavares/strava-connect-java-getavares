"""
Configurações e fixtures para testes pytest
"""
import pytest
import os
from unittest.mock import Mock, MagicMock, patch
import sys

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from strava_client import StravaClient


@pytest.fixture
def client_credentials():
    """Credenciais mock para testes"""
    return {
        "client_id": "test_client_id_12345",
        "client_secret": "test_client_secret_abc123",
        "access_token": "test_access_token_xyz789"
    }


@pytest.fixture
def strava_client(client_credentials):
    """Instância do cliente Strava para testes"""
    return StravaClient(
        client_id=client_credentials["client_id"],
        client_secret=client_credentials["client_secret"],
        access_token=client_credentials["access_token"]
    )


@pytest.fixture
def mock_athlete_response():
    """Mock de resposta de atleta"""
    return {
        "id": 123456,
        "username": "test_athlete",
        "firstname": "Test",
        "lastname": "Athlete",
        "city": "São Paulo",
        "state": "SP",
        "country": "Brazil",
        "sex": "M",
        "summit": False,
        "created_at": "2020-01-01T00:00:00Z",
        "updated_at": "2025-11-24T10:30:00Z",
        "badge_type_id": 4,
        "weight": 75.5,
        "profile_medium": "https://example.com/profile_medium.jpg",
        "profile": "https://example.com/profile.jpg",
        "friend": False,
        "follower": False
    }


@pytest.fixture
def mock_activities_response():
    """Mock de resposta de atividades"""
    return [
        {
            "id": 9876543210,
            "resource_state": 2,
            "external_id": "garmin_uuid",
            "upload_id": 11111111,
            "athlete": {"id": 123456, "resource_state": 1},
            "name": "Morning Run",
            "distance": 5000.0,
            "moving_time": 1800,
            "elapsed_time": 1850,
            "total_elevation_gain": 120.5,
            "elev_high": 450.0,
            "elev_low": 330.0,
            "type": "Run",
            "sport_type": "Run",
            "start_date": "2025-11-24T06:00:00Z",
            "start_date_local": "2025-11-24T03:00:00Z",
            "timezone": "America/Sao_Paulo",
            "utc_offset": -10800.0,
            "location_city": "São Paulo",
            "location_state": "SP",
            "location_country": "Brazil",
            "start_latlng": [-23.5505, -46.6333],
            "end_latlng": [-23.5505, -46.6333],
            "achievement_count": 2,
            "kudos_count": 5,
            "comment_count": 1,
            "athlete_count": 1,
            "photo_count": 0,
            "map": {
                "id": "map_12345",
                "summary_polyline": "encoded_polyline_here",
                "resource_state": 2
            },
            "trainer": False,
            "commute": False,
            "manual": False,
            "private": False,
            "visibility": "everyone",
            "flagged": False,
            "workout_type": 0,
            "average_speed": 2.78,
            "max_speed": 3.5,
            "average_cadence": 85.5,
            "average_temp": 22,
            "average_watts": 250.5,
            "weighted_average_watts": 275.0,
            "kilojoules": 450.0,
            "device_watts": False,
            "has_heartrate": True,
            "average_heartrate": 155.2,
            "max_heartrate": 175.0,
            "heartrate_opt_out": False,
            "display_hide_heartrate_option": True,
            "from_accepted_tag": False,
            "pr_count": 1,
            "total_photo_count": 2,
            "has_kudoed": False,
            "suffer_score": 150
        },
        {
            "id": 9876543209,
            "resource_state": 2,
            "external_id": "garmin_uuid_2",
            "upload_id": 11111112,
            "athlete": {"id": 123456, "resource_state": 1},
            "name": "Evening Ride",
            "distance": 25000.0,
            "moving_time": 5400,
            "elapsed_time": 5500,
            "total_elevation_gain": 450.0,
            "elev_high": 550.0,
            "elev_low": 100.0,
            "type": "Ride",
            "sport_type": "Ride",
            "start_date": "2025-11-23T17:00:00Z",
            "start_date_local": "2025-11-23T14:00:00Z",
            "timezone": "America/Sao_Paulo",
            "utc_offset": -10800.0,
            "location_city": "São Paulo",
            "location_state": "SP",
            "location_country": "Brazil",
            "start_latlng": [-23.5505, -46.6333],
            "end_latlng": [-23.5505, -46.6333],
            "achievement_count": 5,
            "kudos_count": 15,
            "comment_count": 3,
            "athlete_count": 2,
            "photo_count": 5,
            "map": {
                "id": "map_12346",
                "summary_polyline": "encoded_polyline_here_2",
                "resource_state": 2
            },
            "trainer": False,
            "commute": False,
            "manual": False,
            "private": False,
            "visibility": "everyone",
            "flagged": False,
            "workout_type": 0,
            "average_speed": 16.67,
            "max_speed": 45.0,
            "average_cadence": 90.5,
            "average_temp": 20,
            "average_watts": 180.5,
            "weighted_average_watts": 195.0,
            "kilojoules": 972.0,
            "device_watts": True,
            "has_heartrate": True,
            "average_heartrate": 145.2,
            "max_heartrate": 165.0,
            "heartrate_opt_out": False,
            "display_hide_heartrate_option": True,
            "from_accepted_tag": False,
            "pr_count": 2,
            "total_photo_count": 8,
            "has_kudoed": False,
            "suffer_score": 120
        }
    ]


@pytest.fixture
def mock_stats_response():
    """Mock de resposta de estatísticas"""
    return {
        "biggest_ride_elevation": 3200,
        "biggest_climb_elevation_gain": 800,
        "recent_ride_totals": {
            "count": 5,
            "distance": 125000.0,
            "moving_time": 27000,
            "elapsed_time": 28000,
            "elevation_gain": 1200.0
        },
        "recent_run_totals": {
            "count": 8,
            "distance": 50000.0,
            "moving_time": 14400,
            "elapsed_time": 15000,
            "elevation_gain": 500.0
        },
        "recent_swim_totals": {
            "count": 2,
            "distance": 5000.0,
            "moving_time": 600,
            "elapsed_time": 600,
            "elevation_gain": 0.0
        },
        "ytd_ride_totals": {
            "count": 50,
            "distance": 1250000.0,
            "moving_time": 270000,
            "elapsed_time": 280000,
            "elevation_gain": 12000.0
        },
        "ytd_run_totals": {
            "count": 80,
            "distance": 500000.0,
            "moving_time": 144000,
            "elapsed_time": 150000,
            "elevation_gain": 5000.0
        },
        "all_ride_totals": {
            "count": 250,
            "distance": 6250000.0,
            "moving_time": 1350000,
            "elapsed_time": 1400000,
            "elevation_gain": 60000.0
        },
        "all_run_totals": {
            "count": 400,
            "distance": 2500000.0,
            "moving_time": 720000,
            "elapsed_time": 750000,
            "elevation_gain": 25000.0
        },
        "all_swim_totals": {
            "count": 50,
            "distance": 250000.0,
            "moving_time": 30000,
            "elapsed_time": 30000,
            "elevation_gain": 0.0
        }
    }


@pytest.fixture
def mock_requests_post(monkeypatch):
    """Mock do requests.post"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "access_token": "test_token",
        "refresh_token": "test_refresh",
        "expires_at": 1234567890,
        "token_type": "Bearer"
    }
    
    def mock_post(*args, **kwargs):
        return mock_response
    
    monkeypatch.setattr("requests.post", mock_post)
    return mock_response


@pytest.fixture
def mock_requests_get(monkeypatch):
    """Mock do requests.get"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {
        "X-RateLimit-Limit": "600",
        "X-RateLimit-Reset": str(int(time.time()) + 3600)
    }
    
    def mock_get(*args, **kwargs):
        return mock_response
    
    monkeypatch.setattr("requests.get", mock_get)
    return mock_response


import time
