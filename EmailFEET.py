import sys
import smtplib
import email.utils
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.multipart import MIMEBase
from email import Encoders
import time

SENDER = 'foo@bar.com'
SENDERNAME = 'Suraj Khetani'

RECIPIENT  = sys.argv[1]

USERNAME_SMTP = ""
PASSWORD_SMTP = "BGizKwz8iKdSpVIxz2mVvdLuA9385RcdDCLC4/PMVK7h"
HOST = ""
PORT = 587

# The subject line of the email.
SUBJECT = 'Amazon SES Test (Python smtplib)'

# The email body for recipients with non-HTML email clients.
BODY_TEXT = ("EmailFEET Filter Enumeration Test\r\n"
             "Interface using the Python smtplib package."
            )

# The HTML body of the email.
BODY_HTML = """<html>
<head></head>
<body>
  <h1>EmailFEET Filter Enumeration Test</h1>
  <p> Test </p>
</body>
</html>
            """

# Create message container - the correct MIME type is multipart/alternative.
#msg.add_header('X-SES-CONFIGURATION-SET',CONFIGURATION_SET)

# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(BODY_TEXT, 'plain')
part2 = MIMEText(BODY_HTML, 'html')

# Attach parts into message container.
# Attaching files

path = '/var/www/html/WebFEET/WebFEET0.6/payloads/'
files = os.listdir(path)
#length = len(files)
#part3 = MIMEBase('application', "octet-stream")

for f in files:
        #path_new = path + files[f]
        path_new = os.path.join(path, f)
        print (f)
        print (path_new)
        part3 = MIMEBase('application', "octet-stream")
        part3.set_payload(open(path_new, "rb").read())
        msg = MIMEMultipart('alternative')
        msg['Subject'] = SUBJECT
        msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
        msg['To'] = RECIPIENT
        msg.attach(part1)
        msg.attach(part2)
        Encoders.encode_base64(part3)
        part3.add_header('Content-Disposition', 'attachment; filename={}'.format(f))
        msg.attach(part3)
        try:
                server = smtplib.SMTP(HOST, PORT)
                server.ehlo()
                server.starttls()
                #stmplib docs recommend calling ehlo() before & after starttls()
                server.ehlo()
                server.login(USERNAME_SMTP, PASSWORD_SMTP)
                server.sendmail(SENDER, RECIPIENT, msg.as_string())
                server.close()
                print ("Email sent!")
        except Exception as e:
                print ("Error: ", e)
        time.sleep(2)
