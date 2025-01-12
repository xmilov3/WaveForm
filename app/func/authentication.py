import re
from app.db.password_utils import hash_password, verify_password

def validate_password(password):
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if not any(c.isupper() for c in password):
        raise ValueError("Password must contain uppercase letter")
    if not any(c.islower() for c in password):
        raise ValueError("Password must contain lowercase letter")
    if not any(c.isdigit() for c in password):
        raise ValueError("Password must contain digit")

def validate_email(email):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        raise ValueError("Invalid email format")

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
        if any(field is None for field in [username, email, password, birth_date, gender]):
            raise ValueError("All fields are required")
        
        validate_password(password)
        validate_email(email)
        
        cursor = connection.cursor()
        
        cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            raise Exception("Username already exists")
        
        cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            raise Exception("Email already exists")
        
        hashed_password = hash_password(password)
        query = """
            INSERT INTO users (username, email, password_hash, birth_date, gender, created_at)
            VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP())
        """
        cursor.execute(query, (username, email, hashed_password, birth_date, gender))
        connection.commit()
        return True
        
    except ValueError as e:
        print(f"Validation error: {e}")
        raise
    except Exception as e:
        print(f"Error while registering user: {e}")
        raise
    finally:
        if cursor:
            cursor.close()