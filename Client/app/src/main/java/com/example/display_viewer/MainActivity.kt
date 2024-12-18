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
import java.io.InputStream
import java.net.Socket

class MainActivity : AppCompatActivity() {

    private lateinit var surfaceView: SurfaceView
    private lateinit var surfaceHolder: SurfaceHolder
    private lateinit var connectionButton: Button
    private var isConnected = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE;
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
                //DomekL 192.168.72.26
                //TomTom 172.20.10.3
                val socket = Socket("172.20.10.3", 5050)
                val inputStream: InputStream = socket.getInputStream()

                runOnUiThread {
                    showToast("Connected!")
                    isConnected = true
                    connectionButton.visibility = Button.GONE
                }

                while (true) {
                    // Read image size from the server
                    val sizeBuffer = ByteArray(4)
                    if (inputStream.read(sizeBuffer) == -1) break
                    val imageSize = java.nio.ByteBuffer.wrap(sizeBuffer).int

                    // Read image data from the server
                    val imageBuffer = ByteArray(imageSize)
                    var bytesRead = 0
                    while (bytesRead < imageSize) {
                        val read = inputStream.read(imageBuffer, bytesRead, imageSize - bytesRead)
                        if (read == -1) break
                        bytesRead += read
                    }

                    // Decode the image data into a Bitmap
                    val bitmap = BitmapFactory.decodeByteArray(imageBuffer, 0, imageSize)

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
