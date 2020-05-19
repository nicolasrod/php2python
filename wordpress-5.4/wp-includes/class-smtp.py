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
#// PHPMailer RFC821 SMTP email transport class.
#// PHP Version 5
#// @package PHPMailer
#// @link https://github.com/PHPMailer/PHPMailer/ The PHPMailer GitHub project
#// @author Marcus Bointon (Synchro/coolbru) <phpmailer@synchromedia.co.uk>
#// @author Jim Jagielski (jimjag) <jimjag@gmail.com>
#// @author Andy Prevost (codeworxtech) <codeworxtech@users.sourceforge.net>
#// @author Brent R. Matzelle (original founder)
#// @copyright 2014 Marcus Bointon
#// @copyright 2010 - 2012 Jim Jagielski
#// @copyright 2004 - 2009 Andy Prevost
#// @license http://www.gnu.org/copyleft/lesser.html GNU Lesser General Public License
#// @note This program is distributed in the hope that it will be useful - WITHOUT
#// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#// FITNESS FOR A PARTICULAR PURPOSE.
#// 
#// 
#// PHPMailer RFC821 SMTP email transport class.
#// Implements RFC 821 SMTP commands and provides some utility methods for sending mail to an SMTP server.
#// @package PHPMailer
#// @author Chris Ryan
#// @author Marcus Bointon <phpmailer@synchromedia.co.uk>
#//
class SMTP():
    VERSION = "5.2.27"
    CRLF = "\r\n"
    DEFAULT_SMTP_PORT = 25
    MAX_LINE_LENGTH = 998
    DEBUG_OFF = 0
    DEBUG_CLIENT = 1
    DEBUG_SERVER = 2
    DEBUG_CONNECTION = 3
    DEBUG_LOWLEVEL = 4
    #// 
    #// The PHPMailer SMTP Version number.
    #// @var string
    #// @deprecated Use the `VERSION` constant instead
    #// @see SMTP::VERSION
    #//
    Version = "5.2.27"
    #// 
    #// SMTP server port number.
    #// @var integer
    #// @deprecated This is only ever used as a default value, so use the `DEFAULT_SMTP_PORT` constant instead
    #// @see SMTP::DEFAULT_SMTP_PORT
    #//
    SMTP_PORT = 25
    #// 
    #// SMTP reply line ending.
    #// @var string
    #// @deprecated Use the `CRLF` constant instead
    #// @see SMTP::CRLF
    #//
    CRLF = "\r\n"
    #// 
    #// Debug output level.
    #// Options:
    #// self::DEBUG_OFF (`0`) No debug output, default
    #// self::DEBUG_CLIENT (`1`) Client commands
    #// self::DEBUG_SERVER (`2`) Client commands and server responses
    #// self::DEBUG_CONNECTION (`3`) As DEBUG_SERVER plus connection status
    #// self::DEBUG_LOWLEVEL (`4`) Low-level data output, all messages
    #// @var integer
    #//
    do_debug = self.DEBUG_OFF
    #// 
    #// How to handle debug output.
    #// Options:
    #// `echo` Output plain-text as-is, appropriate for CLI
    #// `html` Output escaped, line breaks converted to `<br>`, appropriate for browser output
    #// `error_log` Output to error log as configured in php.ini
    #// 
    #// Alternatively, you can provide a callable expecting two params: a message string and the debug level:
    #// <code>
    #// $smtp->Debugoutput = function($str, $level) {echo "debug level $level; message: $str";};
    #// </code>
    #// @var string|callable
    #//
    Debugoutput = "echo"
    #// 
    #// Whether to use VERP.
    #// @link http://en.wikipedia.org/wiki/Variable_envelope_return_path
    #// @link http://www.postfix.org/VERP_README.html Info on VERP
    #// @var boolean
    #//
    do_verp = False
    #// 
    #// The timeout value for connection, in seconds.
    #// Default of 5 minutes (300sec) is from RFC2821 section 4.5.3.2
    #// This needs to be quite high to function correctly with hosts using greetdelay as an anti-spam measure.
    #// @link http://tools.ietf.org/html/rfc2821#section-4.5.3.2
    #// @var integer
    #//
    Timeout = 300
    #// 
    #// How long to wait for commands to complete, in seconds.
    #// Default of 5 minutes (300sec) is from RFC2821 section 4.5.3.2
    #// @var integer
    #//
    Timelimit = 300
    #// 
    #// @var array Patterns to extract an SMTP transaction id from reply to a DATA command.
    #// The first capture group in each regex will be used as the ID.
    #//
    smtp_transaction_id_patterns = Array({"exim": "/[0-9]{3} OK id=(.*)/"}, {"sendmail": "/[0-9]{3} 2.0.0 (.*) Message/"}, {"postfix": "/[0-9]{3} 2.0.0 Ok: queued as (.*)/"})
    #// 
    #// @var string The last transaction ID issued in response to a DATA command,
    #// if one was detected
    #//
    last_smtp_transaction_id = Array()
    #// 
    #// The socket for the server connection.
    #// @var resource
    #//
    smtp_conn = Array()
    #// 
    #// Error information, if any, for the last SMTP command.
    #// @var array
    #//
    error = Array({"error": "", "detail": "", "smtp_code": "", "smtp_code_ex": ""})
    #// 
    #// The reply the server sent to us for HELO.
    #// If null, no HELO string has yet been received.
    #// @var string|null
    #//
    helo_rply = None
    #// 
    #// The set of SMTP extensions sent in reply to EHLO command.
    #// Indexes of the array are extension names.
    #// Value at index 'HELO' or 'EHLO' (according to command that was sent)
    #// represents the server name. In case of HELO it is the only element of the array.
    #// Other values can be boolean TRUE or an array containing extension options.
    #// If null, no HELO/EHLO string has yet been received.
    #// @var array|null
    #//
    server_caps = None
    #// 
    #// The most recent reply received from the server.
    #// @var string
    #//
    last_reply = ""
    #// 
    #// Output debugging info via a user-selected method.
    #// @see SMTP::$Debugoutput
    #// @see SMTP::$do_debug
    #// @param string $str Debug string to output
    #// @param integer $level The debug level of this message; see DEBUG_* constants
    #// @return void
    #//
    def edebug(self, str_=None, level_=0):
        
        
        if level_ > self.do_debug:
            return
        # end if
        #// Avoid clash with built-in function names
        if (not php_in_array(self.Debugoutput, Array("error_log", "html", "echo"))) and php_is_callable(self.Debugoutput):
            php_call_user_func(self.Debugoutput, str_, level_)
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
                php_print(gmdate("Y-m-d H:i:s") + " " + htmlentities(php_preg_replace("/[\\r\\n]+/", "", str_), ENT_QUOTES, "UTF-8") + "<br>\n")
                break
            # end if
            if case("echo"):
                pass
            # end if
            if case():
                #// Normalize line breaks
                str_ = php_preg_replace("/(\\r\\n|\\r|\\n)/ms", "\n", str_)
                php_print(gmdate("Y-m-d H:i:s") + " " + php_str_replace("\n", "\n                                         ", php_trim(str_)) + "\n")
            # end if
        # end for
    # end def edebug
    #// 
    #// Connect to an SMTP server.
    #// @param string $host SMTP server IP or host name
    #// @param integer $port The port number to connect to
    #// @param integer $timeout How long to wait for the connection to open
    #// @param array $options An array of options for stream_context_create()
    #// @access public
    #// @return boolean
    #//
    def connect(self, host_=None, port_=None, timeout_=30, options_=None):
        if port_ is None:
            port_ = None
        # end if
        if options_ is None:
            options_ = Array()
        # end if
        
        streamok_ = None
        #// This is enabled by default since 5.0.0 but some providers disable it
        #// Check this once and cache the result
        if php_is_null(streamok_):
            streamok_ = php_function_exists("stream_socket_client")
        # end if
        #// Clear errors to avoid confusion
        self.seterror("")
        #// Make sure we are __not__ connected
        if self.connected():
            #// Already connected, generate error
            self.seterror("Already connected to a server")
            return False
        # end if
        if php_empty(lambda : port_):
            port_ = self.DEFAULT_SMTP_PORT
        # end if
        #// Connect to the SMTP server
        self.edebug(str("Connection: opening to ") + str(host_) + str(":") + str(port_) + str(", timeout=") + str(timeout_) + str(", options=") + var_export(options_, True), self.DEBUG_CONNECTION)
        errno_ = 0
        errstr_ = ""
        if streamok_:
            socket_context_ = stream_context_create(options_)
            set_error_handler(Array(self, "errorHandler"))
            self.smtp_conn = stream_socket_client(host_ + ":" + port_, errno_, errstr_, timeout_, STREAM_CLIENT_CONNECT, socket_context_)
            restore_error_handler()
        else:
            #// Fall back to fsockopen which should work in more places, but is missing some features
            self.edebug("Connection: stream_socket_client not available, falling back to fsockopen", self.DEBUG_CONNECTION)
            set_error_handler(Array(self, "errorHandler"))
            self.smtp_conn = fsockopen(host_, port_, errno_, errstr_, timeout_)
            restore_error_handler()
        # end if
        #// Verify we connected properly
        if (not is_resource(self.smtp_conn)):
            self.seterror("Failed to connect to server", errno_, errstr_)
            self.edebug("SMTP ERROR: " + self.error["error"] + str(": ") + str(errstr_) + str(" (") + str(errno_) + str(")"), self.DEBUG_CLIENT)
            return False
        # end if
        self.edebug("Connection: opened", self.DEBUG_CONNECTION)
        #// SMTP server can take longer to respond, give longer timeout for first read
        #// Windows does not have support for this timeout function
        if php_substr(PHP_OS, 0, 3) != "WIN":
            max_ = php_ini_get("max_execution_time")
            #// Don't bother if unlimited
            if max_ != 0 and timeout_ > max_:
                php_no_error(lambda: set_time_limit(timeout_))
            # end if
            stream_set_timeout(self.smtp_conn, timeout_, 0)
        # end if
        #// Get any announcement
        announce_ = self.get_lines()
        self.edebug("SERVER -> CLIENT: " + announce_, self.DEBUG_SERVER)
        return True
    # end def connect
    #// 
    #// Initiate a TLS (encrypted) session.
    #// @access public
    #// @return boolean
    #//
    def starttls(self):
        
        
        if (not self.sendcommand("STARTTLS", "STARTTLS", 220)):
            return False
        # end if
        #// Allow the best TLS version(s) we can
        crypto_method_ = STREAM_CRYPTO_METHOD_TLS_CLIENT
        #// PHP 5.6.7 dropped inclusion of TLS 1.1 and 1.2 in STREAM_CRYPTO_METHOD_TLS_CLIENT
        #// so add them back in manually if we can
        if php_defined("STREAM_CRYPTO_METHOD_TLSv1_2_CLIENT"):
            crypto_method_ |= STREAM_CRYPTO_METHOD_TLSv1_2_CLIENT
            crypto_method_ |= STREAM_CRYPTO_METHOD_TLSv1_1_CLIENT
        # end if
        #// Begin encrypted connection
        set_error_handler(Array(self, "errorHandler"))
        crypto_ok_ = stream_socket_enable_crypto(self.smtp_conn, True, crypto_method_)
        restore_error_handler()
        return crypto_ok_
    # end def starttls
    #// 
    #// Perform SMTP authentication.
    #// Must be run after hello().
    #// @see hello()
    #// @param string $username The user name
    #// @param string $password The password
    #// @param string $authtype The auth type (PLAIN, LOGIN, CRAM-MD5)
    #// @param string $realm The auth realm for NTLM
    #// @param string $workstation The auth workstation for NTLM
    #// @param null|OAuth $OAuth An optional OAuth instance (@see PHPMailerOAuth)
    #// @return bool True if successfully authenticated.* @access public
    #//
    def authenticate(self, username_=None, password_=None, authtype_=None, realm_="", workstation_="", OAuth_=None):
        if authtype_ is None:
            authtype_ = None
        # end if
        if OAuth_ is None:
            OAuth_ = None
        # end if
        
        if (not self.server_caps):
            self.seterror("Authentication is not allowed before HELO/EHLO")
            return False
        # end if
        if php_array_key_exists("EHLO", self.server_caps):
            #// SMTP extensions are available; try to find a proper authentication method
            if (not php_array_key_exists("AUTH", self.server_caps)):
                self.seterror("Authentication is not allowed at this stage")
                #// 'at this stage' means that auth may be allowed after the stage changes
                #// e.g. after STARTTLS
                return False
            # end if
            self.edebug("Auth method requested: " + authtype_ if authtype_ else "UNKNOWN", self.DEBUG_LOWLEVEL)
            self.edebug("Auth methods available on the server: " + php_implode(",", self.server_caps["AUTH"]), self.DEBUG_LOWLEVEL)
            if php_empty(lambda : authtype_):
                for method_ in Array("CRAM-MD5", "LOGIN", "PLAIN"):
                    if php_in_array(method_, self.server_caps["AUTH"]):
                        authtype_ = method_
                        break
                    # end if
                # end for
                if php_empty(lambda : authtype_):
                    self.seterror("No supported authentication methods found")
                    return False
                # end if
                self.edebug("Auth method selected: " + authtype_, self.DEBUG_LOWLEVEL)
            # end if
            if (not php_in_array(authtype_, self.server_caps["AUTH"])):
                self.seterror(str("The requested authentication method \"") + str(authtype_) + str("\" is not supported by the server"))
                return False
            # end if
        elif php_empty(lambda : authtype_):
            authtype_ = "LOGIN"
        # end if
        for case in Switch(authtype_):
            if case("PLAIN"):
                #// Start authentication
                if (not self.sendcommand("AUTH", "AUTH PLAIN", 334)):
                    return False
                # end if
                #// Send encoded username and password
                if (not self.sendcommand("User & Password", php_base64_encode(" " + username_ + " " + password_), 235)):
                    return False
                # end if
                break
            # end if
            if case("LOGIN"):
                #// Start authentication
                if (not self.sendcommand("AUTH", "AUTH LOGIN", 334)):
                    return False
                # end if
                if (not self.sendcommand("Username", php_base64_encode(username_), 334)):
                    return False
                # end if
                if (not self.sendcommand("Password", php_base64_encode(password_), 235)):
                    return False
                # end if
                break
            # end if
            if case("CRAM-MD5"):
                #// Start authentication
                if (not self.sendcommand("AUTH CRAM-MD5", "AUTH CRAM-MD5", 334)):
                    return False
                # end if
                #// Get the challenge
                challenge_ = php_base64_decode(php_substr(self.last_reply, 4))
                #// Build the response
                response_ = username_ + " " + self.hmac(challenge_, password_)
                #// send encoded credentials
                return self.sendcommand("Username", php_base64_encode(response_), 235)
            # end if
            if case():
                self.seterror(str("Authentication method \"") + str(authtype_) + str("\" is not supported"))
                return False
            # end if
        # end for
        return True
    # end def authenticate
    #// 
    #// Calculate an MD5 HMAC hash.
    #// Works like hash_hmac('md5', $data, $key)
    #// in case that function is not available
    #// @param string $data The data to hash
    #// @param string $key The key to hash with
    #// @access protected
    #// @return string
    #//
    def hmac(self, data_=None, key_=None):
        
        
        if php_function_exists("hash_hmac"):
            return php_hash_hmac("md5", data_, key_)
        # end if
        #// The following borrowed from
        #// http://php.net/manual/en/function.mhash.php#27225
        #// RFC 2104 HMAC implementation for php.
        #// Creates an md5 HMAC.
        #// Eliminates the need to install mhash to compute a HMAC
        #// by Lance Rushing
        bytelen_ = 64
        #// byte length for md5
        if php_strlen(key_) > bytelen_:
            key_ = pack("H*", php_md5(key_))
        # end if
        key_ = php_str_pad(key_, bytelen_, chr(0))
        ipad_ = php_str_pad("", bytelen_, chr(54))
        opad_ = php_str_pad("", bytelen_, chr(92))
        k_ipad_ = key_ ^ ipad_
        k_opad_ = key_ ^ opad_
        return php_md5(k_opad_ + pack("H*", php_md5(k_ipad_ + data_)))
    # end def hmac
    #// 
    #// Check connection state.
    #// @access public
    #// @return boolean True if connected.
    #//
    def connected(self):
        
        
        if is_resource(self.smtp_conn):
            sock_status_ = stream_get_meta_data(self.smtp_conn)
            if sock_status_["eof"]:
                #// The socket is valid but we are not connected
                self.edebug("SMTP NOTICE: EOF caught while checking if connected", self.DEBUG_CLIENT)
                self.close()
                return False
            # end if
            return True
            pass
        # end if
        return False
    # end def connected
    #// 
    #// Close the socket and clean up the state of the class.
    #// Don't use this function without first trying to use QUIT.
    #// @see quit()
    #// @access public
    #// @return void
    #//
    def close(self):
        
        
        self.seterror("")
        self.server_caps = None
        self.helo_rply = None
        if is_resource(self.smtp_conn):
            #// close the connection and cleanup
            php_fclose(self.smtp_conn)
            self.smtp_conn = None
            #// Makes for cleaner serialization
            self.edebug("Connection: closed", self.DEBUG_CONNECTION)
        # end if
    # end def close
    #// 
    #// Send an SMTP DATA command.
    #// Issues a data command and sends the msg_data to the server,
    #// finializing the mail transaction. $msg_data is the message
    #// that is to be send with the headers. Each header needs to be
    #// on a single line followed by a <CRLF> with the message headers
    #// and the message body being separated by and additional <CRLF>.
    #// Implements rfc 821: DATA <CRLF>
    #// @param string $msg_data Message data to send
    #// @access public
    #// @return boolean
    #//
    def data(self, msg_data_=None):
        
        
        #// This will use the standard timelimit
        if (not self.sendcommand("DATA", "DATA", 354)):
            return False
        # end if
        #// The server is ready to accept data!
        #// According to rfc821 we should not send more than 1000 characters on a single line (including the CRLF)
        #// so we will break the data up into lines by \r and/or \n then if needed we will break each of those into
        #// smaller lines to fit within the limit.
        #// We will also look for lines that start with a '.' and prepend an additional '.'.
        #// NOTE: this does not count towards line-length limit.
        #// 
        #// Normalize line breaks before exploding
        lines_ = php_explode("\n", php_str_replace(Array("\r\n", "\r"), "\n", msg_data_))
        #// To distinguish between a complete RFC822 message and a plain message body, we check if the first field
        #// of the first line (':' separated) does not contain a space then it _should_ be a header and we will
        #// process all lines before a blank line as headers.
        #//
        field_ = php_substr(lines_[0], 0, php_strpos(lines_[0], ":"))
        in_headers_ = False
        if (not php_empty(lambda : field_)) and php_strpos(field_, " ") == False:
            in_headers_ = True
        # end if
        for line_ in lines_:
            lines_out_ = Array()
            if in_headers_ and line_ == "":
                in_headers_ = False
            # end if
            #// Break this line up into several smaller lines if it's too long
            #// Micro-optimisation: isset($str[$len]) is faster than (strlen($str) > $len),
            while True:
                
                if not ((php_isset(lambda : line_[self.MAX_LINE_LENGTH]))):
                    break
                # end if
                #// Working backwards, try to find a space within the last MAX_LINE_LENGTH chars of the line to break on
                #// so as to avoid breaking in the middle of a word
                pos_ = php_strrpos(php_substr(line_, 0, self.MAX_LINE_LENGTH), " ")
                #// Deliberately matches both false and 0
                if (not pos_):
                    #// No nice break found, add a hard break
                    pos_ = self.MAX_LINE_LENGTH - 1
                    lines_out_[-1] = php_substr(line_, 0, pos_)
                    line_ = php_substr(line_, pos_)
                else:
                    #// Break at the found point
                    lines_out_[-1] = php_substr(line_, 0, pos_)
                    #// Move along by the amount we dealt with
                    line_ = php_substr(line_, pos_ + 1)
                # end if
                #// If processing headers add a LWSP-char to the front of new line RFC822 section 3.1.1
                if in_headers_:
                    line_ = "   " + line_
                # end if
            # end while
            lines_out_[-1] = line_
            #// Send the lines to the server
            for line_out_ in lines_out_:
                #// RFC2821 section 4.5.2
                if (not php_empty(lambda : line_out_)) and line_out_[0] == ".":
                    line_out_ = "." + line_out_
                # end if
                self.client_send(line_out_ + self.CRLF)
            # end for
        # end for
        #// Message data has been sent, complete the command
        #// Increase timelimit for end of DATA command
        savetimelimit_ = self.Timelimit
        self.Timelimit = self.Timelimit * 2
        result_ = self.sendcommand("DATA END", ".", 250)
        self.recordlasttransactionid()
        #// Restore timelimit
        self.Timelimit = savetimelimit_
        return result_
    # end def data
    #// 
    #// Send an SMTP HELO or EHLO command.
    #// Used to identify the sending server to the receiving server.
    #// This makes sure that client and server are in a known state.
    #// Implements RFC 821: HELO <SP> <domain> <CRLF>
    #// and RFC 2821 EHLO.
    #// @param string $host The host name or IP to connect to
    #// @access public
    #// @return boolean
    #//
    def hello(self, host_=""):
        
        
        #// Try extended hello first (RFC 2821)
        return php_bool(self.sendhello("EHLO", host_) or self.sendhello("HELO", host_))
    # end def hello
    #// 
    #// Send an SMTP HELO or EHLO command.
    #// Low-level implementation used by hello()
    #// @see hello()
    #// @param string $hello The HELO string
    #// @param string $host The hostname to say we are
    #// @access protected
    #// @return boolean
    #//
    def sendhello(self, hello_=None, host_=None):
        
        
        noerror_ = self.sendcommand(hello_, hello_ + " " + host_, 250)
        self.helo_rply = self.last_reply
        if noerror_:
            self.parsehellofields(hello_)
        else:
            self.server_caps = None
        # end if
        return noerror_
    # end def sendhello
    #// 
    #// Parse a reply to HELO/EHLO command to discover server extensions.
    #// In case of HELO, the only parameter that can be discovered is a server name.
    #// @access protected
    #// @param string $type - 'HELO' or 'EHLO'
    #//
    def parsehellofields(self, type_=None):
        
        
        self.server_caps = Array()
        lines_ = php_explode("\n", self.helo_rply)
        for n_,s_ in lines_:
            #// First 4 chars contain response code followed by - or space
            s_ = php_trim(php_substr(s_, 4))
            if php_empty(lambda : s_):
                continue
            # end if
            fields_ = php_explode(" ", s_)
            if (not php_empty(lambda : fields_)):
                if (not n_):
                    name_ = type_
                    fields_ = fields_[0]
                else:
                    name_ = php_array_shift(fields_)
                    for case in Switch(name_):
                        if case("SIZE"):
                            fields_ = fields_[0] if fields_ else 0
                            break
                        # end if
                        if case("AUTH"):
                            if (not php_is_array(fields_)):
                                fields_ = Array()
                            # end if
                            break
                        # end if
                        if case():
                            fields_ = True
                        # end if
                    # end for
                # end if
                self.server_caps[name_] = fields_
            # end if
        # end for
    # end def parsehellofields
    #// 
    #// Send an SMTP MAIL command.
    #// Starts a mail transaction from the email address specified in
    #// $from. Returns true if successful or false otherwise. If True
    #// the mail transaction is started and then one or more recipient
    #// commands may be called followed by a data command.
    #// Implements rfc 821: MAIL <SP> FROM:<reverse-path> <CRLF>
    #// @param string $from Source address of this message
    #// @access public
    #// @return boolean
    #//
    def mail(self, from_=None):
        
        
        useVerp_ = " XVERP" if self.do_verp else ""
        return self.sendcommand("MAIL FROM", "MAIL FROM:<" + from_ + ">" + useVerp_, 250)
    # end def mail
    #// 
    #// Send an SMTP QUIT command.
    #// Closes the socket if there is no error or the $close_on_error argument is true.
    #// Implements from rfc 821: QUIT <CRLF>
    #// @param boolean $close_on_error Should the connection close if an error occurs?
    #// @access public
    #// @return boolean
    #//
    def quit(self, close_on_error_=None):
        if close_on_error_ is None:
            close_on_error_ = True
        # end if
        
        noerror_ = self.sendcommand("QUIT", "QUIT", 221)
        err_ = self.error
        #// Save any error
        if noerror_ or close_on_error_:
            self.close()
            self.error = err_
            pass
        # end if
        return noerror_
    # end def quit
    #// 
    #// Send an SMTP RCPT command.
    #// Sets the TO argument to $toaddr.
    #// Returns true if the recipient was accepted false if it was rejected.
    #// Implements from rfc 821: RCPT <SP> TO:<forward-path> <CRLF>
    #// @param string $address The address the message is being sent to
    #// @access public
    #// @return boolean
    #//
    def recipient(self, address_=None):
        
        
        return self.sendcommand("RCPT TO", "RCPT TO:<" + address_ + ">", Array(250, 251))
    # end def recipient
    #// 
    #// Send an SMTP RSET command.
    #// Abort any transaction that is currently in progress.
    #// Implements rfc 821: RSET <CRLF>
    #// @access public
    #// @return boolean True on success.
    #//
    def reset(self):
        
        
        return self.sendcommand("RSET", "RSET", 250)
    # end def reset
    #// 
    #// Send a command to an SMTP server and check its return code.
    #// @param string $command The command name - not sent to the server
    #// @param string $commandstring The actual command to send
    #// @param integer|array $expect One or more expected integer success codes
    #// @access protected
    #// @return boolean True on success.
    #//
    def sendcommand(self, command_=None, commandstring_=None, expect_=None):
        
        
        if (not self.connected()):
            self.seterror(str("Called ") + str(command_) + str(" without being connected"))
            return False
        # end if
        #// Reject line breaks in all commands
        if php_strpos(commandstring_, "\n") != False or php_strpos(commandstring_, "\r") != False:
            self.seterror(str("Command '") + str(command_) + str("' contained line breaks"))
            return False
        # end if
        self.client_send(commandstring_ + self.CRLF)
        self.last_reply = self.get_lines()
        #// Fetch SMTP code and possible error code explanation
        matches_ = Array()
        if php_preg_match("/^([0-9]{3})[ -](?:([0-9]\\.[0-9]\\.[0-9]) )?/", self.last_reply, matches_):
            code_ = matches_[1]
            code_ex_ = matches_[2] if php_count(matches_) > 2 else None
            #// Cut off error code from each response line
            detail_ = php_preg_replace(str("/") + str(code_) + str("[ -]") + php_str_replace(".", "\\.", code_ex_) + " " if code_ex_ else "" + "/m", "", self.last_reply)
        else:
            #// Fall back to simple parsing if regex fails
            code_ = php_substr(self.last_reply, 0, 3)
            code_ex_ = None
            detail_ = php_substr(self.last_reply, 4)
        # end if
        self.edebug("SERVER -> CLIENT: " + self.last_reply, self.DEBUG_SERVER)
        if (not php_in_array(code_, expect_)):
            self.seterror(str(command_) + str(" command failed"), detail_, code_, code_ex_)
            self.edebug("SMTP ERROR: " + self.error["error"] + ": " + self.last_reply, self.DEBUG_CLIENT)
            return False
        # end if
        self.seterror("")
        return True
    # end def sendcommand
    #// 
    #// Send an SMTP SAML command.
    #// Starts a mail transaction from the email address specified in $from.
    #// Returns true if successful or false otherwise. If True
    #// the mail transaction is started and then one or more recipient
    #// commands may be called followed by a data command. This command
    #// will send the message to the users terminal if they are logged
    #// in and send them an email.
    #// Implements rfc 821: SAML <SP> FROM:<reverse-path> <CRLF>
    #// @param string $from The address the message is from
    #// @access public
    #// @return boolean
    #//
    def sendandmail(self, from_=None):
        
        
        return self.sendcommand("SAML", str("SAML FROM:") + str(from_), 250)
    # end def sendandmail
    #// 
    #// Send an SMTP VRFY command.
    #// @param string $name The name to verify
    #// @access public
    #// @return boolean
    #//
    def verify(self, name_=None):
        
        
        return self.sendcommand("VRFY", str("VRFY ") + str(name_), Array(250, 251))
    # end def verify
    #// 
    #// Send an SMTP NOOP command.
    #// Used to keep keep-alives alive, doesn't actually do anything
    #// @access public
    #// @return boolean
    #//
    def noop(self):
        
        
        return self.sendcommand("NOOP", "NOOP", 250)
    # end def noop
    #// 
    #// Send an SMTP TURN command.
    #// This is an optional command for SMTP that this class does not support.
    #// This method is here to make the RFC821 Definition complete for this class
    #// and _may_ be implemented in future
    #// Implements from rfc 821: TURN <CRLF>
    #// @access public
    #// @return boolean
    #//
    def turn(self):
        
        
        self.seterror("The SMTP TURN command is not implemented")
        self.edebug("SMTP NOTICE: " + self.error["error"], self.DEBUG_CLIENT)
        return False
    # end def turn
    #// 
    #// Send raw data to the server.
    #// @param string $data The data to send
    #// @access public
    #// @return integer|boolean The number of bytes sent to the server or false on error
    #//
    def client_send(self, data_=None):
        
        
        self.edebug(str("CLIENT -> SERVER: ") + str(data_), self.DEBUG_CLIENT)
        set_error_handler(Array(self, "errorHandler"))
        result_ = fwrite(self.smtp_conn, data_)
        restore_error_handler()
        return result_
    # end def client_send
    #// 
    #// Get the latest error.
    #// @access public
    #// @return array
    #//
    def geterror(self):
        
        
        return self.error
    # end def geterror
    #// 
    #// Get SMTP extensions available on the server
    #// @access public
    #// @return array|null
    #//
    def getserverextlist(self):
        
        
        return self.server_caps
    # end def getserverextlist
    #// 
    #// A multipurpose method
    #// The method works in three ways, dependent on argument value and current state
    #// 1. HELO/EHLO was not sent - returns null and set up $this->error
    #// 2. HELO was sent
    #// $name = 'HELO': returns server name
    #// $name = 'EHLO': returns boolean false
    #// $name = any string: returns null and set up $this->error
    #// 3. EHLO was sent
    #// $name = 'HELO'|'EHLO': returns server name
    #// $name = any string: if extension $name exists, returns boolean True
    #// or its options. Otherwise returns boolean False
    #// In other words, one can use this method to detect 3 conditions:
    #// - null returned: handshake was not or we don't know about ext (refer to $this->error)
    #// - false returned: the requested feature exactly not exists
    #// - positive value returned: the requested feature exists
    #// @param string $name Name of SMTP extension or 'HELO'|'EHLO'
    #// @return mixed
    #//
    def getserverext(self, name_=None):
        
        
        if (not self.server_caps):
            self.seterror("No HELO/EHLO was sent")
            return None
        # end if
        #// the tight logic knot ;)
        if (not php_array_key_exists(name_, self.server_caps)):
            if name_ == "HELO":
                return self.server_caps["EHLO"]
            # end if
            if name_ == "EHLO" or php_array_key_exists("EHLO", self.server_caps):
                return False
            # end if
            self.seterror("HELO handshake was used. Client knows nothing about server extensions")
            return None
        # end if
        return self.server_caps[name_]
    # end def getserverext
    #// 
    #// Get the last reply from the server.
    #// @access public
    #// @return string
    #//
    def getlastreply(self):
        
        
        return self.last_reply
    # end def getlastreply
    #// 
    #// Read the SMTP server's response.
    #// Either before eof or socket timeout occurs on the operation.
    #// With SMTP we can tell if we have more lines to read if the
    #// 4th character is '-' symbol. If it is a space then we don't
    #// need to read anything else.
    #// @access protected
    #// @return string
    #//
    def get_lines(self):
        
        
        #// If the connection is bad, give up straight away
        if (not is_resource(self.smtp_conn)):
            return ""
        # end if
        data_ = ""
        endtime_ = 0
        stream_set_timeout(self.smtp_conn, self.Timeout)
        if self.Timelimit > 0:
            endtime_ = time() + self.Timelimit
        # end if
        while True:
            
            if not (is_resource(self.smtp_conn) and (not php_feof(self.smtp_conn))):
                break
            # end if
            str_ = php_no_error(lambda: php_fgets(self.smtp_conn, 515))
            self.edebug(str("SMTP -> get_lines(): $data is \"") + str(data_) + str("\""), self.DEBUG_LOWLEVEL)
            self.edebug(str("SMTP -> get_lines(): $str is  \"") + str(str_) + str("\""), self.DEBUG_LOWLEVEL)
            data_ += str_
            #// If response is only 3 chars (not valid, but RFC5321 S4.2 says it must be handled),
            #// or 4th character is a space, we are done reading, break the loop,
            #// string array access is a micro-optimisation over strlen
            if (not (php_isset(lambda : str_[3]))) or (php_isset(lambda : str_[3])) and str_[3] == " ":
                break
            # end if
            #// Timed-out? Log and break
            info_ = stream_get_meta_data(self.smtp_conn)
            if info_["timed_out"]:
                self.edebug("SMTP -> get_lines(): timed-out (" + self.Timeout + " sec)", self.DEBUG_LOWLEVEL)
                break
            # end if
            #// Now check if reads took too long
            if endtime_ and time() > endtime_:
                self.edebug("SMTP -> get_lines(): timelimit reached (" + self.Timelimit + " sec)", self.DEBUG_LOWLEVEL)
                break
            # end if
        # end while
        return data_
    # end def get_lines
    #// 
    #// Enable or disable VERP address generation.
    #// @param boolean $enabled
    #//
    def setverp(self, enabled_=None):
        if enabled_ is None:
            enabled_ = False
        # end if
        
        self.do_verp = enabled_
    # end def setverp
    #// 
    #// Get VERP address generation mode.
    #// @return boolean
    #//
    def getverp(self):
        
        
        return self.do_verp
    # end def getverp
    #// 
    #// Set error messages and codes.
    #// @param string $message The error message
    #// @param string $detail Further detail on the error
    #// @param string $smtp_code An associated SMTP error code
    #// @param string $smtp_code_ex Extended SMTP code
    #//
    def seterror(self, message_=None, detail_="", smtp_code_="", smtp_code_ex_=""):
        
        
        self.error = Array({"error": message_, "detail": detail_, "smtp_code": smtp_code_, "smtp_code_ex": smtp_code_ex_})
    # end def seterror
    #// 
    #// Set debug output method.
    #// @param string|callable $method The name of the mechanism to use for debugging output, or a callable to handle it.
    #//
    def setdebugoutput(self, method_="echo"):
        
        
        self.Debugoutput = method_
    # end def setdebugoutput
    #// 
    #// Get debug output method.
    #// @return string
    #//
    def getdebugoutput(self):
        
        
        return self.Debugoutput
    # end def getdebugoutput
    #// 
    #// Set debug output level.
    #// @param integer $level
    #//
    def setdebuglevel(self, level_=0):
        
        
        self.do_debug = level_
    # end def setdebuglevel
    #// 
    #// Get debug output level.
    #// @return integer
    #//
    def getdebuglevel(self):
        
        
        return self.do_debug
    # end def getdebuglevel
    #// 
    #// Set SMTP timeout.
    #// @param integer $timeout
    #//
    def settimeout(self, timeout_=0):
        
        
        self.Timeout = timeout_
    # end def settimeout
    #// 
    #// Get SMTP timeout.
    #// @return integer
    #//
    def gettimeout(self):
        
        
        return self.Timeout
    # end def gettimeout
    #// 
    #// Reports an error number and string.
    #// @param integer $errno The error number returned by PHP.
    #// @param string $errmsg The error message returned by PHP.
    #// @param string $errfile The file the error occurred in
    #// @param integer $errline The line number the error occurred on
    #//
    def errorhandler(self, errno_=None, errmsg_=None, errfile_="", errline_=0):
        
        
        notice_ = "Connection failed."
        self.seterror(notice_, errno_, errmsg_)
        self.edebug(notice_ + " Error #" + errno_ + ": " + errmsg_ + str(" [") + str(errfile_) + str(" line ") + str(errline_) + str("]"), self.DEBUG_CONNECTION)
    # end def errorhandler
    #// 
    #// Extract and return the ID of the last SMTP transaction based on
    #// a list of patterns provided in SMTP::$smtp_transaction_id_patterns.
    #// Relies on the host providing the ID in response to a DATA command.
    #// If no reply has been received yet, it will return null.
    #// If no pattern was matched, it will return false.
    #// @return bool|null|string
    #//
    def recordlasttransactionid(self):
        
        
        reply_ = self.getlastreply()
        if php_empty(lambda : reply_):
            self.last_smtp_transaction_id = None
        else:
            self.last_smtp_transaction_id = False
            for smtp_transaction_id_pattern_ in self.smtp_transaction_id_patterns:
                if php_preg_match(smtp_transaction_id_pattern_, reply_, matches_):
                    self.last_smtp_transaction_id = matches_[1]
                # end if
            # end for
        # end if
        return self.last_smtp_transaction_id
    # end def recordlasttransactionid
    #// 
    #// Get the queue/transaction ID of the last SMTP transaction
    #// If no reply has been received yet, it will return null.
    #// If no pattern was matched, it will return false.
    #// @return bool|null|string
    #// @see recordLastTransactionID()
    #//
    def getlasttransactionid(self):
        
        
        return self.last_smtp_transaction_id
    # end def getlasttransactionid
# end class SMTP
