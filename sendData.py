import json
import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, COMMASPACE
from os.path import basename

path = './logs/'

#Type here your email and password to get this faster
email = ""
password = ""

def getAllData():
    dataset = []
    filenames = []
    for f in os.listdir(path):
        if f.startswith('classified_profiles_'):
            try:
                with open(os.path.join(path, f), 'r') as t:
                    # print(t.read())
                    d = json.loads(t.read())
                    # print(d)
                for o in d:
                    if 'username' in list(o.keys()):
                        dataset.append(o)
                filenames.append(f)
            except Exception as e:
                print('{} - Skipping {}'.format(str(e), f))
    return filenames, dataset


def pack(d):
    with open(path+'tmp_to_send.json', 'w') as f:
        json.dump(d, f)
    return path+'tmp_to_send.json'


def sendEmail(send_from, psw, send_to=['contact.timgrossmann@gmail.com'],
              subject='instapy-gender-classification: Logs',
              text='Hi there,\n\tThis is my contribution to instapy gender classification', datalen=None,
              files=None, server='smtp.gmail.com', port=587):
        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = COMMASPACE.join(send_to)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject

        if datalen:
            text = text + " with {} user classified".format(datalen)
        msg.attach(MIMEText(text))

        for f in files or []:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(f)
                )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)

        smtp = smtplib.SMTP(server, port)
        smtp.starttls()
        smtp.login(send_from, psw)
        problems = smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.quit()


def deleteFileList(list_of_filenames):
    print("Cleaning up ...")
    for x in list_of_filenames:
        os.remove(os.path.join(path, x))
    os.rename(os.path.join(path+'tmp_to_send.json'), os.path.join(path, 'tmp_to_send.json.backup'))


if __name__ == '__main__':
    try:
        print("Looking for the files ...")
        list_of_filenames, data = getAllData()
        if len(data) == 0:
            raise Exception("Dataset empty - run the script to classify some usernames")
        print("Compressing ... ")
        filename = pack(data)
        if len(email) == 0 or len(password) == 0:
            email = input("Insert your email: ")
            password = input("Insert your password: ")
        if not email.endswith('gmail.com'):
            raise Exception("This feature available only with gmail - restart this script providing one")
        print("Sending email ...")
        sendEmail(email, password, files=[filename], datalen=len(data))
        print("All done ...")
        deleteFileList(list_of_filenames)
    except Exception as e:
        print("An error occurred: ", str(e))
