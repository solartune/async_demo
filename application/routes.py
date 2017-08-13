from .views import TreeView
from aiohttp import web


def setup_routes(app):
    # handler = TreeView
    # app.router.add_get('/', handler.get)
    # app.router.add_post('/', handler.post)
    # app.router.add_get('/detail/{obj_id:\d+}', handler.get_object)
    # app.router.add_post('/search', handler.search)
    app.router.add_route('*', '/', TreeView)
