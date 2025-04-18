from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response, JSONResponse
from fastapi import Request, status
from cachetools import TTLCache
import time

from src.utils import AuthorizeBroker

# MIDDLEWARE
class TraderAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self,app):
        super().__init__(app)
        self.access_token_cache = TTLCache(maxsize=1000, ttl=800)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.url.path.startswith("/api/"):
            try:
                authorization = self.access_token_cache.get("bearer_token")
                if authorization:
                    request.state.auth_token = {
                        "token": authorization
                    }
                    response = await call_next(request)
                    return response
                access_token = AuthorizeBroker()
                authorization=f"Bearer {access_token}"
                self.access_token_cache["bearer_token"] = f"Bearer {access_token}"
                request.state.auth_token = {
                    "token":authorization
                }
                response = await call_next(request)
                return response
            except Exception as e:
                return JSONResponse(
                    content={"error": {"message": f"Error -> {e}"}},
                    status_code=status.HTTP_400_BAD_REQUEST
                )
        response = await call_next(request)
        return response