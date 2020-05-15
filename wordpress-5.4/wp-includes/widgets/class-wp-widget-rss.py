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
#// Widget API: WP_Widget_RSS class
#// 
#// @package WordPress
#// @subpackage Widgets
#// @since 4.4.0
#// 
#// 
#// Core class used to implement a RSS widget.
#// 
#// @since 2.8.0
#// 
#// @see WP_Widget
#//
class WP_Widget_RSS(WP_Widget):
    #// 
    #// Sets up a new RSS widget instance.
    #// 
    #// @since 2.8.0
    #//
    def __init__(self):
        
        widget_ops = Array({"description": __("Entries from any RSS or Atom feed."), "customize_selective_refresh": True})
        control_ops = Array({"width": 400, "height": 200})
        super().__init__("rss", __("RSS"), widget_ops, control_ops)
    # end def __init__
    #// 
    #// Outputs the content for the current RSS widget instance.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $args     Display arguments including 'before_title', 'after_title',
    #// 'before_widget', and 'after_widget'.
    #// @param array $instance Settings for the current RSS widget instance.
    #//
    def widget(self, args=None, instance=None):
        
        if (php_isset(lambda : instance["error"])) and instance["error"]:
            return
        # end if
        url = instance["url"] if (not php_empty(lambda : instance["url"])) else ""
        while True:
            
            if not (php_stristr(url, "http") != url):
                break
            # end if
            url = php_substr(url, 1)
        # end while
        if php_empty(lambda : url):
            return
        # end if
        #// Self-URL destruction sequence.
        if php_in_array(untrailingslashit(url), Array(site_url(), home_url())):
            return
        # end if
        rss = fetch_feed(url)
        title = instance["title"]
        desc = ""
        link = ""
        if (not is_wp_error(rss)):
            desc = esc_attr(strip_tags(html_entity_decode(rss.get_description(), ENT_QUOTES, get_option("blog_charset"))))
            if php_empty(lambda : title):
                title = strip_tags(rss.get_title())
            # end if
            link = strip_tags(rss.get_permalink())
            while True:
                
                if not (php_stristr(link, "http") != link):
                    break
                # end if
                link = php_substr(link, 1)
            # end while
        # end if
        if php_empty(lambda : title):
            title = desc if (not php_empty(lambda : desc)) else __("Unknown Feed")
        # end if
        #// This filter is documented in wp-includes/widgets/class-wp-widget-pages.php
        title = apply_filters("widget_title", title, instance, self.id_base)
        url = strip_tags(url)
        icon = includes_url("images/rss.png")
        if title:
            title = "<a class=\"rsswidget\" href=\"" + esc_url(url) + "\"><img class=\"rss-widget-icon\" style=\"border:0\" width=\"14\" height=\"14\" src=\"" + esc_url(icon) + "\" alt=\"RSS\" /></a> <a class=\"rsswidget\" href=\"" + esc_url(link) + "\">" + esc_html(title) + "</a>"
        # end if
        php_print(args["before_widget"])
        if title:
            php_print(args["before_title"] + title + args["after_title"])
        # end if
        wp_widget_rss_output(rss, instance)
        php_print(args["after_widget"])
        if (not is_wp_error(rss)):
            rss.__del__()
        # end if
        rss = None
    # end def widget
    #// 
    #// Handles updating settings for the current RSS widget instance.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $new_instance New settings for this instance as input by the user via
    #// WP_Widget::form().
    #// @param array $old_instance Old settings for this instance.
    #// @return array Updated settings to save.
    #//
    def update(self, new_instance=None, old_instance=None):
        
        testurl = (php_isset(lambda : new_instance["url"])) and (not (php_isset(lambda : old_instance["url"]))) or new_instance["url"] != old_instance["url"]
        return wp_widget_rss_process(new_instance, testurl)
    # end def update
    #// 
    #// Outputs the settings form for the RSS widget.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $instance Current settings.
    #//
    def form(self, instance=None):
        
        if php_empty(lambda : instance):
            instance = Array({"title": "", "url": "", "items": 10, "error": False, "show_summary": 0, "show_author": 0, "show_date": 0})
        # end if
        instance["number"] = self.number
        wp_widget_rss_form(instance)
    # end def form
# end class WP_Widget_RSS
