/* Engineer Jokar Web - enhanced UI */
const $ = (s) => document.querySelector(s);
const chaptersEl = $("#chapters");
const viewer = $("#viewer");
const breadcrumb = $("#breadcrumb");
const statsEl = $("#stats");
const state = { chapters: [], levelsCache: {}, lessonsCache: {}, view: "home" };
const LS_TASKS = "netenc_tasks_v1";
const LS_NOTES = "netenc_notes_v1";

async function api(path, opts) {
  opts = opts || {};
  const headers = Object.assign({}, opts.headers || {});
  if (typeof netencGetToken === "function") {
    headers["Authorization"] = "Bearer " + netencGetToken();
    headers["X-NetEnc-Token"] = netencGetToken();
  }
  const r = await fetch(path, Object.assign({}, opts, { headers: headers }));
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}
function asList(data, key) {
  if (Array.isArray(data)) return data;
  if (data && Array.isArray(data[key])) return data[key];
  if (data && Array.isArray(data.items)) return data.items;
  return [];
}
function escapeHtml(s) {
  var d = document.createElement("div");
  d.textContent = s == null ? "" : String(s);
  return d.innerHTML;
}
function uid() { return "id_" + Date.now().toString(36) + Math.random().toString(36).slice(2, 8); }
function loadLS(key) { try { return JSON.parse(localStorage.getItem(key) || "[]"); } catch (e) { return []; } }
function saveLS(key, arr) { localStorage.setItem(key, JSON.stringify(arr)); }
function setNav(activeId) {
  ["btnHome", "btnTasks", "btnNotes", "btnScenarios", "btnQuiz", "btnInfo", "btnKnowledge"].forEach(function (id) {
    var el = document.getElementById(id);
    if (el) el.classList.toggle("active", id === activeId);
  });
}
async function loadStats() {
  try {
    var s = await api("/api/stats");
    statsEl.textContent = s.chapters + " فصل · " + s.levels + " زیر‌فصل · " + s.lessons + " درس · " + s.scenarios + " سناریو · محتوا: " + s.with_content;
  } catch (e) { statsEl.textContent = "خطا در آمار"; }
}
async function loadChapters() {
  chaptersEl.innerHTML = '<div class="loading">بارگذاری فهرست فصل‌ها…</div>';
  try {
    var list = asList(await api("/api/chapters"), "chapters");
    state.chapters = list;
    chaptersEl.innerHTML = "";
    if (!list.length) { chaptersEl.innerHTML = '<div class="loading">فصلی نیست — بازسازی را بزنید</div>'; return; }
    list.forEach(function (ch) {
      var wrap = document.createElement("div");
      wrap.className = "ch-item";
      wrap.innerHTML = '<button type="button" class="ch-btn" data-id="' + ch.id + '"><span class="caret">▶</span><span class="ch-title">' + escapeHtml(ch.title_fa) + '</span><span class="badge">' + ch.order_index + '</span></button><div class="nested" id="ch-nest-' + ch.id + '"></div>';
      chaptersEl.appendChild(wrap);
    });
  } catch (err) { chaptersEl.innerHTML = '<div class="loading">خطا: ' + escapeHtml(err.message) + "</div>"; }
}
function renderHome() {
  state.view = "home"; setNav("btnHome"); breadcrumb.textContent = "خانه";
  var tasks = loadLS(LS_TASKS); var notes = loadLS(LS_NOTES);
  var openTasks = tasks.filter(function (t) { return !t.done; }).length;
  viewer.innerHTML = '<div class="welcome"><h1>دایرةالمعارف شبکه — Network Engineer</h1><p>محتوای غنی · اینفوگرافیک · کار و نکته · سناریو · آزمون ' + QUIZ_BANK.length + ' سوالی.</p><div class="grid" style="margin-bottom:14px"><div class="card-link"><strong>' + openTasks + '</strong><span class="muted">کار باز</span></div><div class="card-link"><strong>' + notes.length + '</strong><span class="muted">نکته</span></div><div class="card-link"><strong>' + QUIZ_BANK.length + '</strong><span class="muted">سوال</span></div><div class="card-link"><strong>' + (state.chapters.length || "—") + '</strong><span class="muted">فصل</span></div></div><div class="grid"><div class="card-link" data-go="info"><strong>اینفوگرافیک</strong><span class="muted">مسیر پکت</span></div><div class="card-link" data-go="knowledge"><strong>مدیریت دانش</strong><span class="muted">مرور</span></div><div class="card-link" data-go="tasks"><strong>کارها</strong><span class="muted">اولویت</span></div><div class="card-link" data-go="notes"><strong>نکته‌ها</strong><span class="muted">جستجو</span></div><div class="card-link" data-go="scenarios"><strong>سناریو</strong><span class="muted">Capstone</span></div><div class="card-link" data-go="quiz"><strong>آزمون</strong><span class="muted">' + QUIZ_BANK.length + ' سوال</span></div></div></div>';
  viewer.querySelectorAll("[data-go]").forEach(function (el) {
    el.addEventListener("click", function () {
      var g = el.getAttribute("data-go");
      if (g === "tasks") renderTasks();
      if (g === "notes") renderNotes();
      if (g === "scenarios") renderScenarios();
      if (g === "quiz") renderQuiz();
      if (g === "info") renderInfographics();
      if (g === "knowledge") renderKnowledge();
    });
  });
}
function renderTasks() {
  state.view = "tasks"; setNav("btnTasks"); breadcrumb.textContent = "کارهای روزانه";
  var today = new Date().toISOString().slice(0, 10);
  viewer.innerHTML = '<div class="ws-panel"><h2>کارهای روزانه</h2><p class="muted">اولویت · سررسید · فیلتر · خروجی</p><div class="ws-form"><input id="taskTitle" placeholder="عنوان" /><textarea id="taskBody" placeholder="توضیح"></textarea><div style="display:flex;gap:8px;flex-wrap:wrap"><input id="taskDue" type="date" value="' + today + '" style="flex:1" /><select id="taskPri" style="flex:1"><option value="normal">عادی</option><option value="high">بالا</option><option value="low">پایین</option></select></div><div style="display:flex;gap:8px;flex-wrap:wrap"><button type="button" id="taskAdd">افزودن</button><button type="button" class="ghost" id="taskFilterAll">همه</button><button type="button" class="ghost" id="taskFilterOpen">باز</button><button type="button" class="ghost" id="taskFilterDone">انجام‌شده</button><button type="button" class="ghost" id="taskExport">خروجی</button></div></div><div class="ws-list" id="taskList"></div></div>';
  var listEl = $("#taskList"); var filter = "all";
  function paint() {
    var arr = loadLS(LS_TASKS).slice();
    if (filter === "open") arr = arr.filter(function (t) { return !t.done; });
    if (filter === "done") arr = arr.filter(function (t) { return t.done; });
    arr.sort(function (a, b) { if (a.done !== b.done) return a.done ? 1 : -1; var pw = { high: 0, normal: 1, low: 2 }; return (pw[a.pri] || 1) - (pw[b.pri] || 1); });
    if (!arr.length) { listEl.innerHTML = '<div class="loading">موردی نیست</div>'; return; }
    listEl.innerHTML = arr.map(function (t) {
      var pri = t.pri === "high" ? "🔴 " : t.pri === "low" ? "⚪ " : "🔵 ";
      return '<div class="ws-item ' + (t.done ? "done" : "") + '" data-id="' + t.id + '"><div class="row"><div><h3>' + (t.done ? "✓ " : "○ ") + pri + escapeHtml(t.title) + '</h3><p>' + escapeHtml(t.body || "") + '</p><div class="meta">سررسید: ' + escapeHtml(t.due || "—") + '</div></div><div class="actions"><button type="button" class="ghost t-toggle">' + (t.done ? "بازگشت" : "انجام شد") + '</button><button type="button" class="ghost danger t-del">حذف</button></div></div></div>';
    }).join("");
    listEl.querySelectorAll(".t-toggle").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var id = btn.closest(".ws-item").dataset.id; var all = loadLS(LS_TASKS); var t = all.find(function (x) { return x.id === id; });
        if (t) t.done = !t.done; saveLS(LS_TASKS, all); paint();
      });
    });
    listEl.querySelectorAll(".t-del").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var id = btn.closest(".ws-item").dataset.id;
        saveLS(LS_TASKS, loadLS(LS_TASKS).filter(function (x) { return x.id !== id; })); paint();
      });
    });
  }
  $("#taskAdd").onclick = function () {
    var title = $("#taskTitle").value.trim(); if (!title) return;
    var all = loadLS(LS_TASKS);
    all.unshift({ id: uid(), title: title, body: $("#taskBody").value.trim(), due: $("#taskDue").value, pri: $("#taskPri").value || "normal", done: false, ts: Date.now() });
    saveLS(LS_TASKS, all); $("#taskTitle").value = ""; $("#taskBody").value = ""; paint();
  };
  $("#taskFilterAll").onclick = function () { filter = "all"; paint(); };
  $("#taskFilterOpen").onclick = function () { filter = "open"; paint(); };
  $("#taskFilterDone").onclick = function () { filter = "done"; paint(); };
  $("#taskExport").onclick = function () {
    var arr = loadLS(LS_TASKS);
    var text = arr.map(function (t, i) { return (i + 1) + ". [" + (t.done ? "x" : " ") + "] " + (t.pri || "normal") + " | " + t.title + (t.due ? " @ " + t.due : "") + (t.body ? "\n   " + t.body : ""); }).join("\n");
    var w = window.open("", "_blank"); if (w) w.document.write("<pre>" + escapeHtml(text || "خالی") + "</pre>");
  };
  paint();
}
function renderNotes() {
  state.view = "notes"; setNav("btnNotes"); breadcrumb.textContent = "نکته‌ها";
  viewer.innerHTML = '<div class="ws-panel"><h2>نکته‌ها</h2><p class="muted">برچسب · جستجو · خروجی</p><div class="ws-form"><input id="noteTitle" placeholder="عنوان" /><textarea id="noteBody" placeholder="متن"></textarea><input id="noteTag" placeholder="برچسب" /><input id="noteSearch" placeholder="جستجو…" /><div style="display:flex;gap:8px"><button type="button" id="noteAdd">ذخیره</button><button type="button" class="ghost" id="noteExport">خروجی</button></div></div><div class="ws-list" id="noteList"></div></div>';
  var listEl = $("#noteList");
  function paint() {
    var q = (($("#noteSearch") && $("#noteSearch").value) || "").trim().toLowerCase();
    var arr = loadLS(LS_NOTES).filter(function (n) {
      if (!q) return true;
      return (n.title || "").toLowerCase().indexOf(q) >= 0 || (n.body || "").toLowerCase().indexOf(q) >= 0 || (n.tag || "").toLowerCase().indexOf(q) >= 0;
    });
    if (!arr.length) { listEl.innerHTML = '<div class="loading">موردی نیست</div>'; return; }
    listEl.innerHTML = arr.map(function (n) {
      return '<div class="ws-item" data-id="' + n.id + '"><div class="row"><div><h3>' + escapeHtml(n.title) + '</h3><p>' + escapeHtml(n.body || "") + '</p><div class="meta">' + (n.tag ? "#" + escapeHtml(n.tag) + " · " : "") + (n.ts ? new Date(n.ts).toLocaleString("fa-IR") : "") + '</div></div><div class="actions"><button type="button" class="ghost danger n-del">حذف</button></div></div></div>';
    }).join("");
    listEl.querySelectorAll(".n-del").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var id = btn.closest(".ws-item").dataset.id;
        saveLS(LS_NOTES, loadLS(LS_NOTES).filter(function (x) { return x.id !== id; })); paint();
      });
    });
  }
  $("#noteAdd").onclick = function () {
    var title = $("#noteTitle").value.trim(); if (!title) return;
    var all = loadLS(LS_NOTES);
    all.unshift({ id: uid(), title: title, body: $("#noteBody").value.trim(), tag: $("#noteTag").value.trim(), ts: Date.now() });
    saveLS(LS_NOTES, all); $("#noteTitle").value = ""; $("#noteBody").value = ""; $("#noteTag").value = ""; paint();
  };
  $("#noteSearch").oninput = function () { paint(); };
  $("#noteExport").onclick = function () {
    var arr = loadLS(LS_NOTES);
    var text = arr.map(function (n, i) { return (i + 1) + ". " + n.title + (n.tag ? " [" + n.tag + "]" : "") + "\n" + (n.body || ""); }).join("\n\n");
    var w = window.open("", "_blank"); if (w) w.document.write("<pre>" + escapeHtml(text || "خالی") + "</pre>");
  };
  paint();
}
async function renderScenarios() {
  state.view = "scenarios"; setNav("btnScenarios"); breadcrumb.textContent = "سناریوها";
  viewer.innerHTML = '<div class="loading">…</div>';
  try {
    var list = asList(await api("/api/scenarios"), "scenarios");
    if (!list.length) { viewer.innerHTML = '<div class="ws-panel"><p>سناریویی نیست</p></div>'; return; }
    viewer.innerHTML = '<div class="scenario-list">' + list.map(function (s) { return '<div class="scenario-card" data-sid="' + s.id + '"><h3>' + escapeHtml(s.title_fa || s.code || "") + '</h3></div>'; }).join("") + '</div>';
    viewer.querySelectorAll(".scenario-card").forEach(function (card) {
      card.addEventListener("click", async function () {
        var sc = await api("/api/scenarios/" + card.dataset.sid);
        breadcrumb.textContent = sc.title_fa || "سناریو";
        viewer.innerHTML = '<div class="lesson-card"><h1>' + escapeHtml(sc.title_fa || "") + '</h1><pre class="content-pre">' + escapeHtml(sc.business_context || sc.tasks || "—") + '</pre><p><button type="button" class="ghost" id="backSc">بازگشت</button></p></div>';
        $("#backSc").onclick = function () { renderScenarios(); };
      });
    });
  } catch (e) { viewer.innerHTML = '<div class="loading">خطا</div>'; }
}
var QUIZ_BANK = [
  { q: "جداسازی Broadcast Domain در لایه ۲؟", opts: ["VLAN", "OSPF", "FTP", "NTP"], a: 0 },
  { q: "برقراری اتصال TCP؟", opts: ["Three-way Handshake", "ARP Storm", "DHCP Discover", "ICMP Echo"], a: 0 },
  { q: "کدام آدرس خصوصی است؟", opts: ["8.8.8.8", "192.168.10.5", "1.1.1.1", "9.9.9.9"], a: 1 },
  { q: "هدف اصلی NAT؟", opts: ["رمزنگاری", "ترجمه آدرس", "OSPF", "DNS"], a: 1 },
  { q: "رکورد DNS برای IPv6؟", opts: ["A", "AAAA", "MX", "CNAME"], a: 1 },
  { q: "Native VLAN روی Trunk؟", opts: ["بدون تگ ارسال می‌شود", "همیشه VLAN 100", "فقط مدیریت", "غیرفعال"], a: 0 },
  { q: "OSPF Area 0؟", opts: ["Backbone", "فقط Stub", "فقط NSSA", "جایگزین BGP"], a: 0 },
  { q: "eBGP در برابر iBGP؟", opts: ["بین AS در برابر داخل AS", "سرعت لینک", "فقط IPv6", "نوع کابل"], a: 0 },
  { q: "ترتیب DHCP؟", opts: ["Discover-Offer-Request-Ack", "Ack-Request-Offer", "Only Discover", "ARP-first"], a: 0 },
  { q: "هدف STP؟", opts: ["جلوگیری از حلقه L2", "رمزنگاری", "NAT", "QoS"], a: 0 },
  { q: "HSRP/VRRP؟", opts: ["Gateway مجازی", "فقط DNS", "فقط VPN", "L7 LB"], a: 0 },
  { q: "Stateful Firewall؟", opts: ["ردیابی Session", "فقط IP ثابت", "بدون لاگ", "فقط IDS"], a: 0 },
  { q: "RPO یعنی؟", opts: ["حداکثر داده قابل از دست رفتن", "زمان بازیابی", "حجم دیسک", "تعداد نوار"], a: 0 },
  { q: "AAA؟", opts: ["Authentication Authorization Accounting", "ARP ACL Address", "Always Allow All", "Active Agent"], a: 0 },
  { q: "Idempotent؟", opts: ["تکرار نتیجه را خراب نمی‌کند", "فقط یک‌بار", "بدون Inventory", "بدون لاگ"], a: 0 },
  { q: "SNMP؟", opts: ["مانیتورینگ", "فایل‌شیر", "رمز دیسک", "تلفن"], a: 0 },
  { q: "Port Security؟", opts: ["محدود کردن MAC", "OSPF", "BGP flap", "DNS"], a: 0 },
  { q: "MTU بزرگ‌تر از مسیر؟", opts: ["Fragment یا Drop", "سرعت بی‌نهایت", "قطع STP", "حذف VLAN"], a: 0 },
  { q: "Syslog؟", opts: ["جمع رویداد", "مسیریابی", "NAT", "Backup"], a: 0 },
  { q: "SD-WAN؟", opts: ["سیاست مسیر بر اساس کیفیت لینک", "فقط مس", "فقط WiFi", "چاپگر"], a: 0 },
  { q: "WireGuard؟", opts: ["تونل رمز سبک", "فقط L2", "جایگزین STP", "چاپ"], a: 0 },
  { q: "DHCP Snooping؟", opts: ["ضد DHCP جعلی", "افزایش OSPF", "NAT", "حذف VLAN"], a: 0 },
  { q: "MikroTik chain input؟", opts: ["به خود روتر", "فقط WAN", "فقط forward", "فقط VPN"], a: 0 },
  { q: "IPsec Phase1؟", opts: ["کانال IKE", "فقط NAT", "فقط DNS", "STP"], a: 0 },
  { q: "APIPA؟", opts: ["169.254.0.0/16", "10.0.0.0/8", "8.8.8.0/24", "224.0.0.0/4"], a: 0 },
  { q: "BPDU Guard؟", opts: ["قطع پورت با BPDU", "افزایش BW", "NAT", "DNS cache"], a: 0 },
  { q: "Local Pref؟", opts: ["خروج از AS", "رمزنگاری", "فقط IPv6", "نام interface"], a: 0 },
  { q: "RTO؟", opts: ["زمان بازگشت سرویس", "حجم بکاپ", "تعداد VLAN", "سرعت پورت"], a: 0 },
  { q: "802.1X RADIUS؟", opts: ["احراز هویت", "فقط DHCP", "STP root", "NAT"], a: 0 },
  { q: "ECMP؟", opts: ["چند مسیر هم‌ارز", "یک مسیر", "قطع OSPF", "حذف ACL"], a: 0 },
  { q: "DMZ؟", opts: ["سرویس محدود به داخل", "حذف فایروال", "فقط WiFi", "چاپگر"], a: 0 },
  { q: "NetFlow؟", opts: ["Top Talker / جریان", "رمز دیسک", "تعویض کابل", "NTP"], a: 0 },
  { q: "Split-tunnel؟", opts: ["بخشی از ترافیک از تونل", "همه قطع", "فقط DNS", "چاپ"], a: 0 },
  { q: "همسایه OSPF؟", opts: ["show ip ospf neighbor", "show vlan brief", "show arp only", "show clock"], a: 0 },
  { q: "هدف CoPP؟", opts: ["محافظت control plane", "فقط NAT", "حذف VLAN", "چاپ"], a: 0 }
];
function renderQuiz() {
  state.view = "quiz"; setNav("btnQuiz"); breadcrumb.textContent = "سوالات";
  var i = 0, score = 0;
  function show() {
    if (i >= QUIZ_BANK.length) {
      viewer.innerHTML = '<div class="quiz-box"><h2>پایان</h2><p>' + score + '/' + QUIZ_BANK.length + '</p><button type="button" id="quizAgain">دوباره</button> <button type="button" class="ghost" id="goHome2">خانه</button></div>';
      $("#quizAgain").onclick = function () { i = 0; score = 0; show(); };
      $("#goHome2").onclick = function () { renderHome(); };
      return;
    }
    var item = QUIZ_BANK[i];
    viewer.innerHTML = '<div class="quiz-box"><div class="q">(' + (i + 1) + '/' + QUIZ_BANK.length + ') ' + escapeHtml(item.q) + '</div>' + item.opts.map(function (o, idx) { return '<button type="button" class="opt" data-i="' + idx + '">' + escapeHtml(o) + '</button>'; }).join('') + '</div>';
    var locked = false;
    viewer.querySelectorAll(".opt").forEach(function (btn) {
      btn.addEventListener("click", function () {
        if (locked) return; locked = true;
        var ok = +btn.dataset.i === item.a; if (ok) score++;
        btn.classList.add(ok ? "correct" : "wrong");
        viewer.querySelectorAll(".opt").forEach(function (b) { if (+b.dataset.i === item.a) b.classList.add("correct"); });
        setTimeout(function () { i++; show(); }, 650);
      });
    });
  }
  show();
}
async function renderInfographics() {
  state.view = "info"; setNav("btnInfo"); breadcrumb.textContent = "اینفوگرافیک";
  viewer.innerHTML = '<div class="loading">…</div>';
  try {
    var data = await api("/api/infographics"); var items = data.items || [];
    if (!items.length) { viewer.innerHTML = '<div class="ws-panel"><p>خالی</p></div>'; return; }
    viewer.innerHTML = '<div class="info-gallery"><div class="ws-panel" style="max-width:960px"><h2>اینفوگرافیک</h2><p><button type="button" class="ghost" id="infoHome">خانه</button></p><div class="info-toc">' + items.map(function (it, idx) { return '<a class="chip" href="#inf-' + idx + '">' + escapeHtml(it.title || '') + '</a>'; }).join('') + '</div>' + items.map(function (it, idx) { return '<article class="info-card" id="inf-' + idx + '"><h3>' + escapeHtml(it.title || '') + '</h3><div class="info-svg">' + (it.svg || '') + '</div></article>'; }).join('') + '</div></div>';
    var ih = document.getElementById("infoHome"); if (ih) ih.onclick = function () { renderHome(); };
  } catch (e) { viewer.innerHTML = '<div class="loading">خطا</div>'; }
}
function renderKnowledge() {
  state.view = "knowledge"; setNav("btnKnowledge"); breadcrumb.textContent = "مدیریت دانش";
  viewer.innerHTML = '<div class="ws-panel" style="max-width:900px"><h2>مدیریت دانش</h2><p><button type="button" class="ghost" id="kmHome">خانه</button></p><div class="grid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px"><div class="card-link" data-km="tasks"><strong>کارها</strong></div><div class="card-link" data-km="notes"><strong>نکته‌ها</strong></div><div class="card-link" data-km="quiz"><strong>آزمون (' + QUIZ_BANK.length + ')</strong></div><div class="card-link" data-km="info"><strong>اینفوگرافیک</strong></div><div class="card-link" data-km="scenarios"><strong>سناریو</strong></div><a class="card-link" href="/workspace" style="text-decoration:none;color:inherit"><strong>فضای کاری+</strong></a></div></div>';
  document.getElementById("kmHome").onclick = function () { renderHome(); };
  viewer.querySelectorAll("[data-km]").forEach(function (el) {
    el.addEventListener("click", function () {
      var k = el.getAttribute("data-km");
      if (k === "tasks") renderTasks(); if (k === "notes") renderNotes();
      if (k === "quiz") renderQuiz(); if (k === "info") renderInfographics(); if (k === "scenarios") renderScenarios();
    });
  });
}
chaptersEl.addEventListener("click", async function (e) {
  var chBtn = e.target.closest(".ch-btn"); var lvBtn = e.target.closest(".lv-btn"); var lesBtn = e.target.closest(".les-btn");
  if (chBtn) return onChapterClick(chBtn); if (lvBtn) return onLevelClick(lvBtn); if (lesBtn) return onLessonClick(lesBtn);
});
async function onChapterClick(btn) {
  var id = +btn.dataset.id; var nest = document.getElementById("ch-nest-" + id); var caret = btn.querySelector(".caret");
  if (nest.classList.contains("open")) { nest.classList.remove("open"); caret.textContent = "▶"; btn.classList.remove("active"); return; }
  btn.classList.add("active"); caret.textContent = "▼"; nest.classList.add("open"); nest.innerHTML = '<div class="loading">…</div>';
  try {
    if (!state.levelsCache[id]) { var data = await api("/api/chapters/" + id + "/levels"); state.levelsCache[id] = asList(data, "levels"); }
    var levels = state.levelsCache[id] || []; nest.innerHTML = "";
    levels.forEach(function (lv) {
      var d = document.createElement("div"); d.className = "lv-item";
      d.innerHTML = '<button type="button" class="lv-btn" data-id="' + lv.id + '" data-ch="' + id + '"><span class="caret">▶</span><span class="ch-title">' + escapeHtml(lv.title_fa || lv.code || ("سطح " + lv.id)) + '</span></button><div class="nested" id="lv-nest-' + lv.id + '"></div>';
      nest.appendChild(d);
    });
    if (!levels.length) nest.innerHTML = '<div class="loading">زیرفصلی نیست</div>';
  } catch (err) { nest.innerHTML = '<div class="loading">خطا</div>'; }
}
async function onLevelClick(btn) {
  var id = +btn.dataset.id; var nest = document.getElementById("lv-nest-" + id); var caret = btn.querySelector(".caret");
  if (nest.classList.contains("open")) { nest.classList.remove("open"); caret.textContent = "▶"; btn.classList.remove("active"); return; }
  btn.classList.add("active"); caret.textContent = "▼"; nest.classList.add("open"); nest.innerHTML = '<div class="loading">…</div>';
  try {
    if (!state.lessonsCache[id]) { var data = await api("/api/levels/" + id + "/lessons"); state.lessonsCache[id] = asList(data, "lessons"); }
    var lessons = state.lessonsCache[id] || []; nest.innerHTML = "";
    lessons.forEach(function (ls) {
      var d = document.createElement("div"); d.className = "les-item";
      var ok = ls.has_content || ls.with_content || (ls.content_len && ls.content_len > 50);
      d.innerHTML = '<button type="button" class="les-btn" data-id="' + ls.id + '"><span class="dot ' + (ok ? "ok" : "") + '"></span><span class="ch-title">' + escapeHtml(ls.title_fa || ls.title || ("درس " + ls.id)) + '</span></button>';
      nest.appendChild(d);
    });
    if (!lessons.length) nest.innerHTML = '<div class="loading">درسی نیست</div>';
  } catch (err) { nest.innerHTML = '<div class="loading">خطا</div>'; }
}
async function onLessonClick(btn) {
  var id = +btn.dataset.id; breadcrumb.textContent = "درس"; viewer.innerHTML = '<div class="loading">…</div>';
  try {
    var L = await api("/api/lessons/" + id);
    var body = L.full_content || L.content || L.body || ""; var cmds = L.commands || ""; var examples = L.examples || ""; var notes = L.notes || "";
    breadcrumb.textContent = L.title_fa || "درس";
    viewer.innerHTML = '<div class="lesson-card"><h1>' + escapeHtml(L.title_fa || "") + '</h1><div class="tabs"><button type="button" class="tab active" data-tab="main">محتوا</button>' + (cmds ? '<button type="button" class="tab" data-tab="cmd">دستورات</button>' : '') + (examples ? '<button type="button" class="tab" data-tab="ex">مثال</button>' : '') + (notes ? '<button type="button" class="tab" data-tab="note">نکات</button>' : '') + '</div><div class="tab-body" id="tabMain"><pre class="content-pre">' + escapeHtml(body) + '</pre></div>' + (cmds ? '<div class="tab-body" id="tabCmd" hidden><pre class="content-pre">' + escapeHtml(cmds) + '</pre></div>' : '') + (examples ? '<div class="tab-body" id="tabEx" hidden><pre class="content-pre">' + escapeHtml(examples) + '</pre></div>' : '') + (notes ? '<div class="tab-body" id="tabNote" hidden><pre class="content-pre">' + escapeHtml(notes) + '</pre></div>' : '') + '</div>';
    viewer.querySelectorAll(".tab").forEach(function (tab) {
      tab.addEventListener("click", function () {
        viewer.querySelectorAll(".tab").forEach(function (t) { t.classList.remove("active"); }); tab.classList.add("active");
        var map = { main: "tabMain", cmd: "tabCmd", ex: "tabEx", note: "tabNote" };
        Object.keys(map).forEach(function (k) { var el = document.getElementById(map[k]); if (el) el.hidden = tab.getAttribute("data-tab") !== k; });
      });
    });
  } catch (e) { viewer.innerHTML = '<div class="loading">خطا</div>'; }
}
var btnHome = document.getElementById("btnHome"); if (btnHome) btnHome.onclick = function () { renderHome(); };
var btnTasks = document.getElementById("btnTasks"); if (btnTasks) btnTasks.onclick = function () { renderTasks(); };
var btnNotes = document.getElementById("btnNotes"); if (btnNotes) btnNotes.onclick = function () { renderNotes(); };
var btnScenarios = document.getElementById("btnScenarios"); if (btnScenarios) btnScenarios.onclick = function () { renderScenarios(); };
var btnQuiz = document.getElementById("btnQuiz"); if (btnQuiz) btnQuiz.onclick = function () { renderQuiz(); };
var btnInfo = document.getElementById("btnInfo"); if (btnInfo) btnInfo.onclick = function () { renderInfographics(); };
var btnKnowledge = document.getElementById("btnKnowledge"); if (btnKnowledge) btnKnowledge.onclick = function () { renderKnowledge(); };
var btnBrand = document.getElementById("btnBrand"); if (btnBrand) btnBrand.onclick = function () { renderHome(); };
var btnLogout = document.getElementById("btnLogout"); if (btnLogout) btnLogout.onclick = function () { if (typeof netencLock === "function") netencLock(); location.reload(); };
var btnReseed = document.getElementById("btnReseed");
if (btnReseed) btnReseed.onclick = async function () {
  if (!confirm("بازسازی؟")) return;
  try { await api("/api/reseed", { method: "POST" }); state.levelsCache = {}; state.lessonsCache = {}; await loadStats(); await loadChapters(); alert("انجام شد"); }
  catch (e) { alert("خطا: " + e.message); }
};
var btnSearch = document.getElementById("btnSearch"); var qInput = document.getElementById("q");
if (btnSearch && qInput) {
  async function doSearch() {
    var q = qInput.value.trim(); if (!q) return;
    breadcrumb.textContent = "جستجو: " + q; viewer.innerHTML = '<div class="loading">…</div>';
    try {
      var data = await api("/api/search?q=" + encodeURIComponent(q));
      var items = asList(data, "results"); if (!items.length) items = asList(data, "lessons");
      if (!items.length) { viewer.innerHTML = '<div class="ws-panel"><p>نتیجه‌ای نبود</p></div>'; return; }
      viewer.innerHTML = '<div class="scenario-list">' + items.map(function (it) { return '<div class="scenario-card" data-lid="' + (it.id || it.lesson_id) + '"><h3>' + escapeHtml(it.title_fa || it.title || '') + '</h3></div>'; }).join('') + '</div>';
      viewer.querySelectorAll("[data-lid]").forEach(function (card) {
        card.addEventListener("click", function () { onLessonClick({ dataset: { id: card.getAttribute("data-lid") } }); });
      });
    } catch (e) { viewer.innerHTML = '<div class="loading">خطا</div>'; }
  }
  btnSearch.onclick = doSearch;
  qInput.addEventListener("keydown", function (e) { if (e.key === "Enter") doSearch(); });
}
if (typeof netencSetupLogin === "function") {
  netencSetupLogin(function () { loadStats(); loadChapters(); renderHome(); });
} else { loadStats(); loadChapters(); renderHome(); }
