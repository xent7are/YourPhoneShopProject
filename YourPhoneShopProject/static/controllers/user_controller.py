import json
import os
import re
from bottle import request, response
from datetime import datetime, date
import phonenumbers
from phonenumbers import NumberParseException, is_valid_number

def get_users():
    # Чтение списка пользователей из JSON-файла
    json_file = 'static/jsons/active_users.json'
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except Exception:
        raise

def save_users(users):
    # Сохранение списка пользователей в JSON-файл
    json_file = 'static/jsons/active_users.json'
    try:
        with open(json_file, 'w', encoding='utf-8') as file:
            json.dump(users, file, ensure_ascii=False, indent=4)
    except Exception:
        raise

def delete_user():
    # Удаление пользователя по ID
    user_id = request.json.get('user_id')
    users = get_users()
    if 0 <= int(user_id) < len(users):
        if users[int(user_id)].get('profile_picture'):
            try:
                # удаление фото пользователя
                os.remove(users[int(user_id)]['profile_picture'].lstrip('/'))
            except OSError:
                pass
        # удаление пользователя из списка users по индексу
        users.pop(int(user_id))
        save_users(users)
        return {'status': 'success'}
    else:
        response.status = 400
        return {'status': 'error', 'message': 'Invalid user ID'}

def handle_users():
    # Обработка GET и POST запросов для страницы пользователей
    users = get_users()
    errors = []
    form_data = {'name': '', 'email': '', 'phone': '', 'birth_date': '', 'profile_picture_name': ''}

    if request.method == 'POST':
        # Получение данных формы
        form_data['name'] = request.forms.get('name', '').strip()
        form_data['email'] = request.forms.get('email', '').strip()
        form_data['phone'] = request.forms.get('phone', '').strip()
        form_data['birth_date'] = request.forms.get('birth_date', '').strip()
        form_data['profile_picture_name'] = request.forms.get('profile_picture_name', '').strip()
        profile_picture = request.files.get('profile_picture')

        # Установка имени файла для отображения, если файл загружен
        if profile_picture and profile_picture.filename:
            form_data['profile_picture_name'] = profile_picture.filename

        # Валидация данных
        errors = validate_user_form(form_data, profile_picture, users)

        # Если нет ошибок, добавляем пользователя
        if not errors:
            new_user = {
                'name': form_data['name'],
                'email': form_data['email'],
                'phone': form_data['phone'],
                'birth_date': form_data['birth_date'],
                'registration_date': datetime.now().strftime('%Y-%m-%d'),
                'profile_picture': None
            }

            # Сохранение фотографии, если она загружена
            if profile_picture and profile_picture.file:
                try:
                    file_extension = profile_picture.filename.rsplit('.', 1)[-1].lower()
                    # создание нового уникального имени файла на основе текущей даты и времени и названия профиля
                    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{form_data['name'].replace(' ', '_')}.{file_extension}"
                    save_path = os.path.join('static', 'images', 'user_icons', filename)
                    # если нет нужной директории - ее создание
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)
                    # сохранение файла
                    profile_picture.save(save_path, overwrite=True)
                    new_user['profile_picture'] = f"/static/images/user_icons/{filename}"
                except Exception:
                    errors.append("Failed to save profile picture.")

            if not errors:
                users.append(new_user)
                users.sort(key=lambda x: x['registration_date'], reverse=True)
                save_users(users)
                response.set_header('Location', '/users')
                response.status = 303
                form_data = {'name': '', 'email': '', 'phone': '', 'birth_date': '', 'profile_picture_name': ''}

    # Сортировка пользователей по дате регистрации (новые первыми)
    users.sort(key=lambda x: x['registration_date'], reverse=True)

    return {
        'users': users,
        'title': 'Active users',
        'year': datetime.now().year,
        'errors': errors,
        'form_data': form_data
    }

