# -*- coding: utf-8 -*-
"""وضعیت مطالعه و صف مرور — SRS (Again/Hard/Good/Easy)."""
from __future__ import annotations

from datetime import datetime, timedelta


def ensure_study_table(conn):
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS study_progress (
            lesson_uid TEXT PRIMARY KEY,
            status TEXT DEFAULT 'new',
            ease REAL DEFAULT 2.5,
            interval_hours INTEGER DEFAULT 1,
            last_studied TEXT,
            next_review TEXT,
            times_studied INTEGER DEFAULT 0,
            notes TEXT DEFAULT ''
        );
        CREATE INDEX IF NOT EXISTS idx_study_next ON study_progress(next_review);
        CREATE INDEX IF NOT EXISTS idx_study_status ON study_progress(status);
        """
    )
    conn.commit()


def _now():
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def mark_study(conn, lesson_uid: str, action: str):
    """action: again | hard | good | easy | studied | forgot"""
    ensure_study_table(conn)
    row = conn.execute("SELECT * FROM study_progress WHERE lesson_uid=?", (lesson_uid,)).fetchone()
    now = datetime.utcnow()
    if row is None:
        ease, interval, times = 2.5, 0, 0
    else:
        ease = float(row["ease"] if hasattr(row, "keys") else row[2] or 2.5)
        interval = int(row["interval_hours"] if hasattr(row, "keys") else row[3] or 0)
        times = int(row["times_studied"] if hasattr(row, "keys") else row[6] or 0)

    times += 1
    action = (action or "good").lower()
    if action in ("again", "forgot"):
        ease = max(1.3, ease - 0.25)
        interval = 1
        status = "learning"
        next_r = now + timedelta(hours=1)
    elif action == "hard":
        ease = max(1.3, ease - 0.1)
        interval = 6 if interval <= 0 else max(3, int(interval * 1.2))
        status = "review"
        next_r = now + timedelta(hours=interval)
    elif action == "easy":
        ease = min(3.0, ease + 0.15)
        interval = 72 if interval <= 0 else max(48, int(interval * ease * 1.3))
        if interval > 24 * 45:
            interval = 24 * 45
        status = "known" if times >= 2 else "learning"
        next_r = now + timedelta(hours=interval)
    else:
        if interval <= 0 or interval < 24:
            interval = 24
        else:
            interval = max(24, int(interval * ease))
        if interval > 24 * 30:
            interval = 24 * 30
        status = "known" if times >= 3 and interval >= 72 else "learning"
        next_r = now + timedelta(hours=interval)

    conn.execute(
        """INSERT INTO study_progress(lesson_uid,status,ease,interval_hours,last_studied,next_review,times_studied)
           VALUES(?,?,?,?,?,?,?)
           ON CONFLICT(lesson_uid) DO UPDATE SET
             status=excluded.status, ease=excluded.ease, interval_hours=excluded.interval_hours,
             last_studied=excluded.last_studied, next_review=excluded.next_review,
             times_studied=excluded.times_studied""",
        (lesson_uid, status, ease, interval, _now(), next_r.replace(microsecond=0).isoformat() + "Z", times),
    )
    conn.commit()
    return {"uid": lesson_uid, "status": status, "next_review": next_r.isoformat() + "Z",
            "interval_hours": interval, "ease": ease, "times_studied": times}


def due_reviews(conn, limit=50):
    ensure_study_table(conn)
    now = _now()
    rows = conn.execute(
        """SELECT lesson_uid, status, next_review, times_studied FROM study_progress
           WHERE next_review IS NOT NULL AND next_review <= ? ORDER BY next_review LIMIT ?""",
        (now, limit),
    ).fetchall()
    return [dict(r) if hasattr(r, "keys") else {"lesson_uid": r[0], "status": r[1], "next_review": r[2], "times_studied": r[3]} for r in rows]


def study_stats(conn):
    ensure_study_table(conn)
    def cnt(st):
        return conn.execute("SELECT COUNT(*) c FROM study_progress WHERE status=?", (st,)).fetchone()[0]
    total = conn.execute("SELECT COUNT(*) c FROM study_progress").fetchone()[0]
    return {"tracked": total, "new": cnt("new"), "learning": cnt("learning"),
            "known": cnt("known"), "review": cnt("review"), "due": len(due_reviews(conn, 500))}
