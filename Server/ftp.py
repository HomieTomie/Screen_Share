from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from threading import Thread
import socket
import os

def start_ftp_server():
    authorizer = DummyAuthorizer()
    
    # Define user with access to files
    ftp_user = "user"
    ftp_password = "12345"
    base_dir = os.path.dirname(os.path.abspath("cat.mp4"))
    authorizer.add_user(ftp_user, ftp_password, base_dir, perm="elradfmw")

    handler = FTPHandler
    handler.authorizer = authorizer

    # Bind the FTP server
    server = FTPServer(("0.0.0.0", 2121), handler)
    print("FTP server started on port 2121")

    # Start the server
    server.serve_forever()

def stream_file_over_ftsp(host="127.0.0.1", port=5050):
    """FTSP-like server for streaming a file."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"FTSP server running on {host}:{port}")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection accepted from {addr}")
            with client_socket:
                with open("cat.mp4", "rb") as f:
                    while chunk := f.read(1024):  # Stream the file in chunks
                        client_socket.sendall(chunk)

if __name__ == "__main__":
    # Start the FTP server in a separate thread
    ftp_thread = Thread(target=start_ftp_server)
    ftp_thread.daemon = True
    ftp_thread.start()

    # Start FTSP server for streaming
    try:
        stream_file_over_ftsp()
    except KeyboardInterrupt:
        print("Server shutting down.")
