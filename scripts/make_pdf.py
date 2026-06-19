#!/usr/bin/env python3
"""Build Sprint 1 PDF report for TRIBE v2 Evaluation."""
import warnings
warnings.filterwarnings('ignore')
import os
os.chdir("/opt/data/projects/tribev2-evaluation")

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image, Table,
                                 TableStyle, PageBreak, HRFlowable)
from reportlab.lib.colors import HexColor

W, H = A4
MARGIN = 2.2 * cm

DARK_BLUE  = HexColor('#1a3a5c')
MID_BLUE   = HexColor('#2e6da4')
LIGHT_BLUE = HexColor('#d0e4f5')
ACCENT     = HexColor('#e8a020')
GRAY       = HexColor('#666666')
LIGHT_GRAY = HexColor('#f5f5f5')
WHITE      = colors.white

doc = SimpleDocTemplate(
    "figures/SPRINT1_REPORT.pdf",
    pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=2.5*cm, bottomMargin=2.5*cm,
    title="TRIBE v2 Evaluation — Sprint 1 Report",
    author="Hermes Agent",
)

styles = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, parent=styles['Normal'], **kw)

title_style   = S('Title2', fontSize=22, textColor=DARK_BLUE, leading=28, spaceAfter=6,
                   alignment=TA_CENTER, fontName='Helvetica-Bold')
subtitle_style = S('Subtitle2', fontSize=12, textColor=MID_BLUE, spaceAfter=4,
                   alignment=TA_CENTER, fontName='Helvetica')
h1_style  = S('H1x', fontSize=14, textColor=DARK_BLUE, spaceBefore=16, spaceAfter=6,
               fontName='Helvetica-Bold')
h2_style  = S('H2x', fontSize=11, textColor=MID_BLUE, spaceBefore=10, spaceAfter=4,
               fontName='Helvetica-Bold')
body_style = S('Body2', fontSize=9.5, leading=14, spaceAfter=4,
               alignment=TA_JUSTIFY, fontName='Helvetica')
bullet_style = S('Bullet2', fontSize=9.5, leading=13, spaceAfter=2,
                 fontName='Helvetica', leftIndent=14, bulletIndent=4)
caption_style = S('Caption2', fontSize=8, textColor=GRAY, spaceAfter=6,
                  alignment=TA_CENTER, fontName='Helvetica-Oblique')
footer_style = S('Footer2', fontSize=7.5, textColor=GRAY, alignment=TA_CENTER,
                 fontName='Helvetica')
warn_style = S('Warn', fontSize=9, leading=13, textColor=HexColor('#8B0000'),
               fontName='Helvetica', leftIndent=8)
exec_style = S('Exec', fontSize=9.5, leading=14, alignment=TA_JUSTIFY)

def HR():
    return HRFlowable(width="100%", thickness=0.5, color=MID_BLUE, spaceAfter=6, spaceBefore=2)

def section(title, content):
    return [Paragraph(title, h1_style), HR(), *content, Spacer(1, 8)]

def subsection(title, content):
    return [Paragraph(title, h2_style), *content]

def bullet(txt):
    return Paragraph(txt, bullet_style)

def img(path, w_cm=16, h_cm=None):
    h = (h_cm or w_cm) * cm
    w = w_cm * cm
    return Image(path, width=w, height=h)

# ── palette helper ────────────────────────────────────────────────────────────
def ts(data, header_bg=DARK_BLUE, alternating=(LIGHT_GRAY, WHITE)):
    """Short-cut TableStyle with alternating rows."""
    nrows = len(data)
    style = [
        ('BACKGROUND', (0,0), (-1,0), header_bg),
        ('TEXTCOLOR',  (0,0), (-1,0), WHITE),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,-1), 8.5),
        ('GRID',       (0,0), (-1,-1), 0.3, HexColor('#cccccc')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
    ]
    for i in range(1, nrows):
        bg = alternating[i % 2]
        style.append(('BACKGROUND', (0,i), (-1,i), bg))
    return TableStyle(style)

# ── colour label cell ────────────────────────────────────────────────────────
GREEN = HexColor('#2e7d32')

story = []

