/* Engineer Jokar Web — login-gated UI */
const $ = (s) => document.querySelector(s);
const chaptersEl = $("#chapters");
const viewer = $("#viewer");
const breadcrumb = $("#breadcrumb");
const statsEl = $("#stats");

const state = {
  chapters: [],
  levelsCache: {},
  lessonsCache: {},
  view: "home",
};

const LS_TASKS = "netenc_tasks_v1";
const LS_NOTES = "netenc_notes_v1";

async function api(path, opts = {}) {
  const headers = Object.assign({}, (opts && opts.headers) || {});
  if (typeof netencGetToken === "function") {
    headers["Authorization"] = "Bearer " + netencGetToken();
    headers["X-NetEnc-Token"] = netencGetToken();
  }
  const r = await fetch(path, Object.assign({}, opts, { headers }));
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
  return String(s || "")
    .replace(/&/g, "&")
    .replace(/</g, "<")
    .replace(/>/g, ">")
    .replace(/"/g, """);
}

function uid() {
  return "id_" + Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
}

function loadLS(key) {
  try {
    return JSON.parse(localStorage.getItem(key) || "[]");
  } catch (e) {
    return [];
  }
}
function saveLS(key, arr) {
  localStorage.setItem(key, JSON.stringify(arr));
}

function setNav(activeId) {
  ["btnHome", "btnTasks", "btnNotes", "btnScenarios", "btnQuiz", "btnInfo"].forEach((id) => {
    const el = document.getElementById(id);
    if (el) el.classList.toggle("active", id === activeId);
  });
}

async function loadStats() {
  try {
    const s = await api("/api/stats");
    statsEl.textContent = `${s.chapters} فصل · ${s.levels} زیر‌فصل · ${s.lessons} درس · ${s.scenarios} سناریو · محتوا: ${s.with_content}`;
  } catch (e) {
    statsEl.textContent = "خطا در آمار";
  }
}

async function loadChapters() {
  chaptersEl.innerHTML = `<div class="loading">بارگذاری فهرست فصل‌ها…</div>`;
  try {
    const list = asList(await api("/api/chapters"), "chapters");
    state.chapters = list;
    chaptersEl.innerHTML = "";
    if (!list.length) {
      chaptersEl.innerHTML = `<div class="loading">فصلی نیست — بازسازی را بزنید</div>`;
      return;
    }
    list.forEach((ch) => {
      const wrap = document.createElement("div");
      wrap.className = "ch-item";
      wrap.innerHTML = `
      <button type="button" class="ch-btn" data-id="${ch.id}">
        <span class="caret">▶</span>
        <span class="ch-title">${escapeHtml(ch.title_fa)}</span>
        <span class="badge">${ch.order_index}</span>
      </button>
      <div class="nested" id="ch-nest-${ch.id}"></div>`;
      chaptersEl.appendChild(wrap);
    });
  } catch (err) {
    chaptersEl.innerHTML = `<div class="loading">خطا: ${escapeHtml(err.message)}</div>`;
  }
}

function renderHome() {
  state.view = "home";
  setNav("btnHome");
  breadcrumb.textContent = "خانه";
  viewer.innerHTML = `
    <div class="welcome">
      <h1>دایرةالمعارف شبکه — Network Engineer</h1>
      <p>مطالب دسته‌محور · اینفوگرافیک · کارها و نکته‌ها · سناریو و سوالات.</p>
      <div class="grid">
        <div class="card-link" data-go="info"><strong>اینفوگرافیک</strong><span class="muted">مسیر پکت / سوئیچ / روتر / وای‌فای</span></div>
        <div class="card-link" data-go="tasks"><strong>کارهای روزانه</strong><span class="muted">لیست کار و پیگیری</span></div>
        <div class="card-link" data-go="notes"><strong>نکته‌ها</strong><span class="muted">یادداشت سریع</span></div>
        <div class="card-link" data-go="scenarios"><strong>سناریوها</strong><span class="muted">Capstone سازمانی</span></div>
        <div class="card-link" data-go="quiz"><strong>سوالات</strong><span class="muted">مرور چندگزینه‌ای</span></div>
      </div>
    </div>`;
  viewer.querySelectorAll("[data-go]").forEach((el) => {
    el.addEventListener("click", () => {
      const g = el.getAttribute("data-go");
      if (g === "tasks") renderTasks();
      if (g === "notes") renderNotes();
      if (g === "scenarios") renderScenarios();
      if (g === "quiz") renderQuiz();
      if (g === "info") renderInfographics();
    });
  });
}

