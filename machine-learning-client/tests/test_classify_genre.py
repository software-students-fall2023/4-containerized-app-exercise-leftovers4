import io
import unittest
from unittest.mock import Mock, patch
import knn_classifier


class TestClassifyGenre(unittest.TestCase):
    @patch("feature_extraction.extract_features")
    @patch("knn_classifier.load_model")
    def test_successful_classification(self, mock_load_model, mock_extract_features):
        # Mocking the model's predict method
        mock_model = Mock()
        mock_model.predict.return_value = ["Rock"]
        mock_load_model.return_value = mock_model

        mock_extract_features.return_value = [0.5, 0.2, 0.3]

        audio_info = io.BytesIO(b"binary audio data").read()
        result = knn_classifier.classify_genre(audio_info, mock_load_model())

        self.assertEqual(result, "Rock")

    @patch("feature_extraction.extract_features", side_effect=ValueError)
    def test_invalid_audio_file(self, mock_extract_features):
        """
        Test the classify_genre function's response to an invalid audio file path.
        This test ensures that an exception is raised when an invalid file path is provided.
        """
        audio_data = b""
        model = Mock()

        with self.assertRaises(ValueError):
            knn_classifier.classify_genre(audio_data, model)

    @patch("feature_extraction.extract_features")
    @patch("knn_classifier.load_model")
    def test_model_prediction_error(self, mock_load_model, mock_extract_features):
        """
        Test the classify_genre function's behavior when the model's predict method raises an error.
        This test checks if the function properly handles exceptions raised during prediction.
        """

        mock_extract_features.return_value = [0.5, 0.2, 0.3]
        mock_model = Mock()
        mock_model.predict.side_effect = RuntimeError
        mock_load_model.return_value = mock_model

        audio_data = io.BytesIO(b"binary audio data").read()

        with self.assertRaises(RuntimeError):
            knn_classifier.classify_genre(audio_data, mock_load_model())
