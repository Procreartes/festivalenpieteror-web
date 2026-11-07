#!/usr/bin/env python3
"""Genera las páginas HTML de la web del Festival En Pie Teror.

Uso:  python3 scripts/generar.py
Compañías, espectáculos, funciones, espacios y ediciones salen de data/*.json (se editan desde el portal).
Textos fijos y colaboradores están en este fichero.
No edites los .html a mano: se sobrescriben.
"""
import html
import json
import unicodedata
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
from iconos import ICO  # noqa: E402
from datos import DIAS_CORTOS, GENEROS, NOMBRE_GENERO, Datos, fecha_larga, fechas_texto  # noqa: E402

D = Datos()

DOMINIO = "https://festivalenpieteror.com"
FORMULARIO = "https://portal.grupolivon.com/publico/inscripciones/enpie"
EDICION_CONVOCATORIA = 2027
INSTAGRAM = "https://www.instagram.com/festivalenpieteror/"
FACEBOOK = "https://www.facebook.com/FestivalenPie"
YOUTUBE = "https://www.youtube.com/@FestivalEnPieTeror"
VIDEO_ID = "5TzG4Ktgveo"
ICO["yt"] = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.6 7.2a2.6 2.6 0 0 0-1.8-1.8C18.2 5 12 5 12 5s-6.2 0-7.8.4A2.6 2.6 0 0 0 2.4 7.2 27 27 0 0 0 2 12a27 27 0 0 0 .4 4.8 2.6 2.6 0 0 0 1.8 1.8C5.8 19 12 19 12 19s6.2 0 7.8-.4a2.6 2.6 0 0 0 1.8-1.8A27 27 0 0 0 22 12a27 27 0 0 0-.4-4.8zM10 15V9l5.2 3z"/></svg>'
ICO["play"] = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 4.5v15l13-7.5z"/></svg>'
ICO["pdf"] = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6M12 12v6M9 15l3 3 3-3"/></svg>'

ICO["estrella"] = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M12 3.2l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17.2l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/></svg>'
ICO["compartir"] = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="M8.6 13.5l6.8 4M15.4 6.5l-6.8 4"/></svg>'
ICO["buscar"] = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>'
ICO["reloj"] = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
ICO["papelera"] = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3"/></svg>'
ICO["atras"] = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>'

COLABORAN = [
    ("cabildo-fundacion-nanino-diaz", "Cabildo de Gran Canaria · Fundación Nanino Díaz Cutillas", "https://cabildo.grancanaria.com/", ""),
    ("islas-canarias", "Islas Canarias", "https://www.holaislascanarias.com/", ""),
    ("gobierno-de-canarias", "Gobierno de Canarias", "https://www.gobiernodecanarias.org/", ""),
    ("aguas-de-teror", "Aguas de Teror", "https://www.aguasdeteror.com/", ""),
    ("7up", "7UP", "https://www.aguasdeteror.com/", ""),
    ("ahembo", "Ahembo", "https://www.ahembo.com/", "bajo"),
    ("clipper", "Clipper", "https://www.ahembo.com/", ""),
    ("disaterura", "Disaterura", "", ""),
    ("estrella-galicia", "Estrella Galicia", "https://estrellagalicia.es/", ""),
]
DISCIPLINAS = ["Circo", "Clown", "Teatro de calle", "Teatro gestual", "Humor", "Danza", "Acrobacia", "Aéreos", "Malabares",
               "Magia", "Títeres", "Música", "Pasacalles", "Itinerante", "Instalación", "Público familiar"]
EDADES = ["Todos los públicos", "+3", "+6", "+9", "+12", "+16", "+18"]
FORMATOS = ["Fijo (en un espacio)", "Itinerante", "Fijo o itinerante", "Espacio no convencional"]

ONDA = ('<div class="rasgado" aria-hidden="true"><svg viewBox="0 0 1440 60" preserveAspectRatio="none">'
        '<path fill="currentColor" d="M0 34 L40 28 L88 40 L130 24 L176 36 L220 22 L268 38 L318 26 L360 40 L410 30 L456 18 L506 34 '
        'L548 26 L598 40 L646 24 L690 36 L742 20 L790 34 L836 28 L886 42 L934 24 L978 34 L1028 22 L1074 38 L1122 28 L1170 40 '
        'L1214 24 L1262 34 L1310 20 L1356 36 L1400 26 L1440 34 L1440 60 L0 60 Z"/></svg></div>')


def plano(t):
    t = unicodedata.normalize("NFD", str(t).lower())
    return "".join(c for c in t if not unicodedata.combining(c))


def esc(t):
    return html.escape(str(t), quote=True)


def img(ruta, alt, anchos, sizes, carga="lazy", prioridad=False, clase=""):
    srcset = ", ".join(f"/{ruta}-{w}.webp {w}w" for w in anchos)
    return (f'<img src="/{ruta}-{anchos[0]}.webp" srcset="{srcset}" sizes="{sizes}" alt="{esc(alt)}" loading="{carga}" decoding="async"'
            f'{" fetchpriority=\"high\"" if prioridad else ""}{f" class={chr(34)}{clase}{chr(34)}" if clase else ""}>')


def cabecera():
    items = [("/programa", "Programa"), ("/companias", "Compañías"), ("/#video", "Vídeo"), ("/#sostenibilidad", "Sostenibilidad"),
             ("/#teror", "Teror")]
    lis = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in items)
    return f'''<a class="saltar" href="#contenido">Saltar al contenido</a>
<header class="nav">
  <div class="contenedor">
    <a class="marca" href="/" aria-label="Festival En Pie Teror, ir al inicio"><img src="/img/logos/enpie-color.webp" alt="" width="72" height="44"><small>Festival Internacional de Artes en la Calle</small></a>
    <button class="boton-menu" type="button" aria-controls="menu" aria-expanded="false"><span class="visualmente-oculto">Abrir menú</span>{ICO["menu"]}</button>
    <ul class="menu" id="menu">{lis}<li class="cta"><a href="/inscripcion">Inscribe tu compañía</a></li></ul>
  </div>
</header>'''


def pie():
    return f'''<footer class="pie">
  <div class="contenedor">
    <div class="pie-arriba">
      <img class="logo" src="/img/logos/enpie-blanco.webp" alt="En Pie, Festival de Arte en la Calle" width="114" height="70" loading="lazy">
      <div class="pie-org"><img src="/img/logos/ayuntamiento-teror.webp" alt="Ayuntamiento de Teror" width="151" height="80" loading="lazy">
        <span>Organiza el Ayuntamiento de Teror.</span></div>
      <div class="pie-redes">
        <a href="{INSTAGRAM}" rel="noopener" aria-label="Instagram del Festival En Pie Teror">{ICO["ig"]}</a>
        <a href="{FACEBOOK}" rel="noopener" aria-label="Facebook del Festival En Pie Teror">{ICO["fb"]}</a>
        <a href="{YOUTUBE}" rel="noopener" aria-label="YouTube del Festival En Pie Teror">{ICO["yt"]}</a>
      </div>
    </div>
    <div class="pie-base">
      <span>© <span id="anio">2026</span> Ayuntamiento de Teror · Festival Internacional de Artes en la Calle En Pie Teror</span>
      <span><a href="/aviso-legal.html">Aviso legal</a> · <a href="/privacidad.html">Privacidad</a> · <a href="/cookies.html">Cookies</a></span>
    </div>
  </div>
</footer>
<script src="/js/main.js" defer></script>'''


