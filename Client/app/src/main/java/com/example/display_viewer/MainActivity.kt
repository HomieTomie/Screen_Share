package com.example.display_viewer

import android.content.pm.ActivityInfo
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.os.Bundle
import android.view.SurfaceHolder
import android.view.SurfaceView
import android.widget.Button
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import java.net.DatagramPacket
import java.net.DatagramSocket
import java.net.InetAddress

class MainActivity : AppCompatActivity() {

    private lateinit var surfaceView: SurfaceView
    private lateinit var surfaceHolder: SurfaceHolder
    private lateinit var connectionButton: Button
    private var isConnected = false
    private val serverAddress = "192.168.1.100" // IP address of the server
    private val serverPort = 1234 // Port number used in the server-side UDP stream

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE
        setContentView(R.layout.layout)

        // Initialize views
        surfaceView = findViewById(R.id.surfaceView)
        surfaceHolder = surfaceView.holder
        connectionButton = findViewById(R.id.connectionButton)

        // Set button click listener
        connectionButton.setOnClickListener {
            if (!isConnected) {
                showToast("Connecting...")
                startStream()
                supportActionBar?.hide()
            }
        }
    }

    private fun startStream() {
        Thread {
            try {
                val socket = DatagramSocket(serverPort)
                socket.connect(InetAddress.getByName(serverAddress), serverPort)

                runOnUiThread {
                    showToast("Connected!")
                    isConnected = true
                    connectionButton.visibility = Button.GONE
                }

                val buffer = ByteArray(65535) // Buffer to hold the incoming data packets

                while (true) {
                    val packet = DatagramPacket(buffer, buffer.size)
                    socket.receive(packet) // Receive the UDP packet

                    // Assuming we are receiving video frames (H.264 encoded)
                    val imageData = packet.data.copyOf(packet.length)

                    // Decode the image data into a Bitmap
                    val bitmap = BitmapFactory.decodeByteArray(imageData, 0, imageData.size)

                    // Draw the Bitmap on the SurfaceView
                    surfaceHolder.lockCanvas()?.let { canvas ->
                        // Scale the Bitmap to match the SurfaceView dimensions
                        val scaledBitmap = Bitmap.createScaledBitmap(bitmap, canvas.width, canvas.height, true)
                        canvas.drawBitmap(scaledBitmap, 0f, 0f, null)
                        surfaceHolder.unlockCanvasAndPost(canvas)
                    }
                }
            } catch (e: Exception) {
                e.printStackTrace()
                runOnUiThread {
                    showToast("Failed to connect: ${e.message}")
                    isConnected = false
                }
            }
        }.start()
    }

    // Function to show toast messages
    private fun showToast(message: String) {
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show()
    }
}
