import os
import datetime
from flask import Flask, request, render_template, redirect, url_for
import requests

app = Flask(__name__)
GEOCODING_URL = "https://api.openweathermap.org/geo/1.0/direct"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.route("/")
def index():
    return redirect(url_for("Home"))

@app.route("/home", methods=["GET", "POST"])
def Home():
    if request.method == "POST":
        city = request.form.get("search", "").strip()
        if not city or len(city) > 120:
            return "Enter a valid city name.", 400
        return redirect(url_for("get_weather", city=city))
    return render_template("index.html")

@app.route("/weather/<city>")
def get_weather(city):
    key = os.environ.get("OPENWEATHER_API_KEY")
    if not key:
        return "Weather service is not configured.", 503
    try:
        response = requests.get(GEOCODING_URL, params={"q": city, "appid": key, "limit": 1}, timeout=10)
        response.raise_for_status()
        locations = response.json()
        if not locations:
            return "City not found.", 404
        location = locations[0]
        response = requests.get(WEATHER_URL, params={
            "lat": location["lat"], "lon": location["lon"], "appid": key, "units": "metric"
        }, timeout=10)
        response.raise_for_status()
        data = response.json()
        return render_template("main.html",
            city_name=location.get("name", city),
            today=datetime.datetime.now(datetime.timezone.utc).strftime("%A, %d %B %Y %H:%M UTC"),
            temp=round(data["main"]["temp"]),
            wind_speed=round(data["wind"]["speed"] * 3.6, 1),
            humidity=data["main"]["humidity"],
            weather=data["weather"][0]["main"])
    except (requests.RequestException, ValueError, KeyError, IndexError, TypeError):
        return "Weather service is temporarily unavailable.", 502

if __name__ == "__main__":
    app.run()
