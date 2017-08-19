from aiohttp import web

from .views import TreeView, AuthView


def setup_routes(app):
    tree_handler = TreeView()
    auth_handler = AuthView()
    app.router.add_get('/', tree_handler.list)
    app.router.add_post('/', tree_handler.add)
    app.router.add_get('/detail/{obj_id:\d+}', tree_handler.detail)
    app.router.add_post('/search', tree_handler.search)
    app.router.add_post('/registration', auth_handler.registration)
    app.router.add_post('/login', auth_handler.login)
