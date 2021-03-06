import sys
from email.header import Header
from zope.interface import implementer
from twisted.internet import defer, reactor
from twisted.mail import smtp
from twisted.python import log

@implementer(smtp.IMessageDelivery)
class StdoutMessageDelivery(object):
    
    def __init__(self, protocol):
        self.protocol = protocol
    def receivedHeader(self, helo, origin, recipients):
        clientHostname, _ = helo
        myHostname = self.protocol.transport.getHost().host
        headerValue = "from %s by %s with ESMTP ; %s" % (
        clientHostname, myHostname, smtp.rfc822date())
        return "Received: %s" % Header(headerValue)
    def validateFrom(self, helo, origin):
    # Accept any sender.
        return origin
    def validateTo(self, user):
        print(user.dest.domain.decode('utf-8'))
    # Accept recipients @localhost.
        if user.dest.domain.decode('utf-8') == "localhost":
            return StdoutMessage
        else:
            log.msg("Received email for invalid recipient %s" % user)
            raise smtp.SMTPBadRcpt(user)

@implementer(smtp.IMessage)
class StdoutMessage(object):
  
    def __init__(self):
        self.lines = []
    def lineReceived(self, line):
        if(type(line)==str):
            line =line
        else:
            line = line.decode("utf-8")    
        self.lines.append(line)
    def eomReceived(self):
        print ("New message received:")
        
        print ("\n".join(self.lines))
        self.lines = None
        return defer.succeed(None)

class StdoutSMTPFactory(smtp.SMTPFactory):
    def buildProtocol(self, addr):
        proto = smtp.ESMTP()
        proto.delivery = StdoutMessageDelivery(proto)
        return proto

log.startLogging(sys.stdout)
reactor.listenTCP(9090, StdoutSMTPFactory())
reactor.run()            