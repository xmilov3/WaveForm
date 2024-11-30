def authenticate_user(connection, username, password):
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE username = %s AND password_hash = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        cursor.close()
        
        return user is not None 
    except Exception as e:
        print(f"Błąd podczas autoryzacji: {e}")
        return False

def register_user(connection, username, password):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(query, (username, password))
        connection.commit()
        return True
    except Exception as e:
        print(f"Error while registering user: {e}")
        return False
    finally:
        cursor.close()
