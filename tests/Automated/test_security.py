import unittest
from unittest.mock import MagicMock, patch
from app.func.authentication import register_user, authenticate_user
from app.db.database import create_connection
import mysql.connector 

class TestUserSecurity(unittest.TestCase):
    # def setUp(self):
    #     self.connection = create_connection()
    #     self.test_user = {
    #         'username': 'test_security_user',
    #         'email': 'test@security.com',
    #         'password': 'TestPassword123!',
    #         'birth_date': '2000-01-01',
    #         'gender': 'men'
    #     }
    
    def setUp(self):
        self.connection = mysql.connector.connect(
            host='mysql',
            database='WaveForm_db',
            user='root',
            password=''
        )
        # Initialize test_user
        self.test_user = {
            'username': 'test_security_user',
            'email': 'test@security.com',
            'password': 'TestPassword123!',
            'birth_date': '2000-01-01',
            'gender': 'men'
        }
        
    def test_password_hashing(self):
        register_user(
            self.connection,
            self.test_user['username'],
            self.test_user['email'],
            self.test_user['password'],
            self.test_user['birth_date'],
            self.test_user['gender']
        )
        
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT password_hash FROM users WHERE username = %s",
            (self.test_user['username'],)
        )
        hashed_password = cursor.fetchone()[0]
        
        self.assertNotEqual(hashed_password, self.test_user['password'])
        self.assertTrue(len(hashed_password) >= 60)

    def test_password_strength(self):
        weak_passwords = [
            'short',
            'nodigits',
            'no-uppercase',
            'NO-LOWERCASE',
            '12345678',
        ]
        
        for password in weak_passwords:
            self.test_user['password'] = password
            with self.assertRaises(ValueError):
                register_user(
                    self.connection,
                    self.test_user['username'],
                    self.test_user['email'],
                    password,
                    self.test_user['birth_date'],
                    self.test_user['gender']
                )

    def test_data_integrity(self):
        register_user(
            self.connection,
            self.test_user['username'],
            self.test_user['email'],
            'ValidPass123!',
            '2000-01-01',
            'men'
        )

        with self.assertRaises(Exception) as context:
            register_user(
                self.connection,
                self.test_user['username'],  # Same username
                'different@email.com',
                'DifferentPass123!',
                '2000-01-01',
                'men'
            )
        self.assertIn("already exists", str(context.exception))

        with self.assertRaises(Exception) as context:
            register_user(
                self.connection,
                'different_username',
                self.test_user['email'],  # Same email
                'DifferentPass123!',
                '2000-01-01',
                'men'
            )
        self.assertIn("already exists", str(context.exception))
        
    def test_email_validation(self):
        invalid_emails = [
            'notanemail',
            '@nodomain',
            'no@domain.',
            'spaces in@email.com', 
            'special#@email.com'
        ]
        
        for email in invalid_emails:
            with self.assertRaises(ValueError):
                register_user(
                    self.connection,
                    'test_user',
                    email,
                    'ValidPass123!',
                    '2000-01-01',
                    'men'
                )

    def test_sql_injection_prevention(self):
        malicious_inputs = [
            "' OR '1'='1",
            "; DROP TABLE users;",
            "' UNION SELECT * FROM users--",
            "admin'--"
        ]
        
        for malicious_input in malicious_inputs:
            result = authenticate_user(
                self.connection,
                malicious_input,
                'password123'
            )
            self.assertFalse(result)

    def test_session_security(self):
        from app.func.session import user_session
        
        user_session.set_user(1, 'test_user')
        user_session.clear_session()
        
        self.assertIsNone(user_session.user_id)
        self.assertIsNone(user_session.username)

    def tearDown(self):
        if hasattr(self, 'connection') and self.connection:
            try:
                if hasattr(self, 'test_user'):
                    cursor = self.connection.cursor()
                    cursor.execute(
                        "DELETE FROM users WHERE username = %s",
                        (self.test_user['username'],)
                    )
                    self.connection.commit()
                    cursor.close()
            finally:
                self.connection.close()

if __name__ == '__main__':
    unittest.main()