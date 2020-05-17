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
    def __init__(self, verb_=None, le_=None):
        if verb_ is None:
            verb_ = False
        # end if
        if le_ is None:
            le_ = False
        # end if
        
        super().__init__(False, verb_, le_)
    # end def __init__
    #// <!-- --------------------------------------------------------------------------------------- -->
    #// <!--       Private functions                                                                 -->
    #// <!-- --------------------------------------------------------------------------------------- -->
    def _settimeout(self, sock_=None):
        
        
        if (not php_no_error(lambda: stream_set_timeout(sock_, self._timeout))):
            self.pusherror("_settimeout", "socket set send timeout")
            self._quit()
            return False
        # end if
        return True
    # end def _settimeout
    def _connect(self, host_=None, port_=None):
        
        
        self.sendmsg("Creating socket")
        sock_ = php_no_error(lambda: fsockopen(host_, port_, errno_, errstr_, self._timeout))
        if (not sock_):
            self.pusherror("_connect", "socket connect failed", errstr_ + " (" + errno_ + ")")
            return False
        # end if
        self._connected = True
        return sock_
    # end def _connect
    def _readmsg(self, fnction_="_readmsg"):
        
        
        if (not self._connected):
            self.pusherror(fnction_, "Connect first")
            return False
        # end if
        result_ = True
        self._message = ""
        self._code = 0
        go_ = True
        while True:
            tmp_ = php_no_error(lambda: php_fgets(self._ftp_control_sock, 512))
            if tmp_ == False:
                go_ = result_
                self.pusherror(fnction_, "Read failed")
            else:
                self._message += tmp_
                if php_preg_match("/^([0-9]{3})(-(.*[" + CRLF + "]{1,2})+\\1)? [^" + CRLF + "]+[" + CRLF + "]{1,2}$/", self._message, regs_):
                    go_ = False
                # end if
            # end if
            
            if go_:
                break
            # end if
        # end while
        if self.LocalEcho:
            php_print("GET < " + php_rtrim(self._message, CRLF) + CRLF)
        # end if
        self._code = php_int(regs_[1])
        return result_
    # end def _readmsg
    def _exec(self, cmd_=None, fnction_="_exec"):
        
        
        if (not self._ready):
            self.pusherror(fnction_, "Connect first")
            return False
        # end if
        if self.LocalEcho:
            php_print("PUT > ", cmd_, CRLF)
        # end if
        status_ = php_no_error(lambda: fputs(self._ftp_control_sock, cmd_ + CRLF))
        if status_ == False:
            self.pusherror(fnction_, "socket write failed")
            return False
        # end if
        self._lastaction = time()
        if (not self._readmsg(fnction_)):
            return False
        # end if
        return True
    # end def _exec
    def _data_prepare(self, mode_=None):
        if mode_ is None:
            mode_ = FTP_ASCII
        # end if
        
        if (not self._settype(mode_)):
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
            ip_port_ = php_explode(",", php_preg_replace("/^.+ \\(?([0-9]{1,3},[0-9]{1,3},[0-9]{1,3},[0-9]{1,3},[0-9]+,[0-9]+)\\)?.*$/s", "\\1", self._message))
            self._datahost = ip_port_[0] + "." + ip_port_[1] + "." + ip_port_[2] + "." + ip_port_[3]
            self._dataport = php_int(ip_port_[4]) << 8 + php_int(ip_port_[5])
            self.sendmsg("Connecting to " + self._datahost + ":" + self._dataport)
            self._ftp_data_sock = php_no_error(lambda: fsockopen(self._datahost, self._dataport, errno_, errstr_, self._timeout))
            if (not self._ftp_data_sock):
                self.pusherror("_data_prepare", "fsockopen fails", errstr_ + " (" + errno_ + ")")
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
    def _data_read(self, mode_=None, fp_=None):
        if mode_ is None:
            mode_ = FTP_ASCII
        # end if
        
        if is_resource(fp_):
            out_ = 0
        else:
            out_ = ""
        # end if
        if (not self._passive):
            self.sendmsg("Only passive connections available!")
            return False
        # end if
        while True:
            
            if not ((not php_feof(self._ftp_data_sock))):
                break
            # end if
            block_ = fread(self._ftp_data_sock, self._ftp_buff_size)
            if mode_ != FTP_BINARY:
                block_ = php_preg_replace("/\r\n|\r|\n/", self._eol_code[self.OS_local], block_)
            # end if
            if is_resource(fp_):
                out_ += fwrite(fp_, block_, php_strlen(block_))
            else:
                out_ += block_
            # end if
        # end while
        return out_
    # end def _data_read
    def _data_write(self, mode_=None, fp_=None):
        if mode_ is None:
            mode_ = FTP_ASCII
        # end if
        
        if is_resource(fp_):
            out_ = 0
        else:
            out_ = ""
        # end if
        if (not self._passive):
            self.sendmsg("Only passive connections available!")
            return False
        # end if
        if is_resource(fp_):
            while True:
                
                if not ((not php_feof(fp_))):
                    break
                # end if
                block_ = fread(fp_, self._ftp_buff_size)
                if (not self._data_write_block(mode_, block_)):
                    return False
                # end if
            # end while
        elif (not self._data_write_block(mode_, fp_)):
            return False
        # end if
        return True
    # end def _data_write
    def _data_write_block(self, mode_=None, block_=None):
        
        
        if mode_ != FTP_BINARY:
            block_ = php_preg_replace("/\r\n|\r|\n/", self._eol_code[self.OS_remote], block_)
        # end if
        while True:
            t_ = php_no_error(lambda: fwrite(self._ftp_data_sock, block_))
            if t_ == False:
                self.pusherror("_data_write", "Can't write to socket")
                return False
            # end if
            block_ = php_substr(block_, t_)
            
            if (not php_empty(lambda : block_)):
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
    def _quit(self, force_=None):
        if force_ is None:
            force_ = False
        # end if
        
        if self._connected or force_:
            php_no_error(lambda: php_fclose(self._ftp_control_sock))
            self._connected = False
            self.sendmsg("Socket closed")
        # end if
    # end def _quit
# end class ftp_pure
