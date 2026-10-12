/* Engineer Jokar Web - login-gated UI */
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
    statsEl.textContent = s.chapters + " فصل · " + s.levels + " زیر‌فصل · " + s.lessons + " درس · " + s.scenarios + " سناریو · محتوا: " + s.with_content;
  } catch (e) {
    statsEl.textContent = "خطا در آمار";
  }
}

async function loadChapters() {
  chaptersEl.innerHTML = '<div class="loading">بارگذاری فهرست فصل‌ها…</div>';
  try {
    const list = asList(await api("/api/chapters"), "chapters");
    state.chapters = list;
    chaptersEl.innerHTML = "";
    if (!list.length) {
      chaptersEl.innerHTML = '<div class="loading">فصلی نیست — بازسازی را بزنید</div>';
      return;
    }
    list.forEach((ch) => {
      const wrap = document.createElement("div");
      wrap.className = "ch-item";
      wrap.innerHTML =
        '<button type="button" class="ch-btn" data-id="' +
        ch.id +
        '">' +
        '<span class="caret">▶</span>' +
        '<span class="ch-title">' +
        escapeHtml(ch.title_fa) +
        "</span>" +
        '<span class="badge">' +
        ch.order_index +
        "</span></button>" +
        '<div class="nested" id="ch-nest-' +
        ch.id +
        '"></div>';
      chaptersEl.appendChild(wrap);
    });
  } catch (err) {
    chaptersEl.innerHTML = '<div class="loading">خطا: ' + escapeHtml(err.message) + "</div>";
  }
}

