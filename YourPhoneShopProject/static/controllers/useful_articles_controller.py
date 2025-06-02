# -*- coding: cp1251 -*-

import os
import json
import re
from datetime import datetime
import uuid
from bottle import request, response
import phonenumbers
from phonenumbers import NumberParseException

# ������� ��� ��������� ������ ������ �� JSON-�����
def get_articles():
    json_file = 'static/jsons/articles.json'
    articles = []
    try:
        # �������� ������ �� JSON-�����
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        # ����� ������� � �� ������ ��� ������������ ������
        for author_name, author_data in data['authors'].items():
            for date, date_articles in author_data['articles_by_date'].items():
                for idx, article in enumerate(date_articles):
                    # �������������� ������ ���� � ������� � ������ datetime
                    datetime_obj = datetime.strptime(date + ' ' + article['time'], '%Y-%m-%d %H:%M')
                    article['date_added'] = datetime_obj.strftime('%d.%m.%Y %H:%M')
                    article['author'] = author_name
                    article['email'] = author_data.get('email', '')
                    article['phone'] = author_data.get('phone', '')
                    article['index_in_date'] = idx
                    articles.append(article)
        # ���������� ������ �� ���� ���������� � �������� �������
        articles.sort(key=lambda x: x['date_added'], reverse=True)
    except (FileNotFoundError, json.JSONDecodeError):
        # ����������� ������� ������ � ������ ������ ������ �����
        pass
    return articles

