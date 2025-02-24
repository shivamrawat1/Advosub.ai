import json
from pathlib import Path

def save_submission(data):
    file_path = Path('submissions.json')
    
    if file_path.exists():
        with open(file_path, 'r') as f:
            submissions = json.load(f)
    else:
        submissions = []
    
    submissions.append(data)
    
    with open(file_path, 'w') as f:
        json.dump(submissions, f, indent=4) 