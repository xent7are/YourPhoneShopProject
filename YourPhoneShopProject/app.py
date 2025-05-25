import bottle
import os
import sys
from bottle import template
from datetime import datetime

import routes
from static.controllers.partners_controller import *

if '--debug' in sys.argv[1:] or 'SERVER_DEBUG' in os.environ:
    bottle.debug(True)

def wsgi_app():
    return bottle.default_app()

if __name__ == '__main__':
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static').replace('\\', '/')
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555

    @bottle.route('/static/<filepath:path>')
    def server_static(filepath):
        return bottle.static_file(filepath, root=STATIC_ROOT)

    @bottle.route('/favorites')
    def favorites():
        return template('views/viewFav.tpl', title='Favorites', year=datetime.now().year)

    @bottle.route('/viewingProduct')
    def viewing_product():
        return template('views/viewingProduct.tpl', title='Product', year=datetime.now().year)

    bottle.run(server='wsgiref', host=HOST, port=PORT)