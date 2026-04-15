import re

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app import auth
from app.routers import categories, recipe_stats, recipes
from app.routers.admin import router as admin_router
from app.routers.catalog import router as catalog_router
from app.settings import settings

app = FastAPI()


class NormalizePathMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        path = request.scope.get("path", "")
        normalized = re.sub(r"/+", "/", path)
        if path != normalized:
            request.scope["path"] = normalized
            request.scope["raw_path"] = normalized.encode()
        response = await call_next(request)
        return response


app.add_middleware(NormalizePathMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(recipe_stats.router)
app.include_router(recipes.router)
app.include_router(categories.router)
app.include_router(catalog_router)
app.include_router(admin_router)


@app.get("/health")
def health():
    return {"status": "ok"}
