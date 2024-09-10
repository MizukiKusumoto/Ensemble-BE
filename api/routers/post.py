from fastapi import APIRouter

router = APIRouter()


@router.get("/post")
async def get_post_by_id(id: str) -> dict[str, str]:
    return {"message": "get posts"}


@router.post("/post")
async def post_post() -> dict[str, str]:
    return {"message": "post post"}
