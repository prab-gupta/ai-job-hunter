# Installation & Environment Setup Guide

This guide walks through configuring the `ai-job-hunter` plugin across different AI coding environments.

---

## 1. System Prerequisites

### Core Tooling
- **Python:** 3.10+
- **Node.js:** 18+
- **Tectonic (LaTeX Compiler):**
  ```bash
  # macOS (Homebrew)
  brew install tectonic poppler

  # Linux (Ubuntu/Debian)
  curl --proto '=https' --tlsv1.2 -fsSL https://drop-sh.tectonic-typesetting.net | sh
  sudo apt-get install -y poppler-utils
  ```
- **Playwright (Browser Automation):**
  ```bash
  pip install playwright beautifulsoup4 requests
  playwright install chromium
  ```

---

## 2. Framework Integration

### A. Google Antigravity & Gemini CLI
1. Place the plugin directory inside `.agents/plugins/ai-job-hunter/` of your project workspace, or into `~/.gemini/config/plugins/ai-job-hunter/` for global discovery.
2. Antigravity will automatically load `plugin.json`, mounting skills and rules on demand via progressive disclosure.

### B. Anthropic Claude Code
1. Ensure `.claude/` in your workspace contains the skills and commands:
   ```bash
   cp -r .agents/plugins/ai-job-hunter/.claude/* .claude/
   ```
2. Claude Code will expose `/tailor`, `/apply`, `/sweep`, and `/loop` slash commands.

### C. OpenAI Codex
1. Codex automatically reads `CODEX.md` and `.codex/config.json` at the root of the workspace.

---

## 3. Environment Variables (Optional for Automated OTP Retrieval)

For automated 8-box Greenhouse email verification code resolution:
```bash
export GMAIL_USER="prabhavitg@gmail.com"
export GMAIL_APP_PASS="xeoa zwqw caqg uqza"
```
