#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
#// 
#// PHPMailer - PHP email creation and transport class.
#// PHP Version 5
#// @package PHPMailer
#// @link https://github.com/PHPMailer/PHPMailer/ The PHPMailer GitHub project
#// @author Marcus Bointon (Synchro/coolbru) <phpmailer@synchromedia.co.uk>
#// @author Jim Jagielski (jimjag) <jimjag@gmail.com>
#// @author Andy Prevost (codeworxtech) <codeworxtech@users.sourceforge.net>
#// @author Brent R. Matzelle (original founder)
#// @copyright 2012 - 2014 Marcus Bointon
#// @copyright 2010 - 2012 Jim Jagielski
#// @copyright 2004 - 2009 Andy Prevost
#// @license http://www.gnu.org/copyleft/lesser.html GNU Lesser General Public License
#// @note This program is distributed in the hope that it will be useful - WITHOUT
#// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#// FITNESS FOR A PARTICULAR PURPOSE.
#// 
#// 
#// PHPMailer - PHP email creation and transport class.
#// @package PHPMailer
#// @author Marcus Bointon (Synchro/coolbru) <phpmailer@synchromedia.co.uk>
#// @author Jim Jagielski (jimjag) <jimjag@gmail.com>
#// @author Andy Prevost (codeworxtech) <codeworxtech@users.sourceforge.net>
#// @author Brent R. Matzelle (original founder)
#//
class PHPMailer():
    #// 
    #// The PHPMailer Version number.
    #// @var string
    #//
    Version = "5.2.27"
    #// 
    #// Email priority.
    #// Options: null (default), 1 = High, 3 = Normal, 5 = low.
    #// When null, the header is not set at all.
    #// @var integer
    #//
    Priority = None
    #// 
    #// The character set of the message.
    #// @var string
    #//
    CharSet = "iso-8859-1"
    #// 
    #// The MIME Content-type of the message.
    #// @var string
    #//
    ContentType = "text/plain"
    #// 
    #// The message encoding.
    #// Options: "8bit", "7bit", "binary", "base64", and "quoted-printable".
    #// @var string
    #//
    Encoding = "8bit"
    #// 
    #// Holds the most recent mailer error message.
    #// @var string
    #//
    ErrorInfo = ""
    #// 
    #// The From email address for the message.
    #// @var string
    #//
    From = "root@localhost"
    #// 
    #// The From name of the message.
    #// @var string
    #//
    FromName = "Root User"
    #// 
    #// The Sender email (Return-Path) of the message.
    #// If not empty, will be sent via -f to sendmail or as 'MAIL FROM' in smtp mode.
    #// @var string
    #//
    Sender = ""
    #// 
    #// The Return-Path of the message.
    #// If empty, it will be set to either From or Sender.
    #// @var string
    #// @deprecated Email senders should never set a return-path header;
    #// it's the receiver's job (RFC5321 section 4.4), so this no longer does anything.
    #// @link https://tools.ietf.org/html/rfc5321#section-4.4 RFC5321 reference
    #//
    ReturnPath = ""
    #// 
    #// The Subject of the message.
    #// @var string
    #//
    Subject = ""
    #// 
    #// An HTML or plain text message body.
    #// If HTML then call isHTML(true).
    #// @var string
    #//
    Body = ""
    #// 
    #// The plain-text message body.
    #// This body can be read by mail clients that do not have HTML email
    #// capability such as mutt & Eudora.
    #// Clients that can read HTML will view the normal Body.
    #// @var string
    #//
    AltBody = ""
    #// 
    #// An iCal message part body.
    #// Only supported in simple alt or alt_inline message types
    #// To generate iCal events, use the bundled extras/EasyPeasyICS.php class or iCalcreator
    #// @link http://sprain.ch/blog/downloads/php-class-easypeasyics-create-ical-files-with-php
    #// @link http://kigkonsult.se/iCalcreator
    #// @var string
    #//
    Ical = ""
    #// 
    #// The complete compiled MIME message body.
    #// @access protected
    #// @var string
    #//
    MIMEBody = ""
    #// 
    #// The complete compiled MIME message headers.
    #// @var string
    #// @access protected
    #//
    MIMEHeader = ""
    #// 
    #// Extra headers that createHeader() doesn't fold in.
    #// @var string
    #// @access protected
    #//
    mailHeader = ""
    #// 
    #// Word-wrap the message body to this number of chars.
    #// Set to 0 to not wrap. A useful value here is 78, for RFC2822 section 2.1.1 compliance.
    #// @var integer
    #//
    WordWrap = 0
    #// 
    #// Which method to use to send mail.
    #// Options: "mail", "sendmail", or "smtp".
    #// @var string
    #//
    Mailer = "mail"
    #// 
    #// The path to the sendmail program.
    #// @var string
    #//
    Sendmail = "/usr/sbin/sendmail"
    #// 
    #// Whether mail() uses a fully sendmail-compatible MTA.
    #// One which supports sendmail's "-oi -f" options.
    #// @var boolean
    #//
    UseSendmailOptions = True
    #// 
    #// Path to PHPMailer plugins.
    #// Useful if the SMTP class is not in the PHP include path.
    #// @var string
    #// @deprecated Should not be needed now there is an autoloader.
    #//
    PluginDir = ""
    #// 
    #// The email address that a reading confirmation should be sent to, also known as read receipt.
    #// @var string
    #//
    ConfirmReadingTo = ""
    #// 
    #// The hostname to use in the Message-ID header and as default HELO string.
    #// If empty, PHPMailer attempts to find one with, in order,
    #// $_SERVER['SERVER_NAME'], gethostname(), php_uname('n'), or the value
    #// 'localhost.localdomain'.
    #// @var string
    #//
    Hostname = ""
    #// 
    #// An ID to be used in the Message-ID header.
    #// If empty, a unique id will be generated.
    #// You can set your own, but it must be in the format "<id@domain>",
    #// as defined in RFC5322 section 3.6.4 or it will be ignored.
    #// @see https://tools.ietf.org/html/rfc5322#section-3.6.4
    #// @var string
    #//
    MessageID = ""
    #// 
    #// The message Date to be used in the Date header.
    #// If empty, the current date will be added.
    #// @var string
    #//
    MessageDate = ""
    #// 
    #// SMTP hosts.
    #// Either a single hostname or multiple semicolon-delimited hostnames.
    #// You can also specify a different port
    #// for each host by using this format: [hostname:port]
    #// (e.g. "smtp1.example.com:25;smtp2.example.com").
    #// You can also specify encryption type, for example:
    #// (e.g. "tls://smtp1.example.com:587;ssl://smtp2.example.com:465").
    #// Hosts will be tried in order.
    #// @var string
    #//
    Host = "localhost"
    #// 
    #// The default SMTP server port.
    #// @var integer
    #// @TODO Why is this needed when the SMTP class takes care of it?
    #//
    Port = 25
    #// 
    #// The SMTP HELO of the message.
    #// Default is $Hostname. If $Hostname is empty, PHPMailer attempts to find
    #// one with the same method described above for $Hostname.
    #// @var string
    #// @see PHPMailer::$Hostname
    #//
    Helo = ""
    #// 
    #// What kind of encryption to use on the SMTP connection.
    #// Options: '', 'ssl' or 'tls'
    #// @var string
    #//
    SMTPSecure = ""
    #// 
    #// Whether to enable TLS encryption automatically if a server supports it,
    #// even if `SMTPSecure` is not set to 'tls'.
    #// Be aware that in PHP >= 5.6 this requires that the server's certificates are valid.
    #// @var boolean
    #//
    SMTPAutoTLS = True
    #// 
    #// Whether to use SMTP authentication.
    #// Uses the Username and Password properties.
    #// @var boolean
    #// @see PHPMailer::$Username
    #// @see PHPMailer::$Password
    #//
    SMTPAuth = False
    #// 
    #// Options array passed to stream_context_create when connecting via SMTP.
    #// @var array
    #//
    SMTPOptions = Array()
    #// 
    #// SMTP username.
    #// @var string
    #//
    Username = ""
    #// 
    #// SMTP password.
    #// @var string
    #//
    Password = ""
    #// 
    #// SMTP auth type.
    #// Options are CRAM-MD5, LOGIN, PLAIN, attempted in that order if not specified
    #// @var string
    #//
    AuthType = ""
    #// 
    #// SMTP realm.
    #// Used for NTLM auth
    #// @var string
    #//
    Realm = ""
    #// 
    #// SMTP workstation.
    #// Used for NTLM auth
    #// @var string
    #//
    Workstation = ""
    #// 
    #// The SMTP server timeout in seconds.
    #// Default of 5 minutes (300sec) is from RFC2821 section 4.5.3.2
    #// @var integer
    #//
    Timeout = 300
    #// 
    #// SMTP class debug output mode.
    #// Debug output level.
    #// Options:
    #// `0` No output
    #// `1` Commands
    #// `2` Data and commands
    #// `3` As 2 plus connection status
    #// `4` Low-level data output
    #// @var integer
    #// @see SMTP::$do_debug
    #//
    SMTPDebug = 0
    #// 
    #// How to handle debug output.
    #// Options:
    #// `echo` Output plain-text as-is, appropriate for CLI
    #// `html` Output escaped, line breaks converted to `<br>`, appropriate for browser output
    #// `error_log` Output to error log as configured in php.ini
    #// 
    #// Alternatively, you can provide a callable expecting two params: a message string and the debug level:
    #// <code>
    #// $mail->Debugoutput = function($str, $level) {echo "debug level $level; message: $str";};
    #// </code>
    #// @var string|callable
    #// @see SMTP::$Debugoutput
    #//
    Debugoutput = "echo"
    #// 
    #// Whether to keep SMTP connection open after each message.
    #// If this is set to true then to close the connection
    #// requires an explicit call to smtpClose().
    #// @var boolean
    #//
    SMTPKeepAlive = False
    #// 
    #// Whether to split multiple to addresses into multiple messages
    #// or send them all in one message.
    #// Only supported in `mail` and `sendmail` transports, not in SMTP.
    #// @var boolean
    #//
    SingleTo = False
    #// 
    #// Storage for addresses when SingleTo is enabled.
    #// @var array
    #// @TODO This should really not be public
    #//
    SingleToArray = Array()
    #// 
    #// Whether to generate VERP addresses on send.
    #// Only applicable when sending via SMTP.
    #// @link https://en.wikipedia.org/wiki/Variable_envelope_return_path
    #// @link http://www.postfix.org/VERP_README.html Postfix VERP info
    #// @var boolean
    #//
    do_verp = False
    #// 
    #// Whether to allow sending messages with an empty body.
    #// @var boolean
    #//
    AllowEmpty = False
    #// 
    #// The default line ending.
    #// @note The default remains "\n". We force CRLF where we know
    #// it must be used via self::CRLF.
    #// @var string
    #//
    LE = "\n"
    #// 
    #// DKIM selector.
    #// @var string
    #//
    DKIM_selector = ""
    #// 
    #// DKIM Identity.
    #// Usually the email address used as the source of the email.
    #// @var string
    #//
    DKIM_identity = ""
    #// 
    #// DKIM passphrase.
    #// Used if your key is encrypted.
    #// @var string
    #//
    DKIM_passphrase = ""
    #// 
    #// DKIM signing domain name.
    #// @example 'example.com'
    #// @var string
    #//
    DKIM_domain = ""
    #// 
    #// DKIM private key file path.
    #// @var string
    #//
    DKIM_private = ""
    #// 
    #// DKIM private key string.
    #// If set, takes precedence over `$DKIM_private`.
    #// @var string
    #//
    DKIM_private_string = ""
    #// 
    #// Callback Action function name.
    #// 
    #// The function that handles the result of the send email action.
    #// It is called out by send() for each email sent.
    #// 
    #// Value can be any php callable: http://www.php.net/is_callable
    #// 
    #// Parameters:
    #// boolean $result        result of the send action
    #// array   $to            email addresses of the recipients
    #// array   $cc            cc email addresses
    #// array   $bcc           bcc email addresses
    #// string  $subject       the subject
    #// string  $body          the email body
    #// string  $from          email address of sender
    #// @var string
    #//
    action_function = ""
    #// 
    #// What to put in the X-Mailer header.
    #// Options: An empty string for PHPMailer default, whitespace for none, or a string to use
    #// @var string
    #//
    XMailer = ""
    #// 
    #// Which validator to use by default when validating email addresses.
    #// May be a callable to inject your own validator, but there are several built-in validators.
    #// @see PHPMailer::validateAddress()
    #// @var string|callable
    #// @static
    #//
    validator = "auto"
    #// 
    #// An instance of the SMTP sender class.
    #// @var SMTP
    #// @access protected
    #//
    smtp = None
    #// 
    #// The array of 'to' names and addresses.
    #// @var array
    #// @access protected
    #//
    to = Array()
    #// 
    #// The array of 'cc' names and addresses.
    #// @var array
    #// @access protected
    #//
    cc = Array()
    #// 
    #// The array of 'bcc' names and addresses.
    #// @var array
    #// @access protected
    #//
    bcc = Array()
    #// 
    #// The array of reply-to names and addresses.
    #// @var array
    #// @access protected
    #//
    ReplyTo = Array()
    #// 
    #// An array of all kinds of addresses.
    #// Includes all of $to, $cc, $bcc
    #// @var array
    #// @access protected
    #// @see PHPMailer::$to @see PHPMailer::$cc @see PHPMailer::$bcc
    #//
    all_recipients = Array()
    #// 
    #// An array of names and addresses queued for validation.
    #// In send(), valid and non duplicate entries are moved to $all_recipients
    #// and one of $to, $cc, or $bcc.
    #// This array is used only for addresses with IDN.
    #// @var array
    #// @access protected
    #// @see PHPMailer::$to @see PHPMailer::$cc @see PHPMailer::$bcc
    #// @see PHPMailer::$all_recipients
    #//
    RecipientsQueue = Array()
    #// 
    #// An array of reply-to names and addresses queued for validation.
    #// In send(), valid and non duplicate entries are moved to $ReplyTo.
    #// This array is used only for addresses with IDN.
    #// @var array
    #// @access protected
    #// @see PHPMailer::$ReplyTo
    #//
    ReplyToQueue = Array()
    #// 
    #// The array of attachments.
    #// @var array
    #// @access protected
    #//
    attachment = Array()
    #// 
    #// The array of custom headers.
    #// @var array
    #// @access protected
    #//
    CustomHeader = Array()
    #// 
    #// The most recent Message-ID (including angular brackets).
    #// @var string
    #// @access protected
    #//
    lastMessageID = ""
    #// 
    #// The message's MIME type.
    #// @var string
    #// @access protected
    #//
    message_type = ""
    #// 
    #// The array of MIME boundary strings.
    #// @var array
    #// @access protected
    #//
    boundary = Array()
    #// 
    #// The array of available languages.
    #// @var array
    #// @access protected
    #//
    language = Array()
    #// 
    #// The number of errors encountered.
    #// @var integer
    #// @access protected
    #//
    error_count = 0
    #// 
    #// The S/MIME certificate file path.
    #// @var string
    #// @access protected
    #//
    sign_cert_file = ""
    #// 
    #// The S/MIME key file path.
    #// @var string
    #// @access protected
    #//
    sign_key_file = ""
    #// 
    #// The optional S/MIME extra certificates ("CA Chain") file path.
    #// @var string
    #// @access protected
    #//
    sign_extracerts_file = ""
    #// 
    #// The S/MIME password for the key.
    #// Used only if the key is encrypted.
    #// @var string
    #// @access protected
    #//
    sign_key_pass = ""
    #// 
    #// Whether to throw exceptions for errors.
    #// @var boolean
    #// @access protected
    #//
    exceptions = False
    #// 
    #// Unique ID used for message ID and boundaries.
    #// @var string
    #// @access protected
    #//
    uniqueid = ""
    STOP_MESSAGE = 0
    STOP_CONTINUE = 1
    STOP_CRITICAL = 2
    CRLF = "\r\n"
    MAX_LINE_LENGTH = 998
    #// 
    #// Constructor.
    #// @param boolean $exceptions Should we throw external exceptions?
    #//
    def __init__(self, exceptions_=None):
        if exceptions_ is None:
            exceptions_ = None
        # end if
        
        if exceptions_ != None:
            self.exceptions = php_bool(exceptions_)
        # end if
        #// Pick an appropriate debug output format automatically
        self.Debugoutput = "echo" if php_strpos(PHP_SAPI, "cli") != False else "html"
    # end def __init__
    #// 
    #// Destructor.
    #//
    def __del__(self):
        
        
        #// Close any open SMTP connection nicely
        self.smtpclose()
    # end def __del__
    #// 
    #// Call mail() in a safe_mode-aware fashion.
    #// Also, unless sendmail_path points to sendmail (or something that
    #// claims to be sendmail), don't pass params (not a perfect fix,
    #// but it will do)
    #// @param string $to To
    #// @param string $subject Subject
    #// @param string $body Message Body
    #// @param string $header Additional Header(s)
    #// @param string $params Params
    #// @access private
    #// @return boolean
    #//
    def mailpassthru(self, to_=None, subject_=None, body_=None, header_=None, params_=None):
        
        
        #// Check overloading of mail function to avoid double-encoding
        if php_ini_get("mbstring.func_overload") & 1:
            subject_ = self.secureheader(subject_)
        else:
            subject_ = self.encodeheader(self.secureheader(subject_))
        # end if
        #// Can't use additional_parameters in safe_mode, calling mail() with null params breaks
        #// @link http://php.net/manual/en/function.mail.php
        if php_ini_get("safe_mode") or (not self.UseSendmailOptions) or php_is_null(params_):
            result_ = php_no_error(lambda: mail(to_, subject_, body_, header_))
        else:
            result_ = php_no_error(lambda: mail(to_, subject_, body_, header_, params_))
        # end if
        return result_
    # end def mailpassthru
    #// 
    #// Output debugging info via user-defined method.
    #// Only generates output if SMTP debug output is enabled (@see SMTP::$do_debug).
    #// @see PHPMailer::$Debugoutput
    #// @see PHPMailer::$SMTPDebug
    #// @param string $str
    #//
    def edebug(self, str_=None):
        
        
        if self.SMTPDebug <= 0:
            return
        # end if
        #// Avoid clash with built-in function names
        if (not php_in_array(self.Debugoutput, Array("error_log", "html", "echo"))) and php_is_callable(self.Debugoutput):
            php_call_user_func(self.Debugoutput, str_, self.SMTPDebug)
            return
        # end if
        for case in Switch(self.Debugoutput):
            if case("error_log"):
                #// Don't output, just log
                php_error_log(str_)
                break
            # end if
            if case("html"):
                #// Cleans up output a bit for a better looking, HTML-safe output
                php_print(htmlentities(php_preg_replace("/[\\r\\n]+/", "", str_), ENT_QUOTES, "UTF-8") + "<br>\n")
                break
            # end if
            if case("echo"):
                pass
            # end if
            if case():
                #// Normalize line breaks
                str_ = php_preg_replace("/\\r\\n?/ms", "\n", str_)
                php_print(gmdate("Y-m-d H:i:s") + " " + php_str_replace("\n", "\n                                         ", php_trim(str_)) + "\n")
            # end if
        # end for
    # end def edebug
    #// 
    #// Sets message type to HTML or plain.
    #// @param boolean $isHtml True for HTML mode.
    #// @return void
    #//
    def ishtml(self, isHtml_=None):
        if isHtml_ is None:
            isHtml_ = True
        # end if
        
        if isHtml_:
            self.ContentType = "text/html"
        else:
            self.ContentType = "text/plain"
        # end if
    # end def ishtml
    #// 
    #// Send messages using SMTP.
    #// @return void
    #//
    def issmtp(self):
        
        
        self.Mailer = "smtp"
    # end def issmtp
    #// 
    #// Send messages using PHP's mail() function.
    #// @return void
    #//
    def ismail(self):
        
        
        self.Mailer = "mail"
    # end def ismail
    #// 
    #// Send messages using $Sendmail.
    #// @return void
    #//
    def issendmail(self):
        
        
        ini_sendmail_path_ = php_ini_get("sendmail_path")
        if (not php_stristr(ini_sendmail_path_, "sendmail")):
            self.Sendmail = "/usr/sbin/sendmail"
        else:
            self.Sendmail = ini_sendmail_path_
        # end if
        self.Mailer = "sendmail"
    # end def issendmail
    #// 
    #// Send messages using qmail.
    #// @return void
    #//
    def isqmail(self):
        
        
        ini_sendmail_path_ = php_ini_get("sendmail_path")
        if (not php_stristr(ini_sendmail_path_, "qmail")):
            self.Sendmail = "/var/qmail/bin/qmail-inject"
        else:
            self.Sendmail = ini_sendmail_path_
        # end if
        self.Mailer = "qmail"
    # end def isqmail
    #// 
    #// Add a "To" address.
    #// @param string $address The email address to send to
    #// @param string $name
    #// @return boolean true on success, false if address already used or invalid in some way
    #//
    def addaddress(self, address_=None, name_=""):
        
        
        return self.addorenqueueanaddress("to", address_, name_)
    # end def addaddress
    #// 
    #// Add a "CC" address.
    #// @note: This function works with the SMTP mailer on win32, not with the "mail" mailer.
    #// @param string $address The email address to send to
    #// @param string $name
    #// @return boolean true on success, false if address already used or invalid in some way
    #//
    def addcc(self, address_=None, name_=""):
        
        
        return self.addorenqueueanaddress("cc", address_, name_)
    # end def addcc
    #// 
    #// Add a "BCC" address.
    #// @note: This function works with the SMTP mailer on win32, not with the "mail" mailer.
    #// @param string $address The email address to send to
    #// @param string $name
    #// @return boolean true on success, false if address already used or invalid in some way
    #//
    def addbcc(self, address_=None, name_=""):
        
        
        return self.addorenqueueanaddress("bcc", address_, name_)
    # end def addbcc
    #// 
    #// Add a "Reply-To" address.
    #// @param string $address The email address to reply to
    #// @param string $name
    #// @return boolean true on success, false if address already used or invalid in some way
    #//
    def addreplyto(self, address_=None, name_=""):
        
        
        return self.addorenqueueanaddress("Reply-To", address_, name_)
    # end def addreplyto
    #// 
    #// Add an address to one of the recipient arrays or to the ReplyTo array. Because PHPMailer
    #// can't validate addresses with an IDN without knowing the PHPMailer::$CharSet (that can still
    #// be modified after calling this function), addition of such addresses is delayed until send().
    #// Addresses that have been added already return false, but do not throw exceptions.
    #// @param string $kind One of 'to', 'cc', 'bcc', or 'ReplyTo'
    #// @param string $address The email address to send, resp. to reply to
    #// @param string $name
    #// @throws phpmailerException
    #// @return boolean true on success, false if address already used or invalid in some way
    #// @access protected
    #//
    def addorenqueueanaddress(self, kind_=None, address_=None, name_=None):
        
        
        address_ = php_trim(address_)
        name_ = php_trim(php_preg_replace("/[\\r\\n]+/", "", name_))
        #// Strip breaks and trim
        pos_ = php_strrpos(address_, "@")
        if pos_ == False:
            #// At-sign is misssing.
            error_message_ = self.lang("invalid_address") + str(" (addAnAddress ") + str(kind_) + str("): ") + str(address_)
            self.seterror(error_message_)
            self.edebug(error_message_)
            if self.exceptions:
                raise php_new_class("phpmailerException", lambda : phpmailerException(error_message_))
            # end if
            return False
        # end if
        params_ = Array(kind_, address_, name_)
        pos_ += 1
        #// Enqueue addresses with IDN until we know the PHPMailer::$CharSet.
        pos_ += 1
        if self.has8bitchars(php_substr(address_, pos_)) and self.idnsupported():
            if kind_ != "Reply-To":
                if (not php_array_key_exists(address_, self.RecipientsQueue)):
                    self.RecipientsQueue[address_] = params_
                    return True
                # end if
            else:
                if (not php_array_key_exists(address_, self.ReplyToQueue)):
                    self.ReplyToQueue[address_] = params_
                    return True
                # end if
            # end if
            return False
        # end if
        #// Immediately add standard addresses without IDN.
        return call_user_func_array(Array(self, "addAnAddress"), params_)
    # end def addorenqueueanaddress
    #// 
    #// Add an address to one of the recipient arrays or to the ReplyTo array.
    #// Addresses that have been added already return false, but do not throw exceptions.
    #// @param string $kind One of 'to', 'cc', 'bcc', or 'ReplyTo'
    #// @param string $address The email address to send, resp. to reply to
    #// @param string $name
    #// @throws phpmailerException
    #// @return boolean true on success, false if address already used or invalid in some way
    #// @access protected
    #//
    def addanaddress(self, kind_=None, address_=None, name_=""):
        
        
        if (not php_in_array(kind_, Array("to", "cc", "bcc", "Reply-To"))):
            error_message_ = self.lang("Invalid recipient kind: ") + kind_
            self.seterror(error_message_)
            self.edebug(error_message_)
            if self.exceptions:
                raise php_new_class("phpmailerException", lambda : phpmailerException(error_message_))
            # end if
            return False
        # end if
        if (not self.validateaddress(address_)):
            error_message_ = self.lang("invalid_address") + str(" (addAnAddress ") + str(kind_) + str("): ") + str(address_)
            self.seterror(error_message_)
            self.edebug(error_message_)
            if self.exceptions:
                raise php_new_class("phpmailerException", lambda : phpmailerException(error_message_))
            # end if
            return False
        # end if
        if kind_ != "Reply-To":
            if (not php_array_key_exists(php_strtolower(address_), self.all_recipients)):
                php_array_push(self.kind_, Array(address_, name_))
                self.all_recipients[php_strtolower(address_)] = True
                return True
            # end if
        else:
            if (not php_array_key_exists(php_strtolower(address_), self.ReplyTo)):
                self.ReplyTo[php_strtolower(address_)] = Array(address_, name_)
                return True
            # end if
        # end if
        return False
    # end def addanaddress
    #// 
    #// Parse and validate a string containing one or more RFC822-style comma-separated email addresses
    #// of the form "display name <address>" into an array of name/address pairs.
    #// Uses the imap_rfc822_parse_adrlist function if the IMAP extension is available.
    #// Note that quotes in the name part are removed.
    #// @param string $addrstr The address list string
    #// @param bool $useimap Whether to use the IMAP extension to parse the list
    #// @return array
    #// @link http://www.andrew.cmu.edu/user/agreen1/testing/mrbs/web/Mail/RFC822.php A more careful implementation
    #//
    def parseaddresses(self, addrstr_=None, useimap_=None):
        if useimap_ is None:
            useimap_ = True
        # end if
        
        addresses_ = Array()
        if useimap_ and php_function_exists("imap_rfc822_parse_adrlist"):
            #// Use this built-in parser if it's available
            list_ = imap_rfc822_parse_adrlist(addrstr_, "")
            for address_ in list_:
                if address_.host != ".SYNTAX-ERROR.":
                    if self.validateaddress(address_.mailbox + "@" + address_.host):
                        addresses_[-1] = Array({"name": address_.personal if property_exists(address_, "personal") else "", "address": address_.mailbox + "@" + address_.host})
                    # end if
                # end if
            # end for
        else:
            #// Use this simpler parser
            list_ = php_explode(",", addrstr_)
            for address_ in list_:
                address_ = php_trim(address_)
                #// Is there a separate name part?
                if php_strpos(address_, "<") == False:
                    #// No separate name, just use the whole thing
                    if self.validateaddress(address_):
                        addresses_[-1] = Array({"name": "", "address": address_})
                    # end if
                else:
                    name_, email_ = php_explode("<", address_)
                    email_ = php_trim(php_str_replace(">", "", email_))
                    if self.validateaddress(email_):
                        addresses_[-1] = Array({"name": php_trim(php_str_replace(Array("\"", "'"), "", name_)), "address": email_})
                    # end if
                # end if
            # end for
        # end if
        return addresses_
    # end def parseaddresses
    #// 
    #// Set the From and FromName properties.
    #// @param string $address
    #// @param string $name
    #// @param boolean $auto Whether to also set the Sender address, defaults to true
    #// @throws phpmailerException
    #// @return boolean
    #//
    def setfrom(self, address_=None, name_="", auto_=None):
        if auto_ is None:
            auto_ = True
        # end if
        
        address_ = php_trim(address_)
        name_ = php_trim(php_preg_replace("/[\\r\\n]+/", "", name_))
        pos_ += 1
        #// Strip breaks and trim
        #// Don't validate now addresses with IDN. Will be done in send().
        pos_ = php_strrpos(address_, "@")
        pos_ += 1
        if pos_ == False or (not self.has8bitchars(php_substr(address_, pos_))) or (not self.idnsupported()) and (not self.validateaddress(address_)):
            error_message_ = self.lang("invalid_address") + str(" (setFrom) ") + str(address_)
            self.seterror(error_message_)
            self.edebug(error_message_)
            if self.exceptions:
                raise php_new_class("phpmailerException", lambda : phpmailerException(error_message_))
            # end if
            return False
        # end if
        self.From = address_
        self.FromName = name_
        if auto_:
            if php_empty(lambda : self.Sender):
                self.Sender = address_
            # end if
        # end if
        return True
    # end def setfrom
    #// 
    #// Return the Message-ID header of the last email.
    #// Technically this is the value from the last time the headers were created,
    #// but it's also the message ID of the last sent message except in
    #// pathological cases.
    #// @return string
    #//
    def getlastmessageid(self):
        
        
        return self.lastMessageID
    # end def getlastmessageid
    #// 
    #// Check that a string looks like an email address.
    #// @param string $address The email address to check
    #// @param string|callable $patternselect A selector for the validation pattern to use :
    #// `auto` Pick best pattern automatically;
    #// `pcre8` Use the squiloople.com pattern, requires PCRE > 8.0, PHP >= 5.3.2, 5.2.14;
    #// `pcre` Use old PCRE implementation;
    #// `php` Use PHP built-in FILTER_VALIDATE_EMAIL;
    #// `html5` Use the pattern given by the HTML5 spec for 'email' type form input elements.
    #// `noregex` Don't use a regex: super fast, really dumb.
    #// Alternatively you may pass in a callable to inject your own validator, for example:
    #// PHPMailer::validateAddress('user@example.com', function($address) {
    #// return (strpos($address, '@') !== false);
    #// });
    #// You can also set the PHPMailer::$validator static to a callable, allowing built-in methods to use your validator.
    #// @return boolean
    #// @static
    #// @access public
    #//
    @classmethod
    def validateaddress(self, address_=None, patternselect_=None):
        if patternselect_ is None:
            patternselect_ = None
        # end if
        
        if php_is_null(patternselect_):
            patternselect_ = self.validator
        # end if
        if php_is_callable(patternselect_):
            return php_call_user_func(patternselect_, address_)
        # end if
        #// Reject line breaks in addresses; it's valid RFC5322, but not RFC5321
        if php_strpos(address_, "\n") != False or php_strpos(address_, "\r") != False:
            return False
        # end if
        if (not patternselect_) or patternselect_ == "auto":
            #// Check this constant first so it works when extension_loaded() is disabled by safe mode
            #// Constant was added in PHP 5.2.4
            if php_defined("PCRE_VERSION"):
                #// This pattern can get stuck in a recursive loop in PCRE <= 8.0.2
                if php_version_compare(PCRE_VERSION, "8.0.3") >= 0:
                    patternselect_ = "pcre8"
                else:
                    patternselect_ = "pcre"
                # end if
            elif php_function_exists("extension_loaded") and php_extension_loaded("pcre"):
                #// Fall back to older PCRE
                patternselect_ = "pcre"
            else:
                #// Filter_var appeared in PHP 5.2.0 and does not require the PCRE extension
                if php_version_compare(PHP_VERSION, "5.2.0") >= 0:
                    patternselect_ = "php"
                else:
                    patternselect_ = "noregex"
                # end if
            # end if
        # end if
        for case in Switch(patternselect_):
            if case("pcre8"):
                #// 
                #// Uses the same RFC5322 regex on which FILTER_VALIDATE_EMAIL is based, but allows dotless domains.
                #// @link http://squiloople.com/2009/12/20/email-address-validation
                #// @copyright 2009-2010 Michael Rushton
                #// Feel free to use and redistribute this code. But please keep this copyright notice.
                #//
                return php_bool(php_preg_match("/^(?!(?>(?1)\"?(?>\\\\[ -~]|[^\"])\"?(?1)){255,})(?!(?>(?1)\"?(?>\\\\[ -~]|[^\"])\"?(?1)){65,}@)" + "((?>(?>(?>((?>(?>(?>\\x0D\\x0A)?[\\t ])+|(?>[\\t ]*\\x0D\\x0A)?[\\t ]+)?)(\\((?>(?2)" + "(?>[\\x01-\\x08\\x0B\\x0C\\x0E-'*-\\[\\]-\\x7F]|\\\\[\\x00-\\x7F]|(?3)))*(?2)\\)))+(?2))|(?2))?)" + "([!#-'*+\\/-9=?^-~-]+|\"(?>(?2)(?>[\\x01-\\x08\\x0B\\x0C\\x0E-!#-\\[\\]-\\x7F]|\\\\[\\x00-\\x7F]))*" + "(?2)\")(?>(?1)\\.(?1)(?4))*(?1)@(?!(?1)[a-z0-9-]{64,})(?1)(?>([a-z0-9](?>[a-z0-9-]*[a-z0-9])?)" + "(?>(?1)\\.(?!(?1)[a-z0-9-]{64,})(?1)(?5)){0,126}|\\[(?:(?>IPv6:(?>([a-f0-9]{1,4})(?>:(?6)){7}" + "|(?!(?:.*[a-f0-9][:\\]]){8,})((?6)(?>:(?6)){0,6})?::(?7)?))|(?>(?>IPv6:(?>(?6)(?>:(?6)){5}:" + "|(?!(?:.*[a-f0-9]:){6,})(?8)?::(?>((?6)(?>:(?6)){0,4}):)?))?(25[0-5]|2[0-4][0-9]|1[0-9]{2}" + "|[1-9]?[0-9])(?>\\.(?9)){3}))\\])(?1)$/isD", address_))
            # end if
            if case("pcre"):
                #// An older regex that doesn't need a recent PCRE
                return php_bool(php_preg_match("/^(?!(?>\"?(?>\\\\[ -~]|[^\"])\"?){255,})(?!(?>\"?(?>\\\\[ -~]|[^\"])\"?){65,}@)(?>" + "[!#-'*+\\/-9=?^-~-]+|\"(?>(?>[\\x01-\\x08\\x0B\\x0C\\x0E-!#-\\[\\]-\\x7F]|\\\\[\\x00-\\xFF]))*\")" + "(?>\\.(?>[!#-'*+\\/-9=?^-~-]+|\"(?>(?>[\\x01-\\x08\\x0B\\x0C\\x0E-!#-\\[\\]-\\x7F]|\\\\[\\x00-\\xFF]))*\"))*" + "@(?>(?![a-z0-9-]{64,})(?>[a-z0-9](?>[a-z0-9-]*[a-z0-9])?)(?>\\.(?![a-z0-9-]{64,})" + "(?>[a-z0-9](?>[a-z0-9-]*[a-z0-9])?)){0,126}|\\[(?:(?>IPv6:(?>(?>[a-f0-9]{1,4})(?>:" + "[a-f0-9]{1,4}){7}|(?!(?:.*[a-f0-9][:\\]]){8,})(?>[a-f0-9]{1,4}(?>:[a-f0-9]{1,4}){0,6})?" + "::(?>[a-f0-9]{1,4}(?>:[a-f0-9]{1,4}){0,6})?))|(?>(?>IPv6:(?>[a-f0-9]{1,4}(?>:" + "[a-f0-9]{1,4}){5}:|(?!(?:.*[a-f0-9]:){6,})(?>[a-f0-9]{1,4}(?>:[a-f0-9]{1,4}){0,4})?" + "::(?>(?:[a-f0-9]{1,4}(?>:[a-f0-9]{1,4}){0,4}):)?))?(?>25[0-5]|2[0-4][0-9]|1[0-9]{2}" + "|[1-9]?[0-9])(?>\\.(?>25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])){3}))\\])$/isD", address_))
            # end if
            if case("html5"):
                #// 
                #// This is the pattern used in the HTML5 spec for validation of 'email' type form input elements.
                #// @link http://www.whatwg.org/specs/web-apps/current-work/#e-mail-state-(type=email)
                #//
                return php_bool(php_preg_match("/^[a-zA-Z0-9.!#$%&'*+\\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}" + "[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/sD", address_))
            # end if
            if case("noregex"):
                #// No PCRE! Do something _very_ approximate!
                #// Check the address is 3 chars or longer and contains an @ that's not the first or last char
                return php_strlen(address_) >= 3 and php_strpos(address_, "@") >= 1 and php_strpos(address_, "@") != php_strlen(address_) - 1
            # end if
            if case("php"):
                pass
            # end if
            if case():
                return php_bool(filter_var(address_, FILTER_VALIDATE_EMAIL))
            # end if
        # end for
    # end def validateaddress
    #// 
    #// Tells whether IDNs (Internationalized Domain Names) are supported or not. This requires the
    #// "intl" and "mbstring" PHP extensions.
    #// @return bool "true" if required functions for IDN support are present
    #//
    def idnsupported(self):
        
        
        #// @TODO: Write our own "idn_to_ascii" function for PHP <= 5.2.
        return php_function_exists("idn_to_ascii") and php_function_exists("mb_convert_encoding")
    # end def idnsupported
    #// 
    #// Converts IDN in given email address to its ASCII form, also known as punycode, if possible.
    #// Important: Address must be passed in same encoding as currently set in PHPMailer::$CharSet.
    #// This function silently returns unmodified address if:
    #// - No conversion is necessary (i.e. domain name is not an IDN, or is already in ASCII form)
    #// - Conversion to punycode is impossible (e.g. required PHP functions are not available)
    #// or fails for any reason (e.g. domain has characters not allowed in an IDN)
    #// @see PHPMailer::$CharSet
    #// @param string $address The email address to convert
    #// @return string The encoded address in ASCII form
    #//
    def punyencodeaddress(self, address_=None):
        
        
        #// Verify we have required functions, CharSet, and at-sign.
        pos_ = php_strrpos(address_, "@")
        if self.idnsupported() and (not php_empty(lambda : self.CharSet)) and pos_ != False:
            pos_ += 1
            pos_ += 1
            domain_ = php_substr(address_, pos_)
            #// Verify CharSet string is a valid one, and domain properly encoded in this CharSet.
            if self.has8bitchars(domain_) and php_no_error(lambda: mb_check_encoding(domain_, self.CharSet)):
                domain_ = mb_convert_encoding(domain_, "UTF-8", self.CharSet)
                punycode_ = idn_to_ascii(domain_, 0, INTL_IDNA_VARIANT_UTS46) if php_defined("INTL_IDNA_VARIANT_UTS46") else idn_to_ascii(domain_)
                if punycode_ != False:
                    return php_substr(address_, 0, pos_) + punycode_
                # end if
            # end if
        # end if
        return address_
    # end def punyencodeaddress
    #// 
    #// Create a message and send it.
    #// Uses the sending method specified by $Mailer.
    #// @throws phpmailerException
    #// @return boolean false on error - See the ErrorInfo property for details of the error.
    #//
    def send(self):
        
        
        try: 
            if (not self.presend()):
                return False
            # end if
            return self.postsend()
        except phpmailerException as exc_:
            self.mailHeader = ""
            self.seterror(exc_.getmessage())
            if self.exceptions:
                raise exc_
            # end if
            return False
        # end try
    # end def send
    #// 
    #// Prepare a message for sending.
    #// @throws phpmailerException
    #// @return boolean
    #//
    def presend(self):
        
        
        try: 
            self.error_count = 0
            #// Reset errors
            self.mailHeader = ""
            #// Dequeue recipient and Reply-To addresses with IDN
            for params_ in php_array_merge(self.RecipientsQueue, self.ReplyToQueue):
                params_[1] = self.punyencodeaddress(params_[1])
                call_user_func_array(Array(self, "addAnAddress"), params_)
            # end for
            if php_count(self.to) + php_count(self.cc) + php_count(self.bcc) < 1:
                raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("provide_address"), self.STOP_CRITICAL))
            # end if
            #// Validate From, Sender, and ConfirmReadingTo addresses
            for address_kind_ in Array("From", "Sender", "ConfirmReadingTo"):
                self.address_kind_ = php_trim(self.address_kind_)
                if php_empty(lambda : self.address_kind_):
                    continue
                # end if
                self.address_kind_ = self.punyencodeaddress(self.address_kind_)
                if (not self.validateaddress(self.address_kind_)):
                    error_message_ = self.lang("invalid_address") + " (punyEncode) " + self.address_kind_
                    self.seterror(error_message_)
                    self.edebug(error_message_)
                    if self.exceptions:
                        raise php_new_class("phpmailerException", lambda : phpmailerException(error_message_))
                    # end if
                    return False
                # end if
            # end for
            #// Set whether the message is multipart/alternative
            if self.alternativeexists():
                self.ContentType = "multipart/alternative"
            # end if
            self.setmessagetype()
            #// Refuse to send an empty message unless we are specifically allowing it
            if (not self.AllowEmpty) and php_empty(lambda : self.Body):
                raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("empty_message"), self.STOP_CRITICAL))
            # end if
            #// Create body before headers in case body makes changes to headers (e.g. altering transfer encoding)
            self.MIMEHeader = ""
            self.MIMEBody = self.createbody()
            #// createBody may have added some headers, so retain them
            tempheaders_ = self.MIMEHeader
            self.MIMEHeader = self.createheader()
            self.MIMEHeader += tempheaders_
            #// To capture the complete message when using mail(), create
            #// an extra header list which createHeader() doesn't fold in
            if self.Mailer == "mail":
                if php_count(self.to) > 0:
                    self.mailHeader += self.addrappend("To", self.to)
                else:
                    self.mailHeader += self.headerline("To", "undisclosed-recipients:;")
                # end if
                self.mailHeader += self.headerline("Subject", self.encodeheader(self.secureheader(php_trim(self.Subject))))
            # end if
            #// Sign with DKIM if enabled
            if (not php_empty(lambda : self.DKIM_domain)) and (not php_empty(lambda : self.DKIM_selector)) and (not php_empty(lambda : self.DKIM_private_string)) or (not php_empty(lambda : self.DKIM_private)) and self.ispermittedpath(self.DKIM_private) and php_file_exists(self.DKIM_private):
                header_dkim_ = self.dkim_add(self.MIMEHeader + self.mailHeader, self.encodeheader(self.secureheader(self.Subject)), self.MIMEBody)
                self.MIMEHeader = php_rtrim(self.MIMEHeader, "\r\n ") + self.CRLF + php_str_replace("\r\n", "\n", header_dkim_) + self.CRLF
            # end if
            return True
        except phpmailerException as exc_:
            self.seterror(exc_.getmessage())
            if self.exceptions:
                raise exc_
            # end if
            return False
        # end try
    # end def presend
    #// 
    #// Actually send a message.
    #// Send the email via the selected mechanism
    #// @throws phpmailerException
    #// @return boolean
    #//
    def postsend(self):
        
        
        try: 
            #// Choose the mailer and send through it
            for case in Switch(self.Mailer):
                if case("sendmail"):
                    pass
                # end if
                if case("qmail"):
                    return self.sendmailsend(self.MIMEHeader, self.MIMEBody)
                # end if
                if case("smtp"):
                    return self.smtpsend(self.MIMEHeader, self.MIMEBody)
                # end if
                if case("mail"):
                    return self.mailsend(self.MIMEHeader, self.MIMEBody)
                # end if
                if case():
                    sendMethod_ = self.Mailer + "Send"
                    if php_method_exists(self, sendMethod_):
                        return self.sendmethod_(self.MIMEHeader, self.MIMEBody)
                    # end if
                    return self.mailsend(self.MIMEHeader, self.MIMEBody)
                # end if
            # end for
        except phpmailerException as exc_:
            self.seterror(exc_.getmessage())
            self.edebug(exc_.getmessage())
            if self.exceptions:
                raise exc_
            # end if
        # end try
        return False
    # end def postsend
    #// 
    #// Send mail using the $Sendmail program.
    #// @param string $header The message headers
    #// @param string $body The message body
    #// @see PHPMailer::$Sendmail
    #// @throws phpmailerException
    #// @access protected
    #// @return boolean
    #//
    def sendmailsend(self, header_=None, body_=None):
        
        
        #// CVE-2016-10033, CVE-2016-10045: Don't pass -f if characters will be escaped.
        if (not php_empty(lambda : self.Sender)) and self.isshellsafe(self.Sender):
            if self.Mailer == "qmail":
                sendmailFmt_ = "%s -f%s"
            else:
                sendmailFmt_ = "%s -oi -f%s -t"
            # end if
        else:
            if self.Mailer == "qmail":
                sendmailFmt_ = "%s"
            else:
                sendmailFmt_ = "%s -oi -t"
            # end if
        # end if
        #// TODO: If possible, this should be changed to escapeshellarg.  Needs thorough testing.
        sendmail_ = php_sprintf(sendmailFmt_, escapeshellcmd(self.Sendmail), self.Sender)
        if self.SingleTo:
            for toAddr_ in self.SingleToArray:
                mail_ = popen(sendmail_, "w")
                if (not php_no_error(lambda: mail_)):
                    raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("execute") + self.Sendmail, self.STOP_CRITICAL))
                # end if
                fputs(mail_, "To: " + toAddr_ + "\n")
                fputs(mail_, header_)
                fputs(mail_, body_)
                result_ = pclose(mail_)
                self.docallback(result_ == 0, Array(toAddr_), self.cc, self.bcc, self.Subject, body_, self.From)
                if result_ != 0:
                    raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("execute") + self.Sendmail, self.STOP_CRITICAL))
                # end if
            # end for
        else:
            mail_ = popen(sendmail_, "w")
            if (not php_no_error(lambda: mail_)):
                raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("execute") + self.Sendmail, self.STOP_CRITICAL))
            # end if
            fputs(mail_, header_)
            fputs(mail_, body_)
            result_ = pclose(mail_)
            self.docallback(result_ == 0, self.to, self.cc, self.bcc, self.Subject, body_, self.From)
            if result_ != 0:
                raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("execute") + self.Sendmail, self.STOP_CRITICAL))
            # end if
        # end if
        return True
    # end def sendmailsend
    #// 
    #// Fix CVE-2016-10033 and CVE-2016-10045 by disallowing potentially unsafe shell characters.
    #// 
    #// Note that escapeshellarg and escapeshellcmd are inadequate for our purposes, especially on Windows.
    #// @param string $string The string to be validated
    #// @see https://github.com/PHPMailer/PHPMailer/issues/924 CVE-2016-10045 bug report
    #// @access protected
    #// @return boolean
    #//
    def isshellsafe(self, string_=None):
        
        
        #// Future-proof
        if escapeshellcmd(string_) != string_ or (not php_in_array(escapeshellarg(string_), Array(str("'") + str(string_) + str("'"), str("\"") + str(string_) + str("\"")))):
            return False
        # end if
        length_ = php_strlen(string_)
        i_ = 0
        while i_ < length_:
            
            c_ = string_[i_]
            #// All other characters have a special meaning in at least one common shell, including = and +.
            #// Full stop (.) has a special meaning in cmd.exe, but its impact should be negligible here.
            #// Note that this does permit non-Latin alphanumeric characters based on the current locale.
            if (not ctype_alnum(c_)) and php_strpos("@_-.", c_) == False:
                return False
            # end if
            i_ += 1
        # end while
        return True
    # end def isshellsafe
    #// 
    #// Check whether a file path is of a permitted type.
    #// Used to reject URLs and phar files from functions that access local file paths,
    #// such as addAttachment.
    #// @param string $path A relative or absolute path to a file.
    #// @return bool
    #//
    def ispermittedpath(self, path_=None):
        
        
        return (not php_preg_match("#^[a-z]+://#i", path_))
    # end def ispermittedpath
    #// 
    #// Send mail using the PHP mail() function.
    #// @param string $header The message headers
    #// @param string $body The message body
    #// @link http://www.php.net/manual/en/book.mail.php
    #// @throws phpmailerException
    #// @access protected
    #// @return boolean
    #//
    def mailsend(self, header_=None, body_=None):
        
        
        toArr_ = Array()
        for toaddr_ in self.to:
            toArr_[-1] = self.addrformat(toaddr_)
        # end for
        to_ = php_implode(", ", toArr_)
        params_ = None
        #// This sets the SMTP envelope sender which gets turned into a return-path header by the receiver
        if (not php_empty(lambda : self.Sender)) and self.validateaddress(self.Sender):
            #// CVE-2016-10033, CVE-2016-10045: Don't pass -f if characters will be escaped.
            if self.isshellsafe(self.Sender):
                params_ = php_sprintf("-f%s", self.Sender)
            # end if
        # end if
        if (not php_empty(lambda : self.Sender)) and (not php_ini_get("safe_mode")) and self.validateaddress(self.Sender):
            old_from_ = php_ini_get("sendmail_from")
            php_ini_set("sendmail_from", self.Sender)
        # end if
        result_ = False
        if self.SingleTo and php_count(toArr_) > 1:
            for toAddr_ in toArr_:
                result_ = self.mailpassthru(toAddr_, self.Subject, body_, header_, params_)
                self.docallback(result_, Array(toAddr_), self.cc, self.bcc, self.Subject, body_, self.From)
            # end for
        else:
            result_ = self.mailpassthru(to_, self.Subject, body_, header_, params_)
            self.docallback(result_, self.to, self.cc, self.bcc, self.Subject, body_, self.From)
        # end if
        if (php_isset(lambda : old_from_)):
            php_ini_set("sendmail_from", old_from_)
        # end if
        if (not result_):
            raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("instantiate"), self.STOP_CRITICAL))
        # end if
        return True
    # end def mailsend
    #// 
    #// Get an instance to use for SMTP operations.
    #// Override this function to load your own SMTP implementation
    #// @return SMTP
    #//
    def getsmtpinstance(self):
        
        
        if (not php_is_object(self.smtp)):
            php_include_file("class-smtp.php", once=True)
            self.smtp = php_new_class("SMTP", lambda : SMTP())
        # end if
        return self.smtp
    # end def getsmtpinstance
    #// 
    #// Send mail via SMTP.
    #// Returns false if there is a bad MAIL FROM, RCPT, or DATA input.
    #// Uses the PHPMailerSMTP class by default.
    #// @see PHPMailer::getSMTPInstance() to use a different class.
    #// @param string $header The message headers
    #// @param string $body The message body
    #// @throws phpmailerException
    #// @uses SMTP
    #// @access protected
    #// @return boolean
    #//
    def smtpsend(self, header_=None, body_=None):
        
        
        bad_rcpt_ = Array()
        if (not self.smtpconnect(self.SMTPOptions)):
            raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("smtp_connect_failed"), self.STOP_CRITICAL))
        # end if
        if (not php_empty(lambda : self.Sender)) and self.validateaddress(self.Sender):
            smtp_from_ = self.Sender
        else:
            smtp_from_ = self.From
        # end if
        if (not self.smtp.mail(smtp_from_)):
            self.seterror(self.lang("from_failed") + smtp_from_ + " : " + php_implode(",", self.smtp.geterror()))
            raise php_new_class("phpmailerException", lambda : phpmailerException(self.ErrorInfo, self.STOP_CRITICAL))
        # end if
        #// Attempt to send to all recipients
        for togroup_ in Array(self.to, self.cc, self.bcc):
            for to_ in togroup_:
                if (not self.smtp.recipient(to_[0])):
                    error_ = self.smtp.geterror()
                    bad_rcpt_[-1] = Array({"to": to_[0], "error": error_["detail"]})
                    isSent_ = False
                else:
                    isSent_ = True
                # end if
                self.docallback(isSent_, Array(to_[0]), Array(), Array(), self.Subject, body_, self.From)
            # end for
        # end for
        #// Only send the DATA command if we have viable recipients
        if php_count(self.all_recipients) > php_count(bad_rcpt_) and (not self.smtp.data(header_ + body_)):
            raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("data_not_accepted"), self.STOP_CRITICAL))
        # end if
        if self.SMTPKeepAlive:
            self.smtp.reset()
        else:
            self.smtp.quit()
            self.smtp.close()
        # end if
        #// Create error message for any bad addresses
        if php_count(bad_rcpt_) > 0:
            errstr_ = ""
            for bad_ in bad_rcpt_:
                errstr_ += bad_["to"] + ": " + bad_["error"]
            # end for
            raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("recipients_failed") + errstr_, self.STOP_CONTINUE))
        # end if
        return True
    # end def smtpsend
    #// 
    #// Initiate a connection to an SMTP server.
    #// Returns false if the operation failed.
    #// @param array $options An array of options compatible with stream_context_create()
    #// @uses SMTP
    #// @access public
    #// @throws phpmailerException
    #// @return boolean
    #//
    def smtpconnect(self, options_=None):
        if options_ is None:
            options_ = None
        # end if
        
        if php_is_null(self.smtp):
            self.smtp = self.getsmtpinstance()
        # end if
        #// If no options are provided, use whatever is set in the instance
        if php_is_null(options_):
            options_ = self.SMTPOptions
        # end if
        #// Already connected?
        if self.smtp.connected():
            return True
        # end if
        self.smtp.settimeout(self.Timeout)
        self.smtp.setdebuglevel(self.SMTPDebug)
        self.smtp.setdebugoutput(self.Debugoutput)
        self.smtp.setverp(self.do_verp)
        hosts_ = php_explode(";", self.Host)
        lastexception_ = None
        for hostentry_ in hosts_:
            hostinfo_ = Array()
            if (not php_preg_match("/^((ssl|tls):\\/\\/)*([a-zA-Z0-9\\.-]*|\\[[a-fA-F0-9:]+\\]):?([0-9]*)$/", php_trim(hostentry_), hostinfo_)):
                #// Not a valid host entry
                self.edebug("Ignoring invalid host: " + hostentry_)
                continue
            # end if
            #// $hostinfo[2]: optional ssl or tls prefix
            #// $hostinfo[3]: the hostname
            #// $hostinfo[4]: optional port number
            #// The host string prefix can temporarily override the current setting for SMTPSecure
            #// If it's not specified, the default value is used
            prefix_ = ""
            secure_ = self.SMTPSecure
            tls_ = self.SMTPSecure == "tls"
            if "ssl" == hostinfo_[2] or "" == hostinfo_[2] and "ssl" == self.SMTPSecure:
                prefix_ = "ssl://"
                tls_ = False
                #// Can't have SSL and TLS at the same time
                secure_ = "ssl"
            elif hostinfo_[2] == "tls":
                tls_ = True
                #// tls doesn't use a prefix
                secure_ = "tls"
            # end if
            #// Do we need the OpenSSL extension?
            sslext_ = php_defined("OPENSSL_ALGO_SHA1")
            if "tls" == secure_ or "ssl" == secure_:
                #// Check for an OpenSSL constant rather than using extension_loaded, which is sometimes disabled
                if (not sslext_):
                    raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("extension_missing") + "openssl", self.STOP_CRITICAL))
                # end if
            # end if
            host_ = hostinfo_[3]
            port_ = self.Port
            tport_ = php_int(hostinfo_[4])
            if tport_ > 0 and tport_ < 65536:
                port_ = tport_
            # end if
            if self.smtp.connect(prefix_ + host_, port_, self.Timeout, options_):
                try: 
                    if self.Helo:
                        hello_ = self.Helo
                    else:
                        hello_ = self.serverhostname()
                    # end if
                    self.smtp.hello(hello_)
                    #// Automatically enable TLS encryption if:
                    #// it's not disabled
                    #// we have openssl extension
                    #// we are not already using SSL
                    #// the server offers STARTTLS
                    if self.SMTPAutoTLS and sslext_ and secure_ != "ssl" and self.smtp.getserverext("STARTTLS"):
                        tls_ = True
                    # end if
                    if tls_:
                        if (not self.smtp.starttls()):
                            raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("connect_host")))
                        # end if
                        #// We must resend EHLO after TLS negotiation
                        self.smtp.hello(hello_)
                    # end if
                    if self.SMTPAuth:
                        if (not self.smtp.authenticate(self.Username, self.Password, self.AuthType, self.Realm, self.Workstation)):
                            raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("authenticate")))
                        # end if
                    # end if
                    return True
                except phpmailerException as exc_:
                    lastexception_ = exc_
                    self.edebug(exc_.getmessage())
                    #// We must have connected, but then failed TLS or Auth, so close connection nicely
                    self.smtp.quit()
                # end try
            # end if
        # end for
        #// If we get here, all connection attempts have failed, so close connection hard
        self.smtp.close()
        #// As we've caught all exceptions, just report whatever the last one was
        if self.exceptions and (not php_is_null(lastexception_)):
            raise lastexception_
        # end if
        return False
    # end def smtpconnect
    #// 
    #// Close the active SMTP session if one exists.
    #// @return void
    #//
    def smtpclose(self):
        
        
        if php_is_a(self.smtp, "SMTP"):
            if self.smtp.connected():
                self.smtp.quit()
                self.smtp.close()
            # end if
        # end if
    # end def smtpclose
    #// 
    #// Set the language for error messages.
    #// Returns false if it cannot load the language file.
    #// The default language is English.
    #// @param string $langcode ISO 639-1 2-character language code (e.g. French is "fr")
    #// @param string $lang_path Path to the language file directory, with trailing separator (slash)
    #// @return boolean
    #// @access public
    #//
    def setlanguage(self, langcode_="en", lang_path_=""):
        
        
        #// Backwards compatibility for renamed language codes
        renamed_langcodes_ = Array({"br": "pt_br", "cz": "cs", "dk": "da", "no": "nb", "se": "sv", "sr": "rs"})
        if (php_isset(lambda : renamed_langcodes_[langcode_])):
            langcode_ = renamed_langcodes_[langcode_]
        # end if
        #// Define full set of translatable strings in English
        PHPMAILER_LANG_ = Array({"authenticate": "SMTP Error: Could not authenticate.", "connect_host": "SMTP Error: Could not connect to SMTP host.", "data_not_accepted": "SMTP Error: data not accepted.", "empty_message": "Message body empty", "encoding": "Unknown encoding: ", "execute": "Could not execute: ", "file_access": "Could not access file: ", "file_open": "File Error: Could not open file: ", "from_failed": "The following From address failed: ", "instantiate": "Could not instantiate mail function.", "invalid_address": "Invalid address: ", "mailer_not_supported": " mailer is not supported.", "provide_address": "You must provide at least one recipient email address.", "recipients_failed": "SMTP Error: The following recipients failed: ", "signing": "Signing Error: ", "smtp_connect_failed": "SMTP connect() failed.", "smtp_error": "SMTP server error: ", "variable_set": "Cannot set or reset variable: ", "extension_missing": "Extension missing: "})
        if php_empty(lambda : lang_path_):
            #// Calculate an absolute path so it can work if CWD is not here
            lang_path_ = php_dirname(__FILE__) + DIRECTORY_SEPARATOR + "language" + DIRECTORY_SEPARATOR
        # end if
        #// Validate $langcode
        if (not php_preg_match("/^[a-z]{2}(?:_[a-zA-Z]{2})?$/", langcode_)):
            langcode_ = "en"
        # end if
        foundlang_ = True
        lang_file_ = lang_path_ + "phpmailer.lang-" + langcode_ + ".php"
        #// There is no English translation file
        if langcode_ != "en":
            #// Make sure language file path is readable
            if (not self.ispermittedpath(lang_file_)) or (not php_is_readable(lang_file_)):
                foundlang_ = False
            else:
                #// Overwrite language-specific strings.
                #// This way we'll never have missing translation keys.
                foundlang_ = php_include_file(lang_file_, once=False)
            # end if
        # end if
        self.language = PHPMAILER_LANG_
        return php_bool(foundlang_)
        pass
    # end def setlanguage
    #// 
    #// Get the array of strings for the current language.
    #// @return array
    #//
    def gettranslations(self):
        
        
        return self.language
    # end def gettranslations
    #// 
    #// Create recipient headers.
    #// @access public
    #// @param string $type
    #// @param array $addr An array of recipient,
    #// where each recipient is a 2-element indexed array with element 0 containing an address
    #// and element 1 containing a name, like:
    #// array(array('joe@example.com', 'Joe User'), array('zoe@example.com', 'Zoe User'))
    #// @return string
    #//
    def addrappend(self, type_=None, addr_=None):
        
        
        addresses_ = Array()
        for address_ in addr_:
            addresses_[-1] = self.addrformat(address_)
        # end for
        return type_ + ": " + php_implode(", ", addresses_) + self.LE
    # end def addrappend
    #// 
    #// Format an address for use in a message header.
    #// @access public
    #// @param array $addr A 2-element indexed array, element 0 containing an address, element 1 containing a name
    #// like array('joe@example.com', 'Joe User')
    #// @return string
    #//
    def addrformat(self, addr_=None):
        
        
        if php_empty(lambda : addr_[1]):
            #// No name provided
            return self.secureheader(addr_[0])
        else:
            return self.encodeheader(self.secureheader(addr_[1]), "phrase") + " <" + self.secureheader(addr_[0]) + ">"
        # end if
    # end def addrformat
    #// 
    #// Word-wrap message.
    #// For use with mailers that do not automatically perform wrapping
    #// and for quoted-printable encoded messages.
    #// Original written by philippe.
    #// @param string $message The message to wrap
    #// @param integer $length The line length to wrap to
    #// @param boolean $qp_mode Whether to run in Quoted-Printable mode
    #// @access public
    #// @return string
    #//
    def wraptext(self, message_=None, length_=None, qp_mode_=None):
        if qp_mode_ is None:
            qp_mode_ = False
        # end if
        
        if qp_mode_:
            soft_break_ = php_sprintf(" =%s", self.LE)
        else:
            soft_break_ = self.LE
        # end if
        #// If utf-8 encoding is used, we will need to make sure we don't
        #// split multibyte characters when we wrap
        is_utf8_ = php_strtolower(self.CharSet) == "utf-8"
        lelen_ = php_strlen(self.LE)
        crlflen_ = php_strlen(self.CRLF)
        message_ = self.fixeol(message_)
        #// Remove a trailing line break
        if php_substr(message_, -lelen_) == self.LE:
            message_ = php_substr(message_, 0, -lelen_)
        # end if
        #// Split message into lines
        lines_ = php_explode(self.LE, message_)
        #// Message will be rebuilt in here
        message_ = ""
        for line_ in lines_:
            words_ = php_explode(" ", line_)
            buf_ = ""
            firstword_ = True
            for word_ in words_:
                if qp_mode_ and php_strlen(word_) > length_:
                    space_left_ = length_ - php_strlen(buf_) - crlflen_
                    if (not firstword_):
                        if space_left_ > 20:
                            len_ = space_left_
                            if is_utf8_:
                                len_ = self.utf8charboundary(word_, len_)
                            elif php_substr(word_, len_ - 1, 1) == "=":
                                len_ -= 1
                            elif php_substr(word_, len_ - 2, 1) == "=":
                                len_ -= 2
                            # end if
                            part_ = php_substr(word_, 0, len_)
                            word_ = php_substr(word_, len_)
                            buf_ += " " + part_
                            message_ += buf_ + php_sprintf("=%s", self.CRLF)
                        else:
                            message_ += buf_ + soft_break_
                        # end if
                        buf_ = ""
                    # end if
                    while True:
                        
                        if not (php_strlen(word_) > 0):
                            break
                        # end if
                        if length_ <= 0:
                            break
                        # end if
                        len_ = length_
                        if is_utf8_:
                            len_ = self.utf8charboundary(word_, len_)
                        elif php_substr(word_, len_ - 1, 1) == "=":
                            len_ -= 1
                        elif php_substr(word_, len_ - 2, 1) == "=":
                            len_ -= 2
                        # end if
                        part_ = php_substr(word_, 0, len_)
                        word_ = php_substr(word_, len_)
                        if php_strlen(word_) > 0:
                            message_ += part_ + php_sprintf("=%s", self.CRLF)
                        else:
                            buf_ = part_
                        # end if
                    # end while
                else:
                    buf_o_ = buf_
                    if (not firstword_):
                        buf_ += " "
                    # end if
                    buf_ += word_
                    if php_strlen(buf_) > length_ and buf_o_ != "":
                        message_ += buf_o_ + soft_break_
                        buf_ = word_
                    # end if
                # end if
                firstword_ = False
            # end for
            message_ += buf_ + self.CRLF
        # end for
        return message_
    # end def wraptext
    #// 
    #// Find the last character boundary prior to $maxLength in a utf-8
    #// quoted-printable encoded string.
    #// Original written by Colin Brown.
    #// @access public
    #// @param string $encodedText utf-8 QP text
    #// @param integer $maxLength Find the last character boundary prior to this length
    #// @return integer
    #//
    def utf8charboundary(self, encodedText_=None, maxLength_=None):
        
        
        foundSplitPos_ = False
        lookBack_ = 3
        while True:
            
            if not ((not foundSplitPos_)):
                break
            # end if
            lastChunk_ = php_substr(encodedText_, maxLength_ - lookBack_, lookBack_)
            encodedCharPos_ = php_strpos(lastChunk_, "=")
            if False != encodedCharPos_:
                #// Found start of encoded character byte within $lookBack block.
                #// Check the encoded byte value (the 2 chars after the '=')
                hex_ = php_substr(encodedText_, maxLength_ - lookBack_ + encodedCharPos_ + 1, 2)
                dec_ = hexdec(hex_)
                if dec_ < 128:
                    #// Single byte character.
                    #// If the encoded char was found at pos 0, it will fit
                    #// otherwise reduce maxLength to start of the encoded char
                    if encodedCharPos_ > 0:
                        maxLength_ = maxLength_ - lookBack_ - encodedCharPos_
                    # end if
                    foundSplitPos_ = True
                elif dec_ >= 192:
                    #// First byte of a multi byte character
                    #// Reduce maxLength to split at start of character
                    maxLength_ = maxLength_ - lookBack_ - encodedCharPos_
                    foundSplitPos_ = True
                elif dec_ < 192:
                    #// Middle byte of a multi byte character, look further back
                    lookBack_ += 3
                # end if
            else:
                #// No encoded character found
                foundSplitPos_ = True
            # end if
        # end while
        return maxLength_
    # end def utf8charboundary
    #// 
    #// Apply word wrapping to the message body.
    #// Wraps the message body to the number of chars set in the WordWrap property.
    #// You should only do this to plain-text bodies as wrapping HTML tags may break them.
    #// This is called automatically by createBody(), so you don't need to call it yourself.
    #// @access public
    #// @return void
    #//
    def setwordwrap(self):
        
        
        if self.WordWrap < 1:
            return
        # end if
        for case in Switch(self.message_type):
            if case("alt"):
                pass
            # end if
            if case("alt_inline"):
                pass
            # end if
            if case("alt_attach"):
                pass
            # end if
            if case("alt_inline_attach"):
                self.AltBody = self.wraptext(self.AltBody, self.WordWrap)
                break
            # end if
            if case():
                self.Body = self.wraptext(self.Body, self.WordWrap)
                break
            # end if
        # end for
    # end def setwordwrap
    #// 
    #// Assemble message headers.
    #// @access public
    #// @return string The assembled headers
    #//
    def createheader(self):
        
        
        result_ = ""
        result_ += self.headerline("Date", self.rfcdate() if self.MessageDate == "" else self.MessageDate)
        #// To be created automatically by mail()
        if self.SingleTo:
            if self.Mailer != "mail":
                for toaddr_ in self.to:
                    self.SingleToArray[-1] = self.addrformat(toaddr_)
                # end for
            # end if
        else:
            if php_count(self.to) > 0:
                if self.Mailer != "mail":
                    result_ += self.addrappend("To", self.to)
                # end if
            elif php_count(self.cc) == 0:
                result_ += self.headerline("To", "undisclosed-recipients:;")
            # end if
        # end if
        result_ += self.addrappend("From", Array(Array(php_trim(self.From), self.FromName)))
        #// sendmail and mail() extract Cc from the header before sending
        if php_count(self.cc) > 0:
            result_ += self.addrappend("Cc", self.cc)
        # end if
        #// sendmail and mail() extract Bcc from the header before sending
        if self.Mailer == "sendmail" or self.Mailer == "qmail" or self.Mailer == "mail" and php_count(self.bcc) > 0:
            result_ += self.addrappend("Bcc", self.bcc)
        # end if
        if php_count(self.ReplyTo) > 0:
            result_ += self.addrappend("Reply-To", self.ReplyTo)
        # end if
        #// mail() sets the subject itself
        if self.Mailer != "mail":
            result_ += self.headerline("Subject", self.encodeheader(self.secureheader(self.Subject)))
        # end if
        #// Only allow a custom message ID if it conforms to RFC 5322 section 3.6.4
        #// https://tools.ietf.org/html/rfc5322#section-3.6.4
        if "" != self.MessageID and php_preg_match("/^<.*@.*>$/", self.MessageID):
            self.lastMessageID = self.MessageID
        else:
            self.lastMessageID = php_sprintf("<%s@%s>", self.uniqueid, self.serverhostname())
        # end if
        result_ += self.headerline("Message-ID", self.lastMessageID)
        if (not php_is_null(self.Priority)):
            result_ += self.headerline("X-Priority", self.Priority)
        # end if
        if self.XMailer == "":
            result_ += self.headerline("X-Mailer", "PHPMailer " + self.Version + " (https://github.com/PHPMailer/PHPMailer)")
        else:
            myXmailer_ = php_trim(self.XMailer)
            if myXmailer_:
                result_ += self.headerline("X-Mailer", myXmailer_)
            # end if
        # end if
        if self.ConfirmReadingTo != "":
            result_ += self.headerline("Disposition-Notification-To", "<" + self.ConfirmReadingTo + ">")
        # end if
        #// Add custom headers
        for header_ in self.CustomHeader:
            result_ += self.headerline(php_trim(header_[0]), self.encodeheader(php_trim(header_[1])))
        # end for
        if (not self.sign_key_file):
            result_ += self.headerline("MIME-Version", "1.0")
            result_ += self.getmailmime()
        # end if
        return result_
    # end def createheader
    #// 
    #// Get the message MIME type headers.
    #// @access public
    #// @return string
    #//
    def getmailmime(self):
        
        
        result_ = ""
        ismultipart_ = True
        for case in Switch(self.message_type):
            if case("inline"):
                result_ += self.headerline("Content-Type", "multipart/related;")
                result_ += self.textline("  boundary=\"" + self.boundary[1] + "\"")
                break
            # end if
            if case("attach"):
                pass
            # end if
            if case("inline_attach"):
                pass
            # end if
            if case("alt_attach"):
                pass
            # end if
            if case("alt_inline_attach"):
                result_ += self.headerline("Content-Type", "multipart/mixed;")
                result_ += self.textline("  boundary=\"" + self.boundary[1] + "\"")
                break
            # end if
            if case("alt"):
                pass
            # end if
            if case("alt_inline"):
                result_ += self.headerline("Content-Type", "multipart/alternative;")
                result_ += self.textline("  boundary=\"" + self.boundary[1] + "\"")
                break
            # end if
            if case():
                #// Catches case 'plain': and case '':
                result_ += self.textline("Content-Type: " + self.ContentType + "; charset=" + self.CharSet)
                ismultipart_ = False
                break
            # end if
        # end for
        #// RFC1341 part 5 says 7bit is assumed if not specified
        if self.Encoding != "7bit":
            #// RFC 2045 section 6.4 says multipart MIME parts may only use 7bit, 8bit or binary CTE
            if ismultipart_:
                if self.Encoding == "8bit":
                    result_ += self.headerline("Content-Transfer-Encoding", "8bit")
                # end if
                pass
            else:
                result_ += self.headerline("Content-Transfer-Encoding", self.Encoding)
            # end if
        # end if
        if self.Mailer != "mail":
            result_ += self.LE
        # end if
        return result_
    # end def getmailmime
    #// 
    #// Returns the whole MIME message.
    #// Includes complete headers and body.
    #// Only valid post preSend().
    #// @see PHPMailer::preSend()
    #// @access public
    #// @return string
    #//
    def getsentmimemessage(self):
        
        
        return php_rtrim(self.MIMEHeader + self.mailHeader, "\n\r") + self.CRLF + self.CRLF + self.MIMEBody
    # end def getsentmimemessage
    #// 
    #// Create unique ID
    #// @return string
    #//
    def generateid(self):
        
        
        return php_md5(php_uniqid(time()))
    # end def generateid
    #// 
    #// Assemble the message body.
    #// Returns an empty string on failure.
    #// @access public
    #// @throws phpmailerException
    #// @return string The assembled message body
    #//
    def createbody(self):
        
        
        body_ = ""
        #// Create unique IDs and preset boundaries
        self.uniqueid = self.generateid()
        self.boundary[1] = "b1_" + self.uniqueid
        self.boundary[2] = "b2_" + self.uniqueid
        self.boundary[3] = "b3_" + self.uniqueid
        if self.sign_key_file:
            body_ += self.getmailmime() + self.LE
        # end if
        self.setwordwrap()
        bodyEncoding_ = self.Encoding
        bodyCharSet_ = self.CharSet
        #// Can we do a 7-bit downgrade?
        if bodyEncoding_ == "8bit" and (not self.has8bitchars(self.Body)):
            bodyEncoding_ = "7bit"
            #// All ISO 8859, Windows codepage and UTF-8 charsets are ascii compatible up to 7-bit
            bodyCharSet_ = "us-ascii"
        # end if
        #// If lines are too long, and we're not already using an encoding that will shorten them,
        #// change to quoted-printable transfer encoding for the body part only
        if "base64" != self.Encoding and self.haslinelongerthanmax(self.Body):
            bodyEncoding_ = "quoted-printable"
        # end if
        altBodyEncoding_ = self.Encoding
        altBodyCharSet_ = self.CharSet
        #// Can we do a 7-bit downgrade?
        if altBodyEncoding_ == "8bit" and (not self.has8bitchars(self.AltBody)):
            altBodyEncoding_ = "7bit"
            #// All ISO 8859, Windows codepage and UTF-8 charsets are ascii compatible up to 7-bit
            altBodyCharSet_ = "us-ascii"
        # end if
        #// If lines are too long, and we're not already using an encoding that will shorten them,
        #// change to quoted-printable transfer encoding for the alt body part only
        if "base64" != altBodyEncoding_ and self.haslinelongerthanmax(self.AltBody):
            altBodyEncoding_ = "quoted-printable"
        # end if
        #// Use this as a preamble in all multipart message types
        mimepre_ = "This is a multi-part message in MIME format." + self.LE + self.LE
        for case in Switch(self.message_type):
            if case("inline"):
                body_ += mimepre_
                body_ += self.getboundary(self.boundary[1], bodyCharSet_, "", bodyEncoding_)
                body_ += self.encodestring(self.Body, bodyEncoding_)
                body_ += self.LE + self.LE
                body_ += self.attachall("inline", self.boundary[1])
                break
            # end if
            if case("attach"):
                body_ += mimepre_
                body_ += self.getboundary(self.boundary[1], bodyCharSet_, "", bodyEncoding_)
                body_ += self.encodestring(self.Body, bodyEncoding_)
                body_ += self.LE + self.LE
                body_ += self.attachall("attachment", self.boundary[1])
                break
            # end if
            if case("inline_attach"):
                body_ += mimepre_
                body_ += self.textline("--" + self.boundary[1])
                body_ += self.headerline("Content-Type", "multipart/related;")
                body_ += self.textline("    boundary=\"" + self.boundary[2] + "\"")
                body_ += self.LE
                body_ += self.getboundary(self.boundary[2], bodyCharSet_, "", bodyEncoding_)
                body_ += self.encodestring(self.Body, bodyEncoding_)
                body_ += self.LE + self.LE
                body_ += self.attachall("inline", self.boundary[2])
                body_ += self.LE
                body_ += self.attachall("attachment", self.boundary[1])
                break
            # end if
            if case("alt"):
                body_ += mimepre_
                body_ += self.getboundary(self.boundary[1], altBodyCharSet_, "text/plain", altBodyEncoding_)
                body_ += self.encodestring(self.AltBody, altBodyEncoding_)
                body_ += self.LE + self.LE
                body_ += self.getboundary(self.boundary[1], bodyCharSet_, "text/html", bodyEncoding_)
                body_ += self.encodestring(self.Body, bodyEncoding_)
                body_ += self.LE + self.LE
                if (not php_empty(lambda : self.Ical)):
                    body_ += self.getboundary(self.boundary[1], "", "text/calendar; method=REQUEST", "")
                    body_ += self.encodestring(self.Ical, self.Encoding)
                    body_ += self.LE + self.LE
                # end if
                body_ += self.endboundary(self.boundary[1])
                break
            # end if
            if case("alt_inline"):
                body_ += mimepre_
                body_ += self.getboundary(self.boundary[1], altBodyCharSet_, "text/plain", altBodyEncoding_)
                body_ += self.encodestring(self.AltBody, altBodyEncoding_)
                body_ += self.LE + self.LE
                body_ += self.textline("--" + self.boundary[1])
                body_ += self.headerline("Content-Type", "multipart/related;")
                body_ += self.textline("    boundary=\"" + self.boundary[2] + "\"")
                body_ += self.LE
                body_ += self.getboundary(self.boundary[2], bodyCharSet_, "text/html", bodyEncoding_)
                body_ += self.encodestring(self.Body, bodyEncoding_)
                body_ += self.LE + self.LE
                body_ += self.attachall("inline", self.boundary[2])
                body_ += self.LE
                body_ += self.endboundary(self.boundary[1])
                break
            # end if
            if case("alt_attach"):
                body_ += mimepre_
                body_ += self.textline("--" + self.boundary[1])
                body_ += self.headerline("Content-Type", "multipart/alternative;")
                body_ += self.textline("    boundary=\"" + self.boundary[2] + "\"")
                body_ += self.LE
                body_ += self.getboundary(self.boundary[2], altBodyCharSet_, "text/plain", altBodyEncoding_)
                body_ += self.encodestring(self.AltBody, altBodyEncoding_)
                body_ += self.LE + self.LE
                body_ += self.getboundary(self.boundary[2], bodyCharSet_, "text/html", bodyEncoding_)
                body_ += self.encodestring(self.Body, bodyEncoding_)
                body_ += self.LE + self.LE
                body_ += self.endboundary(self.boundary[2])
                body_ += self.LE
                body_ += self.attachall("attachment", self.boundary[1])
                break
            # end if
            if case("alt_inline_attach"):
                body_ += mimepre_
                body_ += self.textline("--" + self.boundary[1])
                body_ += self.headerline("Content-Type", "multipart/alternative;")
                body_ += self.textline("    boundary=\"" + self.boundary[2] + "\"")
                body_ += self.LE
                body_ += self.getboundary(self.boundary[2], altBodyCharSet_, "text/plain", altBodyEncoding_)
                body_ += self.encodestring(self.AltBody, altBodyEncoding_)
                body_ += self.LE + self.LE
                body_ += self.textline("--" + self.boundary[2])
                body_ += self.headerline("Content-Type", "multipart/related;")
                body_ += self.textline("    boundary=\"" + self.boundary[3] + "\"")
                body_ += self.LE
                body_ += self.getboundary(self.boundary[3], bodyCharSet_, "text/html", bodyEncoding_)
                body_ += self.encodestring(self.Body, bodyEncoding_)
                body_ += self.LE + self.LE
                body_ += self.attachall("inline", self.boundary[3])
                body_ += self.LE
                body_ += self.endboundary(self.boundary[2])
                body_ += self.LE
                body_ += self.attachall("attachment", self.boundary[1])
                break
            # end if
            if case():
                #// Catch case 'plain' and case '', applies to simple `text/plain` and `text/html` body content types
                #// Reset the `Encoding` property in case we changed it for line length reasons
                self.Encoding = bodyEncoding_
                body_ += self.encodestring(self.Body, self.Encoding)
                break
            # end if
        # end for
        if self.iserror():
            body_ = ""
        elif self.sign_key_file:
            try: 
                if (not php_defined("PKCS7_TEXT")):
                    raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("extension_missing") + "openssl"))
                # end if
                #// @TODO would be nice to use php://temp streams here, but need to wrap for PHP < 5.1
                file_ = php_tempnam(php_sys_get_temp_dir(), "mail")
                if False == file_put_contents(file_, body_):
                    raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("signing") + " Could not write temp file"))
                # end if
                signed_ = php_tempnam(php_sys_get_temp_dir(), "signed")
                #// Workaround for PHP bug https://bugs.php.net/bug.php?id=69197
                if php_empty(lambda : self.sign_extracerts_file):
                    sign_ = php_no_error(lambda: openssl_pkcs7_sign(file_, signed_, "file://" + php_realpath(self.sign_cert_file), Array("file://" + php_realpath(self.sign_key_file), self.sign_key_pass), None))
                else:
                    sign_ = php_no_error(lambda: openssl_pkcs7_sign(file_, signed_, "file://" + php_realpath(self.sign_cert_file), Array("file://" + php_realpath(self.sign_key_file), self.sign_key_pass), None, PKCS7_DETACHED, self.sign_extracerts_file))
                # end if
                if sign_:
                    php_no_error(lambda: unlink(file_))
                    body_ = php_file_get_contents(signed_)
                    php_no_error(lambda: unlink(signed_))
                    #// The message returned by openssl contains both headers and body, so need to split them up
                    parts_ = php_explode("\n\n", body_, 2)
                    self.MIMEHeader += parts_[0] + self.LE + self.LE
                    body_ = parts_[1]
                else:
                    php_no_error(lambda: unlink(file_))
                    php_no_error(lambda: unlink(signed_))
                    raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("signing") + openssl_error_string()))
                # end if
            except phpmailerException as exc_:
                body_ = ""
                if self.exceptions:
                    raise exc_
                # end if
            # end try
        # end if
        return body_
    # end def createbody
    #// 
    #// Return the start of a message boundary.
    #// @access protected
    #// @param string $boundary
    #// @param string $charSet
    #// @param string $contentType
    #// @param string $encoding
    #// @return string
    #//
    def getboundary(self, boundary_=None, charSet_=None, contentType_=None, encoding_=None):
        
        
        result_ = ""
        if charSet_ == "":
            charSet_ = self.CharSet
        # end if
        if contentType_ == "":
            contentType_ = self.ContentType
        # end if
        if encoding_ == "":
            encoding_ = self.Encoding
        # end if
        result_ += self.textline("--" + boundary_)
        result_ += php_sprintf("Content-Type: %s; charset=%s", contentType_, charSet_)
        result_ += self.LE
        #// RFC1341 part 5 says 7bit is assumed if not specified
        if encoding_ != "7bit":
            result_ += self.headerline("Content-Transfer-Encoding", encoding_)
        # end if
        result_ += self.LE
        return result_
    # end def getboundary
    #// 
    #// Return the end of a message boundary.
    #// @access protected
    #// @param string $boundary
    #// @return string
    #//
    def endboundary(self, boundary_=None):
        
        
        return self.LE + "--" + boundary_ + "--" + self.LE
    # end def endboundary
    #// 
    #// Set the message type.
    #// PHPMailer only supports some preset message types, not arbitrary MIME structures.
    #// @access protected
    #// @return void
    #//
    def setmessagetype(self):
        
        
        type_ = Array()
        if self.alternativeexists():
            type_[-1] = "alt"
        # end if
        if self.inlineimageexists():
            type_[-1] = "inline"
        # end if
        if self.attachmentexists():
            type_[-1] = "attach"
        # end if
        self.message_type = php_implode("_", type_)
        if self.message_type == "":
            #// The 'plain' message_type refers to the message having a single body element, not that it is plain-text
            self.message_type = "plain"
        # end if
    # end def setmessagetype
    #// 
    #// Format a header line.
    #// @access public
    #// @param string $name
    #// @param string $value
    #// @return string
    #//
    def headerline(self, name_=None, value_=None):
        
        
        return name_ + ": " + value_ + self.LE
    # end def headerline
    #// 
    #// Return a formatted mail line.
    #// @access public
    #// @param string $value
    #// @return string
    #//
    def textline(self, value_=None):
        
        
        return value_ + self.LE
    # end def textline
    #// 
    #// Add an attachment from a path on the filesystem.
    #// Never use a user-supplied path to a file!
    #// Returns false if the file could not be found or read.
    #// Explicitly *does not* support passing URLs; PHPMailer is not an HTTP client.
    #// If you need to do that, fetch the resource yourself and pass it in via a local file or string.
    #// @param string $path Path to the attachment.
    #// @param string $name Overrides the attachment name.
    #// @param string $encoding File encoding (see $Encoding).
    #// @param string $type File extension (MIME) type.
    #// @param string $disposition Disposition to use
    #// @throws phpmailerException
    #// @return boolean
    #//
    def addattachment(self, path_=None, name_="", encoding_="base64", type_="", disposition_="attachment"):
        
        
        try: 
            if (not self.ispermittedpath(path_)) or (not php_no_error(lambda: php_is_file(path_))):
                raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("file_access") + path_, self.STOP_CONTINUE))
            # end if
            #// If a MIME type is not specified, try to work it out from the file name
            if type_ == "":
                type_ = self.filenametotype(path_)
            # end if
            filename_ = php_basename(path_)
            if name_ == "":
                name_ = filename_
            # end if
            self.attachment[-1] = Array({0: path_, 1: filename_, 2: name_, 3: encoding_, 4: type_, 5: False, 6: disposition_, 7: 0})
        except phpmailerException as exc_:
            self.seterror(exc_.getmessage())
            self.edebug(exc_.getmessage())
            if self.exceptions:
                raise exc_
            # end if
            return False
        # end try
        return True
    # end def addattachment
    #// 
    #// Return the array of attachments.
    #// @return array
    #//
    def getattachments(self):
        
        
        return self.attachment
    # end def getattachments
    #// 
    #// Attach all file, string, and binary attachments to the message.
    #// Returns an empty string on failure.
    #// @access protected
    #// @param string $disposition_type
    #// @param string $boundary
    #// @return string
    #//
    def attachall(self, disposition_type_=None, boundary_=None):
        
        
        #// Return text of body
        mime_ = Array()
        cidUniq_ = Array()
        incl_ = Array()
        #// Add all attachments
        for attachment_ in self.attachment:
            #// Check if it is a valid disposition_filter
            if attachment_[6] == disposition_type_:
                #// Check for string attachment
                string_ = ""
                path_ = ""
                bString_ = attachment_[5]
                if bString_:
                    string_ = attachment_[0]
                else:
                    path_ = attachment_[0]
                # end if
                inclhash_ = php_md5(serialize(attachment_))
                if php_in_array(inclhash_, incl_):
                    continue
                # end if
                incl_[-1] = inclhash_
                name_ = attachment_[2]
                encoding_ = attachment_[3]
                type_ = attachment_[4]
                disposition_ = attachment_[6]
                cid_ = attachment_[7]
                if disposition_ == "inline" and php_array_key_exists(cid_, cidUniq_):
                    continue
                # end if
                cidUniq_[cid_] = True
                mime_[-1] = php_sprintf("--%s%s", boundary_, self.LE)
                #// Only include a filename property if we have one
                if (not php_empty(lambda : name_)):
                    mime_[-1] = php_sprintf("Content-Type: %s; name=\"%s\"%s", type_, self.encodeheader(self.secureheader(name_)), self.LE)
                else:
                    mime_[-1] = php_sprintf("Content-Type: %s%s", type_, self.LE)
                # end if
                #// RFC1341 part 5 says 7bit is assumed if not specified
                if encoding_ != "7bit":
                    mime_[-1] = php_sprintf("Content-Transfer-Encoding: %s%s", encoding_, self.LE)
                # end if
                if disposition_ == "inline":
                    mime_[-1] = php_sprintf("Content-ID: <%s>%s", cid_, self.LE)
                # end if
                #// If a filename contains any of these chars, it should be quoted,
                #// but not otherwise: RFC2183 & RFC2045 5.1
                #// Fixes a warning in IETF's msglint MIME checker
                #// Allow for bypassing the Content-Disposition header totally
                if (not php_empty(lambda : disposition_)):
                    encoded_name_ = self.encodeheader(self.secureheader(name_))
                    if php_preg_match("/[ \\(\\)<>@,;:\\\"\\/\\[\\]\\?=]/", encoded_name_):
                        mime_[-1] = php_sprintf("Content-Disposition: %s; filename=\"%s\"%s", disposition_, encoded_name_, self.LE + self.LE)
                    else:
                        if (not php_empty(lambda : encoded_name_)):
                            mime_[-1] = php_sprintf("Content-Disposition: %s; filename=%s%s", disposition_, encoded_name_, self.LE + self.LE)
                        else:
                            mime_[-1] = php_sprintf("Content-Disposition: %s%s", disposition_, self.LE + self.LE)
                        # end if
                    # end if
                else:
                    mime_[-1] = self.LE
                # end if
                #// Encode as string attachment
                if bString_:
                    mime_[-1] = self.encodestring(string_, encoding_)
                    if self.iserror():
                        return ""
                    # end if
                    mime_[-1] = self.LE + self.LE
                else:
                    mime_[-1] = self.encodefile(path_, encoding_)
                    if self.iserror():
                        return ""
                    # end if
                    mime_[-1] = self.LE + self.LE
                # end if
            # end if
        # end for
        mime_[-1] = php_sprintf("--%s--%s", boundary_, self.LE)
        return php_implode("", mime_)
    # end def attachall
    #// 
    #// Encode a file attachment in requested format.
    #// Returns an empty string on failure.
    #// @param string $path The full path to the file
    #// @param string $encoding The encoding to use; one of 'base64', '7bit', '8bit', 'binary', 'quoted-printable'
    #// @throws phpmailerException
    #// @access protected
    #// @return string
    #//
    def encodefile(self, path_=None, encoding_="base64"):
        
        
        try: 
            if (not self.ispermittedpath(path_)) or (not php_file_exists(path_)):
                raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("file_open") + path_, self.STOP_CONTINUE))
            # end if
            magic_quotes_ = PHP_VERSION_ID < 70400 and get_magic_quotes_runtime()
            #// WP: Patched for PHP 7.4.
            if magic_quotes_:
                if php_version_compare(PHP_VERSION, "5.3.0", "<"):
                    set_magic_quotes_runtime(False)
                else:
                    #// Doesn't exist in PHP 5.4, but we don't need to check because
                    #// get_magic_quotes_runtime always returns false in 5.4+
                    #// so it will never get here
                    php_ini_set("magic_quotes_runtime", False)
                # end if
            # end if
            file_buffer_ = php_file_get_contents(path_)
            file_buffer_ = self.encodestring(file_buffer_, encoding_)
            if magic_quotes_:
                if php_version_compare(PHP_VERSION, "5.3.0", "<"):
                    set_magic_quotes_runtime(magic_quotes_)
                else:
                    php_ini_set("magic_quotes_runtime", magic_quotes_)
                # end if
            # end if
            return file_buffer_
        except Exception as exc_:
            self.seterror(exc_.getmessage())
            return ""
        # end try
    # end def encodefile
    #// 
    #// Encode a string in requested format.
    #// Returns an empty string on failure.
    #// @param string $str The text to encode
    #// @param string $encoding The encoding to use; one of 'base64', '7bit', '8bit', 'binary', 'quoted-printable'
    #// @access public
    #// @return string
    #//
    def encodestring(self, str_=None, encoding_="base64"):
        
        
        encoded_ = ""
        for case in Switch(php_strtolower(encoding_)):
            if case("base64"):
                encoded_ = chunk_split(php_base64_encode(str_), 76, self.LE)
                break
            # end if
            if case("7bit"):
                pass
            # end if
            if case("8bit"):
                encoded_ = self.fixeol(str_)
                #// Make sure it ends with a line break
                if php_substr(encoded_, -php_strlen(self.LE)) != self.LE:
                    encoded_ += self.LE
                # end if
                break
            # end if
            if case("binary"):
                encoded_ = str_
                break
            # end if
            if case("quoted-printable"):
                encoded_ = self.encodeqp(str_)
                break
            # end if
            if case():
                self.seterror(self.lang("encoding") + encoding_)
                break
            # end if
        # end for
        return encoded_
    # end def encodestring
    #// 
    #// Encode a header string optimally.
    #// Picks shortest of Q, B, quoted-printable or none.
    #// @access public
    #// @param string $str
    #// @param string $position
    #// @return string
    #//
    def encodeheader(self, str_=None, position_="text"):
        
        
        matchcount_ = 0
        for case in Switch(php_strtolower(position_)):
            if case("phrase"):
                if (not php_preg_match("/[\\200-\\377]/", str_)):
                    #// Can't use addslashes as we don't know the value of magic_quotes_sybase
                    encoded_ = addcslashes(str_, " ..\\\"")
                    if str_ == encoded_ and (not php_preg_match("/[^A-Za-z0-9!#$%&'*+\\/=?^_`{|}~ -]/", str_)):
                        return encoded_
                    else:
                        return str("\"") + str(encoded_) + str("\"")
                    # end if
                # end if
                matchcount_ = preg_match_all("/[^\\040\\041\\043-\\133\\135-\\176]/", str_, matches_)
                break
            # end if
            if case("comment"):
                matchcount_ = preg_match_all("/[()\"]/", str_, matches_)
            # end if
            if case("text"):
                pass
            # end if
            if case():
                matchcount_ += preg_match_all("/[\\000-\\010\\013\\014\\016-\\037\\177-\\377]/", str_, matches_)
                break
            # end if
        # end for
        #// There are no chars that need encoding
        if matchcount_ == 0:
            return str_
        # end if
        maxlen_ = 75 - 7 - php_strlen(self.CharSet)
        #// Try to select the encoding which should produce the shortest output
        if matchcount_ > php_strlen(str_) / 3:
            #// More than a third of the content will need encoding, so B encoding will be most efficient
            encoding_ = "B"
            if php_function_exists("mb_strlen") and self.hasmultibytes(str_):
                #// Use a custom function which correctly encodes and wraps long
                #// multibyte strings without breaking lines within a character
                encoded_ = self.base64encodewrapmb(str_, "\n")
            else:
                encoded_ = php_base64_encode(str_)
                maxlen_ -= maxlen_ % 4
                encoded_ = php_trim(chunk_split(encoded_, maxlen_, "\n"))
            # end if
        else:
            encoding_ = "Q"
            encoded_ = self.encodeq(str_, position_)
            encoded_ = self.wraptext(encoded_, maxlen_, True)
            encoded_ = php_str_replace("=" + self.CRLF, "\n", php_trim(encoded_))
        # end if
        encoded_ = php_preg_replace("/^(.*)$/m", " =?" + self.CharSet + str("?") + str(encoding_) + str("?\\1?="), encoded_)
        encoded_ = php_trim(php_str_replace("\n", self.LE, encoded_))
        return encoded_
    # end def encodeheader
    #// 
    #// Check if a string contains multi-byte characters.
    #// @access public
    #// @param string $str multi-byte text to wrap encode
    #// @return boolean
    #//
    def hasmultibytes(self, str_=None):
        
        
        if php_function_exists("mb_strlen"):
            return php_strlen(str_) > php_mb_strlen(str_, self.CharSet)
        else:
            #// Assume no multibytes (we can't handle without mbstring functions anyway)
            return False
        # end if
    # end def hasmultibytes
    #// 
    #// Does a string contain any 8-bit chars (in any charset)?
    #// @param string $text
    #// @return boolean
    #//
    def has8bitchars(self, text_=None):
        
        
        return php_bool(php_preg_match("/[\\x80-\\xFF]/", text_))
    # end def has8bitchars
    #// 
    #// Encode and wrap long multibyte strings for mail headers
    #// without breaking lines within a character.
    #// Adapted from a function by paravoid
    #// @link http://www.php.net/manual/en/function.mb-encode-mimeheader.php#60283
    #// @access public
    #// @param string $str multi-byte text to wrap encode
    #// @param string $linebreak string to use as linefeed/end-of-line
    #// @return string
    #//
    def base64encodewrapmb(self, str_=None, linebreak_=None):
        if linebreak_ is None:
            linebreak_ = None
        # end if
        
        start_ = "=?" + self.CharSet + "?B?"
        end_ = "?="
        encoded_ = ""
        if linebreak_ == None:
            linebreak_ = self.LE
        # end if
        mb_length_ = php_mb_strlen(str_, self.CharSet)
        #// Each line must have length <= 75, including $start and $end
        length_ = 75 - php_strlen(start_) - php_strlen(end_)
        #// Average multi-byte ratio
        ratio_ = mb_length_ / php_strlen(str_)
        #// Base64 has a 4:3 ratio
        avgLength_ = floor(length_ * ratio_ * 0.75)
        i_ = 0
        while i_ < mb_length_:
            
            lookBack_ = 0
            while True:
                offset_ = avgLength_ - lookBack_
                chunk_ = php_mb_substr(str_, i_, offset_, self.CharSet)
                chunk_ = php_base64_encode(chunk_)
                lookBack_ += 1
                
                if php_strlen(chunk_) > length_:
                    break
                # end if
            # end while
            encoded_ += chunk_ + linebreak_
            i_ += offset_
        # end while
        #// Chomp the last linefeed
        encoded_ = php_substr(encoded_, 0, -php_strlen(linebreak_))
        return encoded_
    # end def base64encodewrapmb
    #// 
    #// Encode a string in quoted-printable format.
    #// According to RFC2045 section 6.7.
    #// @access public
    #// @param string $string The text to encode
    #// @param integer $line_max Number of chars allowed on a line before wrapping
    #// @return string
    #// @link http://www.php.net/manual/en/function.quoted-printable-decode.php#89417 Adapted from this comment
    #//
    def encodeqp(self, string_=None, line_max_=76):
        
        
        #// Use native function if it's available (>= PHP5.3)
        if php_function_exists("quoted_printable_encode"):
            return quoted_printable_encode(string_)
        # end if
        #// Fall back to a pure PHP implementation
        string_ = php_str_replace(Array("%20", "%0D%0A.", "%0D%0A", "%"), Array(" ", "\r\n=2E", "\r\n", "="), rawurlencode(string_))
        return php_preg_replace("/[^\\r\\n]{" + line_max_ - 3 + "}[^=\\r\\n]{2}/", "$0=\r\n", string_)
    # end def encodeqp
    #// 
    #// Backward compatibility wrapper for an old QP encoding function that was removed.
    #// @see PHPMailer::encodeQP()
    #// @access public
    #// @param string $string
    #// @param integer $line_max
    #// @param boolean $space_conv
    #// @return string
    #// @deprecated Use encodeQP instead.
    #//
    def encodeqpphp(self, string_=None, line_max_=76, space_conv_=None):
        if space_conv_ is None:
            space_conv_ = False
        # end if
        
        return self.encodeqp(string_, line_max_)
    # end def encodeqpphp
    #// 
    #// Encode a string using Q encoding.
    #// @link http://tools.ietf.org/html/rfc2047
    #// @param string $str the text to encode
    #// @param string $position Where the text is going to be used, see the RFC for what that means
    #// @access public
    #// @return string
    #//
    def encodeq(self, str_=None, position_="text"):
        
        
        #// There should not be any EOL in the string
        pattern_ = ""
        encoded_ = php_str_replace(Array("\r", "\n"), "", str_)
        for case in Switch(php_strtolower(position_)):
            if case("phrase"):
                #// RFC 2047 section 5.3
                pattern_ = "^A-Za-z0-9!*+\\/ -"
                break
            # end if
            if case("comment"):
                #// RFC 2047 section 5.2
                pattern_ = "\\(\\)\""
            # end if
            if case("text"):
                pass
            # end if
            if case():
                #// RFC 2047 section 5.1
                #// Replace every high ascii, control, =, ? and _ characters
                pattern_ = "\\000-\\011\\013\\014\\016-\\037\\075\\077\\137\\177-\\377" + pattern_
                break
            # end if
        # end for
        matches_ = Array()
        if preg_match_all(str("/[") + str(pattern_) + str("]/"), encoded_, matches_):
            #// If the string contains an '=', make sure it's the first thing we replace
            #// so as to avoid double-encoding
            eqkey_ = php_array_search("=", matches_[0])
            if False != eqkey_:
                matches_[0][eqkey_] = None
                array_unshift(matches_[0], "=")
            # end if
            for char_ in array_unique(matches_[0]):
                encoded_ = php_str_replace(char_, "=" + php_sprintf("%02X", php_ord(char_)), encoded_)
            # end for
        # end if
        #// Replace every spaces to _ (more readable than =20)
        return php_str_replace(" ", "_", encoded_)
    # end def encodeq
    #// 
    #// Add a string or binary attachment (non-filesystem).
    #// This method can be used to attach ascii or binary data,
    #// such as a BLOB record from a database.
    #// @param string $string String attachment data.
    #// @param string $filename Name of the attachment.
    #// @param string $encoding File encoding (see $Encoding).
    #// @param string $type File extension (MIME) type.
    #// @param string $disposition Disposition to use
    #// @return void
    #//
    def addstringattachment(self, string_=None, filename_=None, encoding_="base64", type_="", disposition_="attachment"):
        
        
        #// If a MIME type is not specified, try to work it out from the file name
        if type_ == "":
            type_ = self.filenametotype(filename_)
        # end if
        #// Append to $attachment array
        self.attachment[-1] = Array({0: string_, 1: filename_, 2: php_basename(filename_), 3: encoding_, 4: type_, 5: True, 6: disposition_, 7: 0})
    # end def addstringattachment
    #// 
    #// Add an embedded (inline) attachment from a file.
    #// This can include images, sounds, and just about any other document type.
    #// These differ from 'regular' attachments in that they are intended to be
    #// displayed inline with the message, not just attached for download.
    #// This is used in HTML messages that embed the images
    #// the HTML refers to using the $cid value.
    #// Never use a user-supplied path to a file!
    #// @param string $path Path to the attachment.
    #// @param string $cid Content ID of the attachment; Use this to reference
    #// the content when using an embedded image in HTML.
    #// @param string $name Overrides the attachment name.
    #// @param string $encoding File encoding (see $Encoding).
    #// @param string $type File MIME type.
    #// @param string $disposition Disposition to use
    #// @return boolean True on successfully adding an attachment
    #//
    def addembeddedimage(self, path_=None, cid_=None, name_="", encoding_="base64", type_="", disposition_="inline"):
        
        
        if (not self.ispermittedpath(path_)) or (not php_no_error(lambda: php_is_file(path_))):
            self.seterror(self.lang("file_access") + path_)
            return False
        # end if
        #// If a MIME type is not specified, try to work it out from the file name
        if type_ == "":
            type_ = self.filenametotype(path_)
        # end if
        filename_ = php_basename(path_)
        if name_ == "":
            name_ = filename_
        # end if
        #// Append to $attachment array
        self.attachment[-1] = Array({0: path_, 1: filename_, 2: name_, 3: encoding_, 4: type_, 5: False, 6: disposition_, 7: cid_})
        return True
    # end def addembeddedimage
    #// 
    #// Add an embedded stringified attachment.
    #// This can include images, sounds, and just about any other document type.
    #// Be sure to set the $type to an image type for images:
    #// JPEG images use 'image/jpeg', GIF uses 'image/gif', PNG uses 'image/png'.
    #// @param string $string The attachment binary data.
    #// @param string $cid Content ID of the attachment; Use this to reference
    #// the content when using an embedded image in HTML.
    #// @param string $name
    #// @param string $encoding File encoding (see $Encoding).
    #// @param string $type MIME type.
    #// @param string $disposition Disposition to use
    #// @return boolean True on successfully adding an attachment
    #//
    def addstringembeddedimage(self, string_=None, cid_=None, name_="", encoding_="base64", type_="", disposition_="inline"):
        
        
        #// If a MIME type is not specified, try to work it out from the name
        if type_ == "" and (not php_empty(lambda : name_)):
            type_ = self.filenametotype(name_)
        # end if
        #// Append to $attachment array
        self.attachment[-1] = Array({0: string_, 1: name_, 2: name_, 3: encoding_, 4: type_, 5: True, 6: disposition_, 7: cid_})
        return True
    # end def addstringembeddedimage
    #// 
    #// Check if an inline attachment is present.
    #// @access public
    #// @return boolean
    #//
    def inlineimageexists(self):
        
        
        for attachment_ in self.attachment:
            if attachment_[6] == "inline":
                return True
            # end if
        # end for
        return False
    # end def inlineimageexists
    #// 
    #// Check if an attachment (non-inline) is present.
    #// @return boolean
    #//
    def attachmentexists(self):
        
        
        for attachment_ in self.attachment:
            if attachment_[6] == "attachment":
                return True
            # end if
        # end for
        return False
    # end def attachmentexists
    #// 
    #// Check if this message has an alternative body set.
    #// @return boolean
    #//
    def alternativeexists(self):
        
        
        return (not php_empty(lambda : self.AltBody))
    # end def alternativeexists
    #// 
    #// Clear queued addresses of given kind.
    #// @access protected
    #// @param string $kind 'to', 'cc', or 'bcc'
    #// @return void
    #//
    def clearqueuedaddresses(self, kind_=None):
        
        
        RecipientsQueue_ = self.RecipientsQueue
        for address_,params_ in RecipientsQueue_.items():
            if params_[0] == kind_:
                self.RecipientsQueue[address_] = None
            # end if
        # end for
    # end def clearqueuedaddresses
    #// 
    #// Clear all To recipients.
    #// @return void
    #//
    def clearaddresses(self):
        
        
        for to_ in self.to:
            self.all_recipients[php_strtolower(to_[0])] = None
        # end for
        self.to = Array()
        self.clearqueuedaddresses("to")
    # end def clearaddresses
    #// 
    #// Clear all CC recipients.
    #// @return void
    #//
    def clearccs(self):
        
        
        for cc_ in self.cc:
            self.all_recipients[php_strtolower(cc_[0])] = None
        # end for
        self.cc = Array()
        self.clearqueuedaddresses("cc")
    # end def clearccs
    #// 
    #// Clear all BCC recipients.
    #// @return void
    #//
    def clearbccs(self):
        
        
        for bcc_ in self.bcc:
            self.all_recipients[php_strtolower(bcc_[0])] = None
        # end for
        self.bcc = Array()
        self.clearqueuedaddresses("bcc")
    # end def clearbccs
    #// 
    #// Clear all ReplyTo recipients.
    #// @return void
    #//
    def clearreplytos(self):
        
        
        self.ReplyTo = Array()
        self.ReplyToQueue = Array()
    # end def clearreplytos
    #// 
    #// Clear all recipient types.
    #// @return void
    #//
    def clearallrecipients(self):
        
        
        self.to = Array()
        self.cc = Array()
        self.bcc = Array()
        self.all_recipients = Array()
        self.RecipientsQueue = Array()
    # end def clearallrecipients
    #// 
    #// Clear all filesystem, string, and binary attachments.
    #// @return void
    #//
    def clearattachments(self):
        
        
        self.attachment = Array()
    # end def clearattachments
    #// 
    #// Clear all custom headers.
    #// @return void
    #//
    def clearcustomheaders(self):
        
        
        self.CustomHeader = Array()
    # end def clearcustomheaders
    #// 
    #// Add an error message to the error container.
    #// @access protected
    #// @param string $msg
    #// @return void
    #//
    def seterror(self, msg_=None):
        
        
        self.error_count += 1
        if self.Mailer == "smtp" and (not php_is_null(self.smtp)):
            lasterror_ = self.smtp.geterror()
            if (not php_empty(lambda : lasterror_["error"])):
                msg_ += self.lang("smtp_error") + lasterror_["error"]
                if (not php_empty(lambda : lasterror_["detail"])):
                    msg_ += " Detail: " + lasterror_["detail"]
                # end if
                if (not php_empty(lambda : lasterror_["smtp_code"])):
                    msg_ += " SMTP code: " + lasterror_["smtp_code"]
                # end if
                if (not php_empty(lambda : lasterror_["smtp_code_ex"])):
                    msg_ += " Additional SMTP info: " + lasterror_["smtp_code_ex"]
                # end if
            # end if
        # end if
        self.ErrorInfo = msg_
    # end def seterror
    #// 
    #// Return an RFC 822 formatted date.
    #// @access public
    #// @return string
    #// @static
    #//
    @classmethod
    def rfcdate(self):
        
        
        #// Set the time zone to whatever the default is to avoid 500 errors
        #// Will default to UTC if it's not set properly in php.ini
        php_date_default_timezone_set(php_no_error(lambda: php_date_default_timezone_get()))
        return date("D, j M Y H:i:s O")
    # end def rfcdate
    #// 
    #// Get the server hostname.
    #// Returns 'localhost.localdomain' if unknown.
    #// @access protected
    #// @return string
    #//
    def serverhostname(self):
        
        
        result_ = "localhost.localdomain"
        if (not php_empty(lambda : self.Hostname)):
            result_ = self.Hostname
        elif (php_isset(lambda : PHP_SERVER)) and php_array_key_exists("SERVER_NAME", PHP_SERVER) and (not php_empty(lambda : PHP_SERVER["SERVER_NAME"])):
            result_ = PHP_SERVER["SERVER_NAME"]
        elif php_function_exists("gethostname") and gethostname() != False:
            result_ = gethostname()
        elif php_uname("n") != False:
            result_ = php_uname("n")
        # end if
        return result_
    # end def serverhostname
    #// 
    #// Get an error message in the current language.
    #// @access protected
    #// @param string $key
    #// @return string
    #//
    def lang(self, key_=None):
        
        
        if php_count(self.language) < 1:
            self.setlanguage("en")
            pass
        # end if
        if php_array_key_exists(key_, self.language):
            if key_ == "smtp_connect_failed":
                #// Include a link to troubleshooting docs on SMTP connection failure
                #// this is by far the biggest cause of support questions
                #// but it's usually not PHPMailer's fault.
                return self.language[key_] + " https://github.com/PHPMailer/PHPMailer/wiki/Troubleshooting"
            # end if
            return self.language[key_]
        else:
            #// Return the key as a fallback
            return key_
        # end if
    # end def lang
    #// 
    #// Check if an error occurred.
    #// @access public
    #// @return boolean True if an error did occur.
    #//
    def iserror(self):
        
        
        return self.error_count > 0
    # end def iserror
    #// 
    #// Ensure consistent line endings in a string.
    #// Changes every end of line from CRLF, CR or LF to $this->LE.
    #// @access public
    #// @param string $str String to fixEOL
    #// @return string
    #//
    def fixeol(self, str_=None):
        
        
        #// Normalise to \n
        nstr_ = php_str_replace(Array("\r\n", "\r"), "\n", str_)
        #// Now convert LE as needed
        if self.LE != "\n":
            nstr_ = php_str_replace("\n", self.LE, nstr_)
        # end if
        return nstr_
    # end def fixeol
    #// 
    #// Add a custom header.
    #// $name value can be overloaded to contain
    #// both header name and value (name:value)
    #// @access public
    #// @param string $name Custom header name
    #// @param string $value Header value
    #// @return void
    #//
    def addcustomheader(self, name_=None, value_=None):
        if value_ is None:
            value_ = None
        # end if
        
        if value_ == None:
            #// Value passed in as name:value
            self.CustomHeader[-1] = php_explode(":", name_, 2)
        else:
            self.CustomHeader[-1] = Array(name_, value_)
        # end if
    # end def addcustomheader
    #// 
    #// Returns all custom headers.
    #// @return array
    #//
    def getcustomheaders(self):
        
        
        return self.CustomHeader
    # end def getcustomheaders
    #// 
    #// Create a message body from an HTML string.
    #// Automatically inlines images and creates a plain-text version by converting the HTML,
    #// overwriting any existing values in Body and AltBody.
    #// Do not source $message content from user input!
    #// $basedir is prepended when handling relative URLs, e.g. <img src="/images/a.png"> and must not be empty
    #// will look for an image file in $basedir/images/a.png and convert it to inline.
    #// If you don't provide a $basedir, relative paths will be left untouched (and thus probably break in email)
    #// If you don't want to apply these transformations to your HTML, just set Body and AltBody directly.
    #// @access public
    #// @param string $message HTML message string
    #// @param string $basedir Absolute path to a base directory to prepend to relative paths to images
    #// @param boolean|callable $advanced Whether to use the internal HTML to text converter
    #// or your own custom converter @see PHPMailer::html2text()
    #// @return string $message The transformed message Body
    #//
    def msghtml(self, message_=None, basedir_="", advanced_=None):
        if advanced_ is None:
            advanced_ = False
        # end if
        
        preg_match_all("/(src|background)=[\"'](.*)[\"']/Ui", message_, images_)
        if php_array_key_exists(2, images_):
            if php_strlen(basedir_) > 1 and php_substr(basedir_, -1) != "/":
                #// Ensure $basedir has a trailing
                basedir_ += "/"
            # end if
            for imgindex_,url_ in images_[2].items():
                #// Convert data URIs into embedded images
                if php_preg_match("#^data:(image[^;,]*)(;base64)?,#", url_, match_):
                    data_ = php_substr(url_, php_strpos(url_, ","))
                    if match_[2]:
                        data_ = php_base64_decode(data_)
                    else:
                        data_ = rawurldecode(data_)
                    # end if
                    cid_ = php_md5(url_) + "@phpmailer.0"
                    #// RFC2392 S 2
                    if self.addstringembeddedimage(data_, cid_, "embed" + imgindex_, "base64", match_[1]):
                        message_ = php_str_replace(images_[0][imgindex_], images_[1][imgindex_] + "=\"cid:" + cid_ + "\"", message_)
                    # end if
                    continue
                # end if
                if (not php_empty(lambda : basedir_)) and php_strpos(url_, "..") == False and php_substr(url_, 0, 4) != "cid:" and (not php_preg_match("#^[a-z][a-z0-9+.-]*:?//#i", url_)):
                    filename_ = php_basename(url_)
                    directory_ = php_dirname(url_)
                    if directory_ == ".":
                        directory_ = ""
                    # end if
                    cid_ = php_md5(url_) + "@phpmailer.0"
                    #// RFC2392 S 2
                    if php_strlen(directory_) > 1 and php_substr(directory_, -1) != "/":
                        directory_ += "/"
                    # end if
                    if self.addembeddedimage(basedir_ + directory_ + filename_, cid_, filename_, "base64", self._mime_types(php_str(self.mb_pathinfo(filename_, PATHINFO_EXTENSION)))):
                        message_ = php_preg_replace("/" + images_[1][imgindex_] + "=[\"']" + preg_quote(url_, "/") + "[\"']/Ui", images_[1][imgindex_] + "=\"cid:" + cid_ + "\"", message_)
                    # end if
                # end if
            # end for
        # end if
        self.ishtml(True)
        #// Convert all message body line breaks to CRLF, makes quoted-printable encoding work much better
        self.Body = self.normalizebreaks(message_)
        self.AltBody = self.normalizebreaks(self.html2text(message_, advanced_))
        if (not self.alternativeexists()):
            self.AltBody = "To view this email message, open it in a program that understands HTML!" + self.CRLF + self.CRLF
        # end if
        return self.Body
    # end def msghtml
    #// 
    #// Convert an HTML string into plain text.
    #// This is used by msgHTML().
    #// Note - older versions of this function used a bundled advanced converter
    #// which was been removed for license reasons in #232.
    #// Example usage:
    #// <code>
    #// Use default conversion
    #// $plain = $mail->html2text($html);
    #// Use your own custom converter
    #// $plain = $mail->html2text($html, function($html) {
    #// $converter = new MyHtml2text($html);
    #// return $converter->get_text();
    #// });
    #// </code>
    #// @param string $html The HTML text to convert
    #// @param boolean|callable $advanced Any boolean value to use the internal converter,
    #// or provide your own callable for custom conversion.
    #// @return string
    #//
    def html2text(self, html_=None, advanced_=None):
        if advanced_ is None:
            advanced_ = False
        # end if
        
        if php_is_callable(advanced_):
            return php_call_user_func(advanced_, html_)
        # end if
        return html_entity_decode(php_trim(strip_tags(php_preg_replace("/<(head|title|style|script)[^>]*>.*?<\\/\\1>/si", "", html_))), ENT_QUOTES, self.CharSet)
    # end def html2text
    #// 
    #// Get the MIME type for a file extension.
    #// @param string $ext File extension
    #// @access public
    #// @return string MIME type of file.
    #// @static
    #//
    @classmethod
    def _mime_types(self, ext_=""):
        
        
        mimes_ = Array({"xl": "application/excel", "js": "application/javascript", "hqx": "application/mac-binhex40", "cpt": "application/mac-compactpro", "bin": "application/macbinary", "doc": "application/msword", "word": "application/msword", "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "xltx": "application/vnd.openxmlformats-officedocument.spreadsheetml.template", "potx": "application/vnd.openxmlformats-officedocument.presentationml.template", "ppsx": "application/vnd.openxmlformats-officedocument.presentationml.slideshow", "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation", "sldx": "application/vnd.openxmlformats-officedocument.presentationml.slide", "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "dotx": "application/vnd.openxmlformats-officedocument.wordprocessingml.template", "xlam": "application/vnd.ms-excel.addin.macroEnabled.12", "xlsb": "application/vnd.ms-excel.sheet.binary.macroEnabled.12", "class": "application/octet-stream", "dll": "application/octet-stream", "dms": "application/octet-stream", "exe": "application/octet-stream", "lha": "application/octet-stream", "lzh": "application/octet-stream", "psd": "application/octet-stream", "sea": "application/octet-stream", "so": "application/octet-stream", "oda": "application/oda", "pdf": "application/pdf", "ai": "application/postscript", "eps": "application/postscript", "ps": "application/postscript", "smi": "application/smil", "smil": "application/smil", "mif": "application/vnd.mif", "xls": "application/vnd.ms-excel", "ppt": "application/vnd.ms-powerpoint", "wbxml": "application/vnd.wap.wbxml", "wmlc": "application/vnd.wap.wmlc", "dcr": "application/x-director", "dir": "application/x-director", "dxr": "application/x-director", "dvi": "application/x-dvi", "gtar": "application/x-gtar", "php3": "application/x-httpd-php", "php4": "application/x-httpd-php", "php": "application/x-httpd-php", "phtml": "application/x-httpd-php", "phps": "application/x-httpd-php-source", "swf": "application/x-shockwave-flash", "sit": "application/x-stuffit", "tar": "application/x-tar", "tgz": "application/x-tar", "xht": "application/xhtml+xml", "xhtml": "application/xhtml+xml", "zip": "application/zip", "mid": "audio/midi", "midi": "audio/midi", "mp2": "audio/mpeg", "mp3": "audio/mpeg", "mpga": "audio/mpeg", "aif": "audio/x-aiff", "aifc": "audio/x-aiff", "aiff": "audio/x-aiff", "ram": "audio/x-pn-realaudio", "rm": "audio/x-pn-realaudio", "rpm": "audio/x-pn-realaudio-plugin", "ra": "audio/x-realaudio", "wav": "audio/x-wav", "bmp": "image/bmp", "gif": "image/gif", "jpeg": "image/jpeg", "jpe": "image/jpeg", "jpg": "image/jpeg", "png": "image/png", "tiff": "image/tiff", "tif": "image/tiff", "eml": "message/rfc822", "css": "text/css", "html": "text/html", "htm": "text/html", "shtml": "text/html", "log": "text/plain", "text": "text/plain", "txt": "text/plain", "rtx": "text/richtext", "rtf": "text/rtf", "vcf": "text/vcard", "vcard": "text/vcard", "xml": "text/xml", "xsl": "text/xml", "mpeg": "video/mpeg", "mpe": "video/mpeg", "mpg": "video/mpeg", "mov": "video/quicktime", "qt": "video/quicktime", "rv": "video/vnd.rn-realvideo", "avi": "video/x-msvideo", "movie": "video/x-sgi-movie"})
        if php_array_key_exists(php_strtolower(ext_), mimes_):
            return mimes_[php_strtolower(ext_)]
        # end if
        return "application/octet-stream"
    # end def _mime_types
    #// 
    #// Map a file name to a MIME type.
    #// Defaults to 'application/octet-stream', i.e.. arbitrary binary data.
    #// @param string $filename A file name or full path, does not need to exist as a file
    #// @return string
    #// @static
    #//
    @classmethod
    def filenametotype(self, filename_=None):
        
        
        #// In case the path is a URL, strip any query string before getting extension
        qpos_ = php_strpos(filename_, "?")
        if False != qpos_:
            filename_ = php_substr(filename_, 0, qpos_)
        # end if
        pathinfo_ = self.mb_pathinfo(filename_)
        return self._mime_types(pathinfo_["extension"])
    # end def filenametotype
    #// 
    #// Multi-byte-safe pathinfo replacement.
    #// Drop-in replacement for pathinfo(), but multibyte-safe, cross-platform-safe, old-version-safe.
    #// Works similarly to the one in PHP >= 5.2.0
    #// @link http://www.php.net/manual/en/function.pathinfo.php#107461
    #// @param string $path A filename or path, does not need to exist as a file
    #// @param integer|string $options Either a PATHINFO_* constant,
    #// or a string name to return only the specified piece, allows 'filename' to work on PHP < 5.2
    #// @return string|array
    #// @static
    #//
    @classmethod
    def mb_pathinfo(self, path_=None, options_=None):
        if options_ is None:
            options_ = None
        # end if
        
        ret_ = Array({"dirname": "", "basename": "", "extension": "", "filename": ""})
        pathinfo_ = Array()
        if php_preg_match("%^(.*?)[\\\\/]*(([^/\\\\]*?)(\\.([^\\.\\\\/]+?)|))[\\\\/\\.]*$%im", path_, pathinfo_):
            if php_array_key_exists(1, pathinfo_):
                ret_["dirname"] = pathinfo_[1]
            # end if
            if php_array_key_exists(2, pathinfo_):
                ret_["basename"] = pathinfo_[2]
            # end if
            if php_array_key_exists(5, pathinfo_):
                ret_["extension"] = pathinfo_[5]
            # end if
            if php_array_key_exists(3, pathinfo_):
                ret_["filename"] = pathinfo_[3]
            # end if
        # end if
        for case in Switch(options_):
            if case(PATHINFO_DIRNAME):
                pass
            # end if
            if case("dirname"):
                return ret_["dirname"]
            # end if
            if case(PATHINFO_BASENAME):
                pass
            # end if
            if case("basename"):
                return ret_["basename"]
            # end if
            if case(PATHINFO_EXTENSION):
                pass
            # end if
            if case("extension"):
                return ret_["extension"]
            # end if
            if case(PATHINFO_FILENAME):
                pass
            # end if
            if case("filename"):
                return ret_["filename"]
            # end if
            if case():
                return ret_
            # end if
        # end for
    # end def mb_pathinfo
    #// 
    #// Set or reset instance properties.
    #// You should avoid this function - it's more verbose, less efficient, more error-prone and
    #// harder to debug than setting properties directly.
    #// Usage Example:
    #// `$mail->set('SMTPSecure', 'tls');`
    #// is the same as:
    #// `$mail->SMTPSecure = 'tls';`
    #// @access public
    #// @param string $name The property name to set
    #// @param mixed $value The value to set the property to
    #// @return boolean
    #// @TODO Should this not be using the __set() magic function?
    #//
    def set(self, name_=None, value_=""):
        
        
        if property_exists(self, name_):
            self.name_ = value_
            return True
        else:
            self.seterror(self.lang("variable_set") + name_)
            return False
        # end if
    # end def set
    #// 
    #// Strip newlines to prevent header injection.
    #// @access public
    #// @param string $str
    #// @return string
    #//
    def secureheader(self, str_=None):
        
        
        return php_trim(php_str_replace(Array("\r", "\n"), "", str_))
    # end def secureheader
    #// 
    #// Normalize line breaks in a string.
    #// Converts UNIX LF, Mac CR and Windows CRLF line breaks into a single line break format.
    #// Defaults to CRLF (for message bodies) and preserves consecutive breaks.
    #// @param string $text
    #// @param string $breaktype What kind of line break to use, defaults to CRLF
    #// @return string
    #// @access public
    #// @static
    #//
    @classmethod
    def normalizebreaks(self, text_=None, breaktype_="\r\n"):
        
        
        return php_preg_replace("/(\\r\\n|\\r|\\n)/ms", breaktype_, text_)
    # end def normalizebreaks
    #// 
    #// Set the public and private key files and password for S/MIME signing.
    #// @access public
    #// @param string $cert_filename
    #// @param string $key_filename
    #// @param string $key_pass Password for private key
    #// @param string $extracerts_filename Optional path to chain certificate
    #//
    def sign(self, cert_filename_=None, key_filename_=None, key_pass_=None, extracerts_filename_=""):
        
        
        self.sign_cert_file = cert_filename_
        self.sign_key_file = key_filename_
        self.sign_key_pass = key_pass_
        self.sign_extracerts_file = extracerts_filename_
    # end def sign
    #// 
    #// Quoted-Printable-encode a DKIM header.
    #// @access public
    #// @param string $txt
    #// @return string
    #//
    def dkim_qp(self, txt_=None):
        
        
        line_ = ""
        i_ = 0
        while i_ < php_strlen(txt_):
            
            ord_ = php_ord(txt_[i_])
            if 33 <= ord_ and ord_ <= 58 or ord_ == 60 or 62 <= ord_ and ord_ <= 126:
                line_ += txt_[i_]
            else:
                line_ += "=" + php_sprintf("%02X", ord_)
            # end if
            i_ += 1
        # end while
        return line_
    # end def dkim_qp
    #// 
    #// Generate a DKIM signature.
    #// @access public
    #// @param string $signHeader
    #// @throws phpmailerException
    #// @return string The DKIM signature value
    #//
    def dkim_sign(self, signHeader_=None):
        
        
        if (not php_defined("PKCS7_TEXT")):
            if self.exceptions:
                raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("extension_missing") + "openssl"))
            # end if
            return ""
        # end if
        privKeyStr_ = self.DKIM_private_string if (not php_empty(lambda : self.DKIM_private_string)) else php_file_get_contents(self.DKIM_private)
        if "" != self.DKIM_passphrase:
            privKey_ = openssl_pkey_get_private(privKeyStr_, self.DKIM_passphrase)
        else:
            privKey_ = openssl_pkey_get_private(privKeyStr_)
        # end if
        #// Workaround for missing digest algorithms in old PHP & OpenSSL versions
        #// @link http://stackoverflow.com/a/11117338/333340
        if php_version_compare(PHP_VERSION, "5.3.0") >= 0 and php_in_array("sha256WithRSAEncryption", openssl_get_md_methods(True)):
            if openssl_sign(signHeader_, signature_, privKey_, "sha256WithRSAEncryption"):
                openssl_pkey_free(privKey_)
                return php_base64_encode(signature_)
            # end if
        else:
            pinfo_ = openssl_pkey_get_details(privKey_)
            hash_ = hash("sha256", signHeader_)
            #// 'Magic' constant for SHA256 from RFC3447
            #// @link https://tools.ietf.org/html/rfc3447#page-43
            t_ = "3031300d060960864801650304020105000420" + hash_
            pslen_ = pinfo_["bits"] / 8 - php_strlen(t_) / 2 + 3
            eb_ = pack("H*", "0001" + php_str_repeat("FF", pslen_) + "00" + t_)
            if openssl_private_encrypt(eb_, signature_, privKey_, OPENSSL_NO_PADDING):
                openssl_pkey_free(privKey_)
                return php_base64_encode(signature_)
            # end if
        # end if
        openssl_pkey_free(privKey_)
        return ""
    # end def dkim_sign
    #// 
    #// Generate a DKIM canonicalization header.
    #// @access public
    #// @param string $signHeader Header
    #// @return string
    #//
    def dkim_headerc(self, signHeader_=None):
        
        
        signHeader_ = php_preg_replace("/\\r\\n\\s+/", " ", signHeader_)
        lines_ = php_explode("\r\n", signHeader_)
        for key_,line_ in lines_.items():
            heading_, value_ = php_explode(":", line_, 2)
            heading_ = php_strtolower(heading_)
            value_ = php_preg_replace("/\\s{2,}/", " ", value_)
            #// Compress useless spaces
            lines_[key_] = heading_ + ":" + php_trim(value_)
            pass
        # end for
        signHeader_ = php_implode("\r\n", lines_)
        return signHeader_
    # end def dkim_headerc
    #// 
    #// Generate a DKIM canonicalization body.
    #// @access public
    #// @param string $body Message Body
    #// @return string
    #//
    def dkim_bodyc(self, body_=None):
        
        
        if body_ == "":
            return "\r\n"
        # end if
        #// stabilize line endings
        body_ = php_str_replace("\r\n", "\n", body_)
        body_ = php_str_replace("\n", "\r\n", body_)
        #// END stabilize line endings
        while True:
            
            if not (php_substr(body_, php_strlen(body_) - 4, 4) == "\r\n\r\n"):
                break
            # end if
            body_ = php_substr(body_, 0, php_strlen(body_) - 2)
        # end while
        return body_
    # end def dkim_bodyc
    #// 
    #// Create the DKIM header and body in a new message header.
    #// @access public
    #// @param string $headers_line Header lines
    #// @param string $subject Subject
    #// @param string $body Body
    #// @return string
    #//
    def dkim_add(self, headers_line_=None, subject_=None, body_=None):
        
        
        DKIMsignatureType_ = "rsa-sha256"
        #// Signature & hash algorithms
        DKIMcanonicalization_ = "relaxed/simple"
        #// Canonicalization of header/body
        DKIMquery_ = "dns/txt"
        #// Query method
        DKIMtime_ = time()
        #// Signature Timestamp = seconds since 00:00:00 - Jan 1, 1970 (UTC time zone)
        subject_header_ = str("Subject: ") + str(subject_)
        headers_ = php_explode(self.LE, headers_line_)
        from_header_ = ""
        to_header_ = ""
        date_header_ = ""
        current_ = ""
        for header_ in headers_:
            if php_strpos(header_, "From:") == 0:
                from_header_ = header_
                current_ = "from_header"
            elif php_strpos(header_, "To:") == 0:
                to_header_ = header_
                current_ = "to_header"
            elif php_strpos(header_, "Date:") == 0:
                date_header_ = header_
                current_ = "date_header"
            else:
                if (not php_empty(lambda : current__)) and php_strpos(header_, " =?") == 0:
                    current__ += header_
                else:
                    current_ = ""
                # end if
            # end if
        # end for
        from_ = php_str_replace("|", "=7C", self.dkim_qp(from_header_))
        to_ = php_str_replace("|", "=7C", self.dkim_qp(to_header_))
        date_ = php_str_replace("|", "=7C", self.dkim_qp(date_header_))
        subject_ = php_str_replace("|", "=7C", self.dkim_qp(subject_header_))
        #// Copied header fields (dkim-quoted-printable)
        body_ = self.dkim_bodyc(body_)
        DKIMlen_ = php_strlen(body_)
        #// Length of body
        DKIMb64_ = php_base64_encode(pack("H*", hash("sha256", body_)))
        #// Base64 of packed binary SHA-256 hash of body
        if "" == self.DKIM_identity:
            ident_ = ""
        else:
            ident_ = " i=" + self.DKIM_identity + ";"
        # end if
        dkimhdrs_ = "DKIM-Signature: v=1; a=" + DKIMsignatureType_ + "; q=" + DKIMquery_ + "; l=" + DKIMlen_ + "; s=" + self.DKIM_selector + ";\r\n" + "    t=" + DKIMtime_ + "; c=" + DKIMcanonicalization_ + ";\r\n" + "  h=From:To:Date:Subject;\r\n" + "    d=" + self.DKIM_domain + ";" + ident_ + "\r\n" + str("  z=") + str(from_) + str("\r\n") + str(" |") + str(to_) + str("\r\n") + str("    |") + str(date_) + str("\r\n") + str("  |") + str(subject_) + str(";\r\n") + "  bh=" + DKIMb64_ + ";\r\n" + "   b="
        toSign_ = self.dkim_headerc(from_header_ + "\r\n" + to_header_ + "\r\n" + date_header_ + "\r\n" + subject_header_ + "\r\n" + dkimhdrs_)
        signed_ = self.dkim_sign(toSign_)
        return dkimhdrs_ + signed_ + "\r\n"
    # end def dkim_add
    #// 
    #// Detect if a string contains a line longer than the maximum line length allowed.
    #// @param string $str
    #// @return boolean
    #// @static
    #//
    @classmethod
    def haslinelongerthanmax(self, str_=None):
        
        
        #// +2 to include CRLF line break for a 1000 total
        return php_bool(php_preg_match("/^(.{" + self.MAX_LINE_LENGTH + 2 + ",})/m", str_))
    # end def haslinelongerthanmax
    #// 
    #// Allows for public read access to 'to' property.
    #// @note: Before the send() call, queued addresses (i.e. with IDN) are not yet included.
    #// @access public
    #// @return array
    #//
    def gettoaddresses(self):
        
        
        return self.to
    # end def gettoaddresses
    #// 
    #// Allows for public read access to 'cc' property.
    #// @note: Before the send() call, queued addresses (i.e. with IDN) are not yet included.
    #// @access public
    #// @return array
    #//
    def getccaddresses(self):
        
        
        return self.cc
    # end def getccaddresses
    #// 
    #// Allows for public read access to 'bcc' property.
    #// @note: Before the send() call, queued addresses (i.e. with IDN) are not yet included.
    #// @access public
    #// @return array
    #//
    def getbccaddresses(self):
        
        
        return self.bcc
    # end def getbccaddresses
    #// 
    #// Allows for public read access to 'ReplyTo' property.
    #// @note: Before the send() call, queued addresses (i.e. with IDN) are not yet included.
    #// @access public
    #// @return array
    #//
    def getreplytoaddresses(self):
        
        
        return self.ReplyTo
    # end def getreplytoaddresses
    #// 
    #// Allows for public read access to 'all_recipients' property.
    #// @note: Before the send() call, queued addresses (i.e. with IDN) are not yet included.
    #// @access public
    #// @return array
    #//
    def getallrecipientaddresses(self):
        
        
        return self.all_recipients
    # end def getallrecipientaddresses
    #// 
    #// Perform a callback.
    #// @param boolean $isSent
    #// @param array $to
    #// @param array $cc
    #// @param array $bcc
    #// @param string $subject
    #// @param string $body
    #// @param string $from
    #//
    def docallback(self, isSent_=None, to_=None, cc_=None, bcc_=None, subject_=None, body_=None, from_=None):
        
        
        if (not php_empty(lambda : self.action_function)) and php_is_callable(self.action_function):
            params_ = Array(isSent_, to_, cc_, bcc_, subject_, body_, from_)
            call_user_func_array(self.action_function, params_)
        # end if
    # end def docallback
# end class PHPMailer
#// 
#// PHPMailer exception handler
#// @package PHPMailer
#//
class phpmailerException(Exception):
    #// 
    #// Prettify error message output
    #// @return string
    #//
    def errormessage(self):
        
        
        errorMsg_ = "<strong>" + php_htmlspecialchars(self.getmessage()) + "</strong><br />\n"
        return errorMsg_
    # end def errormessage
# end class phpmailerException
