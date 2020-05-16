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
    link = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 2.5.0
    #// 
    #// @param array $opt
    #//
    def __init__(self, opt=""):
        
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
        if php_empty(lambda : opt["port"]):
            self.options["port"] = 21
        else:
            self.options["port"] = opt["port"]
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
        self.options["ssl"] = False
        if (php_isset(lambda : opt["connection_type"])) and "ftps" == opt["connection_type"]:
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
    def get_contents(self, file=None):
        
        tempfile = wp_tempnam(file)
        temp = fopen(tempfile, "w+")
        if (not temp):
            unlink(tempfile)
            return False
        # end if
        if (not ftp_fget(self.link, temp, file, FTP_BINARY)):
            php_fclose(temp)
            unlink(tempfile)
            return False
        # end if
        fseek(temp, 0)
        #// Skip back to the start of the file being written to.
        contents = ""
        while True:
            
            if not ((not php_feof(temp))):
                break
            # end if
            contents += fread(temp, 8 * KB_IN_BYTES)
        # end while
        php_fclose(temp)
        unlink(tempfile)
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
        
        tempfile = wp_tempnam(file)
        temp = fopen(tempfile, "wb+")
        if (not temp):
            unlink(tempfile)
            return False
        # end if
        mbstring_binary_safe_encoding()
        data_length = php_strlen(contents)
        bytes_written = fwrite(temp, contents)
        reset_mbstring_encoding()
        if data_length != bytes_written:
            php_fclose(temp)
            unlink(tempfile)
            return False
        # end if
        fseek(temp, 0)
        #// Skip back to the start of the file being written to.
        ret = ftp_fput(self.link, file, temp, FTP_BINARY)
        php_fclose(temp)
        unlink(tempfile)
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
        
        cwd = ftp_pwd(self.link)
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
        
        return php_no_error(lambda: ftp_chdir(self.link, dir))
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
        if (not php_function_exists("ftp_chmod")):
            return php_bool(ftp_site(self.link, php_sprintf("CHMOD %o %s", mode, file)))
        # end if
        return php_bool(ftp_chmod(self.link, mode, file))
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
        
        return ftp_rename(self.link, source, destination)
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
            return ftp_delete(self.link, file)
        # end if
        if (not recursive):
            return ftp_rmdir(self.link, file)
        # end if
        filelist = self.dirlist(trailingslashit(file))
        if (not php_empty(lambda : filelist)):
            for delete_file in filelist:
                self.delete(trailingslashit(file) + delete_file["name"], recursive, delete_file["type"])
            # end for
        # end if
        return ftp_rmdir(self.link, file)
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
        
        list = ftp_nlist(self.link, file)
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
        
        return self.exists(file) and (not self.is_dir(file))
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
        result = php_no_error(lambda: ftp_chdir(self.link, trailingslashit(path)))
        if result and path == self.cwd() or self.cwd() != cwd:
            php_no_error(lambda: ftp_chdir(self.link, cwd))
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
        
        return ftp_mdtm(self.link, file)
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
        
        return ftp_size(self.link, file)
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
        if (not ftp_mkdir(self.link, path)):
            return False
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
    #// @staticvar bool $is_windows
    #// @param string $line
    #// @return array
    #//
    def parselisting(self, line=None):
        
        is_windows = None
        if is_null(is_windows):
            is_windows = php_stripos(ftp_systype(self.link), "win") != False
        # end if
        if is_windows and php_preg_match("/([0-9]{2})-([0-9]{2})-([0-9]{2}) +([0-9]{2}):([0-9]{2})(AM|PM) +([0-9]+|<DIR>) +(.+)/", line, lucifer):
            b = Array()
            if lucifer[3] < 70:
                lucifer[3] += 2000
            else:
                lucifer[3] += 1900
                pass
            # end if
            b["isdir"] = "<DIR>" == lucifer[7]
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
            b["time"] = mktime(lucifer[4] + 12 if strcasecmp(lucifer[6], "PM") == 0 else 0, lucifer[5], 0, lucifer[1], lucifer[2], lucifer[3])
            b["am/pm"] = lucifer[6]
            b["name"] = lucifer[8]
        elif (not is_windows):
            lucifer = php_preg_split("/[ ]/", line, 9, PREG_SPLIT_NO_EMPTY)
            if lucifer:
                #// echo $line."\n";
                lcount = php_count(lucifer)
                if lcount < 8:
                    return ""
                # end if
                b = Array()
                b["isdir"] = "d" == lucifer[0][0]
                b["islink"] = "l" == lucifer[0][0]
                if b["isdir"]:
                    b["type"] = "d"
                elif b["islink"]:
                    b["type"] = "l"
                else:
                    b["type"] = "f"
                # end if
                b["perms"] = lucifer[0]
                b["permsn"] = self.getnumchmodfromh(b["perms"])
                b["number"] = lucifer[1]
                b["owner"] = lucifer[2]
                b["group"] = lucifer[3]
                b["size"] = lucifer[4]
                if 8 == lcount:
                    sscanf(lucifer[5], "%d-%d-%d", b["year"], b["month"], b["day"])
                    sscanf(lucifer[6], "%d:%d", b["hour"], b["minute"])
                    b["time"] = mktime(b["hour"], b["minute"], 0, b["month"], b["day"], b["year"])
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
        #// Replace symlinks formatted as "source -> target" with just the source name.
        if (php_isset(lambda : b["islink"])) and b["islink"]:
            b["name"] = php_preg_replace("/(\\s*->\\s*.*)$/", "", b["name"])
        # end if
        return b
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
    def dirlist(self, path=".", include_hidden=True, recursive=False):
        
        if self.is_file(path):
            limit_file = php_basename(path)
            path = php_dirname(path) + "/"
        else:
            limit_file = False
        # end if
        pwd = ftp_pwd(self.link)
        if (not php_no_error(lambda: ftp_chdir(self.link, path))):
            #// Can't change to folder = folder doesn't exist.
            return False
        # end if
        list = ftp_rawlist(self.link, "-a", False)
        php_no_error(lambda: ftp_chdir(self.link, pwd))
        if php_empty(lambda : list):
            #// Empty array = non-existent folder (real folder will show . at least).
            return False
        # end if
        dirlist = Array()
        for k,v in list:
            entry = self.parselisting(v)
            if php_empty(lambda : entry):
                continue
            # end if
            if "." == entry["name"] or ".." == entry["name"]:
                continue
            # end if
            if (not include_hidden) and "." == entry["name"][0]:
                continue
            # end if
            if limit_file and entry["name"] != limit_file:
                continue
            # end if
            dirlist[entry["name"]] = entry
        # end for
        ret = Array()
        for struc in dirlist:
            if "d" == struc["type"]:
                if recursive:
                    struc["files"] = self.dirlist(path + "/" + struc["name"], include_hidden, recursive)
                else:
                    struc["files"] = Array()
                # end if
            # end if
            ret[struc["name"]] = struc
        # end for
        return ret
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
