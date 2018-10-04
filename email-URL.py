import os
import sys
import imaplib
import getpass
import email
import requests

#To find URls in Download emails
def extract_URLs(M):

    #Finding unread emails with the subject D/download
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

        #Decoding ad saving messsage contents
        msg = email.message_from_string(data[0][1].decode('utf-8'))
        extracted.append(re.search("(?P<url>https?://[^\s]+)", msg.get_payload(),re.U).group("url"))
        
    return extracted


#Accessing email account
M = imaplib.IMAP4_SSL('imap.gmail.com')

try:
    M.login('USER@gmail.com', 'PASSWORD') #Using an app password is recommended
except imaplib.IMAP4.error: #On failure
    print("Login failed")

rv,data = M.select("INBOX")

if rv == 'OK':
    URLs = []
    URLs.extend(extract_URLs(M))
    M.close
M.logout

#Placing download location
os.chdir(os.path.expanduser("~")+"/Downloads/") #Only works on default download folder

if (URLs == []) :
    print('No URLs found')

for URL in URLs:
    URL = str(URL)
    #fetching data from url
    r = requests.get(URL)

    print(URL)
    
    if (r.status_code != 200) : #Checking for success
        print("^ Download failed ^")
    
    #finding file name at end of URL
    beginning = 0
    for c in range(len(URL)-1, 0, -1):
        beginning -= 1
        if URL[c] == "/":
            beginning += 1
            break

    #Saving downloaded file
    with open(URL[beginning: len(URL) + 1], 'wb') as f:
        f.write(r.content)
