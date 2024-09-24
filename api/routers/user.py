from fastapi import APIRouter, HTTPException
from neomodel import config
from dotenv import load_dotenv
import os

import api.schemas.user as user_schema
from api.cruds.user import (
    create_user_func,
    get_user_by_id_func,
    login_user_func,
    update_user_labels_func,
)
from api.cruds.bert_matching import find_similar_users_neo4j  # 渡邊T追加分
from api.models.main import User

load_dotenv()

config.DATABASE_URL = os.getenv("NEO4J_URL")

router = APIRouter()


@router.get("/user", response_model=user_schema.UserReadResponse)
def get_user_by_id(id: str) -> dict[str, str]:
    user: User = get_user_by_id_func(id)
    return {
        "id": user.element_id,
        "name": user.name,
        "email": user.email,
        "is_available": user.is_available,
        "activity": user.activity,
        "latest_login": user.latest_login,
        "introduction": user.introduction,
        "profile_image": user.profile_image,
        "background_image": user.background_image,
    }


@router.post("/user/login", response_model=user_schema.UserReadResponse)
def login_user(item: user_schema.UserLoginRequest) -> dict[str, str]:
    user: User = login_user_func(email=item.email, password=item.password)
    return user


@router.post("/user/new", response_model=user_schema.UserCreateResponse)
def post_user(
    user: user_schema.UserCreateRequest,
) -> user_schema.UserCreateResponse:
    user: User = create_user_func(user.name, user.email, user.password, user.labels)
    return {"id": user.element_id}


# 渡邊T追加分
@router.get(
    "/user/similar/{user_id}", response_model=list[user_schema.SimilarUserResponse]
)
def get_similar_users(user_id: str) -> list:
    """指定されたユーザーIDに類似したユーザーを取得する"""
    user: User = get_user_by_id_func(id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    similar_users = find_similar_users_neo4j(user.name, top_k=15)
    return similar_users


@router.put("/user/labels/{user_id}", response_model=user_schema.UserReadResponse)
def update_user_labels(user_id: str, labels_data: user_schema.UserUpdateLabelsRequest):
    """ユーザーの属性を更新する"""
    user = update_user_labels_func(user_id, labels_data.labels)
    return {
        "id": user.element_id,
        "name": user.name,
        "email": user.email,
        "is_available": user.is_available,
        "activity": user.activity,
        "latest_login": user.latest_login,
        "introduction": user.introduction,
        "profile_image": user.profile_image,
        "background_image": user.background_image,
    }
