const APP_PASSWORD = "engineerjokar";
const AUTH_KEY = "netenc_unlocked_v1";
const TOKEN_KEY = "netenc_token_v1";

function netencIsUnlocked() {
  try {
    return sessionStorage.getItem(AUTH_KEY) === "1" || localStorage.getItem(AUTH_KEY) === "1";
  } catch (e) {
    return false;
  }
}

function netencGetToken() {
  try {
    return sessionStorage.getItem(TOKEN_KEY) || localStorage.getItem(TOKEN_KEY) || APP_PASSWORD;
  } catch (e) {
    return APP_PASSWORD;
  }
}

function netencUnlock() {
  try {
    sessionStorage.setItem(AUTH_KEY, "1");
    sessionStorage.setItem(TOKEN_KEY, APP_PASSWORD);
    localStorage.setItem(AUTH_KEY, "1");
    localStorage.setItem(TOKEN_KEY, APP_PASSWORD);
  } catch (e) {}
}

function netencLock() {
  try {
    [sessionStorage, localStorage].forEach((s) => {
      s.removeItem(AUTH_KEY);
      s.removeItem(TOKEN_KEY);
    });
  } catch (e) {}
}

function normalizePass(v) {
  return String(v || "")
    .replace(/[\u200c\u200f\u200e\ufeff\u00a0]/g, "")
    .replace(/\s+/g, "")
    .trim()
    .toLowerCase();
}

function netencSetupLogin(onOk) {
  const gate = document.getElementById("loginGate");
  const root = document.getElementById("appRoot");
  const form = document.getElementById("loginForm");
  const pass = document.getElementById("loginPass");
  const btn = document.getElementById("loginBtn");
  const err = document.getElementById("loginErr");

  function showApp() {
    if (gate) {
      gate.hidden = true;
      gate.style.cssText = "display:none!important";
    }
    if (root) {
      root.hidden = false;
      root.style.cssText = "";
    }
    if (typeof onOk === "function") {
      try { onOk(); } catch (e) { console.error(e); }
    }
  }

  function tryLogin() {
    const v = normalizePass(pass && pass.value);
    if (v === APP_PASSWORD) {
      if (err) err.hidden = true;
      netencUnlock();
      showApp();
      return true;
    }
    if (err) {
      err.hidden = false;
      err.textContent = "رمز نادرست است";
    }
    if (pass) {
      pass.value = "";
      pass.focus();
    }
    return false;
  }

  if (netencIsUnlocked()) {
    showApp();
    return;
  }

  if (gate) {
    gate.hidden = false;
    gate.style.display = "flex";
  }
  if (root) {
    root.hidden = true;
    root.style.display = "none";
  }

  if (form) {
    form.setAttribute("action", "#");
    form.setAttribute("method", "post");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      e.stopPropagation();
      tryLogin();
      return false;
    });
  }
  if (btn) {
    btn.type = "button";
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      tryLogin();
    });
  }
  if (pass) {
    pass.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        tryLogin();
      }
    });
  }
}

window.netencGetToken = netencGetToken;
window.netencSetupLogin = netencSetupLogin;
window.netencLock = netencLock;
