#*************************Author : Eng. Kondwani Nirenda *************************
#************Date code was last updated : 5th August ,2023***************************
#To use this code just  pip install mediapipe to install media pipe in commandline or terminal
#Then pip install pyserial to install serial communication module in commandline or terminal

import cv2
import mediapipe as mp
import serial

# Define the serial port to communicate with Arduino
SERIAL_PORT = 'COM5'  # Change this to the appropriate serial port of your Arduino

# Initialize MediaPipe Hand Tracking
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Create a connection to the Arduino
arduino = serial.Serial(SERIAL_PORT, 9600, timeout=1)

# Function to send the gesture signal to Arduino
def send_signal_to_arduino(signal):
    arduino.write(signal.encode())

# Main function for gesture recognition
def main():
    # Initialize webcam video capture
    cap = cv2.VideoCapture(1)

    with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Failed to capture frame.")
                break

            # Convert the image to RGB for MediaPipe
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Process the hand landmarks using MediaPipe
            results = hands.process(image_rgb)

            # Draw the hand landmarks on the image
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    # Hand landmarks indices
                    thumb_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
                    index_finger_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y

                          # Define the threshold value for the thumbs-up gesture
                    thumbs_up_threshold = 0.2  # Adjust this value based on your hand's position

                    # Check if the thumb tip is below the index finger tip (thumbs-up)
                    if thumb_tip_y < index_finger_tip_y - thumbs_up_threshold:
                        send_signal_to_arduino('1')  # Turn on the LED
                    else:
                         send_signal_to_arduino('0')  # Turn off the LED
#****************************this part is for the index finger gesture *****************************
                    # mp_drawing.draw_landmarks(
                    #     image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # # Get the x-coordinate of the index finger tip
                    # index_finger_x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x

                    # # Define a threshold value for gesture recognition
                    # gesture_threshold = 0.6

                    # Send signal to Arduino based on the gesture
                    # if index_finger_x > gesture_threshold:
                    #     send_signal_to_arduino('1')  # Turn on the LED
                    #     print(1)
                    # else:
                    #     send_signal_to_arduino('0')  # Turn off the LED
                    #     print(0)

            # Display the image with annotations
            cv2.imshow('Gesture Control', image)

            # Exit the loop when 'q' is pressed
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    arduino.close()

if __name__ == "__main__":
    main()
