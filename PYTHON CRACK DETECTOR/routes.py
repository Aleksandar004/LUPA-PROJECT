from flask import Blueprint, request, jsonify
from crack_detection import detect_cracks, draw_cracks
from database import insert_crack_summary
import cv2

import psycopg2
from config import DATABASE_URL

process_crack_route = Blueprint('process_crack_route', __name__)

@process_crack_route.route('/process-crack', methods=['POST'])
def process_crack():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    image_path = f'uploads/{file.filename}'
    file.save(image_path)

    cracks, edges = detect_cracks(image_path)
    crack_count = len(cracks)
    total_length = sum(cv2.arcLength(contour, closed=False) for contour in cracks)

    conn = psycopg2.connect(DATABASE_URL)
    image_id = insert_crack_summary(conn, crack_count)

    processed_image_path = draw_cracks(image_path, cracks, conn)
    conn.close()

    return jsonify({
        "total_length": total_length,
        "crack_count": crack_count,
        "message": "Crack details successfully inserted into the database.",
        "processed_image": processed_image_path
    }), 200
