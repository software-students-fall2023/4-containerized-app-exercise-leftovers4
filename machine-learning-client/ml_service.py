"""
This module periodically accesses a MongoDB database to classify unclassified
audio files using a pre-trained KNN model. It is designed to run continuously,
checking the database at regular intervals for audio files that have not been
classified and updating their genre using the KNN model.

The script loads a pre-trained KNN model from a file and establishes a connection
with the MongoDB database. It then iteratively processes unclassified audio files:
it retrieves the binary audio data from each file, uses the `feature_extraction`
module to extract features from the audio, applies the KNN model to predict the
genre, and updates the database record with the predicted genre.

This script is intended to run as a background process, periodically
waking up to check for new unclassified audio files in the database.

Usage Instructions:
- Ensure the MongoDB database is accessible and contains audio data.
- The script assumes environment variables for MongoDB connection are set.
- Run the script; it will periodically classify audio files in the database.
"""


import os
import time
import knn_classifier
from pymongo import MongoClient

# Load the model
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
valid_model_path = os.path.join(parent_dir, "knn_classifier.pkl")
model = knn_classifier.load_model(valid_model_path)

# Database connection
client = MongoClient(os.getenv("MONGODB_URI"))
database = client[os.getenv("MONGODB_DATABASE")]
collection = database[os.getenv("MONGODB_COLLECTION")]


def classify_undetermined():
    """Fetch and classify audio files from the database that haven't been classified."""
    unclassified = collection.find({"genre": {"$exists": False}})
    for audio in unclassified:
        genre = knn_classifier.classify_genre(audio['audio_data'], model)
        collection.update_one({"_id": audio["_id"]}, {"$set": {"genre": genre}})


if __name__ == "__main__":
    while True:
        classify_undetermined()
        time.sleep(30)  # wait for 30 seconds before checking again
