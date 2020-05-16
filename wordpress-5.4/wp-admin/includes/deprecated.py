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
#// Deprecated admin functions from past WordPress versions. You shouldn't use these
#// functions and look for the alternatives instead. The functions will be removed
#// in a later version.
#// 
#// @package WordPress
#// @subpackage Deprecated
#// 
#// 
#// Deprecated functions come here to die.
#// 
#// 
#// @since 2.1.0
#// @deprecated 2.1.0 Use wp_editor()
#// @see wp_editor()
#//
def tinymce_include(*args_):
    
    _deprecated_function(__FUNCTION__, "2.1.0", "wp_editor()")
    wp_tiny_mce()
# end def tinymce_include
#// 
#// Unused Admin function.
#// 
#// @since 2.0.0
#// @deprecated 2.5.0
#// 
#//
def documentation_link(*args_):
    
    _deprecated_function(__FUNCTION__, "2.5.0")
# end def documentation_link
#// 
#// Calculates the new dimensions for a downsampled image.
#// 
#// @since 2.0.0
#// @deprecated 3.0.0 Use wp_constrain_dimensions()
#// @see wp_constrain_dimensions()
#// 
#// @param int $width Current width of the image
#// @param int $height Current height of the image
#// @param int $wmax Maximum wanted width
#// @param int $hmax Maximum wanted height
#// @return array Shrunk dimensions (width, height).
#//
def wp_shrink_dimensions(width=None, height=None, wmax=128, hmax=96, *args_):
    
    _deprecated_function(__FUNCTION__, "3.0.0", "wp_constrain_dimensions()")
    return wp_constrain_dimensions(width, height, wmax, hmax)
# end def wp_shrink_dimensions
#// 
#// Calculated the new dimensions for a downsampled image.
#// 
#// @since 2.0.0
#// @deprecated 3.5.0 Use wp_constrain_dimensions()
#// @see wp_constrain_dimensions()
#// 
#// @param int $width Current width of the image
#// @param int $height Current height of the image
#// @return array Shrunk dimensions (width, height).
#//
def get_udims(width=None, height=None, *args_):
    
    _deprecated_function(__FUNCTION__, "3.5.0", "wp_constrain_dimensions()")
    return wp_constrain_dimensions(width, height, 128, 96)
# end def get_udims
#// 
#// Legacy function used to generate the categories checklist control.
#// 
#// @since 0.71
#// @deprecated 2.6.0 Use wp_category_checklist()
#// @see wp_category_checklist()
#// 
#// @param int $default       Unused.
#// @param int $parent        Unused.
#// @param array $popular_ids Unused.
#//
def dropdown_categories(default=0, parent=0, popular_ids=Array(), *args_):
    
    _deprecated_function(__FUNCTION__, "2.6.0", "wp_category_checklist()")
    global post_ID
    php_check_if_defined("post_ID")
    wp_category_checklist(post_ID)
# end def dropdown_categories
#// 
#// Legacy function used to generate a link categories checklist control.
#// 
#// @since 2.1.0
#// @deprecated 2.6.0 Use wp_link_category_checklist()
#// @see wp_link_category_checklist()
#// 
#// @param int $default Unused.
#//
def dropdown_link_categories(default=0, *args_):
    
    _deprecated_function(__FUNCTION__, "2.6.0", "wp_link_category_checklist()")
    global link_id
    php_check_if_defined("link_id")
    wp_link_category_checklist(link_id)
# end def dropdown_link_categories
#// 
#// Get the real filesystem path to a file to edit within the admin.
#// 
#// @since 1.5.0
#// @deprecated 2.9.0
#// @uses WP_CONTENT_DIR Full filesystem path to the wp-content directory.
#// 
#// @param string $file Filesystem path relative to the wp-content directory.
#// @return string Full filesystem path to edit.
#//
def get_real_file_to_edit(file=None, *args_):
    
    _deprecated_function(__FUNCTION__, "2.9.0")
    return WP_CONTENT_DIR + file
# end def get_real_file_to_edit
#// 
#// Legacy function used for generating a categories drop-down control.
#// 
#// @since 1.2.0
#// @deprecated 3.0.0 Use wp_dropdown_categories()
#// @see wp_dropdown_categories()
#// 
#// @param int $currentcat    Optional. ID of the current category. Default 0.
#// @param int $currentparent Optional. Current parent category ID. Default 0.
#// @param int $parent        Optional. Parent ID to retrieve categories for. Default 0.
#// @param int $level         Optional. Number of levels deep to display. Default 0.
#// @param array $categories  Optional. Categories to include in the control. Default 0.
#// @return bool|null False if no categories were found.
#//
def wp_dropdown_cats(currentcat=0, currentparent=0, parent=0, level=0, categories=0, *args_):
    
    _deprecated_function(__FUNCTION__, "3.0.0", "wp_dropdown_categories()")
    if (not categories):
        categories = get_categories(Array({"hide_empty": 0}))
    # end if
    if categories:
        for category in categories:
            if currentcat != category.term_id and parent == category.parent:
                pad = php_str_repeat("&#8211; ", level)
                category.name = esc_html(category.name)
                php_print(str("\n   <option value='") + str(category.term_id) + str("'"))
                if currentparent == category.term_id:
                    php_print(" selected='selected'")
                # end if
                php_print(str(">") + str(pad) + str(category.name) + str("</option>"))
                wp_dropdown_cats(currentcat, currentparent, category.term_id, level + 1, categories)
            # end if
        # end for
    else:
        return False
    # end if
# end def wp_dropdown_cats
#// 
#// Register a setting and its sanitization callback
#// 
#// @since 2.7.0
#// @deprecated 3.0.0 Use register_setting()
#// @see register_setting()
#// 
#// @param string $option_group A settings group name. Should correspond to a whitelisted option key name.
#// Default whitelisted option key names include 'general', 'discussion', 'media',
#// 'reading', 'writing', 'misc', 'options', and 'privacy'.
#// @param string $option_name The name of an option to sanitize and save.
#// @param callable $sanitize_callback A callback function that sanitizes the option's value.
#//
def add_option_update_handler(option_group=None, option_name=None, sanitize_callback="", *args_):
    
    _deprecated_function(__FUNCTION__, "3.0.0", "register_setting()")
    register_setting(option_group, option_name, sanitize_callback)
