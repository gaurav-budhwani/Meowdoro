"use strict";

const form = document.getElementById("license-form");
const input = document.getElementById("license-key");
const button = document.getElementById("activate-button");
const statusMessage = document.getElementById("status-message");
const languageButtons = document.querySelectorAll(".language-option");

const I18N = {
  en: {
    language: "Language",
    intro: "Enter a prototype key to activate Catjang. Default keys are listed in the project README.",
    licenseKey: "License key",
    activate: "Activate",
    missingKey: "Please enter a license key.",
    activating: "Activating...",
    activated: "Activated. Starting Catjang.",
    genericError: "We could not activate this license key.",
  },
};

let currentLanguage = "en";

function t(key) {
  return (I18N[currentLanguage] && I18N[currentLanguage][key]) || I18N.en[key] || key;
}

function applyLanguage(language) {
  currentLanguage = I18N[language] ? language : "en";
  document.documentElement.lang = currentLanguage;
  for (const el of document.querySelectorAll("[data-i18n]")) {
    el.textContent = t(el.dataset.i18n);
  }
  for (const el of document.querySelectorAll("[data-i18n-aria-label]")) {
    el.setAttribute("aria-label", t(el.dataset.i18nAriaLabel));
  }
  for (const btn of languageButtons) {
    btn.classList.toggle("is-active", btn.dataset.language === currentLanguage);
  }
}

function setStatus(message, ok = false) {
  statusMessage.textContent = message || "";
  statusMessage.classList.toggle("is-ok", ok);
}

function normalizeError(error) {
  if (!error) return t("genericError");
  if (typeof error === "string") return error;
  if (error.message) return error.message;
  return t("genericError");
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const licenseKey = input.value.trim();
  if (!licenseKey) {
    setStatus(t("missingKey"));
    input.focus();
    return;
  }

  button.disabled = true;
  input.disabled = true;
  setStatus(t("activating"));

  try {
    await window.electronAPI.licenseActivate(licenseKey);
    setStatus(t("activated"), true);
  } catch (error) {
    setStatus(normalizeError(error));
    button.disabled = false;
    input.disabled = false;
    input.focus();
  }
});

window.electronAPI.onLicenseError((message) => {
  if (message) setStatus(message);
});

window.electronAPI.onLanguageChanged((language) => {
  applyLanguage(language);
});

for (const btn of languageButtons) {
  btn.addEventListener("click", async () => {
    const language = await window.electronAPI.languageSet(btn.dataset.language);
    applyLanguage(language);
    setStatus("");
  });
}

window.addEventListener("DOMContentLoaded", async () => {
  applyLanguage(await window.electronAPI.languageGet());
  input.focus();
});
