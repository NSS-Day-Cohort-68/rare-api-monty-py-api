import sqlite3
import json


def create_comment(comment_info):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        INSERT INTO Comments (post_id, author_id, content)
        VALUES (?,?,?)
            """,
            (
                comment_info["post_id"],
                comment_info["author_id"],
                comment_info["content"],
            ),
        )

    return True if db_cursor.rowcount > 0 else False


def delete_comment(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        DELETE FROM Comments WHERE id = ?
            """,
            (pk,),
        )
    return True if db_cursor.rowcount > 0 else False
