#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 14:46:32 2024

@author: felipe
"""
#UNA MUESTRA DE CADA AUDIO

import os
import random
from pydub import AudioSegment

# Define la ruta de tu carpeta con los audios
carpeta_audios = '/home/felipe/Documents/LSD/horneros/protocolos/Protocolos prueba N2/audios para armar protocolo'  # Cambia esto por la ruta correcta


# Cargar los nombres de los archivos de audio
audios = [os.path.join(carpeta_audios, f) for f in os.listdir(carpeta_audios) if f.endswith(('.wav', '.mp3'))]

# Configura el número de repeticiones por audio y el intervalo de silencio (3.5 minutos en milisegundos)
repeticiones_por_audio = 6  # Número de veces que cada audio debe aparecer
intervalo_silencio_min = 5  # Intervalo de silencio en minutos
intervalo_silencio = AudioSegment.silent(duration=intervalo_silencio_min * 60 * 1000)  # Convertir a milisegundos

# Crea una lista balanceada de audios
audios_balanceados = audios * repeticiones_por_audio  # Cada audio se repite n veces

# Barajar la lista de audios balanceados
random.shuffle(audios_balanceados)

# Secuencia de audio para exportar y lista para el orden
secuencia_final = AudioSegment.empty()
orden_audios = []  # Lista para almacenar el orden de los audios y su tiempo de inicio
tiempo_actual = 0  # Tiempo actual en segundos

for audio_path in audios_balanceados:
    audio = AudioSegment.from_file(audio_path)
    secuencia_final += audio + intervalo_silencio
    orden_audios.append((os.path.basename(audio_path), tiempo_actual))  # Agrega nombre del archivo y tiempo de inicio
    tiempo_actual += (len(audio) / 1000) + (intervalo_silencio.duration_seconds)  # Actualiza el tiempo actual


# Cambia esta ruta a la carpeta donde quieras guardar los archivos de salida
ruta_salida = '/home/felipe/Documents/LSD/horneros/protocolos/Protocolos prueba N2'

# Agregar la ruta a los nombres de archivo
nombre_salida_audio = os.path.join(ruta_salida, f"audio_balanceado_{intervalo_silencio_min}min_{repeticiones_por_audio}repeticiones.wav")
nombre_salida_txt = os.path.join(ruta_salida, f"orden_audios_{intervalo_silencio_min}min_{repeticiones_por_audio}repeticiones.txt")

# Exporta el audio combinado
secuencia_final.export(nombre_salida_audio, format="wav")

# Calcula y muestra la duración del archivo final en minutos y segundos
duracion_total_min = secuencia_final.duration_seconds // 60
duracion_total_seg = secuencia_final.duration_seconds % 60

# Exporta la secuencia de audios a un archivo de texto
with open(nombre_salida_txt, "w") as f:
    for audio_name, inicio in orden_audios:
        f.write(f"{audio_name} - inicia en: {inicio:.2f} segundos\n")

# Imprime la duración total del archivo final
print(f"Duración total del archivo: {int(duracion_total_min)} minutos y {int(duracion_total_seg)} segundos")
print(f"Archivo de audio generado: {nombre_salida_audio}")
print(f"Orden de los audios ha sido guardado en: {nombre_salida_txt}")




#%%% MUCHOS AUDIOS RANDOM DE CADA CATEGORIA
import os
import random
from pydub import AudioSegment

# Definir las rutas de las carpetas
carpeta1 = '/home/felipe/Documents/LSD/horneros/protocolos/propios'
carpeta2 = '/home/felipe/Documents/LSD/horneros/protocolos/control'
carpeta3 = '/home/felipe/Documents/LSD/horneros/protocolos/ajenos'


# Cargar los nombres de los archivos de audio
audios_carpeta1 = [os.path.join(carpeta1, f) for f in os.listdir(carpeta1)]
audios_carpeta2 = [os.path.join(carpeta2, f) for f in os.listdir(carpeta2)]
audios_carpeta3 = [os.path.join(carpeta3, f) for f in os.listdir(carpeta3)]

# Configura el número de repeticiones y el intervalo de silencio (en milisegundos)
repeticiones = 5
intervalo_silencio = AudioSegment.silent(duration=8 * 60 * 1000)

# Secuencia de audio para exportar
secuencia_final = AudioSegment.empty()

for _ in range(repeticiones):
    # Selecciona un audio aleatorio de cada carpeta
    audio1 = AudioSegment.from_file(random.choice(audios_carpeta1))
    audio2 = AudioSegment.from_file(random.choice(audios_carpeta2))
    audio3 = AudioSegment.from_file(random.choice(audios_carpeta3))
    
    # Orden aleatorio de los tres audios
    secuencia = [audio1, audio2, audio3]
    random.shuffle(secuencia)
    
    # Combina los audios con intervalos de silencio
    for audio in secuencia:
        secuencia_final += audio + intervalo_silencio

# Exporta el audio combinado
secuencia_final.export("protocolo_experimento.wav", format="wav")

# Calcula y muestra la duración del archivo final en minutos y segundos
duracion_total_min = secuencia_final.duration_seconds // 60
duracion_total_seg = secuencia_final.duration_seconds % 60
print(f"Duración total del archivo: {int(duracion_total_min)} minutos y {int(duracion_total_seg)} segundos")
print("Archivo de audio generado: protocolo_experimento.wav")
