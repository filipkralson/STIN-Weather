import pytest
from pytest_mock import MockerFixture
from project.utils.weather import (
    get_current_weather,
    get_current_weather_by_ip,
    get_weather_forecast,
    get_weather_history,
)


@pytest.fixture
def mock_requests_get(mocker: MockerFixture):
    return mocker.patch('requests.get')


def test_get_current_weather(mock_requests_get):
    mock_response = {
        "current": {
            "temp_c": 20
        }
    }
    mock_requests_get.return_value.json.return_value = mock_response
    city_name = "Prague"
    data = get_current_weather(city_name)
    assert data['current']['temp_c'] == 20


@pytest.fixture
def mock_requests_get_success(mocker: MockerFixture):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"city": "Prague"}
    return mocker.patch('project.utils.weather.requests.get', return_value=mock_response)


@pytest.fixture
def mock_requests_get_failure(mocker: MockerFixture):
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    return mocker.patch('project.utils.weather.requests.get', return_value=mock_response)


def test_get_current_weather_by_ip_success(mock_requests_get_success):
    result = get_current_weather_by_ip()
    assert result is None


def test_get_weather_forecast(mock_requests_get):
    mock_response = {
        "forecast": {
            "forecastday": [
                {"date": "2022-04-03", "day": {"maxtemp_c": 20}},
                {"date": "2022-04-04", "day": {"maxtemp_c": 22}}
            ]
        }
    }
    mock_requests_get.return_value.json.return_value = mock_response
    city_name = "Prague"
    data = get_weather_forecast(city_name)
    assert len(data['forecast']['forecastday']) == 2


def test_get_weather_history(mock_requests_get):
    mock_response = {
        "forecast": {
            "forecastday": [
                {"date": "2022-04-03", "hour": [{"time": "2022-04-03 12:00", "temp_c": 20}]},
                {"date": "2022-04-04", "hour": [{"time": "2022-04-04 12:00", "temp_c": 22}]}
            ]
        }
    }
    mock_requests_get.return_value.json.return_value = mock_response
    city_name = "Prague"
    data = get_weather_history(city_name)
    assert len(data) == 2
