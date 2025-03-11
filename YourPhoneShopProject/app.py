import bottle
import os
import sys
from bottle import template

import routes

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
        return template('views/viewFav.tpl', title='Favorites', year=2025)

    @bottle.route('/viewingProduct')
    def favorites():
        return template('views/viewingProduct.tpl', title='Product', year=2025)

    bottle.run(server='wsgiref', host=HOST, port=PORT)
