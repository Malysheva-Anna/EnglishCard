INSERT INTO words (english_word, russian_translation, is_common)
VALUES
    ('apple', 'яблоко', TRUE),
    ('red', 'красный', TRUE),
    ('blue', 'синий', TRUE),
    ('green', 'зелёный', TRUE),
    ('house', 'дом', TRUE),
    ('book', 'книга', TRUE),
    ('cat', 'кошка', TRUE),
    ('dog', 'собака', TRUE),
    ('water', 'вода', TRUE),
    ('sun', 'солнце', TRUE)
ON CONFLICT (english_word) DO NOTHING;