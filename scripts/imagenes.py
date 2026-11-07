#!/usr/bin/env python3
"""Descarga las imágenes de la antigua web de Wix (y la miniatura del vídeo y el programa en PDF) y las guarda
en WebP optimizado dentro de img/. Lo ejecuta la acción de GitHub «Publicar la web».

Solo descarga lo que falta: las fotos de compañías y espectáculos salen de data/companias.json
(campo imagen_wix) y se guardan en img/companias/<id>-400|800.webp e img/espectaculos/<compañía>--<espectáculo>-…

    pip install pillow && python3 scripts/imagenes.py
"""
import io
import json
import pathlib
import urllib.request

from PIL import Image, ImageOps

RAIZ = pathlib.Path(__file__).resolve().parent.parent
W = "https://static.wixstatic.com/media/0171ea_{}"

# destino (sin sufijo), URL, anchos
FOTOS = [
    ("img/fotos/puja-asteroide", W.format("acf49b51f5454ef9a2509f3c433d93b1~mv2.jpg"), [900, 1600, 2400]),
    ("img/fotos/festival", W.format("eeabc9d3a7fe4e77a7af9fbcb08ed3ba~mv2.jpg"), [500]),
    ("img/fotos/valla-2026", W.format("69ace100f20241a882dda2aa4cff72bc~mv2.jpg"), [840]),
    ("img/fotos/sacude", W.format("3d39b332e92644c5866fa9ac3cc57c6a~mv2.jpg"), [1200, 2400]),
    ("img/fotos/video-promo", "https://i.ytimg.com/vi/5TzG4Ktgveo/maxresdefault.jpg", [800, 1280]),
]

# destino, URL, alto final
LOGOS = [
    ("img/logos/enpie-color.webp", W.format("b17c8fc5b66449598791e2dcb3c3a5d7~mv2.png"), 200),
    ("img/logos/enpie-blanco.webp", W.format("d7645e6c65e34c9fba3ed28c7747ef41~mv2.png"), 240),
    ("img/logos/enpie-icono.webp", W.format("5576f6edfb5c4a81b7e3b17cefdc54e1~mv2.png"), 160),
    ("img/logos/ayuntamiento-teror.webp", W.format("b8e0727c9c154996b41c1665315114a5~mv2.png"), 160),
    ("img/logos/cabildo-fundacion-nanino-diaz.webp", W.format("3fe652ba4a414e9cb32d62f7780679a7~mv2.png"), 140),
    ("img/logos/islas-canarias.webp", W.format("6f9ab0c4642446cebc06bcf9ba08bfde~mv2.png"), 140),
    ("img/logos/gobierno-de-canarias.webp", W.format("b461b0b4bd38444da4b1f2807a7f0dd2~mv2.png"), 140),
    ("img/logos/aguas-de-teror.webp", W.format("3f3e2bbc571241f4a5fb62ca9c424f0a~mv2.jpg"), 140),
    ("img/logos/ahembo.webp", W.format("29bf72a0152140afa2a28c0b2558ace9~mv2.png"), 60),
    ("img/logos/7up.webp", W.format("bade5e9378a64e30bc5875b73dc41462~mv2.png"), 140),
    ("img/logos/clipper.webp", W.format("192ff0ef495948688f22e9200c9a8b64~mv2.png"), 140),
    ("img/logos/disaterura.webp", W.format("c37fe5c6f0964483aa486d9919be11b4~mv2.png"), 140),
    ("img/logos/estrella-galicia.webp", W.format("1e57db6ac77e4f85a7ce9882d91eff10~mv2.png"), 140),
]

PDF = ("programa/programa-en-pie-teror-2026.pdf",
       "https://www.festivalenpieteror.com/_files/ugd/0171ea_48b70eb8a4d8425b90155466d366e3f1.pdf")


def bajar_bytes(url):
    req = urllib.request.Request(url, headers={"User-Agent": "festivalenpieteror-web"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read()


def bajar(url):
    im = Image.open(io.BytesIO(bajar_bytes(url)))
    im.load()
    return ImageOps.exif_transpose(im)


def guardar(im, destino, calidad=80):
    p = RAIZ / destino
    p.parent.mkdir(parents=True, exist_ok=True)
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGBA" if ("A" in im.getbands() or im.mode == "P") else "RGB")
    im.save(p, "WEBP", quality=calidad, method=6)
    print(f"  {destino}  {im.size[0]}x{im.size[1]}  {p.stat().st_size // 1024} KB")


def desde_datos():
    datos = RAIZ / "data/companias.json"
    if not datos.exists():
        return
    pendientes = []
    for c in json.loads(datos.read_text(encoding="utf-8")):
        if c.get("imagen_wix"):
            pendientes.append((f"img/companias/{c['id']}", c["imagen_wix"]))
        for e in c.get("espectaculos", []):
            if e.get("imagen_wix") and e["imagen_wix"] != c.get("imagen_wix"):
                pendientes.append((f"img/espectaculos/{c['id']}--{e['id']}", e["imagen_wix"]))
    for destino, wix in pendientes:
        if (RAIZ / f"{destino}-400.webp").exists():
            continue
        print(destino)
        try:
            im = bajar(f"https://static.wixstatic.com/media/{wix}").convert("RGB")
        except Exception as e:
            print("  ERROR", e)
            continue
        for w in (400, 800):
            c = im.copy()
            if c.width > w:
                c = c.resize((w, round(c.height * w / c.width)), Image.LANCZOS)
            guardar(c, f"{destino}-{w}.webp")


def main():
    desde_datos()
    for destino, url, anchos in FOTOS:
        if (RAIZ / f"{destino}-{anchos[0]}.webp").exists():
            continue
        print(destino)
        try:
            im = bajar(url).convert("RGB")
        except Exception as e:  # una imagen que falle no para las demás
            print("  ERROR", e)
            continue
        for w in anchos:
            c = im.copy()
            if c.width > w:
                c = c.resize((w, round(c.height * w / c.width)), Image.LANCZOS)
            guardar(c, f"{destino}-{w}.webp")
    for destino, url, alto in LOGOS:
        if (RAIZ / destino).exists():
            continue
        print(destino)
        try:
            im = bajar(url)
        except Exception as e:
            print("  ERROR", e)
            continue
        if im.height > alto:
            im = im.resize((round(im.width * alto / im.height), alto), Image.LANCZOS)
        guardar(im, destino, calidad=90)
    if (RAIZ / "img/og-en-pie-teror.jpg").exists() and (RAIZ / PDF[0]).exists():
        return
    try:
        im = bajar(W.format("acf49b51f5454ef9a2509f3c433d93b1~mv2.jpg")).convert("RGB")
        ImageOps.fit(im, (1200, 630), Image.LANCZOS).save(RAIZ / "img/og-en-pie-teror.jpg", "JPEG", quality=84, optimize=True, progressive=True)
        print("  img/og-en-pie-teror.jpg")
    except Exception as e:
        print("  ERROR og", e)
    try:
        p = RAIZ / PDF[0]
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(bajar_bytes(PDF[1]))
        print(f"  {PDF[0]}  {p.stat().st_size // 1024} KB")
    except Exception as e:
        print("  ERROR pdf", e)


if __name__ == "__main__":
    main()
