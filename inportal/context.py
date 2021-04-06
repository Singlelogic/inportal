import os
from dotenv import load_dotenv


load_dotenv()

def footer_email(request):
    """Returns the email address specified in the site footer"""
    email = os.getenv('EMAIL')
    return {'footer_email': email}
