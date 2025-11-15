import streamlit as st
import plotly.express as px
import pandas as pd
from backend import get_data

st.title("5-Day Weather Forecast")

# User Inputs
place = st.text_input("Place:")
days = st.slider("Forecast Days", min_value=1, max_value=5, help="Number of days to forecast")
option = st.selectbox("Select data to view", ("Temperature", "Sky"))
st.subheader(f"{option} for the next {days} day(s) in {place}")

if place:
    with st.spinner("Retrieving forecast..."):
        filtered_data = get_data(place, days)

    if not filtered_data:
        st.error("No data returned. Please check the city name.")
    else:
        # Temperature Section
        if option == "Temperature":
            temperature = [item["main"]["temp"] for item in filtered_data]
            date = [pd.to_datetime(item["dt_txt"]) for item in filtered_data]

            # Display basic stats
            col1, col2, col3 = st.columns(3)
            col1.metric("Max Temp", f"{max(temperature):.1f} °C")
            col2.metric("Min Temp", f"{min(temperature):.1f} °C")
            col3.metric("Avg Temp", f"{sum(temperature)/len(temperature):.1f} °C")

            # Temperature Plot
            fig = px.line(
                x=date,
                y=temperature,
                labels={"x": "Date/Time", "y": "Temperature (°C)"},
                title="Temperature Trend"
            )
            st.plotly_chart(fig)

        # Sky Condition Section
        if option == "Sky":
            # Map known weather conditions to emojis
            emoji_map = {
                "Clear": "☀️",
                "Clouds": "☁️",
                "Rain": "🌧️",
                "Snow": "❄️",
                "Drizzle": "🌦️",
                "Thunderstorm": "⛈️",
                "Mist": "🌫️",
                "Fog": "🌫️",
                "Haze": "🌫️"
            }

            # Extract sky conditions and descriptions
            sky_conditions = [
                (item.get("weather") or [{"main": "Unknown", "description": "Unknown"}])[0].get("main", "Unknown")
                for item in filtered_data
            ]
            descriptions = [
                (item.get("weather") or [{"main": "Unknown", "description": "Unknown"}])[0].get("description",
                                                                                                "Unknown").capitalize()
                for item in filtered_data
            ]

            # Map conditions to emojis, fallback to 🌡️ for unknown
            emoji_list = [emoji_map.get(cond, "🌡️") for cond in sky_conditions]

            st.write("### Sky Conditions Timeline")

            # Display emojis + descriptions in scalable rows
            max_per_row = 5  # adjust if needed
            for i in range(0, len(emoji_list), max_per_row):
                row_emojis = emoji_list[i:i + max_per_row]
                row_desc = descriptions[i:i + max_per_row]
                cols = st.columns(len(row_emojis))
                for col, emoji, desc in zip(cols, row_emojis, row_desc):
                    col.markdown(f"<h1 style='font-size:60px;text-align:center'>{emoji}</h1>", unsafe_allow_html=True)
                    col.markdown(f"<p style='text-align:center'>{desc}</p>", unsafe_allow_html=True)

