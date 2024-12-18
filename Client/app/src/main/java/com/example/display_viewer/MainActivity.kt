package com.example.display_viewer

import android.os.Bundle
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity
import com.google.android.exoplayer2.ExoPlayer
import com.google.android.exoplayer2.MediaItem
import com.google.android.exoplayer2.ui.PlayerView

class MainActivity : AppCompatActivity() {
    private var player: ExoPlayer? = null
    private var playerView: PlayerView? = null
    private var connectButton: Button? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.layout)

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
