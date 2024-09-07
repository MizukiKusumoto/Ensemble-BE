from fastapi import APIRouter
from neomodel import config
from datetime import datetime

import api.schemas.user as user_schema
from api.cruds.user import create_user, get_user_by_email
from api.models.main import User

config.DATABASE_URL = "bolt://neo4j:neo4jtest@localhost:7687"

router = APIRouter()


@router.get("/user", response_model=user_schema.UserReadResponse)
def get_user(email: str) -> dict[str, str]:
    user: User = get_user_by_email(email)
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
    user: User = create_user(user.name, user.email, user.password)
    return {"id": user.element_id}
