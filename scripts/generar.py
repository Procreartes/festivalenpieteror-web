#!/usr/bin/env python3
"""Genera las páginas HTML de la web del Festival En Pie Teror.

Uso:  python3 scripts/generar.py
Los datos (compañías, cifras, espacios, colaboradores) están arriba de este fichero.
No edites los .html a mano: se sobrescriben.
"""
import html
import json
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
from iconos import ICO  # noqa: E402

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

# (slug de imagen, compañía, espectáculo, disciplina tal como venía, filtros)
COMPANIAS = [
    ("collectif-bislacco", "Collectif Bislacco", "Smooth as Fiasco", "Circo caótico y musical", "circo musica"),
    ("grupo-puja", "Grupo Puja", "Verne", "Teatro, danza y circo aéreo", "teatro circo"),
    ("la-cote-folle", "La Côte Folle", "Entre Bous i Vaques", "Circo, portés, funambulismo y danza", "circo teatro"),
    ("pere-hosta", "Pere Hosta", "Woof", "Clown, humor e impro", "humor"),
    ("jesus-soria", "Jesús Soria", "Hablo más que salto", "Comedia y acrobacia", "humor circo"),
    ("joe-farnarier", "Joe Farnarier", "Invisible", "Danza, teatro y acrobacia", "teatro circo"),
    ("trocos-lucos", "Trocos Lucos", "Tartana", "Báscula y verticales", "circo"),
    ("circo-akroshcan", "Circo Akroshcan", "A-kabaret", "Circo, varieté, danza y teatro", "circo teatro"),
    ("el-gordo-y-el-chapa", "El Gordo y el Chapa", "El último hombre bala", "Circo y clown", "circo humor"),
    ("tadeo-campanotto", "Tadeo Campanotto", "Show de Tadeo", "Malabares, magia y humor", "circo humor"),
    ("giuseppe-salchichone", "Giuseppe Salchichone", "Los retos de Giuseppe Salchichone", "Clown, malabares y magia", "humor circo"),
    ("tami-circo", "Tami Circo", "DJTami", "Rueda cyr, clown, malabares y acrobacias", "circo humor"),
    ("toto-el-payaso", "Totó el Payaso", "El Ring", "Teatro y humor", "humor teatro"),
    ("el-nino-de-la-hipoteca", "El Niño de la Hipoteca", "En concierto", "Música y humor", "musica humor"),
    ("andrea-rodriguez-tropico", "Andrea Rodríguez y la Banda del Trópico", "Trópico de Capri", "Música", "musica"),
    ("aseres", "Aseres", "En concierto", "Música", "musica"),
    ("perrakos-soundsystem", "Perrakos Soundsystem", "Fiestaka en Teror", "Fiestaka", "musica"),
    ("enkassette", "Enkassette", "Concierto", "Música", "musica"),
    ("son-de-la-isla", "Son de la Isla", "Son de la Isla", "Música", "musica"),
    ("la-dixie-de-en-pie", "La Dixie de En Pie", "Dixieland itinerante", "Música por las calles", "musica"),
    ("noelia-mederos", "Noelia Mederos", "En concierto", "Canto", "musica"),
    ("patri-viera", "Patri Viera", "En concierto", "Canto", "musica"),
    ("risoterapia-islas-canarias", "Risoterapia Islas Canarias", "Taller de risoterapia", "Terapia de la risa (taller)", "talleres"),
]
FILTROS = [("todas", "Todas"), ("circo", "Circo"), ("humor", "Clown y humor"), ("teatro", "Teatro y danza"),
           ("musica", "Música"), ("talleres", "Talleres")]
CIFRAS = [("26", "compañías y artistas"), ("42", "funciones en tres días"), ("8", "espacios de Teror convertidos en escenario"),
          ("2", "compañías internacionales"), ("XIII", "ediciones del festival"), ("0 €", "todo gratis y en la calle")]
