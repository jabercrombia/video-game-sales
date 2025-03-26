from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List

from db import get_db_connection

router = APIRouter()

@router.get("/platform/{name}")
def get_platform(
    name: str,
    include: Optional[str] = Query(None, alias="include"),
    query: str = Query(default="name", alias="query"),
    order: str = Query(default="ASC", alias="order"),
    limit: Optional[int] = Query(None, alias="limit"),
):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    cursor = conn.cursor()

    # Define columns per table to avoid ambiguity
    vgsales_columns = {
        "id", "name", "platform", "year", "genre", "publisher",
        "na_sales", "eu_sales", "jp_sales", "other_sales", "global_sales"
    }

    platform_alias_columns = {"alias_name"}

    all_columns = vgsales_columns | platform_alias_columns  # Union of both sets

    selected_columns = all_columns.copy()  # Default to selecting all

    if include:
        requested_columns = set(include.split(","))
        selected_columns = requested_columns.intersection(all_columns)

    if not selected_columns:
        return HTTPException(status_code=400, detail="No valid columns selected.")
    
    if query not in all_columns:
        query = "name"

    order = order.upper()
    if order not in ["ASC", "DESC"]:
        order = "DESC"

    # Prefix table names to avoid ambiguity
    column_str = ", ".join([f"v.{col}" if col in vgsales_columns else f"p.{col}" for col in selected_columns])
    query_column = f"v.{query}" if query in vgsales_columns else f"p.{query}"

    # Construct SQL query dynamically
    sql_query = f"""
        SELECT {column_str}
        FROM vgsales v
        JOIN platform_aliases p ON v.platform = p.platform_name 
        WHERE LOWER(p.alias_name) = LOWER(%s)
        ORDER BY {query_column} {order}
    """

    params = [name]

    if limit:
        sql_query += " LIMIT %s"
        params.append(limit)

    cursor.execute(sql_query, params)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    results = [dict(zip(selected_columns, row)) for row in rows]

    return results
