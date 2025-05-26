# -*- coding: cp1251 -*-

import os
import json
import re
from datetime import datetime
import uuid
from bottle import request, response
import phonenumbers
from phonenumbers import NumberParseException, is_valid_number

# Функция для получения списка статей из JSON-файла
def get_articles():
    json_file = 'static/jsons/articles.json'
    articles = []
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        for author_name, author_data in data['authors'].items():
            for date, date_articles in author_data['articles_by_date'].items():
                for article in date_articles:
                    # Парсинг даты и времени статьи
                    datetime_obj = datetime.strptime(date + ' ' + article['time'], '%Y-%m-%d %H:%M')
                    article['date_added'] = datetime_obj.strftime('%d.%m.%Y %H:%M')
                    article['author'] = author_name
                    article['email'] = author_data.get('email', '')
                    article['phone'] = author_data.get('phone', '')
                    articles.append(article)
        # Сортировка статей по дате (новые первыми)
        articles.sort(key=lambda x: x['date_added'], reverse=True)
    except (FileNotFoundError, json.JSONDecodeError):
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
        raise Exception(f"Ошибка сохранения статей: {str(e)}")

# Функция для проверки адреса электронной почты
def validate_email(email):
    email = email.strip()
    if not email:
        return False, "Email не может быть пустым."
    if len(email) > 254:
        return False, "Email слишком длинный. Максимальная длина - 254 символа."
    if '@' not in email:
        return False, "Email должен содержать символ '@'."
    parts = email.split('@', 1)
    subject_part = parts[0]
    domain_part = parts[1] if len(parts) > 1 else ''
    if len(subject_part) < 3:
        return False, "Преддоменная часть email слишком короткая. Минимальная длина — 3 символа."
    if len(subject_part) > 64:
        return False, "Преддоменная часть email слишком длинная. Максимальная длина — 64 символа."
    if len(domain_part) < 4:
        return False, "Доменная часть email слишком короткая. Минимальная длина — 4 символа."
    if len(domain_part) > 190:
        return False, "Доменная часть email слишком длинная. Максимальная длина — 190 символов."
    # Определение списка разрешенных доменов
    allowed_domains = ['gmail.com', 'mail.ru', 'inbox.ru', 'yandex.ru']
    # Формирование паттерна для доменов
    domain_pattern = '|'.join(re.escape(domain) for domain in allowed_domains)
    # Формирование регулярного выражения для email
    pattern = rf'^[a-zA-Z0-9_.+-]+@({domain_pattern})$'
    # Проверка соответствия email паттерну
    if not re.match(pattern, email):
        return False, f"Email должен быть на английском языке и соответствовать формату (например, user@gmail.com). Допустимые домены: {', '.join(allowed_domains)}."
    return True, email

# Функция для проверки URL-адреса
def validate_url(url):
    url = url.strip()
    if not url:
        return False, "Ссылка не может быть пустой."
    # Регулярное выражение для строгого формата https://domain.tld/path
    url_pattern = r'^https://[a-zA-Z0-9-]+\.[a-zA-Z]{2,6}(/[a-zA-Z0-9-._~:/?#[\]@!$&\'()*+,;=]*)?$'
    # Проверка соответствия URL паттерну
    if not re.match(url_pattern, url):
        return False, "Недопустимый формат ссылки. Используйте формат https://domain.tld/path."
    return True, url

# Функция для проверки имени автора
def validate_author(author):
    author = author.strip()
    if not author:
        return False, "Имя автора не может быть пустым."
    if len(author) < 3:
        return False, "Имя автора должно содержать минимум 3 символа."
    if len(author) > 50:
        return False, "Имя автора не должно превышать 50 символов."
    # Проверка на английские буквы и цифры
    if not re.match(r'^[a-zA-Z0-9]+(?: [a-zA-Z0-9]+)*$', author):
        return False, "Имя автора должно содержать только английские буквы и цифры, без лишних пробелов."
    # Проверка на недопустимые имена вроде "a a a"
    if re.match(r'^(?:\w\s+){2,}\w$', author):
        return False, "Имя автора не может состоять из отдельных букв, разделенных пробелами."
    return True, author

# Функция для проверки заголовка статьи
def validate_title(title):
    title = title.strip()
    if not title:
        return False, "Заголовок не может быть пустым."
    if len(title) < 5:
        return False, "Заголовок должен содержать минимум 5 символов."
    if len(title) > 100:
        return False, "Заголовок не должен превышать 100 символов."
    # Подсчет букв
    letter_count = sum(c.isalpha() for c in title)
    if letter_count < 5:
        return False, "Заголовок должен содержать минимум 5 букв."
    # Проверка на английские буквы, цифры, пробелы и специальные символы
    if not re.match(r'^[a-zA-Z0-9,.!?;:\-\'\"&()]+(?: [a-zA-Z0-9,.!?;:\-\'\"&()]+)*$', title):
        return False, "Заголовок должен содержать только английские буквы, цифры, пробелы и разрешенные символы (,.!?;:-'\"&())."
    return True, title

