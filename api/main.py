from fastapi import FastAPI
from neomodel import config # 渡邊T追加分

from api.routers import user, post

app = FastAPI()

config.AUTO_INSTALL_LABELS = True  # uid の自動生成を有効にする

app.include_router(user.router)
app.include_router(post.router)