# end def add_option_update_handler
#// 
#// Unregister a setting
#// 
#// @since 2.7.0
#// @deprecated 3.0.0 Use unregister_setting()
#// @see unregister_setting()
#// 
#// @param string $option_group
#// @param string $option_name
#// @param callable $sanitize_callback
#//
def remove_option_update_handler(option_group=None, option_name=None, sanitize_callback="", *args_):
    
    _deprecated_function(__FUNCTION__, "3.0.0", "unregister_setting()")
    unregister_setting(option_group, option_name, sanitize_callback)
# end def remove_option_update_handler
#// 
#// Determines the language to use for CodePress syntax highlighting.
#// 
#// @since 2.8.0
#// @deprecated 3.0.0
#// 
#// @param string $filename
#//
def codepress_get_lang(filename=None, *args_):
    
    _deprecated_function(__FUNCTION__, "3.0.0")
# end def codepress_get_lang
#// 
#// Adds JavaScript required to make CodePress work on the theme/plugin editors.
#// 
#// @since 2.8.0
#// @deprecated 3.0.0
#//
def codepress_footer_js(*args_):
    
    _deprecated_function(__FUNCTION__, "3.0.0")
# end def codepress_footer_js
#// 
#// Determine whether to use CodePress.
#// 
#// @since 2.8.0
#// @deprecated 3.0.0
#//
def use_codepress(*args_):
    
    _deprecated_function(__FUNCTION__, "3.0.0")
# end def use_codepress
#// 
#// Get all user IDs.
#// 
#// @deprecated 3.1.0 Use get_users()
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @return array List of user IDs.
#//
def get_author_user_ids(*args_):
    
    _deprecated_function(__FUNCTION__, "3.1.0", "get_users()")
    global wpdb
    php_check_if_defined("wpdb")
    if (not is_multisite()):
        level_key = wpdb.get_blog_prefix() + "user_level"
    else:
        level_key = wpdb.get_blog_prefix() + "capabilities"
    # end if
    #// WPMU site admins don't have user_levels.
    return wpdb.get_col(wpdb.prepare(str("SELECT user_id FROM ") + str(wpdb.usermeta) + str(" WHERE meta_key = %s AND meta_value != '0'"), level_key))
# end def get_author_user_ids
#// 
#// Gets author users who can edit posts.
#// 
#// @deprecated 3.1.0 Use get_users()
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int $user_id User ID.
#// @return array|bool List of editable authors. False if no editable users.
#//
def get_editable_authors(user_id=None, *args_):
    
    _deprecated_function(__FUNCTION__, "3.1.0", "get_users()")
    global wpdb
    php_check_if_defined("wpdb")
    editable = get_editable_user_ids(user_id)
    if (not editable):
        return False
    else:
        editable = join(",", editable)
        authors = wpdb.get_results(str("SELECT * FROM ") + str(wpdb.users) + str(" WHERE ID IN (") + str(editable) + str(") ORDER BY display_name"))
    # end if
    return apply_filters("get_editable_authors", authors)
# end def get_editable_authors
#// 
#// Gets the IDs of any users who can edit posts.
#// 
#// @deprecated 3.1.0 Use get_users()
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int  $user_id       User ID.
#// @param bool $exclude_zeros Optional. Whether to exclude zeroes. Default true.
#// @return array Array of editable user IDs, empty array otherwise.
#//
def get_editable_user_ids(user_id=None, exclude_zeros=True, post_type="post", *args_):
    
    _deprecated_function(__FUNCTION__, "3.1.0", "get_users()")
    global wpdb
    php_check_if_defined("wpdb")
    user = get_userdata(user_id)
    if (not user):
        return Array()
    # end if
    post_type_obj = get_post_type_object(post_type)
    if (not user.has_cap(post_type_obj.cap.edit_others_posts)):
        if user.has_cap(post_type_obj.cap.edit_posts) or (not exclude_zeros):
            return Array(user.ID)
        else:
            return Array()
        # end if
    # end if
    if (not is_multisite()):
        level_key = wpdb.get_blog_prefix() + "user_level"
    else:
        level_key = wpdb.get_blog_prefix() + "capabilities"
    # end if
    #// WPMU site admins don't have user_levels.
    query = wpdb.prepare(str("SELECT user_id FROM ") + str(wpdb.usermeta) + str(" WHERE meta_key = %s"), level_key)
    if exclude_zeros:
        query += " AND meta_value != '0'"
    # end if
    return wpdb.get_col(query)
# end def get_editable_user_ids
#// 
#// Gets all users who are not authors.
#// 
#// @deprecated 3.1.0 Use get_users()
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#//
def get_nonauthor_user_ids(*args_):
    
    _deprecated_function(__FUNCTION__, "3.1.0", "get_users()")
    global wpdb
    php_check_if_defined("wpdb")
    if (not is_multisite()):
        level_key = wpdb.get_blog_prefix() + "user_level"
    else:
        level_key = wpdb.get_blog_prefix() + "capabilities"
    # end if
    #// WPMU site admins don't have user_levels.
    return wpdb.get_col(wpdb.prepare(str("SELECT user_id FROM ") + str(wpdb.usermeta) + str(" WHERE meta_key = %s AND meta_value = '0'"), level_key))
