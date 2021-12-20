"""This app will let the user input a song and return the top 5 
most similar songs using a KNN model and the Spotify API."""

from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Below will load the pickled-model
# TODO: UNCOMMENT BELOW WHEN WE HAVE THE MODEL
# with open(pickled_model_name, 'rb') as file:
#     KNN_Model = pickle.load(file)

def get_similar_songs(your_song):
    """Use the KKN model on the user's song input."""
    # TODO: USE THE KNN MODEL TO PREDICT TOP 5 MOST
    # SIMILAR SONGS FROM THE SPOTIFY DATASET
    return None

@app.route('/', methods=['GET','POST'])
def root():
    """The home page."""
    your_song=request.form
    if request.method == 'POST':
        
    return render_template('index.html', your_song=your_song)


# Below will test form data on another URL, but right now
# it's not being used. Perhaps delete when we have 
# @app.route('/data', methods=['POST','GET'])
# def data():
#     """A testing page."""
#     if request.method == 'GET':
#         return f"Go back and submit your song first!"
#     if request.method == 'POST':
#         your_song = request.form
#         return render_template('data.html', your_song=your_song)