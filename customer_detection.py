

import cv2
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolo11n.pt")


def detect_customers(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    total_detections = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Detect persons only (class 0)
        results = model(
            frame,
            classes=[0],
            conf=0.4,
            verbose=False
        )

        # Draw detection boxes
        annotated_frame = results[0].plot()

        # Count people detected in this frame
        current_count = len(results[0].boxes)

        cv2.putText(
            annotated_frame,
            f"People detected: {current_count}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.imshow("Smart Retail - Customer Detection", annotated_frame)

        total_detections += current_count

        # Press Q to close
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    print("Total person detections across frames:", total_detections)


if __name__ == "__main__":
    video_path = input("Enter video file path: ")
    detect_customers(video_path)
