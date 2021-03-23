# import libraries 
import speech_recognition as sr 
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence

# this function splits the audio file into chunks and applies speech recognition
def get_large_audio_transcription(path):
    # opens the audio file using pydub library
    sound = AudioSegment.from_wav(path)  
    
    # splits audio sound at silence length to get chunks
    chunks = split_on_silence(sound,
        min_silence_len = 500, # adjust this according to desired silence length
        silence_thresh = sound.dBFS-14, # adjusts this according to desired threshold
        keep_silence  = 500, # adjust this to keep the silence
    )
    
    # creates directory to store the audio chunks
    folderName = "audio-chunks"
    if not os.path.isdir(folderName):
        os.mkdir(folderName)
    wholeText = ""
    
    # processes each chunk 
    for i, audioChunk in enumerate(chunks, start=1):
        # export audio chunk and save it in the output directory.
        chunkFilename = os.path.join(folderName, f"chunk{i}.wav")
        audioChunk.export(chunkFilename, format="wav")
        
        # applies recognition to the chunk
        with sr.AudioFile(chunkFilename) as source:
            audioListened = r.record(source)
            # try converting the chunk to text
            try:
                text = r.recognize_google(audioListened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunkFilename, ":", text)
                wholeText += text
    # returns the text for all chunks detected
    return wholeText
  
# main
def main():
  # creates a speech recognition object to read from an audio file
  recognitionFile = sr.Recognizer()
  # file name
  path = "samples_whatstheweatherlike.wav"
  # prints recognized text
  print("\nFull text from input audio file:", get_large_audio_transcription(path))
    
  # creates a speech recognition object to read from a microphone
  recognitionMicrophone = sr.Recognizer()
    
  # reads source audio from the microphone
  with sr.Microphone() as source:
    audio_data = recognitionMicrophone.record(source, duration=5)
    print("Recognizing...")
    # converts speech to text
    text = recognitionMicrophone.recognize_google(audio_data)
    # prints recognized text
    print(text)

# calls main
main()
