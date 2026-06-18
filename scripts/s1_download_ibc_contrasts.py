#!/usr/bin/env python3
"""
S1-3 / S1-4: Download IBC contrast maps via ibc_api.
Downloads per-subject MNI305 volumetric z-scored GLM contrast maps
for the 4 task families, then computes group-average maps.

Uses direct ebrains_drive API to bypass ibc_api's broken device-flow auth.
"""
import os
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

# Load EBRAINS token
TOKEN_FILE = Path("/opt/data/home/.ebrains_token")
token = TOKEN_FILE.read_text().strip() if TOKEN_FILE.exists() else None
if not token:
    raise RuntimeError("No EBRAINS token found at /opt/data/home/.ebrains_token")
print(f"[Auth] Token loaded from {TOKEN_FILE}")

import ibc_api.utils as ibc
import pandas as pd
from ebrains_drive import BucketApiClient
from tqdm import tqdm

OUT = Path("/opt/data/projects/tribev2-evaluation/data/ibc_contrast_maps")
OUT.mkdir(parents=True, exist_ok=True)

TASK_CONTRASTS = {
    "FaceBody": {
        "task": "PreferenceFaces",
        "contrasts": ["face_constant", "face_linear", "face_quadratic"],
    },
    "Visu": {
        "task": "HcpEmotion",
        "contrasts": ["face", "shape"],
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

ALL_SUBJECTS = ["01", "02", "04", "05", "06", "07", "08", "09", "11", "12", "13", "14", "15"]

# ── Direct downloader using BucketApiClient ──────────────────────────────────

def get_bucket(token: str):
    """Create a BucketApiClient and get the volume_maps dataset bucket."""
    client = BucketApiClient(token=token)
    # Get the dataset id from ibc_api's metadata
    db_info = ibc.get_info(data_type="volume_maps")
    # The dataset_id is not directly exposed, but we can find it from metadata
    import ibc_api.metadata as md
    metadata = md.fetch_metadata()
    dataset = metadata["volume_maps"][0]
    dataset_id = dataset["id"]
    print(f"[Bucket] dataset_id = {dataset_id}")
    bucket = client.buckets.get_dataset(dataset_id, request_access=True)
    return bucket

def download_files(df: pd.DataFrame, bucket, save_dir: Path, label: str):
    """Download all files in a filtered dataframe using bucket.get_file()."""
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)
    
    # Get src/dst file paths
    src_files, dst_files = ibc.get_file_paths(df, save_to_dir=str(save_dir))
    
    failed = []
    for src, dst in tqdm(zip(src_files, dst_files), total=len(src_files), desc=label):
        dst_path = Path(dst)
        if dst_path.exists():
            continue
        try:
            f = bucket.get_file(src)
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            dst_path.write_bytes(f.get_content())
        except Exception as e:
            tqdm.write(f"ERROR: {src}: {e}")
            failed.append(src)
    
    if failed:
        print(f"  Warning: {len(failed)}/{len(src_files)} files failed")
    return len(src_files) - len(failed)

# ── Main ────────────────────────────────────────────────────────────────────

def main():
    db = ibc.get_info(data_type="volume_maps")
    print(f"Loaded catalogue: {len(db)} entries")
    
    bucket = get_bucket(token)
    
    all_downloaded = {}
    for task_key, cfg in TASK_CONTRASTS.items():
        task_name = cfg["task"]
        contrasts = cfg["contrasts"]
        
        print(f"\n{'='*60}")
        print(f"Task family: {task_key} (IBC task: {task_name})")
        print(f"Contrasts: {contrasts}")
        print(f"Subjects: {ALL_SUBJECTS}")
        
        downloaded = {}
        for contrast in contrasts:
            filtered = ibc.filter_data(db, subject_list=ALL_SUBJECTS, task_list=[task_name])
            filtered = filtered[filtered["contrast"].isin([contrast])]
            if len(filtered) == 0:
                print(f"  [WARN] No entries for contrast={contrast}, task={task_name}")
                continue
            
            n = download_files(filtered, bucket, OUT / task_key, f"{task_key}/{contrast}")
            downloaded[contrast] = n
            print(f"  → {n} files saved to {OUT / task_key}")
        
        all_downloaded[task_key] = downloaded
    
    print(f"\n{'='*60}")
    print("DOWNLOAD SUMMARY")
    print(f"Output: {OUT}")
    for task_key, contrasts in all_downloaded.items():
        for contrast, n in contrasts.items():
            print(f"  {task_key}/{contrast}: {n} files")
    print("\nDone! Next step: S1-5 (parcellate with Glasser 360 atlas).")

if __name__ == "__main__":
    main()
