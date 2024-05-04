import cv2
import numpy as np
import pytesseract
import time

# Function to process frame and detect text
def process_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Apply thresholding to create binary image with black text on white background
    thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)[1]

    items = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = items[0] if len(items) == 2 else items[1]

    img_contour = frame.copy()
    detected_text = ""
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        ratio = h / w
        area = cv2.contourArea(c)
        base = np.ones(thresh.shape, dtype=np.uint8)
        if 100 < area < 100000:
            base[y:y + h, x:x + w] = thresh[y:y + h, x:x + w]
            segment = cv2.bitwise_not(base)  # Invert the binary image

            custom_config = r'-l eng --oem 3 --psm 10 -c tessedit_char_whitelist="AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz" '
            text = pytesseract.image_to_string(segment, config=custom_config)
            detected_text += text + "\n"

            # Draw contours on the frame
            cv2.drawContours(img_contour, [c], -1, (0, 0, 255), 2)

    return img_contour, detected_text

# Open camera stream
cap = cv2.VideoCapture(0)

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
        
        if detected_text == prev_text and detected_text != "" and detected_text != " ":
            if time.time() - pause_start_time >= 1:
                print("Pausing processing for 3 seconds.............................")
                pause_processing = True
                pause_start_time = time.time()
        else:
            prev_text = detected_text
            pause_start_time = time.time()

        cv2.imshow("Camera Stream", processed_frame)
    else:
        # Display a message indicating processing is paused
        cv2.imshow("Camera Stream", resized_frame)
    
    # Display detected text
    print("Detected text: ", detected_text)

    # Check if 3 seconds have elapsed since processing was paused
    if pause_processing and time.time() - pause_start_time >= 3:
        pause_processing = False  # Resume processing

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
