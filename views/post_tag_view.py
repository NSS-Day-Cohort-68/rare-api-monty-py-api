import sqlite3
import json


def create_post_tag(post_tag_info):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        INSERT INTO PostTags(post_id, tag_id)
        VALUES(?,?)
            """,
            (post_tag_info["post_id"], post_tag_info["tag_id"]),
        )

        rows_affected = db_cursor.rowcount

    return True if rows_affected > 0 else False


def delete_post_tag(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        DELETE FROM PostTags WHERE id = ?
            """,
            (pk,),
        )

        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False
