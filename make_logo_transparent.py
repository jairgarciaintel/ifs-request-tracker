#!/usr/bin/env python3
"""
Recorta el espacio en blanco del logo inline de Intel Foundry y hace el fondo
transparente, dejando solo las letras. Salida: foundry-inline-black-trim.png

Uso: python3 make_logo_transparent.py
"""
from PIL import Image
import os

SRC = "foundry logos/foundry-product-logos-inline-black.jpg"
OUT = "foundry-inline-black-trim.png"

# Umbral: pixeles mas claros que esto se consideran "fondo" (blanco) -> transparentes
WHITE_THRESHOLD = 235

def main():
    base = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(base, SRC)
    out = os.path.join(base, OUT)

    img = Image.open(src).convert("RGBA")
    px = img.load()
    w, h = img.size

    # 1) Hacer transparente todo lo que sea ~blanco
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if r >= WHITE_THRESHOLD and g >= WHITE_THRESHOLD and b >= WHITE_THRESHOLD:
                px[x, y] = (r, g, b, 0)  # transparente

    # 2) Recortar al bounding box de lo que quedo visible (las letras)
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)

    # 3) Pequeno padding uniforme para que no quede pegado al borde
    pad = 12
    padded = Image.new("RGBA", (img.width + pad * 2, img.height + pad * 2), (0, 0, 0, 0))
    padded.paste(img, (pad, pad), img)

    padded.save(out, "PNG")
    print(f"OK -> {out}  ({padded.width}x{padded.height})")

if __name__ == "__main__":
    main()
