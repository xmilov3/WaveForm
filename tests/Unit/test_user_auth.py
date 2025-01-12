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

        self.cursor.fetchone.return_value = None

        self.test_user = {
            'username': 'test_reg_user',
            'email': 'test_reg@example.com',
            'password': 'Test_password1',
            'birth_date': '2000-01-01',
            'gender': 'men',
            'hashed_password': 'hashed_test_password'
        }

    @patch('app.func.authentication.hash_password')
    def test_pass_register_user(self, mock_hash_password):
        mock_hash_password.return_value = self.test_user['hashed_password']
        self.cursor.fetchone.return_value = None

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

    def test_fail_register_user_missing_fields(self):
        with self.assertRaises(ValueError) as context:
            register_user(
                self.connection,
                self.test_user['username'],
                self.test_user['email'],
                self.test_user['password'],
                self.test_user['birth_date'],
                None
            )

    @patch('app.func.authentication.hash_password')
    def test_fail_register_user_duplicate(self, mock_hash_password):
        mock_hash_password.return_value = self.test_user['hashed_password']
        self.cursor.fetchone.return_value = {'username': 'test_reg_user'}

        with self.assertRaises(Exception) as context:
            register_user(
                self.connection,
                self.test_user['username'],
                self.test_user['email'],
                self.test_user['password'],
                self.test_user['birth_date'],
                self.test_user['gender']
            )
        self.assertIn("already exists", str(context.exception))

    def test_fail_register_user_invalid_email(self):
        with self.assertRaises(ValueError) as context:
            register_user(
                self.connection,
                self.test_user['username'],
                "invalid_email",
                self.test_user['password'],
                self.test_user['birth_date'],
                self.test_user['gender']
            )
        self.assertIn("Invalid email format", str(context.exception))

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