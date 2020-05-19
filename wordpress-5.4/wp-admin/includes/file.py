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
#// Filesystem API: Top-level functionality
#// 
#// Functions for reading, writing, modifying, and deleting files on the file system.
#// Includes functionality for theme-specific files as well as operations for uploading,
#// archiving, and rendering output when necessary.
#// 
#// @package WordPress
#// @subpackage Filesystem
#// @since 2.3.0
#// 
#// The descriptions for theme files.
wp_file_descriptions_ = Array({"functions.php": __("Theme Functions"), "header.php": __("Theme Header"), "footer.php": __("Theme Footer"), "sidebar.php": __("Sidebar"), "comments.php": __("Comments"), "searchform.php": __("Search Form"), "404.php": __("404 Template"), "link.php": __("Links Template"), "index.php": __("Main Index Template"), "archive.php": __("Archives"), "author.php": __("Author Template"), "taxonomy.php": __("Taxonomy Template"), "category.php": __("Category Template"), "tag.php": __("Tag Template"), "home.php": __("Posts Page"), "search.php": __("Search Results"), "date.php": __("Date Template"), "singular.php": __("Singular Template"), "single.php": __("Single Post"), "page.php": __("Single Page"), "front-page.php": __("Homepage"), "privacy-policy.php": __("Privacy Policy Page"), "attachment.php": __("Attachment Template"), "image.php": __("Image Attachment Template"), "video.php": __("Video Attachment Template"), "audio.php": __("Audio Attachment Template"), "application.php": __("Application Attachment Template"), "embed.php": __("Embed Template"), "embed-404.php": __("Embed 404 Template"), "embed-content.php": __("Embed Content Template"), "header-embed.php": __("Embed Header Template"), "footer-embed.php": __("Embed Footer Template"), "style.css": __("Stylesheet"), "editor-style.css": __("Visual Editor Stylesheet"), "editor-style-rtl.css": __("Visual Editor RTL Stylesheet"), "rtl.css": __("RTL Stylesheet"), "my-hacks.php": __("my-hacks.php (legacy hacks support)"), ".htaccess": __(".htaccess (for rewrite rules )"), "wp-layout.css": __("Stylesheet"), "wp-comments.php": __("Comments Template"), "wp-comments-popup.php": __("Popup Comments Template"), "comments-popup.php": __("Popup Comments")})
#// 
#// Get the description for standard WordPress theme files and other various standard
#// WordPress files
#// 
#// @since 1.5.0
#// 
#// @global array $wp_file_descriptions Theme file descriptions.
#// @global array $allowed_files        List of allowed files.
#// @param string $file Filesystem path or filename
#// @return string Description of file from $wp_file_descriptions or basename of $file if description doesn't exist.
#// Appends 'Page Template' to basename of $file if the file is a page template
#//
def get_file_description(file_=None, *_args_):
    
    
    global wp_file_descriptions_
    global allowed_files_
    php_check_if_defined("wp_file_descriptions_","allowed_files_")
    dirname_ = pathinfo(file_, PATHINFO_DIRNAME)
    file_path_ = allowed_files_[file_]
    if (php_isset(lambda : wp_file_descriptions_[php_basename(file_)])) and "." == dirname_:
        return wp_file_descriptions_[php_basename(file_)]
    elif php_file_exists(file_path_) and php_is_file(file_path_):
        template_data_ = php_implode("", file(file_path_))
        if php_preg_match("|Template Name:(.*)$|mi", template_data_, name_):
            #// translators: %s: Template name.
            return php_sprintf(__("%s Page Template"), _cleanup_header_comment(name_[1]))
        # end if
    # end if
    return php_trim(php_basename(file_))
# end def get_file_description
#// 
#// Get the absolute filesystem path to the root of the WordPress installation
#// 
#// @since 1.5.0
#// 
#// @return string Full filesystem path to the root of the WordPress installation
#//
def get_home_path(*_args_):
    
    
    home_ = set_url_scheme(get_option("home"), "http")
    siteurl_ = set_url_scheme(get_option("siteurl"), "http")
    if (not php_empty(lambda : home_)) and 0 != strcasecmp(home_, siteurl_):
        wp_path_rel_to_home_ = php_str_ireplace(home_, "", siteurl_)
        #// $siteurl - $home
        pos_ = php_strripos(php_str_replace("\\", "/", PHP_SERVER["SCRIPT_FILENAME"]), trailingslashit(wp_path_rel_to_home_))
        home_path_ = php_substr(PHP_SERVER["SCRIPT_FILENAME"], 0, pos_)
        home_path_ = trailingslashit(home_path_)
    else:
        home_path_ = ABSPATH
    # end if
    return php_str_replace("\\", "/", home_path_)
# end def get_home_path
#// 
#// Returns a listing of all files in the specified folder and all subdirectories up to 100 levels deep.
#// The depth of the recursiveness can be controlled by the $levels param.
#// 
#// @since 2.6.0
#// @since 4.9.0 Added the `$exclusions` parameter.
#// 
#// @param string   $folder     Optional. Full path to folder. Default empty.
#// @param int      $levels     Optional. Levels of folders to follow, Default 100 (PHP Loop limit).
#// @param string[] $exclusions Optional. List of folders and files to skip.
#// @return bool|string[] False on failure, else array of files.
#//
def list_files(folder_="", levels_=100, exclusions_=None, *_args_):
    if exclusions_ is None:
        exclusions_ = Array()
    # end if
    
    if php_empty(lambda : folder_):
        return False
    # end if
    folder_ = trailingslashit(folder_)
    if (not levels_):
        return False
    # end if
    files_ = Array()
    dir_ = php_no_error(lambda: php_opendir(folder_))
    if dir_:
        while True:
            file_ = php_readdir(dir_)
            if not (file_ != False):
                break
            # end if
            #// Skip current and parent folder links.
            if php_in_array(file_, Array(".", ".."), True):
                continue
            # end if
            #// Skip hidden and excluded files.
            if "." == file_[0] or php_in_array(file_, exclusions_, True):
                continue
            # end if
            if php_is_dir(folder_ + file_):
                files2_ = list_files(folder_ + file_, levels_ - 1)
                if files2_:
                    files_ = php_array_merge(files_, files2_)
                else:
                    files_[-1] = folder_ + file_ + "/"
                # end if
            else:
                files_[-1] = folder_ + file_
            # end if
        # end while
        php_closedir(dir_)
    # end if
    return files_
# end def list_files
#// 
#// Get list of file extensions that are editable in plugins.
#// 
#// @since 4.9.0
#// 
#// @param string $plugin Path to the plugin file relative to the plugins directory.
#// @return string[] Array of editable file extensions.
#//
def wp_get_plugin_file_editable_extensions(plugin_=None, *_args_):
    
    
    editable_extensions_ = Array("bash", "conf", "css", "diff", "htm", "html", "http", "inc", "include", "js", "json", "jsx", "less", "md", "patch", "php", "php3", "php4", "php5", "php7", "phps", "phtml", "sass", "scss", "sh", "sql", "svg", "text", "txt", "xml", "yaml", "yml")
    #// 
    #// Filters file type extensions editable in the plugin editor.
    #// 
    #// @since 2.8.0
    #// @since 4.9.0 Added the `$plugin` parameter.
    #// 
    #// @param string[] $editable_extensions An array of editable plugin file extensions.
    #// @param string   $plugin              Path to the plugin file relative to the plugins directory.
    #//
    editable_extensions_ = apply_filters("editable_extensions", editable_extensions_, plugin_)
    return editable_extensions_
# end def wp_get_plugin_file_editable_extensions
#// 
#// Get list of file extensions that are editable for a given theme.
#// 
#// @param WP_Theme $theme Theme object.
#// @return string[] Array of editable file extensions.
#//
def wp_get_theme_file_editable_extensions(theme_=None, *_args_):
    
    
    default_types_ = Array("bash", "conf", "css", "diff", "htm", "html", "http", "inc", "include", "js", "json", "jsx", "less", "md", "patch", "php", "php3", "php4", "php5", "php7", "phps", "phtml", "sass", "scss", "sh", "sql", "svg", "text", "txt", "xml", "yaml", "yml")
    #// 
    #// Filters the list of file types allowed for editing in the Theme editor.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string[] $default_types List of allowed file types.
    #// @param WP_Theme $theme         The current Theme object.
    #//
    file_types_ = apply_filters("wp_theme_editor_filetypes", default_types_, theme_)
    #// Ensure that default types are still there.
    return array_unique(php_array_merge(file_types_, default_types_))
# end def wp_get_theme_file_editable_extensions
#// 
#// Print file editor templates (for plugins and themes).
#// 
#// @since 4.9.0
#//
def wp_print_file_editor_templates(*_args_):
    
    
    php_print("""   <script type=\"text/html\" id=\"tmpl-wp-file-editor-notice\">
    <div class=\"notice inline notice-{{ data.type || 'info' }} {{ data.alt ? 'notice-alt' : '' }} {{ data.dismissible ? 'is-dismissible' : '' }} {{ data.classes || '' }}\">
    <# if ( 'php_error' === data.code ) { #>
    <p>
    """)
    php_printf(__("Your PHP code changes were rolled back due to an error on line %1$s of file %2$s. Please fix and try saving again."), "{{ data.line }}", "{{ data.file }}")
    php_print("""               </p>
    <pre>{{ data.message }}</pre>
    <# } else if ( 'file_not_writable' === data.code ) { #>
    <p>
    """)
    php_printf(__("You need to make this file writable before you can save your changes. See <a href=\"%s\">Changing File Permissions</a> for more information."), __("https://wordpress.org/support/article/changing-file-permissions/"))
    php_print("""               </p>
    <# } else { #>
    <p>{{ data.message || data.code }}</p>
    <# if ( 'lint_errors' === data.code ) { #>
    <p>
    <# var elementId = 'el-' + String( Math.random() ); #>
    <input id=\"{{ elementId }}\"  type=\"checkbox\">
    <label for=\"{{ elementId }}\">""")
    _e("Update anyway, even though it might break your site?")
    php_print("""</label>
    </p>
    <# } #>
    <# } #>
    <# if ( data.dismissible ) { #>
    <button type=\"button\" class=\"notice-dismiss\"><span class=\"screen-reader-text\">""")
    _e("Dismiss")
    php_print("""</span></button>
    <# } #>
    </div>
    </script>
    """)
