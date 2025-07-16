from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    if request.method == 'POST':
        city = request.form['city']
        api_key = request.form['api_key']
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        full_url = f"{base_url}appid={api_key}&q={city}&units=metric"
        response = requests.get(full_url)

        if response.status_code == 200:
            data = response.json()
            weather_data = {
                'city': city,
                'temp': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description'],
                'wind_speed': data['wind']['speed']
            }
        else:
            weather_data = {'error': 'City not found or API error'}

    return render_template('index.html', weather=weather_data)

if __name__ == '__main__':
    app.run(debug=True)