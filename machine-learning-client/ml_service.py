import pickle
import os
from flask import Flask, request, jsonify
from feature_extraction import extract_features

app = Flask(__name__)

script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, 'knn_classifier.pkl')
with open('model_path', 'rb') as file:
    model = pickle.load(file)

@app.route('/classify', methods=['POST'])
def classify_audio():
    """
    API endpoint to classify the genre of an uploaded audio file.

    This function handles POST requests for an audio file. It extracts
    features from the audio, predicts the genre using the pre-trained KNN model, 
    and returns the genre prediction in JSON format.

    The audio file should be included in the request's files with the key 'audioFile'.

    Returns:
        On success: A JSON response containing the predicted genre.
        On failure: A JSON response with an error message, if the 'audioFile' key is not found.
    """
    if 'audioFile' in request.files:
        audio_file = request.files['audioFile']

        # Process the audio file
        features = extract_features(audio_file)
        features_reshaped = features.reshape(1, -1)
        genre_prediction = model.predict(features_reshaped)

        return jsonify({'genre': genre_prediction[0]})

    return "No audio file found", 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
