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
#// WordPress FTP Sockets Filesystem.
#// 
#// @package WordPress
#// @subpackage Filesystem
#// 
#// 
#// WordPress Filesystem Class for implementing FTP Sockets.
#// 
#// @since 2.5.0
#// 
#// @see WP_Filesystem_Base
#//
class WP_Filesystem_ftpsockets(WP_Filesystem_Base):
    #// 
    #// @since 2.5.0
    #// @var ftp
    #//
    ftp = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 2.5.0
    #// 
    #// @param array $opt
    #//
    def __init__(self, opt_=""):
        
        
        self.method = "ftpsockets"
        self.errors = php_new_class("WP_Error", lambda : WP_Error())
        #// Check if possible to use ftp functions.
        if (not php_include_file(ABSPATH + "wp-admin/includes/class-ftp.php", once=False)):
            return
        # end if
        self.ftp = php_new_class("ftp", lambda : ftp())
        if php_empty(lambda : opt_["port"]):
            self.options["port"] = 21
        else:
            self.options["port"] = php_int(opt_["port"])
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
    # end def __init__
    #// 
    #// Connects filesystem.
    #// 
    #// @since 2.5.0
    #// 
    #// @return bool True on success, false on failure.
    #//
    def connect(self):
        
        
        if (not self.ftp):
            return False
        # end if
        self.ftp.settimeout(FS_CONNECT_TIMEOUT)
        if (not self.ftp.setserver(self.options["hostname"], self.options["port"])):
            self.errors.add("connect", php_sprintf(__("Failed to connect to FTP Server %s"), self.options["hostname"] + ":" + self.options["port"]))
            return False
        # end if
        if (not self.ftp.connect()):
            self.errors.add("connect", php_sprintf(__("Failed to connect to FTP Server %s"), self.options["hostname"] + ":" + self.options["port"]))
            return False
        # end if
        if (not self.ftp.login(self.options["username"], self.options["password"])):
            self.errors.add("auth", php_sprintf(__("Username/Password incorrect for %s"), self.options["username"]))
            return False
        # end if
        self.ftp.settype(FTP_BINARY)
        self.ftp.passive(True)
        self.ftp.settimeout(FS_TIMEOUT)
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
        
        
        if (not self.exists(file_)):
            return False
        # end if
        temp_ = wp_tempnam(file_)
        temphandle_ = fopen(temp_, "w+")
        if (not temphandle_):
            unlink(temp_)
            return False
        # end if
        mbstring_binary_safe_encoding()
        if (not self.ftp.fget(temphandle_, file_)):
            php_fclose(temphandle_)
            unlink(temp_)
            reset_mbstring_encoding()
            return ""
            pass
        # end if
        reset_mbstring_encoding()
        fseek(temphandle_, 0)
        #// Skip back to the start of the file being written to.
        contents_ = ""
        while True:
            
            if not ((not php_feof(temphandle_))):
                break
            # end if
            contents_ += fread(temphandle_, 8 * KB_IN_BYTES)
        # end while
        php_fclose(temphandle_)
        unlink(temp_)
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
        
        temp_ = wp_tempnam(file_)
        temphandle_ = php_no_error(lambda: fopen(temp_, "w+"))
        if (not temphandle_):
            unlink(temp_)
            return False
        # end if
        #// The FTP class uses string functions internally during file download/upload.
        mbstring_binary_safe_encoding()
        bytes_written_ = fwrite(temphandle_, contents_)
        if False == bytes_written_ or php_strlen(contents_) != bytes_written_:
            php_fclose(temphandle_)
            unlink(temp_)
            reset_mbstring_encoding()
            return False
        # end if
        fseek(temphandle_, 0)
        #// Skip back to the start of the file being written to.
        ret_ = self.ftp.fput(file_, temphandle_)
        reset_mbstring_encoding()
        php_fclose(temphandle_)
        unlink(temp_)
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
        
        
        cwd_ = self.ftp.pwd()
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
        
        
        return self.ftp.chdir(dir_)
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
        return self.ftp.chmod(file_, mode_)
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
        
        return self.ftp.rename(source_, destination_)
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
            return self.ftp.delete(file_)
        # end if
        if (not recursive_):
            return self.ftp.rmdir(file_)
        # end if
        return self.ftp.mdel(file_)
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
        
        
        list_ = self.ftp.nlist(file_)
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
        
        
        if self.is_dir(file_):
            return False
        # end if
        if self.exists(file_):
            return True
        # end if
        return False
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
        if self.chdir(path_):
            self.chdir(cwd_)
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
        
        
        return self.ftp.mdtm(file_)
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
        
        
        return self.ftp.filesize(file_)
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
        if (not self.ftp.mkdir(path_)):
            return False
        # end if
        if (not chmod_):
            chmod_ = FS_CHMOD_DIR
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
        mbstring_binary_safe_encoding()
        list_ = self.ftp.dirlist(path_)
        if php_empty(lambda : list_) and (not self.exists(path_)):
            reset_mbstring_encoding()
            return False
        # end if
        ret_ = Array()
        for struc_ in list_:
            if "." == struc_["name"] or ".." == struc_["name"]:
                continue
            # end if
            if (not include_hidden_) and "." == struc_["name"][0]:
                continue
            # end if
            if limit_file_ and struc_["name"] != limit_file_:
                continue
            # end if
            if "d" == struc_["type"]:
                if recursive_:
                    struc_["files"] = self.dirlist(path_ + "/" + struc_["name"], include_hidden_, recursive_)
                else:
                    struc_["files"] = Array()
                # end if
            # end if
            #// Replace symlinks formatted as "source -> target" with just the source name.
            if struc_["islink"]:
                struc_["name"] = php_preg_replace("/(\\s*->\\s*.*)$/", "", struc_["name"])
            # end if
            #// Add the octal representation of the file permissions.
            struc_["permsn"] = self.getnumchmodfromh(struc_["perms"])
            ret_[struc_["name"]] = struc_
        # end for
        reset_mbstring_encoding()
        return ret_
    # end def dirlist
    #// 
    #// Destructor.
    #// 
    #// @since 2.5.0
    #//
    def __del__(self):
        
        
        self.ftp.quit()
    # end def __del__
# end class WP_Filesystem_ftpsockets
