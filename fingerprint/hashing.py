"""
Python module for peak detection and hashing.
"""

from scipy.ndimage import maximum_filter
import numpy as np

# Peak picking
def get_peaks(S_db, neighborhood_size=20, threshold_db=-40):
    """
    Get peaks from a spectrogram.
    
    Args:
    S_db: ndarray that represents the spectrogram.
    neighborhood_size: Number of points to select a peak from.
    threshold_db: Threshold for a point to be a peak.
    
    Returns:
    An ndarray that represents peaks as boolean values.
    """
    # Apply maximum filter
    local_max = maximum_filter(S_db, size=neighborhood_size) == S_db

    # Apply threshold
    detected_peaks = (S_db > threshold_db) & local_max
    
    return np.argwhere(detected_peaks)
    
def generate_hashes(peaks, fan_value=15, min_delta=0, max_delta=200):
    """
    Generate hashes from peak pairs.
    
    Args:
    peaks: list of (freq_bin, time_bin)
    fan_value: how many targets to connect to each anchor
    min_delta: minimum time separation (in frames)
    max_delta: maximum time separation (in frames)
    
    Returns:
    A list containint hashes from peak pairs.
    """

    hashes = []

    for i in range(len(peaks)):
        anchor_freq, anchor_time = peaks[i]

        # look ahead to next fan_value peaks
        for j in range(1, fan_value + 1):
            if i + j < len(peaks):
                target_freq, target_time = peaks[i + j]
                delta_t = target_time - anchor_time

                if min_delta <= delta_t <= max_delta:
                    h = (anchor_freq, target_freq, delta_t)
                    hashes.append((h, anchor_time))

    return hashes