# end def get_nonauthor_user_ids
if (not php_class_exists("WP_User_Search", False)):
    #// 
    #// WordPress User Search class.
    #// 
    #// @since 2.1.0
    #// @deprecated 3.1.0 Use WP_User_Query
    #//
    class WP_User_Search():
        results = Array()
        search_term = Array()
        page = Array()
        role = Array()
        raw_page = Array()
        users_per_page = 50
        first_user = Array()
        last_user = Array()
        query_limit = Array()
        query_orderby = Array()
        query_from = Array()
        query_where = Array()
        total_users_for_query = 0
        too_many_total_users = False
        search_errors = Array()
        paging_text = Array()
        #// 
        #// PHP5 Constructor - Sets up the object properties.
        #// 
        #// @since 2.1.0
        #// 
        #// @param string $search_term Search terms string.
        #// @param int $page Optional. Page ID.
        #// @param string $role Role name.
        #// @return WP_User_Search
        #//
        def __init__(self, search_term="", page="", role=""):
            
            _deprecated_function(__FUNCTION__, "3.1.0", "WP_User_Query")
            self.search_term = wp_unslash(search_term)
            self.raw_page = False if "" == page else php_int(page)
            self.page = 1 if php_int("" == page) else page
            self.role = role
            self.prepare_query()
            self.query()
            self.do_paging()
        # end def __init__
        #// 
        #// PHP4 Constructor - Sets up the object properties.
        #// 
        #// @since 2.1.0
        #// 
        #// @param string $search_term Search terms string.
        #// @param int $page Optional. Page ID.
        #// @param string $role Role name.
        #// @return WP_User_Search
        #//
        def wp_user_search(self, search_term="", page="", role=""):
            
            self.__init__(search_term, page, role)
        # end def wp_user_search
        #// 
        #// Prepares the user search query (legacy).
        #// 
        #// @since 2.1.0
        #// @access public
        #//
        def prepare_query(self):
            
            global wpdb
            php_check_if_defined("wpdb")
            self.first_user = self.page - 1 * self.users_per_page
            self.query_limit = wpdb.prepare(" LIMIT %d, %d", self.first_user, self.users_per_page)
            self.query_orderby = " ORDER BY user_login"
            search_sql = ""
            if self.search_term:
                searches = Array()
                search_sql = "AND ("
                for col in Array("user_login", "user_nicename", "user_email", "user_url", "display_name"):
                    searches[-1] = wpdb.prepare(col + " LIKE %s", "%" + like_escape(self.search_term) + "%")
                # end for
                search_sql += php_implode(" OR ", searches)
                search_sql += ")"
            # end if
            self.query_from = str(" FROM ") + str(wpdb.users)
            self.query_where = str(" WHERE 1=1 ") + str(search_sql)
            if self.role:
                self.query_from += str(" INNER JOIN ") + str(wpdb.usermeta) + str(" ON ") + str(wpdb.users) + str(".ID = ") + str(wpdb.usermeta) + str(".user_id")
                self.query_where += wpdb.prepare(str(" AND ") + str(wpdb.usermeta) + str(".meta_key = '") + str(wpdb.prefix) + str("capabilities' AND ") + str(wpdb.usermeta) + str(".meta_value LIKE %s"), "%" + self.role + "%")
            elif is_multisite():
                level_key = wpdb.prefix + "capabilities"
                #// WPMU site admins don't have user_levels.
                self.query_from += str(", ") + str(wpdb.usermeta)
                self.query_where += str(" AND ") + str(wpdb.users) + str(".ID = ") + str(wpdb.usermeta) + str(".user_id AND meta_key = '") + str(level_key) + str("'")
            # end if
            do_action_ref_array("pre_user_search", Array(self))
        # end def prepare_query
        #// 
        #// Executes the user search query.
        #// 
        #// @since 2.1.0
        #// @access public
        #//
        def query(self):
            
            global wpdb
            php_check_if_defined("wpdb")
            self.results = wpdb.get_col(str("SELECT DISTINCT(") + str(wpdb.users) + str(".ID)") + self.query_from + self.query_where + self.query_orderby + self.query_limit)
            if self.results:
                self.total_users_for_query = wpdb.get_var(str("SELECT COUNT(DISTINCT(") + str(wpdb.users) + str(".ID))") + self.query_from + self.query_where)
            else:
                self.search_errors = php_new_class("WP_Error", lambda : WP_Error("no_matching_users_found", __("No users found.")))
            # end if
        # end def query
        #// 
        #// Prepares variables for use in templates.
        #// 
        #// @since 2.1.0
        #// @access public
        #//
        def prepare_vars_for_template_usage(self):
            
            pass
        # end def prepare_vars_for_template_usage
        #// 
        #// Handles paging for the user search query.
        #// 
        #// @since 2.1.0
        #// @access public
        #//
        def do_paging(self):
            
            if self.total_users_for_query > self.users_per_page:
                #// Have to page the results.
                args = Array()
                if (not php_empty(lambda : self.search_term)):
                    args["usersearch"] = urlencode(self.search_term)
                # end if
                if (not php_empty(lambda : self.role)):
                    args["role"] = urlencode(self.role)
                # end if
                self.paging_text = paginate_links(Array({"total": ceil(self.total_users_for_query / self.users_per_page), "current": self.page, "base": "users.php?%_%", "format": "userspage=%#%", "add_args": args}))
                if self.paging_text:
                    self.paging_text = php_sprintf("<span class=\"displaying-num\">" + __("Displaying %1$s&#8211;%2$s of %3$s") + "</span>%s", number_format_i18n(self.page - 1 * self.users_per_page + 1), number_format_i18n(php_min(self.page * self.users_per_page, self.total_users_for_query)), number_format_i18n(self.total_users_for_query), self.paging_text)
                # end if
            # end if
        # end def do_paging
        #// 
        #// Retrieves the user search query results.
        #// 
        #// @since 2.1.0
        #// @access public
        #// 
        #// @return array
        #//
        def get_results(self):
            
            return self.results
        # end def get_results
        #// 
        #// Displaying paging text.
        #// 
        #// @see do_paging() Builds paging text.
        #// 
        #// @since 2.1.0
        #// @access public
        #//
        def page_links(self):
            
            php_print(self.paging_text)
        # end def page_links
        #// 
        #// Whether paging is enabled.
        #// 
        #// @see do_paging() Builds paging text.
        #// 
        #// @since 2.1.0
        #// @access public
        #// 
        #// @return bool
        #//
        def results_are_paged(self):
            
            if self.paging_text:
                return True
            # end if
            return False
        # end def results_are_paged
        #// 
        #// Whether there are search terms.
        #// 
        #// @since 2.1.0
        #// @access public
        #// 
        #// @return bool
        #//
        def is_search(self):
            
            if self.search_term:
                return True
            # end if
            return False
        # end def is_search
    # end class WP_User_Search
