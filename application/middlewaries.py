
from aiohttp.web import json_response

import jwt

from configs.settings import JWT_SECRET, JWT_ALGORITHM


async def auth_middleware(app, handler):
    async def middleware(request):
        request.user = None
        jwt_token = request.headers.get('Authorization', None)
        if jwt_token:
            try:
                payload = jwt.decode(
                    jwt_token, JWT_SECRET, algorithms=[JWT_ALGORITHM]
                )
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                return json_response(
                    {'message': 'Token is invalid'}, status=400)

            request.user = request.app.db.auth \
                .find_one({'login': payload['login']})
        return await handler(request)
    return middleware
