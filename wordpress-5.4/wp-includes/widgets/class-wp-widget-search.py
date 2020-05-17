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
        
        
        widget_ops_ = Array({"classname": "widget_search", "description": __("A search form for your site."), "customize_selective_refresh": True})
        super().__init__("search", _x("Search", "Search widget"), widget_ops_)
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
    def widget(self, args_=None, instance_=None):
        
        
        title_ = instance_["title"] if (not php_empty(lambda : instance_["title"])) else ""
        #// This filter is documented in wp-includes/widgets/class-wp-widget-pages.php
        title_ = apply_filters("widget_title", title_, instance_, self.id_base)
        php_print(args_["before_widget"])
        if title_:
            php_print(args_["before_title"] + title_ + args_["after_title"])
        # end if
        #// Use current theme search form if it exists.
        get_search_form()
        php_print(args_["after_widget"])
    # end def widget
    #// 
    #// Outputs the settings form for the Search widget.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $instance Current settings.
    #//
    def form(self, instance_=None):
        
        
        instance_ = wp_parse_args(instance_, Array({"title": ""}))
        title_ = instance_["title"]
        php_print("     <p><label for=\"")
        php_print(self.get_field_id("title"))
        php_print("\">")
        _e("Title:")
        php_print(" <input class=\"widefat\" id=\"")
        php_print(self.get_field_id("title"))
        php_print("\" name=\"")
        php_print(self.get_field_name("title"))
        php_print("\" type=\"text\" value=\"")
        php_print(esc_attr(title_))
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
    def update(self, new_instance_=None, old_instance_=None):
        
        
        instance_ = old_instance_
        new_instance_ = wp_parse_args(new_instance_, Array({"title": ""}))
        instance_["title"] = sanitize_text_field(new_instance_["title"])
        return instance_
    # end def update
# end class WP_Widget_Search
