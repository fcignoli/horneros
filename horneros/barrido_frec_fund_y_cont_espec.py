#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 16:37:07 2025

@author: felipe
"""
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.fft import fft, fftfreq
from tqdm import tqdm  # Para la barra de progreso

# Parámetros fijos
gamma = 4.5 * 10**3
f0 = 0.1
t = np.linspace(0, 10, 5000)  # Tiempo más largo para mejor resolución en FFT


# Rango de kappa y beta
#kappa_vals = np.linspace(0.1, 5.0, 25)
#beta_vals = np.linspace(-0.1, 0.5, 25)

kappa_vals = np.linspace(-0.05, .2, 50)
beta_vals = np.linspace(-0.2, 1, 50)

# Matrices para almacenar resultados
freq_map = np.zeros((len(beta_vals), len(kappa_vals)))
spectral_content_map = np.zeros_like(freq_map)

def sistema(z, t, gamma, kappa, beta, f0):
    x, y = z
    dxdt = y
    dydt = -gamma**2 * kappa * x - gamma * x**2 * y + beta * gamma * y + f0
    return [dxdt, dydt]

# Loop con barra de progreso
for i, beta in enumerate(tqdm(beta_vals, desc="Barriendo beta")):
    for j, kappa in enumerate(kappa_vals):
        # Simular el sistema
        z0 = [0.1, 0.0]  # Condiciones iniciales
        sol = odeint(sistema, z0, t, args=(gamma, kappa, beta, f0))
        x = sol[:, 0]
        
        # Calcular FFT
        n = len(t)
        freqs = fftfreq(n, d=t[1]-t[0])[:n//2]
        fft_x = np.abs(fft(x)[:n//2])
        
        # Encontrar picos en el espectro
        peaks, _ = find_peaks(fft_x, height=0.1 * np.max(fft_x))
        if len(peaks) > 0:
            freq_map[i, j] = freqs[peaks[0]]  # Frecuencia fundamental
        else:
            freq_map[i, j] = 0
        
        # Medir contenido espectral (entropía)
        power = fft_x / (np.sum(fft_x) + 1e-10)  # Evitar división por cero
        spectral_entropy = -np.sum(power * np.log2(power + 1e-10))  # +1e-10 para evitar log(0)
        spectral_content_map[i, j] = spectral_entropy

# Graficar (igual que antes)
plt.figure(figsize=(12, 5))

# Mapa 1: Frecuencia fundamental
plt.subplot(1, 2, 1)
plt.imshow(freq_map, extent=[kappa_vals.min(), kappa_vals.max(), beta_vals.min(), beta_vals.max()], 
           origin='lower', aspect='auto', cmap='viridis')
plt.colorbar(label='Frecuencia fundamental (Hz)')
plt.xlabel('$\kappa$')
plt.ylabel('$\\beta$')
plt.title('Frecuencia fundamental')

# Mapa 2: Contenido espectral (entropía)
plt.subplot(1, 2, 2)
plt.imshow(spectral_content_map, extent=[kappa_vals.min(), kappa_vals.max(), beta_vals.min(), beta_vals.max()], 
           origin='lower', aspect='auto', cmap='plasma')
plt.colorbar(label='Entropía espectral')
plt.xlabel('$\kappa$')
plt.ylabel('$\\beta$')
plt.title('Complejidad espectral')

plt.tight_layout()
plt.show()

#%%

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.fft import fft, fftfreq
from tqdm import tqdm
import os
from joblib import Parallel, delayed

# Parámetros fijos
gamma = 4.5 * 10**3
f0 = 6000
t = np.linspace(0, 10, 2500)  # Tiempo más largo para mejor resolución en FFT


# Rango de kappa y beta
#kappa_vals = np.linspace(0.1, 5.0, 25)
#beta_vals = np.linspace(-0.1, 0.5, 25)

kappa_vals = np.linspace(-0.05, .2, 50)
beta_vals = np.linspace(-0.2, 1, 50)

# Inicializar matrices de resultados
freq_map = np.zeros((len(beta_vals), len(kappa_vals)))
spectral_content_map = np.zeros_like(freq_map)

# Función del sistema (igual que antes)
def sistema(z, t, gamma, kappa, beta, f0):
    x, y = z
    dxdt = y
    dydt = -gamma**2 * kappa * x - gamma * x**2 * y + beta * gamma * y + f0
    return [dxdt, dydt]

# Función para simular un único beta (para paralelización)
def simular_beta(i, beta, freq_map, spectral_content_map):
    for j, kappa in enumerate(kappa_vals):
        z0 = [0.1, 0.0]
        sol = odeint(sistema, z0, t, args=(gamma, kappa, beta, f0))
        x = sol[:, 0]
        
        # Calcular FFT y frecuencia fundamental
        n = len(t)
        freqs = fftfreq(n, d=t[1]-t[0])[:n//2]
        fft_x = np.abs(fft(x)[:n//2])
        peaks, _ = find_peaks(fft_x, height=0.1 * np.max(fft_x))
        freq_map[i, j] = freqs[peaks[0]] if len(peaks) > 0 else 0
        
        # Calcular entropía espectral
        power = fft_x / (np.sum(fft_x) + 1e-10)
        spectral_entropy = -np.sum(power * np.log2(power + 1e-10))
        spectral_content_map[i, j] = spectral_entropy
    
    return i, freq_map[i, :], spectral_content_map[i, :]

# Cargar resultados previos si existen
if os.path.exists('freq_map.npy') and os.path.exists('spectral_content_map.npy'):
    freq_map = np.load('freq_map.npy')
    spectral_content_map = np.load('spectral_content_map.npy')
    print("¡Datos previos cargados! Reanudando cálculos...")

# Identificar betas no procesados (para reanudar)
pending_indices = [i for i, beta in enumerate(beta_vals) 
                  if np.all(freq_map[i, :] == 0)]

# Paralelización con joblib
results = Parallel(n_jobs=-1)(  # Usa todos los núcleos disponibles
    delayed(simular_beta)(i, beta_vals[i], freq_map, spectral_content_map)
    for i in pending_indices
)

# Actualizar matrices con resultados
for i, freq_row, spectral_row in results:
    freq_map[i, :] = freq_row
    spectral_content_map[i, :] = spectral_row
    # Guardar progreso después de cada beta
    np.save('freq_map.npy', freq_map)
    np.save('spectral_content_map.npy', spectral_content_map)

# Graficar (igual que antes)
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.imshow(freq_map, extent=[kappa_vals.min(), kappa_vals.max(), beta_vals.min(), beta_vals.max()], 
           origin='lower', aspect='auto', cmap='viridis')
plt.colorbar(label='Frecuencia fundamental (Hz)')
plt.xlabel('$\kappa$')
plt.ylabel('$\\beta$')
plt.title('Frecuencia fundamental')

plt.subplot(1, 2, 2)
plt.imshow(spectral_content_map, extent=[kappa_vals.min(), kappa_vals.max(), beta_vals.min(), beta_vals.max()], 
           origin='lower', aspect='auto', cmap='plasma')
plt.colorbar(label='Entropía espectral')
plt.xlabel('$\kappa$')
plt.ylabel('$\\beta$')
plt.title('Complejidad espectral')

plt.tight_layout()
plt.show()