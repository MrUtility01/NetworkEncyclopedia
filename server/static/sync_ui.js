/* LAN IP + Sync status bar — IP از /api/lan بدون توکن — پورت پیش‌فرض 83 */
async function loadLanAndSync() {
  const lanEl = document.getElementById("lanIp");
  const hintEl = document.getElementById("androidHint");
  const statusEl = document.getElementById("syncStatus");
  if (!lanEl) return;
  try {
    const r = await fetch("/api/lan");
    const data = await r.json();
    const ip = data.lan_ip || (data.lan_ips && data.lan_ips[0]) || "127.0.0.1";
    const port = data.port || 83;
    lanEl.textContent = ip;
    if (hintEl) hintEl.textContent = "http://" + ip + ":" + port;
    if (statusEl) {
      const extra = (data.lan_ips && data.lan_ips.length > 1)
        ? " · سایر: " + data.lan_ips.slice(1).join(", ")
        : "";
      statusEl.textContent = "پورت " + port + " · bind " + (data.bind_host || "0.0.0.0") + extra;
    }
  } catch (e) {
    lanEl.textContent = "خطا";
    if (statusEl) statusEl.textContent = String(e.message || e);
  }
}

document.getElementById("btnCopyIp")?.addEventListener("click", async () => {
  const ip = document.getElementById("lanIp")?.textContent || "";
  const hint = document.getElementById("androidHint")?.textContent || ("http://" + ip + ":83");
  try {
    await navigator.clipboard.writeText(hint);
    const st = document.getElementById("syncStatus");
    if (st) st.textContent = "کپی شد: " + hint;
  } catch {
    prompt("آدرس را کپی کنید:", hint);
  }
});

document.getElementById("btnSyncStatus")?.addEventListener("click", async () => {
  const statusEl = document.getElementById("syncStatus");
  if (statusEl) statusEl.textContent = "در حال بررسی…";
  try {
    const h = await fetch("/api/health").then((r) => r.json());
    const s = h.stats || {};
    statusEl.textContent =
      "سلامت OK · فصل " + (s.chapters || 0) +
      " · درس " + (s.lessons || 0) +
      " · محتوا " + (s.with_content || 0) +
      " · LAN " + (h.lan_ip || "—");
  } catch (e) {
    if (statusEl) statusEl.textContent = "خطا: " + (e.message || e);
  }
});

loadLanAndSync();
