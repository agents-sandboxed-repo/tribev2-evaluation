#!/usr/bin/env python3
"""
S1-3 / S1-4: Download IBC contrast maps via ibc_api.
Downloads per-subject MNI305 volumetric z-scored GLM contrast maps
for the 4 task families, then computes group-average maps.
"""
import ibc_api.utils as ibc
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

# ── Output directory ──────────────────────────────────────────────────────────
OUT = Path("/opt/data/projects/tribev2-evaluation/data/ibc_contrast_maps")
OUT.mkdir(parents=True, exist_ok=True)

# ── Task-family → IBC task + contrast mapping ──────────────────────────────────
# Each entry: (ibc_task, contrast_pattern, display_name)
TASK_CONTRASTS = {
    "FaceBody": {
        "task": "PreferenceFaces",
        "contrasts": ["face_constant", "face_linear", "face_quadratic"],
    },
    "Visu": {
        "task": "HcpEmotion",
        "contrasts": ["face", "shape"],   # face vs. shape = visual category contrast
    },
    "RSVP": {
        "task": "RSVPLanguage",
        "contrasts": ["complex-simple", "complex", "jabberwocky-consonant_string"],
    },
    "EmotionalPain": {
        "task": "EmotionalPain",
        "contrasts": ["emotional_pain", "physical_pain"],
    },
}

# All subjects available in IBC
ALL_SUBJECTS = ["01", "02", "04", "05", "06", "07", "08", "09", "11", "12", "13", "14", "15"]

def get_db():
    """Fetch the full volume_maps catalogue."""
    print("Fetching IBC volume_maps catalogue...")
    return ibc.get_info(data_type="volume_maps")

def download_task_contrasts(db, task_key: str, subjects: list) -> dict:
    """Download all contrast maps for a given task family."""
    cfg = TASK_CONTRASTS[task_key]
    ibc_task = cfg["task"]
    contrasts = cfg["contrasts"]

    print(f"\n{'='*60}")
    print(f"Task family: {task_key} (IBC task: {ibc_task})")
    print(f"Contrasts: {contrasts}")
    print(f"Subjects: {subjects}")

    downloaded = {}
    for contrast in contrasts:
        # Filter DB
        # Filter by subject + task (contrast filter done manually)
        filtered = ibc.filter_data(
            db,
            subject_list=subjects,
            task_list=[ibc_task],
        )
        # Further filter by contrast
        filtered = filtered[filtered["contrast"].isin([contrast])]
        if len(filtered) == 0:
            print(f"  [WARN] No entries for contrast={contrast}, task={ibc_task}")
            continue

        print(f"  Downloading contrast={contrast} ({len(filtered)} files)...")
        result = ibc.download_data(
            filtered,
            save_to=str(OUT / task_key),
        )
        # result is a DataFrame with local paths
        downloaded[contrast] = result
        print(f"  → {len(result)} files saved to {OUT / task_key}")

    return downloaded

def main():
    db = get_db()
    all_downloaded = {}

    for task_key in TASK_CONTRASTS:
        downloaded = download_task_contrasts(db, task_key, ALL_SUBJECTS)
        all_downloaded[task_key] = downloaded

    # Print summary
    print(f"\n{'='*60}")
    print("DOWNLOAD SUMMARY")
    print(f"Output: {OUT}")
    for task_key, contrasts in all_downloaded.items():
        for contrast, df in contrasts.items():
            print(f"  {task_key}/{contrast}: {len(df)} subject files")
    print("\nDone! Next step: S1-5 (parcellate with Glasser 360 atlas).")

if __name__ == "__main__":
    main()
