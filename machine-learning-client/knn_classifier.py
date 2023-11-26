"""
This module includes functionality for loading a pre-trained K-Nearest Neighbors (KNN) 
machine learning model and classifying the genre of an audio file using that model. It 
contains two primary functions: `load_model` to load the trained KNN model from a file, 
and `classify_genre` to predict the genre of a given audio file. The module also 
includes a main script section that tests the classify function given an example file.

The `load_model` function handles the loading of the model and ensures that appropriate 
errors are raised in case of issues like the model file not being found. The `classify_genre`
function integrates feature extraction (using an external module `feature_extraction`) and 
the model's prediction capabilities to determine the music genre of an audio file.
"""

import pickle
import os
import numpy as np
import feature_extraction


def load_model(model_path):
    """
    Load a pre-trained KNN model from the specified file.

    Parameters:
    model_path (str): The file path where the trained model is stored.

    Returns:
    object: The loaded model object, ready for making predictions.
    """
    try:
        with open(model_path, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"No model file found at specified path: {model_path}"
        ) from exc
    except Exception as e:
        raise RuntimeError(f"Error loading model from file: {e}") from e


# def classify_genre(audio_path, model):
#     """
#     Classify the genre of an audio file using a pre-trained model.

#     This function extracts features from the given audio file and uses the
#     provided model to predict the genre of the audio.

#     Parameters:
#     audio_path (str): The file path of the audio recording to be classified.
#     model (object): The trained machine learning model used for classification.

#     Returns:
#     str: The predicted genre of the audio file.
#     """
#     features = feature_extraction.extract_features(audio_path)

#     features_reshaped = np.array(features).reshape(1, -1)

#     genre_prediction = model.predict(features_reshaped)

#     return genre_prediction[0]


def classify_genre(audio_data, model):
    """
    Classify the genre of an audio data using a pre-trained model.

    Parameters:
    audio_data (bytes): Binary audio data.
    model (object): The trained machine learning model used for classification.

    Returns:
    str: The predicted genre of the audio data.
    """
    features = feature_extraction.extract_features(audio_data)
    features_reshaped = np.array(features).reshape(1, -1)
    genre_prediction = model.predict(features_reshaped)
    return genre_prediction[0]


# if __name__ == "__main__":
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     MODEL_PATH = os.path.join(script_dir, "knn_classifier.pkl")
#     knn_model = load_model(MODEL_PATH)

#     # Path to new audio
#     PATH_TO_AUDIO = input("Enter the audio recording path: ")

#     # Classify the genre of the audio file
#     # predicted_genre = classify_genre(PATH_TO_AUDIO, knn_model)
#     # print("Predicted Genre:", predicted_genre)

#     with open(PATH_TO_AUDIO, "rb") as file_input:
#         audio_info = file_input.read()

#     predicted_genre = classify_genre(audio_info, knn_model)

#     print("Predicted Genre:", predicted_genre)
