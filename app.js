(() => {
  const doc = document;
  const lang = doc.documentElement.lang || "en";
  const toast = doc.getElementById("toast");
  let toastTimer = null;

  const showToast = (message) => {
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove("show"), 1800);
  };

  // Before / after app grid
  const grid = doc.getElementById("appGrid");
  if (grid) {
    const cards = Array.from(grid.querySelectorAll(".app"));
    const count = doc.querySelector("[data-count]");
    const buttons = Array.from(doc.querySelectorAll("[data-view]"));
    const total = cards.length;
    const clean = cards.filter((card) => !card.classList.contains("bloat")).length;

    const setView = (view) => {
      grid.dataset.view = view;
      buttons.forEach((button) => {
        button.setAttribute("aria-pressed", button.dataset.view === view ? "true" : "false");
      });
      if (count) {
        const shown = view === "before" ? total : clean;
        count.textContent = `${shown} ${lang === "es" ? "apps" : "apps"}`;
      }
    };

    buttons.forEach((button) => {
      button.addEventListener("click", () => setView(button.dataset.view));
    });
    setView(grid.dataset.view || "after");
  }

  // Brand tabs
  const brandTabs = Array.from(doc.querySelectorAll("[data-brand]"));
  const brandPanels = Array.from(doc.querySelectorAll("[data-brand-panel]"));
  if (brandTabs.length) {
    const activateBrand = (name, focus = false) => {
      brandTabs.forEach((tab) => {
        const active = tab.dataset.brand === name;
        tab.setAttribute("aria-selected", active ? "true" : "false");
        tab.tabIndex = active ? 0 : -1;
        if (active && focus) tab.focus();
      });
      brandPanels.forEach((panel) => {
        panel.hidden = panel.dataset.brandPanel !== name;
      });
    };

    const initial = brandTabs.find((tab) => tab.getAttribute("aria-selected") === "true") || brandTabs[0];
    activateBrand(initial.dataset.brand);
    brandTabs.forEach((tab, index) => {
      tab.addEventListener("click", () => activateBrand(tab.dataset.brand));
      tab.addEventListener("keydown", (event) => {
        if (event.key !== "ArrowRight" && event.key !== "ArrowLeft") return;
        event.preventDefault();
        const delta = event.key === "ArrowRight" ? 1 : -1;
        const next = brandTabs[(index + delta + brandTabs.length) % brandTabs.length];
        activateBrand(next.dataset.brand, true);
      });
    });
  }

  // Copy buttons
  const copyText = async (text) => {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return;
    }
    const area = doc.createElement("textarea");
    area.value = text;
    area.setAttribute("readonly", "");
    area.className = "copy-buffer";
    doc.body.appendChild(area);
    area.select();
    const ok = doc.execCommand("copy");
    area.remove();
    if (!ok) throw new Error("copy failed");
  };

  doc.querySelectorAll("[data-copy]").forEach((button) => {
    button.addEventListener("click", async () => {
      const original = button.textContent;
      try {
        await copyText(button.dataset.copy || "");
        button.textContent = lang === "es" ? "Copiado" : "Copied";
        showToast(lang === "es" ? "Copiado al portapapeles" : "Copied to clipboard");
        setTimeout(() => { button.textContent = original; }, 1600);
      } catch {
        showToast(lang === "es" ? "No se pudo copiar" : "Could not copy");
      }
    });
  });
})();
