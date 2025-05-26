# -*- coding: cp1251 -*-

import os
import json
import re
from datetime import datetime
import uuid
from bottle import request, response
import phonenumbers
from phonenumbers import NumberParseException, is_valid_number

# ������� ��� ��������� ������ ������ �� JSON-�����
def get_articles():
    json_file = 'static/jsons/articles.json'
    articles = []
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        for author_name, author_data in data['authors'].items():
            for date, date_articles in author_data['articles_by_date'].items():
                for article in date_articles:
                    # ������� ���� � ������� ������
                    datetime_obj = datetime.strptime(date + ' ' + article['time'], '%Y-%m-%d %H:%M')
                    article['date_added'] = datetime_obj.strftime('%d.%m.%Y %H:%M')
                    article['author'] = author_name
                    article['email'] = author_data.get('email', '')
                    article['phone'] = author_data.get('phone', '')
                    articles.append(article)
        # ���������� ������ �� ���� (����� �������)
        articles.sort(key=lambda x: x['date_added'], reverse=True)
    except (FileNotFoundError, json.JSONDecodeError):
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
        raise Exception(f"������ ���������� ������: {str(e)}")

# ������� ��� �������� ������ ����������� �����
def validate_email(email):
    email = email.strip()
    if not email:
        return False, "Email �� ����� ���� ������."
    if len(email) > 254:
        return False, "Email ������� �������. ������������ ����� - 254 �������."
    if '@' not in email:
        return False, "Email ������ ��������� ������ '@'."
    parts = email.split('@', 1)
    subject_part = parts[0]
    domain_part = parts[1] if len(parts) > 1 else ''
    if len(subject_part) < 3:
        return False, "������������ ����� email ������� ��������. ����������� ����� � 3 �������."
    if len(subject_part) > 64:
        return False, "������������ ����� email ������� �������. ������������ ����� � 64 �������."
    if len(domain_part) < 4:
        return False, "�������� ����� email ������� ��������. ����������� ����� � 4 �������."
    if len(domain_part) > 190:
        return False, "�������� ����� email ������� �������. ������������ ����� � 190 ��������."
    # ����������� ������ ����������� �������
    allowed_domains = ['gmail.com', 'mail.ru', 'inbox.ru', 'yandex.ru']
    # ������������ �������� ��� �������
    domain_pattern = '|'.join(re.escape(domain) for domain in allowed_domains)
    # ������������ ����������� ��������� ��� email
    pattern = rf'^[a-zA-Z0-9_.+-]+@({domain_pattern})$'
    # �������� ������������ email ��������
    if not re.match(pattern, email):
        return False, f"Email ������ ���� �� ���������� ����� � ��������������� ������� (��������, user@gmail.com). ���������� ������: {', '.join(allowed_domains)}."
    return True, email

# ������� ��� �������� URL-������
def validate_url(url):
    url = url.strip()
    if not url:
        return False, "������ �� ����� ���� ������."
    # ���������� ��������� ��� �������� ������� https://domain.tld/path
    url_pattern = r'^https://[a-zA-Z0-9-]+\.[a-zA-Z]{2,6}(/[a-zA-Z0-9-._~:/?#[\]@!$&\'()*+,;=]*)?$'
    # �������� ������������ URL ��������
    if not re.match(url_pattern, url):
        return False, "������������ ������ ������. ����������� ������ https://domain.tld/path."
    return True, url

# ������� ��� �������� ����� ������
def validate_author(author):
    author = author.strip()
    if not author:
        return False, "��� ������ �� ����� ���� ������."
    if len(author) < 3:
        return False, "��� ������ ������ ��������� ������� 3 �������."
    if len(author) > 50:
        return False, "��� ������ �� ������ ��������� 50 ��������."
    # �������� �� ���������� ����� � �����
    if not re.match(r'^[a-zA-Z0-9]+(?: [a-zA-Z0-9]+)*$', author):
        return False, "��� ������ ������ ��������� ������ ���������� ����� � �����, ��� ������ ��������."
    # �������� �� ������������ ����� ����� "a a a"
    if re.match(r'^(?:\w\s+){2,}\w$', author):
        return False, "��� ������ �� ����� �������� �� ��������� ����, ����������� ���������."
    return True, author

# ������� ��� �������� ��������� ������
def validate_title(title):
    title = title.strip()
    if not title:
        return False, "��������� �� ����� ���� ������."
    if len(title) < 5:
        return False, "��������� ������ ��������� ������� 5 ��������."
    if len(title) > 100:
        return False, "��������� �� ������ ��������� 100 ��������."
    # ������� ����
    letter_count = sum(c.isalpha() for c in title)
    if letter_count < 5:
        return False, "��������� ������ ��������� ������� 5 ����."
    # �������� �� ���������� �����, �����, ������� � ����������� �������
    if not re.match(r'^[a-zA-Z0-9,.!?;:\-\'\"&()]+(?: [a-zA-Z0-9,.!?;:\-\'\"&()]+)*$', title):
        return False, "��������� ������ ��������� ������ ���������� �����, �����, ������� � ����������� ������� (,.!?;:-'\"&())."
    return True, title