# end def wp_print_file_editor_templates
#// 
#// Attempt to edit a file for a theme or plugin.
#// 
#// When editing a PHP file, loopback requests will be made to the admin and the homepage
#// to attempt to see if there is a fatal error introduced. If so, the PHP change will be
#// reverted.
#// 
#// @since 4.9.0
#// 
#// @param string[] $args {
#// Args. Note that all of the arg values are already unslashed. They are, however,
#// coming straight from `$_POST` and are not validated or sanitized in any way.
#// 
#// @type string $file       Relative path to file.
#// @type string $plugin     Path to the plugin file relative to the plugins directory.
#// @type string $theme      Theme being edited.
#// @type string $newcontent New content for the file.
#// @type string $nonce      Nonce.
#// }
#// @return true|WP_Error True on success or `WP_Error` on failure.
#//
def wp_edit_theme_plugin_file(args_=None, *_args_):
    
    
    if php_empty(lambda : args_["file"]):
        return php_new_class("WP_Error", lambda : WP_Error("missing_file"))
    # end if
    file_ = args_["file"]
    if 0 != validate_file(file_):
        return php_new_class("WP_Error", lambda : WP_Error("bad_file"))
    # end if
    if (not (php_isset(lambda : args_["newcontent"]))):
        return php_new_class("WP_Error", lambda : WP_Error("missing_content"))
    # end if
    content_ = args_["newcontent"]
    if (not (php_isset(lambda : args_["nonce"]))):
        return php_new_class("WP_Error", lambda : WP_Error("missing_nonce"))
    # end if
    plugin_ = None
    theme_ = None
    real_file_ = None
    if (not php_empty(lambda : args_["plugin"])):
        plugin_ = args_["plugin"]
        if (not current_user_can("edit_plugins")):
            return php_new_class("WP_Error", lambda : WP_Error("unauthorized", __("Sorry, you are not allowed to edit plugins for this site.")))
        # end if
        if (not wp_verify_nonce(args_["nonce"], "edit-plugin_" + file_)):
            return php_new_class("WP_Error", lambda : WP_Error("nonce_failure"))
        # end if
        if (not php_array_key_exists(plugin_, get_plugins())):
            return php_new_class("WP_Error", lambda : WP_Error("invalid_plugin"))
        # end if
        if 0 != validate_file(file_, get_plugin_files(plugin_)):
            return php_new_class("WP_Error", lambda : WP_Error("bad_plugin_file_path", __("Sorry, that file cannot be edited.")))
        # end if
        editable_extensions_ = wp_get_plugin_file_editable_extensions(plugin_)
        real_file_ = WP_PLUGIN_DIR + "/" + file_
        is_active_ = php_in_array(plugin_, get_option("active_plugins", Array()), True)
    elif (not php_empty(lambda : args_["theme"])):
        stylesheet_ = args_["theme"]
        if 0 != validate_file(stylesheet_):
            return php_new_class("WP_Error", lambda : WP_Error("bad_theme_path"))
        # end if
        if (not current_user_can("edit_themes")):
            return php_new_class("WP_Error", lambda : WP_Error("unauthorized", __("Sorry, you are not allowed to edit templates for this site.")))
        # end if
        theme_ = wp_get_theme(stylesheet_)
        if (not theme_.exists()):
            return php_new_class("WP_Error", lambda : WP_Error("non_existent_theme", __("The requested theme does not exist.")))
        # end if
        if (not wp_verify_nonce(args_["nonce"], "edit-theme_" + stylesheet_ + "_" + file_)):
            return php_new_class("WP_Error", lambda : WP_Error("nonce_failure"))
        # end if
        if theme_.errors() and "theme_no_stylesheet" == theme_.errors().get_error_code():
            return php_new_class("WP_Error", lambda : WP_Error("theme_no_stylesheet", __("The requested theme does not exist.") + " " + theme_.errors().get_error_message()))
        # end if
        editable_extensions_ = wp_get_theme_file_editable_extensions(theme_)
        allowed_files_ = Array()
        for type_ in editable_extensions_:
            for case in Switch(type_):
                if case("php"):
                    allowed_files_ = php_array_merge(allowed_files_, theme_.get_files("php", -1))
                    break
                # end if
                if case("css"):
                    style_files_ = theme_.get_files("css", -1)
                    allowed_files_["style.css"] = style_files_["style.css"]
                    allowed_files_ = php_array_merge(allowed_files_, style_files_)
                    break
                # end if
                if case():
                    allowed_files_ = php_array_merge(allowed_files_, theme_.get_files(type_, -1))
                    break
                # end if
            # end for
        # end for
        #// Compare based on relative paths.
        if 0 != validate_file(file_, php_array_keys(allowed_files_)):
            return php_new_class("WP_Error", lambda : WP_Error("disallowed_theme_file", __("Sorry, that file cannot be edited.")))
        # end if
        real_file_ = theme_.get_stylesheet_directory() + "/" + file_
        is_active_ = get_stylesheet() == stylesheet_ or get_template() == stylesheet_
    else:
        return php_new_class("WP_Error", lambda : WP_Error("missing_theme_or_plugin"))
    # end if
    #// Ensure file is real.
    if (not php_is_file(real_file_)):
        return php_new_class("WP_Error", lambda : WP_Error("file_does_not_exist", __("File does not exist! Please double check the name and try again.")))
    # end if
    #// Ensure file extension is allowed.
    extension_ = None
    if php_preg_match("/\\.([^.]+)$/", real_file_, matches_):
        extension_ = php_strtolower(matches_[1])
        if (not php_in_array(extension_, editable_extensions_, True)):
            return php_new_class("WP_Error", lambda : WP_Error("illegal_file_type", __("Files of this type are not editable.")))
        # end if
    # end if
    previous_content_ = php_file_get_contents(real_file_)
    if (not is_writeable(real_file_)):
        return php_new_class("WP_Error", lambda : WP_Error("file_not_writable"))
    # end if
    f_ = fopen(real_file_, "w+")
    if False == f_:
        return php_new_class("WP_Error", lambda : WP_Error("file_not_writable"))
    # end if
    written_ = fwrite(f_, content_)
    php_fclose(f_)
    if False == written_:
        return php_new_class("WP_Error", lambda : WP_Error("unable_to_write", __("Unable to write to file.")))
    # end if
    if "php" == extension_ and php_function_exists("opcache_invalidate"):
        opcache_invalidate(real_file_, True)
    # end if
    if is_active_ and "php" == extension_:
        scrape_key_ = php_md5(rand())
        transient_ = "scrape_key_" + scrape_key_
        scrape_nonce_ = php_strval(rand())
        #// It shouldn't take more than 60 seconds to make the two loopback requests.
        set_transient(transient_, scrape_nonce_, 60)
        cookies_ = wp_unslash(PHP_COOKIE)
        scrape_params_ = Array({"wp_scrape_key": scrape_key_, "wp_scrape_nonce": scrape_nonce_})
        headers_ = Array({"Cache-Control": "no-cache"})
        #// This filter is documented in wp-includes/class-wp-http-streams.php
        sslverify_ = apply_filters("https_local_ssl_verify", False)
        #// Include Basic auth in loopback requests.
        if (php_isset(lambda : PHP_SERVER["PHP_AUTH_USER"])) and (php_isset(lambda : PHP_SERVER["PHP_AUTH_PW"])):
            headers_["Authorization"] = "Basic " + php_base64_encode(wp_unslash(PHP_SERVER["PHP_AUTH_USER"]) + ":" + wp_unslash(PHP_SERVER["PHP_AUTH_PW"]))
        # end if
        #// Make sure PHP process doesn't die before loopback requests complete.
        set_time_limit(300)
        #// Time to wait for loopback requests to finish.
        timeout_ = 100
        needle_start_ = str("###### wp_scraping_result_start:") + str(scrape_key_) + str(" ######")
        needle_end_ = str("###### wp_scraping_result_end:") + str(scrape_key_) + str(" ######")
        #// Attempt loopback request to editor to see if user just whitescreened themselves.
        if plugin_:
            url_ = add_query_arg(php_compact("plugin_", "file_"), admin_url("plugin-editor.php"))
        elif (php_isset(lambda : stylesheet_)):
            url_ = add_query_arg(Array({"theme": stylesheet_, "file": file_}), admin_url("theme-editor.php"))
        else:
            url_ = admin_url()
        # end if
        url_ = add_query_arg(scrape_params_, url_)
        r_ = wp_remote_get(url_, php_compact("cookies_", "headers_", "timeout_", "sslverify_"))
        body_ = wp_remote_retrieve_body(r_)
        scrape_result_position_ = php_strpos(body_, needle_start_)
        loopback_request_failure_ = Array({"code": "loopback_request_failed", "message": __("Unable to communicate back with site to check for fatal errors, so the PHP change was reverted. You will need to upload your PHP file change by some other means, such as by using SFTP.")})
        json_parse_failure_ = Array({"code": "json_parse_error"})
        result_ = None
        if False == scrape_result_position_:
            result_ = loopback_request_failure_
        else:
            error_output_ = php_substr(body_, scrape_result_position_ + php_strlen(needle_start_))
            error_output_ = php_substr(error_output_, 0, php_strpos(error_output_, needle_end_))
            result_ = php_json_decode(php_trim(error_output_), True)
            if php_empty(lambda : result_):
                result_ = json_parse_failure_
            # end if
        # end if
        #// Try making request to homepage as well to see if visitors have been whitescreened.
        if True == result_:
            url_ = home_url("/")
            url_ = add_query_arg(scrape_params_, url_)
            r_ = wp_remote_get(url_, php_compact("cookies_", "headers_", "timeout_"))
            body_ = wp_remote_retrieve_body(r_)
            scrape_result_position_ = php_strpos(body_, needle_start_)
            if False == scrape_result_position_:
                result_ = loopback_request_failure_
            else:
                error_output_ = php_substr(body_, scrape_result_position_ + php_strlen(needle_start_))
                error_output_ = php_substr(error_output_, 0, php_strpos(error_output_, needle_end_))
                result_ = php_json_decode(php_trim(error_output_), True)
                if php_empty(lambda : result_):
                    result_ = json_parse_failure_
                # end if
            # end if
        # end if
        delete_transient(transient_)
        if True != result_:
            #// Roll-back file change.
            file_put_contents(real_file_, previous_content_)
            if php_function_exists("opcache_invalidate"):
                opcache_invalidate(real_file_, True)
            # end if
            if (not (php_isset(lambda : result_["message"]))):
                message_ = __("Something went wrong.")
            else:
                message_ = result_["message"]
                result_["message"] = None
            # end if
            return php_new_class("WP_Error", lambda : WP_Error("php_error", message_, result_))
        # end if
    # end if
    if type(theme_).__name__ == "WP_Theme":
        theme_.cache_delete()
    # end if
    return True
# end def wp_edit_theme_plugin_file
#// 
#// Returns a filename of a Temporary unique file.
#// Please note that the calling function must unlink() this itself.
#// 
#// The filename is based off the passed parameter or defaults to the current unix timestamp,
#// while the directory can either be passed as well, or by leaving it blank, default to a writable temporary directory.
#// 
#// @since 2.6.0
#// 
#// @param string $filename Optional. Filename to base the Unique file off. Default empty.
#// @param string $dir      Optional. Directory to store the file in. Default empty.
#// @return string a writable filename
#//
def wp_tempnam(filename_="", dir_="", *_args_):
    
    
    if php_empty(lambda : dir_):
        dir_ = get_temp_dir()
    # end if
    if php_empty(lambda : filename_) or "." == filename_ or "/" == filename_ or "\\" == filename_:
        filename_ = php_uniqid()
    # end if
    #// Use the basename of the given file without the extension as the name for the temporary directory.
    temp_filename_ = php_basename(filename_)
    temp_filename_ = php_preg_replace("|\\.[^.]*$|", "", temp_filename_)
    #// If the folder is falsey, use its parent directory name instead.
    if (not temp_filename_):
        return wp_tempnam(php_dirname(filename_), dir_)
    # end if
    #// Suffix some random data to avoid filename conflicts.
    temp_filename_ += "-" + wp_generate_password(6, False)
    temp_filename_ += ".tmp"
    temp_filename_ = dir_ + wp_unique_filename(dir_, temp_filename_)
    fp_ = php_no_error(lambda: fopen(temp_filename_, "x"))
    if (not fp_) and php_is_writable(dir_) and php_file_exists(temp_filename_):
        return wp_tempnam(filename_, dir_)
    # end if
    if fp_:
        php_fclose(fp_)
    # end if
    return temp_filename_
