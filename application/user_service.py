from application.database_connection import get_connection


def get_or_create_user(username):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        'SELECT id FROM users WHERE username = %s',
        (username,)
    )

    user = cur.fetchone()

    if user is None:
        cur.execute(
            'INSERT INTO users (username) VALUES (%s) RETURNING id',
            (username,)
        )

        user_id = cur.fetchone()[0]

        cur.execute(
            'SELECT id FROM words WHERE is_common = TRUE'
        )

        words = cur.fetchall()

        for word in words:
            cur.execute(
                'INSERT INTO user_words (user_id, word_id) VALUES (%s, %s)',
                (user_id, word[0])
            )

        conn.commit()

    else:
        user_id = user[0]

    cur.close()
    conn.close()

    return user_id