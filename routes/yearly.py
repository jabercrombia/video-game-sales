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
                year,SUM(na_sales::NUMERIC) AS na_sales,SUM(jp_sales::NUMERIC) AS jp_sales,SUM(eu_sales::NUMERIC) AS eu_sales, SUM(other_sales::NUMERIC) AS other_sales, SUM(global_sales::NUMERIC) AS total_sales
                FROM vgsales
                WHERE year IS NOT NULL
                AND year ~ '^[0-9]+$'  -- Regex: Only numeric years
                AND global_sales::NUMERIC IS NOT NULL
                AND global_sales::NUMERIC > 0
                AND na_sales::NUMERIC IS NOT NULL
                AND na_sales::NUMERIC > 0
                AND jp_sales::NUMERIC IS NOT NULL
                AND jp_sales::NUMERIC > 0
                AND eu_sales::NUMERIC IS NOT NULL
                AND eu_sales::NUMERIC > 0
                AND other_sales::NUMERIC IS NOT NULL
                AND other_sales::NUMERIC > 0
                GROUP BY year
                ORDER BY year ASC;
        """)

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    formatted_data = [{"year": row[0], "na_sales": row[1],  "jp_sales": row[2], "eu_sales": row[3],  "other_sales": row[4],  "other_sales": row[5]} for row in rows]
    return formatted_data
