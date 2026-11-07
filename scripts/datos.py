"""Carga y prepara los datos del festival (data/*.json) para generar la web.

Los JSON se editan desde el portal (Programación En Pie) o a mano. Estructura:
  companias.json   [{id, nombre, procedencia, web, instagram, espectaculos: [{id, titulo, disciplinas, generos, edad,
                     duracion, sinopsis, descripcion, frase, video: {tipo, id, url}}]}]
  funciones.json   [{id, edicion, inicio "AAAA-MM-DDTHH:MM" (hora de Canarias), espacio, compania, espectaculo, nota}]
  espacios.json    [{id, nombre, corto, lat, lng, direccion}]
  ediciones.json   [{anio, numero, estado: archivo|programada|proxima, fechas (texto libre, opcional)}]
                   «proxima» = se anuncia en portada pero su programa es borrador (no se publica)
"""
import json
import pathlib
from datetime import datetime, timedelta

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DATA = RAIZ / "data"

GENEROS = [("circo", "Circo"), ("humor", "Clown y humor"), ("teatro", "Teatro y danza"), ("musica", "Música"),
           ("magia", "Magia"), ("talleres", "Talleres")]
NOMBRE_GENERO = dict(GENEROS)
DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
DIAS_CORTOS = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
HORA_CORTE = 6  # lo que empieza antes de las 6:00 cuenta como noche del día anterior


def _cargar(nombre, defecto):
    p = DATA / nombre
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else defecto


def imagen_existe(ruta):
    return (RAIZ / f"{ruta}-400.webp").exists()


class Datos:
    def __init__(self):
        self.companias = _cargar("companias.json", [])
        self.espacios = _cargar("espacios.json", [])
        self.ediciones = sorted(_cargar("ediciones.json", []), key=lambda e: e["anio"])
        self.por_compania = {c["id"]: c for c in self.companias}
        self.por_espacio = {e["id"]: e for e in self.espacios}
        self.funciones = []
        # Una edición «proxima» es un borrador: su programa no se publica hasta pasarla a «programada»
        borrador = {e["anio"] for e in self.ediciones if e.get("estado") == "proxima"}
        for f in _cargar("funciones.json", []):
            if f.get("edicion") in borrador:
                continue
            c = self.por_compania.get(f["compania"])
            if not c:
                continue
            e = next((x for x in c["espectaculos"] if x["id"] == f.get("espectaculo")), None) or (c["espectaculos"] or [{}])[0]
            inicio = datetime.strptime(f["inicio"], "%Y-%m-%dT%H:%M")
            dia = (inicio - timedelta(hours=HORA_CORTE)).date()
            fin = inicio + timedelta(minutes=e.get("duracion") or 60)
            self.funciones.append({**f, "c": c, "e": e, "inicio_dt": inicio, "fin_dt": fin, "dia": dia,
                                   "esp": self.por_espacio.get(f["espacio"], {"id": f["espacio"], "nombre": f["espacio"], "corto": f["espacio"]})})
        self.funciones.sort(key=lambda f: (f["inicio_dt"], f["c"]["nombre"]))
        for c in self.companias:
            fs = [f for f in self.funciones if f["compania"] == c["id"]]
            c["anios"] = sorted({f["edicion"] for f in fs})
            c["funciones"] = fs
            c["imagen"] = f"img/companias/{c['id']}" if imagen_existe(f"img/companias/{c['id']}") else None
            orden = {e["id"]: max([f["edicion"] for f in fs if f["espectaculo"] == e["id"]] or [0]) for e in c["espectaculos"]}
            c["espectaculos"].sort(key=lambda e: -orden[e["id"]])
            for e in c["espectaculos"]:
                ruta = f"img/espectaculos/{c['id']}--{e['id']}"
                e["imagen"] = ruta if imagen_existe(ruta) else c["imagen"]
                e["anios"] = sorted({f["edicion"] for f in fs if f["espectaculo"] == e["id"]})
            c["generos"] = sorted({g for e in c["espectaculos"] for g in e.get("generos", [])}, key=[g for g, _ in GENEROS].index)
        self.companias.sort(key=lambda c: c["nombre"].lower())

    # ----- ediciones
    def anios_con_programa(self):
        return sorted({f["edicion"] for f in self.funciones}, reverse=True)

    def edicion(self, anio):
        return next((e for e in self.ediciones if e["anio"] == anio), {"anio": anio, "numero": "", "estado": "archivo"})

    def proxima(self):
        """La edición que se anuncia en portada: la marcada como «proxima» o «programada» más reciente."""
        vivas = [e for e in self.ediciones if e.get("estado") in ("proxima", "programada")]
        return vivas[-1] if vivas else (self.ediciones[-1] if self.ediciones else {"anio": datetime.now().year, "numero": "", "estado": "proxima"})

    def ultima_con_programa(self):
        anios = self.anios_con_programa()
        return anios[0] if anios else None

    def funciones_de(self, anio):
        return [f for f in self.funciones if f["edicion"] == anio]

    def companias_de(self, anio):
        ids = {f["compania"] for f in self.funciones_de(anio)}
        return [c for c in self.companias if c["id"] in ids]

    def dias_de(self, anio):
        return sorted({f["dia"] for f in self.funciones_de(anio)})


def fecha_larga(d):
    return f"{DIAS[d.weekday()]} {d.day} de {MESES[d.month - 1]}"


def fechas_texto(dias):
    """[28, 29, 30 ago 2026] -> '28, 29 y 30 de agosto de 2026'"""
    if not dias:
        return ""
    if len({(d.month, d.year) for d in dias}) == 1:
        nums = [str(d.day) for d in dias]
        lista = nums[0] if len(nums) == 1 else ", ".join(nums[:-1]) + " y " + nums[-1]
        return f"{lista} de {MESES[dias[0].month - 1]} de {dias[0].year}"
    return " · ".join(f"{d.day} de {MESES[d.month - 1]}" for d in dias) + f" de {dias[-1].year}"
