# Week 4 Artifact Export and GitHub Evidence

**Owner:** Miftha Thahniyath  
**Role:** Artifact and GitHub Evidence Lead

## Kaggle Output Structure

```text
/kaggle/working/autospectra_week04_outputs/
├── models/
├── plots/
└── reports/
```

## Download Packages

```text
/kaggle/working/AutoSPECTRA_Week04_Images.zip
/kaggle/working/AutoSPECTRA_Week04_Evidence.zip
```

The image ZIP contains only PNG figures.

The evidence ZIP contains:

- PNG figures;
- model-comparison CSV;
- per-class metrics CSV;
- feature-importance CSV;
- image manifest;
- prediction-shape audit;
- Week 4 JSON summary.

Trained `.joblib` files are deliberately excluded from the evidence ZIP.

## GitHub Recommendation

Commit the notebook, small CSV/JSON reports and selected PNG figures. Keep raw HCRL data and large generated model binaries outside GitHub.
