# -*- coding: cp1251 -*-
import unittest
import os
from unittest.mock import Mock
from static.controllers.useful_articles_controller import validate_email, validate_url, validate_author, validate_title, validate_phone, validate_description, validate_image

# Тестирование функции validate_email
class TestValidateEmail(unittest.TestCase):
    def test_valid_emails(self):
        valid_emails = [
            "nikita@gmail.com",
            "nikita.stebunov@yandex.ru",
            "nikita.s@inbox.ru",
            "nikita+test@mail.ru",
            "stebunov.nikita@gmail.com",
            "nikita_stebunov123@mail.ru",
            "nik" + "a" * 61 + "@mail.ru",
            "user123@yandex.ru",
            "test.user@inbox.ru"
        ]
        for email in valid_emails:
            self.assertTrue(validate_email(email)[0], f"Email: {email} должен быть корректным")

    def test_invalid_emails(self):
        invalid_emails = [
            "",                                 # Пустая строка
            "   ",                              # Строка из пробелов
            "nikita" * 40 + "@gmail.com",       # Слишком длинный email
            "nikita",                           # Без @
            "nikita@",                          # Без домена
            "ni@gmail.com",                     # Короткая преддоменная часть
            "nikita" * 11 + "@gmail.com",       # Длинная преддоменная часть
            "nikita@com",                       # Короткая доменная часть
            "nikita@" + "a" * 191,              # Длинная доменная часть
            "nikita.stebunov@mail.com",         # Недопустимый домен
            "никита.стебунов@gmail.com",        # Русские символы
            "nikita..stebunov@gmail.com",       # Двойная точка
            "nikita#stebunov@gmail.com",        # Недопустимый символ
            "nikita@ stebunov@gmail.com",       # Пробел в домене
            "nikita@@gmail.com"                 # Две @@
        ]
        for email in invalid_emails:
            self.assertFalse(validate_email(email)[0], f"Email: {email} должен быть некорректным")

# Тестирование функции validate_url
class TestValidateUrl(unittest.TestCase):
    def test_valid_urls(self):
        valid_urls = [
            "https://www.dns-shop.ru",
            "https://www.dns-shop.ru/catalog",
            "https://www.dns-shop.ru/catalog/17a892f816404e77/noutbuki",
            "https://www.dns-shop.ru/product/123456",
            "https://www.dns-shop.ru/catalog/17a8a01d16404e77/smartfony",
            "https://www.dns-shop.ru/search?query=laptop",
            "https://www.dns-shop.ru/cart",
            "https://www.dns-shop.ru/profile/orders"
        ]
        for url in valid_urls:
            self.assertTrue(validate_url(url)[0], f"URL: {url} должен быть корректным")

    def test_invalid_urls(self):
        invalid_urls = [
            "",                                     # Пустая строка
            "   ",                                  # Строка из пробелов
            "https://www dns-shop.ru",              # Пробел в домене
            "https://www.dns-shop.ru/ catalog",     # Пробел в пути
            "http://www.dns-shop.ru",               # Неправильный протокол
            "https://dns-shop",                     # Без TLD
            "ftp://www.dns-shop.ru",                # Неправильный протокол
            "https://www.dns-shop.ru/#catalog",     # Фрагмент
            "https://www.dns-shop..ru",             # Двойная точка
            "https://www.dns-shop.ru/@catalog",     # Недопустимый символ
            "https://днс-шоп.ру",                   # Русские символы
            "https://www.dns-shop.ru:8080",         # Порт
            "https:// www.dns-shop.ru"              # Пробел перед доменом
        ]
        for url in invalid_urls:
            self.assertFalse(validate_url(url)[0], f"URL: {url} должен быть некорректным")

# Тестирование функции validate_author
class TestValidateAuthor(unittest.TestCase):
    def test_valid_authors(self):
        valid_authors = [
            "Nikita Stebunov",
            "Nikita",
            "Nikita123",
            "Stebunov Nikita",
            "Nikita S",
            "Stebunov123",
            "Nikita Stebunov123",
            "Nikita_Stebunov",
            "Nikita-Stebunov",
            "Nikita_Stebunov-123"
        ]
        for author in valid_authors:
            self.assertTrue(validate_author(author)[0], f"Author: {author} должен быть корректным")

    def test_invalid_authors(self):
        invalid_authors = [
            "",                             # Пустая строка
            "   ",                          # Строка из пробелов
            "Nikita  Stebunov",             # Двойной пробел
            "Ni",                           # Слишком короткое
            "Nikita Stebunov" * 4,          # Слишком длинное
            "Nikita@Stebunov",              # Недопустимый символ
            "N i k i t a",                  # Отдельные буквы
            "Никита Стебунов",              # Русские символы
            "N I K I T A S T E B U N O V"   # Отдельные буквы
        ]
        for author in invalid_authors:
            self.assertFalse(validate_author(author)[0], f"Author: {author} должен быть некорректным")

# Тестирование функции validate_title
class TestValidateTitle(unittest.TestCase):
    def test_valid_titles(self):
        valid_titles = [
            "How to extend the battery life?",
            "How to extend the battery life!: Tips",
            "How to extend the battery 123",
            "How to extend the battery life & more",
            "How to extend the battery life's secrets",
            "How to extend: battery life",
            "How to extend the battery life"
        ]
        for title in valid_titles:
            self.assertTrue(validate_title(title)[0], f"Title: {title} должен быть корректным")

    def test_invalid_titles(self):
        invalid_titles = [
            "",                                     # Пустая строка
            "   ",                                  # Строка из пробелов
            "How to  extend the battery life",      # Двойной пробел
            "How",                                  # Слишком короткое
            "How to extend the battery life? " * 5, # Слишком длинное
            "12345",                                # Недостаточно букв
            "How to extend the battery@life",       # Недопустимый символ
            "Как продлить жизнь батареи?",          # Русские символы
            "How to extend the battery#life"        # Недопустимый символ
        ]
        for title in invalid_titles:
            self.assertFalse(validate_title(title)[0], f"Title: {title} должен быть некорректным")

