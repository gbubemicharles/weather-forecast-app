import requests

API_KEY = "366597db51ba66a8aa26aa37e1a4baaa"

def get_data(place, forecast_days=None):
    url = (
        f"http://api.openweathermap.org/data/2.5/forecast"
        f"?q={place}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url)
    data = response.json()

    # Handle errors (e.g., invalid city name)
    if data.get("cod") != "200":
        return []

    filtered_data = data.get("list", [])
    nr_values = 8 * forecast_days  # 8 data points per day (3h intervals)
    return filtered_data[:nr_values]


if __name__ == "__main__":
    print(get_data(place="Tokyo", forecast_days=2))


