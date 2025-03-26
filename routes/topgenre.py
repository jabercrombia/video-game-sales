from fastapi import APIRouter, HTTPException
from db import get_db_connection

router = APIRouter()

@router.get("/top-genre/{platform}")
def get_top_genre(platform: str):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    cursor = conn.cursor()

    # ✅ SQL Query using the platform from the route parameter
    sql_query = """
        SELECT genre, SUM(global_sales::NUMERIC) AS total_sales
        FROM vgsales v
        JOIN platform_aliases p ON v.platform = p.platform_name
        WHERE LOWER(p.alias_name) = LOWER(%s)  -- Use parameterized query
        GROUP BY genre
        ORDER BY total_sales DESC
        LIMIT 5;
    """

    # ✅ Pass platform as a parameter tuple to avoid SQL injection
    cursor.execute(sql_query, (platform,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # change hyphen to underscore for genre
    results = [{"genre": row[0].replace('-','_'), "total_sales": row[1]} for row in rows]

    return results
