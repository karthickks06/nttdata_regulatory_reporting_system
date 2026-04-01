"""SQL generation utility functions"""

from typing import Dict, Any, List, Optional


def generate_insert_statement(
    table: str,
    data: Dict[str, Any],
    returning: Optional[List[str]] = None
) -> str:
    """
    Generate INSERT statement from data dictionary.

    Args:
        table: Table name
        data: Column-value pairs
        returning: Columns to return (PostgreSQL)

    Returns:
        SQL INSERT statement
    """
    columns = list(data.keys())
    values = []

    for value in data.values():
        if isinstance(value, str):
            values.append(f"'{value}'")
        elif value is None:
            values.append("NULL")
        else:
            values.append(str(value))

    sql = f"INSERT INTO {table} ({', '.join(columns)})\n"
    sql += f"VALUES ({', '.join(values)})"

    if returning:
        sql += f"\nRETURNING {', '.join(returning)}"

    sql += ";"

    return sql


def generate_update_statement(
    table: str,
    data: Dict[str, Any],
    where: Dict[str, Any],
    returning: Optional[List[str]] = None
) -> str:
    """
    Generate UPDATE statement.

    Args:
        table: Table name
        data: Column-value pairs to update
        where: WHERE clause conditions
        returning: Columns to return (PostgreSQL)

    Returns:
        SQL UPDATE statement
    """
    # Build SET clause
    set_parts = []
    for key, value in data.items():
        if isinstance(value, str):
            set_parts.append(f"{key} = '{value}'")
        elif value is None:
            set_parts.append(f"{key} = NULL")
        else:
            set_parts.append(f"{key} = {value}")

    # Build WHERE clause
    where_parts = []
    for key, value in where.items():
        if isinstance(value, str):
            where_parts.append(f"{key} = '{value}'")
        elif value is None:
            where_parts.append(f"{key} IS NULL")
        else:
            where_parts.append(f"{key} = {value}")

    sql = f"UPDATE {table}\n"
    sql += f"SET {', '.join(set_parts)}\n"
    sql += f"WHERE {' AND '.join(where_parts)}"

    if returning:
        sql += f"\nRETURNING {', '.join(returning)}"

    sql += ";"

    return sql


def generate_select_statement(
    table: str,
    columns: Optional[List[str]] = None,
    where: Optional[Dict[str, Any]] = None,
    order_by: Optional[List[str]] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None
) -> str:
    """
    Generate SELECT statement.

    Args:
        table: Table name
        columns: Columns to select (None for *)
        where: WHERE conditions
        order_by: ORDER BY columns
        limit: LIMIT value
        offset: OFFSET value

    Returns:
        SQL SELECT statement
    """
    # SELECT clause
    if columns:
        sql = f"SELECT {', '.join(columns)}\n"
    else:
        sql = "SELECT *\n"

    # FROM clause
    sql += f"FROM {table}"

    # WHERE clause
    if where:
        where_parts = []
        for key, value in where.items():
            if isinstance(value, str):
                where_parts.append(f"{key} = '{value}'")
            elif value is None:
                where_parts.append(f"{key} IS NULL")
            else:
                where_parts.append(f"{key} = {value}")

        sql += f"\nWHERE {' AND '.join(where_parts)}"

    # ORDER BY clause
    if order_by:
        sql += f"\nORDER BY {', '.join(order_by)}"

    # LIMIT clause
    if limit:
        sql += f"\nLIMIT {limit}"

    # OFFSET clause
    if offset:
        sql += f"\nOFFSET {offset}"

    sql += ";"

    return sql


