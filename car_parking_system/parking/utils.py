import cv2
from paddleocr import PaddleOCR
from ultralytics import YOLO


# def get_ocr_model():
#     return PaddleOCR(use_gpu=False, show_log=False)

# # Load YOLO model
# yolo_model = YOLO('yolov8n.pt')  # Replace with custom ANPR weights if available

# # Initialize PaddleOCR
# ocr_reader = PaddleOCR(use_angle_cls=True, lang='en')

# def detect_number_plate(image_path):
#     image = cv2.imread(image_path)

#     # YOLO Detection
#     results = yolo_model(image)
#     for result in results:
#         for box in result.boxes:
#             x1, y1, x2, y2 = map(int, box.xyxy[0])
#             cropped_plate = image[y1:y2, x1:x2]

#             # OCR for text recognition
#             ocr_results = ocr_reader.ocr(cropped_plate, cls=True)
#             if ocr_results:
#                 plate_text = ocr_results[0][0][1][0]
#                 return plate_text.strip()

#     return None






def get_ocr_model():
    return PaddleOCR(use_gpu=False, show_log=False)

# Load YOLO model
yolo_model = YOLO('yolov8n.pt')  # Replace with custom ANPR weights if available

# Initialize PaddleOCR
ocr_reader = get_ocr_model()

def detect_number_plate(image_path):
    try:
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Image not found or invalid format.")

        # YOLO Detection
        results = yolo_model(image)
        for result in results:
            for box in result.boxes.data:
                x1, y1, x2, y2 = map(int, box[:4])
                height, width, _ = image.shape
                x1, y1, x2, y2 = max(0, x1), max(0, y1), min(width, x2), min(height, y2)

                cropped_plate = image[y1:y2, x1:x2]
                if cropped_plate.size > 0:
                    # OCR for text recognition
                    ocr_results = ocr_reader.ocr(cropped_plate, cls=True)
                    if ocr_results:
                        plate_text = ocr_results[0][0][1][0]
                        return plate_text.strip()

        print("No number plate detected.")
        return None
    except Exception as e:
        print(f"Error during detection: {e}")
        return None




