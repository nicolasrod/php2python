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
    ftp = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 2.5.0
    #// 
    #// @param array $opt
    #//
    def __init__(self, opt=""):
        
        self.method = "ftpsockets"
        self.errors = php_new_class("WP_Error", lambda : WP_Error())
        #// Check if possible to use ftp functions.
        if (not php_include_file(ABSPATH + "wp-admin/includes/class-ftp.php", once=False)):
            return
        # end if
        self.ftp = php_new_class("ftp", lambda : ftp())
        if php_empty(lambda : opt["port"]):
            self.options["port"] = 21
        else:
            self.options["port"] = int(opt["port"])
        # end if
        if php_empty(lambda : opt["hostname"]):
            self.errors.add("empty_hostname", __("FTP hostname is required"))
        else:
            self.options["hostname"] = opt["hostname"]
        # end if
        #// Check if the options provided are OK.
        if php_empty(lambda : opt["username"]):
            self.errors.add("empty_username", __("FTP username is required"))
        else:
            self.options["username"] = opt["username"]
        # end if
        if php_empty(lambda : opt["password"]):
            self.errors.add("empty_password", __("FTP password is required"))
        else:
            self.options["password"] = opt["password"]
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
    def get_contents(self, file=None):
        
        if (not self.exists(file)):
            return False
        # end if
        temp = wp_tempnam(file)
        temphandle = fopen(temp, "w+")
        if (not temphandle):
            unlink(temp)
            return False
        # end if
        mbstring_binary_safe_encoding()
        if (not self.ftp.fget(temphandle, file)):
            php_fclose(temphandle)
            unlink(temp)
            reset_mbstring_encoding()
            return ""
            pass
        # end if
        reset_mbstring_encoding()
        fseek(temphandle, 0)
        #// Skip back to the start of the file being written to.
        contents = ""
        while True:
            
            if not ((not php_feof(temphandle))):
                break
            # end if
            contents += fread(temphandle, 8 * KB_IN_BYTES)
        # end while
        php_fclose(temphandle)
        unlink(temp)
        return contents
    # end def get_contents
    #// 
    #// Reads entire file into an array.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $file Path to the file.
    #// @return array|false File contents in an array on success, false on failure.
    #//
    def get_contents_array(self, file=None):
        
        return php_explode("\n", self.get_contents(file))
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
    def put_contents(self, file=None, contents=None, mode=False):
        
        temp = wp_tempnam(file)
        temphandle = php_no_error(lambda: fopen(temp, "w+"))
        if (not temphandle):
            unlink(temp)
            return False
        # end if
        #// The FTP class uses string functions internally during file download/upload.
        mbstring_binary_safe_encoding()
        bytes_written = fwrite(temphandle, contents)
        if False == bytes_written or php_strlen(contents) != bytes_written:
            php_fclose(temphandle)
            unlink(temp)
            reset_mbstring_encoding()
            return False
        # end if
        fseek(temphandle, 0)
        #// Skip back to the start of the file being written to.
        ret = self.ftp.fput(file, temphandle)
        reset_mbstring_encoding()
        php_fclose(temphandle)
        unlink(temp)
        self.chmod(file, mode)
        return ret
    # end def put_contents
    #// 
    #// Gets the current working directory.
    #// 
    #// @since 2.5.0
    #// 
    #// @return string|false The current working directory on success, false on failure.
    #//
    def cwd(self):
        
        cwd = self.ftp.pwd()
        if cwd:
            cwd = trailingslashit(cwd)
        # end if
        return cwd
    # end def cwd
    #// 
    #// Changes current directory.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $dir The new current directory.
    #// @return bool True on success, false on failure.
    #//
    def chdir(self, dir=None):
        
        return self.ftp.chdir(dir)
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
    def chmod(self, file=None, mode=False, recursive=False):
        
        if (not mode):
            if self.is_file(file):
                mode = FS_CHMOD_FILE
            elif self.is_dir(file):
                mode = FS_CHMOD_DIR
            else:
                return False
            # end if
        # end if
        #// chmod any sub-objects if recursive.
        if recursive and self.is_dir(file):
            filelist = self.dirlist(file)
            for filename,filemeta in filelist:
                self.chmod(file + "/" + filename, mode, recursive)
            # end for
        # end if
        #// chmod the file or directory.
        return self.ftp.chmod(file, mode)
    # end def chmod
    #// 
    #// Gets the file owner.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $file Path to the file.
    #// @return string|false Username of the owner on success, false on failure.
    #//
    def owner(self, file=None):
        
        dir = self.dirlist(file)
        return dir[file]["owner"]
    # end def owner
    #// 
    #// Gets the permissions of the specified file or filepath in their octal format.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $file Path to the file.
    #// @return string Mode of the file (the last 3 digits).
    #//
    def getchmod(self, file=None):
        
        dir = self.dirlist(file)
        return dir[file]["permsn"]
    # end def getchmod
    #// 
    #// Gets the file's group.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $file Path to the file.
    #// @return string|false The group on success, false on failure.
    #//
    def group(self, file=None):
        
        dir = self.dirlist(file)
        return dir[file]["group"]
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
    def copy(self, source=None, destination=None, overwrite=False, mode=False):
        
        if (not overwrite) and self.exists(destination):
            return False
        # end if
        content = self.get_contents(source)
        if False == content:
            return False
        # end if
        return self.put_contents(destination, content, mode)
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
    def move(self, source=None, destination=None, overwrite=False):
        
        return self.ftp.rename(source, destination)
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
    def delete(self, file=None, recursive=False, type=False):
        
        if php_empty(lambda : file):
            return False
        # end if
        if "f" == type or self.is_file(file):
            return self.ftp.delete(file)
        # end if
        if (not recursive):
            return self.ftp.rmdir(file)
        # end if
        return self.ftp.mdel(file)
    # end def delete
    #// 
    #// Checks if a file or directory exists.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $file Path to file or directory.
    #// @return bool Whether $file exists or not.
    #//
    def exists(self, file=None):
        
        list = self.ftp.nlist(file)
        if php_empty(lambda : list) and self.is_dir(file):
            return True
            pass
        # end if
        return (not php_empty(lambda : list))
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
    def is_file(self, file=None):
        
        if self.is_dir(file):
            return False
        # end if
        if self.exists(file):
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
    def is_dir(self, path=None):
        
        cwd = self.cwd()
        if self.chdir(path):
            self.chdir(cwd)
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
    def is_readable(self, file=None):
        
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
    def is_writable(self, file=None):
        
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
    def atime(self, file=None):
        
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
    def mtime(self, file=None):
        
        return self.ftp.mdtm(file)
    # end def mtime
    #// 
    #// Gets the file size (in bytes).
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $file Path to file.
    #// @return int|false Size of the file in bytes on success, false on failure.
    #//
    def size(self, file=None):
        
        return self.ftp.filesize(file)
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
    def touch(self, file=None, time=0, atime=0):
        
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
    def mkdir(self, path=None, chmod=False, chown=False, chgrp=False):
        
        path = untrailingslashit(path)
        if php_empty(lambda : path):
            return False
        # end if
        if (not self.ftp.mkdir(path)):
            return False
        # end if
        if (not chmod):
            chmod = FS_CHMOD_DIR
        # end if
        self.chmod(path, chmod)
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
    def rmdir(self, path=None, recursive=False):
        
        return self.delete(path, recursive)
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
    def dirlist(self, path=".", include_hidden=True, recursive=False):
        
        if self.is_file(path):
            limit_file = php_basename(path)
            path = php_dirname(path) + "/"
        else:
            limit_file = False
        # end if
        mbstring_binary_safe_encoding()
        list = self.ftp.dirlist(path)
        if php_empty(lambda : list) and (not self.exists(path)):
            reset_mbstring_encoding()
            return False
        # end if
        ret = Array()
        for struc in list:
            if "." == struc["name"] or ".." == struc["name"]:
                continue
            # end if
            if (not include_hidden) and "." == struc["name"][0]:
                continue
            # end if
            if limit_file and struc["name"] != limit_file:
                continue
            # end if
            if "d" == struc["type"]:
                if recursive:
                    struc["files"] = self.dirlist(path + "/" + struc["name"], include_hidden, recursive)
                else:
                    struc["files"] = Array()
                # end if
            # end if
            #// Replace symlinks formatted as "source -> target" with just the source name.
            if struc["islink"]:
                struc["name"] = php_preg_replace("/(\\s*->\\s*.*)$/", "", struc["name"])
            # end if
            #// Add the octal representation of the file permissions.
            struc["permsn"] = self.getnumchmodfromh(struc["perms"])
            ret[struc["name"]] = struc
        # end for
        reset_mbstring_encoding()
        return ret
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
