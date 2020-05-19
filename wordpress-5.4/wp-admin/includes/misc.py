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
def got_mod_rewrite(*_args_):
    
    
    got_rewrite_ = apache_mod_loaded("mod_rewrite", True)
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
    return apply_filters("got_rewrite", got_rewrite_)
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
def got_url_rewrite(*_args_):
    
    
    got_url_rewrite_ = got_mod_rewrite() or PHP_GLOBALS["is_nginx"] or iis7_supports_permalinks()
    #// 
    #// Filters whether URL rewriting is available.
    #// 
    #// @since 3.7.0
    #// 
    #// @param bool $got_url_rewrite Whether URL rewriting is available.
    #//
    return apply_filters("got_url_rewrite", got_url_rewrite_)
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
def extract_from_markers(filename_=None, marker_=None, *_args_):
    
    
    result_ = Array()
    if (not php_file_exists(filename_)):
        return result_
    # end if
    markerdata_ = php_explode("\n", php_implode("", file(filename_)))
    state_ = False
    for markerline_ in markerdata_:
        if False != php_strpos(markerline_, "# END " + marker_):
            state_ = False
        # end if
        if state_:
            if "#" == php_substr(markerline_, 0, 1):
                continue
            # end if
            result_[-1] = markerline_
        # end if
        if False != php_strpos(markerline_, "# BEGIN " + marker_):
            state_ = True
        # end if
    # end for
    return result_
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
def insert_with_markers(filename_=None, marker_=None, insertion_=None, *_args_):
    
    
    if (not php_file_exists(filename_)):
        if (not php_is_writable(php_dirname(filename_))):
            return False
        # end if
        if (not touch(filename_)):
            return False
        # end if
        #// Make sure the file is created with a minimum set of permissions.
        perms_ = fileperms(filename_)
        if perms_:
            chmod(filename_, perms_ | 420)
        # end if
    elif (not is_writeable(filename_)):
        return False
    # end if
    if (not php_is_array(insertion_)):
        insertion_ = php_explode("\n", insertion_)
    # end if
    switched_locale_ = switch_to_locale(get_locale())
    instructions_ = php_sprintf(__("The directives (lines) between `BEGIN %1$s` and `END %1$s` are\ndynamically generated, and should only be modified via WordPress filters.\nAny changes to the directives between these markers will be overwritten."), marker_)
    instructions_ = php_explode("\n", instructions_)
    for line_,text_ in instructions_.items():
        instructions_[line_] = "# " + text_
    # end for
    #// 
    #// Filters the inline instructions inserted before the dynamically generated content.
    #// 
    #// @since 5.3.0
    #// 
    #// @param string[] $instructions Array of lines with inline instructions.
    #// @param string   $marker       The marker being inserted.
    #//
    instructions_ = apply_filters("insert_with_markers_inline_instructions", instructions_, marker_)
    if switched_locale_:
        restore_previous_locale()
    # end if
    insertion_ = php_array_merge(instructions_, insertion_)
    start_marker_ = str("# BEGIN ") + str(marker_)
    end_marker_ = str("# END ") + str(marker_)
    fp_ = fopen(filename_, "r+")
    if (not fp_):
        return False
    # end if
    #// Attempt to get a lock. If the filesystem supports locking, this will block until the lock is acquired.
    flock(fp_, LOCK_EX)
    lines_ = Array()
    while True:
        
        if not ((not php_feof(fp_))):
            break
        # end if
        lines_[-1] = php_rtrim(php_fgets(fp_), "\r\n")
    # end while
    #// Split out the existing file into the preceding lines, and those that appear after the marker.
    pre_lines_ = Array()
    post_lines_ = Array()
    existing_lines_ = Array()
    found_marker_ = False
    found_end_marker_ = False
    for line_ in lines_:
        if (not found_marker_) and False != php_strpos(line_, start_marker_):
            found_marker_ = True
            continue
        elif (not found_end_marker_) and False != php_strpos(line_, end_marker_):
            found_end_marker_ = True
            continue
        # end if
        if (not found_marker_):
            pre_lines_[-1] = line_
        elif found_marker_ and found_end_marker_:
            post_lines_[-1] = line_
        else:
            existing_lines_[-1] = line_
        # end if
    # end for
    #// Check to see if there was a change.
    if existing_lines_ == insertion_:
        flock(fp_, LOCK_UN)
        php_fclose(fp_)
        return True
    # end if
    #// Generate the new file data.
    new_file_data_ = php_implode("\n", php_array_merge(pre_lines_, Array(start_marker_), insertion_, Array(end_marker_), post_lines_))
    #// Write to the start of the file, and truncate it to that length.
    fseek(fp_, 0)
    bytes_ = fwrite(fp_, new_file_data_)
    if bytes_:
        ftruncate(fp_, ftell(fp_))
    # end if
    php_fflush(fp_)
    flock(fp_, LOCK_UN)
    php_fclose(fp_)
    return php_bool(bytes_)
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
def save_mod_rewrite_rules(*_args_):
    
    
    if is_multisite():
        return
    # end if
    global wp_rewrite_
    php_check_if_defined("wp_rewrite_")
    #// Ensure get_home_path() is declared.
    php_include_file(ABSPATH + "wp-admin/includes/file.php", once=True)
    home_path_ = get_home_path()
    htaccess_file_ = home_path_ + ".htaccess"
    #// 
    #// If the file doesn't already exist check for write access to the directory
    #// and whether we have some rules. Else check for write access to the file.
    #//
    if (not php_file_exists(htaccess_file_)) and php_is_writable(home_path_) and wp_rewrite_.using_mod_rewrite_permalinks() or php_is_writable(htaccess_file_):
        if got_mod_rewrite():
            rules_ = php_explode("\n", wp_rewrite_.mod_rewrite_rules())
            return insert_with_markers(htaccess_file_, "WordPress", rules_)
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
def iis7_save_url_rewrite_rules(*_args_):
    
    
    if is_multisite():
        return
    # end if
    global wp_rewrite_
    php_check_if_defined("wp_rewrite_")
    #// Ensure get_home_path() is declared.
    php_include_file(ABSPATH + "wp-admin/includes/file.php", once=True)
    home_path_ = get_home_path()
    web_config_file_ = home_path_ + "web.config"
    #// Using win_is_writable() instead of is_writable() because of a bug in Windows PHP.
    if iis7_supports_permalinks() and (not php_file_exists(web_config_file_)) and win_is_writable(home_path_) and wp_rewrite_.using_mod_rewrite_permalinks() or win_is_writable(web_config_file_):
        rule_ = wp_rewrite_.iis7_url_rewrite_rules(False)
        if (not php_empty(lambda : rule_)):
            return iis7_add_rewrite_rule(web_config_file_, rule_)
        else:
            return iis7_delete_rewrite_rule(web_config_file_)
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
def update_recently_edited(file_=None, *_args_):
    
    
    oldfiles_ = get_option("recently_edited")
    if oldfiles_:
        oldfiles_ = php_array_reverse(oldfiles_)
        oldfiles_[-1] = file_
        oldfiles_ = php_array_reverse(oldfiles_)
        oldfiles_ = array_unique(oldfiles_)
        if 5 < php_count(oldfiles_):
            php_array_pop(oldfiles_)
        # end if
    else:
        oldfiles_[-1] = file_
    # end if
    update_option("recently_edited", oldfiles_)
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
def wp_make_theme_file_tree(allowed_files_=None, *_args_):
    
    
    tree_list_ = Array()
    for file_name_,absolute_filename_ in allowed_files_.items():
        list_ = php_explode("/", file_name_)
        last_dir_ = tree_list_
        for dir_ in list_:
            last_dir_ = last_dir_[dir_]
        # end for
        last_dir_ = file_name_
    # end for
    return tree_list_
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
def wp_print_theme_file_tree(tree_=None, level_=2, size_=1, index_=1, *_args_):
    
    
    global relative_file_
    global stylesheet_
    php_check_if_defined("relative_file_","stylesheet_")
    if php_is_array(tree_):
        index_ = 0
        size_ = php_count(tree_)
        for label_,theme_file_ in tree_.items():
            index_ += 1
            if (not php_is_array(theme_file_)):
                wp_print_theme_file_tree(theme_file_, level_, index_, size_)
                continue
            # end if
            php_print("         <li role=\"treeitem\" aria-expanded=\"true\" tabindex=\"-1\"\n              aria-level=\"")
            php_print(esc_attr(level_))
            php_print("\"\n             aria-setsize=\"")
            php_print(esc_attr(size_))
            php_print("\"\n             aria-posinset=\"")
            php_print(esc_attr(index_))
            php_print("\">\n                <span class=\"folder-label\">")
            php_print(esc_html(label_))
            php_print(" <span class=\"screen-reader-text\">")
            _e("folder")
            php_print("</span><span aria-hidden=\"true\" class=\"icon\"></span></span>\n                <ul role=\"group\" class=\"tree-folder\">")
            wp_print_theme_file_tree(theme_file_, level_ + 1, index_, size_)
            php_print("</ul>\n          </li>\n         ")
        # end for
    else:
        filename_ = tree_
        url_ = add_query_arg(Array({"file": rawurlencode(tree_), "theme": rawurlencode(stylesheet_)}), self_admin_url("theme-editor.php"))
        php_print("     <li role=\"none\" class=\"")
        php_print(esc_attr("current-file" if relative_file_ == filename_ else ""))
        php_print("\">\n            <a role=\"treeitem\" tabindex=\"")
        php_print(esc_attr("0" if relative_file_ == filename_ else "-1"))
        php_print("\"\n             href=\"")
        php_print(esc_url(url_))
        php_print("\"\n             aria-level=\"")
        php_print(esc_attr(level_))
        php_print("\"\n             aria-setsize=\"")
        php_print(esc_attr(size_))
        php_print("\"\n             aria-posinset=\"")
        php_print(esc_attr(index_))
        php_print("\">\n                ")
        file_description_ = esc_html(get_file_description(filename_))
        if file_description_ != filename_ and wp_basename(filename_) != file_description_:
            file_description_ += "<br /><span class=\"nonessential\">(" + esc_html(filename_) + ")</span>"
        # end if
        if relative_file_ == filename_:
            php_print("<span class=\"notice notice-info\">" + file_description_ + "</span>")
        else:
            php_print(file_description_)
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
def wp_make_plugin_file_tree(plugin_editable_files_=None, *_args_):
    
    
    tree_list_ = Array()
    for plugin_file_ in plugin_editable_files_:
        list_ = php_explode("/", php_preg_replace("#^.+?/#", "", plugin_file_))
        last_dir_ = tree_list_
        for dir_ in list_:
            last_dir_ = last_dir_[dir_]
        # end for
        last_dir_ = plugin_file_
    # end for
    return tree_list_
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
def wp_print_plugin_file_tree(tree_=None, label_="", level_=2, size_=1, index_=1, *_args_):
    
    
    global file_
    global plugin_
    php_check_if_defined("file_","plugin_")
    if php_is_array(tree_):
        index_ = 0
        size_ = php_count(tree_)
        for label_,plugin_file_ in tree_.items():
            index_ += 1
            if (not php_is_array(plugin_file_)):
                wp_print_plugin_file_tree(plugin_file_, label_, level_, index_, size_)
                continue
            # end if
            php_print("         <li role=\"treeitem\" aria-expanded=\"true\" tabindex=\"-1\"\n              aria-level=\"")
            php_print(esc_attr(level_))
            php_print("\"\n             aria-setsize=\"")
            php_print(esc_attr(size_))
            php_print("\"\n             aria-posinset=\"")
            php_print(esc_attr(index_))
            php_print("\">\n                <span class=\"folder-label\">")
            php_print(esc_html(label_))
            php_print(" <span class=\"screen-reader-text\">")
            _e("folder")
            php_print("</span><span aria-hidden=\"true\" class=\"icon\"></span></span>\n                <ul role=\"group\" class=\"tree-folder\">")
            wp_print_plugin_file_tree(plugin_file_, "", level_ + 1, index_, size_)
            php_print("</ul>\n          </li>\n         ")
        # end for
    else:
        url_ = add_query_arg(Array({"file": rawurlencode(tree_), "plugin": rawurlencode(plugin_)}), self_admin_url("plugin-editor.php"))
        php_print("     <li role=\"none\" class=\"")
        php_print(esc_attr("current-file" if file_ == tree_ else ""))
        php_print("\">\n            <a role=\"treeitem\" tabindex=\"")
        php_print(esc_attr("0" if file_ == tree_ else "-1"))
        php_print("\"\n             href=\"")
        php_print(esc_url(url_))
        php_print("\"\n             aria-level=\"")
        php_print(esc_attr(level_))
        php_print("\"\n             aria-setsize=\"")
        php_print(esc_attr(size_))
        php_print("\"\n             aria-posinset=\"")
        php_print(esc_attr(index_))
        php_print("\">\n                ")
        if file_ == tree_:
            php_print("<span class=\"notice notice-info\">" + esc_html(label_) + "</span>")
        else:
            php_print(esc_html(label_))
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
def update_home_siteurl(old_value_=None, value_=None, *_args_):
    
    
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
def wp_reset_vars(vars_=None, *_args_):
    
    global PHP_GLOBALS
    for var_ in vars_:
        if php_empty(lambda : PHP_POST[var_]):
            if php_empty(lambda : PHP_REQUEST[var_]):
                PHP_GLOBALS[var_] = ""
            else:
                PHP_GLOBALS[var_] = PHP_REQUEST[var_]
            # end if
        else:
            PHP_GLOBALS[var_] = PHP_POST[var_]
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
def show_message(message_=None, *_args_):
    
    
    if is_wp_error(message_):
        if message_.get_error_data() and php_is_string(message_.get_error_data()):
            message_ = message_.get_error_message() + ": " + message_.get_error_data()
        else:
            message_ = message_.get_error_message()
        # end if
    # end if
    php_print(str("<p>") + str(message_) + str("</p>\n"))
    wp_ob_end_flush_all()
    flush()
