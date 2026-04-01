"""Generic code generator sub-agent for generating code in multiple languages"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import re


class CodeGeneratorAgent:
    """
    Generic code generator for multiple programming languages.

    Capabilities:
    - Generate code templates
    - Apply code transformations
    - Validate syntax
    - Format and beautify code
    - Generate documentation
    """

    def __init__(self):
        self.name = "CodeGenerator"
        self.supported_languages = ["python", "sql", "javascript", "java", "scala"]

    async def generate_code(
        self,
        language: str,
        template: str,
        context: Dict[str, Any],
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate code from template and context.

        Args:
            language: Programming language
            template: Code template with placeholders
            context: Context variables for template
            options: Generation options

        Returns:
            Generated code with metadata
        """
        try:
            if language.lower() not in self.supported_languages:
                return {
                    "success": False,
                    "error": f"Unsupported language: {language}"
                }

            # Replace placeholders in template
            code = self._apply_template(template, context)

            # Format code
            if options and options.get("format", True):
                code = await self._format_code(code, language)

            # Validate syntax
            if options and options.get("validate", True):
                validation = await self._validate_syntax(code, language)
                if not validation["valid"]:
                    return {
                        "success": False,
                        "error": "Syntax validation failed",
                        "validation": validation
                    }

            return {
                "success": True,
                "language": language,
                "code": code,
                "lines_of_code": len(code.split('\n')),
                "generated_at": datetime.utcnow().isoformat()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "language": language
            }

    def _apply_template(
        self,
        template: str,
        context: Dict[str, Any]
    ) -> str:
        """Apply context variables to template"""
        code = template

        # Replace {{variable}} placeholders
        for key, value in context.items():
            placeholder = f"{{{{{key}}}}}"
            code = code.replace(placeholder, str(value))

        return code

    async def _format_code(
        self,
        code: str,
        language: str
    ) -> str:
        """Format code based on language conventions"""
        if language == "python":
            # Basic Python formatting
            try:
                import black
                code = black.format_str(code, mode=black.Mode())
            except:
                # Fallback to basic formatting
                pass

        elif language == "sql":
            # Basic SQL formatting
            code = self._format_sql(code)

        return code

    def _format_sql(self, sql: str) -> str:
        """Basic SQL formatting"""
        # Uppercase SQL keywords
        keywords = [
            'SELECT', 'FROM', 'WHERE', 'JOIN', 'LEFT', 'RIGHT', 'INNER',
            'ON', 'AND', 'OR', 'GROUP BY', 'ORDER BY', 'HAVING',
            'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'ALTER', 'DROP'
        ]

        formatted = sql
        for keyword in keywords:
            # Replace lowercase with uppercase
            pattern = re.compile(r'\b' + keyword.lower() + r'\b', re.IGNORECASE)
            formatted = pattern.sub(keyword, formatted)

        return formatted

    async def _validate_syntax(
        self,
        code: str,
        language: str
    ) -> Dict[str, Any]:
        """Validate code syntax"""
        if language == "python":
            import ast
            try:
                ast.parse(code)
                return {"valid": True}
            except SyntaxError as e:
                return {
                    "valid": False,
                    "error": str(e),
                    "line": e.lineno
                }

        elif language == "sql":
            # Basic SQL validation
            return self._validate_sql_basic(code)

        else:
            # For other languages, return True (assume valid)
            return {"valid": True}

    def _validate_sql_basic(self, sql: str) -> Dict[str, Any]:
        """Basic SQL syntax validation"""
        # Check for balanced parentheses
        if sql.count('(') != sql.count(')'):
            return {
                "valid": False,
                "error": "Unbalanced parentheses"
            }

        # Check for required keywords
        sql_upper = sql.upper()
        if not any(kw in sql_upper for kw in ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE']):
            return {
                "valid": False,
                "error": "Missing SQL statement keyword"
            }

        return {"valid": True}

    async def generate_function(
        self,
        language: str,
        function_name: str,
        parameters: List[Dict[str, str]],
        return_type: Optional[str] = None,
        body: Optional[str] = None,
        docstring: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a function/method in specified language.

        Args:
            language: Programming language
            function_name: Function name
            parameters: List of parameters with name and type
            return_type: Return type (optional)
            body: Function body (optional)
            docstring: Documentation string (optional)

        Returns:
            Generated function code
        """
        try:
            if language == "python":
                code = self._generate_python_function(
                    function_name, parameters, return_type, body, docstring
                )
            elif language == "java":
                code = self._generate_java_method(
                    function_name, parameters, return_type, body, docstring
                )
            elif language == "javascript":
                code = self._generate_javascript_function(
                    function_name, parameters, body, docstring
                )
            else:
                return {
                    "success": False,
                    "error": f"Function generation not supported for {language}"
                }

            return {
                "success": True,
                "language": language,
                "function_name": function_name,
                "code": code
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _generate_python_function(
        self,
        name: str,
        parameters: List[Dict[str, str]],
        return_type: Optional[str],
        body: Optional[str],
        docstring: Optional[str]
    ) -> str:
        """Generate Python function"""
        # Build parameter list
        params = []
        for param in parameters:
            param_str = param['name']
            if 'type' in param:
                param_str += f": {param['type']}"
            if 'default' in param:
                param_str += f" = {param['default']}"
            params.append(param_str)

        param_str = ", ".join(params)

        # Build function signature
        signature = f"def {name}({param_str})"
        if return_type:
            signature += f" -> {return_type}"
        signature += ":"

        # Build function body
        lines = [signature]

        if docstring:
            lines.append(f'    """{docstring}"""')

        if body:
            for line in body.split('\n'):
                lines.append(f"    {line}")
        else:
            lines.append("    pass")

        return "\n".join(lines)

    def _generate_java_method(
        self,
        name: str,
        parameters: List[Dict[str, str]],
        return_type: Optional[str],
        body: Optional[str],
        docstring: Optional[str]
    ) -> str:
        """Generate Java method"""
        # Build parameter list
        params = []
        for param in parameters:
            param_type = param.get('type', 'Object')
            param_str = f"{param_type} {param['name']}"
            params.append(param_str)

        param_str = ", ".join(params)
        ret_type = return_type or "void"

        lines = []

        if docstring:
            lines.append("/**")
            lines.append(f" * {docstring}")
            lines.append(" */")

        lines.append(f"public {ret_type} {name}({param_str}) {{")

        if body:
            for line in body.split('\n'):
                lines.append(f"    {line}")
        else:
            if ret_type != "void":
                lines.append(f"    return null;")

        lines.append("}")

        return "\n".join(lines)

    def _generate_javascript_function(
        self,
        name: str,
        parameters: List[Dict[str, str]],
        body: Optional[str],
        docstring: Optional[str]
    ) -> str:
        """Generate JavaScript function"""
        params = [param['name'] for param in parameters]
        param_str = ", ".join(params)

        lines = []

        if docstring:
            lines.append("/**")
            lines.append(f" * {docstring}")
            lines.append(" */")

        lines.append(f"function {name}({param_str}) {{")

        if body:
            for line in body.split('\n'):
                lines.append(f"    {line}")
        else:
            lines.append("    // TODO: Implement")

        lines.append("}")

        return "\n".join(lines)

    async def generate_class(
        self,
        language: str,
        class_name: str,
        properties: List[Dict[str, str]],
        methods: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate a class definition.

        Args:
            language: Programming language
            class_name: Class name
            properties: Class properties/fields
            methods: Class methods

        Returns:
            Generated class code
        """
        try:
            if language == "python":
                code = self._generate_python_class(class_name, properties, methods)
            elif language == "java":
                code = self._generate_java_class(class_name, properties, methods)
            else:
                return {
                    "success": False,
                    "error": f"Class generation not supported for {language}"
                }

            return {
                "success": True,
                "language": language,
                "class_name": class_name,
                "code": code
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _generate_python_class(
        self,
        name: str,
        properties: List[Dict[str, str]],
        methods: List[Dict[str, Any]]
    ) -> str:
        """Generate Python class"""
        lines = [f"class {name}:"]
        lines.append(f'    """Generated class: {name}"""')
        lines.append("")

        # Constructor
        if properties:
            params = ["self"]
            for prop in properties:
                params.append(f"{prop['name']}: {prop.get('type', 'Any')}")

            lines.append(f"    def __init__({', '.join(params)}):")
            for prop in properties:
                lines.append(f"        self.{prop['name']} = {prop['name']}")
            lines.append("")

        # Methods
        for method in methods:
            method_code = self._generate_python_function(
                method['name'],
                method.get('parameters', []),
                method.get('return_type'),
                method.get('body'),
                method.get('docstring')
            )
            # Indent for class
            for line in method_code.split('\n'):
                lines.append(f"    {line}")
            lines.append("")

        return "\n".join(lines)

    def _generate_java_class(
        self,
        name: str,
        properties: List[Dict[str, str]],
        methods: List[Dict[str, Any]]
    ) -> str:
        """Generate Java class"""
        lines = [f"public class {name} {{"]

        # Properties
        for prop in properties:
            prop_type = prop.get('type', 'Object')
            lines.append(f"    private {prop_type} {prop['name']};")

        if properties:
            lines.append("")

        # Getters and setters
        for prop in properties:
            prop_type = prop.get('type', 'Object')
            prop_name = prop['name']
            cap_name = prop_name[0].upper() + prop_name[1:]

            lines.append(f"    public {prop_type} get{cap_name}() {{")
            lines.append(f"        return {prop_name};")
            lines.append("    }")
            lines.append("")

            lines.append(f"    public void set{cap_name}({prop_type} {prop_name}) {{")
            lines.append(f"        this.{prop_name} = {prop_name};")
            lines.append("    }")
            lines.append("")

        # Methods
        for method in methods:
            method_code = self._generate_java_method(
                method['name'],
                method.get('parameters', []),
                method.get('return_type'),
                method.get('body'),
                method.get('docstring')
            )
            for line in method_code.split('\n'):
                lines.append(f"    {line}")
            lines.append("")

        lines.append("}")

        return "\n".join(lines)
