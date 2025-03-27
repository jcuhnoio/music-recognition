import sqlite3

import sys

sys.path.insert(1, './fingerprint')

import fft
import hashing

conn = sqlite3.connect('./db/fingerprints.db')
cursor = conn.cursor()

# Assuming you've already created the table above

def insert_fingerprints(song_id, hashes):
    for h, anchor_time in hashes:
        freq1, freq2, delta_t = h
        cursor.execute(
            "INSERT INTO fingerprints (song_id, freq_anchor, freq_target, delta_t, anchor_time) VALUES (?, ?, ?, ?, ?)",
            (song_id, freq1, freq2, delta_t, anchor_time)
        )
    conn.commit()

def insert_wav(song_name, wav_file):
    cursor.execute("INSERT INTO songs (song_name) VALUES (?)", (song_name,))
    song_id = cursor.lastrowid   # get the auto-incremented song_id
    conn.commit()
    
    S_db = fft.stft(wav_file)
    peaks = hashing.get_peaks(S_db)
    hashes = hashing.generate_hashes(peaks)
    
    insert_fingerprints(song_id, hashes)
    
insert_wav('AC-DC - Back In Black', 'foo.wav')