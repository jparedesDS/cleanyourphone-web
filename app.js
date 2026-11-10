(() => {
  const doc = document;
  const lang = doc.documentElement.lang || "en";
  const toast = doc.getElementById("toast");
  let toastTimer = null;

  const MESSAGES = {
    en: {
      copied: "Copied",
      copied_toast: "Copied to clipboard",
      copy_failed: "Could not copy",
      feedback_not_configured: "Feedback is not configured in this build.",
      feedback_consent: "Tick the consent box before sending.",
      feedback_empty: "Write a message or a checklist.",
      feedback_too_long: "The text is too long.",
      feedback_sending: "Sending...",
      feedback_sending_discord: "Sending to Discord...",
      feedback_rate_limited: "Please wait a few minutes before sending again.",
      feedback_not_configured_error: "Feedback is not configured. Tell the maintainer.",
      feedback_failed: "Could not send.",
      feedback_sent: "Sent. Thanks for helping.",
    },
    es: {
      copied: "Copiado",
      copied_toast: "Copiado al portapapeles",
      copy_failed: "No se pudo copiar",
      feedback_not_configured: "El feedback no está configurado en esta copia.",
      feedback_consent: "Marca la casilla para aceptar el envío.",
      feedback_empty: "Escribe un mensaje o un checklist.",
      feedback_too_long: "El texto es demasiado largo.",
      feedback_sending: "Enviando...",
      feedback_sending_discord: "Enviando al Discord...",
      feedback_rate_limited: "Espera unos minutos antes de enviar otra vez.",
      feedback_not_configured_error: "El feedback no está configurado. Avisa al maintainer.",
      feedback_failed: "No se pudo enviar.",
      feedback_sent: "Enviado. Gracias por ayudar.",
    },
    "pt-BR": {
      copied: "Copiado",
      copied_toast: "Copiado para a área de transferência",
      copy_failed: "Não foi possível copiar",
      feedback_not_configured: "O feedback não está configurado nesta versão.",
      feedback_consent: "Marque a caixa de consentimento antes de enviar.",
      feedback_empty: "Escreva uma mensagem ou um checklist.",
      feedback_too_long: "O texto é muito longo.",
      feedback_sending: "Enviando...",
      feedback_sending_discord: "Enviando para o Discord...",
      feedback_rate_limited: "Aguarde alguns minutos antes de enviar novamente.",
      feedback_not_configured_error: "O feedback não está configurado. Avise o maintainer.",
      feedback_failed: "Não foi possível enviar.",
      feedback_sent: "Enviado. Obrigado por ajudar.",
    },
    fr: {
      copied: "Copié",
      copied_toast: "Copié dans le presse-papiers",
      copy_failed: "Impossible de copier",
      feedback_not_configured: "Les retours ne sont pas configurés dans cette version.",
      feedback_consent: "Cochez la case de consentement avant d'envoyer.",
      feedback_empty: "Écrivez un message ou une checklist.",
      feedback_too_long: "Le texte est trop long.",
      feedback_sending: "Envoi...",
      feedback_sending_discord: "Envoi vers Discord...",
      feedback_rate_limited: "Patientez quelques minutes avant de renvoyer.",
      feedback_not_configured_error: "Les retours ne sont pas configurés. Prévenez le mainteneur.",
      feedback_failed: "Impossible d'envoyer.",
      feedback_sent: "Envoyé. Merci pour votre aide.",
    },
    de: {
      copied: "Kopiert",
      copied_toast: "In die Zwischenablage kopiert",
      copy_failed: "Kopieren fehlgeschlagen",
      feedback_not_configured: "Feedback ist in dieser Version nicht konfiguriert.",
      feedback_consent: "Bestätige das Einverständnis vor dem Senden.",
      feedback_empty: "Schreibe eine Nachricht oder eine Checkliste.",
      feedback_too_long: "Der Text ist zu lang.",
      feedback_sending: "Wird gesendet...",
      feedback_sending_discord: "Wird an Discord gesendet...",
      feedback_rate_limited: "Bitte warte ein paar Minuten, bevor du erneut sendest.",
      feedback_not_configured_error: "Feedback ist nicht konfiguriert. Informiere den Maintainer.",
      feedback_failed: "Senden fehlgeschlagen.",
      feedback_sent: "Gesendet. Danke für die Hilfe.",
    },
    it: {
      copied: "Copiato",
      copied_toast: "Copiato negli appunti",
      copy_failed: "Impossibile copiare",
      feedback_not_configured: "Il feedback non è configurato in questa versione.",
      feedback_consent: "Seleziona la casella di consenso prima di inviare.",
      feedback_empty: "Scrivi un messaggio o una checklist.",
      feedback_too_long: "Il testo è troppo lungo.",
      feedback_sending: "Invio...",
      feedback_sending_discord: "Invio a Discord...",
      feedback_rate_limited: "Attendi qualche minuto prima di inviare di nuovo.",
      feedback_not_configured_error: "Il feedback non è configurato. Avvisa il maintainer.",
      feedback_failed: "Impossibile inviare.",
      feedback_sent: "Inviato. Grazie per l'aiuto.",
    },
    ja: {
      copied: "コピーしました",
      copied_toast: "クリップボードにコピーしました",
      copy_failed: "コピーできませんでした",
      feedback_not_configured: "このビルドではフィードバックが設定されていません。",
      feedback_consent: "送信前に同意チェックボックスをオンにしてください。",
      feedback_empty: "メッセージまたはチェックリストを入力してください。",
      feedback_too_long: "テキストが長すぎます。",
      feedback_sending: "送信中...",
      feedback_sending_discord: "Discord に送信中...",
      feedback_rate_limited: "数分待ってから再送信してください。",
      feedback_not_configured_error: "フィードバックが設定されていません。メンテナーに知らせてください。",
      feedback_failed: "送信できませんでした。",
      feedback_sent: "送信しました。ご協力ありがとうございます。",
    },
    "zh-CN": {
      copied: "已复制",
      copied_toast: "已复制到剪贴板",
      copy_failed: "无法复制",
      feedback_not_configured: "此版本未配置反馈。",
      feedback_consent: "发送前请勾选同意框。",
      feedback_empty: "请填写消息或检查清单。",
      feedback_too_long: "文本过长。",
      feedback_sending: "正在发送...",
      feedback_sending_discord: "正在发送到 Discord...",
      feedback_rate_limited: "请等待几分钟后再发送。",
      feedback_not_configured_error: "反馈未配置。请联系维护者。",
      feedback_failed: "无法发送。",
      feedback_sent: "已发送。感谢你的帮助。",
    },
    "zh-TW": {
      copied: "已複製",
      copied_toast: "已複製到剪貼簿",
      copy_failed: "無法複製",
      feedback_not_configured: "此版本未設定意見回饋。",
      feedback_consent: "送出前請勾選同意方塊。",
      feedback_empty: "請填寫訊息或檢查清單。",
      feedback_too_long: "文字過長。",
      feedback_sending: "傳送中...",
      feedback_sending_discord: "正在傳送到 Discord...",
      feedback_rate_limited: "請等待幾分鐘後再送出。",
      feedback_not_configured_error: "意見回饋未設定。請通知維護者。",
      feedback_failed: "無法送出。",
      feedback_sent: "已送出。感謝你的協助。",
    },
    ko: {
      copied: "복사됨",
      copied_toast: "클립보드에 복사됨",
      copy_failed: "복사할 수 없습니다",
      feedback_not_configured: "이 빌드에는 피드백이 설정되어 있지 않습니다.",
      feedback_consent: "보내기 전에 동의 체크박스를 선택하세요.",
      feedback_empty: "메시지나 체크리스트를 작성하세요.",
      feedback_too_long: "텍스트가 너무 깁니다.",
      feedback_sending: "보내는 중...",
      feedback_sending_discord: "Discord로 보내는 중...",
      feedback_rate_limited: "몇 분 후에 다시 보내세요.",
      feedback_not_configured_error: "피드백이 설정되어 있지 않습니다. 메인테이너에게 알려주세요.",
      feedback_failed: "보낼 수 없습니다.",
      feedback_sent: "보냈습니다. 도와주셔서 감사합니다.",
    },
  };

  const messages = MESSAGES[lang] || MESSAGES.en;

  const showToast = (message) => {
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove("show"), 1800);
  };

  const languageSelect = doc.getElementById("language-select");
  if (languageSelect) {
    languageSelect.addEventListener("change", () => {
      if (languageSelect.value) {
        window.location.assign(languageSelect.value);
      }
    });
  }

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
        label.textContent = messages.copied;
        showToast(messages.copied_toast);
        setTimeout(() => { label.textContent = original; }, 1600);
      } catch {
        showToast(messages.copy_failed);
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
      setStatus(messages.feedback_not_configured, "error");
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
        setStatus(messages.feedback_consent, "error");
        return;
      }
      if (!payload.message && !payload.checklist) {
        setStatus(messages.feedback_empty, "error");
        return;
      }
      if (payload.message.length > 4000 || payload.checklist.length > 6000) {
        setStatus(messages.feedback_too_long, "error");
        return;
      }

      const original = submit.textContent;
      submit.disabled = true;
      submit.textContent = messages.feedback_sending;
      setStatus(messages.feedback_sending_discord);

      try {
        const response = await fetch(endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await response.json().catch(() => ({}));
        if (!response.ok) {
          if (response.status === 429) {
            throw new Error(messages.feedback_rate_limited);
          }
          if (response.status === 503) {
            throw new Error(messages.feedback_not_configured_error);
          }
          throw new Error(data.error || messages.feedback_failed);
        }
        feedbackForm.reset();
        setStatus(messages.feedback_sent, "success");
      } catch (error) {
        setStatus(error.message || messages.feedback_failed, "error");
      } finally {
        submit.disabled = false;
        submit.textContent = original;
      }
    });
  }
})();
