import os

from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorClient
from aiohttp_swagger import setup_swagger

from .routes import setup_routes
from .middlewaries import auth_middleware


app = web.Application(middlewares=[auth_middleware])
setup_routes(app)
setup_swagger(app)

app.db_client = AsyncIOMotorClient(
    os.getenv('MONGODB_HOST'), int(os.getenv('MONGODB_PORT')))
app.db = app.db_client.asyncio_db
