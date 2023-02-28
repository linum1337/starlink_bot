import email
import imaplib
from email.header import decode_header

import user_bd


def mail_parse(login):
    print('Mail parse is here!')

    imap_host = 'imap.gmail.com'
    imap_user = 'levokumkabilling1337@gmail.com'
    imap_pass = 'ejketwjlyowpgpgi'
    payload_arg = []
    fin_mail = []

    # connect to host using SSL
    imap = imaplib.IMAP4_SSL(imap_host)

    ## login to server
    imap.login(imap_user, imap_pass)

    imap.select('"[Gmail]/Sent Mail"')
    sav = ' '
    tmp, data = imap.search(None, 'ALL')
    for num in data[0].split():
        tmp, data = imap.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])
        bytes, encoding = decode_header(msg['subject'])[0]
        fin_subj = bytes.decode(encoding)
        if login in fin_subj:
            for part in msg.walk():
                payload = part.get_payload(decode=True)
                payload_arg.append((payload, fin_subj))
                imap.store(num, '+FLAGS', '\\Deleted')
        msg = email.message_from_bytes(data[0][1])

    for i in payload_arg:
        if login in i[1]:
            fin_mail.append(i)
    if len(fin_mail) != 0:
        return fin_mail[1][0].decode('utf-8')
    else:
        return fin_mail

