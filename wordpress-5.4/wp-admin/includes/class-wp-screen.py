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
    action = Array()
    base = Array()
    columns = 0
    id = Array()
    in_admin = Array()
    is_network = Array()
    is_user = Array()
    parent_base = Array()
    parent_file = Array()
    post_type = Array()
    taxonomy = Array()
    _help_tabs = Array()
    _help_sidebar = ""
    _screen_reader_content = Array()
    _old_compat_help = Array()
    _options = Array()
    _registry = Array()
    _show_screen_options = Array()
    _screen_settings = Array()
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
    def get(self, hook_name=""):
        
        if type(hook_name).__name__ == "WP_Screen":
            return hook_name
        # end if
        post_type = None
        taxonomy = None
        in_admin = False
        action = ""
        is_block_editor = False
        if hook_name:
            id = hook_name
        else:
            id = PHP_GLOBALS["hook_suffix"]
        # end if
        #// For those pesky meta boxes.
        if hook_name and post_type_exists(hook_name):
            post_type = id
            id = "post"
            pass
        else:
            if ".php" == php_substr(id, -4):
                id = php_substr(id, 0, -4)
            # end if
            if "post-new" == id or "link-add" == id or "media-new" == id or "user-new" == id:
                id = php_substr(id, 0, -4)
                action = "add"
            # end if
        # end if
        if (not post_type) and hook_name:
            if "-network" == php_substr(id, -8):
                id = php_substr(id, 0, -8)
                in_admin = "network"
            elif "-user" == php_substr(id, -5):
                id = php_substr(id, 0, -5)
                in_admin = "user"
            # end if
            id = sanitize_key(id)
            if "edit-comments" != id and "edit-tags" != id and "edit-" == php_substr(id, 0, 5):
                maybe = php_substr(id, 5)
                if taxonomy_exists(maybe):
                    id = "edit-tags"
                    taxonomy = maybe
                elif post_type_exists(maybe):
                    id = "edit"
                    post_type = maybe
                # end if
            # end if
            if (not in_admin):
                in_admin = "site"
            # end if
        else:
            if php_defined("WP_NETWORK_ADMIN") and WP_NETWORK_ADMIN:
                in_admin = "network"
            elif php_defined("WP_USER_ADMIN") and WP_USER_ADMIN:
                in_admin = "user"
            else:
                in_admin = "site"
            # end if
        # end if
        if "index" == id:
            id = "dashboard"
        elif "front" == id:
            in_admin = False
        # end if
        base = id
        #// If this is the current screen, see if we can be more accurate for post types and taxonomies.
        if (not hook_name):
            if (php_isset(lambda : PHP_REQUEST["post_type"])):
                post_type = PHP_REQUEST["post_type"] if post_type_exists(PHP_REQUEST["post_type"]) else False
            # end if
            if (php_isset(lambda : PHP_REQUEST["taxonomy"])):
                taxonomy = PHP_REQUEST["taxonomy"] if taxonomy_exists(PHP_REQUEST["taxonomy"]) else False
            # end if
            for case in Switch(base):
                if case("post"):
                    if (php_isset(lambda : PHP_REQUEST["post"])) and (php_isset(lambda : PHP_POST["post_ID"])) and int(PHP_REQUEST["post"]) != int(PHP_POST["post_ID"]):
                        wp_die(__("A post ID mismatch has been detected."), __("Sorry, you are not allowed to edit this item."), 400)
                    elif (php_isset(lambda : PHP_REQUEST["post"])):
                        post_id = int(PHP_REQUEST["post"])
                    elif (php_isset(lambda : PHP_POST["post_ID"])):
                        post_id = int(PHP_POST["post_ID"])
                    else:
                        post_id = 0
                    # end if
                    if post_id:
                        post = get_post(post_id)
                        if post:
                            post_type = post.post_type
                            #// This filter is documented in wp-admin/post.php
                            replace_editor = apply_filters("replace_editor", False, post)
                            if (not replace_editor):
                                is_block_editor = use_block_editor_for_post(post)
                            # end if
                        # end if
                    # end if
                    break
                # end if
                if case("edit-tags"):
                    pass
                # end if
                if case("term"):
                    if None == post_type and is_object_in_taxonomy("post", taxonomy if taxonomy else "post_tag"):
                        post_type = "post"
                    # end if
                    break
                # end if
                if case("upload"):
                    post_type = "attachment"
                    break
                # end if
            # end for
        # end if
        for case in Switch(base):
            if case("post"):
                if None == post_type:
                    post_type = "post"
                # end if
                #// When creating a new post, use the default block editor support value for the post type.
                if php_empty(lambda : post_id):
                    is_block_editor = use_block_editor_for_post_type(post_type)
                # end if
                id = post_type
                break
            # end if
            if case("edit"):
                if None == post_type:
                    post_type = "post"
                # end if
                id += "-" + post_type
                break
            # end if
            if case("edit-tags"):
                pass
            # end if
            if case("term"):
                if None == taxonomy:
                    taxonomy = "post_tag"
                # end if
                #// The edit-tags ID does not contain the post type. Look for it in the request.
                if None == post_type:
                    post_type = "post"
                    if (php_isset(lambda : PHP_REQUEST["post_type"])) and post_type_exists(PHP_REQUEST["post_type"]):
                        post_type = PHP_REQUEST["post_type"]
                    # end if
                # end if
                id = "edit-" + taxonomy
                break
            # end if
        # end for
        if "network" == in_admin:
            id += "-network"
            base += "-network"
        elif "user" == in_admin:
            id += "-user"
            base += "-user"
        # end if
        if (php_isset(lambda : self._registry[id])):
            screen = self._registry[id]
            if get_current_screen() == screen:
                return screen
            # end if
        else:
            screen = php_new_class("WP_Screen", lambda : WP_Screen())
            screen.id = id
        # end if
        screen.base = base
        screen.action = action
        screen.post_type = str(post_type)
        screen.taxonomy = str(taxonomy)
        screen.is_user = "user" == in_admin
        screen.is_network = "network" == in_admin
        screen.in_admin = in_admin
        screen.is_block_editor = is_block_editor
        self._registry[id] = screen
        return screen
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
        
        global current_screen,taxnow,typenow
        php_check_if_defined("current_screen","taxnow","typenow")
        current_screen = self
        taxnow = self.taxonomy
        typenow = self.post_type
        #// 
        #// Fires after the current screen has been set.
        #// 
        #// @since 3.0.0
        #// 
        #// @param WP_Screen $current_screen Current WP_Screen object.
        #//
        do_action("current_screen", current_screen)
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
    def in_admin(self, admin=None):
        
        if php_empty(lambda : admin):
            return bool(self.in_admin)
        # end if
        return admin == self.in_admin
    # end def in_admin
    #// 
    #// Sets or returns whether the block editor is loading on the current screen.
    #// 
    #// @since 5.0.0
    #// 
    #// @param bool $set Optional. Sets whether the block editor is loading on the current screen or not.
    #// @return bool True if the block editor is being loaded, false otherwise.
    #//
    def is_block_editor(self, set=None):
        
        if None != set:
            self.is_block_editor = bool(set)
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
    def add_old_compat_help(self, screen=None, help=None):
        
        self._old_compat_help[screen.id] = help
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
    def set_parentage(self, parent_file=None):
        
        self.parent_file = parent_file
        self.parent_base = php_explode("?", parent_file)
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
    def add_option(self, option=None, args=Array()):
        
        self._options[option] = args
    # end def add_option
    #// 
    #// Remove an option from the screen.
    #// 
    #// @since 3.8.0
    #// 
    #// @param string $option Option ID.
    #//
    def remove_option(self, option=None):
        
        self._options[option] = None
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
    def get_option(self, option=None, key=False):
        
        if (not (php_isset(lambda : self._options[option]))):
            return None
        # end if
        if key:
            if (php_isset(lambda : self._options[option][key])):
                return self._options[option][key]
            # end if
            return None
        # end if
        return self._options[option]
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
        
        help_tabs = self._help_tabs
        priorities = Array()
        for help_tab in help_tabs:
            if (php_isset(lambda : priorities[help_tab["priority"]])):
                priorities[help_tab["priority"]][-1] = help_tab
            else:
                priorities[help_tab["priority"]] = Array(help_tab)
            # end if
        # end for
        ksort(priorities)
        sorted = Array()
        for list in priorities:
            for tab in list:
                sorted[tab["id"]] = tab
            # end for
        # end for
        return sorted
    # end def get_help_tabs
    #// 
    #// Gets the arguments for a help tab.
    #// 
    #// @since 3.4.0
    #// 
    #// @param string $id Help Tab ID.
    #// @return array Help tab arguments.
    #//
    def get_help_tab(self, id=None):
        
        if (not (php_isset(lambda : self._help_tabs[id]))):
            return None
        # end if
        return self._help_tabs[id]
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
    def add_help_tab(self, args=None):
        
        defaults = Array({"title": False, "id": False, "content": "", "callback": False, "priority": 10})
        args = wp_parse_args(args, defaults)
        args["id"] = sanitize_html_class(args["id"])
        #// Ensure we have an ID and title.
        if (not args["id"]) or (not args["title"]):
            return
        # end if
        #// Allows for overriding an existing tab with that ID.
        self._help_tabs[args["id"]] = args
    # end def add_help_tab
    #// 
    #// Removes a help tab from the contextual help for the screen.
    #// 
    #// @since 3.3.0
    #// 
    #// @param string $id The help tab ID.
    #//
    def remove_help_tab(self, id=None):
        
        self._help_tabs[id] = None
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
    def set_help_sidebar(self, content=None):
        
        self._help_sidebar = content
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
    def get_screen_reader_text(self, key=None):
        
        if (not (php_isset(lambda : self._screen_reader_content[key]))):
            return None
        # end if
        return self._screen_reader_content[key]
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
    def set_screen_reader_content(self, content=Array()):
        
        defaults = Array({"heading_views": __("Filter items list"), "heading_pagination": __("Items list navigation"), "heading_list": __("Items list")})
        content = wp_parse_args(content, defaults)
        self._screen_reader_content = content
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
        old_help = self._old_compat_help[self.id] if (php_isset(lambda : self._old_compat_help[self.id])) else ""
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
        old_help = apply_filters_deprecated("contextual_help", Array(old_help, self.id, self), "3.3.0", "get_current_screen()->add_help_tab(), get_current_screen()->remove_help_tab()")
        #// Default help only if there is no old-style block of text and no new-style help tabs.
        if php_empty(lambda : old_help) and (not self.get_help_tabs()):
            #// 
            #// Filters the default legacy contextual help text.
            #// 
            #// @since 2.8.0
            #// @deprecated 3.3.0 Use {@see get_current_screen()->add_help_tab()} or
            #// {@see get_current_screen()->remove_help_tab()} instead.
            #// 
            #// @param string $old_help_default Default contextual help text.
            #//
            default_help = apply_filters_deprecated("default_contextual_help", Array(""), "3.3.0", "get_current_screen()->add_help_tab(), get_current_screen()->remove_help_tab()")
            if default_help:
                old_help = "<p>" + default_help + "</p>"
            # end if
        # end if
        if old_help:
            self.add_help_tab(Array({"id": "old-contextual-help", "title": __("Overview"), "content": old_help}))
        # end if
        help_sidebar = self.get_help_sidebar()
        help_class = "hidden"
        if (not help_sidebar):
            help_class += " no-sidebar"
        # end if
        pass
        php_print("     <div id=\"screen-meta\" class=\"metabox-prefs\">\n\n            <div id=\"contextual-help-wrap\" class=\"")
        php_print(esc_attr(help_class))
        php_print("\" tabindex=\"-1\" aria-label=\"")
        esc_attr_e("Contextual Help Tab")
        php_print("""\">
        <div id=\"contextual-help-back\"></div>
        <div id=\"contextual-help-columns\">
        <div class=\"contextual-help-tabs\">
        <ul>
        """)
        class_ = " class=\"active\""
        for tab in self.get_help_tabs():
            link_id = str("tab-link-") + str(tab["id"])
            panel_id = str("tab-panel-") + str(tab["id"])
            php_print("\n                           <li id=\"")
            php_print(esc_attr(link_id))
            php_print("\"")
            php_print(class_)
            php_print(">\n                              <a href=\"")
            php_print(esc_url(str("#") + str(panel_id)))
            php_print("\" aria-controls=\"")
            php_print(esc_attr(panel_id))
            php_print("\">\n                                    ")
            php_print(esc_html(tab["title"]))
            php_print("                             </a>\n                          </li>\n                         ")
            class_ = ""
        # end for
        php_print("""                       </ul>
        </div>
        """)
        if help_sidebar:
            php_print("                 <div class=\"contextual-help-sidebar\">\n                       ")
            php_print(help_sidebar)
            php_print("                 </div>\n                    ")
        # end if
        php_print("\n                   <div class=\"contextual-help-tabs-wrap\">\n                     ")
        classes = "help-tab-content active"
        for tab in self.get_help_tabs():
            panel_id = str("tab-panel-") + str(tab["id"])
            php_print("\n                           <div id=\"")
            php_print(esc_attr(panel_id))
            php_print("\" class=\"")
            php_print(classes)
            php_print("\">\n                                ")
            #// Print tab content.
            php_print(tab["content"])
            #// If it exists, fire tab callback.
            if (not php_empty(lambda : tab["callback"])):
                call_user_func_array(tab["callback"], Array(self, tab))
            # end if
            php_print("                         </div>\n                            ")
            classes = "help-tab-content"
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
        columns = apply_filters("screen_layout_columns", Array(), self.id, self)
        if (not php_empty(lambda : columns)) and (php_isset(lambda : columns[self.id])):
            self.add_option("layout_columns", Array({"max": columns[self.id]}))
        # end if
        if self.get_option("layout_columns"):
            self.columns = int(get_user_option(str("screen_layout_") + str(self.id)))
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
        
        global wp_meta_boxes
        php_check_if_defined("wp_meta_boxes")
        if php_is_bool(self._show_screen_options):
            return self._show_screen_options
        # end if
        columns = get_column_headers(self)
        show_screen = (not php_empty(lambda : wp_meta_boxes[self.id])) or columns or self.get_option("per_page")
        self._screen_settings = ""
        if "post" == self.base:
            expand = "<fieldset class=\"editor-expand hidden\"><legend>" + __("Additional settings") + "</legend><label for=\"editor-expand-toggle\">"
            expand += "<input type=\"checkbox\" id=\"editor-expand-toggle\"" + checked(get_user_setting("editor_expand", "on"), "on", False) + " />"
            expand += __("Enable full-height editor and distraction-free functionality.") + "</label></fieldset>"
            self._screen_settings = expand
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
            show_screen = True
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
        self._show_screen_options = apply_filters("screen_options_show_screen", show_screen, self)
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
    def render_screen_options(self, options=Array()):
        
        options = wp_parse_args(options, Array({"wrap": True}))
        wrapper_start = ""
        wrapper_end = ""
        form_start = ""
        form_end = ""
        #// Output optional wrapper.
        if options["wrap"]:
            wrapper_start = "<div id=\"screen-options-wrap\" class=\"hidden\" tabindex=\"-1\" aria-label=\"" + esc_attr__("Screen Options Tab") + "\">"
            wrapper_end = "</div>"
        # end if
        #// Don't output the form and nonce for the widgets accessibility mode links.
        if "widgets" != self.base:
            form_start = "\n<form id='adv-settings' method='post'>\n"
            form_end = "\n" + wp_nonce_field("screen-options-nonce", "screenoptionnonce", False, False) + "\n</form>\n"
        # end if
        php_print(wrapper_start + form_start)
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
        show_button = apply_filters("screen_options_show_submit", False, self)
        if show_button:
            submit_button(__("Apply"), "primary", "screen-options-apply", True)
        # end if
        php_print(form_end + wrapper_end)
    # end def render_screen_options
    #// 
    #// Render the meta boxes preferences.
    #// 
    #// @since 4.4.0
    #// 
    #// @global array $wp_meta_boxes
    #//
    def render_meta_boxes_preferences(self):
        
        global wp_meta_boxes
        php_check_if_defined("wp_meta_boxes")
        if (not (php_isset(lambda : wp_meta_boxes[self.id]))):
            return
        # end if
        php_print("     <fieldset class=\"metabox-prefs\">\n        <legend>")
        _e("Boxes")
        php_print("</legend>\n      ")
        meta_box_prefs(self)
        if "dashboard" == self.id and has_action("welcome_panel") and current_user_can("edit_theme_options"):
            if (php_isset(lambda : PHP_REQUEST["welcome"])):
                welcome_checked = 0 if php_empty(lambda : PHP_REQUEST["welcome"]) else 1
                update_user_meta(get_current_user_id(), "show_welcome_panel", welcome_checked)
            else:
                welcome_checked = get_user_meta(get_current_user_id(), "show_welcome_panel", True)
                if 2 == welcome_checked and wp_get_current_user().user_email != get_option("admin_email"):
                    welcome_checked = False
                # end if
            # end if
            php_print("<label for=\"wp_welcome_panel-hide\">")
            php_print("<input type=\"checkbox\" id=\"wp_welcome_panel-hide\"" + checked(bool(welcome_checked), True, False) + " />")
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
        
        columns = get_column_headers(self)
        hidden = get_hidden_columns(self)
        if (not columns):
            return
        # end if
        legend = columns["_title"] if (not php_empty(lambda : columns["_title"])) else __("Columns")
        php_print("     <fieldset class=\"metabox-prefs\">\n        <legend>")
        php_print(legend)
        php_print("</legend>\n      ")
        special = Array("_title", "cb", "comment", "media", "name", "title", "username", "blogname")
        for column,title in columns:
            #// Can't hide these for they are special.
            if php_in_array(column, special):
                continue
            # end if
            if php_empty(lambda : title):
                continue
            # end if
            #// 
            #// The Comments column uses HTML in the display name with some screen
            #// reader text. Make sure to strip tags from the Comments column
            #// title and any other custom column title plugins might add.
            #//
            title = wp_strip_all_tags(title)
            id = str(column) + str("-hide")
            php_print("<label>")
            php_print("<input class=\"hide-column-tog\" name=\"" + id + "\" type=\"checkbox\" id=\"" + id + "\" value=\"" + column + "\"" + checked((not php_in_array(column, hidden)), True, False) + " />")
            php_print(str(title) + str("</label>\n"))
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
        screen_layout_columns = self.get_columns()
        num = self.get_option("layout_columns", "max")
        php_print("     <fieldset class='columns-prefs'>\n      <legend class=\"screen-layout\">")
        _e("Layout")
        php_print("</legend>\n      ")
        i = 1
        while i <= num:
            
            php_print("         <label class=\"columns-prefs-")
            php_print(i)
            php_print("\">\n            <input type='radio' name='screen_columns' value='")
            php_print(esc_attr(i))
            php_print("' ")
            checked(screen_layout_columns, i)
            php_print(" />\n            ")
            printf(_n("%s column", "%s columns", i), number_format_i18n(i))
            php_print("         </label>\n      ")
            i += 1
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
        per_page_label = self.get_option("per_page", "label")
        if None == per_page_label:
            per_page_label = __("Number of items per page:")
        # end if
        option = self.get_option("per_page", "option")
        if (not option):
            option = php_str_replace("-", "_", str(self.id) + str("_per_page"))
        # end if
        per_page = int(get_user_option(option))
        if php_empty(lambda : per_page) or per_page < 1:
            per_page = self.get_option("per_page", "default")
            if (not per_page):
                per_page = 20
            # end if
        # end if
        if "edit_comments_per_page" == option:
            comment_status = PHP_REQUEST["comment_status"] if (php_isset(lambda : PHP_REQUEST["comment_status"])) else "all"
            #// This filter is documented in wp-admin/includes/class-wp-comments-list-table.php
            per_page = apply_filters("comments_per_page", per_page, comment_status)
        elif "categories_per_page" == option:
            #// This filter is documented in wp-admin/includes/class-wp-terms-list-table.php
            per_page = apply_filters("edit_categories_per_page", per_page)
        else:
            #// This filter is documented in wp-admin/includes/class-wp-list-table.php
            per_page = apply_filters(str(option), per_page)
        # end if
        #// Back compat.
        if (php_isset(lambda : self.post_type)):
            #// This filter is documented in wp-admin/includes/post.php
            per_page = apply_filters("edit_posts_per_page", per_page, self.post_type)
        # end if
        #// This needs a submit button.
        add_filter("screen_options_show_submit", "__return_true")
        php_print("     <fieldset class=\"screen-options\">\n       <legend>")
        _e("Pagination")
        php_print("</legend>\n          ")
        if per_page_label:
            php_print("             <label for=\"")
            php_print(esc_attr(option))
            php_print("\">")
            php_print(per_page_label)
            php_print("</label>\n               <input type=\"number\" step=\"1\" min=\"1\" max=\"999\" class=\"screen-per-page\" name=\"wp_screen_options[value]\"\n                   id=\"")
            php_print(esc_attr(option))
            php_print("\" maxlength=\"3\"\n                 value=\"")
            php_print(esc_attr(per_page))
            php_print("\" />\n          ")
        # end if
        php_print("             <input type=\"hidden\" name=\"wp_screen_options[option]\" value=\"")
        php_print(esc_attr(option))
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
        
        screen = get_current_screen()
        #// Currently only enabled for posts lists.
        if "edit" != screen.base:
            return
        # end if
        view_mode_post_types = get_post_types(Array({"hierarchical": False, "show_ui": True}))
        #// 
        #// Filters the post types that have different view mode options.
        #// 
        #// @since 4.4.0
        #// 
        #// @param string[] $view_mode_post_types Array of post types that can change view modes.
        #// Default non-hierarchical post types with show_ui on.
        #//
        view_mode_post_types = apply_filters("view_mode_post_types", view_mode_post_types)
        if (not php_in_array(self.post_type, view_mode_post_types)):
            return
        # end if
        global mode
        php_check_if_defined("mode")
        #// This needs a submit button.
        add_filter("screen_options_show_submit", "__return_true")
        php_print("     <fieldset class=\"metabox-prefs view-mode\">\n      <legend>")
        _e("View Mode")
        php_print("</legend>\n              <label for=\"list-view-mode\">\n                    <input id=\"list-view-mode\" type=\"radio\" name=\"mode\" value=\"list\" ")
        checked("list", mode)
        php_print(" />\n                    ")
        _e("List View")
        php_print("             </label>\n              <label for=\"excerpt-view-mode\">\n                 <input id=\"excerpt-view-mode\" type=\"radio\" name=\"mode\" value=\"excerpt\" ")
        checked("excerpt", mode)
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
    def render_screen_reader_content(self, key="", tag="h2"):
        
        if (not (php_isset(lambda : self._screen_reader_content[key]))):
            return
        # end if
        php_print(str("<") + str(tag) + str(" class='screen-reader-text'>") + self._screen_reader_content[key] + str("</") + str(tag) + str(">"))
    # end def render_screen_reader_content
# end class WP_Screen
