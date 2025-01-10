from app.db.password_utils import hash_password, verify_password

def authenticate_user(connection, username, password):
    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        
        if not user or not user['password_hash']:
            return False
        
        stored_password = user['password_hash']
        
        return verify_password(stored_password, password)
            
    except Exception as e:
        print(f"Error while authentication: {e}")
        return False
    finally:
        if cursor:
            cursor.close()


def register_user(connection, username, email, password, birth_date, gender):
    cursor = None
    try:
        cursor = connection.cursor()
        hashed_password = hash_password(password)
        query = """
            INSERT INTO users (username, email, password_hash, birth_date, gender, created_at)
            VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP())
        """
        cursor.execute(query, (username, email, hashed_password, birth_date, gender))
        connection.commit()
        return True
    except Exception as e:
        print(f"Error while registering user: {e}")
        return False
    finally:
        if cursor:
            cursor.close()