import subprocess

def start_stream():
    command = [
        'ffmpeg',
        '-f', 'gdigrab',  # Input format (desktop capture)
        '-framerate', '15',  # Lower frame rate (15 fps to reduce load and minimize delay)
        '-i', 'title=LeapMotion',  # Capture the entire desktop (use 'title=LeapMotion' for specific window)
        '-c:v', 'libx264',  # Video codec (H.264)
        '-preset', 'ultrafast',  # Ultra-fast encoding preset for minimal latency
        '-tune', 'zerolatency',  # Tune for zero latency (important for real-time streaming)
        '-x264opts', 'keyint=15:min-keyint=15:no-scenecut',  # Frequent keyframes (15 frame interval)
        '-b:v', '500k',  # Low bitrate (500k) to minimize data usage and reduce latency
        '-s', '800x480',  # Lower resolution (800x480) to reduce processing load
        '-max_delay', '0',  # No buffering, instant frame output
        '-flush_packets', '1',  # Flush packets immediately after encoding
        '-f', 'rtp',  # Use mpegts as the container for RTP stream
        'rtp://192.168.72.26:1234',  # Stream over UDP to localhost on port 1234
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
