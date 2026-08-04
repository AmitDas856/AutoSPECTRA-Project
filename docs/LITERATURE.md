# Technical Review — literature notes  *(Report Part B · LO1 = 10%, feeds Evaluation = 30%)*

> Real, citable sources for **AutoSPECTRA** (CAN-bus intrusion detection). Each member writes their own Part B prose; these shared facts + citations are the raw material. Export into Zotero (APA) and confirm authors/pages before the report.

## What Part B must show ("concepts at the forefront of the discipline")
1. Why the CAN bus is insecure and why ML beats fixed rules (zero-day attacks).
2. The main detection families: signature, sequence (LSTM/GRU), unsupervised anomaly (autoencoder), and **image-encoded CNN**.
3. How these are benchmarked (Car-Hacking dataset, per-class metrics).

## Source matrix
| # | Theme | Source (year, venue) | Key finding | Use in our report |
|---|-------|----------------------|-------------|-------------------|
| 1 | Dataset/benchmark | **HCRL Car-Hacking Dataset (2018)** — Seo et al., real 2010 Hyundai, 1.3M msgs, 5 attack classes | The standard public CAN-IDS benchmark | Our primary dataset + the baseline everyone compares to |
| 2 | CV / image-CNN | **Rec-CNN (2022), Vehicular Communications** — CNN on recurrence-plot images of CAN IDs | ~0.99 accuracy encoding CAN traffic as images | Justifies our Computer-Vision layer (Block 2) |
| 3 | CNN IDS | In-vehicle network intrusion detection using deep CNN (2019/2021), Vehicular Communications | CNN on CAN frames detects DoS/fuzzy/spoof at high accuracy | Core method evidence |
| 4 | Survey | **A survey of deep-learning-based IDS in automotive applications (2023), Expert Systems w/ Applications** | Maps the whole DL-CAN-IDS field | Breadth cite; positions our approach |
| 5 | Survey (in-vehicle) | Özdemir et al., A Survey of Anomaly Detection in In-Vehicle Networks (2024), arXiv:2409.07505 | CAN is the most-studied component; security + safety | Shared with my RSC review — frames the data source |
| 6 | Sequence model | LSTM/GRU on Car-Hacking — "Securing the CAN bus using deep learning" (2025), Scientific Reports | LSTM ~0.999 accuracy on the dataset | Our sequence-model comparison + a target to benchmark against |
| 7 | Supervised vs semi-supervised | Comparative Study: Supervised vs Semi-supervised ML for In-vehicle CAN (2022), arXiv:2207.10286 | Labelled vs unlabelled trade-offs | Justifies our supervised baseline + anomaly comparison |
| 8 | Alt. dataset | ROAD dataset (2020), arXiv:2012.14600 | A more realistic CAN-IDS dataset + critique of older ones | Cross-check / future work; shows we know the data's limits |
| 9 | Explainability | VAE-based KD meets Explainable AI for in-vehicle IDS (2024), arXiv:2410.09043 | Lightweight + explainable detection | Future-work + ethics (why a flag fired) |

## Narrative skeleton (turn into prose)
- **Problem:** CAN broadcasts unauthenticated frames; injection/spoofing attacks are demonstrated and safety-critical.
- **Rules vs ML:** signature rules miss novel attacks; learned models generalise.
- **Three method families:** sequence models (LSTM/GRU), unsupervised anomaly (autoencoder), and **image-encoded CNNs** (recurrence/grid) — the last is our headline and the CV component.
- **Evaluation norm:** the Car-Hacking dataset with per-class precision/recall/F1; published results sit at ~0.99, so our numbers are directly comparable (and we must discuss *why* near-perfect scores can be misleading — single vehicle, easy attacks).

## Verify-before-citing
Titles/venues/years above are from live search and are real; confirm authors, exact venues and DOIs in Zotero before the APA list. Never hand-type citations.

## Gap for Gemini / a teammate
Expand each row into 2–3 sentences of critical prose and add 3–4 more 2024–2026 CAN-IDS papers (especially transformer-based and cross-dataset generalisation). Reuse the Gemini prompt in `GEMINI-PROMPT.md` (swap the project context to AutoSPECTRA).
