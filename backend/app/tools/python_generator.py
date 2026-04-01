"""Python code generation utility functions"""

from typing import Dict, Any, List, Optional


def generate_function(
    name: str,
    parameters: List[Dict[str, str]],
    return_type: Optional[str] = None,
    body: Optional[str] = None,
    docstring: Optional[str] = None,
    is_async: bool = False
) -> str:
    """
    Generate Python function.

    Args:
        name: Function name
        parameters: List of parameters with name, type, default
        return_type: Return type annotation
        body: Function body
        docstring: Documentation string
        is_async: Whether function is async

    Returns:
        Generated function code
    """
    lines = []

    # Build parameter list
    params = []
    for param in parameters:
        param_str = param['name']

        if 'type' in param:
            param_str += f": {param['type']}"

        if 'default' in param:
            default = param['default']
            if isinstance(default, str) and not default.startswith(("'", '"')):
                param_str += f" = '{default}'"
            else:
                param_str += f" = {default}"

        params.append(param_str)

    param_str = ", ".join(params)

    # Build function signature
    if is_async:
        signature = f"async def {name}({param_str})"
    else:
        signature = f"def {name}({param_str})"

    if return_type:
        signature += f" -> {return_type}"

    signature += ":"

    lines.append(signature)

    # Add docstring
    if docstring:
        lines.append(f'    """{docstring}"""')

    # Add body
    if body:
        for line in body.split('\n'):
            lines.append(f"    {line}")
    else:
        lines.append("    pass")

    return "\n".join(lines)


def generate_class(
    name: str,
    base_classes: Optional[List[str]] = None,
    properties: Optional[List[Dict[str, str]]] = None,
    methods: Optional[List[Dict[str, Any]]] = None,
    docstring: Optional[str] = None
) -> str:
    """
    Generate Python class.

    Args:
        name: Class name
        base_classes: List of base class names
        properties: List of class properties
        methods: List of method definitions
        docstring: Class documentation

    Returns:
        Generated class code
    """
    lines = []

    # Class definition
    if base_classes:
        class_def = f"class {name}({', '.join(base_classes)}):"
    else:
        class_def = f"class {name}:"

    lines.append(class_def)

    # Docstring
    if docstring:
        lines.append(f'    """{docstring}"""')
    else:
        lines.append(f'    """Generated class: {name}"""')

    lines.append("")

    # Constructor
    if properties:
        params = ["self"]
        for prop in properties:
            param = prop['name']
            if 'type' in prop:
                param += f": {prop['type']}"
            if 'default' in prop:
                param += f" = {prop['default']}"
            params.append(param)

        lines.append(f"    def __init__({', '.join(params)}):")
        lines.append('        """Initialize instance"""')

        for prop in properties:
            lines.append(f"        self.{prop['name']} = {prop['name']}")

        lines.append("")

    # Methods
    if methods:
        for method in methods:
            method_code = generate_function(
                name=method['name'],
                parameters=method.get('parameters', []),
                return_type=method.get('return_type'),
                body=method.get('body'),
                docstring=method.get('docstring'),
                is_async=method.get('is_async', False)
            )

            # Indent for class
            for line in method_code.split('\n'):
                lines.append(f"    {line}")

            lines.append("")

    return "\n".join(lines)


def generate_dataclass(
    name: str,
    fields: List[Dict[str, str]],
    docstring: Optional[str] = None
) -> str:
    """
    Generate Python dataclass.

    Args:
        name: Dataclass name
        fields: List of field definitions
        docstring: Class documentation

    Returns:
        Generated dataclass code
    """
    lines = [
        "from dataclasses import dataclass",
        "",
        "",
        "@dataclass",
        f"class {name}:"
    ]

    if docstring:
        lines.append(f'    """{docstring}"""')

    for field in fields:
        field_name = field['name']
        field_type = field['type']
        field_def = f"    {field_name}: {field_type}"

        if 'default' in field:
            field_def += f" = {field['default']}"

        lines.append(field_def)

    return "\n".join(lines)