# end if
#// 
#// Retrieves editable posts from other users.
#// 
#// @since 2.3.0
#// @deprecated 3.1.0 Use get_posts()
#// @see get_posts()
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int    $user_id User ID to not retrieve posts from.
#// @param string $type    Optional. Post type to retrieve. Accepts 'draft', 'pending' or 'any' (all).
#// Default 'any'.
#// @return array List of posts from others.
#//
def get_others_unpublished_posts(user_id=None, type="any", *args_):
    
    _deprecated_function(__FUNCTION__, "3.1.0")
    global wpdb
    php_check_if_defined("wpdb")
    editable = get_editable_user_ids(user_id)
    if php_in_array(type, Array("draft", "pending")):
        type_sql = str(" post_status = '") + str(type) + str("' ")
    else:
        type_sql = " ( post_status = 'draft' OR post_status = 'pending' ) "
    # end if
    dir = "ASC" if "pending" == type else "DESC"
    if (not editable):
        other_unpubs = ""
    else:
        editable = join(",", editable)
        other_unpubs = wpdb.get_results(wpdb.prepare(str("SELECT ID, post_title, post_author FROM ") + str(wpdb.posts) + str(" WHERE post_type = 'post' AND ") + str(type_sql) + str(" AND post_author IN (") + str(editable) + str(") AND post_author != %d ORDER BY post_modified ") + str(dir), user_id))
    # end if
    return apply_filters("get_others_drafts", other_unpubs)
# end def get_others_unpublished_posts
#// 
#// Retrieve drafts from other users.
#// 
#// @deprecated 3.1.0 Use get_posts()
#// @see get_posts()
#// 
#// @param int $user_id User ID.
#// @return array List of drafts from other users.
#//
def get_others_drafts(user_id=None, *args_):
    
    _deprecated_function(__FUNCTION__, "3.1.0")
    return get_others_unpublished_posts(user_id, "draft")
# end def get_others_drafts
#// 
#// Retrieve pending review posts from other users.
#// 
#// @deprecated 3.1.0 Use get_posts()
#// @see get_posts()
#// 
#// @param int $user_id User ID.
#// @return array List of posts with pending review post type from other users.
#//
def get_others_pending(user_id=None, *args_):
    
    _deprecated_function(__FUNCTION__, "3.1.0")
    return get_others_unpublished_posts(user_id, "pending")
# end def get_others_pending
#// 
#// Output the QuickPress dashboard widget.
#// 
#// @since 3.0.0
#// @deprecated 3.2.0 Use wp_dashboard_quick_press()
#// @see wp_dashboard_quick_press()
#//
def wp_dashboard_quick_press_output(*args_):
    
    _deprecated_function(__FUNCTION__, "3.2.0", "wp_dashboard_quick_press()")
    wp_dashboard_quick_press()
# end def wp_dashboard_quick_press_output
#// 
#// Outputs the TinyMCE editor.
#// 
#// @since 2.7.0
#// @deprecated 3.3.0 Use wp_editor()
#// @see wp_editor()
#// 
#// @staticvar int $num
#//
def wp_tiny_mce(teeny=False, settings=False, *args_):
    
    _deprecated_function(__FUNCTION__, "3.3.0", "wp_editor()")
    num = 1
    if (not php_class_exists("_WP_Editors", False)):
        php_include_file(ABSPATH + WPINC + "/class-wp-editor.php", once=True)
    # end if
    editor_id = "content" + num
    num += 1
    set = Array({"teeny": teeny, "tinymce": settings if settings else True, "quicktags": False})
    set = _WP_Editors.parse_settings(editor_id, set)
    _WP_Editors.editor_settings(editor_id, set)
# end def wp_tiny_mce
#// 
#// Preloads TinyMCE dialogs.
#// 
#// @deprecated 3.3.0 Use wp_editor()
#// @see wp_editor()
#//
def wp_preload_dialogs(*args_):
    
    _deprecated_function(__FUNCTION__, "3.3.0", "wp_editor()")
# end def wp_preload_dialogs
#// 
#// Prints TinyMCE editor JS.
#// 
#// @deprecated 3.3.0 Use wp_editor()
#// @see wp_editor()
#//
def wp_print_editor_js(*args_):
    
    _deprecated_function(__FUNCTION__, "3.3.0", "wp_editor()")
# end def wp_print_editor_js
#// 
#// Handles quicktags.
#// 
#// @deprecated 3.3.0 Use wp_editor()
#// @see wp_editor()
#//
def wp_quicktags(*args_):
    
    _deprecated_function(__FUNCTION__, "3.3.0", "wp_editor()")
# end def wp_quicktags
#// 
#// Returns the screen layout options.
#// 
#// @since 2.8.0
#// @deprecated 3.3.0 WP_Screen::render_screen_layout()
#// @see WP_Screen::render_screen_layout()
#//
def screen_layout(screen=None, *args_):
    
    _deprecated_function(__FUNCTION__, "3.3.0", "$current_screen->render_screen_layout()")
    current_screen = get_current_screen()
    if (not current_screen):
        return ""
    # end if
    ob_start()
    current_screen.render_screen_layout()
    return ob_get_clean()
# end def screen_layout
#// 
#// Returns the screen's per-page options.
#// 
#// @since 2.8.0
#// @deprecated 3.3.0 Use WP_Screen::render_per_page_options()
#// @see WP_Screen::render_per_page_options()
#//
def screen_options(screen=None, *args_):
    
    _deprecated_function(__FUNCTION__, "3.3.0", "$current_screen->render_per_page_options()")
    current_screen = get_current_screen()
    if (not current_screen):
        return ""
    # end if
    ob_start()
    current_screen.render_per_page_options()
    return ob_get_clean()
# end def screen_options
#// 
#// Renders the screen's help.
#// 
#// @since 2.7.0
#// @deprecated 3.3.0 Use WP_Screen::render_screen_meta()
#// @see WP_Screen::render_screen_meta()
#//
def screen_meta(screen=None, *args_):
    
    current_screen = get_current_screen()
    current_screen.render_screen_meta()
