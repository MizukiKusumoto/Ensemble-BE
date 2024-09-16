# 渡邊T追加分
from fastapi import APIRouter, HTTPException
from typing import List
from neomodel import db, DoesNotExist

from api.models.main import Recruitment
from api.schemas.recruitment import RecruitmentCreate, RecruitmentResponse

router = APIRouter(prefix="/recruitment", tags=["recruitment"])

@router.post("/", response_model=RecruitmentResponse)
async def create_recruitment(recruitment_data: RecruitmentCreate):
    """新規の人材募集作成"""
    recruitment = Recruitment(
        title=recruitment_data.title,
        description=recruitment_data.description,
        image_urls=recruitment_data.image_urls,
        deadline=recruitment_data.deadline,
        labels=recruitment_data.labels,  # 属性部分を追加
    ).save()
    return {
        "id": recruitment.element_id,
        "title": recruitment.title,
        "description": recruitment.description,
        "image_urls": recruitment.image_urls,
        "deadline": recruitment.deadline,
        "created_at": recruitment.created_at,
        "updated_at": recruitment.updated_at,
    }

# @router.get("/{recruitment_id}", response_model=RecruitmentResponse)
# async def get_recruitment_by_id(recruitment_id: str):
#     """IDで指定された人材募集投稿を取得する"""
#     try:
#         recruitment = Recruitment.nodes.get(element_id=recruitment_id)
#     except DoesNotExist:
#         raise HTTPException(status_code=404, detail="Recruitment not found")
#     return {
#         "id": recruitment.element_id,
#         "title": recruitment.title,
#         "description": recruitment.description,
#         "image_urls": recruitment.image_urls,
#         "deadline": recruitment.deadline,
#         "created_at": recruitment.created_at,
#         "updated_at": recruitment.updated_at,
#     }