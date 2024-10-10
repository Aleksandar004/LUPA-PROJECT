from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def insert_crack_coordinates(conn, x_start, y_start, x_end, y_end):
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO "CrackCoordinates" (x_start, y_start, x_end, y_end) VALUES (%s, %s, %s, %s) RETURNING id',
        (int(x_start), int(y_start), int(x_end), int(y_end))
    )
    crack_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return crack_id

def insert_crack_summary(conn, crack_count):
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO "CrackSummary" (crack_count) VALUES (%s) RETURNING image_id',
        (crack_count,)
    )
    image_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return image_id
