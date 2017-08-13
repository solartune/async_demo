from aiohttp import web

from .views import TreeView


def setup_routes(app):
    handler = TreeView()
    app.router.add_get('/', handler.list)
    app.router.add_post('/', handler.add)
    app.router.add_get('/detail/{obj_id:\d+}', handler.detail)
    app.router.add_post('/search', handler.search)
