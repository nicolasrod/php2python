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
    link = False
    sftp_link = Array()
    keys = False
    #// 
    #// Constructor.
    #// 
    #// @since 2.7.0
    #// 
    #// @param array $opt
    #//
    def __init__(self, opt=""):
        
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
        if php_empty(lambda : opt["port"]):
            self.options["port"] = 22
        else:
            self.options["port"] = opt["port"]
        # end if
        if php_empty(lambda : opt["hostname"]):
            self.errors.add("empty_hostname", __("SSH2 hostname is required"))
        else:
            self.options["hostname"] = opt["hostname"]
        # end if
        #// Check if the options provided are OK.
        if (not php_empty(lambda : opt["public_key"])) and (not php_empty(lambda : opt["private_key"])):
            self.options["public_key"] = opt["public_key"]
            self.options["private_key"] = opt["private_key"]
            self.options["hostkey"] = Array({"hostkey": "ssh-rsa"})
            self.keys = True
        elif php_empty(lambda : opt["username"]):
            self.errors.add("empty_username", __("SSH2 username is required"))
        # end if
        if (not php_empty(lambda : opt["username"])):
            self.options["username"] = opt["username"]
        # end if
        if php_empty(lambda : opt["password"]):
            #// Password can be blank if we are using keys.
            if (not self.keys):
                self.errors.add("empty_password", __("SSH2 password is required"))
            # end if
        else:
            self.options["password"] = opt["password"]
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
    def sftp_path(self, path=None):
        
        if "/" == path:
            path = "/./"
        # end if
        return "ssh2.sftp://" + self.sftp_link + "/" + php_ltrim(path, "/")
    # end def sftp_path
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $command
    #// @param bool $returnbool
    #// @return bool|string True on success, false on failure. String if the command was executed, `$returnbool`
    #// is false (default), and data from the resulting stream was retrieved.
    #//
    def run_command(self, command=None, returnbool=False):
        
        if (not self.link):
            return False
        # end if
        stream = ssh2_exec(self.link, command)
        if (not stream):
            self.errors.add("command", php_sprintf(__("Unable to perform command: %s"), command))
        else:
            stream_set_blocking(stream, True)
            stream_set_timeout(stream, FS_TIMEOUT)
            data = stream_get_contents(stream)
            php_fclose(stream)
            if returnbool:
                return False if False == data else "" != php_trim(data)
            else:
                return data
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
    def get_contents(self, file=None):
        
        return php_file_get_contents(self.sftp_path(file))
    # end def get_contents
    #// 
    #// Reads entire file into an array.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $file Path to the file.
    #// @return array|false File contents in an array on success, false on failure.
    #//
    def get_contents_array(self, file=None):
        
        return file(self.sftp_path(file))
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
    def put_contents(self, file=None, contents=None, mode=False):
        
        ret = file_put_contents(self.sftp_path(file), contents)
        if php_strlen(contents) != ret:
            return False
        # end if
        self.chmod(file, mode)
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
        
        cwd = ssh2_sftp_realpath(self.sftp_link, ".")
        if cwd:
            cwd = trailingslashit(php_trim(cwd))
        # end if
        return cwd
    # end def cwd
    #// 
    #// Changes current directory.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $dir The new current directory.
    #// @return bool True on success, false on failure.
    #//
    def chdir(self, dir=None):
        
        return self.run_command("cd " + dir, True)
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
    def chgrp(self, file=None, group=None, recursive=False):
        
        if (not self.exists(file)):
            return False
        # end if
        if (not recursive) or (not self.is_dir(file)):
            return self.run_command(php_sprintf("chgrp %s %s", escapeshellarg(group), escapeshellarg(file)), True)
        # end if
        return self.run_command(php_sprintf("chgrp -R %s %s", escapeshellarg(group), escapeshellarg(file)), True)
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
    def chmod(self, file=None, mode=False, recursive=False):
        
        if (not self.exists(file)):
            return False
        # end if
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
            return self.run_command(php_sprintf("chmod %o %s", mode, escapeshellarg(file)), True)
        # end if
        return self.run_command(php_sprintf("chmod -R %o %s", mode, escapeshellarg(file)), True)
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
    def chown(self, file=None, owner=None, recursive=False):
        
        if (not self.exists(file)):
            return False
        # end if
        if (not recursive) or (not self.is_dir(file)):
            return self.run_command(php_sprintf("chown %s %s", escapeshellarg(owner), escapeshellarg(file)), True)
        # end if
        return self.run_command(php_sprintf("chown -R %s %s", escapeshellarg(owner), escapeshellarg(file)), True)
    # end def chown
    #// 
    #// Gets the file owner.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $file Path to the file.
    #// @return string|false Username of the owner on success, false on failure.
    #//
    def owner(self, file=None):
        
        owneruid = php_no_error(lambda: fileowner(self.sftp_path(file)))
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
    #// @since 2.7.0
    #// 
    #// @param string $file Path to the file.
    #// @return string Mode of the file (the last 3 digits).
    #//
    def getchmod(self, file=None):
        
        return php_substr(decoct(php_no_error(lambda: fileperms(self.sftp_path(file)))), -3)
    # end def getchmod
    #// 
    #// Gets the file's group.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $file Path to the file.
    #// @return string|false The group on success, false on failure.
    #//
    def group(self, file=None):
        
        gid = php_no_error(lambda: filegroup(self.sftp_path(file)))
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
    #// @since 2.7.0
    #// 
    #// @param string $source      Path to the source file.
    #// @param string $destination Path to the destination file.
    #// @param bool   $overwrite   Optional. Whether to overwrite the destination file if it exists.
    #// Default false.
    #// @return bool True on success, false on failure.
    #//
    def move(self, source=None, destination=None, overwrite=False):
        
        if self.exists(destination):
            if overwrite:
                #// We need to remove the destination file before we can rename the source.
                self.delete(destination, False, "f")
            else:
                #// If we're not overwriting, the rename will fail, so return early.
                return False
            # end if
        # end if
        return ssh2_sftp_rename(self.sftp_link, source, destination)
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
    def delete(self, file=None, recursive=False, type=False):
        
        if "f" == type or self.is_file(file):
            return ssh2_sftp_unlink(self.sftp_link, file)
        # end if
        if (not recursive):
            return ssh2_sftp_rmdir(self.sftp_link, file)
        # end if
        filelist = self.dirlist(file)
        if php_is_array(filelist):
            for filename,fileinfo in filelist:
                self.delete(file + "/" + filename, recursive, fileinfo["type"])
            # end for
        # end if
        return ssh2_sftp_rmdir(self.sftp_link, file)
    # end def delete
    #// 
    #// Checks if a file or directory exists.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $file Path to file or directory.
    #// @return bool Whether $file exists or not.
    #//
    def exists(self, file=None):
        
        return php_file_exists(self.sftp_path(file))
    # end def exists
    #// 
    #// Checks if resource is a file.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $file File path.
    #// @return bool Whether $file is a file.
    #//
    def is_file(self, file=None):
        
        return php_is_file(self.sftp_path(file))
    # end def is_file
    #// 
    #// Checks if resource is a directory.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $path Directory path.
    #// @return bool Whether $path is a directory.
    #//
    def is_dir(self, path=None):
        
        return php_is_dir(self.sftp_path(path))
    # end def is_dir
    #// 
    #// Checks if a file is readable.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $file Path to file.
    #// @return bool Whether $file is readable.
    #//
    def is_readable(self, file=None):
        
        return php_is_readable(self.sftp_path(file))
    # end def is_readable
    #// 
    #// Checks if a file or directory is writable.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $file Path to file or directory.
    #// @return bool Whether $file is writable.
    #//
    def is_writable(self, file=None):
        
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
    def atime(self, file=None):
        
        return fileatime(self.sftp_path(file))
    # end def atime
    #// 
    #// Gets the file modification time.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $file Path to file.
    #// @return int|false Unix timestamp representing modification time, false on failure.
    #//
    def mtime(self, file=None):
        
        return filemtime(self.sftp_path(file))
    # end def mtime
    #// 
    #// Gets the file size (in bytes).
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $file Path to file.
    #// @return int|false Size of the file in bytes on success, false on failure.
    #//
    def size(self, file=None):
        
        return filesize(self.sftp_path(file))
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
    def touch(self, file=None, time=0, atime=0):
        
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
    def mkdir(self, path=None, chmod=False, chown=False, chgrp=False):
        
        path = untrailingslashit(path)
        if php_empty(lambda : path):
            return False
        # end if
        if (not chmod):
            chmod = FS_CHMOD_DIR
        # end if
        if (not ssh2_sftp_mkdir(self.sftp_link, path, chmod, True)):
            return False
        # end if
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
    #// @since 2.7.0
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
        ret = Array()
        dir = dir(self.sftp_path(path))
        if (not dir):
            return False
        # end if
        while True:
            entry = dir.read()
            if not (False != entry):
                break
            # end if
            struc = Array()
            struc["name"] = entry
            if "." == struc["name"] or ".." == struc["name"]:
                continue
                pass
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
# end class WP_Filesystem_SSH2
