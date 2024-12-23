from threading import Thread
import mss
import cv2
import numpy as np
import ffmpeg
import subprocess

def stream_display_via_ffmpeg(host="127.0.0.1", port=8080):
    """Stream display using FFmpeg for VLC compatibility."""
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Capture the primary monitor

        # Start FFmpeg subprocess
        ffmpeg_command = (
            ffmpeg
            .input('pipe:0', format='rawvideo', pix_fmt='bgr24', s=f"{monitor['width']}x{monitor['height']}")
            .output(f"http://{host}:{port}", format='mpegts', vcodec='libx264', r=30, pix_fmt='yuv420p', preset='ultrafast', tune='zerolatency')
            .global_args('-loglevel', 'verbose')  # Change to 'error' after debugging
            .compile()
        )
        ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)

        print(f"Streaming display to http://{host}:{port}")
        try:
            while True:
                # Capture the screen
                img = np.array(sct.grab(monitor))[:, :, :3]  # Drop alpha channel
                ffmpeg_process.stdin.write(img.tobytes())
        except KeyboardInterrupt:
            print("Shutting down stream.")
        finally:
            ffmpeg_process.stdin.close()
            ffmpeg_process.wait()

if __name__ == "__main__":
    try:
        stream_display_via_ffmpeg()
    except KeyboardInterrupt:
        print("Server shutting down.")
