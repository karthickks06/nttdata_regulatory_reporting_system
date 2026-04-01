"""SQL generator sub-agent for generating SQL queries and DDL statements"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import re


class SQLGeneratorAgent:
    """
    Specialized SQL code generator agent.

    Capabilities:
    - Generate SELECT queries
    - Generate INSERT/UPDATE/DELETE statements
    - Generate DDL (CREATE TABLE, ALTER TABLE)
    - Generate views and stored procedures
    - Optimize SQL queries
    """

    def __init__(self, dialect: str = "postgresql"):
        self.name = "SQLGenerator"
        self.dialect = dialect
        self.supported_dialects = ["postgresql", "mysql", "oracle", "mssql"]

    async def generate_select_query(
        self,
        table: str,
        columns: Optional[List[str]] = None,
        where: Optional[Dict[str, Any]] = None,
        joins: Optional[List[Dict[str, Any]]] = None,
        order_by: Optional[List[str]] = None,
        limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate SELECT query.

        Args:
            table: Table name
            columns: List of columns (None for SELECT *)
            where: WHERE conditions
            joins: JOIN clauses
            order_by: ORDER BY columns
            limit: LIMIT value

        Returns:
            Generated SQL query
        """
        try:
            # Build SELECT clause
            if columns:
                select_clause = f"SELECT {', '.join(columns)}"
            else:
                select_clause = "SELECT *"

            # Build FROM clause
            from_clause = f"FROM {table}"

            # Build JOINs
            join_clauses = []
            if joins:
                for join in joins:
                    join_type = join.get('type', 'INNER').upper()
                    join_table = join['table']
                    on_condition = join['on']
                    join_clauses.append(
                        f"{join_type} JOIN {join_table} ON {on_condition}"
                    )

            # Build WHERE clause
            where_clause = ""
            if where:
                conditions = []
                for key, value in where.items():
                    if isinstance(value, str):
                        conditions.append(f"{key} = '{value}'")
                    elif value is None:
                        conditions.append(f"{key} IS NULL")
                    else:
                        conditions.append(f"{key} = {value}")
                where_clause = "WHERE " + " AND ".join(conditions)

            # Build ORDER BY clause
            order_clause = ""
            if order_by:
                order_clause = f"ORDER BY {', '.join(order_by)}"

            # Build LIMIT clause
            limit_clause = ""
            if limit:
                limit_clause = f"LIMIT {limit}"

            # Combine all clauses
            query_parts = [select_clause, from_clause]
            query_parts.extend(join_clauses)
            if where_clause:
                query_parts.append(where_clause)
            if order_clause:
                query_parts.append(order_clause)
            if limit_clause:
                query_parts.append(limit_clause)

            query = "\n".join(query_parts) + ";"

            return {
                "success": True,
                "query": query,
                "query_type": "SELECT",
                "dialect": self.dialect
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def generate_insert_query(
        self,
        table: str,
        columns: List[str],
        values: Optional[List[Any]] = None,
        returning: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Generate INSERT query.

        Args:
            table: Table name
            columns: Column names
            values: Values to insert (optional, generates placeholder)
            returning: Columns to return (PostgreSQL)

        Returns:
            Generated SQL query
        """
        try:
            columns_str = ", ".join(columns)

            if values:
                # Escape string values
                formatted_values = []
                for val in values:
                    if isinstance(val, str):
                        formatted_values.append(f"'{val}'")
                    elif val is None:
                        formatted_values.append("NULL")
                    else:
                        formatted_values.append(str(val))
                values_str = ", ".join(formatted_values)
            else:
                # Generate placeholders
                if self.dialect == "postgresql":
                    placeholders = [f"${i+1}" for i in range(len(columns))]
                else:
                    placeholders = ["?" for _ in columns]
                values_str = ", ".join(placeholders)

            query = f"INSERT INTO {table} ({columns_str})\nVALUES ({values_str})"

            # Add RETURNING clause for PostgreSQL
            if returning and self.dialect == "postgresql":
                query += f"\nRETURNING {', '.join(returning)}"

            query += ";"

            return {
                "success": True,
                "query": query,
                "query_type": "INSERT",
                "dialect": self.dialect
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def generate_update_query(
        self,
        table: str,
        set_values: Dict[str, Any],
        where: Dict[str, Any],
        returning: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Generate UPDATE query.

        Args:
            table: Table name
            set_values: Columns and values to update
            where: WHERE conditions
            returning: Columns to return (PostgreSQL)

        Returns:
            Generated SQL query
        """
        try:
            # Build SET clause
            set_parts = []
            for key, value in set_values.items():
                if isinstance(value, str):
                    set_parts.append(f"{key} = '{value}'")
                elif value is None:
                    set_parts.append(f"{key} = NULL")
                else:
                    set_parts.append(f"{key} = {value}")

            set_clause = ", ".join(set_parts)

            # Build WHERE clause
            where_parts = []
            for key, value in where.items():
                if isinstance(value, str):
                    where_parts.append(f"{key} = '{value}'")
                elif value is None:
                    where_parts.append(f"{key} IS NULL")
                else:
                    where_parts.append(f"{key} = {value}")

            where_clause = " AND ".join(where_parts)

            query = f"UPDATE {table}\nSET {set_clause}\nWHERE {where_clause}"

            # Add RETURNING clause
            if returning and self.dialect == "postgresql":
                query += f"\nRETURNING {', '.join(returning)}"

            query += ";"

            return {
                "success": True,
                "query": query,
                "query_type": "UPDATE",
                "dialect": self.dialect
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def generate_create_table(
        self,
        table_name: str,
        columns: List[Dict[str, Any]],
        primary_key: Optional[List[str]] = None,
        foreign_keys: Optional[List[Dict[str, Any]]] = None,
        indexes: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Generate CREATE TABLE statement.

        Args:
            table_name: Table name
            columns: Column definitions
            primary_key: Primary key columns
            foreign_keys: Foreign key definitions
            indexes: Index definitions

        Returns:
            Generated DDL statement
        """
        try:
            lines = [f"CREATE TABLE {table_name} ("]

            # Column definitions
            column_defs = []
            for col in columns:
                col_name = col['name']
                col_type = col['type']
                col_def = f"    {col_name} {col_type}"

                if col.get('not_null', False):
                    col_def += " NOT NULL"

                if col.get('unique', False):
                    col_def += " UNIQUE"

                if 'default' in col:
                    col_def += f" DEFAULT {col['default']}"

                column_defs.append(col_def)

            # Primary key constraint
            if primary_key:
                pk_cols = ", ".join(primary_key)
                column_defs.append(f"    PRIMARY KEY ({pk_cols})")

            # Foreign key constraints
            if foreign_keys:
                for fk in foreign_keys:
                    fk_cols = ", ".join(fk['columns'])
                    ref_table = fk['ref_table']
                    ref_cols = ", ".join(fk['ref_columns'])
                    fk_def = f"    FOREIGN KEY ({fk_cols}) REFERENCES {ref_table}({ref_cols})"

                    if 'on_delete' in fk:
                        fk_def += f" ON DELETE {fk['on_delete']}"

                    column_defs.append(fk_def)

            lines.append(",\n".join(column_defs))
            lines.append(");")

            query = "\n".join(lines)

            # Add index creation statements
            index_queries = []
            if indexes:
                for idx in indexes:
                    idx_name = idx['name']
                    idx_cols = ", ".join(idx['columns'])
                    idx_type = idx.get('type', '')

                    idx_query = f"CREATE {idx_type} INDEX {idx_name} ON {table_name} ({idx_cols});"
                    index_queries.append(idx_query)

            full_query = query
            if index_queries:
                full_query += "\n\n" + "\n".join(index_queries)

            return {
                "success": True,
                "query": full_query,
                "query_type": "CREATE_TABLE",
                "dialect": self.dialect
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def generate_view(
        self,
        view_name: str,
        select_query: str,
        replace: bool = False
    ) -> Dict[str, Any]:
        """
        Generate CREATE VIEW statement.

        Args:
            view_name: View name
            select_query: SELECT query for view
            replace: Use CREATE OR REPLACE

        Returns:
            Generated view DDL
        """
        try:
            if replace and self.dialect == "postgresql":
                query = f"CREATE OR REPLACE VIEW {view_name} AS\n{select_query}"
            else:
                query = f"CREATE VIEW {view_name} AS\n{select_query}"

            if not query.endswith(';'):
                query += ";"

            return {
                "success": True,
                "query": query,
                "query_type": "CREATE_VIEW",
                "dialect": self.dialect
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def generate_stored_procedure(
        self,
        procedure_name: str,
        parameters: List[Dict[str, str]],
        body: str,
        return_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate stored procedure (PostgreSQL function).

        Args:
            procedure_name: Procedure name
            parameters: Parameter definitions
            body: Procedure body
            return_type: Return type

        Returns:
            Generated procedure DDL
        """
        try:
            if self.dialect != "postgresql":
                return {
                    "success": False,
                    "error": "Stored procedures only supported for PostgreSQL dialect"
                }

            # Build parameter list
            param_defs = []
            for param in parameters:
                param_def = f"{param['name']} {param['type']}"
                if 'default' in param:
                    param_def += f" DEFAULT {param['default']}"
                param_defs.append(param_def)

            params_str = ", ".join(param_defs)
            ret_type = return_type or "void"

            query = f"""CREATE OR REPLACE FUNCTION {procedure_name}({params_str})
RETURNS {ret_type} AS $$
BEGIN
{body}
END;
$$ LANGUAGE plpgsql;"""

            return {
                "success": True,
                "query": query,
                "query_type": "CREATE_FUNCTION",
                "dialect": self.dialect
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def optimize_query(
        self,
        query: str
    ) -> Dict[str, Any]:
        """
        Provide query optimization suggestions.

        Args:
            query: SQL query to optimize

        Returns:
            Optimization suggestions
        """
        suggestions = []

        # Check for SELECT *
        if "SELECT *" in query.upper():
            suggestions.append({
                "type": "SELECT_STAR",
                "message": "Avoid SELECT * - specify only needed columns",
                "severity": "medium"
            })

        # Check for missing WHERE clause
        if "DELETE" in query.upper() and "WHERE" not in query.upper():
            suggestions.append({
                "type": "UNSAFE_DELETE",
                "message": "DELETE without WHERE clause will delete all rows",
                "severity": "high"
            })

        if "UPDATE" in query.upper() and "WHERE" not in query.upper():
            suggestions.append({
                "type": "UNSAFE_UPDATE",
                "message": "UPDATE without WHERE clause will update all rows",
                "severity": "high"
            })

        # Check for LIKE with leading wildcard
        if re.search(r"LIKE\s+'%", query, re.IGNORECASE):
            suggestions.append({
                "type": "LEADING_WILDCARD",
                "message": "LIKE with leading wildcard cannot use index",
                "severity": "medium"
            })

        return {
            "success": True,
            "query": query,
            "suggestions": suggestions,
            "suggestion_count": len(suggestions)
        }
