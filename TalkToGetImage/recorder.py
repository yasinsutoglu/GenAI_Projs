import pyaudio 
import wave # lib for WAV type audio 

# func to be used in multithread
def record(record_active, frames): 
    audio = pyaudio.PyAudio()

   
    stream = audio.open(
        format=pyaudio.paInt16, # 16bits data format
        channels=1,  
        rate=44100, # 44100Hz freqs
        input=True, 
        frames_per_buffer=1024 # stream data frames
    )

    while record_active.is_set(): 
        data = stream.read(1024, exception_on_overflow=False)
        frames.append(data)

    
    stream.stop_stream() # stream stopping
    stream.close() 
    audio.terminate() 

    sound_file = wave.open("voice_prompt.wav", "wb") 
    # below settings similar to audio stream 
    sound_file.setnchannels(1)
    sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    sound_file.setframerate(44100)
    sound_file.writeframes(b''.join(frames)) # writeframes() => sound data parts joined frame by frame in binary and written
    sound_file.close()