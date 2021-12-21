"""This app will let the user input a song and return the top 5 
most similar songs using a KNN model and the Spotify API."""

from flask import Flask, render_template, request
import pandas as pd
import pickle


app = Flask(__name__)

# Below will load the pickled-model
filename = "models/app_data/Spotify_model_new"
model = pickle.load(open(filename, 'rb'))


def get_similar_songs(input_variables):
    """Use the KKN model on the user's song input."""
    # TODO: USE THE KNN MODEL TO PREDICT TOP 5 MOST
    # SIMILAR SONGS FROM THE SPOTIFY DATASET
    return None

@app.route('/', methods=['GET','POST'])
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