# ══════════════════════════════════════════════════════════════════════════════
# COVER
# ══════════════════════════════════════════════════════════════════════════════
story += [
    Spacer(1, 2*cm),
    Paragraph("TRIBE v2 Evaluation", title_style),
    Paragraph("Sprint 1 — IBC Data Acquisition &amp; Parcellation", subtitle_style),
    Spacer(1, 0.3*cm),
    Table(
        [
            ["Project",        "TRIBE v2 Validation"],
            ["Repository",     "github.com/agents-sandboxed-repo/tribev2-evaluation"],
            ["Sprint",         "Sprint 1: Data Infrastructure"],
            ["Date",           "June 2026"],
            ["Status",         "S1-3 ✓  S1-4 ✓  S1-5 ✓  S1-6 ✓"],
        ],
        colWidths=[4.5*cm, 11.5*cm],
        style=TableStyle([
            ('BACKGROUND', (0,0), (0,-1), LIGHT_BLUE),
            ('TEXTCOLOR', (0,0), (0,-1), DARK_BLUE),
            ('FONTNAME',  (0,0), (0,-1), 'Helvetica-Bold'),
            ('FONTSIZE',  (0,0), (-1,-1), 9.5),
            ('ROWBACKGROUNDS', (1,0), (1,-1), [LIGHT_GRAY, WHITE]),
            ('GRID', (0,0), (-1,-1), 0.3, HexColor('#cccccc')),
            ('TOPPADDING',    (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ])
    ),
    Spacer(1, 1.5*cm),
    Paragraph(
        "<b>Executive Summary</b><br/>"
        "Sprint 1 established the data infrastructure for the TRIBE v2 encoding model validation. "
        "Eight contrast z-maps from four IBC task families were acquired for subject sub-07, "
        "parcellated into 384 Schaefer 400 parcels, and the full IBC catalogue (57,938 entries) "
        "was documented. The EBRAINS DataProxy bucket was found to be unreachable from this "
        "server; 14 downstream tasks (S2–S4) remain in the backlog pending bucket access or "
        "local data transfer.",
        exec_style
    ),
    Spacer(1, 1*cm),
    Paragraph(
        "Prepared by Hermes Agent (automated) · ollama-cloud · minimax-m2.7",
        S('attrib', fontSize=8, textColor=GRAY, alignment=TA_CENTER)
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 1. CONTEXT
# ══════════════════════════════════════════════════════════════════════════════
story += section("1. Project Context &amp; Goals", [
    Paragraph(
        "TRIBE v2 (facebook/tribev2) is a large-scale encoding model trained on diverse "
        "neuroimaging datasets including IBC (Interstellar Brain Collective). This evaluation "
        "assesses how well TRIBE v2 predicts brain responses to novel stimuli not seen during "
        "training — specifically IBC contrast maps from four task families: "
        "<b>ArchiEmotional</b>, <b>ArchiStandard</b>, <b>PreferenceFaces</b>, and "
        "<b>RSVPLanguage</b>.",
        body_style
    ),
    Paragraph("The validation pipeline spans four sprints:", body_style),
    bullet("<b>Sprint 1 (S1)</b>: Data acquisition + parcellation  ←  this sprint"),
    bullet("<b>Sprint 2 (S2)</b>: Stimulus acquisition for each task family"),
    bullet("<b>Sprint 3 (S3)</b>: TRIBE v2 inference + GLM analysis"),
    bullet("<b>Sprint 4 (S4)</b>: Correlation metrics + publication figures"),
    Spacer(1, 6),
    Paragraph("Primary research questions:", body_style),
    bullet("R<sub>tribe_vs_group</sub>: How well does TRIBE v2 match the IBC group-average response?"),
    bullet("R<sub>tribe_vs_subject</sub>: How well does TRIBE v2 predict individual subject responses?"),
    bullet("Which task domains show the highest model–brain alignment?"),
    bullet("Where does TRIBE v2 fail, and what does that reveal about model limitations?"),
])

# ══════════════════════════════════════════════════════════════════════════════
# 2. DATA
# ══════════════════════════════════════════════════════════════════════════════
story += section("2. Data Sources &amp; Inventory", [
    Paragraph(
        "Two data sources were targeted: (1) the EBRAINS DataProxy bucket for "
        "pre-computed contrast maps, and (2) the OpenNeuro archive for raw BOLD runs. "
        "Only the OpenNeuro raw runs were successfully downloaded.",
        body_style
    ),
    subsection("2.1 IBC Contrast Maps — Catalogue (S1-3)", [
        Paragraph(
            "The <b>ibc_api</b> Python package (v0.0.1) was used to query the EBRAINS "
            "Knowledge Graph and retrieve the full IBC volume map catalogue. Authentication "
            "uses a cached token at <mono>~/.ebrains_token</mono>.",
            body_style
        ),
        Table(
            [
                ["Property",         "Value"],
                ["Catalogue entries", "57,938"],
                ["Subjects",          "13 (sub-01 to 05, 07, 09–15)"],
                ["Tasks",            "HcpWm · HcpEmotion · HcpSocial · HcpMotor · HcpLanguage · ArchiStandard · ArchiEmotional · PreferenceFaces · RSVPLanguage · EmotionalPain"],
                ["Space",            "MNI152NLin2009cAsym (1.5 mm isotropic)"],
                ["Format",           "NIfTI (.nii.gz)"],
                ["Bucket",           "data-proxy.ebrains.eu — BLOCKED (timeout)"],
                ["IAM",             "iam.ebrains.eu — reachable"],
                ["Catalogue CSV",   "ibc_data/available_volume_maps.csv ✓"],
            ],
            colWidths=[4.5*cm, 11.5*cm],
            style=TableStyle([
                ('BACKGROUND', (0,0), (-1,0), DARK_BLUE),
                ('TEXTCOLOR',  (0,0), (-1,0), WHITE),
                ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE',   (0,0), (-1,-1), 8.5),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT_GRAY, WHITE]),
                ('GRID',       (0,0), (-1,-1), 0.3, HexColor('#cccccc')),
                ('TOPPADDING',    (0,0), (-1,-1), 4),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                ('LEFTPADDING',   (0,0), (-1,-1), 6),
                ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
            ])
        ),
        Spacer(1, 6),
        Table(
            [[
                Paragraph(
                    "<b>⚠ Bucket blocker</b>: The EBRAINS DataProxy endpoint "
                    "(data-proxy.ebrains.eu) is unreachable from this server (connection "
                    "timeout after 30 s). Authentication succeeds (IAM reachable) but "
                    "all file operations fail. Workaround: download on a local machine "
                    "with valid credentials and transfer via USB.",
                    warn_style
                )
            ]],
            colWidths=[16*cm],
            style=TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), HexColor('#fff0f0')),
                ('BOX', (0,0), (-1,-1), 1, HexColor('#cc0000')),
                ('TOPPADDING',    (0,0), (-1,-1), 6),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                ('LEFTPADDING',   (0,0), (-1,-1), 8),
            ])
        ),
    ]),
    Spacer(1, 8),
    subsection("2.2 Fallback: Self-Computed Z-Maps (sub-07)", [
        Paragraph(
            "Eight pre-existing z-scored GLM contrast maps for <b>sub-07</b> were available "
            "from a prior session (computed from OpenNeuro BOLD runs). These form the "
            "proof-of-concept dataset for Sprint 1.",
            body_style
        ),
        Table(
            [
                ["File", "Shape", "Task Family", "Z-Range"],
                ["ArchiEmotional_emotional_expr_gt_control_z.nii.gz", "(128, 128, 93)", "ArchiEmotional", "[-4.62, +4.45]"],
                ["ArchiEmotional_emotional_face_gt_control_z.nii.gz", "(128, 128, 93)", "ArchiEmotional", "[-4.89, +4.36]"],
                ["ArchiStandard_audio_gt_baseline_z.nii.gz", "(128, 128, 84)*", "ArchiStandard", "[-4.29, +5.71]"],
                ["ArchiStandard_checkerboard_gt_baseline_z.nii.gz", "(128, 128, 84)*", "ArchiStandard", "[-4.44, +4.45]"],
                ["PreferenceFaces_face_gt_baseline_z.nii.gz", "(128, 128, 93)", "PreferenceFaces", "[-5.52, +7.27]"],
                ["RSVPLanguage_language_gt_baseline_z.nii.gz", "(128, 128, 93)", "RSVPLanguage", "[-5.36, +4.52]"],
                ["RSVPLanguage_sentence_complex_vs_pseudo_z.nii.gz", "(128, 128, 93)", "RSVPLanguage", "[-4.79, +5.36]"],
                ["RSVPLanguage_sentence_gt_word_z.nii.gz", "(128, 128, 93)", "RSVPLanguage", "[-5.32, +7.17]"],
            ],
            colWidths=[6.5*cm, 2.8*cm, 2.8*cm, 3.9*cm],
            style=TableStyle([
                ('BACKGROUND', (0,0), (-1,0), MID_BLUE),
                ('TEXTCOLOR',  (0,0), (-1,0), WHITE),
                ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE',   (0,0), (-1,-1), 7.5),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT_GRAY, WHITE]),
                ('GRID',       (0,0), (-1,-1), 0.3, HexColor('#cccccc')),
                ('TOPPADDING',    (0,0), (-1,-1), 3),
                ('BOTTOMPADDING', (0,0), (-1,-1), 3),
                ('LEFTPADDING',   (0,0), (-1,-1), 5),
                ('FONTNAME',   (0,1), (0,-1), 'Courier'),
            ])
        ),
        Paragraph(
            "* ArchiStandard maps have 84 axial slices vs 93 for all others — "
            "resampled to 93 slices before averaging (see Section 3.1).",
            S('fn', fontSize=7.5, textColor=GRAY, fontName='Helvetica-Oblique')
        ),
    ]),
])

