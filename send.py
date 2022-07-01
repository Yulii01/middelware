import sys
from email.mime.text import MIMEText
from twisted.internet import reactor
from twisted.mail.smtp import sendmail
from twisted.python import log

log.startLogging(sys.stdout)
host = "localhost"
sender = "secretadmirer@example.com"
recipients = ["recipient@localhost"]
msg = MIMEText("""Violets are blue
aki estoy yo
""")
msg["Subject"] = "Roses are red"
msg["From"] = '"Secret Admirer" <%s>' % (sender,)
msg["To"] = ", ".join(recipients)

deferred = sendmail(host, sender, recipients, msg.as_bytes(), port=9090)
deferred.addBoth(lambda result: reactor.stop())
reactor.run()