# end def wp_tempnam
#// 
#// Makes sure that the file that was requested to be edited is allowed to be edited.
#// 
#// Function will die if you are not allowed to edit the file.
#// 
#// @since 1.5.0
#// 
#// @param string   $file          File the user is attempting to edit.
#// @param string[] $allowed_files Optional. Array of allowed files to edit. `$file` must match an entry exactly.
#// @return string|void Returns the file name on success, dies on failure.
#//
def validate_file_to_edit(file_=None, allowed_files_=None, *_args_):
    if allowed_files_ is None:
        allowed_files_ = Array()
    # end if
    
    code_ = validate_file(file_, allowed_files_)
    if (not code_):
        return file_
    # end if
    for case in Switch(code_):
        if case(1):
            wp_die(__("Sorry, that file cannot be edited."))
        # end if
        if case(3):
            wp_die(__("Sorry, that file cannot be edited."))
        # end if
    # end for
# end def validate_file_to_edit
#// 
#// Handle PHP uploads in WordPress, sanitizing file names, checking extensions for mime type,
#// and moving the file to the appropriate directory within the uploads directory.
#// 
#// @access private
#// @since 4.0.0
#// 
#// @see wp_handle_upload_error
#// 
#// @param string[]       $file      Reference to a single element of `$_FILES`. Call the function once for each uploaded file.
#// @param string[]|false $overrides An associative array of names => values to override default variables. Default false.
#// @param string         $time      Time formatted in 'yyyy/mm'.
#// @param string         $action    Expected value for `$_POST['action']`.
#// @return string[] On success, returns an associative array of file attributes. On failure, returns
#// `$overrides['upload_error_handler']( &$file, $message )` or `array( 'error' => $message )`.
#//
def _wp_handle_upload(file_=None, overrides_=None, time_=None, action_=None, *_args_):
    
    
    #// The default error handler.
    if (not php_function_exists("wp_handle_upload_error")):
        def wp_handle_upload_error(file_=None, message_=None, *_args_):
            
            
            return Array({"error": message_})
        # end def wp_handle_upload_error
    # end if
    #// 
    #// Filters the data for a file before it is uploaded to WordPress.
    #// 
    #// The dynamic portion of the hook name, `$action`, refers to the post action.
    #// 
    #// @since 2.9.0 as 'wp_handle_upload_prefilter'.
    #// @since 4.0.0 Converted to a dynamic hook with `$action`.
    #// 
    #// @param string[] $file An array of data for a single file.
    #//
    file_ = apply_filters(str(action_) + str("_prefilter"), file_)
    #// You may define your own function and pass the name in $overrides['upload_error_handler'].
    upload_error_handler_ = "wp_handle_upload_error"
    if (php_isset(lambda : overrides_["upload_error_handler"])):
        upload_error_handler_ = overrides_["upload_error_handler"]
    # end if
    #// You may have had one or more 'wp_handle_upload_prefilter' functions error out the file. Handle that gracefully.
    if (php_isset(lambda : file_["error"])) and (not php_is_numeric(file_["error"])) and file_["error"]:
        return call_user_func_array(upload_error_handler_, Array(file_, file_["error"]))
    # end if
    #// Install user overrides. Did we mention that this voids your warranty?
    #// You may define your own function and pass the name in $overrides['unique_filename_callback'].
    unique_filename_callback_ = None
    if (php_isset(lambda : overrides_["unique_filename_callback"])):
        unique_filename_callback_ = overrides_["unique_filename_callback"]
    # end if
    #// 
    #// This may not have originally been intended to be overridable,
    #// but historically has been.
    #//
    if (php_isset(lambda : overrides_["upload_error_strings"])):
        upload_error_strings_ = overrides_["upload_error_strings"]
    else:
        #// Courtesy of php.net, the strings that describe the error indicated in $_FILES[{form field}]['error'].
        upload_error_strings_ = Array(False, php_sprintf(__("The uploaded file exceeds the %1$s directive in %2$s."), "upload_max_filesize", "php.ini"), php_sprintf(__("The uploaded file exceeds the %s directive that was specified in the HTML form."), "MAX_FILE_SIZE"), __("The uploaded file was only partially uploaded."), __("No file was uploaded."), "", __("Missing a temporary folder."), __("Failed to write file to disk."), __("File upload stopped by extension."))
    # end if
    #// All tests are on by default. Most can be turned off by $overrides[{test_name}] = false;
    test_form_ = overrides_["test_form"] if (php_isset(lambda : overrides_["test_form"])) else True
    test_size_ = overrides_["test_size"] if (php_isset(lambda : overrides_["test_size"])) else True
    #// If you override this, you must provide $ext and $type!!
    test_type_ = overrides_["test_type"] if (php_isset(lambda : overrides_["test_type"])) else True
    mimes_ = overrides_["mimes"] if (php_isset(lambda : overrides_["mimes"])) else False
    #// A correct form post will pass this test.
    if test_form_ and (not (php_isset(lambda : PHP_POST["action"]))) or PHP_POST["action"] != action_:
        return call_user_func_array(upload_error_handler_, Array(file_, __("Invalid form submission.")))
    # end if
    #// A successful upload will pass this test. It makes no sense to override this one.
    if (php_isset(lambda : file_["error"])) and file_["error"] > 0:
        return call_user_func_array(upload_error_handler_, Array(file_, upload_error_strings_[file_["error"]]))
    # end if
    #// A properly uploaded file will pass this test. There should be no reason to override this one.
    test_uploaded_file_ = is_uploaded_file(file_["tmp_name"]) if "wp_handle_upload" == action_ else php_no_error(lambda: php_is_readable(file_["tmp_name"]))
    if (not test_uploaded_file_):
        return call_user_func_array(upload_error_handler_, Array(file_, __("Specified file failed upload test.")))
    # end if
    test_file_size_ = file_["size"] if "wp_handle_upload" == action_ else filesize(file_["tmp_name"])
    #// A non-empty file will pass this test.
    if test_size_ and (not test_file_size_ > 0):
        if is_multisite():
            error_msg_ = __("File is empty. Please upload something more substantial.")
        else:
            error_msg_ = php_sprintf(__("File is empty. Please upload something more substantial. This error could also be caused by uploads being disabled in your %1$s file or by %2$s being defined as smaller than %3$s in %1$s."), "php.ini", "post_max_size", "upload_max_filesize")
        # end if
        return call_user_func_array(upload_error_handler_, Array(file_, error_msg_))
    # end if
    #// A correct MIME type will pass this test. Override $mimes or use the upload_mimes filter.
    if test_type_:
        wp_filetype_ = wp_check_filetype_and_ext(file_["tmp_name"], file_["name"], mimes_)
        ext_ = "" if php_empty(lambda : wp_filetype_["ext"]) else wp_filetype_["ext"]
        type_ = "" if php_empty(lambda : wp_filetype_["type"]) else wp_filetype_["type"]
        proper_filename_ = "" if php_empty(lambda : wp_filetype_["proper_filename"]) else wp_filetype_["proper_filename"]
        #// Check to see if wp_check_filetype_and_ext() determined the filename was incorrect.
        if proper_filename_:
            file_["name"] = proper_filename_
        # end if
        if (not type_) or (not ext_) and (not current_user_can("unfiltered_upload")):
            return call_user_func_array(upload_error_handler_, Array(file_, __("Sorry, this file type is not permitted for security reasons.")))
        # end if
        if (not type_):
            type_ = file_["type"]
        # end if
    else:
        type_ = ""
    # end if
    #// 
    #// A writable uploads dir will pass this test. Again, there's no point
    #// overriding this one.
    #//
    uploads_ = wp_upload_dir(time_)
    if (not uploads_ and False == uploads_["error"]):
        return call_user_func_array(upload_error_handler_, Array(file_, uploads_["error"]))
    # end if
    filename_ = wp_unique_filename(uploads_["path"], file_["name"], unique_filename_callback_)
    #// Move the file to the uploads dir.
    new_file_ = uploads_["path"] + str("/") + str(filename_)
    #// 
    #// Filters whether to short-circuit moving the uploaded file after passing all checks.
    #// 
    #// If a non-null value is passed to the filter, moving the file and any related error
    #// reporting will be completely skipped.
    #// 
    #// @since 4.9.0
    #// 
    #// @param mixed    $move_new_file If null (default) move the file after the upload.
    #// @param string[] $file          An array of data for a single file.
    #// @param string   $new_file      Filename of the newly-uploaded file.
    #// @param string   $type          File type.
    #//
    move_new_file_ = apply_filters("pre_move_uploaded_file", None, file_, new_file_, type_)
    if None == move_new_file_:
        if "wp_handle_upload" == action_:
            move_new_file_ = php_no_error(lambda: move_uploaded_file(file_["tmp_name"], new_file_))
        else:
            #// Use copy and unlink because rename breaks streams.
            #// phpcs:ignore WordPress.PHP.NoSilencedErrors.Discouraged
            move_new_file_ = php_no_error(lambda: copy(file_["tmp_name"], new_file_))
            unlink(file_["tmp_name"])
        # end if
        if False == move_new_file_:
            if 0 == php_strpos(uploads_["basedir"], ABSPATH):
                error_path_ = php_str_replace(ABSPATH, "", uploads_["basedir"]) + uploads_["subdir"]
            else:
                error_path_ = php_basename(uploads_["basedir"]) + uploads_["subdir"]
            # end if
            return upload_error_handler_(file_, php_sprintf(__("The uploaded file could not be moved to %s."), error_path_))
        # end if
    # end if
    #// Set correct file permissions.
    stat_ = stat(php_dirname(new_file_))
    perms_ = stat_["mode"] & 438
    chmod(new_file_, perms_)
    #// Compute the URL.
    url_ = uploads_["url"] + str("/") + str(filename_)
    if is_multisite():
        delete_transient("dirsize_cache")
    # end if
    #// 
    #// Filters the data array for the uploaded file.
    #// 
    #// @since 2.1.0
    #// 
    #// @param array  $upload {
    #// Array of upload data.
    #// 
    #// @type string $file Filename of the newly-uploaded file.
    #// @type string $url  URL of the uploaded file.
    #// @type string $type File type.
    #// }
    #// @param string $context The type of upload action. Values include 'upload' or 'sideload'.
    #//
    return apply_filters("wp_handle_upload", Array({"file": new_file_, "url": url_, "type": type_}), "sideload" if "wp_handle_sideload" == action_ else "upload")
