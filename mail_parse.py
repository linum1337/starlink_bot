import imaplib
import email
from email.header import decode_header
import base64
from bs4 import BeautifulSoup
import re

mail_pass = "ejketwjlyowpgpgi"
username = "levokumkabilling1337@gmail.com"
imap_server = "imap.gmail.com"
imap = imaplib.IMAP4_SSL(imap_server)
print(imap.login(username, mail_pass))

# select the e-mails
res, messages = imap.select('"[Gmail]/Sent Mail"')
g = int(str(messages[0])[2:-1])
print(g)
# calculates the total number of sent messages
messages = int(messages[0])

# determine the number of e-mails to be fetched
n = g

# iterating over the e-mails
for i in range(messages, messages - n, -1):
    res, msg = imap.fetch(str(i), "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            msg = email.message_from_bytes(response[1])
            text = msg.get_payload()
            print(msg)
            # getting the sender's mail id
            From = msg["From"]

            # getting the subject of the sent mail
            subject = msg["Subject"]

            # printing the details
            print("From : ", From)
            print("subject : ", subject)