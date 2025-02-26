import json
import os
from pathlib import Path
import traceback

def save_submission(data):
    try:
        file_path = Path('submissions.json')
        print(f"Saving to file: {file_path.absolute()}")
        
        # Initialize with empty array if file doesn't exist or is empty
        if not file_path.exists() or os.path.getsize(file_path) == 0:
            print("File doesn't exist or is empty, initializing with empty list")
            submissions = []
        else:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    print(f"Read content from file: {content[:100]}...")
                    submissions = json.loads(content)
                    print(f"Loaded {len(submissions)} existing submissions")
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {str(e)}")
                submissions = []
        
        # Ensure submissions is a list
        if not isinstance(submissions, list):
            print(f"Submissions is not a list, it's a {type(submissions)}")
            submissions = []
        
        # Ensure we're storing a single topic instead of an array of topics
        if 'topics[]' in data:
            data['topic'] = data.pop('topics[]')[0] if isinstance(data['topics[]'], list) else data.pop('topics[]')
        
        submissions.append(data)
        print(f"Added new submission, now have {len(submissions)} submissions")
        
        with open(file_path, 'w') as f:
            json_data = json.dumps(submissions, indent=4)
            f.write(json_data)
            print(f"Wrote {len(json_data)} bytes to {file_path}")
        
        # Verify the file was written
        if file_path.exists():
            size = os.path.getsize(file_path)
            print(f"File exists after write, size: {size} bytes")
        else:
            print("Warning: File doesn't exist after write!")
        
        return True
    except Exception as e:
        print(f"Error in save_submission: {str(e)}")
        traceback.print_exc()
        raise 