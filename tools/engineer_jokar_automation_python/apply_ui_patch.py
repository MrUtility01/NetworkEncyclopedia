# -*- coding: utf-8 -*-
"""Add separate assessment and answer-key tabs to the existing NetworkEncyclopedia web UI."""
from __future__ import annotations
import argparse
from datetime import datetime
from pathlib import Path
import shutil
import sys

TAB_ANCHOR = '    { id: "meta", label: "Meta / پرامپت", body: formatMeta(les) },\n  ];'
TAB_REPLACEMENT = '''    { id: "meta", label: "Meta / پرامپت", body: formatMeta(les) },
    { id: "assessment", label: "سؤال‌ها", body: formatAssessmentQuestions(les) },
    { id: "answer-key", label: "پاسخ‌نامه", body: formatAssessmentAnswers(les) },
  ];'''
FUNCTION_ANCHOR = 'async function showScenarios() {'
FUNCTIONS = r'''function formatAssessmentQuestions(les) {
  const assessment = ((les.meta || {}).assessment || {});
  const questions = assessment.questions || [];
  if (!questions.length) return "برای این درس سؤال ارزیابی ثبت نشده است.";
  return questions.map((q, index) => {
    const lines = [`${index + 1}. [${q.difficulty || ""}] ${q.question || ""}`];
    (q.options || []).forEach((option) => {
      lines.push(`   ${option.id || "-"}) ${option.text || ""}`);
    });
    return lines.join("\n");
  }).join("\n\n");
}
function formatAssessmentAnswers(les) {
  const assessment = ((les.meta || {}).assessment || {});
  const answers = assessment.answer_key || [];
  const questions = assessment.questions || [];
  if (!answers.length) return "پاسخ‌نامهٔ جداگانه برای این درس ثبت نشده است.";
  const questionById = Object.fromEntries(questions.map((q) => [q.id, q]));
  return answers.map((answer, index) => {
    const q = questionById[answer.question_id] || {};
    const lines = [`${index + 1}. ${q.question || answer.question_id || "پاسخ"}`];
    if (answer.correct_option_id) {
      const option = (q.options || []).find((o) => o.id === answer.correct_option_id);
      lines.push(`گزینهٔ صحیح: ${answer.correct_option_id}${option ? `) ${option.text}` : ""}`);
    }
    if (answer.answer) lines.push(`پاسخ: ${answer.answer}`);
    if (answer.rationale) lines.push(`دلیل: ${answer.rationale}`);
    if (answer.rubric && answer.rubric.length) lines.push(`معیار ارزیابی: ${answer.rubric.join("؛ ")}`);
    if (answer.distractor_rationales && answer.distractor_rationales.length) {
      lines.push("گزینه‌های نادرست:");
      answer.distractor_rationales.forEach((d) => lines.push(`- ${d.option_id}: ${d.why_wrong}`));
    }
    return lines.join("\n");
  }).join("\n\n");
}

'''


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--project', type=Path, default=Path('.'), help='Root of the checked-out NetworkEncyclopedia project')
    ap.add_argument('--apply', action='store_true', help='Write the patch; default is dry-run')
    args = ap.parse_args()
    target = args.project / 'server' / 'static' / 'app.js'
    if not target.is_file():
        print(f'Cannot find {target}. Run from the repository root or pass --project.', file=sys.stderr)
        return 2
    text = target.read_text(encoding='utf-8')
    if 'formatAssessmentQuestions(les)' in text and 'formatAssessmentAnswers(les)' in text:
        print('Assessment tabs already appear to be installed; no change made.')
        return 0
    if text.count(TAB_ANCHOR) != 1 or text.count(FUNCTION_ANCHOR) != 1:
        print('Expected UI anchors were not found exactly once; refusing to edit an unexpected app.js version.', file=sys.stderr)
        return 2
    if not args.apply:
        print(f'DRY RUN: would add separate assessment/answer-key tabs to {target}')
        print('No file was changed. Rerun with --apply after reviewing the target file/version.')
        return 0
    backup = target.with_name(f'app.js.before-assessment-patch-{datetime.now().strftime("%Y%m%d-%H%M%S")}.js')
    shutil.copy2(target, backup)
    patched = text.replace(TAB_ANCHOR, TAB_REPLACEMENT, 1).replace(FUNCTION_ANCHOR, FUNCTIONS + FUNCTION_ANCHOR, 1)
    target.write_text(patched, encoding='utf-8')
    print(f'Patched: {target}')
    print(f'Backup: {backup}')
    print('The question and answer-key tabs read only meta.assessment.questions and meta.assessment.answer_key.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
