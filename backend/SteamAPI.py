import os
import requests


class SteamAPI:
    def __init__(self):
        self.api_key = os.getenv("STEAM_API_KEY")
        if not self.api_key:
            raise ValueError("Missing STEAM_API_KEY environment variable")
        self.url_base = "https://api.steampowered.com/"

    def GetPlayerSummariesv2(self, steamid):
        """
        Get generic public information from a user's profile.
        https://developer.valvesoftware.com/wiki/Steam_Web_API#GetPlayerSummaries_(v0002)

        Params:
            steamid: One or more steamids in the following format
                id (number, singular, lists do not work)
                'id'
                'id1, id2'

        Returns:
            None if request fails
            JSON profile summary if success
        """

        url = self.url_base + "ISteamUser/GetPlayerSummaries/v0002/"
        params = {
                "key": self.api_key,
                "steamids": steamid
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            # Request failed
            return None
        return response.json()
