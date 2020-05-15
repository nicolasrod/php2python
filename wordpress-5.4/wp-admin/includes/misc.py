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
#// Misc WordPress Administration API.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// 
#// Returns whether the server is running Apache with the mod_rewrite module loaded.
#// 
#// @since 2.0.0
#// 
#// @return bool Whether the server is running Apache with the mod_rewrite module loaded.
#//
def got_mod_rewrite(*args_):
    
    got_rewrite = apache_mod_loaded("mod_rewrite", True)
    #// 
    #// Filters whether Apache and mod_rewrite are present.
    #// 
    #// This filter was previously used to force URL rewriting for other servers,
    #// like nginx. Use the {@see 'got_url_rewrite'} filter in got_url_rewrite() instead.
    #// 
    #// @since 2.5.0
    #// 
    #// @see got_url_rewrite()
    #// 
    #// @param bool $got_rewrite Whether Apache and mod_rewrite are present.
    #//
    return apply_filters("got_rewrite", got_rewrite)
# end def got_mod_rewrite
#// 
#// Returns whether the server supports URL rewriting.
#// 
#// Detects Apache's mod_rewrite, IIS 7.0+ permalink support, and nginx.
#// 
#// @since 3.7.0
#// 
#// @global bool $is_nginx
#// 
#// @return bool Whether the server supports URL rewriting.
#//
def got_url_rewrite(*args_):
    
    got_url_rewrite = got_mod_rewrite() or PHP_GLOBALS["is_nginx"] or iis7_supports_permalinks()
    #// 
    #// Filters whether URL rewriting is available.
    #// 
    #// @since 3.7.0
    #// 
    #// @param bool $got_url_rewrite Whether URL rewriting is available.
    #//
    return apply_filters("got_url_rewrite", got_url_rewrite)
# end def got_url_rewrite
#// 
#// Extracts strings from between the BEGIN and END markers in the .htaccess file.
#// 
#// @since 1.5.0
#// 
#// @param string $filename Filename to extract the strings from.
#// @param string $marker   The marker to extract the strings from.
#// @return string[] An array of strings from a file (.htaccess) from between BEGIN and END markers.
#//
def extract_from_markers(filename=None, marker=None, *args_):
    
    result = Array()
    if (not php_file_exists(filename)):
        return result
    # end if
    markerdata = php_explode("\n", php_implode("", file(filename)))
    state = False
    for markerline in markerdata:
        if False != php_strpos(markerline, "# END " + marker):
            state = False
        # end if
        if state:
            if "#" == php_substr(markerline, 0, 1):
                continue
            # end if
            result[-1] = markerline
        # end if
        if False != php_strpos(markerline, "# BEGIN " + marker):
            state = True
        # end if
    # end for
    return result
# end def extract_from_markers
#// 
#// Inserts an array of strings into a file (.htaccess), placing it between
#// BEGIN and END markers.
#// 
#// Replaces existing marked info. Retains surrounding
#// data. Creates file if none exists.
#// 
#// @since 1.5.0
#// 
#// @param string       $filename  Filename to alter.
#// @param string       $marker    The marker to alter.
#// @param array|string $insertion The new content to insert.
#// @return bool True on write success, false on failure.
#//
def insert_with_markers(filename=None, marker=None, insertion=None, *args_):
    
    if (not php_file_exists(filename)):
        if (not php_is_writable(php_dirname(filename))):
            return False
        # end if
        if (not touch(filename)):
            return False
        # end if
        #// Make sure the file is created with a minimum set of permissions.
        perms = fileperms(filename)
        if perms:
            chmod(filename, perms | 420)
        # end if
    elif (not is_writeable(filename)):
        return False
    # end if
    if (not php_is_array(insertion)):
        insertion = php_explode("\n", insertion)
    # end if
    switched_locale = switch_to_locale(get_locale())
    instructions = php_sprintf(__("The directives (lines) between `BEGIN %1$s` and `END %1$s` are\ndynamically generated, and should only be modified via WordPress filters.\nAny changes to the directives between these markers will be overwritten."), marker)
    instructions = php_explode("\n", instructions)
    for line,text in instructions:
        instructions[line] = "# " + text
    # end for
    #// 
    #// Filters the inline instructions inserted before the dynamically generated content.
    #// 
    #// @since 5.3.0
    #// 
    #// @param string[] $instructions Array of lines with inline instructions.
    #// @param string   $marker       The marker being inserted.
    #//
    instructions = apply_filters("insert_with_markers_inline_instructions", instructions, marker)
    if switched_locale:
        restore_previous_locale()
    # end if
    insertion = php_array_merge(instructions, insertion)
    start_marker = str("# BEGIN ") + str(marker)
    end_marker = str("# END ") + str(marker)
    fp = fopen(filename, "r+")
    if (not fp):
        return False
    # end if
    #// Attempt to get a lock. If the filesystem supports locking, this will block until the lock is acquired.
    flock(fp, LOCK_EX)
    lines = Array()
    while True:
        
        if not ((not php_feof(fp))):
            break
        # end if
        lines[-1] = php_rtrim(php_fgets(fp), "\r\n")
    # end while
    #// Split out the existing file into the preceding lines, and those that appear after the marker.
    pre_lines = Array()
    post_lines = Array()
    existing_lines = Array()
    found_marker = False
    found_end_marker = False
    for line in lines:
        if (not found_marker) and False != php_strpos(line, start_marker):
            found_marker = True
            continue
        elif (not found_end_marker) and False != php_strpos(line, end_marker):
            found_end_marker = True
            continue
        # end if
        if (not found_marker):
            pre_lines[-1] = line
        elif found_marker and found_end_marker:
            post_lines[-1] = line
        else:
            existing_lines[-1] = line
        # end if
    # end for
    #// Check to see if there was a change.
    if existing_lines == insertion:
        flock(fp, LOCK_UN)
        php_fclose(fp)
        return True
    # end if
    #// Generate the new file data.
    new_file_data = php_implode("\n", php_array_merge(pre_lines, Array(start_marker), insertion, Array(end_marker), post_lines))
    #// Write to the start of the file, and truncate it to that length.
    fseek(fp, 0)
    bytes = fwrite(fp, new_file_data)
    if bytes:
        ftruncate(fp, ftell(fp))
    # end if
    php_fflush(fp)
    flock(fp, LOCK_UN)
    php_fclose(fp)
    return bool(bytes)
