# Weather App

A Flask application that looks up current weather using the OpenWeather geocoding and weather APIs.

![Application screenshot](https://github.com/user-attachments/assets/3df87561-708c-4248-99ff-0e5f7c3eecf5)

## Run locally

```bash
git clone https://github.com/ARWA044/weather-app.git
cd weather-app
python -m venv .venv
python -m pip install -r requirements.txt
```
Activate the virtual environment before installing (PowerShell: `.venv\Scripts\Activate.ps1`; Bash: `source .venv/bin/activate`). Set your own OpenWeather API key:

```bash
export OPENWEATHER_API_KEY=your_key
python 'weather app/main.py'
```

In PowerShell use `$env:OPENWEATHER_API_KEY = 'your_key'` instead of `export`. Open http://127.0.0.1:5000/.

## Security and reliability

Never commit an API key. Revoke and replace any key previously committed, including in Git history. Requests use HTTPS and timeouts; missing cities and upstream failures return appropriate HTTP errors. Wind speed is displayed in km/h. This is a local demonstration, not a production hosting configuration.
