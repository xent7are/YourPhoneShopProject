# -*- coding: cp1251 -*-
import unittest
import os
from unittest.mock import Mock
from static.controllers.useful_articles_controller import validate_email, validate_url, validate_author, validate_title, validate_phone, validate_description, validate_image

# ������������ ������� validate_email
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
            self.assertTrue(validate_email(email)[0], f"Email: {email} ������ ���� ����������")

    def test_invalid_emails(self):
        invalid_emails = [
            "",                                 # ������ ������
            "   ",                              # ������ �� ��������
            "nikita" * 40 + "@gmail.com",       # ������� ������� email
            "nikita",                           # ��� @
            "nikita@",                          # ��� ������
            "ni@gmail.com",                     # �������� ������������ �����
            "nikita" * 11 + "@gmail.com",       # ������� ������������ �����
            "nikita@com",                       # �������� �������� �����
            "nikita@" + "a" * 191,              # ������� �������� �����
            "nikita.stebunov@mail.com",         # ������������ �����
            "������.��������@gmail.com",        # ������� �������
            "nikita..stebunov@gmail.com",       # ������� �����
            "nikita#stebunov@gmail.com",        # ������������ ������
            "nikita@ stebunov@gmail.com",       # ������ � ������
            "nikita@@gmail.com"                 # ��� @@
        ]
        for email in invalid_emails:
            self.assertFalse(validate_email(email)[0], f"Email: {email} ������ ���� ������������")

# ������������ ������� validate_url
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
            self.assertTrue(validate_url(url)[0], f"URL: {url} ������ ���� ����������")

    def test_invalid_urls(self):
        invalid_urls = [
            "",                                     # ������ ������
            "   ",                                  # ������ �� ��������
            "https://www dns-shop.ru",              # ������ � ������
            "https://www.dns-shop.ru/ catalog",     # ������ � ����
            "http://www.dns-shop.ru",               # ������������ ��������
            "https://dns-shop",                     # ��� TLD
            "ftp://www.dns-shop.ru",                # ������������ ��������
            "https://www.dns-shop.ru/#catalog",     # ��������
            "https://www.dns-shop..ru",             # ������� �����
            "https://www.dns-shop.ru/@catalog",     # ������������ ������
            "https://���-���.��",                   # ������� �������
            "https://www.dns-shop.ru:8080",         # ����
            "https:// www.dns-shop.ru"              # ������ ����� �������
        ]
        for url in invalid_urls:
            self.assertFalse(validate_url(url)[0], f"URL: {url} ������ ���� ������������")

# ������������ ������� validate_author
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
            self.assertTrue(validate_author(author)[0], f"Author: {author} ������ ���� ����������")

    def test_invalid_authors(self):
        invalid_authors = [
            "",                             # ������ ������
            "   ",                          # ������ �� ��������
            "Nikita  Stebunov",             # ������� ������
            "Ni",                           # ������� ��������
            "Nikita Stebunov" * 4,          # ������� �������
            "Nikita@Stebunov",              # ������������ ������
            "N i k i t a",                  # ��������� �����
            "������ ��������",              # ������� �������
            "N I K I T A S T E B U N O V"   # ��������� �����
        ]
        for author in invalid_authors:
            self.assertFalse(validate_author(author)[0], f"Author: {author} ������ ���� ������������")

# ������������ ������� validate_title
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
            self.assertTrue(validate_title(title)[0], f"Title: {title} ������ ���� ����������")

    def test_invalid_titles(self):
        invalid_titles = [
            "",                                     # ������ ������
            "   ",                                  # ������ �� ��������
            "How to  extend the battery life",      # ������� ������
            "How",                                  # ������� ��������
            "How to extend the battery life? " * 5, # ������� �������
            "12345",                                # ������������ ����
            "How to extend the battery@life",       # ������������ ������
            "��� �������� ����� �������?",          # ������� �������
            "How to extend the battery#life"        # ������������ ������
        ]
        for title in invalid_titles:
            self.assertFalse(validate_title(title)[0], f"Title: {title} ������ ���� ������������")

# ������������ ������� validate_phone
class TestValidatePhone(unittest.TestCase):
    def test_valid_phones(self):
        valid_phones = [
            "+71234567890",
            "+79991234567",
            "+79123456789",
            "+79876543210"
        ]
        for phone in valid_phones:
            self.assertTrue(validate_phone(phone)[0], f"Phone: {phone} ������ ���� ����������")

    def test_invalid_phones(self):
        invalid_phones = [
            "",                        # ������ ������
            "   ",                     # ������ �� ��������
            "+7 123 456 7890",         # �������
            "1234567890",              # ��� +7
            "+71234",                  # ������� ��������
            "+71234nikita",            # �����
            "+81234567890",            # �������� ��� ������
            "+712345678901",           # ������� �������
            "+7999123456",             # ������� ��������
            "+7 912 345 67 89"         # ������� � �������
        ]
        for phone in invalid_phones:
            self.assertFalse(validate_phone(phone)[0], f"Phone: {phone} ������ ���� ������������")

# ������������ ������� validate_description
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
            self.assertTrue(validate_description(description)[0], f"Description: {description} ������ ���� ����������")

    def test_invalid_descriptions(self):
        invalid_descriptions = [
            "",                             # ������ ������
            "   ",                          # ������ �� ��������
            "Nikita  Stebunov",             # ������� ��������
            "Nikita Stebunov" * 22,         # ������� �������
            "1234567890" * 5,               # ������������ ����
            "Nikita@Stebunov Description",  # ������������ ������
            "������ ��������: ��������",    # ������� �������
            "N I K I T A S T E B U N O V",  # ������������ ����
            "Nikita  Stebunov description", # ������� ������
            "Nikita#Stebunov Test"          # ������������ ������
        ]
        for description in invalid_descriptions:
            self.assertFalse(validate_description(description)[0], f"Description: {description} ������ ���� ������������")

# ������������ ������� validate_image
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
            self.assertTrue(validate_image(image)[0], f"Image: {image.filename} ������ ���� ����������")

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
                self.assertFalse(validate_image(image)[0], f"Image: None ������ ���� ������������")
            else:
                self.assertFalse(validate_image(image)[0], f"Image: {image.filename} ������ ���� ������������")

if __name__ == '__main__':
    unittest.main()