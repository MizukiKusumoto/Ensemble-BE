from fastapi import APIRouter

import api.schemas.user as user_schema


router = APIRouter()


@router.get("/user", response_model=user_schema.User)
async def get_users() -> dict[str, str]:
    return user_schema.User(
        id=1, name="Mizuki", email="test@test.com", password="password"
    )


@router.post("/user", response_model=user_schema.UserCreateResponse)
async def create_user(
    user: user_schema.UserCreateRequest,
) -> user_schema.UserCreateResponse:
    return user_schema.UserCreateResponse(
        id=1, name=user.name, email=user.email, password=user.password
    )
