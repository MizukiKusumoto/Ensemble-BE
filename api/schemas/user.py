from pydantic import BaseModel, Field


class UserBase(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    email: str
    password: str = Field(min_length=8, max_length=50)


class UserCreateRequest(UserBase):
    pass


class UserCreateResponse(UserBase):
    id: int


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
