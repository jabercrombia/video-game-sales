from fastapi import APIRouter, HTTPException
from db import get_db_connection
from itertools import groupby

router = APIRouter()

# return all films
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
                global_sales 
            FROM vgsales ORDER BY name ASC LIMIT 100
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
                "other_sales": row[7],  # Added missing field
                "global_sales": row[8]  # Included global sales
            }
        }
        nested_sales.append(game_data)  # Moved inside the loop

    return nested_sales  # Returns the correctly formatted list