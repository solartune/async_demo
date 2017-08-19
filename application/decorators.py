from aiohttp.web import json_response


class login_required:

    def __init__(self, func):
        self.func = func

    def __call__(self, request):
        if not request.user:
            return json_response({'message': 'Login required'}, status=401)
        return self.func(self, request)