# end def insert_with_markers
#// 
#// Updates the htaccess file with the current rules if it is writable.
#// 
#// Always writes to the file if it exists and is writable to ensure that we
#// blank out old rules.
#// 
#// @since 1.5.0
#// 
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// 
#// @return bool|null True on write success, false on failure. Null in multisite.
#//
def save_mod_rewrite_rules(*args_):
    
    if is_multisite():
        return
    # end if
    global wp_rewrite
    php_check_if_defined("wp_rewrite")
    #// Ensure get_home_path() is declared.
    php_include_file(ABSPATH + "wp-admin/includes/file.php", once=True)
    home_path = get_home_path()
    htaccess_file = home_path + ".htaccess"
    #// 
    #// If the file doesn't already exist check for write access to the directory
    #// and whether we have some rules. Else check for write access to the file.
    #//
    if (not php_file_exists(htaccess_file)) and php_is_writable(home_path) and wp_rewrite.using_mod_rewrite_permalinks() or php_is_writable(htaccess_file):
        if got_mod_rewrite():
            rules = php_explode("\n", wp_rewrite.mod_rewrite_rules())
            return insert_with_markers(htaccess_file, "WordPress", rules)
        # end if
    # end if
    return False
# end def save_mod_rewrite_rules
#// 
#// Updates the IIS web.config file with the current rules if it is writable.
#// If the permalinks do not require rewrite rules then the rules are deleted from the web.config file.
#// 
#// @since 2.8.0
#// 
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// 
#// @return bool|null True on write success, false on failure. Null in multisite.
#//
def iis7_save_url_rewrite_rules(*args_):
    
    if is_multisite():
        return
    # end if
    global wp_rewrite
    php_check_if_defined("wp_rewrite")
    #// Ensure get_home_path() is declared.
    php_include_file(ABSPATH + "wp-admin/includes/file.php", once=True)
    home_path = get_home_path()
    web_config_file = home_path + "web.config"
    #// Using win_is_writable() instead of is_writable() because of a bug in Windows PHP.
    if iis7_supports_permalinks() and (not php_file_exists(web_config_file)) and win_is_writable(home_path) and wp_rewrite.using_mod_rewrite_permalinks() or win_is_writable(web_config_file):
        rule = wp_rewrite.iis7_url_rewrite_rules(False)
        if (not php_empty(lambda : rule)):
            return iis7_add_rewrite_rule(web_config_file, rule)
        else:
            return iis7_delete_rewrite_rule(web_config_file)
        # end if
    # end if
    return False
# end def iis7_save_url_rewrite_rules
#// 
#// Update the "recently-edited" file for the plugin or theme editor.
#// 
#// @since 1.5.0
#// 
#// @param string $file
#//
def update_recently_edited(file=None, *args_):
    
    oldfiles = get_option("recently_edited")
    if oldfiles:
        oldfiles = array_reverse(oldfiles)
        oldfiles[-1] = file
        oldfiles = array_reverse(oldfiles)
        oldfiles = array_unique(oldfiles)
        if 5 < php_count(oldfiles):
            php_array_pop(oldfiles)
        # end if
    else:
        oldfiles[-1] = file
    # end if
    update_option("recently_edited", oldfiles)
# end def update_recently_edited
#// 
#// Makes a tree structure for the theme editor's file list.
#// 
#// @since 4.9.0
#// @access private
#// 
#// @param array $allowed_files List of theme file paths.
#// @return array Tree structure for listing theme files.
#//
def wp_make_theme_file_tree(allowed_files=None, *args_):
    
    tree_list = Array()
    for file_name,absolute_filename in allowed_files:
        list = php_explode("/", file_name)
        last_dir = tree_list
        for dir in list:
            last_dir = last_dir[dir]
        # end for
        last_dir = file_name
    # end for
    return tree_list
# end def wp_make_theme_file_tree
#// 
#// Outputs the formatted file list for the theme editor.
#// 
#// @since 4.9.0
#// @access private
#// 
#// @global string $relative_file Name of the file being edited relative to the
#// theme directory.
#// @global string $stylesheet    The stylesheet name of the theme being edited.
#// 
#// @param array|string $tree  List of file/folder paths, or filename.
#// @param int          $level The aria-level for the current iteration.
#// @param int          $size  The aria-setsize for the current iteration.
#// @param int          $index The aria-posinset for the current iteration.
#//
def wp_print_theme_file_tree(tree=None, level=2, size=1, index=1, *args_):
    
    global relative_file,stylesheet
    php_check_if_defined("relative_file","stylesheet")
    if php_is_array(tree):
        index = 0
        size = php_count(tree)
        for label,theme_file in tree:
            index += 1
            if (not php_is_array(theme_file)):
                wp_print_theme_file_tree(theme_file, level, index, size)
                continue
            # end if
            php_print("         <li role=\"treeitem\" aria-expanded=\"true\" tabindex=\"-1\"\n              aria-level=\"")
            php_print(esc_attr(level))
            php_print("\"\n             aria-setsize=\"")
            php_print(esc_attr(size))
            php_print("\"\n             aria-posinset=\"")
            php_print(esc_attr(index))
            php_print("\">\n                <span class=\"folder-label\">")
            php_print(esc_html(label))
            php_print(" <span class=\"screen-reader-text\">")
            _e("folder")
            php_print("</span><span aria-hidden=\"true\" class=\"icon\"></span></span>\n                <ul role=\"group\" class=\"tree-folder\">")
            wp_print_theme_file_tree(theme_file, level + 1, index, size)
            php_print("</ul>\n          </li>\n         ")
        # end for
    else:
        filename = tree
        url = add_query_arg(Array({"file": rawurlencode(tree), "theme": rawurlencode(stylesheet)}), self_admin_url("theme-editor.php"))
        php_print("     <li role=\"none\" class=\"")
        php_print(esc_attr("current-file" if relative_file == filename else ""))
        php_print("\">\n            <a role=\"treeitem\" tabindex=\"")
        php_print(esc_attr("0" if relative_file == filename else "-1"))
        php_print("\"\n             href=\"")
        php_print(esc_url(url))
        php_print("\"\n             aria-level=\"")
        php_print(esc_attr(level))
        php_print("\"\n             aria-setsize=\"")
        php_print(esc_attr(size))
        php_print("\"\n             aria-posinset=\"")
        php_print(esc_attr(index))
        php_print("\">\n                ")
        file_description = esc_html(get_file_description(filename))
        if file_description != filename and wp_basename(filename) != file_description:
            file_description += "<br /><span class=\"nonessential\">(" + esc_html(filename) + ")</span>"
        # end if
        if relative_file == filename:
            php_print("<span class=\"notice notice-info\">" + file_description + "</span>")
        else:
            php_print(file_description)
        # end if
        php_print("         </a>\n      </li>\n     ")
    # end if
