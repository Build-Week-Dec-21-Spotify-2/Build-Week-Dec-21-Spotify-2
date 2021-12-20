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
            json formatted search results
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

        return search_response.json()['artists']['items']

    def search_track(self, track_name):
        '''queries the Spotify API and returns json
        search results

        Args:
            track (str):
                the track name to search for

        Returns:
            json formatted search results
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

        return search_response.json()['tracks']['items']

    def search_playlist(self, playlist_name):
        '''queires the Spotify API and returns json search
        results

        Args:
            playlist_name (str):
                the name of the playlist to search for

        Returns:
            json formatted search results
        '''
        search_url = BASE_API_URL + f'search?type=playlist&\
            include_external=audio&q={playlist_name}&limit=50'

        search_response = requests.get(
            search_url,
            headers={
                'authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
                }
            )

        return search_response.json()['playlists']['items']

    def get_track(self, track_id):
        '''queries the Spotify API and returns info on
        the audio track

        Args:
            track_id (str):
                the track id of the desired track

        Returns:
            json formatted track information
        '''
        track_url = BASE_API_URL + f'tracks/{track_id}'

        track_response = requests.get(
            track_url,
            headers={
                'authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
                }
            )

        return track_response.json()

    def get_track_features(self, track_id):
        '''queries the Spotify API and returns the audio
        features of a given track id

        Args:
            track_id (str):
                the Spotify track id of the desired track

        Returns:
            json formatted audio features'''
        features_url = BASE_API_URL + f'audio-features/{track_id}'

        features_response = requests.get(
            features_url,
            headers={
                'authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
        )

        return features_response.json()

    def get_playlist_tracks(self, playlist_id):
        '''queries the Spotify API and returns the tracks
        of a given playlist

        Args:
            playlist_id (str):
                the spotify id of a playlist

        Returns:
            json formated list of tracks in a playlist
        '''
        playlist_tracks_url = BASE_API_URL + f'playlists/{playlist_id}'

        features_response = requests.get(
            playlist_tracks_url,
            headers={
                'authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
        )

        return features_response.json()['tracks']['items']
