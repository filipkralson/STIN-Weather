import requests
from flask import request
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

BASE_URL = "https://api.weatherapi.com/v1"
load_dotenv()
API_KEY = os.getenv("API_KEY")


def get_current_weather(city_name):
    url = f"{BASE_URL}/current.json"
    params = {"key": API_KEY, "q": city_name}
    response = requests.get(url, params=params)
    data = response.json()
    return data


def get_current_weather_by_ip():
    try:
        ip_address = request.remote_addr
        if ip_address == '127.0.0.1' or ip_address == '0.0.0.0':
            return get_current_weather("Liberec")
        else:
            response = requests.get(f"https://ipinfo.io/{ip_address}/json")
            if response.status_code == 200:
                data = response.json()
                city_name = data.get("city")
                return get_current_weather(city_name)
            else:
                return get_current_weather("Liberec")
    except Exception as e:
        print("Error:", e)
        return None


def get_weather_forecast(city_name):
    url = f"{BASE_URL}/forecast.json"
    params = {"key": API_KEY, "q": city_name, "days": 7}
    response = requests.get(url, params=params)
    data = response.json()
    return data


def get_weather_history(city_name):
    url = f"{BASE_URL}/history.json"
    end_dt = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    dt = ((datetime.now() - timedelta(days=1)) - timedelta(days=7)).strftime('%Y-%m-%d')
    params = {
        "key": API_KEY,
        "q": city_name,
        "dt": dt,
        "end_dt": end_dt,
    }

    response = requests.get(url, params=params)
    data = response.json()

    filtered_data = []
    if 'forecast' in data and 'forecastday' in data['forecast']:
        for forecast_day in data['forecast']['forecastday']:
            for hour_forecast in forecast_day['hour']:
                if hour_forecast['time'].endswith('12:00'):
                    filtered_data.append(hour_forecast)
    return filtered_data
