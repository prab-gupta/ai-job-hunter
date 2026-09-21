from fastmcp import FastMCP
import subprocess
import os
import sys

# Create the MCP server
mcp = FastMCP("ai-job-hunter")

def run_script(script_name: str, args: list[str]) -> str:
    """Helper to run python scripts from the scripts/ directory."""
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_name)
    try:
        result = subprocess.run(
            [sys.executable, script_path] + args,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error running {script_name}:\nSTDOUT: {e.stdout}\nSTDERR: {e.stderr}"

@mcp.tool()
def dedupe_check(company: str, url: str) -> str:
    """Checks if a job application already exists in the ledger."""
    return run_script("dedupe.py", ["--check", company, url])

@mcp.tool()
def compile_latex(cv_path: str, letter_path: str) -> str:
    """Compiles bespoke LaTeX CV and Cover Letter."""
    args = []
    if cv_path:
        args.extend(["--cv", cv_path])
    if letter_path:
        args.extend(["--letter", letter_path])
    return run_script("latex_builder.py", args)

@mcp.tool()
def apply_greenhouse(url: str, company: str, role: str, cv: str, letter: str) -> str:
    """Submits an application via Greenhouse."""
    return run_script("apply_greenhouse.py", [
        "--url", url,
        "--company", company,
        "--role", role,
        "--cv", cv,
        "--letter", letter
    ])

@mcp.tool()
def apply_ashby(url: str, company: str, role: str, cv: str, letter: str) -> str:
    """Submits an application via Ashby."""
    return run_script("apply_ashby.py", [
        "--url", url,
        "--company", company,
        "--role", role,
        "--cv", cv,
        "--letter", letter
    ])

@mcp.tool()
def apply_workable(url: str, company: str, role: str, cv: str, letter: str) -> str:
    """Submits an application via Workable."""
    return run_script("apply_workable.py", [
        "--url", url,
        "--company", company,
        "--role", role,
        "--cv", cv,
        "--letter", letter
    ])

@mcp.tool()
def apply_personio(url: str, company: str, role: str, cv: str, letter: str) -> str:
    """Submits an application via Personio."""
    return run_script("apply_personio.py", [
        "--url", url,
        "--company", company,
        "--role", role,
        "--cv", cv,
        "--letter", letter
    ])

@mcp.tool()
def sweep_jobs() -> str:
    """Runs a multi-aggregator sweep for new job postings."""
    return run_script("sweep.py", [])

if __name__ == "__main__":
    mcp.run()
