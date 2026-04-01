from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user, get_db
from app.models.user import User

router = APIRouter()

@router.get("/")
async def list_users(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return {"users": []}
