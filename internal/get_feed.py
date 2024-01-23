import sqlite3


def get_feed(cursor: sqlite3.Cursor, _id: int):
    select_query = "SELECT * FROM rss where id = ?"

    cursor.execute(select_query, (_id,))

    return cursor.fetchone()


def get_all_feeds(cursor: sqlite3.Cursor):
    select_query = "SELECT * FROM rss"

    cursor.execute(select_query)

    return cursor.fetchall()
