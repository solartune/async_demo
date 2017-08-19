import logging
import json
import os

from aiohttp.web import View, json_response, Response
from pymongo import ReturnDocument


from datetime import datetime, timedelta
import jwt

from .helpers import encrypt_password, check_password
from .decorators import login_required
from configs.settings import JWT_SECRET, JWT_ALGORITHM, JWT_EXP_DELTA_SECONDS


class AuthView:

    async def registration(self, request):
        data = await request.json()
        user = await request.app.db.auth.insert({
            'login': data['login'],
            'password': encrypt_password(data['password']),
            'created_at': datetime.utcnow()
        })
        return json_response({'message': 'New user has been created!'})

    async def login(self, request):
        data = await request.json()
        logging.info(data)
        user = await request.app.db.auth.find_one({'login': data['login']})
        if not check_password(data['password'], user['password']):
            return json_response({'message': 'Wrong credentials'}, status=400)

        payload = {
            'login': user['login'],
            'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
        }

        jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
        return json_response({'token': jwt_token.decode('utf-8')})


class TreeView:

    @login_required
    async def list(self, request):
        objects = request.app.db.tree.find()
        return json_response(await objects.to_list(None))

    @login_required
    async def add(self, request):
        data = await request.json()
        obj = await request.app.db.tree.find_one_and_update(
            {'_id': data['id']},
            {'$set': {'text': data['text']}},
            projection={'text': True, '_id': False},
            upsert=True,
            return_document=ReturnDocument.AFTER)
        return json_response(obj)

    @login_required
    async def detail(self, request):
        obj_id = int(request.match_info.get('obj_id'))
        obj = await request.app.db.tree.find_one({'_id': obj_id})
        return json_response(obj)

    @login_required
    async def search(self, request):
        data = await request.json()
        request.app.db.tree.create_index([('text', 'text')])
        objects = request.app.db.tree.find(
            {'$text': {'$search': data['query']}})

        return json_response(await objects.to_list(None))
