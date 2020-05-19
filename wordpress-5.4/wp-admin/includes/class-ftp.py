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
    #// Public variables
    LocalEcho = Array()
    Verbose = Array()
    OS_local = Array()
    OS_remote = Array()
    #// Private variables
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
    def __init__(self, port_mode_=None, verb_=None, le_=None):
        if port_mode_ is None:
            port_mode_ = False
        # end if
        if verb_ is None:
            verb_ = False
        # end if
        if le_ is None:
            le_ = False
        # end if
        
        self.LocalEcho = le_
        self.Verbose = verb_
        self._lastaction = None
        self._error_array = Array()
        self._eol_code = Array({FTP_OS_Unix: "\n", FTP_OS_Mac: "\r", FTP_OS_Windows: "\r\n"})
        self.AuthorizedTransferMode = Array(FTP_AUTOASCII, FTP_ASCII, FTP_BINARY)
        self.OS_FullName = Array({FTP_OS_Unix: "UNIX", FTP_OS_Windows: "WINDOWS", FTP_OS_Mac: "MACOS"})
        self.AutoAsciiExt = Array("ASP", "BAT", "C", "CPP", "CSS", "CSV", "JS", "H", "HTM", "HTML", "SHTML", "INI", "LOG", "PHP3", "PHTML", "PL", "PERL", "SH", "SQL", "TXT")
        self._port_available = port_mode_ == True
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
    def ftp_base(self, port_mode_=None):
        if port_mode_ is None:
            port_mode_ = False
        # end if
        
        self.__init__(port_mode_)
    # end def ftp_base
    #// <!-- --------------------------------------------------------------------------------------- -->
    #// <!--       Public functions                                                                  -->
    #// <!-- --------------------------------------------------------------------------------------- -->
    def parselisting(self, line_=None):
        
        
        is_windows_ = self.OS_remote == FTP_OS_Windows
        if is_windows_ and php_preg_match("/([0-9]{2})-([0-9]{2})-([0-9]{2}) +([0-9]{2}):([0-9]{2})(AM|PM) +([0-9]+|<DIR>) +(.+)/", line_, lucifer_):
            b_ = Array()
            if lucifer_[3] < 70:
                lucifer_[3] += 2000
            else:
                lucifer_[3] += 1900
            # end if
            #// 4digit year fix
            b_["isdir"] = lucifer_[7] == "<DIR>"
            if b_["isdir"]:
                b_["type"] = "d"
            else:
                b_["type"] = "f"
            # end if
            b_["size"] = lucifer_[7]
            b_["month"] = lucifer_[1]
            b_["day"] = lucifer_[2]
            b_["year"] = lucifer_[3]
            b_["hour"] = lucifer_[4]
            b_["minute"] = lucifer_[5]
            b_["time"] = php_no_error(lambda: mktime(lucifer_[4] + 12 if strcasecmp(lucifer_[6], "PM") == 0 else 0, lucifer_[5], 0, lucifer_[1], lucifer_[2], lucifer_[3]))
            b_["am/pm"] = lucifer_[6]
            b_["name"] = lucifer_[8]
        else:
            lucifer_ = php_preg_split("/[ ]/", line_, 9, PREG_SPLIT_NO_EMPTY)
            if (not is_windows_) and lucifer_:
                #// echo $line."\n";
                lcount_ = php_count(lucifer_)
                if lcount_ < 8:
                    return ""
                # end if
                b_ = Array()
                b_["isdir"] = lucifer_[0][0] == "d"
                b_["islink"] = lucifer_[0][0] == "l"
                if b_["isdir"]:
                    b_["type"] = "d"
                elif b_["islink"]:
                    b_["type"] = "l"
                else:
                    b_["type"] = "f"
                # end if
                b_["perms"] = lucifer_[0]
                b_["number"] = lucifer_[1]
                b_["owner"] = lucifer_[2]
                b_["group"] = lucifer_[3]
                b_["size"] = lucifer_[4]
                if lcount_ == 8:
                    sscanf(lucifer_[5], "%d-%d-%d", b_["year"], b_["month"], b_["day"])
                    sscanf(lucifer_[6], "%d:%d", b_["hour"], b_["minute"])
                    b_["time"] = php_no_error(lambda: mktime(b_["hour"], b_["minute"], 0, b_["month"], b_["day"], b_["year"]))
                    b_["name"] = lucifer_[7]
                else:
                    b_["month"] = lucifer_[5]
                    b_["day"] = lucifer_[6]
                    if php_preg_match("/([0-9]{2}):([0-9]{2})/", lucifer_[7], l2_):
                        b_["year"] = gmdate("Y")
                        b_["hour"] = l2_[1]
                        b_["minute"] = l2_[2]
                    else:
                        b_["year"] = lucifer_[7]
                        b_["hour"] = 0
                        b_["minute"] = 0
                    # end if
                    b_["time"] = strtotime(php_sprintf("%d %s %d %02d:%02d", b_["day"], b_["month"], b_["year"], b_["hour"], b_["minute"]))
                    b_["name"] = lucifer_[8]
                # end if
            # end if
        # end if
        return b_
    # end def parselisting
    def sendmsg(self, message_="", crlf_=None):
        if crlf_ is None:
            crlf_ = True
        # end if
        
        if self.Verbose:
            php_print(message_ + CRLF if crlf_ else "")
            flush()
        # end if
        return True
    # end def sendmsg
    def settype(self, mode_=None):
        if mode_ is None:
            mode_ = FTP_AUTOASCII
        # end if
        
        if (not php_in_array(mode_, self.AuthorizedTransferMode)):
            self.sendmsg("Wrong type")
            return False
        # end if
        self._type = mode_
        self.sendmsg("Transfer type: " + "binary" if self._type == FTP_BINARY else "ASCII" if self._type == FTP_ASCII else "auto ASCII")
        return True
    # end def settype
    def _settype(self, mode_=None):
        if mode_ is None:
            mode_ = FTP_ASCII
        # end if
        
        if self._ready:
            if mode_ == FTP_BINARY:
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
    def passive(self, pasv_=None):
        if pasv_ is None:
            pasv_ = None
        # end if
        
        if php_is_null(pasv_):
            self._passive = (not self._passive)
        else:
            self._passive = pasv_
        # end if
        if (not self._port_available) and (not self._passive):
            self.sendmsg("Only passive connections available!")
            self._passive = True
            return False
        # end if
        self.sendmsg("Passive mode " + "on" if self._passive else "off")
        return True
    # end def passive
    def setserver(self, host_=None, port_=21, reconnect_=None):
        if reconnect_ is None:
            reconnect_ = True
        # end if
        
        if (not is_long(port_)):
            self.verbose = True
            self.sendmsg("Incorrect port syntax")
            return False
        else:
            ip_ = php_no_error(lambda: gethostbyname(host_))
            dns_ = php_no_error(lambda: gethostbyaddr(host_))
            if (not ip_):
                ip_ = host_
            # end if
            if (not dns_):
                dns_ = host_
            # end if
            #// Validate the IPAddress PHP4 returns -1 for invalid, PHP5 false
            #// -1 === "255.255.255.255" which is the broadcast address which is also going to be invalid
            ipaslong_ = ip2long(ip_)
            if ipaslong_ == False or ipaslong_ == -1:
                self.sendmsg("Wrong host name/address \"" + host_ + "\"")
                return False
            # end if
            self._host = ip_
            self._fullhost = dns_
            self._port = port_
            self._dataport = port_ - 1
        # end if
        self.sendmsg("Host \"" + self._fullhost + "(" + self._host + "):" + self._port + "\"")
        if reconnect_:
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
    def setumask(self, umask_=18):
        
        
        self._umask = umask_
        umask(self._umask)
        self.sendmsg("UMASK 0" + decoct(self._umask))
        return True
    # end def setumask
    def settimeout(self, timeout_=30):
        
        
        self._timeout = timeout_
        self.sendmsg("Timeout " + self._timeout)
        if self._connected:
            if (not self._settimeout(self._ftp_control_sock)):
                return False
            # end if
        # end if
        return True
    # end def settimeout
    def connect(self, server_=None):
        if server_ is None:
            server_ = None
        # end if
        
        if (not php_empty(lambda : server_)):
            if (not self.setserver(server_)):
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
        syst_ = self.systype()
        if (not syst_):
            self.sendmsg("Can't detect remote OS")
        else:
            if php_preg_match("/win|dos|novell/i", syst_[0]):
                self.OS_remote = FTP_OS_Windows
            elif php_preg_match("/os/i", syst_[0]):
                self.OS_remote = FTP_OS_Mac
            elif php_preg_match("/(li|u)nix/i", syst_[0]):
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
    def quit(self, force_=None):
        if force_ is None:
            force_ = False
        # end if
        
        if self._ready:
            if (not self._exec("QUIT")) and (not force_):
                return False
            # end if
            if (not self._checkcode()) and (not force_):
                return False
            # end if
            self._ready = False
            self.sendmsg("Session finished")
        # end if
        self._quit()
        return True
    # end def quit
    def login(self, user_=None, pass_=None):
        if user_ is None:
            user_ = None
        # end if
        if pass_ is None:
            pass_ = None
        # end if
        
        if (not php_is_null(user_)):
            self._login = user_
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
    def chdir(self, pathname_=None):
        
        
        if (not self._exec("CWD " + pathname_, "chdir")):
            return False
        # end if
        if (not self._checkcode()):
            return False
        # end if
        return True
    # end def chdir
    def rmdir(self, pathname_=None):
        
        
        if (not self._exec("RMD " + pathname_, "rmdir")):
            return False
        # end if
        if (not self._checkcode()):
            return False
        # end if
        return True
    # end def rmdir
    def mkdir(self, pathname_=None):
        
        
        if (not self._exec("MKD " + pathname_, "mkdir")):
            return False
        # end if
        if (not self._checkcode()):
            return False
        # end if
        return True
    # end def mkdir
    def rename(self, from_=None, to_=None):
        
        
        if (not self._exec("RNFR " + from_, "rename")):
            return False
        # end if
        if (not self._checkcode()):
            return False
        # end if
        if self._code == 350:
            if (not self._exec("RNTO " + to_, "rename")):
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
    def filesize(self, pathname_=None):
        
        
        if (not (php_isset(lambda : self._features["SIZE"]))):
            self.pusherror("filesize", "not supported by server")
            return False
        # end if
        if (not self._exec("SIZE " + pathname_, "filesize")):
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
    def mdtm(self, pathname_=None):
        
        
        if (not (php_isset(lambda : self._features["MDTM"]))):
            self.pusherror("mdtm", "not supported by server")
            return False
        # end if
        if (not self._exec("MDTM " + pathname_, "mdtm")):
            return False
        # end if
        if (not self._checkcode()):
            return False
        # end if
        mdtm_ = php_preg_replace("/^[0-9]{3} ([0-9]+).*$/s", "\\1", self._message)
        date_ = sscanf(mdtm_, "%4d%2d%2d%2d%2d%2d")
        timestamp_ = mktime(date_[3], date_[4], date_[5], date_[1], date_[2], date_[0])
        return timestamp_
    # end def mdtm
    def systype(self):
        
        
        if (not self._exec("SYST", "systype")):
            return False
        # end if
        if (not self._checkcode()):
            return False
        # end if
        DATA_ = php_explode(" ", self._message)
        return Array(DATA_[1], DATA_[3])
    # end def systype
    def delete(self, pathname_=None):
        
        
        if (not self._exec("DELE " + pathname_, "delete")):
            return False
        # end if
        if (not self._checkcode()):
            return False
        # end if
        return True
    # end def delete
    def site(self, command_=None, fnction_="site"):
        
        
        if (not self._exec("SITE " + command_, fnction_)):
            return False
        # end if
        if (not self._checkcode()):
            return False
        # end if
        return True
    # end def site
    def chmod(self, pathname_=None, mode_=None):
        
        
        if (not self.site(php_sprintf("CHMOD %o %s", mode_, pathname_), "chmod")):
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
        f_ = php_preg_split("/[" + CRLF + "]+/", php_preg_replace("/[0-9]{3}[ -].*[" + CRLF + "]+/", "", self._message), -1, PREG_SPLIT_NO_EMPTY)
        self._features = Array()
        for k_,v_ in f_.items():
            v_ = php_explode(" ", php_trim(v_))
            self._features[php_array_shift(v_)] = v_
        # end for
        return True
    # end def features
    def rawlist(self, pathname_="", arg_=""):
        
        
        return self._list(" " + arg_ if arg_ else "" + " " + pathname_ if pathname_ else "", "LIST", "rawlist")
    # end def rawlist
    def nlist(self, pathname_="", arg_=""):
        
        
        return self._list(" " + arg_ if arg_ else "" + " " + pathname_ if pathname_ else "", "NLST", "nlist")
    # end def nlist
    def is_exists(self, pathname_=None):
        
        
        return self.file_exists(pathname_)
    # end def is_exists
    def file_exists(self, pathname_=None):
        
        
        exists_ = True
        if (not self._exec("RNFR " + pathname_, "rename")):
            exists_ = False
        else:
            if (not self._checkcode()):
                exists_ = False
            # end if
            self.abort()
        # end if
        if exists_:
            self.sendmsg("Remote file " + pathname_ + " exists")
        else:
            self.sendmsg("Remote file " + pathname_ + " does not exist")
        # end if
        return exists_
    # end def file_exists
    def fget(self, fp_=None, remotefile_=None, rest_=0):
        
        
        if self._can_restore and rest_ != 0:
            fseek(fp_, rest_)
        # end if
        pi_ = pathinfo(remotefile_)
        if self._type == FTP_ASCII or self._type == FTP_AUTOASCII and php_in_array(php_strtoupper(pi_["extension"]), self.AutoAsciiExt):
            mode_ = FTP_ASCII
        else:
            mode_ = FTP_BINARY
        # end if
        if (not self._data_prepare(mode_)):
            return False
        # end if
        if self._can_restore and rest_ != 0:
            self.restore(rest_)
        # end if
        if (not self._exec("RETR " + remotefile_, "get")):
            self._data_close()
            return False
        # end if
        if (not self._checkcode()):
            self._data_close()
            return False
        # end if
        out_ = self._data_read(mode_, fp_)
        self._data_close()
        if (not self._readmsg()):
            return False
        # end if
        if (not self._checkcode()):
            return False
        # end if
        return out_
    # end def fget
    def get(self, remotefile_=None, localfile_=None, rest_=0):
        if localfile_ is None:
            localfile_ = None
        # end if
        
        if php_is_null(localfile_):
            localfile_ = remotefile_
        # end if
        if php_no_error(lambda: php_file_exists(localfile_)):
            self.sendmsg("Warning : local file will be overwritten")
        # end if
        fp_ = php_no_error(lambda: fopen(localfile_, "w"))
        if (not fp_):
            self.pusherror("get", "can't open local file", "Cannot create \"" + localfile_ + "\"")
            return False
        # end if
        if self._can_restore and rest_ != 0:
            fseek(fp_, rest_)
        # end if
        pi_ = pathinfo(remotefile_)
        if self._type == FTP_ASCII or self._type == FTP_AUTOASCII and php_in_array(php_strtoupper(pi_["extension"]), self.AutoAsciiExt):
            mode_ = FTP_ASCII
        else:
            mode_ = FTP_BINARY
        # end if
        if (not self._data_prepare(mode_)):
            php_fclose(fp_)
            return False
        # end if
        if self._can_restore and rest_ != 0:
            self.restore(rest_)
        # end if
        if (not self._exec("RETR " + remotefile_, "get")):
            self._data_close()
            php_fclose(fp_)
            return False
        # end if
        if (not self._checkcode()):
            self._data_close()
            php_fclose(fp_)
            return False
        # end if
        out_ = self._data_read(mode_, fp_)
        php_fclose(fp_)
        self._data_close()
        if (not self._readmsg()):
            return False
        # end if
        if (not self._checkcode()):
            return False
        # end if
        return out_
    # end def get
    def fput(self, remotefile_=None, fp_=None, rest_=0):
        
        
        if self._can_restore and rest_ != 0:
            fseek(fp_, rest_)
        # end if
        pi_ = pathinfo(remotefile_)
        if self._type == FTP_ASCII or self._type == FTP_AUTOASCII and php_in_array(php_strtoupper(pi_["extension"]), self.AutoAsciiExt):
            mode_ = FTP_ASCII
        else:
            mode_ = FTP_BINARY
        # end if
        if (not self._data_prepare(mode_)):
            return False
        # end if
        if self._can_restore and rest_ != 0:
            self.restore(rest_)
        # end if
        if (not self._exec("STOR " + remotefile_, "put")):
            self._data_close()
            return False
        # end if
        if (not self._checkcode()):
            self._data_close()
            return False
        # end if
        ret_ = self._data_write(mode_, fp_)
        self._data_close()
        if (not self._readmsg()):
            return False
        # end if
        if (not self._checkcode()):
            return False
        # end if
        return ret_
    # end def fput
    def put(self, localfile_=None, remotefile_=None, rest_=0):
        if remotefile_ is None:
            remotefile_ = None
        # end if
        
        if php_is_null(remotefile_):
            remotefile_ = localfile_
        # end if
        if (not php_file_exists(localfile_)):
            self.pusherror("put", "can't open local file", "No such file or directory \"" + localfile_ + "\"")
            return False
        # end if
        fp_ = php_no_error(lambda: fopen(localfile_, "r"))
        if (not fp_):
            self.pusherror("put", "can't open local file", "Cannot read file \"" + localfile_ + "\"")
            return False
        # end if
        if self._can_restore and rest_ != 0:
            fseek(fp_, rest_)
        # end if
        pi_ = pathinfo(localfile_)
        if self._type == FTP_ASCII or self._type == FTP_AUTOASCII and php_in_array(php_strtoupper(pi_["extension"]), self.AutoAsciiExt):
            mode_ = FTP_ASCII
        else:
            mode_ = FTP_BINARY
        # end if
        if (not self._data_prepare(mode_)):
            php_fclose(fp_)
            return False
        # end if
        if self._can_restore and rest_ != 0:
            self.restore(rest_)
        # end if
        if (not self._exec("STOR " + remotefile_, "put")):
            self._data_close()
            php_fclose(fp_)
            return False
        # end if
        if (not self._checkcode()):
            self._data_close()
            php_fclose(fp_)
            return False
        # end if
        ret_ = self._data_write(mode_, fp_)
        php_fclose(fp_)
        self._data_close()
        if (not self._readmsg()):
            return False
        # end if
        if (not self._checkcode()):
            return False
        # end if
        return ret_
    # end def put
    def mput(self, local_=".", remote_=None, continious_=None):
        if remote_ is None:
            remote_ = None
        # end if
        if continious_ is None:
            continious_ = False
        # end if
        
        local_ = php_realpath(local_)
        if (not php_no_error(lambda: php_file_exists(local_))):
            self.pusherror("mput", "can't open local folder", "Cannot stat folder \"" + local_ + "\"")
            return False
        # end if
        if (not php_is_dir(local_)):
            return self.put(local_, remote_)
        # end if
        if php_empty(lambda : remote_):
            remote_ = "."
        elif (not self.file_exists(remote_)) and (not self.mkdir(remote_)):
            return False
        # end if
        handle_ = php_opendir(local_)
        if handle_:
            list_ = Array()
            while True:
                file_ = php_readdir(handle_)
                if not (False != file_):
                    break
                # end if
                if file_ != "." and file_ != "..":
                    list_[-1] = file_
                # end if
            # end while
            php_closedir(handle_)
        else:
            self.pusherror("mput", "can't open local folder", "Cannot read folder \"" + local_ + "\"")
            return False
        # end if
        if php_empty(lambda : list_):
            return True
        # end if
        ret_ = True
        for el_ in list_:
            if php_is_dir(local_ + "/" + el_):
                t_ = self.mput(local_ + "/" + el_, remote_ + "/" + el_)
            else:
                t_ = self.put(local_ + "/" + el_, remote_ + "/" + el_)
            # end if
            if (not t_):
                ret_ = False
                if (not continious_):
                    break
                # end if
            # end if
        # end for
        return ret_
    # end def mput
    def mget(self, remote_=None, local_=".", continious_=None):
        if continious_ is None:
            continious_ = False
        # end if
        
        list_ = self.rawlist(remote_, "-lA")
        if list_ == False:
            self.pusherror("mget", "can't read remote folder list", "Can't read remote folder \"" + remote_ + "\" contents")
            return False
        # end if
        if php_empty(lambda : list_):
            return True
        # end if
        if (not php_no_error(lambda: php_file_exists(local_))):
            if (not php_no_error(lambda: mkdir(local_))):
                self.pusherror("mget", "can't create local folder", "Cannot create folder \"" + local_ + "\"")
                return False
            # end if
        # end if
        for k_,v_ in list_.items():
            list_[k_] = self.parselisting(v_)
            if (not list_[k_]) or list_[k_]["name"] == "." or list_[k_]["name"] == "..":
                list_[k_] = None
            # end if
        # end for
        ret_ = True
        for el_ in list_:
            if el_["type"] == "d":
                if (not self.mget(remote_ + "/" + el_["name"], local_ + "/" + el_["name"], continious_)):
                    self.pusherror("mget", "can't copy folder", "Can't copy remote folder \"" + remote_ + "/" + el_["name"] + "\" to local \"" + local_ + "/" + el_["name"] + "\"")
                    ret_ = False
                    if (not continious_):
                        break
                    # end if
                # end if
            else:
                if (not self.get(remote_ + "/" + el_["name"], local_ + "/" + el_["name"])):
                    self.pusherror("mget", "can't copy file", "Can't copy remote file \"" + remote_ + "/" + el_["name"] + "\" to local \"" + local_ + "/" + el_["name"] + "\"")
                    ret_ = False
                    if (not continious_):
                        break
                    # end if
                # end if
            # end if
            php_no_error(lambda: chmod(local_ + "/" + el_["name"], el_["perms"]))
            t_ = strtotime(el_["date"])
            if t_ != -1 and t_ != False:
                php_no_error(lambda: touch(local_ + "/" + el_["name"], t_))
            # end if
        # end for
        return ret_
    # end def mget
    def mdel(self, remote_=None, continious_=None):
        if continious_ is None:
            continious_ = False
        # end if
        
        list_ = self.rawlist(remote_, "-la")
        if list_ == False:
            self.pusherror("mdel", "can't read remote folder list", "Can't read remote folder \"" + remote_ + "\" contents")
            return False
        # end if
        for k_,v_ in list_.items():
            list_[k_] = self.parselisting(v_)
            if (not list_[k_]) or list_[k_]["name"] == "." or list_[k_]["name"] == "..":
                list_[k_] = None
            # end if
        # end for
        ret_ = True
        for el_ in list_:
            if php_empty(lambda : el_):
                continue
            # end if
            if el_["type"] == "d":
                if (not self.mdel(remote_ + "/" + el_["name"], continious_)):
                    ret_ = False
                    if (not continious_):
                        break
                    # end if
                # end if
            else:
                if (not self.delete(remote_ + "/" + el_["name"])):
                    self.pusherror("mdel", "can't delete file", "Can't delete remote file \"" + remote_ + "/" + el_["name"] + "\"")
                    ret_ = False
                    if (not continious_):
                        break
                    # end if
                # end if
            # end if
        # end for
        if (not self.rmdir(remote_)):
            self.pusherror("mdel", "can't delete folder", "Can't delete remote folder \"" + remote_ + "/" + el_["name"] + "\"")
            ret_ = False
        # end if
        return ret_
    # end def mdel
    def mmkdir(self, dir_=None, mode_=511):
        
        
        if php_empty(lambda : dir_):
            return False
        # end if
        if self.is_exists(dir_) or dir_ == "/":
            return True
        # end if
        if (not self.mmkdir(php_dirname(dir_), mode_)):
            return False
        # end if
        r_ = self.mkdir(dir_, mode_)
        self.chmod(dir_, mode_)
        return r_
    # end def mmkdir
    def glob(self, pattern_=None, handle_=None):
        if handle_ is None:
            handle_ = None
        # end if
        
        path_ = output_ = None
        if PHP_OS == "WIN32":
            slash_ = "\\"
        else:
            slash_ = "/"
        # end if
        lastpos_ = php_strrpos(pattern_, slash_)
        if (not lastpos_ == False):
            path_ = php_substr(pattern_, 0, -lastpos_ - 1)
            pattern_ = php_substr(pattern_, lastpos_)
        else:
            path_ = php_getcwd()
        # end if
        if php_is_array(handle_) and (not php_empty(lambda : handle_)):
            for dir_ in handle_:
                if self.glob_pattern_match(pattern_, dir_):
                    output_[-1] = dir_
                # end if
            # end for
        else:
            handle_ = php_no_error(lambda: php_opendir(path_))
            if handle_ == False:
                return False
            # end if
            while True:
                dir_ = php_readdir(handle_)
                if not (dir_):
                    break
                # end if
                if self.glob_pattern_match(pattern_, dir_):
                    output_[-1] = dir_
                # end if
            # end while
            php_closedir(handle_)
        # end if
        if php_is_array(output_):
            return output_
        # end if
        return False
    # end def glob
    def glob_pattern_match(self, pattern_=None, string_=None):
        
        
        out_ = None
        chunks_ = php_explode(";", pattern_)
        for pattern_ in chunks_:
            escape_ = Array("$", "^", ".", "{", "}", "(", ")", "[", "]", "|")
            while True:
                
                if not (php_strpos(pattern_, "**") != False):
                    break
                # end if
                pattern_ = php_str_replace("**", "*", pattern_)
            # end while
            for probe_ in escape_:
                pattern_ = php_str_replace(probe_, str("\\") + str(probe_), pattern_)
            # end for
            pattern_ = php_str_replace("?*", "*", php_str_replace("*?", "*", php_str_replace("*", ".*", php_str_replace("?", ".{1,1}", pattern_))))
            out_[-1] = pattern_
        # end for
        if php_count(out_) == 1:
            return self.glob_regexp(str("^") + str(out_[0]) + str("$"), string_)
        else:
            for tester_ in out_:
                if self.my_regexp(str("^") + str(tester_) + str("$"), string_):
                    return True
                # end if
            # end for
        # end if
        return False
    # end def glob_pattern_match
    def glob_regexp(self, pattern_=None, probe_=None):
        
        
        sensitive_ = PHP_OS != "WIN32"
        return php_preg_match("/" + preg_quote(pattern_, "/") + "/", probe_) if sensitive_ else php_preg_match("/" + preg_quote(pattern_, "/") + "/i", probe_)
    # end def glob_regexp
    def dirlist(self, remote_=None):
        
        
        list_ = self.rawlist(remote_, "-la")
        if list_ == False:
            self.pusherror("dirlist", "can't read remote folder list", "Can't read remote folder \"" + remote_ + "\" contents")
            return False
        # end if
        dirlist_ = Array()
        for k_,v_ in list_.items():
            entry_ = self.parselisting(v_)
            if php_empty(lambda : entry_):
                continue
            # end if
            if entry_["name"] == "." or entry_["name"] == "..":
                continue
            # end if
            dirlist_[entry_["name"]] = entry_
        # end for
        return dirlist_
    # end def dirlist
    #// <!-- --------------------------------------------------------------------------------------- -->
    #// <!--       Private functions                                                                 -->
    #// <!-- --------------------------------------------------------------------------------------- -->
    def _checkcode(self):
        
        
        return self._code < 400 and self._code > 0
    # end def _checkcode
    def _list(self, arg_="", cmd_="LIST", fnction_="_list"):
        
        
        if (not self._data_prepare()):
            return False
        # end if
        if (not self._exec(cmd_ + arg_, fnction_)):
            self._data_close()
            return False
        # end if
        if (not self._checkcode()):
            self._data_close()
            return False
        # end if
        out_ = ""
        if self._code < 200:
            out_ = self._data_read()
            self._data_close()
            if (not self._readmsg()):
                return False
            # end if
            if (not self._checkcode()):
                return False
            # end if
            if out_ == False:
                return False
            # end if
            out_ = php_preg_split("/[" + CRLF + "]+/", out_, -1, PREG_SPLIT_NO_EMPTY)
            pass
        # end if
        return out_
    # end def _list
    #// <!-- --------------------------------------------------------------------------------------- -->
    #// <!-- Partie : gestion des erreurs                                                            -->
    #// <!-- --------------------------------------------------------------------------------------- -->
    #// Gnre une erreur pour traitement externe  la classe
    def pusherror(self, fctname_=None, msg_=None, desc_=None):
        if desc_ is None:
            desc_ = False
        # end if
        
        error_ = Array()
        error_["time"] = time()
        error_["fctname"] = fctname_
        error_["msg"] = msg_
        error_["desc"] = desc_
        if desc_:
            tmp_ = " (" + desc_ + ")"
        else:
            tmp_ = ""
        # end if
        self.sendmsg(fctname_ + ": " + msg_ + tmp_)
        return php_array_push(self._error_array, error_)
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
mod_sockets_ = php_extension_loaded("sockets")
if (not mod_sockets_) and php_function_exists("dl") and php_is_callable("dl"):
    prefix_ = "php_" if PHP_SHLIB_SUFFIX == "dll" else ""
    php_no_error(lambda: php_dl(prefix_ + "sockets." + PHP_SHLIB_SUFFIX))
    mod_sockets_ = php_extension_loaded("sockets")
# end if
php_include_file(__DIR__ + "/class-ftp-" + "sockets" if mod_sockets_ else "pure" + ".php", once=True)
if mod_sockets_:
    class ftp(ftp_sockets):
        pass
    # end class ftp
else:
    class ftp(ftp_pure):
        pass
    # end class ftp
# end if
