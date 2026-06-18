#!/usr/bin/env python3
"""Populate Sprint 1 tasks into the TRIBEv2 Evaluation Kanban board."""
import sqlite3, datetime

db = '/opt/data/kanban/boards/tribev2-evaluation/kanban.db'
conn = sqlite3.connect(db)

# Get list IDs
lists = {row[1]: row[0] for row in conn.execute('SELECT id, title FROM lists WHERE board_id=1').fetchall()}
backlog_id = lists['Backlog']
in_progress_id = lists['In Progress']

tasks = [
    # (title, description, labels, list_id, position)
    (
        "S1-1: Clone TRIBE v2 repo + setup environment",
        "Clone https://github.com/facebookresearch/tribev2. Follow README for env setup (Python, torch, etc.). Verify installation by checking 'import tribev2' works in Python.",
        "sprint1,setup",
        backlog_id, 0
    ),
    (
        "S1-2: Download TRIBE v2 model weights from HuggingFace",
        "Download from https://huggingface.co/facebook/tribev2. Verify model loads correctly: load the unseen-subject linear layer weights and confirm dimensions.",
        "sprint1,setup,weights",
        backlog_id, 1
    ),
    (
        "S1-3: Download IBC contrast maps via ibc_api",
        "Use ibc_api package or EBRAINS repository to download pre-computed z-scored GLM contrast maps for all 4 task families: FaceBody, Visu, RSVP, EmotionalPain. Download all available subjects in MNI volumetric space.",
        "sprint1,data,IBC",
        backlog_id, 2
    ),
    (
        "S1-4: Download IBC group-average contrast maps",
        "Download the corresponding group-average contrast maps for all 4 task families. These serve as the reference for R_tribe_vs_group.",
        "sprint1,data,IBC",
        backlog_id, 3
    ),
    (
        "S1-5: Parcellate contrast maps with Glasser's 360 atlas",
        "Download the Glasser 360 parcellation atlas (MNI space). Parcellate all per-subject and group-average contrast maps using this atlas, yielding vectors of length 360 per subject per contrast. Store as numpy arrays.",
        "sprint1,data,parcellation",
        backlog_id, 4
    ),
    (
        "S1-6: Populate Backlog with S2–S4 task descriptions",
        "Add task cards for Sprints 2, 3, and 4 to the Backlog: S2 (stimuli acquisition for FaceBody/Visu/RSVP/EmotionalPain), S3 (TRIBE v2 unseen-subject runs + GLM), S4 (correlation computation + figures).",
        "planning",
        backlog_id, 5
    ),
]

for title, desc, labels, list_id, pos in tasks:
    conn.execute(
        'INSERT INTO cards (list_id, title, description, labels, position) VALUES (?, ?, ?, ?, ?)',
        (list_id, title, desc, labels, pos)
    )

conn.commit()
print(f"Inserted {len(tasks)} Sprint 1 tasks into kanban board.")
conn.close()
