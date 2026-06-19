# IEEE Cover Letter Workbench

Status: planning workbench, not a final cover letter.

This file prepares the cover-letter logic for a possible IEEE Transactions submission. It must be rewritten after the target journal, final method, author list, and final evidence tables are fixed.

## Target Use

Primary working target:

> IEEE Transactions on Intelligent Transportation Systems

The cover letter must make the transportation-system relevance explicit. If the advisor selects another IEEE Transactions venue, rewrite the first paragraph and contribution framing before submission.

## Evidence Rules

Do not state the following in the cover letter until the corresponding evidence exists:

- TOFC improves detection performance.
- UAVDT confirms cross-dataset generalization.
- The method achieves state-of-the-art performance.
- The method outperforms larger-capacity detectors.
- Official VisDrone test-dev results are available.
- Any metric not present in audited local tables or official evaluation outputs.

## Cover Letter Skeleton

Use this as structure only.

```text
Dear Editor-in-Chief and Editorial Office,

We are submitting the manuscript entitled "[FINAL TITLE]" for consideration as a [ARTICLE TYPE] in [TARGET JOURNAL].

The manuscript addresses UAV-assisted traffic perception, where pedestrians, vehicles, bicycles, motorcycles, and other road users often appear as small, dense, and occluded targets in aerial imagery. This topic is aligned with the journal scope because it studies computer-vision-based sensing and evaluation for intelligent transportation systems.

The main contribution of the manuscript is [FINAL CONTRIBUTION SUMMARY]. All experimental results are based on traceable training logs, validation outputs, model artifacts, and audited result tables. The manuscript reports [DATASETS], [BASELINES], [ABLATIONS], scale-wise analysis, and speed/complexity measurements.

Compared with existing work, the manuscript emphasizes [EVIDENCE-BACKED NOVELTY], while explicitly discussing the trade-off between lightweight deployment and absolute accuracy. In particular, the comparison with larger-capacity detectors is used as a capacity reference rather than as an unsupported superiority claim.

This manuscript has not been submitted elsewhere and is not under consideration by another journal or conference. All authors have approved the submission. Any prior related materials, code repository, or preprint status will be disclosed according to IEEE policy.

Thank you for considering our submission.

Sincerely,
[CORRESPONDING AUTHOR NAME]
[AFFILIATION]
[EMAIL]
```

## Placeholder Unlock Table

| Placeholder | Required Evidence / Confirmation |
| --- | --- |
| `[FINAL TITLE]` | Final method route and target journal confirmed. |
| `[ARTICLE TYPE]` | Advisor confirms Regular Paper, Short Paper, or another type. |
| `[TARGET JOURNAL]` | Advisor confirms exact IEEE venue. |
| `[FINAL CONTRIBUTION SUMMARY]` | Must match final introduction contribution list. |
| `[DATASETS]` | Use VisDrone only unless UAVDT or another dataset is complete. |
| `[BASELINES]` | Use only completed local baselines or clearly marked literature-only comparisons. |
| `[ABLATIONS]` | Use only completed P2/input/CA/TOFC/training-policy ablations. |
| `[EVIDENCE-BACKED NOVELTY]` | TOFC or fallback high-resolution study wording selected from real results. |
| Corresponding author fields | User/advisor confirmation required. |

## Submission-Ethics Notes

- The paused CEA route should not be submitted simultaneously with the IEEE manuscript.
- If any Chinese manuscript, public report, or preprint overlaps with the IEEE submission, it must be disclosed and cited as required.
- The final paper should not reuse the CEA manuscript as a direct translation; the IEEE manuscript must be rewritten around the final English contribution and evidence.
- The public GitHub repository can be mentioned only after the advisor agrees to code/data release scope.

## Final Cover Letter Checklist

Before creating a final `cover_letter_draft.md`:

| Check | Status Needed |
| --- | --- |
| Exact target journal | Confirmed |
| Article type | Confirmed |
| Final title | Confirmed |
| Author list/order | Confirmed |
| Corresponding author | Confirmed |
| Final method evidence | Complete |
| Cross-dataset claims | Complete or omitted |
| Code/data availability wording | Confirmed |
| No unsupported metric claims | Verified against `paper/ieee_claim_audit.md` |
