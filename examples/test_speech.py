import speech_recognition as sr
import os

# ------ USING THE GOOGLE API --------------------------------

# # create a Recognizer object
# r = sr.Recognizer()

# # use the default microphone as the audio source
# with sr.Microphone() as source:
#     print("Speak now...")
#     # listen for speech and store it as audio data
#     audio_data = r.record(source, duration=5)

#     # recognize speech using Google Speech Recognition
#     text = r.recognize_google(audio_data)

#     # print the recognized text
#     print(f"You said: {text}")



# ------ USING THE SPHINX MODEL --------------------------------

# create a Recognizer object
r = sr.Recognizer()

# set the engine to use PocketSphinx
r.energy_threshold = 4000  # adjust this value to suit your microphone
r.dynamic_energy_threshold = True  # automatically adjust the threshold based on ambient noise

# use the default microphone as the audio source
with sr.Microphone() as source:
    print("Speak now...")
    # listen for speech and store it as audio data
    audio_data = r.record(source, duration=5)

    # recognize speech using PocketSphinx
    text = r.recognize_sphinx(audio_data)

    # print the recognized text
    print(f"You said: {text}")