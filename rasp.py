import cv2
import numpy as np
import pytesseract
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

# Initialize PiCamera
camera = PiCamera()
camera.resolution = (640, 480)  # Adjust resolution as needed
camera.framerate = 30  # Adjust framerate as needed
rawCapture = PiRGBArray(camera, size=(640, 480))  # Adjust size as needed

# Allow the camera to warm up
time.sleep(0.1)

# Function to process frame and detect text
def process_frame(frame):
    # Your existing image processing code here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    items = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = items[0] if len(items) == 2 else items[1]

    img_contour = frame.copy()
    detected_text = ""
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        ratio = h / w
        area = cv2.contourArea(c)
        base = np.ones(thresh.shape, dtype=np.uint8)
        if ratio > 0.9 and 100 < area < 100000:
            base[y:y + h, x:x + w] = thresh[y:y + h, x:x + w]
            segment = cv2.bitwise_not(base)

            custom_config = r'-l eng --oem 3 --psm 10 -c tessedit_char_whitelist="AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz" '
            text = pytesseract.image_to_string(segment, config=custom_config)
            detected_text += text + "\n"

            # Draw contours on the frame
            cv2.drawContours(img_contour, [c], -1, (0, 0, 255), 2)
    
    # Display detected text
    print("Detected text: ", detected_text)

    return img_contour

# Capture frames from PiCamera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # Grab the raw NumPy array representing the image
    image = frame.array

    # Process the frame
    processed_frame = process_frame(image)

    # Display the processed frame
    cv2.imshow("PiCamera Stream", processed_frame)
    
    # Clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # Check for 'q' key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cv2.destroyAllWindows()
