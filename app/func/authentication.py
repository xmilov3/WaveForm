def authenticate_user(connection, username, password):
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE username = %s AND password_hash = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        cursor.close()
        
        return user is not None 
    except Exception as e:
        print(f"Error while authentication: {e}")
        return False

def register_user(connection, username, email, password, birth_date, gender):
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO users (username, email, password_hash, birth_date, gender, created_at)
            VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP())
        """
        cursor.execute(query, (username, email, password, birth_date, gender))
        connection.commit()
        return True
    except Exception as e:
        print(f"Error while registering user: {e}")
        return False
    finally:
        cursor.close()

