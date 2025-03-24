from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List

from db import get_db_connection

router = APIRouter()

# return all films
@router.get("/platform/{name}")
def get_platform(
    name: str,
    include: Optional[str] = Query(None, alias="include"),  # Columns to include
    query: str = Query(default="name", alias="query"),  
    order: str = Query(default="ASC", alias="order"),
    limit: int = Query(default=10, alias="limit")  # Default limit = 10
):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    cursor = conn.cursor()

    # Allowed columns to prevent SQL injection
    all_columns = {
        "rank", "name", "platform", "alias_name", "year", "genre", "publisher",
        "na_sales", "eu_sales", "jp_sales", "other_sales", "global_sales"
    }

    selected_columns = all_columns.copy()  # Default: Select all columns

    # Handle inclusion of specific columns
    if include:
        requested_columns = set(include.split(","))
        selected_columns = requested_columns.intersection(all_columns)  # Only keep valid columns

    # Ensure at least one column is selected
    if not selected_columns:
        return HTTPException(status_code=400, detail="No valid columns selected.")
    
    # Validate query sorting column
    if query not in all_columns:
        query = "name"  # Default

    order = order.upper()
    if order not in ["ASC", "DESC"]:
        order = "DESC"  # Default
        
    if limit < 1 or limit > 100:  # Restricting limit between 1 and 100
        limit = 10  # Default limitj

    # Construct dynamic SQL query
    column_str = ", ".join(selected_columns)  # Convert set to SQL-friendly string
    sql_query = f"""
        SELECT {column_str}
        FROM vgsales v
        JOIN platform_aliases p ON v.platform = p.platform_name 
        WHERE LOWER(p.alias_name) = LOWER(%s)
        ORDER BY {query} {order}
        LIMIT %s;
    """

    cursor.execute(sql_query, (name, limit))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # ✅ Convert SQL results to dictionary format
    results = [dict(zip(selected_columns, row)) for row in rows]

    return results
