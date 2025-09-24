# Aged Jobs (30+ Days) — GitHub Pages MVP

This repo builds a simple website that lists jobs that have been open for more than **30 days** from public **Greenhouse** and **Lever** job board JSON feeds.

## Quick Start

1. **Edit companies** in `build_jobs.py` — replace the example slugs under `COMPANIES` with companies you care about.
2. **Run locally** (optional):
   ```bash
   python -m venv .venv
   # mac/linux:
   source .venv/bin/activate
   # windows:
   # .venv\Scripts\activate
   pip install -r requirements.txt
   python build_jobs.py
   ```
   This produces `jobs_30plus.json`.
3. **Open** `index.html` locally; it will render the list with basic search & filters.
4. **Deploy with GitHub Pages:**
   - Create a new public repo, upload all files (including `jobs_30plus.json` for the first publish).
   - Repo Settings → **Pages** → Source = `main` branch `/ (root)`.
   - Your site goes live at `https://<user>.github.io/<repo>/`.
5. **Auto-refresh daily (optional but recommended):**
   - Keep the repo public.
   - The included GitHub Action runs daily, regenerates `jobs_30plus.json`, commits, and keeps the site fresh.

### Change the "30 days" threshold

In `build_jobs.py`, change `DAYS_OLD = 30`.

### Notes

- **No scraping.** We only read public JSON from ATS providers.
- **Recruiters excluded.** Simple substring match for "recruit"/"staff"; tweak to your needs.
- **Hiring managers.** Use enrichment APIs (Apollo, Clearbit, etc.) outside this MVP if you want contact suggestions.
