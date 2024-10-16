from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from services.auth import AuthService


class SessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request,
        call_next
    ) -> Response:
        
        if not request.url.path.startswith('/api') \
            or request.url.path.startswith('/api/signup') \
            or request.url.path.startswith('/api/signin') \
            or request.url.path.startswith('/api/logout') \
            or request.url.path.startswith('/api/ping'):

            return await call_next(request)

        session_id = request.cookies.get("session")

        if not session_id:
            response = Response(status_code=401)
            response.delete_cookie("session")
            return response

        username = AuthService().get_username(session_id)

        if not username:
            response = Response(status_code=401)
            response.delete_cookie("session")
            return response

        response = await call_next(request)
        return response
