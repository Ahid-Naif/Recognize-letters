import cv2
import numpy as np
import pytesseract
import time
import re
import serial

# Initialize serial connection with port
try:
    ser = serial.Serial('COM9', 9600, timeout=1)
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit(1)

# Function to send a single message
def send_message(message):
    print("Sending message:", message)
    ser.write(message.encode())  # Send message to Arduino

def extract_single_letter(text):
    # Remove all whitespace characters
    cleaned_text = re.sub(r'\s+', '', text)
    # Extract a single letter (ignores numbers or symbols)
    match = re.match(r'([a-zA-Z])$', cleaned_text)
    return match.group(1) if match else None

# Function to process frame and detect text
def process_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Adaptive thresholding for improved text detection under varying lighting
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY_INV, 11, 2)

    items = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = items[0] if len(items) == 2 else items[1]

    img_contour = frame.copy()
    detected_text = ""

    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        ratio = w / h   # Aspect ratio calculation
        area = cv2.contourArea(c)

        # Aspect ratio, size, and area constraints for better text detection
        if 0.4 < ratio < 3.0 and 10 < w < 150 and 10 < h < 150:
            base = np.ones(thresh.shape, dtype=np.uint8)
            base[y:y + h, x:x + w] = thresh[y:y + h, x:x + w]
            segment = cv2.bitwise_not(base)  # Invert binary image for Tesseract

            custom_config = r'-l eng --oem 3 --psm 10 -c tessedit_char_whitelist="AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"'
            text = pytesseract.image_to_string(segment, config=custom_config)
            detected_text = text
            # print("text: ", detected_text)
            # print("\n")

            # Draw valid contours
            cv2.drawContours(img_contour, [c], -1, (0, 0, 255), 2)

    return img_contour, detected_text

# Open camera stream
cap = cv2.VideoCapture(1)

prev_text = ""
pause_processing = False
pause_start_time = time.time()

# Set the desired width and height for resizing
resize_width = 320
resize_height = 240

while True:
    ret, frame = cap.read()
    if not pause_processing:
        if not ret:
            break
        
        # Resize the frame
        resized_frame = cv2.resize(frame, (resize_width, resize_height))
        
        processed_frame, detected_text = process_frame(resized_frame)
        # print("UnFiltered  text: ", detected_text)
        filtered_text = extract_single_letter(detected_text)
        
        if filtered_text == prev_text and filtered_text != "" and filtered_text != " ":
            if time.time() - pause_start_time >= 1:
                print("Pausing processing for 3 seconds.............................")
                pause_processing = True
                pause_start_time = time.time()
        else:
            if filtered_text is not None:
                detected_text = filtered_text
                prev_text = detected_text
                pause_start_time = time.time()

                # Display detected text
                print("Detected text: ", detected_text)
                send_message(detected_text)

        cv2.imshow("Camera Stream", processed_frame)
    else:
        # Display a message indicating processing is paused
        cv2.imshow("Camera Stream", resized_frame)

    # Check if 3 seconds have elapsed since processing was paused
    if pause_processing and time.time() - pause_start_time >= 3:
        pause_processing = False  # Resume processing

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()