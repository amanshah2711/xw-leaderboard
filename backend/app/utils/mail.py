
import resend
import os
from flask import render_template
from ..utils import frontend_url
from ..utils.encryption import generate_token
from ..utils.encryption import email_verify_salt

resend.api_key = os.getenv('RESEND_API_KEY')

def send_reset_email(reset_link, addressee):
    html_body = render_template('password_reset.html', reset_link=reset_link)
    return email_wrapper(addressee=addressee, body=html_body)

def send_email_verification_email(verify_link, addressee):
    html_body = render_template('email_verification.html', verify_link=verify_link)
    return email_wrapper(addressee=addressee, body=html_body)

def create_and_send_verification_email(addressee, id):
        token = generate_token({'addressee' : addressee, 'id' : id}, email_verify_salt)
        verify_url = frontend_url + '/api/verify-email/' + token
        return send_email_verification_email(verify_link=verify_url, addressee=addressee)
    
def email_wrapper(addressee, body):
    try:
        value = resend.Emails.send({
            'from': 'XW Courier <pheidippides@updates.amanshah2711.me>',
            'to': [addressee],
            "subject": "[XWLeaderboard] Email Verification",
            'html': body,
        }) 
        return True, str(value)    
    except Exception as e:
        return False, f'Failed to send email {e}' 
         


     