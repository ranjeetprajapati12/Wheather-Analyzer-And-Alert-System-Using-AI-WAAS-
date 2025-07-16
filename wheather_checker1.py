import requests

def get_weather(city_name, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    full_url = f"{base_url}appid={api_key}&q={city_name}&units=metric"
    response = requests.get(full_url)

    if response.status_code == 200:
        data = response.json()
        main = data['main']
        wind = data['wind']
        weather_description = data['weather'][0]['description']

        result = f"""
City: {city_name}
Temperature: {main['temp']}\u00b0C
Humidity: {main['humidity']}%
Pressure: {main['pressure']} hPa
Weather: {weather_description}
Wind Speed: {wind['speed']} m/s
        """
        print(result)
    else:
        print("City not found or error in fetching data.")

if __name__ == "__main__":
    print("Weather Checker App")
    city = input("Enter city name: ")
    api_key = input("Enter your OpenWeatherMap API key: ")
    get_weather(city, api_key)