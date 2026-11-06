from database_connection import get_connection


def get_user_words(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        '''
        SELECT words.id, words.english_word, words.russian_translation
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
            INSERT INTO words (english_word, russian_translation)
            VALUES (%s, %s)
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