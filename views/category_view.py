import sqlite3
import json


def create_category(category_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            INSERT INTO Categories (label)
            VALUES (?)
            """,
            (category_data["label"],),
        )

        new_category_id = db_cursor.lastrowid

    return new_category_id


def delete_category(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        DELETE FROM Categories WHERE id = ?
        """,
            (pk,),
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False


# Might need to fix??
def update_category(pk, category_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            UPDATE Categories
                SET
                    label = ?
            WHERE id = ?
            """,
            (category_data["label"], pk),
        )

    return True if db_cursor.rowcount > 0 else False


def get_all_categories(url):
    # Open a connection to the database\
    if url["query_params"]:
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Write the SQL query to get the information you want
            db_cursor.execute(
                """
            SELECT
                c.id,
                c.label
            FROM Categories c
            """
            )
            query_results = db_cursor.fetchall()

            # Initialize an empty list and then add each dictionary to it
            category = []
            for row in query_results:
                category.append(dict(row))

            # Serialize Python list to JSON encoded string
            serialized_categories = json.dumps(category)

        return serialized_categories
