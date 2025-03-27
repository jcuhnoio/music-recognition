CREATE TABLE IF NOT EXISTS songs (
    song_id INTEGER PRIMARY KEY AUTOINCREMENT,
    song_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fingerprints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    song_id INTEGER NOT NULL,
    freq_anchor INTEGER NOT NULL,
    freq_target INTEGER NOT NULL,
    delta_t INTEGER NOT NULL,
    anchor_time INTEGER NOT NULL
);

CREATE INDEX idx_hash ON fingerprints(freq_anchor, freq_target, delta_t);
