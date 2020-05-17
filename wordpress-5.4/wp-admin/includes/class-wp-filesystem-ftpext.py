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
#// WordPress FTP Filesystem.
#// 
#// @package WordPress
#// @subpackage Filesystem
#// 
#// 
#// WordPress Filesystem Class for implementing FTP.
#// 
#// @since 2.5.0
#// 
#// @see WP_Filesystem_Base
#//
class WP_Filesystem_FTPext(WP_Filesystem_Base):
    #// 
    #// @since 2.5.0
    #// @var resource
    #//
    link = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 2.5.0
    #// 
    #// @param array $opt
    #//
    def __init__(self, opt_=""):
        
        
        self.method = "ftpext"
        self.errors = php_new_class("WP_Error", lambda : WP_Error())
        #// Check if possible to use ftp functions.
        if (not php_extension_loaded("ftp")):
            self.errors.add("no_ftp_ext", __("The ftp PHP extension is not available"))
            return
        # end if
        #// This class uses the timeout on a per-connection basis, others use it on a per-action basis.
        if (not php_defined("FS_TIMEOUT")):
            php_define("FS_TIMEOUT", 240)
        # end if
        if php_empty(lambda : opt_["port"]):
            self.options["port"] = 21
        else:
            self.options["port"] = opt_["port"]
        # end if
        if php_empty(lambda : opt_["hostname"]):
            self.errors.add("empty_hostname", __("FTP hostname is required"))
        else:
            self.options["hostname"] = opt_["hostname"]
        # end if
        #// Check if the options provided are OK.
        if php_empty(lambda : opt_["username"]):
            self.errors.add("empty_username", __("FTP username is required"))
        else:
            self.options["username"] = opt_["username"]
        # end if
        if php_empty(lambda : opt_["password"]):
            self.errors.add("empty_password", __("FTP password is required"))
        else:
            self.options["password"] = opt_["password"]
        # end if
        self.options["ssl"] = False
        if (php_isset(lambda : opt_["connection_type"])) and "ftps" == opt_["connection_type"]:
            self.options["ssl"] = True
        # end if
    # end def __init__
    #// 
    #// Connects filesystem.
    #// 
    #// @since 2.5.0
    #// 
    #// @return bool True on success, false on failure.
    #//
    def connect(self):
        
        
        if (php_isset(lambda : self.options["ssl"])) and self.options["ssl"] and php_function_exists("ftp_ssl_connect"):
            self.link = php_no_error(lambda: ftp_ssl_connect(self.options["hostname"], self.options["port"], FS_CONNECT_TIMEOUT))
        else:
            self.link = php_no_error(lambda: ftp_connect(self.options["hostname"], self.options["port"], FS_CONNECT_TIMEOUT))
        # end if
        if (not self.link):
            self.errors.add("connect", php_sprintf(__("Failed to connect to FTP Server %s"), self.options["hostname"] + ":" + self.options["port"]))
            return False
        # end if
        if (not php_no_error(lambda: ftp_login(self.link, self.options["username"], self.options["password"]))):
            self.errors.add("auth", php_sprintf(__("Username/Password incorrect for %s"), self.options["username"]))
            return False
        # end if
        #// Set the connection to use Passive FTP.
        ftp_pasv(self.link, True)
        if php_no_error(lambda: ftp_get_option(self.link, FTP_TIMEOUT_SEC)) < FS_TIMEOUT:
            php_no_error(lambda: ftp_set_option(self.link, FTP_TIMEOUT_SEC, FS_TIMEOUT))
        # end if
        return True
    # end def connect
    #// 
    #// Reads entire file into a string.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $file Name of the file to read.
    #// @return string|false Read data on success, false if no temporary file could be opened,
    #// or if the file couldn't be retrieved.
    #//
    def get_contents(self, file_=None):
        
        
        tempfile_ = wp_tempnam(file_)
        temp_ = fopen(tempfile_, "w+")
        if (not temp_):
            unlink(tempfile_)
            return False
        # end if
        if (not ftp_fget(self.link, temp_, file_, FTP_BINARY)):
            php_fclose(temp_)
            unlink(tempfile_)
            return False
        # end if
        fseek(temp_, 0)
        #// Skip back to the start of the file being written to.
        contents_ = ""
        while True:
            
            if not ((not php_feof(temp_))):
                break
            # end if
            contents_ += fread(temp_, 8 * KB_IN_BYTES)
        # end while
        php_fclose(temp_)
        unlink(tempfile_)
        return contents_
    # end def get_contents
    #// 
    #// Reads entire file into an array.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $file Path to the file.
    #// @return array|false File contents in an array on success, false on failure.
    #//
    def get_contents_array(self, file_=None):
        
        
        return php_explode("\n", self.get_contents(file_))
    # end def get_contents_array
    #// 
    #// Writes a string to a file.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string    $file     Remote path to the file where to write the data.
    #// @param string    $contents The data to write.
    #// @param int|false $mode     Optional. The file permissions as octal number, usually 0644.
    #// Default false.
    #// @return bool True on success, false on failure.
    #//
    def put_contents(self, file_=None, contents_=None, mode_=None):
        if mode_ is None:
            mode_ = False
        # end if
        
        tempfile_ = wp_tempnam(file_)
        temp_ = fopen(tempfile_, "wb+")
        if (not temp_):
            unlink(tempfile_)
            return False
        # end if
        mbstring_binary_safe_encoding()
        data_length_ = php_strlen(contents_)
        bytes_written_ = fwrite(temp_, contents_)
        reset_mbstring_encoding()
        if data_length_ != bytes_written_:
            php_fclose(temp_)
            unlink(tempfile_)
            return False
        # end if
        fseek(temp_, 0)
        #// Skip back to the start of the file being written to.
        ret_ = ftp_fput(self.link, file_, temp_, FTP_BINARY)
        php_fclose(temp_)
        unlink(tempfile_)
        self.chmod(file_, mode_)
        return ret_
    # end def put_contents
    #// 
    #// Gets the current working directory.
    #// 
    #// @since 2.5.0
    #// 
    #// @return string|false The current working directory on success, false on failure.
    #//
    def cwd(self):
        
        
        cwd_ = ftp_pwd(self.link)
        if cwd_:
            cwd_ = trailingslashit(cwd_)
        # end if
        return cwd_
    # end def cwd
    #// 
    #// Changes current directory.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $dir The new current directory.
    #// @return bool True on success, false on failure.
    #//
    def chdir(self, dir_=None):
        
        
        return php_no_error(lambda: ftp_chdir(self.link, dir_))
    # end def chdir
    #// 
    #// Changes filesystem permissions.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string    $file      Path to the file.
    #// @param int|false $mode      Optional. The permissions as octal number, usually 0644 for files,
    #// 0755 for directories. Default false.
    #// @param bool      $recursive Optional. If set to true, changes file permissions recursively.
    #// Default false.
    #// @return bool True on success, false on failure.
    #//
    def chmod(self, file_=None, mode_=None, recursive_=None):
        if mode_ is None:
            mode_ = False
        # end if
        if recursive_ is None:
            recursive_ = False
        # end if
        
        if (not mode_):
            if self.is_file(file_):
                mode_ = FS_CHMOD_FILE
            elif self.is_dir(file_):
                mode_ = FS_CHMOD_DIR
            else:
                return False
            # end if
        # end if
        #// chmod any sub-objects if recursive.
        if recursive_ and self.is_dir(file_):
            filelist_ = self.dirlist(file_)
            for filename_,filemeta_ in filelist_:
                self.chmod(file_ + "/" + filename_, mode_, recursive_)
            # end for
        # end if
        #// chmod the file or directory.
        if (not php_function_exists("ftp_chmod")):
            return php_bool(ftp_site(self.link, php_sprintf("CHMOD %o %s", mode_, file_)))
        # end if
        return php_bool(ftp_chmod(self.link, mode_, file_))
    # end def chmod
    #// 
    #// Gets the file owner.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $file Path to the file.
    #// @return string|false Username of the owner on success, false on failure.
    #//
    def owner(self, file_=None):
        
        
        dir_ = self.dirlist(file_)
        return dir_[file_]["owner"]
    # end def owner
    #// 
    #// Gets the permissions of the specified file or filepath in their octal format.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $file Path to the file.
    #// @return string Mode of the file (the last 3 digits).
    #//
    def getchmod(self, file_=None):
        
        
        dir_ = self.dirlist(file_)
        return dir_[file_]["permsn"]
    # end def getchmod
    #// 
    #// Gets the file's group.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $file Path to the file.
    #// @return string|false The group on success, false on failure.
    #//
    def group(self, file_=None):
        
        
        dir_ = self.dirlist(file_)
        return dir_[file_]["group"]
    # end def group
    #// 
    #// Copies a file.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string    $source      Path to the source file.
    #// @param string    $destination Path to the destination file.
    #// @param bool      $overwrite   Optional. Whether to overwrite the destination file if it exists.
    #// Default false.
    #// @param int|false $mode        Optional. The permissions as octal number, usually 0644 for files,
    #// 0755 for dirs. Default false.
    #// @return bool True on success, false on failure.
    #//
    def copy(self, source_=None, destination_=None, overwrite_=None, mode_=None):
        if overwrite_ is None:
            overwrite_ = False
        # end if
        if mode_ is None:
            mode_ = False
        # end if
        
        if (not overwrite_) and self.exists(destination_):
            return False
        # end if
        content_ = self.get_contents(source_)
        if False == content_:
            return False
        # end if
        return self.put_contents(destination_, content_, mode_)
    # end def copy
    #// 
    #// Moves a file.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $source      Path to the source file.
    #// @param string $destination Path to the destination file.
    #// @param bool   $overwrite   Optional. Whether to overwrite the destination file if it exists.
    #// Default false.
    #// @return bool True on success, false on failure.
    #//
    def move(self, source_=None, destination_=None, overwrite_=None):
        if overwrite_ is None:
            overwrite_ = False
        # end if
        
        return ftp_rename(self.link, source_, destination_)
    # end def move
    #// 
    #// Deletes a file or directory.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string       $file      Path to the file or directory.
    #// @param bool         $recursive Optional. If set to true, deletes files and folders recursively.
    #// Default false.
    #// @param string|false $type      Type of resource. 'f' for file, 'd' for directory.
    #// Default false.
    #// @return bool True on success, false on failure.
    #//
    def delete(self, file_=None, recursive_=None, type_=None):
        if recursive_ is None:
            recursive_ = False
        # end if
        if type_ is None:
            type_ = False
        # end if
        
        if php_empty(lambda : file_):
            return False
        # end if
        if "f" == type_ or self.is_file(file_):
            return ftp_delete(self.link, file_)
        # end if
        if (not recursive_):
            return ftp_rmdir(self.link, file_)
        # end if
        filelist_ = self.dirlist(trailingslashit(file_))
        if (not php_empty(lambda : filelist_)):
            for delete_file_ in filelist_:
                self.delete(trailingslashit(file_) + delete_file_["name"], recursive_, delete_file_["type"])
            # end for
        # end if
        return ftp_rmdir(self.link, file_)
    # end def delete
    #// 
    #// Checks if a file or directory exists.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $file Path to file or directory.
    #// @return bool Whether $file exists or not.
    #//
    def exists(self, file_=None):
        
        
        list_ = ftp_nlist(self.link, file_)
        if php_empty(lambda : list_) and self.is_dir(file_):
            return True
            pass
        # end if
        return (not php_empty(lambda : list_))
        pass
    # end def exists
    #// 
    #// Checks if resource is a file.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $file File path.
    #// @return bool Whether $file is a file.
    #//
    def is_file(self, file_=None):
        
        
        return self.exists(file_) and (not self.is_dir(file_))
    # end def is_file
    #// 
    #// Checks if resource is a directory.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $path Directory path.
    #// @return bool Whether $path is a directory.
    #//
    def is_dir(self, path_=None):
        
        
        cwd_ = self.cwd()
        result_ = php_no_error(lambda: ftp_chdir(self.link, trailingslashit(path_)))
        if result_ and path_ == self.cwd() or self.cwd() != cwd_:
            php_no_error(lambda: ftp_chdir(self.link, cwd_))
            return True
        # end if
        return False
    # end def is_dir
    #// 
    #// Checks if a file is readable.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $file Path to file.
    #// @return bool Whether $file is readable.
    #//
    def is_readable(self, file_=None):
        
        
        return True
    # end def is_readable
    #// 
    #// Checks if a file or directory is writable.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $file Path to file or directory.
    #// @return bool Whether $file is writable.
    #//
    def is_writable(self, file_=None):
        
        
        return True
    # end def is_writable
    #// 
    #// Gets the file's last access time.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $file Path to file.
    #// @return int|false Unix timestamp representing last access time, false on failure.
    #//
    def atime(self, file_=None):
        
        
        return False
    # end def atime
    #// 
    #// Gets the file modification time.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $file Path to file.
    #// @return int|false Unix timestamp representing modification time, false on failure.
    #//
    def mtime(self, file_=None):
        
        
        return ftp_mdtm(self.link, file_)
    # end def mtime
    #// 
    #// Gets the file size (in bytes).
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $file Path to file.
    #// @return int|false Size of the file in bytes on success, false on failure.
    #//
    def size(self, file_=None):
        
        
        return ftp_size(self.link, file_)
    # end def size
    #// 
    #// Sets the access and modification times of a file.
    #// 
    #// Note: If $file doesn't exist, it will be created.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $file  Path to file.
    #// @param int    $time  Optional. Modified time to set for file.
    #// Default 0.
    #// @param int    $atime Optional. Access time to set for file.
    #// Default 0.
    #// @return bool True on success, false on failure.
    #//
    def touch(self, file_=None, time_=0, atime_=0):
        
        
        return False
    # end def touch
    #// 
    #// Creates a directory.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string     $path  Path for new directory.
    #// @param int|false  $chmod Optional. The permissions as octal number (or false to skip chmod).
    #// Default false.
    #// @param string|int $chown Optional. A user name or number (or false to skip chown).
    #// Default false.
    #// @param string|int $chgrp Optional. A group name or number (or false to skip chgrp).
    #// Default false.
    #// @return bool True on success, false on failure.
    #//
    def mkdir(self, path_=None, chmod_=None, chown_=None, chgrp_=None):
        if chmod_ is None:
            chmod_ = False
        # end if
        if chown_ is None:
            chown_ = False
        # end if
        if chgrp_ is None:
            chgrp_ = False
        # end if
        
        path_ = untrailingslashit(path_)
        if php_empty(lambda : path_):
            return False
        # end if
        if (not ftp_mkdir(self.link, path_)):
            return False
        # end if
        self.chmod(path_, chmod_)
        return True
    # end def mkdir
    #// 
    #// Deletes a directory.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $path      Path to directory.
    #// @param bool   $recursive Optional. Whether to recursively remove files/directories.
    #// Default false.
    #// @return bool True on success, false on failure.
    #//
    def rmdir(self, path_=None, recursive_=None):
        if recursive_ is None:
            recursive_ = False
        # end if
        
        return self.delete(path_, recursive_)
    # end def rmdir
    #// 
    #// @staticvar bool $is_windows
    #// @param string $line
    #// @return array
    #//
    def parselisting(self, line_=None):
        
        
        is_windows_ = None
        if is_null(is_windows_):
            is_windows_ = php_stripos(ftp_systype(self.link), "win") != False
        # end if
        if is_windows_ and php_preg_match("/([0-9]{2})-([0-9]{2})-([0-9]{2}) +([0-9]{2}):([0-9]{2})(AM|PM) +([0-9]+|<DIR>) +(.+)/", line_, lucifer_):
            b_ = Array()
            if lucifer_[3] < 70:
                lucifer_[3] += 2000
            else:
                lucifer_[3] += 1900
                pass
            # end if
            b_["isdir"] = "<DIR>" == lucifer_[7]
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
            b_["time"] = mktime(lucifer_[4] + 12 if strcasecmp(lucifer_[6], "PM") == 0 else 0, lucifer_[5], 0, lucifer_[1], lucifer_[2], lucifer_[3])
            b_["am/pm"] = lucifer_[6]
            b_["name"] = lucifer_[8]
        elif (not is_windows_):
            lucifer_ = php_preg_split("/[ ]/", line_, 9, PREG_SPLIT_NO_EMPTY)
            if lucifer_:
                #// echo $line."\n";
                lcount_ = php_count(lucifer_)
                if lcount_ < 8:
                    return ""
                # end if
                b_ = Array()
                b_["isdir"] = "d" == lucifer_[0][0]
                b_["islink"] = "l" == lucifer_[0][0]
                if b_["isdir"]:
                    b_["type"] = "d"
                elif b_["islink"]:
                    b_["type"] = "l"
                else:
                    b_["type"] = "f"
                # end if
                b_["perms"] = lucifer_[0]
                b_["permsn"] = self.getnumchmodfromh(b_["perms"])
                b_["number"] = lucifer_[1]
                b_["owner"] = lucifer_[2]
                b_["group"] = lucifer_[3]
                b_["size"] = lucifer_[4]
                if 8 == lcount_:
                    sscanf(lucifer_[5], "%d-%d-%d", b_["year"], b_["month"], b_["day"])
                    sscanf(lucifer_[6], "%d:%d", b_["hour"], b_["minute"])
                    b_["time"] = mktime(b_["hour"], b_["minute"], 0, b_["month"], b_["day"], b_["year"])
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
        #// Replace symlinks formatted as "source -> target" with just the source name.
        if (php_isset(lambda : b_["islink"])) and b_["islink"]:
            b_["name"] = php_preg_replace("/(\\s*->\\s*.*)$/", "", b_["name"])
        # end if
        return b_
    # end def parselisting
    #// 
    #// Gets details for files in a directory or a specific file.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $path           Path to directory or file.
    #// @param bool   $include_hidden Optional. Whether to include details of hidden ("." prefixed) files.
    #// Default true.
    #// @param bool   $recursive      Optional. Whether to recursively include file details in nested directories.
    #// Default false.
    #// @return array|false {
    #// Array of files. False if unable to list directory contents.
    #// 
    #// @type string $name        Name of the file or directory.
    #// @type string $perms       *nix representation of permissions.
    #// @type int    $permsn      Octal representation of permissions.
    #// @type string $owner       Owner name or ID.
    #// @type int    $size        Size of file in bytes.
    #// @type int    $lastmodunix Last modified unix timestamp.
    #// @type mixed  $lastmod     Last modified month (3 letter) and day (without leading 0).
    #// @type int    $time        Last modified time.
    #// @type string $type        Type of resource. 'f' for file, 'd' for directory.
    #// @type mixed  $files       If a directory and $recursive is true, contains another array of files.
    #// }
    #//
    def dirlist(self, path_=".", include_hidden_=None, recursive_=None):
        if include_hidden_ is None:
            include_hidden_ = True
        # end if
        if recursive_ is None:
            recursive_ = False
        # end if
        
        if self.is_file(path_):
            limit_file_ = php_basename(path_)
            path_ = php_dirname(path_) + "/"
        else:
            limit_file_ = False
        # end if
        pwd_ = ftp_pwd(self.link)
        if (not php_no_error(lambda: ftp_chdir(self.link, path_))):
            #// Can't change to folder = folder doesn't exist.
            return False
        # end if
        list_ = ftp_rawlist(self.link, "-a", False)
        php_no_error(lambda: ftp_chdir(self.link, pwd_))
        if php_empty(lambda : list_):
            #// Empty array = non-existent folder (real folder will show . at least).
            return False
        # end if
        dirlist_ = Array()
        for k_,v_ in list_:
            entry_ = self.parselisting(v_)
            if php_empty(lambda : entry_):
                continue
            # end if
            if "." == entry_["name"] or ".." == entry_["name"]:
                continue
            # end if
            if (not include_hidden_) and "." == entry_["name"][0]:
                continue
            # end if
            if limit_file_ and entry_["name"] != limit_file_:
                continue
            # end if
            dirlist_[entry_["name"]] = entry_
        # end for
        ret_ = Array()
        for struc_ in dirlist_:
            if "d" == struc_["type"]:
                if recursive_:
                    struc_["files"] = self.dirlist(path_ + "/" + struc_["name"], include_hidden_, recursive_)
                else:
                    struc_["files"] = Array()
                # end if
            # end if
            ret_[struc_["name"]] = struc_
        # end for
        return ret_
    # end def dirlist
    #// 
    #// Destructor.
    #// 
    #// @since 2.5.0
    #//
    def __del__(self):
        
        
        if self.link:
            ftp_close(self.link)
        # end if
    # end def __del__
# end class WP_Filesystem_FTPext
