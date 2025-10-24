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

    def GetOwnedGames(self, steamid):
        """
        Get a list of appids of games the user owns + free games they've played.
        https://developer.valvesoftware.com/wiki/Steam_Web_API#GetOwnedGames_(v0001)

        Params:
            steamid: number or string 'id'

        Returns:
            None if request fails
            number of games (int), dict of games{appid: total playtime}
                playtime is in minutes
        """

        url = self.url_base + "IPlayerService/GetOwnedGames/v0001/"
        params = {
                "key": self.api_key,
                "steamid": steamid,
                "include_played_free_games": True
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            # Request failed
            print(response.status_code)
            return None

        response = response.json().get('response')
        game_count = int(response.get('game_count'))
        games = response.get('games', [])
        games_filtered = {}
        for game in games:
            appid = int(game.get('appid'))
            total_playtime = int(game.get('playtime_forever'))
            games_filtered[appid] = total_playtime

        return game_count, games_filtered
