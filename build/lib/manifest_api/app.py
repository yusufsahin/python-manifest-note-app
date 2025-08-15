import os, ujson
from fastapi import FastAPI
from .db import engine, Base
from .runtime import make_models
from .dyn_crud import build_router

def create_app(manifest_path: str) -> FastAPI:
    Base.metadata.create_all(bind=engine)
    app = FastAPI(title="manifest-api", version="0.1.0")

    @app.get("/health", tags=["health"])
    def health():
        return {"ok": True}

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = ujson.load(f)

    for entity in manifest.get("entities", []):
        CreateModel, UpdateModel, OutModel = make_models(entity)
        router = build_router(entity, CreateModel, UpdateModel, OutModel)
        app.include_router(router)

    return app