ESPACIOS = ["Plaza de Sintes", "Plaza Teresa de Bolívar", "Alameda de Pío XII", "Plaza El Pino", "Bulevar",
            "Oficinas Municipales", "Sala Polivalente (Antiguo Ayuntamiento)", "Itinerante por las calles"]
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


def esc(t):
    return html.escape(str(t), quote=True)


def img(ruta, alt, anchos, sizes, carga="lazy", prioridad=False, clase=""):
    srcset = ", ".join(f"/{ruta}-{w}.webp {w}w" for w in anchos)
    return (f'<img src="/{ruta}-{anchos[0]}.webp" srcset="{srcset}" sizes="{sizes}" alt="{esc(alt)}" loading="{carga}" decoding="async"'
            f'{" fetchpriority=\"high\"" if prioridad else ""}{f" class={chr(34)}{clase}{chr(34)}" if clase else ""}>')


def cabecera():
    items = [("/#companias", "Compañías 2026"), ("/#video", "Vídeo"), ("/#espacios", "Espacios"), ("/#sostenibilidad", "Sostenibilidad"),
             ("/#teror", "Teror")]
    lis = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in items)
    return f'''<a class="saltar" href="#contenido">Saltar al contenido</a>
<header class="nav">
  <div class="contenedor">
    <a class="marca" href="/" aria-label="Festival En Pie Teror, ir al inicio"><img src="/img/logos/enpie-color.webp" alt="" width="72" height="44"><small>Festival Internacional de Artes en la Calle</small></a>
    <button class="boton-menu" type="button" aria-controls="menu" aria-expanded="false"><span class="visualmente-oculto">Abrir menú</span>{ICO["menu"]}</button>
    <ul class="menu" id="menu">{lis}<li class="cta"><a href="/#inscripcion">Inscribe tu compañía</a></li></ul>
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


def pagina(titulo, descripcion, ruta, cuerpo, extra_head="", og="/img/og-en-pie-teror.jpg"):
    return f'''<!doctype html>
