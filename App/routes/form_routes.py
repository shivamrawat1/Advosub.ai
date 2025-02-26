from flask import Blueprint, render_template, request, redirect, url_for, flash
from App.services.submission_service import save_submission
import json

form_bp = Blueprint('form', __name__)

@form_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Debug: Print all form data
            print("Form data received:", request.form)
            
            # Get the single topic (interest) from the form
            topic = request.form.get('topic', '')
            print("Topic received:", topic)
            
            # Validate required fields
            if not request.form.get('name') or not request.form.get('email') or not request.form.get('frequency'):
                return render_template('mainpage.html', error="All fields are required")
            
            submission = {
                'name': request.form.get('name'),
                'email': request.form.get('email'),
                'topic': topic.strip(),
                'frequency': request.form.get('frequency')
            }
            
            print("Saving submission:", json.dumps(submission, indent=2))
            result = save_submission(submission)
            print("Save result:", result)
            
            return render_template('mainpage.html', success=True)
        except Exception as e:
            # Log the error in a production environment
            print(f"Error saving submission: {str(e)}")
            import traceback
            traceback.print_exc()
            return render_template('mainpage.html', error="An error occurred while saving your submission")
    
    return render_template('mainpage.html')