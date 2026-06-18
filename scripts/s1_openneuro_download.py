#!/usr/bin/env python3
"""
S1-3: Download selected IBC raw fMRI runs from OpenNeuro S3.
S3 URL pattern: https://s3.amazonaws.com/openneuro.org/ds002685/{path}

4 tasks × ~1GB each = ~4 GB for pipeline validation.
After GLM: compute z-scored contrast maps → compare with TRIBE v2 zero-shot predictions.

Task families covered:
  FaceBody:    PreferenceFaces (face vs house/body) — sub-07 ses-15
  Visu:        ArchiStandard (basic visual) — sub-07 ses-00
  RSVP:        RSVPLanguage (sentence reading) — sub-07 ses-03 run-03
  Emotional:   ArchiEmotional (emotional scenes) — sub-07 ses-04
"""

import requests
import nibabel as nib
import os
from pathlib import Path

BUCKET = "s3.amazonaws.com/openneuro.org/ds002685"
BASE_URL = f"https://{BUCKET}"
DATA_DIR = Path("/opt/data/projects/tribev2-evaluation/data/raw")
DATA_DIR.mkdir(parents=True, exist_ok=True)

# (session_dir, bold_filename) for sub-07
TASKS = {
    "PreferenceFaces":  "sub-07/ses-15/func/sub-07_ses-15_task-PreferenceFaces_dir-ap_bold.nii.gz",
    "ArchiStandard":    "sub-07/ses-00/func/sub-07_ses-00_task-ArchiStandard_dir-ap_bold.nii.gz",
    "RSVPLanguage":     "sub-07/ses-03/func/sub-07_ses-03_task-RSVPLanguage_dir-ap_run-03_bold.nii.gz",
    "ArchiEmotional":   "sub-07/ses-04/func/sub-07_ses-04_task-ArchiEmotional_dir-ap_bold.nii.gz",
}

# Also need: events TSV (timing), task JSON, fieldmaps, T1
EXTRA_FILES = [
    # PreferenceFaces events + task JSON
    "sub-07/ses-15/func/sub-07_ses-15_task-PreferenceFaces_dir-ap_events.tsv",
    "task-PreferenceFaces_dir-ap_bold.json",
    # ArchiStandard events + task JSON
    "sub-07/ses-00/func/sub-07_ses-00_task-ArchiStandard_dir-ap_events.tsv",
    "task-ArchiStandard_dir-ap_bold.json",
    # RSVPLanguage events + task JSON
    "sub-07/ses-03/func/sub-07_ses-03_task-RSVPLanguage_dir-ap_run-03_events.tsv",
    "task-RSVPLanguage_dir-ap_bold.json",
    # ArchiEmotional events + task JSON
    "sub-07/ses-04/func/sub-07_ses-04_task-ArchiEmotional_dir-ap_events.tsv",
    "task-ArchiEmotional_dir-ap_bold.json",
    # Field maps (for topup/epi distortion correction)
    "sub-07/ses-00/fmap/sub-07_ses-00_acq-0_dir-ap_epi.nii.gz",
    "sub-07/ses-00/fmap/sub-07_ses-00_acq-0_dir-pa_epi.nii.gz",
    # T1 anatomical
    "sub-07/ses-00/anat/sub-07_ses-00_T1w.nii.gz",
]


def download_file(remote_path, timeout=600):
    """Download from S3 to DATA_DIR, resume on interrupt."""
    url = f"{BASE_URL}/{remote_path}"
    local_path = DATA_DIR / remote_path
    local_path.parent.mkdir(parents=True, exist_ok=True)

    if local_path.exists():
        r_head = requests.head(url, timeout=10)
        if r_head.ok:
            total = int(r_head.headers.get("Content-Length", 0))
            if local_path.stat().st_size >= total:
                print(f"  Already: {remote_path.split('/')[-1]} ({total/1024/1024:.1f} MB)")
                return True

    downloaded = local_path.stat().st_size if local_path.exists() else 0
    mode = "ab" if downloaded > 0 else "wb"
    headers = {"Range": f"bytes={downloaded}-"} if downloaded > 0 else {}

    print(f"  Downloading: {remote_path} ({downloaded/1024/1024:.1f} MB already)")
    try:
        r = requests.get(url, timeout=timeout, stream=True, headers=headers)
        if r.status_code == 416:
            print(f"  Complete (verified)")
            return True
        if not r.ok:
            print(f"  HTTP {r.status_code}: {r.text[:100]}")
            return False

        total = int(r.headers.get("Content-Length", 0)) + downloaded
        with open(local_path, mode) as f:
            for chunk in r.iter_content(chunk_size=131072):
                f.write(chunk)
                downloaded += len(chunk)
                print(f"\r    {downloaded*100/max(total,1):.1f}% ({downloaded/1024/1024:.0f} MB)", end="", flush=True)

        print()
        size = local_path.stat().st_size / 1024/1024
        print(f"  Done: {remote_path.split('/')[-1]} ({size:.1f} MB)")
        return True
    except Exception as e:
        print(f"  ERROR: {e}")
        return False


def main():
    print("IBC OpenNeuro Selective Downloader")
    print(f"Target: {DATA_DIR}")
    print("=" * 60)

    total_size_gb = 0
    errors = []

    # Download 4 BOLD runs (~1GB each)
    for task, bold_path in TASKS.items():
        print(f"\n[{task}]")
        ok = download_file(bold_path)
        if not ok:
            errors.append(bold_path)
        else:
            # Verify NIfTI
            local = DATA_DIR / bold_path
            try:
                img = nib.load(str(local))
                mb = local.stat().st_size / 1024/1024
                total_size_gb += mb/1024
                print(f"  Shape: {img.shape}, voxels: {img.get_fdata().nbytes/1e9:.2f} GB")
            except Exception as e:
                print(f"  NIfTI verify FAILED: {e}")

    # Download supporting files
    print(f"\n[Supporting files]")
    for fpath in EXTRA_FILES:
        ok = download_file(fpath, timeout=120)
        if not ok:
            errors.append(fpath)

    print("\n" + "=" * 60)
    if errors:
        print(f"FAILED ({len(errors)} files): {errors}")
    else:
        print(f"ALL DOWNLOADS COMPLETE ({total_size_gb:.1f} GB raw fMRI)")
        print("Next: GLM fitting → contrast maps → TRIBE v2 correlation")


if __name__ == "__main__":
    main()