function renderTasks() {
  state.view = "tasks";
  setNav("btnTasks");
  breadcrumb.textContent = "کارهای روزانه";
  const today = new Date().toISOString().slice(0, 10);
  viewer.innerHTML = `
    <div class="ws-panel">
      <h2>مدیریت کارهای روزانه</h2>
      <div class="ws-form">
        <input id="taskTitle" placeholder="عنوان کار" />
        <textarea id="taskBody" placeholder="توضیح / چک‌لیست"></textarea>
        <input id="taskDue" type="date" value="${today}" />
        <button type="button" id="taskAdd">افزودن کار</button>
      </div>
      <div class="ws-list" id="taskList"></div>
    </div>`;
  const listEl = $("#taskList");
  function paint() {
    const arr = loadLS(LS_TASKS);
    if (!arr.length) {
      listEl.innerHTML = `<div class="loading">هنوز کاری ثبت نشده</div>`;
      return;
    }
    arr.sort((a, b) => (a.done === b.done ? 0 : a.done ? 1 : -1));
    listEl.innerHTML = arr
      .map(
        (t) => `
      <div class="ws-item ${t.done ? "done" : ""}" data-id="${t.id}">
        <div class="row">
          <div>
            <h3>${t.done ? "✓ " : "○ "}${escapeHtml(t.title)}</h3>
            <p>${escapeHtml(t.body || "")}</p>
            <div class="meta">موعد: ${escapeHtml(t.due || "—")} · ${escapeHtml(t.created || "")}</div>
          </div>
          <div class="actions">
            <button type="button" class="ghost t-toggle">${t.done ? "بازگشت" : "انجام شد"}</button>
            <button type="button" class="ghost danger t-del">حذف</button>
          </div>
        </div>
      </div>`
      )
      .join("");
    listEl.querySelectorAll(".t-toggle").forEach((btn) => {
      btn.addEventListener("click", () => {
        const id = btn.closest(".ws-item").dataset.id;
        const all = loadLS(LS_TASKS);
        const t = all.find((x) => x.id === id);
        if (t) t.done = !t.done;
        saveLS(LS_TASKS, all);
        paint();
      });
    });
    listEl.querySelectorAll(".t-del").forEach((btn) => {
      btn.addEventListener("click", () => {
        const id = btn.closest(".ws-item").dataset.id;
        saveLS(LS_TASKS, loadLS(LS_TASKS).filter((x) => x.id !== id));
        paint();
      });
    });
  }
  $("#taskAdd").onclick = () => {
    const title = $("#taskTitle").value.trim();
    if (!title) return;
    const all = loadLS(LS_TASKS);
    all.unshift({
      id: uid(), title,
      body: $("#taskBody").value.trim(),
      due: $("#taskDue").value,
      done: false,
      created: new Date().toLocaleString("fa-IR"),
    });
    saveLS(LS_TASKS, all);
    $("#taskTitle").value = "";
    $("#taskBody").value = "";
    paint();
  };
  paint();
}

function renderNotes() {
  state.view = "notes";
  setNav("btnNotes");
  breadcrumb.textContent = "نکته‌ها و یادداشت‌ها";
  viewer.innerHTML = `
    <div class="ws-panel">
      <h2>مدیریت نکته‌ها</h2>
      <div class="ws-form">
        <input id="noteTitle" placeholder="عنوان نکته" />
        <textarea id="noteBody" placeholder="متن نکته"></textarea>
        <input id="noteTag" placeholder="برچسب" />
        <button type="button" id="noteAdd">ذخیره نکته</button>
      </div>
      <div class="ws-list" id="noteList"></div>
    </div>`;
  const listEl = $("#noteList");
  function paint() {
    const arr = loadLS(LS_NOTES);
    if (!arr.length) {
      listEl.innerHTML = `<div class="loading">نکته‌ای نیست</div>`;
      return;
    }
    listEl.innerHTML = arr
      .map(
        (n) => `
      <div class="ws-item" data-id="${n.id}">
        <div class="row">
          <div>
            <h3>${escapeHtml(n.title)}</h3>
            <p>${escapeHtml(n.body || "")}</p>
            <div class="meta">${escapeHtml(n.tag || "")} · ${escapeHtml(n.created || "")}</div>
          </div>
          <div class="actions">
            <button type="button" class="ghost danger n-del">حذف</button>
          </div>
        </div>
      </div>`
      )
      .join("");
    listEl.querySelectorAll(".n-del").forEach((btn) => {
      btn.addEventListener("click", () => {
        const id = btn.closest(".ws-item").dataset.id;
        saveLS(LS_NOTES, loadLS(LS_NOTES).filter((x) => x.id !== id));
        paint();
      });
    });
  }
  $("#noteAdd").onclick = () => {
    const title = $("#noteTitle").value.trim();
    if (!title) return;
    const all = loadLS(LS_NOTES);
    all.unshift({
      id: uid(), title,
      body: $("#noteBody").value.trim(),
      tag: $("#noteTag").value.trim(),
      created: new Date().toLocaleString("fa-IR"),
    });
    saveLS(LS_NOTES, all);
    $("#noteTitle").value = "";
    $("#noteBody").value = "";
    $("#noteTag").value = "";
    paint();
  };
  paint();
}

