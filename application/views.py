import logging
import json
import os

from aiohttp.web import View, json_response, Response
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument

logger = logging.getLogger(__file__)


class TreeView(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_client = AsyncIOMotorClient(
            os.getenv('MONGODB_HOST'), int(os.getenv('MONGODB_PORT')))
        self.db = self.db_client.asyncio_db

    async def get(self):
        objects = self.db.tree.find()
        return json_response(await objects.to_list(None))

    async def post(self):
        data = await self.request.json()
        obj = await self.db.tree.find_one_and_update(
            {'_id': data['id']},
            {'$set': {'text': data['text']}},
            projection={'text': True, '_id': False},
            upsert=True,
            return_document=ReturnDocument.AFTER)
        return json_response({'obj': str(obj)})

    async def get_object(self):
        obj_id = self.match_info.get('obj_id')
        data = {'type': 'get_object', 'obj_id': obj_id}
        return json_response(data)

    async def search(self):
        data = {'type': 'search'}
        return json_response(data)
