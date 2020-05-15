#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import cgi
    import os
    import os.path
    import copy
    import sys
    from goto import with_goto
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
    Version = "5.2.27"
    Priority = None
    CharSet = "iso-8859-1"
    ContentType = "text/plain"
    Encoding = "8bit"
    ErrorInfo = ""
    From = "root@localhost"
    FromName = "Root User"
    Sender = ""
    ReturnPath = ""
    Subject = ""
    Body = ""
    AltBody = ""
    Ical = ""
    MIMEBody = ""
    MIMEHeader = ""
    mailHeader = ""
    WordWrap = 0
    Mailer = "mail"
    Sendmail = "/usr/sbin/sendmail"
    UseSendmailOptions = True
    PluginDir = ""
    ConfirmReadingTo = ""
    Hostname = ""
    MessageID = ""
    MessageDate = ""
    Host = "localhost"
    Port = 25
    Helo = ""
    SMTPSecure = ""
    SMTPAutoTLS = True
    SMTPAuth = False
    SMTPOptions = Array()
    Username = ""
    Password = ""
    AuthType = ""
    Realm = ""
    Workstation = ""
    Timeout = 300
    SMTPDebug = 0
    Debugoutput = "echo"
    SMTPKeepAlive = False
    SingleTo = False
    SingleToArray = Array()
    do_verp = False
    AllowEmpty = False
    LE = "\n"
    DKIM_selector = ""
    DKIM_identity = ""
    DKIM_passphrase = ""
    DKIM_domain = ""
    DKIM_private = ""
    DKIM_private_string = ""
    action_function = ""
    XMailer = ""
    validator = "auto"
    smtp = None
    to = Array()
    cc = Array()
    bcc = Array()
    ReplyTo = Array()
    all_recipients = Array()
    RecipientsQueue = Array()
    ReplyToQueue = Array()
    attachment = Array()
    CustomHeader = Array()
    lastMessageID = ""
    message_type = ""
    boundary = Array()
    language = Array()
    error_count = 0
    sign_cert_file = ""
    sign_key_file = ""
    sign_extracerts_file = ""
    sign_key_pass = ""
    exceptions = False
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
    def __init__(self, exceptions=None):
        
        if exceptions != None:
            self.exceptions = bool(exceptions)
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
    def mailpassthru(self, to=None, subject=None, body=None, header=None, params=None):
        
        #// Check overloading of mail function to avoid double-encoding
        if php_ini_get("mbstring.func_overload") & 1:
            subject = self.secureheader(subject)
        else:
            subject = self.encodeheader(self.secureheader(subject))
        # end if
        #// Can't use additional_parameters in safe_mode, calling mail() with null params breaks
        #// @link http://php.net/manual/en/function.mail.php
        if php_ini_get("safe_mode") or (not self.UseSendmailOptions) or php_is_null(params):
            result = php_no_error(lambda: mail(to, subject, body, header))
        else:
            result = php_no_error(lambda: mail(to, subject, body, header, params))
        # end if
        return result
    # end def mailpassthru
    #// 
    #// Output debugging info via user-defined method.
    #// Only generates output if SMTP debug output is enabled (@see SMTP::$do_debug).
    #// @see PHPMailer::$Debugoutput
    #// @see PHPMailer::$SMTPDebug
    #// @param string $str
    #//
    def edebug(self, str=None):
        
        if self.SMTPDebug <= 0:
            return
        # end if
        #// Avoid clash with built-in function names
        if (not php_in_array(self.Debugoutput, Array("error_log", "html", "echo"))) and php_is_callable(self.Debugoutput):
            php_call_user_func(self.Debugoutput, str, self.SMTPDebug)
            return
        # end if
        for case in Switch(self.Debugoutput):
            if case("error_log"):
                #// Don't output, just log
                php_error_log(str)
                break
            # end if
            if case("html"):
                #// Cleans up output a bit for a better looking, HTML-safe output
                php_print(htmlentities(php_preg_replace("/[\\r\\n]+/", "", str), ENT_QUOTES, "UTF-8") + "<br>\n")
                break
            # end if
            if case("echo"):
                pass
            # end if
            if case():
                #// Normalize line breaks
                str = php_preg_replace("/\\r\\n?/ms", "\n", str)
                php_print(gmdate("Y-m-d H:i:s") + " " + php_str_replace("\n", "\n                                         ", php_trim(str)) + "\n")
            # end if
        # end for
    # end def edebug
    #// 
    #// Sets message type to HTML or plain.
    #// @param boolean $isHtml True for HTML mode.
    #// @return void
    #//
    def ishtml(self, isHtml=True):
        
        if isHtml:
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
        
        ini_sendmail_path = php_ini_get("sendmail_path")
        if (not php_stristr(ini_sendmail_path, "sendmail")):
            self.Sendmail = "/usr/sbin/sendmail"
        else:
            self.Sendmail = ini_sendmail_path
        # end if
        self.Mailer = "sendmail"
    # end def issendmail
    #// 
    #// Send messages using qmail.
    #// @return void
    #//
    def isqmail(self):
        
        ini_sendmail_path = php_ini_get("sendmail_path")
        if (not php_stristr(ini_sendmail_path, "qmail")):
            self.Sendmail = "/var/qmail/bin/qmail-inject"
        else:
            self.Sendmail = ini_sendmail_path
        # end if
        self.Mailer = "qmail"
    # end def isqmail
    #// 
    #// Add a "To" address.
    #// @param string $address The email address to send to
    #// @param string $name
    #// @return boolean true on success, false if address already used or invalid in some way
    #//
    def addaddress(self, address=None, name=""):
        
        return self.addorenqueueanaddress("to", address, name)
    # end def addaddress
    #// 
    #// Add a "CC" address.
    #// @note: This function works with the SMTP mailer on win32, not with the "mail" mailer.
    #// @param string $address The email address to send to
    #// @param string $name
    #// @return boolean true on success, false if address already used or invalid in some way
    #//
    def addcc(self, address=None, name=""):
        
        return self.addorenqueueanaddress("cc", address, name)
    # end def addcc
    #// 
    #// Add a "BCC" address.
    #// @note: This function works with the SMTP mailer on win32, not with the "mail" mailer.
    #// @param string $address The email address to send to
    #// @param string $name
    #// @return boolean true on success, false if address already used or invalid in some way
    #//
    def addbcc(self, address=None, name=""):
        
        return self.addorenqueueanaddress("bcc", address, name)
    # end def addbcc
    #// 
    #// Add a "Reply-To" address.
    #// @param string $address The email address to reply to
    #// @param string $name
    #// @return boolean true on success, false if address already used or invalid in some way
    #//
    def addreplyto(self, address=None, name=""):
        
        return self.addorenqueueanaddress("Reply-To", address, name)
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
    def addorenqueueanaddress(self, kind=None, address=None, name=None):
        
        address = php_trim(address)
        name = php_trim(php_preg_replace("/[\\r\\n]+/", "", name))
        #// Strip breaks and trim
        pos = php_strrpos(address, "@")
        if pos == False:
            #// At-sign is misssing.
            error_message = self.lang("invalid_address") + str(" (addAnAddress ") + str(kind) + str("): ") + str(address)
            self.seterror(error_message)
            self.edebug(error_message)
            if self.exceptions:
                raise php_new_class("phpmailerException", lambda : phpmailerException(error_message))
            # end if
            return False
        # end if
        params = Array(kind, address, name)
        pos += 1
        #// Enqueue addresses with IDN until we know the PHPMailer::$CharSet.
        if self.has8bitchars(php_substr(address, pos)) and self.idnsupported():
            if kind != "Reply-To":
                if (not php_array_key_exists(address, self.RecipientsQueue)):
                    self.RecipientsQueue[address] = params
                    return True
                # end if
            else:
                if (not php_array_key_exists(address, self.ReplyToQueue)):
                    self.ReplyToQueue[address] = params
                    return True
                # end if
            # end if
            return False
        # end if
        #// Immediately add standard addresses without IDN.
        return call_user_func_array(Array(self, "addAnAddress"), params)
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
    def addanaddress(self, kind=None, address=None, name=""):
        
        if (not php_in_array(kind, Array("to", "cc", "bcc", "Reply-To"))):
            error_message = self.lang("Invalid recipient kind: ") + kind
            self.seterror(error_message)
            self.edebug(error_message)
            if self.exceptions:
                raise php_new_class("phpmailerException", lambda : phpmailerException(error_message))
            # end if
            return False
        # end if
        if (not self.validateaddress(address)):
            error_message = self.lang("invalid_address") + str(" (addAnAddress ") + str(kind) + str("): ") + str(address)
            self.seterror(error_message)
            self.edebug(error_message)
            if self.exceptions:
                raise php_new_class("phpmailerException", lambda : phpmailerException(error_message))
            # end if
            return False
        # end if
        if kind != "Reply-To":
            if (not php_array_key_exists(php_strtolower(address), self.all_recipients)):
                php_array_push(self.kind, Array(address, name))
                self.all_recipients[php_strtolower(address)] = True
                return True
            # end if
        else:
            if (not php_array_key_exists(php_strtolower(address), self.ReplyTo)):
                self.ReplyTo[php_strtolower(address)] = Array(address, name)
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
    def parseaddresses(self, addrstr=None, useimap=True):
        
        addresses = Array()
        if useimap and php_function_exists("imap_rfc822_parse_adrlist"):
            #// Use this built-in parser if it's available
            list = imap_rfc822_parse_adrlist(addrstr, "")
            for address in list:
                if address.host != ".SYNTAX-ERROR.":
                    if self.validateaddress(address.mailbox + "@" + address.host):
                        addresses[-1] = Array({"name": address.personal if property_exists(address, "personal") else "", "address": address.mailbox + "@" + address.host})
                    # end if
                # end if
            # end for
        else:
            #// Use this simpler parser
            list = php_explode(",", addrstr)
            for address in list:
                address = php_trim(address)
                #// Is there a separate name part?
                if php_strpos(address, "<") == False:
                    #// No separate name, just use the whole thing
                    if self.validateaddress(address):
                        addresses[-1] = Array({"name": "", "address": address})
                    # end if
                else:
                    name, email = php_explode("<", address)
                    email = php_trim(php_str_replace(">", "", email))
                    if self.validateaddress(email):
                        addresses[-1] = Array({"name": php_trim(php_str_replace(Array("\"", "'"), "", name)), "address": email})
                    # end if
                # end if
            # end for
        # end if
        return addresses
    # end def parseaddresses
    #// 
    #// Set the From and FromName properties.
    #// @param string $address
    #// @param string $name
    #// @param boolean $auto Whether to also set the Sender address, defaults to true
    #// @throws phpmailerException
    #// @return boolean
    #//
    def setfrom(self, address=None, name="", auto=True):
        
        address = php_trim(address)
        name = php_trim(php_preg_replace("/[\\r\\n]+/", "", name))
        pos += 1
        #// Strip breaks and trim
        #// Don't validate now addresses with IDN. Will be done in send().
        pos = php_strrpos(address, "@")
        if pos == False or (not self.has8bitchars(php_substr(address, pos))) or (not self.idnsupported()) and (not self.validateaddress(address)):
            error_message = self.lang("invalid_address") + str(" (setFrom) ") + str(address)
            self.seterror(error_message)
            self.edebug(error_message)
            if self.exceptions:
                raise php_new_class("phpmailerException", lambda : phpmailerException(error_message))
            # end if
            return False
        # end if
        self.From = address
        self.FromName = name
        if auto:
            if php_empty(lambda : self.Sender):
                self.Sender = address
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
    def validateaddress(self, address=None, patternselect=None):
        
        if php_is_null(patternselect):
            patternselect = self.validator
        # end if
        if php_is_callable(patternselect):
            return php_call_user_func(patternselect, address)
        # end if
        #// Reject line breaks in addresses; it's valid RFC5322, but not RFC5321
        if php_strpos(address, "\n") != False or php_strpos(address, "\r") != False:
            return False
        # end if
        if (not patternselect) or patternselect == "auto":
            #// Check this constant first so it works when extension_loaded() is disabled by safe mode
            #// Constant was added in PHP 5.2.4
            if php_defined("PCRE_VERSION"):
                #// This pattern can get stuck in a recursive loop in PCRE <= 8.0.2
                if php_version_compare(PCRE_VERSION, "8.0.3") >= 0:
                    patternselect = "pcre8"
                else:
                    patternselect = "pcre"
                # end if
            elif php_function_exists("extension_loaded") and php_extension_loaded("pcre"):
                #// Fall back to older PCRE
                patternselect = "pcre"
            else:
                #// Filter_var appeared in PHP 5.2.0 and does not require the PCRE extension
                if php_version_compare(PHP_VERSION, "5.2.0") >= 0:
                    patternselect = "php"
                else:
                    patternselect = "noregex"
                # end if
            # end if
        # end if
        for case in Switch(patternselect):
            if case("pcre8"):
                #// 
                #// Uses the same RFC5322 regex on which FILTER_VALIDATE_EMAIL is based, but allows dotless domains.
                #// @link http://squiloople.com/2009/12/20/email-address-validation
                #// @copyright 2009-2010 Michael Rushton
                #// Feel free to use and redistribute this code. But please keep this copyright notice.
                #//
                return bool(php_preg_match("/^(?!(?>(?1)\"?(?>\\\\[ -~]|[^\"])\"?(?1)){255,})(?!(?>(?1)\"?(?>\\\\[ -~]|[^\"])\"?(?1)){65,}@)" + "((?>(?>(?>((?>(?>(?>\\x0D\\x0A)?[\\t ])+|(?>[\\t ]*\\x0D\\x0A)?[\\t ]+)?)(\\((?>(?2)" + "(?>[\\x01-\\x08\\x0B\\x0C\\x0E-'*-\\[\\]-\\x7F]|\\\\[\\x00-\\x7F]|(?3)))*(?2)\\)))+(?2))|(?2))?)" + "([!#-'*+\\/-9=?^-~-]+|\"(?>(?2)(?>[\\x01-\\x08\\x0B\\x0C\\x0E-!#-\\[\\]-\\x7F]|\\\\[\\x00-\\x7F]))*" + "(?2)\")(?>(?1)\\.(?1)(?4))*(?1)@(?!(?1)[a-z0-9-]{64,})(?1)(?>([a-z0-9](?>[a-z0-9-]*[a-z0-9])?)" + "(?>(?1)\\.(?!(?1)[a-z0-9-]{64,})(?1)(?5)){0,126}|\\[(?:(?>IPv6:(?>([a-f0-9]{1,4})(?>:(?6)){7}" + "|(?!(?:.*[a-f0-9][:\\]]){8,})((?6)(?>:(?6)){0,6})?::(?7)?))|(?>(?>IPv6:(?>(?6)(?>:(?6)){5}:" + "|(?!(?:.*[a-f0-9]:){6,})(?8)?::(?>((?6)(?>:(?6)){0,4}):)?))?(25[0-5]|2[0-4][0-9]|1[0-9]{2}" + "|[1-9]?[0-9])(?>\\.(?9)){3}))\\])(?1)$/isD", address))
            # end if
            if case("pcre"):
                #// An older regex that doesn't need a recent PCRE
                return bool(php_preg_match("/^(?!(?>\"?(?>\\\\[ -~]|[^\"])\"?){255,})(?!(?>\"?(?>\\\\[ -~]|[^\"])\"?){65,}@)(?>" + "[!#-'*+\\/-9=?^-~-]+|\"(?>(?>[\\x01-\\x08\\x0B\\x0C\\x0E-!#-\\[\\]-\\x7F]|\\\\[\\x00-\\xFF]))*\")" + "(?>\\.(?>[!#-'*+\\/-9=?^-~-]+|\"(?>(?>[\\x01-\\x08\\x0B\\x0C\\x0E-!#-\\[\\]-\\x7F]|\\\\[\\x00-\\xFF]))*\"))*" + "@(?>(?![a-z0-9-]{64,})(?>[a-z0-9](?>[a-z0-9-]*[a-z0-9])?)(?>\\.(?![a-z0-9-]{64,})" + "(?>[a-z0-9](?>[a-z0-9-]*[a-z0-9])?)){0,126}|\\[(?:(?>IPv6:(?>(?>[a-f0-9]{1,4})(?>:" + "[a-f0-9]{1,4}){7}|(?!(?:.*[a-f0-9][:\\]]){8,})(?>[a-f0-9]{1,4}(?>:[a-f0-9]{1,4}){0,6})?" + "::(?>[a-f0-9]{1,4}(?>:[a-f0-9]{1,4}){0,6})?))|(?>(?>IPv6:(?>[a-f0-9]{1,4}(?>:" + "[a-f0-9]{1,4}){5}:|(?!(?:.*[a-f0-9]:){6,})(?>[a-f0-9]{1,4}(?>:[a-f0-9]{1,4}){0,4})?" + "::(?>(?:[a-f0-9]{1,4}(?>:[a-f0-9]{1,4}){0,4}):)?))?(?>25[0-5]|2[0-4][0-9]|1[0-9]{2}" + "|[1-9]?[0-9])(?>\\.(?>25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])){3}))\\])$/isD", address))
            # end if
            if case("html5"):
                #// 
                #// This is the pattern used in the HTML5 spec for validation of 'email' type form input elements.
                #// @link http://www.whatwg.org/specs/web-apps/current-work/#e-mail-state-(type=email)
                #//
                return bool(php_preg_match("/^[a-zA-Z0-9.!#$%&'*+\\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}" + "[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/sD", address))
            # end if
            if case("noregex"):
                #// No PCRE! Do something _very_ approximate!
                #// Check the address is 3 chars or longer and contains an @ that's not the first or last char
                return php_strlen(address) >= 3 and php_strpos(address, "@") >= 1 and php_strpos(address, "@") != php_strlen(address) - 1
            # end if
            if case("php"):
                pass
            # end if
            if case():
                return bool(filter_var(address, FILTER_VALIDATE_EMAIL))
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
    def punyencodeaddress(self, address=None):
        
        #// Verify we have required functions, CharSet, and at-sign.
        pos = php_strrpos(address, "@")
        if self.idnsupported() and (not php_empty(lambda : self.CharSet)) and pos != False:
            pos += 1
            domain = php_substr(address, pos)
            #// Verify CharSet string is a valid one, and domain properly encoded in this CharSet.
            if self.has8bitchars(domain) and php_no_error(lambda: mb_check_encoding(domain, self.CharSet)):
                domain = mb_convert_encoding(domain, "UTF-8", self.CharSet)
                punycode = idn_to_ascii(domain, 0, INTL_IDNA_VARIANT_UTS46) if php_defined("INTL_IDNA_VARIANT_UTS46") else idn_to_ascii(domain)
                if punycode != False:
                    return php_substr(address, 0, pos) + punycode
                # end if
            # end if
        # end if
        return address
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
        except phpmailerException as exc:
            self.mailHeader = ""
            self.seterror(exc.getmessage())
            if self.exceptions:
                raise exc
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
            for params in php_array_merge(self.RecipientsQueue, self.ReplyToQueue):
                params[1] = self.punyencodeaddress(params[1])
                call_user_func_array(Array(self, "addAnAddress"), params)
            # end for
            if php_count(self.to) + php_count(self.cc) + php_count(self.bcc) < 1:
                raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("provide_address"), self.STOP_CRITICAL))
            # end if
            #// Validate From, Sender, and ConfirmReadingTo addresses
            for address_kind in Array("From", "Sender", "ConfirmReadingTo"):
                self.address_kind = php_trim(self.address_kind)
                if php_empty(lambda : self.address_kind):
                    continue
                # end if
                self.address_kind = self.punyencodeaddress(self.address_kind)
                if (not self.validateaddress(self.address_kind)):
                    error_message = self.lang("invalid_address") + " (punyEncode) " + self.address_kind
                    self.seterror(error_message)
                    self.edebug(error_message)
                    if self.exceptions:
                        raise php_new_class("phpmailerException", lambda : phpmailerException(error_message))
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
            tempheaders = self.MIMEHeader
            self.MIMEHeader = self.createheader()
            self.MIMEHeader += tempheaders
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
                header_dkim = self.dkim_add(self.MIMEHeader + self.mailHeader, self.encodeheader(self.secureheader(self.Subject)), self.MIMEBody)
                self.MIMEHeader = php_rtrim(self.MIMEHeader, "\r\n ") + self.CRLF + php_str_replace("\r\n", "\n", header_dkim) + self.CRLF
            # end if
            return True
        except phpmailerException as exc:
            self.seterror(exc.getmessage())
            if self.exceptions:
                raise exc
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
                    sendMethod = self.Mailer + "Send"
                    if php_method_exists(self, sendMethod):
                        return self.sendmethod(self.MIMEHeader, self.MIMEBody)
                    # end if
                    return self.mailsend(self.MIMEHeader, self.MIMEBody)
                # end if
            # end for
        except phpmailerException as exc:
            self.seterror(exc.getmessage())
            self.edebug(exc.getmessage())
            if self.exceptions:
                raise exc
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
    def sendmailsend(self, header=None, body=None):
        
        #// CVE-2016-10033, CVE-2016-10045: Don't pass -f if characters will be escaped.
        if (not php_empty(lambda : self.Sender)) and self.isshellsafe(self.Sender):
            if self.Mailer == "qmail":
                sendmailFmt = "%s -f%s"
            else:
                sendmailFmt = "%s -oi -f%s -t"
            # end if
        else:
            if self.Mailer == "qmail":
                sendmailFmt = "%s"
            else:
                sendmailFmt = "%s -oi -t"
            # end if
        # end if
        #// TODO: If possible, this should be changed to escapeshellarg.  Needs thorough testing.
        sendmail = php_sprintf(sendmailFmt, escapeshellcmd(self.Sendmail), self.Sender)
        if self.SingleTo:
            for toAddr in self.SingleToArray:
                mail = popen(sendmail, "w")
                if (not php_no_error(lambda: mail)):
                    raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("execute") + self.Sendmail, self.STOP_CRITICAL))
                # end if
                fputs(mail, "To: " + toAddr + "\n")
                fputs(mail, header)
                fputs(mail, body)
                result = pclose(mail)
                self.docallback(result == 0, Array(toAddr), self.cc, self.bcc, self.Subject, body, self.From)
                if result != 0:
                    raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("execute") + self.Sendmail, self.STOP_CRITICAL))
                # end if
            # end for
        else:
            mail = popen(sendmail, "w")
            if (not php_no_error(lambda: mail)):
                raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("execute") + self.Sendmail, self.STOP_CRITICAL))
            # end if
            fputs(mail, header)
            fputs(mail, body)
            result = pclose(mail)
            self.docallback(result == 0, self.to, self.cc, self.bcc, self.Subject, body, self.From)
            if result != 0:
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
    def isshellsafe(self, string=None):
        
        #// Future-proof
        if escapeshellcmd(string) != string or (not php_in_array(escapeshellarg(string), Array(str("'") + str(string) + str("'"), str("\"") + str(string) + str("\"")))):
            return False
        # end if
        length = php_strlen(string)
        i = 0
        while i < length:
            
            c = string[i]
            #// All other characters have a special meaning in at least one common shell, including = and +.
            #// Full stop (.) has a special meaning in cmd.exe, but its impact should be negligible here.
            #// Note that this does permit non-Latin alphanumeric characters based on the current locale.
            if (not ctype_alnum(c)) and php_strpos("@_-.", c) == False:
                return False
            # end if
            i += 1
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
    def ispermittedpath(self, path=None):
        
        return (not php_preg_match("#^[a-z]+://#i", path))
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
    def mailsend(self, header=None, body=None):
        
        toArr = Array()
        for toaddr in self.to:
            toArr[-1] = self.addrformat(toaddr)
        # end for
        to = php_implode(", ", toArr)
        params = None
        #// This sets the SMTP envelope sender which gets turned into a return-path header by the receiver
        if (not php_empty(lambda : self.Sender)) and self.validateaddress(self.Sender):
            #// CVE-2016-10033, CVE-2016-10045: Don't pass -f if characters will be escaped.
            if self.isshellsafe(self.Sender):
                params = php_sprintf("-f%s", self.Sender)
            # end if
        # end if
        if (not php_empty(lambda : self.Sender)) and (not php_ini_get("safe_mode")) and self.validateaddress(self.Sender):
            old_from = php_ini_get("sendmail_from")
            php_ini_set("sendmail_from", self.Sender)
        # end if
        result = False
        if self.SingleTo and php_count(toArr) > 1:
            for toAddr in toArr:
                result = self.mailpassthru(toAddr, self.Subject, body, header, params)
                self.docallback(result, Array(toAddr), self.cc, self.bcc, self.Subject, body, self.From)
            # end for
        else:
            result = self.mailpassthru(to, self.Subject, body, header, params)
            self.docallback(result, self.to, self.cc, self.bcc, self.Subject, body, self.From)
        # end if
        if (php_isset(lambda : old_from)):
            php_ini_set("sendmail_from", old_from)
        # end if
        if (not result):
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
    def smtpsend(self, header=None, body=None):
        
        bad_rcpt = Array()
        if (not self.smtpconnect(self.SMTPOptions)):
            raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("smtp_connect_failed"), self.STOP_CRITICAL))
        # end if
        if (not php_empty(lambda : self.Sender)) and self.validateaddress(self.Sender):
            smtp_from = self.Sender
        else:
            smtp_from = self.From
        # end if
        if (not self.smtp.mail(smtp_from)):
            self.seterror(self.lang("from_failed") + smtp_from + " : " + php_implode(",", self.smtp.geterror()))
            raise php_new_class("phpmailerException", lambda : phpmailerException(self.ErrorInfo, self.STOP_CRITICAL))
        # end if
        #// Attempt to send to all recipients
        for togroup in Array(self.to, self.cc, self.bcc):
            for to in togroup:
                if (not self.smtp.recipient(to[0])):
                    error = self.smtp.geterror()
                    bad_rcpt[-1] = Array({"to": to[0], "error": error["detail"]})
                    isSent = False
                else:
                    isSent = True
                # end if
                self.docallback(isSent, Array(to[0]), Array(), Array(), self.Subject, body, self.From)
            # end for
        # end for
        #// Only send the DATA command if we have viable recipients
        if php_count(self.all_recipients) > php_count(bad_rcpt) and (not self.smtp.data(header + body)):
            raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("data_not_accepted"), self.STOP_CRITICAL))
        # end if
        if self.SMTPKeepAlive:
            self.smtp.reset()
        else:
            self.smtp.quit()
            self.smtp.close()
        # end if
        #// Create error message for any bad addresses
        if php_count(bad_rcpt) > 0:
            errstr = ""
            for bad in bad_rcpt:
                errstr += bad["to"] + ": " + bad["error"]
            # end for
            raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("recipients_failed") + errstr, self.STOP_CONTINUE))
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
    def smtpconnect(self, options=None):
        
        if php_is_null(self.smtp):
            self.smtp = self.getsmtpinstance()
        # end if
        #// If no options are provided, use whatever is set in the instance
        if php_is_null(options):
            options = self.SMTPOptions
        # end if
        #// Already connected?
        if self.smtp.connected():
            return True
        # end if
        self.smtp.settimeout(self.Timeout)
        self.smtp.setdebuglevel(self.SMTPDebug)
        self.smtp.setdebugoutput(self.Debugoutput)
        self.smtp.setverp(self.do_verp)
        hosts = php_explode(";", self.Host)
        lastexception = None
        for hostentry in hosts:
            hostinfo = Array()
            if (not php_preg_match("/^((ssl|tls):\\/\\/)*([a-zA-Z0-9\\.-]*|\\[[a-fA-F0-9:]+\\]):?([0-9]*)$/", php_trim(hostentry), hostinfo)):
                #// Not a valid host entry
                self.edebug("Ignoring invalid host: " + hostentry)
                continue
            # end if
            #// $hostinfo[2]: optional ssl or tls prefix
            #// $hostinfo[3]: the hostname
            #// $hostinfo[4]: optional port number
            #// The host string prefix can temporarily override the current setting for SMTPSecure
            #// If it's not specified, the default value is used
            prefix = ""
            secure = self.SMTPSecure
            tls = self.SMTPSecure == "tls"
            if "ssl" == hostinfo[2] or "" == hostinfo[2] and "ssl" == self.SMTPSecure:
                prefix = "ssl://"
                tls = False
                #// Can't have SSL and TLS at the same time
                secure = "ssl"
            elif hostinfo[2] == "tls":
                tls = True
                #// tls doesn't use a prefix
                secure = "tls"
            # end if
            #// Do we need the OpenSSL extension?
            sslext = php_defined("OPENSSL_ALGO_SHA1")
            if "tls" == secure or "ssl" == secure:
                #// Check for an OpenSSL constant rather than using extension_loaded, which is sometimes disabled
                if (not sslext):
                    raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("extension_missing") + "openssl", self.STOP_CRITICAL))
                # end if
            # end if
            host = hostinfo[3]
            port = self.Port
            tport = int(hostinfo[4])
            if tport > 0 and tport < 65536:
                port = tport
            # end if
            if self.smtp.connect(prefix + host, port, self.Timeout, options):
                try: 
                    if self.Helo:
                        hello = self.Helo
                    else:
                        hello = self.serverhostname()
                    # end if
                    self.smtp.hello(hello)
                    #// Automatically enable TLS encryption if:
                    #// it's not disabled
                    #// we have openssl extension
                    #// we are not already using SSL
                    #// the server offers STARTTLS
                    if self.SMTPAutoTLS and sslext and secure != "ssl" and self.smtp.getserverext("STARTTLS"):
                        tls = True
                    # end if
                    if tls:
                        if (not self.smtp.starttls()):
                            raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("connect_host")))
                        # end if
                        #// We must resend EHLO after TLS negotiation
                        self.smtp.hello(hello)
                    # end if
                    if self.SMTPAuth:
                        if (not self.smtp.authenticate(self.Username, self.Password, self.AuthType, self.Realm, self.Workstation)):
                            raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("authenticate")))
                        # end if
                    # end if
                    return True
                except phpmailerException as exc:
                    lastexception = exc
                    self.edebug(exc.getmessage())
                    #// We must have connected, but then failed TLS or Auth, so close connection nicely
                    self.smtp.quit()
                # end try
            # end if
        # end for
        #// If we get here, all connection attempts have failed, so close connection hard
        self.smtp.close()
        #// As we've caught all exceptions, just report whatever the last one was
        if self.exceptions and (not php_is_null(lastexception)):
            raise lastexception
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
    def setlanguage(self, langcode="en", lang_path=""):
        
        #// Backwards compatibility for renamed language codes
        renamed_langcodes = Array({"br": "pt_br", "cz": "cs", "dk": "da", "no": "nb", "se": "sv", "sr": "rs"})
        if (php_isset(lambda : renamed_langcodes[langcode])):
            langcode = renamed_langcodes[langcode]
        # end if
        #// Define full set of translatable strings in English
        PHPMAILER_LANG = Array({"authenticate": "SMTP Error: Could not authenticate.", "connect_host": "SMTP Error: Could not connect to SMTP host.", "data_not_accepted": "SMTP Error: data not accepted.", "empty_message": "Message body empty", "encoding": "Unknown encoding: ", "execute": "Could not execute: ", "file_access": "Could not access file: ", "file_open": "File Error: Could not open file: ", "from_failed": "The following From address failed: ", "instantiate": "Could not instantiate mail function.", "invalid_address": "Invalid address: ", "mailer_not_supported": " mailer is not supported.", "provide_address": "You must provide at least one recipient email address.", "recipients_failed": "SMTP Error: The following recipients failed: ", "signing": "Signing Error: ", "smtp_connect_failed": "SMTP connect() failed.", "smtp_error": "SMTP server error: ", "variable_set": "Cannot set or reset variable: ", "extension_missing": "Extension missing: "})
        if php_empty(lambda : lang_path):
            #// Calculate an absolute path so it can work if CWD is not here
            lang_path = php_dirname(__FILE__) + DIRECTORY_SEPARATOR + "language" + DIRECTORY_SEPARATOR
        # end if
        #// Validate $langcode
        if (not php_preg_match("/^[a-z]{2}(?:_[a-zA-Z]{2})?$/", langcode)):
            langcode = "en"
        # end if
        foundlang = True
        lang_file = lang_path + "phpmailer.lang-" + langcode + ".php"
        #// There is no English translation file
        if langcode != "en":
            #// Make sure language file path is readable
            if (not self.ispermittedpath(lang_file)) or (not php_is_readable(lang_file)):
                foundlang = False
            else:
                #// Overwrite language-specific strings.
                #// This way we'll never have missing translation keys.
                foundlang = php_include_file(lang_file, once=False)
            # end if
        # end if
        self.language = PHPMAILER_LANG
        return bool(foundlang)
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
    def addrappend(self, type=None, addr=None):
        
        addresses = Array()
        for address in addr:
            addresses[-1] = self.addrformat(address)
        # end for
        return type + ": " + php_implode(", ", addresses) + self.LE
    # end def addrappend
    #// 
    #// Format an address for use in a message header.
    #// @access public
    #// @param array $addr A 2-element indexed array, element 0 containing an address, element 1 containing a name
    #// like array('joe@example.com', 'Joe User')
    #// @return string
    #//
    def addrformat(self, addr=None):
        
        if php_empty(lambda : addr[1]):
            #// No name provided
            return self.secureheader(addr[0])
        else:
            return self.encodeheader(self.secureheader(addr[1]), "phrase") + " <" + self.secureheader(addr[0]) + ">"
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
    def wraptext(self, message=None, length=None, qp_mode=False):
        
        if qp_mode:
            soft_break = php_sprintf(" =%s", self.LE)
        else:
            soft_break = self.LE
        # end if
        #// If utf-8 encoding is used, we will need to make sure we don't
        #// split multibyte characters when we wrap
        is_utf8 = php_strtolower(self.CharSet) == "utf-8"
        lelen = php_strlen(self.LE)
        crlflen = php_strlen(self.CRLF)
        message = self.fixeol(message)
        #// Remove a trailing line break
        if php_substr(message, -lelen) == self.LE:
            message = php_substr(message, 0, -lelen)
        # end if
        #// Split message into lines
        lines = php_explode(self.LE, message)
        #// Message will be rebuilt in here
        message = ""
        for line in lines:
            words = php_explode(" ", line)
            buf = ""
            firstword = True
            for word in words:
                if qp_mode and php_strlen(word) > length:
                    space_left = length - php_strlen(buf) - crlflen
                    if (not firstword):
                        if space_left > 20:
                            len = space_left
                            if is_utf8:
                                len = self.utf8charboundary(word, len)
                            elif php_substr(word, len - 1, 1) == "=":
                                len -= 1
                            elif php_substr(word, len - 2, 1) == "=":
                                len -= 2
                            # end if
                            part = php_substr(word, 0, len)
                            word = php_substr(word, len)
                            buf += " " + part
                            message += buf + php_sprintf("=%s", self.CRLF)
                        else:
                            message += buf + soft_break
                        # end if
                        buf = ""
                    # end if
                    while True:
                        
                        if not (php_strlen(word) > 0):
                            break
                        # end if
                        if length <= 0:
                            break
                        # end if
                        len = length
                        if is_utf8:
                            len = self.utf8charboundary(word, len)
                        elif php_substr(word, len - 1, 1) == "=":
                            len -= 1
                        elif php_substr(word, len - 2, 1) == "=":
                            len -= 2
                        # end if
                        part = php_substr(word, 0, len)
                        word = php_substr(word, len)
                        if php_strlen(word) > 0:
                            message += part + php_sprintf("=%s", self.CRLF)
                        else:
                            buf = part
                        # end if
                    # end while
                else:
                    buf_o = buf
                    if (not firstword):
                        buf += " "
                    # end if
                    buf += word
                    if php_strlen(buf) > length and buf_o != "":
                        message += buf_o + soft_break
                        buf = word
                    # end if
                # end if
                firstword = False
            # end for
            message += buf + self.CRLF
        # end for
        return message
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
    def utf8charboundary(self, encodedText=None, maxLength=None):
        
        foundSplitPos = False
        lookBack = 3
        while True:
            
            if not ((not foundSplitPos)):
                break
            # end if
            lastChunk = php_substr(encodedText, maxLength - lookBack, lookBack)
            encodedCharPos = php_strpos(lastChunk, "=")
            if False != encodedCharPos:
                #// Found start of encoded character byte within $lookBack block.
                #// Check the encoded byte value (the 2 chars after the '=')
                hex = php_substr(encodedText, maxLength - lookBack + encodedCharPos + 1, 2)
                dec = hexdec(hex)
                if dec < 128:
                    #// Single byte character.
                    #// If the encoded char was found at pos 0, it will fit
                    #// otherwise reduce maxLength to start of the encoded char
                    if encodedCharPos > 0:
                        maxLength = maxLength - lookBack - encodedCharPos
                    # end if
                    foundSplitPos = True
                elif dec >= 192:
                    #// First byte of a multi byte character
                    #// Reduce maxLength to split at start of character
                    maxLength = maxLength - lookBack - encodedCharPos
                    foundSplitPos = True
                elif dec < 192:
                    #// Middle byte of a multi byte character, look further back
                    lookBack += 3
                # end if
            else:
                #// No encoded character found
                foundSplitPos = True
            # end if
        # end while
        return maxLength
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
        
        result = ""
        result += self.headerline("Date", self.rfcdate() if self.MessageDate == "" else self.MessageDate)
        #// To be created automatically by mail()
        if self.SingleTo:
            if self.Mailer != "mail":
                for toaddr in self.to:
                    self.SingleToArray[-1] = self.addrformat(toaddr)
                # end for
            # end if
        else:
            if php_count(self.to) > 0:
                if self.Mailer != "mail":
                    result += self.addrappend("To", self.to)
                # end if
            elif php_count(self.cc) == 0:
                result += self.headerline("To", "undisclosed-recipients:;")
            # end if
        # end if
        result += self.addrappend("From", Array(Array(php_trim(self.From), self.FromName)))
        #// sendmail and mail() extract Cc from the header before sending
        if php_count(self.cc) > 0:
            result += self.addrappend("Cc", self.cc)
        # end if
        #// sendmail and mail() extract Bcc from the header before sending
        if self.Mailer == "sendmail" or self.Mailer == "qmail" or self.Mailer == "mail" and php_count(self.bcc) > 0:
            result += self.addrappend("Bcc", self.bcc)
        # end if
        if php_count(self.ReplyTo) > 0:
            result += self.addrappend("Reply-To", self.ReplyTo)
        # end if
        #// mail() sets the subject itself
        if self.Mailer != "mail":
            result += self.headerline("Subject", self.encodeheader(self.secureheader(self.Subject)))
        # end if
        #// Only allow a custom message ID if it conforms to RFC 5322 section 3.6.4
        #// https://tools.ietf.org/html/rfc5322#section-3.6.4
        if "" != self.MessageID and php_preg_match("/^<.*@.*>$/", self.MessageID):
            self.lastMessageID = self.MessageID
        else:
            self.lastMessageID = php_sprintf("<%s@%s>", self.uniqueid, self.serverhostname())
        # end if
        result += self.headerline("Message-ID", self.lastMessageID)
        if (not php_is_null(self.Priority)):
            result += self.headerline("X-Priority", self.Priority)
        # end if
        if self.XMailer == "":
            result += self.headerline("X-Mailer", "PHPMailer " + self.Version + " (https://github.com/PHPMailer/PHPMailer)")
        else:
            myXmailer = php_trim(self.XMailer)
            if myXmailer:
                result += self.headerline("X-Mailer", myXmailer)
            # end if
        # end if
        if self.ConfirmReadingTo != "":
            result += self.headerline("Disposition-Notification-To", "<" + self.ConfirmReadingTo + ">")
        # end if
        #// Add custom headers
        for header in self.CustomHeader:
            result += self.headerline(php_trim(header[0]), self.encodeheader(php_trim(header[1])))
        # end for
        if (not self.sign_key_file):
            result += self.headerline("MIME-Version", "1.0")
            result += self.getmailmime()
        # end if
        return result
    # end def createheader
    #// 
    #// Get the message MIME type headers.
    #// @access public
    #// @return string
    #//
    def getmailmime(self):
        
        result = ""
        ismultipart = True
        for case in Switch(self.message_type):
            if case("inline"):
                result += self.headerline("Content-Type", "multipart/related;")
                result += self.textline("   boundary=\"" + self.boundary[1] + "\"")
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
                result += self.headerline("Content-Type", "multipart/mixed;")
                result += self.textline("   boundary=\"" + self.boundary[1] + "\"")
                break
            # end if
            if case("alt"):
                pass
            # end if
            if case("alt_inline"):
                result += self.headerline("Content-Type", "multipart/alternative;")
                result += self.textline("   boundary=\"" + self.boundary[1] + "\"")
                break
            # end if
            if case():
                #// Catches case 'plain': and case '':
                result += self.textline("Content-Type: " + self.ContentType + "; charset=" + self.CharSet)
                ismultipart = False
                break
            # end if
        # end for
        #// RFC1341 part 5 says 7bit is assumed if not specified
        if self.Encoding != "7bit":
            #// RFC 2045 section 6.4 says multipart MIME parts may only use 7bit, 8bit or binary CTE
            if ismultipart:
                if self.Encoding == "8bit":
                    result += self.headerline("Content-Transfer-Encoding", "8bit")
                # end if
                pass
            else:
                result += self.headerline("Content-Transfer-Encoding", self.Encoding)
            # end if
        # end if
        if self.Mailer != "mail":
            result += self.LE
        # end if
        return result
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
        
        return php_md5(uniqid(time()))
    # end def generateid
    #// 
    #// Assemble the message body.
    #// Returns an empty string on failure.
    #// @access public
    #// @throws phpmailerException
    #// @return string The assembled message body
    #//
    def createbody(self):
        
        body = ""
        #// Create unique IDs and preset boundaries
        self.uniqueid = self.generateid()
        self.boundary[1] = "b1_" + self.uniqueid
        self.boundary[2] = "b2_" + self.uniqueid
        self.boundary[3] = "b3_" + self.uniqueid
        if self.sign_key_file:
            body += self.getmailmime() + self.LE
        # end if
        self.setwordwrap()
        bodyEncoding = self.Encoding
        bodyCharSet = self.CharSet
        #// Can we do a 7-bit downgrade?
        if bodyEncoding == "8bit" and (not self.has8bitchars(self.Body)):
            bodyEncoding = "7bit"
            #// All ISO 8859, Windows codepage and UTF-8 charsets are ascii compatible up to 7-bit
            bodyCharSet = "us-ascii"
        # end if
        #// If lines are too long, and we're not already using an encoding that will shorten them,
        #// change to quoted-printable transfer encoding for the body part only
        if "base64" != self.Encoding and self.haslinelongerthanmax(self.Body):
            bodyEncoding = "quoted-printable"
        # end if
        altBodyEncoding = self.Encoding
        altBodyCharSet = self.CharSet
        #// Can we do a 7-bit downgrade?
        if altBodyEncoding == "8bit" and (not self.has8bitchars(self.AltBody)):
            altBodyEncoding = "7bit"
            #// All ISO 8859, Windows codepage and UTF-8 charsets are ascii compatible up to 7-bit
            altBodyCharSet = "us-ascii"
        # end if
        #// If lines are too long, and we're not already using an encoding that will shorten them,
        #// change to quoted-printable transfer encoding for the alt body part only
        if "base64" != altBodyEncoding and self.haslinelongerthanmax(self.AltBody):
            altBodyEncoding = "quoted-printable"
        # end if
        #// Use this as a preamble in all multipart message types
        mimepre = "This is a multi-part message in MIME format." + self.LE + self.LE
        for case in Switch(self.message_type):
            if case("inline"):
                body += mimepre
                body += self.getboundary(self.boundary[1], bodyCharSet, "", bodyEncoding)
                body += self.encodestring(self.Body, bodyEncoding)
                body += self.LE + self.LE
                body += self.attachall("inline", self.boundary[1])
                break
            # end if
            if case("attach"):
                body += mimepre
                body += self.getboundary(self.boundary[1], bodyCharSet, "", bodyEncoding)
                body += self.encodestring(self.Body, bodyEncoding)
                body += self.LE + self.LE
                body += self.attachall("attachment", self.boundary[1])
                break
            # end if
            if case("inline_attach"):
                body += mimepre
                body += self.textline("--" + self.boundary[1])
                body += self.headerline("Content-Type", "multipart/related;")
                body += self.textline(" boundary=\"" + self.boundary[2] + "\"")
                body += self.LE
                body += self.getboundary(self.boundary[2], bodyCharSet, "", bodyEncoding)
                body += self.encodestring(self.Body, bodyEncoding)
                body += self.LE + self.LE
                body += self.attachall("inline", self.boundary[2])
                body += self.LE
                body += self.attachall("attachment", self.boundary[1])
                break
            # end if
            if case("alt"):
                body += mimepre
                body += self.getboundary(self.boundary[1], altBodyCharSet, "text/plain", altBodyEncoding)
                body += self.encodestring(self.AltBody, altBodyEncoding)
                body += self.LE + self.LE
                body += self.getboundary(self.boundary[1], bodyCharSet, "text/html", bodyEncoding)
                body += self.encodestring(self.Body, bodyEncoding)
                body += self.LE + self.LE
                if (not php_empty(lambda : self.Ical)):
                    body += self.getboundary(self.boundary[1], "", "text/calendar; method=REQUEST", "")
                    body += self.encodestring(self.Ical, self.Encoding)
                    body += self.LE + self.LE
                # end if
                body += self.endboundary(self.boundary[1])
                break
            # end if
            if case("alt_inline"):
                body += mimepre
                body += self.getboundary(self.boundary[1], altBodyCharSet, "text/plain", altBodyEncoding)
                body += self.encodestring(self.AltBody, altBodyEncoding)
                body += self.LE + self.LE
                body += self.textline("--" + self.boundary[1])
                body += self.headerline("Content-Type", "multipart/related;")
                body += self.textline(" boundary=\"" + self.boundary[2] + "\"")
                body += self.LE
                body += self.getboundary(self.boundary[2], bodyCharSet, "text/html", bodyEncoding)
                body += self.encodestring(self.Body, bodyEncoding)
                body += self.LE + self.LE
                body += self.attachall("inline", self.boundary[2])
                body += self.LE
                body += self.endboundary(self.boundary[1])
                break
            # end if
            if case("alt_attach"):
                body += mimepre
                body += self.textline("--" + self.boundary[1])
                body += self.headerline("Content-Type", "multipart/alternative;")
                body += self.textline(" boundary=\"" + self.boundary[2] + "\"")
                body += self.LE
                body += self.getboundary(self.boundary[2], altBodyCharSet, "text/plain", altBodyEncoding)
                body += self.encodestring(self.AltBody, altBodyEncoding)
                body += self.LE + self.LE
                body += self.getboundary(self.boundary[2], bodyCharSet, "text/html", bodyEncoding)
                body += self.encodestring(self.Body, bodyEncoding)
                body += self.LE + self.LE
                body += self.endboundary(self.boundary[2])
                body += self.LE
                body += self.attachall("attachment", self.boundary[1])
                break
            # end if
            if case("alt_inline_attach"):
                body += mimepre
                body += self.textline("--" + self.boundary[1])
                body += self.headerline("Content-Type", "multipart/alternative;")
                body += self.textline(" boundary=\"" + self.boundary[2] + "\"")
                body += self.LE
                body += self.getboundary(self.boundary[2], altBodyCharSet, "text/plain", altBodyEncoding)
                body += self.encodestring(self.AltBody, altBodyEncoding)
                body += self.LE + self.LE
                body += self.textline("--" + self.boundary[2])
                body += self.headerline("Content-Type", "multipart/related;")
                body += self.textline(" boundary=\"" + self.boundary[3] + "\"")
                body += self.LE
                body += self.getboundary(self.boundary[3], bodyCharSet, "text/html", bodyEncoding)
                body += self.encodestring(self.Body, bodyEncoding)
                body += self.LE + self.LE
                body += self.attachall("inline", self.boundary[3])
                body += self.LE
                body += self.endboundary(self.boundary[2])
                body += self.LE
                body += self.attachall("attachment", self.boundary[1])
                break
            # end if
            if case():
                #// Catch case 'plain' and case '', applies to simple `text/plain` and `text/html` body content types
                #// Reset the `Encoding` property in case we changed it for line length reasons
                self.Encoding = bodyEncoding
                body += self.encodestring(self.Body, self.Encoding)
                break
            # end if
        # end for
        if self.iserror():
            body = ""
        elif self.sign_key_file:
            try: 
                if (not php_defined("PKCS7_TEXT")):
                    raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("extension_missing") + "openssl"))
                # end if
                #// @TODO would be nice to use php://temp streams here, but need to wrap for PHP < 5.1
                file = php_tempnam(php_sys_get_temp_dir(), "mail")
                if False == file_put_contents(file, body):
                    raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("signing") + " Could not write temp file"))
                # end if
                signed = php_tempnam(php_sys_get_temp_dir(), "signed")
                #// Workaround for PHP bug https://bugs.php.net/bug.php?id=69197
                if php_empty(lambda : self.sign_extracerts_file):
                    sign = php_no_error(lambda: openssl_pkcs7_sign(file, signed, "file://" + php_realpath(self.sign_cert_file), Array("file://" + php_realpath(self.sign_key_file), self.sign_key_pass), None))
                else:
                    sign = php_no_error(lambda: openssl_pkcs7_sign(file, signed, "file://" + php_realpath(self.sign_cert_file), Array("file://" + php_realpath(self.sign_key_file), self.sign_key_pass), None, PKCS7_DETACHED, self.sign_extracerts_file))
                # end if
                if sign:
                    php_no_error(lambda: unlink(file))
                    body = php_file_get_contents(signed)
                    php_no_error(lambda: unlink(signed))
                    #// The message returned by openssl contains both headers and body, so need to split them up
                    parts = php_explode("\n\n", body, 2)
                    self.MIMEHeader += parts[0] + self.LE + self.LE
                    body = parts[1]
                else:
                    php_no_error(lambda: unlink(file))
                    php_no_error(lambda: unlink(signed))
                    raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("signing") + openssl_error_string()))
                # end if
            except phpmailerException as exc:
                body = ""
                if self.exceptions:
                    raise exc
                # end if
            # end try
        # end if
        return body
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
    def getboundary(self, boundary=None, charSet=None, contentType=None, encoding=None):
        
        result = ""
        if charSet == "":
            charSet = self.CharSet
        # end if
        if contentType == "":
            contentType = self.ContentType
        # end if
        if encoding == "":
            encoding = self.Encoding
        # end if
        result += self.textline("--" + boundary)
        result += php_sprintf("Content-Type: %s; charset=%s", contentType, charSet)
        result += self.LE
        #// RFC1341 part 5 says 7bit is assumed if not specified
        if encoding != "7bit":
            result += self.headerline("Content-Transfer-Encoding", encoding)
        # end if
        result += self.LE
        return result
    # end def getboundary
    #// 
    #// Return the end of a message boundary.
    #// @access protected
    #// @param string $boundary
    #// @return string
    #//
    def endboundary(self, boundary=None):
        
        return self.LE + "--" + boundary + "--" + self.LE
    # end def endboundary
    #// 
    #// Set the message type.
    #// PHPMailer only supports some preset message types, not arbitrary MIME structures.
    #// @access protected
    #// @return void
    #//
    def setmessagetype(self):
        
        type = Array()
        if self.alternativeexists():
            type[-1] = "alt"
        # end if
        if self.inlineimageexists():
            type[-1] = "inline"
        # end if
        if self.attachmentexists():
            type[-1] = "attach"
        # end if
        self.message_type = php_implode("_", type)
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
    def headerline(self, name=None, value=None):
        
        return name + ": " + value + self.LE
    # end def headerline
    #// 
    #// Return a formatted mail line.
    #// @access public
    #// @param string $value
    #// @return string
    #//
    def textline(self, value=None):
        
        return value + self.LE
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
    def addattachment(self, path=None, name="", encoding="base64", type="", disposition="attachment"):
        
        try: 
            if (not self.ispermittedpath(path)) or (not php_no_error(lambda: php_is_file(path))):
                raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("file_access") + path, self.STOP_CONTINUE))
            # end if
            #// If a MIME type is not specified, try to work it out from the file name
            if type == "":
                type = self.filenametotype(path)
            # end if
            filename = php_basename(path)
            if name == "":
                name = filename
            # end if
            self.attachment[-1] = Array({0: path, 1: filename, 2: name, 3: encoding, 4: type, 5: False, 6: disposition, 7: 0})
        except phpmailerException as exc:
            self.seterror(exc.getmessage())
            self.edebug(exc.getmessage())
            if self.exceptions:
                raise exc
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
    def attachall(self, disposition_type=None, boundary=None):
        
        #// Return text of body
        mime = Array()
        cidUniq = Array()
        incl = Array()
        #// Add all attachments
        for attachment in self.attachment:
            #// Check if it is a valid disposition_filter
            if attachment[6] == disposition_type:
                #// Check for string attachment
                string = ""
                path = ""
                bString = attachment[5]
                if bString:
                    string = attachment[0]
                else:
                    path = attachment[0]
                # end if
                inclhash = php_md5(serialize(attachment))
                if php_in_array(inclhash, incl):
                    continue
                # end if
                incl[-1] = inclhash
                name = attachment[2]
                encoding = attachment[3]
                type = attachment[4]
                disposition = attachment[6]
                cid = attachment[7]
                if disposition == "inline" and php_array_key_exists(cid, cidUniq):
                    continue
                # end if
                cidUniq[cid] = True
                mime[-1] = php_sprintf("--%s%s", boundary, self.LE)
                #// Only include a filename property if we have one
                if (not php_empty(lambda : name)):
                    mime[-1] = php_sprintf("Content-Type: %s; name=\"%s\"%s", type, self.encodeheader(self.secureheader(name)), self.LE)
                else:
                    mime[-1] = php_sprintf("Content-Type: %s%s", type, self.LE)
                # end if
                #// RFC1341 part 5 says 7bit is assumed if not specified
                if encoding != "7bit":
                    mime[-1] = php_sprintf("Content-Transfer-Encoding: %s%s", encoding, self.LE)
                # end if
                if disposition == "inline":
                    mime[-1] = php_sprintf("Content-ID: <%s>%s", cid, self.LE)
                # end if
                #// If a filename contains any of these chars, it should be quoted,
                #// but not otherwise: RFC2183 & RFC2045 5.1
                #// Fixes a warning in IETF's msglint MIME checker
                #// Allow for bypassing the Content-Disposition header totally
                if (not php_empty(lambda : disposition)):
                    encoded_name = self.encodeheader(self.secureheader(name))
                    if php_preg_match("/[ \\(\\)<>@,;:\\\"\\/\\[\\]\\?=]/", encoded_name):
                        mime[-1] = php_sprintf("Content-Disposition: %s; filename=\"%s\"%s", disposition, encoded_name, self.LE + self.LE)
                    else:
                        if (not php_empty(lambda : encoded_name)):
                            mime[-1] = php_sprintf("Content-Disposition: %s; filename=%s%s", disposition, encoded_name, self.LE + self.LE)
                        else:
                            mime[-1] = php_sprintf("Content-Disposition: %s%s", disposition, self.LE + self.LE)
                        # end if
                    # end if
                else:
                    mime[-1] = self.LE
                # end if
                #// Encode as string attachment
                if bString:
                    mime[-1] = self.encodestring(string, encoding)
                    if self.iserror():
                        return ""
                    # end if
                    mime[-1] = self.LE + self.LE
                else:
                    mime[-1] = self.encodefile(path, encoding)
                    if self.iserror():
                        return ""
                    # end if
                    mime[-1] = self.LE + self.LE
                # end if
            # end if
        # end for
        mime[-1] = php_sprintf("--%s--%s", boundary, self.LE)
        return php_implode("", mime)
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
    def encodefile(self, path=None, encoding="base64"):
        
        try: 
            if (not self.ispermittedpath(path)) or (not php_file_exists(path)):
                raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("file_open") + path, self.STOP_CONTINUE))
            # end if
            magic_quotes = PHP_VERSION_ID < 70400 and get_magic_quotes_runtime()
            #// WP: Patched for PHP 7.4.
            if magic_quotes:
                if php_version_compare(PHP_VERSION, "5.3.0", "<"):
                    set_magic_quotes_runtime(False)
                else:
                    #// Doesn't exist in PHP 5.4, but we don't need to check because
                    #// get_magic_quotes_runtime always returns false in 5.4+
                    #// so it will never get here
                    php_ini_set("magic_quotes_runtime", False)
                # end if
            # end if
            file_buffer = php_file_get_contents(path)
            file_buffer = self.encodestring(file_buffer, encoding)
            if magic_quotes:
                if php_version_compare(PHP_VERSION, "5.3.0", "<"):
                    set_magic_quotes_runtime(magic_quotes)
                else:
                    php_ini_set("magic_quotes_runtime", magic_quotes)
                # end if
            # end if
            return file_buffer
        except Exception as exc:
            self.seterror(exc.getmessage())
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
    def encodestring(self, str=None, encoding="base64"):
        
        encoded = ""
        for case in Switch(php_strtolower(encoding)):
            if case("base64"):
                encoded = chunk_split(php_base64_encode(str), 76, self.LE)
                break
            # end if
            if case("7bit"):
                pass
            # end if
            if case("8bit"):
                encoded = self.fixeol(str)
                #// Make sure it ends with a line break
                if php_substr(encoded, -php_strlen(self.LE)) != self.LE:
                    encoded += self.LE
                # end if
                break
            # end if
            if case("binary"):
                encoded = str
                break
            # end if
            if case("quoted-printable"):
                encoded = self.encodeqp(str)
                break
            # end if
            if case():
                self.seterror(self.lang("encoding") + encoding)
                break
            # end if
        # end for
        return encoded
    # end def encodestring
    #// 
    #// Encode a header string optimally.
    #// Picks shortest of Q, B, quoted-printable or none.
    #// @access public
    #// @param string $str
    #// @param string $position
    #// @return string
    #//
    def encodeheader(self, str=None, position="text"):
        
        matchcount = 0
        for case in Switch(php_strtolower(position)):
            if case("phrase"):
                if (not php_preg_match("/[\\200-\\377]/", str)):
                    #// Can't use addslashes as we don't know the value of magic_quotes_sybase
                    encoded = addcslashes(str, " ..\\\"")
                    if str == encoded and (not php_preg_match("/[^A-Za-z0-9!#$%&'*+\\/=?^_`{|}~ -]/", str)):
                        return encoded
                    else:
                        return str("\"") + str(encoded) + str("\"")
                    # end if
                # end if
                matchcount = preg_match_all("/[^\\040\\041\\043-\\133\\135-\\176]/", str, matches)
                break
            # end if
            if case("comment"):
                matchcount = preg_match_all("/[()\"]/", str, matches)
            # end if
            if case("text"):
                pass
            # end if
            if case():
                matchcount += preg_match_all("/[\\000-\\010\\013\\014\\016-\\037\\177-\\377]/", str, matches)
                break
            # end if
        # end for
        #// There are no chars that need encoding
        if matchcount == 0:
            return str
        # end if
        maxlen = 75 - 7 - php_strlen(self.CharSet)
        #// Try to select the encoding which should produce the shortest output
        if matchcount > php_strlen(str) / 3:
            #// More than a third of the content will need encoding, so B encoding will be most efficient
            encoding = "B"
            if php_function_exists("mb_strlen") and self.hasmultibytes(str):
                #// Use a custom function which correctly encodes and wraps long
                #// multibyte strings without breaking lines within a character
                encoded = self.base64encodewrapmb(str, "\n")
            else:
                encoded = php_base64_encode(str)
                maxlen -= maxlen % 4
                encoded = php_trim(chunk_split(encoded, maxlen, "\n"))
            # end if
        else:
            encoding = "Q"
            encoded = self.encodeq(str, position)
            encoded = self.wraptext(encoded, maxlen, True)
            encoded = php_str_replace("=" + self.CRLF, "\n", php_trim(encoded))
        # end if
        encoded = php_preg_replace("/^(.*)$/m", " =?" + self.CharSet + str("?") + str(encoding) + str("?\\1?="), encoded)
        encoded = php_trim(php_str_replace("\n", self.LE, encoded))
        return encoded
    # end def encodeheader
    #// 
    #// Check if a string contains multi-byte characters.
    #// @access public
    #// @param string $str multi-byte text to wrap encode
    #// @return boolean
    #//
    def hasmultibytes(self, str=None):
        
        if php_function_exists("mb_strlen"):
            return php_strlen(str) > php_mb_strlen(str, self.CharSet)
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
    def has8bitchars(self, text=None):
        
        return bool(php_preg_match("/[\\x80-\\xFF]/", text))
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
    def base64encodewrapmb(self, str=None, linebreak=None):
        
        start = "=?" + self.CharSet + "?B?"
        end_ = "?="
        encoded = ""
        if linebreak == None:
            linebreak = self.LE
        # end if
        mb_length = php_mb_strlen(str, self.CharSet)
        #// Each line must have length <= 75, including $start and $end
        length = 75 - php_strlen(start) - php_strlen(end_)
        #// Average multi-byte ratio
        ratio = mb_length / php_strlen(str)
        #// Base64 has a 4:3 ratio
        avgLength = floor(length * ratio * 0.75)
        i = 0
        while i < mb_length:
            
            lookBack = 0
            while True:
                offset = avgLength - lookBack
                chunk = php_mb_substr(str, i, offset, self.CharSet)
                chunk = php_base64_encode(chunk)
                lookBack += 1
                
                if php_strlen(chunk) > length:
                    break
                # end if
            # end while
            encoded += chunk + linebreak
            i += offset
        # end while
        #// Chomp the last linefeed
        encoded = php_substr(encoded, 0, -php_strlen(linebreak))
        return encoded
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
    def encodeqp(self, string=None, line_max=76):
        
        #// Use native function if it's available (>= PHP5.3)
        if php_function_exists("quoted_printable_encode"):
            return quoted_printable_encode(string)
        # end if
        #// Fall back to a pure PHP implementation
        string = php_str_replace(Array("%20", "%0D%0A.", "%0D%0A", "%"), Array(" ", "\r\n=2E", "\r\n", "="), rawurlencode(string))
        return php_preg_replace("/[^\\r\\n]{" + line_max - 3 + "}[^=\\r\\n]{2}/", "$0=\r\n", string)
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
    def encodeqpphp(self, string=None, line_max=76, space_conv=False):
        
        return self.encodeqp(string, line_max)
    # end def encodeqpphp
    #// 
    #// Encode a string using Q encoding.
    #// @link http://tools.ietf.org/html/rfc2047
    #// @param string $str the text to encode
    #// @param string $position Where the text is going to be used, see the RFC for what that means
    #// @access public
    #// @return string
    #//
    def encodeq(self, str=None, position="text"):
        
        #// There should not be any EOL in the string
        pattern = ""
        encoded = php_str_replace(Array("\r", "\n"), "", str)
        for case in Switch(php_strtolower(position)):
            if case("phrase"):
                #// RFC 2047 section 5.3
                pattern = "^A-Za-z0-9!*+\\/ -"
                break
            # end if
            if case("comment"):
                #// RFC 2047 section 5.2
                pattern = "\\(\\)\""
            # end if
            if case("text"):
                pass
            # end if
            if case():
                #// RFC 2047 section 5.1
                #// Replace every high ascii, control, =, ? and _ characters
                pattern = "\\000-\\011\\013\\014\\016-\\037\\075\\077\\137\\177-\\377" + pattern
                break
            # end if
        # end for
        matches = Array()
        if preg_match_all(str("/[") + str(pattern) + str("]/"), encoded, matches):
            #// If the string contains an '=', make sure it's the first thing we replace
            #// so as to avoid double-encoding
            eqkey = php_array_search("=", matches[0])
            if False != eqkey:
                matches[0][eqkey] = None
                array_unshift(matches[0], "=")
            # end if
            for char in array_unique(matches[0]):
                encoded = php_str_replace(char, "=" + php_sprintf("%02X", php_ord(char)), encoded)
            # end for
        # end if
        #// Replace every spaces to _ (more readable than =20)
        return php_str_replace(" ", "_", encoded)
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
    def addstringattachment(self, string=None, filename=None, encoding="base64", type="", disposition="attachment"):
        
        #// If a MIME type is not specified, try to work it out from the file name
        if type == "":
            type = self.filenametotype(filename)
        # end if
        #// Append to $attachment array
        self.attachment[-1] = Array({0: string, 1: filename, 2: php_basename(filename), 3: encoding, 4: type, 5: True, 6: disposition, 7: 0})
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
    def addembeddedimage(self, path=None, cid=None, name="", encoding="base64", type="", disposition="inline"):
        
        if (not self.ispermittedpath(path)) or (not php_no_error(lambda: php_is_file(path))):
            self.seterror(self.lang("file_access") + path)
            return False
        # end if
        #// If a MIME type is not specified, try to work it out from the file name
        if type == "":
            type = self.filenametotype(path)
        # end if
        filename = php_basename(path)
        if name == "":
            name = filename
        # end if
        #// Append to $attachment array
        self.attachment[-1] = Array({0: path, 1: filename, 2: name, 3: encoding, 4: type, 5: False, 6: disposition, 7: cid})
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
    def addstringembeddedimage(self, string=None, cid=None, name="", encoding="base64", type="", disposition="inline"):
        
        #// If a MIME type is not specified, try to work it out from the name
        if type == "" and (not php_empty(lambda : name)):
            type = self.filenametotype(name)
        # end if
        #// Append to $attachment array
        self.attachment[-1] = Array({0: string, 1: name, 2: name, 3: encoding, 4: type, 5: True, 6: disposition, 7: cid})
        return True
    # end def addstringembeddedimage
    #// 
    #// Check if an inline attachment is present.
    #// @access public
    #// @return boolean
    #//
    def inlineimageexists(self):
        
        for attachment in self.attachment:
            if attachment[6] == "inline":
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
        
        for attachment in self.attachment:
            if attachment[6] == "attachment":
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
    def clearqueuedaddresses(self, kind=None):
        
        RecipientsQueue = self.RecipientsQueue
        for address,params in RecipientsQueue:
            if params[0] == kind:
                self.RecipientsQueue[address] = None
            # end if
        # end for
    # end def clearqueuedaddresses
    #// 
    #// Clear all To recipients.
    #// @return void
    #//
    def clearaddresses(self):
        
        for to in self.to:
            self.all_recipients[php_strtolower(to[0])] = None
        # end for
        self.to = Array()
        self.clearqueuedaddresses("to")
    # end def clearaddresses
    #// 
    #// Clear all CC recipients.
    #// @return void
    #//
    def clearccs(self):
        
        for cc in self.cc:
            self.all_recipients[php_strtolower(cc[0])] = None
        # end for
        self.cc = Array()
        self.clearqueuedaddresses("cc")
    # end def clearccs
    #// 
    #// Clear all BCC recipients.
    #// @return void
    #//
    def clearbccs(self):
        
        for bcc in self.bcc:
            self.all_recipients[php_strtolower(bcc[0])] = None
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
    def seterror(self, msg=None):
        
        self.error_count += 1
        if self.Mailer == "smtp" and (not php_is_null(self.smtp)):
            lasterror = self.smtp.geterror()
            if (not php_empty(lambda : lasterror["error"])):
                msg += self.lang("smtp_error") + lasterror["error"]
                if (not php_empty(lambda : lasterror["detail"])):
                    msg += " Detail: " + lasterror["detail"]
                # end if
                if (not php_empty(lambda : lasterror["smtp_code"])):
                    msg += " SMTP code: " + lasterror["smtp_code"]
                # end if
                if (not php_empty(lambda : lasterror["smtp_code_ex"])):
                    msg += " Additional SMTP info: " + lasterror["smtp_code_ex"]
                # end if
            # end if
        # end if
        self.ErrorInfo = msg
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
        
        result = "localhost.localdomain"
        if (not php_empty(lambda : self.Hostname)):
            result = self.Hostname
        elif (php_isset(lambda : PHP_SERVER)) and php_array_key_exists("SERVER_NAME", PHP_SERVER) and (not php_empty(lambda : PHP_SERVER["SERVER_NAME"])):
            result = PHP_SERVER["SERVER_NAME"]
        elif php_function_exists("gethostname") and gethostname() != False:
            result = gethostname()
        elif php_uname("n") != False:
            result = php_uname("n")
        # end if
        return result
    # end def serverhostname
    #// 
    #// Get an error message in the current language.
    #// @access protected
    #// @param string $key
    #// @return string
    #//
    def lang(self, key=None):
        
        if php_count(self.language) < 1:
            self.setlanguage("en")
            pass
        # end if
        if php_array_key_exists(key, self.language):
            if key == "smtp_connect_failed":
                #// Include a link to troubleshooting docs on SMTP connection failure
                #// this is by far the biggest cause of support questions
                #// but it's usually not PHPMailer's fault.
                return self.language[key] + " https://github.com/PHPMailer/PHPMailer/wiki/Troubleshooting"
            # end if
            return self.language[key]
        else:
            #// Return the key as a fallback
            return key
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
    def fixeol(self, str=None):
        
        #// Normalise to \n
        nstr = php_str_replace(Array("\r\n", "\r"), "\n", str)
        #// Now convert LE as needed
        if self.LE != "\n":
            nstr = php_str_replace("\n", self.LE, nstr)
        # end if
        return nstr
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
    def addcustomheader(self, name=None, value=None):
        
        if value == None:
            #// Value passed in as name:value
            self.CustomHeader[-1] = php_explode(":", name, 2)
        else:
            self.CustomHeader[-1] = Array(name, value)
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
    def msghtml(self, message=None, basedir="", advanced=False):
        
        preg_match_all("/(src|background)=[\"'](.*)[\"']/Ui", message, images)
        if php_array_key_exists(2, images):
            if php_strlen(basedir) > 1 and php_substr(basedir, -1) != "/":
                #// Ensure $basedir has a trailing
                basedir += "/"
            # end if
            for imgindex,url in images[2]:
                #// Convert data URIs into embedded images
                if php_preg_match("#^data:(image[^;,]*)(;base64)?,#", url, match):
                    data = php_substr(url, php_strpos(url, ","))
                    if match[2]:
                        data = php_base64_decode(data)
                    else:
                        data = rawurldecode(data)
                    # end if
                    cid = php_md5(url) + "@phpmailer.0"
                    #// RFC2392 S 2
                    if self.addstringembeddedimage(data, cid, "embed" + imgindex, "base64", match[1]):
                        message = php_str_replace(images[0][imgindex], images[1][imgindex] + "=\"cid:" + cid + "\"", message)
                    # end if
                    continue
                # end if
                if (not php_empty(lambda : basedir)) and php_strpos(url, "..") == False and php_substr(url, 0, 4) != "cid:" and (not php_preg_match("#^[a-z][a-z0-9+.-]*:?//#i", url)):
                    filename = php_basename(url)
                    directory = php_dirname(url)
                    if directory == ".":
                        directory = ""
                    # end if
                    cid = php_md5(url) + "@phpmailer.0"
                    #// RFC2392 S 2
                    if php_strlen(directory) > 1 and php_substr(directory, -1) != "/":
                        directory += "/"
                    # end if
                    if self.addembeddedimage(basedir + directory + filename, cid, filename, "base64", self._mime_types(str(self.mb_pathinfo(filename, PATHINFO_EXTENSION)))):
                        message = php_preg_replace("/" + images[1][imgindex] + "=[\"']" + preg_quote(url, "/") + "[\"']/Ui", images[1][imgindex] + "=\"cid:" + cid + "\"", message)
                    # end if
                # end if
            # end for
        # end if
        self.ishtml(True)
        #// Convert all message body line breaks to CRLF, makes quoted-printable encoding work much better
        self.Body = self.normalizebreaks(message)
        self.AltBody = self.normalizebreaks(self.html2text(message, advanced))
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
    def html2text(self, html=None, advanced=False):
        
        if php_is_callable(advanced):
            return php_call_user_func(advanced, html)
        # end if
        return html_entity_decode(php_trim(strip_tags(php_preg_replace("/<(head|title|style|script)[^>]*>.*?<\\/\\1>/si", "", html))), ENT_QUOTES, self.CharSet)
    # end def html2text
    #// 
    #// Get the MIME type for a file extension.
    #// @param string $ext File extension
    #// @access public
    #// @return string MIME type of file.
    #// @static
    #//
    @classmethod
    def _mime_types(self, ext=""):
        
        mimes = Array({"xl": "application/excel", "js": "application/javascript", "hqx": "application/mac-binhex40", "cpt": "application/mac-compactpro", "bin": "application/macbinary", "doc": "application/msword", "word": "application/msword", "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "xltx": "application/vnd.openxmlformats-officedocument.spreadsheetml.template", "potx": "application/vnd.openxmlformats-officedocument.presentationml.template", "ppsx": "application/vnd.openxmlformats-officedocument.presentationml.slideshow", "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation", "sldx": "application/vnd.openxmlformats-officedocument.presentationml.slide", "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "dotx": "application/vnd.openxmlformats-officedocument.wordprocessingml.template", "xlam": "application/vnd.ms-excel.addin.macroEnabled.12", "xlsb": "application/vnd.ms-excel.sheet.binary.macroEnabled.12", "class": "application/octet-stream", "dll": "application/octet-stream", "dms": "application/octet-stream", "exe": "application/octet-stream", "lha": "application/octet-stream", "lzh": "application/octet-stream", "psd": "application/octet-stream", "sea": "application/octet-stream", "so": "application/octet-stream", "oda": "application/oda", "pdf": "application/pdf", "ai": "application/postscript", "eps": "application/postscript", "ps": "application/postscript", "smi": "application/smil", "smil": "application/smil", "mif": "application/vnd.mif", "xls": "application/vnd.ms-excel", "ppt": "application/vnd.ms-powerpoint", "wbxml": "application/vnd.wap.wbxml", "wmlc": "application/vnd.wap.wmlc", "dcr": "application/x-director", "dir": "application/x-director", "dxr": "application/x-director", "dvi": "application/x-dvi", "gtar": "application/x-gtar", "php3": "application/x-httpd-php", "php4": "application/x-httpd-php", "php": "application/x-httpd-php", "phtml": "application/x-httpd-php", "phps": "application/x-httpd-php-source", "swf": "application/x-shockwave-flash", "sit": "application/x-stuffit", "tar": "application/x-tar", "tgz": "application/x-tar", "xht": "application/xhtml+xml", "xhtml": "application/xhtml+xml", "zip": "application/zip", "mid": "audio/midi", "midi": "audio/midi", "mp2": "audio/mpeg", "mp3": "audio/mpeg", "mpga": "audio/mpeg", "aif": "audio/x-aiff", "aifc": "audio/x-aiff", "aiff": "audio/x-aiff", "ram": "audio/x-pn-realaudio", "rm": "audio/x-pn-realaudio", "rpm": "audio/x-pn-realaudio-plugin", "ra": "audio/x-realaudio", "wav": "audio/x-wav", "bmp": "image/bmp", "gif": "image/gif", "jpeg": "image/jpeg", "jpe": "image/jpeg", "jpg": "image/jpeg", "png": "image/png", "tiff": "image/tiff", "tif": "image/tiff", "eml": "message/rfc822", "css": "text/css", "html": "text/html", "htm": "text/html", "shtml": "text/html", "log": "text/plain", "text": "text/plain", "txt": "text/plain", "rtx": "text/richtext", "rtf": "text/rtf", "vcf": "text/vcard", "vcard": "text/vcard", "xml": "text/xml", "xsl": "text/xml", "mpeg": "video/mpeg", "mpe": "video/mpeg", "mpg": "video/mpeg", "mov": "video/quicktime", "qt": "video/quicktime", "rv": "video/vnd.rn-realvideo", "avi": "video/x-msvideo", "movie": "video/x-sgi-movie"})
        if php_array_key_exists(php_strtolower(ext), mimes):
            return mimes[php_strtolower(ext)]
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
    def filenametotype(self, filename=None):
        
        #// In case the path is a URL, strip any query string before getting extension
        qpos = php_strpos(filename, "?")
        if False != qpos:
            filename = php_substr(filename, 0, qpos)
        # end if
        pathinfo = self.mb_pathinfo(filename)
        return self._mime_types(pathinfo["extension"])
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
    def mb_pathinfo(self, path=None, options=None):
        
        ret = Array({"dirname": "", "basename": "", "extension": "", "filename": ""})
        pathinfo = Array()
        if php_preg_match("%^(.*?)[\\\\/]*(([^/\\\\]*?)(\\.([^\\.\\\\/]+?)|))[\\\\/\\.]*$%im", path, pathinfo):
            if php_array_key_exists(1, pathinfo):
                ret["dirname"] = pathinfo[1]
            # end if
            if php_array_key_exists(2, pathinfo):
                ret["basename"] = pathinfo[2]
            # end if
            if php_array_key_exists(5, pathinfo):
                ret["extension"] = pathinfo[5]
            # end if
            if php_array_key_exists(3, pathinfo):
                ret["filename"] = pathinfo[3]
            # end if
        # end if
        for case in Switch(options):
            if case(PATHINFO_DIRNAME):
                pass
            # end if
            if case("dirname"):
                return ret["dirname"]
            # end if
            if case(PATHINFO_BASENAME):
                pass
            # end if
            if case("basename"):
                return ret["basename"]
            # end if
            if case(PATHINFO_EXTENSION):
                pass
            # end if
            if case("extension"):
                return ret["extension"]
            # end if
            if case(PATHINFO_FILENAME):
                pass
            # end if
            if case("filename"):
                return ret["filename"]
            # end if
            if case():
                return ret
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
    def set(self, name=None, value=""):
        
        if property_exists(self, name):
            self.name = value
            return True
        else:
            self.seterror(self.lang("variable_set") + name)
            return False
        # end if
    # end def set
    #// 
    #// Strip newlines to prevent header injection.
    #// @access public
    #// @param string $str
    #// @return string
    #//
    def secureheader(self, str=None):
        
        return php_trim(php_str_replace(Array("\r", "\n"), "", str))
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
    def normalizebreaks(self, text=None, breaktype="\r\n"):
        
        return php_preg_replace("/(\\r\\n|\\r|\\n)/ms", breaktype, text)
    # end def normalizebreaks
    #// 
    #// Set the public and private key files and password for S/MIME signing.
    #// @access public
    #// @param string $cert_filename
    #// @param string $key_filename
    #// @param string $key_pass Password for private key
    #// @param string $extracerts_filename Optional path to chain certificate
    #//
    def sign(self, cert_filename=None, key_filename=None, key_pass=None, extracerts_filename=""):
        
        self.sign_cert_file = cert_filename
        self.sign_key_file = key_filename
        self.sign_key_pass = key_pass
        self.sign_extracerts_file = extracerts_filename
    # end def sign
    #// 
    #// Quoted-Printable-encode a DKIM header.
    #// @access public
    #// @param string $txt
    #// @return string
    #//
    def dkim_qp(self, txt=None):
        
        line = ""
        i = 0
        while i < php_strlen(txt):
            
            ord = php_ord(txt[i])
            if 33 <= ord and ord <= 58 or ord == 60 or 62 <= ord and ord <= 126:
                line += txt[i]
            else:
                line += "=" + php_sprintf("%02X", ord)
            # end if
            i += 1
        # end while
        return line
    # end def dkim_qp
    #// 
    #// Generate a DKIM signature.
    #// @access public
    #// @param string $signHeader
    #// @throws phpmailerException
    #// @return string The DKIM signature value
    #//
    def dkim_sign(self, signHeader=None):
        
        if (not php_defined("PKCS7_TEXT")):
            if self.exceptions:
                raise php_new_class("phpmailerException", lambda : phpmailerException(self.lang("extension_missing") + "openssl"))
            # end if
            return ""
        # end if
        privKeyStr = self.DKIM_private_string if (not php_empty(lambda : self.DKIM_private_string)) else php_file_get_contents(self.DKIM_private)
        if "" != self.DKIM_passphrase:
            privKey = openssl_pkey_get_private(privKeyStr, self.DKIM_passphrase)
        else:
            privKey = openssl_pkey_get_private(privKeyStr)
        # end if
        #// Workaround for missing digest algorithms in old PHP & OpenSSL versions
        #// @link http://stackoverflow.com/a/11117338/333340
        if php_version_compare(PHP_VERSION, "5.3.0") >= 0 and php_in_array("sha256WithRSAEncryption", openssl_get_md_methods(True)):
            if openssl_sign(signHeader, signature, privKey, "sha256WithRSAEncryption"):
                openssl_pkey_free(privKey)
                return php_base64_encode(signature)
            # end if
        else:
            pinfo = openssl_pkey_get_details(privKey)
            hash = hash("sha256", signHeader)
            #// 'Magic' constant for SHA256 from RFC3447
            #// @link https://tools.ietf.org/html/rfc3447#page-43
            t = "3031300d060960864801650304020105000420" + hash
            pslen = pinfo["bits"] / 8 - php_strlen(t) / 2 + 3
            eb = pack("H*", "0001" + php_str_repeat("FF", pslen) + "00" + t)
            if openssl_private_encrypt(eb, signature, privKey, OPENSSL_NO_PADDING):
                openssl_pkey_free(privKey)
                return php_base64_encode(signature)
            # end if
        # end if
        openssl_pkey_free(privKey)
        return ""
    # end def dkim_sign
    #// 
    #// Generate a DKIM canonicalization header.
    #// @access public
    #// @param string $signHeader Header
    #// @return string
    #//
    def dkim_headerc(self, signHeader=None):
        
        signHeader = php_preg_replace("/\\r\\n\\s+/", " ", signHeader)
        lines = php_explode("\r\n", signHeader)
        for key,line in lines:
            heading, value = php_explode(":", line, 2)
            heading = php_strtolower(heading)
            value = php_preg_replace("/\\s{2,}/", " ", value)
            #// Compress useless spaces
            lines[key] = heading + ":" + php_trim(value)
            pass
        # end for
        signHeader = php_implode("\r\n", lines)
        return signHeader
    # end def dkim_headerc
    #// 
    #// Generate a DKIM canonicalization body.
    #// @access public
    #// @param string $body Message Body
    #// @return string
    #//
    def dkim_bodyc(self, body=None):
        
        if body == "":
            return "\r\n"
        # end if
        #// stabilize line endings
        body = php_str_replace("\r\n", "\n", body)
        body = php_str_replace("\n", "\r\n", body)
        #// END stabilize line endings
        while True:
            
            if not (php_substr(body, php_strlen(body) - 4, 4) == "\r\n\r\n"):
                break
            # end if
            body = php_substr(body, 0, php_strlen(body) - 2)
        # end while
        return body
    # end def dkim_bodyc
    #// 
    #// Create the DKIM header and body in a new message header.
    #// @access public
    #// @param string $headers_line Header lines
    #// @param string $subject Subject
    #// @param string $body Body
    #// @return string
    #//
    def dkim_add(self, headers_line=None, subject=None, body=None):
        
        DKIMsignatureType = "rsa-sha256"
        #// Signature & hash algorithms
        DKIMcanonicalization = "relaxed/simple"
        #// Canonicalization of header/body
        DKIMquery = "dns/txt"
        #// Query method
        DKIMtime = time()
        #// Signature Timestamp = seconds since 00:00:00 - Jan 1, 1970 (UTC time zone)
        subject_header = str("Subject: ") + str(subject)
        headers = php_explode(self.LE, headers_line)
        from_header = ""
        to_header = ""
        date_header = ""
        current = ""
        for header in headers:
            if php_strpos(header, "From:") == 0:
                from_header = header
                current = "from_header"
            elif php_strpos(header, "To:") == 0:
                to_header = header
                current = "to_header"
            elif php_strpos(header, "Date:") == 0:
                date_header = header
                current = "date_header"
            else:
                if (not php_empty(lambda : current)) and php_strpos(header, " =?") == 0:
                    current += header
                else:
                    current = ""
                # end if
            # end if
        # end for
        from_ = php_str_replace("|", "=7C", self.dkim_qp(from_header))
        to = php_str_replace("|", "=7C", self.dkim_qp(to_header))
        date = php_str_replace("|", "=7C", self.dkim_qp(date_header))
        subject = php_str_replace("|", "=7C", self.dkim_qp(subject_header))
        #// Copied header fields (dkim-quoted-printable)
        body = self.dkim_bodyc(body)
        DKIMlen = php_strlen(body)
        #// Length of body
        DKIMb64 = php_base64_encode(pack("H*", hash("sha256", body)))
        #// Base64 of packed binary SHA-256 hash of body
        if "" == self.DKIM_identity:
            ident = ""
        else:
            ident = " i=" + self.DKIM_identity + ";"
        # end if
        dkimhdrs = "DKIM-Signature: v=1; a=" + DKIMsignatureType + "; q=" + DKIMquery + "; l=" + DKIMlen + "; s=" + self.DKIM_selector + ";\r\n" + "    t=" + DKIMtime + "; c=" + DKIMcanonicalization + ";\r\n" + "    h=From:To:Date:Subject;\r\n" + "    d=" + self.DKIM_domain + ";" + ident + "\r\n" + str("   z=") + str(from_) + str("\r\n") + str(" |") + str(to) + str("\r\n") + str(" |") + str(date) + str("\r\n") + str("   |") + str(subject) + str(";\r\n") + "   bh=" + DKIMb64 + ";\r\n" + "    b="
        toSign = self.dkim_headerc(from_header + "\r\n" + to_header + "\r\n" + date_header + "\r\n" + subject_header + "\r\n" + dkimhdrs)
        signed = self.dkim_sign(toSign)
        return dkimhdrs + signed + "\r\n"
    # end def dkim_add
    #// 
    #// Detect if a string contains a line longer than the maximum line length allowed.
    #// @param string $str
    #// @return boolean
    #// @static
    #//
    @classmethod
    def haslinelongerthanmax(self, str=None):
        
        #// +2 to include CRLF line break for a 1000 total
        return bool(php_preg_match("/^(.{" + self.MAX_LINE_LENGTH + 2 + ",})/m", str))
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
    def docallback(self, isSent=None, to=None, cc=None, bcc=None, subject=None, body=None, from_=None):
        
        if (not php_empty(lambda : self.action_function)) and php_is_callable(self.action_function):
            params = Array(isSent, to, cc, bcc, subject, body, from_)
            call_user_func_array(self.action_function, params)
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
        
        errorMsg = "<strong>" + htmlspecialchars(self.getmessage()) + "</strong><br />\n"
        return errorMsg
    # end def errormessage
# end class phpmailerException
