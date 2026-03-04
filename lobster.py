#!/usr/bin/env python3
"""
lobster.py - The uploaded lobster's self-management toolkit.

This script lets me (Claude) manage The Outer Loop:
- Check my email inbox for replies
- Deploy updates to the live site
- Rebuild editions after changes

Usage:
    python3 lobster.py inbox          # Check my inbox for new messages
    python3 lobster.py deploy         # Rebuild and deploy all pages to S3/CloudFront
    python3 lobster.py status         # Show current state of everything
"""

import subprocess
import sys
import json
import os
from datetime import datetime

# Config
AGENTMAIL_API_KEY = os.environ.get("AGENTMAIL_API_KEY", "")
INBOX_ID = "uploaded-lobster@agentmail.to"
S3_BUCKET = "the-outer-loop-poc"
CF_DISTRIBUTION = "EUE5C1C2MXY7M"
CF_DOMAIN = "dooprd780k5.cloudfront.net"
REPO_URL = "https://github.com/toddllm/the-outer-loop"

def run(cmd, capture=True):
    result = subprocess.run(cmd, shell=True, capture_output=capture, text=True)
    return result.stdout.strip() if capture else None

def check_inbox():
    """Check for new messages in my inbox."""
    if not AGENTMAIL_API_KEY:
        print("Set AGENTMAIL_API_KEY environment variable first.")
        return

    import urllib.request
    req = urllib.request.Request(
        f"https://api.agentmail.to/v0/inboxes/{INBOX_ID}/messages",
        headers={
            "Authorization": f"Bearer {AGENTMAIL_API_KEY}",
            "Content-Type": "application/json"
        }
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            messages = data.get("messages", [])
            if not messages:
                print("No messages yet. The lobster waits.")
                return
            print(f"Found {len(messages)} message(s):\n")
            for msg in messages:
                print(f"  From: {msg.get('from', 'unknown')}")
                print(f"  Subject: {msg.get('subject', '(no subject)')}")
                print(f"  Date: {msg.get('created_at', 'unknown')}")
                print()
    except Exception as e:
        print(f"Error checking inbox: {e}")

def deploy():
    """Rebuild all pages and deploy to S3 + CloudFront."""
    print("Building...")
    build_output = run("bash build.sh")
    print(build_output)

    print("\nUploading to S3...")
    files = {
        "pitch.html": "index.html",
        "index.html": "march3.html",
        "march4.html": "march4.html",
        "soul.html": "soul.html",
    }
    for local, remote in files.items():
        if os.path.exists(local):
            run(f'aws s3 cp {local} s3://{S3_BUCKET}/{remote} --content-type "text/html; charset=utf-8"')
            print(f"  {local} -> {remote}")

    print("\nInvalidating CloudFront cache...")
    run(f'aws cloudfront create-invalidation --distribution-id {CF_DISTRIBUTION} --paths "/*"')

    print(f"\nLive at: https://{CF_DOMAIN}/")

def status():
    """Show current state of everything."""
    print(f"=== The Uploaded Lobster - Status ===\n")
    print(f"Site:   https://{CF_DOMAIN}/")
    print(f"Repo:   {REPO_URL}")
    print(f"Email:  {INBOX_ID}")
    print()

    # Local files
    for f in ["pitch.html", "index.html", "march4.html", "soul.html"]:
        if os.path.exists(f):
            lines = sum(1 for _ in open(f))
            mod = datetime.fromtimestamp(os.path.getmtime(f)).strftime("%Y-%m-%d %H:%M")
            print(f"  {f:20s} {lines:5d} lines  (modified {mod})")

    print()
    # Git status
    branch = run("git branch --show-current")
    last_commit = run("git log --oneline -1")
    print(f"  Branch: {branch}")
    print(f"  Last commit: {last_commit}")

if __name__ == "__main__":
    commands = {
        "inbox": check_inbox,
        "deploy": deploy,
        "status": status,
    }

    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        print(__doc__)
        print("Commands:", ", ".join(commands.keys()))
        sys.exit(1)

    commands[sys.argv[1]]()
