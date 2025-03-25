from fastapi import APIRouter, HTTPException
from db import get_db_connection

router = APIRouter()

# return all films
@router.get("/yearly/")
def get_yearly():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")


    cursor = conn.cursor()
    cursor.execute("""
            SELECT 
                year, SUM(global_sales::NUMERIC) AS total_sales
                FROM vgsales
                WHERE year IS NOT NULL
                AND year ~ '^[0-9]+$'  -- Regex: Only numeric years
                AND global_sales::NUMERIC IS NOT NULL
                AND global_sales::NUMERIC > 0
                GROUP BY year
                ORDER BY year ASC;
        """)

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    formatted_data = [{"genre": row[0], "total_sales": row[1]} for row in rows]
    return formatted_data
