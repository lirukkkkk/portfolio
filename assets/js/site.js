(() => {
  const root = document.documentElement;
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const finePointer = matchMedia("(hover: hover) and (pointer: fine)").matches;
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} },
  };
  const $$ = (s, el = document) => Array.from(el.querySelectorAll(s));

  /* ---------- Theme ---------- */
  const themeBtn = document.querySelector("[data-theme-toggle]");
  if (themeBtn) {
    themeBtn.addEventListener("click", () => {
      const current = root.dataset.theme || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
      const next = current === "dark" ? "light" : "dark";
      const apply = () => {
        root.dataset.theme = next;
        store.set("theme", next);
        const meta = document.querySelector('meta[name="theme-color"]');
        if (meta) meta.content = next === "dark" ? "#121211" : "#f2f1ed";
      };
      if (!document.startViewTransition || reduce) return apply();
      const r = themeBtn.getBoundingClientRect();
      const x = r.left + r.width / 2, y = r.top + r.height / 2;
      const end = Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y));
      root.classList.add("theme-vt");
      const vt = document.startViewTransition(apply);
      vt.ready.then(() => root.animate({ clipPath: ["circle(0px at " + x + "px " + y + "px)", "circle(" + end + "px at " + x + "px " + y + "px)"] },
        { duration: 520, easing: "cubic-bezier(0.77, 0, 0.175, 1)", pseudoElement: "::view-transition-new(root)" }));
      vt.finished.finally(() => root.classList.remove("theme-vt"));
    });
  }

  /* ---------- Language ---------- */
  const dict = window.I18N || {};
  let lang = store.get("lang") || "pt";
  const textNodes = $$("[data-i18n]");
  const attrNodes = $$("[data-i18n-attr]");
  const original = new Map();
  const origAttr = new Map();
  textNodes.forEach((el) => original.set(el, el.innerHTML));
  function applyLang(l) {
    lang = l;
    root.lang = l === "en" ? "en" : "pt-BR";
    textNodes.forEach((el) => {
      const v = dict[el.dataset.i18n];
      el.innerHTML = l === "pt" || !v ? original.get(el) : v;
    });
    attrNodes.forEach((el) => {
      el.dataset.i18nAttr.split(";").forEach((pair) => {
        const [attr, key] = pair.split(":");
        const v = dict[key];
        const id = attr + "@";
        if (!origAttr.has(el)) origAttr.set(el, {});
        const o = origAttr.get(el);
        if (!(id in o)) o[id] = el.getAttribute(attr) || "";
        el.setAttribute(attr, l === "pt" || !v ? o[id] : v);
      });
    });
    $$("[data-lang-toggle]").forEach((b) => { b.textContent = l === "pt" ? "EN" : "PT"; });
    store.set("lang", l);
    document.dispatchEvent(new CustomEvent("langchange"));
  }
  $$("[data-lang-toggle]").forEach((b) => b.addEventListener("click", () => applyLang(lang === "pt" ? "en" : "pt")));
  if (lang !== "pt") applyLang(lang);
  const t = (k, fb) => (lang === "en" && dict[k]) || fb;

  /* ---------- Header border on scroll ---------- */
  const top = document.querySelector(".top");
  if (top) {
    const onScroll = () => top.classList.toggle("is-scrolled", scrollY > 8);
    addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* ---------- Reveal ---------- */
  $$(".arch a").forEach((a, i) => { a.classList.add("rv"); a.style.setProperty("--d", (i % 4) * 70 + "ms"); });
  $$(".group .g-grid .media, .group .g-wide .media").forEach((m, i) => { m.classList.add("rv", "rv-img"); m.style.setProperty("--d", (i % 3) * 70 + "ms"); });
  if (location.search.includes("captura")) document.querySelectorAll("img[loading=lazy]").forEach((i) => { i.loading = "eager"; });
  const rv = $$(".rv");
  if (rv.length && "IntersectionObserver" in window && !location.search.includes("captura")) {
    root.classList.add("js-rv");
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.05 });
    rv.forEach((el) => io.observe(el));
  }

  /* ---------- Carousels ---------- */
  $$("[data-car]").forEach((car) => {
    const track = car.querySelector(".car-track");
    const meter = car.querySelector(".car-meter i");
    const count = car.querySelector(".car-count");
    const [prev, next] = $$(".car-btns button", car);
    const slides = Array.from(track.children);
    const update = () => {
      const max = track.scrollWidth - track.clientWidth;
      const ratio = track.clientWidth / track.scrollWidth;
      const p = max > 0 ? track.scrollLeft / max : 0;
      if (meter) {
        meter.style.setProperty("--w", Math.min(100, ratio * 100) + "%");
        meter.style.setProperty("--x", (p * (1 / Math.max(ratio, 0.0001) - 1) * 100) + "%");
      }
      const w = slides[0] ? slides[0].getBoundingClientRect().width + 12 : 1;
      const idx = Math.min(slides.length, Math.round(track.scrollLeft / w) + 1);
      if (count) count.textContent = String(idx).padStart(2, "0") + " / " + String(slides.length).padStart(2, "0");
      if (prev) prev.disabled = track.scrollLeft < 4;
      if (next) next.disabled = track.scrollLeft > max - 4;
    };
    const step = (dir) => {
      const w = slides[0].getBoundingClientRect().width + 12;
      track.scrollBy({ left: dir * w, behavior: reduce ? "auto" : "smooth" });
    };
    prev && prev.addEventListener("click", () => step(-1));
    next && next.addEventListener("click", () => step(1));
    track.addEventListener("scroll", () => requestAnimationFrame(update), { passive: true });
    addEventListener("resize", update);
    track.addEventListener("keydown", (e) => {
      if (e.key === "ArrowRight") { e.preventDefault(); step(1); }
      if (e.key === "ArrowLeft") { e.preventDefault(); step(-1); }
    });
    // mouse drag (touch scrolls natively)
    let down = false, sx = 0, sl = 0, moved = false;
    track.addEventListener("pointerdown", (e) => {
      if (e.pointerType !== "mouse" || e.button !== 0) return;
      down = true; moved = false; sx = e.clientX; sl = track.scrollLeft;
    });
    addEventListener("pointermove", (e) => {
      if (!down) return;
      const dx = e.clientX - sx;
      if (!moved && Math.abs(dx) > 5) { moved = true; track.classList.add("is-dragging"); }
      if (moved) track.scrollLeft = sl - dx;
    });
    addEventListener("pointerup", () => {
      if (!down) return;
      down = false;
      if (moved) {
        track.classList.remove("is-dragging");
        const w = slides[0].getBoundingClientRect().width + 12;
        track.scrollTo({ left: Math.round(track.scrollLeft / w) * w, behavior: reduce ? "auto" : "smooth" });
        const block = (ev) => { ev.preventDefault(); ev.stopPropagation(); };
        track.addEventListener("click", block, { capture: true, once: true });
        setTimeout(() => track.removeEventListener("click", block, { capture: true }), 50);
      }
    });
    update();
  });

  /* ---------- Lightbox ---------- */
  const lb = document.querySelector(".lb");
  if (lb) {
    const stage = lb.querySelector(".lb-pic");
    const cap = lb.querySelector(".lb-cap");
    let list = [], i = 0;
    const show = () => {
      const el = list[i];
      const src = el.querySelector("img");
      const sources = Array.from(el.querySelectorAll("source")).map((s) => `<source type="${s.type}" srcset="${s.srcset}" sizes="100vw">`).join("");
      const holder = document.createElement("div");
      holder.innerHTML = `<picture>${sources}<img src="${src.currentSrc || src.src}" alt=""></picture>`;
      const img = holder.querySelector("img");
      img.alt = src.alt;
      const swap = () => stage.replaceChildren(holder.firstElementChild);
      if (!stage.firstChild) swap(); else (img.decode ? img.decode().then(swap, swap) : swap());
      cap.textContent = (el.dataset.cap ? el.dataset.cap + " · " : "") + (i + 1) + " / " + list.length;
    };
    document.addEventListener("click", (e) => {
      const z = e.target.closest("[data-zoom]");
      if (!z) return;
      e.preventDefault();
      const group = z.closest("[data-zoom-group]") || document;
      list = $$("[data-zoom]", group);
      i = list.indexOf(z);
      show();
      lb.showModal();
    });
    lb.querySelector("[data-lb-close]").addEventListener("click", () => lb.close());
    lb.querySelector("[data-lb-prev]").addEventListener("click", () => { i = (i - 1 + list.length) % list.length; show(); });
    lb.querySelector("[data-lb-next]").addEventListener("click", () => { i = (i + 1) % list.length; show(); });
    lb.addEventListener("keydown", (e) => {
      if (e.key === "ArrowRight") { i = (i + 1) % list.length; show(); }
      if (e.key === "ArrowLeft") { i = (i - 1 + list.length) % list.length; show(); }
    });
    lb.addEventListener("click", (e) => { if (e.target === lb || e.target.classList.contains("lb-stage")) lb.close(); });
  }

  /* ---------- Videos: play only on screen ---------- */
  const vids = $$("video[data-auto]");
  if (vids.length && "IntersectionObserver" in window) {
    const vio = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        const vid = e.target;
        if (e.isIntersecting && !reduce) vid.play().catch(() => {});
        else vid.pause();
      });
    }, { threshold: 0.35 });
    vids.forEach((vid) => vio.observe(vid));
  }
  $$("[data-sound]").forEach((b) => b.addEventListener("click", () => {
    const vid = b.parentElement.querySelector("video");
    vid.muted = !vid.muted;
    b.setAttribute("aria-pressed", String(!vid.muted));
    if (!vid.muted) vid.play().catch(() => {});
  }));

  /* ---------- Category filters (work index + archive) ---------- */
  const setFilter = (bar, seg) => {
    const target = document.querySelector(bar.dataset.filter);
    $$("button", bar).forEach((x) => x.setAttribute("aria-pressed", String(x.dataset.seg === seg)));
    const items = $$("[data-tags]", target);
    const apply = () => {
      let shown = 0;
      items.forEach((it) => { const ok = seg === "all" || it.dataset.tags.split(" ").includes(seg); it.hidden = !ok; if (ok) shown++; });
      const empty = target.parentElement.querySelector(".ix-empty");
      if (empty) empty.hidden = shown > 0;
      const vids = target.id === "ix" && document.getElementById("ix-vids");
      if (vids) {
        const on = seg === "motion";
        vids.hidden = !on; target.hidden = on;
        if (on && empty) empty.hidden = true;
        if (!on) $$("video", vids).forEach((v) => v.pause());
      }
    };
    if (document.startViewTransition && !reduce) document.startViewTransition(apply); else apply();
    if (bar.dataset.filter === "#ix") $$(".mq-btn").forEach((m) => m.classList.toggle("on", m.dataset.cat === seg));
  };
  $$("[data-filter]").forEach((bar) => {
    bar.addEventListener("click", (e) => {
      const b = e.target.closest("button[data-seg]");
      if (b) setFilter(bar, b.dataset.seg);
    });
  });
  document.addEventListener("click", (e) => {
    const m = e.target.closest(".mq-btn");
    if (!m) return;
    const bar = document.querySelector('[data-filter="#ix"]');
    if (!bar) return;
    const seg = m.classList.contains("on") ? "all" : m.dataset.cat;
    setFilter(bar, seg);
    document.getElementById("trabalhos").scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
  });

  /* ---------- Scroll progress ---------- */
  const bar = document.createElement("div");
  bar.className = "scroll-bar";
  bar.setAttribute("aria-hidden", "true");
  document.body.appendChild(bar);
  const onProg = () => {
    const max = document.documentElement.scrollHeight - innerHeight;
    bar.style.transform = "scaleX(" + (max > 0 ? Math.min(1, scrollY / max) : 0) + ")";
  };
  addEventListener("scroll", () => requestAnimationFrame(onProg), { passive: true });
  onProg();

  /* ---------- Marquee: steady drift, drag to scrub ---------- */
  $$("[data-marquee]").forEach((mq) => {
    const track = mq.querySelector(".mq-track");
    let x = 0, last = performance.now(), visible = true, vel = 0;
    let down = false, px = 0, lastX = 0, lastT = 0;
    const wrap = () => {
      const half = track.scrollWidth / 2;
      if (half <= 0) return;
      while (x <= -half) x += half;
      while (x > 0) x -= half;
    };
    new IntersectionObserver((en) => { visible = en[0].isIntersecting; }).observe(mq);
    let moved = false, hover = false;
    mq.addEventListener("pointerenter", (e) => { if (e.pointerType === "mouse") hover = true; });
    mq.addEventListener("pointerleave", () => { hover = false; });
    mq.addEventListener("pointerdown", (e) => {
      down = true; moved = false; px = lastX = e.clientX; lastT = performance.now(); vel = 0;
    });
    mq.addEventListener("pointermove", (e) => {
      if (!down) return;
      if (!moved) {
        if (Math.abs(e.clientX - px) < 6) return;
        moved = true; mq.setPointerCapture(e.pointerId); mq.classList.add("is-dragging");
      }
      const now = performance.now(), dx = e.clientX - lastX;
      x += dx * 1.6;
      vel = (dx * 1.6) / Math.max(1, now - lastT);
      lastX = e.clientX; lastT = now;
      wrap(); track.style.transform = "translate3d(" + x + "px,0,0)";
    });
    const up = () => { down = false; mq.classList.remove("is-dragging"); };
    mq.addEventListener("click", (e) => { if (moved) { e.stopPropagation(); e.preventDefault(); moved = false; } }, true);
    mq.addEventListener("pointerup", up);
    mq.addEventListener("pointercancel", up);
    const tick = (now) => {
      const dt = Math.min(64, now - last); last = now;
      if (visible && !down) {
        x += (reduce || hover ? 0 : -0.04 * dt) + vel * dt;
        vel *= 0.94;
        if (Math.abs(vel) < 0.002) vel = 0;
        wrap(); track.style.transform = "translate3d(" + x + "px,0,0)";
      }
      requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  });

  /* ---------- Magnetic buttons ---------- */
  if (finePointer && !reduce) {
    $$(".btn").forEach((b) => {
      b.classList.add("mag");
      b.addEventListener("pointermove", (e) => {
        const r = b.getBoundingClientRect();
        const mx = (e.clientX - r.left - r.width / 2) * 0.22, my = (e.clientY - r.top - r.height / 2) * 0.3;
        b.style.transform = "translate(" + Math.max(-8, Math.min(8, mx)) + "px, " + Math.max(-6, Math.min(6, my)) + "px)";
      });
      b.addEventListener("pointerleave", () => { b.style.transform = ""; });
    });
  }

  /* ---------- Briefing form → WhatsApp / e-mail ---------- */
  const form = document.querySelector("[data-brief]");
  if (form) {
    const msg = form.querySelector(".form-msg");
    const build = () => {
      const f = new FormData(form);
      const name = (f.get("name") || "").trim();
      const service = f.get("service") || "";
      const sel = form.querySelector('[name="service"]');
      if (!name || !service) {
        msg.textContent = t("form.required", "Preencha seu nome e o que você precisa.");
        msg.classList.add("err");
        const bad = !name ? form.querySelector('[name="name"]') : sel;
        bad.setAttribute("aria-invalid", "true");
        bad.focus();
        return null;
      }
      $$("[aria-invalid]", form).forEach((x) => x.removeAttribute("aria-invalid"));
      msg.classList.remove("err");
      msg.textContent = "";
      const label = (n) => { const o = form.querySelector(`[name="${n}"]`); return o && o.tagName === "SELECT" ? o.options[o.selectedIndex].text : (f.get(n) || "").trim(); };
      const lines = [
        lang === "en" ? `Hi Alan! I'm ${name}.` : `Oi, Alan! Sou ${name}.`,
        f.get("company") && (lang === "en" ? `Company: ${f.get("company")}` : `Empresa: ${f.get("company")}`),
        (lang === "en" ? "I need: " : "Preciso de: ") + label("service"),
        f.get("segment") && (lang === "en" ? `Industry: ${f.get("segment")}` : `Segmento: ${f.get("segment")}`),
        f.get("deadline") && (lang === "en" ? `Deadline: ${f.get("deadline")}` : `Prazo: ${f.get("deadline")}`),
        f.get("refs") && (lang === "en" ? `References: ${f.get("refs")}` : `Referências: ${f.get("refs")}`),
        f.get("msg") && "\n" + f.get("msg"),
      ].filter(Boolean);
      return { name, text: lines.join("\n") };
    };
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const r = build();
      if (!r) return;
      const via = e.submitter && e.submitter.value;
      if (via === "mail") {
        const subject = (lang === "en" ? "Brief — " : "Briefing — ") + r.name;
        location.href = `mailto:${form.dataset.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(r.text)}`;
      } else {
        window.open(`https://wa.me/${form.dataset.whats}?text=${encodeURIComponent(r.text)}`, "_blank", "noopener");
      }
    });
    form.addEventListener("input", (e) => { if (e.target.hasAttribute("aria-invalid")) e.target.removeAttribute("aria-invalid"); });
  }


  /* ---------- Compartilhar ---------- */
  const shareBtn = document.querySelector("[data-share]");
  if (shareBtn) {
    const pop = shareBtn.parentElement.querySelector(".share-pop");
    const url = location.href.split("#")[0];
    const title = document.title;
    const msg = (document.documentElement.lang === "en" ? "Check out Alan Veloso's portfolio: " : "Olha o portfólio do Alan Veloso: ") + url;
    pop.querySelector("[data-share-whats]").href = "https://wa.me/?text=" + encodeURIComponent(msg);
    pop.querySelector("[data-share-mail]").href = "mailto:?subject=" + encodeURIComponent(title) + "&body=" + encodeURIComponent(msg);
    const close = () => { pop.hidden = true; shareBtn.setAttribute("aria-expanded", "false"); };
    const touch = matchMedia("(hover: none), (pointer: coarse)").matches;
    shareBtn.addEventListener("click", async (ev) => {
      ev.stopPropagation();
      if (touch && navigator.share) {          /* celular: tela de compartilhar do aparelho */
        try { await navigator.share({ title, text: msg.replace(url, "").trim(), url }); } catch (e) {}
        return;
      }
      const open = pop.hidden;                  /* computador: menu com copiar, WhatsApp e e-mail */
      pop.hidden = !open;
      shareBtn.setAttribute("aria-expanded", String(open));
    });
    pop.querySelector("[data-share-copy]").addEventListener("click", async (ev) => {
      const b = ev.currentTarget, label = b.querySelector("span");
      try { await navigator.clipboard.writeText(url); } catch (e) {
        const t = document.createElement("textarea"); t.value = url; document.body.appendChild(t); t.select();
        try { document.execCommand("copy"); } catch (e2) {} t.remove();
      }
      const old = label.textContent;
      label.textContent = (window.I18N && document.documentElement.lang === "en") ? I18N["share.copied"] : "Link copiado";
      b.classList.add("ok");
      setTimeout(() => { label.textContent = old; b.classList.remove("ok"); close(); }, 1400);
    });
    pop.querySelectorAll("a").forEach((a) => a.addEventListener("click", () => setTimeout(close, 100)));
    document.addEventListener("click", (ev) => { if (!pop.hidden && !pop.contains(ev.target)) close(); });
    document.addEventListener("keydown", (ev) => { if (ev.key === "Escape" && !pop.hidden) { close(); shareBtn.focus(); } });
  }

  /* ---------- Cursor preview (index lists) ---------- */
  const prevBox = document.querySelector("[data-preview]");
  if (prevBox && finePointer) {
    const imgs = $$("img", prevBox);
    let px = 0, py = 0, x = 0, y = 0, on = false;
    $$("[data-preview-item]").forEach((row) => {
      row.addEventListener("pointerenter", () => {
        on = true; prevBox.classList.add("on");
        const k = row.dataset.previewItem;
        imgs.forEach((im) => im.classList.toggle("on", im.dataset.k === k));
      });
      row.addEventListener("pointerleave", () => { on = false; prevBox.classList.remove("on"); });
    });
    addEventListener("pointermove", (e) => { px = e.clientX; py = e.clientY; }, { passive: true });
    const tick = () => {
      x += (px - x) * (reduce ? 1 : 0.18); y += (py - y) * (reduce ? 1 : 0.18);
      prevBox.style.transform = `translate3d(${x}px, ${y}px, 0)`;
      requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }
})();
