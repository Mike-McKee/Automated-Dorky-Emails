from __future__ import print_function
import os

import base64
from email.message import EmailMessage
from google_auth_oauthlib.flow import InstalledAppFlow
import google.auth
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from get_random_item import get_random_item

import EMAILS

def gmail_send_message():
    """Create and insert a draft email.
       Print the returned draft's message and id.
       Returns: Draft object, including draft id and message meta data.

      Load pre-authorized user credentials from the environment.
      TODO(developer) - See https://developers.google.com/identity
      for guides on implementing OAuth2 for the application.
    """
    sender = EMAILS.SENDER
    recipient = EMAILS.RECIPIENT

    # Have to change the order of these based on the list get_random_item() returns
    message_contents = get_random_item()
    title = message_contents[4]
    date = message_contents[1]
    summary = message_contents[3]
    link = message_contents[2]

    # flow = InstalledAppFlow.from_client_secrets_file('GOOGLE_SECRETS/credentials.json', SCOPES)
    # creds = flow.run_local_server()
    SCOPES = ['https://www.googleapis.com/auth/gmail.compose']
    creds = Credentials.from_authorized_user_file('SECRETS/token.json', SCOPES)

    try:
        # create gmail api client
        service = build('gmail', 'v1', credentials=creds)

        message = EmailMessage()

        message_html = f"""
        <html>
        <body>
            <p>Good morning you beautiful boy!<br><br>
            You ready to learn something today? Here's what I've got for ya...<br><br>
            <strong>Title:</strong> {title}<br>
            <strong>Date:</strong> {date}<br>
            <strong>Summary:</strong> {summary}<br>
            <strong>Link:</strong> <a href="{link}">{link}</a><br><br>
            Enjoy your reading!</p>
        </body>
        </html>
        """

        message.set_content(f'''Good morning you beautiful boy!\n\nYou ready to learn something today? Here's what I've got for ya...\n\nTitle: {title}\n\nDate: {date}\n\nSummary: {summary}\n\nLink: {link}\n\nEnjoy your reading!''')
        message.add_alternative(message_html,subtype='html')

        message['To'] = recipient
        message['From'] = sender
        message['Subject'] = 'A studious email for a studious dork'

        raw_message = message.as_bytes()
        encoded_message = base64.urlsafe_b64encode(raw_message).decode()

        create_message = {
                'raw': encoded_message
            }

        # pylint: disable=E1101
        send_message = service.users().messages().send(userId="me",body=create_message).execute()

        print("=========================EMAIL SUCCESSFULLY SENT=========================")

    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None

    return send_message


if __name__ == '__main__':
    gmail_send_message()