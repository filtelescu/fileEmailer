import os
import time 
import sys
from string import Template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import stat


# you would fill in myAddress + myPassword with your email and your google app password (for gmail use)

myAddress = 'insert email here'
myPassword = 'insert google app pasword here'

print("\n")
print("-" * 80) 
print("project initiated")
print("-" * 80)
print("\n")

path_to_watch = "C:/Users/Binary/Desktop/fileEmailer/listenHere"
before = dict ([(f, None) for f in os.listdir (path_to_watch)])
while 1:
    time.sleep (5)
    after = dict ([(f, None) for f in os.listdir (path_to_watch)])
    added = [f for f in after if not f in before]
    removed = [f for f in before if not f in after]

    if added: 
        print("Added: ", ", ".join(added))

        # this takes away all non-essential parts of the file being added so only the name is left
        # this way the attachment is able to change based on what I save and can constantly run in the background
        # otherwise I would have to manually input the file I want emailed, taking x amount of time
        # which defeats the purpose of sending a file "quickly"

        noSpace = str(added)
        finalFileName = noSpace
        finalNameTwo = finalFileName.replace("'", "")
        finalNameThree = finalNameTwo.replace("[", "")
        finaleNameFour = finalNameThree.replace("]", "")
        finalNameFive = finaleNameFour.split(",", 1)
        finalWordFile = finalNameFive[0]

        print("sending file: " + finalWordFile)
        

        # I used these print statements to help me determine where the program was listening

        # print("Working in: " + os.getcwd() + "\n")
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        os.chdir('C:/Users/Binary/Desktop/fileEmailer/listenHere')
        # print("Updated: now working in: " + os.getcwd() + "\n")



        # the actual mail sending part of the code

        def getContacts(filename):
            names = []
            emails = []
            with open(filename, mode='r', encoding='utf-8') as contactsFile:
                for aContact in contactsFile:
                    names.append(aContact.split()[0])
                    emails.append(aContact.split()[1])
            return names,emails

        def readTemplate(filename):
            with open(filename, 'r', encoding='utf-8') as templateFile:
                templateFileContent = templateFile.read()
            return Template(templateFileContent)  

        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login(myAddress, myPassword)

        names, emails = getContacts('contacts.txt')
        messageTemplate = readTemplate('message.txt')



        for name, email in zip(names, emails):
            

            msg = MIMEMultipart()
            message = messageTemplate.substitute(PERSON_NAME=name.title())

            msg['From'] = myAddress
            msg['To'] = email
            msg['Subject'] = "Your backup"

            os.chmod("C:/Users/Binary/Desktop/fileEmailer", stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
            msg.attach(MIMEText(message, 'plain'))
            filename = finalWordFile
            attachment = open(finalWordFile, 'rb')

            p = MIMEBase('application', 'octet-stream')
            p.set_payload((attachment).read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', 'attachment; filename = %s' %filename)
            msg.attach(p)

            s.send_message(msg)
            
            del msg 

            print("Backup saved")

        

    before = after
