#!/usr/bin/env python3
"""
S1-4: Fit GLM to raw fMRI runs → compute z-scored contrast maps.
Uses nilearn's FirstLevelModel for OLS beta estimation.

Pipeline:
  4 BOLD runs (sub-07, MNI305 space)
    → nilearn FirstLevelModel (hrf + derivative, high-pass filter)
    → design matrix + contrasts
    → per-run beta maps (97×115×97 MNI305)
    → z-score across voxels per contrast

Contrast naming follows IBC conventions:
  PreferenceFaces: face > house/body
  ArchiStandard:  basic visual processing
  RSVPLanguage:  sentence > baseline
  ArchiEmotional: emotional > neutral scenes

Output: contrast_maps/sub-07/{task}_contrast.nii.gz (z-scored)
"""

import json, warnings
import numpy as np
import nibabel as nib
from pathlib import Path
from nilearn.glm import first_level

DATA_DIR = Path("/opt/data/projects/tribev2-evaluation/data/raw")
OUT_DIR  = Path("/opt/data/projects/tribev2-evaluation/data/contrast_maps/sub-07")
OUT_DIR.mkdir(parents=True, exist_ok=True)

TR = 2.0  # IBC uses TR=2s

# ── Task definitions ─────────────────────────────────────────────────────────
TASKS = [
    {
        # ses-15: PreferenceFaces — face vs house/body images
        # Events show only 'face' — house is likely the implicit baseline
        "name": "PreferenceFaces",
        "run":  "sub-07/ses-15/func/sub-07_ses-15_task-PreferenceFaces_dir-ap_bold.nii.gz",
        "events": "sub-07/ses-15/func/sub-07_ses-15_task-PreferenceFaces_dir-ap_events.tsv",
        "contrasts": [
            ("face_gt_baseline",    ["face"],            []),
            # house/body implicit in fixation baseline
        ],
    },
    {
        # ses-00: ArchiStandard — checkerboard + simple visual categories
        "name": "ArchiStandard",
        "run":  "sub-07/ses-00/func/sub-07_ses-00_task-ArchiStandard_dir-ap_bold.nii.gz",
        "events": "sub-07/ses-00/func/sub-07_ses-00_task-ArchiStandard_dir-ap_events.tsv",
        "contrasts": [
            ("checkerboard_gt_baseline", ["horizontal_checkerboard", "vertical_checkerboard"], []),
            ("audio_gt_baseline",        ["audio_sentence", "audio_left_hand", "audio_right_hand", "audio_computation"], []),
        ],
    },
    {
        # ses-03: RSVPLanguage — sentence reading vs word/pseudoword
        "name": "RSVPLanguage",
        "run":  "sub-07/ses-03/func/sub-07_ses-03_task-RSVPLanguage_dir-ap_run-03_bold.nii.gz",
        "events": "sub-07/ses-03/func/sub-07_ses-03_task-RSVPLanguage_dir-ap_run-03_events.tsv",
        "contrasts": [
            ("sentence_gt_word",        ["simple_sentence_adj", "simple_sentence_coord", "simple_sentence_cvp"], ["word_list"]),
            ("sentence_complex_vs_pseudo", ["complex_sentence_objclef", "complex_sentence_objrel", "complex_sentence_subjrel", "jabberwocky"], ["pseudoword_list"]),
            ("language_gt_baseline",    ["simple_sentence_adj", "simple_sentence_coord", "simple_sentence_cvp", "complex_sentence_objclef", "complex_sentence_objrel", "complex_sentence_subjrel", "word_list", "consonant_strings", "pseudoword_list"], []),
        ],
    },
    {
        # ses-04: ArchiEmotional — emotional expression vs control
        "name": "ArchiEmotional",
        "run":  "sub-07/ses-04/func/sub-07_ses-04_task-ArchiEmotional_dir-ap_bold.nii.gz",
        "events": "sub-07/ses-04/func/sub-07_ses-04_task-ArchiEmotional_dir-ap_events.tsv",
        "contrasts": [
            ("emotional_face_gt_control", ["face_trusty", "face_gender"], ["face_control"]),
            ("emotional_expr_gt_control", ["expression_intention", "expression_gender"], ["expression_control"]),
        ],
    },
]


def load_events(events_path):
    """Load events TSV, return DataFrame with onset/duration/trial_type."""
    import pandas as pd
    df = pd.read_csv(DATA_DIR / events_path, sep="\t")
    # IBC uses: onset, duration, trial_type
    assert {"onset", "duration", "trial_type"}.issubset(df.columns), \
        f"Missing columns in {events_path}: {list(df.columns)}"
    return df[["onset", "duration", "trial_type"]]


if __name__ == "__main__":
    print("IBC GLM Contrast Estimation")
    print("=" * 60)

    all_contrasts = []
    for task_def in TASKS:
        task_name = task_def["name"]
        print(f"\n[{task_name}]")

        bold_path  = task_def["run"]
        events_df  = load_events(task_def["events"])
        print(f"  Events: {len(events_df)} trials, types: {events_df['trial_type'].unique().tolist()}")

        bold_img   = nib.load(str(DATA_DIR / bold_path))
        n_scans    = bold_img.shape[3]
        frame_times = np.arange(n_scans) * TR
        print(f"  BOLD: shape={bold_img.shape}, TR={TR}s, frames={n_scans}")

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            model = first_level.FirstLevelModel(
                signal_scaling=False,
                minimize_memory=False,
                hrf_model="spm + derivative",
                high_pass=1/128,
                slice_time_ref=0.5,
                t_r=TR,
                noise_model="ols",
            )
            model.fit([bold_img], [events_df])

        # Build contrast matrix
        conditions = sorted(events_df["trial_type"].unique().tolist())
        print(f"  Conditions: {conditions}")

        for contrast_name, pos_conds, neg_conds in task_def["contrasts"]:
            # Build t-contrast vector
            vec = np.zeros(len(conditions))
            for c in pos_conds:
                if c in conditions:
                    vec[conditions.index(c)] = 1
            for c in neg_conds:
                if c in conditions:
                    vec[conditions.index(c)] = -1

            if vec.sum() == 0:
                print(f"  SKIP {contrast_name}: no matching conditions")
                continue

            try:
                # Pass contrast vector (array) as first arg — nilearn uses it directly
                result = model.compute_contrast(vec, stat_type='t', output_type='z_score')
                if isinstance(result, list):
                    z_map = result[0]
                else:
                    z_map = result

                # Save
                out_path = OUT_DIR / f"{task_name}_{contrast_name}_z.nii.gz"
                nib.save(z_map, str(out_path))
                all_contrasts.append(str(out_path))
                print(f"  {contrast_name}: saved ({z_map.shape})")

                # Quick stats
                data = z_map.get_fdata()
                print(f"    z-map: mean={data.mean():.2f}, std={data.std():.2f}, "
                      f"min={data.min():.2f}, max={data.max():.2f}")
            except Exception as e:
                print(f"  FAILED {contrast_name}: {e}")

    print(f"\n{'='*60}")
    print(f"Done. {len(all_contrasts)} contrast maps saved to {OUT_DIR}")
    for c in all_contrasts:
        print(f"  {c}")
