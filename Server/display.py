import subprocess

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
    ]

    try:
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
