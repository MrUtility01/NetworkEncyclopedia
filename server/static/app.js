/* Engineer Jokar Web — light UI + tasks + notes + scenarios + quiz */
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

async function api(path, opts) {
  const r = await fetch(path, opts);
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
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
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
  ["btnHome", "btnTasks", "btnNotes", "btnScenarios", "btnQuiz"].forEach((id) => {
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
      <h1>دایرةالمعارف شبکه — Engineer Jokar</h1>
      <p>تم روشن · مطالب آموزشی · کارهای روزانه · نکته‌ها · سناریو و سوالات. از فهرست سمت راست فصل را باز کنید.</p>
      <div class="grid">
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
    });
  });
}

function renderTasks() {
  state.view = "tasks";
  setNav("btnTasks");
  breadcrumb.textContent = "کارهای روزانه";
  const tasks = loadLS(LS_TASKS);
  const today = new Date().toISOString().slice(0, 10);
  viewer.innerHTML = `
    <div class="ws-panel">
      <h2>مدیریت کارهای روزانه</h2>
      <div class="ws-form">
        <input id="taskTitle" placeholder="عنوان کار (مثلاً بکاپ روتر شعبه)" />
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
        saveLS(
          LS_TASKS,
          loadLS(LS_TASKS).filter((x) => x.id !== id)
        );
        paint();
      });
    });
  }
  $("#taskAdd").onclick = () => {
    const title = $("#taskTitle").value.trim();
    if (!title) return;
    const all = loadLS(LS_TASKS);
    all.unshift({
      id: uid(),
      title,
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
        <textarea id="noteBody" placeholder="متن نکته / دستور / هشدار"></textarea>
        <input id="noteTag" placeholder="برچسب (مثلاً MikroTik، BGP)" />
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
        saveLS(
          LS_NOTES,
          loadLS(LS_NOTES).filter((x) => x.id !== id)
        );
        paint();
      });
    });
  }
  $("#noteAdd").onclick = () => {
    const title = $("#noteTitle").value.trim();
    if (!title) return;
    const all = loadLS(LS_NOTES);
    all.unshift({
      id: uid(),
      title,
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
      viewer.innerHTML = `<div class="ws-panel"><p>سناریویی ثبت نشده. پس از seed کامل اینجا ظاهر می‌شود.</p></div>`;
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
          <span class="chip">${escapeHtml(s.difficulty || "")}</span>
        </div>
      </div>`
      )
      .join("")}</div>`;
    viewer.querySelectorAll(".scenario-card").forEach((card) => {
      card.addEventListener("click", async () => {
        viewer.innerHTML = `<div class="loading">بارگذاری…</div>`;
        try {
          const sc = await api(`/api/scenarios/${card.dataset.sid}`);
          breadcrumb.textContent = sc.title_fa || "سناریو";
          viewer.innerHTML = `
            <div class="lesson-card">
              <h1>${escapeHtml(sc.title_fa || "")}</h1>
              <div class="meta-row">
                <span class="chip">${escapeHtml(sc.code || "")}</span>
                <span class="chip">${escapeHtml(sc.level || "")}</span>
                <span class="chip">${escapeHtml(sc.difficulty || "")}</span>
              </div>
              <div class="tabs">
                <button type="button" class="tab active" data-k="business_context">زمینه</button>
                <button type="button" class="tab" data-k="requirements">نیازمندی</button>
                <button type="button" class="tab" data-k="tasks">وظایف</button>
                <button type="button" class="tab" data-k="hints">راهنما</button>
                <button type="button" class="tab" data-k="solution">راه‌حل</button>
                <button type="button" class="tab" data-k="verification">اعتبارسنجی</button>
              </div>
              <div class="tab-body"><pre class="content-pre">${escapeHtml(sc.business_context || "—")}</pre></div>
              <p style="margin-top:12px"><button type="button" class="ghost" id="backSc">بازگشت به لیست</button></p>
            </div>`;
          const body = viewer.querySelector(".tab-body");
          viewer.querySelectorAll(".tab").forEach((tab) => {
            tab.addEventListener("click", () => {
              viewer.querySelectorAll(".tab").forEach((t) => t.classList.remove("active"));
              tab.classList.add("active");
              const k = tab.dataset.k;
              body.innerHTML = `<pre class="content-pre">${escapeHtml(sc[k] || "—")}</pre>`;
            });
          });
          $("#backSc").onclick = () => renderScenarios();
        } catch (e) {
          viewer.innerHTML = `<div class="loading">خطا: ${escapeHtml(e.message)}</div>`;
        }
      });
    });
  } catch (e) {
    viewer.innerHTML = `<div class="loading">خطا: ${escapeHtml(e.message)}</div>`;
  }
}

const QUIZ_BANK = [
  {
    q: "کدام پروتکل برای تفکیک Broadcast Domain در لایه ۲ استفاده می‌شود؟",
    opts: ["VLAN", "OSPF", "FTP", "NTP"],
    a: 0,
    exp: "VLAN دامنه پخش را در سوئیچ جدا می‌کند.",
  },
  {
    q: "در TCP، مرحله برقراری اتصال چه نام دارد؟",
    opts: ["Three-way Handshake", "ARP Request", "DHCP Discover", "ICMP Echo"],
    a: 0,
    exp: "SYN → SYN-ACK → ACK",
  },
  {
    q: "کدام آدرس خصوصی است؟",
    opts: ["8.8.8.8", "192.168.10.5", "1.1.1.1", "9.9.9.9"],
    a: 1,
    exp: "RFC1918: 10/8, 172.16/12, 192.168/16",
  },
  {
    q: "هدف اصلی NAT چیست؟",
    opts: ["رمزنگاری ترافیک", "ترجمه آدرس خصوصی به عمومی", "تعیین مسیر OSPF", "سرویس DNS"],
    a: 1,
    exp: "NAT آدرس‌ها را بین داخل و خارج نگاشت می‌کند.",
  },
  {
    q: "MikroTik از چه رابطی برای CLI استفاده می‌کند؟",
    opts: ["RouterOS CLI / Winbox / API", "فقط GUI ویندوز", "فقط SNMP", "فقط Telnet بدون احراز"],
    a: 0,
    exp: "RouterOS چند روش مدیریت دارد.",
  },
  {
    q: "کدام رکورد DNS برای IPv6 است؟",
    opts: ["A", "AAAA", "MX", "CNAME"],
    a: 1,
    exp: "AAAA برای IPv6",
  },
  {
    q: "در OSPF، DR/BDR در کدام نوع شبکه مهم‌تر است؟",
    opts: ["Point-to-Point", "Broadcast Multi-access", "فقط Loopback", "فقط Static"],
    a: 1,
    exp: "در شبکه‌های Multi-access مثل Ethernet",
  },
  {
    q: "هدف ACL استاندارد معمولاً چیست؟",
    opts: ["فیلتر بر اساس IP مبدأ", "فیلتر لایه ۷", "رمزنگاری", "Load Balancing"],
    a: 0,
    exp: "Standard ACL بر source IP تمرکز دارد.",
  },
];

function renderQuiz() {
  state.view = "quiz";
  setNav("btnQuiz");
  breadcrumb.textContent = "سوالات چندگزینه‌ای";
  let i = 0;
  let score = 0;
  function show() {
    if (i >= QUIZ_BANK.length) {
      viewer.innerHTML = `
        <div class="quiz-box">
          <h2>پایان آزمون</h2>
          <p>امتیاز: <strong>${score}</strong> از ${QUIZ_BANK.length}</p>
          <button type="button" id="quizAgain">شروع دوباره</button>
        </div>`;
      $("#quizAgain").onclick = () => {
        i = 0;
        score = 0;
        show();
      };
      return;
    }
    const item = QUIZ_BANK[i];
    viewer.innerHTML = `
      <div class="quiz-box">
        <div class="muted">سوال ${i + 1} از ${QUIZ_BANK.length}</div>
        <div class="q">${escapeHtml(item.q)}</div>
        ${item.opts
          .map((o, idx) => `<button type="button" class="opt" data-i="${idx}">${escapeHtml(o)}</button>`)
          .join("")}
        <div id="quizExp" class="muted" style="margin-top:10px"></div>
      </div>`;
    let locked = false;
    viewer.querySelectorAll(".opt").forEach((btn) => {
      btn.addEventListener("click", () => {
        if (locked) return;
        locked = true;
        const choice = +btn.dataset.i;
        viewer.querySelectorAll(".opt").forEach((b) => {
          const bi = +b.dataset.i;
          if (bi === item.a) b.classList.add("correct");
          if (bi === choice && choice !== item.a) b.classList.add("wrong");
        });
        if (choice === item.a) score++;
        $("#quizExp").textContent = item.exp || "";
        setTimeout(() => {
          i++;
          show();
        }, 900);
      });
    });
  }
  show();
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
      <div class="lv-item">
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
  setNav("btnHome");
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
    { id: "objectives", label: "اهداف", body: les.learning_objectives },
  ];
  viewer.innerHTML = `
    <div class="lesson-card">
      <h1>${escapeHtml(les.title_fa || "")}</h1>
      <div class="meta-row">
        <span class="chip ${tag}">${escapeHtml(les.tags || "")}</span>
        <span class="chip">${escapeHtml(les.title_en || "")}</span>
      </div>
      <div class="tabs">
        ${tabs.map((t, i) => `<button type="button" class="tab ${i === 0 ? "active" : ""}" data-tab="${t.id}">${t.label}</button>`).join("")}
      </div>
      <div class="tab-body" id="tab-body">${formatBody(tabs[0].body)}</div>
      <p style="margin-top:12px">
        <button type="button" class="ghost" id="saveNoteFromLesson">ذخیره به‌عنوان نکته</button>
      </p>
    </div>`;
  viewer.querySelectorAll(".tab").forEach((tabBtn) => {
    tabBtn.addEventListener("click", () => {
      viewer.querySelectorAll(".tab").forEach((t) => t.classList.remove("active"));
      tabBtn.classList.add("active");
      const t = tabs.find((x) => x.id === tabBtn.dataset.tab);
      $("#tab-body").innerHTML = formatBody(t ? t.body : "");
    });
  });
  const sn = $("#saveNoteFromLesson");
  if (sn) {
    sn.onclick = () => {
      const all = loadLS(LS_NOTES);
      all.unshift({
        id: uid(),
        title: les.title_fa || "درس",
        body: (les.summary || les.full_content || "").slice(0, 2000),
        tag: les.tags || "",
        created: new Date().toLocaleString("fa-IR"),
      });
      saveLS(LS_NOTES, all);
      sn.textContent = "ذخیره شد ✓";
    };
  }
}

function formatBody(body) {
  if (body == null || body === "") return `<p class="muted-p">محتوایی ثبت نشده</p>`;
  return `<pre class="content-pre">${escapeHtml(String(body))}</pre>`;
}

$("#btnHome").onclick = () => renderHome();
$("#btnTasks").onclick = () => renderTasks();
$("#btnNotes").onclick = () => renderNotes();
$("#btnScenarios").onclick = () => renderScenarios();
$("#btnQuiz").onclick = () => renderQuiz();

$("#btnSearch").onclick = async () => {
  const q = $("#q").value.trim();
  if (!q) return;
  breadcrumb.textContent = `جستجو: ${q}`;
  viewer.innerHTML = `<div class="loading">جستجو…</div>`;
  try {
    const rows = asList(await api(`/api/search?q=${encodeURIComponent(q)}`), "items");
    if (!rows.length) {
      viewer.innerHTML = `<div class="ws-panel"><p>نتیجه‌ای نبود</p></div>`;
      return;
    }
    viewer.innerHTML = `<div class="scenario-list">${rows
      .map(
        (r) => `
      <div class="scenario-card" data-lid="${r.id}">
        <h3>${escapeHtml(r.title_fa || "")}</h3>
        <div class="tags">
          <span class="chip">${escapeHtml(r.chapter_title || "")}</span>
          <span class="chip">${escapeHtml(r.level_title || "")}</span>
          <span class="chip">${escapeHtml(r.tags || "")}</span>
        </div>
      </div>`
      )
      .join("")}</div>`;
    viewer.querySelectorAll("[data-lid]").forEach((card) => {
      card.addEventListener("click", async () => {
        const les = await api(`/api/lessons/${card.dataset.lid}`);
        breadcrumb.textContent = les.title_fa || "";
        renderLesson(les);
      });
    });
  } catch (e) {
    viewer.innerHTML = `<div class="loading">خطا: ${escapeHtml(e.message)}</div>`;
  }
};

$("#q").addEventListener("keydown", (e) => {
  if (e.key === "Enter") $("#btnSearch").click();
});

$("#btnReseed").onclick = async () => {
  if (!confirm("بازسازی ساختار دیتابیس؟ ممکن است چند دقیقه طول بکشد.")) return;
  try {
    await api("/api/reseed", {
      method: "POST",
      headers: { Authorization: "Bearer 09136555866", "X-NetEnc-Token": "09136555866" },
    });
    state.levelsCache = {};
    state.lessonsCache = {};
    await loadStats();
    await loadChapters();
    alert("انجام شد");
  } catch (e) {
    alert("خطا: " + e.message);
  }
};

loadStats();
loadChapters();
renderHome();
