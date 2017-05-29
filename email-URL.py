import os
import sys
import imaplib
import getpass
import email
import requests

#to find URls in Download emails
def extract_URLs(M):

    #finding unread emails with the subject D/download
    rv, data = M.search(None, 'UNSEEN SUBJECT', 'Download' or 'download')
    if rv != 'OK':
      print("No messages found!")
      return

    extracted = []

    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print("ERROR getting message", num)
            return

        #decoding ad saving messsage contents
        msg = email.message_from_string(data[0][1].decode('utf-8'))
        extracted.append(msg.get_payload())
        
    return extracted


#accessing email account
M = imaplib.IMAP4_SSL('imap.gmail.com')

try:
    M.login('USER@gmail.com', 'PASSWORD') #using an app password is recommended
except imaplib.IMAP4.error:
    print("LOGIN FAILED!!! ")

rv,data = M.select("INBOX")

if rv == 'OK':
    URLs = []
    URLs.extend(extract_URLs(M))
    M.close
M.logout

#Placing download location
user = getpass.getuser()
if (sys.platform == 'darwin') : #mac computer
    os.chdir('/Users/' + user + '/Downloads/')
elif (sys.platform == 'win32' or sys.platform == 'windows') : #windows
    os.chdir('C:\\users\\' + user + '\\downloads\\')

if (URLs == []) :
    print('No URLs found')

for URL in URLs:
    #reformatting URL and downloading file
    edited = URL.replace('=\r\n', '')
    edited = edited.strip()
    r = requests.get(edited)

    print(edited)
    
    if (r.status_code != 200) : #checking for success
        print("^ Download failed ^")
    
    #finding file name at end of URL
    beginning = 0
    for c in range(len(edited)-1, 0, -1):
        beginning -= 1
        if edited[c] == "/":
            beginning += 1
            break

    #saving downloaded file
    with open(edited[beginning: len(edited) + 1], 'wb') as f:
        f.write(r.content)