# end def wp_print_theme_file_tree
#// 
#// Makes a tree structure for the plugin editor's file list.
#// 
#// @since 4.9.0
#// @access private
#// 
#// @param array $plugin_editable_files List of plugin file paths.
#// @return array Tree structure for listing plugin files.
#//
def wp_make_plugin_file_tree(plugin_editable_files=None, *args_):
    
    tree_list = Array()
    for plugin_file in plugin_editable_files:
        list = php_explode("/", php_preg_replace("#^.+?/#", "", plugin_file))
        last_dir = tree_list
        for dir in list:
            last_dir = last_dir[dir]
        # end for
        last_dir = plugin_file
    # end for
    return tree_list
# end def wp_make_plugin_file_tree
#// 
#// Outputs the formatted file list for the plugin editor.
#// 
#// @since 4.9.0
#// @access private
#// 
#// @param array|string $tree  List of file/folder paths, or filename.
#// @param string       $label Name of file or folder to print.
#// @param int          $level The aria-level for the current iteration.
#// @param int          $size  The aria-setsize for the current iteration.
#// @param int          $index The aria-posinset for the current iteration.
#//
def wp_print_plugin_file_tree(tree=None, label="", level=2, size=1, index=1, *args_):
    
    global file,plugin
    php_check_if_defined("file","plugin")
    if php_is_array(tree):
        index = 0
        size = php_count(tree)
        for label,plugin_file in tree:
            index += 1
            if (not php_is_array(plugin_file)):
                wp_print_plugin_file_tree(plugin_file, label, level, index, size)
                continue
            # end if
            php_print("         <li role=\"treeitem\" aria-expanded=\"true\" tabindex=\"-1\"\n              aria-level=\"")
            php_print(esc_attr(level))
            php_print("\"\n             aria-setsize=\"")
            php_print(esc_attr(size))
            php_print("\"\n             aria-posinset=\"")
            php_print(esc_attr(index))
            php_print("\">\n                <span class=\"folder-label\">")
            php_print(esc_html(label))
            php_print(" <span class=\"screen-reader-text\">")
            _e("folder")
            php_print("</span><span aria-hidden=\"true\" class=\"icon\"></span></span>\n                <ul role=\"group\" class=\"tree-folder\">")
            wp_print_plugin_file_tree(plugin_file, "", level + 1, index, size)
            php_print("</ul>\n          </li>\n         ")
        # end for
    else:
        url = add_query_arg(Array({"file": rawurlencode(tree), "plugin": rawurlencode(plugin)}), self_admin_url("plugin-editor.php"))
        php_print("     <li role=\"none\" class=\"")
        php_print(esc_attr("current-file" if file == tree else ""))
        php_print("\">\n            <a role=\"treeitem\" tabindex=\"")
        php_print(esc_attr("0" if file == tree else "-1"))
        php_print("\"\n             href=\"")
        php_print(esc_url(url))
        php_print("\"\n             aria-level=\"")
        php_print(esc_attr(level))
        php_print("\"\n             aria-setsize=\"")
        php_print(esc_attr(size))
        php_print("\"\n             aria-posinset=\"")
        php_print(esc_attr(index))
        php_print("\">\n                ")
        if file == tree:
            php_print("<span class=\"notice notice-info\">" + esc_html(label) + "</span>")
        else:
            php_print(esc_html(label))
        # end if
        php_print("         </a>\n      </li>\n     ")
    # end if
# end def wp_print_plugin_file_tree
#// 
#// Flushes rewrite rules if siteurl, home or page_on_front changed.
#// 
#// @since 2.1.0
#// 
#// @param string $old_value
#// @param string $value
#//
def update_home_siteurl(old_value=None, value=None, *args_):
    
    if wp_installing():
        return
    # end if
    if is_multisite() and ms_is_switched():
        delete_option("rewrite_rules")
    else:
        flush_rewrite_rules()
    # end if
# end def update_home_siteurl
#// 
#// Resets global variables based on $_GET and $_POST
#// 
#// This function resets global variables based on the names passed
#// in the $vars array to the value of $_POST[$var] or $_GET[$var] or ''
#// if neither is defined.
#// 
#// @since 2.0.0
#// 
#// @param array $vars An array of globals to reset.
#//
def wp_reset_vars(vars=None, *args_):
    global PHP_GLOBALS
    for var in vars:
        if php_empty(lambda : PHP_POST[var]):
            if php_empty(lambda : PHP_REQUEST[var]):
                PHP_GLOBALS[var] = ""
            else:
                PHP_GLOBALS[var] = PHP_REQUEST[var]
            # end if
        else:
            PHP_GLOBALS[var] = PHP_POST[var]
        # end if
    # end for
