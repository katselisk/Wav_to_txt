import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from time import sleep
import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

kimeno = ""
filename = ""


def fileDialog():
    global filename
    filename = filedialog.askopenfilename(initialdir="/", title="Select A Audio files", filetype=(("Audio files", "*.wav"), ("all files", "*.*")))
    

def track_to_text(sound):
    r = sr.Recognizer()

    with sr.AudioFile(sound) as source:
        r.adjust_for_ambient_noise(source)
        
        audio = r.listen(source)

    try:
        return r.recognize_google(audio)

  
    except Exception:
        return " * "
        pass


def vres_ta_kona(sound, silence_threshold=-50.0, chunk_size=10):
    
    trim_ms = 80000 # ms
    

    assert chunk_size > 0 # to avoid infinite loop

    while sound[trim_ms:trim_ms+chunk_size].dBFS > silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms


def main():
    root= Tk()
    root.minsize(350, 100)
    root.title("-- katselis kostas --")
    root.button = ttk.Button( text="Open A File", command=fileDialog).pack()
    label = ttk.Label( text="Διάλεξε το αρχείο ήχου σε μορφή wav και πατά το start ").pack()
    root.button2 = ttk.Button( text="start", command = root.destroy).pack()
    root.mainloop()
    
    path = filename
    os.system("cls")

    sound = AudioSegment.from_file(path, format="wav")
    kimeno = ""
    i = 0
    while len(sound) > 60000:
        i += 1
        end = len(sound)
        komati = vres_ta_kona(sound)

        track = sound[0:komati]
        name = f"trak_{i}.wav"
        track.export(name, format="wav")

        sound = sound[komati:end]
        sleep(1)

        print(f"\n###\nΞεκινάω την ακρόαση στο {i}o κομμάτι ")
        txt = track_to_text(name)
        os.system("cls")
        print(txt)
        save_to = f"{path} .txt"

        if i == 1:
            with open(save_to, "w", encoding='utf-8') as f :
                f.write(txt)
        else :
            with open(save_to, "r", encoding='utf-8') as f :
                Tab = (f.read())
                Tab += "\n" + txt
            with open(save_to, "w", encoding='utf-8') as f :
                f.write(Tab)


        os.remove(name)

    print(f"Το αρχείο ήχου σώθηκε ως κείμενο στον παρακάτω σύνδεσμο \n {save_to}")
        
   


if __name__ == "__main__":
    main()

    

