# Festival En Pie Teror — web

Web estática de **festivalenpieteror.com** (titular: Ayuntamiento de Teror). Sustituye a la antigua web de Wix.
Se publica en Cloudflare (Workers con recursos estáticos) conectada a este repositorio: cada cambio en `main` se publica solo.

## Formulario de inscripción de compañías

La sección «Inscribe tu compañía» envía la ficha a `https://portal.grupolivon.com/publico/inscripciones/enpie`.
El portal la guarda en el CRM (Livon Gestión) y aparece en **Portal → Inscripciones de compañías**, donde se valora y se
cambia de estado. La persona de contacto entra sola en Contactos → Personas, sin duplicarse.
La edición a la que se apuntan (2027) y abrir o cerrar la convocatoria se cambian en el portal (`ENPIE_EDICION`,
`ENPIE_INSCRIPCIONES`); el año que se ve en la web, en `EDICION_CONVOCATORIA` de `scripts/generar.py`.

## Cambiar contenidos

Todo está en `scripts/generar.py` (compañías, cifras, espacios, colaboradores, textos y legales).
Después de editar, ejecuta `python3 scripts/generar.py` y sube los cambios. No edites los `.html` a mano.
Imágenes de compañías: `img/companias/NOMBRE-400.webp` y `NOMBRE-800.webp` (cuadradas).

## Imágenes

Se trajeron de Wix con la acción **Traer imágenes de Wix** (`.github/workflows/imagenes-wix.yml`), que las descarga y
guarda en WebP, junto al programa 2026 en PDF (`programa/`).

## Qué incluye

Aviso legal, privacidad y cookies · `sitemap.xml` y `robots.txt` · página 404 · redirecciones de las direcciones antiguas de
Wix (`_redirects`) · imagen para redes · textos ALT · imágenes WebP con carga diferida · tipografías alojadas en la propia web ·
vídeo de YouTube sin cookies que solo se carga al pulsar · cabeceras de seguridad en `_headers` · datos estructurados.