# end def _wp_handle_upload
#// 
#// Wrapper for _wp_handle_upload().
#// 
#// Passes the {@see 'wp_handle_upload'} action.
#// 
#// @since 2.0.0
#// 
#// @see _wp_handle_upload()
#// 
#// @param array      $file      Reference to a single element of `$_FILES`. Call the function once for
#// each uploaded file.
#// @param array|bool $overrides Optional. An associative array of names=>values to override default
#// variables. Default false.
#// @param string     $time      Optional. Time formatted in 'yyyy/mm'. Default null.
#// @return array On success, returns an associative array of file attributes. On failure, returns
#// $overrides['upload_error_handler'](&$file, $message ) or array( 'error'=>$message ).
#//
def wp_handle_upload(file_=None, overrides_=None, time_=None, *_args_):
    if overrides_ is None:
        overrides_ = False
    # end if
    if time_ is None:
        time_ = None
    # end if
    
    #// 
    #// $_POST['action'] must be set and its value must equal $overrides['action']
    #// or this:
    #//
    action_ = "wp_handle_upload"
    if (php_isset(lambda : overrides_["action"])):
        action_ = overrides_["action"]
    # end if
    return _wp_handle_upload(file_, overrides_, time_, action_)
# end def wp_handle_upload
#// 
#// Wrapper for _wp_handle_upload().
#// 
#// Passes the {@see 'wp_handle_sideload'} action.
#// 
#// @since 2.6.0
#// 
#// @see _wp_handle_upload()
#// 
#// @param array      $file      An array similar to that of a PHP `$_FILES` POST array
#// @param array|bool $overrides Optional. An associative array of names=>values to override default
#// variables. Default false.
#// @param string     $time      Optional. Time formatted in 'yyyy/mm'. Default null.
#// @return array On success, returns an associative array of file attributes. On failure, returns
#// $overrides['upload_error_handler'](&$file, $message ) or array( 'error'=>$message ).
#//
def wp_handle_sideload(file_=None, overrides_=None, time_=None, *_args_):
    if overrides_ is None:
        overrides_ = False
    # end if
    if time_ is None:
        time_ = None
    # end if
    
    #// 
    #// $_POST['action'] must be set and its value must equal $overrides['action']
    #// or this:
    #//
    action_ = "wp_handle_sideload"
    if (php_isset(lambda : overrides_["action"])):
        action_ = overrides_["action"]
    # end if
    return _wp_handle_upload(file_, overrides_, time_, action_)
# end def wp_handle_sideload
#// 
#// Downloads a URL to a local temporary file using the WordPress HTTP API.
#// 
#// Please note that the calling function must unlink() the file.
#// 
#// @since 2.5.0
#// @since 5.2.0 Signature Verification with SoftFail was added.
#// 
#// @param string $url                    The URL of the file to download.
#// @param int    $timeout                The timeout for the request to download the file. Default 300 seconds.
#// @param bool   $signature_verification Whether to perform Signature Verification. Default false.
#// @return string|WP_Error Filename on success, WP_Error on failure.
#//
def download_url(url_=None, timeout_=300, signature_verification_=None, *_args_):
    if signature_verification_ is None:
        signature_verification_ = False
    # end if
    
    #// WARNING: The file is not automatically deleted, the script must unlink() the file.
    if (not url_):
        return php_new_class("WP_Error", lambda : WP_Error("http_no_url", __("Invalid URL Provided.")))
    # end if
    url_filename_ = php_basename(php_parse_url(url_, PHP_URL_PATH))
    tmpfname_ = wp_tempnam(url_filename_)
    if (not tmpfname_):
        return php_new_class("WP_Error", lambda : WP_Error("http_no_file", __("Could not create Temporary file.")))
    # end if
    response_ = wp_safe_remote_get(url_, Array({"timeout": timeout_, "stream": True, "filename": tmpfname_}))
    if is_wp_error(response_):
        unlink(tmpfname_)
        return response_
    # end if
    response_code_ = wp_remote_retrieve_response_code(response_)
    if 200 != response_code_:
        data_ = Array({"code": response_code_})
        #// Retrieve a sample of the response body for debugging purposes.
        tmpf_ = fopen(tmpfname_, "rb")
        if tmpf_:
            #// 
            #// Filters the maximum error response body size in `download_url()`.
            #// 
            #// @since 5.1.0
            #// 
            #// @see download_url()
            #// 
            #// @param int $size The maximum error response body size. Default 1 KB.
            #//
            response_size_ = apply_filters("download_url_error_max_body_size", KB_IN_BYTES)
            data_["body"] = fread(tmpf_, response_size_)
            php_fclose(tmpf_)
        # end if
        unlink(tmpfname_)
        return php_new_class("WP_Error", lambda : WP_Error("http_404", php_trim(wp_remote_retrieve_response_message(response_)), data_))
    # end if
    content_md5_ = wp_remote_retrieve_header(response_, "content-md5")
    if content_md5_:
        md5_check_ = verify_file_md5(tmpfname_, content_md5_)
        if is_wp_error(md5_check_):
            unlink(tmpfname_)
            return md5_check_
        # end if
    # end if
    #// If the caller expects signature verification to occur, check to see if this URL supports it.
    if signature_verification_:
        #// 
        #// Filters the list of hosts which should have Signature Verification attempted on.
        #// 
        #// @since 5.2.0
        #// 
        #// @param string[] $hostnames List of hostnames.
        #//
        signed_hostnames_ = apply_filters("wp_signature_hosts", Array("wordpress.org", "downloads.wordpress.org", "s.w.org"))
        signature_verification_ = php_in_array(php_parse_url(url_, PHP_URL_HOST), signed_hostnames_, True)
    # end if
    #// Perform signature valiation if supported.
    if signature_verification_:
        signature_ = wp_remote_retrieve_header(response_, "x-content-signature")
        if (not signature_):
            #// Retrieve signatures from a file if the header wasn't included.
            #// WordPress.org stores signatures at $package_url.sig.
            signature_url_ = False
            url_path_ = php_parse_url(url_, PHP_URL_PATH)
            if php_substr(url_path_, -4) == ".zip" or php_substr(url_path_, -7) == ".tar.gz":
                signature_url_ = php_str_replace(url_path_, url_path_ + ".sig", url_)
            # end if
            #// 
            #// Filter the URL where the signature for a file is located.
            #// 
            #// @since 5.2.0
            #// 
            #// @param false|string $signature_url The URL where signatures can be found for a file, or false if none are known.
            #// @param string $url                 The URL being verified.
            #//
            signature_url_ = apply_filters("wp_signature_url", signature_url_, url_)
            if signature_url_:
                signature_request_ = wp_safe_remote_get(signature_url_, Array({"limit_response_size": 10 * KB_IN_BYTES}))
                if (not is_wp_error(signature_request_)) and 200 == wp_remote_retrieve_response_code(signature_request_):
                    signature_ = php_explode("\n", wp_remote_retrieve_body(signature_request_))
                # end if
            # end if
        # end if
        #// Perform the checks.
        signature_verification_ = verify_file_signature(tmpfname_, signature_, php_basename(php_parse_url(url_, PHP_URL_PATH)))
    # end if
    if is_wp_error(signature_verification_):
        if apply_filters("wp_signature_softfail", True, url_):
            signature_verification_.add_data(tmpfname_, "softfail-filename")
        else:
            #// Hard-fail.
            unlink(tmpfname_)
        # end if
        return signature_verification_
    # end if
    return tmpfname_
# end def download_url
#// 
#// Calculates and compares the MD5 of a file to its expected value.
#// 
#// @since 3.7.0
#// 
#// @param string $filename     The filename to check the MD5 of.
#// @param string $expected_md5 The expected MD5 of the file, either a base64-encoded raw md5,
#// or a hex-encoded md5.
#// @return bool|WP_Error True on success, false when the MD5 format is unknown/unexpected,
#// WP_Error on failure.
#//
def verify_file_md5(filename_=None, expected_md5_=None, *_args_):
    
    
    if 32 == php_strlen(expected_md5_):
        expected_raw_md5_ = pack("H*", expected_md5_)
    elif 24 == php_strlen(expected_md5_):
        expected_raw_md5_ = php_base64_decode(expected_md5_)
    else:
        return False
        pass
    # end if
    file_md5_ = php_md5_file(filename_, True)
    if file_md5_ == expected_raw_md5_:
        return True
    # end if
    return php_new_class("WP_Error", lambda : WP_Error("md5_mismatch", php_sprintf(__("The checksum of the file (%1$s) does not match the expected checksum value (%2$s)."), bin2hex(file_md5_), bin2hex(expected_raw_md5_))))
