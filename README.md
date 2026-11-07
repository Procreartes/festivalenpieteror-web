# Festival En Pie Teror — web

Web estática de **festivalenpieteror.com** (titular: Ayuntamiento de Teror). Sustituye a la antigua web de Wix.
Se publica en Cloudflare (Workers con recursos estáticos) conectada a este repositorio: cada cambio en `main` se publica solo.

## Formulario de inscripción de compañías

La sección «Inscribe tu compañía» envía la ficha a `https://portal.grupolivon.com/publico/inscripciones/enpie`.
El portal la guarda en el CRM (Livon Gestión) y aparece en **Portal → Inscripciones de compañías**, donde se valora y se
cambia de estado. La persona de contacto entra sola en Contactos → Personas, sin duplicarse.
La edición a la que se apuntan (2027) y abrir o cerrar la convocatoria se cambian en el portal (`ENPIE_EDICION`,
`ENPIE_INSCRIPCIONES`); el año que se ve en la web, en `EDICION_CONVOCATORIA` de `scripts/generar.py`.

## Programa, compañías y archivo

Compañías, espectáculos, funciones, espacios y ediciones viven en `data/*.json` (se importaron de Wix con
`scripts/importar_wix.py`: ediciones 2024, 2025 y 2026). Se editan desde **Portal → Gestor de webs → Festival En Pie Teror →
Programación y compañías** (funciones a mano o importadas de un CSV, fichas, fotos, espacios y ediciones) y se publican
en un único commit. Salen en la web:

- `/programa` (última edición publicada) y `/programa/AAAA`: filtros por día, espacio, compañía y género, y
  **Mi itinerario** (estrellas, aviso de solapes, compartir por enlace y descargar al calendario). Se guarda en el navegador.
- `/companias`: archivo de todas las compañías por año y género. `/companias/NOMBRE`: ficha con textos, vídeo y funciones.
- Las fichas antiguas de Wix (`/companias/...`) redirigen a las nuevas (`data/redirecciones-wix.json`).

Ediciones: **próxima** = se anuncia en portada y su programa es borrador; **programada** = el programa sale en la web;
**archivo** = ya pasó. Las horas son las reales de Canarias; lo que empieza antes de las 6:00 sale en la noche anterior.

## Cómo se publica

La acción **Publicar la web** (`.github/workflows/publicar.yml`) se lanza al cambiar `data/`, `scripts/` o fotos de
compañías: trae de Wix las fotos que falten, ejecuta `python3 scripts/generar.py` y sube las páginas; Cloudflare publica.
Textos fijos, colaboradores y legales están en `scripts/generar.py`. No edites los `.html` a mano.
Fotos: `img/companias/ID-400|800.webp` y, si un espectáculo tiene la suya, `img/espectaculos/ID--ESPECTACULO-400|800.webp`.

## Qué incluye

Aviso legal, privacidad y cookies · `sitemap.xml` y `robots.txt` · página 404 · redirecciones de las direcciones antiguas de
Wix (`_redirects`) · imagen para redes · textos ALT · imágenes WebP con carga diferida · tipografías alojadas en la propia web ·
vídeo de YouTube sin cookies que solo se carga al pulsar · cabeceras de seguridad en `_headers` · datos estructurados.
