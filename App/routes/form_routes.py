from flask import Blueprint, render_template, request, redirect, url_for, flash
from App.services.submission_service import save_submission
from App.services.perplexity_service import get_news_for_topic
from App.services.newsletter_services import generate_newsletter
from App.services.email_service import send_newsletter_email
import json
import time

form_bp = Blueprint('form', __name__)

@form_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Debug: Print all form data
            print("Form data received:", request.form)
            
            # Get form data
            name = request.form.get('name')
            email = request.form.get('email')
            topic = request.form.get('topic', '')
            frequency = request.form.get('frequency')
            
            print("Topic received:", topic)
            
            # Validate required fields
            if not name or not email or not topic or not frequency:
                return render_template('mainpage.html', error="All fields are required")
            
            # 1. Save submission to JSON
            submission = {
                'name': name,
                'email': email,
                'topic': topic.strip(),
                'frequency': frequency
            }
            
            print("Saving submission:", json.dumps(submission, indent=2))
            save_result = save_submission(submission)
            print("Save result:", save_result)
            
            # 2. Get news articles for the topic
            print(f"Fetching news for topic: {topic}")
            news_results = get_news_for_topic(topic)
            print(f"Found {len(news_results)} news articles")
            
            # 3. Generate newsletter content
            print("Generating newsletter content")
            newsletter_content = generate_newsletter(news_results)
            print("Newsletter generated successfully")
            
            # 4. Send email with newsletter
            print(f"Sending newsletter to {email}")
            email_result = send_newsletter_email(name, email, topic, frequency, newsletter_content)
            
            if not email_result:
                return render_template('mainpage.html', error="Failed to send the newsletter email. Please try again.")
            
            return render_template('mainpage.html', success=True)
            
        except Exception as e:
            # Log the error in a production environment
            print(f"Error processing submission: {str(e)}")
            import traceback
            traceback.print_exc()
            return render_template('mainpage.html', error="An error occurred while processing your submission")
    
    return render_template('mainpage.html')