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
#// mail_fetch/setup.php
#// 
#// Copyright (c) 1999-2011 CDI (cdi@thewebmasters.net) All Rights Reserved
#// Modified by Philippe Mingo 2001-2009 mingo@rotedic.com
#// An RFC 1939 compliant wrapper class for the POP3 protocol.
#// 
#// Licensed under the GNU GPL. For full terms see the file COPYING.
#// 
#// POP3 class
#// 
#// @copyright 1999-2011 The SquirrelMail Project Team
#// @license http://opensource.org/licenses/gpl-license.php GNU Public License
#// @package plugins
#// @subpackage mail_fetch
#//
class POP3():
    ERROR = ""
    #// Error string.
    TIMEOUT = 60
    #// Default timeout before giving up on a
    #// network operation.
    COUNT = -1
    #// Mailbox msg count
    BUFFER = 512
    #// Socket buffer for socket fgets() calls.
    #// Per RFC 1939 the returned line a POP3
    #// server can send is 512 bytes.
    FP = ""
    #// The connection to the server's
    #// file descriptor
    MAILSERVER = ""
    #// Set this to hard code the server name
    DEBUG = False
    #// set to true to echo pop3
    #// commands and responses to error_log
    #// this WILL log passwords!
    BANNER = ""
    #// Holds the banner returned by the
    #// pop server - used for apop()
    ALLOWAPOP = False
    #// Allow or disallow apop()
    #// This must be set to true
    #// manually
    #// 
    #// PHP5 constructor.
    #//
    def __init__(self, server_="", timeout_=""):
        
        
        settype(self.BUFFER, "integer")
        if (not php_empty(lambda : server_)):
            #// Do not allow programs to alter MAILSERVER
            #// if it is already specified. They can get around
            #// this if they -really- want to, so don't count on it.
            if php_empty(lambda : self.MAILSERVER):
                self.MAILSERVER = server_
            # end if
        # end if
        if (not php_empty(lambda : timeout_)):
            settype(timeout_, "integer")
            self.TIMEOUT = timeout_
            if (not php_ini_get("safe_mode")):
                set_time_limit(timeout_)
            # end if
        # end if
        return True
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def pop3(self, server_="", timeout_=""):
        
        
        self.__init__(server_, timeout_)
    # end def pop3
    def update_timer(self):
        
        
        if (not php_ini_get("safe_mode")):
            set_time_limit(self.TIMEOUT)
        # end if
        return True
    # end def update_timer
    def connect(self, server_=None, port_=110):
        
        
        #// Opens a socket to the specified server. Unless overridden,
        #// port defaults to 110. Returns true on success, false on fail
        #// If MAILSERVER is set, override $server with its value.
        if (not (php_isset(lambda : port_))) or (not port_):
            port_ = 110
        # end if
        if (not php_empty(lambda : self.MAILSERVER)):
            server_ = self.MAILSERVER
        # end if
        if php_empty(lambda : server_):
            self.ERROR = "POP3 connect: " + _("No server specified")
            self.FP = None
            return False
        # end if
        fp_ = php_no_error(lambda: fsockopen(str(server_), port_, errno_, errstr_))
        if (not fp_):
            self.ERROR = "POP3 connect: " + _("Error ") + str("[") + str(errno_) + str("] [") + str(errstr_) + str("]")
            self.FP = None
            return False
        # end if
        socket_set_blocking(fp_, -1)
        self.update_timer()
        reply_ = php_fgets(fp_, self.BUFFER)
        reply_ = self.strip_clf(reply_)
        if self.DEBUG:
            php_error_log(str("POP3 SEND [connect: ") + str(server_) + str("] GOT [") + str(reply_) + str("]"), 0)
        # end if
        if (not self.is_ok(reply_)):
            self.ERROR = "POP3 connect: " + _("Error ") + str("[") + str(reply_) + str("]")
            self.FP = None
            return False
        # end if
        self.FP = fp_
        self.BANNER = self.parse_banner(reply_)
        return True
    # end def connect
    def user(self, user_=""):
        
        
        #// Sends the USER command, returns true or false
        if php_empty(lambda : user_):
            self.ERROR = "POP3 user: " + _("no login ID submitted")
            return False
        elif (not (php_isset(lambda : self.FP))):
            self.ERROR = "POP3 user: " + _("connection not established")
            return False
        else:
            reply_ = self.send_cmd(str("USER ") + str(user_))
            if (not self.is_ok(reply_)):
                self.ERROR = "POP3 user: " + _("Error ") + str("[") + str(reply_) + str("]")
                return False
            else:
                return True
            # end if
        # end if
    # end def user
    def pass_(self, pass_=""):
        
        
        #// Sends the PASS command, returns # of msgs in mailbox,
        #// returns false (undef) on Auth failure
        if php_empty(lambda : pass_):
            self.ERROR = "POP3 pass: " + _("No password submitted")
            return False
        elif (not (php_isset(lambda : self.FP))):
            self.ERROR = "POP3 pass: " + _("connection not established")
            return False
        else:
            reply_ = self.send_cmd(str("PASS ") + str(pass_))
            if (not self.is_ok(reply_)):
                self.ERROR = "POP3 pass: " + _("Authentication failed") + str(" [") + str(reply_) + str("]")
                self.quit()
                return False
            else:
                #// Auth successful.
                count_ = self.last("count")
                self.COUNT = count_
                return count_
            # end if
        # end if
    # end def pass_
    def apop(self, login_=None, pass_=None):
        
        
        #// Attempts an APOP login. If this fails, it'll
        #// try a standard login. YOUR SERVER MUST SUPPORT
        #// THE USE OF THE APOP COMMAND!
        #// (apop is optional per rfc1939)
        if (not (php_isset(lambda : self.FP))):
            self.ERROR = "POP3 apop: " + _("No connection to server")
            return False
        elif (not self.ALLOWAPOP):
            retVal_ = self.login(login_, pass_)
            return retVal_
        elif php_empty(lambda : login_):
            self.ERROR = "POP3 apop: " + _("No login ID submitted")
            return False
        elif php_empty(lambda : pass_):
            self.ERROR = "POP3 apop: " + _("No password submitted")
            return False
        else:
            banner_ = self.BANNER
            if (not banner_) or php_empty(lambda : banner_):
                self.ERROR = "POP3 apop: " + _("No server banner") + " - " + _("abort")
                retVal_ = self.login(login_, pass_)
                return retVal_
            else:
                AuthString_ = banner_
                AuthString_ += pass_
                APOPString_ = php_md5(AuthString_)
                cmd_ = str("APOP ") + str(login_) + str(" ") + str(APOPString_)
                reply_ = self.send_cmd(cmd_)
                if (not self.is_ok(reply_)):
                    self.ERROR = "POP3 apop: " + _("apop authentication failed") + " - " + _("abort")
                    retVal_ = self.login(login_, pass_)
                    return retVal_
                else:
                    #// Auth successful.
                    count_ = self.last("count")
                    self.COUNT = count_
                    return count_
                # end if
            # end if
        # end if
    # end def apop
    def login(self, login_="", pass_=""):
        
        
        #// Sends both user and pass. Returns # of msgs in mailbox or
        #// false on failure (or -1, if the error occurs while getting
        #// the number of messages.)
        if (not (php_isset(lambda : self.FP))):
            self.ERROR = "POP3 login: " + _("No connection to server")
            return False
        else:
            fp_ = self.FP
            if (not self.user(login_)):
                #// Preserve the error generated by user()
                return False
            else:
                count_ = self.pass_(pass_)
                if (not count_) or count_ == -1:
                    #// Preserve the error generated by last() and pass()
                    return False
                else:
                    return count_
                # end if
            # end if
        # end if
    # end def login
    def top(self, msgNum_=None, numLines_="0"):
        
        
        #// Gets the header and first $numLines of the msg body
        #// returns data in an array with each returned line being
        #// an array element. If $numLines is empty, returns
        #// only the header information, and none of the body.
        if (not (php_isset(lambda : self.FP))):
            self.ERROR = "POP3 top: " + _("No connection to server")
            return False
        # end if
        self.update_timer()
        fp_ = self.FP
        buffer_ = self.BUFFER
        cmd_ = str("TOP ") + str(msgNum_) + str(" ") + str(numLines_)
        fwrite(fp_, str("TOP ") + str(msgNum_) + str(" ") + str(numLines_) + str("\r\n"))
        reply_ = php_fgets(fp_, buffer_)
        reply_ = self.strip_clf(reply_)
        if self.DEBUG:
            php_no_error(lambda: php_error_log(str("POP3 SEND [") + str(cmd_) + str("] GOT [") + str(reply_) + str("]"), 0))
        # end if
        if (not self.is_ok(reply_)):
            self.ERROR = "POP3 top: " + _("Error ") + str("[") + str(reply_) + str("]")
            return False
        # end if
        count_ = 0
        MsgArray_ = Array()
        line_ = php_fgets(fp_, buffer_)
        while True:
            
            if not ((not php_preg_match("/^\\.\\r\\n/", line_))):
                break
            # end if
            MsgArray_[count_] = line_
            count_ += 1
            line_ = php_fgets(fp_, buffer_)
            if php_empty(lambda : line_):
                break
            # end if
        # end while
        return MsgArray_
    # end def top
    def pop_list(self, msgNum_=""):
        
        
        #// If called with an argument, returns that msgs' size in octets
        #// No argument returns an associative array of undeleted
        #// msg numbers and their sizes in octets
        if (not (php_isset(lambda : self.FP))):
            self.ERROR = "POP3 pop_list: " + _("No connection to server")
            return False
        # end if
        fp_ = self.FP
        Total_ = self.COUNT
        if (not Total_) or Total_ == -1:
            return False
        # end if
        if Total_ == 0:
            return Array("0", "0")
            pass
        # end if
        self.update_timer()
        if (not php_empty(lambda : msgNum_)):
            cmd_ = str("LIST ") + str(msgNum_)
            fwrite(fp_, str(cmd_) + str("\r\n"))
            reply_ = php_fgets(fp_, self.BUFFER)
            reply_ = self.strip_clf(reply_)
            if self.DEBUG:
                php_no_error(lambda: php_error_log(str("POP3 SEND [") + str(cmd_) + str("] GOT [") + str(reply_) + str("]"), 0))
            # end if
            if (not self.is_ok(reply_)):
                self.ERROR = "POP3 pop_list: " + _("Error ") + str("[") + str(reply_) + str("]")
                return False
            # end if
            junk_, num_, size_ = php_preg_split("/\\s+/", reply_)
            return size_
        # end if
        cmd_ = "LIST"
        reply_ = self.send_cmd(cmd_)
        if (not self.is_ok(reply_)):
            reply_ = self.strip_clf(reply_)
            self.ERROR = "POP3 pop_list: " + _("Error ") + str("[") + str(reply_) + str("]")
            return False
        # end if
        MsgArray_ = Array()
        MsgArray_[0] = Total_
        msgC_ = 1
        while msgC_ <= Total_:
            
            if msgC_ > Total_:
                break
            # end if
            line_ = php_fgets(fp_, self.BUFFER)
            line_ = self.strip_clf(line_)
            if php_strpos(line_, ".") == 0:
                self.ERROR = "POP3 pop_list: " + _("Premature end of list")
                return False
            # end if
            thisMsg_, msgSize_ = php_preg_split("/\\s+/", line_)
            settype(thisMsg_, "integer")
            if thisMsg_ != msgC_:
                MsgArray_[msgC_] = "deleted"
            else:
                MsgArray_[msgC_] = msgSize_
            # end if
            msgC_ += 1
        # end while
        return MsgArray_
    # end def pop_list
    def get(self, msgNum_=None):
        
        
        #// Retrieve the specified msg number. Returns an array
        #// where each line of the msg is an array element.
        if (not (php_isset(lambda : self.FP))):
            self.ERROR = "POP3 get: " + _("No connection to server")
            return False
        # end if
        self.update_timer()
        fp_ = self.FP
        buffer_ = self.BUFFER
        cmd_ = str("RETR ") + str(msgNum_)
        reply_ = self.send_cmd(cmd_)
        if (not self.is_ok(reply_)):
            self.ERROR = "POP3 get: " + _("Error ") + str("[") + str(reply_) + str("]")
            return False
        # end if
        count_ = 0
        MsgArray_ = Array()
        line_ = php_fgets(fp_, buffer_)
        while True:
            
            if not ((not php_preg_match("/^\\.\\r\\n/", line_))):
                break
            # end if
            if line_[0] == ".":
                line_ = php_substr(line_, 1)
            # end if
            MsgArray_[count_] = line_
            count_ += 1
            line_ = php_fgets(fp_, buffer_)
            if php_empty(lambda : line_):
                break
            # end if
        # end while
        return MsgArray_
    # end def get
    def last(self, type_="count"):
        
        
        #// Returns the highest msg number in the mailbox.
        #// returns -1 on error, 0+ on success, if type != count
        #// results in a popstat() call (2 element array returned)
        last_ = -1
        if (not (php_isset(lambda : self.FP))):
            self.ERROR = "POP3 last: " + _("No connection to server")
            return last_
        # end if
        reply_ = self.send_cmd("STAT")
        if (not self.is_ok(reply_)):
            self.ERROR = "POP3 last: " + _("Error ") + str("[") + str(reply_) + str("]")
            return last_
        # end if
        Vars_ = php_preg_split("/\\s+/", reply_)
        count_ = Vars_[1]
        size_ = Vars_[2]
        settype(count_, "integer")
        settype(size_, "integer")
        if type_ != "count":
            return Array(count_, size_)
        # end if
        return count_
    # end def last
    def reset(self):
        
        
        #// Resets the status of the remote server. This includes
        #// resetting the status of ALL msgs to not be deleted.
        #// This method automatically closes the connection to the server.
        if (not (php_isset(lambda : self.FP))):
            self.ERROR = "POP3 reset: " + _("No connection to server")
            return False
        # end if
        reply_ = self.send_cmd("RSET")
        if (not self.is_ok(reply_)):
            #// The POP3 RSET command -never- gives a -ERR
            #// response - if it ever does, something truly
            #// wild is going on.
            self.ERROR = "POP3 reset: " + _("Error ") + str("[") + str(reply_) + str("]")
            php_no_error(lambda: php_error_log(str("POP3 reset: ERROR [") + str(reply_) + str("]"), 0))
        # end if
        self.quit()
        return True
    # end def reset
    def send_cmd(self, cmd_=""):
        
        
        #// Sends a user defined command string to the
        #// POP server and returns the results. Useful for
        #// non-compliant or custom POP servers.
        #// Do NOT includ the \r\n as part of your command
        #// string - it will be appended automatically.
        #// The return value is a standard fgets() call, which
        #// will read up to $this->BUFFER bytes of data, until it
        #// encounters a new line, or EOF, whichever happens first.
        #// This method works best if $cmd responds with only
        #// one line of data.
        if (not (php_isset(lambda : self.FP))):
            self.ERROR = "POP3 send_cmd: " + _("No connection to server")
            return False
        # end if
        if php_empty(lambda : cmd_):
            self.ERROR = "POP3 send_cmd: " + _("Empty command string")
            return ""
        # end if
        fp_ = self.FP
        buffer_ = self.BUFFER
        self.update_timer()
        fwrite(fp_, str(cmd_) + str("\r\n"))
        reply_ = php_fgets(fp_, buffer_)
        reply_ = self.strip_clf(reply_)
        if self.DEBUG:
            php_no_error(lambda: php_error_log(str("POP3 SEND [") + str(cmd_) + str("] GOT [") + str(reply_) + str("]"), 0))
        # end if
        return reply_
    # end def send_cmd
    def quit(self):
        
        
        #// Closes the connection to the POP3 server, deleting
        #// any msgs marked as deleted.
        if (not (php_isset(lambda : self.FP))):
            self.ERROR = "POP3 quit: " + _("connection does not exist")
            return False
        # end if
        fp_ = self.FP
        cmd_ = "QUIT"
        fwrite(fp_, str(cmd_) + str("\r\n"))
        reply_ = php_fgets(fp_, self.BUFFER)
        reply_ = self.strip_clf(reply_)
        if self.DEBUG:
            php_no_error(lambda: php_error_log(str("POP3 SEND [") + str(cmd_) + str("] GOT [") + str(reply_) + str("]"), 0))
        # end if
        php_fclose(fp_)
        self.FP = None
        return True
    # end def quit
    def popstat(self):
        
        
        #// Returns an array of 2 elements. The number of undeleted
        #// msgs in the mailbox, and the size of the mbox in octets.
        PopArray_ = self.last("array")
        if PopArray_ == -1:
            return False
        # end if
        if (not PopArray_) or php_empty(lambda : PopArray_):
            return False
        # end if
        return PopArray_
    # end def popstat
    def uidl(self, msgNum_=""):
        
        
        #// Returns the UIDL of the msg specified. If called with
        #// no arguments, returns an associative array where each
        #// undeleted msg num is a key, and the msg's uidl is the element
        #// Array element 0 will contain the total number of msgs
        if (not (php_isset(lambda : self.FP))):
            self.ERROR = "POP3 uidl: " + _("No connection to server")
            return False
        # end if
        fp_ = self.FP
        buffer_ = self.BUFFER
        if (not php_empty(lambda : msgNum_)):
            cmd_ = str("UIDL ") + str(msgNum_)
            reply_ = self.send_cmd(cmd_)
            if (not self.is_ok(reply_)):
                self.ERROR = "POP3 uidl: " + _("Error ") + str("[") + str(reply_) + str("]")
                return False
            # end if
            ok_, num_, myUidl_ = php_preg_split("/\\s+/", reply_)
            return myUidl_
        else:
            self.update_timer()
            UIDLArray_ = Array()
            Total_ = self.COUNT
            UIDLArray_[0] = Total_
            if Total_ < 1:
                return UIDLArray_
            # end if
            cmd_ = "UIDL"
            fwrite(fp_, "UIDL\r\n")
            reply_ = php_fgets(fp_, buffer_)
            reply_ = self.strip_clf(reply_)
            if self.DEBUG:
                php_no_error(lambda: php_error_log(str("POP3 SEND [") + str(cmd_) + str("] GOT [") + str(reply_) + str("]"), 0))
            # end if
            if (not self.is_ok(reply_)):
                self.ERROR = "POP3 uidl: " + _("Error ") + str("[") + str(reply_) + str("]")
                return False
            # end if
            line_ = ""
            count_ = 1
            line_ = php_fgets(fp_, buffer_)
            while True:
                
                if not ((not php_preg_match("/^\\.\\r\\n/", line_))):
                    break
                # end if
                msg_, msgUidl_ = php_preg_split("/\\s+/", line_)
                msgUidl_ = self.strip_clf(msgUidl_)
                if count_ == msg_:
                    UIDLArray_[msg_] = msgUidl_
                else:
                    UIDLArray_[count_] = "deleted"
                # end if
                count_ += 1
                line_ = php_fgets(fp_, buffer_)
            # end while
        # end if
        return UIDLArray_
    # end def uidl
    def delete(self, msgNum_=""):
        
        
        #// Flags a specified msg as deleted. The msg will not
        #// be deleted until a quit() method is called.
        if (not (php_isset(lambda : self.FP))):
            self.ERROR = "POP3 delete: " + _("No connection to server")
            return False
        # end if
        if php_empty(lambda : msgNum_):
            self.ERROR = "POP3 delete: " + _("No msg number submitted")
            return False
        # end if
        reply_ = self.send_cmd(str("DELE ") + str(msgNum_))
        if (not self.is_ok(reply_)):
            self.ERROR = "POP3 delete: " + _("Command failed ") + str("[") + str(reply_) + str("]")
            return False
        # end if
        return True
    # end def delete
    #// 
    #// The following methods are internal to the class.
    def is_ok(self, cmd_=""):
        
        
        #// Return true or false on +OK or -ERR
        if php_empty(lambda : cmd_):
            return False
        else:
            return php_stripos(cmd_, "+OK") != False
        # end if
    # end def is_ok
    def strip_clf(self, text_=""):
        
        
        #// Strips \r\n from server responses
        if php_empty(lambda : text_):
            return text_
        else:
            stripped_ = php_str_replace(Array("\r", "\n"), "", text_)
            return stripped_
        # end if
    # end def strip_clf
    def parse_banner(self, server_text_=None):
        
        
        outside_ = True
        banner_ = ""
        length_ = php_strlen(server_text_)
        count_ = 0
        while count_ < length_:
            
            digit_ = php_substr(server_text_, count_, 1)
            if (not php_empty(lambda : digit_)):
                if (not outside_) and digit_ != "<" and digit_ != ">":
                    banner_ += digit_
                # end if
                if digit_ == "<":
                    outside_ = False
                # end if
                if digit_ == ">":
                    outside_ = True
                # end if
            # end if
            count_ += 1
        # end while
        banner_ = self.strip_clf(banner_)
        #// Just in case
        return str("<") + str(banner_) + str(">")
    # end def parse_banner
# end class POP3
#// End class
#// For php4 compatibility
if (not php_function_exists("stripos")):
    def stripos(haystack_=None, needle_=None, *_args_):
        
        
        return php_strpos(haystack_, php_stristr(haystack_, needle_))
    # end def stripos
# end if
