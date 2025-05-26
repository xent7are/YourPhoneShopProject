# -*- coding: cp1251 -*-

import unittest
import os
import json
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from datetime import datetime
import uuid

# ������ ����������� �������
from static.controllers.partners_controller import (
    load_partners,
    save_partners,
    partners_get,
    partners_post,
    delete_partner
)

class TestPartnersController(unittest.TestCase):
    def setUp(self):
        # ������� ��������� ���������� ��� ������
        self.test_dir = tempfile.mkdtemp()
        self.partners_file = os.path.join(self.test_dir, 'active_partners.json')
        self.upload_dir = os.path.join(self.test_dir, 'images/partners')
        
        # ��������� ���� � ������
        from static.controllers import partners_controller
        partners_controller.PARTNERS_FILE = self.partners_file
        partners_controller.UPLOAD_DIR = self.upload_dir
        
        # ������ ������ ���������
        self.sample_partners = [
            {
                'name': 'Partner 1',
                'email': 'partner1@test.com',
                'address': 'Address 1',
                'region_code': '+1',
                'phone': '1234567890',
                'description': 'Description 1',
                'date': '2023-01-01',
                'logo': '/static/images/partners/logo1.png'
            },
            {
                'name': 'Partner 2',
                'email': 'partner2@test.com',
                'address': 'Address 2',
                'region_code': '+7',
                'phone': '9876543210',
                'description': 'Description 2',
                'date': '2023-02-01',
                'logo': ''
            }
        ]
        
        # ������� �������� ���� � ����������
        with open(self.partners_file, 'w') as f:
            json.dump(self.sample_partners, f, indent=4)
    
    def tearDown(self):
        # ������� ��������� ����������
        shutil.rmtree(self.test_dir)
    
    def test_load_partners(self):
        # ���� �������� ������������ ���������
        partners = load_partners()
        self.assertEqual(len(partners), 2)
        self.assertEqual(partners[0]['name'], 'Partner 1')
        
        # ���� �������� �� ��������������� �����
        os.remove(self.partners_file)
        partners = load_partners()
        self.assertEqual(partners, [])
    
    def test_save_partners(self):
        # ���� ���������� ���������
        new_partners = self.sample_partners.copy()
        new_partners.append({
            'name': 'New Partner',
            'email': 'new@test.com',
            'address': 'New Address',
            'region_code': '+44',
            'phone': '1111111111',
            'description': 'New Description',
            'date': '2023-03-01',
            'logo': ''
        })
        
        save_partners(new_partners)
        
        with open(self.partners_file, 'r') as f:
            saved_partners = json.load(f)
        
        self.assertEqual(len(saved_partners), 3)
        self.assertEqual(saved_partners[2]['name'], 'New Partner')
    
    @patch('static.controllers.partners_controller.template')
    def test_partners_get(self, mock_template):
        # ���� GET-�������
        result = partners_get()
        
        # ���������, ��� template ������ � ����������� �����������
        mock_template.assert_called_once_with(
            'partners.tpl',
            partners=sorted(self.sample_partners, key=lambda x: x['date'], reverse=True),
            errors=None,
            form_data={},
            year=datetime.now().year
        )
    
    @patch('static.controllers.partners_controller.template')
    @patch('static.controllers.partners_controller.request')
    @patch('static.controllers.partners_controller.uuid.uuid4')
    @patch('os.makedirs')
    @patch('os.path.exists', return_value=True)
    def test_partners_post_valid(self, mock_exists, mock_makedirs, mock_uuid, mock_request, mock_template):
        # ���� POST-������� � ��������� �������
        mock_request.forms = {
            'name': 'New Partner',
            'email': 'new@test.com',
            'address': 'Valid Address 123',
            'region_code': '+1',
            'phone': '(123) 456-7890',
            'description': 'Test Description'
        }
    
        # ����������� ��� ��� uuid
        test_uuid = 'test-uuid-123'
        mock_uuid.return_value = test_uuid
    
        # ��� ����� ��������
        mock_file = MagicMock()
        mock_file.filename = 'logo.png'
        mock_file.content_type = 'image/png'
        mock_file.content_length = 1024  # 1KB
        mock_request.files = {'partner_logo': mock_file}
    
        result = partners_post()
    
        # ���������, ��� template ������ � ������� ��������
        self.assertEqual(mock_template.call_args[1]['errors'], None)
    
        # ���������, ��� ������� ��������
        with open(self.partners_file, 'r') as f:
            partners = json.load(f)
    
        self.assertEqual(len(partners), 3)
        self.assertEqual(partners[2]['name'], 'New Partner')
    
        # ���������, ��� ���� � �������� ����������� ���������
        expected_logo_path = f"/{self.upload_dir}/{test_uuid}.png"
        self.assertEqual(partners[2]['logo'], expected_logo_path)
    
        # ���������, ��� ���� ������� ������ ������ ��� ���������� �����
        mock_makedirs.assert_called_once_with(self.upload_dir, exist_ok=True)
        mock_file.save.assert_called_once_with(os.path.join(self.upload_dir, f"{test_uuid}.png"))
    
    @patch('static.controllers.partners_controller.template')
    @patch('static.controllers.partners_controller.request')
    def test_partners_post_invalid(self, mock_request, mock_template):
        # ���� POST-������� � ����������� �������
        mock_request.forms = {
            'name': '',  # ������ ���
            'email': 'invalid-email',  # ���������� email
            'address': 'Short',  # ������� �������� �����
            'region_code': '+999',  # ���������� ��� �������
            'phone': '123',  # ���������� �������
            'description': ''
        }
        mock_request.files = {'partner_logo': None}
        
        result = partners_post()
        
        # ���������, ��� ��������� ��� ������
        errors = mock_template.call_args[1]['errors']
        self.assertIn("Name or Company is required.", errors)
        self.assertIn("Invalid email format.", errors)
        self.assertIn("The address must not contain less than 15 characters.", errors)
        self.assertIn("Invalid region code.", errors)
        self.assertIn("Phone number must be exactly 10 digits (e.g., (123) 456-7890).", errors)
        
        # ���������, ��� ������ ����� ���������� �������
        form_data = mock_template.call_args[1]['form_data']
        self.assertEqual(form_data['email'], 'invalid-email')
    
    @patch('static.controllers.partners_controller.template')
    @patch('static.controllers.partners_controller.request')
    def test_partners_post_invalid_file(self, mock_request, mock_template):
        # ���� � ���������� ������ ��������
        mock_request.forms = {
            'name': 'Valid Name',
            'email': 'valid@test.com',
            'address': 'Valid Address 123',
            'region_code': '+1',
            'phone': '(123) 456-7890',
            'description': ''
        }
        
        # ��� ������� �������� �����
        mock_file = MagicMock()
        mock_file.filename = 'big_logo.png'
        mock_file.content_type = 'image/png'
        mock_file.content_length = 6 * 1024 * 1024  # 6MB
        mock_request.files = {'partner_logo': mock_file}
        
        result = partners_post()
        
        errors = mock_template.call_args[1]['errors']
        self.assertIn("Logo file size must not exceed 5MB.", errors)
        
        # ��� ����� � �������� �����
        mock_file.content_length = 1024  # 1KB
        mock_file.content_type = 'application/pdf'
        result = partners_post()
        
        errors = mock_template.call_args[1]['errors']
        self.assertIn("Logo must be a PNG or JPG file.", errors)
    
    @patch('static.controllers.partners_controller.request')
    @patch('static.controllers.partners_controller.response')
    def test_delete_partner_valid(self, mock_response, mock_request):
        # ���� �������� ������������� ��������
        mock_request.body = MagicMock()
        mock_request.body.read.return_value = json.dumps({'partner_id': 0}).encode('utf-8')
        
        # ������� �������� �������
        os.makedirs(self.upload_dir, exist_ok=True)
        test_logo_path = os.path.join(self.upload_dir, 'test_logo.png')
        with open(test_logo_path, 'w') as f:
            f.write('test')
        
        # ��������� ������ �������� � ���������
        with open(self.partners_file, 'r+') as f:
            partners = json.load(f)
            partners[0]['logo'] = f'/{self.upload_dir}/test_logo.png'
            f.seek(0)
            json.dump(partners, f, indent=4)
            f.truncate()
        
        result = delete_partner()
        
        # ��������� �����
        self.assertEqual(json.loads(result)['status'], 'success')
        
        # ���������, ��� ������� ������
        with open(self.partners_file, 'r') as f:
            partners = json.load(f)
        
        self.assertEqual(len(partners), 1)
        
        # ���������, ��� ������� ������
        self.assertFalse(os.path.exists(test_logo_path))
    
    @patch('static.controllers.partners_controller.request')
    @patch('static.controllers.partners_controller.response')
    def test_delete_partner_invalid_id(self, mock_response, mock_request):
        # ���� �������� � ���������� ID
        mock_request.body = MagicMock()
        mock_request.body.read.return_value = json.dumps({'partner_id': 999}).encode('utf-8')
        
        result = delete_partner()
        
        # ��������� ����� �� ������
        response_data = json.loads(result)
        self.assertEqual(response_data['status'], 'error')
        self.assertEqual(response_data['message'], 'Invalid partner ID')
        self.assertEqual(mock_response.status, 400)
    
    @patch('static.controllers.partners_controller.request')
    @patch('static.controllers.partners_controller.response')
    def test_delete_partner_no_logo(self, mock_response, mock_request):
        # ���� �������� �������� ��� ��������
        mock_request.body = MagicMock()
        mock_request.body.read.return_value = json.dumps({'partner_id': 1}).encode('utf-8')
        
        result = delete_partner()
        
        # ��������� �����
        self.assertEqual(json.loads(result)['status'], 'success')
        
        # ���������, ��� ������� ������
        with open(self.partners_file, 'r') as f:
            partners = json.load(f)
        
        self.assertEqual(len(partners), 1)
    
    @patch('static.controllers.partners_controller.request')
    @patch('static.controllers.partners_controller.response')
    def test_delete_partner_exception(self, mock_response, mock_request):
        # ���� ��������� ����������
        mock_request.body = MagicMock()
        mock_request.body.read.side_effect = Exception("Test error")
        
        result = delete_partner()
        
        # ��������� ����� �� ������
        response_data = json.loads(result)
        self.assertEqual(response_data['status'], 'error')
        self.assertEqual(response_data['message'], 'Test error')
        self.assertEqual(mock_response.status, 500)

if __name__ == '__main__':
    unittest.main()