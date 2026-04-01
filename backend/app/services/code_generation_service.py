"""Code generation orchestration service"""

from typing import Dict, Any, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.sub_agents.code_generator import CodeGeneratorAgent
from app.sub_agents.sql_generator import SQLGeneratorAgent
from app.models.generated_code import GeneratedCode


class CodeGenerationService:
    """Service for orchestrating code generation"""

    def __init__(self):
        self.code_generator = CodeGeneratorAgent()
        self.sql_generator = SQLGeneratorAgent()

    async def generate_code(
        db: AsyncSession,
        language: str,
        template: str,
        context: Dict[str, Any],
        save_to_db: bool = True
    ) -> Dict[str, Any]:
        """
        Generate code from template.

        Args:
            db: Database session
            language: Programming language
            template: Code template
            context: Template context
            save_to_db: Whether to save to database

        Returns:
            Generation result
        """
        try:
            generator = CodeGeneratorAgent()

            result = await generator.generate_code(
                language=language,
                template=template,
                context=context
            )

            if save_to_db and result.get("success"):
                generated_code = GeneratedCode(
                    code_type=language,
                    code_content=result["code"],
                    description=f"Generated {language} code",
                    status="generated"
                )
                db.add(generated_code)
                await db.commit()
                await db.refresh(generated_code)

                result["code_id"] = generated_code.id

            return result

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def generate_sql_query(
        self,
        db: AsyncSession,
        query_type: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate SQL query"""
        try:
            if query_type == "select":
                result = await self.sql_generator.generate_select_query(**params)
            elif query_type == "insert":
                result = await self.sql_generator.generate_insert_query(**params)
            elif query_type == "update":
                result = await self.sql_generator.generate_update_query(**params)
            elif query_type == "create_table":
                result = await self.sql_generator.generate_create_table(**params)
            else:
                return {
                    "success": False,
                    "error": f"Unknown query type: {query_type}"
                }

            if result.get("success"):
                generated_code = GeneratedCode(
                    code_type="sql",
                    code_content=result["query"],
                    description=f"Generated SQL {query_type}",
                    status="generated"
                )
                db.add(generated_code)
                await db.commit()
                result["code_id"] = generated_code.id

            return result

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def validate_generated_code(
        self,
        code: str,
        language: str
    ) -> Dict[str, Any]:
        """Validate generated code"""
        from app.sub_agents.validator import ValidatorAgent

        validator = ValidatorAgent()
        return await validator.validate_code(code, language)
