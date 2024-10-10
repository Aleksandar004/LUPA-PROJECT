import cv2
import numpy as np
import os
from database import insert_crack_coordinates

def detect_cracks(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    edges = cv2.Canny(blurred, 30, 130)

    kernel = np.ones((3, 3), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)
    edges = cv2.erode(edges, kernel, iterations=1)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cracks = [contour for contour in contours if cv2.contourArea(contour) > 50]
    return cracks, edges

def draw_cracks(image_path, cracks, conn):
    img = cv2.imread(image_path)
    for contour in cracks:
        cv2.polylines(img, [contour], isClosed=False, color=(0, 0, 255), thickness=2)

        if len(contour) > 1:
            x_start, y_start = contour[0][0]
            x_end, y_end = contour[-1][0]
            insert_crack_coordinates(conn, x_start, y_start, x_end, y_end)

    processed_image_path = os.path.splitext(image_path)[0] + "_processed.png"
    cv2.imwrite(processed_image_path, img)
    return processed_image_path
