import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_confirmation_email(name, email, topics, frequency):
    """
    Send a confirmation email to the new subscriber
    """
    try:
        # Email configuration
        sender_email = os.environ.get('EMAIL_USER', 'your-email@gmail.com')  # Set this in environment variables
        sender_password = os.environ.get('EMAIL_PASSWORD', 'your-app-password')  # Set this in environment variables
        
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