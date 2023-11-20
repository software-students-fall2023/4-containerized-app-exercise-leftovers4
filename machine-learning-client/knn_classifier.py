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
        with open(model_path, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"No model file found at specified path: {model_path}") from exc
    except Exception as e:
        raise RuntimeError(f"Error loading model from file: {e}") from e

def classify_genre(audio_path, model):
    """
    Classify the genre of an audio file using a pre-trained model.

    This function extracts features from the given audio file and uses the
    provided model to predict the genre of the audio.

    Parameters:
    audio_path (str): The file path of the audio recording to be classified.
    model (object): The trained machine learning model used for classification.

    Returns:
    str: The predicted genre of the audio file.
    """
    features = feature_extraction.extract_features(audio_path)

    features_reshaped = np.array(features).reshape(1, -1)

    genre_prediction = model.predict(features_reshaped)

    return genre_prediction[0]

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(script_dir, 'knn_classifier.pkl')
    knn_model = load_model(MODEL_PATH)

    # Path to new audio
    PATH_TO_AUDIO = input("Enter the audio recording path: ")

    # Classify the genre of the audio file
    predicted_genre = classify_genre(PATH_TO_AUDIO, knn_model)
    print("Predicted Genre:", predicted_genre)
