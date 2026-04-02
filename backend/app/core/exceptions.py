"""Custom exception classes for the application"""

from typing import Any, Dict, Optional
from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    """Exception raised when a resource is not found"""
    def __init__(self, detail: str = "Resource not found", headers: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            headers=headers
        )


class UnauthorizedException(HTTPException):
    """Exception raised when authentication fails"""
    def __init__(self, detail: str = "Unauthorized", headers: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers=headers or {"WWW-Authenticate": "Bearer"}
        )


class ForbiddenException(HTTPException):
    """Exception raised when user lacks required permissions"""
    def __init__(self, detail: str = "Forbidden - insufficient permissions", headers: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            headers=headers
        )


class BadRequestException(HTTPException):
    """Exception raised for invalid request data"""
    def __init__(self, detail: str = "Bad request", headers: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            headers=headers
        )


class ConflictException(HTTPException):
    """Exception raised when a resource conflict occurs"""
    def __init__(self, detail: str = "Resource conflict", headers: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            headers=headers
        )


class ValidationException(HTTPException):
    """Exception raised for validation errors"""
    def __init__(self, detail: str = "Validation error", errors: Optional[list] = None, headers: Optional[Dict[str, Any]] = None):
        if errors:
            detail_with_errors = {
                "message": detail,
                "errors": errors
            }
            super().__init__(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=detail_with_errors,
                headers=headers
            )
        else:
            super().__init__(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=detail,
                headers=headers
            )


class InternalServerException(HTTPException):
    """Exception raised for internal server errors"""
    def __init__(self, detail: str = "Internal server error", headers: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            headers=headers
        )


class ServiceUnavailableException(HTTPException):
    """Exception raised when a service is unavailable"""
    def __init__(self, detail: str = "Service unavailable", headers: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail,
            headers=headers
        )


class TooManyRequestsException(HTTPException):
    """Exception raised when rate limit is exceeded"""
    def __init__(self, detail: str = "Too many requests", retry_after: Optional[int] = None, headers: Optional[Dict[str, Any]] = None):
        custom_headers = headers or {}
        if retry_after:
            custom_headers["Retry-After"] = str(retry_after)
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail,
            headers=custom_headers
        )


class DatabaseException(Exception):
    """Exception raised for database-related errors"""
    def __init__(self, message: str, original_exception: Optional[Exception] = None):
        self.message = message
        self.original_exception = original_exception
        super().__init__(self.message)


class AgentExecutionException(Exception):
    """Exception raised when an agent execution fails"""
    def __init__(self, agent_name: str, message: str, original_exception: Optional[Exception] = None):
        self.agent_name = agent_name
        self.message = message
        self.original_exception = original_exception
        super().__init__(f"Agent {agent_name} failed: {message}")


class WorkflowException(Exception):
    """Exception raised when a workflow execution fails"""
    def __init__(self, workflow_id: str, message: str, original_exception: Optional[Exception] = None):
        self.workflow_id = workflow_id
        self.message = message
        self.original_exception = original_exception
        super().__init__(f"Workflow {workflow_id} failed: {message}")


class ValidationError(Exception):
    """Exception raised for data validation errors"""
    def __init__(self, message: str, field: Optional[str] = None, errors: Optional[Dict[str, Any]] = None):
        self.message = message
        self.field = field
        self.errors = errors or {}
        super().__init__(self.message)


class ConfigurationException(Exception):
    """Exception raised for configuration errors"""
    def __init__(self, message: str, config_key: Optional[str] = None):
        self.message = message
        self.config_key = config_key
        super().__init__(self.message)


class FileProcessingException(Exception):
    """Exception raised when file processing fails"""
    def __init__(self, filename: str, message: str, original_exception: Optional[Exception] = None):
        self.filename = filename
        self.message = message
        self.original_exception = original_exception
        super().__init__(f"File processing failed for {filename}: {message}")
