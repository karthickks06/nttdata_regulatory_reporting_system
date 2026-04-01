"""Code and data validator sub-agent"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import re
import ast


class ValidatorAgent:
    """
    Validator agent for code and data validation.

    Capabilities:
    - Validate code syntax
    - Validate data schemas
    - Validate business rules
    - Check compliance requirements
    - Detect anomalies
    """

    def __init__(self):
        self.name = "Validator"

    async def validate_code(
        self,
        code: str,
        language: str
    ) -> Dict[str, Any]:
        """
        Validate code syntax and basic quality.

        Args:
            code: Code to validate
            language: Programming language

        Returns:
            Validation result with errors and warnings
        """
        errors = []
        warnings = []

        try:
            if language == "python":
                result = self._validate_python(code)
                errors.extend(result.get('errors', []))
                warnings.extend(result.get('warnings', []))

            elif language == "sql":
                result = self._validate_sql(code)
                errors.extend(result.get('errors', []))
                warnings.extend(result.get('warnings', []))

            else:
                warnings.append({
                    "type": "UNSUPPORTED_LANGUAGE",
                    "message": f"Validation not fully supported for {language}"
                })

            return {
                "success": len(errors) == 0,
                "language": language,
                "errors": errors,
                "warnings": warnings,
                "error_count": len(errors),
                "warning_count": len(warnings),
                "validated_at": datetime.utcnow().isoformat()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "language": language
            }

    def _validate_python(self, code: str) -> Dict[str, Any]:
        """Validate Python code"""
        errors = []
        warnings = []

        # Syntax validation
        try:
            ast.parse(code)
        except SyntaxError as e:
            errors.append({
                "type": "SYNTAX_ERROR",
                "message": str(e.msg),
                "line": e.lineno,
                "offset": e.offset
            })
            return {"errors": errors, "warnings": warnings}

        # Check for common issues
        lines = code.split('\n')

        # Check line length
        for idx, line in enumerate(lines, 1):
            if len(line) > 120:
                warnings.append({
                    "type": "LINE_TOO_LONG",
                    "message": f"Line {idx} exceeds 120 characters",
                    "line": idx
                })

        # Check for bare except
        if re.search(r'except\s*:', code):
            warnings.append({
                "type": "BARE_EXCEPT",
                "message": "Bare except clause catches all exceptions"
            })

        # Check for missing docstrings
        if 'def ' in code or 'class ' in code:
            if '"""' not in code and "'''" not in code:
                warnings.append({
                    "type": "MISSING_DOCSTRING",
                    "message": "Functions/classes should have docstrings"
                })

        return {"errors": errors, "warnings": warnings}

    def _validate_sql(self, code: str) -> Dict[str, Any]:
        """Validate SQL code"""
        errors = []
        warnings = []

        sql_upper = code.upper()

        # Check for dangerous operations
        if 'DELETE' in sql_upper and 'WHERE' not in sql_upper:
            errors.append({
                "type": "UNSAFE_DELETE",
                "message": "DELETE without WHERE clause will delete all rows"
            })

        if 'UPDATE' in sql_upper and 'WHERE' not in sql_upper:
            errors.append({
                "type": "UNSAFE_UPDATE",
                "message": "UPDATE without WHERE clause will update all rows"
            })

        if 'DROP TABLE' in sql_upper:
            warnings.append({
                "type": "DROP_TABLE",
                "message": "DROP TABLE is a destructive operation"
            })

        # Check for SQL injection vulnerabilities (basic)
        if re.search(r'["\'].*\+.*["\']', code):
            warnings.append({
                "type": "SQL_INJECTION_RISK",
                "message": "Possible SQL injection vulnerability - use parameterized queries"
            })

        # Check balanced parentheses
        if code.count('(') != code.count(')'):
            errors.append({
                "type": "UNBALANCED_PARENTHESES",
                "message": "Unbalanced parentheses in SQL"
            })

        return {"errors": errors, "warnings": warnings}

    async def validate_data_schema(
        self,
        data: Dict[str, Any],
        schema: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate data against schema.

        Args:
            data: Data to validate
            schema: Schema definition

        Returns:
            Validation result
        """
        errors = []

        try:
            for field, rules in schema.items():
                value = data.get(field)

                # Required field check
                if rules.get('required', False) and value is None:
                    errors.append({
                        "field": field,
                        "type": "REQUIRED_FIELD",
                        "message": f"Field '{field}' is required"
                    })
                    continue

                if value is None:
                    continue

                # Type check
                expected_type = rules.get('type')
                if expected_type:
                    if not self._check_type(value, expected_type):
                        errors.append({
                            "field": field,
                            "type": "TYPE_MISMATCH",
                            "message": f"Field '{field}' expected {expected_type}, got {type(value).__name__}"
                        })

                # Min/Max checks for numbers
                if isinstance(value, (int, float)):
                    if 'min' in rules and value < rules['min']:
                        errors.append({
                            "field": field,
                            "type": "MIN_VALUE",
                            "message": f"Field '{field}' must be >= {rules['min']}"
                        })
                    if 'max' in rules and value > rules['max']:
                        errors.append({
                            "field": field,
                            "type": "MAX_VALUE",
                            "message": f"Field '{field}' must be <= {rules['max']}"
                        })

                # Length checks for strings
                if isinstance(value, str):
                    if 'min_length' in rules and len(value) < rules['min_length']:
                        errors.append({
                            "field": field,
                            "type": "MIN_LENGTH",
                            "message": f"Field '{field}' must be at least {rules['min_length']} characters"
                        })
                    if 'max_length' in rules and len(value) > rules['max_length']:
                        errors.append({
                            "field": field,
                            "type": "MAX_LENGTH",
                            "message": f"Field '{field}' must be at most {rules['max_length']} characters"
                        })

                # Pattern matching
                if 'pattern' in rules and isinstance(value, str):
                    if not re.match(rules['pattern'], value):
                        errors.append({
                            "field": field,
                            "type": "PATTERN_MISMATCH",
                            "message": f"Field '{field}' does not match required pattern"
                        })

            return {
                "success": len(errors) == 0,
                "errors": errors,
                "error_count": len(errors),
                "validated_at": datetime.utcnow().isoformat()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _check_type(self, value: Any, expected_type: str) -> bool:
        """Check if value matches expected type"""
        type_map = {
            'string': str,
            'str': str,
            'integer': int,
            'int': int,
            'float': float,
            'number': (int, float),
            'boolean': bool,
            'bool': bool,
            'list': list,
            'array': list,
            'dict': dict,
            'object': dict
        }

        expected = type_map.get(expected_type.lower())
        if expected:
            return isinstance(value, expected)

        return True

    async def validate_business_rules(
        self,
        data: Dict[str, Any],
        rules: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Validate business rules.

        Args:
            data: Data to validate
            rules: List of business rules

        Returns:
            Validation result
        """
        violations = []

        try:
            for rule in rules:
                rule_type = rule.get('type')
                rule_id = rule.get('id', 'unknown')

                if rule_type == 'comparison':
                    # Compare two fields
                    field1 = rule['field1']
                    field2 = rule['field2']
                    operator = rule['operator']

                    value1 = data.get(field1)
                    value2 = data.get(field2)

                    if not self._compare_values(value1, value2, operator):
                        violations.append({
                            "rule_id": rule_id,
                            "type": "BUSINESS_RULE_VIOLATION",
                            "message": rule.get('message', f"Rule {rule_id} violated")
                        })

                elif rule_type == 'range':
                    # Check if value is in range
                    field = rule['field']
                    min_val = rule.get('min')
                    max_val = rule.get('max')

                    value = data.get(field)

                    if value is not None:
                        if min_val is not None and value < min_val:
                            violations.append({
                                "rule_id": rule_id,
                                "type": "OUT_OF_RANGE",
                                "message": f"{field} below minimum value"
                            })
                        if max_val is not None and value > max_val:
                            violations.append({
                                "rule_id": rule_id,
                                "type": "OUT_OF_RANGE",
                                "message": f"{field} above maximum value"
                            })

                elif rule_type == 'required_if':
                    # Field required if condition is met
                    field = rule['field']
                    condition_field = rule['condition_field']
                    condition_value = rule['condition_value']

                    if data.get(condition_field) == condition_value:
                        if data.get(field) is None:
                            violations.append({
                                "rule_id": rule_id,
                                "type": "CONDITIONAL_REQUIRED",
                                "message": f"{field} is required when {condition_field} is {condition_value}"
                            })

            return {
                "success": len(violations) == 0,
                "violations": violations,
                "violation_count": len(violations),
                "validated_at": datetime.utcnow().isoformat()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _compare_values(self, value1: Any, value2: Any, operator: str) -> bool:
        """Compare two values with operator"""
        if operator == '==':
            return value1 == value2
        elif operator == '!=':
            return value1 != value2
        elif operator == '>':
            return value1 > value2
        elif operator == '>=':
            return value1 >= value2
        elif operator == '<':
            return value1 < value2
        elif operator == '<=':
            return value1 <= value2
        else:
            return True

    async def detect_anomalies(
        self,
        data_points: List[float],
        threshold: float = 2.0
    ) -> Dict[str, Any]:
        """
        Detect anomalies in numerical data.

        Args:
            data_points: List of numerical values
            threshold: Z-score threshold for anomaly detection

        Returns:
            Anomaly detection results
        """
        try:
            if len(data_points) < 2:
                return {
                    "success": False,
                    "error": "Need at least 2 data points for anomaly detection"
                }

            # Calculate mean and standard deviation
            mean = sum(data_points) / len(data_points)
            variance = sum((x - mean) ** 2 for x in data_points) / len(data_points)
            std_dev = variance ** 0.5

            # Detect anomalies using z-score
            anomalies = []
            for idx, value in enumerate(data_points):
                if std_dev > 0:
                    z_score = abs((value - mean) / std_dev)
                    if z_score > threshold:
                        anomalies.append({
                            "index": idx,
                            "value": value,
                            "z_score": z_score,
                            "deviation": abs(value - mean)
                        })

            return {
                "success": True,
                "anomalies": anomalies,
                "anomaly_count": len(anomalies),
                "statistics": {
                    "mean": mean,
                    "std_dev": std_dev,
                    "min": min(data_points),
                    "max": max(data_points)
                },
                "threshold": threshold
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
