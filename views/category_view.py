import sqlite3
import json


def create_category(category_data):
    """
    Inserts a new category into the database.

    Args:
        category_data (dict): A dictionary containing data for the new category.
            Must include a 'label' key with the label of the category.

    Returns:
        int: The ID of the newly inserted category.
    """
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
    """
    Deletes a category from the database.

    Args:
        pk (int): The primary key (ID) of the category to delete.

    Returns:
        bool: True if the category was successfully deleted, False otherwise.
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        DELETE FROM Categories WHERE id = ?
        """,
            (pk,),
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False


def update_category(pk, category_data):
    """
    Updates an existing category in the database.

    Args:
        pk (int): The primary key (ID) of the category to update.
        category_data (dict): A dictionary containing updated data for the category.
            Must include a 'label' key with the updated label of the category.

    Returns:
        bool: True if the category was successfully updated, False otherwise.
    """

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
    """
    Retrieves all categories from a specified URL.

    Args:
        url (str): The URL from which to retrieve the categories.

    Returns:
        list: A list of dictionaries representing the categories retrieved from the URL.
    """
    if url["query_params"]:
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute(
                """
            SELECT
                c.id,
                c.label
            FROM Categories c
            """
            )
            query_results = db_cursor.fetchall()

            category = []
            for row in query_results:
                category.append(dict(row))

            serialized_categories = json.dumps(category)

        return serialized_categories