def validate_user_form(data, file=None, existing_users=None):
    """
    Валидация данных формы пользователя и загруженного файла
    Аргументы:
        data (dict): Данные формы с ключами 'name', 'email', 'phone', 'birth_date', 'profile_picture_name'
        file: Объект загруженного файла (необязательно)
        existing_users (list): Список существующих пользователей для проверки уникальности
    Возвращает:
        list: Список сообщений об ошибках (пустой, если ошибок нет)
    """
    errors = []
    existing_users = existing_users or []

    # Проверка имени (не пустое, ≤ 64 символов, только латинские буквы)
    name = data.get('name', '').strip()
    if not name:
        errors.append("Name field is required!")
    elif len(name) > 64:
        errors.append("Name must be no more than 64 characters!")
    elif not re.match(r'^[a-zA-Z\s]+$', name):
        errors.append("Name must contain only Latin letters and spaces!")

    # Проверка email (валидный формат, разрешенный домен, уникальность)
    email = data.get('email', '').strip()
    if not email:
        errors.append("Email field is required!")
    elif not is_valid_email(email):
        errors.append("Invalid email format or domain. Please use email from allowed domains (e.g., gmail.com, mail.ru)!")
    elif any(user['email'].lower() == email.lower() for user in existing_users):
        errors.append("This email is already registered!")

    # Проверка телефона (валидный международный формат, уникальность)
    phone = data.get('phone', '').strip()
    if not phone:
        errors.append("Phone field is required!")
    else:
        try:
            parsed_phone = phonenumbers.parse(phone, 'RU')
            if not phonenumbers.is_valid_number(parsed_phone):
                errors.append("Invalid phone number. Example: +79123456789")
            elif any(user['phone'] == phone for user in existing_users):
                errors.append("This phone number is already registered!")
        except NumberParseException:
            errors.append("Invalid phone format. Use international format like +79123456789")

    # Проверка даты рождения (формат YYYY-MM-DD, возраст ≥ 14)
    birth_date = data.get('birth_date', '').strip()
    date_pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not birth_date:
        errors.append("Birth Date field is required!")
    elif not re.match(date_pattern, birth_date):
        errors.append("Birth Date must be in YYYY-MM-DD format (e.g., 2000-05-11)!")
    else:
        try:
            birth_date_obj = datetime.strptime(birth_date, '%Y-%m-%d').date()
            today = date.today()
            age = today.year - birth_date_obj.year - ((today.month, today.day) < (birth_date_obj.month, birth_date_obj.day))
            if age < 14:
                errors.append("You must be at least 14 years old to register!")
            if age > 100:
                errors.append("You must be younger than 100 years to register!")
            if birth_date_obj > today:
                errors.append("Birth Date cannot be in the future!")
        except ValueError:
            errors.append("Invalid Birth Date. Please check the entered values!")

    # Проверка загруженного файла (если предоставлен)
    if file and file.filename:
        allowed_extensions = {'.png', '.jpg', '.jpeg'}
        max_file_size = 5 * 1024 * 1024
        file_extension = file.filename.lower().rsplit('.', 1)[-1] if '.' in file.filename else ''
        if f'.{file_extension}' not in allowed_extensions:
            errors.append("Invalid file format. Only PNG, JPG and JPEG are allowed!")
        elif file.file and hasattr(file.file, 'seek'):
            try:
                file.file.seek(0, 2)
                file_size = file.file.tell()
                file.file.seek(0)
                if file_size > max_file_size:
                    errors.append("Profile picture size exceeds 5 MB!")
            except Exception:
                errors.append("Error while checking profile picture.")

    return errors

def is_valid_email(email):
    """
    Проверка формата email и разрешенных доменов
    Аргументы:
        email (str): Адрес электронной почты для проверки
    Возвращает:
        bool: True если email валиден, False в противном случае
    """
    if len(email) > 254 or len(email) < 1:
        return False
    
    parts = email.split('@')
    if len(parts) != 2:
        return False
    
    local_part, domain_part = parts
    
    if len(local_part) > 64 or len(local_part) < 1:
        return False
    
    if len(domain_part) > 255 or len(domain_part) < 1:
        return False
    
    local_pattern = r'^[a-zA-Z0-9][a-zA-Z0-9_%+-]*(?:\.[a-zA-Z0-9_%+-]+)*$'
    if not re.match(local_pattern, local_part):
        return False
    
    allowed_domains = [
        "google.com", "youtube.com", "facebook.com", "instagram.com",
        "x.com", "whatsapp.com", "wikipedia.org", "yahoo.com",
        "reddit.com", "yahoo.co.jp", "gmail.com", "mail.ru"
    ]
    
    return domain_part in allowed_domains