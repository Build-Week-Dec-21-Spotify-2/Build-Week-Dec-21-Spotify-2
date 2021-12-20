from os import getenv
import requests

# Spotify API Credentials
SPOTIFY_CLIENT = getenv('SPOTIFY_CLIENT')
SPOTIFY_SECRET = getenv('SPOTIFY_SECRET')

# # Spotify API URL paths
AUTH_URL = 'https://accounts.spotify.com/api/token'
BASE_API_URL = 'https://api.spotify.com/v1/'


class SpotifyApi():
    '''establish access to the spotify api and perform search queries.

    How To:
    - construct the object with the client id and client secret for
    your spotify app

    - call .get_access_token() to authenticate your connection

    - call one of the search methods to retrieve search results in
    json format
    '''
    def __init__(self, client_id, client_secret):
        '''SpotifyAPI constructor

        Args:
            client_id (str):
                Spotify client id
            client_secret (str):
                Spotify client secret
        '''
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = ""

    def get_access_token(self):
        '''Acquires an access token to access the
        Spotify API

        Returns:
            (str) Spotify access token
        '''
        # request access token from Spotify
        access_request = requests.post(
            AUTH_URL,
            data={
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'client_credentials'
                }
            )

        # try to save access token to access_token (str). If this
        # fails, it will return am exception(KeyError).
        try:
            self.access_token = access_request.json()['access_token']

        except KeyError as err:
            print("Unable to obtain access key: ", err)
            print("For some reason, no access key was granted. \
                  This could be due invalid credentials, or an \
                  issue connecting the the authorization url")

        return self.access_token

    def search_artist(self, artist):
        '''queries the Spotify API and returns json
        search results

        Args:
            artist (str):
                the artist name to search for

        Returns:
            json search results
        '''
        search_url = BASE_API_URL + f'search?type=artist&\
            include_external=audio&q={artist}&limit=50'

        search_response = requests.get(
            search_url,
            headers={
                'authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
                }
            )

        return search_response.json()

    def search_track(self, track_name):
        '''queries the Spotify API and returns json
        search results

        Args:
            track (str):
                the track name to search for

        Returns:
            json search results
        '''
        search_url = BASE_API_URL + f'search?type=track&\
            include_external=audio&q={track_name}&limit=50'

        search_response = requests.get(
            search_url,
            headers={
                'authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
                }
            )

        return search_response.json()
