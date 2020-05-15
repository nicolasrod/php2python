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
#// PemFTP - An Ftp implementation in pure PHP
#// 
#// @package PemFTP
#// @since 2.5.0
#// 
#// @version 1.0
#// @copyright Alexey Dotsenko
#// @author Alexey Dotsenko
#// @link https://www.phpclasses.org/package/1743-PHP-FTP-client-in-pure-PHP.html
#// @license LGPL https://opensource.org/licenses/lgpl-license.html
#// 
#// 
#// Defines the newline characters, if not defined already.
#// 
#// This can be redefined.
#// 
#// @since 2.5.0
#// @var string
#//
if (not php_defined("CRLF")):
    php_define("CRLF", "\r\n")
# end if
#// 
#// Sets whatever to autodetect ASCII mode.
#// 
#// This can be redefined.
#// 
#// @since 2.5.0
#// @var int
#//
if (not php_defined("FTP_AUTOASCII")):
    php_define("FTP_AUTOASCII", -1)
# end if
#// 
#// 
#// This can be redefined.
#// @since 2.5.0
#// @var int
#//
if (not php_defined("FTP_BINARY")):
    php_define("FTP_BINARY", 1)
# end if
#// 
#// 
#// This can be redefined.
#// @since 2.5.0
#// @var int
#//
if (not php_defined("FTP_ASCII")):
    php_define("FTP_ASCII", 0)
# end if
#// 
#// Whether to force FTP.
#// 
#// This can be redefined.
#// 
#// @since 2.5.0
#// @var bool
#//
if (not php_defined("FTP_FORCE")):
    php_define("FTP_FORCE", True)
