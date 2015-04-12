#!/usr/bin/python

# Usage: python send.py "/path/to/the/file.any"
 
# Import smtplib for the actual sending function
import smtplib
 
# For guessing MIME type
import mimetypes
 
# Import the email modules we'll need
import email
import email.mime.application
 
#Import sys to deal with command line arguments
import sys
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-b", "--body", dest="body",
                  type="string", default="empty body",
                  help="EMail body", metavar="body")
parser.add_option("-s", "--subject", dest="subject",
                  type="string", default="empty subject",
                  help="EMail subject", metavar="subject")
parser.add_option("-f", "--file", dest="file",
                  type="string", default="",
                  help="file to attach to EMail", metavar="file")

(options, args) = parser.parse_args()
 
# Create a text/plain message
msg = email.mime.Multipart.MIMEMultipart()
msg['Subject'] = options.subject
msg['From'] = 'thomas.gfuelner@gmail.com'
msg['To'] = 'thomas.gfuelner@gmail.com'
 
# The main body is just another attachment
body = email.mime.Text.MIMEText(options.body)
msg.attach(body)
 
if options.file != "":
	# PDF attachment block code
		 
	directory=sys.argv[1]
		 
	# Split de directory into fields separated by / to substract filename
		 
	spl_dir=directory.split('/')
		 
	# We attach the name of the file to filename by taking the last
	# position of the fragmented string, which is, indeed, the name
	# of the file we've selected
		 
	filename=spl_dir[len(spl_dir)-1]
		 
	# We'll do the same but this time to extract the file format (pdf, epub, docx...)
	 
	spl_type=directory.split('.')
		 
	type=spl_type[len(spl_type)-1]
		 
	fp=open(directory,'rb')
	att = email.mime.application.MIMEApplication(fp.read(),_subtype=type)
	fp.close()
	att.add_header('Content-Disposition','attachment',filename=filename)
	msg.attach(att)
 
# send via Gmail server
# NOTE: my ISP, Centurylink, seems to be automatically rewriting
# port 25 packets to be port 587 and it is trashing port 587 packets.
# So, I use the default port 25, but I authenticate.
s = smtplib.SMTP('smtp.gmail.com:587')
s.starttls()
s.login('thomas.gfuellner@gmail.com','Googlepwd')
s.sendmail('thomas.gfuellner@gmail.com',['thomas.gfuellner@gmail.com'], msg.as_string())
s.quit()
