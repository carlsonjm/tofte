"""The trial's page: what went in, who came out, and why each join was made.

It is written beside the contacts it describes and is not meant to leave the
computer. What `counts` returns holds no names and no handles.
"""

from __future__ import annotations

import html
from collections import Counter

from .model import Result, agree

REASONS = {
    "same-handle": "the same number or address is on both cards",
    "hand": "you joined them",
    "same-name": "the same full name",
    "same-first-name": "the same single name",
    "shared-handle": "they share a number or address that looks like a place's",
}


def counts(res: Result) -> dict:
    joined = [p for p in res.people if len(p.records) > 1]
    differ = sum(1 for p in joined for j in p.joins
                 if not agree(res.records[j.a].name, res.records[j.b].name))
    return {
        "cards": len(res.records),
        "handles": len({h.key for r in res.records for h in r.handles}),
        "cards_without_handles": sum(1 for r in res.records if not r.handles),
        "people": len(res.people),
        "people_made_from_several_cards": len(joined),
        "automatic_joins": sum(len(p.joins) for p in res.people),
        "joins_where_names_differ": differ,
        "suggestions": dict(Counter(f"{s.strength} {s.reason}" for s in res.suggestions)),
        "shared_handles_not_joined": len(res.shared),
        "joins_stopped_by_a_split": len(res.blocked),
    }


def page(res: Result) -> str:
    e = html.escape
    c = counts(res)
    recs = res.records

    def handles(hs):
        return ", ".join(e(h.value) for h in hs) or "no number or address"

    out = [f"""<!doctype html><meta charset="utf-8"><title>Person model trial</title>
<style>
:root{{--bg:#F8F8FF;--ink:#141414;--soft:#5c5c66;--line:#dcdce4;--card:#fff;--warn:#9a5b00}}
@media (prefers-color-scheme:dark){{:root{{--bg:#141414;--ink:#F8F8FF;--soft:#a0a0ac;--line:#33333a;--card:#1d1d21;--warn:#f0b35a}}}}
body{{background:var(--bg);color:var(--ink);font:16px/1.5 system-ui,sans-serif;max-width:860px;margin:0 auto;padding:32px 16px}}
h1{{font-size:28px;margin:0 0 4px}}h2{{font-size:20px;margin:40px 0 8px}}p{{margin:8px 0}}.soft{{color:var(--soft)}}
.tiles{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:20px 0}}
.tile{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px}}.tile b{{font-size:28px;display:block}}
.row{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px;margin:8px 0}}
.row b{{font-size:17px}}.warn{{color:var(--warn);font-weight:600}}details{{margin:8px 0}}summary{{cursor:pointer}}
</style>
<h1>Person model trial</h1>
<p class="soft">Phone contacts only. This page stays on this computer.</p>
<div class="tiles">
<div class="tile"><b>{c['cards']}</b>contact cards in</div>
<div class="tile"><b>{c['people']}</b>people out</div>
<div class="tile"><b>{c['automatic_joins']}</b>automatic joins</div>
<div class="tile"><b>{len(res.suggestions)}</b>suggestions</div>
</div>
<p>What to check: under "Joined automatically", is every row truly one person? One wrong row fails the trial.
Under "Suggestions", which rows should have been joined?</p>
<h2>Joined automatically</h2>"""]
    joined = [p for p in res.people if len(p.records) > 1]
    joined.sort(key=lambda p: all(agree(recs[j.a].name, recs[j.b].name) for j in p.joins))
    if not joined:
        out.append('<p class="soft">Nothing was joined.</p>')
    for p in joined:
        names = sorted({recs[i].name or "(no name)" for i in p.records})
        differ = any(not agree(recs[j.a].name, recs[j.b].name) for j in p.joins)
        why = "; ".join(sorted({f"{REASONS[j.reason]} ({e(j.handle.split(':', 1)[-1])})" for j in p.joins}))
        out.append(f'<div class="row"><b>{e(p.name or "(no name)")}</b><br>'
                   f'{len(p.records)} cards: {e(" · ".join(names))}<br>'
                   f'<span class="soft">{handles(p.handles)}</span><br>'
                   f'<span class="soft">Why: {why}</span>'
                   + ('<br><span class="warn">The names differ. Please look closely.</span>' if differ else "")
                   + "</div>")
    out.append("<h2>Suggestions, not joined</h2>")
    if not res.suggestions:
        out.append('<p class="soft">No suggestions.</p>')
    for s in res.suggestions:
        a, b = (res.people[i] for i in s.people)
        out.append(f'<div class="row"><b>{e(a.name or "(no name)")}</b> and <b>{e(b.name or "(no name)")}</b><br>'
                   f'<span class="soft">{handles(a.handles)} &nbsp;|&nbsp; {handles(b.handles)}</span><br>'
                   f'<span class="soft">{"Likely" if s.strength == "strong" else "Possible"}: {REASONS[s.reason]}</span></div>')
    out.append("<h2>Shared numbers and addresses, joining nobody</h2>")
    if not res.shared:
        out.append('<p class="soft">None found.</p>')
    for key, rs in res.shared.items():
        out.append(f'<div class="row"><b>{e(key.split(":", 1)[-1])}</b><br>'
                   f'{e(" · ".join(recs[i].name or "(no name)" for i in rs))}</div>')
    out.append(f"<h2>Everyone</h2><details><summary>All {len(res.people)} people</summary>")
    for p in sorted(res.people, key=lambda p: p.name.casefold()):
        out.append(f'<p><b>{e(p.name or "(no name)")}</b> <span class="soft">{handles(p.handles)}</span></p>')
    out.append("</details>")
    return "\n".join(out)
