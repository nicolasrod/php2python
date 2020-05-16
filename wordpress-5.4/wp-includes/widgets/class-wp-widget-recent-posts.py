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
#// Widget API: WP_Widget_Recent_Posts class
#// 
#// @package WordPress
#// @subpackage Widgets
#// @since 4.4.0
#// 
#// 
#// Core class used to implement a Recent Posts widget.
#// 
#// @since 2.8.0
#// 
#// @see WP_Widget
#//
class WP_Widget_Recent_Posts(WP_Widget):
    #// 
    #// Sets up a new Recent Posts widget instance.
    #// 
    #// @since 2.8.0
    #//
    def __init__(self):
        
        widget_ops = Array({"classname": "widget_recent_entries", "description": __("Your site&#8217;s most recent Posts."), "customize_selective_refresh": True})
        super().__init__("recent-posts", __("Recent Posts"), widget_ops)
        self.alt_option_name = "widget_recent_entries"
    # end def __init__
    #// 
    #// Outputs the content for the current Recent Posts widget instance.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $args     Display arguments including 'before_title', 'after_title',
    #// 'before_widget', and 'after_widget'.
    #// @param array $instance Settings for the current Recent Posts widget instance.
    #//
    def widget(self, args=None, instance=None):
        
        if (not (php_isset(lambda : args["widget_id"]))):
            args["widget_id"] = self.id
        # end if
        title = instance["title"] if (not php_empty(lambda : instance["title"])) else __("Recent Posts")
        #// This filter is documented in wp-includes/widgets/class-wp-widget-pages.php
        title = apply_filters("widget_title", title, instance, self.id_base)
        number = absint(instance["number"]) if (not php_empty(lambda : instance["number"])) else 5
        if (not number):
            number = 5
        # end if
        show_date = instance["show_date"] if (php_isset(lambda : instance["show_date"])) else False
        r = php_new_class("WP_Query", lambda : WP_Query(apply_filters("widget_posts_args", Array({"posts_per_page": number, "no_found_rows": True, "post_status": "publish", "ignore_sticky_posts": True}), instance)))
        if (not r.have_posts()):
            return
        # end if
        php_print("     ")
        php_print(args["before_widget"])
        php_print("     ")
        if title:
            php_print(args["before_title"] + title + args["after_title"])
        # end if
        php_print("     <ul>\n          ")
        for recent_post in r.posts:
            php_print("             ")
            post_title = get_the_title(recent_post.ID)
            title = post_title if (not php_empty(lambda : post_title)) else __("(no title)")
            aria_current = ""
            if get_queried_object_id() == recent_post.ID:
                aria_current = " aria-current=\"page\""
            # end if
            php_print("             <li>\n                  <a href=\"")
            the_permalink(recent_post.ID)
            php_print("\"")
            php_print(aria_current)
            php_print(">")
            php_print(title)
            php_print("</a>\n                   ")
            if show_date:
                php_print("                     <span class=\"post-date\">")
                php_print(get_the_date("", recent_post.ID))
                php_print("</span>\n                    ")
            # end if
            php_print("             </li>\n         ")
        # end for
        php_print("     </ul>\n     ")
        php_print(args["after_widget"])
    # end def widget
    #// 
    #// Handles updating the settings for the current Recent Posts widget instance.
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
        instance["number"] = php_int(new_instance["number"])
        instance["show_date"] = php_bool(new_instance["show_date"]) if (php_isset(lambda : new_instance["show_date"])) else False
        return instance
    # end def update
    #// 
    #// Outputs the settings form for the Recent Posts widget.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $instance Current settings.
    #//
    def form(self, instance=None):
        
        title = esc_attr(instance["title"]) if (php_isset(lambda : instance["title"])) else ""
        number = absint(instance["number"]) if (php_isset(lambda : instance["number"])) else 5
        show_date = php_bool(instance["show_date"]) if (php_isset(lambda : instance["show_date"])) else False
        php_print("     <p><label for=\"")
        php_print(self.get_field_id("title"))
        php_print("\">")
        _e("Title:")
        php_print("</label>\n       <input class=\"widefat\" id=\"")
        php_print(self.get_field_id("title"))
        php_print("\" name=\"")
        php_print(self.get_field_name("title"))
        php_print("\" type=\"text\" value=\"")
        php_print(title)
        php_print("\" /></p>\n\n        <p><label for=\"")
        php_print(self.get_field_id("number"))
        php_print("\">")
        _e("Number of posts to show:")
        php_print("</label>\n       <input class=\"tiny-text\" id=\"")
        php_print(self.get_field_id("number"))
        php_print("\" name=\"")
        php_print(self.get_field_name("number"))
        php_print("\" type=\"number\" step=\"1\" min=\"1\" value=\"")
        php_print(number)
        php_print("\" size=\"3\" /></p>\n\n     <p><input class=\"checkbox\" type=\"checkbox\"")
        checked(show_date)
        php_print(" id=\"")
        php_print(self.get_field_id("show_date"))
        php_print("\" name=\"")
        php_print(self.get_field_name("show_date"))
        php_print("\" />\n      <label for=\"")
        php_print(self.get_field_id("show_date"))
        php_print("\">")
        _e("Display post date?")
        php_print("</label></p>\n       ")
    # end def form
# end class WP_Widget_Recent_Posts
