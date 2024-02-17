import speech_recognition as sr
import base64
import wave
import io

# file = open("audio.txt",'r')
# base64_audio_string = file.readline()
# Decode the base64 audio file into a binary format
audio_data = base64.b64decode(base64_audio_string)

# Write the decoded data to a temporary WAV file
with io.BytesIO(audio_data) as f:
    wav_file = wave.open(f, 'rb')
   
# Create a recognizer object
r = sr.Recognizer()

# Use the recognizer object to read the audio data from the WAV file
with sr.AudioFile(wav_file) as source:
    audio_data = r.record(source)

# Use the Google Web Speech API to transcribe the speech in the audio data
try:
    transcription = r.recognize_google(audio_data, language='hi-IN') # Set the language code for the target language here
except sr.UnknownValueError:
    print("Could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

if transcription:
    print("Transcription: " + transcription)
    # Analyze the transcription to determine the language
    if 'हिंदी' in transcription.lower():
        print("The language is Hindi")
    elif 'বাংলা' in transcription.lower():
        print("The language is Bangla")
    # Add more conditions for other languages as needed