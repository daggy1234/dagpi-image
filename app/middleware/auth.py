from fastapi import Request
from fastapi.responses import JSONResponse

from ..utils.client import Client


async def auth_check(request: Request, call_next):
    if (request.url.path != "/") and (request.url.path != "/metrics/"):
        try:
            token = request.headers['Authorization']
        except KeyError:
            return JSONResponse({'message': 'Unauthorized'}, status_code=403)
        print(token)
        tok = await Client.auth(token)
        print(tok.auth)
        if tok.auth:
            if not tok.ratelimited:
                response = await call_next(request)
                return response
            else:
                return JSONResponse({'message': 'Ratelimited'}, status_code=429)
        else:
            return JSONResponse({'message': 'Unauthorized'}, status_code=403)
    else:
        response = await call_next(request)
        return response
