import numpy as np
import wave
import serial
import time

# === SETTINGS ===
com_port = 'COM3'  # ✅ CHANGE this to your ESP32 COM port
baud_rate = 115200
wav_file = "Baby Girl.wav"  # Must be 16-bit PCM WAV

# === OPEN SERIAL ===
try:
    ser = serial.Serial(com_port, baud_rate)
    print(f"[OK] Connected to {com_port}")
    time.sleep(2)
except Exception as e:
    print("[ERROR] Serial connection failed:", e)
    exit()

# === OPEN AUDIO ===
try:
    wf = wave.open(wav_file, 'rb')
    print(f"[OK] Opened WAV: {wav_file}")
except Exception as e:
    print("[ERROR] Failed to load WAV file:", e)
    exit()

frame_rate = wf.getframerate()
chunk_size = int(frame_rate * 0.05)  # 50ms

print("[START] LED sync playback...")

while True:
    data = wf.readframes(chunk_size)
    if len(data) == 0:
        break

    # Process audio safely
    try:
        audio_data = np.frombuffer(data, dtype=np.int16)
        if wf.getnchannels() == 2:
            audio_data = audio_data[::2]

        if len(audio_data) == 0 or np.all(audio_data == 0):
            level = 0
        else:
            rms = np.sqrt(np.mean(np.square(audio_data.astype(np.float32))))
            level = min(5, int(rms / 2000))  # Tweak divisor if needed

        # Debug print
        print(f"Level: {level}")

        # Send to ESP32
        ser.write(f"{level}\n".encode())

        time.sleep(0.05)

    except Exception as e:
        print("[ERROR] Processing chunk:", e)

wf.close()
print("[DONE] Playback finished.")