# Тестирование функции validate_phone
class TestValidatePhone(unittest.TestCase):
    def test_valid_phones(self):
        valid_phones = [
            "+71234567890",
            "+79991234567",
            "+79123456789",
            "+79876543210"
        ]
        for phone in valid_phones:
            self.assertTrue(validate_phone(phone)[0], f"Phone: {phone} должен быть корректным")

    def test_invalid_phones(self):
        invalid_phones = [
            "",                        # Пустая строка
            "   ",                     # Строка из пробелов
            "+7 123 456 7890",         # Пробелы
            "1234567890",              # Без +7
            "+71234",                  # Слишком короткий
            "+71234nikita",            # Буквы
            "+81234567890",            # Неверный код страны
            "+712345678901",           # Слишком длинный
            "+7999123456",             # Слишком короткий
            "+7 912 345 67 89"         # Пробелы в формате
        ]
        for phone in invalid_phones:
            self.assertFalse(validate_phone(phone)[0], f"Phone: {phone} должен быть некорректным")

# Тестирование функции validate_description
class TestValidateDescription(unittest.TestCase):
    def test_valid_descriptions(self):
        valid_descriptions = [
            "Nikita Stebunov wrote this description to test the validation. It has enough letters to pass.",
            "Nikita's article: Lorem ipsum dolor sit amet, consectetur adipiscing elit, authored by Stebunov.",
            "Nikita, test 123! Description by Stebunov with allowed chars.",
            "Stebunov Nikita: This is a detailed test description with enough letters to meet the requirements.",
            "Nikita Stebunov presents: A journey through testing with valid chars, numbers 123, and symbols!"
        ]
        for description in valid_descriptions:
            self.assertTrue(validate_description(description)[0], f"Description: {description} должен быть корректным")

    def test_invalid_descriptions(self):
        invalid_descriptions = [
            "",                             # Пустая строка
            "   ",                          # Строка из пробелов
            "Nikita  Stebunov",             # Слишком короткое
            "Nikita Stebunov" * 22,         # Слишком длинное
            "1234567890" * 5,               # Недостаточно букв
            "Nikita@Stebunov Description",  # Недопустимый символ
            "Никита Стебунов: Описание",    # Русские символы
            "N I K I T A S T E B U N O V",  # Недостаточно букв
            "Nikita  Stebunov description", # Двойной пробел
            "Nikita#Stebunov Test"          # Недопустимый символ
        ]
        for description in invalid_descriptions:
            self.assertFalse(validate_description(description)[0], f"Description: {description} должен быть некорректным")

# Тестирование функции validate_image
class TestValidateImage(unittest.TestCase):
    def test_valid_images(self):
        valid_image_png = Mock()
        valid_image_png.filename = "nikita.png"
        valid_image_png.content_type = 'image/png'

        valid_image_jpg = Mock()
        valid_image_jpg.filename = 'nikita.jpg'
        valid_image_jpg.content_type = 'image/jpeg'

        valid_image_jpeg = Mock()
        valid_image_jpeg.filename = "nikita.jpeg"
        valid_image_jpeg.content_type = 'image/jpeg'

        valid_image_st_png = Mock()
        valid_image_st_png.filename = "nikita_stebunov.png"
        valid_image_st_png.content_type = "image/png"

        valid_image_st_jpg = Mock()
        valid_image_st_jpg.filename = "nikita_stebunov.jpg"
        valid_image_st_jpg.content_type = "image/jpeg"

        valid_images = [
            valid_image_png,
            valid_image_jpg,
            valid_image_jpeg,
            valid_image_st_png,
            valid_image_st_jpg
        ]
        for image in valid_images:
            self.assertTrue(validate_image(image)[0], f"Image: {image.filename} должен быть корректным")

    def test_invalid_images(self):
        invalid_image_gif = Mock()
        invalid_image_gif.filename = "nikita.gif"
        invalid_image_gif.content_type = "image/gif"

        invalid_image_not_image = Mock()
        invalid_image_not_image.filename = "nikita.txt"
        invalid_image_not_image.content_type = "text/plain"

        invalid_image_no_ext = Mock()
        invalid_image_no_ext.filename = "nikita"
        invalid_image_no_ext.content_type = "image/png"

        invalid_image_empty = Mock()
        invalid_image_empty.filename = ""
        invalid_image_empty.content_type = "image/png"

        invalid_image_space = Mock()
        invalid_image_space.filename = "nikita stebunov.png"
        invalid_image_space.content_type = "image/png"

        invalid_images = [
            None,
            invalid_image_gif,
            invalid_image_not_image,
            invalid_image_no_ext,
            invalid_image_empty,
            invalid_image_space
        ]
        for image in invalid_images:
            if image is None:
                self.assertFalse(validate_image(image)[0], f"Image: None должен быть некорректным")
            else:
                self.assertFalse(validate_image(image)[0], f"Image: {image.filename} должен быть некорректным")

if __name__ == '__main__':
    unittest.main()