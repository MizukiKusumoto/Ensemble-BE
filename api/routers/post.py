from fastapi import APIRouter

router = APIRouter()

@router.get("/posts")
async def get_posts() -> dict[str, str]:
  return {"message": "get posts"}