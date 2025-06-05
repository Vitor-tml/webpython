import sounddevice as sd
import soundfile as sf
import numpy as np
import threading
import time

class AudioPlayer:
    def __init__(self, filename):
        self.filename = filename
        self.data, self.samplerate = sf.read(self.filename, dtype='float32')
        self.stream_pointer = 0
        self.volume = 1.0
        self.stop_event = threading.Event()

    def callback(self, outdata, frames, time, status):
        if(status):
            print(status)
        
        chunk = self.data[self.stream_pointer:self.stream_pointer + frames]

        # Se a amostra de audio for menor que o tamanho do bloco, preenche com silêncio
        # Isso significa que o áudio acabou
        if( len(chunk) < frames):
            outdata[:len(chunk)] = chunk * self.volume
            outdata[len(chunk):] = 0
            raise sd.CallbackStop() # Para o stream no final
        else:
            outdata[:] = chunk * self.volume

        self.stream_pointer += frames # Aponta para o próximo pedaço de áudio

    def input_thread(self):
        vol = float(input("Volume (ex: 0.5 para metade, 2 para dobro): "))
        while vol > 0:
            try:
                self.volume = vol
                vol = float(input("\nVolume (ex: 0.5 para metade, 2 para dobro): "))
            except ValueError:
                print("\nPor favor, insira um número válido.")
        self.stop_event.set()

    def audioSizeMS(self):
    #Duração do áudio em milissegundos
        return len(self.data) / self.samplerate * 1000
    
    def playAudio(self):
        with sd.OutputStream(channels=self.data.shape[1],
                             samplerate=self.samplerate,
                             callback=self.callback,
                             blocksize=1024):
            print("Tocando... digite valores para volume durante a execução.")
            # Checka a cada 200 ms se o usuário saiu do programa
            while not self.stop_event.is_set():
                sd.sleep(200)