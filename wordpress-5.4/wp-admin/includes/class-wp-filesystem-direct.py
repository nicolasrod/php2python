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
#// WordPress Direct Filesystem.
#// 
#// @package WordPress
#// @subpackage Filesystem
#// 
#// 
#// WordPress Filesystem Class for direct PHP file and folder manipulation.
#// 
#// @since 2.5.0
#// 
#// @see WP_Filesystem_Base
#//
class WP_Filesystem_Direct(WP_Filesystem_Base):
    #// 
    #// Constructor.
    #// 
    #// @since 2.5.0
    #// 
    #// @param mixed $arg Not used.
    #//
    def __init__(self, arg=None):
        
        self.method = "direct"
        self.errors = php_new_class("WP_Error", lambda : WP_Error())
    # end def __init__
    #// 
    #// Reads entire file into a string.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $file Name of the file to read.
    #// @return string|false Read data on success, false on failure.
    #//
    def get_contents(self, file=None):
        
        return php_no_error(lambda: php_file_get_contents(file))
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
        
        return php_no_error(lambda: file(file))
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
        
        fp = php_no_error(lambda: fopen(file, "wb"))
        if (not fp):
            return False
        # end if
        mbstring_binary_safe_encoding()
        data_length = php_strlen(contents)
        bytes_written = fwrite(fp, contents)
        reset_mbstring_encoding()
        php_fclose(fp)
        if data_length != bytes_written:
            return False
        # end if
        self.chmod(file, mode)
        return True
    # end def put_contents
    #// 
    #// Gets the current working directory.
    #// 
    #// @since 2.5.0
    #// 
    #// @return string|false The current working directory on success, false on failure.
    #//
    def cwd(self):
        
        return php_getcwd()
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
        
        return php_no_error(lambda: php_chdir(dir))
    # end def chdir
    #// 
    #// Changes the file group.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string     $file      Path to the file.
    #// @param string|int $group     A group name or number.
    #// @param bool       $recursive Optional. If set to true, changes file group recursively.
    #// Default false.
    #// @return bool True on success, false on failure.
    #//
    def chgrp(self, file=None, group=None, recursive=False):
        
        if (not self.exists(file)):
            return False
        # end if
        if (not recursive):
            return chgrp(file, group)
        # end if
        if (not self.is_dir(file)):
            return chgrp(file, group)
        # end if
        #// Is a directory, and we want recursive.
        file = trailingslashit(file)
        filelist = self.dirlist(file)
        for filename in filelist:
            self.chgrp(file + filename, group, recursive)
        # end for
        return True
    # end def chgrp
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
        if (not recursive) or (not self.is_dir(file)):
            return chmod(file, mode)
        # end if
        #// Is a directory, and we want recursive.
        file = trailingslashit(file)
        filelist = self.dirlist(file)
        for filename,filemeta in filelist:
            self.chmod(file + filename, mode, recursive)
        # end for
        return True
    # end def chmod
    #// 
    #// Changes the owner of a file or directory.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string     $file      Path to the file or directory.
    #// @param string|int $owner     A user name or number.
    #// @param bool       $recursive Optional. If set to true, changes file owner recursively.
    #// Default false.
    #// @return bool True on success, false on failure.
    #//
    def chown(self, file=None, owner=None, recursive=False):
        
        if (not self.exists(file)):
            return False
        # end if
        if (not recursive):
            return chown(file, owner)
        # end if
        if (not self.is_dir(file)):
            return chown(file, owner)
        # end if
        #// Is a directory, and we want recursive.
        filelist = self.dirlist(file)
        for filename in filelist:
            self.chown(file + "/" + filename, owner, recursive)
        # end for
        return True
    # end def chown
    #// 
    #// Gets the file owner.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $file Path to the file.
    #// @return string|false Username of the owner on success, false on failure.
    #//
    def owner(self, file=None):
        
        owneruid = php_no_error(lambda: fileowner(file))
        if (not owneruid):
            return False
        # end if
        if (not php_function_exists("posix_getpwuid")):
            return owneruid
        # end if
        ownerarray = posix_getpwuid(owneruid)
        return ownerarray["name"]
    # end def owner
    #// 
    #// Gets the permissions of the specified file or filepath in their octal format.
    #// 
    #// FIXME does not handle errors in fileperms()
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $file Path to the file.
    #// @return string Mode of the file (the last 3 digits).
    #//
    def getchmod(self, file=None):
        
        return php_substr(decoct(php_no_error(lambda: fileperms(file))), -3)
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
        
        gid = php_no_error(lambda: filegroup(file))
        if (not gid):
            return False
        # end if
        if (not php_function_exists("posix_getgrgid")):
            return gid
        # end if
        grouparray = posix_getgrgid(gid)
        return grouparray["name"]
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
        rtval = copy(source, destination)
        if mode:
            self.chmod(destination, mode)
        # end if
        return rtval
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
        
        if (not overwrite) and self.exists(destination):
            return False
        # end if
        #// Try using rename first. if that fails (for example, source is read only) try copy.
        if php_no_error(lambda: rename(source, destination)):
            return True
        # end if
        if self.copy(source, destination, overwrite) and self.exists(destination):
            self.delete(source)
            return True
        else:
            return False
        # end if
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
            #// Some filesystems report this as /, which can cause non-expected recursive deletion of all files in the filesystem.
            return False
        # end if
        file = php_str_replace("\\", "/", file)
        #// For Win32, occasional problems deleting files otherwise.
        if "f" == type or self.is_file(file):
            return php_no_error(lambda: unlink(file))
        # end if
        if (not recursive) and self.is_dir(file):
            return php_no_error(lambda: rmdir(file))
        # end if
        #// At this point it's a folder, and we're in recursive mode.
        file = trailingslashit(file)
        filelist = self.dirlist(file, True)
        retval = True
        if php_is_array(filelist):
            for filename,fileinfo in filelist:
                if (not self.delete(file + filename, recursive, fileinfo["type"])):
                    retval = False
                # end if
            # end for
        # end if
        if php_file_exists(file) and (not php_no_error(lambda: rmdir(file))):
            retval = False
        # end if
        return retval
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
        
        return php_no_error(lambda: php_file_exists(file))
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
        
        return php_no_error(lambda: php_is_file(file))
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
        
        return php_no_error(lambda: php_is_dir(path))
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
        
        return php_no_error(lambda: php_is_readable(file))
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
        
        return php_no_error(lambda: php_is_writable(file))
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
        
        return php_no_error(lambda: fileatime(file))
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
        
        return php_no_error(lambda: filemtime(file))
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
        
        return php_no_error(lambda: filesize(file))
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
        
        if 0 == time:
            time = time()
        # end if
        if 0 == atime:
            atime = time()
        # end if
        return touch(file, time, atime)
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
        
        #// Safe mode fails with a trailing slash under certain PHP versions.
        path = untrailingslashit(path)
        if php_empty(lambda : path):
            return False
        # end if
        if (not chmod):
            chmod = FS_CHMOD_DIR
        # end if
        if (not php_no_error(lambda: mkdir(path))):
            return False
        # end if
        self.chmod(path, chmod)
        if chown:
            self.chown(path, chown)
        # end if
        if chgrp:
            self.chgrp(path, chgrp)
        # end if
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
    def dirlist(self, path=None, include_hidden=True, recursive=False):
        
        if self.is_file(path):
            limit_file = php_basename(path)
            path = php_dirname(path)
        else:
            limit_file = False
        # end if
        if (not self.is_dir(path)) or (not self.is_readable(path)):
            return False
        # end if
        dir = dir(path)
        if (not dir):
            return False
        # end if
        ret = Array()
        while True:
            entry = dir.read()
            if not (False != entry):
                break
            # end if
            struc = Array()
            struc["name"] = entry
            if "." == struc["name"] or ".." == struc["name"]:
                continue
            # end if
            if (not include_hidden) and "." == struc["name"][0]:
                continue
            # end if
            if limit_file and struc["name"] != limit_file:
                continue
            # end if
            struc["perms"] = self.gethchmod(path + "/" + entry)
            struc["permsn"] = self.getnumchmodfromh(struc["perms"])
            struc["number"] = False
            struc["owner"] = self.owner(path + "/" + entry)
            struc["group"] = self.group(path + "/" + entry)
            struc["size"] = self.size(path + "/" + entry)
            struc["lastmodunix"] = self.mtime(path + "/" + entry)
            struc["lastmod"] = gmdate("M j", struc["lastmodunix"])
            struc["time"] = gmdate("h:i:s", struc["lastmodunix"])
            struc["type"] = "d" if self.is_dir(path + "/" + entry) else "f"
            if "d" == struc["type"]:
                if recursive:
                    struc["files"] = self.dirlist(path + "/" + struc["name"], include_hidden, recursive)
                else:
                    struc["files"] = Array()
                # end if
            # end if
            ret[struc["name"]] = struc
        # end while
        dir.close()
        dir = None
        return ret
    # end def dirlist
# end class WP_Filesystem_Direct
