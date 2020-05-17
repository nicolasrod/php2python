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
#// Screen API: WP_Screen class
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 4.4.0
#// 
#// 
#// Core class used to implement an admin screen API.
#// 
#// @since 3.3.0
#//
class WP_Screen():
    #// 
    #// Any action associated with the screen.
    #// 
    #// 'add' for *-add.php and *-new.php screens. Empty otherwise.
    #// 
    #// @since 3.3.0
    #// @var string
    #//
    action = Array()
    #// 
    #// The base type of the screen.
    #// 
    #// This is typically the same as `$id` but with any post types and taxonomies stripped.
    #// For example, for an `$id` of 'edit-post' the base is 'edit'.
    #// 
    #// @since 3.3.0
    #// @var string
    #//
    base = Array()
    #// 
    #// The number of columns to display. Access with get_columns().
    #// 
    #// @since 3.4.0
    #// @var int
    #//
    columns = 0
    #// 
    #// The unique ID of the screen.
    #// 
    #// @since 3.3.0
    #// @var string
    #//
    id = Array()
    #// 
    #// Which admin the screen is in. network | user | site | false
    #// 
    #// @since 3.5.0
    #// @var string
    #//
    in_admin = Array()
    #// 
    #// Whether the screen is in the network admin.
    #// 
    #// Deprecated. Use in_admin() instead.
    #// 
    #// @since 3.3.0
    #// @deprecated 3.5.0
    #// @var bool
    #//
    is_network = Array()
    #// 
    #// Whether the screen is in the user admin.
    #// 
    #// Deprecated. Use in_admin() instead.
    #// 
    #// @since 3.3.0
    #// @deprecated 3.5.0
    #// @var bool
    #//
    is_user = Array()
    #// 
    #// The base menu parent.
    #// 
    #// This is derived from `$parent_file` by removing the query string and any .php extension.
    #// `$parent_file` values of 'edit.php?post_type=page' and 'edit.php?post_type=post'
    #// have a `$parent_base` of 'edit'.
    #// 
    #// @since 3.3.0
    #// @var string
    #//
    parent_base = Array()
    #// 
    #// The parent_file for the screen per the admin menu system.
    #// 
    #// Some `$parent_file` values are 'edit.php?post_type=page', 'edit.php', and 'options-general.php'.
    #// 
    #// @since 3.3.0
    #// @var string
    #//
    parent_file = Array()
    #// 
    #// The post type associated with the screen, if any.
    #// 
    #// The 'edit.php?post_type=page' screen has a post type of 'page'.
    #// The 'edit-tags.php?taxonomy=$taxonomy&post_type=page' screen has a post type of 'page'.
    #// 
    #// @since 3.3.0
    #// @var string
    #//
    post_type = Array()
    #// 
    #// The taxonomy associated with the screen, if any.
    #// 
    #// The 'edit-tags.php?taxonomy=category' screen has a taxonomy of 'category'.
    #// 
    #// @since 3.3.0
    #// @var string
    #//
    taxonomy = Array()
    #// 
    #// The help tab data associated with the screen, if any.
    #// 
    #// @since 3.3.0
    #// @var array
    #//
    _help_tabs = Array()
    #// 
    #// The help sidebar data associated with screen, if any.
    #// 
    #// @since 3.3.0
    #// @var string
    #//
    _help_sidebar = ""
    #// 
    #// The accessible hidden headings and text associated with the screen, if any.
    #// 
    #// @since 4.4.0
    #// @var array
    #//
    _screen_reader_content = Array()
    #// 
    #// Stores old string-based help.
    #// 
    #// @var array
    #//
    _old_compat_help = Array()
    #// 
    #// The screen options associated with screen, if any.
    #// 
    #// @since 3.3.0
    #// @var array
    #//
    _options = Array()
    #// 
    #// The screen object registry.
    #// 
    #// @since 3.3.0
    #// 
    #// @var array
    #//
    _registry = Array()
    #// 
    #// Stores the result of the public show_screen_options function.
    #// 
    #// @since 3.3.0
    #// @var bool
    #//
    _show_screen_options = Array()
    #// 
    #// Stores the 'screen_settings' section of screen options.
    #// 
    #// @since 3.3.0
    #// @var string
    #//
    _screen_settings = Array()
    #// 
    #// Whether the screen is using the block editor.
    #// 
    #// @since 5.0.0
    #// @var bool
    #//
    is_block_editor = False
    #// 
    #// Fetches a screen object.
    #// 
    #// @since 3.3.0
    #// 
    #// @global string $hook_suffix
    #// 
    #// @param string|WP_Screen $hook_name Optional. The hook name (also known as the hook suffix) used to determine the screen.
    #// Defaults to the current $hook_suffix global.
    #// @return WP_Screen Screen object.
    #//
    @classmethod
    def get(self, hook_name_=""):
        
        
        if type(hook_name_).__name__ == "WP_Screen":
            return hook_name_
        # end if
        post_type_ = None
        taxonomy_ = None
        in_admin_ = False
        action_ = ""
        is_block_editor_ = False
        if hook_name_:
            id_ = hook_name_
        else:
            id_ = PHP_GLOBALS["hook_suffix"]
        # end if
        #// For those pesky meta boxes.
        if hook_name_ and post_type_exists(hook_name_):
            post_type_ = id_
            id_ = "post"
            pass
        else:
            if ".php" == php_substr(id_, -4):
                id_ = php_substr(id_, 0, -4)
            # end if
            if "post-new" == id_ or "link-add" == id_ or "media-new" == id_ or "user-new" == id_:
                id_ = php_substr(id_, 0, -4)
                action_ = "add"
            # end if
        # end if
        if (not post_type_) and hook_name_:
            if "-network" == php_substr(id_, -8):
                id_ = php_substr(id_, 0, -8)
                in_admin_ = "network"
            elif "-user" == php_substr(id_, -5):
                id_ = php_substr(id_, 0, -5)
                in_admin_ = "user"
            # end if
            id_ = sanitize_key(id_)
            if "edit-comments" != id_ and "edit-tags" != id_ and "edit-" == php_substr(id_, 0, 5):
                maybe_ = php_substr(id_, 5)
                if taxonomy_exists(maybe_):
                    id_ = "edit-tags"
                    taxonomy_ = maybe_
                elif post_type_exists(maybe_):
                    id_ = "edit"
                    post_type_ = maybe_
                # end if
            # end if
            if (not in_admin_):
                in_admin_ = "site"
            # end if
        else:
            if php_defined("WP_NETWORK_ADMIN") and WP_NETWORK_ADMIN:
                in_admin_ = "network"
            elif php_defined("WP_USER_ADMIN") and WP_USER_ADMIN:
                in_admin_ = "user"
            else:
                in_admin_ = "site"
            # end if
        # end if
        if "index" == id_:
            id_ = "dashboard"
        elif "front" == id_:
            in_admin_ = False
        # end if
        base_ = id_
        #// If this is the current screen, see if we can be more accurate for post types and taxonomies.
        if (not hook_name_):
            if (php_isset(lambda : PHP_REQUEST["post_type"])):
                post_type_ = PHP_REQUEST["post_type"] if post_type_exists(PHP_REQUEST["post_type"]) else False
            # end if
            if (php_isset(lambda : PHP_REQUEST["taxonomy"])):
                taxonomy_ = PHP_REQUEST["taxonomy"] if taxonomy_exists(PHP_REQUEST["taxonomy"]) else False
            # end if
            for case in Switch(base_):
                if case("post"):
                    if (php_isset(lambda : PHP_REQUEST["post"])) and (php_isset(lambda : PHP_POST["post_ID"])) and php_int(PHP_REQUEST["post"]) != php_int(PHP_POST["post_ID"]):
                        wp_die(__("A post ID mismatch has been detected."), __("Sorry, you are not allowed to edit this item."), 400)
                    elif (php_isset(lambda : PHP_REQUEST["post"])):
                        post_id_ = php_int(PHP_REQUEST["post"])
                    elif (php_isset(lambda : PHP_POST["post_ID"])):
                        post_id_ = php_int(PHP_POST["post_ID"])
                    else:
                        post_id_ = 0
                    # end if
                    if post_id_:
                        post_ = get_post(post_id_)
                        if post_:
                            post_type_ = post_.post_type
                            #// This filter is documented in wp-admin/post.php
                            replace_editor_ = apply_filters("replace_editor", False, post_)
                            if (not replace_editor_):
                                is_block_editor_ = use_block_editor_for_post(post_)
                            # end if
                        # end if
                    # end if
                    break
                # end if
                if case("edit-tags"):
                    pass
                # end if
                if case("term"):
                    if None == post_type_ and is_object_in_taxonomy("post", taxonomy_ if taxonomy_ else "post_tag"):
                        post_type_ = "post"
                    # end if
                    break
                # end if
                if case("upload"):
                    post_type_ = "attachment"
                    break
                # end if
            # end for
        # end if
        for case in Switch(base_):
            if case("post"):
                if None == post_type_:
                    post_type_ = "post"
                # end if
                #// When creating a new post, use the default block editor support value for the post type.
                if php_empty(lambda : post_id_):
                    is_block_editor_ = use_block_editor_for_post_type(post_type_)
                # end if
                id_ = post_type_
                break
            # end if
            if case("edit"):
                if None == post_type_:
                    post_type_ = "post"
                # end if
                id_ += "-" + post_type_
                break
            # end if
            if case("edit-tags"):
                pass
            # end if
            if case("term"):
                if None == taxonomy_:
                    taxonomy_ = "post_tag"
                # end if
                #// The edit-tags ID does not contain the post type. Look for it in the request.
                if None == post_type_:
                    post_type_ = "post"
                    if (php_isset(lambda : PHP_REQUEST["post_type"])) and post_type_exists(PHP_REQUEST["post_type"]):
                        post_type_ = PHP_REQUEST["post_type"]
                    # end if
                # end if
                id_ = "edit-" + taxonomy_
                break
            # end if
        # end for
        if "network" == in_admin_:
            id_ += "-network"
            base_ += "-network"
        elif "user" == in_admin_:
            id_ += "-user"
            base_ += "-user"
        # end if
        if (php_isset(lambda : self._registry[id_])):
            screen_ = self._registry[id_]
            if get_current_screen() == screen_:
                return screen_
            # end if
        else:
            screen_ = php_new_class("WP_Screen", lambda : WP_Screen())
            screen_.id = id_
        # end if
        screen_.base = base_
        screen_.action = action_
        screen_.post_type = php_str(post_type_)
        screen_.taxonomy = php_str(taxonomy_)
        screen_.is_user = "user" == in_admin_
        screen_.is_network = "network" == in_admin_
        screen_.in_admin = in_admin_
        screen_.is_block_editor = is_block_editor_
        self._registry[id_] = screen_
        return screen_
    # end def get
    #// 
    #// Makes the screen object the current screen.
    #// 
    #// @see set_current_screen()
    #// @since 3.3.0
    #// 
    #// @global WP_Screen $current_screen WordPress current screen object.
    #// @global string    $taxnow
    #// @global string    $typenow
    #//
    def set_current_screen(self):
        
        
        global current_screen_
        global taxnow_
        global typenow_
        php_check_if_defined("current_screen_","taxnow_","typenow_")
        current_screen_ = self
        taxnow_ = self.taxonomy
        typenow_ = self.post_type
        #// 
        #// Fires after the current screen has been set.
        #// 
        #// @since 3.0.0
        #// 
        #// @param WP_Screen $current_screen Current WP_Screen object.
        #//
        do_action("current_screen", current_screen_)
    # end def set_current_screen
    #// 
    #// Constructor
    #// 
    #// @since 3.3.0
    #//
    def __init__(self):
        
        
        pass
    # end def __init__
    #// 
    #// Indicates whether the screen is in a particular admin
    #// 
    #// @since 3.5.0
    #// 
    #// @param string $admin The admin to check against (network | user | site).
    #// If empty any of the three admins will result in true.
    #// @return bool True if the screen is in the indicated admin, false otherwise.
    #//
    def in_admin(self, admin_=None):
        if admin_ is None:
            admin_ = None
        # end if
        
        if php_empty(lambda : admin_):
            return php_bool(self.in_admin)
        # end if
        return admin_ == self.in_admin
    # end def in_admin
    #// 
    #// Sets or returns whether the block editor is loading on the current screen.
    #// 
    #// @since 5.0.0
    #// 
    #// @param bool $set Optional. Sets whether the block editor is loading on the current screen or not.
    #// @return bool True if the block editor is being loaded, false otherwise.
    #//
    def is_block_editor(self, set_=None):
        if set_ is None:
            set_ = None
        # end if
        
        if None != set_:
            self.is_block_editor = php_bool(set_)
        # end if
        return self.is_block_editor
    # end def is_block_editor
    #// 
    #// Sets the old string-based contextual help for the screen for backward compatibility.
    #// 
    #// @since 3.3.0
    #// 
    #// @param WP_Screen $screen A screen object.
    #// @param string $help Help text.
    #//
    @classmethod
    def add_old_compat_help(self, screen_=None, help_=None):
        
        
        self._old_compat_help[screen_.id] = help_
    # end def add_old_compat_help
    #// 
    #// Set the parent information for the screen.
    #// 
    #// This is called in admin-header.php after the menu parent for the screen has been determined.
    #// 
    #// @since 3.3.0
    #// 
    #// @param string $parent_file The parent file of the screen. Typically the $parent_file global.
    #//
    def set_parentage(self, parent_file_=None):
        
        
        self.parent_file = parent_file_
        self.parent_base = php_explode("?", parent_file_)
        self.parent_base = php_str_replace(".php", "", self.parent_base)
    # end def set_parentage
    #// 
    #// Adds an option for the screen.
    #// 
    #// Call this in template files after admin.php is loaded and before admin-header.php is loaded
    #// to add screen options.
    #// 
    #// @since 3.3.0
    #// 
    #// @param string $option Option ID
    #// @param mixed $args Option-dependent arguments.
    #//
    def add_option(self, option_=None, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        self._options[option_] = args_
    # end def add_option
    #// 
    #// Remove an option from the screen.
    #// 
    #// @since 3.8.0
    #// 
    #// @param string $option Option ID.
    #//
    def remove_option(self, option_=None):
        
        
        self._options[option_] = None
    # end def remove_option
    #// 
    #// Remove all options from the screen.
    #// 
    #// @since 3.8.0
    #//
    def remove_options(self):
        
        
        self._options = Array()
    # end def remove_options
    #// 
    #// Get the options registered for the screen.
    #// 
    #// @since 3.8.0
    #// 
    #// @return array Options with arguments.
    #//
    def get_options(self):
        
        
        return self._options
    # end def get_options
    #// 
    #// Gets the arguments for an option for the screen.
    #// 
    #// @since 3.3.0
    #// 
    #// @param string $option Option name.
    #// @param string $key    Optional. Specific array key for when the option is an array.
    #// Default false.
    #// @return string The option value if set, null otherwise.
    #//
    def get_option(self, option_=None, key_=None):
        if key_ is None:
            key_ = False
        # end if
        
        if (not (php_isset(lambda : self._options[option_]))):
            return None
        # end if
        if key_:
            if (php_isset(lambda : self._options[option_][key_])):
                return self._options[option_][key_]
            # end if
            return None
        # end if
        return self._options[option_]
    # end def get_option
    #// 
    #// Gets the help tabs registered for the screen.
    #// 
    #// @since 3.4.0
    #// @since 4.4.0 Help tabs are ordered by their priority.
    #// 
    #// @return array Help tabs with arguments.
    #//
    def get_help_tabs(self):
        
        
        help_tabs_ = self._help_tabs
        priorities_ = Array()
        for help_tab_ in help_tabs_:
            if (php_isset(lambda : priorities_[help_tab_["priority"]])):
                priorities_[help_tab_["priority"]][-1] = help_tab_
            else:
                priorities_[help_tab_["priority"]] = Array(help_tab_)
            # end if
        # end for
        ksort(priorities_)
        sorted_ = Array()
        for list_ in priorities_:
            for tab_ in list_:
                sorted_[tab_["id"]] = tab_
            # end for
        # end for
        return sorted_
    # end def get_help_tabs
    #// 
    #// Gets the arguments for a help tab.
    #// 
    #// @since 3.4.0
    #// 
    #// @param string $id Help Tab ID.
    #// @return array Help tab arguments.
    #//
    def get_help_tab(self, id_=None):
        
        
        if (not (php_isset(lambda : self._help_tabs[id_]))):
            return None
        # end if
        return self._help_tabs[id_]
    # end def get_help_tab
    #// 
    #// Add a help tab to the contextual help for the screen.
    #// 
    #// Call this on the `load-$pagenow` hook for the relevant screen,
    #// or fetch the `$current_screen` object, or use get_current_screen()
    #// and then call the method from the object.
    #// 
    #// You may need to filter `$current_screen` using an if or switch statement
    #// to prevent new help tabs from being added to ALL admin screens.
    #// 
    #// @since 3.3.0
    #// @since 4.4.0 The `$priority` argument was added.
    #// 
    #// @param array $args {
    #// Array of arguments used to display the help tab.
    #// 
    #// @type string $title    Title for the tab. Default false.
    #// @type string $id       Tab ID. Must be HTML-safe and should be unique for this menu.
    #// It is NOT allowed to contain any empty spaces. Default false.
    #// @type string $content  Optional. Help tab content in plain text or HTML. Default empty string.
    #// @type string $callback Optional. A callback to generate the tab content. Default false.
    #// @type int    $priority Optional. The priority of the tab, used for ordering. Default 10.
    #// }
    #//
    def add_help_tab(self, args_=None):
        
        
        defaults_ = Array({"title": False, "id": False, "content": "", "callback": False, "priority": 10})
        args_ = wp_parse_args(args_, defaults_)
        args_["id"] = sanitize_html_class(args_["id"])
        #// Ensure we have an ID and title.
        if (not args_["id"]) or (not args_["title"]):
            return
        # end if
        #// Allows for overriding an existing tab with that ID.
        self._help_tabs[args_["id"]] = args_
    # end def add_help_tab
    #// 
    #// Removes a help tab from the contextual help for the screen.
    #// 
    #// @since 3.3.0
    #// 
    #// @param string $id The help tab ID.
    #//
    def remove_help_tab(self, id_=None):
        
        
        self._help_tabs[id_] = None
    # end def remove_help_tab
    #// 
    #// Removes all help tabs from the contextual help for the screen.
    #// 
    #// @since 3.3.0
    #//
    def remove_help_tabs(self):
        
        
        self._help_tabs = Array()
    # end def remove_help_tabs
    #// 
    #// Gets the content from a contextual help sidebar.
    #// 
    #// @since 3.4.0
    #// 
    #// @return string Contents of the help sidebar.
    #//
    def get_help_sidebar(self):
        
        
        return self._help_sidebar
    # end def get_help_sidebar
    #// 
    #// Add a sidebar to the contextual help for the screen.
    #// 
    #// Call this in template files after admin.php is loaded and before admin-header.php is loaded
    #// to add a sidebar to the contextual help.
    #// 
    #// @since 3.3.0
    #// 
    #// @param string $content Sidebar content in plain text or HTML.
    #//
    def set_help_sidebar(self, content_=None):
        
        
        self._help_sidebar = content_
    # end def set_help_sidebar
    #// 
    #// Gets the number of layout columns the user has selected.
    #// 
    #// The layout_columns option controls the max number and default number of
    #// columns. This method returns the number of columns within that range selected
    #// by the user via Screen Options. If no selection has been made, the default
    #// provisioned in layout_columns is returned. If the screen does not support
    #// selecting the number of layout columns, 0 is returned.
    #// 
    #// @since 3.4.0
    #// 
    #// @return int Number of columns to display.
    #//
    def get_columns(self):
        
        
        return self.columns
    # end def get_columns
    #// 
    #// Get the accessible hidden headings and text used in the screen.
    #// 
    #// @since 4.4.0
    #// 
    #// @see set_screen_reader_content() For more information on the array format.
    #// 
    #// @return array An associative array of screen reader text strings.
    #//
    def get_screen_reader_content(self):
        
        
        return self._screen_reader_content
    # end def get_screen_reader_content
    #// 
    #// Get a screen reader text string.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $key Screen reader text array named key.
    #// @return string Screen reader text string.
    #//
    def get_screen_reader_text(self, key_=None):
        
        
        if (not (php_isset(lambda : self._screen_reader_content[key_]))):
            return None
        # end if
        return self._screen_reader_content[key_]
    # end def get_screen_reader_text
    #// 
    #// Add accessible hidden headings and text for the screen.
    #// 
    #// @since 4.4.0
    #// 
    #// @param array $content {
    #// An associative array of screen reader text strings.
    #// 
    #// @type string $heading_views      Screen reader text for the filter links heading.
    #// Default 'Filter items list'.
    #// @type string $heading_pagination Screen reader text for the pagination heading.
    #// Default 'Items list navigation'.
    #// @type string $heading_list       Screen reader text for the items list heading.
    #// Default 'Items list'.
    #// }
    #//
    def set_screen_reader_content(self, content_=None):
        if content_ is None:
            content_ = Array()
        # end if
        
        defaults_ = Array({"heading_views": __("Filter items list"), "heading_pagination": __("Items list navigation"), "heading_list": __("Items list")})
        content_ = wp_parse_args(content_, defaults_)
        self._screen_reader_content = content_
    # end def set_screen_reader_content
    #// 
    #// Remove all the accessible hidden headings and text for the screen.
    #// 
    #// @since 4.4.0
    #//
    def remove_screen_reader_content(self):
        
        
        self._screen_reader_content = Array()
    # end def remove_screen_reader_content
    #// 
    #// Render the screen's help section.
    #// 
    #// This will trigger the deprecated filters for backward compatibility.
    #// 
    #// @since 3.3.0
    #// 
    #// @global string $screen_layout_columns
    #//
    def render_screen_meta(self):
        
        global PHP_GLOBALS
        #// 
        #// Filters the legacy contextual help list.
        #// 
        #// @since 2.7.0
        #// @deprecated 3.3.0 Use {@see get_current_screen()->add_help_tab()} or
        #// {@see get_current_screen()->remove_help_tab()} instead.
        #// 
        #// @param array     $old_compat_help Old contextual help.
        #// @param WP_Screen $this            Current WP_Screen instance.
        #//
        self._old_compat_help = apply_filters_deprecated("contextual_help_list", Array(self._old_compat_help, self), "3.3.0", "get_current_screen()->add_help_tab(), get_current_screen()->remove_help_tab()")
        old_help_ = self._old_compat_help[self.id] if (php_isset(lambda : self._old_compat_help[self.id])) else ""
        #// 
        #// Filters the legacy contextual help text.
        #// 
        #// @since 2.7.0
        #// @deprecated 3.3.0 Use {@see get_current_screen()->add_help_tab()} or
        #// {@see get_current_screen()->remove_help_tab()} instead.
        #// 
        #// @param string    $old_help  Help text that appears on the screen.
        #// @param string    $screen_id Screen ID.
        #// @param WP_Screen $this      Current WP_Screen instance.
        #//
        old_help_ = apply_filters_deprecated("contextual_help", Array(old_help_, self.id, self), "3.3.0", "get_current_screen()->add_help_tab(), get_current_screen()->remove_help_tab()")
        #// Default help only if there is no old-style block of text and no new-style help tabs.
        if php_empty(lambda : old_help_) and (not self.get_help_tabs()):
            #// 
            #// Filters the default legacy contextual help text.
            #// 
            #// @since 2.8.0
            #// @deprecated 3.3.0 Use {@see get_current_screen()->add_help_tab()} or
            #// {@see get_current_screen()->remove_help_tab()} instead.
            #// 
            #// @param string $old_help_default Default contextual help text.
            #//
            default_help_ = apply_filters_deprecated("default_contextual_help", Array(""), "3.3.0", "get_current_screen()->add_help_tab(), get_current_screen()->remove_help_tab()")
            if default_help_:
                old_help_ = "<p>" + default_help_ + "</p>"
            # end if
        # end if
        if old_help_:
            self.add_help_tab(Array({"id": "old-contextual-help", "title": __("Overview"), "content": old_help_}))
        # end if
        help_sidebar_ = self.get_help_sidebar()
        help_class_ = "hidden"
        if (not help_sidebar_):
            help_class_ += " no-sidebar"
        # end if
        pass
        php_print("     <div id=\"screen-meta\" class=\"metabox-prefs\">\n\n            <div id=\"contextual-help-wrap\" class=\"")
        php_print(esc_attr(help_class_))
        php_print("\" tabindex=\"-1\" aria-label=\"")
        esc_attr_e("Contextual Help Tab")
        php_print("""\">
        <div id=\"contextual-help-back\"></div>
        <div id=\"contextual-help-columns\">
        <div class=\"contextual-help-tabs\">
        <ul>
        """)
        class_ = " class=\"active\""
        for tab_ in self.get_help_tabs():
            link_id_ = str("tab-link-") + str(tab_["id"])
            panel_id_ = str("tab-panel-") + str(tab_["id"])
            php_print("\n                           <li id=\"")
            php_print(esc_attr(link_id_))
            php_print("\"")
            php_print(class_)
            php_print(">\n                              <a href=\"")
            php_print(esc_url(str("#") + str(panel_id_)))
            php_print("\" aria-controls=\"")
            php_print(esc_attr(panel_id_))
            php_print("\">\n                                    ")
            php_print(esc_html(tab_["title"]))
            php_print("                             </a>\n                          </li>\n                         ")
            class_ = ""
        # end for
        php_print("""                       </ul>
        </div>
        """)
        if help_sidebar_:
            php_print("                 <div class=\"contextual-help-sidebar\">\n                       ")
            php_print(help_sidebar_)
            php_print("                 </div>\n                    ")
        # end if
        php_print("\n                   <div class=\"contextual-help-tabs-wrap\">\n                     ")
        classes_ = "help-tab-content active"
        for tab_ in self.get_help_tabs():
            panel_id_ = str("tab-panel-") + str(tab_["id"])
            php_print("\n                           <div id=\"")
            php_print(esc_attr(panel_id_))
            php_print("\" class=\"")
            php_print(classes_)
            php_print("\">\n                                ")
            #// Print tab content.
            php_print(tab_["content"])
            #// If it exists, fire tab callback.
            if (not php_empty(lambda : tab_["callback"])):
                call_user_func_array(tab_["callback"], Array(self, tab_))
            # end if
            php_print("                         </div>\n                            ")
            classes_ = "help-tab-content"
        # end for
        php_print("""                   </div>
        </div>
        </div>
        """)
        #// Setup layout columns.
        #// 
        #// Filters the array of screen layout columns.
        #// 
        #// This hook provides back-compat for plugins using the back-compat
        #// Filters instead of add_screen_option().
        #// 
        #// @since 2.8.0
        #// 
        #// @param array     $empty_columns Empty array.
        #// @param string    $screen_id     Screen ID.
        #// @param WP_Screen $this          Current WP_Screen instance.
        #//
        columns_ = apply_filters("screen_layout_columns", Array(), self.id, self)
        if (not php_empty(lambda : columns_)) and (php_isset(lambda : columns_[self.id])):
            self.add_option("layout_columns", Array({"max": columns_[self.id]}))
        # end if
        if self.get_option("layout_columns"):
            self.columns = php_int(get_user_option(str("screen_layout_") + str(self.id)))
            if (not self.columns) and self.get_option("layout_columns", "default"):
                self.columns = self.get_option("layout_columns", "default")
            # end if
        # end if
        PHP_GLOBALS["screen_layout_columns"] = self.columns
        #// Set the global for back-compat.
        #// Add screen options.
        if self.show_screen_options():
            self.render_screen_options()
        # end if
        php_print("     </div>\n        ")
        if (not self.get_help_tabs()) and (not self.show_screen_options()):
            return
        # end if
        php_print("     <div id=\"screen-meta-links\">\n        ")
        if self.show_screen_options():
            php_print("         <div id=\"screen-options-link-wrap\" class=\"hide-if-no-js screen-meta-toggle\">\n          <button type=\"button\" id=\"show-settings-link\" class=\"button show-settings\" aria-controls=\"screen-options-wrap\" aria-expanded=\"false\">")
            _e("Screen Options")
            php_print("</button>\n          </div>\n            ")
        # end if
        if self.get_help_tabs():
            php_print("         <div id=\"contextual-help-link-wrap\" class=\"hide-if-no-js screen-meta-toggle\">\n         <button type=\"button\" id=\"contextual-help-link\" class=\"button show-settings\" aria-controls=\"contextual-help-wrap\" aria-expanded=\"false\">")
            _e("Help")
            php_print("</button>\n          </div>\n        ")
        # end if
        php_print("     </div>\n        ")
    # end def render_screen_meta
    #// 
    #// @global array $wp_meta_boxes
    #// 
    #// @return bool
    #//
    def show_screen_options(self):
        
        
        global wp_meta_boxes_
        php_check_if_defined("wp_meta_boxes_")
        if php_is_bool(self._show_screen_options):
            return self._show_screen_options
        # end if
        columns_ = get_column_headers(self)
        show_screen_ = (not php_empty(lambda : wp_meta_boxes_[self.id])) or columns_ or self.get_option("per_page")
        self._screen_settings = ""
        if "post" == self.base:
            expand_ = "<fieldset class=\"editor-expand hidden\"><legend>" + __("Additional settings") + "</legend><label for=\"editor-expand-toggle\">"
            expand_ += "<input type=\"checkbox\" id=\"editor-expand-toggle\"" + checked(get_user_setting("editor_expand", "on"), "on", False) + " />"
            expand_ += __("Enable full-height editor and distraction-free functionality.") + "</label></fieldset>"
            self._screen_settings = expand_
        # end if
        #// 
        #// Filters the screen settings text displayed in the Screen Options tab.
        #// 
        #// This filter is currently only used on the Widgets screen to enable
        #// accessibility mode.
        #// 
        #// @since 3.0.0
        #// 
        #// @param string    $screen_settings Screen settings.
        #// @param WP_Screen $this            WP_Screen object.
        #//
        self._screen_settings = apply_filters("screen_settings", self._screen_settings, self)
        if self._screen_settings or self._options:
            show_screen_ = True
        # end if
        #// 
        #// Filters whether to show the Screen Options tab.
        #// 
        #// @since 3.2.0
        #// 
        #// @param bool      $show_screen Whether to show Screen Options tab.
        #// Default true.
        #// @param WP_Screen $this        Current WP_Screen instance.
        #//
        self._show_screen_options = apply_filters("screen_options_show_screen", show_screen_, self)
        return self._show_screen_options
    # end def show_screen_options
    #// 
    #// Render the screen options tab.
    #// 
    #// @since 3.3.0
    #// 
    #// @param array $options {
    #// @type bool $wrap  Whether the screen-options-wrap div will be included. Defaults to true.
    #// }
    #//
    def render_screen_options(self, options_=None):
        if options_ is None:
            options_ = Array()
        # end if
        
        options_ = wp_parse_args(options_, Array({"wrap": True}))
        wrapper_start_ = ""
        wrapper_end_ = ""
        form_start_ = ""
        form_end_ = ""
        #// Output optional wrapper.
        if options_["wrap"]:
            wrapper_start_ = "<div id=\"screen-options-wrap\" class=\"hidden\" tabindex=\"-1\" aria-label=\"" + esc_attr__("Screen Options Tab") + "\">"
            wrapper_end_ = "</div>"
        # end if
        #// Don't output the form and nonce for the widgets accessibility mode links.
        if "widgets" != self.base:
            form_start_ = "\n<form id='adv-settings' method='post'>\n"
            form_end_ = "\n" + wp_nonce_field("screen-options-nonce", "screenoptionnonce", False, False) + "\n</form>\n"
        # end if
        php_print(wrapper_start_ + form_start_)
        self.render_meta_boxes_preferences()
        self.render_list_table_columns_preferences()
        self.render_screen_layout()
        self.render_per_page_options()
        self.render_view_mode()
        php_print(self._screen_settings)
        #// 
        #// Filters whether to show the Screen Options submit button.
        #// 
        #// @since 4.4.0
        #// 
        #// @param bool      $show_button Whether to show Screen Options submit button.
        #// Default false.
        #// @param WP_Screen $this        Current WP_Screen instance.
        #//
        show_button_ = apply_filters("screen_options_show_submit", False, self)
        if show_button_:
            submit_button(__("Apply"), "primary", "screen-options-apply", True)
        # end if
        php_print(form_end_ + wrapper_end_)
    # end def render_screen_options
    #// 
    #// Render the meta boxes preferences.
    #// 
    #// @since 4.4.0
    #// 
    #// @global array $wp_meta_boxes
    #//
    def render_meta_boxes_preferences(self):
        
        
        global wp_meta_boxes_
        php_check_if_defined("wp_meta_boxes_")
        if (not (php_isset(lambda : wp_meta_boxes_[self.id]))):
            return
        # end if
        php_print("     <fieldset class=\"metabox-prefs\">\n        <legend>")
        _e("Boxes")
        php_print("</legend>\n      ")
        meta_box_prefs(self)
        if "dashboard" == self.id and has_action("welcome_panel") and current_user_can("edit_theme_options"):
            if (php_isset(lambda : PHP_REQUEST["welcome"])):
                welcome_checked_ = 0 if php_empty(lambda : PHP_REQUEST["welcome"]) else 1
                update_user_meta(get_current_user_id(), "show_welcome_panel", welcome_checked_)
            else:
                welcome_checked_ = get_user_meta(get_current_user_id(), "show_welcome_panel", True)
                if 2 == welcome_checked_ and wp_get_current_user().user_email != get_option("admin_email"):
                    welcome_checked_ = False
                # end if
            # end if
            php_print("<label for=\"wp_welcome_panel-hide\">")
            php_print("<input type=\"checkbox\" id=\"wp_welcome_panel-hide\"" + checked(php_bool(welcome_checked_), True, False) + " />")
            php_print(_x("Welcome", "Welcome panel") + "</label>\n")
        # end if
        php_print("     </fieldset>\n       ")
    # end def render_meta_boxes_preferences
    #// 
    #// Render the list table columns preferences.
    #// 
    #// @since 4.4.0
    #//
    def render_list_table_columns_preferences(self):
        
        
        columns_ = get_column_headers(self)
        hidden_ = get_hidden_columns(self)
        if (not columns_):
            return
        # end if
        legend_ = columns_["_title"] if (not php_empty(lambda : columns_["_title"])) else __("Columns")
        php_print("     <fieldset class=\"metabox-prefs\">\n        <legend>")
        php_print(legend_)
        php_print("</legend>\n      ")
        special_ = Array("_title", "cb", "comment", "media", "name", "title", "username", "blogname")
        for column_,title_ in columns_:
            #// Can't hide these for they are special.
            if php_in_array(column_, special_):
                continue
            # end if
            if php_empty(lambda : title_):
                continue
            # end if
            #// 
            #// The Comments column uses HTML in the display name with some screen
            #// reader text. Make sure to strip tags from the Comments column
            #// title and any other custom column title plugins might add.
            #//
            title_ = wp_strip_all_tags(title_)
            id_ = str(column_) + str("-hide")
            php_print("<label>")
            php_print("<input class=\"hide-column-tog\" name=\"" + id_ + "\" type=\"checkbox\" id=\"" + id_ + "\" value=\"" + column_ + "\"" + checked((not php_in_array(column_, hidden_)), True, False) + " />")
            php_print(str(title_) + str("</label>\n"))
        # end for
        php_print("     </fieldset>\n       ")
    # end def render_list_table_columns_preferences
    #// 
    #// Render the option for number of columns on the page
    #// 
    #// @since 3.3.0
    #//
    def render_screen_layout(self):
        
        
        if (not self.get_option("layout_columns")):
            return
        # end if
        screen_layout_columns_ = self.get_columns()
        num_ = self.get_option("layout_columns", "max")
        php_print("     <fieldset class='columns-prefs'>\n      <legend class=\"screen-layout\">")
        _e("Layout")
        php_print("</legend>\n      ")
        i_ = 1
        while i_ <= num_:
            
            php_print("         <label class=\"columns-prefs-")
            php_print(i_)
            php_print("\">\n            <input type='radio' name='screen_columns' value='")
            php_print(esc_attr(i_))
            php_print("' ")
            checked(screen_layout_columns_, i_)
            php_print(" />\n            ")
            printf(_n("%s column", "%s columns", i_), number_format_i18n(i_))
            php_print("         </label>\n      ")
            i_ += 1
        # end while
        php_print("     </fieldset>\n       ")
    # end def render_screen_layout
    #// 
    #// Render the items per page option
    #// 
    #// @since 3.3.0
    #//
    def render_per_page_options(self):
        
        
        if None == self.get_option("per_page"):
            return
        # end if
        per_page_label_ = self.get_option("per_page", "label")
        if None == per_page_label_:
            per_page_label_ = __("Number of items per page:")
        # end if
        option_ = self.get_option("per_page", "option")
        if (not option_):
            option_ = php_str_replace("-", "_", str(self.id) + str("_per_page"))
        # end if
        per_page_ = php_int(get_user_option(option_))
        if php_empty(lambda : per_page_) or per_page_ < 1:
            per_page_ = self.get_option("per_page", "default")
            if (not per_page_):
                per_page_ = 20
            # end if
        # end if
        if "edit_comments_per_page" == option_:
            comment_status_ = PHP_REQUEST["comment_status"] if (php_isset(lambda : PHP_REQUEST["comment_status"])) else "all"
            #// This filter is documented in wp-admin/includes/class-wp-comments-list-table.php
            per_page_ = apply_filters("comments_per_page", per_page_, comment_status_)
        elif "categories_per_page" == option_:
            #// This filter is documented in wp-admin/includes/class-wp-terms-list-table.php
            per_page_ = apply_filters("edit_categories_per_page", per_page_)
        else:
            #// This filter is documented in wp-admin/includes/class-wp-list-table.php
            per_page_ = apply_filters(str(option_), per_page_)
        # end if
        #// Back compat.
        if (php_isset(lambda : self.post_type)):
            #// This filter is documented in wp-admin/includes/post.php
            per_page_ = apply_filters("edit_posts_per_page", per_page_, self.post_type)
        # end if
        #// This needs a submit button.
        add_filter("screen_options_show_submit", "__return_true")
        php_print("     <fieldset class=\"screen-options\">\n       <legend>")
        _e("Pagination")
        php_print("</legend>\n          ")
        if per_page_label_:
            php_print("             <label for=\"")
            php_print(esc_attr(option_))
            php_print("\">")
            php_print(per_page_label_)
            php_print("</label>\n               <input type=\"number\" step=\"1\" min=\"1\" max=\"999\" class=\"screen-per-page\" name=\"wp_screen_options[value]\"\n                   id=\"")
            php_print(esc_attr(option_))
            php_print("\" maxlength=\"3\"\n                 value=\"")
            php_print(esc_attr(per_page_))
            php_print("\" />\n          ")
        # end if
        php_print("             <input type=\"hidden\" name=\"wp_screen_options[option]\" value=\"")
        php_print(esc_attr(option_))
        php_print("\" />\n      </fieldset>\n       ")
    # end def render_per_page_options
    #// 
    #// Render the list table view mode preferences.
    #// 
    #// @since 4.4.0
    #// 
    #// @global string $mode List table view mode.
    #//
    def render_view_mode(self):
        
        
        screen_ = get_current_screen()
        #// Currently only enabled for posts lists.
        if "edit" != screen_.base:
            return
        # end if
        view_mode_post_types_ = get_post_types(Array({"hierarchical": False, "show_ui": True}))
        #// 
        #// Filters the post types that have different view mode options.
        #// 
        #// @since 4.4.0
        #// 
        #// @param string[] $view_mode_post_types Array of post types that can change view modes.
        #// Default non-hierarchical post types with show_ui on.
        #//
        view_mode_post_types_ = apply_filters("view_mode_post_types", view_mode_post_types_)
        if (not php_in_array(self.post_type, view_mode_post_types_)):
            return
        # end if
        global mode_
        php_check_if_defined("mode_")
        #// This needs a submit button.
        add_filter("screen_options_show_submit", "__return_true")
        php_print("     <fieldset class=\"metabox-prefs view-mode\">\n      <legend>")
        _e("View Mode")
        php_print("</legend>\n              <label for=\"list-view-mode\">\n                    <input id=\"list-view-mode\" type=\"radio\" name=\"mode\" value=\"list\" ")
        checked("list", mode_)
        php_print(" />\n                    ")
        _e("List View")
        php_print("             </label>\n              <label for=\"excerpt-view-mode\">\n                 <input id=\"excerpt-view-mode\" type=\"radio\" name=\"mode\" value=\"excerpt\" ")
        checked("excerpt", mode_)
        php_print(" />\n                    ")
        _e("Excerpt View")
        php_print("             </label>\n      </fieldset>\n       ")
    # end def render_view_mode
    #// 
    #// Render screen reader text.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $key The screen reader text array named key.
    #// @param string $tag Optional. The HTML tag to wrap the screen reader text. Default h2.
    #//
    def render_screen_reader_content(self, key_="", tag_="h2"):
        
        
        if (not (php_isset(lambda : self._screen_reader_content[key_]))):
            return
        # end if
        php_print(str("<") + str(tag_) + str(" class='screen-reader-text'>") + self._screen_reader_content[key_] + str("</") + str(tag_) + str(">"))
    # end def render_screen_reader_content
# end class WP_Screen