# ══════════════════════════════════════════════════════════════════════════════
# 3. METHODS
# ══════════════════════════════════════════════════════════════════════════════
story += [PageBreak()]
story += section("3. Methods", [
    subsection("3.1 Group-Average Computation (S1-4)", [
        Paragraph(
            "The eight contrast maps were averaged voxel-wise to produce a single "
            "<b>group_average_sub-07.nii.gz</b> file representing the mean z-score "
            "across conditions for sub-07. Two processing steps were required:",
            body_style
        ),
        bullet(
            "<b>Resampling</b>: ArchiStandard maps (84 slices) resampled to 93 slices "
            "using <mono>scipy.ndimage.zoom</mono> with linear interpolation (order=1) "
            "along the z-axis, followed by centre-cropping to exactly (128, 128, 93)."
        ),
        bullet(
            "<b>Averaging</b>: All 8 maps stacked along a 4th dimension; "
            "voxel-wise mean and std computed across the contrast axis."
        ),
        bullet(
            "Affine matrix from ArchiEmotional (MNI 1.5mm) used as reference orientation."
        ),
        Paragraph(
            "The inter-condition std map (<b>group_std_sub-07.nii.gz</b>) was also "
            "produced to characterise variability across contrasts.",
            body_style
        ),
    ]),
    subsection("3.2 Atlas &amp; Parcellation (S1-5)", [
        Paragraph(
            "The <b>Schaefer 400</b> parcellation (Yeo et al. 2011) was used as a "
            "proxy for the originally planned Glasser 360 atlas. The atlas was downloaded "
            "at 1mm resolution via nilearn's <mono>fetch_atlas_schaefer_2018()</mono> "
            "and resampled to 1.5mm to match the contrast maps.",
            body_style
        ),
        bullet(
            "<b>Resampling</b>: <mono>nibabel.processing.resample_from_to</mono> with "
            "nearest-neighbour (order=0) to preserve integer parcel labels."
        ),
        bullet(
            "<b>Result</b>: 384 non-zero parcels (16 of 400 fall outside the brain "
            "mask after resampling to the 1.5mm field of view)."
        ),
        bullet(
            "<b>Feature extraction</b>: per-parcel mean z-score across all voxels "
            "within the parcel mask, for each of the 8 contrast maps."
        ),
        Paragraph(
            "The parcel × contrast feature matrix was saved as "
            "<b>parcellated_contrasts.csv</b> (384 rows × 10 columns: "
            "parcel_id, parcel_label, 8 contrast columns).",
            body_style
        ),
    ]),
])

