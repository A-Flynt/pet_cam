import cv2
import socket

# Set up socket for server
SERVER_IP = '0.0.0.0'
SERVER_PORT = 6000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, SERVER_PORT))

# Open video file
VIDEO_SOURCE = 0  # Change this to the index of your USB camera if it's not the default camera
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Set up frame size and encoding parameters
frame_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_rate = int(camera.get(cv2.CAP_PROP_FPS))
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

# Loop through video frames and send to connected clients
while True:

    try:
        # Read video frame
        ret, frame = camera.read()
        if not ret:
            break

        # Convert frame to bytes
        encoded_frame = cv2.imencode('.jpg', frame, encode_param)[1].tobytes()
        #encoded_frame_arr = [encoded_frame[0:len(encoded_frame)//2+1], encoded_frame[(len(encoded_frame)//2)+1:]]
        #print(encoded_frame_arr)
        # Send frame to connected clients
        server_socket.sendto(encoded_frame, ('192.168.50.192', 6000))  # Change the IP address and port to the clients you want to send the frames to
        #server_socket.sendto(encoded_frame_arr[1], ('192.168.50.192', 6000))  # Change the IP address and port to the clients you want to send the frames to
    except Exception:
        quit()





'''
import cv2
import socket
import numpy as np

# Initialize socket
UDP_IP = "0.0.0.0" # Listen to all network interfaces
UDP_PORT = 5000 # Choose a free port
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# Initialize camera
cap = cv2.VideoCapture(0)

# Define video encoding parameters
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Encode frame as JPEG
    _, img_encoded = cv2.imencode('.jpg', frame, encode_param)
    data = np.array(img_encoded)
    stringData = data.tostring()

    # Send frame over UDP
    sock.sendto(stringData, ("255.255.255.0", UDP_PORT)) # Broadcast to all clients on the network
'''