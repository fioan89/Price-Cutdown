__author__ = 'fauri'

import smtplib
import socket

from sys import stderr

GMAIL_SMTP_HOST = 'smtp.gmail.com'
GMAIL_SMTP_PORT = 587


def recvline(sock):
    stop = 0
    line = ''
    while True:
        i = sock.recv(1)
        if i == '\n': stop = 1
        line += i
        if stop == 1:
            break
    return line


class ProxSMTP(smtplib.SMTP):
    def __init__(self, host='', port=0, p_address='', p_port=0, local_hostname=None,
                 timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        """Initialize a new instance.

        If specified, `host' is the name of the remote host to which to
        connect.  If specified, `port' specifies the port to which to connect.
        By default, smtplib.SMTP_PORT is used.  An SMTPConnectError is raised
        if the specified `host' doesn't respond correctly.  If specified,
        `local_hostname` is used as the FQDN of the local host.  By default,
        the local hostname is found using socket.getfqdn().

        """
        self.p_address = p_address
        self.p_port = p_port

        self.timeout = timeout
        self.esmtp_features = {}
        self.default_port = smtplib.SMTP_PORT
        if host:
            (code, msg) = self.connect(host, port)
            if code != 220:
                raise smtplib.SMTPConnectError(code, msg)
        if local_hostname is not None:
            self.local_hostname = local_hostname
        else:
            # RFC 2821 says we should use the fqdn in the EHLO/HELO verb, and
            # if that can't be calculated, that we should use a domain literal
            # instead (essentially an encoded IP address like [A.B.C.D]).
            fqdn = socket.getfqdn()
            if '.' in fqdn:
                self.local_hostname = fqdn
            else:
                # We can't find an fqdn hostname, so use a domain literal
                addr = '127.0.0.1'
                try:
                    addr = socket.gethostbyname(socket.gethostname())
                except socket.gaierror:
                    pass
                self.local_hostname = '[%s]' % addr
        smtplib.SMTP.__init__(self)

    def _get_socket(self, port, host, timeout):
        # This makes it simpler for SMTP_SSL to use the SMTP connect code
        # and just alter the socket connection bit.
        if self.debuglevel > 0: print>> stderr, 'connect:', (host, port)
        new_socket = socket.create_connection((self.p_address, self.p_port), timeout)
        new_socket.sendall("CONNECT {0}:{1} HTTP/1.1\r\n\r\n".format(port, host))
        for x in xrange(2): recvline(new_socket)
        return new_socket


class GmailPostMan():
    def __init__(self, gmail_username, gmail_password, proxy_address='', proxy_port=8080):
        self.gmail_username = gmail_username
        self.gmail_password = gmail_password

        if self.gmail_username.endswith('@gmail.com'):
            self.gmail_username = self.gmail_username.split('@')[0]
        self.email_from = '{0}@gmail.com'.format(self.gmail_username)
        self.smt_server = ProxSMTP(GMAIL_SMTP_HOST, GMAIL_SMTP_PORT, p_address=proxy_address, p_port=proxy_port)

    def send_to(self, subject='', message_body='', to=None):
        """
        Sends an email using the logged account with the specified subject and message body to the list of receivers.
        :param subject: a string subject title
        :param message_body: a string message body
        :param to: a list of addresses to send this mail to.  A bare
                             string will be treated as a list with 1 address.
        """
        header = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
                  % (self.email_from, ", ".join(to), subject))
        message = header + message_body + "\r\n"
        self.smt_server.ehlo()
        self.smt_server.starttls()
        self.smt_server.login(self.gmail_username, self.gmail_password)
        try:
            self.smt_server.sendmail(self.email_from, to, message)
        finally:
            self.smt_server.quit()
