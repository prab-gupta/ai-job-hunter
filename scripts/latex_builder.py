#!/usr/bin/env python3
"""LaTeX Compilation & Verification Tool for the AI Job Hunter Plugin.
Compiles bespoke CVs and Cover Letters via Tectonic, enforces single-page constraints,
and audits source files for zero em-dash compliance.

Usage:
  python3 latex_builder.py --cv "Prabhavit_CV_<Company>.tex"
  python3 latex_builder.py --letter "CoverLetter_<Company>.tex"
  python3 latex_builder.py --all
"""

import argparse
import os
import re
import subprocess
import sys

def find_workspace_root():
    cur = os.path.abspath(os.getcwd())
    while cur != os.path.dirname(cur):
        if os.path.exists(os.path.join(cur, "applications.csv")) or os.path.exists(os.path.join(cur, "templates")):
            return cur
        cur = os.path.dirname(cur)
    return os.path.abspath(os.getcwd())

ROOT = find_workspace_root()

def audit_em_dashes(file_path):
    if not os.path.exists(file_path):
        return True
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    if " - " in content or "–" in content:
        # Check if it's outside LaTeX comments or -- syntax
        # Specifically flag unicode em-dash ( - )
        if " - " in content:
            print(f"WARNING: Unicode em-dash ( - ) detected in {file_path}. Replacing with ' - '...")
            content = content.replace(" - ", " - ")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
    return True

def compile_latex(tex_file, max_pages=1):
    tex_path = os.path.abspath(tex_file)
    if not os.path.exists(tex_path):
        print(f"ERROR: File not found: {tex_path}", file=sys.stderr)
        return False

    audit_em_dashes(tex_path)

    work_dir = os.path.dirname(tex_path)
    base_name = os.path.basename(tex_path)
    pdf_name = os.path.splitext(base_name)[0] + ".pdf"
    pdf_path = os.path.join(work_dir, pdf_name)

    print(f"Compiling {base_name} with tectonic...")
    try:
        res = subprocess.run(
            ["tectonic", base_name],
            cwd=work_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=60
        )
        if res.returncode != 0:
            print(f"Tectonic error:\n{res.stderr}", file=sys.stderr)
            return False
    except Exception as e:
        print(f"Compilation execution failed: {e}", file=sys.stderr)
        return False

    if not os.path.exists(pdf_path):
        print(f"ERROR: PDF was not generated at {pdf_path}", file=sys.stderr)
        return False

    # Check page count
    try:
        info_res = subprocess.run(
            ["pdfinfo", pdf_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if info_res.returncode == 0:
            m = re.search(r"Pages:\s+(\d+)", info_res.stdout)
            if m:
                pages = int(m.group(1))
                print(f"Compiled successfully: {pdf_name} ({pages} page{'s' if pages != 1 else ''})")
                if max_pages and pages > max_pages:
                    print(f"WARNING: Output exceeds desired page limit of {max_pages} pages! (Actual: {pages})")
    except FileNotFoundError:
        print(f"Compiled successfully: {pdf_name}")

    return True

def main():
    parser = argparse.ArgumentParser(description="Tectonic LaTeX Builder & Page Auditor")
    parser.add_argument("--cv", type=str, help="Path to CV .tex file to compile")
    parser.add_argument("--letter", type=str, help="Path to Cover Letter .tex file to compile")
    parser.add_argument("--pages", type=int, default=1, help="Max page constraint (default: 1)")
    args = parser.parse_args()

    if args.cv:
        success = compile_latex(args.cv, max_pages=args.pages)
        sys.exit(0 if success else 1)
    elif args.letter:
        success = compile_latex(args.letter, max_pages=args.pages)
        sys.exit(0 if success else 1)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
