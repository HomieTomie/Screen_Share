import subprocess
import os

def start_stream():
    # Set the environment variable for OpenCV if necessary
    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "protocol_whitelist;file,rtp,udp"

    # Define the FFmpeg command with low-latency settings for real-time streaming
    command = [
        'ffmpeg',
        '-protocol_whitelist', 'file,crypto,data,rtp,udp',  # Ensure all required protocols are allowed
        '-f', 'gdigrab',  # Input format (desktop capture)
        '-framerate', '15',  # Lower frame rate (15 fps to reduce load and minimize delay)
        '-i', 'desktop',  # Capture the entire desktop (use 'title=LeapMotion' for specific window)
        '-c:v', 'libx264',  # Video codec (H.264)
        '-preset', 'ultrafast',  # Ultra-fast encoding preset for minimal latency
        '-tune', 'zerolatency',  # Tune for zero latency (important for real-time streaming)
        '-x264opts', 'keyint=15:min-keyint=15:no-scenecut',  # Frequent keyframes (15 frame interval)
        '-b:v', '500k',  # Low bitrate (500k) to minimize data usage and reduce latency
        '-s', '640x360',  # Lower resolution (640x360) to reduce processing load
        '-max_delay', '0',  # No buffering, instant frame output
        '-flush_packets', '1',  # Flush packets immediately after encoding
        '-f', 'rtp',  # Use mpegts as the container for RTP stream
        'rtp://127.0.0.1:1234',  # Stream over UDP to localhost on port 1234
        #'-sdp_file', 'stream.sdp'  # Optional: You can still use an SDP file if needed
    ]
    
    try:
        print("Starting FFmpeg stream with real-time settings...")
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    except KeyboardInterrupt:
        print("\nStream interrupted by user")

if __name__ == "__main__":
    print("Starting screen capture stream with real-time settings...")
    start_stream()
