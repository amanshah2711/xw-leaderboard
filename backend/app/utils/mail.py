
import resend
import os
from flask import render_template

resend.api_key = os.getenv('RESEND_API_KEY')

def send_reset_email(reset_link, addressee):
    html_body = render_template('password_reset.html', reset_link=reset_link)
    resend.Emails.send({
    'from': 'XW Courier <pheidippides@updates.amanshah2711.me>',
    'to': [addressee],
    "subject": "[XWLeaderboard] Password Reset Request",
    'html': html_body,
})

def send_email_verification_email(verify_link, addressee):
    html_body = render_template('email_verification.html', verify_link=verify_link)
    resend.Emails.send({
    'from': 'XW Courier <pheidippides@updates.amanshah2711.me>',
    'to': [addressee],
    "subject": "[XWLeaderboard] Email Verification",
    'html': html_body,
})
    