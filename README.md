# Means TV alert cards

Public image host for the **creator alert emails** (Uscreen automations). Each launch creator has one card at a fixed address that always shows their newest video:

`https://max-means.github.io/means-tv-alert-cards/cards/<slug>.png`

Slugs: `second-thought`, `hakim`, `prince-shakur`, `positive-leftist-news`, `michael-burns`, `our-changing-climate`, `noncompete`, `luna-oi`.

- `template/card.html`: the card design (434px image slot in a 494px email, rendered at 2x).
- `render.py`: fills the template and writes `cards/<slug>.png`. The watcher job in `means-tv-member-tagging` runs it when a creator publishes, commits the new card here, waits ~10 minutes for GitHub Pages' cache, then tags members.
- Everything in this repo is public. Only put card images and the template here, never member data or keys.

Plan and decisions: see the "Creator New-Video Email Alerts" doc.
