# -*- coding: cp1251 -*-

import os
import json
import re
from datetime import datetime
import uuid
from bottle import request, response
import phonenumbers
from phonenumbers import NumberParseException

# Функция для получения списка статей из JSON-файла
def get_articles():
    json_file = 'static/jsons/articles.json'
    articles = []
    try:
        # Загрузка данных из JSON-файла
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        # Обход авторов и их статей для формирования списка
        for author_name, author_data in data['authors'].items():
            for date, date_articles in author_data['articles_by_date'].items():
                for idx, article in enumerate(date_articles):
                    # Преобразование строки даты и времени в объект datetime
                    datetime_obj = datetime.strptime(date + ' ' + article['time'], '%Y-%m-%d %H:%M')
                    article['date_added'] = datetime_obj.strftime('%d.%m.%Y %H:%M')
                    article['author'] = author_name
                    article['email'] = author_data.get('email', '')
                    article['phone'] = author_data.get('phone', '')
                    article['index_in_date'] = idx
                    articles.append(article)
        # Сортировка статей по дате добавления в обратном порядке
        articles.sort(key=lambda x: x['date_added'], reverse=True)
    except (FileNotFoundError, json.JSONDecodeError):
        # Возвращение пустого списка в случае ошибки чтения файла
        pass
    return articles

