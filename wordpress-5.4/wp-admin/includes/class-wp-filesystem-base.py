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
#// Base WordPress Filesystem
#// 
#// @package WordPress
#// @subpackage Filesystem
#// 
#// 
#// Base WordPress Filesystem class which Filesystem implementations extend.
#// 
#// @since 2.5.0
#//
class WP_Filesystem_Base():
    #// 
    #// Whether to display debug data for the connection.
    #// 
    #// @since 2.5.0
    #// @var bool
    #//
    verbose = False
    #// 
    #// Cached list of local filepaths to mapped remote filepaths.
    #// 
    #// @since 2.7.0
    #// @var array
    #//
    cache = Array()
    #// 
    #// The Access method of the current connection, Set automatically.
    #// 
    #// @since 2.5.0
    #// @var string
    #//
    method = ""
    #// 
    #// @var WP_Error
    #//
    errors = None
    #// 
    #//
    options = Array()
    #// 
    #// Returns the path on the remote filesystem of ABSPATH.
    #// 
    #// @since 2.7.0
    #// 
    #// @return string The location of the remote path.
    #//
    def abspath(self):
        
        
        folder_ = self.find_folder(ABSPATH)
        #// Perhaps the FTP folder is rooted at the WordPress install.
        #// Check for wp-includes folder in root. Could have some false positives, but rare.
        if (not folder_) and self.is_dir("/" + WPINC):
            folder_ = "/"
        # end if
        return folder_
    # end def abspath
    #// 
    #// Returns the path on the remote filesystem of WP_CONTENT_DIR.
    #// 
    #// @since 2.7.0
    #// 
    #// @return string The location of the remote path.
    #//
    def wp_content_dir(self):
        
        
        return self.find_folder(WP_CONTENT_DIR)
    # end def wp_content_dir
    #// 
    #// Returns the path on the remote filesystem of WP_PLUGIN_DIR.
    #// 
    #// @since 2.7.0
    #// 
    #// @return string The location of the remote path.
    #//
    def wp_plugins_dir(self):
        
        
        return self.find_folder(WP_PLUGIN_DIR)
    # end def wp_plugins_dir
    #// 
    #// Returns the path on the remote filesystem of the Themes Directory.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string|false $theme Optional. The theme stylesheet or template for the directory.
    #// Default false.
    #// @return string The location of the remote path.
    #//
    def wp_themes_dir(self, theme_=None):
        if theme_ is None:
            theme_ = False
        # end if
        
        theme_root_ = get_theme_root(theme_)
        #// Account for relative theme roots.
        if "/themes" == theme_root_ or (not php_is_dir(theme_root_)):
            theme_root_ = WP_CONTENT_DIR + theme_root_
        # end if
        return self.find_folder(theme_root_)
    # end def wp_themes_dir
    #// 
    #// Returns the path on the remote filesystem of WP_LANG_DIR.
    #// 
    #// @since 3.2.0
    #// 
    #// @return string The location of the remote path.
    #//
    def wp_lang_dir(self):
        
        
        return self.find_folder(WP_LANG_DIR)
    # end def wp_lang_dir
    #// 
    #// Locates a folder on the remote filesystem.
    #// 
    #// @since 2.5.0
    #// @deprecated 2.7.0 use WP_Filesystem::abspath() or WP_Filesystem::wp_*_dir() instead.
    #// @see WP_Filesystem::abspath()
    #// @see WP_Filesystem::wp_content_dir()
    #// @see WP_Filesystem::wp_plugins_dir()
    #// @see WP_Filesystem::wp_themes_dir()
    #// @see WP_Filesystem::wp_lang_dir()
    #// 
    #// @param string $base The folder to start searching from.
    #// @param bool   $echo True to display debug information.
    #// Default false.
    #// @return string The location of the remote path.
    #//
    def find_base_dir(self, base_=".", echo_=None):
        if echo_ is None:
            echo_ = False
        # end if
        
        _deprecated_function(__FUNCTION__, "2.7.0", "WP_Filesystem::abspath() or WP_Filesystem::wp_*_dir()")
        self.verbose = echo_
        return self.abspath()
    # end def find_base_dir
    #// 
    #// Locates a folder on the remote filesystem.
    #// 
    #// @since 2.5.0
    #// @deprecated 2.7.0 use WP_Filesystem::abspath() or WP_Filesystem::wp_*_dir() methods instead.
    #// @see WP_Filesystem::abspath()
    #// @see WP_Filesystem::wp_content_dir()
    #// @see WP_Filesystem::wp_plugins_dir()
    #// @see WP_Filesystem::wp_themes_dir()
    #// @see WP_Filesystem::wp_lang_dir()
    #// 
    #// @param string $base The folder to start searching from.
    #// @param bool   $echo True to display debug information.
    #// @return string The location of the remote path.
    #//
    def get_base_dir(self, base_=".", echo_=None):
        if echo_ is None:
            echo_ = False
        # end if
        
        _deprecated_function(__FUNCTION__, "2.7.0", "WP_Filesystem::abspath() or WP_Filesystem::wp_*_dir()")
        self.verbose = echo_
        return self.abspath()
    # end def get_base_dir
    #// 
    #// Locates a folder on the remote filesystem.
    #// 
    #// Assumes that on Windows systems, Stripping off the Drive
    #// letter is OK Sanitizes \\ to / in Windows filepaths.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $folder the folder to locate.
    #// @return string|false The location of the remote path, false on failure.
    #//
    def find_folder(self, folder_=None):
        
        
        if (php_isset(lambda : self.cache[folder_])):
            return self.cache[folder_]
        # end if
        if php_stripos(self.method, "ftp") != False:
            constant_overrides_ = Array({"FTP_BASE": ABSPATH, "FTP_CONTENT_DIR": WP_CONTENT_DIR, "FTP_PLUGIN_DIR": WP_PLUGIN_DIR, "FTP_LANG_DIR": WP_LANG_DIR})
            #// Direct matches ( folder = CONSTANT/ ).
            for constant_,dir_ in constant_overrides_.items():
                if (not php_defined(constant_)):
                    continue
                # end if
                if folder_ == dir_:
                    return trailingslashit(constant(constant_))
                # end if
            # end for
            #// Prefix matches ( folder = CONSTANT/subdir ),
            for constant_,dir_ in constant_overrides_.items():
                if (not php_defined(constant_)):
                    continue
                # end if
                if 0 == php_stripos(folder_, dir_):
                    #// $folder starts with $dir.
                    potential_folder_ = php_preg_replace("#^" + preg_quote(dir_, "#") + "/#i", trailingslashit(constant(constant_)), folder_)
                    potential_folder_ = trailingslashit(potential_folder_)
                    if self.is_dir(potential_folder_):
                        self.cache[folder_] = potential_folder_
                        return potential_folder_
                    # end if
                # end if
            # end for
        elif "direct" == self.method:
            folder_ = php_str_replace("\\", "/", folder_)
            #// Windows path sanitisation.
            return trailingslashit(folder_)
        # end if
        folder_ = php_preg_replace("|^([a-z]{1}):|i", "", folder_)
        #// Strip out Windows drive letter if it's there.
        folder_ = php_str_replace("\\", "/", folder_)
        #// Windows path sanitisation.
        if (php_isset(lambda : self.cache[folder_])):
            return self.cache[folder_]
        # end if
        if self.exists(folder_):
            #// Folder exists at that absolute path.
            folder_ = trailingslashit(folder_)
            self.cache[folder_] = folder_
            return folder_
        # end if
        return_ = self.search_for_folder(folder_)
        if return_:
            self.cache[folder_] = return_
        # end if
        return return_
    # end def find_folder
    #// 
    #// Locates a folder on the remote filesystem.
    #// 
    #// Expects Windows sanitized path.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $folder The folder to locate.
    #// @param string $base   The folder to start searching from.
    #// @param bool   $loop   If the function has recursed. Internal use only.
    #// @return string|false The location of the remote path, false to cease looping.
    #//
    def search_for_folder(self, folder_=None, base_=".", loop_=None):
        if loop_ is None:
            loop_ = False
        # end if
        
        if php_empty(lambda : base_) or "." == base_:
            base_ = trailingslashit(self.cwd())
        # end if
        folder_ = untrailingslashit(folder_)
        if self.verbose:
            #// translators: 1: Folder to locate, 2: Folder to start searching from.
            printf("\n" + __("Looking for %1$s in %2$s") + "<br/>\n", folder_, base_)
        # end if
        folder_parts_ = php_explode("/", folder_)
        folder_part_keys_ = php_array_keys(folder_parts_)
        last_index_ = php_array_pop(folder_part_keys_)
        last_path_ = folder_parts_[last_index_]
        files_ = self.dirlist(base_)
        for index_,key_ in folder_parts_.items():
            if index_ == last_index_:
                continue
                pass
            # end if
            #// 
            #// Working from /home/ to /user/ to /wordpress/ see if that file exists within
            #// the current folder, If it's found, change into it and follow through looking
            #// for it. If it can't find WordPress down that route, it'll continue onto the next
            #// folder level, and see if that matches, and so on. If it reaches the end, and still
            #// can't find it, it'll return false for the entire function.
            #//
            if (php_isset(lambda : files_[key_])):
                #// Let's try that folder:
                newdir_ = trailingslashit(path_join(base_, key_))
                if self.verbose:
                    #// translators: %s: Directory name.
                    printf("\n" + __("Changing to %s") + "<br/>\n", newdir_)
                # end if
                #// Only search for the remaining path tokens in the directory, not the full path again.
                newfolder_ = php_implode("/", php_array_slice(folder_parts_, index_ + 1))
                ret_ = self.search_for_folder(newfolder_, newdir_, loop_)
                if ret_:
                    return ret_
                # end if
            # end if
        # end for
        #// Only check this as a last resort, to prevent locating the incorrect install.
        #// All above procedures will fail quickly if this is the right branch to take.
        if (php_isset(lambda : files_[last_path_])):
            if self.verbose:
                #// translators: %s: Directory name.
                printf("\n" + __("Found %s") + "<br/>\n", base_ + last_path_)
            # end if
            return trailingslashit(base_ + last_path_)
        # end if
        #// Prevent this function from looping again.
        #// No need to proceed if we've just searched in `/`.
        if loop_ or "/" == base_:
            return False
        # end if
        #// As an extra last resort, Change back to / if the folder wasn't found.
        #// This comes into effect when the CWD is /home/user/ but WP is at /var/www/....
        return self.search_for_folder(folder_, "/", True)
    # end def search_for_folder
    #// 
    #// Returns the *nix-style file permissions for a file.
    #// 
    #// From the PHP documentation page for fileperms().
    #// 
    #// @link https://www.php.net/manual/en/function.fileperms.php
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $file String filename.
    #// @return string The *nix-style representation of permissions.
    #//
    def gethchmod(self, file_=None):
        
        
        perms_ = php_intval(self.getchmod(file_), 8)
        if perms_ & 49152 == 49152:
            #// Socket.
            info_ = "s"
        elif perms_ & 40960 == 40960:
            #// Symbolic Link.
            info_ = "l"
        elif perms_ & 32768 == 32768:
            #// Regular.
            info_ = "-"
        elif perms_ & 24576 == 24576:
            #// Block special.
            info_ = "b"
        elif perms_ & 16384 == 16384:
            #// Directory.
            info_ = "d"
        elif perms_ & 8192 == 8192:
            #// Character special.
            info_ = "c"
        elif perms_ & 4096 == 4096:
            #// FIFO pipe.
            info_ = "p"
        else:
            #// Unknown.
            info_ = "u"
        # end if
        #// Owner.
        info_ += "r" if perms_ & 256 else "-"
        info_ += "w" if perms_ & 128 else "-"
        info_ += "s" if perms_ & 2048 else "x" if perms_ & 64 else "S" if perms_ & 2048 else "-"
        #// Group.
        info_ += "r" if perms_ & 32 else "-"
        info_ += "w" if perms_ & 16 else "-"
        info_ += "s" if perms_ & 1024 else "x" if perms_ & 8 else "S" if perms_ & 1024 else "-"
        #// World.
        info_ += "r" if perms_ & 4 else "-"
        info_ += "w" if perms_ & 2 else "-"
        info_ += "t" if perms_ & 512 else "x" if perms_ & 1 else "T" if perms_ & 512 else "-"
        return info_
    # end def gethchmod
    #// 
    #// Gets the permissions of the specified file or filepath in their octal format.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $file Path to the file.
    #// @return string Mode of the file (the last 3 digits).
    #//
    def getchmod(self, file_=None):
        
        
        return "777"
    # end def getchmod
    #// 
    #// Converts *nix-style file permissions to a octal number.
    #// 
    #// Converts '-rw-r--r--' to 0644
    #// From "info at rvgate dot nl"'s comment on the PHP documentation for chmod()
    #// 
    #// @link https://www.php.net/manual/en/function.chmod.php#49614
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $mode string The *nix-style file permission.
    #// @return int octal representation
    #//
    def getnumchmodfromh(self, mode_=None):
        
        
        realmode_ = ""
        legal_ = Array("", "w", "r", "x", "-")
        attarray_ = php_preg_split("//", mode_)
        i_ = 0
        c_ = php_count(attarray_)
        while i_ < c_:
            
            key_ = php_array_search(attarray_[i_], legal_)
            if key_:
                realmode_ += legal_[key_]
            # end if
            i_ += 1
        # end while
        mode_ = php_str_pad(realmode_, 10, "-", STR_PAD_LEFT)
        trans_ = Array({"-": "0", "r": "4", "w": "2", "x": "1"})
        mode_ = php_strtr(mode_, trans_)
        newmode_ = mode_[0]
        newmode_ += mode_[1] + mode_[2] + mode_[3]
        newmode_ += mode_[4] + mode_[5] + mode_[6]
        newmode_ += mode_[7] + mode_[8] + mode_[9]
        return newmode_
    # end def getnumchmodfromh
    #// 
    #// Determines if the string provided contains binary characters.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $text String to test against.
    #// @return bool True if string is binary, false otherwise.
    #//
    def is_binary(self, text_=None):
        
        
        return php_bool(php_preg_match("|[^\\x20-\\x7E]|", text_))
        pass
    # end def is_binary
    #// 
    #// Changes the owner of a file or directory.
    #// 
    #// Default behavior is to do nothing, override this in your subclass, if desired.
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
        
        return False
    # end def chown
    #// 
    #// Connects filesystem.
    #// 
    #// @since 2.5.0
    #// @abstract
    #// 
    #// @return bool True on success, false on failure (always true for WP_Filesystem_Direct).
    #//
    def connect(self):
        
        
        return True
    # end def connect
    #// 
    #// Reads entire file into a string.
    #// 
    #// @since 2.5.0
    #// @abstract
    #// 
    #// @param string $file Name of the file to read.
    #// @return string|false Read data on success, false on failure.
    #//
    def get_contents(self, file_=None):
        
        
        return False
    # end def get_contents
    #// 
    #// Reads entire file into an array.
    #// 
    #// @since 2.5.0
    #// @abstract
    #// 
    #// @param string $file Path to the file.
    #// @return array|false File contents in an array on success, false on failure.
    #//
    def get_contents_array(self, file_=None):
        
        
        return False
    # end def get_contents_array
    #// 
    #// Writes a string to a file.
    #// 
    #// @since 2.5.0
    #// @abstract
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
        
        return False
    # end def put_contents
    #// 
    #// Gets the current working directory.
    #// 
    #// @since 2.5.0
    #// @abstract
    #// 
    #// @return string|false The current working directory on success, false on failure.
    #//
    def cwd(self):
        
        
        return False
    # end def cwd
    #// 
    #// Changes current directory.
    #// 
    #// @since 2.5.0
    #// @abstract
    #// 
    #// @param string $dir The new current directory.
    #// @return bool True on success, false on failure.
    #//
    def chdir(self, dir_=None):
        
        
        return False
    # end def chdir
    #// 
    #// Changes the file group.
    #// 
    #// @since 2.5.0
    #// @abstract
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
        
        return False
    # end def chgrp
    #// 
    #// Changes filesystem permissions.
    #// 
    #// @since 2.5.0
    #// @abstract
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
        
        return False
    # end def chmod
    #// 
    #// Gets the file owner.
    #// 
    #// @since 2.5.0
    #// @abstract
    #// 
    #// @param string $file Path to the file.
    #// @return string|false Username of the owner on success, false on failure.
    #//
    def owner(self, file_=None):
        
        
        return False
    # end def owner
    #// 
    #// Gets the file's group.
    #// 
    #// @since 2.5.0
    #// @abstract
    #// 
    #// @param string $file Path to the file.
    #// @return string|false The group on success, false on failure.
    #//
    def group(self, file_=None):
        
        
        return False
    # end def group
    #// 
    #// Copies a file.
    #// 
    #// @since 2.5.0
    #// @abstract
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
        
        return False
    # end def copy
    #// 
    #// Moves a file.
    #// 
    #// @since 2.5.0
    #// @abstract
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
        
        return False
    # end def move
    #// 
    #// Deletes a file or directory.
    #// 
    #// @since 2.5.0
    #// @abstract
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
        
        return False
    # end def delete
    #// 
    #// Checks if a file or directory exists.
    #// 
    #// @since 2.5.0
    #// @abstract
    #// 
    #// @param string $file Path to file or directory.
    #// @return bool Whether $file exists or not.
    #//
    def exists(self, file_=None):
        
        
        return False
    # end def exists
    #// 
    #// Checks if resource is a file.
    #// 
    #// @since 2.5.0
    #// @abstract
    #// 
    #// @param string $file File path.
    #// @return bool Whether $file is a file.
    #//
    def is_file(self, file_=None):
        
        
        return False
    # end def is_file
    #// 
    #// Checks if resource is a directory.
    #// 
    #// @since 2.5.0
    #// @abstract
    #// 
    #// @param string $path Directory path.
    #// @return bool Whether $path is a directory.
    #//
    def is_dir(self, path_=None):
        
        
        return False
    # end def is_dir
    #// 
    #// Checks if a file is readable.
    #// 
    #// @since 2.5.0
    #// @abstract
    #// 
    #// @param string $file Path to file.
    #// @return bool Whether $file is readable.
    #//
    def is_readable(self, file_=None):
        
        
        return False
    # end def is_readable
    #// 
    #// Checks if a file or directory is writable.
    #// 
    #// @since 2.5.0
    #// @abstract
    #// 
    #// @param string $file Path to file or directory.
    #// @return bool Whether $file is writable.
    #//
    def is_writable(self, file_=None):
        
        
        return False
    # end def is_writable
    #// 
    #// Gets the file's last access time.
    #// 
    #// @since 2.5.0
    #// @abstract
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
    #// @abstract
    #// 
    #// @param string $file Path to file.
    #// @return int|false Unix timestamp representing modification time, false on failure.
    #//
    def mtime(self, file_=None):
        
        
        return False
    # end def mtime
    #// 
    #// Gets the file size (in bytes).
    #// 
    #// @since 2.5.0
    #// @abstract
    #// 
    #// @param string $file Path to file.
    #// @return int|false Size of the file in bytes on success, false on failure.
    #//
    def size(self, file_=None):
        
        
        return False
    # end def size
    #// 
    #// Sets the access and modification times of a file.
    #// 
    #// Note: If $file doesn't exist, it will be created.
    #// 
    #// @since 2.5.0
    #// @abstract
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
    #// @abstract
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
        
        return False
    # end def mkdir
    #// 
    #// Deletes a directory.
    #// 
    #// @since 2.5.0
    #// @abstract
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
        
        return False
    # end def rmdir
    #// 
    #// Gets details for files in a directory or a specific file.
    #// 
    #// @since 2.5.0
    #// @abstract
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
        
        return False
    # end def dirlist
# end class WP_Filesystem_Base
