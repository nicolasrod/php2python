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
        
        
        widget_ops_ = Array({"description": __("Entries from any RSS or Atom feed."), "customize_selective_refresh": True})
        control_ops_ = Array({"width": 400, "height": 200})
        super().__init__("rss", __("RSS"), widget_ops_, control_ops_)
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
    def widget(self, args_=None, instance_=None):
        
        
        if (php_isset(lambda : instance_["error"])) and instance_["error"]:
            return
        # end if
        url_ = instance_["url"] if (not php_empty(lambda : instance_["url"])) else ""
        while True:
            
            if not (php_stristr(url_, "http") != url_):
                break
            # end if
            url_ = php_substr(url_, 1)
        # end while
        if php_empty(lambda : url_):
            return
        # end if
        #// Self-URL destruction sequence.
        if php_in_array(untrailingslashit(url_), Array(site_url(), home_url())):
            return
        # end if
        rss_ = fetch_feed(url_)
        title_ = instance_["title"]
        desc_ = ""
        link_ = ""
        if (not is_wp_error(rss_)):
            desc_ = esc_attr(strip_tags(html_entity_decode(rss_.get_description(), ENT_QUOTES, get_option("blog_charset"))))
            if php_empty(lambda : title_):
                title_ = strip_tags(rss_.get_title())
            # end if
            link_ = strip_tags(rss_.get_permalink())
            while True:
                
                if not (php_stristr(link_, "http") != link_):
                    break
                # end if
                link_ = php_substr(link_, 1)
            # end while
        # end if
        if php_empty(lambda : title_):
            title_ = desc_ if (not php_empty(lambda : desc_)) else __("Unknown Feed")
        # end if
        #// This filter is documented in wp-includes/widgets/class-wp-widget-pages.php
        title_ = apply_filters("widget_title", title_, instance_, self.id_base)
        url_ = strip_tags(url_)
        icon_ = includes_url("images/rss.png")
        if title_:
            title_ = "<a class=\"rsswidget\" href=\"" + esc_url(url_) + "\"><img class=\"rss-widget-icon\" style=\"border:0\" width=\"14\" height=\"14\" src=\"" + esc_url(icon_) + "\" alt=\"RSS\" /></a> <a class=\"rsswidget\" href=\"" + esc_url(link_) + "\">" + esc_html(title_) + "</a>"
        # end if
        php_print(args_["before_widget"])
        if title_:
            php_print(args_["before_title"] + title_ + args_["after_title"])
        # end if
        wp_widget_rss_output(rss_, instance_)
        php_print(args_["after_widget"])
        if (not is_wp_error(rss_)):
            rss_.__del__()
        # end if
        rss_ = None
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
    def update(self, new_instance_=None, old_instance_=None):
        
        
        testurl_ = (php_isset(lambda : new_instance_["url"])) and (not (php_isset(lambda : old_instance_["url"]))) or new_instance_["url"] != old_instance_["url"]
        return wp_widget_rss_process(new_instance_, testurl_)
    # end def update
    #// 
    #// Outputs the settings form for the RSS widget.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $instance Current settings.
    #//
    def form(self, instance_=None):
        
        
        if php_empty(lambda : instance_):
            instance_ = Array({"title": "", "url": "", "items": 10, "error": False, "show_summary": 0, "show_author": 0, "show_date": 0})
        # end if
        instance_["number"] = self.number
        wp_widget_rss_form(instance_)
    # end def form
# end class WP_Widget_RSS
