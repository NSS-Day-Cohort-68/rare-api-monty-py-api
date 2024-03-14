import sqlite3
import json


def get_all_posts():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

    db_cursor.execute(
        """ 
    SELECT 
        p.id,
        p.user_id,
        p.category_id,
        p.title,
        p.publication_date,
        p.image_url,
        p.content,
        p.approved,
        c.label,
        u.first_name,
        u.last_name
    FROM Posts p
    JOIN Users u ON u.id = p.user_id
    JOIN Categories c ON c.id = p.category_id
    """
    )
    posts = []
    query_results = db_cursor.fetchall()
    for row in query_results:
        post = {
            "id": row["id"],
            "title": row["title"],
            "publication_date": row["publication_date"],
            "image_url": row["image_url"],
            "content": row["content"],
            "approved": row["approved"],
            "user_id": row["user_id"],
            "category_id": row["category_id"],
        }
        post["category"] = {"id": row["category_id"], "label": row["label"]}
        post["user"] = {
            "id": row["user_id"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
        }
        posts.append(post)
    serialized_posts = json.dumps(posts)
    return serialized_posts


def get_user_posts(userId):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

    db_cursor.execute(
        """ 
        SELECT 
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved, 
            c.label,
            u.first_name,
            u.last_name
        FROM Posts p
        JOIN Users u ON u.id = p.user_id
        JOIN Categories c ON c.id = p.category_id
        WHERE p.user_id = ?
        ORDER BY p.publication_date DESC
        """,
        (userId,),
    )
    posts = []
    query_results = db_cursor.fetchall()

    for row in query_results:
        post = {
            "id": row["id"],
            "title": row["title"],
            "publication_date": row["publication_date"],
            "image_url": row["image_url"],
            "content": row["content"],
            "approved": row["approved"],
            "user_id": row["user_id"],
            "category_id": row["category_id"],
        }
        post["category"] = {"id": row["category_id"], "label": row["label"]}
        post["user"] = {
            "id": row["user_id"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
        }
        posts.append(post)
    serialized_posts = json.dumps(posts)
    return serialized_posts


def get_post_by_id(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        SELECT 
            p.title,
            p.image_url,
            p.content,
            p.publication_date,
            u.first_name,
            u.last_name
        FROM Posts p
        JOIN users u ON p.user_id = u.id
        WHERE p.id = ?
            """,
            (pk,),
        )
        query_results = db_cursor.fetchall()

        post = []

        for row in query_results:
            single_post = {
                "post_title": row["title"],
                "post_image_url": row["image_url"],
                "post_content": row["content"],
                "post_date": row["publication_date"],
                "post_author": {
                    "author_first_name": row["first_name"],
                    "author_last_name": row["last_name"],
                },
            }

            post.append(single_post)

        serialized_post = json.dumps(post)

    return serialized_post


def delete_post(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """ 
            DELETE FROM Posts
            WHERE id = ?
            """,
            (pk,),
        )

        return True if db_cursor.rowcount > 0 else False


def edit_post(pk, data):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

    db_cursor.execute(
        """ 
        UPDATE Posts
            SET
                category_id = ?,
                title = ?,
                image_url = ?,
                content = ?,
        WHERE id = ?
        """,
        (data["category_id"], data["title"], data["image_url"], data["content"], pk),
    )
    return True if db_cursor.rowcount > 0 else False


def create_post(x):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """ 
            INSERT INTO Posts (user_id, category_id, title, publication_date, image_url, content, approved)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                x["user_id"],
                x["category_id"],
                x["title"],
                x["publication_date"],
                x["image_url"],
                x["content"],
                x["approved"],
            ),
        )
    postId = db_cursor.lastrowid
    return json.dumps({"id": postId}) if db_cursor.rowcount > 0 else False
