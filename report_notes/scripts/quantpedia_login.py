#!/usr/bin/env python3
"""
Quantpedia login helper.

This script provides the workflow for logging into Quantpedia
using Playwright MCP. Run the MCP commands interactively.

Credentials are stored in .env file.
"""

import os
from pathlib import Path

# Load .env from ClaudeCodeResearch root
env_path = Path(__file__).parent.parent.parent / ".env"

if env_path.exists():
    with open(env_path) as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

QUANTPEDIA_EMAIL = os.environ.get("QUANTPEDIA_EMAIL", "")
QUANTPEDIA_PASSWORD = os.environ.get("QUANTPEDIA_PASSWORD", "")

WORKFLOW = f"""
# Quantpedia Login Workflow (Playwright MCP)

## Step 1: Navigate to login page
```python
mcp__playwright__browser_navigate(url="https://quantpedia.com/login/")
```

## Step 2: Take snapshot to find form elements
```python
mcp__playwright__browser_snapshot()
```

## Step 3: Fill login form
Look for email/username and password field refs in snapshot, then:
```python
mcp__playwright__browser_type(
    ref="<email_field_ref>",
    text="{QUANTPEDIA_EMAIL}"
)
mcp__playwright__browser_type(
    ref="<password_field_ref>",
    text="{QUANTPEDIA_PASSWORD}"
)
```

## Step 4: Submit form
```python
mcp__playwright__browser_click(
    ref="<submit_button_ref>",
    element="Login button"
)
```

## Step 5: Verify login
```python
mcp__playwright__browser_snapshot()
```
Look for user menu or account indicator.

## Step 6: Navigate to strategy
```python
mcp__playwright__browser_navigate(url="https://quantpedia.com/strategies/<strategy-slug>/")
```

---

# Credentials loaded from .env:
Email: {QUANTPEDIA_EMAIL}
Password: {'*' * len(QUANTPEDIA_PASSWORD) if QUANTPEDIA_PASSWORD else '(not set)'}
"""

if __name__ == "__main__":
    print(WORKFLOW)
