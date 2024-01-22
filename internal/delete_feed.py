import sqlite3


def delete_feed(conn: sqlite3.Connection, _id: int) -> None:
    cursor = conn.cursor()
    delete_query = "DELETE FROM rss where id = ?"

    cursor.execute(delete_query, (_id,))
    conn.commit()
