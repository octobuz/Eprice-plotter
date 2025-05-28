# tests/test_api_live.py

import requests

def test_api_is_up():
    url = "https://api.porssisahko.net/v1/latest-prices.json"
    response = requests.get(url)
    
    assert response.status_code == 200
    assert "prices" in response.json()  # or adjust key as needed