# end def show_message
#// 
#// @since 2.8.0
#// 
#// @param string $content
#// @return array
#//
def wp_doc_link_parse(content_=None, *_args_):
    
    
    if (not php_is_string(content_)) or php_empty(lambda : content_):
        return Array()
    # end if
    if (not php_function_exists("token_get_all")):
        return Array()
    # end if
    tokens_ = token_get_all(content_)
    count_ = php_count(tokens_)
    functions_ = Array()
    ignore_functions_ = Array()
    t_ = 0
    while t_ < count_ - 2:
        
        if (not php_is_array(tokens_[t_])):
            continue
        # end if
        if T_STRING == tokens_[t_][0] and "(" == tokens_[t_ + 1] or "(" == tokens_[t_ + 2]:
            #// If it's a function or class defined locally, there's not going to be any docs available.
            if (php_isset(lambda : tokens_[t_ - 2][1])) and php_in_array(tokens_[t_ - 2][1], Array("function", "class")) or (php_isset(lambda : tokens_[t_ - 2][0])) and T_OBJECT_OPERATOR == tokens_[t_ - 1][0]:
                ignore_functions_[-1] = tokens_[t_][1]
            # end if
            #// Add this to our stack of unique references.
            functions_[-1] = tokens_[t_][1]
        # end if
        t_ += 1
    # end while
    functions_ = array_unique(functions_)
    sort(functions_)
    #// 
    #// Filters the list of functions and classes to be ignored from the documentation lookup.
    #// 
    #// @since 2.8.0
    #// 
    #// @param string[] $ignore_functions Array of names of functions and classes to be ignored.
    #//
    ignore_functions_ = apply_filters("documentation_ignore_functions", ignore_functions_)
    ignore_functions_ = array_unique(ignore_functions_)
    out_ = Array()
    for function_ in functions_:
        if php_in_array(function_, ignore_functions_):
            continue
        # end if
        out_[-1] = function_
    # end for
    return out_
