import mysql.connector
from app.db.song_operations import insert_song


def some_function():
    from app.func.session import user_session
    print(user_session.user_id)
