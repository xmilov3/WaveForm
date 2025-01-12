import unittest
from unittest.mock import MagicMock, patch
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.func.authentication import register_user, authenticate_user

class TestUserAuth(unittest.TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.cursor = MagicMock()
        self.connection.cursor.return_value = self.cursor

        self.test_user = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'test_password',
            'birth_date': '2000-01-01',
            'gender': 'men',
            'hashed_password': 'hashed_test_password'  # Symulate hashed password
        }

    @patch('app.func.authentication.hash_password')
    def test_pass_register_user(self, mock_hash_password):
        mock_hash_password.return_value = self.test_user['hashed_password'] # Configure mock to return hashed password
        
        self.cursor.execute.return_value = None
        self.connection.commit.return_value = None

        result = register_user(
            self.connection,
            self.test_user['username'],
            self.test_user['email'],
            self.test_user['password'],
            self.test_user['birth_date'],
            self.test_user['gender']
        )

        self.assertTrue(result)
        mock_hash_password.assert_called_once_with(self.test_user['password'])

    # Test if the function return False when not all required fields are provided
    def test_fail_register_user_missing_fields(self):
        self.cursor.execute.side_effect = Exception("All fields are required!")
        result = register_user(
            self.connection,
            self.test_user['username'],
            self.test_user['email'],
            self.test_user['password'],
            self.test_user['birth_date'],
            None
        )

        self.assertFalse(result)


    # Test if the function returns False when the user already exists
    @patch('app.func.authentication.hash_password')
    def test_fail_register_user(self, mock_hash_password):
        mock_hash_password.return_value = self.test_user['hashed_password']
        self.cursor.execute.side_effect = Exception("Duplicate entry")

        result = register_user(
            self.connection,
            self.test_user['username'],
            self.test_user['email'],
            self.test_user['password'],
            self.test_user['birth_date'],
            self.test_user['gender']
        )

        self.assertFalse(result)

    @patch('app.func.authentication.verify_password')
    def test_pass_authenticate_user(self, mock_verify_password):
        self.cursor.fetchone.return_value = {
            'user_id': 1,
            'username': self.test_user['username'],
            'password_hash': self.test_user['hashed_password']
        }
        
        mock_verify_password.return_value = True

        result = authenticate_user(
            self.connection,
            self.test_user['username'],
            self.test_user['password']
        )

        self.assertTrue(result)
        mock_verify_password.assert_called_once_with(
            self.test_user['hashed_password'],
            self.test_user['password']
        )

    def test_fail_authenticate_user(self):
        self.cursor.fetchone.return_value = None

        result = authenticate_user(
            self.connection,
            self.test_user['username'],
            'wrong_password'
        )

        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()