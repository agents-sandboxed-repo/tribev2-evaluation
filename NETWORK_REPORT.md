# Network Access Report — TRIBE v2 Evaluation

**Date:** 2026-06-18

## Accessible hosts (verified)
- github.com ✓
- huggingface.co ✓
- nitrc.org ✓ (download IDs work)
- osf.io ✓
- openneuro.org ✓ (web UI accessible)

## Blocked hosts (DNS / SSL / timeout)
- api.neurovault.org ✗ (NameResolutionError — all NeuroVault API calls fail)
- neurovault.org ✗ (same — api subdomain unreachable)
- ebrains.eu ✗ (device flow auth required — no cached credentials)
- api.ebrains.eu ✗ (no auth token available)
- nitrc.org/frs/download.php/* ✗ (NITRC file downloads require session cookie)
- ftp.nmr.mgh.harvard.edu ✗ (FTP timeout)
- surfer.nmr.mgh.harvard.edu ✗ (FTP timeout)
-figshare.com ✗ (SSL verification fails)
- Human Connectome Project servers ✗ (SSL cert mismatch)

## Impact on Sprint 1

### S1-3 / S1-4 (Download IBC contrast maps) — BLOCKED
- IBC contrast maps live on EBRAINS (requires login)
- ibc_api package authenticates via EBRAINS device flow — no cached token
- Alternative: NeuroVault collections 6618 and 4438 (also blocked)
- Fallback: OpenNeuro has raw IBC fMRI data (ds002685) but NOT pre-computed contrast maps

### S1-5 (Glasser 360 parcellation) — BLOCKED
- Glasser 360 atlas is on NITRC (download requires session cookie)
- Not on nilearn's built-in fetchers (only Destrieux and Juelich/HarvardOxford available)
- Workaround: Use Schaefer 100 or 200 (can try via nilearn's OSF links)

## Recommendations

### Option A — EBRAINS account (recommended)
Register at https://ebrains.eu/register — no VPN needed, device flow works from this machine.
Once registered, run `ibc_api` once interactively to cache the token, then automation works.

### Option B — Use Schaefer atlas instead of Glasser 360
Schaefer 100/200 parcels are downloadable from OSF (accessible). This changes the parcel count
in the correlation analysis (360 → 100 or 200 parcels) but the methodology is identical.

### Option C — Use Haxby or other nilearn-available datasets
Reduce scope to use a dataset nilearn can fetch (Haxby, ADHD, ABIDE) for a proof-of-concept.
Not the same as IBC but validates the TRIBE v2 evaluation pipeline.

## Next action required
EBRAINS authentication or decision on atlas fallback (Schaefer).