# ������� ��� �������� ������ ��������
def validate_phone(phone):
    phone = phone.strip()
    if not phone:
        return False, "����� �������� �� ����� ���� ������."
    # �������� ������ ������ �� +7
    if not phone.startswith('+7'):
        return False, "����� �������� ������ ���������� � +7."
    try:
        # ������� ������ ��������
        parsed_phone = phonenumbers.parse(phone, None)
        # �������� ���������� ������
        if not is_valid_number(parsed_phone):
            return False, "������������ ����� ��������. ����������� ������ +71234567890."
    except NumberParseException:
        # ������� ������ ��� �������� �������
        return False, "�������� ������ ������ ��������. ����������� ������ +71234567890."
    return True, phone

# ������� ��� �������� �������� ������
def validate_description(description):
    description = description.strip()
    if not description:
        return False, "�������� �� ����� ���� ������."
    if len(description) < 50:
        return False, "�������� ������ ��������� ������� 50 ��������."
    if len(description) > 300:
        return False, "�������� �� ������ ��������� 300 ��������."
    # ������� ����
    letter_count = sum(c.isalpha() for c in description)
    if letter_count < 50:
        return False, "�������� ������ ��������� ������� 50 ����."
    # �������� �� ���������� �����, �����, ������� � ����������� �������
    if not re.match(r'^[a-zA-Z0-9,.!?;:\-\'\"&()]+(?: [a-zA-Z0-9,.!?;:\-\'\"&()]+)*$', description):
        return False, "�������� ������ ��������� ������ ���������� �����, �����, ������� � ����������� ������� (,.!?;:-'\"&())."
    return True, description

# ������� ��� �������� ������������ �����������
def validate_image(image_file):
    if image_file is None or not image_file.filename:
        return False, "����������� ����������� ��� ��������."
    # �������� ������� �����������
    allowed_extensions = ['.png', '.jpg', '.jpeg']
    # ���������� ���������� �����
    ext = os.path.splitext(image_file.filename)[1].lower()
    if ext not in allowed_extensions:
        return False, "����������� ������ ���� � ������� PNG ��� JPG."
    if not image_file.content_type.startswith('image/'):
        return False, "����������� ���� �� �������� ������������."
    return True, image_file

# ������� ��� ��������� ����� ���������� ������
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
        # ������ JSON-�����
        with open(json_file, 'r', encoding='utf-8') as file:
            articles_data = json.load(file)
        # �������� ������������ email � �������� ��� ������������� ������
        if data['author'] in articles_data['authors']:
            existing_email = articles_data['authors'][data['author']].get('email', '')
            existing_phone = articles_data['authors'][data['author']].get('phone', '')
            if existing_email and existing_email != data['email']:
                errors.append("��������� email �� ������������� email ������ � ���� ������.")
            if existing_phone and existing_phone != data['phone']:
                errors.append("��������� ����� �������� �� ������������� ������ ������ � ���� ������.")
        else:
            # �������� �� ������������ email � �������� ��� ������ ������
            for author_name, author_data in articles_data['authors'].items():
                if author_name != data['author']:
                    if author_data.get('email') == data['email']:
                        errors.append("��������� email ��� ������������ ������ �������.")
                    if author_data.get('phone') == data['phone']:
                        errors.append("��������� ����� �������� ��� ������������ ������ �������.")
    except (FileNotFoundError, json.JSONDecodeError):
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

# ������� ��� �������� ������
def delete_article():
    data = request.json
    author = data.get('author')
    date = data.get('date')
    index = data.get('index')
    if not all([author, date, index is not None]):
        response.status = 400
        return {'status': 'error', 'message': '������������ ��������� �������'}
    json_file = 'static/jsons/articles.json'
    try:
        # ������ JSON-�����
        with open(json_file, 'r', encoding='utf-8') as file:
            articles_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        response.status = 400
        return {'status': 'error', 'message': '������ �������� ������ ������'}
    if author in articles_data['authors'] and date in articles_data['authors'][author]['articles_by_date']:
        articles = articles_data['authors'][author]['articles_by_date'][date]
        index = int(index)
        if 0 <= index < len(articles):
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
            return {'status': 'error', 'message': '������������ ������ ������'}
    else:
        response.status = 400
        return {'status': 'error', 'message': '������ �� �������'}