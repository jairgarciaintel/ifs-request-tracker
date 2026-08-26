#!/usr/bin/env python3
"""
Genera un WAV sintetico tipo "APU / turbina de Airbus arrancando" (spool-up).
Solo usa la libreria estandar (wave, struct, math, random). No graba audio real:
sintetiza un whine de turbina que sube de frecuencia con armonicos + aire.
Salida: apu-sound.wav  (mono, 16-bit, 44.1kHz)
"""
import wave, struct, math, random

SR = 44100          # sample rate
DUR = 3.6           # segundos
N = int(SR * DUR)

def env(i):
    """Envolvente: sube rapido, mantiene, baja al final."""
    t = i / N
    attack = min(t / 0.12, 1.0)          # 0..1 en primeros 12%
    release = min((1.0 - t) / 0.25, 1.0) # baja en el ultimo 25%
    return max(0.0, min(attack, release))

def spool(t):
    """Frecuencia base de la turbina: arranca baja y acelera (spool-up)."""
    # de ~180 Hz a ~1150 Hz con curva tipo aceleracion
    return 180 + (1150 - 180) * (t ** 1.6)

samples = []
phase = 0.0
phase2 = 0.0
phase3 = 0.0
for i in range(N):
    t = i / N
    f = spool(t)
    # tono fundamental + 2 armonicos (whine metalico de turbina)
    phase  += 2 * math.pi * f / SR
    phase2 += 2 * math.pi * (f * 2.02) / SR
    phase3 += 2 * math.pi * (f * 3.01) / SR
    tone = (0.55 * math.sin(phase)
            + 0.28 * math.sin(phase2)
            + 0.16 * math.sin(phase3))
    # "aire" / flujo de la turbina: ruido filtrado que crece con el spool
    air = (random.uniform(-1, 1)) * (0.10 + 0.20 * t)
    # modulacion lenta (variacion de RPM)
    wobble = 1.0 + 0.04 * math.sin(2 * math.pi * 6 * t)
    s = (tone * wobble + air) * env(i) * 0.5
    # clip suave
    s = max(-1.0, min(1.0, s))
    samples.append(int(s * 32767))

with wave.open('apu-sound.wav', 'w') as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(b''.join(struct.pack('<h', s) for s in samples))

print('OK -> apu-sound.wav (%.1fs, %d Hz)' % (DUR, SR))