# end def verify_file_md5
#// 
#// Verifies the contents of a file against its ED25519 signature.
#// 
#// @since 5.2.0
#// 
#// @param string       $filename            The file to validate.
#// @param string|array $signatures          A Signature provided for the file.
#// @param string       $filename_for_errors A friendly filename for errors. Optional.
#// @return bool|WP_Error True on success, false if verification not attempted,
#// or WP_Error describing an error condition.
#//
def verify_file_signature(filename_=None, signatures_=None, filename_for_errors_=None, *_args_):
    if filename_for_errors_ is None:
        filename_for_errors_ = False
    # end if
    
    if (not filename_for_errors_):
        filename_for_errors_ = wp_basename(filename_)
    # end if
    #// Check we can process signatures.
    if (not php_function_exists("sodium_crypto_sign_verify_detached")) or (not php_in_array("sha384", php_array_map("strtolower", hash_algos()))):
        return php_new_class("WP_Error", lambda : WP_Error("signature_verification_unsupported", php_sprintf(__("The authenticity of %s could not be verified as signature verification is unavailable on this system."), "<span class=\"code\">" + esc_html(filename_for_errors_) + "</span>"), "sodium_crypto_sign_verify_detached" if (not php_function_exists("sodium_crypto_sign_verify_detached")) else "sha384"))
    # end if
    #// Check for a edge-case affecting PHP Maths abilities.
    if (not php_extension_loaded("sodium")) and php_in_array(PHP_VERSION_ID, Array(70200, 70201, 70202), True) and php_extension_loaded("opcache"):
        #// Sodium_Compat isn't compatible with PHP 7.2.0~7.2.2 due to a bug in the PHP Opcache extension, bail early as it'll fail.
        #// https://bugs.php.net/bug.php?id=75938
        return php_new_class("WP_Error", lambda : WP_Error("signature_verification_unsupported", php_sprintf(__("The authenticity of %s could not be verified as signature verification is unavailable on this system."), "<span class=\"code\">" + esc_html(filename_for_errors_) + "</span>"), Array({"php": php_phpversion(), "sodium": SODIUM_LIBRARY_VERSION if php_defined("SODIUM_LIBRARY_VERSION") else ParagonIE_Sodium_Compat.VERSION_STRING if php_defined("ParagonIE_Sodium_Compat::VERSION_STRING") else False})))
    # end if
    #// Verify runtime speed of Sodium_Compat is acceptable.
    if (not php_extension_loaded("sodium")) and (not ParagonIE_Sodium_Compat.polyfill_is_fast()):
        sodium_compat_is_fast_ = False
        #// Allow for an old version of Sodium_Compat being loaded before the bundled WordPress one.
        if php_method_exists("ParagonIE_Sodium_Compat", "runtime_speed_test"):
            #// Run `ParagonIE_Sodium_Compat::runtime_speed_test()` in optimized integer mode, as that's what WordPress utilises during signing verifications.
            #// phpcs:disable WordPress.NamingConventions.ValidVariableName
            old_fastMult_ = ParagonIE_Sodium_Compat.fastMult
            ParagonIE_Sodium_Compat.fastMult = True
            sodium_compat_is_fast_ = ParagonIE_Sodium_Compat.runtime_speed_test(100, 10)
            ParagonIE_Sodium_Compat.fastMult = old_fastMult_
            pass
        # end if
        #// This cannot be performed in a reasonable amount of time.
        #// https://github.com/paragonie/sodium_compat#help-sodium_compat-is-slow-how-can-i-make-it-fast
        if (not sodium_compat_is_fast_):
            return php_new_class("WP_Error", lambda : WP_Error("signature_verification_unsupported", php_sprintf(__("The authenticity of %s could not be verified as signature verification is unavailable on this system."), "<span class=\"code\">" + esc_html(filename_for_errors_) + "</span>"), Array({"php": php_phpversion(), "sodium": SODIUM_LIBRARY_VERSION if php_defined("SODIUM_LIBRARY_VERSION") else ParagonIE_Sodium_Compat.VERSION_STRING if php_defined("ParagonIE_Sodium_Compat::VERSION_STRING") else False, "polyfill_is_fast": False, "max_execution_time": php_ini_get("max_execution_time")})))
        # end if
    # end if
    if (not signatures_):
        return php_new_class("WP_Error", lambda : WP_Error("signature_verification_no_signature", php_sprintf(__("The authenticity of %s could not be verified as no signature was found."), "<span class=\"code\">" + esc_html(filename_for_errors_) + "</span>"), Array({"filename": filename_for_errors_})))
    # end if
    trusted_keys_ = wp_trusted_keys()
    file_hash_ = hash_file("sha384", filename_, True)
    mbstring_binary_safe_encoding()
    skipped_key_ = 0
    skipped_signature_ = 0
    for signature_ in signatures_:
        signature_raw_ = php_base64_decode(signature_)
        #// Ensure only valid-length signatures are considered.
        if SODIUM_CRYPTO_SIGN_BYTES != php_strlen(signature_raw_):
            skipped_signature_ += 1
            continue
        # end if
        for key_ in trusted_keys_:
            key_raw_ = php_base64_decode(key_)
            #// Only pass valid public keys through.
            if SODIUM_CRYPTO_SIGN_PUBLICKEYBYTES != php_strlen(key_raw_):
                skipped_key_ += 1
                continue
            # end if
            if sodium_crypto_sign_verify_detached(signature_raw_, file_hash_, key_raw_):
                reset_mbstring_encoding()
                return True
            # end if
        # end for
    # end for
    reset_mbstring_encoding()
    return php_new_class("WP_Error", lambda : WP_Error("signature_verification_failed", php_sprintf(__("The authenticity of %s could not be verified."), "<span class=\"code\">" + esc_html(filename_for_errors_) + "</span>"), Array({"filename": filename_for_errors_, "keys": trusted_keys_, "signatures": signatures_, "hash": bin2hex(file_hash_), "skipped_key": skipped_key_, "skipped_sig": skipped_signature_, "php": php_phpversion(), "sodium": SODIUM_LIBRARY_VERSION if php_defined("SODIUM_LIBRARY_VERSION") else ParagonIE_Sodium_Compat.VERSION_STRING if php_defined("ParagonIE_Sodium_Compat::VERSION_STRING") else False})))
# end def verify_file_signature
#// 
#// Retrieve the list of signing keys trusted by WordPress.
#// 
#// @since 5.2.0
#// 
#// @return string[] Array of base64-encoded signing keys.
#//
def wp_trusted_keys(*_args_):
    
    
    trusted_keys_ = Array()
    if time() < 1617235200:
        #// WordPress.org Key #1 - This key is only valid before April 1st, 2021.
        trusted_keys_[-1] = "fRPyrxb/MvVLbdsYi+OOEv4xc+Eqpsj+kkAS6gNOkI0="
    # end if
    #// TODO: Add key #2 with longer expiration.
    #// 
    #// Filter the valid signing keys used to verify the contents of files.
    #// 
    #// @since 5.2.0
    #// 
    #// @param string[] $trusted_keys The trusted keys that may sign packages.
    #//
    return apply_filters("wp_trusted_keys", trusted_keys_)
# end def wp_trusted_keys
#// 
#// Unzips a specified ZIP file to a location on the filesystem via the WordPress
#// Filesystem Abstraction.
#// 
#// Assumes that WP_Filesystem() has already been called and set up. Does not extract
#// a root-level __MACOSX directory, if present.
#// 
#// Attempts to increase the PHP memory limit to 256M before uncompressing. However,
#// the most memory required shouldn't be much larger than the archive itself.
#// 
#// @since 2.5.0
#// 
#// @global WP_Filesystem_Base $wp_filesystem WordPress filesystem subclass.
#// 
#// @param string $file Full path and filename of ZIP archive.
#// @param string $to   Full path on the filesystem to extract archive to.
#// @return true|WP_Error True on success, WP_Error on failure.
#//
def unzip_file(file_=None, to_=None, *_args_):
    
    
    global wp_filesystem_
    php_check_if_defined("wp_filesystem_")
    if (not wp_filesystem_) or (not php_is_object(wp_filesystem_)):
        return php_new_class("WP_Error", lambda : WP_Error("fs_unavailable", __("Could not access filesystem.")))
    # end if
    #// Unzip can use a lot of memory, but not this much hopefully.
    wp_raise_memory_limit("admin")
    needed_dirs_ = Array()
    to_ = trailingslashit(to_)
    #// Determine any parent directories needed (of the upgrade directory).
    if (not wp_filesystem_.is_dir(to_)):
        #// Only do parents if no children exist.
        path_ = php_preg_split("![/\\\\]!", untrailingslashit(to_))
        i_ = php_count(path_)
        while i_ >= 0:
            
            if php_empty(lambda : path_[i_]):
                continue
            # end if
            dir_ = php_implode("/", php_array_slice(path_, 0, i_ + 1))
            if php_preg_match("!^[a-z]:$!i", dir_):
                continue
            # end if
            if (not wp_filesystem_.is_dir(dir_)):
                needed_dirs_[-1] = dir_
            else:
                break
                pass
            # end if
            i_ -= 1
        # end while
    # end if
    #// 
    #// Filters whether to use ZipArchive to unzip archives.
    #// 
    #// @since 3.0.0
    #// 
    #// @param bool $ziparchive Whether to use ZipArchive. Default true.
    #//
    if php_class_exists("ZipArchive", False) and apply_filters("unzip_file_use_ziparchive", True):
        result_ = _unzip_file_ziparchive(file_, to_, needed_dirs_)
        if True == result_:
            return result_
        elif is_wp_error(result_):
            if "incompatible_archive" != result_.get_error_code():
                return result_
            # end if
        # end if
    # end if
    #// Fall through to PclZip if ZipArchive is not available, or encountered an error opening the file.
    return _unzip_file_pclzip(file_, to_, needed_dirs_)
# end def unzip_file
#// 
#// Attempts to unzip an archive using the ZipArchive class.
#// 
#// This function should not be called directly, use `unzip_file()` instead.
#// 
#// Assumes that WP_Filesystem() has already been called and set up.
#// 
#// @since 3.0.0
#// @see unzip_file()
#// @access private
#// 
#// @global WP_Filesystem_Base $wp_filesystem WordPress filesystem subclass.
#// 
#// @param string   $file        Full path and filename of ZIP archive.
#// @param string   $to          Full path on the filesystem to extract archive to.
#// @param string[] $needed_dirs A partial list of required folders needed to be created.
#// @return true|WP_Error True on success, WP_Error on failure.
#//
def _unzip_file_ziparchive(file_=None, to_=None, needed_dirs_=None, *_args_):
    if needed_dirs_ is None:
        needed_dirs_ = Array()
    # end if
    
    global wp_filesystem_
    php_check_if_defined("wp_filesystem_")
    z_ = php_new_class("ZipArchive", lambda : ZipArchive())
    zopen_ = z_.open(file_, ZIPARCHIVE.CHECKCONS)
    if True != zopen_:
        return php_new_class("WP_Error", lambda : WP_Error("incompatible_archive", __("Incompatible Archive."), Array({"ziparchive_error": zopen_})))
    # end if
    uncompressed_size_ = 0
    i_ = 0
    while i_ < z_.numFiles:
        
        info_ = z_.statindex(i_)
        if (not info_):
            return php_new_class("WP_Error", lambda : WP_Error("stat_failed_ziparchive", __("Could not retrieve file from archive.")))
        # end if
        if "__MACOSX/" == php_substr(info_["name"], 0, 9):
            continue
        # end if
        #// Don't extract invalid files:
        if 0 != validate_file(info_["name"]):
            continue
        # end if
        uncompressed_size_ += info_["size"]
        dirname_ = php_dirname(info_["name"])
        if "/" == php_substr(info_["name"], -1):
            #// Directory.
            needed_dirs_[-1] = to_ + untrailingslashit(info_["name"])
        elif "." != dirname_:
            #// Path to a file.
            needed_dirs_[-1] = to_ + untrailingslashit(dirname_)
        # end if
        i_ += 1
    # end while
    #// 
    #// disk_free_space() could return false. Assume that any falsey value is an error.
    #// A disk that has zero free bytes has bigger problems.
    #// Require we have enough space to unzip the file and copy its contents, with a 10% buffer.
    #//
    if wp_doing_cron():
        available_space_ = php_no_error(lambda: disk_free_space(WP_CONTENT_DIR))
        if available_space_ and uncompressed_size_ * 2.1 > available_space_:
            return php_new_class("WP_Error", lambda : WP_Error("disk_full_unzip_file", __("Could not copy files. You may have run out of disk space."), php_compact("uncompressed_size_", "available_space_")))
        # end if
    # end if
    needed_dirs_ = array_unique(needed_dirs_)
    for dir_ in needed_dirs_:
        #// Check the parent folders of the folders all exist within the creation array.
        if untrailingslashit(to_) == dir_:
            continue
        # end if
        if php_strpos(dir_, to_) == False:
            continue
        # end if
        parent_folder_ = php_dirname(dir_)
        while True:
            
            if not ((not php_empty(lambda : parent_folder_)) and untrailingslashit(to_) != parent_folder_ and (not php_in_array(parent_folder_, needed_dirs_))):
                break
            # end if
            needed_dirs_[-1] = parent_folder_
            parent_folder_ = php_dirname(parent_folder_)
        # end while
    # end for
    asort(needed_dirs_)
    #// Create those directories if need be:
    for _dir_ in needed_dirs_:
        #// Only check to see if the Dir exists upon creation failure. Less I/O this way.
        if (not wp_filesystem_.mkdir(_dir_, FS_CHMOD_DIR)) and (not wp_filesystem_.is_dir(_dir_)):
            return php_new_class("WP_Error", lambda : WP_Error("mkdir_failed_ziparchive", __("Could not create directory."), php_substr(_dir_, php_strlen(to_))))
        # end if
    # end for
    needed_dirs_ = None
    i_ = 0
    while i_ < z_.numFiles:
        
        info_ = z_.statindex(i_)
        if (not info_):
            return php_new_class("WP_Error", lambda : WP_Error("stat_failed_ziparchive", __("Could not retrieve file from archive.")))
        # end if
        if "/" == php_substr(info_["name"], -1):
            continue
        # end if
        if "__MACOSX/" == php_substr(info_["name"], 0, 9):
            continue
        # end if
        #// Don't extract invalid files:
        if 0 != validate_file(info_["name"]):
            continue
        # end if
        contents_ = z_.getfromindex(i_)
        if False == contents_:
            return php_new_class("WP_Error", lambda : WP_Error("extract_failed_ziparchive", __("Could not extract file from archive."), info_["name"]))
        # end if
        if (not wp_filesystem_.put_contents(to_ + info_["name"], contents_, FS_CHMOD_FILE)):
            return php_new_class("WP_Error", lambda : WP_Error("copy_failed_ziparchive", __("Could not copy file."), info_["name"]))
        # end if
        i_ += 1
    # end while
    z_.close()
    return True