# Функция для сохранения данных статей в JSON-файл
def save_articles(articles_data):
    json_file = 'static/jsons/articles.json'
    try:
        # Создание директории для файла, если не существует
        os.makedirs(os.path.dirname(json_file), exist_ok=True)
        # Запись данных в JSON-файл
        with open(json_file, 'w', encoding='utf-8') as file:
            json.dump(articles_data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        # Выброс исключения с описанием ошибки
        raise Exception(f"Error saving articles: {str(e)}")

# Функция для проверки адреса электронной почты
def validate_email(email):
    email = email.strip()
    if not email:
        return False, "Email cannot be empty."
    if len(email) > 254:
        return False, "Email is too long. Maximum length is 254 characters."
    if '@' not in email:
        return False, "Email must contain the '@' symbol."
    parts = email.split('@', 1)
    subject_part = parts[0]
    domain_part = parts[1] if len(parts) > 1 else ''
    if len(subject_part) < 3:
        return False, "Email local part is too short. Minimum length is 3 characters."
    if len(subject_part) > 64:
        return False, "Email local part is too long. Maximum length is 64 characters."
    if len(domain_part) < 4:
        return False, "Email domain part is too short. Minimum length is 4 characters."
    if len(domain_part) > 190:
        return False, "Email domain part is too long. Maximum length is 190 characters."
    if '..' in subject_part:
        return False, "Email local part cannot contain consecutive dots."
    # Определение списка разрешенных доменов
    allowed_domains = ['gmail.com', 'mail.ru', 'inbox.ru', 'yandex.ru']
    # Формирование паттерна для доменов
    domain_pattern = '|'.join(re.escape(domain) for domain in allowed_domains)
    # Формирование регулярного выражения для email
    pattern = rf'^[a-zA-Z0-9_.+-]+@({domain_pattern})$'
    # Проверка соответствия email паттерну
    if not re.match(pattern, email):
        return False, f"Email must be in English and follow the format (e.g., user@gmail.com). Allowed domains: {', '.join(allowed_domains)}."
    return True, email

# Функция для проверки URL-адреса
def validate_url(url):
    url = url.strip()
    if not url:
        return False, "URL cannot be empty."
    # Регулярное выражение для формата https://[subdomain.]domain.tld/path без фрагментов (#) и символа @
    url_pattern = r'^https://([a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+\.[a-zA-Z]{2,6}(/[a-zA-Z0-9-._~:/?[\]!$&\'()*+,;=]*)?$'
    # Проверка соответствия URL паттерну
    if not re.match(url_pattern, url):
        return False, "Invalid URL format. Use the format https://domain.tld/path."
    # Дополнительная проверка на отсутствие фрагмента (#)
    if '#' in url:
        return False, "URL must not contain fragments (e.g., #catalog)."
    return True, url

# Функция для проверки имени автора
def validate_author(author):
    author = author.strip()
    if not author:
        return False, "Author name cannot be empty."
    if len(author) < 3:
        return False, "Author name must contain at least 3 characters."
    if len(author) > 50:
        return False, "Author name must not exceed 50 characters."
    # Подсчет букв
    letter_count = sum(c.isalpha() for c in author)
    if letter_count < 3:
        return False, "Author name must contain at least 3 letters."
    # Проверка на английские буквы, цифры, подчеркивания и дефисы
    if not re.match(r'^[a-zA-Z0-9_-]+(?: [a-zA-Z0-9_-]+)*$', author):
        return False, "Author name must contain only English letters, digits, underscores, hyphens, and single spaces."
    # Проверка на недопустимые имена вроде "a a a"
    if re.match(r'^(?:\w\s+){2,}\w$', author):
        return False, "Author name cannot consist of single characters separated by spaces."
    return True, author

# Функция для проверки заголовка статьи
def validate_title(title):
    title = title.strip()
    if not title:
        return False, "Title cannot be empty."
    if len(title) < 5:
        return False, "Title must contain at least 5 characters."
    if len(title) > 100:
        return False, "Title must not exceed 100 characters."
    # Подсчет букв
    letter_count = sum(c.isalpha() for c in title)
    if letter_count < 5:
        return False, "Title must contain at least 5 letters."
    # Проверка на английские буквы, цифры, пробелы и специальные символы
    if not re.match(r'^[a-zA-Z0-9,.!?;:\-\'\"&()]+(?: [a-zA-Z0-9,.!?;:\-\'\"&()]+)*$', title):
        return False, "Title must contain only English letters, digits, spaces, and allowed characters (,.!?;:-'\"&())."
    return True, title

# Функция для проверки номера телефона
def validate_phone(phone):
    phone = phone.strip()
    if not phone:
        return False, "Phone number cannot be empty."
    # Проверка на пробелы
    if ' ' in phone:
        return False, "Phone number cannot contain spaces."
    # Проверка начала номера на +7
    if not phone.startswith('+7'):
        return False, "Phone number must start with +7."
    # Проверка длины номера (должно быть 12 символов: +7 и 10 цифр)
    if len(phone) != 12:
        return False, "Phone number must contain 10 digits after +7."
    # Проверка, что после +7 идут только цифры
    if not phone[1:].isdigit():
        return False, "Phone number must contain only digits after +7."
    # Проверка номера с использованием библиотеки phonenumbers
    try:
        # Парсинг номера телефона
        parsed_phone = phonenumbers.parse(phone, "RU")
        return True, phone
    except NumberParseException:
        return False, "Invalid phone number format. Use the format +71234567890."

# Функция для проверки описания статьи
def validate_description(description):
    description = description.strip()
    if not description:
        return False, "Description cannot be empty."
    if len(description) < 50:
        return False, "Description must contain at least 50 characters."
    if len(description) > 300:
        return False, "Description must not exceed 300 characters."
    # Подсчет букв
    letter_count = sum(c.isalpha() for c in description)
    if letter_count < 47:
        return False, "Description must contain at least 47 letters."
    # Проверка на английские буквы, цифры, пробелы и специальные символы
    if not re.match(r'^[a-zA-Z0-9,.!?;:\-\'\"&() ]+$', description):
        return False, "Description must contain only English letters, digits, spaces, and allowed characters (,.!?;:-'\"&())."
    return True, description

# Функция для проверки загруженного изображения
def validate_image(image_file):
    if image_file is None or not image_file.filename:
        return False, "Image is required."
    # Проверка на пробелы в имени файла
    if ' ' in image_file.filename:
        return False, "Image filename cannot contain spaces."
    # Проверка формата изображения
    allowed_extensions = ['.png', '.jpg', '.jpeg']
    # Извлечение расширения файла
    ext = os.path.splitext(image_file.filename)[1].lower()
    if ext not in allowed_extensions:
        return False, "Image must be in PNG or JPG format."
    if not image_file.content_type.startswith('image/'):
        return False, "Uploaded file is not an image."
    return True, image_file

# Функция для валидации формы добавления статьи
def validate_article_form(data, image_file, existing_articles):
    errors = []
    # Проверка всех полей формы
    is_valid, result = validate_author(data.get('author', '').strip())
    if not is_valid:
        errors.append(result)
    else:
        data['author'] = result
    is_valid, result = validate_email(data.get('email', '').strip())
    if not is_valid:
        errors.append(result)
    else:
        data['email'] = result
    is_valid, result = validate_phone(data.get('phone', '').strip())
    if not is_valid:
        errors.append(result)
    else:
        data['phone'] = result
    is_valid, result = validate_title(data.get('title', '').strip())
    if not is_valid:
        errors.append(result)
    else:
        data['title'] = result
    is_valid, result = validate_description(data.get('description', '').strip())
    if not is_valid:
        errors.append(result)
    else:
        data['description'] = result
    is_valid, result = validate_url(data.get('link', '').strip())
    if not is_valid:
        errors.append(result)
    else:
        data['link'] = result
    is_valid, result = validate_image(image_file)
    if not is_valid:
        errors.append(result)
    
    json_file = 'static/jsons/articles.json'
    try:
        # Чтение JSON-файла
        with open(json_file, 'r', encoding='utf-8') as file:
            articles_data = json.load(file)
        # Проверка уникальности заголовка среди всех статей
        new_title = data['title']
        for author_name, author_data in articles_data['authors'].items():
            for date, date_articles in author_data['articles_by_date'].items():
                for article in date_articles:
                    if article['title'].lower() == new_title.lower():
                        errors.append(f"An article with the title '{new_title}' already exists.")
                        break
        # Проверка соответствия email и телефона для существующего автора
        if data['author'] in articles_data['authors']:
            existing_email = articles_data['authors'][data['author']].get('email', '')
            existing_phone = articles_data['authors'][data['author']].get('phone', '')
            if existing_email and existing_email != data['email']:
                errors.append("The provided email does not match the author's email in the database.")
            if existing_phone and existing_phone != data['phone']:
                errors.append("The provided phone number does not match the author's phone number in the database.")
        else:
            # Проверка на уникальность email и телефона для нового автора
            for author_name, author_data in articles_data['authors'].items():
                if author_name != data['author']:
                    if author_data.get('email') == data['email']:
                        errors.append("The provided email is already used by another author.")
                    if author_data.get('phone') == data['phone']:
                        errors.append("The provided phone number is already used by another author.")
    except (FileNotFoundError, json.JSONDecodeError):
        # Игнорирование ошибок чтения файла
        pass
    return errors

# Функция для обработки запросов на добавление и отображение статей
def handle_articles():
    articles = get_articles()
    errors = []
    form_data = {'author': '', 'email': '', 'phone': '', 'title': '', 'description': '', 'link': ''}
    show_form = False
    if request.method == 'POST':
        show_form = True
        # Получение данных из формы
        form_data['author'] = request.forms.get('author', '').strip()
        form_data['email'] = request.forms.get('email', '').strip()
        form_data['phone'] = request.forms.get('phone', '').strip()
        form_data['title'] = request.forms.get('title', '').strip()
        form_data['description'] = request.forms.get('description', '').strip()
        form_data['link'] = request.forms.get('link', '').strip()
        image = request.files.get('image')
        errors = validate_article_form(form_data, image, articles)
        if not errors:
            # Сохранение загруженного изображения
            ext = os.path.splitext(image.filename)[1]
            filename = f"{uuid.uuid4()}{ext}"
            save_dir = 'static/images/articles'
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, filename)
            image.save(save_path)
            # Нормализация пути с заменой разделителей
            normalized_path = save_path.replace(os.sep, '/')
            # Формирование пути для JSON
            image_path = f"/{normalized_path}"
            current_date = datetime.now().strftime('%Y-%m-%d')
            current_time = datetime.now().strftime('%H:%M')
            json_file = 'static/jsons/articles.json'
            articles_data = {'authors': {}}
            try:
                # Чтение существующего JSON-файла
                with open(json_file, 'r', encoding='utf-8') as file:
                    articles_data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                # Создание новой структуры при отсутствии файла
                pass
            # Формирование новой статьи
            new_article = {
                'title': form_data['title'],
                'image': image_path,
                'description': form_data['description'],
                'link': form_data['link'],
                'time': current_time
            }
            author = form_data['author']
            if author not in articles_data['authors']:
                # Добавление нового автора
                articles_data['authors'][author] = {
                    'email': form_data['email'],
                    'phone': form_data['phone'],
                    'articles_by_date': {}
                }
            if current_date not in articles_data['authors'][author]['articles_by_date']:
                # Создание новой даты для статей автора
                articles_data['authors'][author]['articles_by_date'][current_date] = []
            articles_data['authors'][author]['articles_by_date'][current_date].append(new_article)
            save_articles(articles_data)
            response.set_header('Location', '/usefulArticles')
            response.status = 303
            form_data = {'author': '', 'email': '', 'phone': '', 'title': '', 'description': '', 'link': ''}
            show_form = False
    # Формирование ответа для шаблона
    return {
        'articles': articles,
        'title': 'Useful Articles',
        'year': datetime.now().year,
        'errors': errors,
        'form_data': form_data,
        'show_form': show_form
    }

