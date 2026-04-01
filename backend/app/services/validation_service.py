"""Validation service for data and code validation"""

from typing import Dict, Any, List
from app.sub_agents.validator import ValidatorAgent


class ValidationService:
    """Service for validation operations"""

    def __init__(self):
        self.validator = ValidatorAgent()

    async def validate_code(
        self,
        code: str,
        language: str
    ) -> Dict[str, Any]:
        """Validate code syntax and quality"""
        return await self.validator.validate_code(code, language)

    async def validate_data_schema(
        self,
        data: Dict[str, Any],
        schema: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate data against schema"""
        return await self.validator.validate_data_schema(data, schema)

    async def validate_business_rules(
        self,
        data: Dict[str, Any],
        rules: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Validate business rules"""
        return await self.validator.validate_business_rules(data, rules)

    async def detect_anomalies(
        self,
        data_points: List[float],
        threshold: float = 2.0
    ) -> Dict[str, Any]:
        """Detect anomalies in data"""
        return await self.validator.detect_anomalies(data_points, threshold)

    async def validate_regulatory_compliance(
        self,
        data: Dict[str, Any],
        requirements: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Validate regulatory compliance.

        Args:
            data: Data to validate
            requirements: Regulatory requirements

        Returns:
            Compliance validation result
        """
        violations = []

        for req in requirements:
            req_id = req.get('id')
            req_type = req.get('type')
            is_mandatory = req.get('is_mandatory', True)

            # Check if requirement is met
            is_met = self._check_requirement(data, req)

            if not is_met and is_mandatory:
                violations.append({
                    "requirement_id": req_id,
                    "requirement_type": req_type,
                    "severity": "high" if is_mandatory else "medium",
                    "message": req.get('message', f"Requirement {req_id} not met")
                })

        return {
            "success": len(violations) == 0,
            "compliant": len(violations) == 0,
            "violations": violations,
            "violation_count": len(violations)
        }

    def _check_requirement(
        self,
        data: Dict[str, Any],
        requirement: Dict[str, Any]
    ) -> bool:
        """Check if a single requirement is met"""
        # Simple implementation - can be enhanced
        field = requirement.get('field')
        condition = requirement.get('condition')

        if not field or not condition:
            return True

        value = data.get(field)

        if condition == 'exists':
            return value is not None

        if condition == 'not_empty':
            return value is not None and value != ""

        return True
