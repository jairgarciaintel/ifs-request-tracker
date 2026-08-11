"""
Convert requests.xlsx (exported from SharePoint) to requests.json
Then auto-push to GitHub.

Usage:
    python convert_excel.py
"""
import openpyxl
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

REPO_DIR = Path(__file__).parent
DATA_DIR = REPO_DIR / 'data'
EXCEL_FILE = DATA_DIR / 'requests.xlsx'
JSON_FILE = DATA_DIR / 'requests.json'


def convert():
    if not EXCEL_FILE.exists():
        print(f"Error: {EXCEL_FILE} not found")
        sys.exit(1)

    wb = openpyxl.load_workbook(str(EXCEL_FILE))
    ws = wb.active
    headers = [cell.value for cell in ws[1]]
    
    rows = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        item = dict(zip(headers, row))
        if item.get('ID') is None:
            continue
        rows.append({
            'id': item['ID'],
            'requestType': item.get('Request Type') or 'Unknown',
            'customer': item.get('Company') or item.get('Project/Portal Name') or '',
            'requestor': item.get('Created By') or '',
            'created': str(item.get('Created') or ''),
            'status': item.get('iGO Admin Only - Status') or '',
            'engagementType': item.get('Engagement Type') or '',
            'priority': item.get('Priority') or '',
            'projectName': item.get('Project/Portal Name') or ''
        })
    
    with open(str(JSON_FILE), 'w') as f:
        json.dump(rows, f, indent=2, default=str)
    
    print(f"Converted {len(rows)} requests -> {JSON_FILE}")
    return len(rows)


def git_push():
    git = 'git'
    git_win = Path(r'C:\Program Files\Git\bin\git.exe')
    if git_win.exists():
        git = str(git_win)

    # Read token from .env
    env_file = REPO_DIR / '.env'
    token = ''
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith('GITHUB_TOKEN='):
                token = line.split('=', 1)[1].strip()

    if token:
        remote = f'https://jairgarciaintel:{token}@github.com/jairgarciaintel/ifs-request-tracker.git'
        subprocess.run([git, 'remote', 'set-url', 'origin', remote], cwd=str(REPO_DIR), capture_output=True)

    subprocess.run([git, 'add', 'data/'], cwd=str(REPO_DIR), capture_output=True)
    
    msg = f'Sync: {datetime.now().strftime("%Y-%m-%d %H:%M")}'
    result = subprocess.run([git, 'commit', '-m', msg], cwd=str(REPO_DIR), capture_output=True, text=True)
    
    if 'nothing to commit' in (result.stdout + result.stderr):
        print('No changes to push.')
        return

    push = subprocess.run([git, 'push'], cwd=str(REPO_DIR), capture_output=True, text=True)
    if push.returncode == 0:
        print('Pushed to GitHub. Page updates in ~1 min.')
    else:
        print(f'Push failed: {push.stderr}')


if __name__ == '__main__':
    print("=" * 40)
    print("IFS Request Tracker - Excel to JSON")
    print("=" * 40)
    convert()
    print("\nPushing to GitHub...")
    git_push()
    print(f"\nDone! https://jairgarciaintel.github.io/ifs-request-tracker/")
