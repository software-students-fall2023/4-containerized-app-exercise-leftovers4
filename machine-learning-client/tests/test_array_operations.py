import numpy as np
import feature_extraction

def test_standardize_array_truncate():
    """Test if the array is correctly truncated to the specified length."""
    input_array = np.array([1, 2, 3, 4, 5])
    fixed_length = 3
    expected_output = np.array([1, 2, 3])
    assert np.array_equal(
        feature_extraction.standardize_array(input_array, fixed_length), expected_output
    )


def test_standardize_array_pad():
    """Test if the array is correctly padded to the specified length."""
    input_array = np.array([1, 2])
    fixed_length = 5
    expected_output = np.array([1, 2, 0, 0, 0])
    assert np.array_equal(
        feature_extraction.standardize_array(input_array, fixed_length), expected_output
    )


def test_standardize_array_no_change():
    """Test if the array remains unchanged when it's already the specified length."""
    input_array = np.array([1, 2, 3])
    fixed_length = 3
    assert np.array_equal(
        feature_extraction.standardize_array(input_array, fixed_length), input_array
    )
