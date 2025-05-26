import unittest
import os
import sys
from datetime import date, timedelta

try:
    # Импорт функциb из модуля user_controller
    from static.controllers.user_controller import validate_user_form
except ImportError as e:
    print(f"Import error: {e}")
    raise

# Добавление корневой директории проекта в sys.path для корректного импорта модулей
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class TestUserController(unittest.TestCase):
    def setUp(self):
        self.valid_data = {
            'name': 'John Doe',
            'email': 'john@gmail.com',
            'phone': '+79123456789',
            'birth_date': '2000-01-01'
        }
        # мнимый зарегистрированный пользователь
        self.existing_users = [
            {'name': 'JaneDoe', 'email': 'jane@gmail.com', 'phone': '+79123456788', 'birth_date': '1999-01-01'}
        ]

    # ТЕСТЫ НА НОМЕР ТЕЛЕФОНА

    # КОРРЕКТНЫЙ тест на обычный номер телефона как из формы
    def test_default_phone(self):
        data = self.valid_data.copy()
        data['phone'] = '+79123456789'  # корректный номер
        errors = validate_user_form(data, file=None, existing_users=self.existing_users)
        self.assertEqual(len(errors), 0)  # отсутствие ошибок

    # КОРРЕКТНЫЙ тест на номер телефона с пробелами
    def test_phone_with_spaces(self):
        data = self.valid_data.copy()
        data['phone'] = '+7 912 345 67 89'  # номер с пробелами
        errors = validate_user_form(data, file=None, existing_users=self.existing_users)
        self.assertEqual(len(errors), 0)  # отсутствие ошибок

    # КОРРЕКТНЫЙ тест на номер телефона со скобками и дефисами
    def test_phone_with_parentheses(self):
        data = self.valid_data.copy()
        data['phone'] = '+7(912)345-67-89'  # номер со скобками и дефисами
        errors = validate_user_form(data, file=None, existing_users=self.existing_users)
        self.assertEqual(len(errors), 0)  # отсутствие ошибок

    # КОРРЕКТНЫЙ тест на международный номер
    def test_international_phone(self):
        data = self.valid_data.copy()
        data['phone'] = '+441234567890'  # международный номер (UK)
        errors = validate_user_form(data, file=None, existing_users=self.existing_users)
        self.assertEqual(len(errors), 0)  # отсутствие ошибок

    # тест на номер телефона в некорректном формате
    def test_phone_invalid_format(self):
        data = self.valid_data.copy()
        data['phone'] = '12345'  # некорректный номер телефона
        errors = validate_user_form(data, file=None, existing_users=self.existing_users)
        self.assertIn("Invalid phone number. Example: +79123456789", errors)

    # тест на уже зарегистрированный номер телефона
    def test_phone_already_registered(self):
        data = self.valid_data.copy()
        data['phone'] = '+79123456788'  # некорректный номер телефона
        errors = validate_user_form(data, file=None, existing_users=self.existing_users)
        self.assertIn("This phone number is already registered!", errors)
    



    # ТЕСТЫ НА ДАТУ РОЖДЕНИЯ
    
    # тест на дату рождения в будущем
    def test_birth_date_future(self):
        data = self.valid_data.copy()
        data['birth_date'] = '2030-12-01'  # некорректная дата рождения
        errors = validate_user_form(data, file=None, existing_users=self.existing_users)
        self.assertIn("Birth Date cannot be in the future!", errors)

    # тест на дату рождения с несуществующим месяцем
    def test_birth_date_invalid_format(self):
        data = self.valid_data.copy()
        data['birth_date'] = '2000-13-01'  # некорректная дата рождения
        errors = validate_user_form(data, file=None, existing_users=self.existing_users)
        self.assertIn("Invalid Birth Date. Please check the entered values!", errors)

    # КОРРЕКТНЫЙ тест на минимальный допустимый возраст (ровно 14 лет)
    def test_min_age_boundary(self):
        data = self.valid_data.copy()
        today = date.today()
        min_age_date = date(today.year - 14, today.month, today.day)  # ровно 14 лет
        data['birth_date'] = min_age_date.strftime('%Y-%m-%d')
        errors = validate_user_form(data, file=None, existing_users=self.existing_users)
        self.assertEqual(len(errors), 0)  # отсутствие ошибок

    # тест на возраст на 1 день младше минимального (13 лет и 364 дня)
    def test_one_day_before_min_age(self):
        data = self.valid_data.copy()
        today = date.today()
        one_day_before = date(today.year - 14, today.month, today.day) + timedelta(days=1)  # 1 день до 14 лет
        data['birth_date'] = one_day_before.strftime('%Y-%m-%d')
        errors = validate_user_form(data, file=None, existing_users=self.existing_users)
        self.assertIn("You must be at least 14 years old to register!", errors)

    # тест на недопустимый возраст (150 лет)
    def test_max_age_boundary(self):
        data = self.valid_data.copy()
        today = date.today()
        max_age_date = date(today.year - 150, today.month, today.day)  # 150 лет
        data['birth_date'] = max_age_date.strftime('%Y-%m-%d')
        errors = validate_user_form(data, file=None, existing_users=self.existing_users)
        self.assertIn("You must be younger than 100 years to register!", errors)

    # КОРРЕКТНЫЙ тест на корректную дату високосного года (29 февраля 2000)
    def test_valid_leap_year_date(self):
        data = self.valid_data.copy()
        data['birth_date'] = '2000-02-29'  # валидная високосная дата
        errors = validate_user_form(data, file=None, existing_users=self.existing_users)
        self.assertEqual(len(errors), 0)  # отсутствие ошибок

    # тест на некорректную дату невисокосного года (29 февраля 1900)
    def test_invalid_leap_year_date(self):
        data = self.valid_data.copy()
        data['birth_date'] = '1900-02-29'  # несуществующая дата (1900 не високосный)
        errors = validate_user_form(data, file=None, existing_users=self.existing_users)
        self.assertIn("Invalid Birth Date. Please check the entered values!", errors)




    # ТЕСТЫ НА ЭЛЕКТРОННУЮ ПОЧТУ
        
    # тест на уже зарегистрированную почту
    def test_email_already_registered(self):
        data = self.valid_data.copy()
        data['email'] = 'jane@gmail.com'  # некорректный адрес почты
        errors = validate_user_form(data, file=None, existing_users=self.existing_users)
        self.assertIn("This email is already registered!", errors)

if __name__ == '__main__':
    unittest.main()