def generate_join_query(
    base_table: str,
    joins: List[Dict[str, Any]],
    columns: Optional[List[str]] = None,
    where: Optional[Dict[str, Any]] = None
) -> str:
    """
    Generate query with JOINs.

    Args:
        base_table: Base table name
        joins: List of join definitions
        columns: Columns to select
        where: WHERE conditions

    Returns:
        SQL query with JOINs
    """
    # SELECT clause
    if columns:
        sql = f"SELECT {', '.join(columns)}\n"
    else:
        sql = "SELECT *\n"

    # FROM clause
    sql += f"FROM {base_table}"

    # JOIN clauses
    for join in joins:
        join_type = join.get('type', 'INNER').upper()
        join_table = join['table']
        on_condition = join['on']

        sql += f"\n{join_type} JOIN {join_table} ON {on_condition}"

    # WHERE clause
    if where:
        where_parts = []
        for key, value in where.items():
            if isinstance(value, str):
                where_parts.append(f"{key} = '{value}'")
            elif value is None:
                where_parts.append(f"{key} IS NULL")
            else:
                where_parts.append(f"{key} = {value}")

        sql += f"\nWHERE {' AND '.join(where_parts)}"

    sql += ";"

    return sql


def generate_aggregate_query(
    table: str,
    aggregates: List[Dict[str, str]],
    group_by: Optional[List[str]] = None,
    having: Optional[str] = None
) -> str:
    """
    Generate aggregate query (GROUP BY).

    Args:
        table: Table name
        aggregates: List of aggregate functions
        group_by: GROUP BY columns
        having: HAVING clause

    Returns:
        SQL aggregate query
    """
    # Build SELECT clause with aggregates
    select_parts = []

    if group_by:
        select_parts.extend(group_by)

    for agg in aggregates:
        func = agg['function']
        column = agg['column']
        alias = agg.get('alias', f"{func}_{column}")

        select_parts.append(f"{func}({column}) AS {alias}")

    sql = f"SELECT {', '.join(select_parts)}\n"
    sql += f"FROM {table}"

    # GROUP BY clause
    if group_by:
        sql += f"\nGROUP BY {', '.join(group_by)}"

    # HAVING clause
    if having:
        sql += f"\nHAVING {having}"

    sql += ";"

    return sql


def generate_cte_query(
    ctes: List[Dict[str, str]],
    final_query: str
) -> str:
    """
    Generate query with Common Table Expressions (CTEs).

    Args:
        ctes: List of CTE definitions (name and query)
        final_query: Final SELECT query

    Returns:
        SQL query with CTEs
    """
    cte_parts = []

    for cte in ctes:
        name = cte['name']
        query = cte['query'].rstrip(';')
        cte_parts.append(f"{name} AS (\n    {query}\n)")

    sql = "WITH " + ",\n".join(cte_parts) + "\n"
    sql += final_query

    if not sql.endswith(';'):
        sql += ";"

    return sql


def escape_sql_string(value: str) -> str:
    """
    Escape string for SQL (prevent injection).

    Args:
        value: String value

    Returns:
        Escaped string
    """
    # Replace single quotes with double single quotes
    return value.replace("'", "''")


def build_where_clause(conditions: Dict[str, Any]) -> str:
    """
    Build WHERE clause from conditions dictionary.

    Args:
        conditions: Column-value pairs

    Returns:
        WHERE clause string
    """
    parts = []

    for key, value in conditions.items():
        if isinstance(value, str):
            parts.append(f"{key} = '{escape_sql_string(value)}'")
        elif value is None:
            parts.append(f"{key} IS NULL")
        elif isinstance(value, (list, tuple)):
            # IN clause
            if all(isinstance(v, str) for v in value):
                values_str = ", ".join(f"'{escape_sql_string(v)}'" for v in value)
            else:
                values_str = ", ".join(str(v) for v in value)
            parts.append(f"{key} IN ({values_str})")
        else:
            parts.append(f"{key} = {value}")

    return " AND ".join(parts)


def generate_bulk_insert(
    table: str,
    columns: List[str],
    rows: List[List[Any]]
) -> str:
    """
    Generate bulk INSERT statement.

    Args:
        table: Table name
        columns: Column names
        rows: List of row values

    Returns:
        Bulk INSERT statement
    """
    sql = f"INSERT INTO {table} ({', '.join(columns)})\nVALUES\n"

    value_rows = []
    for row in rows:
        values = []
        for value in row:
            if isinstance(value, str):
                values.append(f"'{escape_sql_string(value)}'")
            elif value is None:
                values.append("NULL")
            else:
                values.append(str(value))

        value_rows.append(f"({', '.join(values)})")

    sql += ",\n".join(value_rows) + ";"

    return sql
