import logging
import json
import os
from datetime import datetime, timedelta

from aiohttp.web import View, json_response, Response
from pymongo import ReturnDocument
import jwt

from .helpers import encrypt_password, check_password
from .decorators import login_required
from configs.settings import JWT_SECRET, JWT_ALGORITHM, JWT_EXP_DELTA_SECONDS


class AuthView:

    async def registration(self, request):
        """Registration new users in the system."""
        request.app.db.auth.create_index("login", unique=True)
        data = await request.json()
        user = await request.app.db.auth.find_one({'login': data['login']})
        if user:
            return json_response(
                {'message': 'This user already exists'}, status=409)
        await request.app.db.auth.insert_one({
            'login': data['login'],
            'password': encrypt_password(data['password']),
            'created_at': datetime.utcnow()
        })
        return json_response(
            {'message': 'New user has been created!'}, status=201)

    async def login(self, request):
        """Authorize users in the system."""
        data = await request.json()
        user = await request.app.db.auth.find_one({'login': data['login']})

        if not user or not check_password(data['password'], user['password']):
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
        """Shows all objects from the database."""
        objects = await request.app.db.tree.find().to_list(None)
        return json_response(objects)

    @login_required
    async def add(self, request):
        """Adds new object to the system."""
        data = await request.json()
        obj = await request.app.db.tree.find_one_and_update(
            {'_id': data['id']},
            {'$set': {'text': data['text'], 'extra': data['extra']}},
            upsert=True,
            return_document=ReturnDocument.AFTER)
        return json_response(obj)

    @login_required
    async def detail(self, request):
        """Shows one object by its id."""
        obj_id = int(request.match_info.get('obj_id'))
        obj = await request.app.db.tree.find_one({'_id': obj_id})
        if not obj:
            return json_response({
                'message': 'Object with id {0} does not exists'.format(obj_id)
            }, status=404)
        return json_response(obj)

    @login_required
    async def search(self, request):
        """Shows have found objects by a query."""
        data = await request.json()
        request.app.db.tree.create_index([('text', 'text')])
        objects = await request.app.db.tree.find(
            {'$text': {'$search': data['query']}}).to_list(None)

        return json_response(objects)
