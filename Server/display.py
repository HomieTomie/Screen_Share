import subprocess
<<<<<<< HEAD
import platform
import signal
import sys

# Configuration
address = "127.0.0.1"  # IP address for UDP streaming
port = 2222  # Port for the stream

# Determine the screen capture command based on the operating system
def get_screen_capture_command():
    if platform.system() == "Windows":
        # For Windows, use gdigrab to capture the screen
        return [
            "ffmpeg",
            "-f", "gdigrab",  # Use the gdigrab screen capture method (Windows)
            "-i", "desktop",  # Capture the entire desktop
        ]
    elif platform.system() == "Linux":
        # For Linux, use X11 screen capture (make sure to have x11grab installed)
        return [
            "ffmpeg",
            "-f", "x11grab",  # Use the x11grab screen capture method (Linux)
            "-s", "1920x1080",  # Set screen resolution, change if needed
            "-i", ":0.0",  # Capture from display 0
        ]
    else:
        raise Exception("Unsupported OS")

# Start the ffmpeg screen capture stream
def start_ffmpeg_stream():
    screen_capture_command = get_screen_capture_command()
    
    # Add the encoding and streaming options to the command
    ffmpeg_command = screen_capture_command + [
        "-an",  # Disable audio
        "-c:v", "libx264",  # Use H.264 video codec
        "-preset", "ultrafast",  # Optimize for low latency
        "-tune", "zerolatency",  # Tune for real-time streaming
        "-f", "mpegts",  # Format as MPEG-TS
        f"udp://{address}:{port}?pkt_size=1316"  # Stream via UDP
=======

def start_rtp_stream():
    """
    Start streaming the computer screen to a specific Android device using RTP.
    """
    # Hardcoded IP and port
    ip = "172.20.10.8"
    port = 5005

    # FFmpeg command to stream the screen via RTP
    command = [
        "ffmpeg",
        "-f", "gdigrab",  # Capture the screen on Windows
        "-i", "desktop",  # Capture the entire desktop
        "-s", "480x800",  # Set resolution to match the client device
        "-vcodec", "libx264",  # Use H.264 codec for streaming
        "-preset", "ultrafast",  # Use ultrafast preset for low latency
        "-tune", "zerolatency",  # Optimize for low latency
        "-f", "rtp",  # Output format is RTP
        f"rtp://{ip}:{port}"  # Destination address
>>>>>>> b5d949e6eabfaf80721e2608f90cd5fb06afe0eb
    ]

    print("Starting the FFmpeg screen capture stream...")
    return subprocess.Popen(ffmpeg_command)

# Gracefully handle Ctrl+C
def signal_handler(sig, frame):
    print("\nStopping the FFmpeg stream...")
    if ffmpeg_process:
        ffmpeg_process.terminate()
    sys.exit(0)

# Main function to run the program
def main():
    global ffmpeg_process
    # Capture the signal for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    # Start the ffmpeg process to stream the screen
    ffmpeg_process = start_ffmpeg_stream()

    # Keep the script running until interrupted
    try:
<<<<<<< HEAD
        while True:
            pass
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    ffmpeg_process = None  # Global variable to track the FFmpeg process
    main()
=======
        print(f"Starting RTP stream to {ip}:{port}... Press Ctrl+C to stop.")
        # Launch FFmpeg as a subprocess
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to start the RTP stream: {e}")
    except KeyboardInterrupt:
        print("Stream stopped by user.")

if __name__ == "__main__":
    try:
        start_rtp_stream()
    except Exception as e:
        print(f"Error: {e}")
>>>>>>> b5d949e6eabfaf80721e2608f90cd5fb06afe0eb