def pagina(titulo, descripcion, ruta, cuerpo, extra_head="", og="/img/og-en-pie-teror.jpg", canonica=None):
    return f'''<!doctype html>
<html lang="es" class="sin-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titulo)}</title>
<meta name="description" content="{esc(descripcion)}">
<link rel="canonical" href="{DOMINIO}{canonica or ruta}">
<meta name="theme-color" content="#0f2a2e">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Festival En Pie Teror">
<meta property="og:locale" content="es_ES">
<meta property="og:title" content="{esc(titulo)}">
<meta property="og:description" content="{esc(descripcion)}">
<meta property="og:url" content="{DOMINIO}{ruta}">
<meta property="og:image" content="{DOMINIO}{og}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/fonts/bricolage-grotesque-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/estilos.css">
{extra_head}</head>
<body>
{cabecera()}
<main id="contenido">
{cuerpo}
</main>
{pie()}
</body>
</html>
'''


# ---------------------------------------------------------------- formulario
def campo(nombre, etiqueta, tipo="text", req=True, ayuda="", ancho=False, extra="", req2=False):
    r = ' <span class="req">*</span>' if (req or req2) else ""
    attrs = (" required" if req else "") + (" data-req2" if req2 else "") + (f" {extra}" if extra else "")
    if tipo == "textarea":
        control = f'<textarea id="f-{nombre}" name="{nombre}"{attrs}></textarea>'
    else:
        control = f'<input id="f-{nombre}" name="{nombre}" type="{tipo}"{attrs}>'
    return (f'<div class="campo{" ancho" if ancho else ""}"><label for="f-{nombre}">{etiqueta}{r}</label>{control}'
            f'{f"<small>{ayuda}</small>" if ayuda else ""}</div>')


def selector(nombre, etiqueta, opciones, req=True, req2=False):
    r = ' <span class="req">*</span>' if (req or req2) else ""
    ops = '<option value="">Elige…</option>' + "".join(f'<option>{esc(o)}</option>' for o in opciones)
    return (f'<div class="campo"><label for="f-{nombre}">{etiqueta}{r}</label><select id="f-{nombre}" name="{nombre}"'
            f'{" required" if req else ""}{" data-req2" if req2 else ""}>{ops}</select></div>')


def bloque_espectaculo(s):
    """s = '' para el primero, '2' para el segundo (opcional)."""
    req, req2 = (s == ""), (s == "2")
    chips = "".join(f'<label><input type="checkbox" name="disciplinas{s}" value="{esc(d)}"><span>{esc(d)}</span></label>' for d in DISCIPLINAS)
    def c(*a, obligatorio=True, **k):
        return campo(*a, req=req and obligatorio, req2=req2 and obligatorio, **k)
    return f'''<div class="campos">
      {c(f"titulo{s}", "Título del espectáculo", ancho=True)}
      <div class="campo ancho"><label>Disciplinas <span class="req">*</span></label>
        <div class="chips" data-max="4" data-grupo="disciplinas{s}" tabindex="-1">{chips}</div>
        <small>Elige hasta 4. Si no está la tuya, escríbela abajo.</small>
        <input name="disciplinas_otra{s}" type="text" placeholder="Otra disciplina" style="margin-top:8px" aria-label="Otra disciplina"></div>
      {selector(f"edad{s}", "Edad recomendada", EDADES, req=req, req2=req2)}
      {c(f"duracion{s}", "Duración (minutos)", "number", extra='min="5" max="300" inputmode="numeric"')}
      {selector(f"formato{s}", "Formato", FORMATOS, req=req, req2=req2)}
      {c(f"personas{s}", "Personas en gira", "number", extra='min="1" max="60" inputmode="numeric"', ayuda="Artistas y técnicos que viajan.")}
      {c(f"sinopsis{s}", "Sinopsis: qué cuenta el espectáculo", "textarea", ancho=True)}
      {c(f"descripcion{s}", "Descripción: qué va a ver el público", "textarea", ancho=True)}
      {c(f"prensa{s}", "El espectáculo en dos frases (para prensa)", "textarea", ancho=True, extra='maxlength="600" style="min-height:80px"')}
      {c(f"video{s}", "Enlace al vídeo", "url", ayuda="YouTube o Vimeo. Si es privado, incluye la contraseña en observaciones.", extra='placeholder="https://"')}
      {c(f"materiales{s}", "Enlace a fotos, dosier y rider técnico", "url", obligatorio=False, ayuda="Carpeta de Drive, Dropbox o WeTransfer. Fotos en alta calidad y sin texto.", extra='placeholder="https://"')}
      {c(f"espacio{s}", "Espacio que necesitas", obligatorio=False, ayuda="Superficie, tipo de suelo, altura, anclajes…")}
      {c(f"estreno{s}", "Año de estreno", "number", obligatorio=False, extra='min="1980" max="2030" inputmode="numeric"')}
      {c(f"tecnica{s}", "Necesidades técnicas (sonido, luz, toma de corriente…)", "textarea", ancho=True, obligatorio=False, extra='style="min-height:80px"')}
    </div>'''


def formulario():
    return f'''<form id="form-inscripcion" class="formulario aparece" action="{FORMULARIO}" method="post" novalidate>
  <fieldset><legend><span class="num">1</span> La compañía</legend>
    <div class="campos">
      {campo("compania", "Nombre artístico, grupo o compañía", ancho=True)}
      {campo("procedencia", "Procedencia", ayuda="Comunidad autónoma o país (y la isla, si es de Canarias).")}
      {campo("municipio", "Municipio", req=False)}
      {campo("web", "Web", "url", req=False, extra='placeholder="https://"')}
      {campo("instagram", "Instagram", req=False, extra='placeholder="@compania"')}
      {campo("otras_redes", "Otras redes o enlaces", req=False)}
      {campo("cif", "CIF / NIF de quien factura", req=False, ayuda="Si ya lo tienes claro. Se pedirá al contratar.")}
    </div></fieldset>
  <fieldset><legend><span class="num">2</span> Persona de contacto</legend>
    <div class="campos">
      {campo("contacto", "Nombre y apellidos")}
      {campo("cargo", "Qué haces en la compañía", req=False, extra='placeholder="Distribución, dirección, artista…"')}
      {campo("email", "Correo electrónico", "email", extra='autocomplete="email"')}
      {campo("telefono", "Teléfono (mejor móvil con WhatsApp)", "tel", extra='autocomplete="tel" minlength="9" inputmode="tel"')}
    </div></fieldset>
  <fieldset><legend><span class="num">3</span> Tu espectáculo</legend>
    <p class="ayuda">Puedes presentar hasta dos espectáculos.</p>
    <div class="espectaculo-bloque">{bloque_espectaculo("")}</div>
    <div class="espectaculo-bloque" id="espectaculo-2" hidden><h3>Segundo espectáculo <button type="button" class="quitar" id="quitar-espectaculo">Quitar</button></h3>{bloque_espectaculo("2")}</div>
    <button type="button" class="boton boton-tinta" id="anadir-espectaculo">+ Añadir otro espectáculo</button>
  </fieldset>
  <fieldset><legend><span class="num">4</span> Equipo y caché</legend>
    <div class="campos">
      {campo("miembros", "Miembros de la compañía", "textarea", req=False, ancho=True, ayuda="Nombre y función de quienes vendrían (artistas, técnicos…). No pongas DNI ni datos de salud: los pediremos solo si se contrata.")}
      {campo("cache", "Caché orientativo", req=False, ayuda="Por función y, si quieres, por dos funciones. Indica si incluye IGIC/IVA.")}
      {campo("observaciones", "Observaciones", "textarea", req=False, ancho=True, ayuda="Cualquier otra cosa que debamos saber: disponibilidad, giras, idiomas, accesibilidad…")}
    </div></fieldset>
  <fieldset><legend><span class="num">5</span> Privacidad</legend>
    <label class="casilla"><input type="checkbox" name="privacidad" required> <span>He leído la <a href="/privacidad.html" target="_blank">política de privacidad</a> y acepto que el Ayuntamiento de Teror trate estos datos para valorar la propuesta y contactar con la compañía. <span class="req">*</span></span></label>
    <label class="casilla"><input type="checkbox" name="comunicaciones"> <span>Quiero recibir por correo las próximas convocatorias del festival (puedes darte de baja cuando quieras).</span></label>
  </fieldset>
  <div class="trampa" aria-hidden="true"><label>No rellenes este campo <input type="text" name="web_empresa" tabindex="-1" autocomplete="off"></label></div>
  <div class="envio"><button class="boton boton-coral" type="submit">Enviar inscripción {ICO["flecha"]}</button><span class="estado-envio" role="status" aria-live="polite"></span></div>
</form>
<div id="gracias" class="formulario gracias" hidden>
  <h3>¡Inscripción recibida!</h3>
  <p>Gracias por querer venir a Teror. El equipo del festival revisa todas las propuestas y se pondrá en contacto con las compañías seleccionadas.</p>
  <span class="ref"></span>
</div>'''


