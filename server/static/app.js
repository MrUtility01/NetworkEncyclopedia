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
  levelsCache: {}, // chapterId -> levels[]
  lessonsCache: {}, // levelId -> lessons[]
};

async function api(path, opts) {
  const r = await fetch(path, opts);
  if (!r.ok) throw new Error(await r.text());
  return r.json();
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
  const list = await api("/api/chapters");
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

  // بستن بقیه اختیاری — فقط همین را toggle
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
      levels = data.levels;
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
          <span class="ch-title">${escapeHtml(lv.title_fa)}</span>
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
  const caret = btn.querySelector(".caret");
  if (nest.classList.contains("open")) {
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
      lessons = data.lessons;
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
          <span class="ch-title">${escapeHtml(les.title_fa)}</span>
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
    breadcrumb.textContent = les.title_fa;
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
      <h1>${escapeHtml(les.title_fa)}</h1>
      <div class="meta-row">
        <span class="chip ${tag}">${escapeHtml(les.tags || "")}</span>
        <span class="chip">${escapeHtml(les.title_en || "")}</span>
        <span class="chip">وضعیت منبع: ${escapeHtml(les.source_status || "unverified")}</span>
      </div>
      <div class="tabs">
        ${tabs.map((t, i) => `<button type="button" class="tab ${i === 0 ? "active" : ""}" data-tab="${t.id}">${t.label}</button>`).join("")}
      </div>
      ${tabs
        .map(
          (t, i) =>
            `<div class="panel ${i === 0 ? "active" : ""}" id="panel-${t.id}">${
              t.body && String(t.body).trim()
                ? escapeHtml(t.body)
                : `<span class="empty-hint">محتوا هنوز پر نشده — از AI یا ویرایش بعدی پر می‌شود. عنوان و Meta آماده است.</span>`
            }</div>`
        )
        .join("")}
    </div>`;

  viewer.querySelectorAll(".tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      viewer.querySelectorAll(".tab").forEach((x) => x.classList.remove("active"));
      viewer.querySelectorAll(".panel").forEach((x) => x.classList.remove("active"));
      tab.classList.add("active");
      const p = document.getElementById(`panel-${tab.dataset.tab}`);
      if (p) p.classList.add("active");
    });
  });
}

function formatMeta(les) {
  const m = les.meta || {};
  const lines = [
    "=== پرامپت تدریس ===",
    m.ai_teach_prompt || "",
    "",
    "=== پرامپت جستجو ===",
    m.ai_search_prompt || les.search_query || "",
    "",
    "=== پرامپت عیب‌یابی ===",
    m.ai_troubleshoot_prompt || "",
    "",
    "=== حلقه مهندسی ===",
    (m.engineering_loop || []).join(" → "),
  ];
  return lines.join("\n");
}

async function showScenarios() {
  viewer.innerHTML = `<div class="loading">بارگذاری سناریوها…</div>`;
  breadcrumb.textContent = "سناریوهای Capstone";
  const list = await api("/api/scenarios");
  viewer.innerHTML = `
    <h1 style="margin-top:0">۱۰ سناریوی سازمانی</h1>
    <div class="scenario-list">
      ${list
        .map(
          (s) => `
        <div class="scenario-card" data-sid="${s.id}">
          <h3>${escapeHtml(s.code)} — ${escapeHtml(s.title_fa)}</h3>
          <div class="meta-row">
            <span class="chip">${escapeHtml(s.level)}</span>
            <span class="chip">${escapeHtml(s.difficulty)}</span>
            <span class="chip">${s.users || 0} کاربر</span>
            <span class="chip">${s.sites || 0} سایت</span>
            <span class="chip">${s.estimated_hours || 0} ساعت</span>
          </div>
        </div>`
        )
        .join("")}
    </div>`;
  viewer.querySelectorAll(".scenario-card").forEach((card) => {
    card.addEventListener("click", async () => {
      const sc = await api(`/api/scenarios/${card.dataset.sid}`);
      breadcrumb.textContent = sc.title_fa;
      viewer.innerHTML = `
        <div class="scenario-detail">
          <h1>${escapeHtml(sc.code)} — ${escapeHtml(sc.title_fa)}</h1>
          <div class="meta-row">
            <span class="chip">${escapeHtml(sc.vendors || "")}</span>
            <span class="chip">${escapeHtml(sc.category || "")}</span>
          </div>
          ${section("بافت کسب‌وکار", sc.business_context)}
          ${section("نیازمندی‌ها", sc.requirements)}
          ${section("محدودیت‌ها", sc.constraints_text)}
          ${section("وضعیت اولیه", sc.initial_state)}
          ${section("حادثه / علائم", [sc.incident, sc.symptoms].filter(Boolean).join("\n"))}
          ${section("اهداف", sc.objectives)}
          ${section("وظایف", sc.tasks)}
          ${section("راهنمایی", sc.hints)}
          ${section("نتیجه مورد انتظار", sc.expected_result)}
          ${section("راستی‌آزمایی", sc.verification)}
          ${section("مهارت‌های لازم", sc.skills_required)}
        </div>`;
    });
  });
}

function section(title, body) {
  if (!body || !String(body).trim()) return "";
  return `<h2>${escapeHtml(title)}</h2><pre>${escapeHtml(body)}</pre>`;
}

async function doSearch() {
  const q = $("#q").value.trim();
  if (!q) return;
  viewer.innerHTML = `<div class="loading">جستجو…</div>`;
  breadcrumb.textContent = `نتایج: ${q}`;
  const rows = await api(`/api/search?q=${encodeURIComponent(q)}`);
  if (!rows.length) {
    viewer.innerHTML = `<p class="empty-hint">موردی پیدا نشد.</p>`;
    return;
  }
  viewer.innerHTML = `<ul class="search-results">${rows
    .map(
      (r) => `<li data-id="${r.id}">
      <div>${escapeHtml(r.title_fa)}</div>
      <div class="path">${escapeHtml(r.chapter_title)} / ${escapeHtml(r.level_title)} · ${escapeHtml(r.tags || "")}</div>
    </li>`
    )
    .join("")}</ul>`;
  viewer.querySelectorAll("li").forEach((li) => {
    li.addEventListener("click", async () => {
      const les = await api(`/api/lessons/${li.dataset.id}`);
      breadcrumb.textContent = les.title_fa;
      renderLesson(les);
    });
  });
}

$("#btnSearch").addEventListener("click", doSearch);
$("#q").addEventListener("keydown", (e) => {
  if (e.key === "Enter") doSearch();
});
$("#btnScenarios").addEventListener("click", showScenarios);
$("#btnReseed").addEventListener("click", async () => {
  if (!confirm("ساختار از نو ساخته می‌شود (عناوین). ادامه؟")) return;
  viewer.innerHTML = `<div class="loading">بازسازی… ممکن است یک دقیقه طول بکشد</div>`;
  try {
    const info = await api("/api/reseed", { method: "POST" });
    state.levelsCache = {};
    state.lessonsCache = {};
    await loadChapters();
    await loadStats();
    viewer.innerHTML = `<pre>${escapeHtml(JSON.stringify(info, null, 2))}</pre>`;
  } catch (e) {
    viewer.innerHTML = `<div class="loading">خطا: ${escapeHtml(e.message)}</div>`;
  }
});

(async function init() {
  await loadChapters();
  await loadStats();
})();