# end def _unzip_file_ziparchive
#// 
#// Attempts to unzip an archive using the PclZip library.
#// 
#// This function should not be called directly, use `unzip_file()` instead.
#// 
#// Assumes that WP_Filesystem() has already been called and set up.
#// 
#// @since 3.0.0
#// @see unzip_file()
#// @access private
#// 
#// @global WP_Filesystem_Base $wp_filesystem WordPress filesystem subclass.
#// 
#// @param string   $file        Full path and filename of ZIP archive.
#// @param string   $to          Full path on the filesystem to extract archive to.
#// @param string[] $needed_dirs A partial list of required folders needed to be created.
#// @return true|WP_Error True on success, WP_Error on failure.
#//
def _unzip_file_pclzip(file_=None, to_=None, needed_dirs_=None, *_args_):
    if needed_dirs_ is None:
        needed_dirs_ = Array()
    # end if
    
    global wp_filesystem_
    php_check_if_defined("wp_filesystem_")
    mbstring_binary_safe_encoding()
    php_include_file(ABSPATH + "wp-admin/includes/class-pclzip.php", once=True)
    archive_ = php_new_class("PclZip", lambda : PclZip(file_))
    archive_files_ = archive_.extract(PCLZIP_OPT_EXTRACT_AS_STRING)
    reset_mbstring_encoding()
    #// Is the archive valid?
    if (not php_is_array(archive_files_)):
        return php_new_class("WP_Error", lambda : WP_Error("incompatible_archive", __("Incompatible Archive."), archive_.errorinfo(True)))
    # end if
    if 0 == php_count(archive_files_):
        return php_new_class("WP_Error", lambda : WP_Error("empty_archive_pclzip", __("Empty archive.")))
    # end if
    uncompressed_size_ = 0
    #// Determine any children directories needed (From within the archive).
    for file_ in archive_files_:
        if "__MACOSX/" == php_substr(file_["filename"], 0, 9):
            continue
        # end if
        uncompressed_size_ += file_["size"]
        needed_dirs_[-1] = to_ + untrailingslashit(file_["filename"] if file_["folder"] else php_dirname(file_["filename"]))
    # end for
    #// 
    #// disk_free_space() could return false. Assume that any falsey value is an error.
    #// A disk that has zero free bytes has bigger problems.
    #// Require we have enough space to unzip the file and copy its contents, with a 10% buffer.
    #//
    if wp_doing_cron():
        available_space_ = php_no_error(lambda: disk_free_space(WP_CONTENT_DIR))
        if available_space_ and uncompressed_size_ * 2.1 > available_space_:
            return php_new_class("WP_Error", lambda : WP_Error("disk_full_unzip_file", __("Could not copy files. You may have run out of disk space."), php_compact("uncompressed_size_", "available_space_")))
        # end if
    # end if
    needed_dirs_ = array_unique(needed_dirs_)
    for dir_ in needed_dirs_:
        #// Check the parent folders of the folders all exist within the creation array.
        if untrailingslashit(to_) == dir_:
            continue
        # end if
        if php_strpos(dir_, to_) == False:
            continue
        # end if
        parent_folder_ = php_dirname(dir_)
        while True:
            
            if not ((not php_empty(lambda : parent_folder_)) and untrailingslashit(to_) != parent_folder_ and (not php_in_array(parent_folder_, needed_dirs_))):
                break
            # end if
            needed_dirs_[-1] = parent_folder_
            parent_folder_ = php_dirname(parent_folder_)
        # end while
    # end for
    asort(needed_dirs_)
    #// Create those directories if need be:
    for _dir_ in needed_dirs_:
        #// Only check to see if the dir exists upon creation failure. Less I/O this way.
        if (not wp_filesystem_.mkdir(_dir_, FS_CHMOD_DIR)) and (not wp_filesystem_.is_dir(_dir_)):
            return php_new_class("WP_Error", lambda : WP_Error("mkdir_failed_pclzip", __("Could not create directory."), php_substr(_dir_, php_strlen(to_))))
        # end if
    # end for
    needed_dirs_ = None
    #// Extract the files from the zip.
    for file_ in archive_files_:
        if file_["folder"]:
            continue
        # end if
        if "__MACOSX/" == php_substr(file_["filename"], 0, 9):
            continue
        # end if
        #// Don't extract invalid files:
        if 0 != validate_file(file_["filename"]):
            continue
        # end if
        if (not wp_filesystem_.put_contents(to_ + file_["filename"], file_["content"], FS_CHMOD_FILE)):
            return php_new_class("WP_Error", lambda : WP_Error("copy_failed_pclzip", __("Could not copy file."), file_["filename"]))
        # end if
    # end for
    return True
# end def _unzip_file_pclzip
#// 
#// Copies a directory from one location to another via the WordPress Filesystem
#// Abstraction.
#// 
#// Assumes that WP_Filesystem() has already been called and setup.
#// 
#// @since 2.5.0
#// 
#// @global WP_Filesystem_Base $wp_filesystem WordPress filesystem subclass.
#// 
#// @param string   $from      Source directory.
#// @param string   $to        Destination directory.
#// @param string[] $skip_list An array of files/folders to skip copying.
#// @return true|WP_Error True on success, WP_Error on failure.
#//
def copy_dir(from_=None, to_=None, skip_list_=None, *_args_):
    if skip_list_ is None:
        skip_list_ = Array()
    # end if
    
    global wp_filesystem_
    php_check_if_defined("wp_filesystem_")
    dirlist_ = wp_filesystem_.dirlist(from_)
    from_ = trailingslashit(from_)
    to_ = trailingslashit(to_)
    for filename_,fileinfo_ in dirlist_.items():
        if php_in_array(filename_, skip_list_, True):
            continue
        # end if
        if "f" == fileinfo_["type"]:
            if (not wp_filesystem_.copy(from_ + filename_, to_ + filename_, True, FS_CHMOD_FILE)):
                #// If copy failed, chmod file to 0644 and try again.
                wp_filesystem_.chmod(to_ + filename_, FS_CHMOD_FILE)
                if (not wp_filesystem_.copy(from_ + filename_, to_ + filename_, True, FS_CHMOD_FILE)):
                    return php_new_class("WP_Error", lambda : WP_Error("copy_failed_copy_dir", __("Could not copy file."), to_ + filename_))
                # end if
            # end if
        elif "d" == fileinfo_["type"]:
            if (not wp_filesystem_.is_dir(to_ + filename_)):
                if (not wp_filesystem_.mkdir(to_ + filename_, FS_CHMOD_DIR)):
                    return php_new_class("WP_Error", lambda : WP_Error("mkdir_failed_copy_dir", __("Could not create directory."), to_ + filename_))
                # end if
            # end if
            #// Generate the $sub_skip_list for the subdirectory as a sub-set of the existing $skip_list.
            sub_skip_list_ = Array()
            for skip_item_ in skip_list_:
                if 0 == php_strpos(skip_item_, filename_ + "/"):
                    sub_skip_list_[-1] = php_preg_replace("!^" + preg_quote(filename_, "!") + "/!i", "", skip_item_)
                # end if
            # end for
            result_ = copy_dir(from_ + filename_, to_ + filename_, sub_skip_list_)
            if is_wp_error(result_):
                return result_
            # end if
        # end if
    # end for
    return True
# end def copy_dir
#// 
#// Initializes and connects the WordPress Filesystem Abstraction classes.
#// 
#// This function will include the chosen transport and attempt connecting.
#// 
#// Plugins may add extra transports, And force WordPress to use them by returning
#// the filename via the {@see 'filesystem_method_file'} filter.
#// 
#// @since 2.5.0
#// 
#// @global WP_Filesystem_Base $wp_filesystem WordPress filesystem subclass.
#// 
#// @param array|false  $args                         Optional. Connection args, These are passed directly to
#// the `WP_Filesystem_*()` classes. Default false.
#// @param string|false $context                      Optional. Context for get_filesystem_method(). Default false.
#// @param bool         $allow_relaxed_file_ownership Optional. Whether to allow Group/World writable. Default false.
#// @return bool|null True on success, false on failure, null if the filesystem method class file does not exist.
#//
def WP_Filesystem(args_=None, context_=None, allow_relaxed_file_ownership_=None, *_args_):
    if args_ is None:
        args_ = False
    # end if
    if context_ is None:
        context_ = False
    # end if
    if allow_relaxed_file_ownership_ is None:
        allow_relaxed_file_ownership_ = False
    # end if
    
    #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.FunctionNameInvalid
    global wp_filesystem_
    php_check_if_defined("wp_filesystem_")
    php_include_file(ABSPATH + "wp-admin/includes/class-wp-filesystem-base.php", once=True)
    method_ = get_filesystem_method(args_, context_, allow_relaxed_file_ownership_)
    if (not method_):
        return False
    # end if
    if (not php_class_exists(str("WP_Filesystem_") + str(method_))):
        #// 
        #// Filters the path for a specific filesystem method class file.
        #// 
        #// @since 2.6.0
        #// 
        #// @see get_filesystem_method()
        #// 
        #// @param string $path   Path to the specific filesystem method class file.
        #// @param string $method The filesystem method to use.
        #//
        abstraction_file_ = apply_filters("filesystem_method_file", ABSPATH + "wp-admin/includes/class-wp-filesystem-" + method_ + ".php", method_)
        if (not php_file_exists(abstraction_file_)):
            return
        # end if
        php_include_file(abstraction_file_, once=True)
    # end if
    method_ = str("WP_Filesystem_") + str(method_)
    wp_filesystem_ = php_new_class(method_, lambda : {**locals(), **globals()}[method_](args_))
    #// 
    #// Define the timeouts for the connections. Only available after the constructor is called
    #// to allow for per-transport overriding of the default.
    #//
    if (not php_defined("FS_CONNECT_TIMEOUT")):
        php_define("FS_CONNECT_TIMEOUT", 30)
    # end if
    if (not php_defined("FS_TIMEOUT")):
        php_define("FS_TIMEOUT", 30)
    # end if
    if is_wp_error(wp_filesystem_.errors) and wp_filesystem_.errors.has_errors():
        return False
    # end if
    if (not wp_filesystem_.connect()):
        return False
        pass
    # end if
    #// Set the permission constants if not already set.
    if (not php_defined("FS_CHMOD_DIR")):
        php_define("FS_CHMOD_DIR", fileperms(ABSPATH) & 511 | 493)
    # end if
    if (not php_defined("FS_CHMOD_FILE")):
        php_define("FS_CHMOD_FILE", fileperms(ABSPATH + "index.php") & 511 | 420)
    # end if
    return True
