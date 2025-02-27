import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import markdown

def send_confirmation_email(name, email, topics, frequency):
    """
    Send a confirmation email to the new subscriber
    """
    try:
        # Email configuration
        sender_email = os.getenv('EMAIL_USER')
        if not sender_email:
            print("WARNING: EMAIL_USER not found in environment variables")
            sender_email = 'your-email@gmail.com'

        sender_password = os.getenv('EMAIL_PASSWORD')
        if not sender_password:
            print("WARNING: EMAIL_PASSWORD not found in environment variables")
            sender_password = 'your-app-password'
        print(f"Using email: {sender_email}")
        print(f"Password length: {len(sender_password)}")
        
        # Create message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = email
        message['Subject'] = "Welcome to Advosub Newsletter!"
        
        # Format topics as a comma-separated list
        topics_str = ", ".join(topics)
        
        # Email body
        body = f"""
        <html>
        <body>
            <h2>Welcome to Advosub Newsletter, {name}!</h2>
            <p>Thank you for subscribing to our newsletter. We're excited to have you join our community!</p>
            
            <h3>Your Subscription Details:</h3>
            <ul>
                <li><strong>Name:</strong> {name}</li>
                <li><strong>Email:</strong> {email}</li>
                <li><strong>Topics of Interest:</strong> {topics_str}</li>
                <li><strong>Frequency:</strong> {frequency.capitalize()}</li>
            </ul>
            
            <p>You'll start receiving our {frequency} newsletter with the latest updates on {topics_str}.</p>
            
            <p>If you have any questions or need to update your preferences, please reply to this email.</p>
            
            <p>Best regards,<br>
            The Advosub Team</p>
        </body>
        </html>
        """
        
        # Attach HTML content
        message.attach(MIMEText(body, 'html'))
        
        # Connect to Gmail SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(message)
        
        print(f"Confirmation email sent to {email}")
        return True
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        import traceback
        traceback.print_exc()
        return False 

def send_newsletter_email(name, email, topic, frequency, newsletter_content):
    """
    Send a newsletter email to the subscriber
    
    Args:
        name (str): Recipient's name
        email (str): Recipient's email address
        topic (str): Newsletter topic
        frequency (str): Newsletter frequency
        newsletter_content (str): Markdown content of the newsletter
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Debug environment variables
        print("Environment variables:")
        print(f"EMAIL_USER in env: {'EMAIL_USER' in os.environ}")
        print(f"EMAIL_PASSWORD in env: {'EMAIL_PASSWORD' in os.environ}")
        
        # Email configuration
        sender_email = os.getenv('EMAIL_USER')
        if not sender_email:
            print("WARNING: EMAIL_USER not found in environment variables")
            sender_email = 'your-email@gmail.com'

        sender_password = os.getenv('EMAIL_PASSWORD')
        if not sender_password:
            print("WARNING: EMAIL_PASSWORD not found in environment variables")
            sender_password = 'your-app-password'
        print(f"Using email: {sender_email}")
        print(f"Password length: {len(sender_password)}")
        
        # Create message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = email
        message['Subject'] = f"Your {frequency.capitalize()} Newsletter on {topic}"
        
        # Convert markdown to HTML
        html_content = markdown.markdown(newsletter_content)
        
        # Email body
        body = f"""
        <html>
        <body>
            <h2>Hello {name}!</h2>
            <p>Here's your {frequency} newsletter on {topic}:</p>
            
            <div style="margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
                {html_content}
            </div>
            
            <p>You're receiving this because you subscribed to our {frequency} newsletter on {topic}.</p>
            
            <p>If you have any questions or need to update your preferences, please reply to this email.</p>
            
            <p>Best regards,<br>
            The Advosub Team</p>
        </body>
        </html>
        """
        
        # Attach HTML content
        message.attach(MIMEText(body, 'html'))
        
        # Connect to Gmail SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(message)
        
        print(f"Newsletter email sent to {email}")
        return True
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        import traceback
        traceback.print_exc()
        return False 