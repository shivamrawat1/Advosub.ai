from flask import Blueprint, render_template, request, redirect, url_for
from App.services.submission_service import save_submission

form_bp = Blueprint('form', __name__)

@form_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        submission = {
            'name': request.form['name'],
            'email': request.form['email'],
            'topics': request.form['topics']
        }
        save_submission(submission)
        return redirect(url_for('form.index'))
    
    return render_template('mainpage.html') 