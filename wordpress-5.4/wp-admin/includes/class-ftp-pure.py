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
#// FTP implementation using fsockopen to connect.
#// 
#// @package PemFTP
#// @subpackage Pure
#// @since 2.5.0
#// 
#// @version 1.0
#// @copyright Alexey Dotsenko
#// @author Alexey Dotsenko
#// @link https://www.phpclasses.org/package/1743-PHP-FTP-client-in-pure-PHP.html
#// @license LGPL https://opensource.org/licenses/lgpl-license.html
#//
class ftp_pure(ftp_base):
    def __init__(self, verb=False, le=False):
        
        super().__init__(False, verb, le)
    # end def __init__
    #// <!-- --------------------------------------------------------------------------------------- -->
    #// <!--       Private functions                                                                 -->
    #// <!-- --------------------------------------------------------------------------------------- -->
    def _settimeout(self, sock=None):
        
        if (not php_no_error(lambda: stream_set_timeout(sock, self._timeout))):
            self.pusherror("_settimeout", "socket set send timeout")
            self._quit()
            return False
        # end if
        return True
    # end def _settimeout
    def _connect(self, host=None, port=None):
        
        self.sendmsg("Creating socket")
        sock = php_no_error(lambda: fsockopen(host, port, errno, errstr, self._timeout))
        if (not sock):
            self.pusherror("_connect", "socket connect failed", errstr + " (" + errno + ")")
            return False
        # end if
        self._connected = True
        return sock
    # end def _connect
    def _readmsg(self, fnction="_readmsg"):
        
        if (not self._connected):
            self.pusherror(fnction, "Connect first")
            return False
        # end if
        result = True
        self._message = ""
        self._code = 0
        go = True
        while True:
            tmp = php_no_error(lambda: php_fgets(self._ftp_control_sock, 512))
            if tmp == False:
                go = result
                self.pusherror(fnction, "Read failed")
            else:
                self._message += tmp
                if php_preg_match("/^([0-9]{3})(-(.*[" + CRLF + "]{1,2})+\\1)? [^" + CRLF + "]+[" + CRLF + "]{1,2}$/", self._message, regs):
                    go = False
                # end if
            # end if
            
            if go:
                break
            # end if
        # end while
        if self.LocalEcho:
            php_print("GET < " + php_rtrim(self._message, CRLF) + CRLF)
        # end if
        self._code = php_int(regs[1])
        return result
    # end def _readmsg
    def _exec(self, cmd=None, fnction="_exec"):
        
        if (not self._ready):
            self.pusherror(fnction, "Connect first")
            return False
        # end if
        if self.LocalEcho:
            php_print("PUT > ", cmd, CRLF)
        # end if
        status = php_no_error(lambda: fputs(self._ftp_control_sock, cmd + CRLF))
        if status == False:
            self.pusherror(fnction, "socket write failed")
            return False
        # end if
        self._lastaction = time()
        if (not self._readmsg(fnction)):
            return False
        # end if
        return True
    # end def _exec
    def _data_prepare(self, mode=FTP_ASCII):
        
        if (not self._settype(mode)):
            return False
        # end if
        if self._passive:
            if (not self._exec("PASV", "pasv")):
                self._data_close()
                return False
            # end if
            if (not self._checkcode()):
                self._data_close()
                return False
            # end if
            ip_port = php_explode(",", php_preg_replace("/^.+ \\(?([0-9]{1,3},[0-9]{1,3},[0-9]{1,3},[0-9]{1,3},[0-9]+,[0-9]+)\\)?.*$/s", "\\1", self._message))
            self._datahost = ip_port[0] + "." + ip_port[1] + "." + ip_port[2] + "." + ip_port[3]
            self._dataport = php_int(ip_port[4]) << 8 + php_int(ip_port[5])
            self.sendmsg("Connecting to " + self._datahost + ":" + self._dataport)
            self._ftp_data_sock = php_no_error(lambda: fsockopen(self._datahost, self._dataport, errno, errstr, self._timeout))
            if (not self._ftp_data_sock):
                self.pusherror("_data_prepare", "fsockopen fails", errstr + " (" + errno + ")")
                self._data_close()
                return False
            else:
                self._ftp_data_sock
            # end if
        else:
            self.sendmsg("Only passive connections available!")
            return False
        # end if
        return True
    # end def _data_prepare
    def _data_read(self, mode=FTP_ASCII, fp=None):
        
        if is_resource(fp):
            out = 0
        else:
            out = ""
        # end if
        if (not self._passive):
            self.sendmsg("Only passive connections available!")
            return False
        # end if
        while True:
            
            if not ((not php_feof(self._ftp_data_sock))):
                break
            # end if
            block = fread(self._ftp_data_sock, self._ftp_buff_size)
            if mode != FTP_BINARY:
                block = php_preg_replace("/\r\n|\r|\n/", self._eol_code[self.OS_local], block)
            # end if
            if is_resource(fp):
                out += fwrite(fp, block, php_strlen(block))
            else:
                out += block
            # end if
        # end while
        return out
    # end def _data_read
    def _data_write(self, mode=FTP_ASCII, fp=None):
        
        if is_resource(fp):
            out = 0
        else:
            out = ""
        # end if
        if (not self._passive):
            self.sendmsg("Only passive connections available!")
            return False
        # end if
        if is_resource(fp):
            while True:
                
                if not ((not php_feof(fp))):
                    break
                # end if
                block = fread(fp, self._ftp_buff_size)
                if (not self._data_write_block(mode, block)):
                    return False
                # end if
            # end while
        elif (not self._data_write_block(mode, fp)):
            return False
        # end if
        return True
    # end def _data_write
    def _data_write_block(self, mode=None, block=None):
        
        if mode != FTP_BINARY:
            block = php_preg_replace("/\r\n|\r|\n/", self._eol_code[self.OS_remote], block)
        # end if
        while True:
            t = php_no_error(lambda: fwrite(self._ftp_data_sock, block))
            if t == False:
                self.pusherror("_data_write", "Can't write to socket")
                return False
            # end if
            block = php_substr(block, t)
            
            if (not php_empty(lambda : block)):
                break
            # end if
        # end while
        return True
    # end def _data_write_block
    def _data_close(self):
        
        php_no_error(lambda: php_fclose(self._ftp_data_sock))
        self.sendmsg("Disconnected data from remote host")
        return True
    # end def _data_close
    def _quit(self, force=False):
        
        if self._connected or force:
            php_no_error(lambda: php_fclose(self._ftp_control_sock))
            self._connected = False
            self.sendmsg("Socket closed")
        # end if
    # end def _quit
# end class ftp_pure
