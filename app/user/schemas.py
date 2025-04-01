from fastapi_users import schemas


class UserCreate(schemas.BaseUserCreate):
    username: str


class UserRead(schemas.BaseUser[int]):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass
