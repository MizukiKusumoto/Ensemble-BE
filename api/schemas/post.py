from pydantic import BaseModel, Field
import datetime


class PostCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=8, max_length=50)


class UserCreateResponse(BaseModel):
    id: str = Field(...)


class UserReadRequest(BaseModel):
    email: str = Field(..., min_length=1, max_length=50)


class UserReadResponse(BaseModel):
    id: str = Field(...)
    name: str = Field(..., min_length=1, max_length=50)
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
