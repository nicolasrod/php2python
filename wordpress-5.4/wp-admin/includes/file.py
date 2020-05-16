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
wp_file_descriptions = Array({"functions.php": __("Theme Functions"), "header.php": __("Theme Header"), "footer.php": __("Theme Footer"), "sidebar.php": __("Sidebar"), "comments.php": __("Comments"), "searchform.php": __("Search Form"), "404.php": __("404 Template"), "link.php": __("Links Template"), "index.php": __("Main Index Template"), "archive.php": __("Archives"), "author.php": __("Author Template"), "taxonomy.php": __("Taxonomy Template"), "category.php": __("Category Template"), "tag.php": __("Tag Template"), "home.php": __("Posts Page"), "search.php": __("Search Results"), "date.php": __("Date Template"), "singular.php": __("Singular Template"), "single.php": __("Single Post"), "page.php": __("Single Page"), "front-page.php": __("Homepage"), "privacy-policy.php": __("Privacy Policy Page"), "attachment.php": __("Attachment Template"), "image.php": __("Image Attachment Template"), "video.php": __("Video Attachment Template"), "audio.php": __("Audio Attachment Template"), "application.php": __("Application Attachment Template"), "embed.php": __("Embed Template"), "embed-404.php": __("Embed 404 Template"), "embed-content.php": __("Embed Content Template"), "header-embed.php": __("Embed Header Template"), "footer-embed.php": __("Embed Footer Template"), "style.css": __("Stylesheet"), "editor-style.css": __("Visual Editor Stylesheet"), "editor-style-rtl.css": __("Visual Editor RTL Stylesheet"), "rtl.css": __("RTL Stylesheet"), "my-hacks.php": __("my-hacks.php (legacy hacks support)"), ".htaccess": __(".htaccess (for rewrite rules )"), "wp-layout.css": __("Stylesheet"), "wp-comments.php": __("Comments Template"), "wp-comments-popup.php": __("Popup Comments Template"), "comments-popup.php": __("Popup Comments")})
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
def get_file_description(file=None, *args_):
    
    global wp_file_descriptions,allowed_files
    php_check_if_defined("wp_file_descriptions","allowed_files")
    dirname = pathinfo(file, PATHINFO_DIRNAME)
    file_path = allowed_files[file]
    if (php_isset(lambda : wp_file_descriptions[php_basename(file)])) and "." == dirname:
        return wp_file_descriptions[php_basename(file)]
    elif php_file_exists(file_path) and php_is_file(file_path):
        template_data = php_implode("", file(file_path))
        if php_preg_match("|Template Name:(.*)$|mi", template_data, name):
            #// translators: %s: Template name.
            return php_sprintf(__("%s Page Template"), _cleanup_header_comment(name[1]))
        # end if
    # end if
    return php_trim(php_basename(file))
# end def get_file_description
#// 
#// Get the absolute filesystem path to the root of the WordPress installation
#// 
#// @since 1.5.0
#// 
#// @return string Full filesystem path to the root of the WordPress installation
#//
def get_home_path(*args_):
    
    home = set_url_scheme(get_option("home"), "http")
    siteurl = set_url_scheme(get_option("siteurl"), "http")
    if (not php_empty(lambda : home)) and 0 != strcasecmp(home, siteurl):
        wp_path_rel_to_home = php_str_ireplace(home, "", siteurl)
        #// $siteurl - $home
        pos = php_strripos(php_str_replace("\\", "/", PHP_SERVER["SCRIPT_FILENAME"]), trailingslashit(wp_path_rel_to_home))
        home_path = php_substr(PHP_SERVER["SCRIPT_FILENAME"], 0, pos)
        home_path = trailingslashit(home_path)
    else:
        home_path = ABSPATH
    # end if
    return php_str_replace("\\", "/", home_path)
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
def list_files(folder="", levels=100, exclusions=Array(), *args_):
    
    if php_empty(lambda : folder):
        return False
    # end if
    folder = trailingslashit(folder)
    if (not levels):
        return False
    # end if
    files = Array()
    dir = php_no_error(lambda: php_opendir(folder))
    if dir:
        while True:
            file = php_readdir(dir)
            if not (file != False):
                break
            # end if
            #// Skip current and parent folder links.
            if php_in_array(file, Array(".", ".."), True):
                continue
            # end if
            #// Skip hidden and excluded files.
            if "." == file[0] or php_in_array(file, exclusions, True):
                continue
            # end if
            if php_is_dir(folder + file):
                files2 = list_files(folder + file, levels - 1)
                if files2:
                    files = php_array_merge(files, files2)
                else:
                    files[-1] = folder + file + "/"
                # end if
            else:
                files[-1] = folder + file
            # end if
        # end while
        php_closedir(dir)
    # end if
    return files
# end def list_files
#// 
#// Get list of file extensions that are editable in plugins.
#// 
#// @since 4.9.0
#// 
#// @param string $plugin Path to the plugin file relative to the plugins directory.
#// @return string[] Array of editable file extensions.
#//
def wp_get_plugin_file_editable_extensions(plugin=None, *args_):
    
    editable_extensions = Array("bash", "conf", "css", "diff", "htm", "html", "http", "inc", "include", "js", "json", "jsx", "less", "md", "patch", "php", "php3", "php4", "php5", "php7", "phps", "phtml", "sass", "scss", "sh", "sql", "svg", "text", "txt", "xml", "yaml", "yml")
    #// 
    #// Filters file type extensions editable in the plugin editor.
    #// 
    #// @since 2.8.0
    #// @since 4.9.0 Added the `$plugin` parameter.
    #// 
    #// @param string[] $editable_extensions An array of editable plugin file extensions.
    #// @param string   $plugin              Path to the plugin file relative to the plugins directory.
    #//
    editable_extensions = apply_filters("editable_extensions", editable_extensions, plugin)
    return editable_extensions
# end def wp_get_plugin_file_editable_extensions
#// 
#// Get list of file extensions that are editable for a given theme.
#// 
#// @param WP_Theme $theme Theme object.
#// @return string[] Array of editable file extensions.
#//
def wp_get_theme_file_editable_extensions(theme=None, *args_):
    
    default_types = Array("bash", "conf", "css", "diff", "htm", "html", "http", "inc", "include", "js", "json", "jsx", "less", "md", "patch", "php", "php3", "php4", "php5", "php7", "phps", "phtml", "sass", "scss", "sh", "sql", "svg", "text", "txt", "xml", "yaml", "yml")
    #// 
    #// Filters the list of file types allowed for editing in the Theme editor.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string[] $default_types List of allowed file types.
    #// @param WP_Theme $theme         The current Theme object.
    #//
    file_types = apply_filters("wp_theme_editor_filetypes", default_types, theme)
    #// Ensure that default types are still there.
    return array_unique(php_array_merge(file_types, default_types))
