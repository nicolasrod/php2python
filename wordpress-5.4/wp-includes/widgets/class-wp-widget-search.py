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
#// Widget API: WP_Widget_Search class
#// 
#// @package WordPress
#// @subpackage Widgets
#// @since 4.4.0
#// 
#// 
#// Core class used to implement a Search widget.
#// 
#// @since 2.8.0
#// 
#// @see WP_Widget
#//
class WP_Widget_Search(WP_Widget):
    #// 
    #// Sets up a new Search widget instance.
    #// 
    #// @since 2.8.0
    #//
    def __init__(self):
        
        widget_ops = Array({"classname": "widget_search", "description": __("A search form for your site."), "customize_selective_refresh": True})
        super().__init__("search", _x("Search", "Search widget"), widget_ops)
    # end def __init__
    #// 
    #// Outputs the content for the current Search widget instance.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $args     Display arguments including 'before_title', 'after_title',
    #// 'before_widget', and 'after_widget'.
    #// @param array $instance Settings for the current Search widget instance.
    #//
    def widget(self, args=None, instance=None):
        
        title = instance["title"] if (not php_empty(lambda : instance["title"])) else ""
        #// This filter is documented in wp-includes/widgets/class-wp-widget-pages.php
        title = apply_filters("widget_title", title, instance, self.id_base)
        php_print(args["before_widget"])
        if title:
            php_print(args["before_title"] + title + args["after_title"])
        # end if
        #// Use current theme search form if it exists.
        get_search_form()
        php_print(args["after_widget"])
    # end def widget
    #// 
    #// Outputs the settings form for the Search widget.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $instance Current settings.
    #//
    def form(self, instance=None):
        
        instance = wp_parse_args(instance, Array({"title": ""}))
        title = instance["title"]
        php_print("     <p><label for=\"")
        php_print(self.get_field_id("title"))
        php_print("\">")
        _e("Title:")
        php_print(" <input class=\"widefat\" id=\"")
        php_print(self.get_field_id("title"))
        php_print("\" name=\"")
        php_print(self.get_field_name("title"))
        php_print("\" type=\"text\" value=\"")
        php_print(esc_attr(title))
        php_print("\" /></label></p>\n      ")
    # end def form
    #// 
    #// Handles updating settings for the current Search widget instance.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $new_instance New settings for this instance as input by the user via
    #// WP_Widget::form().
    #// @param array $old_instance Old settings for this instance.
    #// @return array Updated settings.
    #//
    def update(self, new_instance=None, old_instance=None):
        
        instance = old_instance
        new_instance = wp_parse_args(new_instance, Array({"title": ""}))
        instance["title"] = sanitize_text_field(new_instance["title"])
        return instance
    # end def update
# end class WP_Widget_Search
