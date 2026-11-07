(function () {
  "use strict";
  try { document.documentElement.classList.remove("sin-js"); } catch (e) {}
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var sinAcentos = function (t) { return String(t || "").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, ""); };

  // Menú móvil
  try {
    var boton = $(".boton-menu"), menu = $("#menu");
    if (boton && menu) {
      var cerrar = function () { menu.classList.remove("abierto"); boton.setAttribute("aria-expanded", "false"); };
      boton.addEventListener("click", function () { boton.setAttribute("aria-expanded", menu.classList.toggle("abierto") ? "true" : "false"); });
      menu.addEventListener("click", function (e) { if (e.target.tagName === "A") cerrar(); });
      document.addEventListener("keydown", function (e) { if (e.key === "Escape") cerrar(); });
    }
  } catch (e) {}

  // Aparición al hacer scroll
  try {
    var el = $$(".aparece");
    if ("IntersectionObserver" in window) {
      var obs = new IntersectionObserver(function (en) {
        en.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add("visible"); obs.unobserve(x.target); } });
      }, { rootMargin: "0px 0px -8% 0px" });
      el.forEach(function (x) { obs.observe(x); });
    } else { el.forEach(function (x) { x.classList.add("visible"); }); }
  } catch (e) {}

  try { var a = $("#anio"); if (a) a.textContent = String(new Date().getFullYear()); } catch (e) {}

  // Filtro de compañías por género (portada) y archivo de compañías (año + género + búsqueda)
  try {
    var archivo = $("#archivo");
    var genero = "todas", anioA = "", qA = "";
    var aplicarCompanias = function () {
      var n = 0;
      $$(".compania").forEach(function (c) {
        var ok = (genero === "todas" || (" " + c.getAttribute("data-tipos") + " ").indexOf(" " + genero + " ") >= 0) &&
          (!anioA || (" " + (c.getAttribute("data-anios") || "") + " ").indexOf(" " + anioA + " ") >= 0) &&
          (!qA || (c.getAttribute("data-texto") || "").indexOf(qA) >= 0);
        c.hidden = !ok; if (ok) n++;
      });
      var cu = $("#a-cuenta"); if (cu) cu.textContent = n + (n === 1 ? " compañía" : " compañías");
      var va = $("#a-vacio"); if (va) va.hidden = n > 0;
    };
    $$(".filtro[data-filtro]").forEach(function (b) {
      b.addEventListener("click", function () {
        genero = b.getAttribute("data-filtro");
        $$(".filtro[data-filtro]").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
        aplicarCompanias();
      });
    });
    if (archivo) {
      $$(".filtro[data-anio]").forEach(function (b) {
        b.addEventListener("click", function () {
          anioA = b.getAttribute("data-anio");
          $$(".filtro[data-anio]").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
          aplicarCompanias();
        });
      });
      var qa = $("#a-q"); if (qa) qa.addEventListener("input", function () { qA = sinAcentos(qa.value.trim()); aplicarCompanias(); });
    }
  } catch (e) {}

  // Vídeos: solo se cargan (YouTube sin cookies / Vimeo) cuando se pulsan
  try {
    $$(".video button").forEach(function (v) {
      v.addEventListener("click", function () {
        var cont = v.parentNode, id = cont.getAttribute("data-video"), tipo = cont.getAttribute("data-tipo") || "youtube";
        var f = document.createElement("iframe");
        f.src = tipo === "vimeo" ? "https://player.vimeo.com/video/" + id + "?autoplay=1&dnt=1" : "https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1&rel=0";
        f.title = cont.getAttribute("data-titulo") || "Vídeo";
        f.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen";
        f.allowFullscreen = true;
        cont.innerHTML = ""; cont.appendChild(f);
      });
    });
  } catch (e) {}

  try { programa(); } catch (e) { if (window.console) console.error(e); }

  // ---------------- Formulario de inscripción ----------------
  var form = $("#form-inscripcion");
  if (!form) return;
  var inicio = Date.now();
  var CLAVE = "enpie-inscripcion-borrador";
  var estado = $(".estado-envio", form);
  var segundo = $("#espectaculo-2"), anadir = $("#anadir-espectaculo"), quitar = $("#quitar-espectaculo");

  function mostrarSegundo(si) {
    if (!segundo) return;
    segundo.hidden = !si;
    if (anadir) anadir.hidden = si;
    $$("[data-req2]", segundo).forEach(function (x) { x.required = si; });
  }
  if (anadir) anadir.addEventListener("click", function () { mostrarSegundo(true); var t = $("input", segundo); if (t) t.focus(); });
  if (quitar) quitar.addEventListener("click", function () { mostrarSegundo(false); });

  // Máximo 4 disciplinas por espectáculo
  $$(".chips[data-max]").forEach(function (grupo) {
    var max = Number(grupo.getAttribute("data-max"));
    grupo.addEventListener("change", function () {
      var marcadas = $$("input:checked", grupo).length;
      $$("input", grupo).forEach(function (i) { i.disabled = !i.checked && marcadas >= max; });
    });
  });

  // Borrador en este navegador (por si se cierra la pestaña a medias)
  function guardarBorrador() {
    try {
      var d = {};
      $$("input,select,textarea", form).forEach(function (i) {
        if (!i.name || i.type === "hidden" || i.name === "web_empresa") return;
        if (i.type === "checkbox") { if (i.checked) (d[i.name] = d[i.name] || []).push(i.value); }
        else d[i.name] = i.value;
      });
      d._dos = segundo && !segundo.hidden;
      localStorage.setItem(CLAVE, JSON.stringify(d));
    } catch (e) {}
  }
  try {
    var b = JSON.parse(localStorage.getItem(CLAVE) || "null");
    if (b) {
      $$("input,select,textarea", form).forEach(function (i) {
        if (!(i.name in b)) return;
        if (i.type === "checkbox") i.checked = (b[i.name] || []).indexOf(i.value) >= 0;
        else i.value = b[i.name];
      });
      mostrarSegundo(Boolean(b._dos));
      $$(".chips[data-max]").forEach(function (g) { g.dispatchEvent(new Event("change")); });
    }
  } catch (e) {}
  form.addEventListener("input", guardarBorrador);
  form.addEventListener("change", guardarBorrador);

  var val = function (n) { var i = form.elements[n]; return i ? String(i.value || "").trim() : ""; };
  var marcadas = function (n) { return $$('input[name="' + n + '"]:checked', form).map(function (i) { return i.value; }); };
  function espectaculo(s) {
    var disc = marcadas("disciplinas" + s);
    var otra = val("disciplinas_otra" + s);
    if (otra) disc.push(otra);
    return {
      titulo: val("titulo" + s), disciplinas: disc.join(", "), edad: val("edad" + s), duracion: val("duracion" + s),
      formato: val("formato" + s), espacio: val("espacio" + s), personas: val("personas" + s), estreno: val("estreno" + s),
      sinopsis: val("sinopsis" + s), descripcion: val("descripcion" + s), prensa: val("prensa" + s),
      video: val("video" + s), materiales: val("materiales" + s), tecnica: val("tecnica" + s)
    };
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    $$(".invalido", form).forEach(function (x) { x.classList.remove("invalido"); });
    var malos = $$("input,select,textarea", form).filter(function (i) { return !i.disabled && !i.closest("[hidden]") && !i.checkValidity(); });
    var sinDisc = [""].concat(segundo && !segundo.hidden ? ["2"] : []).filter(function (s) { return !marcadas("disciplinas" + s).length && !val("disciplinas_otra" + s); });
    sinDisc.forEach(function (s) { var g = $('[data-grupo="disciplinas' + s + '"]', form); if (g) malos.push(g); });
    if (malos.length) {
      malos.forEach(function (i) { i.classList.add("invalido"); });
      estado.className = "estado-envio error";
      estado.textContent = "Revisa los campos marcados en rojo" + (sinDisc.length ? " (elige al menos una disciplina)" : "") + ".";
      malos[0].scrollIntoView({ behavior: "smooth", block: "center" });
      if (malos[0].focus) malos[0].focus({ preventScroll: true });
      return;
    }
    var esps = [espectaculo("")];
    if (segundo && !segundo.hidden && val("titulo2")) esps.push(espectaculo("2"));
    var datos = {
      compania: { nombre: val("compania"), procedencia: val("procedencia"), municipio: val("municipio"), cif: val("cif"),
        web: val("web"), instagram: val("instagram"), otras_redes: val("otras_redes") },
      contacto: { nombre: val("contacto"), cargo: val("cargo"), email: val("email"), telefono: val("telefono") },
      espectaculos: esps, miembros: val("miembros"), cache: val("cache"), observaciones: val("observaciones"),
      acepta_privacidad: form.elements.privacidad.checked, acepta_comunicaciones: form.elements.comunicaciones.checked,
      web_empresa: val("web_empresa"), _t: Date.now() - inicio
    };
    var btn = $("button[type=submit]", form);
    btn.disabled = true; estado.className = "estado-envio"; estado.textContent = "Enviando…";
    fetch(form.getAttribute("action"), { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(datos) })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, j: j }; }); })
      .then(function (r) {
        if (!r.ok) throw new Error(r.j.error || "No se ha podido enviar.");
        try { localStorage.removeItem(CLAVE); } catch (e) {}
        var g = $("#gracias");
        if (g) {
          var ref = $(".ref", g); if (ref && r.j.referencia) ref.textContent = "Referencia " + r.j.referencia; else if (ref) ref.remove();
          form.hidden = true; g.hidden = false; g.scrollIntoView({ behavior: "smooth", block: "center" });
        }
      })
      .catch(function (err) {
        estado.className = "estado-envio error";
        estado.textContent = (err && err.message && err.message !== "Failed to fetch") ? err.message : "No hemos podido conectar. Revisa tu conexión y vuelve a intentarlo.";
      })
      .then(function () { btn.disabled = false; });
  });

  // ---------------- Programa: filtros, «ahora» y mi itinerario ----------------
  function programa() {
    var raiz = $(".programa");
    if (!raiz) return;
    var CLAVE_IT = "enpie-itinerario";
    var funciones = $$(".funcion", raiz);
    var porId = {};
    funciones.forEach(function (f) { porId[f.getAttribute("data-id")] = f; });
    var estado = { q: "", dia: "", espacio: "", compania: "", generos: [], vista: "programa" };
    var q = $("#p-q"), selEsp = $("#p-espacio"), selCia = $("#p-compania");

    // --- itinerario guardado (solo en este navegador)
    var leer = function () { try { return JSON.parse(localStorage.getItem(CLAVE_IT) || "[]").filter(function (x) { return typeof x === "string"; }); } catch (e) { return []; } };
    var mio = leer();
    var guardar = function () { try { localStorage.setItem(CLAVE_IT, JSON.stringify(mio)); } catch (e) {} };
    var compartido = null;

    // --- estado <-> URL
    var leerURL = function () {
      var p = new URLSearchParams(location.search);
      estado.q = p.get("q") || ""; estado.dia = p.get("dia") || ""; estado.espacio = p.get("espacio") || "";
      estado.compania = p.get("compania") || ""; estado.generos = (p.get("genero") || "").split(",").filter(Boolean);
      estado.vista = p.get("vista") === "itinerario" || p.get("it") ? "itinerario" : "programa";
      var it = p.get("it");
      compartido = it ? it.split(",").filter(function (id) { return porId[id]; }) : null;
    };
    var escribirURL = function () {
      var p = new URLSearchParams();
      if (estado.q) p.set("q", estado.q);
      if (estado.dia) p.set("dia", estado.dia);
      if (estado.espacio) p.set("espacio", estado.espacio);
      if (estado.compania) p.set("compania", estado.compania);
      if (estado.generos.length) p.set("genero", estado.generos.join(","));
      if (estado.vista === "itinerario") p.set("vista", "itinerario");
      if (compartido) p.set("it", compartido.join(","));
      var u = location.pathname + (p.toString() ? "?" + p.toString() : "") + location.hash;
      try { history.replaceState(null, "", u); } catch (e) {}
    };

    // --- filtros
    var hayFiltros = function () { return !!(estado.q || estado.dia || estado.espacio || estado.compania || estado.generos.length); };
    var aplicar = function () {
      var n = 0, qq = sinAcentos(estado.q.trim());
      funciones.forEach(function (f) {
        var gs = " " + f.getAttribute("data-generos") + " ";
        var ok = (!estado.dia || f.getAttribute("data-dia") === estado.dia) &&
          (!estado.espacio || f.getAttribute("data-espacio") === estado.espacio) &&
          (!estado.compania || f.getAttribute("data-compania") === estado.compania) &&
          (!estado.generos.length || estado.generos.some(function (g) { return gs.indexOf(" " + g + " ") >= 0; })) &&
          (!qq || (f.getAttribute("data-texto") || "").indexOf(qq) >= 0);
        f.hidden = !ok; if (ok) n++;
      });
      $$(".dia", raiz).forEach(function (d) { d.hidden = !$(".funcion:not([hidden])", d); });
      $("#p-cuenta").textContent = n + (n === 1 ? " función" : " funciones");
      $("#p-vacio").hidden = n > 0;
      $("#p-limpiar").hidden = !hayFiltros();
      $$("[data-dia]", $(".barra-filtros")).forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-dia") === estado.dia ? "true" : "false"); });
      $$("[data-genero]", raiz).forEach(function (b) { b.setAttribute("aria-pressed", estado.generos.indexOf(b.getAttribute("data-genero")) >= 0 ? "true" : "false"); });
      if (q.value !== estado.q) q.value = estado.q;
      selEsp.value = estado.espacio; selCia.value = estado.compania;
      escribirURL();
    };
    q.addEventListener("input", function () { estado.q = q.value; aplicar(); });
    selEsp.addEventListener("change", function () { estado.espacio = selEsp.value; aplicar(); });
    selCia.addEventListener("change", function () { estado.compania = selCia.value; aplicar(); });
    $$("[data-dia]", $(".barra-filtros")).forEach(function (b) { b.addEventListener("click", function () { estado.dia = b.getAttribute("data-dia"); aplicar(); }); });
    $$("[data-genero]", raiz).forEach(function (b) {
      b.addEventListener("click", function () {
        var g = b.getAttribute("data-genero"), i = estado.generos.indexOf(g);
        if (i >= 0) estado.generos.splice(i, 1); else estado.generos.push(g);
        aplicar();
      });
    });
    var limpiar = function () { estado.q = ""; estado.dia = ""; estado.espacio = ""; estado.compania = ""; estado.generos = []; aplicar(); };
    $("#p-limpiar").addEventListener("click", limpiar);
    $$("[data-limpiar]", raiz).forEach(function (b) { b.addEventListener("click", limpiar); });

    // --- estrellas
    var pintarEstrellas = function () {
      funciones.forEach(function (f) {
        var on = mio.indexOf(f.getAttribute("data-id")) >= 0;
        f.classList.toggle("marcada", on);
        var b = $(".estrella", f); b.setAttribute("aria-pressed", on ? "true" : "false");
        b.title = on ? "Quitar de mi itinerario" : "Añadir a mi itinerario";
      });
      var c = $("#contador-itinerario"); c.textContent = String(mio.length); c.classList.toggle("lleno", mio.length > 0);
    };
    raiz.addEventListener("click", function (ev) {
      var b = ev.target.closest && ev.target.closest(".estrella");
      if (!b) return;
      var f = b.closest(".funcion"), id = f && f.getAttribute("data-id");
      if (!id) return;
      var i = mio.indexOf(id);
      if (i >= 0) mio.splice(i, 1); else mio.push(id);
      guardar(); pintarEstrellas();
      if (estado.vista === "itinerario") pintarItinerario();
      b.classList.remove("salta"); void b.offsetWidth; b.classList.add("salta");
    });

    // --- vista itinerario
    var ordenar = function (ids) {
      return ids.filter(function (id) { return porId[id]; }).sort(function (a, b) {
        return porId[a].getAttribute("data-inicio") < porId[b].getAttribute("data-inicio") ? -1 : 1;
      });
    };
    var pintarItinerario = function () {
      var lista = $("#it-lista"), ids = ordenar(compartido || mio);
      lista.innerHTML = "";
      $("#it-vacio").hidden = ids.length > 0;
      $("#it-acciones").hidden = !ids.length || !!compartido;
      var av = $("#it-compartido"); av.hidden = !compartido;
      if (compartido) $("#it-compartido-n").textContent = String(ids.length);
      var ol = null, diaActual = "", finAnterior = "", tituloAnterior = "";
      ids.forEach(function (id) {
        var f = porId[id], d = f.getAttribute("data-dia");
        if (d !== diaActual) {
          diaActual = d; finAnterior = "";
          var t = $(".dia[data-dia='" + d + "'] .dia-titulo", raiz);
          var h = document.createElement("h2"); h.className = "dia-titulo"; h.textContent = t ? t.textContent : d;
          lista.appendChild(h);
          ol = document.createElement("ol"); ol.className = "funciones"; lista.appendChild(ol);
        }
        var copia = f.cloneNode(true);
        copia.hidden = false; copia.removeAttribute("id");
        if (finAnterior && f.getAttribute("data-inicio") < finAnterior) {
          copia.classList.add("solapa");
          var aviso = document.createElement("p"); aviso.className = "aviso-solapa";
          aviso.textContent = "Se pisa con " + tituloAnterior + ": tendrás que elegir o llegar a mitad.";
          $(".funcion-cuerpo", copia).appendChild(aviso);
        }
        if (f.getAttribute("data-fin") > finAnterior) { finAnterior = f.getAttribute("data-fin"); tituloAnterior = f.getAttribute("data-titulo"); }
        if (compartido) { var est = $(".estrella", copia); if (est) est.remove(); }
        ol.appendChild(copia);
      });
    };
    var mostrar = function (vista) {
      estado.vista = vista;
      $("#vista-programa").hidden = vista !== "programa";
      $("#vista-itinerario").hidden = vista !== "itinerario";
      $(".barra-filtros").hidden = vista !== "programa";
      $(".resultado", raiz).hidden = vista !== "programa";
      $("#tab-programa").setAttribute("aria-selected", vista === "programa" ? "true" : "false");
      $("#tab-itinerario").setAttribute("aria-selected", vista === "itinerario" ? "true" : "false");
      if (vista === "itinerario") pintarItinerario();
      escribirURL();
    };
    $("#tab-programa").addEventListener("click", function () { compartido = null; mostrar("programa"); });
    $("#tab-itinerario").addEventListener("click", function () { mostrar("itinerario"); });
    $("#it-guardar").addEventListener("click", function () {
      mio = ordenar(compartido); compartido = null; guardar(); pintarEstrellas(); mostrar("itinerario");
    });
    $("#it-vaciar").addEventListener("click", function () {
      if (!mio.length) return;
      if (!confirmarVaciar.dataset.armado) { confirmarVaciar.dataset.armado = "1"; setEstado("Pulsa otra vez «Vaciar» para borrar todo tu itinerario."); setTimeout(function () { delete confirmarVaciar.dataset.armado; }, 4000); return; }
      delete confirmarVaciar.dataset.armado; mio = []; guardar(); pintarEstrellas(); pintarItinerario(); setEstado("Itinerario vaciado.");
    });
    var confirmarVaciar = $("#it-vaciar");
    var setEstado = function (t) { $("#it-estado").textContent = t; };
    $("#it-compartir").addEventListener("click", function () {
      var url = location.origin + location.pathname + "?it=" + ordenar(mio).join(",");
      var titulo = "Mi itinerario en En Pie " + raiz.getAttribute("data-anio");
      if (navigator.share) { navigator.share({ title: titulo, url: url }).catch(function () {}); return; }
      if (navigator.clipboard) navigator.clipboard.writeText(url).then(function () { setEstado("Enlace copiado: pégalo donde quieras."); }, function () { setEstado(url); });
      else setEstado(url);
    });
    $("#it-calendario").addEventListener("click", function () {
      var dos = function (n) { return (n < 10 ? "0" : "") + n; };
      var aICS = function (s) { var d = new Date(s); return d.getUTCFullYear() + dos(d.getUTCMonth() + 1) + dos(d.getUTCDate()) + "T" + dos(d.getUTCHours()) + dos(d.getUTCMinutes()) + "00Z"; };
      var limpio = function (t) { return String(t).replace(/([,;\\])/g, "\\$1"); };
      // Las horas del festival son de Canarias (UTC+1 en verano, UTC+0 en invierno)
      var conZona = function (s) { var m = +s.slice(5, 7); return s + (m >= 4 && m <= 10 ? ":00+01:00" : ":00+00:00"); };
      var lineas = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Festival En Pie Teror//Itinerario//ES", "CALSCALE:GREGORIAN"];
      ordenar(mio).forEach(function (id) {
        var f = porId[id];
        lineas.push("BEGIN:VEVENT", "UID:" + id + "@festivalenpieteror.com", "DTSTAMP:" + aICS(new Date().toISOString()),
          "DTSTART:" + aICS(conZona(f.getAttribute("data-inicio"))), "DTEND:" + aICS(conZona(f.getAttribute("data-fin"))),
          "SUMMARY:" + limpio(f.getAttribute("data-titulo")), "LOCATION:" + limpio(f.getAttribute("data-lugar") + ", Teror"),
          "URL:" + location.origin + f.getAttribute("data-url"), "END:VEVENT");
      });
      lineas.push("END:VCALENDAR");
      var blob = new Blob([lineas.join("\r\n")], { type: "text/calendar;charset=utf-8" });
      var a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = "mi-itinerario-en-pie.ics";
      document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
      setEstado("Descargado: ábrelo para añadirlo a tu calendario.");
    });

    // --- «ahora»: durante el festival se marca lo que está en marcha y se apaga lo que ya pasó
    var marcarAhora = function () {
      var ahora = new Date(), dos = function (n) { return (n < 10 ? "0" : "") + n; };
      // hora de Canarias aproximada a partir de la del dispositivo
      var t = ahora.getFullYear() + "-" + dos(ahora.getMonth() + 1) + "-" + dos(ahora.getDate()) + "T" + dos(ahora.getHours()) + ":" + dos(ahora.getMinutes());
      var hay = false;
      funciones.forEach(function (f) {
        var en = f.getAttribute("data-inicio") <= t && t < f.getAttribute("data-fin");
        f.classList.toggle("ahora", en); f.classList.toggle("pasada", f.getAttribute("data-fin") <= t && f.getAttribute("data-dia") === t.slice(0, 10));
        if (en) hay = true;
      });
      return { hoy: t.slice(0, 10), hay: hay };
    };

    leerURL();
    var a = marcarAhora();
    if (!estado.dia && !location.search && $$("[data-dia='" + a.hoy + "']", $(".barra-filtros")).length) estado.dia = a.hoy;
    setInterval(marcarAhora, 60000);
    pintarEstrellas();
    aplicar();
    mostrar(estado.vista);
    if (location.hash && location.hash.indexOf("#f-") === 0) {
      var objetivo = $(location.hash);
      if (objetivo) { objetivo.classList.add("destacada"); setTimeout(function () { objetivo.scrollIntoView({ block: "center" }); }, 50); }
    }
  }
})();
