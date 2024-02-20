import imaplib
import email
from email.header import decode_header
import re
import base64
import numpy as np
import warnings
import pickle
import time
import concurrent.futures
from colorama import Fore, Style
from feature import FeatureExtraction




ascii_art = r"""
╔═╗ ╔╗            ╔╗        ╔╗           ╔════╗     ╔╗      
║║╚╗║║            ║║        ║║           ╚══╗ ║    ╔╝╚╗     
║╔╗╚╝║╔══╗    ╔══╗║╚═╗╔╗╔══╗║╚═╗╔╗ ╔╗      ╔╝╔╝╔══╗╚╗╔╝╔══╗ 
║║╚╗║║║╔╗║    ║╔╗║║╔╗║╠╣║══╣║╔╗║║║ ║║     ╔╝╔╝ ║╔╗║ ║║ ╚ ╗║ 
║║ ║║║║╚╝║    ║╚╝║║║║║║║╠══║║║║║║╚═╝║    ╔╝ ╚═╗║║═╣ ║╚╗║╚╝╚╗
╚╝ ╚═╝╚══╝    ║╔═╝╚╝╚╝╚╝╚══╝╚╝╚╝╚═╗╔╝    ╚════╝╚══╝ ╚═╝╚═══╝
              ║║                ╔═╝║                        
              ╚╝                ╚══╝                        
"""

# Print the ASCII art in red
print(Fore.RED + ascii_art + Style.RESET_ALL)
def process_url(url):
    file = open("pickle/model.pkl","rb")
    gbc = pickle.load(file)
    file.close()

    obj = FeatureExtraction(url)
    x = np.array(obj.getFeaturesList()).reshape(1,30)

    y_pro_phishing = gbc.predict_proba(x)[0,0]
    return y_pro_phishing

def fetch_urls_from_email(msg_id, username, password):
    # Connect to the Gmail IMAP server
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(username, password)
    mail.select('inbox')  # Select the inbox or another folder

    # Fetch the email using the id
    _, msg_data = mail.fetch(msg_id, '(RFC822)')
    # Parse the email message
    msg = email.message_from_bytes(msg_data[0][1])

    # Extract URLs from the email body
    urls = set()
    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            payload = part.get_payload()
            # Decode payload if it's encoded with base64
            if part.get('Content-Transfer-Encoding') == 'base64':
                payload = base64.b64decode(payload)
                payload = payload.decode('utf-8', 'ignore')
            urls.update(re.findall(r'(https?://\S+)', payload))
    if len(urls):
        print(urls)
    return urls

def is_spam(urls):
    total_prob = 0
    num_urls = len(urls)
    if num_urls:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_url, url) for url in urls]
            for future in concurrent.futures.as_completed(futures):
                total_prob += future.result()
                print(total_prob)
        return total_prob / num_urls > 0.5
    else:
        return False

def scan_emails(username,password):
    # Connect to the Gmail IMAP server
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(username, password)
    mail.select('inbox')  # Select the inbox or another folder

    # Search for the most recent email
    status, messages = mail.search(None, 'ALL')
    if status == 'OK' and messages[0]:
        msg_ids = messages[0].split()[-1:]
        for msg_id in msg_ids:
            try:
                urls = fetch_urls_from_email(msg_id, username, password)
                if is_spam(urls):
                    # Move email to spam or trash
                    mail.store(msg_id, '+X-GM-LABELS', '\\Trash')
                    print("Email moved to trash")
                else:
                    print("Email not marked as spam")
            except Exception as e:
                print(f"Error processing email: {e}")

    else:
        print("No new emails")

    # Close the connection
    mail.logout()


username = input("Enter your Gmail email address: ")
password = input(f"Enter app password for {username}: ")
# Run the script in a loop to continuously scan for new emails for each user
while True:
    scan_emails(username,password)
    time.sleep(6)  # Check for new emails every minute