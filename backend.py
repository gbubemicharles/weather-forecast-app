import requests
import os
from dotenv import load_dotenv
import streamlit as st

# Load .env only if running locally
load_dotenv()


def get_api_key():
    """Return API key from Streamlit secrets or local .env"""
    try:
        # Use Streamlit secrets if available (deployment)
        return st.secrets["API_KEY"]
    except Exception:
        # Fallback to local .env
        return os.getenv("API_KEY")


API_KEY = get_api_key()


def get_data(place, forecast_days=None):
    """Fetch forecast data for a city from OpenWeatherMap API"""
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={place}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Error fetching data: {response.status_code} - {response.text}")

    data = response.json()
    filtered_data = data["list"]
    nr_values = 8 * forecast_days if forecast_days else len(filtered_data)
    return filtered_data[:nr_values]


if __name__ == "__main__":
    print(get_data(place="Tokyo", forecast_days=2))
