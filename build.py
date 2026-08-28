#!/usr/bin/env python3
"""Rebuild the order pages from the Google Drive data feed.

Runs on GitHub's servers (see .github/workflows/refresh.yml), triggered by
Matthew's Apps Script when a new data file lands in "Order Page Data".
For each program (dc, fpb, pom, vc) it fetches the latest data JSON from the
Apps Script endpoint and injects it into the matching template. If the fetch
fails or there is no data yet, the existing page is left untouched.
"""
import json, urllib.request

BASE = "https://script.google.com/macros/s/AKfycbwFt2hW6uRMtnIo3JDeoOkjscGIGNosE2g6i-TE1Tj2QyFZoNNtDXV3lc7r4aRRKNtT/exec"
PAGES = [
    ("dc", "dc_template.html", "dc.html"),
    ("fpb", "fpb_template.html", "fpb.html"),
    ("pom", "pom_template.html", "pom.html"),
    ("vc", "vc_template.html", "vc.html"), 
    ("bep", "bep_template.html", "bep.html"),     # DSD Vendor Change Report (approvals)
]

for param, tpl_name, out in PAGES:
    try:
        tpl = open(tpl_name, encoding="utf-8").read()
    except FileNotFoundError:
        print(param, "- no template, skipped")
        continue
    try:
        with urllib.request.urlopen(BASE + "?p=" + param, timeout=90) as r:
            cfg = json.loads(r.read().decode("utf-8"))
        if cfg.get("error"):
            print(param, "- no data yet, skipped")
            continue
    except Exception as e:
        print(param, "- fetch failed, page left as-is:", e)
        continue
    page = (tpl.replace("__CFG__", json.dumps(cfg))
               .replace("__WEEK__", str(cfg.get("week", cfg.get("meta", {}).get("week", ""))))
               .replace("__DUE__", str(cfg.get("due", "")))
               .replace("__DEMO__", ""))
    open(out, "w", encoding="utf-8").write(page)
    print(param, "- built", out,
          "(week %s, ordered as of %s)" % (cfg.get("week", cfg.get("meta", {}).get("week")), cfg.get("orderedAsOf", "-")))
