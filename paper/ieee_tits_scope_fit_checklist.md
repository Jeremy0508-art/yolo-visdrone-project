# IEEE T-ITS Scope-Fit Checklist

Status: planning checklist for the IEEE Transactions route.

Last official-source check: 2026-06-19.

## Purpose

This checklist translates the official scope and author guidance of IEEE Transactions on Intelligent Transportation Systems (T-ITS) into concrete requirements for this YOLO-VisDrone project. It does not add new experimental claims. It defines what the final English manuscript must prove before T-ITS is treated as the primary submission target.

## Official Scope Points to Satisfy

Primary source:

- IEEE Transactions on Intelligent Transportation Systems official page: `https://ieee-itss.org/pub/t-its/`

Relevant official-scope implications:

| T-ITS Scope Requirement | Project-Specific Interpretation | Current Status |
| --- | --- | --- |
| Modern transportation systems, including sensing, implementation, experimentation, and evaluation | The manuscript must frame UAV detection as traffic-scene sensing and evaluation, not only as a generic object-detection benchmark. | Partially ready |
| Transportation systems involving surface traffic, infrastructure, pedestrians, bicyclists, and other road users | VisDrone examples and category discussion should emphasize road users: pedestrians, vehicles, bicycles, motorcycles, and dense traffic-like scenes. | Partially ready |
| Computer vision, image processing, data-based learning, AI, and sensor technology are acceptable methodologies | YOLO-based UAV visual perception is in scope if the transportation application is explicit and load-bearing. | Ready as framing |
| A clear application to transportation systems must be addressed | The final manuscript must explain how small-object detection benefits UAV-assisted traffic monitoring, traffic safety observation, or road-user perception. | Pending final writing |
| The method should benefit the considered transportation system | The paper needs more than mAP: it must report speed, complexity, scale-wise small-object behavior, and qualitative traffic-scene examples. | Partially ready |
| Regular papers have a suggested 10-page IEEE double-column length | The future `main.tex` should be planned as a concise regular paper unless the advisor chooses another article type. | Pending |
| Abstract should be 150-250 words, one paragraph, and self-contained | The current abstract workbench should be rewritten only after final method/results are fixed. | Pending |
| Keywords must include methodology and application categories | Candidate index terms should include computer vision / image processing / artificial intelligence and road transportation / pedestrian flows and crowds / smart cities if appropriate. | Pending |

## Required Narrative Shift

The paper should not be introduced as:

> We improve YOLO for VisDrone.

The T-ITS-ready framing should be closer to:

> UAV-assisted traffic sensing requires compact detectors that can recover dense and small road users under aerial viewpoints. This work studies high-resolution lightweight YOLO variants for traffic-scene small-object detection, with explicit accuracy-efficiency and scale-wise evaluation.

This framing is acceptable only if the final manuscript keeps the transportation use case visible in:

- title,
- abstract,
- introduction motivation,
- dataset description,
- qualitative examples,
- discussion of latency/model size,
- conclusion.

## Section-Level T-ITS Fit Tasks

| Manuscript Section | Must Do | Avoid |
| --- | --- | --- |
| Title | Mention UAV traffic, aerial traffic scenes, or transportation perception if T-ITS remains primary. | A purely generic title such as "Improved YOLO for Object Detection" |
| Abstract | State the transportation sensing problem, method, exact evidence-backed results, and efficiency trade-off. | Claims about SOTA or generalization without UAVDT/TOFC evidence |
| Introduction | Explain why aerial road-user detection is hard: tiny scale, dense instances, occlusion, and deployment limits. | A long generic YOLO history without transportation relevance |
| Related Work | Include UAV traffic perception, small-object detection, feature pyramids, and lightweight YOLO. | Treating unrelated natural-image detectors as direct T-ITS baselines |
| Method | Present the selected architecture as supporting high-resolution road-user detection. | Overclaiming CoordAttention or TOFC before the final audit |
| Experiments | Report VisDrone, UAVDT if available, scale-wise metrics, speed/complexity, and traffic-like qualitative cases. | Mixing validation, test-dev, and literature-only numbers in one ranking table |
| Discussion | Acknowledge YOLO11s capacity advantage and deployment trade-offs. | Pretending a nano model is universally superior |
| Conclusion | Close on evidence-backed traffic-scene small-object findings. | Any claim not mapped to audited tables or run logs |

## Evidence Gates for a T-ITS Submission Attempt

| Gate | Minimum Evidence Needed | Current Evidence |
| --- | --- | --- |
| Traffic-scene relevance | VisDrone traffic-like qualitative examples and UAVDT plan/results | VisDrone ready; UAVDT pending |
| Lightweight deployment | Params, GFLOPs, weight size, latency, FPS for final model and baselines | Ready for completed models; pending final model refresh |
| Small road-user detection | Scale-wise recall/precision and local scale-bin AP for final selected model | Ready for current VisDrone models; pending final model if TOFC is selected |
| Cross-dataset robustness | At least UAVDT baseline and final-method comparison | Pending |
| Method novelty | TOFC or another validated module, or a carefully framed systematic high-resolution study | Pending |
| Claim discipline | Claim audit passes on final-facing files | Pending |

## Practical Decision Rule

Treat T-ITS as the primary target only if at least one of the following becomes true:

1. TOFC or another selected final method improves the lightweight accuracy-efficiency trade-off over YOLO11n-P2-960 with complete evidence.
2. UAVDT confirms that the P2/high-resolution finding transfers to another traffic-UAV dataset.
3. The advisor accepts a more analytical paper whose novelty is the controlled high-resolution lightweight YOLO study plus scale-wise traffic-scene evidence, rather than a new architecture.

If none of these conditions is met, the project should pivot to a less selective English journal or to an IEEE open-access venue with a more engineering-oriented scope.

## Manual Items for Advisor Confirmation

- Confirm whether T-ITS is the exact target or only one possible IEEE Transactions venue.
- Confirm whether the paper should be written as a Regular Paper.
- Confirm whether "UAV-assisted traffic perception" is an acceptable application framing.
- Confirm whether TOFC is worth continuing if it only improves small-object recall/AP but not aggregate mAP.
