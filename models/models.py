import pandas as pd
import warnings

# squelch sklearn warnings
warnings.filterwarnings("ignore", category=UserWarning)


def find_recommendations(model, input_feature_vector):
    # Load locally stored pickled model

    # Read in spotify data from csv
    songs = pd.read_csv("models/app_data/song_artist.csv")

    # get 5 nearest songs based on audio features provided
    _, ind = model.kneighbors([input_feature_vector])

    # Convert 'indices' output from array type to list
    ind = list(ind[0])

    id_list = [1, 2, 3, 4, 5]
    artist_song = []

    for each in ind:
        artist_song.append(songs.iloc[each]["artists_song"])

        recommendations = list(zip(id_list, artist_song))

    return recommendations
