"""Agent execution endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.postgres import get_db
from app.models.user import User
from app.schemas.agent import AgentTaskRequest, SubAgentRequest
from app.sub_agents.document_parser import DocumentParserAgent
from app.sub_agents.sql_generator import SQLGeneratorAgent
from app.sub_agents.code_generator import CodeGeneratorAgent
from app.sub_agents.test_generator import TestGeneratorAgent
from app.sub_agents.validator import ValidatorAgent

router = APIRouter()


@router.post("/execute")
async def execute_agent_task(
    request: AgentTaskRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Execute agent task"""
    # This would route to appropriate hierarchical agent
    # For now, return placeholder
    return {
        "success": True,
        "agent_name": request.agent_name,
        "task_type": request.task_type,
        "message": "Agent task queued for execution"
    }


@router.post("/sub-agent/document-parser")
async def execute_document_parser(
    request: SubAgentRequest,
    current_user: User = Depends(get_current_user)
):
    """Execute document parser sub-agent"""
    try:
        agent = DocumentParserAgent()

        if request.operation == "parse":
            file_path = request.parameters.get("file_path")
            result = await agent.parse_document(file_path)
        elif request.operation == "extract_requirements":
            parsed_content = request.parameters.get("parsed_content")
            result = await agent.extract_requirements(parsed_content)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown operation: {request.operation}"
            )

        return {
            "success": True,
            "sub_agent_type": "document_parser",
            "operation": request.operation,
            "result": result
        }

    except Exception as e:
        return {
            "success": False,
            "sub_agent_type": "document_parser",
            "operation": request.operation,
            "error": str(e)
        }


@router.post("/sub-agent/sql-generator")
async def execute_sql_generator(
    request: SubAgentRequest,
    current_user: User = Depends(get_current_user)
):
    """Execute SQL generator sub-agent"""
    try:
        agent = SQLGeneratorAgent()

        if request.operation == "generate_select":
            result = await agent.generate_select_query(**request.parameters)
        elif request.operation == "generate_insert":
            result = await agent.generate_insert_query(**request.parameters)
        elif request.operation == "generate_update":
            result = await agent.generate_update_query(**request.parameters)
        elif request.operation == "generate_create_table":
            result = await agent.generate_create_table(**request.parameters)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown operation: {request.operation}"
            )

        return {
            "success": True,
            "sub_agent_type": "sql_generator",
            "operation": request.operation,
            "result": result
        }

    except Exception as e:
        return {
            "success": False,
            "sub_agent_type": "sql_generator",
            "operation": request.operation,
            "error": str(e)
        }


@router.post("/sub-agent/code-generator")
async def execute_code_generator(
    request: SubAgentRequest,
    current_user: User = Depends(get_current_user)
):
    """Execute code generator sub-agent"""
    try:
        agent = CodeGeneratorAgent()

        if request.operation == "generate_code":
            result = await agent.generate_code(**request.parameters)
        elif request.operation == "generate_function":
            result = await agent.generate_function(**request.parameters)
        elif request.operation == "generate_class":
            result = await agent.generate_class(**request.parameters)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown operation: {request.operation}"
            )

        return {
            "success": True,
            "sub_agent_type": "code_generator",
            "operation": request.operation,
            "result": result
        }

    except Exception as e:
        return {
            "success": False,
            "sub_agent_type": "code_generator",
            "operation": request.operation,
            "error": str(e)
        }


@router.post("/sub-agent/test-generator")
async def execute_test_generator(
    request: SubAgentRequest,
    current_user: User = Depends(get_current_user)
):
    """Execute test generator sub-agent"""
    try:
        agent = TestGeneratorAgent()

        if request.operation == "generate_unit_test":
            result = await agent.generate_unit_test(**request.parameters)
        elif request.operation == "generate_integration_test":
            result = await agent.generate_integration_test(**request.parameters)
        elif request.operation == "generate_test_fixtures":
            result = await agent.generate_test_fixtures(**request.parameters)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown operation: {request.operation}"
            )

        return {
            "success": True,
            "sub_agent_type": "test_generator",
            "operation": request.operation,
            "result": result
        }

    except Exception as e:
        return {
            "success": False,
            "sub_agent_type": "test_generator",
            "operation": request.operation,
            "error": str(e)
        }


@router.post("/sub-agent/validator")
async def execute_validator(
    request: SubAgentRequest,
    current_user: User = Depends(get_current_user)
):
    """Execute validator sub-agent"""
    try:
        agent = ValidatorAgent()

        if request.operation == "validate_code":
            result = await agent.validate_code(**request.parameters)
        elif request.operation == "validate_data_schema":
            result = await agent.validate_data_schema(**request.parameters)
        elif request.operation == "validate_business_rules":
            result = await agent.validate_business_rules(**request.parameters)
        elif request.operation == "detect_anomalies":
            result = await agent.detect_anomalies(**request.parameters)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown operation: {request.operation}"
            )

        return {
            "success": True,
            "sub_agent_type": "validator",
            "operation": request.operation,
            "result": result
        }

    except Exception as e:
        return {
            "success": False,
            "sub_agent_type": "validator",
            "operation": request.operation,
            "error": str(e)
        }
