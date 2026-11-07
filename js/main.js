(function () {
  "use strict";
  try { document.documentElement.classList.remove("sin-js"); } catch (e) {}
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

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

  // Filtro de compañías por disciplina
  try {
    $$(".filtro").forEach(function (b) {
      b.addEventListener("click", function () {
        var f = b.getAttribute("data-filtro");
        $$(".filtro").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
        $$(".compania").forEach(function (c) { c.hidden = f !== "todas" && (" " + c.getAttribute("data-tipos") + " ").indexOf(" " + f + " ") < 0; });
      });
    });
  } catch (e) {}

  // Vídeo: solo se carga YouTube (sin cookies) cuando se pulsa
  try {
    var v = $(".video button");
    if (v) v.addEventListener("click", function () {
      var cont = v.parentNode, id = cont.getAttribute("data-video");
      var f = document.createElement("iframe");
      f.src = "https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1&rel=0";
      f.title = cont.getAttribute("data-titulo") || "Vídeo";
      f.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen";
      f.allowFullscreen = true;
      cont.innerHTML = ""; cont.appendChild(f);
    });
  } catch (e) {}

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
})();
