import json
import os
import re
from bottle import request, response
from datetime import datetime, date
import phonenumbers
from phonenumbers import NumberParseException, is_valid_number

def get_users():
    # Читает список пользователей из JSON-файла.
    json_file = 'static/jsons/active_users.json'
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except Exception:
        raise

def save_users(users):
    # Сохраняет список пользователей в JSON-файл.
    json_file = 'static/jsons/active_users.json'
    try:
        with open(json_file, 'w', encoding='utf-8') as file:
            json.dump(users, file, ensure_ascii=False, indent=4)
    except Exception:
        raise

def is_valid_email(email):
    """
    Проверяет формат email и разрешенные домены.
    Аргументы:
        email (str): Адрес электронной почты для проверки.
    Возвращает:
        bool: True, если email валиден, False в противном случае.
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

def validate_user_form(data, file=None, existing_users=None):
    """
    Проверяет данные формы пользователя и загруженный файл.
    Аргументы:
        data (dict): Данные формы с ключами 'name', 'email', 'phone', 'birth_date'.
        file: Объект загруженного файла (необязательно).
        existing_users (list): Список существующих пользователей для проверки уникальности.
    Возвращает:
        list: Список сообщений об ошибках (пустой, если ошибок нет).
    """
    errors = []
    existing_users = existing_users or []

    # Проверяем имя (не пустое, ≤ 64 символов, только латинские буквы)
    name = data.get('name', '').strip()
    if not name:
        errors.append("Поле 'Имя' обязательно для заполнения!")
    elif len(name) > 64:
        errors.append("Имя должно содержать не более 64 символов!")
    elif not re.match(r'^[a-zA-Z]+$', name):
        errors.append("Имя должно содержать только латинские буквы!")

    # Проверяем email (валидный формат, разрешенный домен, уникальность)
    email = data.get('email', '').strip()
    if not email:
        errors.append("Поле 'Email' обязательно для заполнения!")
    elif not is_valid_email(email):
        errors.append("Неверный формат email или домен. Используйте email из разрешенных доменов (например, gmail.com, mail.ru)!")
    elif any(user['email'].lower() == email.lower() for user in existing_users):
        errors.append("Этот email уже зарегистрирован!")

    # Проверяем телефон (валидный международный формат, уникальность)
    phone = data.get('phone', '').strip()
    if not phone:
        errors.append("Поле 'Телефон' обязательно для заполнения!")
    else:
        try:
            parsed_phone = phonenumbers.parse(phone, None)
            if not is_valid_number(parsed_phone):
                errors.append("Неверный номер телефона. Введите действующий номер телефона (например, +71234567890)!")
            elif any(user['phone'] == phone for user in existing_users):
                errors.append("Этот номер телефона уже зарегистрирован!")
        except NumberParseException:
            errors.append("Неверный формат номера телефона. Используйте правильный формат (например, +71234567890)!")

    # Проверяем дату рождения (формат YYYY-MM-DD, возраст ≥ 14)
    birth_date = data.get('birth_date', '').strip()
    date_pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not birth_date:
        errors.append("Поле 'Дата рождения' обязательно для заполнения!")
    elif not re.match(date_pattern, birth_date):
        errors.append("Дата рождения должна быть в формате ГГГГ-ММ-ДД (например, 2000-05-11)!")
    else:
        try:
            birth_date_obj = datetime.strptime(birth_date, '%Y-%m-%d').date()
            today = date.today()
            age = today.year - birth_date_obj.year - ((today.month, today.day) < (birth_date_obj.month, birth_date_obj.day))
            if age < 14:
                errors.append("Вы должны быть старше 14 лет для регистрации!")
            if age > 100:
                errors.append("Вы должны быть младше 100 лет для регистрации!")
            if birth_date_obj > today:
                errors.append("Дата рождения не может быть в будущем!")
        except ValueError:
            errors.append("Неверная дата рождения. Проверьте введенные значения!")

    # Проверяем загруженный файл (если предоставлен)
    if file and file.filename:
        allowed_extensions = {'.png', '.jpg', '.jpeg'}
        max_file_size = 5 * 1024 * 1024
        file_extension = file.filename.lower().rsplit('.', 1)[-1] if '.' in file.filename else ''
        if f'.{file_extension}' not in allowed_extensions:
            errors.append("Неверный формат файла. Разрешены только PNG, JPG и JPEG!")
        elif file.file and hasattr(file.file, 'seek'):
            try:
                file.file.seek(0, 2)
                file_size = file.file.tell()
                file.file.seek(0)
                if file_size > max_file_size:
                    errors.append("Размер изображения профиля превышает 5 МБ!")
            except Exception:
                errors.append("Ошибка при проверке изображения профиля.")

    return errors

def handle_users():
    # Обрабатывает GET и POST запросы для страницы пользователей.
    users = get_users()
    errors = []
    form_data = {'name': '', 'email': '', 'phone': '', 'birth_date': ''}

    if request.method == 'POST':
        # Получаем данные формы
        form_data['name'] = request.forms.get('name', '').strip()
        form_data['email'] = request.forms.get('email', '').strip()
        form_data['phone'] = request.forms.get('phone', '').strip()
        form_data['birth_date'] = request.forms.get('birth_date', '').strip()
        profile_picture = request.files.get('profile_picture')

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

            # Сохраняем фотографию, если она загружена
            if profile_picture and profile_picture.file:
                try:
                    file_extension = profile_picture.filename.rsplit('.', 1)[-1].lower()
                    filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{form_data['name'].replace(' ', '_')}.{file_extension}"
                    save_path = os.path.join('static', 'images', 'profiles', filename)
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)
                    profile_picture.save(save_path, overwrite=True)
                    new_user['profile_picture'] = f"/static/images/profiles/{filename}"
                except Exception:
                    errors.append("Не удалось сохранить изображение профиля.")

            if not errors:
                users.append(new_user)
                users.sort(key=lambda x: x['registration_date'], reverse=True)
                save_users(users)
                response.set_header('Location', '/users')
                response.status = 303
                form_data = {'name': '', 'email': '', 'phone': '', 'birth_date': ''}

    # Сортируем пользователей по дате регистрации (новые первыми)
    users.sort(key=lambda x: x['registration_date'], reverse=True)

    return {
        'users': users,
        'title': 'Активные пользователи',
        'year': datetime.now().year,
        'errors': errors,
        'form_data': form_data
    }

def delete_user():
    # Удаляет пользователя по ID.
    user_id = request.json.get('user_id')
    users = get_users()
    if 0 <= int(user_id) < len(users):
        if users[int(user_id)].get('profile_picture'):
            try:
                os.remove(users[int(user_id)]['profile_picture'].lstrip('/'))
            except OSError:
                pass
        users.pop(int(user_id))
        save_users(users)
        return {'status': 'success'}
    else:
        response.status = 400
        return {'status': 'error', 'message': 'Неверный ID пользователя'}