#!/usr/bin/env python3
"""Importa la exportación CSV de la colección de Wix «Compañías y Artistas y Horarios» a los datos de la web.

    python3 scripts/importar_wix.py ruta/al/export.csv

Escribe data/companias.json, data/funciones.json, data/espacios.json y data/ediciones.json.
Se usó una vez para traer 2024, 2025 y 2026 desde Wix; a partir de ahí los datos se editan desde el portal
(Programación En Pie) o a mano en esos JSON. Si se vuelve a ejecutar, SOBRESCRIBE los datos.
"""
import csv
import json
import pathlib
import re
import sys
import unicodedata
import urllib.parse
from datetime import datetime, timedelta

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DATA = RAIZ / "data"

# Caracteres que llegaron rotos en la exportación
ROTOS = {"P�blicos": "Públicos", "M�sica": "Música", "Bol�var": "Bolívar", "�xitos": "éxitos", "din�mica": "dinámica"}

# Nombre de compañía tal como venía -> (slug definitivo, nombre bonito)
COMPANIAS = {
    "ASERES": ("aseres", "Aseres"), "Aseres": ("aseres", "Aseres"),
    "BotProject (I)": ("botproject", "BotProject"), "BotProject (II)": ("botproject", "BotProject"),
    "Vol'e Temps (I)": ("vol-e-temps", "Vol'e Temps"), "Vol'e Temps  (II)": ("vol-e-temps", "Vol'e Temps"),
    "Entropias Imposibles (Teatro)": ("entropias-imposibles", "Entropías Imposibles"),
    "Entropías Imposibles": ("entropias-imposibles", "Entropías Imposibles"),
    "PATRI VIERA": ("patri-viera", "Patri Viera"), "Patri Viera": ("patri-viera", "Patri Viera"),
    "Perrakos Sound System": ("perrakos-soundsystem", "Perrakos Soundsystem"),
    "Perrakos Soundsystem": ("perrakos-soundsystem", "Perrakos Soundsystem"),
    "grupo PUJA": ("grupo-puja", "Grupo Puja"),
    "Totó  El Payaso": ("toto-el-payaso", "Totó el Payaso"),
    "Titiriclown ®": ("titiriclown", "Titiriclown"),
    "The Pluger Dixie Band": ("the-plunger-dixie-band", "The Plunger Dixie Band"),
    "Circanario / Aimé Morales": ("circanario-aime-morales", "Circanario / Aimé Morales"),
    "Cía. Suso Imbernón": ("suso-imbernon", "Cía. Suso Imbernón"),
    "Giuseppe Salchichone ": ("giuseppe-salchichone", "Giuseppe Salchichone"),
    "La Gata Japonesa ": ("la-gata-japonesa", "La Gata Japonesa"),
    "eVenti Verticali": ("eventi-verticali", "eVenti Verticali"),
}
# Títulos de espectáculo a corregir (mayúsculas, erratas)
TITULOS = {
    "ASERES EN CONCIERTO": "Aseres en concierto", "PATRI VIERA": "Patri Viera", "INVISIBLE": "Invisible", "VERNE": "Verne",
    "ASTEROIDE B612 (el principito)": "Asteroide B612 (El Principito)", "Taller de rositerapia": "Taller de risoterapia",
    "Taller de Risoterapia": "Taller de risoterapia", "Show de tadeo": "Show de Tadeo", "El Último hombre bala": "El último hombre bala",
    "Son de la isla": "Son de la Isla", "The Plunger Dixie Band - Itinerante": "The Plunger Dixie Band",
}
PROCEDENCIAS = {
    "Islas Canarias - España": "Canarias", "Gran Canaria - España": "Gran Canaria", "Gran canaria": "Gran Canaria",
    "Las Palmas de Gran Canaria - España": "Gran Canaria", "Las Palmas de Gran Canaria, España": "Gran Canaria",
    "Cataluñaa": "Cataluña", "Toulouse/Francia": "Toulouse (Francia)", "Fuerteventura - Las Palmas - España": "Fuerteventura",
    "Comunidad Valenciana -España": "Comunidad Valenciana", "Madrid-Argentina": "Madrid · Argentina",
    "Chile - Gran Canaria": "Chile · Gran Canaria", "Cuba - Gran Canaria": "Cuba · Gran Canaria",
}