# end def wp_reset_vars
#// 
#// Displays the given administration message.
#// 
#// @since 2.1.0
#// 
#// @param string|WP_Error $message
#//
def show_message(message=None, *args_):
    
    if is_wp_error(message):
        if message.get_error_data() and php_is_string(message.get_error_data()):
            message = message.get_error_message() + ": " + message.get_error_data()
        else:
            message = message.get_error_message()
        # end if
    # end if
    php_print(str("<p>") + str(message) + str("</p>\n"))
    wp_ob_end_flush_all()
    flush()
# end def show_message
#// 
#// @since 2.8.0
#// 
#// @param string $content
#// @return array
#//
def wp_doc_link_parse(content=None, *args_):
    
    if (not php_is_string(content)) or php_empty(lambda : content):
        return Array()
    # end if
    if (not php_function_exists("token_get_all")):
        return Array()
    # end if
    tokens = token_get_all(content)
    count = php_count(tokens)
    functions = Array()
    ignore_functions = Array()
    t = 0
    while t < count - 2:
        
        if (not php_is_array(tokens[t])):
            continue
        # end if
        if T_STRING == tokens[t][0] and "(" == tokens[t + 1] or "(" == tokens[t + 2]:
            #// If it's a function or class defined locally, there's not going to be any docs available.
            if (php_isset(lambda : tokens[t - 2][1])) and php_in_array(tokens[t - 2][1], Array("function", "class")) or (php_isset(lambda : tokens[t - 2][0])) and T_OBJECT_OPERATOR == tokens[t - 1][0]:
                ignore_functions[-1] = tokens[t][1]
            # end if
            #// Add this to our stack of unique references.
            functions[-1] = tokens[t][1]
        # end if
        t += 1
    # end while
    functions = array_unique(functions)
    sort(functions)
    #// 
    #// Filters the list of functions and classes to be ignored from the documentation lookup.
    #// 
    #// @since 2.8.0
    #// 
    #// @param string[] $ignore_functions Array of names of functions and classes to be ignored.
    #//
    ignore_functions = apply_filters("documentation_ignore_functions", ignore_functions)
    ignore_functions = array_unique(ignore_functions)
    out = Array()
    for function in functions:
        if php_in_array(function, ignore_functions):
            continue
        # end if
        out[-1] = function
    # end for
    return out
# end def wp_doc_link_parse
#// 
#// Saves option for number of rows when listing posts, pages, comments, etc.
#// 
#// @since 2.8.0
#//
def set_screen_options(*args_):
    
    if (php_isset(lambda : PHP_POST["wp_screen_options"])) and php_is_array(PHP_POST["wp_screen_options"]):
        check_admin_referer("screen-options-nonce", "screenoptionnonce")
        user = wp_get_current_user()
        if (not user):
            return
        # end if
        option = PHP_POST["wp_screen_options"]["option"]
        value = PHP_POST["wp_screen_options"]["value"]
        if sanitize_key(option) != option:
            return
        # end if
        map_option = option
        type = php_str_replace("edit_", "", map_option)
        type = php_str_replace("_per_page", "", type)
        if php_in_array(type, get_taxonomies()):
            map_option = "edit_tags_per_page"
        elif php_in_array(type, get_post_types()):
            map_option = "edit_per_page"
        else:
            option = php_str_replace("-", "_", option)
        # end if
        for case in Switch(map_option):
            if case("edit_per_page"):
                pass
            # end if
            if case("users_per_page"):
                pass
            # end if
            if case("edit_comments_per_page"):
                pass
            # end if
            if case("upload_per_page"):
                pass
            # end if
            if case("edit_tags_per_page"):
                pass
            # end if
            if case("plugins_per_page"):
                pass
            # end if
            if case("export_personal_data_requests_per_page"):
                pass
            # end if
            if case("remove_personal_data_requests_per_page"):
                pass
            # end if
            if case("sites_network_per_page"):
                pass
            # end if
            if case("users_network_per_page"):
                pass
            # end if
            if case("site_users_network_per_page"):
                pass
            # end if
            if case("plugins_network_per_page"):
                pass
            # end if
            if case("themes_network_per_page"):
                pass
            # end if
            if case("site_themes_network_per_page"):
                value = int(value)
                if value < 1 or value > 999:
                    return
                # end if
                break
            # end if
            if case():
                #// 
                #// Filters a screen option value before it is set.
                #// 
                #// The filter can also be used to modify non-standard [items]_per_page
                #// settings. See the parent function for a full list of standard options.
                #// 
                #// Returning false to the filter will skip saving the current option.
                #// 
                #// @since 2.8.0
                #// 
                #// @see set_screen_options()
                #// 
                #// @param bool     $keep   Whether to save or skip saving the screen option value. Default false.
                #// @param string   $option The option name.
                #// @param int      $value  The number of rows to use.
                #//
                value = apply_filters("set-screen-option", False, option, value)
                #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
                if False == value:
                    return
                # end if
                break
            # end if
        # end for
        update_user_meta(user.ID, option, value)
        url = remove_query_arg(Array("pagenum", "apage", "paged"), wp_get_referer())
        if (php_isset(lambda : PHP_POST["mode"])):
            url = add_query_arg(Array({"mode": PHP_POST["mode"]}), url)
        # end if
        wp_safe_redirect(url)
        php_exit(0)
    # end if
