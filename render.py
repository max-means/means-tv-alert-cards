"""Render a creator alert card PNG from template/card.html.

    python render.py --slug hakim --creator "Hakim" \
        --title "Christopher Hitchens was a terrible human being" \
        --thumb https://alpha.uscreencdn.com/images/programs/4442694/horizontal/4362d4d3-....jpg \

Writes cards/<slug>.png (868px wide = the email's 434px image slot at 2x). Needs: pip install playwright && playwright install chromium
The " | Creator" suffix on Uscreen titles is stripped automatically.
"""
import argparse, datetime, html, os, re
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))


def clean_title(title, creator):
    return re.sub(r"\s*\|\s*" + re.escape(creator) + r"\s*$", "", title, flags=re.I).strip()


def full_size(thumb):
    # Uscreen serves a 320px "small_" copy; the same path without the prefix is full size.
    return thumb.replace("/small_", "/")


def render(slug, creator, title, thumb, date=None, out_dir=None):
    # date is accepted for compatibility but no longer shown on the card
    page_html = open(os.path.join(HERE, "template", "card.html"), encoding="utf-8").read()
    for key, val in {
        "CREATOR": html.escape(creator),
        "TITLE": html.escape(clean_title(title, creator)),
        "THUMB": html.escape(full_size(thumb)),
    }.items():
        page_html = page_html.replace("{{" + key + "}}", val)
    out_dir = out_dir or os.path.join(HERE, "cards")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, f"{slug}.png")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 494, "height": 400}, device_scale_factor=2)
        page.set_content(page_html, wait_until="networkidle")
        page.locator(".card").screenshot(path=out)
        browser.close()
    return out


if __name__ == "__main__":
    a = argparse.ArgumentParser()
    for f in ("slug", "creator", "title", "thumb"):
        a.add_argument("--" + f, required=True)
    a.add_argument("--date")
    args = a.parse_args()
    print(render(args.slug, args.creator, args.title, args.thumb, args.date))
