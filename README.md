Great! Below is a fully detailed **README.md** file for your GitHub project titled `Dancing-Leds-with-ESP32`. It explains the concept, hardware setup, code (Python + ESP32), and how everything works — **line-by-line** and **conceptually**, so that any visitor (or future you) can understand and replicate it.

---

## 📂 `README.md` — Dancing LEDs with ESP32 (Music Reactive)

````markdown
# 🎵 Dancing LEDs with ESP32 (Music Reactive)

This project syncs LEDs connected to an ESP32 with music playback, making them "dance" in real time based on the volume level of a WAV audio file. The audio is analyzed using Python, and the LED brightness levels are transmitted to the ESP32 via serial communication.

---

## 🛠️ Components Used

- ESP32 Development Board
- 5x LEDs
- 220Ω resistors (1 per LED)
- Breadboard + Jumper wires
- USB cable (for serial communication)
- Computer with:
  - Python 3.x
  - Arduino IDE

---

## ⚙️ Circuit Diagram

| ESP32 Pin | LED Color (example) | Purpose       |
|-----------|---------------------|---------------|
| D15       | Red                 | LED 1         |
| D5        | Green               | LED 2         |
| D18       | Blue                | LED 3         |
| D22       | Yellow              | LED 4         |
| D23       | White               | LED 5         |

All LEDs are connected with a **220Ω resistor** in series to GND.

---

## 🧠 How It Works

1. **Python** plays and analyzes a `.wav` audio file.
2. It computes the RMS (volume) for each chunk.
3. Maps volume to levels from 0–5.
4. Sends the level over **serial** to ESP32.
5. **ESP32** reads the level and lights up that many LEDs.

---

## 🐍 Python Code: `hello.py`

```python
import numpy as np
import wave
import serial
import time
````

* `numpy`: for numeric calculations (RMS)
* `wave`: for reading `.wav` files
* `serial`: to communicate with ESP32
* `time`: to control timing (delay)

---

```python
# Serial configuration
com_port = 'COM5'  # Change this to your ESP32's COM port
baud_rate = 115200
wav_file = "music.wav"  # Must be a 16-bit mono/stereo WAV file
```

---

```python
# Open serial connection
ser = serial.Serial(com_port, baud_rate)
print(f"[OK] Connected to {com_port}")
time.sleep(2)  # Wait for ESP32 to reset
```

* Initializes serial connection
* ESP32 resets on connection → we wait 2s

---

```python
# Load WAV file
wf = wave.open(wav_file, 'rb')
frame_rate = wf.getframerate()
chunk_size = int(frame_rate * 0.05)  # 50ms audio chunks
```

* Loads `.wav` audio
* Reads audio in chunks of 50ms

---

```python
print("[START] LED sync playback...")
while True:
    data = wf.readframes(chunk_size)
    if len(data) == 0:
        break
```

* Starts reading audio chunks
* Breaks when the file ends

---

```python
    audio_data = np.frombuffer(data, dtype=np.int16)
    if wf.getnchannels() == 2:
        audio_data = audio_data[::2]  # Take left channel
```

* Converts raw bytes to `int16` samples
* If stereo, drops the right channel

---

```python
    rms = np.sqrt(np.mean(np.square(audio_data.astype(np.float32))))
    level = min(5, int(rms / 2000))  # Map volume to 0–5
```

* Computes RMS (volume)
* Converts it to 0–5 range for LED levels

---

```python
    print(f"Level: {level}")
    ser.write(f"{level}\n".encode())  # Send to ESP32
    time.sleep(0.05)
```

* Sends brightness level to ESP32
* Waits 50ms before sending next level

---

```python
wf.close()
print("[DONE] Playback finished.")
```

* Closes the audio file once done

---

## 🤖 Arduino Code (ESP32): `esp32_led_dance.ino`

```cpp
const int ledPins[] = {15, 5, 18, 22, 23};
const int numLeds = sizeof(ledPins) / sizeof(ledPins[0]);
```

* Stores the LED pins
* `numLeds = 5`

---

```cpp
void setup() {
  Serial.begin(115200);
  Serial.println("ESP32 Ready");

  for (int i = 0; i < numLeds; i++) {
    pinMode(ledPins[i], OUTPUT);
  }
}
```

* Starts Serial
* Initializes each LED as OUTPUT

---

```cpp
void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    int level = input.toInt();
    level = constrain(level, 0, numLeds);

    for (int i = 0; i < numLeds; i++) {
      digitalWrite(ledPins[i], i < level ? HIGH : LOW);
    }
  }
}
```

* Waits for serial input
* Converts string to integer
* Lights up `level` number of LEDs

---

## 📷 Screenshots / Video

Add a demo GIF or YouTube link here showing the LEDs dancing to music.

---

## 🔧 Troubleshooting

| Problem                | Solution                                                     |
| ---------------------- | ------------------------------------------------------------ |
| Serial error           | Make sure no other app (like Arduino Serial Monitor) is open |
| No LED movement        | Check your WAV file format (16-bit PCM mono or stereo)       |
| All LEDs always on/off | Tweak the `rms / 2000` scale → try 1000 or 500               |
| Wrong COM port         | Check in Device Manager or Arduino IDE                       |

---

## 🧪 Test WAV File

You can convert your MP3 to WAV using Audacity or VLC:

* Format: 16-bit PCM
* Channels: Mono or Stereo
* Sample rate: 44100 Hz

---

## 🙏 Credits

* Made with ❤️ by Upangshu Basak
* Python audio analysis inspired by basic DSP methods
* Powered by ESP32 and serial communication

---

## 📄 License

MIT License – feel free to use, modify, and share!

```
