"""Code generation schemas"""

from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.generated_code import CodeType, CodeStatus
from app.models.test_case import TestStatus, TestType


# Generated Code Schemas

class GeneratedCodeBase(BaseModel):
    """Base generated code schema"""
    code_type: CodeType = Field(..., description="Type of code (SQL, Python, etc.)")
    language: Optional[str] = Field(default=None, max_length=50, description="Programming language")
    code_content: str = Field(..., description="The generated code content")
    title: Optional[str] = Field(default=None, max_length=500, description="Code title")
    description: Optional[str] = Field(default=None, description="Code description")


class GeneratedCodeCreate(GeneratedCodeBase):
    """Schema for creating generated code"""
    requirement_id: UUID = Field(..., description="Related requirement ID")
    file_name: Optional[str] = Field(default=None, max_length=255, description="File name")
    dependencies: Optional[List[str]] = Field(default=[], description="Code dependencies")
    tags: Optional[List[str]] = Field(default=[], description="Tags")
    metadata: Optional[Dict[str, Any]] = Field(default={}, description="Additional metadata")
    generation_prompt: Optional[str] = Field(default=None, description="Prompt used to generate")

    class Config:
        json_schema_extra = {
            "example": {
                "requirement_id": "uuid-here",
                "code_type": "sql",
                "language": "postgresql",
                "title": "Transaction Reporting Query",
                "code_content": "SELECT * FROM transactions WHERE trade_date >= CURRENT_DATE - INTERVAL '1 day'",
                "description": "Query for daily transaction reporting",
                "file_name": "transaction_report.sql",
                "dependencies": ["transactions_table"],
                "tags": ["reporting", "mifid"]
            }
        }


class GeneratedCodeUpdate(BaseModel):
    """Schema for updating generated code"""
    code_content: Optional[str] = Field(default=None)
    title: Optional[str] = Field(default=None, max_length=500)
    description: Optional[str] = Field(default=None)
    status: Optional[CodeStatus] = Field(default=None)
    is_validated: Optional[bool] = Field(default=None)
    is_deployed: Optional[bool] = Field(default=None)
    validation_errors: Optional[List[str]] = Field(default=None)
    validation_warnings: Optional[List[str]] = Field(default=None)
    tags: Optional[List[str]] = Field(default=None)

    class Config:
        json_schema_extra = {
            "example": {
                "status": "validated",
                "is_validated": True,
                "validation_errors": [],
                "validation_warnings": ["Consider adding index on trade_date"]
            }
        }


class GeneratedCodeResponse(GeneratedCodeBase):
    """Schema for generated code response"""
    id: UUID = Field(..., description="Code ID")
    requirement_id: UUID = Field(..., description="Requirement ID")
    file_name: Optional[str] = Field(default=None, description="File name")
    file_path: Optional[str] = Field(default=None, description="File path")
    status: CodeStatus = Field(..., description="Code status")
    is_validated: bool = Field(..., description="Whether validated")
    is_deployed: bool = Field(..., description="Whether deployed")
    validation_errors: List[str] = Field(default=[], description="Validation errors")
    validation_warnings: List[str] = Field(default=[], description="Validation warnings")
    version: int = Field(..., description="Version number")
    complexity_score: Optional[str] = Field(default=None, description="Complexity score")
    estimated_execution_time: Optional[str] = Field(default=None, description="Estimated execution time")
    dependencies: List[str] = Field(default=[], description="Dependencies")
    tags: List[str] = Field(default=[], description="Tags")
    metadata: Dict[str, Any] = Field(default={}, description="Metadata")
    created_by: Optional[UUID] = Field(default=None, description="Creator user ID")
    validated_by: Optional[UUID] = Field(default=None, description="Validator user ID")
    deployed_by: Optional[UUID] = Field(default=None, description="Deployer user ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Update timestamp")
    validated_at: Optional[datetime] = Field(default=None, description="Validation timestamp")
    deployed_at: Optional[datetime] = Field(default=None, description="Deployment timestamp")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "uuid-here",
                "requirement_id": "uuid-here",
                "code_type": "sql",
                "language": "postgresql",
                "title": "Transaction Reporting Query",
                "code_content": "SELECT * FROM transactions...",
                "status": "validated",
                "is_validated": True,
                "is_deployed": False,
                "version": 1,
                "tags": ["reporting"],
                "created_at": "2024-01-15T10:00:00Z",
                "updated_at": "2024-01-15T11:00:00Z"
            }
        }


# Test Case Schemas

