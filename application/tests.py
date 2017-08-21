import os
import json
from datetime import datetime, timedelta

from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp import web

from motor.motor_asyncio import AsyncIOMotorClient

from .routes import setup_routes
from .middlewaries import auth_middleware
from .helpers import encrypt_password


class AuthTest(AioHTTPTestCase):

    async def get_application(self):
        """
        Override the get_app method to return the project application.
        """
        app = web.Application(middlewares=[auth_middleware])
        setup_routes(app)

        app.db_client = AsyncIOMotorClient(
            os.getenv('MONGODB_HOST'), int(os.getenv('MONGODB_PORT')))
        app.db = app.db_client.asyncio_test_db
        return app

    def setUp(self):
        super().setUp()
        self.app.db_client.drop_database('asyncio_test_db')

    def tearDown(self):
        self.app.db_client.drop_database('asyncio_test_db')
        self.client.session.close()

    @unittest_run_loop
    async def test_registration(self):
        users = await self.app.db.auth.find().to_list(None)
        self.assertEqual(len(users), 0)
        data = json.dumps({"login": "test", "password": "test123"})
        request = await self.client.request("post", "/registration", data=data)
        self.assertEqual(request.status, 201)
        users = await self.app.db.auth.find().to_list(None)
        self.assertEqual(len(users), 1)

    @unittest_run_loop
    async def test_error_if_user_exists(self):
        login = "test"
        password = "test123"
        await self.app.db.auth.insert_one({
            'login': login,
            'password': password,
            'created_at': datetime.utcnow()
        })
        users = await self.app.db.auth.find().to_list(None)
        self.assertEqual(len(users), 1)
        data = json.dumps({"login": login, "password": password})
        request = await self.client.request("post", "/registration", data=data)
        self.assertEqual(request.status, 409)
        users = await self.app.db.auth.find().to_list(None)
        self.assertEqual(len(users), 1)

    @unittest_run_loop
    async def test_login_with_correct_data(self):
        login = "test"
        password = "test123"
        en_password = encrypt_password(password)

        await self.app.db.auth.insert_one({
            'login': login,
            'password': en_password,
            'created_at': datetime.utcnow()
        })
        data = json.dumps({"login": login, "password": password})
        request = await self.client.request("post", "/login", data=data)

        self.assertEqual(request.status, 200)
        content = json.loads(await request.content.read())
        self.assertIn('token', content)

    @unittest_run_loop
    async def test_login_with_wrong_data(self):
        login = "test"
        password = "test123"
        en_password = encrypt_password(password)

        await self.app.db.auth.insert_one({
            'login': login,
            'password': en_password,
            'created_at': datetime.utcnow()
        })
        data = json.dumps({"login": login, "password": "test1"})
        request = await self.client.request("post", "/login", data=data)

        self.assertEqual(request.status, 400)


class TreeTest(AioHTTPTestCase):

    async def get_application(self):
        """
        Override the get_app method to return the project application.
        """
        app = web.Application(middlewares=[auth_middleware])
        setup_routes(app)

        app.db_client = AsyncIOMotorClient(
            os.getenv('MONGODB_HOST'), int(os.getenv('MONGODB_PORT')))
        app.db = app.db_client.asyncio_test_db
        return app

    def setUp(self):
        super().setUp()
        self.app.db_client.drop_database('asyncio_test_db')

    def tearDown(self):
        self.app.db_client.drop_database('asyncio_test_db')
        self.client.session.close()

    async def get_token(self):
        self.login = "test"
        self.password = "test123"
        en_password = encrypt_password(self.password)
        await self.app.db.auth.insert_one({
            'login': self.login,
            'password': en_password,
            'created_at': datetime.utcnow()
        })
        data = json.dumps({"login": self.login, "password": self.password})
        request = await self.client.request("post", "/login", data=data)
        content = json.loads(await request.content.read())
        return content["token"]

    @unittest_run_loop
    async def test_add_object(self):
        objects = await self.app.db.tree.find().to_list(None)
        self.assertEqual(len(objects), 0)

        token = await self.get_token()
        headers = {"Authorization": token}
        data = json.dumps(
            {"id": 1, "text": "some text", "extra": {"field": "extra field"}})
        request = await self.client.request(
            "post", "/", headers=headers, data=data)
        self.assertEqual(request.status, 200)
        objects = await self.app.db.tree.find().to_list(None)
        self.assertEqual(len(objects), 1)

    @unittest_run_loop
    async def test_get_objects(self):
        await self.app.db.tree.insert_many([
            {'_id': 1, 'text': 'some text', "extra": {"field": "extra field"}},
            {
                '_id': 2, 'text': 'some text 2',
                "extra": {"field": "extra field2"}
            },
        ])

        token = await self.get_token()
        headers = {"Authorization": token}
        request = await self.client.request("get", "/", headers=headers)
        self.assertEqual(request.status, 200)
        content = json.loads(await request.content.read())
        self.assertEqual(len(content), 2)

    @unittest_run_loop
    async def test_get_object_details(self):
        obj_id = 1
        await self.app.db.tree.insert_one({
            '_id': obj_id, 'text': 'some text',
            "extra": {"field": "extra field"}
        })

        token = await self.get_token()
        headers = {"Authorization": token}
        request = await self.client.request(
            "get", "/detail/{0}".format(obj_id), headers=headers)
        self.assertEqual(request.status, 200)
        content = json.loads(await request.content.read())
        self.assertEqual(content["_id"], obj_id)

    @unittest_run_loop
    async def test_get_object_details(self):
        await self.app.db.tree.insert_many([
            {'_id': 1, 'text': 'some text', "extra": {"field": "extra field"}},
            {
                '_id': 2, 'text': 'another text',
                "extra": {"field": "another extra"}
            },
            {
                '_id': 3, 'text': 'object description',
                "extra": {"field": "object extra"}
            },
        ])

        token = await self.get_token()
        headers = {"Authorization": token}
        data = json.dumps({"query": "some text"})
        request = await self.client.request(
            "post", "/search", headers=headers, data=data)
        self.assertEqual(request.status, 200)
        content = json.loads(await request.content.read())
        self.assertEqual(len(content), 2)