ESPACIOS = [
    # id, nombre, nombre corto, lat, lng, dirección para el mapa
    ("sintes-escenario", "Plaza de Sintes · Escenario", "Sintes Escenario", 28.0585054, -15.5481718, "Plaza de Sintes, Teror"),
    ("sintes-calle", "Plaza de Sintes · Calle", "Sintes Calle", 28.0585054, -15.5481718, "Plaza de Sintes, Teror"),
    ("teresa-de-bolivar", "Plaza Teresa de Bolívar", "Teresa de Bolívar", 28.0596361, -15.5468912, "Plaza Teresa de Bolívar, Teror"),
    ("alameda", "Alameda de Pío XII", "Alameda", 28.059158, -15.5482407, "Plaza de la Alameda, Teror"),
    ("plaza-del-pino", "Plaza del Pino", "Plaza del Pino", 28.0595658, -15.5474849, "Plaza del Pino, Teror"),
    ("bulevar", "Bulevar (Paseo González Díaz)", "Bulevar", None, None, "Paseo González Díaz, Teror"),
    ("oficinas-municipales", "Oficinas Municipales", "Oficinas Municipales", 28.0606983, -15.5459753, "Plaza Muro Nuevo, Teror"),
    ("antiguo-ayuntamiento", "Sala Polivalente (Antiguo Ayuntamiento)", "Antiguo Ayuntamiento", 28.0595333, -15.5484768, "Calle Padre Cueto, Teror"),
    ("itinerante", "Itinerante por las calles", "Itinerante", None, None, "Teror"),
]
ESCENARIOS = {
    "Sintes Escenario": "sintes-escenario", "Plaza de Sintes 1": "sintes-escenario",
    "Sintes Calle": "sintes-calle", "Plaza de Sintes": "sintes-calle",
    "Teresa de Bolívar": "teresa-de-bolivar", "Plaza Teresa de Bolívar": "teresa-de-bolivar", "Plaza Teresa Bolívar": "teresa-de-bolivar",
    "Alameda": "alameda", "Alameda Pío XII": "alameda",
    "Plaza El Pino": "plaza-del-pino", "Plaza del Pino": "plaza-del-pino",
    "Bulevar": "bulevar", "Boulevar": "bulevar", "Boulevard": "bulevar",
    "Oficinas Municipales": "oficinas-municipales",
    "Antiguo Ayto": "antiguo-ayuntamiento", "Sala Polivalente Antiguo Ayuntamiento": "antiguo-ayuntamiento",
}
EDICIONES = [
    {"anio": 2024, "numero": "XI", "estado": "archivo"},
    {"anio": 2025, "numero": "XII", "estado": "archivo"},
    {"anio": 2026, "numero": "XIII", "estado": "archivo"},
    {"anio": 2027, "numero": "XIV", "estado": "proxima", "fechas": ""},
]
# Géneros para los filtros: palabra clave en las disciplinas -> género
GENEROS = [
    ("circo", ["circo", "acroba", "malabar", "rueda", "mástil", "aére", "trampol", "vertical", "báscula", "portés", "funambul",
               "zancos", "cuerda", "equilibr", "patines", "diábolo"]),
    ("humor", ["clown", "humor", "payas", "comedia", "impro", "parodia"]),
    ("teatro", ["teatro", "danza", "títere", "narración", "gestual", "kamishibai"]),
    ("musica", ["música", "musica", "canto", "concierto", "brass", "fiest", "rave", "verbena", "musical"]),
    ("magia", ["magia", "quick change"]),
    ("talleres", ["taller", "risoterapia", "terapia de la risa"]),
]


def limpio(t):
    t = (t or "").strip()
    for a, b in ROTOS.items():
        t = t.replace(a, b)
    return t


