import re

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app import auth
from app.database import Base, engine
from app.routers import categories, recipe_stats, recipes

Base.metadata.create_all(bind=engine)

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
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(recipe_stats.router)
app.include_router(recipes.router)
app.include_router(categories.router)


@app.get("/health")
def health():
    return {"status": "ok"}