# end def set_screen_options
#// 
#// Check if rewrite rule for WordPress already exists in the IIS 7+ configuration file
#// 
#// @since 2.8.0
#// 
#// @return bool
#// @param string $filename The file path to the configuration file
#//
def iis7_rewrite_rule_exists(filename=None, *args_):
    
    if (not php_file_exists(filename)):
        return False
    # end if
    if (not php_class_exists("DOMDocument", False)):
        return False
    # end if
    doc = php_new_class("DOMDocument", lambda : DOMDocument())
    if doc.load(filename) == False:
        return False
    # end if
    xpath = php_new_class("DOMXPath", lambda : DOMXPath(doc))
    rules = xpath.query("/configuration/system.webServer/rewrite/rules/rule[starts-with(@name,'wordpress')] | /configuration/system.webServer/rewrite/rules/rule[starts-with(@name,'WordPress')]")
    if 0 == rules.length:
        return False
    else:
        return True
    # end if
# end def iis7_rewrite_rule_exists
#// 
#// Delete WordPress rewrite rule from web.config file if it exists there
#// 
#// @since 2.8.0
#// 
#// @param string $filename Name of the configuration file
#// @return bool
#//
def iis7_delete_rewrite_rule(filename=None, *args_):
    
    #// If configuration file does not exist then rules also do not exist, so there is nothing to delete.
    if (not php_file_exists(filename)):
        return True
    # end if
    if (not php_class_exists("DOMDocument", False)):
        return False
    # end if
    doc = php_new_class("DOMDocument", lambda : DOMDocument())
    doc.preserveWhiteSpace = False
    if doc.load(filename) == False:
        return False
    # end if
    xpath = php_new_class("DOMXPath", lambda : DOMXPath(doc))
    rules = xpath.query("/configuration/system.webServer/rewrite/rules/rule[starts-with(@name,'wordpress')] | /configuration/system.webServer/rewrite/rules/rule[starts-with(@name,'WordPress')]")
    if rules.length > 0:
        child = rules.item(0)
        parent = child.parentNode
        parent.removechild(child)
        doc.formatOutput = True
        saveDomDocument(doc, filename)
    # end if
    return True
# end def iis7_delete_rewrite_rule
#// 
#// Add WordPress rewrite rule to the IIS 7+ configuration file.
#// 
#// @since 2.8.0
#// 
#// @param string $filename The file path to the configuration file
#// @param string $rewrite_rule The XML fragment with URL Rewrite rule
#// @return bool
#//
def iis7_add_rewrite_rule(filename=None, rewrite_rule=None, *args_):
    
    if (not php_class_exists("DOMDocument", False)):
        return False
    # end if
    #// If configuration file does not exist then we create one.
    if (not php_file_exists(filename)):
        fp = fopen(filename, "w")
        fwrite(fp, "<configuration/>")
        php_fclose(fp)
    # end if
    doc = php_new_class("DOMDocument", lambda : DOMDocument())
    doc.preserveWhiteSpace = False
    if doc.load(filename) == False:
        return False
    # end if
    xpath = php_new_class("DOMXPath", lambda : DOMXPath(doc))
    #// First check if the rule already exists as in that case there is no need to re-add it.
    wordpress_rules = xpath.query("/configuration/system.webServer/rewrite/rules/rule[starts-with(@name,'wordpress')] | /configuration/system.webServer/rewrite/rules/rule[starts-with(@name,'WordPress')]")
    if wordpress_rules.length > 0:
        return True
    # end if
    #// Check the XPath to the rewrite rule and create XML nodes if they do not exist.
    xmlnodes = xpath.query("/configuration/system.webServer/rewrite/rules")
    if xmlnodes.length > 0:
        rules_node = xmlnodes.item(0)
    else:
        rules_node = doc.createelement("rules")
        xmlnodes = xpath.query("/configuration/system.webServer/rewrite")
        if xmlnodes.length > 0:
            rewrite_node = xmlnodes.item(0)
            rewrite_node.appendchild(rules_node)
        else:
            rewrite_node = doc.createelement("rewrite")
            rewrite_node.appendchild(rules_node)
            xmlnodes = xpath.query("/configuration/system.webServer")
            if xmlnodes.length > 0:
                system_webServer_node = xmlnodes.item(0)
                system_webServer_node.appendchild(rewrite_node)
            else:
                system_webServer_node = doc.createelement("system.webServer")
                system_webServer_node.appendchild(rewrite_node)
                xmlnodes = xpath.query("/configuration")
                if xmlnodes.length > 0:
                    config_node = xmlnodes.item(0)
                    config_node.appendchild(system_webServer_node)
                else:
                    config_node = doc.createelement("configuration")
                    doc.appendchild(config_node)
                    config_node.appendchild(system_webServer_node)
                # end if
            # end if
        # end if
    # end if
    rule_fragment = doc.createdocumentfragment()
    rule_fragment.appendxml(rewrite_rule)
    rules_node.appendchild(rule_fragment)
    doc.encoding = "UTF-8"
    doc.formatOutput = True
    saveDomDocument(doc, filename)
    return True
# end def iis7_add_rewrite_rule
#// 
#// Saves the XML document into a file
#// 
#// @since 2.8.0
#// 
#// @param DOMDocument $doc
#// @param string $filename
#//
def saveDomDocument(doc=None, filename=None, *args_):
    
    #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.FunctionNameInvalid
    config = doc.savexml()
    config = php_preg_replace("/([^\r])\n/", "$1\r\n", config)
    fp = fopen(filename, "w")
    fwrite(fp, config)
    php_fclose(fp)
