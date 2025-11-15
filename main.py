import streamlit as st
import plotly.express as px
from backend import get_data

st.title("5-Day Weather Forecast")

place = st.text_input("Place: ")
days = st.slider("Forecast Days", min_value=1, max_value=5,
                 help="Select the number of forecasted days")
option = st.selectbox("Select data to view", ("Temperature", "Sky"))
st.subheader(f"{option} for the next {days} day(s) in {place}")

if place:
    try:
        filtered_data = get_data(place, days)

        if option == "Temperature":
            temperature = [d["main"]["temp"] for d in filtered_data]
            date = [d["dt_txt"] for d in filtered_data]
            figure = px.line(x=date, y=temperature, labels={"x": "Date", "y": "Temperature (°C)"})
            st.plotly_chart(figure)

        if option == "Sky":
            emoji_map = {"Clear":"☀️", "Clouds":"☁️", "Rain":"🌧️", "Snow":"❄️", "Drizzle":"🌦️", "Thunderstorm":"⛈️"}
            sky_conditions = [d["weather"][0]["main"] for d in filtered_data]
            emoji_list = [emoji_map.get(cond, "🌫️") for cond in sky_conditions]
            st.write(" ".join(emoji_list))

    except Exception as e:
        st.error(f"Failed to fetch weather data: {e}")
