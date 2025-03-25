from fastapi import APIRouter, HTTPException
from db import get_db_connection
from itertools import groupby

router = APIRouter()

# return all sales
@router.get("/allsales/")
def get_allsales():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    cursor = conn.cursor()
    cursor.execute("""
            SELECT 
                name, 
                platform, 
                CAST(regexp_replace(year, '\..*$', '') AS TEXT) AS year, 
                publisher, 
                na_sales, 
                eu_sales, 
                jp_sales, 
                other_sales, 
                global_sales,
                genre
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
            ORDER BY name ASC
        """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    nested_sales = []

    for row in rows:
        game_data = {
            "name": row[0],  # Fixed indexing
            "platform": row[1],
            "year": row[2],
            "publisher": row[3],
            "sales": {
                "na_sales": row[4],
                "eu_sales": row[5],
                "jp_sales": row[6],
                "other_sales": row[7],
                "global_sales": row[8],
            },
            "genre": row[9]
        }
        nested_sales.append(game_data)  # Moved inside the loop

    return nested_sales  # Returns the correctly formatted list