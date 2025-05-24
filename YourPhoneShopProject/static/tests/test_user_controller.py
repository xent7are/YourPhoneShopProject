# -*- coding: cp1251 -*-

import unittest
import os
import sys

try:
    # ������ ������b �� ������ user_controller
    from static.controllers.user_controller import validate_user_form
except ImportError as e:
    print(f"Import error: {e}")
    raise

# ���������� �������� ���������� ������� � sys.path ��� ����������� ������� �������
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class TestUserController(unittest.TestCase):
    def setUp(self):
        # ���������� ������ ��� �����������
        self.valid_data = {
            'name': 'JohnDoe',
            'email': 'john@gmail.com',
            'phone': '+79123456789',
            'birth_date': '2000-01-01'
        }
        # ������ ������������������ ������������
        self.existing_users = [
            {'name': 'JaneDoe', 'email': 'jane@gmail.com', 'phone': '+79123456788', 'birth_date': '1999-01-01'}
        ]

    # ���� �� ���� �������� � �������
    def test_birth_date_future(self):
        data = self.valid_data.copy()
        data['birth_date'] = '2025-12-01'  # ������������ ���� ��������
        errors = validate_user_form(data, file=None, existing_users=self.existing_users)
        self.assertIn("Birth Date cannot be in the future!", errors)

    # ���� �� ���� �������� � �������������� �������
    def test_birth_date_invalid_format(self):
        data = self.valid_data.copy()
        data['birth_date'] = '2000-13-01'  # ������������ ���� ��������
        errors = validate_user_form(data, file=None, existing_users=self.existing_users)
        self.assertIn("Invalid Birth Date. Please check the entered values!", errors)

    # ���� �� ����� �������� � ������������ �������
    def test_phone_invalid_format(self):
        data = self.valid_data.copy()
        data['phone'] = '12345'  # ������������ ����� ��������
        errors = validate_user_form(data, file=None, existing_users=self.existing_users)
        self.assertIn("Phone number format is invalid. Use correct format (e.g., +71234567890)!", errors)

    # ���� �� ��� ������������������ ����� ��������
    def test_phone_already_registered(self):
        data = self.valid_data.copy()
        data['phone'] = '+79123456788'  # ������������ ����� ��������
        errors = validate_user_form(data, file=None, existing_users=self.existing_users)
        self.assertIn("This phone number is already registered!", errors)

        
    # ���� �� ��� ������������������ �����
    def test_email_already_registered(self):
        data = self.valid_data.copy()
        data['email'] = 'jane@gmail.com'  # ������������ ����� �����
        errors = validate_user_form(data, file=None, existing_users=self.existing_users)
        self.assertIn("This email is already registered!", errors)

if __name__ == '__main__':
    unittest.main()