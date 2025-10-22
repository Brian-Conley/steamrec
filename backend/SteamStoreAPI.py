import requests


def get_steam_app_details(appid):
    base_url = "https://store.steampowered.com/api/appdetails"
    params = {"appids": appid}

    res = requests.get(base_url, params=params)
    if res.status_code != 200:
        return None

    return res.json()
