"""
Routes and views for the bottle application.
"""

from bottle import route, view, request, response
from datetime import datetime
from static.controllers.user_controller import handle_users, delete_user

@route('/')
@route('/home')
@view('index')
def home():
    """Renders the home page."""
    return dict(
        title='Home',
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

@route('/users', method=['GET', 'POST'])
@view('viewUsers')
def users():
    """Renders the users page."""
    result = handle_users()
    if result is None:  # Перенаправление после POST
        return
    return result

@route('/delete_user', method='POST')
def delete_user_route():
    """Handles user deletion."""
    return delete_user()