# ══════════════════════════════════════════════════════════════════════════════
# 4. RESULTS
# ══════════════════════════════════════════════════════════════════════════════
story += [PageBreak()]
story += section("4. Results", [
    Paragraph(
        "Figure 1 shows the eight individual contrast z-maps at axial slice z ≈ 0 mm. "
        "Strong positive activations (red) are visible in language cortex for RSVP "
        "contrasts and in fusiform face area for face-related contrasts.",
        body_style
    ),
    img("figures/fig1_individual_contrasts.png", 16, 7),
    Paragraph(
        "Figure 1. Individual contrast z-maps (axial slice z ≈ 0 mm, radiological convention). "
        "Colour scale: ±3. Red = positive activation, Blue = deactivation.",
        caption_style
    ),
    Spacer(1, 8),
    Paragraph(
        "Figure 2 shows the group-average z-map (mean across 8 contrasts) and the "
        "inter-condition standard deviation. High-std regions indicate disagreement "
        "across task conditions — these are the regions where averaging across "
        "contrasts washes out signal.",
        body_style
    ),
    img("figures/fig2_group_average.png", 14, 5.5),
    Paragraph(
        "Figure 2. Group mean (left, RdBu scale) and std (right, viridis scale) "
        "across 8 contrasts for sub-07.",
        caption_style
    ),
    Spacer(1, 8),
    img("figures/fig3_parcellation.png", 14, 4.5),
    Paragraph(
        "Figure 3. Schaefer 400 parcellation at three axial levels (z = 30, 50, 60 voxels). "
        "Colour represents parcel ID (1–400).",
        caption_style
    ),
])

