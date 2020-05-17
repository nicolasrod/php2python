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
#// Upgrade API: WP_Upgrader class
#// 
#// Requires skin classes and WP_Upgrader subclasses for backward compatibility.
#// 
#// @package WordPress
#// @subpackage Upgrader
#// @since 2.8.0
#// 
#// WP_Upgrader_Skin class
php_include_file(ABSPATH + "wp-admin/includes/class-wp-upgrader-skin.php", once=True)
#// Plugin_Upgrader_Skin class
php_include_file(ABSPATH + "wp-admin/includes/class-plugin-upgrader-skin.php", once=True)
#// Theme_Upgrader_Skin class
php_include_file(ABSPATH + "wp-admin/includes/class-theme-upgrader-skin.php", once=True)
#// Bulk_Upgrader_Skin class
php_include_file(ABSPATH + "wp-admin/includes/class-bulk-upgrader-skin.php", once=True)
#// Bulk_Plugin_Upgrader_Skin class
php_include_file(ABSPATH + "wp-admin/includes/class-bulk-plugin-upgrader-skin.php", once=True)
#// Bulk_Theme_Upgrader_Skin class
php_include_file(ABSPATH + "wp-admin/includes/class-bulk-theme-upgrader-skin.php", once=True)
#// Plugin_Installer_Skin class
php_include_file(ABSPATH + "wp-admin/includes/class-plugin-installer-skin.php", once=True)
#// Theme_Installer_Skin class
php_include_file(ABSPATH + "wp-admin/includes/class-theme-installer-skin.php", once=True)
#// Language_Pack_Upgrader_Skin class
php_include_file(ABSPATH + "wp-admin/includes/class-language-pack-upgrader-skin.php", once=True)
#// Automatic_Upgrader_Skin class
php_include_file(ABSPATH + "wp-admin/includes/class-automatic-upgrader-skin.php", once=True)
#// WP_Ajax_Upgrader_Skin class
php_include_file(ABSPATH + "wp-admin/includes/class-wp-ajax-upgrader-skin.php", once=True)
#// 
#// Core class used for upgrading/installing a local set of files via
#// the Filesystem Abstraction classes from a Zip file.
#// 
#// @since 2.8.0
#//
class WP_Upgrader():
    #// 
    #// The error/notification strings used to update the user on the progress.
    #// 
    #// @since 2.8.0
    #// @var array $strings
    #//
    strings = Array()
    #// 
    #// The upgrader skin being used.
    #// 
    #// @since 2.8.0
    #// @var Automatic_Upgrader_Skin|WP_Upgrader_Skin $skin
    #//
    skin = None
    #// 
    #// The result of the installation.
    #// 
    #// This is set by WP_Upgrader::install_package(), only when the package is installed
    #// successfully. It will then be an array, unless a WP_Error is returned by the
    #// {@see 'upgrader_post_install'} filter. In that case, the WP_Error will be assigned to
    #// it.
    #// 
    #// @since 2.8.0
    #// 
    #// @var array|WP_Error $result {
    #// @type string $source             The full path to the source the files were installed from.
    #// @type string $source_files       List of all the files in the source directory.
    #// @type string $destination        The full path to the installation destination folder.
    #// @type string $destination_name   The name of the destination folder, or empty if `$destination`
    #// and `$local_destination` are the same.
    #// @type string $local_destination  The full local path to the destination folder. This is usually
    #// the same as `$destination`.
    #// @type string $remote_destination The full remote path to the destination folder
    #// (i.e., from `$wp_filesystem`).
    #// @type bool   $clear_destination  Whether the destination folder was cleared.
    #// }
    #//
    result = Array()
    #// 
    #// The total number of updates being performed.
    #// 
    #// Set by the bulk update methods.
    #// 
    #// @since 3.0.0
    #// @var int $update_count
    #//
    update_count = 0
    #// 
    #// The current update if multiple updates are being performed.
    #// 
    #// Used by the bulk update methods, and incremented for each update.
    #// 
    #// @since 3.0.0
    #// @var int
    #//
    update_current = 0
    #// 
    #// Construct the upgrader with a skin.
    #// 
    #// @since 2.8.0
    #// 
    #// @param WP_Upgrader_Skin $skin The upgrader skin to use. Default is a WP_Upgrader_Skin.
    #// instance.
    #//
    def __init__(self, skin_=None):
        
        
        if None == skin_:
            self.skin = php_new_class("WP_Upgrader_Skin", lambda : WP_Upgrader_Skin())
        else:
            self.skin = skin_
        # end if
    # end def __init__
    #// 
    #// Initialize the upgrader.
    #// 
    #// This will set the relationship between the skin being used and this upgrader,
    #// and also add the generic strings to `WP_Upgrader::$strings`.
    #// 
    #// @since 2.8.0
    #//
    def init(self):
        
        
        self.skin.set_upgrader(self)
        self.generic_strings()
    # end def init
    #// 
    #// Add the generic strings to WP_Upgrader::$strings.
    #// 
    #// @since 2.8.0
    #//
    def generic_strings(self):
        
        
        self.strings["bad_request"] = __("Invalid data provided.")
        self.strings["fs_unavailable"] = __("Could not access filesystem.")
        self.strings["fs_error"] = __("Filesystem error.")
        self.strings["fs_no_root_dir"] = __("Unable to locate WordPress root directory.")
        self.strings["fs_no_content_dir"] = __("Unable to locate WordPress content directory (wp-content).")
        self.strings["fs_no_plugins_dir"] = __("Unable to locate WordPress plugin directory.")
        self.strings["fs_no_themes_dir"] = __("Unable to locate WordPress theme directory.")
        #// translators: %s: Directory name.
        self.strings["fs_no_folder"] = __("Unable to locate needed folder (%s).")
        self.strings["download_failed"] = __("Download failed.")
        self.strings["installing_package"] = __("Installing the latest version&#8230;")
        self.strings["no_files"] = __("The package contains no files.")
        self.strings["folder_exists"] = __("Destination folder already exists.")
        self.strings["mkdir_failed"] = __("Could not create directory.")
        self.strings["incompatible_archive"] = __("The package could not be installed.")
        self.strings["files_not_writable"] = __("The update cannot be installed because we will be unable to copy some files. This is usually due to inconsistent file permissions.")
        self.strings["maintenance_start"] = __("Enabling Maintenance mode&#8230;")
        self.strings["maintenance_end"] = __("Disabling Maintenance mode&#8230;")
    # end def generic_strings
    #// 
    #// Connect to the filesystem.
    #// 
    #// @since 2.8.0
    #// 
    #// @global WP_Filesystem_Base $wp_filesystem WordPress filesystem subclass.
    #// 
    #// @param string[] $directories                  Optional. Array of directories. If any of these do
    #// not exist, a WP_Error object will be returned.
    #// Default empty array.
    #// @param bool     $allow_relaxed_file_ownership Whether to allow relaxed file ownership.
    #// Default false.
    #// @return bool|WP_Error True if able to connect, false or a WP_Error otherwise.
    #//
    def fs_connect(self, directories_=None, allow_relaxed_file_ownership_=None):
        if directories_ is None:
            directories_ = Array()
        # end if
        if allow_relaxed_file_ownership_ is None:
            allow_relaxed_file_ownership_ = False
        # end if
        
        global wp_filesystem_
        php_check_if_defined("wp_filesystem_")
        credentials_ = self.skin.request_filesystem_credentials(False, directories_[0], allow_relaxed_file_ownership_)
        if False == credentials_:
            return False
        # end if
        if (not WP_Filesystem(credentials_, directories_[0], allow_relaxed_file_ownership_)):
            error_ = True
            if php_is_object(wp_filesystem_) and wp_filesystem_.errors.has_errors():
                error_ = wp_filesystem_.errors
            # end if
            #// Failed to connect. Error and request again.
            self.skin.request_filesystem_credentials(error_, directories_[0], allow_relaxed_file_ownership_)
            return False
        # end if
        if (not php_is_object(wp_filesystem_)):
            return php_new_class("WP_Error", lambda : WP_Error("fs_unavailable", self.strings["fs_unavailable"]))
        # end if
        if is_wp_error(wp_filesystem_.errors) and wp_filesystem_.errors.has_errors():
            return php_new_class("WP_Error", lambda : WP_Error("fs_error", self.strings["fs_error"], wp_filesystem_.errors))
        # end if
        for dir_ in directories_:
            for case in Switch(dir_):
                if case(ABSPATH):
                    if (not wp_filesystem_.abspath()):
                        return php_new_class("WP_Error", lambda : WP_Error("fs_no_root_dir", self.strings["fs_no_root_dir"]))
                    # end if
                    break
                # end if
                if case(WP_CONTENT_DIR):
                    if (not wp_filesystem_.wp_content_dir()):
                        return php_new_class("WP_Error", lambda : WP_Error("fs_no_content_dir", self.strings["fs_no_content_dir"]))
                    # end if
                    break
                # end if
                if case(WP_PLUGIN_DIR):
                    if (not wp_filesystem_.wp_plugins_dir()):
                        return php_new_class("WP_Error", lambda : WP_Error("fs_no_plugins_dir", self.strings["fs_no_plugins_dir"]))
                    # end if
                    break
                # end if
                if case(get_theme_root()):
                    if (not wp_filesystem_.wp_themes_dir()):
                        return php_new_class("WP_Error", lambda : WP_Error("fs_no_themes_dir", self.strings["fs_no_themes_dir"]))
                    # end if
                    break
                # end if
                if case():
                    if (not wp_filesystem_.find_folder(dir_)):
                        return php_new_class("WP_Error", lambda : WP_Error("fs_no_folder", php_sprintf(self.strings["fs_no_folder"], esc_html(php_basename(dir_)))))
                    # end if
                    break
                # end if
            # end for
        # end for
        return True
    # end def fs_connect
    #// 
    #// Download a package.
    #// 
    #// @since 2.8.0
    #// 
    #// @param string $package          The URI of the package. If this is the full path to an
    #// existing local file, it will be returned untouched.
    #// @param bool   $check_signatures Whether to validate file signatures. Default false.
    #// @return string|WP_Error The full path to the downloaded package file, or a WP_Error object.
    #//
    def download_package(self, package_=None, check_signatures_=None):
        if check_signatures_ is None:
            check_signatures_ = False
        # end if
        
        #// 
        #// Filters whether to return the package.
        #// 
        #// @since 3.7.0
        #// 
        #// @param bool        $reply   Whether to bail without returning the package.
        #// Default false.
        #// @param string      $package The package file name.
        #// @param WP_Upgrader $this    The WP_Upgrader instance.
        #//
        reply_ = apply_filters("upgrader_pre_download", False, package_, self)
        if False != reply_:
            return reply_
        # end if
        if (not php_preg_match("!^(http|https|ftp)://!i", package_)) and php_file_exists(package_):
            #// Local file or remote?
            return package_
            pass
        # end if
        if php_empty(lambda : package_):
            return php_new_class("WP_Error", lambda : WP_Error("no_package", self.strings["no_package"]))
        # end if
        self.skin.feedback("downloading_package", package_)
        download_file_ = download_url(package_, 300, check_signatures_)
        if is_wp_error(download_file_) and (not download_file_.get_error_data("softfail-filename")):
            return php_new_class("WP_Error", lambda : WP_Error("download_failed", self.strings["download_failed"], download_file_.get_error_message()))
        # end if
        return download_file_
    # end def download_package
    #// 
    #// Unpack a compressed package file.
    #// 
    #// @since 2.8.0
    #// 
    #// @global WP_Filesystem_Base $wp_filesystem WordPress filesystem subclass.
    #// 
    #// @param string $package        Full path to the package file.
    #// @param bool   $delete_package Optional. Whether to delete the package file after attempting
    #// to unpack it. Default true.
    #// @return string|WP_Error The path to the unpacked contents, or a WP_Error on failure.
    #//
    def unpack_package(self, package_=None, delete_package_=None):
        if delete_package_ is None:
            delete_package_ = True
        # end if
        
        global wp_filesystem_
        php_check_if_defined("wp_filesystem_")
        self.skin.feedback("unpack_package")
        upgrade_folder_ = wp_filesystem_.wp_content_dir() + "upgrade/"
        #// Clean up contents of upgrade directory beforehand.
        upgrade_files_ = wp_filesystem_.dirlist(upgrade_folder_)
        if (not php_empty(lambda : upgrade_files_)):
            for file_ in upgrade_files_:
                wp_filesystem_.delete(upgrade_folder_ + file_["name"], True)
            # end for
        # end if
        #// We need a working directory - strip off any .tmp or .zip suffixes.
        working_dir_ = upgrade_folder_ + php_basename(php_basename(package_, ".tmp"), ".zip")
        #// Clean up working directory.
        if wp_filesystem_.is_dir(working_dir_):
            wp_filesystem_.delete(working_dir_, True)
        # end if
        #// Unzip package to working directory.
        result_ = unzip_file(package_, working_dir_)
        #// Once extracted, delete the package if required.
        if delete_package_:
            unlink(package_)
        # end if
        if is_wp_error(result_):
            wp_filesystem_.delete(working_dir_, True)
            if "incompatible_archive" == result_.get_error_code():
                return php_new_class("WP_Error", lambda : WP_Error("incompatible_archive", self.strings["incompatible_archive"], result_.get_error_data()))
            # end if
            return result_
        # end if
        return working_dir_
    # end def unpack_package
    #// 
    #// Flatten the results of WP_Filesystem::dirlist() for iterating over.
    #// 
    #// @since 4.9.0
    #// @access protected
    #// 
    #// @param  array  $nested_files  Array of files as returned by WP_Filesystem::dirlist()
    #// @param  string $path          Relative path to prepend to child nodes. Optional.
    #// @return array A flattened array of the $nested_files specified.
    #//
    def flatten_dirlist(self, nested_files_=None, path_=""):
        
        
        files_ = Array()
        for name_,details_ in nested_files_:
            files_[path_ + name_] = details_
            #// Append children recursively.
            if (not php_empty(lambda : details_["files"])):
                children_ = self.flatten_dirlist(details_["files"], path_ + name_ + "/")
                #// Merge keeping possible numeric keys, which array_merge() will reindex from 0..n.
                files_ = files_ + children_
            # end if
        # end for
        return files_
    # end def flatten_dirlist
    #// 
    #// Clears the directory where this item is going to be installed into.
    #// 
    #// @since 4.3.0
    #// 
    #// @global WP_Filesystem_Base $wp_filesystem WordPress filesystem subclass.
    #// 
    #// @param string $remote_destination The location on the remote filesystem to be cleared
    #// @return bool|WP_Error True upon success, WP_Error on failure.
    #//
    def clear_destination(self, remote_destination_=None):
        
        
        global wp_filesystem_
        php_check_if_defined("wp_filesystem_")
        files_ = wp_filesystem_.dirlist(remote_destination_, True, True)
        #// False indicates that the $remote_destination doesn't exist.
        if False == files_:
            return True
        # end if
        #// Flatten the file list to iterate over.
        files_ = self.flatten_dirlist(files_)
        #// Check all files are writable before attempting to clear the destination.
        unwritable_files_ = Array()
        #// Check writability.
        for filename_,file_details_ in files_:
            if (not wp_filesystem_.is_writable(remote_destination_ + filename_)):
                #// Attempt to alter permissions to allow writes and try again.
                wp_filesystem_.chmod(remote_destination_ + filename_, FS_CHMOD_DIR if "d" == file_details_["type"] else FS_CHMOD_FILE)
                if (not wp_filesystem_.is_writable(remote_destination_ + filename_)):
                    unwritable_files_[-1] = filename_
                # end if
            # end if
        # end for
        if (not php_empty(lambda : unwritable_files_)):
            return php_new_class("WP_Error", lambda : WP_Error("files_not_writable", self.strings["files_not_writable"], php_implode(", ", unwritable_files_)))
        # end if
        if (not wp_filesystem_.delete(remote_destination_, True)):
            return php_new_class("WP_Error", lambda : WP_Error("remove_old_failed", self.strings["remove_old_failed"]))
        # end if
        return True
    # end def clear_destination
    #// 
    #// Install a package.
    #// 
    #// Copies the contents of a package form a source directory, and installs them in
    #// a destination directory. Optionally removes the source. It can also optionally
    #// clear out the destination folder if it already exists.
    #// 
    #// @since 2.8.0
    #// 
    #// @global WP_Filesystem_Base $wp_filesystem        WordPress filesystem subclass.
    #// @global array              $wp_theme_directories
    #// 
    #// @param array|string $args {
    #// Optional. Array or string of arguments for installing a package. Default empty array.
    #// 
    #// @type string $source                      Required path to the package source. Default empty.
    #// @type string $destination                 Required path to a folder to install the package in.
    #// Default empty.
    #// @type bool   $clear_destination           Whether to delete any files already in the destination
    #// folder. Default false.
    #// @type bool   $clear_working               Whether to delete the files form the working directory
    #// after copying to the destination. Default false.
    #// @type bool   $abort_if_destination_exists Whether to abort the installation if
    #// the destination folder already exists. Default true.
    #// @type array  $hook_extra                  Extra arguments to pass to the filter hooks called by
    #// WP_Upgrader::install_package(). Default empty array.
    #// }
    #// 
    #// @return array|WP_Error The result (also stored in `WP_Upgrader::$result`), or a WP_Error on failure.
    #//
    def install_package(self, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        global wp_filesystem_
        global wp_theme_directories_
        php_check_if_defined("wp_filesystem_","wp_theme_directories_")
        defaults_ = Array({"source": "", "destination": "", "clear_destination": False, "clear_working": False, "abort_if_destination_exists": True, "hook_extra": Array()})
        args_ = wp_parse_args(args_, defaults_)
        #// These were previously extract()'d.
        source_ = args_["source"]
        destination_ = args_["destination"]
        clear_destination_ = args_["clear_destination"]
        set_time_limit(300)
        if php_empty(lambda : source_) or php_empty(lambda : destination_):
            return php_new_class("WP_Error", lambda : WP_Error("bad_request", self.strings["bad_request"]))
        # end if
        self.skin.feedback("installing_package")
        #// 
        #// Filters the install response before the installation has started.
        #// 
        #// Returning a truthy value, or one that could be evaluated as a WP_Error
        #// will effectively short-circuit the installation, returning that value
        #// instead.
        #// 
        #// @since 2.8.0
        #// 
        #// @param bool|WP_Error $response   Response.
        #// @param array         $hook_extra Extra arguments passed to hooked filters.
        #//
        res_ = apply_filters("upgrader_pre_install", True, args_["hook_extra"])
        if is_wp_error(res_):
            return res_
        # end if
        #// Retain the original source and destinations.
        remote_source_ = args_["source"]
        local_destination_ = destination_
        source_files_ = php_array_keys(wp_filesystem_.dirlist(remote_source_))
        remote_destination_ = wp_filesystem_.find_folder(local_destination_)
        #// Locate which directory to copy to the new folder. This is based on the actual folder holding the files.
        if 1 == php_count(source_files_) and wp_filesystem_.is_dir(trailingslashit(args_["source"]) + source_files_[0] + "/"):
            #// Only one folder? Then we want its contents.
            source_ = trailingslashit(args_["source"]) + trailingslashit(source_files_[0])
        elif php_count(source_files_) == 0:
            #// There are no files?
            return php_new_class("WP_Error", lambda : WP_Error("incompatible_archive_empty", self.strings["incompatible_archive"], self.strings["no_files"]))
        else:
            #// It's only a single file, the upgrader will use the folder name of this file as the destination folder.
            #// Folder name is based on zip filename.
            source_ = trailingslashit(args_["source"])
        # end if
        #// 
        #// Filters the source file location for the upgrade package.
        #// 
        #// @since 2.8.0
        #// @since 4.4.0 The $hook_extra parameter became available.
        #// 
        #// @param string      $source        File source location.
        #// @param string      $remote_source Remote file source location.
        #// @param WP_Upgrader $this          WP_Upgrader instance.
        #// @param array       $hook_extra    Extra arguments passed to hooked filters.
        #//
        source_ = apply_filters("upgrader_source_selection", source_, remote_source_, self, args_["hook_extra"])
        if is_wp_error(source_):
            return source_
        # end if
        #// Has the source location changed? If so, we need a new source_files list.
        if source_ != remote_source_:
            source_files_ = php_array_keys(wp_filesystem_.dirlist(source_))
        # end if
        #// 
        #// Protection against deleting files in any important base directories.
        #// Theme_Upgrader & Plugin_Upgrader also trigger this, as they pass the
        #// destination directory (WP_PLUGIN_DIR / wp-content/themes) intending
        #// to copy the directory into the directory, whilst they pass the source
        #// as the actual files to copy.
        #//
        protected_directories_ = Array(ABSPATH, WP_CONTENT_DIR, WP_PLUGIN_DIR, WP_CONTENT_DIR + "/themes")
        if php_is_array(wp_theme_directories_):
            protected_directories_ = php_array_merge(protected_directories_, wp_theme_directories_)
        # end if
        if php_in_array(destination_, protected_directories_):
            remote_destination_ = trailingslashit(remote_destination_) + trailingslashit(php_basename(source_))
            destination_ = trailingslashit(destination_) + trailingslashit(php_basename(source_))
        # end if
        if clear_destination_:
            #// We're going to clear the destination if there's something there.
            self.skin.feedback("remove_old")
            removed_ = self.clear_destination(remote_destination_)
            #// 
            #// Filters whether the upgrader cleared the destination.
            #// 
            #// @since 2.8.0
            #// 
            #// @param true|WP_Error $removed            Whether the destination was cleared. true upon success, WP_Error on failure.
            #// @param string        $local_destination  The local package destination.
            #// @param string        $remote_destination The remote package destination.
            #// @param array         $hook_extra         Extra arguments passed to hooked filters.
            #//
            removed_ = apply_filters("upgrader_clear_destination", removed_, local_destination_, remote_destination_, args_["hook_extra"])
            if is_wp_error(removed_):
                return removed_
            # end if
        elif args_["abort_if_destination_exists"] and wp_filesystem_.exists(remote_destination_):
            #// If we're not clearing the destination folder and something exists there already, bail.
            #// But first check to see if there are actually any files in the folder.
            _files_ = wp_filesystem_.dirlist(remote_destination_)
            if (not php_empty(lambda : _files_)):
                wp_filesystem_.delete(remote_source_, True)
                #// Clear out the source files.
                return php_new_class("WP_Error", lambda : WP_Error("folder_exists", self.strings["folder_exists"], remote_destination_))
            # end if
        # end if
        #// Create destination if needed.
        if (not wp_filesystem_.exists(remote_destination_)):
            if (not wp_filesystem_.mkdir(remote_destination_, FS_CHMOD_DIR)):
                return php_new_class("WP_Error", lambda : WP_Error("mkdir_failed_destination", self.strings["mkdir_failed"], remote_destination_))
            # end if
        # end if
        #// Copy new version of item into place.
        result_ = copy_dir(source_, remote_destination_)
        if is_wp_error(result_):
            if args_["clear_working"]:
                wp_filesystem_.delete(remote_source_, True)
            # end if
            return result_
        # end if
        #// Clear the working folder?
        if args_["clear_working"]:
            wp_filesystem_.delete(remote_source_, True)
        # end if
        destination_name_ = php_basename(php_str_replace(local_destination_, "", destination_))
        if "." == destination_name_:
            destination_name_ = ""
        # end if
        self.result = php_compact("source", "source_files", "destination", "destination_name", "local_destination", "remote_destination", "clear_destination")
        #// 
        #// Filters the installation response after the installation has finished.
        #// 
        #// @since 2.8.0
        #// 
        #// @param bool  $response   Installation response.
        #// @param array $hook_extra Extra arguments passed to hooked filters.
        #// @param array $result     Installation result data.
        #//
        res_ = apply_filters("upgrader_post_install", True, args_["hook_extra"], self.result)
        if is_wp_error(res_):
            self.result = res_
            return res_
        # end if
        #// Bombard the calling function will all the info which we've just used.
        return self.result
    # end def install_package
    #// 
    #// Run an upgrade/installation.
    #// 
    #// Attempts to download the package (if it is not a local file), unpack it, and
    #// install it in the destination folder.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $options {
    #// Array or string of arguments for upgrading/installing a package.
    #// 
    #// @type string $package                     The full path or URI of the package to install.
    #// Default empty.
    #// @type string $destination                 The full path to the destination folder.
    #// Default empty.
    #// @type bool   $clear_destination           Whether to delete any files already in the
    #// destination folder. Default false.
    #// @type bool   $clear_working               Whether to delete the files form the working
    #// directory after copying to the destination.
    #// Default false.
    #// @type bool   $abort_if_destination_exists Whether to abort the installation if the destination
    #// folder already exists. When true, `$clear_destination`
    #// should be false. Default true.
    #// @type bool   $is_multi                    Whether this run is one of multiple upgrade/installation
    #// actions being performed in bulk. When true, the skin
    #// WP_Upgrader::header() and WP_Upgrader::footer()
    #// aren't called. Default false.
    #// @type array  $hook_extra                  Extra arguments to pass to the filter hooks called by
    #// WP_Upgrader::run().
    #// }
    #// @return array|false|WP_error The result from self::install_package() on success, otherwise a WP_Error,
    #// or false if unable to connect to the filesystem.
    #//
    def run(self, options_=None):
        
        
        defaults_ = Array({"package": "", "destination": "", "clear_destination": False, "abort_if_destination_exists": True, "clear_working": True, "is_multi": False, "hook_extra": Array()})
        options_ = wp_parse_args(options_, defaults_)
        #// 
        #// Filters the package options before running an update.
        #// 
        #// See also {@see 'upgrader_process_complete'}.
        #// 
        #// @since 4.3.0
        #// 
        #// @param array $options {
        #// Options used by the upgrader.
        #// 
        #// @type string $package                     Package for update.
        #// @type string $destination                 Update location.
        #// @type bool   $clear_destination           Clear the destination resource.
        #// @type bool   $clear_working               Clear the working resource.
        #// @type bool   $abort_if_destination_exists Abort if the Destination directory exists.
        #// @type bool   $is_multi                    Whether the upgrader is running multiple times.
        #// @type array  $hook_extra {
        #// Extra hook arguments.
        #// 
        #// @type string $action               Type of action. Default 'update'.
        #// @type string $type                 Type of update process. Accepts 'plugin', 'theme', or 'core'.
        #// @type bool   $bulk                 Whether the update process is a bulk update. Default true.
        #// @type string $plugin               Path to the plugin file relative to the plugins directory.
        #// @type string $theme                The stylesheet or template name of the theme.
        #// @type string $language_update_type The language pack update type. Accepts 'plugin', 'theme',
        #// or 'core'.
        #// @type object $language_update      The language pack update offer.
        #// }
        #// }
        #//
        options_ = apply_filters("upgrader_package_options", options_)
        if (not options_["is_multi"]):
            #// Call $this->header separately if running multiple times.
            self.skin.header()
        # end if
        #// Connect to the filesystem first.
        res_ = self.fs_connect(Array(WP_CONTENT_DIR, options_["destination"]))
        #// Mainly for non-connected filesystem.
        if (not res_):
            if (not options_["is_multi"]):
                self.skin.footer()
            # end if
            return False
        # end if
        self.skin.before()
        if is_wp_error(res_):
            self.skin.error(res_)
            self.skin.after()
            if (not options_["is_multi"]):
                self.skin.footer()
            # end if
            return res_
        # end if
        #// 
        #// Download the package (Note, This just returns the filename
        #// of the file if the package is a local file)
        #//
        download_ = self.download_package(options_["package"], True)
        #// Allow for signature soft-fail.
        #// WARNING: This may be removed in the future.
        if is_wp_error(download_) and download_.get_error_data("softfail-filename"):
            #// Don't output the 'no signature could be found' failure message for now.
            if "signature_verification_no_signature" != download_.get_error_code() or WP_DEBUG:
                #// Output the failure error as a normal feedback, and not as an error.
                self.skin.feedback(download_.get_error_message())
                #// Report this failure back to WordPress.org for debugging purposes.
                wp_version_check(Array({"signature_failure_code": download_.get_error_code(), "signature_failure_data": download_.get_error_data()}))
            # end if
            #// Pretend this error didn't happen.
            download_ = download_.get_error_data("softfail-filename")
        # end if
        if is_wp_error(download_):
            self.skin.error(download_)
            self.skin.after()
            if (not options_["is_multi"]):
                self.skin.footer()
            # end if
            return download_
        # end if
        delete_package_ = download_ != options_["package"]
        #// Do not delete a "local" file.
        #// Unzips the file into a temporary directory.
        working_dir_ = self.unpack_package(download_, delete_package_)
        if is_wp_error(working_dir_):
            self.skin.error(working_dir_)
            self.skin.after()
            if (not options_["is_multi"]):
                self.skin.footer()
            # end if
            return working_dir_
        # end if
        #// With the given options, this installs it to the destination directory.
        result_ = self.install_package(Array({"source": working_dir_, "destination": options_["destination"], "clear_destination": options_["clear_destination"], "abort_if_destination_exists": options_["abort_if_destination_exists"], "clear_working": options_["clear_working"], "hook_extra": options_["hook_extra"]}))
        self.skin.set_result(result_)
        if is_wp_error(result_):
            self.skin.error(result_)
            self.skin.feedback("process_failed")
        else:
            #// Installation succeeded.
            self.skin.feedback("process_success")
        # end if
        self.skin.after()
        if (not options_["is_multi"]):
            #// 
            #// Fires when the upgrader process is complete.
            #// 
            #// See also {@see 'upgrader_package_options'}.
            #// 
            #// @since 3.6.0
            #// @since 3.7.0 Added to WP_Upgrader::run().
            #// @since 4.6.0 `$translations` was added as a possible argument to `$hook_extra`.
            #// 
            #// @param WP_Upgrader $this WP_Upgrader instance. In other contexts, $this, might be a
            #// Theme_Upgrader, Plugin_Upgrader, Core_Upgrade, or Language_Pack_Upgrader instance.
            #// @param array       $hook_extra {
            #// Array of bulk item update data.
            #// 
            #// @type string $action       Type of action. Default 'update'.
            #// @type string $type         Type of update process. Accepts 'plugin', 'theme', 'translation', or 'core'.
            #// @type bool   $bulk         Whether the update process is a bulk update. Default true.
            #// @type array  $plugins      Array of the basename paths of the plugins' main files.
            #// @type array  $themes       The theme slugs.
            #// @type array  $translations {
            #// Array of translations update data.
            #// 
            #// @type string $language The locale the translation is for.
            #// @type string $type     Type of translation. Accepts 'plugin', 'theme', or 'core'.
            #// @type string $slug     Text domain the translation is for. The slug of a theme/plugin or
            #// 'default' for core translations.
            #// @type string $version  The version of a theme, plugin, or core.
            #// }
            #// }
            #//
            do_action("upgrader_process_complete", self, options_["hook_extra"])
            self.skin.footer()
        # end if
        return result_
    # end def run
    #// 
    #// Toggle maintenance mode for the site.
    #// 
    #// Creates/deletes the maintenance file to enable/disable maintenance mode.
    #// 
    #// @since 2.8.0
    #// 
    #// @global WP_Filesystem_Base $wp_filesystem Subclass
    #// 
    #// @param bool $enable True to enable maintenance mode, false to disable.
    #//
    def maintenance_mode(self, enable_=None):
        if enable_ is None:
            enable_ = False
        # end if
        
        global wp_filesystem_
        php_check_if_defined("wp_filesystem_")
        file_ = wp_filesystem_.abspath() + ".maintenance"
        if enable_:
            self.skin.feedback("maintenance_start")
            #// Create maintenance file to signal that we are upgrading.
            maintenance_string_ = "<?php $upgrading = " + time() + "; ?>"
            wp_filesystem_.delete(file_)
            wp_filesystem_.put_contents(file_, maintenance_string_, FS_CHMOD_FILE)
        elif (not enable_) and wp_filesystem_.exists(file_):
            self.skin.feedback("maintenance_end")
            wp_filesystem_.delete(file_)
        # end if
    # end def maintenance_mode
    #// 
    #// Creates a lock using WordPress options.
    #// 
    #// @since 4.5.0
    #// 
    #// @param string $lock_name       The name of this unique lock.
    #// @param int    $release_timeout Optional. The duration in seconds to respect an existing lock.
    #// Default: 1 hour.
    #// @return bool False if a lock couldn't be created or if the lock is still valid. True otherwise.
    #//
    @classmethod
    def create_lock(self, lock_name_=None, release_timeout_=None):
        
        
        global wpdb_
        php_check_if_defined("wpdb_")
        if (not release_timeout_):
            release_timeout_ = HOUR_IN_SECONDS
        # end if
        lock_option_ = lock_name_ + ".lock"
        #// Try to lock.
        lock_result_ = wpdb_.query(wpdb_.prepare(str("INSERT IGNORE INTO `") + str(wpdb_.options) + str("` ( `option_name`, `option_value`, `autoload` ) VALUES (%s, %s, 'no') /* LOCK */"), lock_option_, time()))
        if (not lock_result_):
            lock_result_ = get_option(lock_option_)
            #// If a lock couldn't be created, and there isn't a lock, bail.
            if (not lock_result_):
                return False
            # end if
            #// Check to see if the lock is still valid. If it is, bail.
            if lock_result_ > time() - release_timeout_:
                return False
            # end if
            #// There must exist an expired lock, clear it and re-gain it.
            WP_Upgrader.release_lock(lock_name_)
            return WP_Upgrader.create_lock(lock_name_, release_timeout_)
        # end if
        #// Update the lock, as by this point we've definitely got a lock, just need to fire the actions.
        update_option(lock_option_, time())
        return True
    # end def create_lock
    #// 
    #// Releases an upgrader lock.
    #// 
    #// @since 4.5.0
    #// 
    #// @see WP_Upgrader::create_lock()
    #// 
    #// @param string $lock_name The name of this unique lock.
    #// @return bool True if the lock was successfully released. False on failure.
    #//
    @classmethod
    def release_lock(self, lock_name_=None):
        
        
        return delete_option(lock_name_ + ".lock")
    # end def release_lock
# end class WP_Upgrader
#// Plugin_Upgrader class
php_include_file(ABSPATH + "wp-admin/includes/class-plugin-upgrader.php", once=True)
#// Theme_Upgrader class
php_include_file(ABSPATH + "wp-admin/includes/class-theme-upgrader.php", once=True)
#// Language_Pack_Upgrader class
php_include_file(ABSPATH + "wp-admin/includes/class-language-pack-upgrader.php", once=True)
#// Core_Upgrader class
php_include_file(ABSPATH + "wp-admin/includes/class-core-upgrader.php", once=True)
#// File_Upload_Upgrader class
php_include_file(ABSPATH + "wp-admin/includes/class-file-upload-upgrader.php", once=True)
#// WP_Automatic_Updater class
php_include_file(ABSPATH + "wp-admin/includes/class-wp-automatic-updater.php", once=True)
