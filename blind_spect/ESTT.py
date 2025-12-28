import speech_recognition as sr
import sounddevice as sd
import wave
import numpy as np
from googletrans import Translator
translator = Translator()
import pygame
import time
from gtts import gTTS
from mutagen.mp3 import MP3
import time
import telepot
bot1 = telepot.Bot("7767639890:AAHD15_v8H2IC9npSVLLTxueZqvbQG7kS-U")

def Play(text1):
    print(text1)
    myobj = gTTS(text=text1, lang='en-us', tld='com', slow=False)
    myobj.save("voice.mp3")
    print('\n------------Playing--------------\n')
    song = MP3("voice.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load('voice.mp3')
    pygame.mixer.music.play()
    time.sleep(song.info.length)
    pygame.quit()
while True:
    duration = 5
    fs = 44100
    channels=2
    filename="input_audio.wav"

    print("Recording...")
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=channels, dtype=np.int16)
    sd.wait()
    print("Recording complete.")

    # Save the recorded audio to a WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(fs)
        wf.writeframes(audio_data.tobytes())

    # Perform speech recognition
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        recognizer.adjust_for_ambient_noise(source)
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            text = text.lower()
            print("Recognized text:", text)
            if text == 'emergency':
                bot1.sendLocation('5127660117', latitude=13.0378, longitude=77.6190)
                Play('location sent ')
            else:
                Play(text)
                from_lang = 'en'
                to_lang = 'kn'
                text_to_translate = translator.translate(text,src= from_lang,dest= to_lang)
                text1 = text_to_translate.text
                Play(text1)
                to_lang = 'hi'
                text_to_translate = translator.translate(text,src= from_lang,dest= to_lang)
                text1 = text_to_translate.text
                Play(text1)
                to_lang = 'ta'
                text_to_translate = translator.translate(text,src= from_lang,dest= to_lang)
                text1 = text_to_translate.text
                Play(text1)
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
