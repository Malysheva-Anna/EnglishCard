import os
from pathlib import Path

import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

from database_connection import get_connection


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent


def create_database():
    db_name = os.getenv('DB_NAME')

    conn = psycopg2.connect(
        database='postgres',
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )

    conn.autocommit = True

    try:
        with conn.cursor() as cur:
            cur.execute(
                'SELECT 1 FROM pg_database WHERE datname = %s',
                (db_name,)
            )

            if cur.fetchone() is None:
                cur.execute(
                    sql.SQL('CREATE DATABASE {}').format(
                        sql.Identifier(db_name)
                    )
                )
                print('База данных создана.')
            else:
                print('База данных уже существует.')

    finally:
        conn.close()


def create_tables():
    create_tables_path = BASE_DIR / 'database' / 'create_tables.sql'
    insert_data_path = BASE_DIR / 'database' / 'insert_data.sql'

    conn = get_connection()

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    create_tables_path.read_text(encoding='utf-8')
                )

                cur.execute(
                    insert_data_path.read_text(encoding='utf-8')
                )

        print('Таблицы созданы, начальные слова добавлены.')

    finally:
        conn.close()


def initialize_database():
    create_database()
    create_tables()


if __name__ == '__main__':
    initialize_database()