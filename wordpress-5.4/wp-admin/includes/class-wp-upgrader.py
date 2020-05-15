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
    strings = Array()
    skin = None
    result = Array()
    update_count = 0
    update_current = 0
    #// 
    #// Construct the upgrader with a skin.
    #// 
    #// @since 2.8.0
    #// 
    #// @param WP_Upgrader_Skin $skin The upgrader skin to use. Default is a WP_Upgrader_Skin.
    #// instance.
    #//
    def __init__(self, skin=None):
        
        if None == skin:
            self.skin = php_new_class("WP_Upgrader_Skin", lambda : WP_Upgrader_Skin())
        else:
            self.skin = skin
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
    def fs_connect(self, directories=Array(), allow_relaxed_file_ownership=False):
        
        global wp_filesystem
        php_check_if_defined("wp_filesystem")
        credentials = self.skin.request_filesystem_credentials(False, directories[0], allow_relaxed_file_ownership)
        if False == credentials:
            return False
        # end if
        if (not WP_Filesystem(credentials, directories[0], allow_relaxed_file_ownership)):
            error = True
            if php_is_object(wp_filesystem) and wp_filesystem.errors.has_errors():
                error = wp_filesystem.errors
            # end if
            #// Failed to connect. Error and request again.
            self.skin.request_filesystem_credentials(error, directories[0], allow_relaxed_file_ownership)
            return False
        # end if
        if (not php_is_object(wp_filesystem)):
            return php_new_class("WP_Error", lambda : WP_Error("fs_unavailable", self.strings["fs_unavailable"]))
        # end if
        if is_wp_error(wp_filesystem.errors) and wp_filesystem.errors.has_errors():
            return php_new_class("WP_Error", lambda : WP_Error("fs_error", self.strings["fs_error"], wp_filesystem.errors))
        # end if
        for dir in directories:
            for case in Switch(dir):
                if case(ABSPATH):
                    if (not wp_filesystem.abspath()):
                        return php_new_class("WP_Error", lambda : WP_Error("fs_no_root_dir", self.strings["fs_no_root_dir"]))
                    # end if
                    break
                # end if
                if case(WP_CONTENT_DIR):
                    if (not wp_filesystem.wp_content_dir()):
                        return php_new_class("WP_Error", lambda : WP_Error("fs_no_content_dir", self.strings["fs_no_content_dir"]))
                    # end if
                    break
                # end if
                if case(WP_PLUGIN_DIR):
                    if (not wp_filesystem.wp_plugins_dir()):
                        return php_new_class("WP_Error", lambda : WP_Error("fs_no_plugins_dir", self.strings["fs_no_plugins_dir"]))
                    # end if
                    break
                # end if
                if case(get_theme_root()):
                    if (not wp_filesystem.wp_themes_dir()):
                        return php_new_class("WP_Error", lambda : WP_Error("fs_no_themes_dir", self.strings["fs_no_themes_dir"]))
                    # end if
                    break
                # end if
                if case():
                    if (not wp_filesystem.find_folder(dir)):
                        return php_new_class("WP_Error", lambda : WP_Error("fs_no_folder", php_sprintf(self.strings["fs_no_folder"], esc_html(php_basename(dir)))))
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
    def download_package(self, package=None, check_signatures=False):
        
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
        reply = apply_filters("upgrader_pre_download", False, package, self)
        if False != reply:
            return reply
        # end if
        if (not php_preg_match("!^(http|https|ftp)://!i", package)) and php_file_exists(package):
            #// Local file or remote?
            return package
            pass
        # end if
        if php_empty(lambda : package):
            return php_new_class("WP_Error", lambda : WP_Error("no_package", self.strings["no_package"]))
        # end if
        self.skin.feedback("downloading_package", package)
        download_file = download_url(package, 300, check_signatures)
        if is_wp_error(download_file) and (not download_file.get_error_data("softfail-filename")):
            return php_new_class("WP_Error", lambda : WP_Error("download_failed", self.strings["download_failed"], download_file.get_error_message()))
        # end if
        return download_file
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
    def unpack_package(self, package=None, delete_package=True):
        
        global wp_filesystem
        php_check_if_defined("wp_filesystem")
        self.skin.feedback("unpack_package")
        upgrade_folder = wp_filesystem.wp_content_dir() + "upgrade/"
        #// Clean up contents of upgrade directory beforehand.
        upgrade_files = wp_filesystem.dirlist(upgrade_folder)
        if (not php_empty(lambda : upgrade_files)):
            for file in upgrade_files:
                wp_filesystem.delete(upgrade_folder + file["name"], True)
            # end for
        # end if
        #// We need a working directory - strip off any .tmp or .zip suffixes.
        working_dir = upgrade_folder + php_basename(php_basename(package, ".tmp"), ".zip")
        #// Clean up working directory.
        if wp_filesystem.is_dir(working_dir):
            wp_filesystem.delete(working_dir, True)
        # end if
        #// Unzip package to working directory.
        result = unzip_file(package, working_dir)
        #// Once extracted, delete the package if required.
        if delete_package:
            unlink(package)
        # end if
        if is_wp_error(result):
            wp_filesystem.delete(working_dir, True)
            if "incompatible_archive" == result.get_error_code():
                return php_new_class("WP_Error", lambda : WP_Error("incompatible_archive", self.strings["incompatible_archive"], result.get_error_data()))
            # end if
            return result
        # end if
        return working_dir
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
    def flatten_dirlist(self, nested_files=None, path=""):
        
        files = Array()
        for name,details in nested_files:
            files[path + name] = details
            #// Append children recursively.
            if (not php_empty(lambda : details["files"])):
                children = self.flatten_dirlist(details["files"], path + name + "/")
                #// Merge keeping possible numeric keys, which array_merge() will reindex from 0..n.
                files = files + children
            # end if
        # end for
        return files
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
    def clear_destination(self, remote_destination=None):
        
        global wp_filesystem
        php_check_if_defined("wp_filesystem")
        files = wp_filesystem.dirlist(remote_destination, True, True)
        #// False indicates that the $remote_destination doesn't exist.
        if False == files:
            return True
        # end if
        #// Flatten the file list to iterate over.
        files = self.flatten_dirlist(files)
        #// Check all files are writable before attempting to clear the destination.
        unwritable_files = Array()
        #// Check writability.
        for filename,file_details in files:
            if (not wp_filesystem.is_writable(remote_destination + filename)):
                #// Attempt to alter permissions to allow writes and try again.
                wp_filesystem.chmod(remote_destination + filename, FS_CHMOD_DIR if "d" == file_details["type"] else FS_CHMOD_FILE)
                if (not wp_filesystem.is_writable(remote_destination + filename)):
                    unwritable_files[-1] = filename
                # end if
            # end if
        # end for
        if (not php_empty(lambda : unwritable_files)):
            return php_new_class("WP_Error", lambda : WP_Error("files_not_writable", self.strings["files_not_writable"], php_implode(", ", unwritable_files)))
        # end if
        if (not wp_filesystem.delete(remote_destination, True)):
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
    def install_package(self, args=Array()):
        
        global wp_filesystem,wp_theme_directories
        php_check_if_defined("wp_filesystem","wp_theme_directories")
        defaults = Array({"source": "", "destination": "", "clear_destination": False, "clear_working": False, "abort_if_destination_exists": True, "hook_extra": Array()})
        args = wp_parse_args(args, defaults)
        #// These were previously extract()'d.
        source = args["source"]
        destination = args["destination"]
        clear_destination = args["clear_destination"]
        set_time_limit(300)
        if php_empty(lambda : source) or php_empty(lambda : destination):
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
        res = apply_filters("upgrader_pre_install", True, args["hook_extra"])
        if is_wp_error(res):
            return res
        # end if
        #// Retain the original source and destinations.
        remote_source = args["source"]
        local_destination = destination
        source_files = php_array_keys(wp_filesystem.dirlist(remote_source))
        remote_destination = wp_filesystem.find_folder(local_destination)
        #// Locate which directory to copy to the new folder. This is based on the actual folder holding the files.
        if 1 == php_count(source_files) and wp_filesystem.is_dir(trailingslashit(args["source"]) + source_files[0] + "/"):
            #// Only one folder? Then we want its contents.
            source = trailingslashit(args["source"]) + trailingslashit(source_files[0])
        elif php_count(source_files) == 0:
            #// There are no files?
            return php_new_class("WP_Error", lambda : WP_Error("incompatible_archive_empty", self.strings["incompatible_archive"], self.strings["no_files"]))
        else:
            #// It's only a single file, the upgrader will use the folder name of this file as the destination folder.
            #// Folder name is based on zip filename.
            source = trailingslashit(args["source"])
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
        source = apply_filters("upgrader_source_selection", source, remote_source, self, args["hook_extra"])
        if is_wp_error(source):
            return source
        # end if
        #// Has the source location changed? If so, we need a new source_files list.
        if source != remote_source:
            source_files = php_array_keys(wp_filesystem.dirlist(source))
        # end if
        #// 
        #// Protection against deleting files in any important base directories.
        #// Theme_Upgrader & Plugin_Upgrader also trigger this, as they pass the
        #// destination directory (WP_PLUGIN_DIR / wp-content/themes) intending
        #// to copy the directory into the directory, whilst they pass the source
        #// as the actual files to copy.
        #//
        protected_directories = Array(ABSPATH, WP_CONTENT_DIR, WP_PLUGIN_DIR, WP_CONTENT_DIR + "/themes")
        if php_is_array(wp_theme_directories):
            protected_directories = php_array_merge(protected_directories, wp_theme_directories)
        # end if
        if php_in_array(destination, protected_directories):
            remote_destination = trailingslashit(remote_destination) + trailingslashit(php_basename(source))
            destination = trailingslashit(destination) + trailingslashit(php_basename(source))
        # end if
        if clear_destination:
            #// We're going to clear the destination if there's something there.
            self.skin.feedback("remove_old")
            removed = self.clear_destination(remote_destination)
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
            removed = apply_filters("upgrader_clear_destination", removed, local_destination, remote_destination, args["hook_extra"])
            if is_wp_error(removed):
                return removed
            # end if
        elif args["abort_if_destination_exists"] and wp_filesystem.exists(remote_destination):
            #// If we're not clearing the destination folder and something exists there already, bail.
            #// But first check to see if there are actually any files in the folder.
            _files = wp_filesystem.dirlist(remote_destination)
            if (not php_empty(lambda : _files)):
                wp_filesystem.delete(remote_source, True)
                #// Clear out the source files.
                return php_new_class("WP_Error", lambda : WP_Error("folder_exists", self.strings["folder_exists"], remote_destination))
            # end if
        # end if
        #// Create destination if needed.
        if (not wp_filesystem.exists(remote_destination)):
            if (not wp_filesystem.mkdir(remote_destination, FS_CHMOD_DIR)):
                return php_new_class("WP_Error", lambda : WP_Error("mkdir_failed_destination", self.strings["mkdir_failed"], remote_destination))
            # end if
        # end if
        #// Copy new version of item into place.
        result = copy_dir(source, remote_destination)
        if is_wp_error(result):
            if args["clear_working"]:
                wp_filesystem.delete(remote_source, True)
            # end if
            return result
        # end if
        #// Clear the working folder?
        if args["clear_working"]:
            wp_filesystem.delete(remote_source, True)
        # end if
        destination_name = php_basename(php_str_replace(local_destination, "", destination))
        if "." == destination_name:
            destination_name = ""
        # end if
        self.result = compact("source", "source_files", "destination", "destination_name", "local_destination", "remote_destination", "clear_destination")
        #// 
        #// Filters the installation response after the installation has finished.
        #// 
        #// @since 2.8.0
        #// 
        #// @param bool  $response   Installation response.
        #// @param array $hook_extra Extra arguments passed to hooked filters.
        #// @param array $result     Installation result data.
        #//
        res = apply_filters("upgrader_post_install", True, args["hook_extra"], self.result)
        if is_wp_error(res):
            self.result = res
            return res
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
    def run(self, options=None):
        
        defaults = Array({"package": "", "destination": "", "clear_destination": False, "abort_if_destination_exists": True, "clear_working": True, "is_multi": False, "hook_extra": Array()})
        options = wp_parse_args(options, defaults)
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
        options = apply_filters("upgrader_package_options", options)
        if (not options["is_multi"]):
            #// Call $this->header separately if running multiple times.
            self.skin.header()
        # end if
        #// Connect to the filesystem first.
        res = self.fs_connect(Array(WP_CONTENT_DIR, options["destination"]))
        #// Mainly for non-connected filesystem.
        if (not res):
            if (not options["is_multi"]):
                self.skin.footer()
            # end if
            return False
        # end if
        self.skin.before()
        if is_wp_error(res):
            self.skin.error(res)
            self.skin.after()
            if (not options["is_multi"]):
                self.skin.footer()
            # end if
            return res
        # end if
        #// 
        #// Download the package (Note, This just returns the filename
        #// of the file if the package is a local file)
        #//
        download = self.download_package(options["package"], True)
        #// Allow for signature soft-fail.
        #// WARNING: This may be removed in the future.
        if is_wp_error(download) and download.get_error_data("softfail-filename"):
            #// Don't output the 'no signature could be found' failure message for now.
            if "signature_verification_no_signature" != download.get_error_code() or WP_DEBUG:
                #// Output the failure error as a normal feedback, and not as an error.
                self.skin.feedback(download.get_error_message())
                #// Report this failure back to WordPress.org for debugging purposes.
                wp_version_check(Array({"signature_failure_code": download.get_error_code(), "signature_failure_data": download.get_error_data()}))
            # end if
            #// Pretend this error didn't happen.
            download = download.get_error_data("softfail-filename")
        # end if
        if is_wp_error(download):
            self.skin.error(download)
            self.skin.after()
            if (not options["is_multi"]):
                self.skin.footer()
            # end if
            return download
        # end if
        delete_package = download != options["package"]
        #// Do not delete a "local" file.
        #// Unzips the file into a temporary directory.
        working_dir = self.unpack_package(download, delete_package)
        if is_wp_error(working_dir):
            self.skin.error(working_dir)
            self.skin.after()
            if (not options["is_multi"]):
                self.skin.footer()
            # end if
            return working_dir
        # end if
        #// With the given options, this installs it to the destination directory.
        result = self.install_package(Array({"source": working_dir, "destination": options["destination"], "clear_destination": options["clear_destination"], "abort_if_destination_exists": options["abort_if_destination_exists"], "clear_working": options["clear_working"], "hook_extra": options["hook_extra"]}))
        self.skin.set_result(result)
        if is_wp_error(result):
            self.skin.error(result)
            self.skin.feedback("process_failed")
        else:
            #// Installation succeeded.
            self.skin.feedback("process_success")
        # end if
        self.skin.after()
        if (not options["is_multi"]):
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
            do_action("upgrader_process_complete", self, options["hook_extra"])
            self.skin.footer()
        # end if
        return result
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
    def maintenance_mode(self, enable=False):
        
        global wp_filesystem
        php_check_if_defined("wp_filesystem")
        file = wp_filesystem.abspath() + ".maintenance"
        if enable:
            self.skin.feedback("maintenance_start")
            #// Create maintenance file to signal that we are upgrading.
            maintenance_string = "<?php $upgrading = " + time() + "; ?>"
            wp_filesystem.delete(file)
            wp_filesystem.put_contents(file, maintenance_string, FS_CHMOD_FILE)
        elif (not enable) and wp_filesystem.exists(file):
            self.skin.feedback("maintenance_end")
            wp_filesystem.delete(file)
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
    def create_lock(self, lock_name=None, release_timeout=None):
        
        global wpdb
        php_check_if_defined("wpdb")
        if (not release_timeout):
            release_timeout = HOUR_IN_SECONDS
        # end if
        lock_option = lock_name + ".lock"
        #// Try to lock.
        lock_result = wpdb.query(wpdb.prepare(str("INSERT IGNORE INTO `") + str(wpdb.options) + str("` ( `option_name`, `option_value`, `autoload` ) VALUES (%s, %s, 'no') /* LOCK */"), lock_option, time()))
        if (not lock_result):
            lock_result = get_option(lock_option)
            #// If a lock couldn't be created, and there isn't a lock, bail.
            if (not lock_result):
                return False
            # end if
            #// Check to see if the lock is still valid. If it is, bail.
            if lock_result > time() - release_timeout:
                return False
            # end if
            #// There must exist an expired lock, clear it and re-gain it.
            WP_Upgrader.release_lock(lock_name)
            return WP_Upgrader.create_lock(lock_name, release_timeout)
        # end if
        #// Update the lock, as by this point we've definitely got a lock, just need to fire the actions.
        update_option(lock_option, time())
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
    def release_lock(self, lock_name=None):
        
        return delete_option(lock_name + ".lock")
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
