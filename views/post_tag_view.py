import sqlite3
import json


def create_post_tag(post_tag_info):
    """
    Creates a new post-tag relationship in the database.

    Args:
        post_tag_info (dict): A dictionary containing information about the post-tag relationship.
            Must include 'post_id' and 'tag_id' keys with the IDs of the post and tag, respectively.

    Returns:
        int: The ID of the newly created post-tag relationship.
    """
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
    """
    Deletes a post-tag relationship from the database.

    Args:
        pk (int): The primary key (ID) of the post-tag relationship to delete.

    Returns:
        bool: True if the post-tag relationship was successfully deleted, False otherwise.
    """
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
