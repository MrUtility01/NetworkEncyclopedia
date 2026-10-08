/* LAN IP + Sync status bar */
async function loadLanAndSync() {
  const lanEl = document.getElementById("lanIp");
  const hintEl = document.getElementById("androidHint");
  const statusEl = document.getElementById("syncStatus");
  if (!lanEl) return;
  try {
    const r = await fetch("/api/sync/hello");
    const hello = await r.json();
    const ip = hello.lan_ip || "127.0.0.1";
    lanEl.textContent = ip;
    if (hintEl) hintEl.textContent = "http://" + ip + ":5050";
    if (statusEl) {
      const s = hello.stats || {};
      statusEl.textContent =
        "دستگاه: " + (hello.device_id || "—") +
        " · فصل " + (s.chapters || 0) +
        " · درس " + (s.lessons || 0) +
        " · schema " + (hello.schema_version || 1);
    }
  } catch (e) {
    lanEl.textContent = "خطا";
    if (statusEl) statusEl.textContent = String(e.message || e);
  }
}

document.getElementById("btnCopyIp")?.addEventListener("click", async () => {
  const ip = document.getElementById("lanIp")?.textContent || "";
  const url = "http://" + ip + ":5050";
  try {
    await navigator.clipboard.writeText(url);
    const st = document.getElementById("syncStatus");
    if (st) st.textContent = "کپی شد: " + url;
  } catch {
    prompt("آدرس را کپی کنید:", url);
  }
});

document.getElementById("btnSyncStatus")?.addEventListener("click", async () => {
  const statusEl = document.getElementById("syncStatus");
  if (statusEl) statusEl.textContent = "در حال بررسی…";
  try {
    const r = await fetch("/api/sync/manifest");
    const m = await r.json();
    const n = (m.items || []).length;
    statusEl.textContent =
      "manifest: " + n + " رکورد · schema " + (m.schema_version || 1) +
      " · " + (m.generated_at || "");
  } catch (e) {
    if (statusEl) statusEl.textContent = "خطا: " + (e.message || e);
  }
});

loadLanAndSync();