# end def wp_doc_link_parse
#// 
#// Saves option for number of rows when listing posts, pages, comments, etc.
#// 
#// @since 2.8.0
#//
def set_screen_options(*_args_):
    
    
    if (php_isset(lambda : PHP_POST["wp_screen_options"])) and php_is_array(PHP_POST["wp_screen_options"]):
        check_admin_referer("screen-options-nonce", "screenoptionnonce")
        user_ = wp_get_current_user()
        if (not user_):
            return
        # end if
        option_ = PHP_POST["wp_screen_options"]["option"]
        value_ = PHP_POST["wp_screen_options"]["value"]
        if sanitize_key(option_) != option_:
            return
        # end if
        map_option_ = option_
        type_ = php_str_replace("edit_", "", map_option_)
        type_ = php_str_replace("_per_page", "", type_)
        if php_in_array(type_, get_taxonomies()):
            map_option_ = "edit_tags_per_page"
        elif php_in_array(type_, get_post_types()):
            map_option_ = "edit_per_page"
        else:
            option_ = php_str_replace("-", "_", option_)
        # end if
        for case in Switch(map_option_):
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
                value_ = php_int(value_)
                if value_ < 1 or value_ > 999:
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
                value_ = apply_filters("set-screen-option", False, option_, value_)
                #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
                if False == value_:
                    return
                # end if
                break
            # end if
        # end for
        update_user_meta(user_.ID, option_, value_)
        url_ = remove_query_arg(Array("pagenum", "apage", "paged"), wp_get_referer())
        if (php_isset(lambda : PHP_POST["mode"])):
            url_ = add_query_arg(Array({"mode": PHP_POST["mode"]}), url_)
        # end if
        wp_safe_redirect(url_)
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
def iis7_rewrite_rule_exists(filename_=None, *_args_):
    
    
    if (not php_file_exists(filename_)):
        return False
    # end if
    if (not php_class_exists("DOMDocument", False)):
        return False
    # end if
    doc_ = php_new_class("DOMDocument", lambda : DOMDocument())
    if doc_.load(filename_) == False:
        return False
    # end if
    xpath_ = php_new_class("DOMXPath", lambda : DOMXPath(doc_))
    rules_ = xpath_.query("/configuration/system.webServer/rewrite/rules/rule[starts-with(@name,'wordpress')] | /configuration/system.webServer/rewrite/rules/rule[starts-with(@name,'WordPress')]")
    if 0 == rules_.length:
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
def iis7_delete_rewrite_rule(filename_=None, *_args_):
    
    
    #// If configuration file does not exist then rules also do not exist, so there is nothing to delete.
    if (not php_file_exists(filename_)):
        return True
    # end if
    if (not php_class_exists("DOMDocument", False)):
        return False
    # end if
    doc_ = php_new_class("DOMDocument", lambda : DOMDocument())
    doc_.preserveWhiteSpace = False
    if doc_.load(filename_) == False:
        return False
    # end if
    xpath_ = php_new_class("DOMXPath", lambda : DOMXPath(doc_))
    rules_ = xpath_.query("/configuration/system.webServer/rewrite/rules/rule[starts-with(@name,'wordpress')] | /configuration/system.webServer/rewrite/rules/rule[starts-with(@name,'WordPress')]")
    if rules_.length > 0:
        child_ = rules_.item(0)
        parent_ = child_.parentNode
        parent_.removechild(child_)
        doc_.formatOutput = True
        saveDomDocument(doc_, filename_)
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
def iis7_add_rewrite_rule(filename_=None, rewrite_rule_=None, *_args_):
    
    
    if (not php_class_exists("DOMDocument", False)):
        return False
    # end if
    #// If configuration file does not exist then we create one.
    if (not php_file_exists(filename_)):
        fp_ = fopen(filename_, "w")
        fwrite(fp_, "<configuration/>")
        php_fclose(fp_)
    # end if
    doc_ = php_new_class("DOMDocument", lambda : DOMDocument())
    doc_.preserveWhiteSpace = False
    if doc_.load(filename_) == False:
        return False
    # end if
    xpath_ = php_new_class("DOMXPath", lambda : DOMXPath(doc_))
    #// First check if the rule already exists as in that case there is no need to re-add it.
    wordpress_rules_ = xpath_.query("/configuration/system.webServer/rewrite/rules/rule[starts-with(@name,'wordpress')] | /configuration/system.webServer/rewrite/rules/rule[starts-with(@name,'WordPress')]")
    if wordpress_rules_.length > 0:
        return True
    # end if
    #// Check the XPath to the rewrite rule and create XML nodes if they do not exist.
    xmlnodes_ = xpath_.query("/configuration/system.webServer/rewrite/rules")
    if xmlnodes_.length > 0:
        rules_node_ = xmlnodes_.item(0)
    else:
        rules_node_ = doc_.createelement("rules")
        xmlnodes_ = xpath_.query("/configuration/system.webServer/rewrite")
        if xmlnodes_.length > 0:
            rewrite_node_ = xmlnodes_.item(0)
            rewrite_node_.appendchild(rules_node_)
        else:
            rewrite_node_ = doc_.createelement("rewrite")
            rewrite_node_.appendchild(rules_node_)
            xmlnodes_ = xpath_.query("/configuration/system.webServer")
            if xmlnodes_.length > 0:
                system_webServer_node_ = xmlnodes_.item(0)
                system_webServer_node_.appendchild(rewrite_node_)
            else:
                system_webServer_node_ = doc_.createelement("system.webServer")
                system_webServer_node_.appendchild(rewrite_node_)
                xmlnodes_ = xpath_.query("/configuration")
                if xmlnodes_.length > 0:
                    config_node_ = xmlnodes_.item(0)
                    config_node_.appendchild(system_webServer_node_)
                else:
                    config_node_ = doc_.createelement("configuration")
                    doc_.appendchild(config_node_)
                    config_node_.appendchild(system_webServer_node_)
                # end if
            # end if
        # end if
    # end if
    rule_fragment_ = doc_.createdocumentfragment()
    rule_fragment_.appendxml(rewrite_rule_)
    rules_node_.appendchild(rule_fragment_)
    doc_.encoding = "UTF-8"
    doc_.formatOutput = True
    saveDomDocument(doc_, filename_)
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
def saveDomDocument(doc_=None, filename_=None, *_args_):
    
    
    #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.FunctionNameInvalid
    config_ = doc_.savexml()
    config_ = php_preg_replace("/([^\r])\n/", "$1\r\n", config_)
    fp_ = fopen(filename_, "w")
    fwrite(fp_, config_)
    php_fclose(fp_)
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
def admin_color_scheme_picker(user_id_=None, *_args_):
    
    
    global _wp_admin_css_colors_
    php_check_if_defined("_wp_admin_css_colors_")
    php_ksort(_wp_admin_css_colors_)
    if (php_isset(lambda : _wp_admin_css_colors_["fresh"])):
        #// Set Default ('fresh') and Light should go first.
        _wp_admin_css_colors_ = php_array_filter(php_array_merge(Array({"fresh": "", "light": ""}), _wp_admin_css_colors_))
    # end if
    current_color_ = get_user_option("admin_color", user_id_)
    if php_empty(lambda : current_color_) or (not (php_isset(lambda : _wp_admin_css_colors_[current_color_]))):
        current_color_ = "fresh"
    # end if
    php_print(" <fieldset id=\"color-picker\" class=\"scheme-list\">\n      <legend class=\"screen-reader-text\"><span>")
    _e("Admin Color Scheme")
    php_print("</span></legend>\n       ")
    wp_nonce_field("save-color-scheme", "color-nonce", False)
    for color_,color_info_ in _wp_admin_css_colors_.items():
        php_print("         <div class=\"color-option ")
        php_print("selected" if color_ == current_color_ else "")
        php_print("\">\n                <input name=\"admin_color\" id=\"admin_color_")
        php_print(esc_attr(color_))
        php_print("\" type=\"radio\" value=\"")
        php_print(esc_attr(color_))
        php_print("\" class=\"tog\" ")
        checked(color_, current_color_)
        php_print(" />\n                <input type=\"hidden\" class=\"css_url\" value=\"")
        php_print(esc_url(color_info_.url))
        php_print("\" />\n              <input type=\"hidden\" class=\"icon_colors\" value=\"")
        php_print(esc_attr(wp_json_encode(Array({"icons": color_info_.icon_colors}))))
        php_print("\" />\n              <label for=\"admin_color_")
        php_print(esc_attr(color_))
        php_print("\">")
        php_print(esc_html(color_info_.name))
        php_print("""</label>
        <table class=\"color-palette\">
        <tr>
        """)
        for html_color_ in color_info_.colors:
            php_print("                     <td style=\"background-color: ")
            php_print(esc_attr(html_color_))
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
def wp_color_scheme_settings(*_args_):
    
    
    global _wp_admin_css_colors_
    php_check_if_defined("_wp_admin_css_colors_")
    color_scheme_ = get_user_option("admin_color")
    #// It's possible to have a color scheme set that is no longer registered.
    if php_empty(lambda : _wp_admin_css_colors_[color_scheme_]):
        color_scheme_ = "fresh"
    # end if
    if (not php_empty(lambda : _wp_admin_css_colors_[color_scheme_].icon_colors)):
        icon_colors_ = _wp_admin_css_colors_[color_scheme_].icon_colors
    elif (not php_empty(lambda : _wp_admin_css_colors_["fresh"].icon_colors)):
        icon_colors_ = _wp_admin_css_colors_["fresh"].icon_colors
    else:
        #// Fall back to the default set of icon colors if the default scheme is missing.
        icon_colors_ = Array({"base": "#a0a5aa", "focus": "#00a0d2", "current": "#fff"})
    # end if
    php_print("<script type=\"text/javascript\">var _wpColorScheme = " + wp_json_encode(Array({"icons": icon_colors_})) + ";</script>\n")