story += [PageBreak()]
story += [
    Paragraph("4. Results (continued)", h1_style), HR(), Spacer(1, 4),
    img("figures/fig5_contrast_bar.png", 14, 5),
    Paragraph(
        "Figure 4. Mean absolute z-score per contrast (sub-07, Schaefer 400 parcels). "
        "Error bars = std across parcels. PreferenceFaces and RSVPLanguage_sentence_gt_word "
        "show the strongest mean activation.",
        caption_style
    ),
    Spacer(1, 8),
    img("figures/fig6_network_summary.png", 14, 4.5),
    Paragraph(
        "Figure 5. Network-level summary using Yeo 7-Networks labels extracted from "
        "Schaefer parcel names. Left: parcel count per network. Right: mean |z| by "
        "network × contrast.",
        caption_style
    ),
    Spacer(1, 8),
    img("figures/fig4_contrast_correlation.png", 11, 10),
    Paragraph(
        "Figure 6. Pearson correlation matrix between contrasts (parcel-wise profiles, "
        "384 parcels). RSVP Language contrasts (sentence_gt_word, language_gt_baseline) "
        "are highly correlated (r ≈ 0.93); face and emotion contrasts show moderate "
        "inter-correlation.",
        caption_style
    ),
]

# ══════════════════════════════════════════════════════════════════════════════
# 5. DELIVERABLES
# ══════════════════════════════════════════════════════════════════════════════
story += [PageBreak()]
story += section("5. Sprint 1 Deliverables", [
    Table(
        [
            ["Task", "Description", "Status", "Output"],
            ["S1-1", "Clone TRIBE v2 repo + setup env", "✓ Prior", "environment/tribev2/"],
            ["S1-2", "Download TRIBE v2 model weights", "✓ Prior", "best.ckpt (677 MB)"],
            ["S1-3", "Download IBC contrast maps (ibc_api)", "✓ Partial", "available_volume_maps.csv (57,938 entries)"],
            ["S1-4", "Group-average contrast maps", "✓ Fallback", "group_average_sub-07.nii.gz + std"],
            ["S1-5", "Parcellate with atlas", "✓ Proxy atlas", "Schaefer400_1.5mm.nii.gz + parcellated_contrasts.csv"],
            ["S1-6", "Populate Backlog S2–S4", "✓ Done", "14 tasks in Kanban Backlog"],
        ],
        colWidths=[1.6*cm, 7.2*cm, 2*cm, 5.2*cm],
        style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), DARK_BLUE),
            ('TEXTCOLOR',  (0,0), (-1,0), WHITE),
            ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE',   (0,0), (-1,-1), 8.5),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT_GRAY, WHITE]),
            ('GRID', (0,0), (-1,-1), 0.3, HexColor('#cccccc')),
            ('TOPPADDING',    (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING',   (0,0), (-1,-1), 5),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TEXTCOLOR', (2,3), (2,5), GREEN),
            ('FONTNAME',  (2,3), (2,5), 'Helvetica-Bold'),
            ('TEXTCOLOR', (2,1), (2,2), GRAY),
        ])
    ),
])

