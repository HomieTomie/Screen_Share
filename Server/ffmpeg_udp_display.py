import subprocess

def start_stream():
    command = [
        'ffmpeg',
        '-f', 'gdigrab',        # Input format (desktop capture)
        '-framerate', '30',     # Frame rate
        '-i', 'desktop',        # Capture only the LeapMotion window
        '-probesize', '32M',      # Increase probesize to improve stream analysis
        '-c:v', 'libx264',      # Video codec (H.264)
        '-preset', 'ultrafast', # Fast encoding preset
        '-tune', 'zerolatency', # Low latency
        '-b:v', '1000k',        # Video bitrate
        '-f', 'mpegts',         # Set format to RTSP for streaming
        'udp://127.0.0.1:1234',  # Use UDP instead of RTSP
        #'-loglevel', 'debug'    # Enable debug level logging
    ]
    
    try:
        print("Starting FFmpeg stream...")
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    except KeyboardInterrupt:
        print("\nStream interrupted by user")

if __name__ == "__main__":
    print("Starting screen capture stream...")
    start_stream()
