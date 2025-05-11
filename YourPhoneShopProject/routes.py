"""
Routes and views for the bottle application.
"""

from bottle import route, view
from datetime import datetime
import json

@route('/')
@route('/home')
@view('index')
def home():
    """Renders the home page."""
    return dict(
        year=datetime.now().year
    )

@route('/contact')
@view('contact')
def contact():
    """Renders the contact page."""
    return dict(
        title='Contact',
        message='Your contact page.',
        year=datetime.now().year
    )

@route('/about')
@view('about')
def about():
    """Renders the about page."""
    return dict(
        title='About',
        message='Your application description page.',
        year=datetime.now().year
    )

@route('/users')
@view('viewUsers')
def show_users():
    try:
        with open('static\\jsons\\active_users.json', 'r', encoding='utf-8') as file:
            users = json.load(file)
        print("users:", users)
    except FileNotFoundError:
        users = []
        print("users:", users)

    return dict(
        users=users,
        title='Users',
        year=2025
    )
