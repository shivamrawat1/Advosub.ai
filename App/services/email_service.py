import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import markdown
import re

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
        message['Subject'] = "Welcome to Advosub Newsletter! 🎉"
        
        # Format topics as a comma-separated list
        topics_str = ", ".join(topics)
        
        # Email body with improved styling
        body = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: 'Helvetica Neue', Arial, sans-serif;
                    line-height: 1.6;
                    color: #333333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .container {{
                    background-color: #ffffff;
                    border-radius: 8px;
                    padding: 30px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    padding-bottom: 20px;
                    border-bottom: 2px solid #f0f0f0;
                    margin-bottom: 20px;
                }}
                h1, h2, h3 {{
                    color: #2c3e50;
                }}
                h1 {{
                    font-size: 28px;
                    margin-bottom: 10px;
                }}
                h2 {{
                    font-size: 24px;
                    margin-top: 25px;
                }}
                h3 {{
                    font-size: 18px;
                    margin-top: 20px;
                }}
                .details {{
                    background-color: #f9f9f9;
                    border-left: 4px solid #3498db;
                    padding: 15px;
                    margin: 20px 0;
                    border-radius: 4px;
                }}
                ul {{
                    padding-left: 20px;
                }}
                li {{
                    margin-bottom: 8px;
                }}
                .footer {{
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #f0f0f0;
                    font-size: 14px;
                    color: #7f8c8d;
                    text-align: center;
                }}
                .button {{
                    display: inline-block;
                    background-color: #3498db;
                    color: white;
                    text-decoration: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    margin-top: 15px;
                }}
                .highlight {{
                    color: #3498db;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to Advosub Newsletter! 🎉</h1>
                    <p>Your source for important advocacy updates</p>
                </div>
                
                <p>Hello <span class="highlight">{name}</span>,</p>
                
                <p>Thank you for subscribing to our newsletter. We're excited to have you join our community of advocates who care about making a difference!</p>
                
                <div class="details">
                    <h3>Your Subscription Details:</h3>
                    <ul>
                        <li><strong>Name:</strong> {name}</li>
                        <li><strong>Email:</strong> {email}</li>
                        <li><strong>Topics of Interest:</strong> {topics_str}</li>
                        <li><strong>Frequency:</strong> {frequency.capitalize()}</li>
                    </ul>
                </div>
                
                <p>You'll start receiving our <span class="highlight">{frequency}</span> newsletter with the latest updates on <span class="highlight">{topics_str}</span>.</p>
                
                <p>Stay tuned for important news, action items, and ways to get involved with causes that matter to you.</p>
                
                <p>If you have any questions or need to update your preferences, please don't hesitate to reach out.</p>
                
                <div class="footer">
                    <p>Best regards,<br>
                    The Advosub Team</p>
                    <p>© 2023 Advosub. All rights reserved.</p>
                </div>
            </div>
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

def enhance_markdown_for_email(markdown_content):
    """
    Enhance markdown content for better email display
    
    Args:
        markdown_content (str): Original markdown content
        
    Returns:
        str: Enhanced HTML content
    """
    # Convert markdown to HTML
    html_content = markdown.markdown(markdown_content, extensions=['extra'])
    
    # Add custom styling for specific elements
    html_content = html_content.replace('<h1>', '<h1 style="color:#2c3e50; border-bottom: 2px solid #f0f0f0; padding-bottom: 10px;">')
    html_content = html_content.replace('<h2>', '<h2 style="color:#2c3e50; margin-top: 25px; border-bottom: 1px solid #f0f0f0; padding-bottom: 5px;">')
    html_content = html_content.replace('<h3>', '<h3 style="color:#3498db; margin-top: 20px;">')
    html_content = html_content.replace('<ul>', '<ul style="padding-left: 20px;">')
    html_content = html_content.replace('<li>', '<li style="margin-bottom: 8px;">')
    html_content = html_content.replace('<a ', '<a style="color:#3498db; text-decoration: none;" ')
    html_content = html_content.replace('<blockquote>', '<blockquote style="border-left: 4px solid #3498db; padding-left: 15px; margin-left: 0; color: #555;">')
    
    # Add horizontal rule styling
    html_content = html_content.replace('<hr>', '<hr style="border: none; height: 1px; background-color: #f0f0f0; margin: 25px 0;">')
    
    return html_content

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
        message['Subject'] = f"📰 Your {frequency.capitalize()} Newsletter on {topic}"
        
        # Convert and enhance markdown to HTML
        html_content = enhance_markdown_for_email(newsletter_content)
        
        # Email body with improved styling
        body = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: 'Helvetica Neue', Arial, sans-serif;
                    line-height: 1.6;
                    color: #333333;
                    max-width: 650px;
                    margin: 0 auto;
                    padding: 0;
                    background-color: #f9f9f9;
                }}
                .container {{
                    background-color: #ffffff;
                    border-radius: 8px;
                    padding: 30px;
                    margin: 20px auto;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    padding-bottom: 20px;
                    border-bottom: 2px solid #f0f0f0;
                    margin-bottom: 20px;
                }}
                .newsletter-container {{
                    background-color: #ffffff;
                    padding: 25px;
                    border-radius: 5px;
                    margin: 20px 0;
                    border: 1px solid #f0f0f0;
                }}
                h1, h2, h3 {{
                    color: #2c3e50;
                }}
                h1 {{
                    font-size: 26px;
                    margin-bottom: 10px;
                }}
                .footer {{
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #f0f0f0;
                    font-size: 14px;
                    color: #7f8c8d;
                    text-align: center;
                }}
                .highlight {{
                    color: #3498db;
                    font-weight: bold;
                }}
                .date {{
                    color: #7f8c8d;
                    font-size: 14px;
                    text-align: right;
                    margin-bottom: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{topic} Newsletter</h1>
                    <p>Your {frequency} update on important developments</p>
                    <div class="date">{get_current_date()}</div>
                </div>
                
                <p>Hello <span class="highlight">{name}</span>,</p>
                
                <p>Here's your {frequency} newsletter on <span class="highlight">{topic}</span>:</p>
                
                <div class="newsletter-container">
                    {html_content}
                </div>
                
                <p>We hope you found this information valuable. Stay informed and engaged!</p>
                
                <div class="footer">
                    <p>You're receiving this because you subscribed to our {frequency} newsletter on {topic}.</p>
                    <p>If you have any questions or need to update your preferences, please reply to this email.</p>
                    <p>Best regards,<br>
                    The Advosub Team</p>
                    <p>© 2023 Advosub. All rights reserved.</p>
                </div>
            </div>
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

def get_current_date():
    """Return the current date in a formatted string"""
    from datetime import datetime
    return datetime.now().strftime("%B %d, %Y") 