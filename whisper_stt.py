import whisper
import numpy as np

model = whisper.load_model("base")

result = model.transcribe("audio.mp3")
print(result["text"])

