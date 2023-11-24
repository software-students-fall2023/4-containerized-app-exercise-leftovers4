"""
This module is designed to train a (KNN) classifier for music genre classification. 
It processes audio files from different genres, extracts features, and trains the KNN model 
based on these features. The script supports training on multiple genres and evaluates performance 
of the model using standard metrics like accuracy, classification report, and confusion matrix.

The script allows the user to specify the base folder path containing the genre-specific subfolders 
and the list of genres to be processed. The trained model is then saved to a file for future use.

This file is mainly meant to be run on a local system to output the trained model as training takes
significant time and resources.

Functions:
- process_music_genre: Processes audio files in a genre and returns features and labels.
- process_all_genres: Processes audio files across multiple genre folders.
- train_and_evaluate_knn: Trains the KNN classifier and evaluates its performance.

Usage:
- Run the script and input the base folder path when prompted.
- The script processes the audio files, trains the KNN model, and outputs its performance.
- The trained model is saved as 'knn_classifier.pkl'.
"""

import pickle
import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import feature_extraction


def process_music_genre(folder_path, genre):
    """
    Processes all audio files in a given genre folder.

    Parameters:
    folder_path (str): Path to the folder containing songs of a specific genre.
    genre (str): The genre label for the songs in the folder.

    Returns:
    tuple:
        - features_list (list): A list of feature arrays from each audio file.
        - labels_list (list): A list of genre labels for each audio file.
    """
    features_list = []
    labels_list = []

    for file in os.listdir(folder_path):
        if file.endswith(".wav"):
            file_path = os.path.join(folder_path, file)
            features = feature_extraction.extract_features(file_path)
            features_list.append(features)
            labels_list.append(genre)
    return features_list, labels_list


def process_all_genres(base_folder_path, genres):
    """
    Processes audio files across multiple genre folders.

    Parameters:
    base_folder_path (str): Base path to the folders containing music data.
    genres (list): List of genres to be processed.

    Returns:
    tuple:
        - all_features (list): Aggregated list of features from all genres.
        - all_labels (list): Aggregated list of genre label for features.
    """
    all_features = []
    all_labels = []

    for genre in genres:
        folder_path = os.path.join(base_folder_path, genre)
        features, labels = process_music_genre(folder_path, genre)
        all_features.extend(features)
        all_labels.extend(labels)
        print(genre, "completed!")
    return all_features, all_labels


def train_and_evaluate_knn(
    input_base_folder_path, all_genres, test_size=0.2, n_neighbors=5
):
    """
    Processes music data and trains a KNN classifier.

    Parameters:
    base_folder_path (str): Base path to the folders containing music by genre.
    genres (list): List of genres to process.
    test_size (float): Fraction of the dataset to be used as test data.
    n_neighbors (int): Number of neighbors to use for KNN.

    Returns:
    tuple: Returns the classifier and the test results.
    """
    # Process all genres for features and labels, then split into training and testing sets.
    features, labels = process_all_genres(input_base_folder_path, all_genres)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(features), np.array(labels), test_size=test_size, random_state=42
    )

    # Initialize and train the KNN classifier
    knn = KNeighborsClassifier(n_neighbors=n_neighbors)
    knn.fit(x_train, y_train)

    # Predict and evaluate the classifier
    y_pred = knn.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    confusion = confusion_matrix(y_test, y_pred)

    print("Accuracy:", accuracy)
    print("Classification Report:\n", report)
    print("Confusion Matrix:\n", confusion)

    return knn, (accuracy, report, confusion)


if __name__ == "__main__":
    genres_list = [
        "Rock",
        "Pop",
        "Jazz",
        "Classical",
        "HipHopAndRap",
        "EDM",
        "Country",
        "Reggae",
        "R&BAndSoul",
        "Disco",
    ]
    base_path = input("Enter the file path: ")

    # Train the KNN classifier and evaluate its performance
    classifier, results = train_and_evaluate_knn(base_path, genres_list)
    with open("knn_classifier.pkl", "wb") as outfile:
        pickle.dump(classifier, outfile)