# end def saveDomDocument
#// 
#// Display the default admin color scheme picker (Used in user-edit.php)
#// 
#// @since 3.0.0
#// 
#// @global array $_wp_admin_css_colors
#// 
#// @param int $user_id User ID.
#//
def admin_color_scheme_picker(user_id=None, *args_):
    
    global _wp_admin_css_colors
    php_check_if_defined("_wp_admin_css_colors")
    ksort(_wp_admin_css_colors)
    if (php_isset(lambda : _wp_admin_css_colors["fresh"])):
        #// Set Default ('fresh') and Light should go first.
        _wp_admin_css_colors = php_array_filter(php_array_merge(Array({"fresh": "", "light": ""}), _wp_admin_css_colors))
    # end if
    current_color = get_user_option("admin_color", user_id)
    if php_empty(lambda : current_color) or (not (php_isset(lambda : _wp_admin_css_colors[current_color]))):
        current_color = "fresh"
    # end if
    php_print(" <fieldset id=\"color-picker\" class=\"scheme-list\">\n      <legend class=\"screen-reader-text\"><span>")
    _e("Admin Color Scheme")
    php_print("</span></legend>\n       ")
    wp_nonce_field("save-color-scheme", "color-nonce", False)
    for color,color_info in _wp_admin_css_colors:
        php_print("         <div class=\"color-option ")
        php_print("selected" if color == current_color else "")
        php_print("\">\n                <input name=\"admin_color\" id=\"admin_color_")
        php_print(esc_attr(color))
        php_print("\" type=\"radio\" value=\"")
        php_print(esc_attr(color))
        php_print("\" class=\"tog\" ")
        checked(color, current_color)
        php_print(" />\n                <input type=\"hidden\" class=\"css_url\" value=\"")
        php_print(esc_url(color_info.url))
        php_print("\" />\n              <input type=\"hidden\" class=\"icon_colors\" value=\"")
        php_print(esc_attr(wp_json_encode(Array({"icons": color_info.icon_colors}))))
        php_print("\" />\n              <label for=\"admin_color_")
        php_print(esc_attr(color))
        php_print("\">")
        php_print(esc_html(color_info.name))
        php_print("""</label>
        <table class=\"color-palette\">
        <tr>
        """)
        for html_color in color_info.colors:
            php_print("                     <td style=\"background-color: ")
            php_print(esc_attr(html_color))
            php_print("\">&nbsp;</td>\n                     ")
        # end for
        php_print("""                   </tr>
        </table>
        </div>
        """)
    # end for
    php_print(" </fieldset>\n   ")
# end def admin_color_scheme_picker
#// 
#// 
#// @global array $_wp_admin_css_colors
#//
def wp_color_scheme_settings(*args_):
    
    global _wp_admin_css_colors
    php_check_if_defined("_wp_admin_css_colors")
    color_scheme = get_user_option("admin_color")
    #// It's possible to have a color scheme set that is no longer registered.
    if php_empty(lambda : _wp_admin_css_colors[color_scheme]):
        color_scheme = "fresh"
    # end if
    if (not php_empty(lambda : _wp_admin_css_colors[color_scheme].icon_colors)):
        icon_colors = _wp_admin_css_colors[color_scheme].icon_colors
    elif (not php_empty(lambda : _wp_admin_css_colors["fresh"].icon_colors)):
        icon_colors = _wp_admin_css_colors["fresh"].icon_colors
    else:
        #// Fall back to the default set of icon colors if the default scheme is missing.
        icon_colors = Array({"base": "#a0a5aa", "focus": "#00a0d2", "current": "#fff"})
    # end if
    php_print("<script type=\"text/javascript\">var _wpColorScheme = " + wp_json_encode(Array({"icons": icon_colors})) + ";</script>\n")
# end def wp_color_scheme_settings
#// 
#// @since 3.3.0
#//
def _ipad_meta(*args_):
    
    if wp_is_mobile():
        php_print("     <meta name=\"viewport\" id=\"viewport-meta\" content=\"width=device-width, initial-scale=1\">\n     ")
    # end if
# end def _ipad_meta
#// 
#// Check lock status for posts displayed on the Posts screen
#// 
#// @since 3.6.0
#// 
#// @param array  $response  The Heartbeat response.
#// @param array  $data      The $_POST data sent.
#// @param string $screen_id The screen id.
#// @return array The Heartbeat response.
#//
def wp_check_locked_posts(response=None, data=None, screen_id=None, *args_):
    
    checked = Array()
    if php_array_key_exists("wp-check-locked-posts", data) and php_is_array(data["wp-check-locked-posts"]):
        for key in data["wp-check-locked-posts"]:
            post_id = absint(php_substr(key, 5))
            if (not post_id):
                continue
            # end if
            user_id = wp_check_post_lock(post_id)
            if user_id:
                user = get_userdata(user_id)
                if user and current_user_can("edit_post", post_id):
                    send = Array({"text": php_sprintf(__("%s is currently editing"), user.display_name)})
                    avatar = get_avatar(user.ID, 18)
                    if avatar and php_preg_match("|src='([^']+)'|", avatar, matches):
                        send["avatar_src"] = matches[1]
                    # end if
                    checked[key] = send
                # end if
            # end if
        # end for
    # end if
    if (not php_empty(lambda : checked)):
        response["wp-check-locked-posts"] = checked
    # end if
    return response
# end def wp_check_locked_posts
#// 
#// Check lock status on the New/Edit Post screen and refresh the lock
#// 
#// @since 3.6.0
#// 
#// @param array  $response  The Heartbeat response.
#// @param array  $data      The $_POST data sent.
#// @param string $screen_id The screen id.
#// @return array The Heartbeat response.
#//
def wp_refresh_post_lock(response=None, data=None, screen_id=None, *args_):
    
    if php_array_key_exists("wp-refresh-post-lock", data):
        received = data["wp-refresh-post-lock"]
        send = Array()
        post_id = absint(received["post_id"])
        if (not post_id):
            return response
        # end if
        if (not current_user_can("edit_post", post_id)):
            return response
        # end if
        user_id = wp_check_post_lock(post_id)
        user = get_userdata(user_id)
        if user:
            error = Array({"text": php_sprintf(__("%s has taken over and is currently editing."), user.display_name)})
            avatar = get_avatar(user.ID, 64)
            if avatar:
                if php_preg_match("|src='([^']+)'|", avatar, matches):
                    error["avatar_src"] = matches[1]
                # end if
            # end if
            send["lock_error"] = error
        else:
            new_lock = wp_set_post_lock(post_id)
            if new_lock:
                send["new_lock"] = php_implode(":", new_lock)
            # end if
        # end if
        response["wp-refresh-post-lock"] = send
    # end if
    return response
