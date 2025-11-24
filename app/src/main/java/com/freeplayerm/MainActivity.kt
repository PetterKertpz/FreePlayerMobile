package com.freeplayerm

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.material3.Text
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint // <--- ¡CRÍTICO PARA HILT!
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            // UI Temporal para verificar que funciona
            Text(text = "FreePlayerM - Hilt Running")
        }
    }
}