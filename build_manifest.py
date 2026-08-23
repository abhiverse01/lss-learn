#!/usr/bin/env python3
"""
Regenerates the embedded file manifest inside index.html.

Run this from the repo root any time you add, rename, or delete files:

    python3 build_manifest.py

It rescans every file/folder in the repo (skipping index.html itself,
dotfiles, and .git), rebuilds the JSON tree, and swaps it into the
`var MANIFEST = [...]` line inside index.html in place. No other part
of index.html is touched.
"""
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
INDEX_HTML = os.path.join(ROOT, "index.html")

EXT_TYPE = {
    ".html": "html", ".htm": "html",
    ".css": "css",
    ".js": "js",
    ".pdf": "pdf",
    ".md": "md",
    ".json": "json",
    ".txt": "txt",
}

def build(path, is_root=False):
    entries = []
    for name in sorted(os.listdir(path)):
        if name.startswith(".") or name == ".git":
            continue
        if is_root and name == "index.html":
            continue
        full = os.path.join(path, name)
        rel = os.path.relpath(full, ROOT).replace("\\", "/")
        if os.path.isdir(full):
            children = build(full)
            if children:
                entries.append({"type": "dir", "name": name, "path": rel, "children": children})
        else:
            ext = os.path.splitext(name)[1].lower()
            ftype = EXT_TYPE.get(ext, "file")
            size = os.path.getsize(full)
            entries.append({"type": "file", "name": name, "path": rel, "ext": ext, "ftype": ftype, "size": size})
    return entries

def main():
    if not os.path.isfile(INDEX_HTML):
        sys.exit("index.html not found next to this script. Run it from the repo root.")

    tree = build(ROOT, is_root=True)
    manifest_json = json.dumps(tree, separators=(",", ":"))

    html = open(INDEX_HTML, encoding="utf-8").read()
    pattern = re.compile(r"var MANIFEST = \[.*?\];\n", re.S)
    if not pattern.search(html):
        sys.exit("Couldn't find `var MANIFEST = [...]` in index.html — is this the right file?")

    new_html = pattern.sub("var MANIFEST = " + manifest_json.replace("\\", "\\\\") + ";\n", html, count=1)
    open(INDEX_HTML, "w", encoding="utf-8").write(new_html)

    def count_files(nodes):
        c = 0
        for n in nodes:
            c += count_files(n["children"]) if n["type"] == "dir" else 1
        return c

    print(f"Done. Indexed {count_files(tree)} files into index.html.")

if __name__ == "__main__":
    main()
