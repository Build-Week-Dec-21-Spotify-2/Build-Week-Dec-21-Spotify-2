"""This app will let the user input a song and return the top 5
most similar songs using a KNN model and the Spotify API."""

from flask import Flask, render_template, request, Response
import pickle
from spotify_api.spotify_api import SPOTIFY_CLIENT, SPOTIFY_SECRET, SpotifyAPI
from models.models import find_recommendations
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import seaborn as sns
import numpy as np
from io import BytesIO
import base64
import os



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
                    'xtick.color': 'white',
                    'ytick.color': 'white',
                    'figure.facecolor':'black'}
    sns.set_style("whitegrid", rc=custom_style)

    # Create the plot
    fig, ax = plt.subplots(1,1)
    sns.barplot(x=ten_user_track_features, y=ten_features_names,
                    color='green',
                    orient="h",
                    ax=ax)

    # Save it to a temporary buffer.
    buf = BytesIO()
    data = FigureCanvas(fig).print_png(buf)

    fig.savefig('templates/plot.jpg', format='jpg')

    return None

    # Embed the result in the html output.
    # data = base64.b64encode(buf.getbuffer()).decode("ascii")

    # return Response(buf.getvalue(), mimetype='image/png')


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

        # get bar plot
        # plot = create_bar_graph(features_names, user_track_features)
        create_bar_graph(features_names, user_track_features)

        # with open('models/app_data/plot.png', 'wb') as img:
        #     img.write(plot)

        # img = Image.new('RGB', (x,y), "black")
        # fullpath = os.path.join(path, 'plot.png')
        # img.save(fullpath)

        return render_template(
            "recom.html", title="Recommendations",
            recommendations=recommendations,
            track_search=searched_song,
            # plot=plot
            )
    else:
        return render_template('base.html')


# @app.route('/plot.png')
# def plot_png(features_names, user_track_features):
#     """Create bar graph for /reccomendations page"""

#     response = create_bar_graph(features_names, user_track_features)
#     return response


if __name__ == "__main__":
    app.run(debug=True)
