"""
Python module for peak detection.
"""

from scipy.ndimage import maximum_filter
import numpy as np

# Peak picking
def get_peaks(S_db, neighborhood_size=20, threshold_db=-40):
    """
    Get peaks from a spectrogram.
    
    Args:
    S_db: ndarray that represents the spectrogram
    neighborhood_size: 
    """
    # Apply maximum filter
    local_max = maximum_filter(S_db, size=neighborhood_size) == S_db

    # Apply threshold
    detected_peaks = (S_db > threshold_db) & local_max
    
    return np.argwhere(detected_peaks)