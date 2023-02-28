import email
import imaplib
import user_bd
import schedule
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
        if str(user_bd.user_search(login)[3]) in msg['subject']:
            for part in msg.walk():
                payload = part.get_payload(decode=True)
                payload_arg.append((payload, msg['subject']))
                imap.store(num, '+FLAGS', '\\Deleted')
            msg = email.message_from_bytes(data[0][1])

    for i in payload_arg:
        if str(user_bd.user_search(login)[3]) in i[1] and (i[0] != None) and ('dir' not in i[0].decode('utf-8')):
            print(i)
            fin_mail.append(i)
    imap.close()
    return fin_mail
