"""Code generation schemas"""

from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel


class CodeBase(BaseModel):
    """Base code schema"""
    code_type: str
    code_content: str
    description: Optional[str] = None


class CodeCreate(CodeBase):
    """Schema for creating generated code"""
    requirement_id: Optional[int] = None
    status: str = "generated"


class CodeUpdate(BaseModel):
    """Schema for updating generated code"""
    code_content: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class CodeResponse(CodeBase):
    """Schema for code response"""
    id: int
    requirement_id: Optional[int]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CodeGenerationRequest(BaseModel):
    """Schema for code generation request"""
    language: str
    template: Optional[str] = None
    context: Dict[str, Any]
    options: Optional[Dict[str, Any]] = None


class CodeValidationRequest(BaseModel):
    """Schema for code validation request"""
    code: str
    language: str


class CodeValidationResponse(BaseModel):
    """Schema for code validation response"""
    valid: bool
    errors: list = []
    warnings: list = []
