import importlib.util
import sys
from pathlib import Path
from unittest.mock import Mock
import requests
import pytest

@pytest.fixture
def module(monkeypatch):
    path = Path(__file__).resolve().parents[1] / "weather app" / "main.py"
    spec = importlib.util.spec_from_file_location("weather_main", path)
    mod = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, spec.name, mod)
    spec.loader.exec_module(mod)
    return mod

def test_missing_key(module, monkeypatch):
    monkeypatch.delenv("OPENWEATHER_API_KEY", raising=False)
    assert module.app.test_client().get("/weather/Casablanca").status_code == 503

def test_empty_search(module):
    assert module.app.test_client().post("/home", data={"search": " "}).status_code == 400

def test_city_not_found(module, monkeypatch):
    monkeypatch.setenv("OPENWEATHER_API_KEY", "test-only")
    response = Mock()
    response.json.return_value = []
    monkeypatch.setattr(module.requests, "get", Mock(return_value=response))
    assert module.app.test_client().get("/weather/Unknown").status_code == 404

def test_timeout(module, monkeypatch):
    monkeypatch.setenv("OPENWEATHER_API_KEY", "test-only")
    monkeypatch.setattr(module.requests, "get", Mock(side_effect=requests.Timeout))
    assert module.app.test_client().get("/weather/Casablanca").status_code == 502

def test_success(module, monkeypatch):
    monkeypatch.setenv("OPENWEATHER_API_KEY", "test-only")
    geo, weather = Mock(), Mock()
    geo.json.return_value = [{"lat": 33.5, "lon": -7.6, "name": "Casablanca"}]
    weather.json.return_value = {"main": {"temp": 20, "humidity": 70}, "wind": {"speed": 2}, "weather": [{"main": "Clear"}]}
    get = Mock(side_effect=[geo, weather])
    monkeypatch.setattr(module.requests, "get", get)
    response = module.app.test_client().get("/weather/Casablanca")
    assert response.status_code == 200
    assert b"7.2" in response.data
    assert all(call.kwargs["timeout"] == 10 for call in get.call_args_list)
