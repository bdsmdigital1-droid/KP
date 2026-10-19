#!/usr/bin/env python3
"""Собирает страницу КП из slides/NN.jpg и spec.json.

Запуск: python3 _tools/build_page.py <папка КП>
В папке должны лежать slides/01.jpg … и spec.json:
{
  "alts": ["Обложка КП BDSM-digital", "Почему выбирают нас", ...],   # по одному на слайд
  "pills": {"5": [["Сайт аренды яхт на Кипре", "https://..."]], ...} # номер слайда -> кнопки
}
Кнопки контактов и «больше кейсов» добавь в pills сам (см. CONTACTS ниже).
"""
import json, sys, pathlib

WA = ("https://api.whatsapp.com/send/?phone=79968894054&text=%D0%94%D0%BE%D0%B1%D1%80%D1%8B%D0%B9+%D0%B4%D0%B5%D0%BD%D1%8C%2C+"
      "%D1%85%D0%BE%D1%87%D1%83+%D1%83%D0%B2%D0%B5%D0%BB%D0%B8%D1%87%D0%B8%D1%82%D1%8C+%D0%BF%D0%BE%D1%82%D0%BE%D0%BA+"
      "%D0%BA%D0%BB%D0%B8%D0%B5%D0%BD%D1%82%D0%BE%D0%B2+%D1%87%D0%B5%D1%80%D0%B5%D0%B7+%D1%81%D0%B0%D0%B9%D1%82+%D0%B8+"
      "%D0%BA%D0%BE%D0%BC%D0%BF%D0%BB%D0%B5%D0%BA%D1%81%D0%BD%D1%8B%D0%B9+%D0%BC%D0%B0%D1%80%D0%BA%D0%B5%D1%82%D0%B8%D0%BD%D0%B3"
      "&type=phone_number&app_absent=0")
CONTACTS = [["WhatsApp +7 996 889 40 54", WA], ["Telegram @tomas_ana", "https://t.me/tomas_ana"],
            ["bdsm-digital.com", "https://bdsm-digital.com/"]]
MORE_CASES = [["Все кейсы на bdsm-digital.com", "https://bdsm-digital.com/"]]

CSS = """/* Одна колонка слайдов 16:9, под слайдами со ссылками — красные плашки */
:root{--bg:#0e0d0d;--surface:#1a1716;--fg:#f3eeec;--red:#b1120f;--red-hi:#d42a24;
--display:"Oswald","Arial Narrow",Impact,sans-serif;--body:"Golos Text",system-ui,-apple-system,"Segoe UI",sans-serif;color-scheme:dark}
*,*::before,*::after{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--body);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:24px 48px}
main{max-width:1280px;margin:0 auto;display:flex;flex-direction:column;gap:28px}
.slide{margin:0;display:flex;flex-direction:column;gap:14px}
.slide img{display:block;width:100%;height:auto;max-width:100%;aspect-ratio:16/9;background:var(--surface);border-radius:6px}
.pills{display:flex;flex-wrap:wrap;gap:10px}
.pill{display:inline-flex;align-items:center;gap:8px;padding:11px 20px;border-radius:999px;background:var(--red);color:var(--fg);font-family:var(--display);font-weight:500;font-size:15px;letter-spacing:.04em;text-transform:uppercase;text-decoration:none;transition:background .15s}
.pill:hover{background:var(--red-hi)}.pill:focus-visible{outline:2px solid var(--fg);outline-offset:3px}
@media (prefers-reduced-motion:reduce){.pill{transition:none}}
@media (max-width:480px){main{gap:20px}.pill{font-size:13px;padding:10px 16px}}"""

def esc(s): return s.replace("&", "&amp;").replace('"', "&quot;")

def main():
    d = pathlib.Path(sys.argv[1])
    spec = json.loads((d / "spec.json").read_text())
    alts, pills = spec["alts"], {int(k): v for k, v in spec.get("pills", {}).items()}
    n = len(sorted((d / "slides").glob("*.jpg")))
    assert n == len(alts), f"слайдов {n}, alt-текстов {len(alts)}"
    figs = []
    for i, alt in enumerate(alts, 1):
        attr = 'fetchpriority="high"' if i == 1 else 'loading="lazy" decoding="async"'
        p = ""
        if pills.get(i):
            p = '\n    <div class="pills">' + "".join(
                f'<a class="pill" href="{esc(u)}" target="_blank" rel="noopener">{t} <span aria-hidden="true">↗</span></a>'
                for t, u in pills[i]) + "</div>"
        figs.append(f'  <figure class="slide"><img src="slides/{i:02d}.jpg" width="1920" height="1080" alt="{esc(alt)}" {attr}>{p}\n  </figure>')
    html = f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<title>КП BDSM-digital</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Golos+Text:wght@400;500&family=Oswald:wght@500;600&display=swap">
<style>
{CSS}
</style>
</head>
<body>
<main>
{chr(10).join(figs)}
</main>
</body>
</html>
"""
    (d / "index.html").write_text(html)
    (d / "spec.json").unlink()
    print("ok", d / "index.html", n, "слайдов")

if __name__ == "__main__":
    main()