# end def wp_color_scheme_settings
#// 
#// @since 3.3.0
#//
def _ipad_meta(*_args_):
    
    
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
def wp_check_locked_posts(response_=None, data_=None, screen_id_=None, *_args_):
    
    
    checked_ = Array()
    if php_array_key_exists("wp-check-locked-posts", data_) and php_is_array(data_["wp-check-locked-posts"]):
        for key_ in data_["wp-check-locked-posts"]:
            post_id_ = absint(php_substr(key_, 5))
            if (not post_id_):
                continue
            # end if
            user_id_ = wp_check_post_lock(post_id_)
            if user_id_:
                user_ = get_userdata(user_id_)
                if user_ and current_user_can("edit_post", post_id_):
                    send_ = Array({"text": php_sprintf(__("%s is currently editing"), user_.display_name)})
                    avatar_ = get_avatar(user_.ID, 18)
                    if avatar_ and php_preg_match("|src='([^']+)'|", avatar_, matches_):
                        send_["avatar_src"] = matches_[1]
                    # end if
                    checked_[key_] = send_
                # end if
            # end if
        # end for
    # end if
    if (not php_empty(lambda : checked_)):
        response_["wp-check-locked-posts"] = checked_
    # end if
    return response_
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
def wp_refresh_post_lock(response_=None, data_=None, screen_id_=None, *_args_):
    
    
    if php_array_key_exists("wp-refresh-post-lock", data_):
        received_ = data_["wp-refresh-post-lock"]
        send_ = Array()
        post_id_ = absint(received_["post_id"])
        if (not post_id_):
            return response_
        # end if
        if (not current_user_can("edit_post", post_id_)):
            return response_
        # end if
        user_id_ = wp_check_post_lock(post_id_)
        user_ = get_userdata(user_id_)
        if user_:
            error_ = Array({"text": php_sprintf(__("%s has taken over and is currently editing."), user_.display_name)})
            avatar_ = get_avatar(user_.ID, 64)
            if avatar_:
                if php_preg_match("|src='([^']+)'|", avatar_, matches_):
                    error_["avatar_src"] = matches_[1]
                # end if
            # end if
            send_["lock_error"] = error_
        else:
            new_lock_ = wp_set_post_lock(post_id_)
            if new_lock_:
                send_["new_lock"] = php_implode(":", new_lock_)
            # end if
        # end if
        response_["wp-refresh-post-lock"] = send_
    # end if
    return response_
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
def wp_refresh_post_nonces(response_=None, data_=None, screen_id_=None, *_args_):
    
    
    if php_array_key_exists("wp-refresh-post-nonces", data_):
        received_ = data_["wp-refresh-post-nonces"]
        response_["wp-refresh-post-nonces"] = Array({"check": 1})
        post_id_ = absint(received_["post_id"])
        if (not post_id_):
            return response_
        # end if
        if (not current_user_can("edit_post", post_id_)):
            return response_
        # end if
        response_["wp-refresh-post-nonces"] = Array({"replace": Array({"getpermalinknonce": wp_create_nonce("getpermalink"), "samplepermalinknonce": wp_create_nonce("samplepermalink"), "closedpostboxesnonce": wp_create_nonce("closedpostboxes"), "_ajax_linking_nonce": wp_create_nonce("internal-linking"), "_wpnonce": wp_create_nonce("update-post_" + post_id_)})})
    # end if
    return response_
