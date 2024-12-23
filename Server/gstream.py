import gi
import subprocess

# Import necessary GStreamer libraries
gi.require_version('Gst', '1.0')
from gi.repository import Gst

def start_stream():
    # Initialize GStreamer
    Gst.init(None)
    
    # GStreamer pipeline to capture the screen and stream it via RTP/UDP
    pipeline = (
        'ximagesrc ! video/x-raw,framerate=30/1 ! '
        'x264enc tune=zerolatency bitrate=5000 ! '
        'rtph264pay ! udpsink host=127.0.0.1 port=5000'
    )
    
    # Create and set the GStreamer pipeline
    gst_pipeline = Gst.parse_launch(pipeline)
    
    # Start the GStreamer pipeline
    gst_pipeline.set_state(Gst.State.PLAYING)
    
    print("Streaming started. Press Ctrl+C to stop.")
    
    # Wait until the stream is finished
    try:
        Gst.main()
    except KeyboardInterrupt:
        # Stop the stream gracefully
        gst_pipeline.set_state(Gst.State.NULL)
        print("Stream stopped.")

if __name__ == "__main__":
    start_stream()
