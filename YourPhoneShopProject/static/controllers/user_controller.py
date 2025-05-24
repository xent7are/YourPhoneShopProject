import json
from bottle import request, response
from datetime import datetime
from static.controllers.validate_users import validate_user_form

def get_users():
    # ������ ������ ������������� �� JSON-�����.
    json_file = 'static/jsons/active_users.json'
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_users(users):
    # ��������� ������ ������������� � JSON-����.
    json_file = 'static/jsons/active_users.json'
    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump(users, file, ensure_ascii=False, indent=4)

def handle_users():
    # ������������ GET � POST ������� ��� �������� �������������.
    users = get_users()
    errors = []
    form_data = {'name': '', 'email': '', 'phone': '', 'birth_date': ''}

    if request.method == 'POST':
        # �������� ������ �����
        form_data['name'] = request.forms.get('name', '').strip()
        form_data['email'] = request.forms.get('email', '').strip()
        form_data['phone'] = request.forms.get('phone', '').strip()
        form_data['birth_date'] = request.forms.get('birth_date', '').strip()

        # ��������� ������
        errors = validate_user_form(form_data)

        # ���� ��� ������, ��������� ������������
        if not errors:
            new_user = {
                'name': form_data['name'],
                'email': form_data['email'],
                'phone': form_data['phone'],
                'birth_date': form_data['birth_date'],
                'registration_date': datetime.now().strftime('%Y-%m-%d')
            }
            users.append(new_user)
            # ���������� �� ���� ����������� (����� � ������)
            users.sort(key=lambda x: x['registration_date'], reverse=True)
            save_users(users)
            # ��������������� ��� ������� �����
            response.set_header('Location', '/users')
            response.status = 303
            # ������� ����� ����� ��������� ����������
            form_data = {'name': '', 'email': '', 'phone': '', 'birth_date': ''}

    return {
        'users': users,
        'title': 'Active Users',
        'year': datetime.now().year,
        'errors': errors,
        'form_data': form_data
    }

def delete_user():
    # ������� ������������ �� ID.
    user_id = request.json.get('user_id')
    try:
        users = get_users()
        if 0 <= int(user_id) < len(users):
            users.pop(int(user_id))
            save_users(users)
            return {'status': 'success'}
        else:
            response.status = 400
            return {'status': 'error', 'message': 'Invalid user ID'}
    except Exception as e:
        response.status = 500
        return {'status': 'error', 'message': str(e)}