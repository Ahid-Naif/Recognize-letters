import cv2
import numpy as np
import pytesseract
import time
import re
import serial

# Initialize serial connection
try:
    ser = serial.Serial('COM3', 9600, timeout=1)
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit(1)

# Function to send a single message
def send_message(message):
    print("Sending message:", message)
    ser.write(message.encode())  # Send message to Arduino

# Function to clean detected text and extract only one word
def extract_single_word(text):
    cleaned_text = re.sub(r'\s+', ' ', text.strip())
    match = re.match(r'([a-zA-Z]+)$', cleaned_text)
    return match.group(1) if match else None

# Trackbar callback function to update the threshold value
def update_threshold(val):
    global threshold_value
    threshold_value = val

# Default threshold value
threshold_value = 100  # Starting point for the threshold value

# Trackbar callback function to update the Gaussian blur kernel size
def update_blur(val):
    global blur_value
    blur_value = max(1, val | 1)  # Ensure kernel size is always odd and ≥ 1

# Default Gaussian blur kernel size
blur_value = 5

# Create a trackbar for threshold adjustment
cv2.namedWindow("Binary")
cv2.createTrackbar("Threshold", "Binary", 100, 255, update_threshold)
# Create a trackbar for Gaussian Blur size adjustment
cv2.createTrackbar("Blur", "Binary", 5, 31, update_blur)  # Max blur size = 31

# Function to process frame and detect text
def process_frame(frame):
    # Define ROI dimensions relative to the resized frame
    x, y, w, h = 50, 100, 220, 80

    # Draw the rectangle for visual guidance
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Extract ROI from the same resized frame
    roi = frame[y:y + h, x:x + w]

    # Preprocess ROI
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (blur_value, blur_value), 0)

    # Improved threshold value for better text visibility
    _, binary = cv2.threshold(blurred, threshold_value, 255, cv2.THRESH_BINARY)

    # Display binary image for debugging
    cv2.imshow("Binary", binary)

    # OCR Configuration for Word Detection
    custom_config = r'-l eng --oem 3 --psm 8 -c tessedit_char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"'
    detected_text = pytesseract.image_to_string(binary, config=custom_config).strip()

    return frame, detected_text

# Open camera stream
cap = cv2.VideoCapture(0)

# Set the desired width and height for resizing
resize_width = 320
resize_height = 240

# Countdown Timer Variables
scan_interval = 15  # Time interval for OCR scan (in seconds)
last_scan_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize the frame for better performance
    resized_frame = cv2.resize(frame, (resize_width, resize_height))

    # Process the frame for rectangle visibility
    processed_frame, _ = process_frame(resized_frame)

    # Countdown Logic
    remaining_time = max(0, scan_interval - int(time.time() - last_scan_time))

    # Show countdown timer on screen
    cv2.putText(processed_frame, f"Next Scan: {remaining_time}s",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # Perform OCR scan every 10 seconds
    if remaining_time == 0:
        _, detected_text = process_frame(resized_frame)
        filtered_text = extract_single_word(detected_text)

        if filtered_text:
            print("Detected word:", filtered_text)
            send_message(filtered_text)

        last_scan_time = time.time()  # Reset timer

    # Display the processed frame (with the rectangle)
    cv2.imshow("Camera Stream", processed_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
