INSERT INTO words (english_word, russian_translation)
VALUES
    ('apple', 'яблоко'),
    ('red', 'красный'),
    ('blue', 'синий'),
    ('green', 'зелёный'),
    ('house', 'дом'),
    ('book', 'книга'),
    ('cat', 'кошка'),
    ('dog', 'собака'),
    ('water', 'вода'),
    ('sun', 'солнце')
ON CONFLICT (english_word) DO NOTHING;