# ---------------------------------------------------------------- inicio
def tarjeta_compania(c, anio=None, sizes="(max-width:720px) 50vw, (max-width:1000px) 33vw, 280px"):
    """Tarjeta enlazada a la ficha. Con anio, enseña el espectáculo de ese año."""
    e = next((x for x in c["espectaculos"] if anio in x["anios"]), c["espectaculos"][0] if c["espectaculos"] else {"titulo": "", "disciplinas": []})
    foto = img(e["imagen"], f"{c['nombre']}, {e['titulo']}", [400, 800], sizes) if e.get("imagen") else f'<span class="sin-foto" aria-hidden="true">{esc(c["nombre"][:1])}</span>'
    anios = "".join(f"<span>{a}</span>" for a in c["anios"])
    return f'''<li class="compania aparece" data-tipos="{" ".join(c["generos"])}" data-anios="{" ".join(map(str, c["anios"]))}" data-texto="{esc(plano(c["nombre"] + " " + " ".join(x["titulo"] for x in c["espectaculos"]) + " " + c["procedencia"]))}">
      <a href="/companias/{c["id"]}">{foto}
      <div class="compania-cuerpo"><h3>{esc(c["nombre"])}</h3><p class="espectaculo">{esc(e["titulo"])}</p><p class="disciplina">{esc(", ".join(e.get("disciplinas", [])))}</p>
      <p class="origen">{esc(c["procedencia"])}<span class="anios">{anios}</span></p></div></a></li>'''


def botones_generos(con_todas=True):
    usados = {g for c in D.companias for g in c["generos"]}
    return (('<button type="button" class="filtro" data-filtro="todas" aria-pressed="true">Todas</button>' if con_todas else "")
            + "".join(f'<button type="button" class="filtro" data-filtro="{k}" aria-pressed="false">{t}</button>' for k, t in GENEROS if k in usados))