# ══════════════════════════════════════════════════════════════════════════════
# 6. LIMITATIONS
# ══════════════════════════════════════════════════════════════════════════════
story += [Spacer(1, 10)]
story += section("6. Limitations &amp; Open Issues", [
    bullet(
        "<b>Bucket blocker</b>: EBRAINS DataProxy (data-proxy.ebrains.eu) unreachable. "
        "57,938 IBC files not downloadable from this server. "
        "Workaround: download locally and transfer via USB, or request IP whitelist."
    ),
    bullet(
        "<b>Single subject</b>: Validation is based on sub-07 only (n=1). "
        "Generalisability to other IBC subjects is untested."
    ),
    bullet(
        "<b>Atlas substitution</b>: Schaefer 400 used instead of Glasser 360. "
        "Parcel counts differ (384 vs 360); network assignments also differ."
    ),
    bullet(
        "<b>Resampling artefact</b>: ArchiStandard maps resampled from 84→93 slices "
        "introduces slight spatial blurring relative to native-resolution maps."
    ),
    bullet(
        "<b>Group-average proxy</b>: group_average_sub-07.nii.gz averages 8 contrasts "
        "from one subject — not a true IBC group average across ≥13 subjects."
    ),
    bullet(
        "<b>No model predictions yet</b>: TRIBE v2 inference is pending S3 tasks."
    ),
])

# ══════════════════════════════════════════════════════════════════════════════
# 7. NEXT STEPS
# ══════════════════════════════════════════════════════════════════════════════
story += section("7. Recommended Next Steps (S2–S4)", [
    Paragraph("Sprint 2 — Stimulus Acquisition", h2_style),
    bullet("S2-1 to S2-4: Acquire stimulus files for each task family (FaceBody, Visu, RSVP, EmotionalPain) "
           "from OpenNeuro or the IBC raw data bucket."),
    bullet("S2-5: Cross-validate that every z-map contrast has a corresponding stimulus file."),
    Spacer(1, 4),
    Paragraph("Sprint 3 — TRIBE v2 Inference &amp; GLM", h2_style),
    bullet("S3-1 to S3-4: Run TRIBE v2 encoding model on each task's stimuli → predicted parcel responses."),
    bullet("S3-5: GLM beta extraction from raw BOLD runs using nilearn FirstLevelModel."),
    Spacer(1, 4),
    Paragraph("Sprint 4 — Correlation Analysis &amp; Figures", h2_style),
    bullet("S4-1: Compute R<sub>tribe_vs_group</sub> (Pearson r per parcel × condition)."),
    bullet("S4-2: Compute R<sub>tribe_vs_subject</sub>."),
    bullet("S4-3: Publication-quality figures (R distributions, scatter plots, ROI bar charts)."),
    bullet("S4-4: Full validation report committed to GitHub."),
])

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
story += [
    Spacer(1, 12),
    HRFlowable(width="100%", thickness=0.3, color=GRAY),
    Spacer(1, 4),
    Paragraph(
        "TRIBE v2 Evaluation · Sprint 1 Report · "
        "github.com/agents-sandboxed-repo/tribev2-evaluation · "
        "Generated by Hermes Agent · June 2026",
        footer_style
    ),
]

def flatten(seq):
    """Flatten one level of nesting (lists of flowables → flat flowable list)."""
    out = []
    for item in seq:
        if isinstance(item, list):
            out.extend(item)
        else:
            out.append(item)
    return out

story = flatten(story)

doc.build(story)
print("PDF saved: figures/SPRINT1_REPORT.pdf")