# end def wp_refresh_post_lock
#// 
#// Check nonce expiration on the New/Edit Post screen and refresh if needed
#// 
#// @since 3.6.0
#// 
#// @param array  $response  The Heartbeat response.
#// @param array  $data      The $_POST data sent.
#// @param string $screen_id The screen id.
#// @return array The Heartbeat response.
#//
def wp_refresh_post_nonces(response=None, data=None, screen_id=None, *args_):
    
    if php_array_key_exists("wp-refresh-post-nonces", data):
        received = data["wp-refresh-post-nonces"]
        response["wp-refresh-post-nonces"] = Array({"check": 1})
        post_id = absint(received["post_id"])
        if (not post_id):
            return response
        # end if
        if (not current_user_can("edit_post", post_id)):
            return response
        # end if
        response["wp-refresh-post-nonces"] = Array({"replace": Array({"getpermalinknonce": wp_create_nonce("getpermalink"), "samplepermalinknonce": wp_create_nonce("samplepermalink"), "closedpostboxesnonce": wp_create_nonce("closedpostboxes"), "_ajax_linking_nonce": wp_create_nonce("internal-linking"), "_wpnonce": wp_create_nonce("update-post_" + post_id)})})
    # end if
    return response
# end def wp_refresh_post_nonces
#// 
#// Add the latest Heartbeat and REST-API nonce to the Heartbeat response.
#// 
#// @since 5.0.0
#// 
#// @param array  $response  The Heartbeat response.
#// @return array The Heartbeat response.
#//
def wp_refresh_heartbeat_nonces(response=None, *args_):
    
    #// Refresh the Rest API nonce.
    response["rest_nonce"] = wp_create_nonce("wp_rest")
    #// Refresh the Heartbeat nonce.
    response["heartbeat_nonce"] = wp_create_nonce("heartbeat-nonce")
    return response
# end def wp_refresh_heartbeat_nonces
#// 
#// Disable suspension of Heartbeat on the Add/Edit Post screens.
#// 
#// @since 3.8.0
#// 
#// @global string $pagenow
#// 
#// @param array $settings An array of Heartbeat settings.
#// @return array Filtered Heartbeat settings.
#//
def wp_heartbeat_set_suspension(settings=None, *args_):
    
    global pagenow
    php_check_if_defined("pagenow")
    if "post.php" == pagenow or "post-new.php" == pagenow:
        settings["suspension"] = "disable"
    # end if
    return settings
# end def wp_heartbeat_set_suspension
#// 
#// Autosave with heartbeat
#// 
#// @since 3.9.0
#// 
#// @param array $response The Heartbeat response.
#// @param array $data     The $_POST data sent.
#// @return array The Heartbeat response.
#//
def heartbeat_autosave(response=None, data=None, *args_):
    
    if (not php_empty(lambda : data["wp_autosave"])):
        saved = wp_autosave(data["wp_autosave"])
        if is_wp_error(saved):
            response["wp_autosave"] = Array({"success": False, "message": saved.get_error_message()})
        elif php_empty(lambda : saved):
            response["wp_autosave"] = Array({"success": False, "message": __("Error while saving.")})
        else:
            #// translators: Draft saved date format, see https://www.php.net/date
            draft_saved_date_format = __("g:i:s a")
            response["wp_autosave"] = Array({"success": True, "message": php_sprintf(__("Draft saved at %s."), date_i18n(draft_saved_date_format))})
        # end if
    # end if
    return response
# end def heartbeat_autosave
#// 
#// Remove single-use URL parameters and create canonical link based on new URL.
#// 
#// Remove specific query string parameters from a URL, create the canonical link,
#// put it in the admin header, and change the current URL to match.
#// 
#// @since 4.2.0
#//
def wp_admin_canonical_url(*args_):
    
    removable_query_args = wp_removable_query_args()
    if php_empty(lambda : removable_query_args):
        return
    # end if
    #// Ensure we're using an absolute URL.
    current_url = set_url_scheme("http://" + PHP_SERVER["HTTP_HOST"] + PHP_SERVER["REQUEST_URI"])
    filtered_url = remove_query_arg(removable_query_args, current_url)
    php_print(" <link id=\"wp-admin-canonical\" rel=\"canonical\" href=\"")
    php_print(esc_url(filtered_url))
    php_print("""\" />
    <script>
if ( window.history.replaceState ) {
    window.history.replaceState( null, null, document.getElementById( 'wp-admin-canonical' ).href + window.location.hash );
    }
    </script>
    """)
# end def wp_admin_canonical_url
#// 
#// Send a referrer policy header so referrers are not sent externally from administration screens.
#// 
#// @since 4.9.0
#//
def wp_admin_headers(*args_):
    
    policy = "strict-origin-when-cross-origin"
    #// 
    #// Filters the admin referrer policy header value.
    #// 
    #// @since 4.9.0
    #// @since 4.9.5 The default value was changed to 'strict-origin-when-cross-origin'.
    #// 
    #// @link https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy
    #// 
    #// @param string $policy The admin referrer policy header value. Default 'strict-origin-when-cross-origin'.
    #//
    policy = apply_filters("admin_referrer_policy", policy)
    php_header(php_sprintf("Referrer-Policy: %s", policy))
# end def wp_admin_headers
#// 
#// Outputs JS that reloads the page if the user navigated to it with the Back or Forward button.
#// 
#// Used on the Edit Post and Add New Post screens. Needed to ensure the page is not loaded from browser cache,
#// so the post title and editor content are the last saved versions. Ideally this script should run first in the head.
#// 
#// @since 4.6.0
#//
def wp_page_reload_on_back_button_js(*args_):
    
    php_print("""   <script>
if ( typeof performance !== 'undefined' && performance.navigation && performance.navigation.type === 2 ) {
    document.location.reload( true );
    }
    </script>
    """)
