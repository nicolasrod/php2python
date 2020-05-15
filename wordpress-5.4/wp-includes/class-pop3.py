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
    TIMEOUT = 60
    COUNT = -1
    BUFFER = 512
    FP = ""
    MAILSERVER = ""
    DEBUG = False
    BANNER = ""
    ALLOWAPOP = False
    #// Allow or disallow apop()
    #// This must be set to true
    #// manually
    #// 
    #// PHP5 constructor.
    #//
    def __init__(self, server="", timeout=""):
        
        settype(self.BUFFER, "integer")
        if (not php_empty(lambda : server)):
            #// Do not allow programs to alter MAILSERVER
            #// if it is already specified. They can get around
            #// this if they -really- want to, so don't count on it.
            if php_empty(lambda : self.MAILSERVER):
                self.MAILSERVER = server
            # end if
        # end if
        if (not php_empty(lambda : timeout)):
            settype(timeout, "integer")
            self.TIMEOUT = timeout
            if (not php_ini_get("safe_mode")):
                set_time_limit(timeout)
            # end if
        # end if
        return True
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def pop3(self, server="", timeout=""):
        
        self.__init__(server, timeout)
    # end def pop3
    def update_timer(self):
        
        if (not php_ini_get("safe_mode")):
            set_time_limit(self.TIMEOUT)
        # end if
        return True
    # end def update_timer
    def connect(self, server=None, port=110):
        
        #// Opens a socket to the specified server. Unless overridden,
        #// port defaults to 110. Returns true on success, false on fail
        #// If MAILSERVER is set, override $server with its value.
        if (not (php_isset(lambda : port))) or (not port):
            port = 110
        # end if
        if (not php_empty(lambda : self.MAILSERVER)):
            server = self.MAILSERVER
        # end if
        if php_empty(lambda : server):
            self.ERROR = "POP3 connect: " + _("No server specified")
            self.FP = None
            return False
        # end if
        fp = php_no_error(lambda: fsockopen(str(server), port, errno, errstr))
        if (not fp):
            self.ERROR = "POP3 connect: " + _("Error ") + str("[") + str(errno) + str("] [") + str(errstr) + str("]")
            self.FP = None
            return False
        # end if
        socket_set_blocking(fp, -1)
        self.update_timer()
        reply = php_fgets(fp, self.BUFFER)
        reply = self.strip_clf(reply)
        if self.DEBUG:
            php_error_log(str("POP3 SEND [connect: ") + str(server) + str("] GOT [") + str(reply) + str("]"), 0)
        # end if
        if (not self.is_ok(reply)):
            self.ERROR = "POP3 connect: " + _("Error ") + str("[") + str(reply) + str("]")
            self.FP = None
            return False
        # end if
        self.FP = fp
        self.BANNER = self.parse_banner(reply)
        return True
    # end def connect
    def user(self, user=""):
        
        #// Sends the USER command, returns true or false
        if php_empty(lambda : user):
            self.ERROR = "POP3 user: " + _("no login ID submitted")
            return False
        elif (not (php_isset(lambda : self.FP))):
            self.ERROR = "POP3 user: " + _("connection not established")
            return False
        else:
            reply = self.send_cmd(str("USER ") + str(user))
            if (not self.is_ok(reply)):
                self.ERROR = "POP3 user: " + _("Error ") + str("[") + str(reply) + str("]")
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
            reply = self.send_cmd(str("PASS ") + str(pass_))
            if (not self.is_ok(reply)):
                self.ERROR = "POP3 pass: " + _("Authentication failed") + str(" [") + str(reply) + str("]")
                self.quit()
                return False
            else:
                #// Auth successful.
                count = self.last("count")
                self.COUNT = count
                return count
            # end if
        # end if
    # end def pass_
    def apop(self, login=None, pass_=None):
        
        #// Attempts an APOP login. If this fails, it'll
        #// try a standard login. YOUR SERVER MUST SUPPORT
        #// THE USE OF THE APOP COMMAND!
        #// (apop is optional per rfc1939)
        if (not (php_isset(lambda : self.FP))):
            self.ERROR = "POP3 apop: " + _("No connection to server")
            return False
        elif (not self.ALLOWAPOP):
            retVal = self.login(login, pass_)
            return retVal
        elif php_empty(lambda : login):
            self.ERROR = "POP3 apop: " + _("No login ID submitted")
            return False
        elif php_empty(lambda : pass_):
            self.ERROR = "POP3 apop: " + _("No password submitted")
            return False
        else:
            banner = self.BANNER
            if (not banner) or php_empty(lambda : banner):
                self.ERROR = "POP3 apop: " + _("No server banner") + " - " + _("abort")
                retVal = self.login(login, pass_)
                return retVal
            else:
                AuthString = banner
                AuthString += pass_
                APOPString = php_md5(AuthString)
                cmd = str("APOP ") + str(login) + str(" ") + str(APOPString)
                reply = self.send_cmd(cmd)
                if (not self.is_ok(reply)):
                    self.ERROR = "POP3 apop: " + _("apop authentication failed") + " - " + _("abort")
                    retVal = self.login(login, pass_)
                    return retVal
                else:
                    #// Auth successful.
                    count = self.last("count")
                    self.COUNT = count
                    return count
                # end if
            # end if
        # end if
    # end def apop
    def login(self, login="", pass_=""):
        
        #// Sends both user and pass. Returns # of msgs in mailbox or
        #// false on failure (or -1, if the error occurs while getting
        #// the number of messages.)
        if (not (php_isset(lambda : self.FP))):
            self.ERROR = "POP3 login: " + _("No connection to server")
            return False
        else:
            fp = self.FP
            if (not self.user(login)):
                #// Preserve the error generated by user()
                return False
            else:
                count = self.pass_(pass_)
                if (not count) or count == -1:
                    #// Preserve the error generated by last() and pass()
                    return False
                else:
                    return count
                # end if
            # end if
        # end if
    # end def login
    def top(self, msgNum=None, numLines="0"):
        
        #// Gets the header and first $numLines of the msg body
        #// returns data in an array with each returned line being
        #// an array element. If $numLines is empty, returns
        #// only the header information, and none of the body.
        if (not (php_isset(lambda : self.FP))):
            self.ERROR = "POP3 top: " + _("No connection to server")
            return False
        # end if
        self.update_timer()
        fp = self.FP
        buffer = self.BUFFER
        cmd = str("TOP ") + str(msgNum) + str(" ") + str(numLines)
        fwrite(fp, str("TOP ") + str(msgNum) + str(" ") + str(numLines) + str("\r\n"))
        reply = php_fgets(fp, buffer)
        reply = self.strip_clf(reply)
        if self.DEBUG:
            php_no_error(lambda: php_error_log(str("POP3 SEND [") + str(cmd) + str("] GOT [") + str(reply) + str("]"), 0))
        # end if
        if (not self.is_ok(reply)):
            self.ERROR = "POP3 top: " + _("Error ") + str("[") + str(reply) + str("]")
            return False
        # end if
        count = 0
        MsgArray = Array()
        line = php_fgets(fp, buffer)
        while True:
            
            if not ((not php_preg_match("/^\\.\\r\\n/", line))):
                break
            # end if
            MsgArray[count] = line
            count += 1
            line = php_fgets(fp, buffer)
            if php_empty(lambda : line):
                break
            # end if
        # end while
        return MsgArray
    # end def top
    def pop_list(self, msgNum=""):
        
        #// If called with an argument, returns that msgs' size in octets
        #// No argument returns an associative array of undeleted
        #// msg numbers and their sizes in octets
        if (not (php_isset(lambda : self.FP))):
            self.ERROR = "POP3 pop_list: " + _("No connection to server")
            return False
        # end if
        fp = self.FP
        Total = self.COUNT
        if (not Total) or Total == -1:
            return False
        # end if
        if Total == 0:
            return Array("0", "0")
            pass
        # end if
        self.update_timer()
        if (not php_empty(lambda : msgNum)):
            cmd = str("LIST ") + str(msgNum)
            fwrite(fp, str(cmd) + str("\r\n"))
            reply = php_fgets(fp, self.BUFFER)
            reply = self.strip_clf(reply)
            if self.DEBUG:
                php_no_error(lambda: php_error_log(str("POP3 SEND [") + str(cmd) + str("] GOT [") + str(reply) + str("]"), 0))
            # end if
            if (not self.is_ok(reply)):
                self.ERROR = "POP3 pop_list: " + _("Error ") + str("[") + str(reply) + str("]")
                return False
            # end if
            junk, num, size = php_preg_split("/\\s+/", reply)
            return size
        # end if
        cmd = "LIST"
        reply = self.send_cmd(cmd)
        if (not self.is_ok(reply)):
            reply = self.strip_clf(reply)
            self.ERROR = "POP3 pop_list: " + _("Error ") + str("[") + str(reply) + str("]")
            return False
        # end if
        MsgArray = Array()
        MsgArray[0] = Total
        msgC = 1
        while msgC <= Total:
            
            if msgC > Total:
                break
            # end if
            line = php_fgets(fp, self.BUFFER)
            line = self.strip_clf(line)
            if php_strpos(line, ".") == 0:
                self.ERROR = "POP3 pop_list: " + _("Premature end of list")
                return False
            # end if
            thisMsg, msgSize = php_preg_split("/\\s+/", line)
            settype(thisMsg, "integer")
            if thisMsg != msgC:
                MsgArray[msgC] = "deleted"
            else:
                MsgArray[msgC] = msgSize
            # end if
            msgC += 1
        # end while
        return MsgArray
    # end def pop_list
    def get(self, msgNum=None):
        
        #// Retrieve the specified msg number. Returns an array
        #// where each line of the msg is an array element.
        if (not (php_isset(lambda : self.FP))):
            self.ERROR = "POP3 get: " + _("No connection to server")
            return False
        # end if
        self.update_timer()
        fp = self.FP
        buffer = self.BUFFER
        cmd = str("RETR ") + str(msgNum)
        reply = self.send_cmd(cmd)
        if (not self.is_ok(reply)):
            self.ERROR = "POP3 get: " + _("Error ") + str("[") + str(reply) + str("]")
            return False
        # end if
        count = 0
        MsgArray = Array()
        line = php_fgets(fp, buffer)
        while True:
            
            if not ((not php_preg_match("/^\\.\\r\\n/", line))):
                break
            # end if
            if line[0] == ".":
                line = php_substr(line, 1)
            # end if
            MsgArray[count] = line
            count += 1
            line = php_fgets(fp, buffer)
            if php_empty(lambda : line):
                break
            # end if
        # end while
        return MsgArray
    # end def get
    def last(self, type="count"):
        
        #// Returns the highest msg number in the mailbox.
        #// returns -1 on error, 0+ on success, if type != count
        #// results in a popstat() call (2 element array returned)
        last = -1
        if (not (php_isset(lambda : self.FP))):
            self.ERROR = "POP3 last: " + _("No connection to server")
            return last
        # end if
        reply = self.send_cmd("STAT")
        if (not self.is_ok(reply)):
            self.ERROR = "POP3 last: " + _("Error ") + str("[") + str(reply) + str("]")
            return last
        # end if
        Vars = php_preg_split("/\\s+/", reply)
        count = Vars[1]
        size = Vars[2]
        settype(count, "integer")
        settype(size, "integer")
        if type != "count":
            return Array(count, size)
        # end if
        return count
    # end def last
    def reset(self):
        
        #// Resets the status of the remote server. This includes
        #// resetting the status of ALL msgs to not be deleted.
        #// This method automatically closes the connection to the server.
        if (not (php_isset(lambda : self.FP))):
            self.ERROR = "POP3 reset: " + _("No connection to server")
            return False
        # end if
        reply = self.send_cmd("RSET")
        if (not self.is_ok(reply)):
            #// The POP3 RSET command -never- gives a -ERR
            #// response - if it ever does, something truly
            #// wild is going on.
            self.ERROR = "POP3 reset: " + _("Error ") + str("[") + str(reply) + str("]")
            php_no_error(lambda: php_error_log(str("POP3 reset: ERROR [") + str(reply) + str("]"), 0))
        # end if
        self.quit()
        return True
    # end def reset
    def send_cmd(self, cmd=""):
        
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
        if php_empty(lambda : cmd):
            self.ERROR = "POP3 send_cmd: " + _("Empty command string")
            return ""
        # end if
        fp = self.FP
        buffer = self.BUFFER
        self.update_timer()
        fwrite(fp, str(cmd) + str("\r\n"))
        reply = php_fgets(fp, buffer)
        reply = self.strip_clf(reply)
        if self.DEBUG:
            php_no_error(lambda: php_error_log(str("POP3 SEND [") + str(cmd) + str("] GOT [") + str(reply) + str("]"), 0))
        # end if
        return reply
    # end def send_cmd
    def quit(self):
        
        #// Closes the connection to the POP3 server, deleting
        #// any msgs marked as deleted.
        if (not (php_isset(lambda : self.FP))):
            self.ERROR = "POP3 quit: " + _("connection does not exist")
            return False
        # end if
        fp = self.FP
        cmd = "QUIT"
        fwrite(fp, str(cmd) + str("\r\n"))
        reply = php_fgets(fp, self.BUFFER)
        reply = self.strip_clf(reply)
        if self.DEBUG:
            php_no_error(lambda: php_error_log(str("POP3 SEND [") + str(cmd) + str("] GOT [") + str(reply) + str("]"), 0))
        # end if
        php_fclose(fp)
        self.FP = None
        return True
    # end def quit
    def popstat(self):
        
        #// Returns an array of 2 elements. The number of undeleted
        #// msgs in the mailbox, and the size of the mbox in octets.
        PopArray = self.last("array")
        if PopArray == -1:
            return False
        # end if
        if (not PopArray) or php_empty(lambda : PopArray):
            return False
        # end if
        return PopArray
    # end def popstat
    def uidl(self, msgNum=""):
        
        #// Returns the UIDL of the msg specified. If called with
        #// no arguments, returns an associative array where each
        #// undeleted msg num is a key, and the msg's uidl is the element
        #// Array element 0 will contain the total number of msgs
        if (not (php_isset(lambda : self.FP))):
            self.ERROR = "POP3 uidl: " + _("No connection to server")
            return False
        # end if
        fp = self.FP
        buffer = self.BUFFER
        if (not php_empty(lambda : msgNum)):
            cmd = str("UIDL ") + str(msgNum)
            reply = self.send_cmd(cmd)
            if (not self.is_ok(reply)):
                self.ERROR = "POP3 uidl: " + _("Error ") + str("[") + str(reply) + str("]")
                return False
            # end if
            ok, num, myUidl = php_preg_split("/\\s+/", reply)
            return myUidl
        else:
            self.update_timer()
            UIDLArray = Array()
            Total = self.COUNT
            UIDLArray[0] = Total
            if Total < 1:
                return UIDLArray
            # end if
            cmd = "UIDL"
            fwrite(fp, "UIDL\r\n")
            reply = php_fgets(fp, buffer)
            reply = self.strip_clf(reply)
            if self.DEBUG:
                php_no_error(lambda: php_error_log(str("POP3 SEND [") + str(cmd) + str("] GOT [") + str(reply) + str("]"), 0))
            # end if
            if (not self.is_ok(reply)):
                self.ERROR = "POP3 uidl: " + _("Error ") + str("[") + str(reply) + str("]")
                return False
            # end if
            line = ""
            count = 1
            line = php_fgets(fp, buffer)
            while True:
                
                if not ((not php_preg_match("/^\\.\\r\\n/", line))):
                    break
                # end if
                msg, msgUidl = php_preg_split("/\\s+/", line)
                msgUidl = self.strip_clf(msgUidl)
                if count == msg:
                    UIDLArray[msg] = msgUidl
                else:
                    UIDLArray[count] = "deleted"
                # end if
                count += 1
                line = php_fgets(fp, buffer)
            # end while
        # end if
        return UIDLArray
    # end def uidl
    def delete(self, msgNum=""):
        
        #// Flags a specified msg as deleted. The msg will not
        #// be deleted until a quit() method is called.
        if (not (php_isset(lambda : self.FP))):
            self.ERROR = "POP3 delete: " + _("No connection to server")
            return False
        # end if
        if php_empty(lambda : msgNum):
            self.ERROR = "POP3 delete: " + _("No msg number submitted")
            return False
        # end if
        reply = self.send_cmd(str("DELE ") + str(msgNum))
        if (not self.is_ok(reply)):
            self.ERROR = "POP3 delete: " + _("Command failed ") + str("[") + str(reply) + str("]")
            return False
        # end if
        return True
    # end def delete
    #// 
    #// The following methods are internal to the class.
    def is_ok(self, cmd=""):
        
        #// Return true or false on +OK or -ERR
        if php_empty(lambda : cmd):
            return False
        else:
            return php_stripos(cmd, "+OK") != False
        # end if
    # end def is_ok
    def strip_clf(self, text=""):
        
        #// Strips \r\n from server responses
        if php_empty(lambda : text):
            return text
        else:
            stripped = php_str_replace(Array("\r", "\n"), "", text)
            return stripped
        # end if
    # end def strip_clf
    def parse_banner(self, server_text=None):
        
        outside = True
        banner = ""
        length = php_strlen(server_text)
        count = 0
        while count < length:
            
            digit = php_substr(server_text, count, 1)
            if (not php_empty(lambda : digit)):
                if (not outside) and digit != "<" and digit != ">":
                    banner += digit
                # end if
                if digit == "<":
                    outside = False
                # end if
                if digit == ">":
                    outside = True
                # end if
            # end if
            count += 1
        # end while
        banner = self.strip_clf(banner)
        #// Just in case
        return str("<") + str(banner) + str(">")
    # end def parse_banner
# end class POP3
#// End class
#// For php4 compatibility
if (not php_function_exists("stripos")):
    def stripos(haystack=None, needle=None, *args_):
        
        return php_strpos(haystack, php_stristr(haystack, needle))
    # end def stripos
# end if
