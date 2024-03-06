import sqlite3
import json


def create_tag(tag):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        Insert into Tags (label) values (?)
        """,
            (tag["label"]),
        )
        rows_affected = db_cursor.rowcount

    return True if rows_affected > 0 else False


def delete_a_tag(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        DELETE FROM Tags WHERE id = ?
        """,
            (pk,),
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False


def edit_tag(tag_data, pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            UPDATE Tags
                SET
                    label = ?
            WHERE id = ?
            """,
            (tag_data["label"], pk),
        )

    return True if db_cursor.rowcount > 0 else False
