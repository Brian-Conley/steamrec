import requests

base_url = "https://store.steampowered.com/api/appdetails"
base_url_steamspy = "https://steamspy.com/api.php?request=appdetails&appid="


def get_steam_app_details(appid):
    params = {"appids": appid}

    res = requests.get(base_url, params=params)
    if res.status_code != 200:
        return None

    return res.json()


def get_steam_app_details_steamspy(appid):
    res = requests.request(method="GET", url=f"{base_url_steamspy}{appid}")
    if res.status_code != 200:
        return {"success": False,
                "status": res.status_code,
                "message": f"HTTP request failed: {res.status_code}"
                }

    try:
        data = res.json()
    except ValueError:
        return {"success": False,
                "status": -1,
                "message": "Empty/Invalid JSON response"
                }

    req_appid = data.get("appid", -1)
    if int(req_appid) != appid:
        return {"success": False,
                "status": res.status_code,
                "message": f"Different appid: Expected {appid}, got {req_appid}"
                }

    developers = [d.strip() for d in data.get("developer", "").split(',')]
    publishers = [p.strip() for p in data.get("publisher", "").split(',')]
    tags_raw = list(data.get("tags", {}))
    if isinstance(tags_raw, dict):
        tags = list(tags_raw.keys())
    elif isinstance(tags_raw, list):
        tags = tags_raw
    else:
        tags = []
    positive = int(data.get("positive", -1))
    negative = int(data.get("negative", -1))
    total = positive + negative
    if positive < 0 or negative < 0:
        total = -1

    return {
            "success": True,
            "status": res.status_code,
            "message": f"Info for {appid} fetched successfully",
            "developers": developers,
            "publishers": publishers,
            "tags": tags,
            "reviews_positive": positive,
            "reviews_negative": negative,
            "reviews_total": total
            }
