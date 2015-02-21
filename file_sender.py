""" Basic file sending to speed up my report generation at work """

# Base imports that make use of the email packages of Python 
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

""" Used for my personal reports because I tend to add the date in a YYYYMMDD format """
from datetime import date
today = date.today()
date_run = today.strftime('%Y%m%d')

emailfrom = "mnickey@abc.com"						# Who is this sent from?
emailto = "mnickey@abc.com"							# Who is this being sent to?
directory = "C:\Users\mnickey\Documents\Folder\\" 	# The folder that the files are in, \\ for windows machines
filename = "test"									# the name of the file without the extension (can be added if needed)
file_extension = ".csv"								# file extension if not used above
fileToSend = directory + filename + " " + date_run + file_extension
print fileToSend

msg = MIMEMultipart()
msg["From"] = emailfrom
msg["To"] = emailto
msg["Subject"] = "Scheduled reports"
msg.preamble = "Scheduled reports"

ctype, encoding = mimetypes.guess_type(fileToSend)
if ctype is None or encoding is not None:
    ctype = "application/octet-stream"

maintype, subtype = ctype.split("/", 1)

if maintype == "text":
    fp = open(fileToSend)
    # Note: we should handle calculating the charset
    attachment = MIMEText(fp.read(), _subtype=subtype)
    fp.close()
# elif maintype == "image":
#     fp = open(fileToSend, "rb")
#     attachment = MIMEImage(fp.read(), _subtype=subtype)
#     fp.close()
# elif maintype == "audio":
#     fp = open(fileToSend, "rb")
#     attachment = MIMEAudio(fp.read(), _subtype=subtype)
#     fp.close()
else:
    fp = open(fileToSend, "rb")
    attachment = MIMEBase(maintype, subtype)
    attachment.set_payload(fp.read())
    fp.close()
    encoders.encode_base64(attachment)
attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
msg.attach(attachment)

server = smtplib.SMTP("enter your sever here")
# server.starttls()
# server.login(username,password)
server.sendmail(emailfrom, emailto, msg.as_string())
server.quit()
