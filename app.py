"""This app will let the user input a song and return the top 5 
most similar songs using a KNN model and the Spotify API."""

from flask import Flask, render_template, request
import pickle


app = Flask(__name__)

# Below will load the pickled-model
filename = "models/app_data/Spotify_model_new"
model = pickle.load(open(filename, "rb"))


def get_similar_songs(your_song):
    """Use the KKN model on the user's song input."""
    # TODO: USE THE KNN MODEL TO PREDICT TOP 5 MOST
    # SIMILAR SONGS FROM THE SPOTIFY DATASET
    return None

@app.route('/', methods=['GET','POST'])
def root():
    """The home page."""

    if request.method == 'POST':
        your_song=request.form
        return render_template('index.html', your_song=your_song)
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