# end def WP_Filesystem
#// 
#// Determines which method to use for reading, writing, modifying, or deleting
#// files on the filesystem.
#// 
#// The priority of the transports are: Direct, SSH2, FTP PHP Extension, FTP Sockets
#// (Via Sockets class, or `fsockopen()`). Valid values for these are: 'direct', 'ssh2',
#// 'ftpext' or 'ftpsockets'.
#// 
#// The return value can be overridden by defining the `FS_METHOD` constant in `wp-config.php`,
#// or filtering via {@see 'filesystem_method'}.
#// 
#// @link https://wordpress.org/support/article/editing-wp-config-php/#wordpress-upgrade-constants
#// 
#// Plugins may define a custom transport handler, See WP_Filesystem().
#// 
#// @since 2.5.0
#// 
#// @global callable $_wp_filesystem_direct_method
#// 
#// @param array  $args                         Optional. Connection details. Default empty array.
#// @param string $context                      Optional. Full path to the directory that is tested
#// for being writable. Default empty.
#// @param bool   $allow_relaxed_file_ownership Optional. Whether to allow Group/World writable.
#// Default false.
#// @return string The transport to use, see description for valid return values.
#//
def get_filesystem_method(args_=None, context_="", allow_relaxed_file_ownership_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    if allow_relaxed_file_ownership_ is None:
        allow_relaxed_file_ownership_ = False
    # end if
    global PHP_GLOBALS
    #// Please ensure that this is either 'direct', 'ssh2', 'ftpext', or 'ftpsockets'.
    method_ = FS_METHOD if php_defined("FS_METHOD") else False
    if (not context_):
        context_ = WP_CONTENT_DIR
    # end if
    #// If the directory doesn't exist (wp-content/languages) then use the parent directory as we'll create it.
    if WP_LANG_DIR == context_ and (not php_is_dir(context_)):
        context_ = php_dirname(context_)
    # end if
    context_ = trailingslashit(context_)
    if (not method_):
        temp_file_name_ = context_ + "temp-write-test-" + php_str_replace(".", "-", php_uniqid("", True))
        temp_handle_ = php_no_error(lambda: fopen(temp_file_name_, "w"))
        if temp_handle_:
            #// Attempt to determine the file owner of the WordPress files, and that of newly created files.
            wp_file_owner_ = False
            temp_file_owner_ = False
            if php_function_exists("fileowner"):
                wp_file_owner_ = php_no_error(lambda: fileowner(__FILE__))
                temp_file_owner_ = php_no_error(lambda: fileowner(temp_file_name_))
            # end if
            if False != wp_file_owner_ and wp_file_owner_ == temp_file_owner_:
                #// 
                #// WordPress is creating files as the same owner as the WordPress files,
                #// this means it's safe to modify & create new files via PHP.
                #//
                method_ = "direct"
                PHP_GLOBALS["_wp_filesystem_direct_method"] = "file_owner"
            elif allow_relaxed_file_ownership_:
                #// 
                #// The $context directory is writable, and $allow_relaxed_file_ownership is set,
                #// this means we can modify files safely in this directory.
                #// This mode doesn't create new files, only alter existing ones.
                #//
                method_ = "direct"
                PHP_GLOBALS["_wp_filesystem_direct_method"] = "relaxed_ownership"
            # end if
            php_fclose(temp_handle_)
            php_no_error(lambda: unlink(temp_file_name_))
        # end if
    # end if
    if (not method_) and (php_isset(lambda : args_["connection_type"])) and "ssh" == args_["connection_type"] and php_extension_loaded("ssh2") and php_function_exists("stream_get_contents"):
        method_ = "ssh2"
    # end if
    if (not method_) and php_extension_loaded("ftp"):
        method_ = "ftpext"
    # end if
    if (not method_) and php_extension_loaded("sockets") or php_function_exists("fsockopen"):
        method_ = "ftpsockets"
        pass
    # end if
    #// 
    #// Filters the filesystem method to use.
    #// 
    #// @since 2.6.0
    #// 
    #// @param string $method  Filesystem method to return.
    #// @param array  $args    An array of connection details for the method.
    #// @param string $context Full path to the directory that is tested for being writable.
    #// @param bool   $allow_relaxed_file_ownership Whether to allow Group/World writable.
    #//
    return apply_filters("filesystem_method", method_, args_, context_, allow_relaxed_file_ownership_)
# end def get_filesystem_method
#// 
#// Displays a form to the user to request for their FTP/SSH details in order
#// to connect to the filesystem.
#// 
#// All chosen/entered details are saved, excluding the password.
#// 
#// Hostnames may be in the form of hostname:portnumber (eg: wordpress.org:2467)
#// to specify an alternate FTP/SSH port.
#// 
#// Plugins may override this form by returning true|false via the {@see 'request_filesystem_credentials'} filter.
#// 
#// @since 2.5.0
#// @since 4.6.0 The `$context` parameter default changed from `false` to an empty string.
#// 
#// @global string $pagenow
#// 
#// @param string        $form_post                    The URL to post the form to.
#// @param string        $type                         Optional. Chosen type of filesystem. Default empty.
#// @param bool|WP_Error $error                        Optional. Whether the current request has failed to connect,
#// or an error object. Default false.
#// @param string        $context                      Optional. Full path to the directory that is tested for being
#// writable. Default empty.
#// @param array         $extra_fields                 Optional. Extra `POST` fields to be checked for inclusion in
#// the post. Default null.
#// @param bool          $allow_relaxed_file_ownership Optional. Whether to allow Group/World writable. Default false.
#// 
#// @return bool|array True if no filesystem credentials are required, false if they are required but have not been
#// provided, array of credentials if they are required and have been provided.
#//
def request_filesystem_credentials(form_post_=None, type_="", error_=None, context_="", extra_fields_=None, allow_relaxed_file_ownership_=None, *_args_):
    if error_ is None:
        error_ = False
    # end if
    if extra_fields_ is None:
        extra_fields_ = None
    # end if
    if allow_relaxed_file_ownership_ is None:
        allow_relaxed_file_ownership_ = False
    # end if
    
    global pagenow_
    php_check_if_defined("pagenow_")
    #// 
    #// Filters the filesystem credentials.
    #// 
    #// Returning anything other than an empty string will effectively short-circuit
    #// output of the filesystem credentials form, returning that value instead.
    #// 
    #// A filter should return true if no filesystem credentials are required, false if they are required but have not been
    #// provided, or an array of credentials if they are required and have been provided.
    #// 
    #// @since 2.5.0
    #// @since 4.6.0 The `$context` parameter default changed from `false` to an empty string.
    #// 
    #// @param mixed         $credentials                  Credentials to return instead. Default empty string.
    #// @param string        $form_post                    The URL to post the form to.
    #// @param string        $type                         Chosen type of filesystem.
    #// @param bool|WP_Error $error                        Whether the current request has failed to connect,
    #// or an error object.
    #// @param string        $context                      Full path to the directory that is tested for
    #// being writable.
    #// @param array         $extra_fields                 Extra POST fields.
    #// @param bool          $allow_relaxed_file_ownership Whether to allow Group/World writable.
    #//
    req_cred_ = apply_filters("request_filesystem_credentials", "", form_post_, type_, error_, context_, extra_fields_, allow_relaxed_file_ownership_)
    if "" != req_cred_:
        return req_cred_
    # end if
    if php_empty(lambda : type_):
        type_ = get_filesystem_method(Array(), context_, allow_relaxed_file_ownership_)
    # end if
    if "direct" == type_:
        return True
    # end if
    if php_is_null(extra_fields_):
        extra_fields_ = Array("version", "locale")
    # end if
    credentials_ = get_option("ftp_credentials", Array({"hostname": "", "username": ""}))
    submitted_form_ = wp_unslash(PHP_POST)
    #// Verify nonce, or unset submitted form field values on failure.
    if (not (php_isset(lambda : PHP_POST["_fs_nonce"]))) or (not wp_verify_nonce(PHP_POST["_fs_nonce"], "filesystem-credentials")):
        submitted_form_["hostname"] = None
        submitted_form_["username"] = None
        submitted_form_["password"] = None
        submitted_form_["public_key"] = None
        submitted_form_["private_key"] = None
        submitted_form_["connection_type"] = None
    # end if
    #// If defined, set it to that. Else, if POST'd, set it to that. If not, set it to whatever it previously was (saved details in option).
    credentials_["hostname"] = FTP_HOST if php_defined("FTP_HOST") else submitted_form_["hostname"] if (not php_empty(lambda : submitted_form_["hostname"])) else credentials_["hostname"]
    credentials_["username"] = FTP_USER if php_defined("FTP_USER") else submitted_form_["username"] if (not php_empty(lambda : submitted_form_["username"])) else credentials_["username"]
    credentials_["password"] = FTP_PASS if php_defined("FTP_PASS") else submitted_form_["password"] if (not php_empty(lambda : submitted_form_["password"])) else ""
    #// Check to see if we are setting the public/private keys for ssh.
    credentials_["public_key"] = FTP_PUBKEY if php_defined("FTP_PUBKEY") else submitted_form_["public_key"] if (not php_empty(lambda : submitted_form_["public_key"])) else ""
    credentials_["private_key"] = FTP_PRIKEY if php_defined("FTP_PRIKEY") else submitted_form_["private_key"] if (not php_empty(lambda : submitted_form_["private_key"])) else ""
    #// Sanitize the hostname, some people might pass in odd data.
    credentials_["hostname"] = php_preg_replace("|\\w+://|", "", credentials_["hostname"])
    #// Strip any schemes off.
    if php_strpos(credentials_["hostname"], ":"):
        credentials_["hostname"], credentials_["port"] = php_explode(":", credentials_["hostname"], 2)
        if (not php_is_numeric(credentials_["port"])):
            credentials_["port"] = None
        # end if
    else:
        credentials_["port"] = None
    # end if
    if php_defined("FTP_SSH") and FTP_SSH or php_defined("FS_METHOD") and "ssh2" == FS_METHOD:
        credentials_["connection_type"] = "ssh"
    elif php_defined("FTP_SSL") and FTP_SSL and "ftpext" == type_:
        #// Only the FTP Extension understands SSL.
        credentials_["connection_type"] = "ftps"
    elif (not php_empty(lambda : submitted_form_["connection_type"])):
        credentials_["connection_type"] = submitted_form_["connection_type"]
    elif (not (php_isset(lambda : credentials_["connection_type"]))):
        #// All else fails (and it's not defaulted to something else saved), default to FTP.
        credentials_["connection_type"] = "ftp"
    # end if
    if (not error_) and (not php_empty(lambda : credentials_["password"])) and (not php_empty(lambda : credentials_["username"])) and (not php_empty(lambda : credentials_["hostname"])) or "ssh" == credentials_["connection_type"] and (not php_empty(lambda : credentials_["public_key"])) and (not php_empty(lambda : credentials_["private_key"])):
        stored_credentials_ = credentials_
        if (not php_empty(lambda : stored_credentials_["port"])):
            #// Save port as part of hostname to simplify above code.
            stored_credentials_["hostname"] += ":" + stored_credentials_["port"]
        # end if
        stored_credentials_["password"] = None
        stored_credentials_["port"] = None
        stored_credentials_["private_key"] = None
        stored_credentials_["public_key"] = None
        if (not wp_installing()):
            update_option("ftp_credentials", stored_credentials_)
        # end if
        return credentials_
    # end if
    hostname_ = credentials_["hostname"] if (php_isset(lambda : credentials_["hostname"])) else ""
    username_ = credentials_["username"] if (php_isset(lambda : credentials_["username"])) else ""
    public_key_ = credentials_["public_key"] if (php_isset(lambda : credentials_["public_key"])) else ""
    private_key_ = credentials_["private_key"] if (php_isset(lambda : credentials_["private_key"])) else ""
    port_ = credentials_["port"] if (php_isset(lambda : credentials_["port"])) else ""
    connection_type_ = credentials_["connection_type"] if (php_isset(lambda : credentials_["connection_type"])) else ""
    if error_:
        error_string_ = __("<strong>Error</strong>: There was an error connecting to the server, Please verify the settings are correct.")
        if is_wp_error(error_):
            error_string_ = esc_html(error_.get_error_message())
        # end if
        php_print("<div id=\"message\" class=\"error\"><p>" + error_string_ + "</p></div>")
    # end if
    types_ = Array()
    if php_extension_loaded("ftp") or php_extension_loaded("sockets") or php_function_exists("fsockopen"):
        types_["ftp"] = __("FTP")
    # end if
    if php_extension_loaded("ftp"):
        #// Only this supports FTPS.
        types_["ftps"] = __("FTPS (SSL)")
    # end if
    if php_extension_loaded("ssh2") and php_function_exists("stream_get_contents"):
        types_["ssh"] = __("SSH2")
    # end if
    #// 
    #// Filters the connection types to output to the filesystem credentials form.
    #// 
    #// @since 2.9.0
    #// @since 4.6.0 The `$context` parameter default changed from `false` to an empty string.
    #// 
    #// @param string[]      $types       Types of connections.
    #// @param array         $credentials Credentials to connect with.
    #// @param string        $type        Chosen filesystem method.
    #// @param bool|WP_Error $error       Whether the current request has failed to connect,
    #// or an error object.
    #// @param string        $context     Full path to the directory that is tested for being writable.
    #//
    types_ = apply_filters("fs_ftp_connection_types", types_, credentials_, type_, error_, context_)
    php_print("<form action=\"")
    php_print(esc_url(form_post_))
    php_print("\" method=\"post\">\n<div id=\"request-filesystem-credentials-form\" class=\"request-filesystem-credentials-form\">\n    ")
    #// Print a H1 heading in the FTP credentials modal dialog, default is a H2.
    heading_tag_ = "h2"
    if "plugins.php" == pagenow_ or "plugin-install.php" == pagenow_:
        heading_tag_ = "h1"
    # end if
    php_print(str("<") + str(heading_tag_) + str(" id='request-filesystem-credentials-title'>") + __("Connection Information") + str("</") + str(heading_tag_) + str(">"))
    php_print("<p id=\"request-filesystem-credentials-desc\">\n ")
    label_user_ = __("Username")
    label_pass_ = __("Password")
    _e("To perform the requested action, WordPress needs to access your web server.")
    php_print(" ")
    if (php_isset(lambda : types_["ftp"])) or (php_isset(lambda : types_["ftps"])):
        if (php_isset(lambda : types_["ssh"])):
            _e("Please enter your FTP or SSH credentials to proceed.")
            label_user_ = __("FTP/SSH Username")
            label_pass_ = __("FTP/SSH Password")
        else:
            _e("Please enter your FTP credentials to proceed.")
            label_user_ = __("FTP Username")
            label_pass_ = __("FTP Password")
        # end if
        php_print(" ")
    # end if
    _e("If you do not remember your credentials, you should contact your web host.")
    hostname_value_ = esc_attr(hostname_)
    if (not php_empty(lambda : port_)):
        hostname_value_ += str(":") + str(port_)
    # end if
    password_value_ = ""
    if php_defined("FTP_PASS"):
        password_value_ = "*****"
    # end if
    php_print("</p>\n<label for=\"hostname\">\n <span class=\"field-title\">")
    _e("Hostname")
    php_print("</span>\n    <input name=\"hostname\" type=\"text\" id=\"hostname\" aria-describedby=\"request-filesystem-credentials-desc\" class=\"code\" placeholder=\"")
    esc_attr_e("example: www.wordpress.org")
    php_print("\" value=\"")
    php_print(hostname_value_)
    php_print("\"")
    disabled(php_defined("FTP_HOST"))
    php_print(""" />
    </label>
    <div class=\"ftp-username\">
    <label for=\"username\">
    <span class=\"field-title\">""")
    php_print(label_user_)
    php_print("</span>\n        <input name=\"username\" type=\"text\" id=\"username\" value=\"")
    php_print(esc_attr(username_))
    php_print("\"")
    disabled(php_defined("FTP_USER"))
    php_print(""" />
    </label>
    </div>
    <div class=\"ftp-password\">
    <label for=\"password\">
    <span class=\"field-title\">""")
    php_print(label_pass_)
    php_print("</span>\n        <input name=\"password\" type=\"password\" id=\"password\" value=\"")
    php_print(password_value_)
    php_print("\"")
    disabled(php_defined("FTP_PASS"))
    php_print(" />\n        <em>\n      ")
    if (not php_defined("FTP_PASS")):
        _e("This password will not be stored on the server.")
    # end if
    php_print("""</em>
    </label>
    </div>
    <fieldset>
    <legend>""")
    _e("Connection Type")
    php_print("</legend>\n  ")
    disabled_ = disabled(php_defined("FTP_SSL") and FTP_SSL or php_defined("FTP_SSH") and FTP_SSH, True, False)
    for name_,text_ in types_.items():
        php_print(" <label for=\"")
        php_print(esc_attr(name_))
        php_print("\">\n        <input type=\"radio\" name=\"connection_type\" id=\"")
        php_print(esc_attr(name_))
        php_print("\" value=\"")
        php_print(esc_attr(name_))
        php_print("\" ")
        checked(name_, connection_type_)
        php_print(" ")
        php_print(disabled_)
        php_print(" />\n        ")
        php_print(text_)
        php_print(" </label>\n      ")
    # end for
    php_print("</fieldset>\n    ")
    if (php_isset(lambda : types_["ssh"])):
        hidden_class_ = ""
        if "ssh" != connection_type_ or php_empty(lambda : connection_type_):
            hidden_class_ = " class=\"hidden\""
        # end if
        php_print("<fieldset id=\"ssh-keys\"")
        php_print(hidden_class_)
        php_print(">\n<legend>")
        _e("Authentication Keys")
        php_print("</legend>\n<label for=\"public_key\">\n  <span class=\"field-title\">")
        _e("Public Key:")
        php_print("</span>\n    <input name=\"public_key\" type=\"text\" id=\"public_key\" aria-describedby=\"auth-keys-desc\" value=\"")
        php_print(esc_attr(public_key_))
        php_print("\"")
        disabled(php_defined("FTP_PUBKEY"))
        php_print(""" />
        </label>
        <label for=\"private_key\">
        <span class=\"field-title\">""")
        _e("Private Key:")
        php_print("</span>\n    <input name=\"private_key\" type=\"text\" id=\"private_key\" value=\"")
        php_print(esc_attr(private_key_))
        php_print("\"")
        disabled(php_defined("FTP_PRIKEY"))
        php_print(" />\n</label>\n<p id=\"auth-keys-desc\">")
        _e("Enter the location on the server where the public and private keys are located. If a passphrase is needed, enter that in the password field above.")
        php_print("</p>\n</fieldset>\n      ")
    # end if
    for field_ in extra_fields_:
        if (php_isset(lambda : submitted_form_[field_])):
            php_print("<input type=\"hidden\" name=\"" + esc_attr(field_) + "\" value=\"" + esc_attr(submitted_form_[field_]) + "\" />")
        # end if
    # end for
    php_print(" <p class=\"request-filesystem-credentials-action-buttons\">\n       ")
    wp_nonce_field("filesystem-credentials", "_fs_nonce", False, True)
    php_print("     <button class=\"button cancel-button\" data-js-action=\"close\" type=\"button\">")
    _e("Cancel")
    php_print("</button>\n      ")
    submit_button(__("Proceed"), "", "upgrade", False)
    php_print("""   </p>
    </div>
    </form>
    """)
    return False
# end def request_filesystem_credentials
#// 
#// Print the filesystem credentials modal when needed.
#// 
#// @since 4.2.0
#//
def wp_print_request_filesystem_credentials_modal(*_args_):
    
    
    filesystem_method_ = get_filesystem_method()
    ob_start()
    filesystem_credentials_are_stored_ = request_filesystem_credentials(self_admin_url())
    ob_end_clean()
    request_filesystem_credentials_ = "direct" != filesystem_method_ and (not filesystem_credentials_are_stored_)
    if (not request_filesystem_credentials_):
        return
    # end if
    php_print("""   <div id=\"request-filesystem-credentials-dialog\" class=\"notification-dialog-wrap request-filesystem-credentials-dialog\">
    <div class=\"notification-dialog-background\"></div>
    <div class=\"notification-dialog\" role=\"dialog\" aria-labelledby=\"request-filesystem-credentials-title\" tabindex=\"0\">
    <div class=\"request-filesystem-credentials-dialog-content\">
    """)
    request_filesystem_credentials(site_url())
    php_print("""           </div>
    </div>
    </div>
    """)
# end def wp_print_request_filesystem_credentials_modal
