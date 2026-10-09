# -*- coding: utf-8 -*-
"""Safely apply automation/Python lesson content to NetworkEncyclopedia SQLite.

Default mode is read-only/dry-run. Use --apply to write. Use --overwrite to replace
existing teaching fields on the targeted lessons. Existing IDs, UIDs, titles, structure,
scenarios, study data, and all non-target lessons are preserved.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import shutil
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_PACK = ROOT / 'automation_python_curriculum_pack.json'
DEFAULT_DB = Path('server/data/encyclopedia.db')
TEACHING_COLUMNS = [
    'summary', 'full_content', 'commands', 'examples', 'notes', 'search_query',
    'learning_objectives', 'meta_json', 'source_status', 'last_updated', 'content_hash'
]


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def canonical_content_hash(record: dict) -> str:
    # Matches shared/sync_engine.py: semantic fields only, deterministic JSON encoding.
    keys = sorted(k for k in record if k not in ('device_id', 'last_updated', 'content_hash'))
    data = {k: record[k] for k in keys}
    blob = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(blob.encode('utf-8')).hexdigest()


def ensure_column(conn: sqlite3.Connection, table: str, column: str, definition: str) -> None:
    existing = {r['name'] for r in conn.execute(f'PRAGMA table_info({table})')}
    if column not in existing:
        conn.execute(f'ALTER TABLE {table} ADD COLUMN {column} {definition}')


def load_pack(path: Path) -> dict:
    with path.open('r', encoding='utf-8') as f:
        pack = json.load(f)
    lessons = pack.get('lessons')
    if not isinstance(lessons, list) or not lessons:
        raise ValueError('Pack must have a non-empty lessons array.')
    uids = [x.get('uid') for x in lessons]
    if any(not x for x in uids) or len(set(uids)) != len(uids):
        raise ValueError('Pack contains a missing or duplicate UID.')
    for item in lessons:
        if not all(item.get(k) for k in ('chapter_order', 'subchapter_order', 'lesson_order', 'title_fa', 'full_content')):
            raise ValueError(f'Incomplete lesson record: {item.get("uid")}')
        assessment = (item.get('meta') or {}).get('assessment') or {}
        question_ids = {q.get('id') for q in assessment.get('questions', [])}
        answer_ids = {a.get('question_id') for a in assessment.get('answer_key', [])}
        if not question_ids or not answer_ids or question_ids != answer_ids:
            raise ValueError(f'Assessment or separate answer key invalid for {item.get("uid")}')
        if any('answer' in q or 'correct_option_id' in q for q in assessment.get('questions', [])):
            raise ValueError(f'Answer leaked into question section for {item.get("uid")}')
    return pack


def connect_db(db_path: Path) -> sqlite3.Connection:
    if not db_path.exists():
        raise FileNotFoundError(f'Database not found: {db_path}\nExpected NetworkEncyclopedia path: server/data/encyclopedia.db')
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys=ON')
    return conn


def ensure_identity_columns(conn: sqlite3.Connection) -> None:
    # These are already part of the current project schema. If an older database lacks
    # them, add only the sync/content columns needed by the existing server contract.
    for name, definition in [
        ('uid', 'TEXT'), ('content_hash', "TEXT DEFAULT ''"),
        ('device_id', "TEXT DEFAULT ''"), ('deleted', 'INTEGER DEFAULT 0'),
        ('source_status', "TEXT DEFAULT 'unverified'"),
        ('meta_json', "TEXT DEFAULT '{}'"), ('search_query', "TEXT DEFAULT ''"),
        ('learning_objectives', "TEXT DEFAULT ''"), ('last_updated', 'TEXT'),
    ]:
        ensure_column(conn, 'lessons', name, definition)

    # Backfill only blank UIDs using the repo's deterministic recipe; never rewrite a UID.
    rows = conn.execute('''
        SELECT l.id, l.uid, c.order_index AS chapter_order,
               lv.order_index AS subchapter_order, l.order_index AS lesson_order
        FROM lessons l
        JOIN levels lv ON lv.id=l.level_id
        JOIN chapters c ON c.id=lv.chapter_id
        WHERE l.uid IS NULL OR l.uid=''
    ''').fetchall()
    for r in rows:
        generated = f"lesson:ch{int(r['chapter_order']):02d}:lv{int(r['subchapter_order']):03d}:l{int(r['lesson_order']):04d}"
        conn.execute('UPDATE lessons SET uid=? WHERE id=? AND (uid IS NULL OR uid=\'\')', (generated, r['id']))


def collect_targets(conn: sqlite3.Connection, pack: dict) -> tuple[list[dict], list[dict]]:
    rows = conn.execute('''
        SELECT l.*, c.order_index AS chapter_order,
               lv.order_index AS subchapter_order,
               l.order_index AS lesson_order
        FROM lessons l
        JOIN levels lv ON lv.id=l.level_id
        JOIN chapters c ON c.id=lv.chapter_id
    ''').fetchall()
    by_position = {(int(r['chapter_order']), int(r['subchapter_order']), int(r['lesson_order'])): r for r in rows}
    matched, skipped = [], []
    for lesson in pack['lessons']:
        key = (int(lesson['chapter_order']), int(lesson['subchapter_order']), int(lesson['lesson_order']))
        row = by_position.get(key)
        if row is None:
            skipped.append({'uid': lesson['uid'], 'reason': 'position_not_found', 'title_fa': lesson['title_fa']})
            continue
        if row['title_fa'] != lesson['title_fa']:
            skipped.append({
                'uid': lesson['uid'], 'reason': 'title_mismatch',
                'expected_title': lesson['title_fa'], 'database_title': row['title_fa'],
                'actual_uid': row['uid'] if 'uid' in row.keys() else None,
            })
            continue
        matched.append({'content': lesson, 'row': dict(row)})
    return matched, skipped


def make_backup(conn: sqlite3.Connection, db_path: Path) -> Path:
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    backup_path = db_path.with_name(f'{db_path.stem}.before_automation_python_{stamp}{db_path.suffix}')
    dest = sqlite3.connect(str(backup_path))
    try:
        conn.backup(dest)
        dest.commit()
    finally:
        dest.close()
    return backup_path


def current_meta(raw: str) -> dict:
    try:
        value = json.loads(raw or '{}')
        return value if isinstance(value, dict) else {}
    except Exception:
        return {}


def apply_one(conn: sqlite3.Connection, content: dict, row: dict, overwrite: bool) -> bool:
    existing_content = (row.get('full_content') or '').strip()
    if existing_content and not overwrite:
        return False

    # Keep the DB's current UID, even if a local/custom UID differs from the default UID.
    existing_uid = row.get('uid') or content['uid']
    old_meta = current_meta(row.get('meta_json') or '{}')
    new_meta = dict(old_meta)
    # Preserve project-specific metadata keys while updating lesson learning data.
    for key, value in content['meta'].items():
        new_meta[key] = value
    new_meta['lesson_uid'] = existing_uid
    new_meta['content_status'] = 'curated_draft_review_required'
    meta_json = json.dumps(new_meta, ensure_ascii=False, sort_keys=True)
    learning_objectives = '\n'.join(content['learning_objectives'])
    timestamp = now_utc()

    semantic = {
        'uid': existing_uid,
        'entity': 'lesson',
        'title_fa': row['title_fa'],
        'title_en': row.get('title_en') or content.get('title_en') or '',
        'tags': row.get('tags') or content.get('tags') or '',
        'summary': content['summary'],
        'full_content': content['full_content'],
        'commands': content['commands'],
        'examples': content['examples'],
        'notes': content['notes'],
        'meta_json': meta_json,
        'search_query': content['search_query'],
        'learning_objectives': learning_objectives,
        'source_status': 'review_required',
        'deleted': bool(row.get('deleted', 0)),
    }
    digest = canonical_content_hash(semantic)
    conn.execute('''
        UPDATE lessons SET summary=?, full_content=?, commands=?, examples=?, notes=?,
          search_query=?, learning_objectives=?, meta_json=?, source_status=?,
          last_updated=?, content_hash=?
        WHERE id=?
    ''', (
        content['summary'], content['full_content'], content['commands'], content['examples'],
        content['notes'], content['search_query'], learning_objectives, meta_json,
        'review_required', timestamp, digest, row['id'],
    ))
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', type=Path, default=DEFAULT_DB, help='Path to server/data/encyclopedia.db')
    parser.add_argument('--pack', type=Path, default=DEFAULT_PACK, help='Path to JSON content pack')
    parser.add_argument('--apply', action='store_true', help='Write changes; without this the script is dry-run only')
    parser.add_argument('--overwrite', action='store_true', help='Replace current teaching fields on matching target lessons')
    args = parser.parse_args()

    pack = load_pack(args.pack)
    conn = connect_db(args.db)
    try:
        matched, skipped = collect_targets(conn, pack)
        existing = sum(1 for x in matched if (x['row'].get('full_content') or '').strip())
        print(f"Pack lessons: {len(pack['lessons'])}")
        print(f"Matched by chapter/subchapter/order AND exact title: {len(matched)}")
        print(f"Skipped due to missing position/title mismatch: {len(skipped)}")
        print(f"Already containing full_content: {existing}")
        if skipped:
            print('\nSkipped records (first 20):')
            for x in skipped[:20]: print(' -', json.dumps(x, ensure_ascii=False))
        if not args.apply:
            would_update = len(matched) if args.overwrite else sum(1 for x in matched if not (x['row'].get('full_content') or '').strip())
            print(f"DRY RUN: would update {would_update} lesson(s). No teaching content written.")
            print('To apply all targeted content after review, rerun with --apply --overwrite.')
            return 0 if not skipped else 2
        if skipped:
            print('ABORT: target mismatch exists; fix/reconcile the curriculum before applying.', file=sys.stderr)
            return 2
        if not args.overwrite and existing:
            print('ABORT: some target lessons already contain content. Add --overwrite to intentionally replace those teaching fields.', file=sys.stderr)
            return 2
        backup = make_backup(conn, args.db)
        # Snapshot identities for every target, including custom nonblank UIDs.
        expected_identity = {
            item['row']['id']: {
                'uid': item['row'].get('uid') or item['content']['uid'],
                'title_fa': item['row']['title_fa'],
            }
            for item in matched
        }
        conn.execute('BEGIN')
        updates = 0
        try:
            ensure_identity_columns(conn)
            for item in matched:
                if apply_one(conn, item['content'], item['row'], args.overwrite):
                    updates += 1
            # Validate exact target IDs before commit, so failures roll back atomically.
            ids = list(expected_identity)
            placeholders = ','.join('?' for _ in ids)
            query = f'SELECT id, uid, title_fa, full_content, meta_json, source_status FROM lessons WHERE id IN ({placeholders})'
            check = conn.execute(query, ids).fetchall()
            invalid = []
            if len(check) != len(expected_identity):
                invalid.append(('target_rows', 'row_count_changed'))
            for r in check:
                expected = expected_identity[r['id']]
                if r['uid'] != expected['uid']:
                    invalid.append((r['uid'], 'uid_changed'))
                if r['title_fa'] != expected['title_fa']:
                    invalid.append((r['uid'], 'title_changed'))
                if not (r['full_content'] or '').strip():
                    invalid.append((r['uid'], 'empty_content'))
                    continue
                try:
                    meta = json.loads(r['meta_json'] or '{}')
                except Exception:
                    invalid.append((r['uid'], 'invalid_meta_json'))
                    continue
                assess = meta.get('assessment') or {}
                qids = {q.get('id') for q in assess.get('questions', [])}
                aids = {a.get('question_id') for a in assess.get('answer_key', [])}
                if not qids or qids != aids:
                    invalid.append((r['uid'], 'assessment_mismatch'))
                if any('answer' in q or 'correct_option_id' in q for q in assess.get('questions', [])):
                    invalid.append((r['uid'], 'answers_not_separated'))
            if invalid:
                raise ValueError(f'Post-write validation failed; transaction will roll back: {invalid[:20]}')
            conn.commit()
        except Exception as exc:
            conn.rollback()
            print(f'APPLY FAILED; changes rolled back. Backup retained at {backup}. Details: {exc}', file=sys.stderr)
            return 3
        print(f'APPLIED: updated {updates} lessons.')
        print(f'Backup: {backup}')
        print('Existing lesson IDs, non-target records, chapter/level records, and title/UID values were not changed.')
        print('Content status is review_required: examples have not been executed against your specific versions/devices.')
        return 0
    finally:
        conn.close()

if __name__ == '__main__':
    raise SystemExit(main())