# end def wp_refresh_post_nonces
#// 
#// Add the latest Heartbeat and REST-API nonce to the Heartbeat response.
#// 
#// @since 5.0.0
#// 
#// @param array  $response  The Heartbeat response.
#// @return array The Heartbeat response.
#//
def wp_refresh_heartbeat_nonces(response_=None, *_args_):
    
    
    #// Refresh the Rest API nonce.
    response_["rest_nonce"] = wp_create_nonce("wp_rest")
    #// Refresh the Heartbeat nonce.
    response_["heartbeat_nonce"] = wp_create_nonce("heartbeat-nonce")
    return response_
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
def wp_heartbeat_set_suspension(settings_=None, *_args_):
    
    
    global pagenow_
    php_check_if_defined("pagenow_")
    if "post.php" == pagenow_ or "post-new.php" == pagenow_:
        settings_["suspension"] = "disable"
    # end if
    return settings_
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
def heartbeat_autosave(response_=None, data_=None, *_args_):
    
    
    if (not php_empty(lambda : data_["wp_autosave"])):
        saved_ = wp_autosave(data_["wp_autosave"])
        if is_wp_error(saved_):
            response_["wp_autosave"] = Array({"success": False, "message": saved_.get_error_message()})
        elif php_empty(lambda : saved_):
            response_["wp_autosave"] = Array({"success": False, "message": __("Error while saving.")})
        else:
            #// translators: Draft saved date format, see https://www.php.net/date
            draft_saved_date_format_ = __("g:i:s a")
            response_["wp_autosave"] = Array({"success": True, "message": php_sprintf(__("Draft saved at %s."), date_i18n(draft_saved_date_format_))})
        # end if
    # end if
    return response_
