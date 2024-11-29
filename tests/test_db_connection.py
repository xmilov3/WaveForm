from app.db.database import create_connection

connection = create_connection()
if connection:
    cursor = connection.cursor()
    cursor.execute("SELECT DATABASE();")
    print("Current database:", cursor.fetchone())
    connection.close()
