import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import vectordb
from contextlib import asynccontextmanager
import anyio
from typing import Iterator
import os

weaviate_port = os.getenv("EXPOSE_PORT", "16001")
API_ROOT_PATH = ""

@asynccontextmanager
async def lifespan(app: FastAPI):
    limiter = anyio.to_thread.current_default_thread_limiter()
    limiter.total_tokens = 300
    yield

app = FastAPI(lifespan=lifespan, root_path=API_ROOT_PATH)

# app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(vectordb.router)

@app.get("/")
async def home():
    return {"message": "Datalens Weaviate Service!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1221, reload=False)