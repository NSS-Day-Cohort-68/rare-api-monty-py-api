import sqlite3

def get_all_posts():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

    db_cursor.execute(
        """ 
        SELECT *
        FROM Posts p
        JOIN User u ON u.id = p.user_id
        JOIN Categories c ON c.id = p.category_id
        """
    )
    posts = []
    query_results = db_cursor.fetchall()

    for row in query_results:


def get_user_post():

def create_post():

def edit_post():

# join postReactions, postTags, comments