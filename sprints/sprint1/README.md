# Sprint 1: Environment + Data Acquisition

**Goal:** Clone TRIBE v2 repo, download model weights, get IBC raw fMRI from OpenNeuro S3.

## Completed

- [x] S1-1: Clone `facebookresearch/tribev2`, install in polyblock venv (torch 2.12.1+cu130, sm_120 RTX 5080 compatible)
- [x] S1-2: Download `facebook/tribev2` model weights from HuggingFace (676 MB `best.ckpt`) → `environment/models/tribev2/`
- [x] S1-3: Download IBC raw fMRI from OpenNeuro S3 (4 tasks × ~1 GB, sub-07)

## In Progress

### S1-3: Download IBC raw fMRI from OpenNeuro S3

**Status:** Running in background (~4 GB total)

**S3 URL pattern:** `https://s3.amazonaws.com/openneuro.org/ds002685/{path}`

**Files being downloaded:**
- `sub-07/ses-15/task-PreferenceFaces` (FaceBody family)
- `sub-07/ses-00/task-ArchiStandard` (Visu family)
- `sub-07/ses-03/task-RSVPLanguage` (RSVP Language family)
- `sub-07/ses-04/task-ArchiEmotional` (Emotional family)
- Supporting: events TSV, task JSON, fieldmaps (AP/PA epi), T1w

**Why sub-07?** Randomly chosen from 12 available subjects. Pipeline works with any subject.

### S1-4: Compute GLM contrast maps
After raw download → nilearn `FirstLevelModel` GLM fitting → z-scored contrast maps.

### S1-5: Parcellation
Using Schaefer 100/200 (downloaded from OSF) instead of Glasser 360 (NITRC blocked).

### S1-6: Backlog for S2–S4

---

## Network access situation (documented for reproducibility)

| Host | Status | Notes |
|------|--------|-------|
| github.com | ✓ | All repos accessible |
| huggingface.co | ✓ | Model weights, datasets |
| nitrc.org (web) | ✓ | Directory listing only |
| osf.io | ✓ | Figshare/OSF mirrors |
| openneuro.org | ✓ | S3 bucket: `s3.amazonaws.com/openneuro.org/ds002685` |
| api.neurovault.org | ✗ | DNS resolution fails |
| ebrains.eu | ✗ | EBRAINS auth required |
| nitrc.org (files) | ✗ | Session cookie required |
| figshare.com | ✗ | SSL cert mismatch |

## Model info

**TRIBE v2** (`facebook/tribev2`):
- 3 encoders: DINOv2-L (video) + w2v-bert-2.0 (audio) + Llama-3.2-3B (text) → concat → Transformer → fMRI
- **20484 vertices** (fsaverage5 surface space)
- **25 subjects** across 4 datasets (IBC, HCP, BBC, MBC)
- Zero-shot: `average_subjects=True` → bypass per-subject linear layers
- Contrast: outputs (n_samples, 20484) in fsaverage5 space

**IBC data** (OpenNeuro ds002685):
- 12 subjects, 47 tasks, MNI305 space (2mm isotropic, 97×115×97)
- Raw BIDS fMRI — need GLM fitting to get contrast maps

## Pipeline after Sprint 1

```
Raw fMRI (MNI305)
  → nilearn FirstLevelModel GLM → z-scored contrast maps (97×115×97)
  → TRIBE v2 zero-shot → vertex predictions (20484, fsaverage5)
  → Project TRIBE: fsaverage5 → MNI305
  → Correlate: TRIBE predictions vs GLM contrasts
  → Per-contrast Pearson r → R_tribe vs R_group, R_subject
```
