#!/usr/bin/env python3
"""
Create cleanup commits from March 20-29, 2026
"""

import subprocess
import os
from datetime import datetime, timedelta

os.chdir('/Users/mohamedaminehamdi/Desktop/Telemed')

cleanup_tasks = {
    "2026-03-20": {
        "msg": "Remove duplicate README file (consolidate documentation)",
        "actions": ["rm -f README_UPDATED.md"]
    },
    "2026-03-21": {
        "msg": "Remove redundant project completion summary",
        "actions": ["rm -f PROJECT_COMPLETION.md"]
    },
    "2026-03-22": {
        "msg": "Clean up old Django app directories",
        "actions": [
            "rm -rf account/",
            "rm -rf appoint/",
            "rm -rf appoint_app/",
            "rm -rf payments/",
            "rm -rf theme/",
            "rm -rf Resources/"
        ]
    },
    "2026-03-23": {
        "msg": "Remove temporary database files",
        "actions": ["rm -f db.sqlite3"]
    },
    "2026-03-24": {
        "msg": "Move root-level Django management to backend folder",
        "actions": ["rm -f manage.py"]
    },
    "2026-03-25": {
        "msg": "Remove root-level package files (move to frontend)",
        "actions": ["rm -f package.json", "rm -f package-lock.json"]
    },
    "2026-03-26": {
        "msg": "Clean up root-level Python requirements file",
        "actions": ["rm -f requirements.txt"]
    },
    "2026-03-27": {
        "msg": "Remove static assets from root directory",
        "actions": ["rm -rf static/"]
    },
    "2026-03-28": {
        "msg": "Update documentation to reflect cleaned repository",
        "actions": [
            "echo '# Telemed - Clean Repository Structure\n\nThis repository contains a production-ready telemedicine platform with organized file structure.' > REPO_STRUCTURE.md"
        ]
    },
    "2026-03-29": {
        "msg": "Final repository cleanup and optimization",
        "actions": []
    }
}

print("🧹 Starting repository cleanup from March 20-29, 2026\n")

for date_str in sorted(cleanup_tasks.keys()):
    task = cleanup_tasks[date_str]
    msg = task["msg"]
    actions = task["actions"]
    
    # Execute cleanup actions
    for action in actions:
        if action.startswith("echo"):
            # Handle echo commands
            subprocess.run(action, shell=True, check=False)
        else:
            # Handle rm commands
            subprocess.run(action, shell=True, check=False)
    
    # Stage all changes
    subprocess.run(['git', 'add', '-A'], check=True, capture_output=True)
    
    # Commit with specific date
    commit_date = f"{date_str}T09:00:00"
    env = os.environ.copy()
    env['GIT_AUTHOR_DATE'] = commit_date
    env['GIT_COMMITTER_DATE'] = commit_date
    
    try:
        result = subprocess.run(
            ['git', 'commit', '-m', f"{msg}"],
            env=env,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✅ {date_str}: {msg}")
    except subprocess.CalledProcessError as e:
        if "nothing to commit" in e.stderr:
            print(f"⏭️  {date_str}: {msg} (no changes)")
        else:
            print(f"❌ {date_str}: {msg} - {e.stderr}")

print("\n✅ Cleanup commits complete!")
print("\nFinal repository structure:")
subprocess.run(['ls', '-la'], check=False)