# Функция для удаления статьи
def delete_article():
    data = request.json
    author = data.get('author')
    date = data.get('date')
    index = data.get('index')
    if not all([author, date, index is not None]):
        # Проверка наличия всех необходимых параметров
        response.status = 400
        return {'status': 'error', 'message': 'Invalid request parameters'}
    json_file = 'static/jsons/articles.json'
    try:
        # Чтение JSON-файла
        with open(json_file, 'r', encoding='utf-8') as file:
            articles_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        response.status = 400
        return {'status': 'error', 'message': 'Error loading article data'}
    if author in articles_data['authors'] and date in articles_data['authors'][author]['articles_by_date']:
        articles = articles_data['authors'][author]['articles_by_date'][date]
        index = int(index)
        if 0 <= index < len(articles):
            # Удаление статьи по индексу
            articles.pop(index)
            # Удаление даты, если нет статей
            if not articles:
                del articles_data['authors'][author]['articles_by_date'][date]
            # Удаление автора, если нет дат
            if not articles_data['authors'][author]['articles_by_date']:
                del articles_data['authors'][author]
            save_articles(articles_data)
            return {'status': 'success'}
        else:
            response.status = 400
            return {'status': 'error', 'message': 'Invalid article index'}
    else:
        response.status = 400
        return {'status': 'error', 'message': 'Article not found'}