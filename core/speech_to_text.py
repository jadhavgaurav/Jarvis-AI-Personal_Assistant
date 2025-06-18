from vosk import Model, KaldiRecognizer
import pyaudio
import json

def transcribe():
    model = Model("models/vosk-model-small-en-us-0.15") 
    recognizer = KaldiRecognizer(model, 16000)
    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16,
                      channels=1,
                      rate=16000,
                      input=True,
                      frames_per_buffer=8000)
    stream.start_stream()

    print("[🗣️] Listening...")
    while True:
        data = stream.read(4000)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "")
            if text:
                print(f"[📥] You said: {text}")
                return text
