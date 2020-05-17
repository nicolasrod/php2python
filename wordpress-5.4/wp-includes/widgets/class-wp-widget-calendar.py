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
#// Widget API: WP_Widget_Calendar class
#// 
#// @package WordPress
#// @subpackage Widgets
#// @since 4.4.0
#// 
#// 
#// Core class used to implement the Calendar widget.
#// 
#// @since 2.8.0
#// 
#// @see WP_Widget
#//
class WP_Widget_Calendar(WP_Widget):
    #// 
    #// Ensure that the ID attribute only appears in the markup once
    #// 
    #// @since 4.4.0
    #// @var int
    #//
    instance = 0
    #// 
    #// Sets up a new Calendar widget instance.
    #// 
    #// @since 2.8.0
    #//
    def __init__(self):
        
        
        widget_ops_ = Array({"classname": "widget_calendar", "description": __("A calendar of your siteâs posts."), "customize_selective_refresh": True})
        super().__init__("calendar", __("Calendar"), widget_ops_)
    # end def __init__
    #// 
    #// Outputs the content for the current Calendar widget instance.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $args     Display arguments including 'before_title', 'after_title',
    #// 'before_widget', and 'after_widget'.
    #// @param array $instance The settings for the particular instance of the widget.
    #//
    def widget(self, args_=None, instance_=None):
        
        
        title_ = instance_["title"] if (not php_empty(lambda : instance_["title"])) else ""
        #// This filter is documented in wp-includes/widgets/class-wp-widget-pages.php
        title_ = apply_filters("widget_title", title_, instance_, self.id_base)
        php_print(args_["before_widget"])
        if title_:
            php_print(args_["before_title"] + title_ + args_["after_title"])
        # end if
        if 0 == self.instance:
            php_print("<div id=\"calendar_wrap\" class=\"calendar_wrap\">")
        else:
            php_print("<div class=\"calendar_wrap\">")
        # end if
        get_calendar()
        php_print("</div>")
        php_print(args_["after_widget"])
        self.instance += 1
    # end def widget
    #// 
    #// Handles updating settings for the current Calendar widget instance.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $new_instance New settings for this instance as input by the user via
    #// WP_Widget::form().
    #// @param array $old_instance Old settings for this instance.
    #// @return array Updated settings to save.
    #//
    def update(self, new_instance_=None, old_instance_=None):
        
        
        instance_ = old_instance_
        instance_["title"] = sanitize_text_field(new_instance_["title"])
        return instance_
    # end def update
    #// 
    #// Outputs the settings form for the Calendar widget.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $instance Current settings.
    #//
    def form(self, instance_=None):
        
        
        instance_ = wp_parse_args(instance_, Array({"title": ""}))
        php_print("     <p><label for=\"")
        php_print(self.get_field_id("title"))
        php_print("\">")
        _e("Title:")
        php_print("</label>\n       <input class=\"widefat\" id=\"")
        php_print(self.get_field_id("title"))
        php_print("\" name=\"")
        php_print(self.get_field_name("title"))
        php_print("\" type=\"text\" value=\"")
        php_print(esc_attr(instance_["title"]))
        php_print("\" /></p>\n      ")
    # end def form
# end class WP_Widget_Calendar