async function renderScenarios() {
  state.view = "scenarios";
  setNav("btnScenarios");
  breadcrumb.textContent = "سناریوهای Capstone";
  viewer.innerHTML = `<div class="loading">بارگذاری سناریوها…</div>`;
  try {
    const list = asList(await api("/api/scenarios"), "scenarios");
    if (!list.length) {
      viewer.innerHTML = `<div class="ws-panel"><p>سناریویی ثبت نشده.</p></div>`;
      return;
    }
    viewer.innerHTML = `<div class="scenario-list">${list
      .map(
        (s) => `
      <div class="scenario-card" data-sid="${s.id}">
        <h3>${escapeHtml(s.title_fa || s.code || "")}</h3>
        <div class="tags">
          <span class="chip">${escapeHtml(s.category || "Capstone")}</span>
          <span class="chip">${escapeHtml(s.level || "")}</span>
        </div>
      </div>`
      )
      .join("")}</div>`;
    viewer.querySelectorAll(".scenario-card").forEach((card) => {
      card.addEventListener("click", async () => {
        const sc = await api(`/api/scenarios/${card.dataset.sid}`);
        breadcrumb.textContent = sc.title_fa || "سناریو";
        viewer.innerHTML = `
          <div class="lesson-card">
            <h1>${escapeHtml(sc.title_fa || "")}</h1>
            <div class="tabs">
              <button type="button" class="tab active" data-k="business_context">زمینه</button>
              <button type="button" class="tab" data-k="tasks">وظایف</button>
              <button type="button" class="tab" data-k="solution">راه‌حل</button>
              <button type="button" class="tab" data-k="verification">اعتبارسنجی</button>
            </div>
            <div class="tab-body"><pre class="content-pre">${escapeHtml(sc.business_context || "—")}</pre></div>
            <p style="margin-top:12px"><button type="button" class="ghost" id="backSc">بازگشت</button></p>
          </div>`;
        const body = viewer.querySelector(".tab-body");
        viewer.querySelectorAll(".tab").forEach((tab) => {
          tab.addEventListener("click", () => {
            viewer.querySelectorAll(".tab").forEach((t) => t.classList.remove("active"));
            tab.classList.add("active");
            body.innerHTML = `<pre class="content-pre">${escapeHtml(sc[tab.dataset.k] || "—")}</pre>`;
          });
        });
        $("#backSc").onclick = () => renderScenarios();
      });
    });
  } catch (e) {
    viewer.innerHTML = `<div class="loading">خطا: ${escapeHtml(e.message)}</div>`;
  }
}

const QUIZ_BANK = [
  { q: "جداسازی Broadcast Domain در لایه ۲؟", opts: ["VLAN", "OSPF", "FTP", "NTP"], a: 0, exp: "VLAN" },
  { q: "برقراری TCP؟", opts: ["Three-way Handshake", "ARP", "DHCP", "ICMP"], a: 0, exp: "SYN SYN-ACK ACK" },
  { q: "آدرس خصوصی؟", opts: ["8.8.8.8", "192.168.10.5", "1.1.1.1", "9.9.9.9"], a: 1, exp: "RFC1918" },
  { q: "هدف NAT؟", opts: ["رمزنگاری", "ترجمه آدرس", "OSPF", "DNS"], a: 1, exp: "NAT" },
  { q: "رکورد IPv6؟", opts: ["A", "AAAA", "MX", "CNAME"], a: 1, exp: "AAAA" },
];