def generate_pydantic_model(
    name: str,
    fields: List[Dict[str, Any]],
    docstring: Optional[str] = None
) -> str:
    """
    Generate Pydantic model.

    Args:
        name: Model name
        fields: List of field definitions
        docstring: Model documentation

    Returns:
        Generated Pydantic model code
    """
    lines = [
        "from pydantic import BaseModel, Field",
        "from typing import Optional",
        "",
        "",
        f"class {name}(BaseModel):"
    ]

    if docstring:
        lines.append(f'    """{docstring}"""')

    for field in fields:
        field_name = field['name']
        field_type = field['type']

        # Check if optional
        if field.get('optional', False):
            field_type = f"Optional[{field_type}]"

        field_def = f"    {field_name}: {field_type}"

        # Add Field() for validation
        field_args = []

        if 'default' in field:
            field_args.append(f"default={field['default']}")

        if 'description' in field:
            field_args.append(f"description='{field['description']}'")

        if 'min_length' in field:
            field_args.append(f"min_length={field['min_length']}")

        if 'max_length' in field:
            field_args.append(f"max_length={field['max_length']}")

        if field_args:
            field_def += f" = Field({', '.join(field_args)})"

        lines.append(field_def)

    lines.append("")
    lines.append("    class Config:")
    lines.append("        from_attributes = True")

    return "\n".join(lines)


def generate_sqlalchemy_model(
    name: str,
    table_name: str,
    columns: List[Dict[str, Any]],
    relationships: Optional[List[Dict[str, str]]] = None
) -> str:
    """
    Generate SQLAlchemy model.

    Args:
        name: Model class name
        table_name: Database table name
        columns: List of column definitions
        relationships: List of relationship definitions

    Returns:
        Generated SQLAlchemy model code
    """
    lines = [
        "from datetime import datetime",
        "from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey",
        "from sqlalchemy.orm import relationship",
        "from app.db.postgres import Base",
        "",
        "",
        f"class {name}(Base):",
        f'    """{name} model"""',
        "",
        f'    __tablename__ = "{table_name}"',
        ""
    ]

    # Add columns
    for col in columns:
        col_name = col['name']
        col_type = col['type']
        col_def = f"    {col_name} = Column({col_type}"

        # Add column options
        if col.get('primary_key', False):
            col_def += ", primary_key=True"

        if col.get('unique', False):
            col_def += ", unique=True"

        if col.get('nullable', True) is False:
            col_def += ", nullable=False"

        if col.get('index', False):
            col_def += ", index=True"

        if 'default' in col:
            col_def += f", default={col['default']}"

        if 'foreign_key' in col:
            col_def += f", ForeignKey('{col['foreign_key']}')"

        col_def += ")"

        lines.append(col_def)

    # Add relationships
    if relationships:
        lines.append("")
        lines.append("    # Relationships")

        for rel in relationships:
            rel_name = rel['name']
            rel_model = rel['model']
            rel_def = f'    {rel_name} = relationship("{rel_model}"'

            if 'back_populates' in rel:
                rel_def += f", back_populates='{rel['back_populates']}'"

            if 'cascade' in rel:
                rel_def += f", cascade='{rel['cascade']}'"

            rel_def += ")"

            lines.append(rel_def)

    # Add __repr__
    lines.append("")
    lines.append("    def __repr__(self):")
    if 'id' in [c['name'] for c in columns]:
        lines.append(f"        return f\"<{name}(id={{self.id}})>\"")
    else:
        lines.append(f"        return f\"<{name}>\"")

    return "\n".join(lines)


def generate_fastapi_endpoint(
    path: str,
    method: str,
    function_name: str,
    parameters: List[Dict[str, str]],
    response_model: Optional[str] = None,
    docstring: Optional[str] = None
) -> str:
    """
    Generate FastAPI endpoint.

    Args:
        path: Endpoint path
        method: HTTP method
        function_name: Function name
        parameters: Function parameters
        response_model: Response model type
        docstring: Endpoint documentation

    Returns:
        Generated endpoint code
    """
    lines = []

    # Decorator
    decorator = f"@router.{method.lower()}('{path}'"

    if response_model:
        decorator += f", response_model={response_model}"

    decorator += ")"

    lines.append(decorator)

    # Function signature
    params = []
    for param in parameters:
        param_str = f"{param['name']}: {param['type']}"
        if 'default' in param:
            param_str += f" = {param['default']}"
        params.append(param_str)

    lines.append(f"async def {function_name}(")

    for i, param in enumerate(params):
        if i < len(params) - 1:
            lines.append(f"    {param},")
        else:
            lines.append(f"    {param}")

    lines.append("):")

    # Docstring
    if docstring:
        lines.append(f'    """{docstring}"""')

    lines.append("    # TODO: Implement")
    lines.append("    pass")

    return "\n".join(lines)


def generate_imports(modules: List[str]) -> str:
    """
    Generate import statements.

    Args:
        modules: List of modules to import

    Returns:
        Import statements
    """
    lines = []

    for module in modules:
        lines.append(f"from {module}")

    return "\n".join(lines)
