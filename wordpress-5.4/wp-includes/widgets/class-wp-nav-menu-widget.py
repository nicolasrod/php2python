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
#// Widget API: WP_Nav_Menu_Widget class
#// 
#// @package WordPress
#// @subpackage Widgets
#// @since 4.4.0
#// 
#// 
#// Core class used to implement the Navigation Menu widget.
#// 
#// @since 3.0.0
#// 
#// @see WP_Widget
#//
class WP_Nav_Menu_Widget(WP_Widget):
    #// 
    #// Sets up a new Navigation Menu widget instance.
    #// 
    #// @since 3.0.0
    #//
    def __init__(self):
        
        widget_ops = Array({"description": __("Add a navigation menu to your sidebar."), "customize_selective_refresh": True})
        super().__init__("nav_menu", __("Navigation Menu"), widget_ops)
    # end def __init__
    #// 
    #// Outputs the content for the current Navigation Menu widget instance.
    #// 
    #// @since 3.0.0
    #// 
    #// @param array $args     Display arguments including 'before_title', 'after_title',
    #// 'before_widget', and 'after_widget'.
    #// @param array $instance Settings for the current Navigation Menu widget instance.
    #//
    def widget(self, args=None, instance=None):
        
        #// Get menu.
        nav_menu = wp_get_nav_menu_object(instance["nav_menu"]) if (not php_empty(lambda : instance["nav_menu"])) else False
        if (not nav_menu):
            return
        # end if
        title = instance["title"] if (not php_empty(lambda : instance["title"])) else ""
        #// This filter is documented in wp-includes/widgets/class-wp-widget-pages.php
        title = apply_filters("widget_title", title, instance, self.id_base)
        php_print(args["before_widget"])
        if title:
            php_print(args["before_title"] + title + args["after_title"])
        # end if
        nav_menu_args = Array({"fallback_cb": "", "menu": nav_menu})
        #// 
        #// Filters the arguments for the Navigation Menu widget.
        #// 
        #// @since 4.2.0
        #// @since 4.4.0 Added the `$instance` parameter.
        #// 
        #// @param array    $nav_menu_args {
        #// An array of arguments passed to wp_nav_menu() to retrieve a navigation menu.
        #// 
        #// @type callable|bool $fallback_cb Callback to fire if the menu doesn't exist. Default empty.
        #// @type mixed         $menu        Menu ID, slug, or name.
        #// }
        #// @param WP_Term  $nav_menu      Nav menu object for the current menu.
        #// @param array    $args          Display arguments for the current widget.
        #// @param array    $instance      Array of settings for the current widget.
        #//
        wp_nav_menu(apply_filters("widget_nav_menu_args", nav_menu_args, nav_menu, args, instance))
        php_print(args["after_widget"])
    # end def widget
    #// 
    #// Handles updating settings for the current Navigation Menu widget instance.
    #// 
    #// @since 3.0.0
    #// 
    #// @param array $new_instance New settings for this instance as input by the user via
    #// WP_Widget::form().
    #// @param array $old_instance Old settings for this instance.
    #// @return array Updated settings to save.
    #//
    def update(self, new_instance=None, old_instance=None):
        
        instance = Array()
        if (not php_empty(lambda : new_instance["title"])):
            instance["title"] = sanitize_text_field(new_instance["title"])
        # end if
        if (not php_empty(lambda : new_instance["nav_menu"])):
            instance["nav_menu"] = php_int(new_instance["nav_menu"])
        # end if
        return instance
    # end def update
    #// 
    #// Outputs the settings form for the Navigation Menu widget.
    #// 
    #// @since 3.0.0
    #// 
    #// @param array $instance Current settings.
    #// @global WP_Customize_Manager $wp_customize
    #//
    def form(self, instance=None):
        
        global wp_customize
        php_check_if_defined("wp_customize")
        title = instance["title"] if (php_isset(lambda : instance["title"])) else ""
        nav_menu = instance["nav_menu"] if (php_isset(lambda : instance["nav_menu"])) else ""
        #// Get menus.
        menus = wp_get_nav_menus()
        empty_menus_style = ""
        not_empty_menus_style = ""
        if php_empty(lambda : menus):
            empty_menus_style = " style=\"display:none\" "
        else:
            not_empty_menus_style = " style=\"display:none\" "
        # end if
        nav_menu_style = ""
        if (not nav_menu):
            nav_menu_style = "display: none;"
        # end if
        pass
        php_print("     <p class=\"nav-menu-widget-no-menus-message\" ")
        php_print(not_empty_menus_style)
        php_print(">\n          ")
        if type(wp_customize).__name__ == "WP_Customize_Manager":
            url = "javascript: wp.customize.panel( \"nav_menus\" ).focus();"
        else:
            url = admin_url("nav-menus.php")
        # end if
        #// translators: %s: URL to create a new menu.
        printf(__("No menus have been created yet. <a href=\"%s\">Create some</a>."), esc_attr(url))
        php_print("     </p>\n      <div class=\"nav-menu-widget-form-controls\" ")
        php_print(empty_menus_style)
        php_print(">\n          <p>\n               <label for=\"")
        php_print(self.get_field_id("title"))
        php_print("\">")
        _e("Title:")
        php_print("</label>\n               <input type=\"text\" class=\"widefat\" id=\"")
        php_print(self.get_field_id("title"))
        php_print("\" name=\"")
        php_print(self.get_field_name("title"))
        php_print("\" value=\"")
        php_print(esc_attr(title))
        php_print("""\"/>
        </p>
        <p>
        <label for=\"""")
        php_print(self.get_field_id("nav_menu"))
        php_print("\">")
        _e("Select Menu:")
        php_print("</label>\n               <select id=\"")
        php_print(self.get_field_id("nav_menu"))
        php_print("\" name=\"")
        php_print(self.get_field_name("nav_menu"))
        php_print("\">\n                    <option value=\"0\">")
        _e("&mdash; Select &mdash;")
        php_print("</option>\n                  ")
        for menu in menus:
            php_print("                     <option value=\"")
            php_print(esc_attr(menu.term_id))
            php_print("\" ")
            selected(nav_menu, menu.term_id)
            php_print(">\n                          ")
            php_print(esc_html(menu.name))
            php_print("                     </option>\n                 ")
        # end for
        php_print("             </select>\n         </p>\n          ")
        if type(wp_customize).__name__ == "WP_Customize_Manager":
            php_print("             <p class=\"edit-selected-nav-menu\" style=\"")
            php_print(nav_menu_style)
            php_print("\">\n                    <button type=\"button\" class=\"button\">")
            _e("Edit Menu")
            php_print("</button>\n              </p>\n          ")
        # end if
        php_print("     </div>\n        ")
    # end def form
# end class WP_Nav_Menu_Widget
