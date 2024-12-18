<<<<<<< HEAD
rtp://{IP_ADDRESS}:{PORT}
=======
import socket
import cv2
import pickle
import time
import threading
from _thread import *
import base64
import mss
import numpy as np

HEADERSIZE = 4

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip = "127.0.0.1"
port = 5051  # Updated to your desired port for streaming

try:
    s.bind((ip, port))
    print("[+] Server started on " + ip)
except socket.error as e:
    print("[-] Couldn't start server on " + ip)

connected_clients = set()

video_frames = []

# Screen capture function using mss (instead of a video file)
def capture_and_stream():
    print("[+] Server is capturing the screen, please wait...")
    
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Choose the monitor (screen) for capture
        while True:
            screenshot = sct.grab(monitor)
            frame = np.array(screenshot)

            # Resize the frame to a resolution that fits your phone screen
            frame_resized = cv2.resize(frame, (480, 800), interpolation=cv2.INTER_AREA)

            # Encode the frame as a JPEG image
            ret, buffer = cv2.imencode('.jpg', frame_resized)
            if ret:
                encoded_frame = buffer.tobytes()

                # Store the encoded frame for later transmission
                video_frames.append(encoded_frame)

    print("[+] Screen capture and encoding completed... ready to stream.")
    main()

# Client handler thread that sends the frames
def client_thread(address):
    start = time.time_ns()
    try:
        for x in video_frames:
            if address in connected_clients:
                # Send the frame to the client
                s.sendto(pickle.dumps(x), address)
                time.sleep(0.016)  # Simulate frame rate (approx 60 FPS)
        
        # Notify client to disconnect after streaming ends
        s.sendto(bytes("disconnect", "utf-8"), address)
        print(f"Client {address[0]} disconnected.")
        
        end = time.time_ns()
        elapsed_time = (end - start) / 1e9
        print(f"Viewing time for client {address[0]}: {elapsed_time} seconds")
        
        # Log the viewing time
        with open("report.txt", "a") as file:
            file.write(f"\nClient {address[0]} viewed the video for {elapsed_time} seconds")
        
    except Exception as e:
        print(f"Error with client {address[0]}: {e}")

# Main server function
def main():
    while True:
        data, client = s.recvfrom(2 ** 16)
        print(data)
        
        if "dis" in str(data):  # If client sends "disconnect" signal
            connected_clients.remove(client)
        elif client not in connected_clients:  # If it's a new client
            print(f"[+] Streaming to {str(client[0])}")
            connected_clients.add(client)
            t = threading.Thread(target=client_thread, args=(client,))
            t.start()

# Initialize video capture and start streaming
capture_and_stream()
>>>>>>> b5d949e6eabfaf80721e2608f90cd5fb06afe0eb
