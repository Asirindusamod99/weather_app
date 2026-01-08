from flask import Flask, request
import requests
import os
from datetime import date

app = Flask(__name__)

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

@app.route("/", methods=["GET", "POST"])
def weather_page():
    weather_info = ""

    if request.method == "POST":
        city = request.form.get("city")

        weather_url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={WEATHER_API_KEY}&units=metric"
        )
        weather_data = requests.get(weather_url).json()

        if "main" in weather_data:
            weather_info = f"""
            <h3>Weather Report</h3>
            <p><b>City:</b> {weather_data['name']}</p>
            <p><b>Temperature:</b> {weather_data['main']['temp']} °C</p>
            <p><b>Humidity:</b> {weather_data['main']['humidity']} %</p>
            <p><b>Condition:</b> {weather_data['weather'][0]['description']}</p>
            <p><b>Date:</b> {date.today()}</p>
            """
        else:
            weather_info = "<p style='color:red;'>Invalid city name</p>"

    return f"""
    <html>
    <head>
        <title>Weather Monitoring App</title>
    </head>
    <body style="font-family: Arial;">
        <h2>Weather Monitoring App</h2>

        <form method="POST">
            <input type="text" name="city" placeholder="Enter city name" required>
            <button type="submit">Get Weather</button>
        </form>

        <br>
        {weather_info}
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
