---
description: Enforce standard hyphen rule and ban unicode em-dashes across all files, code, and LaTeX.
trigger: always_on
---

# Zero Em-Dash Enforcement Rule

## Policy
1. All files (Markdown, Python, JavaScript, LaTeX, CSV, and text) must use standard ASCII hyphens (` - `) with surrounding spaces, or standard LaTeX syntax (`--` for en-dash in date ranges).
2. The unicode em-dash character (` - ` / `\u2014`) is strictly forbidden across all files, code comments, LaTeX documents, and generated PDFs.
3. When parsing or generating text, always replace unicode em-dashes with ` - `.

## Verification
Run the following audit before committing or generating outputs:
```bash
python3 -c "
import glob
for f in glob.glob('**/*.tex', recursive=True) + glob.glob('**/*.md', recursive=True):
    with open(f) as fp:
        c = fp.read()
    if ' - ' in c:
        print(f'ERROR: Unicode em-dash detected in {f}')
"
```
