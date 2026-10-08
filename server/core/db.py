# -*- coding: utf-8 -*-
"""SQLite سبک برای نسخه وب — فقط ساختار ۶۳ فصلی کامل."""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parent.parent
DB_PATH = BASE / "data" / "encyclopedia.db"


class WebDB:
    def __init__(self, path=None):
        self.path = Path(path) if path else DB_PATH
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.execute("PRAGMA journal_mode = WAL")
        self._create()

    def _create(self):
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS chapters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_index INTEGER NOT NULL,
                title_fa TEXT NOT NULL,
                title_en TEXT DEFAULT '',
                description TEXT DEFAULT ''
            );
            CREATE TABLE IF NOT EXISTS levels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chapter_id INTEGER NOT NULL,
                order_index INTEGER NOT NULL,
                title_fa TEXT NOT NULL,
                title_en TEXT DEFAULT '',
                FOREIGN KEY (chapter_id) REFERENCES chapters(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS lessons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                level_id INTEGER NOT NULL,
                order_index INTEGER NOT NULL,
                title_fa TEXT NOT NULL,
                title_en TEXT DEFAULT '',
                tags TEXT DEFAULT '',
                summary TEXT DEFAULT '',
                full_content TEXT DEFAULT '',
                commands TEXT DEFAULT '',
                examples TEXT DEFAULT '',
                notes TEXT DEFAULT '',
                meta_json TEXT DEFAULT '{}',
                search_query TEXT DEFAULT '',
                learning_objectives TEXT DEFAULT '',
                source_status TEXT DEFAULT 'unverified',
                last_updated TEXT,
                FOREIGN KEY (level_id) REFERENCES levels(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS scenarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE,
                title_fa TEXT NOT NULL,
                title_en TEXT,
                category TEXT DEFAULT 'Capstone',
                level TEXT DEFAULT 'L4',
                difficulty TEXT DEFAULT 'خبره',
                users INTEGER DEFAULT 0,
                sites INTEGER DEFAULT 1,
                vendors TEXT DEFAULT '',
                business_context TEXT DEFAULT '',
                requirements TEXT DEFAULT '',
                constraints_text TEXT DEFAULT '',
                initial_state TEXT DEFAULT '',
                incident TEXT DEFAULT '',
                symptoms TEXT DEFAULT '',
                objectives TEXT DEFAULT '',
                tasks TEXT DEFAULT '',
                hints TEXT DEFAULT '',
                expected_result TEXT DEFAULT '',
                solution TEXT DEFAULT '',
                verification TEXT DEFAULT '',
                skills_required TEXT DEFAULT '',
                estimated_hours INTEGER DEFAULT 8,
                last_updated TEXT
            );
            CREATE TABLE IF NOT EXISTS meta (
                key TEXT PRIMARY KEY,
                value TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_levels_ch ON levels(chapter_id);
            CREATE INDEX IF NOT EXISTS idx_lessons_lv ON lessons(level_id);
            """
        )
        self.conn.commit()

    def get_meta(self, key, default=None):
        r = self.conn.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
        return r["value"] if r else default

    def set_meta(self, key, value):
        self.conn.execute(
            "INSERT INTO meta(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, value),
        )
        self.conn.commit()

    def chapter_count(self):
        return self.conn.execute("SELECT COUNT(*) c FROM chapters").fetchone()["c"]

    def is_seeded(self):
        return self.chapter_count() >= 60

    def seed_full(self, force=False):
        """ساخت کامل ۶۳ فصل از Blueprint — فقط عنوان‌ها (محتوا تنبل)."""
        if self.is_seeded() and not force:
            return {"ok": True, "skipped": True, "chapters": self.chapter_count()}

        from core.full_curriculum import get_full_curriculum
        from core.phase_a import CAPSTONE_SCENARIOS, default_meta

        cur = self.conn.cursor()
        if force:
            cur.executescript(
                "DELETE FROM lessons; DELETE FROM levels; DELETE FROM chapters; DELETE FROM scenarios;"
            )

        curriculum = get_full_curriculum()
        n_ch = n_lv = n_les = 0
        now = datetime.now().isoformat()

        for order, title_fa, title_en, levels in curriculum:
            cur.execute(
                "INSERT INTO chapters(order_index, title_fa, title_en) VALUES (?,?,?)",
                (order, title_fa, title_en),
            )
            ch_id = cur.lastrowid
            n_ch += 1
            for li, (lv_title, lessons) in enumerate(levels, 1):
                cur.execute(
                    "INSERT INTO levels(chapter_id, order_index, title_fa) VALUES (?,?,?)",
                    (ch_id, li, lv_title),
                )
                lv_id = cur.lastrowid
                n_lv += 1
                for oi, (lfa, len_) in enumerate(lessons, 1):
                    tag = lfa[1:3] if lfa.startswith("[L") else "L0"
                    meta = default_meta(lfa, level=tag)
                    cur.execute(
                        """INSERT INTO lessons(
                            level_id, order_index, title_fa, title_en, tags,
                            summary, search_query, learning_objectives, meta_json, last_updated
                        ) VALUES (?,?,?,?,?,?,?,?,?,?)""",
                        (
                            lv_id,
                            oi,
                            lfa,
                            len_,
                            tag,
                            meta.get("description", ""),
                            meta.get("ai_search_prompt", ""),
                            "\n".join(meta.get("learning_objectives") or []),
                            json.dumps(meta, ensure_ascii=False),
                            now,
                        ),
                    )
                    n_les += 1

        for sc in CAPSTONE_SCENARIOS:
            cur.execute(
                """INSERT OR REPLACE INTO scenarios(
                    code, title_fa, title_en, category, level, difficulty,
                    users, sites, vendors, business_context, requirements,
                    constraints_text, initial_state, incident, symptoms,
                    objectives, tasks, hints, expected_result, solution,
                    verification, skills_required, estimated_hours, last_updated
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    sc["code"],
                    sc["title_fa"],
                    sc["title_en"],
                    sc["category"],
                    sc["level"],
                    sc["difficulty"],
                    sc["users"],
                    sc["sites"],
                    sc["vendors"],
                    sc["business_context"],
                    sc["requirements"],
                    sc["constraints"],
                    sc["initial_state"],
                    sc["incident"],
                    sc["symptoms"],
                    sc["objectives"],
                    sc["tasks"],
                    sc["hints"],
                    sc["expected_result"],
                    sc["solution"],
                    sc["verification"],
                    sc["skills_required"],
                    sc["estimated_hours"],
                    now,
                ),
            )

        self.conn.commit()
        self.set_meta("seeded_version", "web-v1-63ch")
        self.set_meta("seeded_at", now)
        return {"ok": True, "chapters": n_ch, "levels": n_lv, "lessons": n_les, "scenarios": len(CAPSTONE_SCENARIOS)}

    def list_chapters(self):
        rows = self.conn.execute(
            "SELECT id, order_index, title_fa, title_en FROM chapters ORDER BY order_index, id"
        ).fetchall()
        return [dict(r) for r in rows]

    def get_chapter(self, chapter_id: int):
        r = self.conn.execute("SELECT * FROM chapters WHERE id=?", (chapter_id,)).fetchone()
        return dict(r) if r else None

    def list_levels(self, chapter_id: int):
        rows = self.conn.execute(
            "SELECT id, order_index, title_fa, title_en FROM levels WHERE chapter_id=? ORDER BY order_index, id",
            (chapter_id,),
        ).fetchall()
        return [dict(r) for r in rows]

    def list_lessons(self, level_id: int):
        rows = self.conn.execute(
            """SELECT id, order_index, title_fa, title_en, tags,
                      CASE WHEN length(COALESCE(full_content,''))>50 THEN 1 ELSE 0 END AS has_content
               FROM lessons WHERE level_id=? ORDER BY order_index, id""",
            (level_id,),
        ).fetchall()
        return [dict(r) for r in rows]

    def get_lesson(self, lesson_id: int):
        r = self.conn.execute("SELECT * FROM lessons WHERE id=?", (lesson_id,)).fetchone()
        if not r:
            return None
        d = dict(r)
        try:
            d["meta"] = json.loads(d.get("meta_json") or "{}")
        except Exception:
            d["meta"] = {}
        return d

    def save_lesson_content(self, lesson_id: int, **fields):
        allowed = {
            "summary",
            "full_content",
            "commands",
            "examples",
            "notes",
            "search_query",
            "learning_objectives",
            "source_status",
        }
        parts = []
        vals = []
        for k, v in fields.items():
            if k in allowed:
                parts.append(f"{k}=?")
                vals.append(v)
        if not parts:
            return False
        parts.append("last_updated=?")
        vals.append(datetime.now().isoformat())
        vals.append(lesson_id)
        self.conn.execute(f"UPDATE lessons SET {', '.join(parts)} WHERE id=?", vals)
        self.conn.commit()
        return True

    def list_scenarios(self):
        rows = self.conn.execute(
            "SELECT id, code, title_fa, category, level, difficulty, users, sites, estimated_hours FROM scenarios ORDER BY code"
        ).fetchall()
        return [dict(r) for r in rows]

    def get_scenario(self, scenario_id: int):
        r = self.conn.execute("SELECT * FROM scenarios WHERE id=?", (scenario_id,)).fetchone()
        return dict(r) if r else None

    def search(self, q: str, limit=50):
        q = (q or "").strip()
        if not q:
            return []
        like = f"%{q}%"
        rows = self.conn.execute(
            """SELECT l.id, l.title_fa, l.tags, lv.title_fa AS level_title, c.title_fa AS chapter_title, c.id AS chapter_id
               FROM lessons l
               JOIN levels lv ON lv.id=l.level_id
               JOIN chapters c ON c.id=lv.chapter_id
               WHERE l.title_fa LIKE ? OR l.summary LIKE ? OR l.full_content LIKE ?
               ORDER BY c.order_index, lv.order_index, l.order_index
               LIMIT ?""",
            (like, like, like, limit),
        ).fetchall()
        return [dict(r) for r in rows]

    def stats(self):
        return {
            "chapters": self.conn.execute("SELECT COUNT(*) c FROM chapters").fetchone()["c"],
            "levels": self.conn.execute("SELECT COUNT(*) c FROM levels").fetchone()["c"],
            "lessons": self.conn.execute("SELECT COUNT(*) c FROM lessons").fetchone()["c"],
            "scenarios": self.conn.execute("SELECT COUNT(*) c FROM scenarios").fetchone()["c"],
            "with_content": self.conn.execute(
                "SELECT COUNT(*) c FROM lessons WHERE length(COALESCE(full_content,''))>50"
            ).fetchone()["c"],
        }


    def ensure_sync_columns(self):
        cols = [
            ("lessons", "uid", "TEXT"),
            ("lessons", "content_hash", "TEXT DEFAULT ''"),
            ("lessons", "device_id", "TEXT DEFAULT ''"),
            ("lessons", "deleted", "INTEGER DEFAULT 0"),
            ("scenarios", "uid", "TEXT"),
            ("scenarios", "content_hash", "TEXT DEFAULT ''"),
            ("scenarios", "device_id", "TEXT DEFAULT ''"),
            ("scenarios", "deleted", "INTEGER DEFAULT 0"),
        ]
        for table, col, defn in cols:
            try:
                self.conn.execute(f"ALTER TABLE {table} ADD COLUMN {col} {defn}")
                self.conn.commit()
            except Exception:
                pass
        # backfill lesson uids
        rows = self.conn.execute(
            """SELECT l.id, c.order_index AS co, lv.order_index AS lo, l.order_index AS o
               FROM lessons l
               JOIN levels lv ON lv.id=l.level_id
               JOIN chapters c ON c.id=lv.chapter_id
               WHERE l.uid IS NULL OR l.uid=''"""
        ).fetchall()
        for r in rows:
            uid = f"lesson:ch{int(r['co']):02d}:lv{int(r['lo']):03d}:l{int(r['o']):04d}"
            self.conn.execute("UPDATE lessons SET uid=? WHERE id=?", (uid, r["id"]))
        scs = self.conn.execute("SELECT id, code FROM scenarios WHERE uid IS NULL OR uid=''").fetchall()
        for r in scs:
            self.conn.execute("UPDATE scenarios SET uid=? WHERE id=?", (f"scenario:{r['code']}", r["id"]))
        self.conn.commit()

    def sync_index(self):
        self.ensure_sync_columns()
        out = []
        for r in self.conn.execute(
            "SELECT uid, last_updated, content_hash, COALESCE(deleted,0) AS deleted FROM lessons WHERE uid IS NOT NULL AND uid!=''"
        ).fetchall():
            out.append({"uid": r["uid"], "entity": "lesson", "last_updated": r["last_updated"] or "",
                        "content_hash": r["content_hash"] or "", "deleted": bool(r["deleted"])})
        for r in self.conn.execute(
            "SELECT uid, last_updated, content_hash, COALESCE(deleted,0) AS deleted FROM scenarios WHERE uid IS NOT NULL AND uid!=''"
        ).fetchall():
            out.append({"uid": r["uid"], "entity": "scenario", "last_updated": r["last_updated"] or "",
                        "content_hash": r["content_hash"] or "", "deleted": bool(r["deleted"])})
        return out

    def sync_pull(self, uids):
        if not uids:
            return []
        self.ensure_sync_columns()
        qmarks = ",".join("?" * len(uids))
        rows = self.conn.execute(
            f"""SELECT uid, title_fa, title_en, tags, summary, full_content, commands, examples, notes,
                       meta_json, search_query, learning_objectives, source_status, last_updated,
                       content_hash, device_id, COALESCE(deleted,0) AS deleted
                FROM lessons WHERE uid IN ({qmarks})""",
            list(uids),
        ).fetchall()
        out = []
        for r in rows:
            d = dict(r)
            d["entity"] = "lesson"
            out.append(d)
        rows2 = self.conn.execute(
            f"SELECT * FROM scenarios WHERE uid IN ({qmarks})", list(uids)
        ).fetchall()
        for r in rows2:
            d = dict(r)
            d["entity"] = "scenario"
            out.append(d)
        return out

    def sync_apply(self, records):
        """اعمال رکوردهای پذیرفته‌شده از کلاینت (LWW)."""
        self.ensure_sync_columns()
        for rec in records:
            uid = rec.get("uid") or ""
            entity = rec.get("entity") or ("scenario" if uid.startswith("scenario:") else "lesson")
            if entity == "lesson":
                row = self.conn.execute("SELECT id FROM lessons WHERE uid=?", (uid,)).fetchone()
                if not row:
                    continue
                self.conn.execute(
                    """UPDATE lessons SET summary=?, full_content=?, commands=?, examples=?, notes=?,
                       meta_json=?, search_query=?, learning_objectives=?, source_status=?,
                       last_updated=?, content_hash=?, device_id=?, deleted=?
                       WHERE uid=?""",
                    (
                        rec.get("summary", ""),
                        rec.get("full_content", ""),
                        rec.get("commands", ""),
                        rec.get("examples", ""),
                        rec.get("notes", ""),
                        rec.get("meta_json", "{}"),
                        rec.get("search_query", ""),
                        rec.get("learning_objectives", ""),
                        rec.get("source_status", "unverified"),
                        rec.get("last_updated"),
                        rec.get("content_hash", ""),
                        rec.get("device_id", ""),
                        1 if rec.get("deleted") else 0,
                        uid,
                    ),
                )
            elif entity == "scenario":
                row = self.conn.execute("SELECT id FROM scenarios WHERE uid=?", (uid,)).fetchone()
                if not row:
                    continue
                self.conn.execute(
                    """UPDATE scenarios SET title_fa=?, tasks=?, solution=?, verification=?,
                       last_updated=?, content_hash=?, device_id=?, deleted=?
                       WHERE uid=?""",
                    (
                        rec.get("title_fa") or "",
                        rec.get("tasks", ""),
                        rec.get("solution", ""),
                        rec.get("verification", ""),
                        rec.get("last_updated"),
                        rec.get("content_hash", ""),
                        rec.get("device_id", ""),
                        1 if rec.get("deleted") else 0,
                        uid,
                    ),
                )
        self.conn.commit()