function renderQuiz() {
  state.view = "quiz";
  setNav("btnQuiz");
  breadcrumb.textContent = "سوالات";
  let i = 0, score = 0;
  function show() {
    if (i >= QUIZ_BANK.length) {
      viewer.innerHTML = `<div class="quiz-box"><h2>پایان</h2><p>${score}/${QUIZ_BANK.length}</p>
        <button type="button" id="quizAgain">دوباره</button></div>`;
      $("#quizAgain").onclick = () => { i = 0; score = 0; show(); };
      return;
    }
    const item = QUIZ_BANK[i];
    viewer.innerHTML = `<div class="quiz-box"><div class="q">${escapeHtml(item.q)}</div>
      ${item.opts.map((o, idx) => `<button type="button" class="opt" data-i="${idx}">${escapeHtml(o)}</button>`).join("")}
      <div id="quizExp" class="muted"></div></div>`;
    let locked = false;
    viewer.querySelectorAll(".opt").forEach((btn) => {
      btn.addEventListener("click", () => {
        if (locked) return;
        locked = true;
        const choice = +btn.dataset.i;
        viewer.querySelectorAll(".opt").forEach((b) => {
          if (+b.dataset.i === item.a) b.classList.add("correct");
          if (+b.dataset.i === choice && choice !== item.a) b.classList.add("wrong");
        });
        if (choice === item.a) score++;
        $("#quizExp").textContent = item.exp || "";
        setTimeout(() => { i++; show(); }, 800);
      });
    });
  }
  show();
}

async function renderInfographics() {
  state.view = "info";
  setNav("btnInfo");
  breadcrumb.textContent = "اینفوگرافیک شبکه";
  viewer.innerHTML = `<div class="loading">بارگذاری نمودارها…</div>`;
  try {
    const data = await api("/api/infographics");
    const items = data.items || [];
    viewer.innerHTML = `
      <div class="ws-panel" style="max-width:900px">
        <h2>اینفوگرافیک مسیر پکت و اجزا</h2>
        ${items.map((it) => `<h3 style="margin-top:18px">${escapeHtml(it.title || "")}</h3><div class="infographic">${it.svg || ""}</div>`).join("")}
      </div>`;
  } catch (e) {
    viewer.innerHTML = `<div class="loading">خطا: ${escapeHtml(e.message)}</div>`;
  }
}

chaptersEl.addEventListener("click", async (e) => {
  const chBtn = e.target.closest(".ch-btn");
  const lvBtn = e.target.closest(".lv-btn");
  const lesBtn = e.target.closest(".les-btn");
  if (chBtn) return onChapterClick(chBtn);
  if (lvBtn) return onLevelClick(lvBtn);
  if (lesBtn) return onLessonClick(lesBtn);
});

async function onChapterClick(btn) {
  const id = +btn.dataset.id;
  const nest = document.getElementById(`ch-nest-${id}`);
  const caret = btn.querySelector(".caret");
  if (nest.classList.contains("open")) {
    nest.classList.remove("open"); caret.textContent = "▶"; btn.classList.remove("active"); return;
  }
  btn.classList.add("active"); caret.textContent = "▼"; nest.classList.add("open");
  nest.innerHTML = `<div class="loading">…</div>`;
  breadcrumb.textContent = btn.querySelector(".ch-title").textContent;
  try {
    let levels = state.levelsCache[id];
    if (!levels) {
      levels = asList(await api(`/api/chapters/${id}/levels`), "levels");
      state.levelsCache[id] = levels;
    }
    nest.innerHTML = levels.length
      ? levels.map((lv) => `
      <div class="lv-item">
        <button type="button" class="lv-btn" data-id="${lv.id}">
          <span class="caret">▶</span><span class="ch-title">${escapeHtml(lv.title_fa || "")}</span>
        </button>
        <div class="nested" id="lv-nest-${lv.id}"></div>
      </div>`).join("")
      : `<div class="loading">زیر‌فصلی نیست</div>`;
  } catch (err) {
    nest.innerHTML = `<div class="loading">خطا: ${escapeHtml(err.message)}</div>`;
  }
}

async function onLevelClick(btn) {
  const id = +btn.dataset.id;
  const nest = document.getElementById(`lv-nest-${id}`);
  if (!nest) return;
  const caret = btn.querySelector(".caret");
  if (nest.classList.contains("open")) {
    nest.classList.remove("open"); caret.textContent = "▶"; return;
  }
  caret.textContent = "▼"; nest.classList.add("open");
  nest.innerHTML = `<div class="loading">…</div>`;
  try {
    let lessons = state.lessonsCache[id];
    if (!lessons) {
      lessons = asList(await api(`/api/levels/${id}/lessons`), "lessons");
      state.lessonsCache[id] = lessons;
    }
    nest.innerHTML = lessons.length
      ? lessons.map((les) => `
      <div class="les-item">
        <button type="button" class="les-btn" data-id="${les.id}">
          <span class="dot ${les.has_content ? "ok" : ""}"></span>
          <span class="ch-title">${escapeHtml(les.title_fa || "")}</span>
          <span class="badge">${escapeHtml(les.tags || "")}</span>
        </button>
      </div>`).join("")
      : `<div class="loading">درسی نیست</div>`;
  } catch (err) {
    nest.innerHTML = `<div class="loading">خطا: ${escapeHtml(err.message)}</div>`;
  }
}

