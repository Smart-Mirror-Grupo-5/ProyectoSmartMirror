import speech_recognition as sr
import pyaudio
import wave
import os
import pyttsx3


class Transcribir:
    def __init__(self, formato: pyaudio, canales: int, tasa_muestreo: int, tamanio: int, tamanio_bufer: int, duracion_grabacion: int, ruta_archivo: str):
        self.formato = formato
        self.canales = canales
        self.tasa_muestreo = tasa_muestreo
        self.tamanio = tamanio
        self.tamanio_bufer = tamanio_bufer
        self.duracion_grabacion = duracion_grabacion
        self.ruta_archivo = ruta_archivo


    def grabacion_de_audio(self):
        #si existe archivo de audio, borrarlo
        if os.path.exists('static/audio/audio_grabacion.wav'):
            os.remove('static/audio/audio_grabacion.wav')
        try:
            audio = pyaudio.PyAudio()
            stream = audio.open(format=self.formato, channels=self.canales,
                                rate=self.tasa_muestreo, input=True, frames_per_buffer=self.tamanio_bufer)
            print("Grabando...")
            frames = []

            for i in range(0, int(self.tasa_muestreo / self.tamanio_bufer * self.duracion_grabacion)):
                data = stream.read(self.tamanio_bufer)
                frames.append(data)

            print("Grabacion finalizada.")

            stream.stop_stream()
            stream.close()
            audio.terminate()

            #! Guardar el archivo de audio

            wf = wave.open(self.ruta_archivo, 'wb')
            wf.setnchannels(self.canales)
            wf.setsampwidth(audio.get_sample_size(self.formato))
            wf.setframerate(self.tasa_muestreo)
            wf.writeframes(b''.join(frames))
            wf.close()

            resultado = self.transcribir_audio(self.ruta_archivo)

            return resultado

        except Exception as exception:
            raise NameError(f"Error al grabar el audio: {exception}")


    def transcribir_audio(self, ruta_audio):
        try:
            r = sr.Recognizer()
            audio_file = sr.AudioFile(ruta_audio)

            with audio_file as source:
                audio = r.record(source)

            texto = r.recognize_google(audio, language='es-ES')

            return texto

        except Exception as exception:
            raise NameError(f"Error al transcribir el audio: {exception}")

formato = pyaudio.paInt16
canales = 1
tasa_muestreo = 44100
tamanio = 1024
tamanio_bufer = 512
duracion_grabacion = 5
ruta_archivo = 'static/audio/audio_grabacion.wav'

transcribir = Transcribir(formato, canales, tasa_muestreo,
                          tamanio, tamanio_bufer, duracion_grabacion, ruta_archivo)

recogida_audio = transcribir.grabacion_de_audio()
#guardar el texto en conversacion.txt
f = open('static/audio/conversacion.txt', 'w')
#guardar el texto
f.write(str(recogida_audio))
#cerrar el archivo
f.close()

texto = open('static/audio/conversacion.txt', 'r')
conversacion = texto.readlines()

engine = pyttsx3.init()

# Configurar la velocidad (ajustar según sea necesario)
engine.setProperty('rate', 150)  # Puedes ajustar el valor, 150 es un ejemplo

for i in conversacion:
    engine.say(i)
    engine.runAndWait()

texto.close()