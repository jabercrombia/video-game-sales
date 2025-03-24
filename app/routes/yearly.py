from fastapi import APIRouter, HTTPException
from db import get_db_connection

router = APIRouter()

# return all films
@router.get("/yearly/{name}/yearly")
def get_platform(name: str):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")


    cursor = conn.cursor()

    cursor.execute("""
            SELECT v.rank, v.name, v.platform, p.alias_name, v.year, v.genre, v.publisher, v.na_sales, v.eu_sales, v.jp_sales, v.other_sales, v.global_sales
            FROM vgsales v
            JOIN platform_aliases p ON v.platform = p.platform_name WHERE LOWER(p.alias_name) = LOWER(%s) LIMIT 10;
        """,(name,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    nested_sales = []

    for row in rows:
        game_data = {
            "id": row[0],
            "name": row[1],  # Fixed indexing
            "platform": row[2],
            "year": row[4],
            "genre" : row[5],
            "publisher": row[6],
            "sales": {
                "na_sales": row[7],
                "eu_sales": row[8],
                "jp_sales": row[9],
                "other_sales": row[10],  # Added missing field
                "global_sales": row[11]  # Included global sales
            }
        }
        nested_sales.append(game_data)  # Moved inside the loop

    return nested_sales  # Returns the correctly formatted list
    # platform = [{"id": row[0], "name": row[1], "platform" : row[2], "year" : row[4], "genre" : row[5], "publisher": row[6]} for row in rows]

    # return platform