# end def screen_meta
#// 
#// Favorite actions were deprecated in version 3.2. Use the admin bar instead.
#// 
#// @since 2.7.0
#// @deprecated 3.2.0 Use WP_Admin_Bar
#// @see WP_Admin_Bar
#//
def favorite_actions(*args_):
    
    _deprecated_function(__FUNCTION__, "3.2.0", "WP_Admin_Bar")
# end def favorite_actions
#// 
#// Handles uploading an image.
#// 
#// @deprecated 3.3.0 Use wp_media_upload_handler()
#// @see wp_media_upload_handler()
#// 
#// @return null|string
#//
def media_upload_image(*args_):
    
    _deprecated_function(__FUNCTION__, "3.3.0", "wp_media_upload_handler()")
    return wp_media_upload_handler()
# end def media_upload_image
#// 
#// Handles uploading an audio file.
#// 
#// @deprecated 3.3.0 Use wp_media_upload_handler()
#// @see wp_media_upload_handler()
#// 
#// @return null|string
#//
def media_upload_audio(*args_):
    
    _deprecated_function(__FUNCTION__, "3.3.0", "wp_media_upload_handler()")
    return wp_media_upload_handler()
# end def media_upload_audio
#// 
#// Handles uploading a video file.
#// 
#// @deprecated 3.3.0 Use wp_media_upload_handler()
#// @see wp_media_upload_handler()
#// 
#// @return null|string
#//
def media_upload_video(*args_):
    
    _deprecated_function(__FUNCTION__, "3.3.0", "wp_media_upload_handler()")
    return wp_media_upload_handler()
# end def media_upload_video
#// 
#// Handles uploading a generic file.
#// 
#// @deprecated 3.3.0 Use wp_media_upload_handler()
#// @see wp_media_upload_handler()
#// 
#// @return null|string
#//
def media_upload_file(*args_):
    
    _deprecated_function(__FUNCTION__, "3.3.0", "wp_media_upload_handler()")
    return wp_media_upload_handler()
# end def media_upload_file
#// 
#// Handles retrieving the insert-from-URL form for an image.
#// 
#// @deprecated 3.3.0 Use wp_media_insert_url_form()
#// @see wp_media_insert_url_form()
#// 
#// @return string
#//
def type_url_form_image(*args_):
    
    _deprecated_function(__FUNCTION__, "3.3.0", "wp_media_insert_url_form('image')")
    return wp_media_insert_url_form("image")
# end def type_url_form_image
#// 
#// Handles retrieving the insert-from-URL form for an audio file.
#// 
#// @deprecated 3.3.0 Use wp_media_insert_url_form()
#// @see wp_media_insert_url_form()
#// 
#// @return string
#//
def type_url_form_audio(*args_):
    
    _deprecated_function(__FUNCTION__, "3.3.0", "wp_media_insert_url_form('audio')")
    return wp_media_insert_url_form("audio")
# end def type_url_form_audio
#// 
#// Handles retrieving the insert-from-URL form for a video file.
#// 
#// @deprecated 3.3.0 Use wp_media_insert_url_form()
#// @see wp_media_insert_url_form()
#// 
#// @return string
#//
def type_url_form_video(*args_):
    
    _deprecated_function(__FUNCTION__, "3.3.0", "wp_media_insert_url_form('video')")
    return wp_media_insert_url_form("video")
# end def type_url_form_video
#// 
#// Handles retrieving the insert-from-URL form for a generic file.
#// 
#// @deprecated 3.3.0 Use wp_media_insert_url_form()
#// @see wp_media_insert_url_form()
#// 
#// @return string
#//
def type_url_form_file(*args_):
    
    _deprecated_function(__FUNCTION__, "3.3.0", "wp_media_insert_url_form('file')")
    return wp_media_insert_url_form("file")
# end def type_url_form_file
#// 
#// Add contextual help text for a page.
#// 
#// Creates an 'Overview' help tab.
#// 
#// @since 2.7.0
#// @deprecated 3.3.0 Use WP_Screen::add_help_tab()
#// @see WP_Screen::add_help_tab()
#// 
#// @param string    $screen The handle for the screen to add help to. This is usually the hook name returned by the add_*_page() functions.
#// @param string    $help   The content of an 'Overview' help tab.
#//
def add_contextual_help(screen=None, help=None, *args_):
    
    _deprecated_function(__FUNCTION__, "3.3.0", "get_current_screen()->add_help_tab()")
    if php_is_string(screen):
        screen = convert_to_screen(screen)
    # end if
    WP_Screen.add_old_compat_help(screen, help)
# end def add_contextual_help
#// 
#// Get the allowed themes for the current site.
#// 
#// @since 3.0.0
#// @deprecated 3.4.0 Use wp_get_themes()
#// @see wp_get_themes()
#// 
#// @return WP_Theme[] Array of WP_Theme objects keyed by their name.
#//
def get_allowed_themes(*args_):
    
    _deprecated_function(__FUNCTION__, "3.4.0", "wp_get_themes( array( 'allowed' => true ) )")
    themes = wp_get_themes(Array({"allowed": True}))
    wp_themes = Array()
    for theme in themes:
        wp_themes[theme.get("Name")] = theme
    # end for
    return wp_themes
# end def get_allowed_themes
#// 
#// Retrieves a list of broken themes.
#// 
#// @since 1.5.0
#// @deprecated 3.4.0 Use wp_get_themes()
#// @see wp_get_themes()
#// 
#// @return array
#//
def get_broken_themes(*args_):
    
    _deprecated_function(__FUNCTION__, "3.4.0", "wp_get_themes( array( 'errors' => true )")
    themes = wp_get_themes(Array({"errors": True}))
    broken = Array()
    for theme in themes:
        name = theme.get("Name")
        broken[name] = Array({"Name": name, "Title": name, "Description": theme.errors().get_error_message()})
    # end for
    return broken
# end def get_broken_themes
#// 
#// Retrieves information on the current active theme.
#// 
#// @since 2.0.0
#// @deprecated 3.4.0 Use wp_get_theme()
#// @see wp_get_theme()
#// 
#// @return WP_Theme
#//
def current_theme_info(*args_):
    
    _deprecated_function(__FUNCTION__, "3.4.0", "wp_get_theme()")
    return wp_get_theme()
