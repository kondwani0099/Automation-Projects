import cv2
import serial

# Replace the serial_port variable with the appropriate serial port your Arduino is connected to
serial_port = "COM5"  # Windows example, for Linux: "/dev/ttyACM0"

# Initialize the serial connection with the Arduino
arduino = serial.Serial(serial_port, 9600, timeout=1)
arduino.flush()

def detect_color(image):
    # Convert the image from BGR to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for red, green, and blue colors in HSV
    lower_red = (0, 100, 100)
    upper_red = (10, 255, 255)
    lower_green = (40, 100, 100)
    upper_green = (80, 255, 255)
    lower_blue = (100, 100, 100)
    upper_blue = (130, 255, 255)

    # Create masks for each color
    mask_red = cv2.inRange(hsv_image, lower_red, upper_red)
    mask_green = cv2.inRange(hsv_image, lower_green, upper_green)
    mask_blue = cv2.inRange(hsv_image, lower_blue, upper_blue)

    # Find the largest contour in each mask
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Choose the color with the largest contour area
    color = None
    if contours_red and max(contours_red, key=cv2.contourArea) is not None:
        color = "red"
    elif contours_green and max(contours_green, key=cv2.contourArea) is not None:
        color = "green"
    elif contours_blue and max(contours_blue, key=cv2.contourArea) is not None:
        color = "blue"

    return color
def draw_bounding_box(frame, color):
    # Draw a bounding box around the detected color region
    if color == "red":
        color_lower = (0, 100, 100)
        color_upper = (10, 255, 255)
        bbox_color = (0, 0, 255)  # Red
    elif color == "green":
        color_lower = (40, 100, 100)
        color_upper = (80, 255, 255)
        bbox_color = (0, 255, 0)  # Green
    elif color == "blue":
        color_lower = (100, 100, 100)
        color_upper = (130, 255, 255)
        bbox_color = (255, 0, 0)  # Blue

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_frame, color_lower, color_upper)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 100:  # Minimum contour area threshold to filter out noise
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), bbox_color, 2)

    return frame

def main():
    cap = cv2.VideoCapture(1)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        color = detect_color(frame)

        if color:
            print("Detected color:", color)
            frame = draw_bounding_box(frame, color)

            # Send a signal to the Arduino based on the detected color
            if color == "red":
                arduino.write(b'R')  # Send 'R' to move the servo to a predefined position for red
            elif color == "green":
                arduino.write(b'G')  # Send 'G' to move the servo to a predefined position for green
            elif color == "blue":
                arduino.write(b'B')  # Send 'B' to move the servo to a predefined position for blue

        cv2.imshow('Color Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    arduino.close()

if __name__ == "__main__":
    main()
