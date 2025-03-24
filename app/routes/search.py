from fastapi import APIRouter, HTTPException
from db import get_db_connection

router = APIRouter()

# return all films
@router.get("/artist/{artist_name}")
def get_artist(artist_name: str):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")


    cursor = conn.cursor()
    cursor.execute("SELECT artist, category, song_or_album, year FROM grammys WHERE artist ILIKE %s", ('%' + artist_name + '%',))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convert to list of dicts
    artist = [{"artist": row[0], "category" : row[1], "song_or_album" : row[2], "year" : row[3] } for row in rows]

    return artist
