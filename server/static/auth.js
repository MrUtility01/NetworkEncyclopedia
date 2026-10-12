const APP_PASSWORD = "engineerjokar";
const AUTH_KEY = "netenc_unlocked_v1";
const TOKEN_KEY = "netenc_token_v1";

function netencIsUnlocked() {
  return sessionStorage.getItem(AUTH_KEY) === "1" || localStorage.getItem(AUTH_KEY) === "1";
}

function netencGetToken() {
  return sessionStorage.getItem(TOKEN_KEY) || localStorage.getItem(TOKEN_KEY) || APP_PASSWORD;
}

function netencUnlock(remember) {
  sessionStorage.setItem(AUTH_KEY, "1");
  sessionStorage.setItem(TOKEN_KEY, APP_PASSWORD);
  if (remember) {
    localStorage.setItem(AUTH_KEY, "1");
    localStorage.setItem(TOKEN_KEY, APP_PASSWORD);
  }
}

function netencLock() {
  [sessionStorage, localStorage].forEach((s) => {
    s.removeItem(AUTH_KEY);
    s.removeItem(TOKEN_KEY);
  });
}

function netencSetupLogin(onOk) {
  const gate = document.getElementById("loginGate");
  const root = document.getElementById("appRoot");
  const form = document.getElementById("loginForm");
  const pass = document.getElementById("loginPass");
  const err = document.getElementById("loginErr");

  function showApp() {
    if (gate) gate.hidden = true;
    if (root) root.hidden = false;
    if (onOk) onOk();
  }

  if (!form) {
    showApp();
    return;
  }
  if (netencIsUnlocked()) {
    showApp();
    return;
  }
  if (gate) gate.hidden = false;
  if (root) root.hidden = true;

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const v = ((pass && pass.value) || "").trim();
    if (v === APP_PASSWORD) {
      if (err) err.hidden = true;
      netencUnlock(true);
      showApp();
    } else {
      if (err) err.hidden = false;
      if (pass) pass.select();
    }
  });

  document.getElementById("btnLogout")?.addEventListener("click", () => {
    netencLock();
    location.reload();
  });
}

window.netencGetToken = netencGetToken;
window.netencSetupLogin = netencSetupLogin;
