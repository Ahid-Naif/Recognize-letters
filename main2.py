import serial
import time

# Initialize serial connection with Arduino
ser = serial.Serial('/dev/ttyAMA0', 9600)  # Adjust port name and baud rate as needed

# Function to send a single message
def send_message(message):
    print("Sending message:", message)
    ser.write(message.encode())  # Send message to Arduino

# Continuously send messages in a loop
message_counter = 1
while True:
    message = str(message_counter)
    send_message(message)
    message_counter += 1
    if message_counter > 3:  # Reset counter after reaching 3
        message_counter = 1
    time.sleep(1)  # Delay for 1 second
