import os

from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorClient

from .routes import setup_routes

app = web.Application()
setup_routes(app)


app.db_client = AsyncIOMotorClient(
    os.getenv('MONGODB_HOST'), int(os.getenv('MONGODB_PORT')))
app.db = app.db_client.asyncio_db
