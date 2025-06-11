
from flask import Flask,request,render_template,redirect,url_for
from string import capwords
import datetime
import requests
Geocoding_API="http://api.openweathermap.org/geo/1.0/direct"
current_weather="https://api.openweathermap.org/data/2.5/weather"
api_key="d7c889c8af80a41b7014fee26e8ba808"
 
app=Flask(__name__)

@app.route('/home', methods=['GET','POST'])
def Home():
    if request.method == "POST":
        city=request.form.get('search')
        return redirect(url_for("get_weather",city=city))
    return render_template('index.html')

@app.route('/weather/<city>',methods=['GET','POST'])
def get_weather(city):
    now=datetime.datetime.now()
    today=now.strftime("%A, %d %B %Y  %I:%M %p")
    city_name=capwords(city)

    params={
        "q":city_name,
        "appid":api_key,
        "limit":5,
    }
    result=requests.get(Geocoding_API,params)
    location=result.json()

    weather_params={
        "lat":location[0]["lat"],
        "lon":location[0]["lon"],
        "appid":api_key
    }
    fresult=requests.get(current_weather,weather_params)
    weather_data=fresult.json()
    
    temp=weather_data["main"]["temp"]
    wind_speed=weather_data["wind"]["speed"]
    humidity=weather_data["main"]["humidity"]
    weather=weather_data["weather"][0]["main"]

    return render_template('main.html',city_name=city_name,today=today,temp=round(temp-273.15),wind_speed=wind_speed,humidity=humidity,weather=weather)

if __name__=="__main__":
    app.run(debug=True)
 