# end def wp_get_theme_file_editable_extensions
#// 
#// Print file editor templates (for plugins and themes).
#// 
#// @since 4.9.0
#//
def wp_print_file_editor_templates(*args_):
    
    php_print("""   <script type=\"text/html\" id=\"tmpl-wp-file-editor-notice\">
    <div class=\"notice inline notice-{{ data.type || 'info' }} {{ data.alt ? 'notice-alt' : '' }} {{ data.dismissible ? 'is-dismissible' : '' }} {{ data.classes || '' }}\">
    <# if ( 'php_error' === data.code ) { #>
    <p>
    """)
    printf(__("Your PHP code changes were rolled back due to an error on line %1$s of file %2$s. Please fix and try saving again."), "{{ data.line }}", "{{ data.file }}")
    php_print("""               </p>
    <pre>{{ data.message }}</pre>
    <# } else if ( 'file_not_writable' === data.code ) { #>
    <p>
    """)
    printf(__("You need to make this file writable before you can save your changes. See <a href=\"%s\">Changing File Permissions</a> for more information."), __("https://wordpress.org/support/article/changing-file-permissions/"))
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
def wp_edit_theme_plugin_file(args=None, *args_):
    
    if php_empty(lambda : args["file"]):
        return php_new_class("WP_Error", lambda : WP_Error("missing_file"))
    # end if
    file = args["file"]
    if 0 != validate_file(file):
        return php_new_class("WP_Error", lambda : WP_Error("bad_file"))
    # end if
    if (not (php_isset(lambda : args["newcontent"]))):
        return php_new_class("WP_Error", lambda : WP_Error("missing_content"))
    # end if
    content = args["newcontent"]
    if (not (php_isset(lambda : args["nonce"]))):
        return php_new_class("WP_Error", lambda : WP_Error("missing_nonce"))
    # end if
    plugin = None
    theme = None
    real_file = None
    if (not php_empty(lambda : args["plugin"])):
        plugin = args["plugin"]
        if (not current_user_can("edit_plugins")):
            return php_new_class("WP_Error", lambda : WP_Error("unauthorized", __("Sorry, you are not allowed to edit plugins for this site.")))
        # end if
        if (not wp_verify_nonce(args["nonce"], "edit-plugin_" + file)):
            return php_new_class("WP_Error", lambda : WP_Error("nonce_failure"))
        # end if
        if (not php_array_key_exists(plugin, get_plugins())):
            return php_new_class("WP_Error", lambda : WP_Error("invalid_plugin"))
        # end if
        if 0 != validate_file(file, get_plugin_files(plugin)):
            return php_new_class("WP_Error", lambda : WP_Error("bad_plugin_file_path", __("Sorry, that file cannot be edited.")))
        # end if
        editable_extensions = wp_get_plugin_file_editable_extensions(plugin)
        real_file = WP_PLUGIN_DIR + "/" + file
        is_active = php_in_array(plugin, get_option("active_plugins", Array()), True)
    elif (not php_empty(lambda : args["theme"])):
        stylesheet = args["theme"]
        if 0 != validate_file(stylesheet):
            return php_new_class("WP_Error", lambda : WP_Error("bad_theme_path"))
        # end if
        if (not current_user_can("edit_themes")):
            return php_new_class("WP_Error", lambda : WP_Error("unauthorized", __("Sorry, you are not allowed to edit templates for this site.")))
        # end if
        theme = wp_get_theme(stylesheet)
        if (not theme.exists()):
            return php_new_class("WP_Error", lambda : WP_Error("non_existent_theme", __("The requested theme does not exist.")))
        # end if
        if (not wp_verify_nonce(args["nonce"], "edit-theme_" + stylesheet + "_" + file)):
            return php_new_class("WP_Error", lambda : WP_Error("nonce_failure"))
        # end if
        if theme.errors() and "theme_no_stylesheet" == theme.errors().get_error_code():
            return php_new_class("WP_Error", lambda : WP_Error("theme_no_stylesheet", __("The requested theme does not exist.") + " " + theme.errors().get_error_message()))
        # end if
        editable_extensions = wp_get_theme_file_editable_extensions(theme)
        allowed_files = Array()
        for type in editable_extensions:
            for case in Switch(type):
                if case("php"):
                    allowed_files = php_array_merge(allowed_files, theme.get_files("php", -1))
                    break
                # end if
                if case("css"):
                    style_files = theme.get_files("css", -1)
                    allowed_files["style.css"] = style_files["style.css"]
                    allowed_files = php_array_merge(allowed_files, style_files)
                    break
                # end if
                if case():
                    allowed_files = php_array_merge(allowed_files, theme.get_files(type, -1))
                    break
                # end if
            # end for
        # end for
        #// Compare based on relative paths.
        if 0 != validate_file(file, php_array_keys(allowed_files)):
            return php_new_class("WP_Error", lambda : WP_Error("disallowed_theme_file", __("Sorry, that file cannot be edited.")))
        # end if
        real_file = theme.get_stylesheet_directory() + "/" + file
        is_active = get_stylesheet() == stylesheet or get_template() == stylesheet
    else:
        return php_new_class("WP_Error", lambda : WP_Error("missing_theme_or_plugin"))
    # end if
    #// Ensure file is real.
    if (not php_is_file(real_file)):
        return php_new_class("WP_Error", lambda : WP_Error("file_does_not_exist", __("File does not exist! Please double check the name and try again.")))
    # end if
    #// Ensure file extension is allowed.
    extension = None
    if php_preg_match("/\\.([^.]+)$/", real_file, matches):
        extension = php_strtolower(matches[1])
        if (not php_in_array(extension, editable_extensions, True)):
            return php_new_class("WP_Error", lambda : WP_Error("illegal_file_type", __("Files of this type are not editable.")))
        # end if
    # end if
    previous_content = php_file_get_contents(real_file)
    if (not is_writeable(real_file)):
        return php_new_class("WP_Error", lambda : WP_Error("file_not_writable"))
    # end if
    f = fopen(real_file, "w+")
    if False == f:
        return php_new_class("WP_Error", lambda : WP_Error("file_not_writable"))
    # end if
    written = fwrite(f, content)
    php_fclose(f)
    if False == written:
        return php_new_class("WP_Error", lambda : WP_Error("unable_to_write", __("Unable to write to file.")))
    # end if
    if "php" == extension and php_function_exists("opcache_invalidate"):
        opcache_invalidate(real_file, True)
    # end if
    if is_active and "php" == extension:
        scrape_key = php_md5(rand())
        transient = "scrape_key_" + scrape_key
        scrape_nonce = php_strval(rand())
        #// It shouldn't take more than 60 seconds to make the two loopback requests.
        set_transient(transient, scrape_nonce, 60)
        cookies = wp_unslash(PHP_COOKIE)
        scrape_params = Array({"wp_scrape_key": scrape_key, "wp_scrape_nonce": scrape_nonce})
        headers = Array({"Cache-Control": "no-cache"})
        #// This filter is documented in wp-includes/class-wp-http-streams.php
        sslverify = apply_filters("https_local_ssl_verify", False)
        #// Include Basic auth in loopback requests.
        if (php_isset(lambda : PHP_SERVER["PHP_AUTH_USER"])) and (php_isset(lambda : PHP_SERVER["PHP_AUTH_PW"])):
            headers["Authorization"] = "Basic " + php_base64_encode(wp_unslash(PHP_SERVER["PHP_AUTH_USER"]) + ":" + wp_unslash(PHP_SERVER["PHP_AUTH_PW"]))
        # end if
        #// Make sure PHP process doesn't die before loopback requests complete.
        set_time_limit(300)
        #// Time to wait for loopback requests to finish.
        timeout = 100
        needle_start = str("###### wp_scraping_result_start:") + str(scrape_key) + str(" ######")
        needle_end = str("###### wp_scraping_result_end:") + str(scrape_key) + str(" ######")
        #// Attempt loopback request to editor to see if user just whitescreened themselves.
        if plugin:
            url = add_query_arg(compact("plugin", "file"), admin_url("plugin-editor.php"))
        elif (php_isset(lambda : stylesheet)):
            url = add_query_arg(Array({"theme": stylesheet, "file": file}), admin_url("theme-editor.php"))
        else:
            url = admin_url()
        # end if
        url = add_query_arg(scrape_params, url)
        r = wp_remote_get(url, compact("cookies", "headers", "timeout", "sslverify"))
        body = wp_remote_retrieve_body(r)
        scrape_result_position = php_strpos(body, needle_start)
        loopback_request_failure = Array({"code": "loopback_request_failed", "message": __("Unable to communicate back with site to check for fatal errors, so the PHP change was reverted. You will need to upload your PHP file change by some other means, such as by using SFTP.")})
        json_parse_failure = Array({"code": "json_parse_error"})
        result = None
        if False == scrape_result_position:
            result = loopback_request_failure
        else:
            error_output = php_substr(body, scrape_result_position + php_strlen(needle_start))
            error_output = php_substr(error_output, 0, php_strpos(error_output, needle_end))
            result = php_json_decode(php_trim(error_output), True)
            if php_empty(lambda : result):
                result = json_parse_failure
            # end if
        # end if
        #// Try making request to homepage as well to see if visitors have been whitescreened.
        if True == result:
            url = home_url("/")
            url = add_query_arg(scrape_params, url)
            r = wp_remote_get(url, compact("cookies", "headers", "timeout"))
            body = wp_remote_retrieve_body(r)
            scrape_result_position = php_strpos(body, needle_start)
            if False == scrape_result_position:
                result = loopback_request_failure
            else:
                error_output = php_substr(body, scrape_result_position + php_strlen(needle_start))
                error_output = php_substr(error_output, 0, php_strpos(error_output, needle_end))
                result = php_json_decode(php_trim(error_output), True)
                if php_empty(lambda : result):
                    result = json_parse_failure
                # end if
            # end if
        # end if
        delete_transient(transient)
        if True != result:
            #// Roll-back file change.
            file_put_contents(real_file, previous_content)
            if php_function_exists("opcache_invalidate"):
                opcache_invalidate(real_file, True)
            # end if
            if (not (php_isset(lambda : result["message"]))):
                message = __("Something went wrong.")
            else:
                message = result["message"]
                result["message"] = None
            # end if
            return php_new_class("WP_Error", lambda : WP_Error("php_error", message, result))
        # end if
    # end if
    if type(theme).__name__ == "WP_Theme":
        theme.cache_delete()
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
def wp_tempnam(filename="", dir="", *args_):
    
    if php_empty(lambda : dir):
        dir = get_temp_dir()
    # end if
    if php_empty(lambda : filename) or "." == filename or "/" == filename or "\\" == filename:
        filename = uniqid()
    # end if
    #// Use the basename of the given file without the extension as the name for the temporary directory.
    temp_filename = php_basename(filename)
    temp_filename = php_preg_replace("|\\.[^.]*$|", "", temp_filename)
    #// If the folder is falsey, use its parent directory name instead.
    if (not temp_filename):
        return wp_tempnam(php_dirname(filename), dir)
    # end if
    #// Suffix some random data to avoid filename conflicts.
    temp_filename += "-" + wp_generate_password(6, False)
    temp_filename += ".tmp"
    temp_filename = dir + wp_unique_filename(dir, temp_filename)
    fp = php_no_error(lambda: fopen(temp_filename, "x"))
    if (not fp) and php_is_writable(dir) and php_file_exists(temp_filename):
        return wp_tempnam(filename, dir)
    # end if
    if fp:
        php_fclose(fp)
    # end if
    return temp_filename
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
def validate_file_to_edit(file=None, allowed_files=Array(), *args_):
    
    code = validate_file(file, allowed_files)
    if (not code):
        return file
    # end if
    for case in Switch(code):
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
def _wp_handle_upload(file=None, overrides=None, time=None, action=None, *args_):
    
    #// The default error handler.
    if (not php_function_exists("wp_handle_upload_error")):
        def wp_handle_upload_error(file=None, message=None, *args_):
            
            return Array({"error": message})
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
    file = apply_filters(str(action) + str("_prefilter"), file)
    #// You may define your own function and pass the name in $overrides['upload_error_handler'].
    upload_error_handler = "wp_handle_upload_error"
    if (php_isset(lambda : overrides["upload_error_handler"])):
        upload_error_handler = overrides["upload_error_handler"]
    # end if
    #// You may have had one or more 'wp_handle_upload_prefilter' functions error out the file. Handle that gracefully.
    if (php_isset(lambda : file["error"])) and (not php_is_numeric(file["error"])) and file["error"]:
        return call_user_func_array(upload_error_handler, Array(file, file["error"]))
    # end if
    #// Install user overrides. Did we mention that this voids your warranty?
    #// You may define your own function and pass the name in $overrides['unique_filename_callback'].
    unique_filename_callback = None
    if (php_isset(lambda : overrides["unique_filename_callback"])):
        unique_filename_callback = overrides["unique_filename_callback"]
    # end if
    #// 
    #// This may not have originally been intended to be overridable,
    #// but historically has been.
    #//
    if (php_isset(lambda : overrides["upload_error_strings"])):
        upload_error_strings = overrides["upload_error_strings"]
    else:
        #// Courtesy of php.net, the strings that describe the error indicated in $_FILES[{form field}]['error'].
        upload_error_strings = Array(False, php_sprintf(__("The uploaded file exceeds the %1$s directive in %2$s."), "upload_max_filesize", "php.ini"), php_sprintf(__("The uploaded file exceeds the %s directive that was specified in the HTML form."), "MAX_FILE_SIZE"), __("The uploaded file was only partially uploaded."), __("No file was uploaded."), "", __("Missing a temporary folder."), __("Failed to write file to disk."), __("File upload stopped by extension."))
    # end if
    #// All tests are on by default. Most can be turned off by $overrides[{test_name}] = false;
    test_form = overrides["test_form"] if (php_isset(lambda : overrides["test_form"])) else True
    test_size = overrides["test_size"] if (php_isset(lambda : overrides["test_size"])) else True
    #// If you override this, you must provide $ext and $type!!
    test_type = overrides["test_type"] if (php_isset(lambda : overrides["test_type"])) else True
    mimes = overrides["mimes"] if (php_isset(lambda : overrides["mimes"])) else False
    #// A correct form post will pass this test.
    if test_form and (not (php_isset(lambda : PHP_POST["action"]))) or PHP_POST["action"] != action:
        return call_user_func_array(upload_error_handler, Array(file, __("Invalid form submission.")))
    # end if
    #// A successful upload will pass this test. It makes no sense to override this one.
    if (php_isset(lambda : file["error"])) and file["error"] > 0:
        return call_user_func_array(upload_error_handler, Array(file, upload_error_strings[file["error"]]))
    # end if
    #// A properly uploaded file will pass this test. There should be no reason to override this one.
    test_uploaded_file = is_uploaded_file(file["tmp_name"]) if "wp_handle_upload" == action else php_no_error(lambda: php_is_readable(file["tmp_name"]))
    if (not test_uploaded_file):
        return call_user_func_array(upload_error_handler, Array(file, __("Specified file failed upload test.")))
    # end if
    test_file_size = file["size"] if "wp_handle_upload" == action else filesize(file["tmp_name"])
    #// A non-empty file will pass this test.
    if test_size and (not test_file_size > 0):
        if is_multisite():
            error_msg = __("File is empty. Please upload something more substantial.")
        else:
            error_msg = php_sprintf(__("File is empty. Please upload something more substantial. This error could also be caused by uploads being disabled in your %1$s file or by %2$s being defined as smaller than %3$s in %1$s."), "php.ini", "post_max_size", "upload_max_filesize")
        # end if
        return call_user_func_array(upload_error_handler, Array(file, error_msg))
    # end if
    #// A correct MIME type will pass this test. Override $mimes or use the upload_mimes filter.
    if test_type:
        wp_filetype = wp_check_filetype_and_ext(file["tmp_name"], file["name"], mimes)
        ext = "" if php_empty(lambda : wp_filetype["ext"]) else wp_filetype["ext"]
        type = "" if php_empty(lambda : wp_filetype["type"]) else wp_filetype["type"]
        proper_filename = "" if php_empty(lambda : wp_filetype["proper_filename"]) else wp_filetype["proper_filename"]
        #// Check to see if wp_check_filetype_and_ext() determined the filename was incorrect.
        if proper_filename:
            file["name"] = proper_filename
        # end if
        if (not type) or (not ext) and (not current_user_can("unfiltered_upload")):
            return call_user_func_array(upload_error_handler, Array(file, __("Sorry, this file type is not permitted for security reasons.")))
        # end if
        if (not type):
            type = file["type"]
        # end if
    else:
        type = ""
    # end if
    #// 
    #// A writable uploads dir will pass this test. Again, there's no point
    #// overriding this one.
    #//
    uploads = wp_upload_dir(time)
    if (not uploads and False == uploads["error"]):
        return call_user_func_array(upload_error_handler, Array(file, uploads["error"]))
    # end if
    filename = wp_unique_filename(uploads["path"], file["name"], unique_filename_callback)
    #// Move the file to the uploads dir.
    new_file = uploads["path"] + str("/") + str(filename)
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
    move_new_file = apply_filters("pre_move_uploaded_file", None, file, new_file, type)
    if None == move_new_file:
        if "wp_handle_upload" == action:
            move_new_file = php_no_error(lambda: move_uploaded_file(file["tmp_name"], new_file))
        else:
            #// Use copy and unlink because rename breaks streams.
            #// phpcs:ignore WordPress.PHP.NoSilencedErrors.Discouraged
            move_new_file = php_no_error(lambda: copy(file["tmp_name"], new_file))
            unlink(file["tmp_name"])
        # end if
        if False == move_new_file:
            if 0 == php_strpos(uploads["basedir"], ABSPATH):
                error_path = php_str_replace(ABSPATH, "", uploads["basedir"]) + uploads["subdir"]
            else:
                error_path = php_basename(uploads["basedir"]) + uploads["subdir"]
            # end if
            return upload_error_handler(file, php_sprintf(__("The uploaded file could not be moved to %s."), error_path))
        # end if
    # end if
    #// Set correct file permissions.
    stat = stat(php_dirname(new_file))
    perms = stat["mode"] & 438
    chmod(new_file, perms)
    #// Compute the URL.
    url = uploads["url"] + str("/") + str(filename)
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
    return apply_filters("wp_handle_upload", Array({"file": new_file, "url": url, "type": type}), "sideload" if "wp_handle_sideload" == action else "upload")
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
def wp_handle_upload(file=None, overrides=False, time=None, *args_):
    
    #// 
    #// $_POST['action'] must be set and its value must equal $overrides['action']
    #// or this:
    #//
    action = "wp_handle_upload"
    if (php_isset(lambda : overrides["action"])):
        action = overrides["action"]
    # end if
    return _wp_handle_upload(file, overrides, time, action)
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
def wp_handle_sideload(file=None, overrides=False, time=None, *args_):
    
    #// 
    #// $_POST['action'] must be set and its value must equal $overrides['action']
    #// or this:
    #//
    action = "wp_handle_sideload"
    if (php_isset(lambda : overrides["action"])):
        action = overrides["action"]
    # end if
    return _wp_handle_upload(file, overrides, time, action)
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
def download_url(url=None, timeout=300, signature_verification=False, *args_):
    
    #// WARNING: The file is not automatically deleted, the script must unlink() the file.
    if (not url):
        return php_new_class("WP_Error", lambda : WP_Error("http_no_url", __("Invalid URL Provided.")))
    # end if
    url_filename = php_basename(php_parse_url(url, PHP_URL_PATH))
    tmpfname = wp_tempnam(url_filename)
    if (not tmpfname):
        return php_new_class("WP_Error", lambda : WP_Error("http_no_file", __("Could not create Temporary file.")))
    # end if
    response = wp_safe_remote_get(url, Array({"timeout": timeout, "stream": True, "filename": tmpfname}))
    if is_wp_error(response):
        unlink(tmpfname)
        return response
    # end if
    response_code = wp_remote_retrieve_response_code(response)
    if 200 != response_code:
        data = Array({"code": response_code})
        #// Retrieve a sample of the response body for debugging purposes.
        tmpf = fopen(tmpfname, "rb")
        if tmpf:
            #// 
            #// Filters the maximum error response body size in `download_url()`.
            #// 
            #// @since 5.1.0
            #// 
            #// @see download_url()
            #// 
            #// @param int $size The maximum error response body size. Default 1 KB.
            #//
            response_size = apply_filters("download_url_error_max_body_size", KB_IN_BYTES)
            data["body"] = fread(tmpf, response_size)
            php_fclose(tmpf)
        # end if
        unlink(tmpfname)
        return php_new_class("WP_Error", lambda : WP_Error("http_404", php_trim(wp_remote_retrieve_response_message(response)), data))
    # end if
    content_md5 = wp_remote_retrieve_header(response, "content-md5")
    if content_md5:
        md5_check = verify_file_md5(tmpfname, content_md5)
        if is_wp_error(md5_check):
            unlink(tmpfname)
            return md5_check
        # end if
    # end if
    #// If the caller expects signature verification to occur, check to see if this URL supports it.
    if signature_verification:
        #// 
        #// Filters the list of hosts which should have Signature Verification attempted on.
        #// 
        #// @since 5.2.0
        #// 
        #// @param string[] $hostnames List of hostnames.
        #//
        signed_hostnames = apply_filters("wp_signature_hosts", Array("wordpress.org", "downloads.wordpress.org", "s.w.org"))
        signature_verification = php_in_array(php_parse_url(url, PHP_URL_HOST), signed_hostnames, True)
    # end if
    #// Perform signature valiation if supported.
    if signature_verification:
        signature = wp_remote_retrieve_header(response, "x-content-signature")
        if (not signature):
            #// Retrieve signatures from a file if the header wasn't included.
            #// WordPress.org stores signatures at $package_url.sig.
            signature_url = False
            url_path = php_parse_url(url, PHP_URL_PATH)
            if php_substr(url_path, -4) == ".zip" or php_substr(url_path, -7) == ".tar.gz":
                signature_url = php_str_replace(url_path, url_path + ".sig", url)
            # end if
            #// 
            #// Filter the URL where the signature for a file is located.
            #// 
            #// @since 5.2.0
            #// 
            #// @param false|string $signature_url The URL where signatures can be found for a file, or false if none are known.
            #// @param string $url                 The URL being verified.
            #//
            signature_url = apply_filters("wp_signature_url", signature_url, url)
            if signature_url:
                signature_request = wp_safe_remote_get(signature_url, Array({"limit_response_size": 10 * KB_IN_BYTES}))
                if (not is_wp_error(signature_request)) and 200 == wp_remote_retrieve_response_code(signature_request):
                    signature = php_explode("\n", wp_remote_retrieve_body(signature_request))
                # end if
            # end if
        # end if
        #// Perform the checks.
        signature_verification = verify_file_signature(tmpfname, signature, php_basename(php_parse_url(url, PHP_URL_PATH)))
    # end if
    if is_wp_error(signature_verification):
        if apply_filters("wp_signature_softfail", True, url):
            signature_verification.add_data(tmpfname, "softfail-filename")
        else:
            #// Hard-fail.
            unlink(tmpfname)
        # end if
        return signature_verification
    # end if
    return tmpfname
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
def verify_file_md5(filename=None, expected_md5=None, *args_):
    
    if 32 == php_strlen(expected_md5):
        expected_raw_md5 = pack("H*", expected_md5)
    elif 24 == php_strlen(expected_md5):
        expected_raw_md5 = php_base64_decode(expected_md5)
    else:
        return False
        pass
    # end if
    file_md5 = php_md5_file(filename, True)
    if file_md5 == expected_raw_md5:
        return True
    # end if
    return php_new_class("WP_Error", lambda : WP_Error("md5_mismatch", php_sprintf(__("The checksum of the file (%1$s) does not match the expected checksum value (%2$s)."), bin2hex(file_md5), bin2hex(expected_raw_md5))))
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
def verify_file_signature(filename=None, signatures=None, filename_for_errors=False, *args_):
    
    if (not filename_for_errors):
        filename_for_errors = wp_basename(filename)
    # end if
    #// Check we can process signatures.
    if (not php_function_exists("sodium_crypto_sign_verify_detached")) or (not php_in_array("sha384", php_array_map("strtolower", hash_algos()))):
        return php_new_class("WP_Error", lambda : WP_Error("signature_verification_unsupported", php_sprintf(__("The authenticity of %s could not be verified as signature verification is unavailable on this system."), "<span class=\"code\">" + esc_html(filename_for_errors) + "</span>"), "sodium_crypto_sign_verify_detached" if (not php_function_exists("sodium_crypto_sign_verify_detached")) else "sha384"))
    # end if
    #// Check for a edge-case affecting PHP Maths abilities.
    if (not php_extension_loaded("sodium")) and php_in_array(PHP_VERSION_ID, Array(70200, 70201, 70202), True) and php_extension_loaded("opcache"):
        #// Sodium_Compat isn't compatible with PHP 7.2.0~7.2.2 due to a bug in the PHP Opcache extension, bail early as it'll fail.
        #// https://bugs.php.net/bug.php?id=75938
        return php_new_class("WP_Error", lambda : WP_Error("signature_verification_unsupported", php_sprintf(__("The authenticity of %s could not be verified as signature verification is unavailable on this system."), "<span class=\"code\">" + esc_html(filename_for_errors) + "</span>"), Array({"php": php_phpversion(), "sodium": SODIUM_LIBRARY_VERSION if php_defined("SODIUM_LIBRARY_VERSION") else ParagonIE_Sodium_Compat.VERSION_STRING if php_defined("ParagonIE_Sodium_Compat::VERSION_STRING") else False})))
    # end if
    #// Verify runtime speed of Sodium_Compat is acceptable.
    if (not php_extension_loaded("sodium")) and (not ParagonIE_Sodium_Compat.polyfill_is_fast()):
        sodium_compat_is_fast = False
        #// Allow for an old version of Sodium_Compat being loaded before the bundled WordPress one.
        if php_method_exists("ParagonIE_Sodium_Compat", "runtime_speed_test"):
            #// Run `ParagonIE_Sodium_Compat::runtime_speed_test()` in optimized integer mode, as that's what WordPress utilises during signing verifications.
            #// phpcs:disable WordPress.NamingConventions.ValidVariableName
            old_fastMult = ParagonIE_Sodium_Compat.fastMult
            ParagonIE_Sodium_Compat.fastMult = True
            sodium_compat_is_fast = ParagonIE_Sodium_Compat.runtime_speed_test(100, 10)
            ParagonIE_Sodium_Compat.fastMult = old_fastMult
            pass
        # end if
        #// This cannot be performed in a reasonable amount of time.
        #// https://github.com/paragonie/sodium_compat#help-sodium_compat-is-slow-how-can-i-make-it-fast
        if (not sodium_compat_is_fast):
            return php_new_class("WP_Error", lambda : WP_Error("signature_verification_unsupported", php_sprintf(__("The authenticity of %s could not be verified as signature verification is unavailable on this system."), "<span class=\"code\">" + esc_html(filename_for_errors) + "</span>"), Array({"php": php_phpversion(), "sodium": SODIUM_LIBRARY_VERSION if php_defined("SODIUM_LIBRARY_VERSION") else ParagonIE_Sodium_Compat.VERSION_STRING if php_defined("ParagonIE_Sodium_Compat::VERSION_STRING") else False, "polyfill_is_fast": False, "max_execution_time": php_ini_get("max_execution_time")})))
        # end if
    # end if
    if (not signatures):
        return php_new_class("WP_Error", lambda : WP_Error("signature_verification_no_signature", php_sprintf(__("The authenticity of %s could not be verified as no signature was found."), "<span class=\"code\">" + esc_html(filename_for_errors) + "</span>"), Array({"filename": filename_for_errors})))
    # end if
    trusted_keys = wp_trusted_keys()
    file_hash = hash_file("sha384", filename, True)
    mbstring_binary_safe_encoding()
    skipped_key = 0
    skipped_signature = 0
    for signature in signatures:
        signature_raw = php_base64_decode(signature)
        #// Ensure only valid-length signatures are considered.
        if SODIUM_CRYPTO_SIGN_BYTES != php_strlen(signature_raw):
            skipped_signature += 1
            continue
        # end if
        for key in trusted_keys:
            key_raw = php_base64_decode(key)
            #// Only pass valid public keys through.
            if SODIUM_CRYPTO_SIGN_PUBLICKEYBYTES != php_strlen(key_raw):
                skipped_key += 1
                continue
            # end if
            if sodium_crypto_sign_verify_detached(signature_raw, file_hash, key_raw):
                reset_mbstring_encoding()
                return True
            # end if
        # end for
    # end for
    reset_mbstring_encoding()
    return php_new_class("WP_Error", lambda : WP_Error("signature_verification_failed", php_sprintf(__("The authenticity of %s could not be verified."), "<span class=\"code\">" + esc_html(filename_for_errors) + "</span>"), Array({"filename": filename_for_errors, "keys": trusted_keys, "signatures": signatures, "hash": bin2hex(file_hash), "skipped_key": skipped_key, "skipped_sig": skipped_signature, "php": php_phpversion(), "sodium": SODIUM_LIBRARY_VERSION if php_defined("SODIUM_LIBRARY_VERSION") else ParagonIE_Sodium_Compat.VERSION_STRING if php_defined("ParagonIE_Sodium_Compat::VERSION_STRING") else False})))