<html lang="es" class="sin-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titulo)}</title>
<meta name="description" content="{esc(descripcion)}">
<link rel="canonical" href="{DOMINIO}{ruta}">
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
def inicio():
    filtros = "".join(f'<button type="button" class="filtro" data-filtro="{k}" aria-pressed="{"true" if k == "todas" else "false"}">{t}</button>' for k, t in FILTROS)
    tarjetas = "".join(f'''<li class="compania aparece" data-tipos="{tipos}">
      {img(f"img/companias/{slug}", f"{nombre}, {esp}", [400, 800], "(max-width:720px) 50vw, (max-width:1000px) 33vw, 280px")}
      <div class="compania-cuerpo"><h3>{esc(nombre)}</h3><p class="espectaculo">{esc(esp)}</p><p class="disciplina">{esc(disc)}</p></div></li>'''
                       for slug, nombre, esp, disc, tipos in COMPANIAS)
    cifras = "".join(f'<li class="cifra aparece"><strong>{a}</strong><span>{b}</span></li>' for a, b in CIFRAS)
    espacios = "".join(f"<li>{esc(e)}</li>" for e in ESPACIOS)
    ritmos = "".join(f"<span>{r}</span>" for r in ["Circo", "Clown", "Teatro de calle", "Acrobacia", "Danza", "Música", "Humor", "Aéreos", "Pasacalles"])
    logos = "".join(
        (f'<li><a href="{u}" rel="noopener"><img class="{c}" src="/img/logos/{s}.webp" alt="{esc(a)}" loading="lazy"></a></li>' if u
         else f'<li><img class="{c}" src="/img/logos/{s}.webp" alt="{esc(a)}" loading="lazy"></li>') for s, a, u, c in COLABORAN)
    ld = {"@context": "https://schema.org", "@type": "Festival", "name": "XIII Festival Internacional de Artes en la Calle En Pie Teror",
          "startDate": "2026-08-28", "endDate": "2026-08-30", "isAccessibleForFree": True,
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
    <p class="pildora">XIII edición · 28, 29 y 30 de agosto de 2026 · ¡Gracias por llenar las calles!</p>
    <h1 class="titular" id="titulo-portada">Teror se pone <em>en pie</em></h1>
    <p class="portada-lema">Festival Internacional de Artes en la Calle. Circo, clown, teatro de calle, danza y música por las plazas y rincones del casco de Teror, en Gran Canaria. Gratis y para todos los públicos.</p>
    <div class="botones">
      <a class="boton boton-coral" href="#inscripcion">Inscribe tu compañía · {EDICION_CONVOCATORIA} {ICO["flecha"]}</a>
      <a class="boton boton-claro" href="#companias">Compañías 2026</a>
      <a class="boton boton-claro" href="#video">{ICO["play"]} Ver el vídeo</a>
    </div>
  </div>
  {ONDA}
</section>

<div class="cinta" aria-hidden="true"><div class="cinta-pista">{ritmos}{ritmos}</div></div>

<section class="seccion" aria-labelledby="titulo-cifras">
  <div class="contenedor">
    <div class="cabecera aparece"><span class="antetitulo">Así fue 2026</span>
      <h2 id="titulo-cifras">Tres días en los que <span class="subrayado">la calle fue el escenario</span></h2>
      <p>Compañías de Canarias, de la península y de fuera de España llenaron plazas, calles y rincones de la Villa con espectáculos para todos los públicos, sin entradas y a la vuelta de cada esquina.</p></div>
    <ul class="cifras">{cifras}</ul>
  </div>
</section>

<section class="seccion papel" id="companias" aria-labelledby="titulo-companias">
  <div class="contenedor">
    <div class="cabecera aparece"><span class="antetitulo">Compañías y artistas 2026</span>
      <h2 id="titulo-companias">Quién llenó Teror de magia</h2>
      <p>Circo, teatro de calle, humor, teatro gestual, clown, acrobacias y mucha música.</p></div>
    <div class="filtros" role="group" aria-label="Filtrar por disciplina">{filtros}</div>
    <ul class="companias">{tarjetas}</ul>
    <div class="botones" style="margin-top:32px"><a class="boton boton-tinta" href="/programa/programa-en-pie-teror-2026.pdf">{ICO["pdf"]} Programa 2026 en PDF</a></div>
  </div>
</section>

<section class="seccion oscuro" id="video" aria-labelledby="titulo-video">
  <div class="contenedor dos-col">
    <div class="aparece"><span class="antetitulo">El festival en un minuto</span>
      <h2 id="titulo-video" style="font-size:clamp(2.3rem,5vw,3.6rem)">Míralo con tus propios ojos</h2>
      <p>Las compañías de esta edición, en un vídeo. Para más, en nuestro canal de YouTube.</p>
      <div class="botones"><a class="boton boton-claro" href="{YOUTUBE}" rel="noopener">{ICO["yt"]} Canal de YouTube</a></div></div>
    <div class="aparece">
      <div class="video" data-video="{VIDEO_ID}" data-titulo="Vídeo promocional del XIII Festival En Pie Teror">
        {img("img/fotos/video-promo", "Vídeo promocional del XIII Festival En Pie Teror", [800, 1280], "(max-width:900px) 100vw, 560px")}
        <button type="button" aria-label="Reproducir el vídeo"><span>{ICO["play"]}</span></button>
      </div>
      <p class="nota-video">Al pulsar se carga el reproductor de YouTube en su modo sin cookies.</p>
    </div>
  </div>
</section>

<section class="seccion" id="espacios" aria-labelledby="titulo-espacios">
  <div class="contenedor dos-col">
    <figure class="foto-marco aparece">{img("img/fotos/sacude", "Espectáculo del festival ante el público en una calle de Teror", [1200, 2400], "(max-width:900px) 100vw, 560px")}</figure>
    <div class="aparece"><span class="antetitulo">Un pueblo convertido en escenario</span>
      <h2 id="titulo-espacios" style="font-size:clamp(2.3rem,5vw,3.6rem)">Ocho espacios, cientos de miradas</h2>
      <p>En En Pie el teatro sale a buscarte: las funciones se reparten por las plazas y calles del casco histórico, y algunas no se están quietas.</p>
      <ul class="espacios" style="--c:var(--noche)">{"".join(f'<li style="background:#fff;border-color:var(--noche);color:var(--noche)">{esc(e)}</li>' for e in ESPACIOS)}</ul></div>
  </div>
</section>

<section class="seccion convocatoria" id="inscripcion" aria-labelledby="titulo-inscripcion">
  <div class="contenedor">
    <div class="cabecera aparece"><span class="antetitulo">Convocatoria {EDICION_CONVOCATORIA} · abierta</span>
      <h2 id="titulo-inscripcion">¿Quieres actuar en En Pie {EDICION_CONVOCATORIA}?</h2>
      <p>Buscamos compañías y artistas de circo, clown, teatro de calle, danza, música y espectáculos itinerantes para la próxima edición. Cuéntanos tu propuesta: tarda unos 10 minutos y se guarda sola en tu navegador por si lo dejas a medias.</p></div>
    <ol class="pasos aparece">
      <li><strong>Rellena la ficha</strong> con tu espectáculo y un enlace al vídeo.</li>
      <li><strong>La revisamos</strong>: el equipo del festival valora todas las propuestas.</li>
      <li><strong>Te llamamos</strong> si tu espectáculo encaja en la programación.</li>
    </ol>
    {formulario()}
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
    <figure class="foto-marco aparece">{img("img/fotos/valla-2026", "Cartel del XIII Festival En Pie Teror en una valla de la carretera", [840], "(max-width:900px) 100vw, 560px")}</figure>
  </div>
</section>

<section class="colaboran" aria-labelledby="titulo-colaboran">
  <div class="contenedor">
    <h2 id="titulo-colaboran">Organiza y colaboran</h2>
    <ul class="logos"><li><a href="https://teror.es/" rel="noopener"><img src="/img/logos/ayuntamiento-teror.webp" alt="Ayuntamiento de Teror" loading="lazy" style="height:64px"></a></li>{logos}</ul>
  </div>
</section>'''
    return pagina("Festival En Pie Teror · Festival Internacional de Artes en la Calle",
                  "Circo, clown, teatro de calle, danza y música en las calles de Teror (Gran Canaria). XIII edición, 28-30 de agosto de 2026. Convocatoria de compañías 2027 abierta.",
                  "/", cuerpo, extra_head=f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n')


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
      <div class="botones"><a class="boton boton-coral" href="/">Volver al inicio {ICO["flecha"]}</a><a class="boton boton-claro" href="/#inscripcion">Inscribe tu compañía</a></div></div></section>'''
    return pagina("Página no encontrada · Festival En Pie Teror", "La página que busca no existe.", "/404.html", cuerpo)


def escribir(ruta, texto):
    p = RAIZ / ruta
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(texto, encoding="utf-8")


def main():
    escribir("index.html", inicio())
    escribir("aviso-legal.html", legal("aviso-legal", "Aviso legal", "Aviso legal de la web del Festival En Pie Teror: datos del titular, el Ayuntamiento de Teror.", AVISO))
    escribir("privacidad.html", legal("privacidad", "Política de privacidad", "Cómo trata el Ayuntamiento de Teror los datos de las inscripciones de compañías y de los correos.", PRIVACIDAD))
    escribir("cookies.html", legal("cookies", "Política de cookies", "Uso de cookies en la web del Festival En Pie Teror.", COOKIES))
    escribir("404.html", no_encontrada())
    urls = ["/", "/aviso-legal.html", "/privacidad.html", "/cookies.html"]
    escribir("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
             + "\n".join(f"  <url><loc>{DOMINIO}{u}</loc></url>" for u in urls) + "\n</urlset>\n")
    escribir("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {DOMINIO}/sitemap.xml\n")
    print("Generadas 5 páginas")


if __name__ == "__main__":
    main()