class TestCaseBase(BaseModel):
    """Base test case schema"""
    test_name: str = Field(..., max_length=255, description="Test name")
    test_description: Optional[str] = Field(default=None, description="Test description")
    test_type: TestType = Field(default=TestType.UNIT, description="Test type")


class TestCaseCreate(TestCaseBase):
    """Schema for creating a test case"""
    generated_code_id: UUID = Field(..., description="Related code ID")
    test_input: Optional[Dict[str, Any]] = Field(default=None, description="Test input data")
    expected_output: Optional[Dict[str, Any]] = Field(default=None, description="Expected output")
    test_data_setup: Optional[str] = Field(default=None, description="Setup SQL/code")
    test_data_teardown: Optional[str] = Field(default=None, description="Teardown SQL/code")
    assertions: Optional[List[Dict[str, Any]]] = Field(default=[], description="Test assertions")
    timeout_seconds: Optional[str] = Field(default="30", description="Timeout")

    class Config:
        json_schema_extra = {
            "example": {
                "generated_code_id": "uuid-here",
                "test_name": "Test daily transaction query",
                "test_description": "Verify query returns correct transactions",
                "test_type": "functional",
                "test_input": {"date": "2024-01-15"},
                "expected_output": {"row_count": 100},
                "assertions": [{"field": "row_count", "operator": ">=", "value": 1}]
            }
        }


class TestCaseResponse(TestCaseBase):
    """Schema for test case response"""
    id: UUID = Field(..., description="Test case ID")
    generated_code_id: UUID = Field(..., description="Related code ID")
    test_input: Optional[Dict[str, Any]] = Field(default=None, description="Test input")
    expected_output: Optional[Dict[str, Any]] = Field(default=None, description="Expected output")
    actual_output: Optional[Dict[str, Any]] = Field(default=None, description="Actual output")
    status: TestStatus = Field(..., description="Test status")
    error_message: Optional[str] = Field(default=None, description="Error message")
    execution_time_ms: Optional[str] = Field(default=None, description="Execution time")
    assertions: List[Dict[str, Any]] = Field(default=[], description="Assertions")
    coverage_percentage: Optional[str] = Field(default=None, description="Code coverage")
    created_by: Optional[UUID] = Field(default=None, description="Creator user ID")
    executed_by: Optional[UUID] = Field(default=None, description="Executor user ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Update timestamp")
    executed_at: Optional[datetime] = Field(default=None, description="Execution timestamp")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "uuid-here",
                "generated_code_id": "uuid-here",
                "test_name": "Test daily transaction query",
                "test_type": "functional",
                "status": "passed",
                "execution_time_ms": "150",
                "coverage_percentage": "85",
                "created_at": "2024-01-15T10:00:00Z",
                "executed_at": "2024-01-15T10:05:00Z"
            }
        }


# Code Generation Request/Response

class CodeGenerationRequest(BaseModel):
    """Schema for code generation request"""
    requirement_id: UUID = Field(..., description="Requirement ID to generate code for")
    code_type: CodeType = Field(..., description="Type of code to generate")
    language: str = Field(..., description="Programming language")
    template: Optional[str] = Field(default=None, description="Template to use")
    context: Dict[str, Any] = Field(..., description="Context for generation")
    options: Optional[Dict[str, Any]] = Field(default=None, description="Additional options")

    class Config:
        json_schema_extra = {
            "example": {
                "requirement_id": "uuid-here",
                "code_type": "sql",
                "language": "postgresql",
                "context": {
                    "source_table": "transactions",
                    "target_fields": ["trade_date", "amount"],
                    "filters": {"status": "completed"}
                },
                "options": {"optimize": True}
            }
        }


class CodeValidationRequest(BaseModel):
    """Schema for code validation request"""
    code_id: UUID = Field(..., description="Code ID to validate")
    validation_rules: Optional[List[str]] = Field(default=None, description="Specific rules to apply")

    class Config:
        json_schema_extra = {
            "example": {
                "code_id": "uuid-here",
                "validation_rules": ["syntax", "security", "performance"]
            }
        }


class CodeValidationResponse(BaseModel):
    """Schema for code validation response"""
    code_id: UUID = Field(..., description="Code ID")
    valid: bool = Field(..., description="Whether code is valid")
    errors: List[str] = Field(default=[], description="Validation errors")
    warnings: List[str] = Field(default=[], description="Validation warnings")
    suggestions: List[str] = Field(default=[], description="Improvement suggestions")
    validated_at: datetime = Field(..., description="Validation timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "code_id": "uuid-here",
                "valid": True,
                "errors": [],
                "warnings": ["Consider adding index"],
                "suggestions": ["Use prepared statements"],
                "validated_at": "2024-01-15T10:00:00Z"
            }
        }