# end def verify_file_signature
#// 
#// Retrieve the list of signing keys trusted by WordPress.
#// 
#// @since 5.2.0
#// 
#// @return string[] Array of base64-encoded signing keys.
#//
def wp_trusted_keys(*args_):
    
    trusted_keys = Array()
    if time() < 1617235200:
        #// WordPress.org Key #1 - This key is only valid before April 1st, 2021.
        trusted_keys[-1] = "fRPyrxb/MvVLbdsYi+OOEv4xc+Eqpsj+kkAS6gNOkI0="
    # end if
    #// TODO: Add key #2 with longer expiration.
    #// 
    #// Filter the valid signing keys used to verify the contents of files.
    #// 
    #// @since 5.2.0
    #// 
    #// @param string[] $trusted_keys The trusted keys that may sign packages.
    #//
    return apply_filters("wp_trusted_keys", trusted_keys)
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
def unzip_file(file=None, to=None, *args_):
    
    global wp_filesystem
    php_check_if_defined("wp_filesystem")
    if (not wp_filesystem) or (not php_is_object(wp_filesystem)):
        return php_new_class("WP_Error", lambda : WP_Error("fs_unavailable", __("Could not access filesystem.")))
    # end if
    #// Unzip can use a lot of memory, but not this much hopefully.
    wp_raise_memory_limit("admin")
    needed_dirs = Array()
    to = trailingslashit(to)
    #// Determine any parent directories needed (of the upgrade directory).
    if (not wp_filesystem.is_dir(to)):
        #// Only do parents if no children exist.
        path = php_preg_split("![/\\\\]!", untrailingslashit(to))
        i = php_count(path)
        while i >= 0:
            
            if php_empty(lambda : path[i]):
                continue
            # end if
            dir = php_implode("/", php_array_slice(path, 0, i + 1))
            if php_preg_match("!^[a-z]:$!i", dir):
                continue
            # end if
            if (not wp_filesystem.is_dir(dir)):
                needed_dirs[-1] = dir
            else:
                break
                pass
            # end if
            i -= 1
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
        result = _unzip_file_ziparchive(file, to, needed_dirs)
        if True == result:
            return result
        elif is_wp_error(result):
            if "incompatible_archive" != result.get_error_code():
                return result
            # end if
        # end if
    # end if
    #// Fall through to PclZip if ZipArchive is not available, or encountered an error opening the file.
    return _unzip_file_pclzip(file, to, needed_dirs)
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
def _unzip_file_ziparchive(file=None, to=None, needed_dirs=Array(), *args_):
    
    global wp_filesystem
    php_check_if_defined("wp_filesystem")
    z = php_new_class("ZipArchive", lambda : ZipArchive())
    zopen = z.open(file, ZIPARCHIVE.CHECKCONS)
    if True != zopen:
        return php_new_class("WP_Error", lambda : WP_Error("incompatible_archive", __("Incompatible Archive."), Array({"ziparchive_error": zopen})))
    # end if
    uncompressed_size = 0
    i = 0
    while i < z.numFiles:
        
        info = z.statindex(i)
        if (not info):
            return php_new_class("WP_Error", lambda : WP_Error("stat_failed_ziparchive", __("Could not retrieve file from archive.")))
        # end if
        if "__MACOSX/" == php_substr(info["name"], 0, 9):
            continue
        # end if
        #// Don't extract invalid files:
        if 0 != validate_file(info["name"]):
            continue
        # end if
        uncompressed_size += info["size"]
        dirname = php_dirname(info["name"])
        if "/" == php_substr(info["name"], -1):
            #// Directory.
            needed_dirs[-1] = to + untrailingslashit(info["name"])
        elif "." != dirname:
            #// Path to a file.
            needed_dirs[-1] = to + untrailingslashit(dirname)
        # end if
        i += 1
    # end while
    #// 
    #// disk_free_space() could return false. Assume that any falsey value is an error.
    #// A disk that has zero free bytes has bigger problems.
    #// Require we have enough space to unzip the file and copy its contents, with a 10% buffer.
    #//
    if wp_doing_cron():
        available_space = php_no_error(lambda: disk_free_space(WP_CONTENT_DIR))
        if available_space and uncompressed_size * 2.1 > available_space:
            return php_new_class("WP_Error", lambda : WP_Error("disk_full_unzip_file", __("Could not copy files. You may have run out of disk space."), compact("uncompressed_size", "available_space")))
        # end if
    # end if
    needed_dirs = array_unique(needed_dirs)
    for dir in needed_dirs:
        #// Check the parent folders of the folders all exist within the creation array.
        if untrailingslashit(to) == dir:
            continue
        # end if
        if php_strpos(dir, to) == False:
            continue
        # end if
        parent_folder = php_dirname(dir)
        while True:
            
            if not ((not php_empty(lambda : parent_folder)) and untrailingslashit(to) != parent_folder and (not php_in_array(parent_folder, needed_dirs))):
                break
            # end if
            needed_dirs[-1] = parent_folder
            parent_folder = php_dirname(parent_folder)
        # end while
    # end for
    asort(needed_dirs)
    #// Create those directories if need be:
    for _dir in needed_dirs:
        #// Only check to see if the Dir exists upon creation failure. Less I/O this way.
        if (not wp_filesystem.mkdir(_dir, FS_CHMOD_DIR)) and (not wp_filesystem.is_dir(_dir)):
            return php_new_class("WP_Error", lambda : WP_Error("mkdir_failed_ziparchive", __("Could not create directory."), php_substr(_dir, php_strlen(to))))
        # end if
    # end for
    needed_dirs = None
    i = 0
    while i < z.numFiles:
        
        info = z.statindex(i)
        if (not info):
            return php_new_class("WP_Error", lambda : WP_Error("stat_failed_ziparchive", __("Could not retrieve file from archive.")))
        # end if
        if "/" == php_substr(info["name"], -1):
            continue
        # end if
        if "__MACOSX/" == php_substr(info["name"], 0, 9):
            continue
        # end if
        #// Don't extract invalid files:
        if 0 != validate_file(info["name"]):
            continue
        # end if
        contents = z.getfromindex(i)
        if False == contents:
            return php_new_class("WP_Error", lambda : WP_Error("extract_failed_ziparchive", __("Could not extract file from archive."), info["name"]))
        # end if
        if (not wp_filesystem.put_contents(to + info["name"], contents, FS_CHMOD_FILE)):
            return php_new_class("WP_Error", lambda : WP_Error("copy_failed_ziparchive", __("Could not copy file."), info["name"]))
        # end if
        i += 1
    # end while
    z.close()
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
def _unzip_file_pclzip(file=None, to=None, needed_dirs=Array(), *args_):
    
    global wp_filesystem
    php_check_if_defined("wp_filesystem")
    mbstring_binary_safe_encoding()
    php_include_file(ABSPATH + "wp-admin/includes/class-pclzip.php", once=True)
    archive = php_new_class("PclZip", lambda : PclZip(file))
    archive_files = archive.extract(PCLZIP_OPT_EXTRACT_AS_STRING)
    reset_mbstring_encoding()
    #// Is the archive valid?
    if (not php_is_array(archive_files)):
        return php_new_class("WP_Error", lambda : WP_Error("incompatible_archive", __("Incompatible Archive."), archive.errorinfo(True)))
    # end if
    if 0 == php_count(archive_files):
        return php_new_class("WP_Error", lambda : WP_Error("empty_archive_pclzip", __("Empty archive.")))
    # end if
    uncompressed_size = 0
    #// Determine any children directories needed (From within the archive).
    for file in archive_files:
        if "__MACOSX/" == php_substr(file["filename"], 0, 9):
            continue
        # end if
        uncompressed_size += file["size"]
        needed_dirs[-1] = to + untrailingslashit(file["filename"] if file["folder"] else php_dirname(file["filename"]))
    # end for
    #// 
    #// disk_free_space() could return false. Assume that any falsey value is an error.
    #// A disk that has zero free bytes has bigger problems.
    #// Require we have enough space to unzip the file and copy its contents, with a 10% buffer.
    #//
    if wp_doing_cron():
        available_space = php_no_error(lambda: disk_free_space(WP_CONTENT_DIR))
        if available_space and uncompressed_size * 2.1 > available_space:
            return php_new_class("WP_Error", lambda : WP_Error("disk_full_unzip_file", __("Could not copy files. You may have run out of disk space."), compact("uncompressed_size", "available_space")))
        # end if
    # end if
    needed_dirs = array_unique(needed_dirs)
    for dir in needed_dirs:
        #// Check the parent folders of the folders all exist within the creation array.
        if untrailingslashit(to) == dir:
            continue
        # end if
        if php_strpos(dir, to) == False:
            continue
        # end if
        parent_folder = php_dirname(dir)
        while True:
            
            if not ((not php_empty(lambda : parent_folder)) and untrailingslashit(to) != parent_folder and (not php_in_array(parent_folder, needed_dirs))):
                break
            # end if
            needed_dirs[-1] = parent_folder
            parent_folder = php_dirname(parent_folder)
        # end while
    # end for
    asort(needed_dirs)
    #// Create those directories if need be:
    for _dir in needed_dirs:
        #// Only check to see if the dir exists upon creation failure. Less I/O this way.
        if (not wp_filesystem.mkdir(_dir, FS_CHMOD_DIR)) and (not wp_filesystem.is_dir(_dir)):
            return php_new_class("WP_Error", lambda : WP_Error("mkdir_failed_pclzip", __("Could not create directory."), php_substr(_dir, php_strlen(to))))
        # end if
    # end for
    needed_dirs = None
    #// Extract the files from the zip.
    for file in archive_files:
        if file["folder"]:
            continue
        # end if
        if "__MACOSX/" == php_substr(file["filename"], 0, 9):
            continue
        # end if
        #// Don't extract invalid files:
        if 0 != validate_file(file["filename"]):
            continue
        # end if
        if (not wp_filesystem.put_contents(to + file["filename"], file["content"], FS_CHMOD_FILE)):
            return php_new_class("WP_Error", lambda : WP_Error("copy_failed_pclzip", __("Could not copy file."), file["filename"]))
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
def copy_dir(from_=None, to=None, skip_list=Array(), *args_):
    
    global wp_filesystem
    php_check_if_defined("wp_filesystem")
    dirlist = wp_filesystem.dirlist(from_)
    from_ = trailingslashit(from_)
    to = trailingslashit(to)
    for filename,fileinfo in dirlist:
        if php_in_array(filename, skip_list, True):
            continue
        # end if
        if "f" == fileinfo["type"]:
            if (not wp_filesystem.copy(from_ + filename, to + filename, True, FS_CHMOD_FILE)):
                #// If copy failed, chmod file to 0644 and try again.
                wp_filesystem.chmod(to + filename, FS_CHMOD_FILE)
                if (not wp_filesystem.copy(from_ + filename, to + filename, True, FS_CHMOD_FILE)):
                    return php_new_class("WP_Error", lambda : WP_Error("copy_failed_copy_dir", __("Could not copy file."), to + filename))
                # end if
            # end if
        elif "d" == fileinfo["type"]:
            if (not wp_filesystem.is_dir(to + filename)):
                if (not wp_filesystem.mkdir(to + filename, FS_CHMOD_DIR)):
                    return php_new_class("WP_Error", lambda : WP_Error("mkdir_failed_copy_dir", __("Could not create directory."), to + filename))
                # end if
            # end if
            #// Generate the $sub_skip_list for the subdirectory as a sub-set of the existing $skip_list.
            sub_skip_list = Array()
            for skip_item in skip_list:
                if 0 == php_strpos(skip_item, filename + "/"):
                    sub_skip_list[-1] = php_preg_replace("!^" + preg_quote(filename, "!") + "/!i", "", skip_item)
                # end if
            # end for
            result = copy_dir(from_ + filename, to + filename, sub_skip_list)
            if is_wp_error(result):
                return result
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
def WP_Filesystem(args=False, context=False, allow_relaxed_file_ownership=False, *args_):
    
    #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.FunctionNameInvalid
    global wp_filesystem
    php_check_if_defined("wp_filesystem")
    php_include_file(ABSPATH + "wp-admin/includes/class-wp-filesystem-base.php", once=True)
    method = get_filesystem_method(args, context, allow_relaxed_file_ownership)
    if (not method):
        return False
    # end if
    if (not php_class_exists(str("WP_Filesystem_") + str(method))):
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
        abstraction_file = apply_filters("filesystem_method_file", ABSPATH + "wp-admin/includes/class-wp-filesystem-" + method + ".php", method)
        if (not php_file_exists(abstraction_file)):
            return
        # end if
        php_include_file(abstraction_file, once=True)
    # end if
    method = str("WP_Filesystem_") + str(method)
    wp_filesystem = php_new_class(method, lambda : {**locals(), **globals()}[method](args))
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
    if is_wp_error(wp_filesystem.errors) and wp_filesystem.errors.has_errors():
        return False
    # end if
    if (not wp_filesystem.connect()):
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
def get_filesystem_method(args=Array(), context="", allow_relaxed_file_ownership=False, *args_):
    global PHP_GLOBALS
    #// Please ensure that this is either 'direct', 'ssh2', 'ftpext', or 'ftpsockets'.
    method = FS_METHOD if php_defined("FS_METHOD") else False
    if (not context):
        context = WP_CONTENT_DIR
    # end if
    #// If the directory doesn't exist (wp-content/languages) then use the parent directory as we'll create it.
    if WP_LANG_DIR == context and (not php_is_dir(context)):
        context = php_dirname(context)
    # end if
    context = trailingslashit(context)
    if (not method):
        temp_file_name = context + "temp-write-test-" + php_str_replace(".", "-", uniqid("", True))
        temp_handle = php_no_error(lambda: fopen(temp_file_name, "w"))
        if temp_handle:
            #// Attempt to determine the file owner of the WordPress files, and that of newly created files.
            wp_file_owner = False
            temp_file_owner = False
            if php_function_exists("fileowner"):
                wp_file_owner = php_no_error(lambda: fileowner(__FILE__))
                temp_file_owner = php_no_error(lambda: fileowner(temp_file_name))
            # end if
            if False != wp_file_owner and wp_file_owner == temp_file_owner:
                #// 
                #// WordPress is creating files as the same owner as the WordPress files,
                #// this means it's safe to modify & create new files via PHP.
                #//
                method = "direct"
                PHP_GLOBALS["_wp_filesystem_direct_method"] = "file_owner"
            elif allow_relaxed_file_ownership:
                #// 
                #// The $context directory is writable, and $allow_relaxed_file_ownership is set,
                #// this means we can modify files safely in this directory.
                #// This mode doesn't create new files, only alter existing ones.
                #//
                method = "direct"
                PHP_GLOBALS["_wp_filesystem_direct_method"] = "relaxed_ownership"
            # end if
            php_fclose(temp_handle)
            php_no_error(lambda: unlink(temp_file_name))
        # end if
    # end if
    if (not method) and (php_isset(lambda : args["connection_type"])) and "ssh" == args["connection_type"] and php_extension_loaded("ssh2") and php_function_exists("stream_get_contents"):
        method = "ssh2"
    # end if
    if (not method) and php_extension_loaded("ftp"):
        method = "ftpext"
    # end if
    if (not method) and php_extension_loaded("sockets") or php_function_exists("fsockopen"):
        method = "ftpsockets"
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
    return apply_filters("filesystem_method", method, args, context, allow_relaxed_file_ownership)
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
def request_filesystem_credentials(form_post=None, type="", error=False, context="", extra_fields=None, allow_relaxed_file_ownership=False, *args_):
    
    global pagenow
    php_check_if_defined("pagenow")
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
    req_cred = apply_filters("request_filesystem_credentials", "", form_post, type, error, context, extra_fields, allow_relaxed_file_ownership)
    if "" != req_cred:
        return req_cred
    # end if
    if php_empty(lambda : type):
        type = get_filesystem_method(Array(), context, allow_relaxed_file_ownership)
    # end if
    if "direct" == type:
        return True
    # end if
    if is_null(extra_fields):
        extra_fields = Array("version", "locale")
    # end if
    credentials = get_option("ftp_credentials", Array({"hostname": "", "username": ""}))
    submitted_form = wp_unslash(PHP_POST)
    #// Verify nonce, or unset submitted form field values on failure.
    if (not (php_isset(lambda : PHP_POST["_fs_nonce"]))) or (not wp_verify_nonce(PHP_POST["_fs_nonce"], "filesystem-credentials")):
        submitted_form["hostname"] = None
        submitted_form["username"] = None
        submitted_form["password"] = None
        submitted_form["public_key"] = None
        submitted_form["private_key"] = None
        submitted_form["connection_type"] = None
    # end if
    #// If defined, set it to that. Else, if POST'd, set it to that. If not, set it to whatever it previously was (saved details in option).
    credentials["hostname"] = FTP_HOST if php_defined("FTP_HOST") else submitted_form["hostname"] if (not php_empty(lambda : submitted_form["hostname"])) else credentials["hostname"]
    credentials["username"] = FTP_USER if php_defined("FTP_USER") else submitted_form["username"] if (not php_empty(lambda : submitted_form["username"])) else credentials["username"]
    credentials["password"] = FTP_PASS if php_defined("FTP_PASS") else submitted_form["password"] if (not php_empty(lambda : submitted_form["password"])) else ""
    #// Check to see if we are setting the public/private keys for ssh.
    credentials["public_key"] = FTP_PUBKEY if php_defined("FTP_PUBKEY") else submitted_form["public_key"] if (not php_empty(lambda : submitted_form["public_key"])) else ""
    credentials["private_key"] = FTP_PRIKEY if php_defined("FTP_PRIKEY") else submitted_form["private_key"] if (not php_empty(lambda : submitted_form["private_key"])) else ""
    #// Sanitize the hostname, some people might pass in odd data.
    credentials["hostname"] = php_preg_replace("|\\w+://|", "", credentials["hostname"])
    #// Strip any schemes off.
    if php_strpos(credentials["hostname"], ":"):
        credentials["hostname"], credentials["port"] = php_explode(":", credentials["hostname"], 2)
        if (not php_is_numeric(credentials["port"])):
            credentials["port"] = None
        # end if
    else:
        credentials["port"] = None
    # end if
    if php_defined("FTP_SSH") and FTP_SSH or php_defined("FS_METHOD") and "ssh2" == FS_METHOD:
        credentials["connection_type"] = "ssh"
    elif php_defined("FTP_SSL") and FTP_SSL and "ftpext" == type:
        #// Only the FTP Extension understands SSL.
        credentials["connection_type"] = "ftps"
    elif (not php_empty(lambda : submitted_form["connection_type"])):
        credentials["connection_type"] = submitted_form["connection_type"]
    elif (not (php_isset(lambda : credentials["connection_type"]))):
        #// All else fails (and it's not defaulted to something else saved), default to FTP.
        credentials["connection_type"] = "ftp"
    # end if
    if (not error) and (not php_empty(lambda : credentials["password"])) and (not php_empty(lambda : credentials["username"])) and (not php_empty(lambda : credentials["hostname"])) or "ssh" == credentials["connection_type"] and (not php_empty(lambda : credentials["public_key"])) and (not php_empty(lambda : credentials["private_key"])):
        stored_credentials = credentials
        if (not php_empty(lambda : stored_credentials["port"])):
            #// Save port as part of hostname to simplify above code.
            stored_credentials["hostname"] += ":" + stored_credentials["port"]
        # end if
        stored_credentials["password"] = None
        stored_credentials["port"] = None
        stored_credentials["private_key"] = None
        stored_credentials["public_key"] = None
        if (not wp_installing()):
            update_option("ftp_credentials", stored_credentials)
        # end if
        return credentials
    # end if
    hostname = credentials["hostname"] if (php_isset(lambda : credentials["hostname"])) else ""
    username = credentials["username"] if (php_isset(lambda : credentials["username"])) else ""
    public_key = credentials["public_key"] if (php_isset(lambda : credentials["public_key"])) else ""
    private_key = credentials["private_key"] if (php_isset(lambda : credentials["private_key"])) else ""
    port = credentials["port"] if (php_isset(lambda : credentials["port"])) else ""
    connection_type = credentials["connection_type"] if (php_isset(lambda : credentials["connection_type"])) else ""
    if error:
        error_string = __("<strong>Error</strong>: There was an error connecting to the server, Please verify the settings are correct.")
        if is_wp_error(error):
            error_string = esc_html(error.get_error_message())
        # end if
        php_print("<div id=\"message\" class=\"error\"><p>" + error_string + "</p></div>")
    # end if
    types = Array()
    if php_extension_loaded("ftp") or php_extension_loaded("sockets") or php_function_exists("fsockopen"):
        types["ftp"] = __("FTP")
    # end if
    if php_extension_loaded("ftp"):
        #// Only this supports FTPS.
        types["ftps"] = __("FTPS (SSL)")
    # end if
    if php_extension_loaded("ssh2") and php_function_exists("stream_get_contents"):
        types["ssh"] = __("SSH2")
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
    types = apply_filters("fs_ftp_connection_types", types, credentials, type, error, context)
    php_print("<form action=\"")
    php_print(esc_url(form_post))
    php_print("\" method=\"post\">\n<div id=\"request-filesystem-credentials-form\" class=\"request-filesystem-credentials-form\">\n    ")
    #// Print a H1 heading in the FTP credentials modal dialog, default is a H2.
    heading_tag = "h2"
    if "plugins.php" == pagenow or "plugin-install.php" == pagenow:
        heading_tag = "h1"
    # end if
    php_print(str("<") + str(heading_tag) + str(" id='request-filesystem-credentials-title'>") + __("Connection Information") + str("</") + str(heading_tag) + str(">"))
    php_print("<p id=\"request-filesystem-credentials-desc\">\n ")
    label_user = __("Username")
    label_pass = __("Password")
    _e("To perform the requested action, WordPress needs to access your web server.")
    php_print(" ")
    if (php_isset(lambda : types["ftp"])) or (php_isset(lambda : types["ftps"])):
        if (php_isset(lambda : types["ssh"])):
            _e("Please enter your FTP or SSH credentials to proceed.")
            label_user = __("FTP/SSH Username")
            label_pass = __("FTP/SSH Password")
        else:
            _e("Please enter your FTP credentials to proceed.")
            label_user = __("FTP Username")
            label_pass = __("FTP Password")
        # end if
        php_print(" ")
    # end if
    _e("If you do not remember your credentials, you should contact your web host.")
    hostname_value = esc_attr(hostname)
    if (not php_empty(lambda : port)):
        hostname_value += str(":") + str(port)
    # end if
    password_value = ""
    if php_defined("FTP_PASS"):
        password_value = "*****"
    # end if
    php_print("</p>\n<label for=\"hostname\">\n <span class=\"field-title\">")
    _e("Hostname")
    php_print("</span>\n    <input name=\"hostname\" type=\"text\" id=\"hostname\" aria-describedby=\"request-filesystem-credentials-desc\" class=\"code\" placeholder=\"")
    esc_attr_e("example: www.wordpress.org")
    php_print("\" value=\"")
    php_print(hostname_value)
    php_print("\"")
    disabled(php_defined("FTP_HOST"))
    php_print(""" />
    </label>
    <div class=\"ftp-username\">
    <label for=\"username\">
    <span class=\"field-title\">""")
    php_print(label_user)
    php_print("</span>\n        <input name=\"username\" type=\"text\" id=\"username\" value=\"")
    php_print(esc_attr(username))
    php_print("\"")
    disabled(php_defined("FTP_USER"))
    php_print(""" />
    </label>
    </div>
    <div class=\"ftp-password\">
    <label for=\"password\">
    <span class=\"field-title\">""")
    php_print(label_pass)
    php_print("</span>\n        <input name=\"password\" type=\"password\" id=\"password\" value=\"")
    php_print(password_value)
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
    disabled = disabled(php_defined("FTP_SSL") and FTP_SSL or php_defined("FTP_SSH") and FTP_SSH, True, False)
    for name,text in types:
        php_print(" <label for=\"")
        php_print(esc_attr(name))
        php_print("\">\n        <input type=\"radio\" name=\"connection_type\" id=\"")
        php_print(esc_attr(name))
        php_print("\" value=\"")
        php_print(esc_attr(name))
        php_print("\" ")
        checked(name, connection_type)
        php_print(" ")
        php_print(disabled)
        php_print(" />\n        ")
        php_print(text)
        php_print(" </label>\n      ")
    # end for
    php_print("</fieldset>\n    ")
    if (php_isset(lambda : types["ssh"])):
        hidden_class = ""
        if "ssh" != connection_type or php_empty(lambda : connection_type):
            hidden_class = " class=\"hidden\""
        # end if
        php_print("<fieldset id=\"ssh-keys\"")
        php_print(hidden_class)
        php_print(">\n<legend>")
        _e("Authentication Keys")
        php_print("</legend>\n<label for=\"public_key\">\n  <span class=\"field-title\">")
        _e("Public Key:")
        php_print("</span>\n    <input name=\"public_key\" type=\"text\" id=\"public_key\" aria-describedby=\"auth-keys-desc\" value=\"")
        php_print(esc_attr(public_key))
        php_print("\"")
        disabled(php_defined("FTP_PUBKEY"))
        php_print(""" />
        </label>
        <label for=\"private_key\">
        <span class=\"field-title\">""")
        _e("Private Key:")
        php_print("</span>\n    <input name=\"private_key\" type=\"text\" id=\"private_key\" value=\"")
        php_print(esc_attr(private_key))
        php_print("\"")
        disabled(php_defined("FTP_PRIKEY"))
        php_print(" />\n</label>\n<p id=\"auth-keys-desc\">")
        _e("Enter the location on the server where the public and private keys are located. If a passphrase is needed, enter that in the password field above.")
        php_print("</p>\n</fieldset>\n      ")
    # end if
    for field in extra_fields:
        if (php_isset(lambda : submitted_form[field])):
            php_print("<input type=\"hidden\" name=\"" + esc_attr(field) + "\" value=\"" + esc_attr(submitted_form[field]) + "\" />")
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
def wp_print_request_filesystem_credentials_modal(*args_):
    
    filesystem_method = get_filesystem_method()
    ob_start()
    filesystem_credentials_are_stored = request_filesystem_credentials(self_admin_url())
    ob_end_clean()
    request_filesystem_credentials = "direct" != filesystem_method and (not filesystem_credentials_are_stored)
    if (not request_filesystem_credentials):
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