# end if
#// 
#// @since 2.5.0
#// @var string
#//
php_define("FTP_OS_Unix", "u")
#// 
#// @since 2.5.0
#// @var string
#//
php_define("FTP_OS_Windows", "w")
#// 
#// @since 2.5.0
#// @var string
#//
php_define("FTP_OS_Mac", "m")
#// 
#// PemFTP base class
#// 
#//
class ftp_base():
    LocalEcho = Array()
    Verbose = Array()
    OS_local = Array()
    OS_remote = Array()
    _lastaction = Array()
    _errors = Array()
    _type = Array()
    _umask = Array()
    _timeout = Array()
    _passive = Array()
    _host = Array()
    _fullhost = Array()
    _port = Array()
    _datahost = Array()
    _dataport = Array()
    _ftp_control_sock = Array()
    _ftp_data_sock = Array()
    _ftp_temp_sock = Array()
    _ftp_buff_size = Array()
    _login = Array()
    _password = Array()
    _connected = Array()
    _ready = Array()
    _code = Array()
    _message = Array()
    _can_restore = Array()
    _port_available = Array()
    _curtype = Array()
    _features = Array()
    _error_array = Array()
    AuthorizedTransferMode = Array()
    OS_FullName = Array()
    _eol_code = Array()
    AutoAsciiExt = Array()
    #// Constructor
    def __init__(self, port_mode=False, verb=False, le=False):
        
        self.LocalEcho = le
        self.Verbose = verb
        self._lastaction = None
        self._error_array = Array()
        self._eol_code = Array({FTP_OS_Unix: "\n", FTP_OS_Mac: "\r", FTP_OS_Windows: "\r\n"})
        self.AuthorizedTransferMode = Array(FTP_AUTOASCII, FTP_ASCII, FTP_BINARY)
        self.OS_FullName = Array({FTP_OS_Unix: "UNIX", FTP_OS_Windows: "WINDOWS", FTP_OS_Mac: "MACOS"})
        self.AutoAsciiExt = Array("ASP", "BAT", "C", "CPP", "CSS", "CSV", "JS", "H", "HTM", "HTML", "SHTML", "INI", "LOG", "PHP3", "PHTML", "PL", "PERL", "SH", "SQL", "TXT")
        self._port_available = port_mode == True
        self.sendmsg("Staring FTP client class" + "" if self._port_available else " without PORT mode support")
        self._connected = False
        self._ready = False
        self._can_restore = False
        self._code = 0
        self._message = ""
        self._ftp_buff_size = 4096
        self._curtype = None
        self.setumask(18)
        self.settype(FTP_AUTOASCII)
        self.settimeout(30)
        self.passive((not self._port_available))
        self._login = "anonymous"
        self._password = "anon@ftp.com"
        self._features = Array()
        self.OS_local = FTP_OS_Unix
        self.OS_remote = FTP_OS_Unix
        self.features = Array()
        if php_strtoupper(php_substr(PHP_OS, 0, 3)) == "WIN":
            self.OS_local = FTP_OS_Windows
        elif php_strtoupper(php_substr(PHP_OS, 0, 3)) == "MAC":
            self.OS_local = FTP_OS_Mac
        # end if
    # end def __init__
    def ftp_base(self, port_mode=False):
        
        self.__init__(port_mode)
    # end def ftp_base
    #// <!-- --------------------------------------------------------------------------------------- -->
    #// <!--       Public functions                                                                  -->
    #// <!-- --------------------------------------------------------------------------------------- -->
    def parselisting(self, line=None):
        
        is_windows = self.OS_remote == FTP_OS_Windows
        if is_windows and php_preg_match("/([0-9]{2})-([0-9]{2})-([0-9]{2}) +([0-9]{2}):([0-9]{2})(AM|PM) +([0-9]+|<DIR>) +(.+)/", line, lucifer):
            b = Array()
            if lucifer[3] < 70:
                lucifer[3] += 2000
            else:
                lucifer[3] += 1900
            # end if
            #// 4digit year fix
            b["isdir"] = lucifer[7] == "<DIR>"
            if b["isdir"]:
                b["type"] = "d"
            else:
                b["type"] = "f"
            # end if
            b["size"] = lucifer[7]
            b["month"] = lucifer[1]
            b["day"] = lucifer[2]
            b["year"] = lucifer[3]
            b["hour"] = lucifer[4]
            b["minute"] = lucifer[5]
            b["time"] = php_no_error(lambda: mktime(lucifer[4] + 12 if strcasecmp(lucifer[6], "PM") == 0 else 0, lucifer[5], 0, lucifer[1], lucifer[2], lucifer[3]))
            b["am/pm"] = lucifer[6]
            b["name"] = lucifer[8]
        else:
            lucifer = php_preg_split("/[ ]/", line, 9, PREG_SPLIT_NO_EMPTY)
            if (not is_windows) and lucifer:
                #// echo $line."\n";
                lcount = php_count(lucifer)
                if lcount < 8:
                    return ""
                # end if
                b = Array()
                b["isdir"] = lucifer[0][0] == "d"
                b["islink"] = lucifer[0][0] == "l"
                if b["isdir"]:
                    b["type"] = "d"
                elif b["islink"]:
                    b["type"] = "l"
                else:
                    b["type"] = "f"
                # end if
                b["perms"] = lucifer[0]
                b["number"] = lucifer[1]
                b["owner"] = lucifer[2]
                b["group"] = lucifer[3]
                b["size"] = lucifer[4]
                if lcount == 8:
                    sscanf(lucifer[5], "%d-%d-%d", b["year"], b["month"], b["day"])
                    sscanf(lucifer[6], "%d:%d", b["hour"], b["minute"])
                    b["time"] = php_no_error(lambda: mktime(b["hour"], b["minute"], 0, b["month"], b["day"], b["year"]))
                    b["name"] = lucifer[7]
                else:
                    b["month"] = lucifer[5]
                    b["day"] = lucifer[6]
                    if php_preg_match("/([0-9]{2}):([0-9]{2})/", lucifer[7], l2):
                        b["year"] = gmdate("Y")
                        b["hour"] = l2[1]
                        b["minute"] = l2[2]
                    else:
                        b["year"] = lucifer[7]
                        b["hour"] = 0
                        b["minute"] = 0
                    # end if
                    b["time"] = strtotime(php_sprintf("%d %s %d %02d:%02d", b["day"], b["month"], b["year"], b["hour"], b["minute"]))
                    b["name"] = lucifer[8]
                # end if
            # end if
        # end if
        return b
    # end def parselisting
    def sendmsg(self, message="", crlf=True):
        
        if self.Verbose:
            php_print(message + CRLF if crlf else "")
            flush()
        # end if
        return True
    # end def sendmsg
    def settype(self, mode=FTP_AUTOASCII):
        
        if (not php_in_array(mode, self.AuthorizedTransferMode)):
            self.sendmsg("Wrong type")
            return False
        # end if
        self._type = mode
        self.sendmsg("Transfer type: " + "binary" if self._type == FTP_BINARY else "ASCII" if self._type == FTP_ASCII else "auto ASCII")
        return True
    # end def settype
    def _settype(self, mode=FTP_ASCII):
        
        if self._ready:
            if mode == FTP_BINARY:
                if self._curtype != FTP_BINARY:
                    if (not self._exec("TYPE I", "SetType")):
                        return False
                    # end if
                    self._curtype = FTP_BINARY
                # end if
            elif self._curtype != FTP_ASCII:
                if (not self._exec("TYPE A", "SetType")):
                    return False
                # end if
                self._curtype = FTP_ASCII
            # end if
        else:
            return False
        # end if
        return True
    # end def _settype
    def passive(self, pasv=None):
        
        if php_is_null(pasv):
            self._passive = (not self._passive)
        else:
            self._passive = pasv
        # end if
        if (not self._port_available) and (not self._passive):
            self.sendmsg("Only passive connections available!")
            self._passive = True
            return False
        # end if
        self.sendmsg("Passive mode " + "on" if self._passive else "off")
        return True
    # end def passive
    def setserver(self, host=None, port=21, reconnect=True):
        
        if (not is_long(port)):
            self.verbose = True
            self.sendmsg("Incorrect port syntax")
            return False
        else:
            ip = php_no_error(lambda: gethostbyname(host))
            dns = php_no_error(lambda: gethostbyaddr(host))
            if (not ip):
                ip = host
            # end if
            if (not dns):
                dns = host
            # end if
            #// Validate the IPAddress PHP4 returns -1 for invalid, PHP5 false
            #// -1 === "255.255.255.255" which is the broadcast address which is also going to be invalid
            ipaslong = ip2long(ip)
            if ipaslong == False or ipaslong == -1:
                self.sendmsg("Wrong host name/address \"" + host + "\"")
                return False
            # end if
            self._host = ip
            self._fullhost = dns
            self._port = port
            self._dataport = port - 1
        # end if
        self.sendmsg("Host \"" + self._fullhost + "(" + self._host + "):" + self._port + "\"")
        if reconnect:
            if self._connected:
                self.sendmsg("Reconnecting")
                if (not self.quit(FTP_FORCE)):
                    return False
                # end if
                if (not self.connect()):
                    return False
                # end if
            # end if
        # end if
        return True
    # end def setserver
    def setumask(self, umask=18):
        
        self._umask = umask
        umask(self._umask)
        self.sendmsg("UMASK 0" + decoct(self._umask))
        return True
    # end def setumask
    def settimeout(self, timeout=30):
        
        self._timeout = timeout
        self.sendmsg("Timeout " + self._timeout)
        if self._connected:
            if (not self._settimeout(self._ftp_control_sock)):
                return False
            # end if
        # end if
        return True
    # end def settimeout
    def connect(self, server=None):
        
        if (not php_empty(lambda : server)):
            if (not self.setserver(server)):
                return False
            # end if
        # end if
        if self._ready:
            return True
        # end if
        self.sendmsg("Local OS : " + self.OS_FullName[self.OS_local])
        self._ftp_control_sock = self._connect(self._host, self._port)
        if (not self._ftp_control_sock):
            self.sendmsg("Error : Cannot connect to remote host \"" + self._fullhost + " :" + self._port + "\"")
            return False
        # end if
        self.sendmsg("Connected to remote host \"" + self._fullhost + ":" + self._port + "\". Waiting for greeting.")
        while True:
            if (not self._readmsg()):
                return False
            # end if
            if (not self._checkcode()):
                return False
            # end if
            self._lastaction = time()
            
            if self._code < 200:
                break
            # end if
        # end while
        self._ready = True
        syst = self.systype()
        if (not syst):
            self.sendmsg("Can't detect remote OS")
        else:
            if php_preg_match("/win|dos|novell/i", syst[0]):
                self.OS_remote = FTP_OS_Windows
            elif php_preg_match("/os/i", syst[0]):
                self.OS_remote = FTP_OS_Mac
            elif php_preg_match("/(li|u)nix/i", syst[0]):
                self.OS_remote = FTP_OS_Unix
            else:
                self.OS_remote = FTP_OS_Mac
            # end if
            self.sendmsg("Remote OS: " + self.OS_FullName[self.OS_remote])
        # end if
        if (not self.features()):
            self.sendmsg("Can't get features list. All supported - disabled")
        else:
            self.sendmsg("Supported features: " + php_implode(", ", php_array_keys(self._features)))
        # end if
        return True
    # end def connect
    def quit(self, force=False):
        
        if self._ready:
            if (not self._exec("QUIT")) and (not force):
                return False
            # end if
            if (not self._checkcode()) and (not force):
                return False
            # end if
            self._ready = False
            self.sendmsg("Session finished")
        # end if
        self._quit()
        return True
    # end def quit
    def login(self, user=None, pass_=None):
        
        if (not php_is_null(user)):
            self._login = user
        else:
            self._login = "anonymous"
        # end if
        if (not php_is_null(pass_)):
            self._password = pass_
        else:
            self._password = "anon@anon.com"
        # end if
        if (not self._exec("USER " + self._login, "login")):
            return False
        # end if
        if (not self._checkcode()):
            return False
        # end if
        if self._code != 230:
            if (not self._exec("PASS " if self._code == 331 else "ACCT " + self._password, "login")):
                return False
            # end if
            if (not self._checkcode()):
                return False
            # end if
        # end if
        self.sendmsg("Authentication succeeded")
        if php_empty(lambda : self._features):
            if (not self.features()):
                self.sendmsg("Can't get features list. All supported - disabled")
            else:
                self.sendmsg("Supported features: " + php_implode(", ", php_array_keys(self._features)))
            # end if
        # end if
        return True
    # end def login
    def pwd(self):
        
        if (not self._exec("PWD", "pwd")):
            return False
        # end if
        if (not self._checkcode()):
            return False
        # end if
        return php_preg_replace("/^[0-9]{3} \"(.+)\".*$/s", "\\1", self._message)
    # end def pwd
    def cdup(self):
        
        if (not self._exec("CDUP", "cdup")):
            return False
        # end if
        if (not self._checkcode()):
            return False
        # end if
        return True
    # end def cdup
    def chdir(self, pathname=None):
        
        if (not self._exec("CWD " + pathname, "chdir")):
            return False
        # end if
        if (not self._checkcode()):
            return False
        # end if
        return True
    # end def chdir
    def rmdir(self, pathname=None):
        
        if (not self._exec("RMD " + pathname, "rmdir")):
            return False
        # end if
        if (not self._checkcode()):
            return False
        # end if
        return True
    # end def rmdir
    def mkdir(self, pathname=None):
        
        if (not self._exec("MKD " + pathname, "mkdir")):
            return False
        # end if
        if (not self._checkcode()):
            return False
        # end if
        return True
    # end def mkdir
    def rename(self, from_=None, to=None):
        
        if (not self._exec("RNFR " + from_, "rename")):
            return False
        # end if
        if (not self._checkcode()):
            return False
        # end if
        if self._code == 350:
            if (not self._exec("RNTO " + to, "rename")):
                return False
            # end if
            if (not self._checkcode()):
                return False
            # end if
        else:
            return False
        # end if
        return True
    # end def rename
    def filesize(self, pathname=None):
        
        if (not (php_isset(lambda : self._features["SIZE"]))):
            self.pusherror("filesize", "not supported by server")
            return False
        # end if
        if (not self._exec("SIZE " + pathname, "filesize")):
            return False
        # end if
        if (not self._checkcode()):
            return False
        # end if
        return php_preg_replace("/^[0-9]{3} ([0-9]+).*$/s", "\\1", self._message)
    # end def filesize
    def abort(self):
        
        if (not self._exec("ABOR", "abort")):
            return False
        # end if
        if (not self._checkcode()):
            if self._code != 426:
                return False
            # end if
            if (not self._readmsg("abort")):
                return False
            # end if
            if (not self._checkcode()):
                return False
            # end if
        # end if
        return True
    # end def abort
    def mdtm(self, pathname=None):
        
        if (not (php_isset(lambda : self._features["MDTM"]))):
            self.pusherror("mdtm", "not supported by server")
            return False
        # end if
        if (not self._exec("MDTM " + pathname, "mdtm")):
            return False
        # end if
        if (not self._checkcode()):
            return False
        # end if
        mdtm = php_preg_replace("/^[0-9]{3} ([0-9]+).*$/s", "\\1", self._message)
        date = sscanf(mdtm, "%4d%2d%2d%2d%2d%2d")
        timestamp = mktime(date[3], date[4], date[5], date[1], date[2], date[0])
        return timestamp
    # end def mdtm
    def systype(self):
        
        if (not self._exec("SYST", "systype")):
            return False
        # end if
        if (not self._checkcode()):
            return False
        # end if
        DATA = php_explode(" ", self._message)
        return Array(DATA[1], DATA[3])
    # end def systype
    def delete(self, pathname=None):
        
        if (not self._exec("DELE " + pathname, "delete")):
            return False
        # end if
        if (not self._checkcode()):
            return False
        # end if
        return True
    # end def delete
    def site(self, command=None, fnction="site"):
        
        if (not self._exec("SITE " + command, fnction)):
            return False
        # end if
        if (not self._checkcode()):
            return False
        # end if
        return True
    # end def site
    def chmod(self, pathname=None, mode=None):
        
        if (not self.site(php_sprintf("CHMOD %o %s", mode, pathname), "chmod")):
            return False
        # end if
        return True
    # end def chmod
    def restore(self, from_=None):
        
        if (not (php_isset(lambda : self._features["REST"]))):
            self.pusherror("restore", "not supported by server")
            return False
        # end if
        if self._curtype != FTP_BINARY:
            self.pusherror("restore", "can't restore in ASCII mode")
            return False
        # end if
        if (not self._exec("REST " + from_, "resore")):
            return False
        # end if
        if (not self._checkcode()):
            return False
        # end if
        return True
    # end def restore
    def features(self):
        
        if (not self._exec("FEAT", "features")):
            return False
        # end if
        if (not self._checkcode()):
            return False
        # end if
        f = php_preg_split("/[" + CRLF + "]+/", php_preg_replace("/[0-9]{3}[ -].*[" + CRLF + "]+/", "", self._message), -1, PREG_SPLIT_NO_EMPTY)
        self._features = Array()
        for k,v in f:
            v = php_explode(" ", php_trim(v))
            self._features[php_array_shift(v)] = v
        # end for
        return True
    # end def features
    def rawlist(self, pathname="", arg=""):
        
        return self._list(" " + arg if arg else "" + " " + pathname if pathname else "", "LIST", "rawlist")
    # end def rawlist
    def nlist(self, pathname="", arg=""):
        
        return self._list(" " + arg if arg else "" + " " + pathname if pathname else "", "NLST", "nlist")
    # end def nlist
    def is_exists(self, pathname=None):
        
        return self.file_exists(pathname)
    # end def is_exists
    def file_exists(self, pathname=None):
        
        exists = True
        if (not self._exec("RNFR " + pathname, "rename")):
            exists = False
        else:
            if (not self._checkcode()):
                exists = False
            # end if
            self.abort()
        # end if
        if exists:
            self.sendmsg("Remote file " + pathname + " exists")
        else:
            self.sendmsg("Remote file " + pathname + " does not exist")
        # end if
        return exists
    # end def file_exists
    def fget(self, fp=None, remotefile=None, rest=0):
        
        if self._can_restore and rest != 0:
            fseek(fp, rest)
        # end if
        pi = pathinfo(remotefile)
        if self._type == FTP_ASCII or self._type == FTP_AUTOASCII and php_in_array(php_strtoupper(pi["extension"]), self.AutoAsciiExt):
            mode = FTP_ASCII
        else:
            mode = FTP_BINARY
        # end if
        if (not self._data_prepare(mode)):
            return False
        # end if
        if self._can_restore and rest != 0:
            self.restore(rest)
        # end if
        if (not self._exec("RETR " + remotefile, "get")):
            self._data_close()
            return False
        # end if
        if (not self._checkcode()):
            self._data_close()
            return False
        # end if
        out = self._data_read(mode, fp)
        self._data_close()
        if (not self._readmsg()):
            return False
        # end if
        if (not self._checkcode()):
            return False
        # end if
        return out
    # end def fget
    def get(self, remotefile=None, localfile=None, rest=0):
        
        if php_is_null(localfile):
            localfile = remotefile
        # end if
        if php_no_error(lambda: php_file_exists(localfile)):
            self.sendmsg("Warning : local file will be overwritten")
        # end if
        fp = php_no_error(lambda: fopen(localfile, "w"))
        if (not fp):
            self.pusherror("get", "can't open local file", "Cannot create \"" + localfile + "\"")
            return False
        # end if
        if self._can_restore and rest != 0:
            fseek(fp, rest)
        # end if
        pi = pathinfo(remotefile)
        if self._type == FTP_ASCII or self._type == FTP_AUTOASCII and php_in_array(php_strtoupper(pi["extension"]), self.AutoAsciiExt):
            mode = FTP_ASCII
        else:
            mode = FTP_BINARY
        # end if
        if (not self._data_prepare(mode)):
            php_fclose(fp)
            return False
        # end if
        if self._can_restore and rest != 0:
            self.restore(rest)
        # end if
        if (not self._exec("RETR " + remotefile, "get")):
            self._data_close()
            php_fclose(fp)
            return False
        # end if
        if (not self._checkcode()):
            self._data_close()
            php_fclose(fp)
            return False
        # end if
        out = self._data_read(mode, fp)
        php_fclose(fp)
        self._data_close()
        if (not self._readmsg()):
            return False
        # end if
        if (not self._checkcode()):
            return False
        # end if
        return out
    # end def get
    def fput(self, remotefile=None, fp=None, rest=0):
        
        if self._can_restore and rest != 0:
            fseek(fp, rest)
        # end if
        pi = pathinfo(remotefile)
        if self._type == FTP_ASCII or self._type == FTP_AUTOASCII and php_in_array(php_strtoupper(pi["extension"]), self.AutoAsciiExt):
            mode = FTP_ASCII
        else:
            mode = FTP_BINARY
        # end if
        if (not self._data_prepare(mode)):
            return False
        # end if
        if self._can_restore and rest != 0:
            self.restore(rest)
        # end if
        if (not self._exec("STOR " + remotefile, "put")):
            self._data_close()
            return False
        # end if
        if (not self._checkcode()):
            self._data_close()
            return False
        # end if
        ret = self._data_write(mode, fp)
        self._data_close()
        if (not self._readmsg()):
            return False
        # end if
        if (not self._checkcode()):
            return False
        # end if
        return ret
    # end def fput
    def put(self, localfile=None, remotefile=None, rest=0):
        
        if php_is_null(remotefile):
            remotefile = localfile
        # end if
        if (not php_file_exists(localfile)):
            self.pusherror("put", "can't open local file", "No such file or directory \"" + localfile + "\"")
            return False
        # end if
        fp = php_no_error(lambda: fopen(localfile, "r"))
        if (not fp):
            self.pusherror("put", "can't open local file", "Cannot read file \"" + localfile + "\"")
            return False
        # end if
        if self._can_restore and rest != 0:
            fseek(fp, rest)
        # end if
        pi = pathinfo(localfile)
        if self._type == FTP_ASCII or self._type == FTP_AUTOASCII and php_in_array(php_strtoupper(pi["extension"]), self.AutoAsciiExt):
            mode = FTP_ASCII
        else:
            mode = FTP_BINARY
        # end if
        if (not self._data_prepare(mode)):
            php_fclose(fp)
            return False
        # end if
        if self._can_restore and rest != 0:
            self.restore(rest)
        # end if
        if (not self._exec("STOR " + remotefile, "put")):
            self._data_close()
            php_fclose(fp)
            return False
        # end if
        if (not self._checkcode()):
            self._data_close()
            php_fclose(fp)
            return False
        # end if
        ret = self._data_write(mode, fp)
        php_fclose(fp)
        self._data_close()
        if (not self._readmsg()):
            return False
        # end if
        if (not self._checkcode()):
            return False
        # end if
        return ret
    # end def put
    def mput(self, local=".", remote=None, continious=False):
        
        local = php_realpath(local)
        if (not php_no_error(lambda: php_file_exists(local))):
            self.pusherror("mput", "can't open local folder", "Cannot stat folder \"" + local + "\"")
            return False
        # end if
        if (not php_is_dir(local)):
            return self.put(local, remote)
        # end if
        if php_empty(lambda : remote):
            remote = "."
        elif (not self.file_exists(remote)) and (not self.mkdir(remote)):
            return False
        # end if
        handle = php_opendir(local)
        if handle:
            list = Array()
            while True:
                file = php_readdir(handle)
                if not (False != file):
                    break
                # end if
                if file != "." and file != "..":
                    list[-1] = file
                # end if
            # end while
            php_closedir(handle)
        else:
            self.pusherror("mput", "can't open local folder", "Cannot read folder \"" + local + "\"")
            return False
        # end if
        if php_empty(lambda : list):
            return True
        # end if
        ret = True
        for el in list:
            if php_is_dir(local + "/" + el):
                t = self.mput(local + "/" + el, remote + "/" + el)
            else:
                t = self.put(local + "/" + el, remote + "/" + el)
            # end if
            if (not t):
                ret = False
                if (not continious):
                    break
                # end if
            # end if
        # end for
        return ret
    # end def mput
    def mget(self, remote=None, local=".", continious=False):
        
        list = self.rawlist(remote, "-lA")
        if list == False:
            self.pusherror("mget", "can't read remote folder list", "Can't read remote folder \"" + remote + "\" contents")
            return False
        # end if
        if php_empty(lambda : list):
            return True
        # end if
        if (not php_no_error(lambda: php_file_exists(local))):
            if (not php_no_error(lambda: mkdir(local))):
                self.pusherror("mget", "can't create local folder", "Cannot create folder \"" + local + "\"")
                return False
            # end if
        # end if
        for k,v in list:
            list[k] = self.parselisting(v)
            if (not list[k]) or list[k]["name"] == "." or list[k]["name"] == "..":
                list[k] = None
            # end if
        # end for
        ret = True
        for el in list:
            if el["type"] == "d":
                if (not self.mget(remote + "/" + el["name"], local + "/" + el["name"], continious)):
                    self.pusherror("mget", "can't copy folder", "Can't copy remote folder \"" + remote + "/" + el["name"] + "\" to local \"" + local + "/" + el["name"] + "\"")
                    ret = False
                    if (not continious):
                        break
                    # end if
                # end if
            else:
                if (not self.get(remote + "/" + el["name"], local + "/" + el["name"])):
                    self.pusherror("mget", "can't copy file", "Can't copy remote file \"" + remote + "/" + el["name"] + "\" to local \"" + local + "/" + el["name"] + "\"")
                    ret = False
                    if (not continious):
                        break
                    # end if
                # end if
            # end if
            php_no_error(lambda: chmod(local + "/" + el["name"], el["perms"]))
            t = strtotime(el["date"])
            if t != -1 and t != False:
                php_no_error(lambda: touch(local + "/" + el["name"], t))
            # end if
        # end for
        return ret
    # end def mget
    def mdel(self, remote=None, continious=False):
        
        list = self.rawlist(remote, "-la")
        if list == False:
            self.pusherror("mdel", "can't read remote folder list", "Can't read remote folder \"" + remote + "\" contents")
            return False
        # end if
        for k,v in list:
            list[k] = self.parselisting(v)
            if (not list[k]) or list[k]["name"] == "." or list[k]["name"] == "..":
                list[k] = None
            # end if
        # end for
        ret = True
        for el in list:
            if php_empty(lambda : el):
                continue
            # end if
            if el["type"] == "d":
                if (not self.mdel(remote + "/" + el["name"], continious)):
                    ret = False
                    if (not continious):
                        break
                    # end if
                # end if
            else:
                if (not self.delete(remote + "/" + el["name"])):
                    self.pusherror("mdel", "can't delete file", "Can't delete remote file \"" + remote + "/" + el["name"] + "\"")
                    ret = False
                    if (not continious):
                        break
                    # end if
                # end if
            # end if
        # end for
        if (not self.rmdir(remote)):
            self.pusherror("mdel", "can't delete folder", "Can't delete remote folder \"" + remote + "/" + el["name"] + "\"")
            ret = False
        # end if
        return ret
    # end def mdel
    def mmkdir(self, dir=None, mode=511):
        
        if php_empty(lambda : dir):
            return False
        # end if
        if self.is_exists(dir) or dir == "/":
            return True
        # end if
        if (not self.mmkdir(php_dirname(dir), mode)):
            return False
        # end if
        r = self.mkdir(dir, mode)
        self.chmod(dir, mode)
        return r
    # end def mmkdir
    def glob(self, pattern=None, handle=None):
        
        path = output = None
        if PHP_OS == "WIN32":
            slash = "\\"
        else:
            slash = "/"
        # end if
        lastpos = php_strrpos(pattern, slash)
        if (not lastpos == False):
            path = php_substr(pattern, 0, -lastpos - 1)
            pattern = php_substr(pattern, lastpos)
        else:
            path = php_getcwd()
        # end if
        if php_is_array(handle) and (not php_empty(lambda : handle)):
            for dir in handle:
                if self.glob_pattern_match(pattern, dir):
                    output[-1] = dir
                # end if
            # end for
        else:
            handle = php_no_error(lambda: php_opendir(path))
            if handle == False:
                return False
            # end if
            while True:
                dir = php_readdir(handle)
                if not (dir):
                    break
                # end if
                if self.glob_pattern_match(pattern, dir):
                    output[-1] = dir
                # end if
            # end while
            php_closedir(handle)
        # end if
        if php_is_array(output):
            return output
        # end if
        return False
    # end def glob
    def glob_pattern_match(self, pattern=None, string=None):
        
        out = None
        chunks = php_explode(";", pattern)
        for pattern in chunks:
            escape = Array("$", "^", ".", "{", "}", "(", ")", "[", "]", "|")
            while True:
                
                if not (php_strpos(pattern, "**") != False):
                    break
                # end if
                pattern = php_str_replace("**", "*", pattern)
            # end while
            for probe in escape:
                pattern = php_str_replace(probe, str("\\") + str(probe), pattern)
            # end for
            pattern = php_str_replace("?*", "*", php_str_replace("*?", "*", php_str_replace("*", ".*", php_str_replace("?", ".{1,1}", pattern))))
            out[-1] = pattern
        # end for
        if php_count(out) == 1:
            return self.glob_regexp(str("^") + str(out[0]) + str("$"), string)
        else:
            for tester in out:
                if self.my_regexp(str("^") + str(tester) + str("$"), string):
                    return True
                # end if
            # end for
        # end if
        return False
    # end def glob_pattern_match
    def glob_regexp(self, pattern=None, probe=None):
        
        sensitive = PHP_OS != "WIN32"
        return php_preg_match("/" + preg_quote(pattern, "/") + "/", probe) if sensitive else php_preg_match("/" + preg_quote(pattern, "/") + "/i", probe)
    # end def glob_regexp
    def dirlist(self, remote=None):
        
        list = self.rawlist(remote, "-la")
        if list == False:
            self.pusherror("dirlist", "can't read remote folder list", "Can't read remote folder \"" + remote + "\" contents")
            return False
        # end if
        dirlist = Array()
        for k,v in list:
            entry = self.parselisting(v)
            if php_empty(lambda : entry):
                continue
            # end if
            if entry["name"] == "." or entry["name"] == "..":
                continue
            # end if
            dirlist[entry["name"]] = entry
        # end for
        return dirlist
    # end def dirlist
    #// <!-- --------------------------------------------------------------------------------------- -->
    #// <!--       Private functions                                                                 -->
    #// <!-- --------------------------------------------------------------------------------------- -->
    def _checkcode(self):
        
        return self._code < 400 and self._code > 0
    # end def _checkcode
    def _list(self, arg="", cmd="LIST", fnction="_list"):
        
        if (not self._data_prepare()):
            return False
        # end if
        if (not self._exec(cmd + arg, fnction)):
            self._data_close()
            return False
        # end if
        if (not self._checkcode()):
            self._data_close()
            return False
        # end if
        out = ""
        if self._code < 200:
            out = self._data_read()
            self._data_close()
            if (not self._readmsg()):
                return False
            # end if
            if (not self._checkcode()):
                return False
            # end if
            if out == False:
                return False
            # end if
            out = php_preg_split("/[" + CRLF + "]+/", out, -1, PREG_SPLIT_NO_EMPTY)
            pass
        # end if
        return out
    # end def _list
    #// <!-- --------------------------------------------------------------------------------------- -->
    #// <!-- Partie : gestion des erreurs                                                            -->
    #// <!-- --------------------------------------------------------------------------------------- -->
    #// Gnre une erreur pour traitement externe  la classe
    def pusherror(self, fctname=None, msg=None, desc=False):
        
        error = Array()
        error["time"] = time()
        error["fctname"] = fctname
        error["msg"] = msg
        error["desc"] = desc
        if desc:
            tmp = " (" + desc + ")"
        else:
            tmp = ""
        # end if
        self.sendmsg(fctname + ": " + msg + tmp)
        return php_array_push(self._error_array, error)
    # end def pusherror
    #// Rcupre une erreur externe
    def poperror(self):
        
        if php_count(self._error_array):
            return php_array_pop(self._error_array)
        else:
            return False
        # end if
    # end def poperror
# end class ftp_base
mod_sockets = php_extension_loaded("sockets")
if (not mod_sockets) and php_function_exists("dl") and php_is_callable("dl"):
    prefix = "php_" if PHP_SHLIB_SUFFIX == "dll" else ""
    php_no_error(lambda: php_dl(prefix + "sockets." + PHP_SHLIB_SUFFIX))
    mod_sockets = php_extension_loaded("sockets")
# end if
php_include_file(__DIR__ + "/class-ftp-" + "sockets" if mod_sockets else "pure" + ".php", once=True)
if mod_sockets:
    class ftp(ftp_sockets):
        pass
    # end class ftp
else:
    class ftp(ftp_pure):
        pass
    # end class ftp
# end if
