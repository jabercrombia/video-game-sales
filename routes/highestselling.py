from fastapi import APIRouter, HTTPException, Query
from db import get_db_connection

router = APIRouter()

# Allowed columns for sorting
VALID_GROUP_COLUMNS = {"genre", "publisher", "platform"}

@router.get("/highest/{column_name}")
def get_highest_total_sales(
    column_name: str,
    limit: int = Query(default=5, alias="limit")  # Default: top 5 results
):
    """
    Returns the highest total sales grouped by a given column.

    Example:
    - `/highest/genre` → Top 5 genres by global sales
    - `/highest/publisher?limit=10` → Top 10 publishers by global sales
    """

    # Validate column name
    if column_name not in VALID_GROUP_COLUMNS:
        raise HTTPException(status_code=400, detail=f"Invalid column '{column_name}'. Allowed: {VALID_GROUP_COLUMNS}")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Construct SQL dynamically
    query = f"""
        SELECT {column_name}, SUM(global_sales::NUMERIC) AS total_sales
        FROM vgsales
        GROUP BY {column_name}
        ORDER BY total_sales DESC
        LIMIT {limit}
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if not rows:
        raise HTTPException(status_code=404, detail="No data found")

    return [{column_name: row[0].replace('-','_').replace(' ','_'), "total_sales": row[1]} for row in rows]