from fastapi import APIRouter
from neomodel import config
from datetime import datetime

import api.schemas.user as user_schema
from api.cruds.user import create_user_func, get_user_by_email_func, get_user_by_id_func, update_user_labels_func
from api.cruds.bert_matching import find_similar_users_neo4j # 渡邊T追加分
from api.models.main import User

config.DATABASE_URL = "bolt://neo4j:0oFKulfd@localhost:7687"

router = APIRouter()


@router.get("/user", response_model=user_schema.UserReadResponse)
def get_user_by_email(email: str) -> dict[str, str]:
    user: User = get_user_by_email_func(email)
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


@router.post("/user", response_model=user_schema.UserCreateResponse)
def post_user(
    user: user_schema.UserCreateRequest,
) -> user_schema.UserCreateResponse:
    user: User = create_user_func(user.name, user.email, user.password)
    return {"id": user.element_id}

# 渡邊T追加分
@router.get("/{uid}/similar", response_model=list[user_schema.SimilarUserResponse])
def get_similar_users(uid: str) -> list:
    """指定されたユーザーIDに類似したユーザーを取得する"""
    user: User = get_user_by_id_func(uid)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    similar_users = find_similar_users_neo4j(user.name, top_k=15)
    return similar_users

@router.put("/{uid}/labels", response_model=user_schema.UserReadResponse)
def update_user_labels(uid: str, labels_data: user_schema.UserUpdateLabelsRequest):
    """ユーザーの属性を更新する"""
    user = update_user_labels_func(uid, labels_data.labels)
    return {
        "id": user.uid,
        "name": user.name,
        "email": user.email,
        "is_available": user.is_available,
        "activity": user.activity,
        "latest_login": user.latest_login,
        "introduction": user.introduction,
        "profile_image": user.profile_image,
        "background_image": user.background_image,
    }