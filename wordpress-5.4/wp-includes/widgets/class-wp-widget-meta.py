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
#// Widget API: WP_Widget_Meta class
#// 
#// @package WordPress
#// @subpackage Widgets
#// @since 4.4.0
#// 
#// 
#// Core class used to implement a Meta widget.
#// 
#// Displays log in/out, RSS feed links, etc.
#// 
#// @since 2.8.0
#// 
#// @see WP_Widget
#//
class WP_Widget_Meta(WP_Widget):
    #// 
    #// Sets up a new Meta widget instance.
    #// 
    #// @since 2.8.0
    #//
    def __init__(self):
        
        widget_ops = Array({"classname": "widget_meta", "description": __("Login, RSS, &amp; WordPress.org links."), "customize_selective_refresh": True})
        super().__init__("meta", __("Meta"), widget_ops)
    # end def __init__
    #// 
    #// Outputs the content for the current Meta widget instance.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $args     Display arguments including 'before_title', 'after_title',
    #// 'before_widget', and 'after_widget'.
    #// @param array $instance Settings for the current Meta widget instance.
    #//
    def widget(self, args=None, instance=None):
        
        title = instance["title"] if (not php_empty(lambda : instance["title"])) else __("Meta")
        #// This filter is documented in wp-includes/widgets/class-wp-widget-pages.php
        title = apply_filters("widget_title", title, instance, self.id_base)
        php_print(args["before_widget"])
        if title:
            php_print(args["before_title"] + title + args["after_title"])
        # end if
        php_print("         <ul>\n          ")
        wp_register()
        php_print("         <li>")
        wp_loginout()
        php_print("</li>\n          <li><a href=\"")
        php_print(esc_url(get_bloginfo("rss2_url")))
        php_print("\">")
        _e("Entries feed")
        php_print("</a></li>\n          <li><a href=\"")
        php_print(esc_url(get_bloginfo("comments_rss2_url")))
        php_print("\">")
        _e("Comments feed")
        php_print("</a></li>\n          ")
        #// 
        #// Filters the "WordPress.org" list item HTML in the Meta widget.
        #// 
        #// @since 3.6.0
        #// @since 4.9.0 Added the `$instance` parameter.
        #// 
        #// @param string $html     Default HTML for the WordPress.org list item.
        #// @param array  $instance Array of settings for the current widget.
        #//
        php_print(apply_filters("widget_meta_poweredby", php_sprintf("<li><a href=\"%1$s\">%2$s</a></li>", esc_url(__("https://wordpress.org/")), __("WordPress.org")), instance))
        wp_meta()
        php_print("         </ul>\n         ")
        php_print(args["after_widget"])
    # end def widget
    #// 
    #// Handles updating settings for the current Meta widget instance.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $new_instance New settings for this instance as input by the user via
    #// WP_Widget::form().
    #// @param array $old_instance Old settings for this instance.
    #// @return array Updated settings to save.
    #//
    def update(self, new_instance=None, old_instance=None):
        
        instance = old_instance
        instance["title"] = sanitize_text_field(new_instance["title"])
        return instance
    # end def update
    #// 
    #// Outputs the settings form for the Meta widget.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $instance Current settings.
    #//
    def form(self, instance=None):
        
        instance = wp_parse_args(instance, Array({"title": ""}))
        php_print("         <p><label for=\"")
        php_print(self.get_field_id("title"))
        php_print("\">")
        _e("Title:")
        php_print("</label> <input class=\"widefat\" id=\"")
        php_print(self.get_field_id("title"))
        php_print("\" name=\"")
        php_print(self.get_field_name("title"))
        php_print("\" type=\"text\" value=\"")
        php_print(esc_attr(instance["title"]))
        php_print("\" /></p>\n      ")
    # end def form
# end class WP_Widget_Meta
