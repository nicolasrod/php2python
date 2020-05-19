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
#// Socket Based FTP implementation
#// 
#// @package PemFTP
#// @subpackage Socket
#// @since 2.5.0
#// 
#// @version 1.0
#// @copyright Alexey Dotsenko
#// @author Alexey Dotsenko
#// @link https://www.phpclasses.org/package/1743-PHP-FTP-client-in-pure-PHP.html
#// @license LGPL https://opensource.org/licenses/lgpl-license.html
#//
class ftp_sockets(ftp_base):
    def __init__(self, verb_=None, le_=None):
        if verb_ is None:
            verb_ = False
        # end if
        if le_ is None:
            le_ = False
        # end if
        
        super().__init__(True, verb_, le_)
    # end def __init__
    #// <!-- --------------------------------------------------------------------------------------- -->
    #// <!--       Private functions                                                                 -->
    #// <!-- --------------------------------------------------------------------------------------- -->
    def _settimeout(self, sock_=None):
        
        
        if (not php_no_error(lambda: socket_set_option(sock_, SOL_SOCKET, SO_RCVTIMEO, Array({"sec": self._timeout, "usec": 0})))):
            self.pusherror("_connect", "socket set receive timeout", socket_strerror(socket_last_error(sock_)))
            php_no_error(lambda: socket_close(sock_))
            return False
        # end if
        if (not php_no_error(lambda: socket_set_option(sock_, SOL_SOCKET, SO_SNDTIMEO, Array({"sec": self._timeout, "usec": 0})))):
            self.pusherror("_connect", "socket set send timeout", socket_strerror(socket_last_error(sock_)))
            php_no_error(lambda: socket_close(sock_))
            return False
        # end if
        return True
    # end def _settimeout
    def _connect(self, host_=None, port_=None):
        
        
        self.sendmsg("Creating socket")
        sock_ = php_no_error(lambda: socket_create(AF_INET, SOCK_STREAM, SOL_TCP))
        if (not sock_):
            self.pusherror("_connect", "socket create failed", socket_strerror(socket_last_error(sock_)))
            return False
        # end if
        if (not self._settimeout(sock_)):
            return False
        # end if
        self.sendmsg("Connecting to \"" + host_ + ":" + port_ + "\"")
        res_ = php_no_error(lambda: socket_connect(sock_, host_, port_))
        if (not res_):
            self.pusherror("_connect", "socket connect failed", socket_strerror(socket_last_error(sock_)))
            php_no_error(lambda: socket_close(sock_))
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
            tmp_ = php_no_error(lambda: socket_read(self._ftp_control_sock, 4096, PHP_BINARY_READ))
            if tmp_ == False:
                go_ = result_
                self.pusherror(fnction_, "Read failed", socket_strerror(socket_last_error(self._ftp_control_sock)))
            else:
                self._message += tmp_
                go_ = (not php_preg_match("/^([0-9]{3})(-.+\\1)? [^" + CRLF + "]+" + CRLF + "$/Us", self._message, regs_))
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
        status_ = php_no_error(lambda: socket_write(self._ftp_control_sock, cmd_ + CRLF))
        if status_ == False:
            self.pusherror(fnction_, "socket write failed", socket_strerror(socket_last_error(self.stream)))
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
        self.sendmsg("Creating data socket")
        self._ftp_data_sock = php_no_error(lambda: socket_create(AF_INET, SOCK_STREAM, SOL_TCP))
        if self._ftp_data_sock < 0:
            self.pusherror("_data_prepare", "socket create failed", socket_strerror(socket_last_error(self._ftp_data_sock)))
            return False
        # end if
        if (not self._settimeout(self._ftp_data_sock)):
            self._data_close()
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
            if (not php_no_error(lambda: socket_connect(self._ftp_data_sock, self._datahost, self._dataport))):
                self.pusherror("_data_prepare", "socket_connect", socket_strerror(socket_last_error(self._ftp_data_sock)))
                self._data_close()
                return False
            else:
                self._ftp_temp_sock = self._ftp_data_sock
            # end if
        else:
            if (not php_no_error(lambda: socket_getsockname(self._ftp_control_sock, addr_, port_))):
                self.pusherror("_data_prepare", "can't get control socket information", socket_strerror(socket_last_error(self._ftp_control_sock)))
                self._data_close()
                return False
            # end if
            if (not php_no_error(lambda: socket_bind(self._ftp_data_sock, addr_))):
                self.pusherror("_data_prepare", "can't bind data socket", socket_strerror(socket_last_error(self._ftp_data_sock)))
                self._data_close()
                return False
            # end if
            if (not php_no_error(lambda: socket_listen(self._ftp_data_sock))):
                self.pusherror("_data_prepare", "can't listen data socket", socket_strerror(socket_last_error(self._ftp_data_sock)))
                self._data_close()
                return False
            # end if
            if (not php_no_error(lambda: socket_getsockname(self._ftp_data_sock, self._datahost, self._dataport))):
                self.pusherror("_data_prepare", "can't get data socket information", socket_strerror(socket_last_error(self._ftp_data_sock)))
                self._data_close()
                return False
            # end if
            if (not self._exec("PORT " + php_str_replace(".", ",", self._datahost + "." + self._dataport >> 8 + "." + self._dataport & 255), "_port")):
                self._data_close()
                return False
            # end if
            if (not self._checkcode()):
                self._data_close()
                return False
            # end if
        # end if
        return True
    # end def _data_prepare
    def _data_read(self, mode_=None, fp_=None):
        if mode_ is None:
            mode_ = FTP_ASCII
        # end if
        if fp_ is None:
            fp_ = None
        # end if
        
        NewLine_ = self._eol_code[self.OS_local]
        if php_is_resource(fp_):
            out_ = 0
        else:
            out_ = ""
        # end if
        if (not self._passive):
            self.sendmsg("Connecting to " + self._datahost + ":" + self._dataport)
            self._ftp_temp_sock = socket_accept(self._ftp_data_sock)
            if self._ftp_temp_sock == False:
                self.pusherror("_data_read", "socket_accept", socket_strerror(socket_last_error(self._ftp_temp_sock)))
                self._data_close()
                return False
            # end if
        # end if
        while True:
            block_ = php_no_error(lambda: socket_read(self._ftp_temp_sock, self._ftp_buff_size, PHP_BINARY_READ))
            if not (block_ != False):
                break
            # end if
            if block_ == "":
                break
            # end if
            if mode_ != FTP_BINARY:
                block_ = php_preg_replace("/\r\n|\r|\n/", self._eol_code[self.OS_local], block_)
            # end if
            if php_is_resource(fp_):
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
        if fp_ is None:
            fp_ = None
        # end if
        
        NewLine_ = self._eol_code[self.OS_local]
        if php_is_resource(fp_):
            out_ = 0
        else:
            out_ = ""
        # end if
        if (not self._passive):
            self.sendmsg("Connecting to " + self._datahost + ":" + self._dataport)
            self._ftp_temp_sock = socket_accept(self._ftp_data_sock)
            if self._ftp_temp_sock == False:
                self.pusherror("_data_write", "socket_accept", socket_strerror(socket_last_error(self._ftp_temp_sock)))
                self._data_close()
                return False
            # end if
        # end if
        if php_is_resource(fp_):
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
            t_ = php_no_error(lambda: socket_write(self._ftp_temp_sock, block_))
            if t_ == False:
                self.pusherror("_data_write", "socket_write", socket_strerror(socket_last_error(self._ftp_temp_sock)))
                self._data_close()
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
        
        
        php_no_error(lambda: socket_close(self._ftp_temp_sock))
        php_no_error(lambda: socket_close(self._ftp_data_sock))
        self.sendmsg("Disconnected data from remote host")
        return True
    # end def _data_close
    def _quit(self):
        
        
        if self._connected:
            php_no_error(lambda: socket_close(self._ftp_control_sock))
            self._connected = False
            self.sendmsg("Socket closed")
        # end if
    # end def _quit
# end class ftp_sockets
