import time
from image_processing import ImageProcessor


class RoadDamageDetector:

    def __init__(self):
        self.processor = ImageProcessor()

    def process(self, image_path):

        start = time.time()

        image = self.processor.load_image(image_path)

        gray = self.processor.grayscale(image)

        blur = self.processor.gaussian_blur(gray)

        thresh = self.processor.threshold(blur)

        edge = self.processor.edge_detection(thresh)

        morph = self.processor.morphology(edge)

        result, count, area = self.processor.detect_damage(
            image,
            morph
        )

        percentage = self.processor.calculate_percentage(
            image,
            area
        )

        status = self.processor.road_status(
            percentage
        )

        process_time = time.time() - start

        return {
            "original": image,
            "gray": gray,
            "blur": blur,
            "threshold": thresh,
            "edge": edge,
            "morphology": morph,
            "result": result,
            "count": count,
            "area": area,
            "percentage": percentage,
            "status": status,
            "time": process_time
        }