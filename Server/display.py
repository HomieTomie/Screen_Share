import socket
import mss
import cv2
import numpy as np
def capture_and_stream():
    PHONE_WIDTH = 480
    PHONE_HEIGHT = 800
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5050))
    server_socket.listen(1)
    print("Waiting for connection...")
    conn, addr = server_socket.accept()
    print(f"Connected to {addr}")
    try:
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            while True:
                screenshot = sct.grab(monitor)
                frame = np.array(screenshot)
                frame_resized = cv2.resize(frame, (PHONE_WIDTH, PHONE_HEIGHT), interpolation=cv2.INTER_AREA)
                _, buffer = cv2.imencode('.jpg', frame_resized)
                size = len(buffer)
                conn.sendall(size.to_bytes(4, 'big') + buffer.tobytes())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
        server_socket.close()
        print("Server closed.")
capture_and_stream()