def slug(t):
    t = unicodedata.normalize("NFKD", t.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def edad(t):
    t = t.strip().lstrip("'")
    if t in ("TP", "") or t.lower().startswith("todos"):
        return "Todos los públicos"
    m = re.search(r"\d+", t)
    return f"+{m.group()}" if m else t


def procedencia(t):
    t = re.sub(r"\s+", " ", t.strip())
    t = PROCEDENCIAS.get(t, t)
    return re.sub(r"\s*-\s*España$", "", t)


def disciplinas(t):
    t = re.sub(r"\s+", " ", t.replace("\n", " ")).strip(" .")
    partes = [p.strip(" .") for p in re.split(r"\s*[,/]\s*|\s*-\s+|\s+-\s*|\s*-\s*(?=[A-ZÁÉÍÓÚ])", t) if p.strip(" .")]
    partes = [p[:1].upper() + p[1:].lower() if p.isupper() else p[:1].upper() + p[1:] for p in partes]
    return ["Música" if p == "Musica" else p for p in partes]


def generos(lista):
    texto = " ".join(lista).lower()
    return [g for g, claves in GENEROS if any(c in texto for c in claves)]


def video(url):
    url = (url or "").strip()
    if not url:
        return None
    m = re.search(r"(?:youtu\.be/|v=|shorts/|embed/)([\w-]{11})", url)
    if m:
        return {"tipo": "youtube", "id": m.group(1), "url": f"https://www.youtube.com/watch?v={m.group(1)}"}
    m = re.search(r"vimeo\.com/(\d+)", url)
    if m:
        return {"tipo": "vimeo", "id": m.group(1), "url": f"https://vimeo.com/{m.group(1)}"}
    return {"tipo": "enlace", "url": url}


def imagen_wix(t):
    m = re.match(r"wix:image://v1/([^/]+)", t or "")
    return m.group(1) if m else None


def texto(t):
    t = limpio(t).replace("\r", "")
    t = re.sub(r"[ \t]+\n", "\n", t)
    return re.sub(r"\n{3,}", "\n\n", t).strip()


def main(ruta):
    lector = csv.reader(open(ruta, encoding="utf-8-sig"))
    cab = next(lector)
    # Hay columnas con el mismo nombre («Escenario»): se queda la primera
    filas = [{k: v for k, v in reversed(list(zip(cab, r)))} for r in lector]
    companias, funciones, redir = {}, [], {}
    for f in filas:
        anio = f["AÑO"].strip()
        if not anio:  # duplicados sin año
            continue
        anio = int(anio)
        nombre_orig = limpio(f["Compañía"])
        cslug, cnombre = COMPANIAS.get(nombre_orig, (slug(nombre_orig), nombre_orig.strip()))
        wix_slug = urllib.parse.unquote(f["Compañias y Artistas y Horarios (Item)"].split("/companias/")[-1])
        if wix_slug != cslug:
            redir[wix_slug] = cslug
        c = companias.setdefault(cslug, {"id": cslug, "nombre": cnombre, "procedencia": "", "imagen": "", "web": "", "instagram": "",
                                         "espectaculos": [], "_anio": 0})
        titulo = limpio(f["Nombre Espectáculo"]).strip()
        titulo = TITULOS.get(titulo, titulo)
        eslug = slug(titulo) or cslug
        e = next((x for x in c["espectaculos"] if x["id"] == eslug), None)
        if e is None:
            e = {"id": eslug, "titulo": titulo, "_anio": 0}
            c["espectaculos"].append(e)
        disc = disciplinas(limpio(f["Disciplinas (máximo 4)"]))
        img = imagen_wix(f["Imagen"])
        if anio >= e["_anio"]:  # los datos más recientes mandan
            e.update({
                "_anio": anio, "disciplinas": disc, "generos": generos(disc + [titulo]), "edad": edad(limpio(f["Edad Recomendada"])),
                "duracion": int(f["Duración (minutos)"]) if f["Duración (minutos)"].strip().isdigit() else None,
                "sinopsis": texto(f["Sinopsis (qué cuenta el espectáculo)"]),
                "descripcion": texto(f["Descripción del Espectáculo (qué va a ver el espectador)"]),
                "frase": texto(f["El espectáculo en 2 frases (para prensa)"]),
                "video": video(f["Enlace Video Promo"]) or e.get("video"),
                "imagen_wix": img or e.get("imagen_wix"),
            })
        if anio >= c["_anio"]:
            c["_anio"] = anio
            c["procedencia"] = procedencia(limpio(f["Procedencia (Comunidad Autónoma / País)"]))
            if img:
                c["imagen_wix"] = img
        # Fecha: Wix la guarda en UTC; en agosto Canarias va a UTC+1
        inicio = datetime.strptime(f["Fecha"][:16], "%Y-%m-%dT%H:%M") + timedelta(hours=1)
        if (inicio.hour, inicio.minute) == (0, 0):
            # En Wix los bolos de medianoche se apuntaban con el día de programa (28/08 0:00 = la noche del 28 al 29)
            inicio += timedelta(days=1)
        esc = limpio(f["Escenario"])
        espacio = "itinerante" if esc.lower().startswith("itinerante") else ESCENARIOS[esc]
        nota = ""
        m = re.match(r"Itinerante\s*\(?(.*?)\)?$", esc)
        if m and m.group(1):
            nota = m.group(1).strip().replace("Boulevard", "Bulevar").replace("Síntes", "Sintes")
            nota = nota[:1].upper() + nota[1:]
        fid = f"{anio}-{inicio:%m%d-%H%M}-{cslug}"
        if any(x["id"] == fid for x in funciones):
            continue
        funciones.append({"id": fid, "edicion": anio, "inicio": inicio.strftime("%Y-%m-%dT%H:%M"), "espacio": espacio,
                          "compania": cslug, "espectaculo": eslug, "nota": nota})

    for c in companias.values():
        c.pop("_anio")
        for e in c["espectaculos"]:
            e.pop("_anio")
            if not e.get("imagen_wix"):
                e.pop("imagen_wix", None)
    lista = sorted(companias.values(), key=lambda c: slug(c["nombre"]))
    funciones.sort(key=lambda x: (x["inicio"], x["compania"]))
    DATA.mkdir(exist_ok=True)

    def guardar(nombre, datos):
        (DATA / nombre).write_text(json.dumps(datos, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    guardar("companias.json", lista)
    guardar("funciones.json", funciones)
    guardar("espacios.json", [dict(zip(("id", "nombre", "corto", "lat", "lng", "direccion"), e)) for e in ESPACIOS])
    guardar("ediciones.json", EDICIONES)
    guardar("redirecciones-wix.json", dict(sorted(redir.items())))
    print(f"{len(lista)} compañías, {sum(len(c['espectaculos']) for c in lista)} espectáculos, {len(funciones)} funciones")


if __name__ == "__main__":
    main(sys.argv[1])
