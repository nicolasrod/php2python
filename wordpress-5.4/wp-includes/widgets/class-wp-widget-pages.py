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
        
        
        widget_ops_ = Array({"classname": "widget_pages", "description": __("A list of your site&#8217;s Pages."), "customize_selective_refresh": True})
        super().__init__("pages", __("Pages"), widget_ops_)
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
    def widget(self, args_=None, instance_=None):
        
        
        title_ = instance_["title"] if (not php_empty(lambda : instance_["title"])) else __("Pages")
        #// 
        #// Filters the widget title.
        #// 
        #// @since 2.6.0
        #// 
        #// @param string $title    The widget title. Default 'Pages'.
        #// @param array  $instance Array of settings for the current widget.
        #// @param mixed  $id_base  The widget ID.
        #//
        title_ = apply_filters("widget_title", title_, instance_, self.id_base)
        sortby_ = "menu_order" if php_empty(lambda : instance_["sortby"]) else instance_["sortby"]
        exclude_ = "" if php_empty(lambda : instance_["exclude"]) else instance_["exclude"]
        if "menu_order" == sortby_:
            sortby_ = "menu_order, post_title"
        # end if
        out_ = wp_list_pages(apply_filters("widget_pages_args", Array({"title_li": "", "echo": 0, "sort_column": sortby_, "exclude": exclude_}), instance_))
        if (not php_empty(lambda : out_)):
            php_print(args_["before_widget"])
            if title_:
                php_print(args_["before_title"] + title_ + args_["after_title"])
            # end if
            php_print("     <ul>\n          ")
            php_print(out_)
            php_print("     </ul>\n         ")
            php_print(args_["after_widget"])
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
    def update(self, new_instance_=None, old_instance_=None):
        
        
        instance_ = old_instance_
        instance_["title"] = sanitize_text_field(new_instance_["title"])
        if php_in_array(new_instance_["sortby"], Array("post_title", "menu_order", "ID")):
            instance_["sortby"] = new_instance_["sortby"]
        else:
            instance_["sortby"] = "menu_order"
        # end if
        instance_["exclude"] = sanitize_text_field(new_instance_["exclude"])
        return instance_
    # end def update
    #// 
    #// Outputs the settings form for the Pages widget.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $instance Current settings.
    #//
    def form(self, instance_=None):
        
        
        #// Defaults.
        instance_ = wp_parse_args(instance_, Array({"sortby": "post_title", "title": "", "exclude": ""}))
        php_print("     <p>\n           <label for=\"")
        php_print(esc_attr(self.get_field_id("title")))
        php_print("\">")
        _e("Title:")
        php_print("</label>\n           <input class=\"widefat\" id=\"")
        php_print(esc_attr(self.get_field_id("title")))
        php_print("\" name=\"")
        php_print(esc_attr(self.get_field_name("title")))
        php_print("\" type=\"text\" value=\"")
        php_print(esc_attr(instance_["title"]))
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
        selected(instance_["sortby"], "post_title")
        php_print(">")
        _e("Page title")
        php_print("</option>\n              <option value=\"menu_order\"")
        selected(instance_["sortby"], "menu_order")
        php_print(">")
        _e("Page order")
        php_print("</option>\n              <option value=\"ID\"")
        selected(instance_["sortby"], "ID")
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
        php_print(esc_attr(instance_["exclude"]))
        php_print("\" name=\"")
        php_print(esc_attr(self.get_field_name("exclude")))
        php_print("\" id=\"")
        php_print(esc_attr(self.get_field_id("exclude")))
        php_print("\" class=\"widefat\" />\n            <br />\n            <small>")
        _e("Page IDs, separated by commas.")
        php_print("</small>\n       </p>\n      ")
    # end def form
# end class WP_Widget_Pages
