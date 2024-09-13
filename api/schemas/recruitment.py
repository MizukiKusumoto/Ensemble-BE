# 渡邊T追加分
from pydantic import BaseModel, Field
from typing import List, Optional
import datetime

class RecruitmentCreate(BaseModel):
    title: str = Field(..., max_length=50)
    description: str = Field(..., max_length=500)
    image_urls: Optional[List[str]] = None  # Optional
    deadline: datetime.datetime 
    
# class RecruitmentResponse(RecruitmentCreate):
#     id: str
#     created_at: datetime.datetime
#     updated_at: datetime.datetime 