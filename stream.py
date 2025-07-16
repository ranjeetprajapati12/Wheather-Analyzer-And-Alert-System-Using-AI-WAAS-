import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.title("Weather Forecast with Condition Categorization")

# Input
location = st.text_input("Enter Location (City Name)", "Delhi")
api_key = st.text_input("Enter OpenWeatherMap API Key", type="password")

# Weather condition label function
def categorize_weather(temp, humidity, wind):
    if 20 <= temp <= 30 and 30 <= humidity <= 60 and wind < 5:
        return "Good"
    elif temp < 15 or temp > 35 or humidity < 25 or humidity > 80 or wind > 8:
        return "Bad"
    else:
        return "Moderate"

if st.button("Get Weather Forecast"):
    if not location or not api_key:
        st.warning("Please enter both Location and API Key.")
    else:
        # Fetch API
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}&units=metric"
        res = requests.get(url)

        if res.status_code != 200:
            st.error("Failed to fetch weather data. Check location or API key.")
        else:
            data = res.json()
            forecast_list = data['list']

            # Parse and categorize data
            weather_data = []
            for entry in forecast_list:
                temp = entry["main"]["temp"]
                humidity = entry["main"]["humidity"]
                wind = entry["wind"]["speed"]
                label = categorize_weather(temp, humidity, wind)

                weather_data.append({
                    "datetime": entry["dt_txt"],
                    "temp": temp,
                    "humidity": humidity,
                    "wind_speed": wind,
                    "condition": label
                })

            df = pd.DataFrame(weather_data)

            # Show table with condition
            st.write("### Weather Forecast with Conditions (Next 5 Days)")
            def highlight_condition(row):
                color = {"Good": "#d4edda", "Moderate": "#fff3cd", "Bad": "#f8d7da"}[row['condition']]
                return [f'background-color: {color}']*len(row)

            st.dataframe(df.style.apply(highlight_condition, axis=1))

            # Plotting charts
            st.write("### Forecast Charts")
            fig, ax = plt.subplots(3, 1, figsize=(10, 12))

            ax[0].plot(df["datetime"], df["temp"], color='red', marker='o')
            ax[0].set_title("Temperature (°C)")
            ax[0].tick_params(axis='x', rotation=45)

            ax[1].plot(df["datetime"], df["humidity"], color='blue', marker='o')
            ax[1].set_title("Humidity (%)")
            ax[1].tick_params(axis='x', rotation=45)

            ax[2].plot(df["datetime"], df["wind_speed"], color='green', marker='o')
            ax[2].set_title("Wind Speed (m/s)")
            ax[2].tick_params(axis='x', rotation=45)

            plt.tight_layout()
            st.pyplot(fig)

            # Summary count
            st.write("### Weather Condition Summary")
            summary = df['condition'].value_counts().rename_axis('Condition').reset_index(name='Counts')
            st.table(summary)
