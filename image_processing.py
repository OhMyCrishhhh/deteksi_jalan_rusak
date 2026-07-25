import cv2
import numpy as np


# ============================
# PARAMETER (mudah diubah)
# ============================

GAUSSIAN_KERNEL = (7, 7)

CANNY_LOW = 30
CANNY_HIGH = 100

MIN_CONTOUR_AREA = 200

MORPH_KERNEL = (3, 3)
MORPH_ITERATIONS = 1


class ImageProcessor:

    def __init__(self):
        pass

    # ============================
    # Membaca gambar
    # ============================

    def load_image(self, path):

        image = cv2.imread(path)

        return image

    # ============================
    # RGB -> Grayscale
    # ============================

    def grayscale(self, image):

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        return gray

    # ============================
    # Mengurangi noise
    # ============================

    def gaussian_blur(self, gray):

        blur = cv2.GaussianBlur(
            gray,
            GAUSSIAN_KERNEL,
            0
        )

        return blur

    # ============================
    # Threshold
    # ============================

    def threshold(self, blur):

        _, thresh = cv2.threshold(
        blur,
        110,
        255,
        cv2.THRESH_BINARY_INV
    )

        return thresh

    # ============================
    # Canny Edge
    # ============================

    def edge_detection(self, thresh):

        edges = cv2.Canny(
            thresh,
            CANNY_LOW,
            CANNY_HIGH
        )

        return edges

    # ============================
    # Morphology
    # ============================

    def morphology(self, edge):

        kernel = np.ones((3,3), np.uint8)

        morph = cv2.dilate(edge, kernel, iterations=2)

        morph = cv2.erode(morph, kernel, iterations=1)

        return morph
    
    # ============================
    # Contour Detection
    # ============================

    def detect_damage(self, image, morph):

        result = image.copy()

        contours, _ = cv2.findContours(
            morph,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        total_area = 0
        damage_count = 0

        for contour in contours:

            area = cv2.contourArea(contour)

            if area < MIN_CONTOUR_AREA:
                continue

            x, y, w, h = cv2.boundingRect(contour)

        # Abaikan objek yang terlalu kecil
            if w < 20 or h < 20:
                continue

            damage_count += 1
            total_area += area

            cv2.rectangle(
                result,
                (x, y),
                (x + w, y + h),
                (0, 0, 255),
                2
    )

            cv2.putText(
                result,
                f"Kerusakan {damage_count}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2
    )

        return result, damage_count, total_area
    # ============================
    # Menghitung persentase
    # ============================

    def calculate_percentage(self, image, total_area):

        h, w = image.shape[:2]

        image_area = h * w

        percentage = (total_area / image_area) * 100

        return percentage
    # ============================
    # Status Jalan
    # ============================

    def road_status(self, percentage):

        if percentage < 3:
            return "Jalan Baik"

        elif percentage < 8:
            return "Rusak Ringan"

        else:
            return "Rusak Berat"