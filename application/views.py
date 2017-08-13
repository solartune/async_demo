import logging
import json
import os

from aiohttp.web import View, json_response, Response
from pymongo import ReturnDocument


class TreeView:

    async def list(self, request):
        objects = request.app.db.tree.find()
        return json_response(await objects.to_list(None))

    async def add(self, request):
        data = await request.json()
        obj = await request.app.db.tree.find_one_and_update(
            {'_id': data['id']},
            {'$set': {'text': data['text']}},
            projection={'text': True, '_id': False},
            upsert=True,
            return_document=ReturnDocument.AFTER)
        return json_response(obj)

    async def detail(self, request):
        obj_id = int(request.match_info.get('obj_id'))
        obj = await request.app.db.tree.find_one({'_id': obj_id})
        return json_response(obj)

    async def search(self, request):
        data = await request.json()
        request.app.db.tree.create_index([('text', 'text')])
        objects = request.app.db.tree.find(
            {'$text': {'$search': data['query']}})

        return json_response(await objects.to_list(None))
