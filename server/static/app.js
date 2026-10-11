/* بارگذاری تنبل: فصل‌ها یک‌جا؛ سطح و درس فقط با کلیک */
const $ = (s) => document.querySelector(s);
const chaptersEl = $("#chapters");
const viewer = $("#viewer");
const breadcrumb = $("#breadcrumb");
const statsEl = $("#stats");

const state = {
  chapters: [],
  openCh: null,
  openLv: null,
  levelsCache: {},
  lessonsCache: {},
};

async function api(path, opts) {
  const r = await fetch(path, opts);
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

/** آرایه یا {levels|lessons: []} را یکسان می‌کند */
function asList(data, key) {
  if (Array.isArray(data)) return data;
  if (data && Array.isArray(data[key])) return data[key];
  if (data && Array.isArray(data.items)) return data.items;
  return [];
}

async function loadStats() {
  try {
    const s = await api("/api/stats");
    statsEl.textContent = `${s.chapters} فصل · ${s.levels} زیر‌فصل · ${s.lessons} درس · ${s.scenarios} سناریو · دارای محتوا: ${s.with_content}`;
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
      chaptersEl.innerHTML = `<div class="loading">فصلی نیست — بازسازی ساختار را بزنید</div>`;
      return;
    }
    list.forEach((ch) => {
      const wrap = document.createElement("div");
      wrap.className = "ch-item";
      wrap.dataset.cid = ch.id;
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

function escapeHtml(s) {
  return String(s || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
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
  const isOpen = nest.classList.contains("open");

  if (isOpen) {
    nest.classList.remove("open");
    caret.textContent = "▶";
    btn.classList.remove("active");
    return;
  }

  document.querySelectorAll(".ch-btn.active").forEach((b) => b.classList.remove("active"));
  btn.classList.add("active");
  caret.textContent = "▼";
  nest.classList.add("open");
  nest.innerHTML = `<div class="loading">بارگذاری زیر‌فصل‌ها…</div>`;
  breadcrumb.textContent = btn.querySelector(".ch-title").textContent;

  try {
    let levels = state.levelsCache[id];
    if (!levels) {
      const data = await api(`/api/chapters/${id}/levels`);
      levels = asList(data, "levels");
      state.levelsCache[id] = levels;
    }
    if (!levels.length) {
      nest.innerHTML = `<div class="loading">زیر‌فصلی نیست</div>`;
      return;
    }
    nest.innerHTML = levels
      .map(
        (lv) => `
      <div class="lv-item" data-lid="${lv.id}">
        <button type="button" class="lv-btn" data-id="${lv.id}" data-cid="${id}">
          <span class="caret">▶</span>
          <span class="ch-title">${escapeHtml(lv.title_fa || "")}</span>
        </button>
        <div class="nested" id="lv-nest-${lv.id}"></div>
      </div>`
      )
      .join("");
  } catch (err) {
    nest.innerHTML = `<div class="loading">خطا: ${escapeHtml(err.message)}</div>`;
  }
}

async function onLevelClick(btn) {
  const id = +btn.dataset.id;
  const nest = document.getElementById(`lv-nest-${id}`);
  if (!nest) return;
  const caret = btn.querySelector(".caret");
  const isOpen = nest.classList.contains("open");

  if (isOpen) {
    nest.classList.remove("open");
    caret.textContent = "▶";
    btn.classList.remove("active");
    return;
  }

  document.querySelectorAll(".lv-btn.active").forEach((b) => b.classList.remove("active"));
  btn.classList.add("active");
  caret.textContent = "▼";
  nest.classList.add("open");
  nest.innerHTML = `<div class="loading">بارگذاری درس‌ها…</div>`;

  try {
    let lessons = state.lessonsCache[id];
    if (!lessons) {
      const data = await api(`/api/levels/${id}/lessons`);
      lessons = asList(data, "lessons");
      state.lessonsCache[id] = lessons;
    }
    if (!lessons.length) {
      nest.innerHTML = `<div class="loading">درسی نیست</div>`;
      return;
    }
    nest.innerHTML = lessons
      .map(
        (les) => `
      <div class="les-item">
        <button type="button" class="les-btn" data-id="${les.id}">
          <span class="dot ${les.has_content ? "ok" : ""}"></span>
          <span class="ch-title">${escapeHtml(les.title_fa || "")}</span>
          <span class="badge">${escapeHtml(les.tags || "")}</span>
        </button>
      </div>`
      )
      .join("");
  } catch (err) {
    nest.innerHTML = `<div class="loading">خطا: ${escapeHtml(err.message)}</div>`;
  }
}

async function onLessonClick(btn) {
  const id = +btn.dataset.id;
  document.querySelectorAll(".les-btn.active").forEach((b) => b.classList.remove("active"));
  btn.classList.add("active");
  viewer.innerHTML = `<div class="loading">بارگذاری درس…</div>`;
  try {
    const les = await api(`/api/lessons/${id}`);
    breadcrumb.textContent = les.title_fa || "";
    renderLesson(les);
  } catch (err) {
    viewer.innerHTML = `<div class="loading">خطا: ${escapeHtml(err.message)}</div>`;
  }
}

function renderLesson(les) {
  const tag = (les.tags || "L0").toLowerCase();
  const tabs = [
    { id: "summary", label: "خلاصه", body: les.summary },
    { id: "content", label: "درس کامل", body: les.full_content },
    { id: "commands", label: "دستورات", body: les.commands },
    { id: "examples", label: "مثال‌ها", body: les.examples },
    { id: "notes", label: "عیب‌یابی / نکات", body: les.notes },
    { id: "objectives", label: "اهداف یادگیری", body: les.learning_objectives },
    { id: "meta", label: "Meta / پرامپت", body: formatMeta(les) },
  ];

  viewer.innerHTML = `
    <div class="lesson-card">
      <h1>${escapeHtml(les.title_fa || "")}</h1>
      <div class="meta-row">
        <span class="chip ${tag}">${escapeHtml(les.tags || "")}</span>
        <span class="chip">${escapeHtml(les.title_en || "")}</span>
        <span class="chip">وضعیت منبع: ${escapeHtml(les.source_status || "unverified")}</span>
      </div>
      <div class="tabs">
        ${tabs.map((t, i) => `<button type="button" class="tab ${i === 0 ? "active" : ""}" data-tab="${t.id}">${t.label}</button>`).join("")}
      </div>
      <div class="tab-body" id="tab-body">${formatBody(tabs[0].body)}</div>
    </div>`;

  viewer.querySelectorAll(".tab").forEach((tabBtn) => {
    tabBtn.addEventListener("click", () => {
      viewer.querySelectorAll(".tab").forEach((t) => t.classList.remove("active"));
      tabBtn.classList.add("active");
      const t = tabs.find((x) => x.id === tabBtn.dataset.tab);
      $("#tab-body").innerHTML = formatBody(t ? t.body : "");
    });
  });
}

function formatBody(body) {
  if (body == null || body === "") return "<p class=\"muted\">محتوایی ثبت نشده</p>";
  const s = String(body);
  if (s.includes("\n") || s.length > 80) {
    return `<pre class="content-pre">${escapeHtml(s)}</pre>`;
  }
  return `<p>${escapeHtml(s)}</p>`;
}

function formatMeta(les) {
  try {
    const m = typeof les.meta === "object" && les.meta ? les.meta : JSON.parse(les.meta_json || "{}");
    return JSON.stringify(m, null, 2);
  } catch (e) {
    return les.meta_json || "";
  }
}

// init
loadStats();
loadChapters();
