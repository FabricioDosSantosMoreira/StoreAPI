from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse
from store.core.config import settings
from store.routers import api_router


# Middleware to /docs
class RedirectToDocsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path == "/":
            return RedirectResponse(url="/docs")
        return await call_next(request)


class App(FastAPI):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            *args,
            **kwargs,
            version="0.0.1",
            title=settings.PROJECT_NAME,
            root_path=settings.ROOT_PATH,
        )

        self.add_middleware(RedirectToDocsMiddleware)
        self.include_router(api_router)


app = App()
