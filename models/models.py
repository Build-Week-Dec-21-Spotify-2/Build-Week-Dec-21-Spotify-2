from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import pickle
import warnings

# squelch sklearn warnings
warnings.filterwarnings("ignore", category=UserWarning)

DB = SQLAlchemy()


class Recommendations(DB.Model):
    """
    Creates a Recommendations Table with SQlAlchemy.
    This is useful for jinja2 HTML formatting in the
    'recommendations.html' file.
    """

    id = DB.Column(DB.BigInteger, primary_key=True)
    artist_song = DB.Column(DB.String, nullable=False)


def find_recommendations(input_feature_vector):
    # Load locally stored pickled model
    model = pickle.load(open('app_data/Spotify_model_new', 'rb'))

    # Read in spotify data from csv
    songs = pd.read_csv("app_data/song_artist.csv")

    # Query the model using the features from the user's
    # selected song
    # Model will return the indices of the 5 most similar
    # songs that it finds within the 100,000 rows
    _, ind = model.kneighbors([input_feature_vector])

    # Convert 'indices' output from array type to list
    ind = list(ind[0])

    id_list = [1, 2, 3, 4, 5]
    artist_song = []

    for each in ind:
        artist_song.append(songs.iloc[each]["artists_song"])

        recommendations = list(zip(id_list, artist_song))

    return recommendations
