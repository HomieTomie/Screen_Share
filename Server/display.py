import subprocess
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
        while True:
            pass
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    ffmpeg_process = None  # Global variable to track the FFmpeg process
    main()
