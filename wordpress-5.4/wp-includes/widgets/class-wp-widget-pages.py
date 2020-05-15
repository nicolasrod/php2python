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
#// Widget API: WP_Widget_Pages class
#// 
#// @package WordPress
#// @subpackage Widgets
#// @since 4.4.0
#// 
#// 
#// Core class used to implement a Pages widget.
#// 
#// @since 2.8.0
#// 
#// @see WP_Widget
#//
class WP_Widget_Pages(WP_Widget):
    #// 
    #// Sets up a new Pages widget instance.
    #// 
    #// @since 2.8.0
    #//
    def __init__(self):
        
        widget_ops = Array({"classname": "widget_pages", "description": __("A list of your site&#8217;s Pages."), "customize_selective_refresh": True})
        super().__init__("pages", __("Pages"), widget_ops)
    # end def __init__
    #// 
    #// Outputs the content for the current Pages widget instance.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $args     Display arguments including 'before_title', 'after_title',
    #// 'before_widget', and 'after_widget'.
    #// @param array $instance Settings for the current Pages widget instance.
    #//
    def widget(self, args=None, instance=None):
        
        title = instance["title"] if (not php_empty(lambda : instance["title"])) else __("Pages")
        #// 
        #// Filters the widget title.
        #// 
        #// @since 2.6.0
        #// 
        #// @param string $title    The widget title. Default 'Pages'.
        #// @param array  $instance Array of settings for the current widget.
        #// @param mixed  $id_base  The widget ID.
        #//
        title = apply_filters("widget_title", title, instance, self.id_base)
        sortby = "menu_order" if php_empty(lambda : instance["sortby"]) else instance["sortby"]
        exclude = "" if php_empty(lambda : instance["exclude"]) else instance["exclude"]
        if "menu_order" == sortby:
            sortby = "menu_order, post_title"
        # end if
        out = wp_list_pages(apply_filters("widget_pages_args", Array({"title_li": "", "echo": 0, "sort_column": sortby, "exclude": exclude}), instance))
        if (not php_empty(lambda : out)):
            php_print(args["before_widget"])
            if title:
                php_print(args["before_title"] + title + args["after_title"])
            # end if
            php_print("     <ul>\n          ")
            php_print(out)
            php_print("     </ul>\n         ")
            php_print(args["after_widget"])
        # end if
    # end def widget
    #// 
    #// Handles updating settings for the current Pages widget instance.
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
        if php_in_array(new_instance["sortby"], Array("post_title", "menu_order", "ID")):
            instance["sortby"] = new_instance["sortby"]
        else:
            instance["sortby"] = "menu_order"
        # end if
        instance["exclude"] = sanitize_text_field(new_instance["exclude"])
        return instance
    # end def update
    #// 
    #// Outputs the settings form for the Pages widget.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $instance Current settings.
    #//
    def form(self, instance=None):
        
        #// Defaults.
        instance = wp_parse_args(instance, Array({"sortby": "post_title", "title": "", "exclude": ""}))
        php_print("     <p>\n           <label for=\"")
        php_print(esc_attr(self.get_field_id("title")))
        php_print("\">")
        _e("Title:")
        php_print("</label>\n           <input class=\"widefat\" id=\"")
        php_print(esc_attr(self.get_field_id("title")))
        php_print("\" name=\"")
        php_print(esc_attr(self.get_field_name("title")))
        php_print("\" type=\"text\" value=\"")
        php_print(esc_attr(instance["title"]))
        php_print("""\" />
        </p>
        <p>
        <label for=\"""")
        php_print(esc_attr(self.get_field_id("sortby")))
        php_print("\">")
        _e("Sort by:")
        php_print("</label>\n           <select name=\"")
        php_print(esc_attr(self.get_field_name("sortby")))
        php_print("\" id=\"")
        php_print(esc_attr(self.get_field_id("sortby")))
        php_print("\" class=\"widefat\">\n              <option value=\"post_title\"")
        selected(instance["sortby"], "post_title")
        php_print(">")
        _e("Page title")
        php_print("</option>\n              <option value=\"menu_order\"")
        selected(instance["sortby"], "menu_order")
        php_print(">")
        _e("Page order")
        php_print("</option>\n              <option value=\"ID\"")
        selected(instance["sortby"], "ID")
        php_print(">")
        _e("Page ID")
        php_print("""</option>
        </select>
        </p>
        <p>
        <label for=\"""")
        php_print(esc_attr(self.get_field_id("exclude")))
        php_print("\">")
        _e("Exclude:")
        php_print("</label>\n           <input type=\"text\" value=\"")
        php_print(esc_attr(instance["exclude"]))
        php_print("\" name=\"")
        php_print(esc_attr(self.get_field_name("exclude")))
        php_print("\" id=\"")
        php_print(esc_attr(self.get_field_id("exclude")))
        php_print("\" class=\"widefat\" />\n            <br />\n            <small>")
        _e("Page IDs, separated by commas.")
        php_print("</small>\n       </p>\n      ")
    # end def form
# end class WP_Widget_Pages
