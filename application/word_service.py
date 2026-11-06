from application.database_connection import get_connection
import random


def get_user_words(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        '''
        SELECT
            words.id,
            words.english_word,
            words.russian_translation,
            words.is_common
        FROM words
        JOIN user_words ON words.id = user_words.word_id
        WHERE user_words.user_id = %s
        ''',
        (user_id,)
    )

    words = cur.fetchall()

    cur.close()
    conn.close()

    return words


def add_word(user_id, english_word, russian_translation):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        'SELECT id FROM words WHERE english_word = %s',
        (english_word,)
    )

    word = cur.fetchone()

    if word is None:
        cur.execute(
            '''
            INSERT INTO words (english_word, russian_translation, is_common)
            VALUES (%s, %s, FALSE)
            RETURNING id
            ''',
            (english_word, russian_translation)
        )

        word_id = cur.fetchone()[0]

    else:
        word_id = word[0]

    cur.execute(
        '''
        SELECT id FROM user_words
        WHERE user_id = %s AND word_id = %s
        ''',
        (user_id, word_id)
    )

    if cur.fetchone() is None:
        cur.execute(
            '''
            INSERT INTO user_words (user_id, word_id)
            VALUES (%s, %s)
            ''',
            (user_id, word_id)
        )

    conn.commit()
    cur.close()
    conn.close()


def delete_word(user_id, word_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        '''
        DELETE FROM user_words
        WHERE user_id = %s AND word_id = %s
        ''',
        (user_id, word_id)
    )

    conn.commit()
    cur.close()
    conn.close()


def get_random_word(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        '''
        SELECT words.id, words.english_word, words.russian_translation
        FROM words
        JOIN user_words ON words.id = user_words.word_id
        WHERE user_words.user_id = %s
        ORDER BY RANDOM()
        LIMIT 1
        ''',
        (user_id,)
    )

    word = cur.fetchone()

    cur.close()
    conn.close()

    return word


def get_answer_options(user_id, correct_word_id):
    words = get_user_words(user_id)

    other_words = [
        word for word in words
        if word[0] != correct_word_id
    ]

    wrong_answers = random.sample(other_words, 3)

    options = [word[1] for word in wrong_answers]
    options.append(
        next(
            word[1] for word in words
            if word[0] == correct_word_id
        )
    )

    random.shuffle(options)

    return options


def check_answer(correct_word_id, selected_answer, user_id):
    words = get_user_words(user_id)

    for word in words:
        if word[0] == correct_word_id:
            return word[1] == selected_answer

    return False