def inicio():
    prox = D.proxima()
    ultimo = D.ultima_con_programa()
    fs, cs = D.funciones_de(ultimo), D.companias_de(ultimo)
    dias = D.dias_de(ultimo)
    ed_ult = D.edicion(ultimo)
    filtros = botones_generos()
    tarjetas = "".join(tarjeta_compania(c, ultimo) for c in cs)
    espacios_usados = [D.por_espacio[i] for i in dict.fromkeys(f["espacio"] for f in fs) if i in D.por_espacio]
    CIFRAS = [(str(len(cs)), "compañías y artistas"), (str(len(fs)), f"funciones en {len(dias)} días"),
              (str(len(espacios_usados)), "espacios de Teror convertidos en escenario"), (str(len(D.companias)), f"compañías han pasado por En Pie desde {D.ediciones[0]['anio'] if D.ediciones else ultimo}"),
              (ed_ult.get("numero") or str(ultimo), "ediciones del festival"), ("0 €", "todo gratis y en la calle")]
    cifras = "".join(f'<li class="cifra aparece"><strong>{a}</strong><span>{b}</span></li>' for a, b in CIFRAS)
    if prox["anio"] > (ultimo or 0):
        pildora = f'{prox.get("numero", "")} edición · {prox["anio"]} · {esc(prox.get("fechas") or "Fechas muy pronto")}'.strip(" ·")
        lema_extra = f'La próxima edición será en {prox["anio"]}. Mientras, revive el programa de {ultimo} y prepara tu propuesta.'
    else:
        pildora = f'{prox.get("numero", "")} edición · {fechas_texto(dias)}'
        lema_extra = "Consulta el programa, filtra por día, espacio o género y monta tu propio itinerario."
    ritmos = "".join(f"<span>{r}</span>" for r in ["Circo", "Clown", "Teatro de calle", "Acrobacia", "Danza", "Música", "Humor", "Aéreos", "Pasacalles"])
    logos = "".join(
        (f'<li><a href="{u}" rel="noopener"><img class="{c}" src="/img/logos/{s}.webp" alt="{esc(a)}" loading="lazy"></a></li>' if u
         else f'<li><img class="{c}" src="/img/logos/{s}.webp" alt="{esc(a)}" loading="lazy"></li>') for s, a, u, c in COLABORAN)
    ld = {"@context": "https://schema.org", "@type": "Festival", "name": f"{ed_ult.get('numero', '')} Festival Internacional de Artes en la Calle En Pie Teror".strip(),
          "startDate": dias[0].isoformat(), "endDate": dias[-1].isoformat(), "isAccessibleForFree": True,
          "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode", "eventStatus": "https://schema.org/EventScheduled",
          "location": {"@type": "Place", "name": "Casco histórico de Teror",
                       "address": {"@type": "PostalAddress", "addressLocality": "Teror", "postalCode": "35330", "addressRegion": "Las Palmas", "addressCountry": "ES"}},
          "image": [DOMINIO + "/img/og-en-pie-teror.jpg"], "organizer": {"@type": "Organization", "name": "Ayuntamiento de Teror", "url": "https://teror.es"},
          "description": "Circo, clown, teatro de calle, danza y música en las calles de Teror (Gran Canaria). Entrada gratuita."}
    ejes = [("bus", "Movilidad sostenible", "Fomento del transporte público y de los desplazamientos sostenibles para llegar a Teror."),
            ("gota", "Agua y energía", "Ahorro de agua y de energía en el montaje y durante los días de festival."),
            ("recicla", "Residuos", "Menos residuos, reutilización de infraestructuras y economía circular."),
            ("manos", "Inclusión", "Accesibilidad, condiciones laborales justas, apoyo al comercio local y concienciación del público.")]
    ejes_html = "".join(f'<li class="eje aparece">{ICO[i]}<h3>{h}</h3><p>{p}</p></li>' for i, h, p in ejes)
    cuerpo = f'''
<section class="portada" aria-labelledby="titulo-portada">
  <figure class="portada-foto">{img("img/fotos/puja-asteroide", "Artista de teatro aéreo de Grupo Puja suspendida sobre el público en las calles de Teror", [900, 1600, 2400], "100vw", carga="eager", prioridad=True)}</figure>
  <div class="contenedor">
    <img class="portada-logo" src="/img/logos/enpie-blanco.webp" alt="En Pie, Festival de Arte en la Calle" width="230" height="141">
    <p class="pildora">{pildora}</p>
    <h1 class="titular" id="titulo-portada">Teror se pone <em>en pie</em></h1>
    <p class="portada-lema">Festival Internacional de Artes en la Calle. Circo, clown, teatro de calle, danza y música por las plazas y rincones del casco de Teror, en Gran Canaria. Gratis y para todos los públicos. {lema_extra}</p>
    <div class="botones">
      <a class="boton boton-coral" href="/inscripcion">Inscribe tu compañía · {EDICION_CONVOCATORIA} {ICO["flecha"]}</a>
      <a class="boton boton-claro" href="/programa">Programa {ultimo}</a>
      <a class="boton boton-claro" href="#video">{ICO["play"]} Ver el vídeo</a>
    </div>
  </div>
  {ONDA}
</section>

<div class="cinta" aria-hidden="true"><div class="cinta-pista">{ritmos}{ritmos}</div></div>

<section class="seccion" aria-labelledby="titulo-cifras">
  <div class="contenedor">
    <div class="cabecera aparece"><span class="antetitulo">Así fue {ultimo}</span>
      <h2 id="titulo-cifras">Tres días en los que <span class="subrayado">la calle fue el escenario</span></h2>
      <p>Compañías de Canarias, de la península y de fuera de España llenaron plazas, calles y rincones de la Villa con espectáculos para todos los públicos, sin entradas y a la vuelta de cada esquina.</p></div>
    <ul class="cifras">{cifras}</ul>
  </div>
</section>

<section class="seccion papel" id="companias" aria-labelledby="titulo-companias">
  <div class="contenedor">
    <div class="cabecera aparece"><span class="antetitulo">Compañías y artistas {ultimo}</span>
      <h2 id="titulo-companias">Quién llenó Teror de magia</h2>
      <p>Circo, teatro de calle, humor, teatro gestual, clown, acrobacias y mucha música.</p></div>
    <div class="filtros" role="group" aria-label="Filtrar por disciplina">{filtros}</div>
    <ul class="companias">{tarjetas}</ul>
    <div class="botones" style="margin-top:32px"><a class="boton boton-coral" href="/programa">{ICO["reloj"]} Programa {ultimo} por horas</a>
      <a class="boton boton-tinta" href="/companias">Todas las compañías desde {D.ediciones[0]["anio"]}</a>
      {f'<a class="boton boton-claro-tinta" href="/programa/programa-en-pie-teror-2026.pdf">{ICO["pdf"]} PDF 2026</a>' if ultimo == 2026 else ""}</div>
  </div>
</section>

<section class="seccion oscuro" id="video" aria-labelledby="titulo-video">
  <div class="contenedor dos-col">
    <div class="aparece"><span class="antetitulo">El festival en un minuto</span>
      <h2 id="titulo-video" style="font-size:clamp(2.3rem,5vw,3.6rem)">Míralo con tus propios ojos</h2>
      <p>Las compañías de esta edición, en un vídeo. Para más, en nuestro canal de YouTube.</p>
      <div class="botones"><a class="boton boton-claro" href="{YOUTUBE}" rel="noopener">{ICO["yt"]} Canal de YouTube</a></div></div>
    <div class="aparece">
      <div class="video" data-video="{VIDEO_ID}" data-titulo="Vídeo promocional del Festival En Pie Teror">
        {img("img/fotos/video-promo", "Vídeo promocional del Festival En Pie Teror", [800, 1280], "(max-width:900px) 100vw, 560px")}
        <button type="button" aria-label="Reproducir el vídeo"><span>{ICO["play"]}</span></button>
      </div>
      <p class="nota-video">Al pulsar se carga el reproductor de YouTube en su modo sin cookies.</p>
    </div>
  </div>
</section>

<section class="seccion" id="espacios" aria-labelledby="titulo-espacios">
  <div class="contenedor dos-col">
    <figure class="foto-marco aparece">{img("img/fotos/sacude", "Artista aérea suspendida en el aire durante una función del festival", [1200, 2400], "(max-width:900px) 100vw, 560px")}</figure>
    <div class="aparece"><span class="antetitulo">Un pueblo convertido en escenario</span>
      <h2 id="titulo-espacios" style="font-size:clamp(2.3rem,5vw,3.6rem)">{len(espacios_usados)} espacios, cientos de miradas</h2>
      <p>En En Pie el teatro sale a buscarte: las funciones se reparten por las plazas y calles del casco histórico, y algunas no se están quietas.</p>
      <ul class="espacios" style="--c:var(--noche)">{"".join(f'<li style="background:#fff;border-color:var(--noche);color:var(--noche)">{esc(e["nombre"])}</li>' for e in espacios_usados)}</ul></div>
  </div>
</section>

<section class="seccion convocatoria" id="convocatoria" aria-labelledby="titulo-convocatoria">
  <div class="contenedor dos-col">
    <div class="aparece"><span class="antetitulo">Convocatoria {EDICION_CONVOCATORIA} · abierta</span>
      <h2 id="titulo-convocatoria" style="font-size:clamp(2.3rem,5.6vw,4rem)">¿Quieres actuar en En Pie {EDICION_CONVOCATORIA}?</h2>
      <p style="font-size:1.15rem">Buscamos compañías y artistas de circo, clown, teatro de calle, danza, música y espectáculos itinerantes para la próxima edición.</p>
      <div class="botones"><a class="boton boton-coral" href="/inscripcion">Inscribe tu compañía {ICO["flecha"]}</a></div></div>
    <ol class="pasos aparece" style="grid-template-columns:1fr;margin:0">
      <li><strong>Rellena la ficha</strong> con tu espectáculo y un enlace al vídeo. Tarda unos 10 minutos.</li>
      <li><strong>La revisamos</strong>: el equipo del festival valora todas las propuestas.</li>
      <li><strong>Te llamamos</strong> si tu espectáculo encaja en la programación.</li>
    </ol>
  </div>
</section>

<section class="seccion" id="sostenibilidad" aria-labelledby="titulo-sostenibilidad">
  <div class="contenedor">
    <div class="cabecera aparece"><span class="antetitulo">Sostenibilidad, inclusión y cultura viva</span>
      <h2 id="titulo-sostenibilidad">Un arte que deja huella, <span class="subrayado">pero no en el planeta</span></h2>
      <p>El Plan de Sostenibilidad del Festival En Pie busca reducir el impacto ambiental del evento y, a la vez, apoyar la inclusión social y la economía local.</p></div>
    <ul class="ejes">{ejes_html}</ul>
  </div>
</section>

<section class="seccion papel" id="teror" aria-labelledby="titulo-teror">
  <div class="contenedor dos-col">
    <div class="aparece"><span class="antetitulo">Ven y quédate</span>
      <h2 id="titulo-teror" style="font-size:clamp(2.3rem,5vw,3.6rem)">Teror, mucho que ver</h2>
      <p>Teror combina historia, arquitectura tradicional y naturaleza a pocos minutos de Las Palmas de Gran Canaria. La Basílica de Nuestra Señora del Pino, sus calles de balcones canarios, sus montañas y su mercado hacen de la Villa el escenario perfecto para un festival de calle.</p>
      <div class="enlaces"><a class="boton boton-turquesa" href="https://turismo.teror.es/" rel="noopener">Turismo de Teror {ICO["flecha"]}</a>
        <a class="boton boton-turquesa" href="https://www.holaislascanarias.com/" rel="noopener">Islas Canarias {ICO["flecha"]}</a></div></div>
    <figure class="foto-marco aparece">{img("img/fotos/teror", "Calle del casco histórico de Teror", [800, 1400], "(max-width:900px) 100vw, 560px")}</figure>
  </div>
</section>

<section class="colaboran" aria-labelledby="titulo-colaboran">
  <div class="contenedor">
    <h2 id="titulo-colaboran">Organiza y colaboran</h2>
    <ul class="logos"><li><a href="https://teror.es/" rel="noopener"><img src="/img/logos/ayuntamiento-teror.webp" alt="Ayuntamiento de Teror" loading="lazy" style="height:64px"></a></li>{logos}</ul>
  </div>
</section>'''
    return pagina("Festival En Pie Teror · Festival Internacional de Artes en la Calle",
                  f"Circo, clown, teatro de calle, danza y música en las calles de Teror (Gran Canaria). Programa {ultimo}, archivo de compañías y convocatoria {EDICION_CONVOCATORIA} abierta.",
                  "/", cuerpo, extra_head=f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n')


# ---------------------------------------------------------------- programa
def hora(dt):
    return f"{dt:%H:%M}"


def chips_generos(gs):
    return "".join(f'<span class="etiqueta etiqueta-{g}">{esc(NOMBRE_GENERO.get(g, g))}</span>' for g in gs)


def tarjeta_funcion(f):
    c, e, esp = f["c"], f["e"], f["esp"]
    lugar = esp["nombre"] + (f" · {f['nota']}" if f.get("nota") else "")
    meta = [lugar] + ([f"{e['duracion']} min"] if e.get("duracion") else []) + ([e["edad"]] if e.get("edad") else [])
    texto = plano(" ".join([c["nombre"], e.get("titulo", ""), lugar, " ".join(e.get("disciplinas", [])), c.get("procedencia", "")]))
    foto = img(e["imagen"], "", [400], "96px") if e.get("imagen") else '<span class="sin-foto" aria-hidden="true"></span>'
    return f'''<li class="funcion" id="f-{f["id"]}" data-id="{f["id"]}" data-dia="{f["dia"].isoformat()}" data-espacio="{esp["id"]}" data-compania="{c["id"]}"
 data-generos="{" ".join(e.get("generos", []))}" data-inicio="{f["inicio_dt"]:%Y-%m-%dT%H:%M}" data-fin="{f["fin_dt"]:%Y-%m-%dT%H:%M}"
 data-titulo="{esc(c["nombre"] + " · " + e.get("titulo", ""))}" data-lugar="{esc(lugar)}" data-url="/companias/{c["id"]}" data-texto="{esc(texto)}">
  <time class="funcion-hora" datetime="{f["inicio_dt"]:%Y-%m-%dT%H:%M}">{hora(f["inicio_dt"])}<small>{hora(f["fin_dt"])}</small></time>
  <a class="funcion-foto" href="/companias/{c["id"]}" tabindex="-1" aria-hidden="true">{foto}</a>
  <div class="funcion-cuerpo">
    <a class="funcion-compania" href="/companias/{c["id"]}">{esc(c["nombre"])}</a>
    <span class="funcion-titulo">{esc(e.get("titulo", ""))}</span>
    <span class="funcion-meta">{ICO["pin"]}<span>{" · ".join(esc(m) for m in meta)}</span></span>
    <span class="etiquetas">{chips_generos(e.get("generos", []))}</span>
  </div>
  <button class="estrella" type="button" aria-pressed="false" title="Añadir a mi itinerario"><span class="visualmente-oculto">Añadir a mi itinerario: {esc(c["nombre"])}, {hora(f["inicio_dt"])}</span>{ICO["estrella"]}</button>
</li>'''


def pagina_programa(anio, ruta, canonica):
    ed = D.edicion(anio)
    fs = D.funciones_de(anio)
    dias = D.dias_de(anio)
    cs = D.companias_de(anio)
    espacios = [D.por_espacio[i] for i in dict.fromkeys(f["espacio"] for f in sorted(fs, key=lambda f: f["espacio"])) if i in D.por_espacio]
    espacios.sort(key=lambda e: [x["id"] for x in D.espacios].index(e["id"]))
    usados = {g for f in fs for g in f["e"].get("generos", [])}
    bloques = "".join(f'''<section class="dia" data-dia="{d.isoformat()}" aria-labelledby="dia-{d.isoformat()}">
      <h2 class="dia-titulo" id="dia-{d.isoformat()}">{fecha_larga(d).capitalize()}</h2>
      <ol class="funciones">{"".join(tarjeta_funcion(f) for f in fs if f["dia"] == d)}</ol></section>''' for d in dias)
    botones_dia = '<button type="button" class="filtro" data-dia="" aria-pressed="true">Todos los días</button>' + "".join(
        f'<button type="button" class="filtro" data-dia="{d.isoformat()}" aria-pressed="false">{DIAS_CORTOS[d.weekday()]} {d.day}</button>' for d in dias)
    ops_esp = "".join(f'<option value="{e["id"]}">{esc(e["nombre"])}</option>' for e in espacios)
    ops_cia = "".join(f'<option value="{c["id"]}">{esc(c["nombre"])}</option>' for c in cs)
    gen = "".join(f'<button type="button" class="filtro filtro-genero" data-genero="{k}" aria-pressed="false">{t}</button>' for k, t in GENEROS if k in usados)
    anios = "".join(f'<a href="/programa/{a}"{" aria-current=\"page\"" if a == anio else ""}>{a}</a>' for a in D.anios_con_programa())
    mapa = "".join(f'''<li><strong>{esc(e["nombre"])}</strong>
      <a href="https://www.google.com/maps/search/?api=1&amp;query={f'{e["lat"]},{e["lng"]}' if e.get("lat") else esc(e["direccion"]).replace(" ", "+")}" rel="noopener">Cómo llegar {ICO["flecha"]}</a></li>''' for e in espacios if e["id"] != "itinerante")
    titulo = f"Programa {anio}"
    cuerpo = f'''
<section class="portada portada-corta portada-programa" aria-labelledby="titulo-programa">
  <figure class="portada-foto">{img("img/fotos/puja-asteroide", "", [900, 1600], "100vw", carga="eager", prioridad=True)}</figure>
  <div class="contenedor">
    <p class="pildora">{esc(ed.get("numero", ""))} edición · {fechas_texto(dias)}</p>
    <h1 class="titular" id="titulo-programa">{titulo}</h1>
    <p class="portada-lema">{len(fs)} funciones de {len(cs)} compañías en {len(espacios)} espacios de Teror. Gratis y en la calle. Filtra por día, espacio, compañía o género y marca con la estrella lo que no te quieres perder: así montas <strong>tu propio itinerario</strong>.</p>
    <nav class="anios-programa" aria-label="Otras ediciones">{anios}</nav>
  </div>
  {ONDA}
</section>
<section class="seccion programa" data-anio="{anio}">
  <div class="contenedor">
    <form class="barra-filtros" role="search" onsubmit="return false">
      <div class="barra-fila">
        <label class="buscador"><span class="visualmente-oculto">Buscar</span>{ICO["buscar"]}<input type="search" id="p-q" placeholder="Busca compañía, espectáculo, espacio…" autocomplete="off"></label>
        <label class="selector"><span>Espacio</span><select id="p-espacio"><option value="">Todos los espacios</option>{ops_esp}</select></label>
        <label class="selector"><span>Compañía</span><select id="p-compania"><option value="">Todas las compañías</option>{ops_cia}</select></label>
      </div>
      <div class="barra-fila" role="group" aria-label="Día">{botones_dia}</div>
      <div class="barra-fila" role="group" aria-label="Género">{gen}</div>
    </form>
    <div class="barra-estado">
      <div class="vistas" role="tablist" aria-label="Vista">
        <button type="button" role="tab" id="tab-programa" aria-selected="true" aria-controls="vista-programa">Programa</button>
        <button type="button" role="tab" id="tab-itinerario" aria-selected="false" aria-controls="vista-itinerario">{ICO["estrella"]} Mi itinerario <span class="contador" id="contador-itinerario">0</span></button>
      </div>
      <p class="resultado"><span role="status" aria-live="polite" id="p-cuenta">{len(fs)} funciones</span> <button type="button" class="limpiar" id="p-limpiar" hidden>Quitar filtros</button></p>
    </div>
    <div id="vista-programa" role="tabpanel" aria-labelledby="tab-programa">
      {bloques}
      <p class="vacio" id="p-vacio" hidden>No hay funciones con esos filtros. <button type="button" class="limpiar" data-limpiar>Quitar filtros</button></p>
    </div>
    <div id="vista-itinerario" role="tabpanel" aria-labelledby="tab-itinerario" hidden>
      <div class="aviso-compartido" id="it-compartido" hidden><p>Te han pasado un itinerario con <strong id="it-compartido-n"></strong> funciones.</p>
        <button type="button" class="boton boton-coral" id="it-guardar">Guardarlo como mi itinerario</button></div>
      <div class="itinerario-acciones" id="it-acciones" hidden>
        <button type="button" class="boton boton-tinta" id="it-compartir">{ICO["compartir"]} Compartir</button>
        <button type="button" class="boton boton-tinta" id="it-calendario">{ICO["cal"]} Añadir al calendario</button>
        <button type="button" class="boton boton-claro-tinta" id="it-vaciar">{ICO["papelera"]} Vaciar</button>
        <span class="estado-it" id="it-estado" role="status" aria-live="polite"></span>
      </div>
      <div id="it-lista"></div>
      <div class="vacio" id="it-vacio"><p><strong>Tu itinerario está vacío.</strong></p><p>Pulsa la estrella {ICO["estrella"]} de las funciones que quieras ver y aquí te las ordenamos por hora, con aviso si dos se pisan.</p></div>
      <p class="nota-it">Tu itinerario se guarda solo en este navegador. Para tenerlo en otro móvil, usa «Compartir».</p>
    </div>
  </div>
</section>
<section class="seccion papel" aria-labelledby="titulo-mapa">
  <div class="contenedor">
    <div class="cabecera"><span class="antetitulo">Los espacios</span><h2 id="titulo-mapa">Dónde está cada escenario</h2>
      <p>Todo está a pocos minutos a pie por el casco histórico de Teror.</p></div>
    <ul class="lista-espacios">{mapa}</ul>
  </div>
</section>'''
    return pagina(f"{titulo} · Festival En Pie Teror", f"Programa {anio} del Festival En Pie Teror: {len(fs)} funciones de circo, clown, teatro de calle y música. Horarios, espacios y tu propio itinerario.",
                  ruta, cuerpo, canonica=canonica)


# ---------------------------------------------------------------- compañías
def pagina_companias():
    anios = D.anios_con_programa()
    botones_anio = '<button type="button" class="filtro" data-anio="" aria-pressed="true">Todos los años</button>' + "".join(
        f'<button type="button" class="filtro" data-anio="{a}" aria-pressed="false">{a}</button>' for a in anios)
    tarjetas = "".join(tarjeta_compania(c) for c in D.companias if c["anios"])
    cuerpo = f'''
<section class="portada portada-corta" aria-labelledby="titulo-archivo">
  <figure class="portada-foto">{img("img/fotos/sacude", "", [1200, 2400], "100vw", carga="eager", prioridad=True)}</figure>
  <div class="contenedor">
    <p class="pildora">{len(D.companias)} compañías · {", ".join(map(str, sorted(anios)))}</p>
    <h1 class="titular" id="titulo-archivo">Quién ha pasado por En Pie</h1>
    <p class="portada-lema">El archivo de compañías y artistas del festival: sus espectáculos, vídeos y las funciones que hicieron en Teror.</p>
  </div>
  {ONDA}
</section>
<section class="seccion archivo">
  <div class="contenedor">
    <form class="barra-filtros" role="search" onsubmit="return false">
      <div class="barra-fila"><label class="buscador"><span class="visualmente-oculto">Buscar</span>{ICO["buscar"]}<input type="search" id="a-q" placeholder="Busca por nombre, espectáculo o procedencia…" autocomplete="off"></label></div>
      <div class="barra-fila" role="group" aria-label="Edición">{botones_anio}</div>
      <div class="barra-fila" role="group" aria-label="Género">{botones_generos()}</div>
    </form>
    <p class="resultado"><span role="status" aria-live="polite" id="a-cuenta">{len(D.companias)} compañías</span></p>
    <ul class="companias" id="archivo">{tarjetas}</ul>
    <p class="vacio" id="a-vacio" hidden>Ninguna compañía con esos filtros.</p>
  </div>
</section>'''
    return pagina("Compañías y artistas · Festival En Pie Teror", "Archivo de compañías y artistas que han actuado en el Festival En Pie Teror: espectáculos, vídeos y funciones.",
                  "/companias", cuerpo)


def video_html(v, titulo, poster):
    if not v:
        return ""
    if v["tipo"] in ("youtube", "vimeo"):
        fondo = img(poster, f"Vídeo de {titulo}", [800], "(max-width:900px) 100vw, 640px") if poster else ""
        return f'''<div class="video" data-video="{esc(v["id"])}" data-tipo="{v["tipo"]}" data-titulo="Vídeo: {esc(titulo)}">{fondo}
          <button type="button" aria-label="Reproducir el vídeo de {esc(titulo)}"><span>{ICO["play"]}</span></button></div>
        <p class="nota-video">Al pulsar se carga el reproductor de {"YouTube en su modo sin cookies" if v["tipo"] == "youtube" else "Vimeo"}. <a href="{esc(v["url"])}" rel="noopener">Verlo en {"YouTube" if v["tipo"] == "youtube" else "Vimeo"}</a></p>'''
    return f'<p><a class="boton boton-tinta" href="{esc(v["url"])}" rel="noopener">{ICO["play"]} Ver el vídeo</a></p>'


def parrafos(t):
    return "".join(f"<p>{esc(p).replace(chr(10), '<br>')}</p>" for p in (t or "").split("\n\n") if p.strip())


def pagina_compania(c, anterior, siguiente):
    portada = c["espectaculos"][0]["imagen"] if c["espectaculos"] else c["imagen"]
    anios = "".join(f'<a href="/programa/{a}">{a}</a>' for a in c["anios"])
    bloques = []
    for e in c["espectaculos"]:
        fs = [f for f in c["funciones"] if f["espectaculo"] == e["id"]]
        lista = "".join(f'''<li><a href="/programa/{f["edicion"]}#f-{f["id"]}"><strong>{f["edicion"]}</strong> · {fecha_larga(f["dia"])} · {hora(f["inicio_dt"])}</a>
          <span>{esc(f["esp"]["nombre"])}{" · " + esc(f["nota"]) if f.get("nota") else ""}</span></li>''' for f in fs)
        datos = [x for x in [e.get("edad"), f'{e["duracion"]} minutos' if e.get("duracion") else None] if x]
        bloques.append(f'''<article class="espectaculo-ficha aparece" id="{e["id"]}">
      <div class="espectaculo-texto">
        <span class="antetitulo">{" · ".join(map(str, e["anios"]))}</span>
        <h2>{esc(e["titulo"])}</h2>
        <p class="disciplinas">{"".join(f"<span>{esc(d)}</span>" for d in e.get("disciplinas", []))}</p>
        {f'<p class="frase">{esc(e["frase"])}</p>' if e.get("frase") else ""}
        <ul class="datos-espectaculo">{"".join(f"<li>{esc(d)}</li>" for d in datos)}</ul>
        {f'<h3>De qué va</h3>{parrafos(e["sinopsis"])}' if e.get("sinopsis") else ""}
        {f'<h3>Qué vas a ver</h3>{parrafos(e["descripcion"])}' if e.get("descripcion") else ""}
      </div>
      <div class="espectaculo-lado">
        {video_html(e.get("video"), e["titulo"], e.get("imagen")) or (img(e["imagen"], f'{c["nombre"]}, {e["titulo"]}', [400, 800], "(max-width:900px) 100vw, 480px", clase="foto-espectaculo") if e.get("imagen") and e["imagen"] != portada else "")}
        {f'<h3>Funciones en En Pie</h3><ul class="funciones-ficha">{lista}</ul>' if lista else ""}
      </div>
    </article>''')
    redes = "".join(f'<a class="boton boton-claro" href="{esc(u)}" rel="noopener">{t}</a>' for u, t in [(c.get("web"), "Web"), (c.get("instagram"), "Instagram")] if u)
    nav = (f'<a href="/companias/{anterior["id"]}" rel="prev">{ICO["atras"]} {esc(anterior["nombre"])}</a>' if anterior else "<span></span>") + \
          (f'<a href="/companias/{siguiente["id"]}" rel="next">{esc(siguiente["nombre"])} {ICO["flecha"]}</a>' if siguiente else "<span></span>")
    ld = {"@context": "https://schema.org", "@type": "PerformingGroup", "name": c["nombre"], "url": f"{DOMINIO}/companias/{c['id']}"}
    if portada:
        ld["image"] = f"{DOMINIO}/{portada}-800.webp"
    desc = (c["espectaculos"][0].get("frase") or c["espectaculos"][0].get("sinopsis") or "")[:180] if c["espectaculos"] else ""
    cuerpo = f'''
<section class="ficha-portada" aria-labelledby="titulo-ficha">
  <div class="contenedor ficha-grid">
    <div class="ficha-foto">{img(portada, c["nombre"], [400, 800], "(max-width:900px) 100vw, 520px", carga="eager", prioridad=True) if portada else '<span class="sin-foto"></span>'}</div>
    <div class="ficha-texto">
      <a class="volver" href="/companias">{ICO["atras"]} Todas las compañías</a>
      <span class="antetitulo">{esc(c["procedencia"])}</span>
      <h1 id="titulo-ficha">{esc(c["nombre"])}</h1>
      <p class="ficha-espectaculos">{" · ".join(esc(e["titulo"]) for e in c["espectaculos"])}</p>
      <p class="etiquetas">{chips_generos(c["generos"])}</p>
      <p class="ficha-anios">En En Pie: {anios}</p>
      {f'<div class="botones">{redes}</div>' if redes else ""}
    </div>
  </div>
</section>
<section class="seccion ficha-cuerpo"><div class="contenedor">{"".join(bloques)}
  <nav class="ficha-nav" aria-label="Otras compañías">{nav}</nav></div></section>'''
    return pagina(f"{c['nombre']} · Festival En Pie Teror", desc or f"{c['nombre']} en el Festival En Pie Teror.", f"/companias/{c['id']}", cuerpo,
                  extra_head=f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n',
                  og=f"/{portada}-800.webp" if portada else "/img/og-en-pie-teror.jpg")


# ---------------------------------------------------------------- legales
TITULAR = '''<table>
<tr><th scope="row">Titular</th><td>Ayuntamiento de Teror</td></tr>
<tr><th scope="row">CIF</th><td>P3502700B</td></tr>
<tr><th scope="row">Domicilio</th><td>Plaza Muro Nuevo, 2 · 35330 Teror (Las Palmas)</td></tr>
<tr><th scope="row">Teléfono</th><td><a href="tel:+34928630075">928 630 075</a></td></tr>
<tr><th scope="row">Email</th><td><a href="mailto:ayuntamiento@teror.es">ayuntamiento@teror.es</a></td></tr>
<tr><th scope="row">Sitio web</th><td>festivalenpieteror.com</td></tr>
</table>'''

AVISO = f'''<h2>1. Datos del titular</h2>
<p>En cumplimiento del artículo 10 de la Ley 34/2002, de Servicios de la Sociedad de la Información y de Comercio Electrónico (LSSI-CE), se informa de los datos del titular de este sitio web:</p>
{TITULAR}
<h2>2. Objeto</h2>
<p>Esta web informa sobre el Festival Internacional de Artes en la Calle En Pie Teror, organizado por el Ayuntamiento de Teror, y recoge las inscripciones de compañías y artistas que quieren participar en próximas ediciones.</p>
<h2>3. Condiciones de uso</h2>
<p>El acceso a la web es libre y gratuito. Quien la visita se compromete a hacer un uso adecuado de sus contenidos y a no emplearlos para actividades ilícitas o contrarias a la buena fe. Enviar una inscripción no supone ningún compromiso de contratación por parte del festival.</p>
<h2>4. Propiedad intelectual e industrial</h2>
<p>Los textos, fotografías, logotipos y diseño de esta web pertenecen al Ayuntamiento de Teror o a terceros que han autorizado su uso, incluidas las compañías participantes en las imágenes de sus espectáculos. Queda prohibida su reproducción sin autorización, salvo para uso personal o para la difusión informativa del festival citando la fuente. Las marcas y logotipos de las entidades colaboradoras pertenecen a sus titulares.</p>
<h2>5. Responsabilidad</h2>
<p>El Ayuntamiento de Teror procura que la información publicada sea correcta y esté actualizada, pero puede haber cambios de programación ajenos a su voluntad. La web contiene enlaces a sitios de terceros, de cuyos contenidos no se hace responsable.</p>
<h2>6. Protección de datos y cookies</h2>
<p>El tratamiento de datos personales se explica en la <a href="/privacidad.html">política de privacidad</a> y el uso de cookies en la <a href="/cookies.html">política de cookies</a>.</p>
<h2>7. Legislación aplicable</h2>
<p>Estas condiciones se rigen por la legislación española.</p>'''

PRIVACIDAD = f'''<p>Esta política explica cómo se tratan los datos personales que se facilitan a través de esta web, de acuerdo con el Reglamento (UE) 2016/679 (RGPD) y la Ley Orgánica 3/2018 de Protección de Datos Personales y garantía de los derechos digitales (LOPDGDD).</p>
<h2>1. Responsable del tratamiento</h2>
{TITULAR}
<h2>2. Qué datos se tratan</h2>
<p><strong>Formulario de inscripción de compañías:</strong> nombre de la compañía y sus datos públicos (web, redes, procedencia), los datos de la persona de contacto (nombre, función, correo y teléfono), la información de los espectáculos, los nombres y funciones de los miembros que se indiquen, el caché orientativo y las observaciones. Pedimos que no se incluyan documentos de identidad, datos bancarios ni datos de salud: solo se solicitarán, si procede, en el momento de la contratación.</p>
<p><strong>Correos que nos envíe:</strong> los datos que contenga el mensaje.</p>
<p>La web no instala cookies de analítica ni de publicidad. Puede utilizarse Cloudflare Web Analytics, que mide visitas de forma agregada sin cookies.</p>
<h2>3. Finalidad y base legal</h2>
<ul>
<li><strong>Valorar la propuesta artística y contactar con la compañía</strong> para la programación del festival: consentimiento de la persona que envía el formulario y aplicación de medidas precontractuales a petición del interesado (art. 6.1.a y 6.1.b RGPD).</li>
<li><strong>Enviar información de próximas convocatorias</strong>, solo si se marca la casilla correspondiente: consentimiento (art. 6.1.a RGPD), que puede retirarse en cualquier momento.</li>
</ul>
<h2>4. Conservación</h2>
<p>Las propuestas se conservan durante la edición a la que se presentan y las tres siguientes, para poder valorarlas en futuras programaciones, salvo que se pida antes su supresión. Los datos para enviar convocatorias, hasta que se retire el consentimiento.</p>
<h2>5. Destinatarios</h2>
<p>No se ceden datos a terceros salvo obligación legal. Acceden a ellos, como encargados del tratamiento y con contrato conforme al art. 28 RGPD, la empresa que presta al Ayuntamiento el servicio de producción y gestión del festival y los proveedores tecnológicos de alojamiento (Cloudflare, Inc., con garantías adecuadas para transferencias internacionales).</p>
<h2>6. Sus derechos</h2>
<p>Puede ejercer los derechos de acceso, rectificación, supresión, oposición, limitación del tratamiento y portabilidad, y retirar el consentimiento, escribiendo a <a href="mailto:ayuntamiento@teror.es">ayuntamiento@teror.es</a> o por registro en el Ayuntamiento de Teror. Si considera que sus derechos no se han respetado, puede reclamar ante la Agencia Española de Protección de Datos (<a href="https://www.aepd.es/" rel="noopener">aepd.es</a>).</p>'''

COOKIES = '''<p>Esta web no utiliza cookies propias ni de terceros con fines de analítica, publicidad o seguimiento, por lo que no muestra aviso de cookies.</p>
<h2>Qué puede almacenarse</h2>
<p>Las cookies técnicas estrictamente necesarias que pueda requerir el servicio de alojamiento (Cloudflare) para la seguridad de la web, exentas de consentimiento (art. 22.2 LSSI-CE). El formulario de inscripción guarda un borrador en el propio navegador (almacenamiento local) para no perder lo escrito; no se envía a ningún sitio hasta que se pulsa «Enviar» y se borra al enviarlo.</p>
<h2>Vídeo de YouTube</h2>
<p>El vídeo solo se carga si se pulsa en él, y lo hace en el modo de privacidad mejorada de YouTube (youtube-nocookie.com).</p>
<h2>Cómo gestionarlas</h2>
<p>Puede borrar o bloquear las cookies y el almacenamiento local desde la configuración de su navegador.</p>'''


def legal(slug, titulo, desc, contenido):
    cuerpo = f'<section class="legal"><div class="contenedor"><h1>{titulo}</h1><p class="actualizado">Última actualización: noviembre de 2026.</p>{contenido}</div></section>'
    return pagina(f"{titulo} · Festival En Pie Teror", desc, f"/{slug}.html", cuerpo)


def no_encontrada():
    cuerpo = f'''<section class="seccion oscuro" style="min-height:62vh"><div class="contenedor">
      <span class="antetitulo">Error 404</span><h1 style="font-size:clamp(2.6rem,6vw,4.4rem)">Este espectáculo se ha ido de gira</h1>
      <p>La página que busca no existe o ha cambiado con la nueva web.</p>
      <div class="botones"><a class="boton boton-coral" href="/">Volver al inicio {ICO["flecha"]}</a><a class="boton boton-claro" href="/inscripcion">Inscribe tu compañía</a></div></div></section>'''
    return pagina("Página no encontrada · Festival En Pie Teror", "La página que busca no existe.", "/404.html", cuerpo)


def pagina_inscripcion():
    cuerpo = f'''
<section class="portada portada-corta" aria-labelledby="titulo-inscripcion">
  <figure class="portada-foto">{img("img/fotos/puja-asteroide", "", [900, 1600], "100vw", carga="eager", prioridad=True)}</figure>
  <div class="contenedor">
    <p class="pildora">Convocatoria {EDICION_CONVOCATORIA} · abierta</p>
    <h1 class="titular" id="titulo-inscripcion" style="max-width:14ch">Inscribe tu compañía en En Pie {EDICION_CONVOCATORIA}</h1>
    <p class="portada-lema">Circo, clown, teatro de calle, danza, música y espectáculos itinerantes. Tarda unos 10 minutos y lo que escribas se guarda en tu navegador por si lo dejas a medias.</p>
  </div>
  {ONDA}
</section>
<section class="seccion" aria-label="Formulario de inscripción">
  <div class="contenedor" style="max-width:980px">
    <ol class="pasos aparece">
      <li><strong>Rellena la ficha</strong> con tu espectáculo y un enlace al vídeo.</li>
      <li><strong>La revisamos</strong>: el equipo del festival valora todas las propuestas.</li>
      <li><strong>Te llamamos</strong> si tu espectáculo encaja en la programación.</li>
    </ol>
    {formulario()}
    <p style="margin-top:28px"><a href="/">← Volver al festival</a></p>
  </div>
</section>'''
    return pagina(f"Inscripción de compañías {EDICION_CONVOCATORIA} · Festival En Pie Teror",
                  f"Convocatoria abierta para compañías y artistas de artes de calle: preséntate al Festival En Pie Teror {EDICION_CONVOCATORIA} (Gran Canaria).",
                  "/inscripcion", cuerpo)


def redirecciones():
    """_redirects: direcciones de la antigua web de Wix -> nueva web."""
    import urllib.parse
    lineas = ["# Generado por scripts/generar.py: no editar a mano", "# Direcciones de la antigua web de Wix",
              "/general-6 /#teror 301", "/s-projects-side-by-side /companias 301", "/compania-galeria /companias 301",
              "/compania-galeria/* /companias 301", "/companias-y-artistas-y-horarios /programa 301", "/companias-y-artistas-y-horarios/* /programa 301",
              "/events/* /programa 301", "/_files/ugd/* /programa/programa-en-pie-teror-2026.pdf 301",
              "/pol* /privacidad.html 301", "/t*rminos-y-condiciones /aviso-legal.html 301"]
    p = RAIZ / "data/redirecciones-wix.json"
    if p.exists():
        vistos = set()
        for viejo, nuevo in json.loads(p.read_text(encoding="utf-8")).items():
            for forma in (urllib.parse.quote(viejo, safe="-'()._~"), viejo):
                if forma not in vistos and " " not in forma:
                    vistos.add(forma)
                    lineas.append(f"/companias/{forma} /companias/{nuevo} 301")
    return "\n".join(lineas) + "\n"


def escribir(ruta, texto):
    p = RAIZ / ruta
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(texto, encoding="utf-8")


def main():
    escribir("index.html", inicio())
    escribir("inscripcion.html", pagina_inscripcion())
    escribir("aviso-legal.html", legal("aviso-legal", "Aviso legal", "Aviso legal de la web del Festival En Pie Teror: datos del titular, el Ayuntamiento de Teror.", AVISO))
    escribir("privacidad.html", legal("privacidad", "Política de privacidad", "Cómo trata el Ayuntamiento de Teror los datos de las inscripciones de compañías y de los correos.", PRIVACIDAD))
    escribir("cookies.html", legal("cookies", "Política de cookies", "Uso de cookies en la web del Festival En Pie Teror.", COOKIES))
    escribir("404.html", no_encontrada())
    urls = ["/", "/inscripcion", "/programa", "/companias", "/aviso-legal.html", "/privacidad.html", "/cookies.html"]
    ultimo = D.ultima_con_programa()
    for a in D.anios_con_programa():
        escribir(f"programa/{a}.html", pagina_programa(a, f"/programa/{a}", f"/programa/{a}"))
        urls.append(f"/programa/{a}")
    if ultimo:
        escribir("programa/index.html", pagina_programa(ultimo, "/programa", f"/programa/{ultimo}"))
    escribir("companias/index.html", pagina_companias())
    con = [c for c in D.companias if c["anios"]]
    for i, c in enumerate(con):
        escribir(f"companias/{c['id']}.html", pagina_compania(c, con[i - 1] if i else None, con[i + 1] if i + 1 < len(con) else None))
        urls.append(f"/companias/{c['id']}")
    # quitar fichas de compañías que ya no existen
    for viejo in (RAIZ / "companias").glob("*.html"):
        if viejo.stem != "index" and viejo.stem not in {c["id"] for c in con}:
            viejo.unlink()
    for viejo in (RAIZ / "programa").glob("*.html"):
        if viejo.stem != "index" and not (viejo.stem.isdigit() and int(viejo.stem) in D.anios_con_programa()):
            viejo.unlink()
    escribir("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
             + "\n".join(f"  <url><loc>{DOMINIO}{u}</loc></url>" for u in urls) + "\n</urlset>\n")
    escribir("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {DOMINIO}/sitemap.xml\n")
    escribir("_redirects", redirecciones())
    print(f"Generadas {len(urls) + 1} páginas")


if __name__ == "__main__":
    main()