# ������� ��� ���������� ������ ������ � JSON-����
def save_articles(articles_data):
    json_file = 'static/jsons/articles.json'
    try:
        # �������� ���������� ��� �����, ���� �� ����������
        os.makedirs(os.path.dirname(json_file), exist_ok=True)
        # ������ ������ � JSON-����
        with open(json_file, 'w', encoding='utf-8') as file:
            json.dump(articles_data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        # ������ ���������� � ��������� ������
        raise Exception(f"Error saving articles: {str(e)}")

# ������� ��� �������� ������ ����������� �����
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
    # ����������� ������ ����������� �������
    allowed_domains = ['gmail.com', 'mail.ru', 'inbox.ru', 'yandex.ru']
    # ������������ �������� ��� �������
    domain_pattern = '|'.join(re.escape(domain) for domain in allowed_domains)
    # ������������ ����������� ��������� ��� email
    pattern = rf'^[a-zA-Z0-9_.+-]+@({domain_pattern})$'
    # �������� ������������ email ��������
    if not re.match(pattern, email):
        return False, f"Email must be in English and follow the format (e.g., user@gmail.com). Allowed domains: {', '.join(allowed_domains)}."
    return True, email

# ������� ��� �������� URL-������
def validate_url(url):
    url = url.strip()
    if not url:
        return False, "URL cannot be empty."
    # ���������� ��������� ��� ������� https://[subdomain.]domain.tld/path ��� ���������� (#) � ������� @
    url_pattern = r'^https://([a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+\.[a-zA-Z]{2,6}(/[a-zA-Z0-9-._~:/?[\]!$&\'()*+,;=]*)?$'
    # �������� ������������ URL ��������
    if not re.match(url_pattern, url):
        return False, "Invalid URL format. Use the format https://domain.tld/path."
    # �������������� �������� �� ���������� ��������� (#)
    if '#' in url:
        return False, "URL must not contain fragments (e.g., #catalog)."
    return True, url

# ������� ��� �������� ����� ������
def validate_author(author):
    author = author.strip()
    if not author:
        return False, "Author name cannot be empty."
    if len(author) < 3:
        return False, "Author name must contain at least 3 characters."
    if len(author) > 50:
        return False, "Author name must not exceed 50 characters."
    # ������� ����
    letter_count = sum(c.isalpha() for c in author)
    if letter_count < 3:
        return False, "Author name must contain at least 3 letters."
    # �������� �� ���������� �����, �����, ������������� � ������
    if not re.match(r'^[a-zA-Z0-9_-]+(?: [a-zA-Z0-9_-]+)*$', author):
        return False, "Author name must contain only English letters, digits, underscores, hyphens, and single spaces."
    # �������� �� ������������ ����� ����� "a a a"
    if re.match(r'^(?:\w\s+){2,}\w$', author):
        return False, "Author name cannot consist of single characters separated by spaces."
    return True, author

# ������� ��� �������� ��������� ������
def validate_title(title):
    title = title.strip()
    if not title:
        return False, "Title cannot be empty."
    if len(title) < 5:
        return False, "Title must contain at least 5 characters."
    if len(title) > 100:
        return False, "Title must not exceed 100 characters."
    # ������� ����
    letter_count = sum(c.isalpha() for c in title)
    if letter_count < 5:
        return False, "Title must contain at least 5 letters."
    # �������� �� ���������� �����, �����, ������� � ����������� �������
    if not re.match(r'^[a-zA-Z0-9,.!?;:\-\'\"&()]+(?: [a-zA-Z0-9,.!?;:\-\'\"&()]+)*$', title):
        return False, "Title must contain only English letters, digits, spaces, and allowed characters (,.!?;:-'\"&())."
    return True, title

# ������� ��� �������� ������ ��������
def validate_phone(phone):
    phone = phone.strip()
    if not phone:
        return False, "Phone number cannot be empty."
    # �������� �� �������
    if ' ' in phone:
        return False, "Phone number cannot contain spaces."
    # �������� ������ ������ �� +7
    if not phone.startswith('+7'):
        return False, "Phone number must start with +7."
    # �������� ����� ������ (������ ���� 12 ��������: +7 � 10 ����)
    if len(phone) != 12:
        return False, "Phone number must contain 10 digits after +7."
    # ��������, ��� ����� +7 ���� ������ �����
    if not phone[1:].isdigit():
        return False, "Phone number must contain only digits after +7."
    # �������� ������ � �������������� ���������� phonenumbers
    try:
        # ������� ������ ��������
        parsed_phone = phonenumbers.parse(phone, "RU")
        return True, phone
    except NumberParseException:
        return False, "Invalid phone number format. Use the format +71234567890."

# ������� ��� �������� �������� ������
def validate_description(description):
    description = description.strip()
    if not description:
        return False, "Description cannot be empty."
    if len(description) < 50:
        return False, "Description must contain at least 50 characters."
    if len(description) > 300:
        return False, "Description must not exceed 300 characters."
    # ������� ����
    letter_count = sum(c.isalpha() for c in description)
    if letter_count < 47:
        return False, "Description must contain at least 47 letters."
    # �������� �� ���������� �����, �����, ������� � ����������� �������
    if not re.match(r'^[a-zA-Z0-9,.!?;:\-\'\"&() ]+$', description):
        return False, "Description must contain only English letters, digits, spaces, and allowed characters (,.!?;:-'\"&())."
    return True, description

# ������� ��� �������� ������������ �����������
def validate_image(image_file):
    if image_file is None or not image_file.filename:
        return False, "Image is required."
    # �������� �� ������� � ����� �����
    if ' ' in image_file.filename:
        return False, "Image filename cannot contain spaces."
    # �������� ������� �����������
    allowed_extensions = ['.png', '.jpg', '.jpeg']
    # ���������� ���������� �����
    ext = os.path.splitext(image_file.filename)[1].lower()
    if ext not in allowed_extensions:
        return False, "Image must be in PNG or JPG format."
    if not image_file.content_type.startswith('image/'):
        return False, "Uploaded file is not an image."
    return True, image_file

# ������� ��� ��������� ����� ���������� ������
def validate_article_form(data, image_file, existing_articles):
    errors = []
    # �������� ���� ����� �����
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
        # ������ JSON-�����
        with open(json_file, 'r', encoding='utf-8') as file:
            articles_data = json.load(file)
        # �������� ������������ ��������� ����� ���� ������
        new_title = data['title']
        for author_name, author_data in articles_data['authors'].items():
            for date, date_articles in author_data['articles_by_date'].items():
                for article in date_articles:
                    if article['title'].lower() == new_title.lower():
                        errors.append(f"An article with the title '{new_title}' already exists.")
                        break
        # �������� ������������ email � �������� ��� ������������� ������
        if data['author'] in articles_data['authors']:
            existing_email = articles_data['authors'][data['author']].get('email', '')
            existing_phone = articles_data['authors'][data['author']].get('phone', '')
            if existing_email and existing_email != data['email']:
                errors.append("The provided email does not match the author's email in the database.")
            if existing_phone and existing_phone != data['phone']:
                errors.append("The provided phone number does not match the author's phone number in the database.")
        else:
            # �������� �� ������������ email � �������� ��� ������ ������
            for author_name, author_data in articles_data['authors'].items():
                if author_name != data['author']:
                    if author_data.get('email') == data['email']:
                        errors.append("The provided email is already used by another author.")
                    if author_data.get('phone') == data['phone']:
                        errors.append("The provided phone number is already used by another author.")
    except (FileNotFoundError, json.JSONDecodeError):
        # ������������� ������ ������ �����
        pass
    return errors

# ������� ��� ��������� �������� �� ���������� � ����������� ������
def handle_articles():
    articles = get_articles()
    errors = []
    form_data = {'author': '', 'email': '', 'phone': '', 'title': '', 'description': '', 'link': ''}
    show_form = False
    if request.method == 'POST':
        show_form = True
        # ��������� ������ �� �����
        form_data['author'] = request.forms.get('author', '').strip()
        form_data['email'] = request.forms.get('email', '').strip()
        form_data['phone'] = request.forms.get('phone', '').strip()
        form_data['title'] = request.forms.get('title', '').strip()
        form_data['description'] = request.forms.get('description', '').strip()
        form_data['link'] = request.forms.get('link', '').strip()
        image = request.files.get('image')
        errors = validate_article_form(form_data, image, articles)
        if not errors:
            # ���������� ������������ �����������
            ext = os.path.splitext(image.filename)[1]
            filename = f"{uuid.uuid4()}{ext}"
            save_dir = 'static/images/articles'
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, filename)
            image.save(save_path)
            # ������������ ���� � ������� ������������
            normalized_path = save_path.replace(os.sep, '/')
            # ������������ ���� ��� JSON
            image_path = f"/{normalized_path}"
            current_date = datetime.now().strftime('%Y-%m-%d')
            current_time = datetime.now().strftime('%H:%M')
            json_file = 'static/jsons/articles.json'
            articles_data = {'authors': {}}
            try:
                # ������ ������������� JSON-�����
                with open(json_file, 'r', encoding='utf-8') as file:
                    articles_data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                # �������� ����� ��������� ��� ���������� �����
                pass
            # ������������ ����� ������
            new_article = {
                'title': form_data['title'],
                'image': image_path,
                'description': form_data['description'],
                'link': form_data['link'],
                'time': current_time
            }
            author = form_data['author']
            if author not in articles_data['authors']:
                # ���������� ������ ������
                articles_data['authors'][author] = {
                    'email': form_data['email'],
                    'phone': form_data['phone'],
                    'articles_by_date': {}
                }
            if current_date not in articles_data['authors'][author]['articles_by_date']:
                # �������� ����� ���� ��� ������ ������
                articles_data['authors'][author]['articles_by_date'][current_date] = []
            articles_data['authors'][author]['articles_by_date'][current_date].append(new_article)
            save_articles(articles_data)
            response.set_header('Location', '/usefulArticles')
            response.status = 303
            form_data = {'author': '', 'email': '', 'phone': '', 'title': '', 'description': '', 'link': ''}
            show_form = False
    # ������������ ������ ��� �������
    return {
        'articles': articles,
        'title': 'Useful Articles',
        'year': datetime.now().year,
        'errors': errors,
        'form_data': form_data,
        'show_form': show_form
    }

# ������� ��� �������� ������
def delete_article():
    data = request.json
    author = data.get('author')
    date = data.get('date')
    index = data.get('index')
    if not all([author, date, index is not None]):
        # �������� ������� ���� ����������� ����������
        response.status = 400
        return {'status': 'error', 'message': 'Invalid request parameters'}
    json_file = 'static/jsons/articles.json'
    try:
        # ������ JSON-�����
        with open(json_file, 'r', encoding='utf-8') as file:
            articles_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        response.status = 400
        return {'status': 'error', 'message': 'Error loading article data'}
    if author in articles_data['authors'] and date in articles_data['authors'][author]['articles_by_date']:
        articles = articles_data['authors'][author]['articles_by_date'][date]
        index = int(index)
        if 0 <= index < len(articles):
            # �������� ������ �� �������
            articles.pop(index)
            # �������� ����, ���� ��� ������
            if not articles:
                del articles_data['authors'][author]['articles_by_date'][date]
            # �������� ������, ���� ��� ���
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