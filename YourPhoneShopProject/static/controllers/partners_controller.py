from bottle import route, post, request, template, response
import json
import os
import re
from datetime import datetime
import uuid

PARTNERS_FILE = 'static/jsons/active_partners.json'
UPLOAD_DIR = 'static/images/partners'

def load_partners():# �������� ����� � ���������
    if os.path.exists(PARTNERS_FILE):
        with open(PARTNERS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_partners(partners):# ���������� �������� � ����
    with open(PARTNERS_FILE, 'w') as f:
        json.dump(partners, f, indent=4)

@route('/partners')
def partners_get(): # �������� ������������ ��������
    partners = load_partners()
    # ���������� �������� �� �������
    partners.sort(key=lambda x: x.get('date', ''), reverse=True)
    return template('partners.tpl', partners=partners, errors=None, form_data={}, year=datetime.now().year)

@post('/partners')
def partners_post(): # ������ ������ �� ����� ���������� ��������
    name = request.forms.get('name').strip()
    email = request.forms.get('email').strip()
    address = request.forms.get('address').strip()
    region_code = request.forms.get('region_code').strip()
    phone = request.forms.get('phone').strip()
    partner_logo = request.files.get('partner_logo')
    
    errors = []
    form_data = {
        'name': name,
        'email': email,
        'address': address,
        'region_code': region_code,
        'phone': phone
    }
    
    # ��������
    if not name:
        errors.append("Name or Company is required.")
    if not email:
        errors.append("Email is required.")
    elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        errors.append("Invalid email format.")
    if not address:
        errors.append("Address is required.")
    elif len(address) > 200:
        errors.append("Address must not exceed 200 characters.")
    elif len(address) < 15:
        errors.append("The address must not contain less than 15 characters.")
    if phone:
        phone_digits = phone.replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
        if not re.match(r'^\d{10}$', phone_digits):
            errors.append("Phone number must be exactly 10 digits (e.g., (123) 456-7890).")
    if not region_code:
        errors.append("Region code is required.")
    elif region_code not in ['+1', '+7', '+44', '+33', '+49']:
        errors.append("Invalid region code.")
    if partner_logo:
        if partner_logo.content_length > 5 * 1024 * 1024:
            errors.append("Logo file size must not exceed 5MB.")
        if not partner_logo.content_type in ['image/png', 'image/jpeg']:
            errors.append("Logo must be a PNG or JPG file.")
    
    if errors: # ��������� ������ ������������ � ��������������� ������
        partners = load_partners()
        partners.sort(key=lambda x: x.get('date', ''), reverse=True)
        return template('partners.tpl', partners=partners, errors=errors, form_data=form_data, year=datetime.now().year)
    
    # ���������� �������� �������
    logo_path = ''
    if partner_logo:
        os.makedirs(UPLOAD_DIR, exist_ok=True) # �������� ���������� ��� ����������
        file_extension = os.path.splitext(partner_logo.filename)[1].lower() # ���������� ���������� �� ������������ �����
        filename = f"{uuid.uuid4()}{file_extension}"
        logo_path = f"/{UPLOAD_DIR}/{filename}"
        partner_logo.save(os.path.join(UPLOAD_DIR, filename))
    
    # ���������� ������ �������
    partners = load_partners()
    new_partner = {
        'name': name,
        'email': email,
        'address': address,
        'region_code': region_code,
        'phone': phone,
        'description': request.forms.get('description').strip(),
        'date': datetime.now().strftime('%Y-%m-%d'),
        'logo': logo_path
    }
    partners.append(new_partner)
    save_partners(partners)
    
    # ������� �����
    return template('partners.tpl', partners=partners, errors=None, form_data={}, year=datetime.now().year)

@post('/delete_partner')
def delete_partner():
    try:
        data = json.load(request.body)
        partner_id = int(data.get('partner_id'))
        partners = load_partners()
        
        if 0 <= partner_id < len(partners):
            # Remove logo file if exists
            if partners[partner_id]['logo']:
                logo_path = partners[partner_id]['logo'].lstrip('/')
                if os.path.exists(logo_path):
                    os.remove(logo_path)
            partners.pop(partner_id)
            save_partners(partners)
            response.content_type = 'application/json'
            return json.dumps({'status': 'success'})
        else:
            response.status = 400
            return json.dumps({'status': 'error', 'message': 'Invalid partner ID'})
    except Exception as e:
        response.status = 500
        return json.dumps({'status': 'error', 'message': str(e)})