# Функция для проверки номера телефона
def validate_phone(phone):
    phone = phone.strip()
    if not phone:
        return False, "Номер телефона не может быть пустым."
    # Проверка начала номера на +7
    if not phone.startswith('+7'):
        return False, "Номер телефона должен начинаться с +7."
    try:
        # Парсинг номера телефона
        parsed_phone = phonenumbers.parse(phone, None)
        # Проверка валидности номера
        if not is_valid_number(parsed_phone):
            return False, "Недопустимый номер телефона. Используйте формат +71234567890."
    except NumberParseException:
        # Возврат ошибки при неверном формате
        return False, "Неверный формат номера телефона. Используйте формат +71234567890."
    return True, phone

# Функция для проверки описания статьи
def validate_description(description):
    description = description.strip()
    if not description:
        return False, "Описание не может быть пустым."
    if len(description) < 50:
        return False, "Описание должно содержать минимум 50 символов."
    if len(description) > 300:
        return False, "Описание не должно превышать 300 символов."
    # Подсчет букв
    letter_count = sum(c.isalpha() for c in description)
    if letter_count < 50:
        return False, "Описание должно содержать минимум 50 букв."
    # Проверка на английские буквы, цифры, пробелы и специальные символы
    if not re.match(r'^[a-zA-Z0-9,.!?;:\-\'\"&()]+(?: [a-zA-Z0-9,.!?;:\-\'\"&()]+)*$', description):
        return False, "Описание должно содержать только английские буквы, цифры, пробелы и разрешенные символы (,.!?;:-'\"&())."
    return True, description

# Функция для проверки загруженного изображения
def validate_image(image_file):
    if image_file is None or not image_file.filename:
        return False, "Изображение обязательно для загрузки."
    # Проверка формата изображения
    allowed_extensions = ['.png', '.jpg', '.jpeg']
    # Извлечение расширения файла
    ext = os.path.splitext(image_file.filename)[1].lower()
    if ext not in allowed_extensions:
        return False, "Изображение должно быть в формате PNG или JPG."
    if not image_file.content_type.startswith('image/'):
        return False, "Загруженный файл не является изображением."
    return True, image_file

# Функция для валидации формы добавления статьи
def validate_article_form(data, image_file, existing_articles):
    errors = []
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
        # Проверка соответствия email и телефона для существующего автора
        if data['author'] in articles_data['authors']:
            existing_email = articles_data['authors'][data['author']].get('email', '')
            existing_phone = articles_data['authors'][data['author']].get('phone', '')
            if existing_email and existing_email != data['email']:
                errors.append("Указанный email не соответствует email автора в базе данных.")
            if existing_phone and existing_phone != data['phone']:
                errors.append("Указанный номер телефона не соответствует номеру автора в базе данных.")
        else:
            # Проверка на уникальность email и телефона для нового автора
            for author_name, author_data in articles_data['authors'].items():
                if author_name != data['author']:
                    if author_data.get('email') == data['email']:
                        errors.append("Указанный email уже используется другим автором.")
                    if author_data.get('phone') == data['phone']:
                        errors.append("Указанный номер телефона уже используется другим автором.")
    except (FileNotFoundError, json.JSONDecodeError):
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
        form_data['author'] = request.forms.get('author', '').strip()
        form_data['email'] = request.forms.get('email', '').strip()
        form_data['phone'] = request.forms.get('phone', '').strip()
        form_data['title'] = request.forms.get('title', '').strip()
        form_data['description'] = request.forms.get('description', '').strip()
        form_data['link'] = request.forms.get('link', '').strip()
        image = request.files.get('image')
        errors = validate_article_form(form_data, image, articles)
        if not errors:
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
                pass
            new_article = {
                'title': form_data['title'],
                'image': image_path,
                'description': form_data['description'],
                'link': form_data['link'],
                'time': current_time
            }
            author = form_data['author']
            if author not in articles_data['authors']:
                articles_data['authors'][author] = {
                    'email': form_data['email'],
                    'phone': form_data['phone'],
                    'articles_by_date': {}
                }
            if current_date not in articles_data['authors'][author]['articles_by_date']:
                articles_data['authors'][author]['articles_by_date'][current_date] = []
            articles_data['authors'][author]['articles_by_date'][current_date].append(new_article)
            save_articles(articles_data)
            response.set_header('Location', '/usefulArticles')
            response.status = 303
            form_data = {'author': '', 'email': '', 'phone': '', 'title': '', 'description': '', 'link': ''}
            show_form = False
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
        response.status = 400
        return {'status': 'error', 'message': 'Недопустимые параметры запроса'}
    json_file = 'static/jsons/articles.json'
    try:
        # Чтение JSON-файла
        with open(json_file, 'r', encoding='utf-8') as file:
            articles_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        response.status = 400
        return {'status': 'error', 'message': 'Ошибка загрузки данных статьи'}
    if author in articles_data['authors'] and date in articles_data['authors'][author]['articles_by_date']:
        articles = articles_data['authors'][author]['articles_by_date'][date]
        index = int(index)
        if 0 <= index < len(articles):
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
            return {'status': 'error', 'message': 'Недопустимый индекс статьи'}
    else:
        response.status = 400
        return {'status': 'error', 'message': 'Статья не найдена'}