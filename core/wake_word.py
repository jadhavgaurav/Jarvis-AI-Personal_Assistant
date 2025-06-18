import pvporcupine
import pyaudio
import struct
import os
from dotenv import load_dotenv
load_dotenv()

ACCESS_KEY = os.getenv("PICOPORCUPINE_ACCESS_KEY")


def listen_for_wake_word(keyword="jarvis"):
    porcupine = pvporcupine.create(access_key=ACCESS_KEY, keywords=[keyword])
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16,
                     channels=1,
                     rate=porcupine.sample_rate,
                     input=True,
                     frames_per_buffer=porcupine.frame_length)

    print("[🎤] Listening for wake word...")
    while True:
        pcm = stream.read(porcupine.frame_length)
        pcm_unpacked = struct.unpack_from("h" * porcupine.frame_length, pcm)
        result = porcupine.process(pcm_unpacked)
        if result >= 0:
            print("[✅] Wake word detected.")
            break

    stream.stop_stream()
    stream.close()
    porcupine.delete()
    pa.terminate()
