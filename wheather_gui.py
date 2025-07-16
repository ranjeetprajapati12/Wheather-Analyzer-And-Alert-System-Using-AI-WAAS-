import tkinter as tk
import requests

def fetch_weather():
    city = city_entry.get()
    api_key = api_key_entry.get()
    if not city or not api_key:
        output_label.config(text="Please enter city and API key")
        return

    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    full_url = f"{base_url}appid={api_key}&q={city}&units=metric"
    response = requests.get(full_url)

    if response.status_code == 200:
        data = response.json()
        main = data['main']
        wind = data['wind']
        weather_description = data['weather'][0]['description']
        result = f"Temperature: {main['temp']}\u00b0C\nHumidity: {main['humidity']}%\nWeather: {weather_description}\nWind Speed: {wind['speed']} m/s"
    else:
        result = "City not found or API error."
    output_label.config(text=result)

app = tk.Tk()
app.title("Weather Checker")
app.geometry("400x300")

tk.Label(app, text="City:").pack()
city_entry = tk.Entry(app)
city_entry.pack()

tk.Label(app, text="API Key:").pack()
api_key_entry = tk.Entry(app)
api_key_entry.pack()

tk.Button(app, text="Check Weather", command=fetch_weather).pack(pady=10)
output_label = tk.Label(app, text="", justify="left")
output_label.pack()

app.mainloop()