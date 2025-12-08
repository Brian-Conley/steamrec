import re
from SteamWebAPI import instance as steamapi

STEAM64_BASE = 76561197960265728

def resolve_vanity(name):
    try:
        resp = steamapi.ResolveVanityURL(name)
    except Exception:
        return None

    if isinstance(resp, str):
        if resp.isdigit() and len(resp) >= 16:
            return resp
        return None

    if isinstance(resp, dict):
        if "response" in resp:
            resp = resp["response"]
        if resp.get("success") != 1:
            return None
        return resp.get("steamid")

    return None


def extract_steamid(raw):
    raw = str(raw).strip()

    if "steamcommunity.com" in raw:
        m = re.search(r"profiles/(\d+)", raw)
        if m:
            return m.group(1)

        m = re.search(r"id/([^/]+)", raw)
        if m:
            return resolve_vanity(m.group(1))

    if raw.isdigit():
        num = int(raw)
        if num > STEAM64_BASE:
            return str(num)
        return str(num + STEAM64_BASE)

    m = re.search(r"\[U:1:(\d+)\]", raw)
    if m:
        steam32 = int(m.group(1))
        return str(steam32 + STEAM64_BASE)

    m = re.search(r"STEAM_[0-5]:([0-1]):(\d+)", raw)
    if m:
        y = int(m.group(1))
        z = int(m.group(2))
        steam32 = z * 2 + y
        return str(steam32 + STEAM64_BASE)

    resolved = resolve_vanity(raw)
    if resolved:
        return resolved

    return None
