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

  const copyText = async (text) => {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return;
    }
    const area = doc.createElement("textarea");
    area.value = text;
    area.setAttribute("readonly", "");
    area.className = "copy-helper";
    doc.body.appendChild(area);
    area.select();
    const ok = doc.execCommand("copy");
    area.remove();
    if (!ok) throw new Error("copy failed");
  };

  doc.querySelectorAll("[data-copy]").forEach((button) => {
    button.addEventListener("click", async () => {
      const label = button.querySelector(".copy-label") || button;
      const original = label.textContent;
      try {
        await copyText(button.dataset.copy || "");
        label.textContent = lang === "es" ? "Copiado" : "Copied";
        showToast(lang === "es" ? "Copiado al portapapeles" : "Copied to clipboard");
        setTimeout(() => { label.textContent = original; }, 1600);
      } catch {
        showToast(lang === "es" ? "No se pudo copiar" : "Could not copy");
      }
    });
  });

  const feedbackForm = doc.getElementById("feedback-form");
  if (feedbackForm) {
    const endpoint = (feedbackForm.dataset.endpoint || "").trim();
    const status = doc.getElementById("feedback-status");
    const submit = doc.getElementById("feedback-submit");
    const consent = doc.getElementById("feedback-consent");
    const message = doc.getElementById("feedback-message");
    const checklist = doc.getElementById("feedback-checklist");
    const contact = doc.getElementById("feedback-contact");
    const kind = doc.getElementById("feedback-kind");
    const website = doc.getElementById("feedback-website");

    const setStatus = (text, tone) => {
      if (!status) return;
      status.textContent = text;
      if (tone) {
        status.dataset.tone = tone;
      } else {
        delete status.dataset.tone;
      }
    };

    if (!endpoint && submit) {
      submit.disabled = true;
      setStatus(
        lang === "es"
          ? "El feedback no está configurado en esta copia."
          : "Feedback is not configured in this build.",
        "error",
      );
    }

    feedbackForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      if (!endpoint || !submit) return;

      const payload = {
        kind: kind ? kind.value : "feedback",
        message: message ? message.value.trim() : "",
        checklist: checklist ? checklist.value.trim() : "",
        contact: contact ? contact.value.trim() : "",
        app_version: "web",
        website: website ? website.value : "",
      };

      if (!consent || !consent.checked) {
        setStatus(
          lang === "es"
            ? "Marca la casilla para aceptar el envío."
            : "Tick the consent box before sending.",
          "error",
        );
        return;
      }
      if (!payload.message && !payload.checklist) {
        setStatus(
          lang === "es"
            ? "Escribe un mensaje o un checklist."
            : "Write a message or a checklist.",
          "error",
        );
        return;
      }
      if (payload.message.length > 4000 || payload.checklist.length > 6000) {
        setStatus(
          lang === "es" ? "El texto es demasiado largo." : "The text is too long.",
          "error",
        );
        return;
      }

      const original = submit.textContent;
      submit.disabled = true;
      submit.textContent = lang === "es" ? "Enviando..." : "Sending...";
      setStatus(lang === "es" ? "Enviando al Discord..." : "Sending to Discord...");

      try {
        const response = await fetch(endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await response.json().catch(() => ({}));
        if (!response.ok) {
          if (response.status === 429) {
            throw new Error(
              lang === "es"
                ? "Espera unos minutos antes de enviar otra vez."
                : "Please wait a few minutes before sending again.",
            );
          }
          if (response.status === 503) {
            throw new Error(
              lang === "es"
                ? "El feedback no está configurado. Avisa al maintainer."
                : "Feedback is not configured. Tell the maintainer.",
            );
          }
          throw new Error(
            data.error ||
              (lang === "es" ? "No se pudo enviar." : "Could not send."),
          );
        }
        feedbackForm.reset();
        setStatus(
          lang === "es"
            ? "Enviado. Gracias por ayudar."
            : "Sent. Thanks for helping.",
          "success",
        );
      } catch (error) {
        setStatus(
          error.message ||
            (lang === "es" ? "No se pudo enviar." : "Could not send."),
          "error",
        );
      } finally {
        submit.disabled = false;
        submit.textContent = original;
      }
    });
  }
})();