# end def heartbeat_autosave
#// 
#// Remove single-use URL parameters and create canonical link based on new URL.
#// 
#// Remove specific query string parameters from a URL, create the canonical link,
#// put it in the admin header, and change the current URL to match.
#// 
#// @since 4.2.0
#//
def wp_admin_canonical_url(*_args_):
    
    
    removable_query_args_ = wp_removable_query_args()
    if php_empty(lambda : removable_query_args_):
        return
    # end if
    #// Ensure we're using an absolute URL.
    current_url_ = set_url_scheme("http://" + PHP_SERVER["HTTP_HOST"] + PHP_SERVER["REQUEST_URI"])
    filtered_url_ = remove_query_arg(removable_query_args_, current_url_)
    php_print(" <link id=\"wp-admin-canonical\" rel=\"canonical\" href=\"")
    php_print(esc_url(filtered_url_))
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
def wp_admin_headers(*_args_):
    
    
    policy_ = "strict-origin-when-cross-origin"
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
    policy_ = apply_filters("admin_referrer_policy", policy_)
    php_header(php_sprintf("Referrer-Policy: %s", policy_))
# end def wp_admin_headers
#// 
#// Outputs JS that reloads the page if the user navigated to it with the Back or Forward button.
#// 
#// Used on the Edit Post and Add New Post screens. Needed to ensure the page is not loaded from browser cache,
#// so the post title and editor content are the last saved versions. Ideally this script should run first in the head.
#// 
#// @since 4.6.0
#//
def wp_page_reload_on_back_button_js(*_args_):
    
    
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
def update_option_new_admin_email(old_value_=None, value_=None, *_args_):
    
    
    if get_option("admin_email") == value_ or (not is_email(value_)):
        return
    # end if
    hash_ = php_md5(value_ + time() + wp_rand())
    new_admin_email_ = Array({"hash": hash_, "newemail": value_})
    update_option("adminhash", new_admin_email_)
    switched_locale_ = switch_to_locale(get_user_locale())
    #// translators: Do not translate USERNAME, ADMIN_URL, EMAIL, SITENAME, SITEURL: those are placeholders.
    email_text_ = __("""Howdy ###USERNAME###,
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
    content_ = apply_filters("new_admin_email_content", email_text_, new_admin_email_)
    current_user_ = wp_get_current_user()
    content_ = php_str_replace("###USERNAME###", current_user_.user_login, content_)
    content_ = php_str_replace("###ADMIN_URL###", esc_url(self_admin_url("options.php?adminhash=" + hash_)), content_)
    content_ = php_str_replace("###EMAIL###", value_, content_)
    content_ = php_str_replace("###SITENAME###", wp_specialchars_decode(get_option("blogname"), ENT_QUOTES), content_)
    content_ = php_str_replace("###SITEURL###", home_url(), content_)
    wp_mail(value_, php_sprintf(__("[%s] New Admin Email Address"), wp_specialchars_decode(get_option("blogname"), ENT_QUOTES)), content_)
    if switched_locale_:
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
def _wp_privacy_settings_filter_draft_page_titles(title_=None, page_=None, *_args_):
    
    
    if "draft" == page_.post_status and "privacy" == get_current_screen().id:
        #// translators: %s: Page title.
        title_ = php_sprintf(__("%s (Draft)"), title_)
    # end if
    return title_
# end def _wp_privacy_settings_filter_draft_page_titles
#// 
#// Checks if the user needs to update PHP.
#// 
#// @since 5.1.0
#// @since 5.1.1 Added the {@see 'wp_is_php_version_acceptable'} filter.
#// 
#// @return array|false $response Array of PHP version data. False on failure.
#//
def wp_check_php_version(*_args_):
    
    
    version_ = php_phpversion()
    key_ = php_md5(version_)
    response_ = get_site_transient("php_check_" + key_)
    if False == response_:
        url_ = "http://api.wordpress.org/core/serve-happy/1.0/"
        if wp_http_supports(Array("ssl")):
            url_ = set_url_scheme(url_, "https")
        # end if
        url_ = add_query_arg("php_version", version_, url_)
        response_ = wp_remote_get(url_)
        if is_wp_error(response_) or 200 != wp_remote_retrieve_response_code(response_):
            return False
        # end if
        #// 
        #// Response should be an array with:
        #// 'recommended_version' - string - The PHP version recommended by WordPress.
        #// 'is_supported' - boolean - Whether the PHP version is actively supported.
        #// 'is_secure' - boolean - Whether the PHP version receives security updates.
        #// 'is_acceptable' - boolean - Whether the PHP version is still acceptable for WordPress.
        #//
        response_ = php_json_decode(wp_remote_retrieve_body(response_), True)
        if (not php_is_array(response_)):
            return False
        # end if
        set_site_transient("php_check_" + key_, response_, WEEK_IN_SECONDS)
    # end if
    if (php_isset(lambda : response_["is_acceptable"])) and response_["is_acceptable"]:
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
        response_["is_acceptable"] = php_bool(apply_filters("wp_is_php_version_acceptable", True, version_))
    # end if
    return response_
# end def wp_check_php_version
