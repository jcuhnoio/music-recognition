"""
Python module for performing STFT on a wav file.
"""

import subprocess
import re
import librosa
import numpy as np

def get_mp3_bitrate(input_file):
    """
    Gets bitrate of mp3 to use for mp3 to wav conversion.
    
    Args:
    input_file: A string representing the path of the input file.
        
    Output:
    An int representing the bitrate.
    """
    command = ["ffmpeg", "-i", input_file]
    result = subprocess.run(command, stderr=subprocess.PIPE, text=True)
    match = re.search(r'Audio:.*?(\d+) kb/s', result.stderr)
    if match:
        bitrate = int(match.group(1))
        return 48000 if bitrate > 128 else 44100
    return 44100  # Default if bitrate is not found

def convert_mp3_to_wav(input_file, output_file):
    """
    Converts mp3 file to wav using ffmpeg.
    """
    sample_rate = get_mp3_bitrate(input_file)
    command = [
        "ffmpeg", "-i", input_file, "-vn", "-acodec", "pcm_s16le", 
        "-ac", "1", "-ar", str(sample_rate), "-f", "wav", output_file
    ]
    
    try:
        subprocess.run(command, check=True)
        print(f"Conversion successful: {output_file} with sample rate {sample_rate}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")

def stft(wav_file):
    """
    Using librosa, takes in a wav file and performs a STFT.
    The wav file is downsampled to 11kHz as we only need to look at frequencies
    below 5kHz (Nyquist rate). Also, the amplitudes of the Fourier coefficients
    are converted to log scale.
    
    Args:
    wav_file: String representing path of wav file
    
    Output:
    Result of STFT
    """
    y, sr = librosa.load(wav_file, sr=11025)
    
    S = np.abs(librosa.stft(y, n_fft=2048, hop_length=512))
    
    # Convert to dB
    S_db = librosa.amplitude_to_db(S, ref=np.max)
    
    return S_db
    

