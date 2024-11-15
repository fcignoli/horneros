#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 17:25:11 2024

@author: felipe
"""

from pydub import AudioSegment

# Define la ruta de los archivos de audio
ruta_canto_propio = '/home/felipe/Documents/LSD/horneros/protocolos/Protocolos prueba N2/audios para armar protocolo/BOS.wav'
ruta_otros_horneros = '/home/felipe/Documents/LSD/horneros/protocolos/Protocolos prueba N2/audios para armar protocolo/CON.wav'
ruta_paloma = '/home/felipe/Documents/LSD/horneros/protocolos/Protocolos prueba N2/audios para armar protocolo/HET.wav'

# Cargar los audios
canto_propio = AudioSegment.from_file(ruta_canto_propio)
otros_horneros = AudioSegment.from_file(ruta_otros_horneros)
paloma = AudioSegment.from_file(ruta_paloma)

# Establece el nivel objetivo de RMS en dBFS (p. ej., -20.0 dBFS es un nivel típico)
nivel_objetivo_dbfs = -20.0

# Función para normalizar el volumen de un audio
def normalizar_volumen(audio, nivel_objetivo):
    diferencia_db = nivel_objetivo - audio.dBFS
    return audio.apply_gain(diferencia_db)

# Normalizar cada audio al nivel objetivo
canto_propio_normalizado = normalizar_volumen(canto_propio, nivel_objetivo_dbfs)
otros_horneros_normalizado = normalizar_volumen(otros_horneros, nivel_objetivo_dbfs)
paloma_normalizado = normalizar_volumen(paloma, nivel_objetivo_dbfs)

# Exportar los audios normalizados
canto_propio_normalizado.export("BOS.wav", format="wav")
otros_horneros_normalizado.export("CON.wav", format="wav")
paloma_normalizado.export("HET.wav", format="wav")

print("Audios normalizados y guardados como archivos independientes.")
