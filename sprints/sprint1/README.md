# TRIBE v2 Evaluation — Sprint 1 Plan

**Goal:** Set up environment, download TRIBE v2 model + IBC contrast maps, parcellate with Glasser 360 atlas.

**Duration:** Sprint 1

---

## Step 1 — TRIBE v2 Setup

### S1-1: Clone TRIBE v2 repo + environment
- Clone https://github.com/facebookresearch/tribev2
- Follow README for environment setup
- Verify: `import tribev2` in Python works

### S1-2: Download TRIBE v2 model weights
- From https://huggingface.co/facebook/tribev2
- Verify: unseen-subject linear layer loads, check dimensions

---

## Step 2 — IBC Data Acquisition + Parcellation

### S1-3: Download IBC contrast maps
- Use `ibc_api` package or EBRAINS direct access
- Download z-scored GLM contrast maps for all 4 task families:
  - **FaceBody** (faces, places, body parts, characters, tools)
  - **Visu** (visual categories)
  - **RSVP** (sentences vs. word lists)
  - **EmotionalPain** (emotional vs. physical pain)
- Download for **all available subjects** in MNI volumetric space

### S1-4: Download IBC group-average contrast maps
- Corresponding group-average maps for each task family
- These are the reference for R_tribe_vs_group

### S1-5: Parcellate with Glasser 360 atlas
- Download Glasser 360 parcellation (MNI space, 360 parcels)
- Parcellate all per-subject and group-average contrast maps
- Output: numpy array shape (360,) per subject per contrast
- Store in structured directory: `data/parcellated/{task}/{contrast}/{subject}.npy`

---

## Task Families & Contrasts

| Task Family | Contrast | Modality |
|---|---|---|
| FaceBody | faces vs. fixation | visual |
| FaceBody | places vs. fixation | visual |
| FaceBody | body parts vs. fixation | visual |
| FaceBody | characters vs. fixation | visual |
| FaceBody | tools vs. fixation | visual |
| Visu | (visual categories) | visual |
| RSVP | sentences vs. word lists | language |
| RSVP | complex vs. simple sentences | language |
| EmotionalPain | emotional vs. physical pain | language |

*Exact contrast names to be confirmed from IBC dataset documentation.*

---

## Directory Structure

```
tribev2-evaluation/
├── environment/
│   ├── tribev2/          # cloned repo
│   └── models/           # downloaded weights (facebook/tribev2)
├── data/
│   ├── raw/
│   │   ├── ibc/         # raw IBC contrast maps (MNI volumina)
│   │   ├── glasser/     # Glasser 360 atlas files
│   │   └── ibc_group/  # group-average maps
│   └── parcellated/
│       └── {task}/
│           └── {contrast}/
│               ├── sub-01.npy  (360,)
│               ├── sub-02.npy  (360,)
│               └── group_avg.npy  (360,)
├── sprints/
│   ├── sprint1/
│   │   ├── README.md   # this file
│   │   └── setup.py    # environment setup script
│   ├── sprint2/  (stimuli)
│   ├── sprint3/  (TRIBE runs)
│   └── sprint4/  (correlation analysis)
└── README.md
```

---

## Definition of Done

- [ ] `import tribev2` works in Python
- [ ] TRIBE v2 model loads from HuggingFace
- [ ] All available IBC subjects' contrast maps downloaded for all 4 task families
- [ ] Group-average contrast maps downloaded for all task families
- [ ] Glasser 360 atlas acquired
- [ ] All contrast maps parcellated → (N_subjects × 360) numpy arrays on disk
- [ ] README.md updated with exact paths and download commands used
- [ ] All code committed to GitHub org
