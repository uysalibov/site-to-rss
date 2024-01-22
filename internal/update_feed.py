import sqlite3
from typing import Dict, Any


def update_feed(conn: sqlite3.Connection, values: Dict[str, Any]) -> None:
    cursor = conn.cursor()
    update_query = """ UPDATE rss
              SET item = ? ,
                  title = ? ,
                  description = ?,
                  link = ?,
                  date = ?
              WHERE id = ?"""

    cursor.execute(
        update_query,
        (
            values.get("item"),
            values.get("title"),
            values.get("description"),
            values.get("link"),
            values.get("date"),
            values.get("id"),
        ),
    )
    conn.commit()
