# -*- coding: utf-8 -*-
"""وضعیت مطالعه و صف مرور (SRS ساده)."""
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
    """action: studied | again | forgot"""
    ensure_study_table(conn)
    row = conn.execute(
        "SELECT * FROM study_progress WHERE lesson_uid=?", (lesson_uid,)
    ).fetchone()
    now = datetime.utcnow()
    if row is None:
        status, ease, interval, times = "new", 2.5, 1, 0
    else:
        status = row["status"] if isinstance(row, dict) else row[1]
        ease = float(row["ease"] if isinstance(row, dict) else row[2] or 2.5)
        interval = int(row["interval_hours"] if isinstance(row, dict) else row[3] or 1)
        times = int(row["times_studied"] if isinstance(row, dict) else row[6] or 0)

    if action == "studied":
        times += 1
        interval = max(1, int(interval * ease))
        if interval > 24 * 30:
            interval = 24 * 30
        status = "known" if times >= 3 and interval >= 24 else "learning"
        next_r = now + timedelta(hours=interval)
    elif action == "again":
        times += 1
        interval = 1
        status = "review"
        next_r = now + timedelta(hours=1)
    else:  # forgot
        times += 1
        interval = 1
        ease = max(1.3, ease - 0.2)
        status = "learning"
        next_r = now + timedelta(hours=1)

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
    return {"uid": lesson_uid, "status": status, "next_review": next_r.isoformat() + "Z", "interval_hours": interval}


def due_reviews(conn, limit=50):
    ensure_study_table(conn)
    now = _now()
    rows = conn.execute(
        """SELECT lesson_uid, status, next_review, times_studied FROM study_progress
           WHERE next_review IS NOT NULL AND next_review <= ?
           ORDER BY next_review LIMIT ?""",
        (now, limit),
    ).fetchall()
    return [dict(r) if hasattr(r, "keys") else {"lesson_uid": r[0], "status": r[1], "next_review": r[2], "times_studied": r[3]} for r in rows]


def study_stats(conn):
    ensure_study_table(conn)
    def cnt(st):
        return conn.execute("SELECT COUNT(*) c FROM study_progress WHERE status=?", (st,)).fetchone()[0]
    total = conn.execute("SELECT COUNT(*) c FROM study_progress").fetchone()[0]
    return {
        "tracked": total,
        "new": cnt("new"),
        "learning": cnt("learning"),
        "known": cnt("known"),
        "review": cnt("review"),
        "due": len(due_reviews(conn, 500)),
    }