# end def current_theme_info
#// 
#// This was once used to display an 'Insert into Post' button.
#// 
#// Now it is deprecated and stubbed.
#// 
#// @deprecated 3.5.0
#//
def _insert_into_post_button(type=None, *args_):
    
    _deprecated_function(__FUNCTION__, "3.5.0")
# end def _insert_into_post_button
#// 
#// This was once used to display a media button.
#// 
#// Now it is deprecated and stubbed.
#// 
#// @deprecated 3.5.0
#//
def _media_button(title=None, icon=None, type=None, id=None, *args_):
    
    _deprecated_function(__FUNCTION__, "3.5.0")
# end def _media_button
#// 
#// Gets an existing post and format it for editing.
#// 
#// @since 2.0.0
#// @deprecated 3.5.0 Use get_post()
#// @see get_post()
#// 
#// @param int $id
#// @return object
#//
def get_post_to_edit(id=None, *args_):
    
    _deprecated_function(__FUNCTION__, "3.5.0", "get_post()")
    return get_post(id, OBJECT, "edit")
# end def get_post_to_edit
#// 
#// Gets the default page information to use.
#// 
#// @since 2.5.0
#// @deprecated 3.5.0 Use get_default_post_to_edit()
#// @see get_default_post_to_edit()
#// 
#// @return WP_Post Post object containing all the default post data as attributes
#//
def get_default_page_to_edit(*args_):
    
    _deprecated_function(__FUNCTION__, "3.5.0", "get_default_post_to_edit( 'page' )")
    page = get_default_post_to_edit()
    page.post_type = "page"
    return page
# end def get_default_page_to_edit
#// 
#// This was once used to create a thumbnail from an Image given a maximum side size.
#// 
#// @since 1.2.0
#// @deprecated 3.5.0 Use image_resize()
#// @see image_resize()
#// 
#// @param mixed $file Filename of the original image, Or attachment id.
#// @param int $max_side Maximum length of a single side for the thumbnail.
#// @param mixed $deprecated Never used.
#// @return string Thumbnail path on success, Error string on failure.
#//
def wp_create_thumbnail(file=None, max_side=None, deprecated="", *args_):
    
    _deprecated_function(__FUNCTION__, "3.5.0", "image_resize()")
    return apply_filters("wp_create_thumbnail", image_resize(file, max_side, max_side))
# end def wp_create_thumbnail
#// 
#// This was once used to display a meta box for the nav menu theme locations.
#// 
#// Deprecated in favor of a 'Manage Locations' tab added to nav menus management screen.
#// 
#// @since 3.0.0
#// @deprecated 3.6.0
#//
def wp_nav_menu_locations_meta_box(*args_):
    
    _deprecated_function(__FUNCTION__, "3.6.0")
# end def wp_nav_menu_locations_meta_box
#// 
#// This was once used to kick-off the Core Updater.
#// 
#// Deprecated in favor of instantating a Core_Upgrader instance directly,
#// and calling the 'upgrade' method.
#// 
#// @since 2.7.0
#// @deprecated 3.7.0 Use Core_Upgrader
#// @see Core_Upgrader
#//
def wp_update_core(current=None, feedback="", *args_):
    
    _deprecated_function(__FUNCTION__, "3.7.0", "new Core_Upgrader();")
    if (not php_empty(lambda : feedback)):
        add_filter("update_feedback", feedback)
    # end if
    php_include_file(ABSPATH + "wp-admin/includes/class-wp-upgrader.php", once=False)
    upgrader = php_new_class("Core_Upgrader", lambda : Core_Upgrader())
    return upgrader.upgrade(current)
# end def wp_update_core
#// 
#// This was once used to kick-off the Plugin Updater.
#// 
#// Deprecated in favor of instantating a Plugin_Upgrader instance directly,
#// and calling the 'upgrade' method.
#// Unused since 2.8.0.
#// 
#// @since 2.5.0
#// @deprecated 3.7.0 Use Plugin_Upgrader
#// @see Plugin_Upgrader
#//
def wp_update_plugin(plugin=None, feedback="", *args_):
    
    _deprecated_function(__FUNCTION__, "3.7.0", "new Plugin_Upgrader();")
    if (not php_empty(lambda : feedback)):
        add_filter("update_feedback", feedback)
    # end if
    php_include_file(ABSPATH + "wp-admin/includes/class-wp-upgrader.php", once=False)
    upgrader = php_new_class("Plugin_Upgrader", lambda : Plugin_Upgrader())
    return upgrader.upgrade(plugin)
# end def wp_update_plugin
#// 
#// This was once used to kick-off the Theme Updater.
#// 
#// Deprecated in favor of instantiating a Theme_Upgrader instance directly,
#// and calling the 'upgrade' method.
#// Unused since 2.8.0.
#// 
#// @since 2.7.0
#// @deprecated 3.7.0 Use Theme_Upgrader
#// @see Theme_Upgrader
#//
def wp_update_theme(theme=None, feedback="", *args_):
    
    _deprecated_function(__FUNCTION__, "3.7.0", "new Theme_Upgrader();")
    if (not php_empty(lambda : feedback)):
        add_filter("update_feedback", feedback)
    # end if
    php_include_file(ABSPATH + "wp-admin/includes/class-wp-upgrader.php", once=False)
    upgrader = php_new_class("Theme_Upgrader", lambda : Theme_Upgrader())
    return upgrader.upgrade(theme)
# end def wp_update_theme
#// 
#// This was once used to display attachment links. Now it is deprecated and stubbed.
#// 
#// @since 2.0.0
#// @deprecated 3.7.0
#// 
#// @param int|bool $id
#//
def the_attachment_links(id=False, *args_):
    
    _deprecated_function(__FUNCTION__, "3.7.0")
# end def the_attachment_links
#// 
#// Displays a screen icon.
#// 
#// @since 2.7.0
#// @deprecated 3.8.0
#//
def screen_icon(*args_):
    
    _deprecated_function(__FUNCTION__, "3.8.0")
    php_print(get_screen_icon())
