# -*- coding: utf-8 -*-
"""Validate structure, curriculum coverage, and separate question/answer storage."""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path

p = Path(__file__).with_name('automation_python_curriculum_pack.json')
data = json.loads(p.read_text(encoding='utf-8'))
lessons = data['lessons']
assert len(lessons) == 135, f'expected 135 lessons, got {len(lessons)}'
assert len({x['uid'] for x in lessons}) == len(lessons), 'duplicate UID'
assert len({(x['chapter_order'], x['subchapter_order'], x['lesson_order']) for x in lessons}) == len(lessons), 'duplicate structural position'
assert len({x['topic'] for x in lessons}) == 27, 'expected 27 distinct topics'
expected_positions = {(21, 4): 35, (35, 3): 25, (51, 1): 25, (51, 2): 25, (51, 3): 25}
assert Counter((x['chapter_order'], x['subchapter_order']) for x in lessons) == expected_positions
required_sections = [
    '## عنوان انگلیسی', '## خلاصه', '## اهداف یادگیری', '## پیش‌نیازها',
    '## مقدمهٔ مفهومی', '## مفاهیم اصلی', '## سازوکار داخلی و معماری',
    '## مثال مرحله‌به‌مرحله و ابزارها', '## مثال محیط کار', '## آزمایشگاه عملی',
    '## عیب‌یابی مرحله‌ای', '## امنیت، محدودیت‌ها و اشتباهات رایج',
    '## نکات پیشرفته', '## جمع‌بندی', '## واژه‌نامه',
]
for lesson in lessons:
    uid = lesson['uid']
    assert lesson['uid'] == f"lesson:ch{lesson['chapter_order']:02d}:lv{lesson['subchapter_order']:03d}:l{lesson['lesson_order']:04d}", uid
    assert len(lesson['full_content']) > 1400, f'short body: {uid}'
    assert all(section in lesson['full_content'] for section in required_sections), f'missing section: {uid}'
    assert lesson['summary'].strip() and lesson['commands'].strip() and lesson['examples'].strip() and lesson['notes'].strip(), f'missing teaching field: {uid}'
    assert lesson['learning_objectives'] and lesson['meta'].get('official_sources'), f'missing objectives/sources: {uid}'
    a = lesson['meta']['assessment']
    questions = a['questions']
    answers = a['answer_key']
    assert len(questions) == 4, f'expected 4 questions: {uid}'
    assert len(answers) == 4, f'expected 4 answer keys: {uid}'
    qids = {q['id'] for q in questions}
    aids = {x['question_id'] for x in answers}
    assert qids == aids, f'question/answer IDs differ: {uid}'
    assert all('answer' not in q and 'correct_option_id' not in q for q in questions), f'answer leaked: {uid}'
    q1 = next(q for q in questions if q['id'] == 'Q1')
    a1 = next(a for a in answers if a['question_id'] == 'Q1')
    assert len(q1.get('options', [])) == 4, f'multiple-choice option count: {uid}'
    option_ids = {o['id'] for o in q1['options']}
    assert a1.get('correct_option_id') in option_ids, f'correct option missing: {uid}'
    expected_wrong = option_ids - {a1['correct_option_id']}
    actual_wrong = {x['option_id'] for x in a1.get('distractor_rationales', [])}
    assert expected_wrong == actual_wrong, f'distractor rationale coverage mismatch: {uid}'
    assert all(x.get('why_wrong') for x in a1['distractor_rationales']), f'empty distractor rationale: {uid}'

print('PASS: valid UTF-8 JSON syntax')
print('PASS: 135 unique lessons across 27 topics')
print('PASS: expected structure covered: ch21/sub4=35; ch35/sub3=25; ch51/sub1-3=75')
print('PASS: all lessons contain the 15 required teaching sections and populated teaching fields')
print('PASS: stable UID pattern and unique structural positions')
print('PASS: each lesson has 4 questions, 4 separated answers, 4 options, and per-distractor rationales')
print('PASS: official sources and learning objectives are present')
print(f'File bytes: {p.stat().st_size}')
