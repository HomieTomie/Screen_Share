package com.example.display_viewer

<<<<<<< HEAD
import android.os.Bundle
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity
import com.google.android.exoplayer2.ExoPlayer
import com.google.android.exoplayer2.MediaItem
import com.google.android.exoplayer2.ui.PlayerView

class MainActivity : AppCompatActivity() {
    private var player: ExoPlayer? = null
    private var playerView: PlayerView? = null
=======
import android.media.MediaPlayer
import android.net.Uri
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.Button
import android.widget.Toast
import android.widget.VideoView
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    private var videoView: VideoView? = null
>>>>>>> b5d949e6eabfaf80721e2608f90cd5fb06afe0eb
    private var connectButton: Button? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.layout)

<<<<<<< HEAD
        playerView = findViewById(R.id.playerView) // Ensure layout has PlayerView
        connectButton = findViewById(R.id.connectButton) // Button for starting the connection

        // Set up button click listener
        connectButton?.setOnClickListener {
            initializePlayer()
        }
    }

    private fun initializePlayer() {
        val serverIp = "172.20.10.3"
        val serverPort = 5005
        val rtpUrl = "rtp://$serverIp:$serverPort"

        // Initialize ExoPlayer
        player = ExoPlayer.Builder(this).build()
        playerView?.player = player

        // Add media item and prepare player
        val mediaItem = MediaItem.fromUri(rtpUrl)
        player?.setMediaItem(mediaItem)
        player?.prepare()
        player?.playWhenReady = true
    }

    override fun onStop() {
        super.onStop()
        // Release player resources
        player?.release()
        player = null
    }
}
=======
        // Link UI components from the layout
        videoView = findViewById(R.id.videoView)
        connectButton = findViewById(R.id.connectButton)

        // Set up the Connect button click listener
        if (connectButton != null) {
            connectButton!!.setOnClickListener { v: View? -> startStreaming() }
        } else {
            Toast.makeText(this, "Error: Connect button not found.", Toast.LENGTH_SHORT).show()
        }
    }

    private fun startStreaming() {
        // Replace with your server's IP and port
        val serverIp = "172.20.10.8" // Server IP
        val serverPort = 5005 // Server port

        val rtpUrl = "rtp://$serverIp:$serverPort"

        try {
            val uri = Uri.parse(rtpUrl)
            videoView!!.setVideoURI(uri)
            videoView!!.setOnPreparedListener { mediaPlayer: MediaPlayer? ->
                Toast.makeText(this, "Connected to stream", Toast.LENGTH_SHORT).show()
                videoView!!.start()
            }
            videoView!!.setOnErrorListener { mediaPlayer: MediaPlayer?, what: Int, extra: Int ->
                Toast.makeText(
                    this,
                    "Error: Unable to play the stream",
                    Toast.LENGTH_LONG
                ).show()
                Log.e(
                    "VideoView",
                    "Error playing stream. What: $what, Extra: $extra"
                )
                true
            }
            videoView!!.requestFocus()
            Toast.makeText(this, "Connecting to stream...", Toast.LENGTH_SHORT).show()
        } catch (e: Exception) {
            Toast.makeText(this, "Error starting stream: " + e.message, Toast.LENGTH_LONG).show()
            Log.e("VideoView", "Exception: " + e.message, e)
        }
    }
}
>>>>>>> b5d949e6eabfaf80721e2608f90cd5fb06afe0eb
