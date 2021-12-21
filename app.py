"""This app will let the user input a song and return the top 5
most similar songs using a KNN model and the Spotify API."""

from flask import Flask, render_template, request
import pandas as pd
import pickle
from spotify_api import SPOTIFY_CLIENT, SPOTIFY_SECRET, SpotifyAPI
from models import find_recommendations


app = Flask(__name__)

# Below will load the pickled-model
filename = "models/app_data/Spotify_model_new"
model = pickle.load(open(filename, 'rb'))

# construct and authenticate SpotifyAPI
spot = SpotifyAPI(SPOTIFY_CLIENT, SPOTIFY_SECRET)
spot.get_access_token()


def lazy_track_search(track_search_term):
    """retrieves the track id from the first search
    result returned

    Args:
        track_search_term (str):
            the term used to search for a track

    Returns:
        track id (str)"""
    track_id = spot.search_track(track_search_term)[0]['id']
    return track_id


def get_feature_vector(track_id):
    """retrieves and formats audio features for
    the given track id

    Args:
        track_id (str):
            Spotify track ID

    Returns:
        list of audio features
    """
    # fetch features for track id
    track_features = spot.get_track_features(track_id)

    # remove unneeded features
    track_features.pop('type')
    track_features.pop('id')
    track_features.pop('uri')
    track_features.pop('track_href')
    track_features.pop('analysis_url')

    feature_vector = list(track_features.values())

    return feature_vector


def get_similar_songs(track_search_term):
    """returns 5 closest song recomendations based on
    the first song returned for the given search term

    Args:
        track_search_term (str):
            the term used to search for spotify tracks

    Returns:
        5 most similar songs
    """
    # get track id of first search result
    track_id = lazy_track_search(track_search_term)

    # get feature vector for track_id
    feature_vector = get_feature_vector(track_id)

    # run features through knn and get recomendations
    recommendations = find_recommendations(feature_vector)

    return recommendations


@app.route('/', methods=['GET', 'POST'])
def root():
    """The home page."""

    if request.method == 'POST':
        # Extract input from form
        your_song=request.form.get("Song")
        your_artist=request.form.get("Artist")

        # Create Dataframe based on input
        # JOSHUA: FEEL FREE TO MANIPULATE BELOW TO GET IT TO WORK
        # WITH THE MODEL
        input_variables = pd.DataFrame([[your_song, your_artist]],
                                        columns=['your_song','your_artist'],
                                        index=['input']
        )
        # GET MODEL'S PREDICTION
        prediction = get_similar_songs(input_variables)


        return render_template('index.html',
                                original_input={
                                        'Song':your_song,
                                        'Artist':your_artist}
        )
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
