"""This app will let the user input a song and return the top 5
most similar songs using a KNN model and the Spotify API."""

from flask import Flask, render_template, request
import pickle
from spotify_api.spotify_api import SPOTIFY_CLIENT, SPOTIFY_SECRET, SpotifyAPI
from models.models import find_recommendations
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


app = Flask(__name__)

# Below will load the pickled-model
filename = "models/app_data/Spotify_model_new"
knn_model = pickle.load(open(filename, 'rb'))

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
    track_id = spot.search_track(track_search_term)

    if len(track_id):
        track_id = track_id[0]['id']
    else:
        track_id = "7KXjTSCq5nL1LoYtL7XAwS"

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
    feature_names = list(track_features.keys())

    return feature_names, feature_vector


def get_similar_songs(model, track_id):
    """returns 5 closest song recomendations based on
    the first song returned for the given search term

    Args:
        model (obj):
            model object from loaded pickle
        track_search_term (str):
            the term used to search for spotify tracks

    Returns:
        5 most similar songs
    """
    # get feature vector for track_id
    _, feature_vector = get_feature_vector(track_id)

    # run features through knn and get recomendations
    recommendations = find_recommendations(model, feature_vector)

    return recommendations


def create_bar_graph(feature_names, user_track_features):
    """returns a bar graph shwoing track features
    based on the user inputted track

    Args:
        features_names (list):
            list of track feature names
        user_track_features:
            list of user inputted track features

    Returns:
        Bar graph showing track features
    """
    # Get first 10 features (the final 3 skew the graph dimensions)
    ten_features_names = feature_names[:-3]
    ten_user_track_features = user_track_features[:-3]

    # Take the log of loudness to help with scale
    ten_features_names[3] = 'relative loudness'
    ten_user_track_features[3] = np.log(-ten_user_track_features[3])

    # Customize the figure
    custom_style = {'axes.labelcolor': 'white',
                    'axes.facecolor': '#181818',
                    'grid.color': '#181818',
                    'xtick.color': 'white',
                    'ytick.color': 'white',
                    'figure.facecolor': '#181818',
                    'font-family': 'roboto'}
    sns.set_style(rc=custom_style)

    # Create the plot
    fig, ax = plt.subplots(1, 1, figsize=(4, 3))
    ax = sns.barplot(x=ten_user_track_features, y=ten_features_names,
                     color='#64D764',
                     orient="h",
                     ax=ax)

    ax.set_yticklabels(ax.get_yticklabels(),
                       fontname='roboto',
                       fontsize=9,
                       weight='bold')
    plt.xticks(fontsize=9, weight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.savefig('static/plot.png', format='png', bbox_inches="tight")

    return None


@app.route("/", methods=["GET", "POST"])
def root():
    """Base view"""

    return render_template("base.html", title="Song Recommender")


@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    """The home page."""

    if request.method == 'POST':
        # Extract input from form
        searched_song = request.form.get("track_search")

        # search spotify for users song, and get the first returned track id
        user_track_id = lazy_track_search(searched_song)

        # get recomendations using users track id
        recommendations = get_similar_songs(knn_model, user_track_id)

        # getting information for graph
        features_names, user_track_features = get_feature_vector(user_track_id)

        # save bar plot
        create_bar_graph(features_names, user_track_features)

        # build spotify embed link (spliting link for PEP8 line length)
        spotify_embed_url = "https://open.spotify.com/embed/track/" + \
            f"{user_track_id}?utm_source=generator&theme=0"

        return render_template(
            "recom.html", title="Recommendations",
            recommendations=recommendations,
            track_search=searched_song,
            spotify_embed_url=spotify_embed_url
            )
    else:
        return render_template('base.html')


if __name__ == "__main__":
    app.run(debug=True)