# end def wp_page_reload_on_back_button_js
#// 
#// Send a confirmation request email when a change of site admin email address is attempted.
#// 
#// The new site admin address will not become active until confirmed.
#// 
#// @since 3.0.0
#// @since 4.9.0 This function was moved from wp-admin/includes/ms.php so it's no longer Multisite specific.
#// 
#// @param string $old_value The old site admin email address.
#// @param string $value     The proposed new site admin email address.
#//
def update_option_new_admin_email(old_value=None, value=None, *args_):
    
    if get_option("admin_email") == value or (not is_email(value)):
        return
    # end if
    hash = php_md5(value + time() + wp_rand())
    new_admin_email = Array({"hash": hash, "newemail": value})
    update_option("adminhash", new_admin_email)
    switched_locale = switch_to_locale(get_user_locale())
    #// translators: Do not translate USERNAME, ADMIN_URL, EMAIL, SITENAME, SITEURL: those are placeholders.
    email_text = __("""Howdy ###USERNAME###,
    You recently requested to have the administration email address on
    your site changed.
    If this is correct, please click on the following link to change it:
    ###ADMIN_URL###
    You can safely ignore and delete this email if you do not want to
    take this action.
    This email has been sent to ###EMAIL###
    Regards,
    All at ###SITENAME###
    ###SITEURL###""")
    #// 
    #// Filters the text of the email sent when a change of site admin email address is attempted.
    #// 
    #// The following strings have a special meaning and will get replaced dynamically:
    #// ###USERNAME###  The current user's username.
    #// ###ADMIN_URL### The link to click on to confirm the email change.
    #// ###EMAIL###     The proposed new site admin email address.
    #// ###SITENAME###  The name of the site.
    #// ###SITEURL###   The URL to the site.
    #// 
    #// @since MU (3.0.0)
    #// @since 4.9.0 This filter is no longer Multisite specific.
    #// 
    #// @param string $email_text      Text in the email.
    #// @param array  $new_admin_email {
    #// Data relating to the new site admin email address.
    #// 
    #// @type string $hash     The secure hash used in the confirmation link URL.
    #// @type string $newemail The proposed new site admin email address.
    #// }
    #//
    content = apply_filters("new_admin_email_content", email_text, new_admin_email)
    current_user = wp_get_current_user()
    content = php_str_replace("###USERNAME###", current_user.user_login, content)
    content = php_str_replace("###ADMIN_URL###", esc_url(self_admin_url("options.php?adminhash=" + hash)), content)
    content = php_str_replace("###EMAIL###", value, content)
    content = php_str_replace("###SITENAME###", wp_specialchars_decode(get_option("blogname"), ENT_QUOTES), content)
    content = php_str_replace("###SITEURL###", home_url(), content)
    wp_mail(value, php_sprintf(__("[%s] New Admin Email Address"), wp_specialchars_decode(get_option("blogname"), ENT_QUOTES)), content)
    if switched_locale:
        restore_previous_locale()
    # end if
# end def update_option_new_admin_email
#// 
#// Appends '(Draft)' to draft page titles in the privacy page dropdown
#// so that unpublished content is obvious.
#// 
#// @since 4.9.8
#// @access private
#// 
#// @param string  $title Page title.
#// @param WP_Post $page  Page data object.
#// 
#// @return string Page title.
#//
def _wp_privacy_settings_filter_draft_page_titles(title=None, page=None, *args_):
    
    if "draft" == page.post_status and "privacy" == get_current_screen().id:
        #// translators: %s: Page title.
        title = php_sprintf(__("%s (Draft)"), title)
    # end if
    return title
# end def _wp_privacy_settings_filter_draft_page_titles
#// 
#// Checks if the user needs to update PHP.
#// 
#// @since 5.1.0
#// @since 5.1.1 Added the {@see 'wp_is_php_version_acceptable'} filter.
#// 
#// @return array|false $response Array of PHP version data. False on failure.
#//
def wp_check_php_version(*args_):
    
    version = php_phpversion()
    key = php_md5(version)
    response = get_site_transient("php_check_" + key)
    if False == response:
        url = "http://api.wordpress.org/core/serve-happy/1.0/"
        if wp_http_supports(Array("ssl")):
            url = set_url_scheme(url, "https")
        # end if
        url = add_query_arg("php_version", version, url)
        response = wp_remote_get(url)
        if is_wp_error(response) or 200 != wp_remote_retrieve_response_code(response):
            return False
        # end if
        #// 
        #// Response should be an array with:
        #// 'recommended_version' - string - The PHP version recommended by WordPress.
        #// 'is_supported' - boolean - Whether the PHP version is actively supported.
        #// 'is_secure' - boolean - Whether the PHP version receives security updates.
        #// 'is_acceptable' - boolean - Whether the PHP version is still acceptable for WordPress.
        #//
        response = php_json_decode(wp_remote_retrieve_body(response), True)
        if (not php_is_array(response)):
            return False
        # end if
        set_site_transient("php_check_" + key, response, WEEK_IN_SECONDS)
    # end if
    if (php_isset(lambda : response["is_acceptable"])) and response["is_acceptable"]:
        #// 
        #// Filters whether the active PHP version is considered acceptable by WordPress.
        #// 
        #// Returning false will trigger a PHP version warning to show up in the admin dashboard to administrators.
        #// 
        #// This filter is only run if the wordpress.org Serve Happy API considers the PHP version acceptable, ensuring
        #// that this filter can only make this check stricter, but not loosen it.
        #// 
        #// @since 5.1.1
        #// 
        #// @param bool   $is_acceptable Whether the PHP version is considered acceptable. Default true.
        #// @param string $version       PHP version checked.
        #//
        response["is_acceptable"] = bool(apply_filters("wp_is_php_version_acceptable", True, version))
    # end if
    return response
# end def wp_check_php_version
