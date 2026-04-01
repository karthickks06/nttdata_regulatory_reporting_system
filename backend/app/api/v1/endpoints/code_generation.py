"""Code generation endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.postgres import get_db
from app.models.user import User
from app.schemas.code import CodeGenerationRequest, CodeValidationRequest, CodeValidationResponse
from app.services.code_generation_service import CodeGenerationService

router = APIRouter()


@router.post("/generate")
async def generate_code(
    request: CodeGenerationRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate code from template"""
    service = CodeGenerationService()

    result = await service.generate_code(
        db=db,
        language=request.language,
        template=request.template or "",
        context=request.context,
        save_to_db=True
    )

    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Code generation failed")
        )

    return result


@router.post("/generate-sql")
async def generate_sql(
    query_type: str,
    params: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate SQL query"""
    service = CodeGenerationService()

    result = await service.generate_sql_query(db, query_type, params)

    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "SQL generation failed")
        )

    return result


@router.post("/validate", response_model=CodeValidationResponse)
async def validate_code(
    request: CodeValidationRequest,
    current_user: User = Depends(get_current_user)
):
    """Validate generated code"""
    service = CodeGenerationService()

    result = await service.validate_generated_code(request.code, request.language)

    return CodeValidationResponse(
        valid=result.get("success", False),
        errors=result.get("errors", []),
        warnings=result.get("warnings", [])
    )