async function onLessonClick(btn) {
  const id = +btn.dataset.id;
  viewer.innerHTML = `<div class="loading">…</div>`;
  try {
    const les = await api(`/api/lessons/${id}`);
    breadcrumb.textContent = les.title_fa || "";
    renderLesson(les);
  } catch (err) {
    viewer.innerHTML = `<div class="loading">خطا: ${escapeHtml(err.message)}</div>`;
  }
}

function formatBody(text) {
  if (!text) return "—";
  return escapeHtml(text);
}

function renderLesson(les) {
  const tag = (les.tags || "L0").toLowerCase();
  const tabs = [
    { id: "summary", label: "خلاصه", body: les.summary },
    { id: "content", label: "درس کامل", body: les.full_content },
    { id: "commands", label: "دستورات", body: les.commands },
    { id: "examples", label: "Lab", body: les.examples },
    { id: "notes", label: "RCA", body: les.notes },
  ];
  viewer.innerHTML = `
    <div class="lesson-card">
      <h1>${escapeHtml(les.title_fa || "")}</h1>
      <div class="meta-row">
        <span class="chip ${tag}">${escapeHtml(les.tags || "")}</span>
        <span class="chip">${escapeHtml(les.title_en || "")}</span>
      </div>
      <div class="tabs">
        ${tabs.map((t, i) => `<button type="button" class="tab ${i === 1 ? "active" : ""}" data-i="${i}">${t.label}</button>`).join("")}
      </div>
      <div class="tab-body"><pre class="content-pre">${formatBody(tabs[1].body)}</pre></div>
    </div>`;
  const body = viewer.querySelector(".tab-body");
  viewer.querySelectorAll(".tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      viewer.querySelectorAll(".tab").forEach((x) => x.classList.remove("active"));
      tab.classList.add("active");
      const i = +tab.dataset.i;
      body.innerHTML = `<pre class="content-pre">${formatBody(tabs[i].body)}</pre>`;
    });
  });
}

$("#btnHome").onclick = () => renderHome();
$("#btnTasks").onclick = () => renderTasks();
$("#btnNotes").onclick = () => renderNotes();
$("#btnScenarios").onclick = () => renderScenarios();
$("#btnQuiz").onclick = () => renderQuiz();
$("#btnInfo").onclick = () => renderInfographics();

$("#btnSearch").onclick = async () => {
  const q = $("#q").value.trim();
  if (!q) return;
  breadcrumb.textContent = `جستجو: ${q}`;
  viewer.innerHTML = `<div class="loading">…</div>`;
  try {
    const rows = asList(await api(`/api/search?q=${encodeURIComponent(q)}`), "items");
    viewer.innerHTML = rows.length
      ? `<div class="scenario-list">${rows.map((r) => `
        <div class="scenario-card" data-lid="${r.id}"><h3>${escapeHtml(r.title_fa || "")}</h3></div>`).join("")}</div>`
      : `<div class="ws-panel"><p>نتیجه‌ای نبود</p></div>`;
    viewer.querySelectorAll("[data-lid]").forEach((card) => {
      card.addEventListener("click", async () => {
        const les = await api(`/api/lessons/${card.dataset.lid}`);
        renderLesson(les);
      });
    });
  } catch (e) {
    viewer.innerHTML = `<div class="loading">خطا</div>`;
  }
};

$("#q").addEventListener("keydown", (e) => { if (e.key === "Enter") $("#btnSearch").click(); });

$("#btnReseed").onclick = async () => {
  if (!confirm("بازسازی؟ چند دقیقه طول می‌کشد.")) return;
  try {
    await api("/api/reseed", { method: "POST" });
    state.levelsCache = {}; state.lessonsCache = {};
    await loadStats(); await loadChapters(); alert("انجام شد");
  } catch (e) { alert("خطا: " + e.message); }
};

if (typeof netencSetupLogin === "function") {
  netencSetupLogin(() => {
    loadStats();
    loadChapters();
    renderHome();
  });
} else {
  loadStats();
  loadChapters();
  renderHome();
}
