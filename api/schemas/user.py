from pydantic import BaseModel, Field
from typing import List, Optional  # 渡邊T追加分
import datetime


class UserCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=8, max_length=50)
    labels: list[str] = Field(...)


class UserCreateResponse(BaseModel):
    id: str = Field(...)


class UserLoginRequest(BaseModel):
    email: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=8, max_length=50)


class UserReadResponse(BaseModel):
    id: str = Field(...)
    name: str = Field(..., min_length=1, max_length=50)
    created_at: datetime.datetime = Field(...)
    email: str = Field(..., min_length=1, max_length=50)
    is_available: bool = Field(...)
    activity: float = Field(...)
    latest_login: datetime.datetime = Field(...)
    introduction: str = Field(..., max_length=500)
    profile_image: str = Field(...)
    background_image: str = Field(...)


class UserUpdateRequest(BaseModel):
    id: str = Field(...)
    name: str = Field(None, min_length=1, max_length=50)
    password: str = Field(None, min_length=8, max_length=50)
    is_available: bool = Field(None)
    activity: float = Field(None)
    introduction: str = Field(None, max_length=500)
    profile_image: str = Field(None)
    background_image: str = Field(None)


class UserDeleteRequest(BaseModel):
    id: str = Field(...)


# 渡邊T追加分
class SimilarUserResponse(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    similarity: float = Field(...)


class UserUpdateLabelsRequest(BaseModel):
    id: str = Field(...)
    labels: Optional[List[str]] = None  # 更新後のラベルのリスト
