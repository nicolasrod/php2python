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
#// WordPress Filesystem Class for implementing SSH2
#// 
#// To use this class you must follow these steps for PHP 5.2.6+
#// 
#// @contrib http://kevin.vanzonneveld.net/techblog/article/make_ssh_connections_with_php/ - Installation Notes
#// 
#// Complie libssh2 (Note: Only 0.14 is officaly working with PHP 5.2.6+ right now, But many users have found the latest versions work)
#// 
#// cd /usr/src
#// wget https://www.libssh2.org/download/libssh2-0.14.tar.gz
#// tar -zxvf libssh2-0.14.tar.gz
#// cd libssh2-0.14
#// ./configure
#// make all install
#// 
#// Note: Do not leave the directory yet!
#// 
#// Enter: pecl install -f ssh2
#// 
#// Copy the ssh.so file it creates to your PHP Module Directory.
#// Open up your PHP.INI file and look for where extensions are placed.
#// Add in your PHP.ini file: extension=ssh2.so
#// 
#// Restart Apache!
#// Check phpinfo() streams to confirm that: ssh2.shell, ssh2.exec, ssh2.tunnel, ssh2.scp, ssh2.sftp  exist.
#// 
#// Note: as of WordPress 2.8, This utilises the PHP5+ function 'stream_get_contents'
#// 
#// @since 2.7.0
#// 
#// @package WordPress
#// @subpackage Filesystem
#//
class WP_Filesystem_SSH2(WP_Filesystem_Base):
    #// 
    #// @since 2.7.0
    #// @var resource
    #//
    link = False
    #// 
    #// @since 2.7.0
    #// @var resource
    #//
    sftp_link = Array()
    #// 
    #// @since 2.7.0
    #// @var bool
    #//
    keys = False
    #// 
    #// Constructor.
    #// 
    #// @since 2.7.0
    #// 
    #// @param array $opt
    #//
    def __init__(self, opt_=""):
        
        
        self.method = "ssh2"
        self.errors = php_new_class("WP_Error", lambda : WP_Error())
        #// Check if possible to use ssh2 functions.
        if (not php_extension_loaded("ssh2")):
            self.errors.add("no_ssh2_ext", __("The ssh2 PHP extension is not available"))
            return
        # end if
        if (not php_function_exists("stream_get_contents")):
            self.errors.add("ssh2_php_requirement", php_sprintf(__("The ssh2 PHP extension is available, however, we require the PHP5 function %s"), "<code>stream_get_contents()</code>"))
            return
        # end if
        #// Set defaults:
        if php_empty(lambda : opt_["port"]):
            self.options["port"] = 22
        else:
            self.options["port"] = opt_["port"]
        # end if
        if php_empty(lambda : opt_["hostname"]):
            self.errors.add("empty_hostname", __("SSH2 hostname is required"))
        else:
            self.options["hostname"] = opt_["hostname"]
        # end if
        #// Check if the options provided are OK.
        if (not php_empty(lambda : opt_["public_key"])) and (not php_empty(lambda : opt_["private_key"])):
            self.options["public_key"] = opt_["public_key"]
            self.options["private_key"] = opt_["private_key"]
            self.options["hostkey"] = Array({"hostkey": "ssh-rsa"})
            self.keys = True
        elif php_empty(lambda : opt_["username"]):
            self.errors.add("empty_username", __("SSH2 username is required"))
        # end if
        if (not php_empty(lambda : opt_["username"])):
            self.options["username"] = opt_["username"]
        # end if
        if php_empty(lambda : opt_["password"]):
            #// Password can be blank if we are using keys.
            if (not self.keys):
                self.errors.add("empty_password", __("SSH2 password is required"))
            # end if
        else:
            self.options["password"] = opt_["password"]
        # end if
    # end def __init__
    #// 
    #// Connects filesystem.
    #// 
    #// @since 2.7.0
    #// 
    #// @return bool True on success, false on failure.
    #//
    def connect(self):
        
        
        if (not self.keys):
            self.link = php_no_error(lambda: ssh2_connect(self.options["hostname"], self.options["port"]))
        else:
            self.link = php_no_error(lambda: ssh2_connect(self.options["hostname"], self.options["port"], self.options["hostkey"]))
        # end if
        if (not self.link):
            self.errors.add("connect", php_sprintf(__("Failed to connect to SSH2 Server %s"), self.options["hostname"] + ":" + self.options["port"]))
            return False
        # end if
        if (not self.keys):
            if (not php_no_error(lambda: ssh2_auth_password(self.link, self.options["username"], self.options["password"]))):
                self.errors.add("auth", php_sprintf(__("Username/Password incorrect for %s"), self.options["username"]))
                return False
            # end if
        else:
            if (not php_no_error(lambda: ssh2_auth_pubkey_file(self.link, self.options["username"], self.options["public_key"], self.options["private_key"], self.options["password"]))):
                self.errors.add("auth", php_sprintf(__("Public and Private keys incorrect for %s"), self.options["username"]))
                return False
            # end if
        # end if
        self.sftp_link = ssh2_sftp(self.link)
        if (not self.sftp_link):
            self.errors.add("connect", php_sprintf(__("Failed to initialize a SFTP subsystem session with the SSH2 Server %s"), self.options["hostname"] + ":" + self.options["port"]))
            return False
        # end if
        return True
    # end def connect
    #// 
    #// Gets the ssh2.sftp PHP stream wrapper path to open for the given file.
    #// 
    #// This method also works around a PHP bug where the root directory (/) cannot
    #// be opened by PHP functions, causing a false failure. In order to work around
    #// this, the path is converted to /./ which is semantically the same as
    #// See https://bugs.php.net/bug.php?id=64169 for more details.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $path The File/Directory path on the remote server to return
    #// @return string The ssh2.sftp:// wrapped path to use.
    #//
    def sftp_path(self, path_=None):
        
        
        if "/" == path_:
            path_ = "/./"
        # end if
        return "ssh2.sftp://" + self.sftp_link + "/" + php_ltrim(path_, "/")
    # end def sftp_path
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $command
    #// @param bool $returnbool
    #// @return bool|string True on success, false on failure. String if the command was executed, `$returnbool`
    #// is false (default), and data from the resulting stream was retrieved.
    #//
    def run_command(self, command_=None, returnbool_=None):
        if returnbool_ is None:
            returnbool_ = False
        # end if
        
        if (not self.link):
            return False
        # end if
        stream_ = ssh2_exec(self.link, command_)
        if (not stream_):
            self.errors.add("command", php_sprintf(__("Unable to perform command: %s"), command_))
        else:
            stream_set_blocking(stream_, True)
            stream_set_timeout(stream_, FS_TIMEOUT)
            data_ = stream_get_contents(stream_)
            php_fclose(stream_)
            if returnbool_:
                return False if False == data_ else "" != php_trim(data_)
            else:
                return data_
            # end if
        # end if
        return False
    # end def run_command
    #// 
    #// Reads entire file into a string.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $file Name of the file to read.
    #// @return string|false Read data on success, false if no temporary file could be opened,
    #// or if the file couldn't be retrieved.
    #//
    def get_contents(self, file_=None):
        
        
        return php_file_get_contents(self.sftp_path(file_))
    # end def get_contents
    #// 
    #// Reads entire file into an array.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $file Path to the file.
    #// @return array|false File contents in an array on success, false on failure.
    #//
    def get_contents_array(self, file_=None):
        
        
        return file(self.sftp_path(file_))
    # end def get_contents_array
    #// 
    #// Writes a string to a file.
    #// 
    #// @since 2.7.0
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
        
        ret_ = file_put_contents(self.sftp_path(file_), contents_)
        if php_strlen(contents_) != ret_:
            return False
        # end if
        self.chmod(file_, mode_)
        return True
    # end def put_contents
    #// 
    #// Gets the current working directory.
    #// 
    #// @since 2.7.0
    #// 
    #// @return string|false The current working directory on success, false on failure.
    #//
    def cwd(self):
        
        
        cwd_ = ssh2_sftp_realpath(self.sftp_link, ".")
        if cwd_:
            cwd_ = trailingslashit(php_trim(cwd_))
        # end if
        return cwd_
    # end def cwd
    #// 
    #// Changes current directory.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $dir The new current directory.
    #// @return bool True on success, false on failure.
    #//
    def chdir(self, dir_=None):
        
        
        return self.run_command("cd " + dir_, True)
    # end def chdir
    #// 
    #// Changes the file group.
    #// 
    #// @since 2.7.0
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
        if (not recursive_) or (not self.is_dir(file_)):
            return self.run_command(php_sprintf("chgrp %s %s", escapeshellarg(group_), escapeshellarg(file_)), True)
        # end if
        return self.run_command(php_sprintf("chgrp -R %s %s", escapeshellarg(group_), escapeshellarg(file_)), True)
    # end def chgrp
    #// 
    #// Changes filesystem permissions.
    #// 
    #// @since 2.7.0
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
        
        if (not self.exists(file_)):
            return False
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
            return self.run_command(php_sprintf("chmod %o %s", mode_, escapeshellarg(file_)), True)
        # end if
        return self.run_command(php_sprintf("chmod -R %o %s", mode_, escapeshellarg(file_)), True)
    # end def chmod
    #// 
    #// Changes the owner of a file or directory.
    #// 
    #// @since 2.7.0
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
        if (not recursive_) or (not self.is_dir(file_)):
            return self.run_command(php_sprintf("chown %s %s", escapeshellarg(owner_), escapeshellarg(file_)), True)
        # end if
        return self.run_command(php_sprintf("chown -R %s %s", escapeshellarg(owner_), escapeshellarg(file_)), True)
    # end def chown
    #// 
    #// Gets the file owner.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $file Path to the file.
    #// @return string|false Username of the owner on success, false on failure.
    #//
    def owner(self, file_=None):
        
        
        owneruid_ = php_no_error(lambda: fileowner(self.sftp_path(file_)))
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
    #// @since 2.7.0
    #// 
    #// @param string $file Path to the file.
    #// @return string Mode of the file (the last 3 digits).
    #//
    def getchmod(self, file_=None):
        
        
        return php_substr(decoct(php_no_error(lambda: fileperms(self.sftp_path(file_)))), -3)
    # end def getchmod
    #// 
    #// Gets the file's group.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $file Path to the file.
    #// @return string|false The group on success, false on failure.
    #//
    def group(self, file_=None):
        
        
        gid_ = php_no_error(lambda: filegroup(self.sftp_path(file_)))
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
    #// @since 2.7.0
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
    #// @since 2.7.0
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
        
        if self.exists(destination_):
            if overwrite_:
                #// We need to remove the destination file before we can rename the source.
                self.delete(destination_, False, "f")
            else:
                #// If we're not overwriting, the rename will fail, so return early.
                return False
            # end if
        # end if
        return ssh2_sftp_rename(self.sftp_link, source_, destination_)
    # end def move
    #// 
    #// Deletes a file or directory.
    #// 
    #// @since 2.7.0
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
        
        if "f" == type_ or self.is_file(file_):
            return ssh2_sftp_unlink(self.sftp_link, file_)
        # end if
        if (not recursive_):
            return ssh2_sftp_rmdir(self.sftp_link, file_)
        # end if
        filelist_ = self.dirlist(file_)
        if php_is_array(filelist_):
            for filename_,fileinfo_ in filelist_.items():
                self.delete(file_ + "/" + filename_, recursive_, fileinfo_["type"])
            # end for
        # end if
        return ssh2_sftp_rmdir(self.sftp_link, file_)
    # end def delete
    #// 
    #// Checks if a file or directory exists.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $file Path to file or directory.
    #// @return bool Whether $file exists or not.
    #//
    def exists(self, file_=None):
        
        
        return php_file_exists(self.sftp_path(file_))
    # end def exists
    #// 
    #// Checks if resource is a file.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $file File path.
    #// @return bool Whether $file is a file.
    #//
    def is_file(self, file_=None):
        
        
        return php_is_file(self.sftp_path(file_))
    # end def is_file
    #// 
    #// Checks if resource is a directory.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $path Directory path.
    #// @return bool Whether $path is a directory.
    #//
    def is_dir(self, path_=None):
        
        
        return php_is_dir(self.sftp_path(path_))
    # end def is_dir
    #// 
    #// Checks if a file is readable.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $file Path to file.
    #// @return bool Whether $file is readable.
    #//
    def is_readable(self, file_=None):
        
        
        return php_is_readable(self.sftp_path(file_))
    # end def is_readable
    #// 
    #// Checks if a file or directory is writable.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $file Path to file or directory.
    #// @return bool Whether $file is writable.
    #//
    def is_writable(self, file_=None):
        
        
        #// PHP will base its writable checks on system_user === file_owner, not ssh_user === file_owner.
        return True
    # end def is_writable
    #// 
    #// Gets the file's last access time.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $file Path to file.
    #// @return int|false Unix timestamp representing last access time, false on failure.
    #//
    def atime(self, file_=None):
        
        
        return fileatime(self.sftp_path(file_))
    # end def atime
    #// 
    #// Gets the file modification time.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $file Path to file.
    #// @return int|false Unix timestamp representing modification time, false on failure.
    #//
    def mtime(self, file_=None):
        
        
        return filemtime(self.sftp_path(file_))
    # end def mtime
    #// 
    #// Gets the file size (in bytes).
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $file Path to file.
    #// @return int|false Size of the file in bytes on success, false on failure.
    #//
    def size(self, file_=None):
        
        
        return filesize(self.sftp_path(file_))
    # end def size
    #// 
    #// Sets the access and modification times of a file.
    #// 
    #// Note: Not implemented.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $file  Path to file.
    #// @param int    $time  Optional. Modified time to set for file.
    #// Default 0.
    #// @param int    $atime Optional. Access time to set for file.
    #// Default 0.
    #//
    def touch(self, file_=None, time_=0, atime_=0):
        
        
        pass
    # end def touch
    #// 
    #// Creates a directory.
    #// 
    #// @since 2.7.0
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
        if (not chmod_):
            chmod_ = FS_CHMOD_DIR
        # end if
        if (not ssh2_sftp_mkdir(self.sftp_link, path_, chmod_, True)):
            return False
        # end if
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
    #// @since 2.7.0
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
    #// @since 2.7.0
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
        ret_ = Array()
        dir_ = dir(self.sftp_path(path_))
        if (not dir_):
            return False
        # end if
        while True:
            entry_ = dir_.read()
            if not (False != entry_):
                break
            # end if
            struc_ = Array()
            struc_["name"] = entry_
            if "." == struc_["name"] or ".." == struc_["name"]:
                continue
                pass
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
# end class WP_Filesystem_SSH2
