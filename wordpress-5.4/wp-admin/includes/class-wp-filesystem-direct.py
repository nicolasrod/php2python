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
    def __init__(self, arg_=None):
        
        
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
    def get_contents(self, file_=None):
        
        
        return php_no_error(lambda: php_file_get_contents(file_))
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
        
        
        return php_no_error(lambda: file(file_))
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
        
        fp_ = php_no_error(lambda: fopen(file_, "wb"))
        if (not fp_):
            return False
        # end if
        mbstring_binary_safe_encoding()
        data_length_ = php_strlen(contents_)
        bytes_written_ = fwrite(fp_, contents_)
        reset_mbstring_encoding()
        php_fclose(fp_)
        if data_length_ != bytes_written_:
            return False
        # end if
        self.chmod(file_, mode_)
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
    def chdir(self, dir_=None):
        
        
        return php_no_error(lambda: php_chdir(dir_))
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
    def chgrp(self, file_=None, group_=None, recursive_=None):
        if recursive_ is None:
            recursive_ = False
        # end if
        
        if (not self.exists(file_)):
            return False
        # end if
        if (not recursive_):
            return chgrp(file_, group_)
        # end if
        if (not self.is_dir(file_)):
            return chgrp(file_, group_)
        # end if
        #// Is a directory, and we want recursive.
        file_ = trailingslashit(file_)
        filelist_ = self.dirlist(file_)
        for filename_ in filelist_:
            self.chgrp(file_ + filename_, group_, recursive_)
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
        if (not recursive_) or (not self.is_dir(file_)):
            return chmod(file_, mode_)
        # end if
        #// Is a directory, and we want recursive.
        file_ = trailingslashit(file_)
        filelist_ = self.dirlist(file_)
        for filename_,filemeta_ in filelist_.items():
            self.chmod(file_ + filename_, mode_, recursive_)
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
    def chown(self, file_=None, owner_=None, recursive_=None):
        if recursive_ is None:
            recursive_ = False
        # end if
        
        if (not self.exists(file_)):
            return False
        # end if
        if (not recursive_):
            return chown(file_, owner_)
        # end if
        if (not self.is_dir(file_)):
            return chown(file_, owner_)
        # end if
        #// Is a directory, and we want recursive.
        filelist_ = self.dirlist(file_)
        for filename_ in filelist_:
            self.chown(file_ + "/" + filename_, owner_, recursive_)
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
    def owner(self, file_=None):
        
        
        owneruid_ = php_no_error(lambda: fileowner(file_))
        if (not owneruid_):
            return False
        # end if
        if (not php_function_exists("posix_getpwuid")):
            return owneruid_
        # end if
        ownerarray_ = posix_getpwuid(owneruid_)
        return ownerarray_["name"]
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
    def getchmod(self, file_=None):
        
        
        return php_substr(decoct(php_no_error(lambda: fileperms(file_))), -3)
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
        
        
        gid_ = php_no_error(lambda: filegroup(file_))
        if (not gid_):
            return False
        # end if
        if (not php_function_exists("posix_getgrgid")):
            return gid_
        # end if
        grouparray_ = posix_getgrgid(gid_)
        return grouparray_["name"]
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
        rtval_ = copy(source_, destination_)
        if mode_:
            self.chmod(destination_, mode_)
        # end if
        return rtval_
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
        
        if (not overwrite_) and self.exists(destination_):
            return False
        # end if
        #// Try using rename first. if that fails (for example, source is read only) try copy.
        if php_no_error(lambda: rename(source_, destination_)):
            return True
        # end if
        if self.copy(source_, destination_, overwrite_) and self.exists(destination_):
            self.delete(source_)
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
    def delete(self, file_=None, recursive_=None, type_=None):
        if recursive_ is None:
            recursive_ = False
        # end if
        if type_ is None:
            type_ = False
        # end if
        
        if php_empty(lambda : file_):
            #// Some filesystems report this as /, which can cause non-expected recursive deletion of all files in the filesystem.
            return False
        # end if
        file_ = php_str_replace("\\", "/", file_)
        #// For Win32, occasional problems deleting files otherwise.
        if "f" == type_ or self.is_file(file_):
            return php_no_error(lambda: unlink(file_))
        # end if
        if (not recursive_) and self.is_dir(file_):
            return php_no_error(lambda: rmdir(file_))
        # end if
        #// At this point it's a folder, and we're in recursive mode.
        file_ = trailingslashit(file_)
        filelist_ = self.dirlist(file_, True)
        retval_ = True
        if php_is_array(filelist_):
            for filename_,fileinfo_ in filelist_.items():
                if (not self.delete(file_ + filename_, recursive_, fileinfo_["type"])):
                    retval_ = False
                # end if
            # end for
        # end if
        if php_file_exists(file_) and (not php_no_error(lambda: rmdir(file_))):
            retval_ = False
        # end if
        return retval_
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
        
        
        return php_no_error(lambda: php_file_exists(file_))
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
        
        
        return php_no_error(lambda: php_is_file(file_))
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
        
        
        return php_no_error(lambda: php_is_dir(path_))
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
        
        
        return php_no_error(lambda: php_is_readable(file_))
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
        
        
        return php_no_error(lambda: php_is_writable(file_))
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
        
        
        return php_no_error(lambda: fileatime(file_))
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
        
        
        return php_no_error(lambda: filemtime(file_))
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
        
        
        return php_no_error(lambda: filesize(file_))
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
        
        
        if 0 == time_:
            time_ = time()
        # end if
        if 0 == atime_:
            atime_ = time()
        # end if
        return touch(file_, time_, atime_)
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
        
        #// Safe mode fails with a trailing slash under certain PHP versions.
        path_ = untrailingslashit(path_)
        if php_empty(lambda : path_):
            return False
        # end if
        if (not chmod_):
            chmod_ = FS_CHMOD_DIR
        # end if
        if (not php_no_error(lambda: mkdir(path_))):
            return False
        # end if
        self.chmod(path_, chmod_)
        if chown_:
            self.chown(path_, chown_)
        # end if
        if chgrp_:
            self.chgrp(path_, chgrp_)
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
    def dirlist(self, path_=None, include_hidden_=None, recursive_=None):
        if include_hidden_ is None:
            include_hidden_ = True
        # end if
        if recursive_ is None:
            recursive_ = False
        # end if
        
        if self.is_file(path_):
            limit_file_ = php_basename(path_)
            path_ = php_dirname(path_)
        else:
            limit_file_ = False
        # end if
        if (not self.is_dir(path_)) or (not self.is_readable(path_)):
            return False
        # end if
        dir_ = dir(path_)
        if (not dir_):
            return False
        # end if
        ret_ = Array()
        while True:
            entry_ = dir_.read()
            if not (False != entry_):
                break
            # end if
            struc_ = Array()
            struc_["name"] = entry_
            if "." == struc_["name"] or ".." == struc_["name"]:
                continue
            # end if
            if (not include_hidden_) and "." == struc_["name"][0]:
                continue
            # end if
            if limit_file_ and struc_["name"] != limit_file_:
                continue
            # end if
            struc_["perms"] = self.gethchmod(path_ + "/" + entry_)
            struc_["permsn"] = self.getnumchmodfromh(struc_["perms"])
            struc_["number"] = False
            struc_["owner"] = self.owner(path_ + "/" + entry_)
            struc_["group"] = self.group(path_ + "/" + entry_)
            struc_["size"] = self.size(path_ + "/" + entry_)
            struc_["lastmodunix"] = self.mtime(path_ + "/" + entry_)
            struc_["lastmod"] = gmdate("M j", struc_["lastmodunix"])
            struc_["time"] = gmdate("h:i:s", struc_["lastmodunix"])
            struc_["type"] = "d" if self.is_dir(path_ + "/" + entry_) else "f"
            if "d" == struc_["type"]:
                if recursive_:
                    struc_["files"] = self.dirlist(path_ + "/" + struc_["name"], include_hidden_, recursive_)
                else:
                    struc_["files"] = Array()
                # end if
            # end if
            ret_[struc_["name"]] = struc_
        # end while
        dir_.close()
        dir_ = None
        return ret_
    # end def dirlist
# end class WP_Filesystem_Direct