# end def screen_icon
#// 
#// Retrieves the screen icon (no longer used in 3.8+).
#// 
#// @since 3.2.0
#// @deprecated 3.8.0
#// 
#// @return string An HTML comment explaining that icons are no longer used.
#//
def get_screen_icon(*args_):
    
    _deprecated_function(__FUNCTION__, "3.8.0")
    return "<!-- Screen icons are no longer used as of WordPress 3.8. -->"
# end def get_screen_icon
#// 
#// Deprecated dashboard widget controls.
#// 
#// @since 2.5.0
#// @deprecated 3.8.0
#//
def wp_dashboard_incoming_links_output(*args_):
    
    pass
# end def wp_dashboard_incoming_links_output
#// 
#// Deprecated dashboard secondary output.
#// 
#// @deprecated 3.8.0
#//
def wp_dashboard_secondary_output(*args_):
    
    pass
# end def wp_dashboard_secondary_output
#// 
#// Deprecated dashboard widget controls.
#// 
#// @since 2.7.0
#// @deprecated 3.8.0
#//
def wp_dashboard_incoming_links(*args_):
    
    pass
# end def wp_dashboard_incoming_links
#// 
#// Deprecated dashboard incoming links control.
#// 
#// @deprecated 3.8.0
#//
def wp_dashboard_incoming_links_control(*args_):
    
    pass
# end def wp_dashboard_incoming_links_control
#// 
#// Deprecated dashboard plugins control.
#// 
#// @deprecated 3.8.0
#//
def wp_dashboard_plugins(*args_):
    
    pass
# end def wp_dashboard_plugins
#// 
#// Deprecated dashboard primary control.
#// 
#// @deprecated 3.8.0
#//
def wp_dashboard_primary_control(*args_):
    
    pass
# end def wp_dashboard_primary_control
#// 
#// Deprecated dashboard recent comments control.
#// 
#// @deprecated 3.8.0
#//
def wp_dashboard_recent_comments_control(*args_):
    
    pass
# end def wp_dashboard_recent_comments_control
#// 
#// Deprecated dashboard secondary section.
#// 
#// @deprecated 3.8.0
#//
def wp_dashboard_secondary(*args_):
    
    pass
# end def wp_dashboard_secondary
#// 
#// Deprecated dashboard secondary control.
#// 
#// @deprecated 3.8.0
#//
def wp_dashboard_secondary_control(*args_):
    
    pass
# end def wp_dashboard_secondary_control
#// 
#// Display plugins text for the WordPress news widget.
#// 
#// @since 2.5.0
#// @deprecated 4.8.0
#// 
#// @param string $rss  The RSS feed URL.
#// @param array  $args Array of arguments for this RSS feed.
#//
def wp_dashboard_plugins_output(rss=None, args=Array(), *args_):
    
    _deprecated_function(__FUNCTION__, "4.8.0")
    #// Plugin feeds plus link to install them.
    popular = fetch_feed(args["url"]["popular"])
    plugin_slugs = get_transient("plugin_slugs")
    if False == plugin_slugs:
        plugin_slugs = php_array_keys(get_plugins())
        set_transient("plugin_slugs", plugin_slugs, DAY_IN_SECONDS)
    # end if
    php_print("<ul>")
    for feed in Array(popular):
        if is_wp_error(feed) or (not feed.get_item_quantity()):
            continue
        # end if
        items = feed.get_items(0, 5)
        #// Pick a random, non-installed plugin.
        while True:
            
            if not (True):
                break
            # end if
            #// Abort this foreach loop iteration if there's no plugins left of this type.
            if 0 == php_count(items):
                continue
            # end if
            item_key = php_array_rand(items)
            item = items[item_key]
            link, frag = php_explode("#", item.get_link())
            link = esc_url(link)
            if php_preg_match("|/([^/]+?)/?$|", link, matches):
                slug = matches[1]
            else:
                items[item_key] = None
                continue
            # end if
            #// Is this random plugin's slug already installed? If so, try again.
            reset(plugin_slugs)
            for plugin_slug in plugin_slugs:
                if slug == php_substr(plugin_slug, 0, php_strlen(slug)):
                    items[item_key] = None
                    continue
                # end if
            # end for
            break
        # end while
        #// Eliminate some common badly formed plugin descriptions.
        while True:
            item_key = php_array_rand(items)
            if not (None != item_key and False != php_strpos(items[item_key].get_description(), "Plugin Name:")):
                break
            # end if
            items[item_key] = None
        # end while
        if (not (php_isset(lambda : items[item_key]))):
            continue
        # end if
        raw_title = item.get_title()
        ilink = wp_nonce_url("plugin-install.php?tab=plugin-information&plugin=" + slug, "install-plugin_" + slug) + "&amp;TB_iframe=true&amp;width=600&amp;height=800"
        php_print("<li class=\"dashboard-news-plugin\"><span>" + __("Popular Plugin") + ":</span> " + esc_html(raw_title) + "&nbsp;<a href=\"" + ilink + "\" class=\"thickbox open-plugin-details-modal\" aria-label=\"" + esc_attr(php_sprintf(__("Install %s"), raw_title)) + "\">(" + __("Install") + ")</a></li>")
        feed.__del__()
        feed = None
    # end for
    php_print("</ul>")
# end def wp_dashboard_plugins_output
#// 
#// This was once used to move child posts to a new parent.
#// 
#// @since 2.3.0
#// @deprecated 3.9.0
#// @access private
#// 
#// @param int $old_ID
#// @param int $new_ID
#//
def _relocate_children(old_ID=None, new_ID=None, *args_):
    
    _deprecated_function(__FUNCTION__, "3.9.0")
