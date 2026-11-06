CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS words (
    id SERIAL PRIMARY KEY,
    english_word VARCHAR(100) NOT NULL UNIQUE,
    russian_translation VARCHAR(100) NOT NULL,
    is_common BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS user_words (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    word_id INTEGER NOT NULL REFERENCES words(id),
    UNIQUE (user_id, word_id)
);