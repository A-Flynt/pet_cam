
import cv2
import socket
import numpy as np

# Set up socket for client
CLIENT_IP = '0.0.0.0'
CLIENT_PORT = 6000
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind((CLIENT_IP, CLIENT_PORT))

# Set up window for displaying video
WINDOW_NAME = 'Video Stream'
cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

# Loop to receive and display video frames
while True:

    # Receive frame from server
    data, addr = client_socket.recvfrom(65507)  # Use a large buffer size to handle larger frames
    #data1, addr = client_socket.recvfrom(65507)  # Use a large buffer size to handle larger frames

    #data = data0+data1

    frame = np.frombuffer(data, dtype=np.uint8)

    #print(frame)

    # Decode frame and display in window
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    cv2.imshow(WINDOW_NAME, frame)

    # Exit if user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
client_socket.close()
cv2.destroyAllWindows()