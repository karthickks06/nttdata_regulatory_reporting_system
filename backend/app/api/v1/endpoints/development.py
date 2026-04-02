"""
Development API Endpoints - Code generation, testing, and pipeline management
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.generated_code import GeneratedCode
from app.models.test_case import TestCase
from app.schemas.code import (
    GeneratedCodeCreate,
    GeneratedCodeUpdate,
    GeneratedCodeResponse,
    TestCaseCreate,
    TestCaseResponse
)
from app.services.code_generation_service import CodeGenerationService
from app.core.rbac import require_permission

router = APIRouter()


@router.post("/code/generate", response_model=GeneratedCodeResponse)
async def generate_code(
    code_data: GeneratedCodeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate code from requirements"""
    # Check permission
    await require_permission(db, current_user.id, "code", "create")

    generated_code = await CodeGenerationService.generate_code(
        db=db,
        requirement_id=code_data.requirement_id,
        code_type=code_data.code_type,
        language=code_data.language,
        user_id=current_user.id
    )

    return generated_code


@router.get("/code/{code_id}", response_model=GeneratedCodeResponse)
async def get_code(
    code_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get generated code by ID"""
    await require_permission(db, current_user.id, "code", "read")

    code = await CodeGenerationService.get_code(db, code_id)
    if not code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Code not found"
        )

    return code


@router.get("/code/requirement/{requirement_id}", response_model=List[GeneratedCodeResponse])
async def get_code_by_requirement(
    requirement_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all generated code for a requirement"""
    await require_permission(db, current_user.id, "code", "read")

    codes = await CodeGenerationService.get_code_by_requirement(db, requirement_id)
    return codes


@router.put("/code/{code_id}", response_model=GeneratedCodeResponse)
async def update_code(
    code_id: UUID,
    code_data: GeneratedCodeUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update generated code"""
    await require_permission(db, current_user.id, "code", "update")

    code = await CodeGenerationService.update_code(
        db=db,
        code_id=code_id,
        code_data=code_data.dict(exclude_unset=True)
    )

    if not code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Code not found"
        )

    return code


@router.post("/code/{code_id}/validate", response_model=GeneratedCodeResponse)
async def validate_code(
    code_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Validate generated code"""
    await require_permission(db, current_user.id, "code", "validate")

    code = await CodeGenerationService.validate_code(db, code_id)
    if not code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Code not found"
        )

    return code


@router.delete("/code/{code_id}")
async def delete_code(
    code_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete generated code"""
    await require_permission(db, current_user.id, "code", "delete")

    success = await CodeGenerationService.delete_code(db, code_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Code not found"
        )

    return {"message": "Code deleted successfully"}


@router.post("/tests/generate", response_model=List[TestCaseResponse])
async def generate_tests(
    code_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate test cases for code"""
    await require_permission(db, current_user.id, "tests", "create")

    tests = await CodeGenerationService.generate_tests(
        db=db,
        code_id=code_id,
        user_id=current_user.id
    )

    return tests


@router.post("/tests/{test_id}/execute", response_model=TestCaseResponse)
async def execute_test(
    test_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Execute a test case"""
    await require_permission(db, current_user.id, "tests", "execute")

    test = await CodeGenerationService.execute_test(db, test_id)
    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test case not found"
        )

    return test


@router.get("/tests/code/{code_id}", response_model=List[TestCaseResponse])
async def get_tests_for_code(
    code_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all test cases for generated code"""
    await require_permission(db, current_user.id, "tests", "read")

    tests = await CodeGenerationService.get_tests_for_code(db, code_id)
    return tests


@router.get("/lineage/{entity_type}/{entity_id}")
async def get_data_lineage(
    entity_type: str,
    entity_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get data lineage for an entity"""
    await require_permission(db, current_user.id, "lineage", "read")

    # Import lineage tool
    from app.tools.data_lineage import DataLineageTool

    lineage_tool = DataLineageTool()
    lineage = await lineage_tool.get_lineage(
        db=db,
        entity_type=entity_type,
        entity_id=str(entity_id)
    )

    return lineage


@router.get("/schema/{source_system}")
async def get_schema(
    source_system: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get database schema for a source system"""
    await require_permission(db, current_user.id, "schema", "read")

    # This would integrate with actual schema discovery
    # For now, return a placeholder
    return {
        "source_system": source_system,
        "tables": [],
        "relationships": []
    }


@router.get("/pipeline/status/{pipeline_id}")
async def get_pipeline_status(
    pipeline_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get data pipeline status"""
    await require_permission(db, current_user.id, "pipeline", "read")

    # Placeholder for pipeline monitoring
    return {
        "pipeline_id": str(pipeline_id),
        "status": "running",
        "progress": 75,
        "last_run": "2026-04-01T12:00:00Z"
    }
