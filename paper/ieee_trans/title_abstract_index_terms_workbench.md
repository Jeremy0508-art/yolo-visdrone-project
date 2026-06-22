# IEEE T-ITS Title, Abstract, and Index Terms Workbench

Status: planning workbench, not final submission text.

This file prepares the front matter for a possible IEEE Transactions on Intelligent Transportation Systems (T-ITS) submission. It must be updated after the final method, cross-dataset evidence, and audited result tables are settled.

## T-ITS Front-Matter Rules

Primary source: `https://ieee-itss.org/pub/t-its/`

| Item | Working Rule |
| --- | --- |
| Article type | Plan as a Regular Paper unless the advisor selects another article type. |
| Length target | Keep the future manuscript close to the suggested 10 IEEE double-column pages. |
| Abstract length | 150-250 words. |
| Abstract form | 150-250 words, one paragraph, self-contained, no displayed equations, no tables, no references, and no unsupported abbreviations. |
| Keywords / index terms | Maximum six; select from both methodology-oriented terms and application-oriented terms where required by T-ITS. |
| Application fit | The title and abstract should make UAV-assisted traffic perception visible if T-ITS remains the target. |
| Official source | Use `paper/ieee_tits_author_requirements_audit.md` before finalizing front matter. |

## Current Safe Title Candidates

Use one of these only if no adaptive module passes the final evidence gate:

1. High-Resolution Lightweight YOLO for Small Object Detection in UAV Traffic Scenes
2. Revisiting High-Resolution Prediction Branches for Lightweight UAV Traffic Object Detection
3. Boundary-Aware High-Resolution Prediction for Lightweight UAV Traffic Object Detection

## Retired Stronger Title Candidate

The following candidate is no longer allowed because the completed method
decision audit rejected ScaleGate as the main method:

| Candidate Title | Reason |
| --- | --- |
| ScaleGate-YOLO11n: Adaptive High-Resolution Prediction for UAV Traffic Object Detection | ScaleGate did not pass the predeclared main-method acceptance routes. |

## Locked Stronger Title Candidates

Use these only after the corresponding evidence exists:

| Candidate Title | Unlock Condition |
| --- | --- |
| CSGate-YOLO11n: Cross-Scale High-Resolution Prediction for UAV Traffic Object Detection | CSGate passes the complete VisDrone/UAVDT method-selection gates and has refreshed speed and scale-wise audits. |
| Scale-Aware High-Resolution Prediction for Lightweight UAV-Assisted Traffic Perception | A later adaptive-P2 module is selected as the final method, with speed and scale-wise audits complete. |
| Adaptive P2 Feature Gating for Lightweight UAV Small-Object Detection | The final method evidence supports an adaptive high-resolution mechanism rather than only a boundary-study route. |

## Abstract Structure

The final abstract should use this order:

1. Problem: small and dense road users in UAV traffic scenes.
2. Gap: lightweight detectors lose fine spatial details or suffer capacity limits.
3. Method: only the final selected method and validated components.
4. Evidence: exact VisDrone and cross-dataset values from audited tables.
5. Efficiency: exact parameters/FLOPs/FPS or latency if reported.
6. Conclusion: evidence-bounded trade-off, not universal superiority.

## Current Safe Abstract Template

This template is safe for internal discussion only and should not be submitted as final text.

> Detecting small road users in unmanned aerial vehicle (UAV) traffic imagery is challenging because objects often appear at tiny scales, in dense layouts, and under occlusion or viewpoint variation. This study investigates lightweight YOLO-based detection for UAV-assisted traffic perception, focusing on how input resolution, high-resolution P2 prediction, and adaptive feature gating affect YOLO11n variants. Completed VisDrone2019-DET and UAVDT experiments are traced to local training logs, validation outputs, and model artifacts. Current evidence indicates that static P2 prediction improves some VisDrone small-object diagnostics but does not transfer to UAVDT under the completed setting. The completed ScaleAwareP2Gate experiment remains mixed/negative evidence rather than the final method, motivating a second-cycle CrossScaleP2P3ConsistencyGate candidate whose performance must remain locked until complete audited runs exist.

Approximate length: 132 words by manual count. This is intentionally short because final numeric CSGate results and the final method decision are still locked.

## Locked Final Abstract Template

Use this only after final evidence exists:

> Detecting small road users in unmanned aerial vehicle (UAV) traffic scenes remains difficult for lightweight detectors because dense objects are easily degraded by downsampling, occlusion, and scale variation. This paper proposes [FINAL METHOD], a [EVIDENCE-BACKED DESCRIPTION] for lightweight traffic-object detection. [FINAL METHOD] is evaluated on VisDrone2019-DET and UAVDT against YOLO11n, YOLOv8n, YOLO11s, static P2, and controlled ablation variants under matched training settings. On [PRIMARY DATASET], it achieves [REAL METRIC], improves [REAL MATCHED BASELINE COMPARISON], and records [REAL EFFICIENCY VALUE]. Scale-wise analysis shows [REAL SMALL-OBJECT FINDING]. Cross-dataset experiments on UAVDT show [REAL SUPPORTED FINDING]. The results indicate that [EVIDENCE-BOUNDED CONCLUSION].

Do not fill any bracketed placeholder without a traceable table or run artifact.

## Candidate Index Terms

Final index terms should be selected after the target journal is confirmed. For T-ITS, keep the total at no more than six, with one to two methodology terms, one to two application terms, and no more than two optional free keywords.

Methodology candidates:

- Computer vision
- Image processing
- Artificial intelligence
- Data-based approaches

Application candidates:

- Road transportation
- Pedestrian flows and crowds
- Smart cities
- Air transportation

Free-keyword candidates:

- UAV object detection
- Small object detection
- Lightweight YOLO
- Traffic perception
- Scale-aware feature fusion

## Front-Matter Claim Checks

Before moving any title, abstract, or index terms into `main.tex`:

| Check | Required State |
| --- | --- |
| Final target journal | Advisor confirms T-ITS or another exact IEEE venue. |
| Final method name | Selected from real metrics, not preference. |
| Result numbers | Match audited CSV/LaTeX tables exactly. |
| Small-object wording | Uses local scale-bin AP or recall wording correctly; no false official AP-small claim. |
| Generalization wording | Uses UAVDT only after conversion and complete runs. |
| Efficiency wording | Uses measured speed/complexity rows only. |
| Comparative wording | Acknowledges YOLO11s-960 if discussing absolute accuracy. |
