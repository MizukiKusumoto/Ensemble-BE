from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from api.routers import user, post

app = FastAPI()

origins = [
    "http://localhost:3000",  # フロントエンドのURL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(post.router)

# ルートディレクトリの「data」フォルダへのパスを設定
UPLOAD_DIR = Path(__file__).parent.parent / "data"

# 「/data」エンドポイントで、アップロードされた画像を提供
app.mount("/data", StaticFiles(directory=UPLOAD_DIR), name="data")