# end def _relocate_children
#// 
#// Add a top-level menu page in the 'objects' section.
#// 
#// This function takes a capability which will be used to determine whether
#// or not a page is included in the menu.
#// 
#// The function which is hooked in to handle the output of the page must check
#// that the user has the required capability as well.
#// 
#// @since 2.7.0
#// 
#// @deprecated 4.5.0 Use add_menu_page()
#// @see add_menu_page()
#// @global int $_wp_last_object_menu
#// 
#// @param string   $page_title The text to be displayed in the title tags of the page when the menu is selected.
#// @param string   $menu_title The text to be used for the menu.
#// @param string   $capability The capability required for this menu to be displayed to the user.
#// @param string   $menu_slug  The slug name to refer to this menu by (should be unique for this menu).
#// @param callable $function   The function to be called to output the content for this page.
#// @param string   $icon_url   The url to the icon to be used for this menu.
#// @return string The resulting page's hook_suffix.
#//
def add_object_page(page_title=None, menu_title=None, capability=None, menu_slug=None, function="", icon_url="", *args_):
    
    _deprecated_function(__FUNCTION__, "4.5.0", "add_menu_page()")
    global _wp_last_object_menu
    php_check_if_defined("_wp_last_object_menu")
    _wp_last_object_menu += 1
    return add_menu_page(page_title, menu_title, capability, menu_slug, function, icon_url, _wp_last_object_menu)
# end def add_object_page
#// 
#// Add a top-level menu page in the 'utility' section.
#// 
#// This function takes a capability which will be used to determine whether
#// or not a page is included in the menu.
#// 
#// The function which is hooked in to handle the output of the page must check
#// that the user has the required capability as well.
#// 
#// @since 2.7.0
#// 
#// @deprecated 4.5.0 Use add_menu_page()
#// @see add_menu_page()
#// @global int $_wp_last_utility_menu
#// 
#// @param string   $page_title The text to be displayed in the title tags of the page when the menu is selected.
#// @param string   $menu_title The text to be used for the menu.
#// @param string   $capability The capability required for this menu to be displayed to the user.
#// @param string   $menu_slug  The slug name to refer to this menu by (should be unique for this menu).
#// @param callable $function   The function to be called to output the content for this page.
#// @param string   $icon_url   The url to the icon to be used for this menu.
#// @return string The resulting page's hook_suffix.
#//
def add_utility_page(page_title=None, menu_title=None, capability=None, menu_slug=None, function="", icon_url="", *args_):
    
    _deprecated_function(__FUNCTION__, "4.5.0", "add_menu_page()")
    global _wp_last_utility_menu
    php_check_if_defined("_wp_last_utility_menu")
    _wp_last_utility_menu += 1
    return add_menu_page(page_title, menu_title, capability, menu_slug, function, icon_url, _wp_last_utility_menu)
# end def add_utility_page
#// 
#// Disables autocomplete on the 'post' form (Add/Edit Post screens) for WebKit browsers,
#// as they disregard the autocomplete setting on the editor textarea. That can break the editor
#// when the user navigates to it with the browser's Back button. See #28037
#// 
#// Replaced with wp_page_reload_on_back_button_js() that also fixes this problem.
#// 
#// @since 4.0.0
#// @deprecated 4.6.0
#// 
#// @link https://core.trac.wordpress.org/ticket/35852
#// 
#// @global bool $is_safari
#// @global bool $is_chrome
#//
def post_form_autocomplete_off(*args_):
    
    global is_safari,is_chrome
    php_check_if_defined("is_safari","is_chrome")
    _deprecated_function(__FUNCTION__, "4.6.0")
    if is_safari or is_chrome:
        php_print(" autocomplete=\"off\"")
    # end if
# end def post_form_autocomplete_off
#// 
#// Display JavaScript on the page.
#// 
#// @since 3.5.0
#// @deprecated 4.9.0
#//
def options_permalink_add_js(*args_):
    
    php_print("""   <script type=\"text/javascript\">
    jQuery(document).ready(function() {
    jQuery('.permalink-structure input:radio').change(function() {
if ( 'custom' == this.value )
    return;
    jQuery('#permalink_structure').val( this.value );
    });
    jQuery( '#permalink_structure' ).on( 'click input', function() {
    jQuery( '#custom_selection' ).prop( 'checked', true );
    });
    });
    </script>
    """)
# end def options_permalink_add_js
#// 
#// Previous class for list table for privacy data export requests.
#// 
#// @since 4.9.6
#// @deprecated 5.3.0
#//
class WP_Privacy_Data_Export_Requests_Table(WP_Privacy_Data_Export_Requests_List_Table):
    def __init__(self, args=None):
        
        _deprecated_function(__CLASS__, "5.3.0", "WP_Privacy_Data_Export_Requests_List_Table")
        if (not (php_isset(lambda : args["screen"]))) or args["screen"] == "export_personal_data":
            args["screen"] = "export-personal-data"
        # end if
        super().__init__(args)
    # end def __init__
# end class WP_Privacy_Data_Export_Requests_Table
#// 
#// Previous class for list table for privacy data erasure requests.
#// 
#// @since 4.9.6
#// @deprecated 5.3.0
#//
class WP_Privacy_Data_Removal_Requests_Table(WP_Privacy_Data_Removal_Requests_List_Table):
    def __init__(self, args=None):
        
        _deprecated_function(__CLASS__, "5.3.0", "WP_Privacy_Data_Removal_Requests_List_Table")
        if (not (php_isset(lambda : args["screen"]))) or args["screen"] == "remove_personal_data":
            args["screen"] = "erase-personal-data"
        # end if
        super().__init__(args)
    # end def __init__
# end class WP_Privacy_Data_Removal_Requests_Table
#// 
#// Was used to add options for the privacy requests screens before they were separate files.
#// 
#// @since 4.9.8
#// @access private
#// @deprecated 5.3.0
#//
def _wp_privacy_requests_screen_options(*args_):
    
    _deprecated_function(__FUNCTION__, "5.3.0")
# end def _wp_privacy_requests_screen_options
#// 
#// Return the user request object for the specified request ID.
#// 
#// @since 4.9.6
#// @deprecated 5.4.0 Use wp_get_user_request()
#// @see wp_get_user_request()
#// 
#// @param int $request_id The ID of the user request.
#// @return WP_User_Request|false
#//
def wp_get_user_request_data(request_id=None, *args_):
    
    _deprecated_function(__FUNCTION__, "5.4.0", "wp_get_user_request()")
    return wp_get_user_request(request_id)
# end def wp_get_user_request_data