function renderHome() {
  state.view = "home";
  setNav("btnHome");
  breadcrumb.textContent = "خانه";
  viewer.innerHTML =
    '<div class="welcome"><h1>دایرةالمعارف شبکه — Network Engineer</h1>' +
    "<p>مطالب دسته‌محور · اینفوگرافیک · کارها و نکته‌ها · سناریو و سوالات.</p>" +
    '<div class="grid">' +
    '<div class="card-link" data-go="info"><strong>اینفوگرافیک</strong><span class="muted">مسیر پکت</span></div>' +
    '<div class="card-link" data-go="tasks"><strong>کارهای روزانه</strong><span class="muted">لیست کار</span></div>' +
    '<div class="card-link" data-go="notes"><strong>نکته‌ها</strong><span class="muted">یادداشت</span></div>' +
    '<div class="card-link" data-go="scenarios"><strong>سناریوها</strong><span class="muted">Capstone</span></div>' +
    '<div class="card-link" data-go="quiz"><strong>سوالات</strong><span class="muted">مرور</span></div>' +
    "</div></div>";
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
  viewer.innerHTML =
    '<div class="ws-panel"><h2>مدیریت کارهای روزانه</h2><div class="ws-form">' +
    '<input id="taskTitle" placeholder="عنوان کار" />' +
    '<textarea id="taskBody" placeholder="توضیح"></textarea>' +
    '<input id="taskDue" type="date" value="' +
    today +
    '" />' +
    '<button type="button" id="taskAdd">افزودن کار</button></div><div class="ws-list" id="taskList"></div></div>';
  const listEl = $("#taskList");
  function paint() {
    const arr = loadLS(LS_TASKS);
    if (!arr.length) {
      listEl.innerHTML = '<div class="loading">هنوز کاری ثبت نشده</div>';
      return;
    }
    arr.sort((a, b) => (a.done === b.done ? 0 : a.done ? 1 : -1));
    listEl.innerHTML = arr
      .map(function (t) {
        return (
          '<div class="ws-item ' +
          (t.done ? "done" : "") +
          '" data-id="' +
          t.id +
          '"><div class="row"><div><h3>' +
          (t.done ? "✓ " : "○ ") +
          escapeHtml(t.title) +
          "</h3><p>" +
          escapeHtml(t.body || "") +
          '</p><div class="meta">موعد: ' +
          escapeHtml(t.due || "—") +
          "</div></div><div class="actions">" +
          '<button type="button" class="ghost t-toggle">' +
          (t.done ? "بازگشت" : "انجام شد") +
          '</button><button type="button" class="ghost danger t-del">حذف</button></div></div></div>'
        );
      })
      .join("");
    listEl.querySelectorAll(".t-toggle").forEach(function (btn) {
      btn.addEventListener("click", function () {
        const id = btn.closest(".ws-item").dataset.id;
        const all = loadLS(LS_TASKS);
        const t = all.find(function (x) {
          return x.id === id;
        });
        if (t) t.done = !t.done;
        saveLS(LS_TASKS, all);
        paint();
      });
    });
    listEl.querySelectorAll(".t-del").forEach(function (btn) {
      btn.addEventListener("click", function () {
        const id = btn.closest(".ws-item").dataset.id;
        saveLS(
          LS_TASKS,
          loadLS(LS_TASKS).filter(function (x) {
            return x.id !== id;
          })
        );
        paint();
      });
    });
  }
  $("#taskAdd").onclick = function () {
    const title = $("#taskTitle").value.trim();
    if (!title) return;
    const all = loadLS(LS_TASKS);
    all.unshift({
      id: uid(),
      title: title,
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
  breadcrumb.textContent = "نکته‌ها";
  viewer.innerHTML =
    '<div class="ws-panel"><h2>نکته‌ها</h2><div class="ws-form">' +
    '<input id="noteTitle" placeholder="عنوان" />' +
    '<textarea id="noteBody" placeholder="متن"></textarea>' +
    '<input id="noteTag" placeholder="برچسب" />' +
    '<button type="button" id="noteAdd">ذخیره</button></div><div class="ws-list" id="noteList"></div></div>';
  const listEl = $("#noteList");
  function paint() {
    const arr = loadLS(LS_NOTES);
    if (!arr.length) {
      listEl.innerHTML = '<div class="loading">نکته‌ای نیست</div>';
      return;
    }
    listEl.innerHTML = arr
      .map(function (n) {
        return (
          '<div class="ws-item" data-id="' +
          n.id +
          '"><div class="row"><div><h3>' +
          escapeHtml(n.title) +
          "</h3><p>" +
          escapeHtml(n.body || "") +
          '</p></div><div class="actions">' +
          '<button type="button" class="ghost danger n-del">حذف</button></div></div></div>'
        );
      })
      .join("");
    listEl.querySelectorAll(".n-del").forEach(function (btn) {
      btn.addEventListener("click", function () {
        const id = btn.closest(".ws-item").dataset.id;
        saveLS(
          LS_NOTES,
          loadLS(LS_NOTES).filter(function (x) {
            return x.id !== id;
          })
        );
        paint();
      });
    });
  }
  $("#noteAdd").onclick = function () {
    const title = $("#noteTitle").value.trim();
    if (!title) return;
    const all = loadLS(LS_NOTES);
    all.unshift({
      id: uid(),
      title: title,
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
  breadcrumb.textContent = "سناریوها";
  viewer.innerHTML = '<div class="loading">…</div>';
  try {
    const list = asList(await api("/api/scenarios"), "scenarios");
    if (!list.length) {
      viewer.innerHTML = '<div class="ws-panel"><p>سناریویی نیست</p></div>';
      return;
    }
    viewer.innerHTML =
      '<div class="scenario-list">' +
      list
        .map(function (s) {
          return (
            '<div class="scenario-card" data-sid="' +
            s.id +
            '"><h3>' +
            escapeHtml(s.title_fa || s.code || "") +
            "</h3></div>"
          );
        })
        .join("") +
      "</div>";
    viewer.querySelectorAll(".scenario-card").forEach(function (card) {
      card.addEventListener("click", async function () {
        const sc = await api("/api/scenarios/" + card.dataset.sid);
        breadcrumb.textContent = sc.title_fa || "سناریو";
        viewer.innerHTML =
          '<div class="lesson-card"><h1>' +
          escapeHtml(sc.title_fa || "") +
          "</h1><pre class="content-pre">" +
          escapeHtml(sc.business_context || sc.tasks || "—") +
          '</pre><button type="button" class="ghost" id="backSc">بازگشت</button></div>';
        $("#backSc").onclick = function () {
          renderScenarios();
        };
      });
    });
  } catch (e) {
    viewer.innerHTML = '<div class="loading">خطا</div>';
  }
}

const QUIZ_BANK = [
  { q: "جداسازی Broadcast Domain؟", opts: ["VLAN", "OSPF", "FTP", "NTP"], a: 0 },
  { q: "برقراری TCP؟", opts: ["Three-way Handshake", "ARP", "DHCP", "ICMP"], a: 0 },
  { q: "آدرس خصوصی؟", opts: ["8.8.8.8", "192.168.10.5", "1.1.1.1", "9.9.9.9"], a: 1 },
  { q: "هدف NAT؟", opts: ["رمزنگاری", "ترجمه آدرس", "OSPF", "DNS"], a: 1 },
  { q: "رکورد IPv6؟", opts: ["A", "AAAA", "MX", "CNAME"], a: 1 },
];

function renderQuiz() {
  state.view = "quiz";
  setNav("btnQuiz");
  breadcrumb.textContent = "سوالات";
  var i = 0,
    score = 0;
  function show() {
    if (i >= QUIZ_BANK.length) {
      viewer.innerHTML =
        '<div class="quiz-box"><h2>پایان</h2><p>' +
        score +
        "/" +
        QUIZ_BANK.length +
        '</p><button type="button" id="quizAgain">دوباره</button></div>';
      $("#quizAgain").onclick = function () {
        i = 0;
        score = 0;
        show();
      };
      return;
    }
    var item = QUIZ_BANK[i];
    viewer.innerHTML =
      '<div class="quiz-box"><div class="q">' +
      escapeHtml(item.q) +
      "</div>" +
      item.opts
        .map(function (o, idx) {
          return '<button type="button" class="opt" data-i="' + idx + '">' + escapeHtml(o) + "</button>";
        })
        .join("") +
      "</div>";
    var locked = false;
    viewer.querySelectorAll(".opt").forEach(function (btn) {
      btn.addEventListener("click", function () {
        if (locked) return;
        locked = true;
        var choice = +btn.dataset.i;
        if (choice === item.a) score++;
        setTimeout(function () {
          i++;
          show();
        }, 500);
      });
    });
  }
  show();
}

async function renderInfographics() {
  state.view = "info";
  setNav("btnInfo");
  breadcrumb.textContent = "اینفوگرافیک";
  viewer.innerHTML = '<div class="loading">…</div>';
  try {
    var data = await api("/api/infographics");
    var items = data.items || [];
    viewer.innerHTML =
      '<div class="ws-panel"><h2>اینفوگرافیک</h2>' +
      items
        .map(function (it) {
          return "<h3>" + escapeHtml(it.title || "") + "</h3><div>" + (it.svg || "") + "</div>";
        })
        .join("") +
      "</div>";
  } catch (e) {
    viewer.innerHTML = '<div class="loading">خطا</div>';
  }
}

chaptersEl.addEventListener("click", async function (e) {
  var chBtn = e.target.closest(".ch-btn");
  var lvBtn = e.target.closest(".lv-btn");
  var lesBtn = e.target.closest(".les-btn");
  if (chBtn) return onChapterClick(chBtn);
  if (lvBtn) return onLevelClick(lvBtn);
  if (lesBtn) return onLessonClick(lesBtn);
});

async function onChapterClick(btn) {
  var id = +btn.dataset.id;
  var nest = document.getElementById("ch-nest-" + id);
  var caret = btn.querySelector(".caret");
  if (nest.classList.contains("open")) {
    nest.classList.remove("open");
    caret.textContent = "▶";
    btn.classList.remove("active");
    return;
  }
  btn.classList.add("active");
  caret.textContent = "▼";
  nest.classList.add("open");
  nest.innerHTML = '<div class="loading">…</div>';
  breadcrumb.textContent = btn.querySelector(".ch-title").textContent;
  try {
    var levels = state.levelsCache[id];
    if (!levels) {
      levels = asList(await api("/api/chapters/" + id + "/levels"), "levels");
      state.levelsCache[id] = levels;
    }
    nest.innerHTML = levels.length
      ? levels
          .map(function (lv) {
            return (
              '<div class="lv-item"><button type="button" class="lv-btn" data-id="' +
              lv.id +
              '"><span class="caret">▶</span><span class="ch-title">' +
              escapeHtml(lv.title_fa || "") +
              '</span></button><div class="nested" id="lv-nest-' +
              lv.id +
              '"></div></div>'
            );
          })
          .join("")
      : '<div class="loading">زیر‌فصلی نیست</div>';
  } catch (err) {
    nest.innerHTML = '<div class="loading">خطا</div>';
  }
}

async function onLevelClick(btn) {
  var id = +btn.dataset.id;
  var nest = document.getElementById("lv-nest-" + id);
  if (!nest) return;
  var caret = btn.querySelector(".caret");
  if (nest.classList.contains("open")) {
    nest.classList.remove("open");
    caret.textContent = "▶";
    return;
  }
  caret.textContent = "▼";
  nest.classList.add("open");
  nest.innerHTML = '<div class="loading">…</div>';
  try {
    var lessons = state.lessonsCache[id];
    if (!lessons) {
      lessons = asList(await api("/api/levels/" + id + "/lessons"), "lessons");
      state.lessonsCache[id] = lessons;
    }
    nest.innerHTML = lessons.length
      ? lessons
          .map(function (les) {
            return (
              '<div class="les-item"><button type="button" class="les-btn" data-id="' +
              les.id +
              '"><span class="dot ' +
              (les.has_content ? "ok" : "") +
              '"></span><span class="ch-title">' +
              escapeHtml(les.title_fa || "") +
              "</span></button></div>"
            );
          })
          .join("")
      : '<div class="loading">درسی نیست</div>';
  } catch (err) {
    nest.innerHTML = '<div class="loading">خطا</div>';
  }
}

async function onLessonClick(btn) {
  var id = +btn.dataset.id;
  viewer.innerHTML = '<div class="loading">…</div>';
  try {
    var les = await api("/api/lessons/" + id);
    breadcrumb.textContent = les.title_fa || "";
    renderLesson(les);
  } catch (err) {
    viewer.innerHTML = '<div class="loading">خطا</div>';
  }
}

function renderLesson(les) {
  var tag = (les.tags || "L0").toLowerCase();
  var tabs = [
    { id: "summary", label: "خلاصه", body: les.summary },
    { id: "content", label: "درس کامل", body: les.full_content },
    { id: "commands", label: "دستورات", body: les.commands },
    { id: "examples", label: "Lab", body: les.examples },
    { id: "notes", label: "RCA", body: les.notes },
  ];
  viewer.innerHTML =
    '<div class="lesson-card"><h1>' +
    escapeHtml(les.title_fa || "") +
    '</h1><div class="meta-row"><span class="chip ' +
    tag +
    '">' +
    escapeHtml(les.tags || "") +
    '</span></div><div class="tabs">' +
    tabs
      .map(function (t, idx) {
        return (
          '<button type="button" class="tab' +
          (idx === 1 ? " active" : "") +
          '" data-k="' +
          t.id +
          '">' +
          t.label +
          "</button>"
        );
      })
      .join("") +
    '</div><div class="tab-body"><pre class="content-pre">' +
    escapeHtml(les.full_content || les.summary || "—") +
    "</pre></div></div>";
  var body = viewer.querySelector(".tab-body");
  viewer.querySelectorAll(".tab").forEach(function (tab) {
    tab.addEventListener("click", function () {
      viewer.querySelectorAll(".tab").forEach(function (t) {
        t.classList.remove("active");
      });
      tab.classList.add("active");
      var key = tab.dataset.k;
      var found = tabs.find(function (t) {
        return t.id === key;
      });
      body.innerHTML = '<pre class="content-pre">' + escapeHtml((found && found.body) || "—") + "</pre>";
    });
  });
}

document.getElementById("btnHome").onclick = function () {
  renderHome();
};
document.getElementById("btnTasks").onclick = function () {
  renderTasks();
};
document.getElementById("btnNotes").onclick = function () {
  renderNotes();
};
document.getElementById("btnScenarios").onclick = function () {
  renderScenarios();
};
document.getElementById("btnQuiz").onclick = function () {
  renderQuiz();
};
document.getElementById("btnInfo").onclick = function () {
  renderInfographics();
};

var btnSearch = document.getElementById("btnSearch");
if (btnSearch) {
  btnSearch.onclick = async function () {
    var q = ($("#q") && $("#q").value.trim()) || "";
    if (!q) return;
    breadcrumb.textContent = "جستجو: " + q;
    viewer.innerHTML = '<div class="loading">…</div>';
    try {
      var rows = asList(await api("/api/search?q=" + encodeURIComponent(q)), "items");
      viewer.innerHTML = rows.length
        ? '<div class="scenario-list">' +
          rows
            .map(function (r) {
              return (
                '<div class="scenario-card" data-lid="' +
                r.id +
                '"><h3>' +
                escapeHtml(r.title_fa || "") +
                "</h3></div>"
              );
            })
            .join("") +
          "</div>"
        : '<div class="ws-panel"><p>نتیجه‌ای نبود</p></div>';
      viewer.querySelectorAll("[data-lid]").forEach(function (card) {
        card.addEventListener("click", async function () {
          var les = await api("/api/lessons/" + card.dataset.lid);
          renderLesson(les);
        });
      });
    } catch (e) {
      viewer.innerHTML = '<div class="loading">خطا</div>';
    }
  };
}

var qEl = document.getElementById("q");
if (qEl) {
  qEl.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && btnSearch) btnSearch.click();
  });
}

var btnReseed = document.getElementById("btnReseed");
if (btnReseed) {
  btnReseed.onclick = async function () {
    if (!confirm("بازسازی؟ چند دقیقه طول می‌کشد.")) return;
    try {
      await api("/api/reseed", { method: "POST" });
      state.levelsCache = {};
      state.lessonsCache = {};
      await loadStats();
      await loadChapters();
      alert("انجام شد");
    } catch (e) {
      alert("خطا: " + e.message);
    }
  };
}

if (typeof netencSetupLogin === "function") {
  netencSetupLogin(function () {
    loadStats();
    loadChapters();
    renderHome();
  });
} else {
  loadStats();
  loadChapters();
  renderHome();
}
