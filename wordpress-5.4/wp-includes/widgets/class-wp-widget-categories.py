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
#// Widget API: WP_Widget_Categories class
#// 
#// @package WordPress
#// @subpackage Widgets
#// @since 4.4.0
#// 
#// 
#// Core class used to implement a Categories widget.
#// 
#// @since 2.8.0
#// 
#// @see WP_Widget
#//
class WP_Widget_Categories(WP_Widget):
    #// 
    #// Sets up a new Categories widget instance.
    #// 
    #// @since 2.8.0
    #//
    def __init__(self):
        
        widget_ops = Array({"classname": "widget_categories", "description": __("A list or dropdown of categories."), "customize_selective_refresh": True})
        super().__init__("categories", __("Categories"), widget_ops)
    # end def __init__
    #// 
    #// Outputs the content for the current Categories widget instance.
    #// 
    #// @since 2.8.0
    #// @since 4.2.0 Creates a unique HTML ID for the `<select>` element
    #// if more than one instance is displayed on the page.
    #// 
    #// @staticvar bool $first_dropdown
    #// 
    #// @param array $args     Display arguments including 'before_title', 'after_title',
    #// 'before_widget', and 'after_widget'.
    #// @param array $instance Settings for the current Categories widget instance.
    #//
    def widget(self, args=None, instance=None):
        
        first_dropdown = True
        title = instance["title"] if (not php_empty(lambda : instance["title"])) else __("Categories")
        #// This filter is documented in wp-includes/widgets/class-wp-widget-pages.php
        title = apply_filters("widget_title", title, instance, self.id_base)
        count = "1" if (not php_empty(lambda : instance["count"])) else "0"
        hierarchical = "1" if (not php_empty(lambda : instance["hierarchical"])) else "0"
        dropdown = "1" if (not php_empty(lambda : instance["dropdown"])) else "0"
        php_print(args["before_widget"])
        if title:
            php_print(args["before_title"] + title + args["after_title"])
        # end if
        cat_args = Array({"orderby": "name", "show_count": count, "hierarchical": hierarchical})
        if dropdown:
            php_print(php_sprintf("<form action=\"%s\" method=\"get\">", esc_url(home_url())))
            dropdown_id = "cat" if first_dropdown else str(self.id_base) + str("-dropdown-") + str(self.number)
            first_dropdown = False
            php_print("<label class=\"screen-reader-text\" for=\"" + esc_attr(dropdown_id) + "\">" + title + "</label>")
            cat_args["show_option_none"] = __("Select Category")
            cat_args["id"] = dropdown_id
            #// 
            #// Filters the arguments for the Categories widget drop-down.
            #// 
            #// @since 2.8.0
            #// @since 4.9.0 Added the `$instance` parameter.
            #// 
            #// @see wp_dropdown_categories()
            #// 
            #// @param array $cat_args An array of Categories widget drop-down arguments.
            #// @param array $instance Array of settings for the current widget.
            #//
            wp_dropdown_categories(apply_filters("widget_categories_dropdown_args", cat_args, instance))
            php_print("</form>")
            type_attr = "" if current_theme_supports("html5", "script") else " type=\"text/javascript\""
            php_print("\n<script")
            php_print(type_attr)
            php_print(""">
            /* <![CDATA[ */
            (function() {
            var dropdown = document.getElementById( \"""")
            php_print(esc_js(dropdown_id))
            php_print("""\" );
            function onCatChange() {
        if ( dropdown.options[ dropdown.selectedIndex ].value > 0 ) {
            dropdown.parentNode.submit();
            }
            }
            dropdown.onchange = onCatChange;
            })();
            /* ]]> */
            </script>
            """)
        else:
            php_print("     <ul>\n          ")
            cat_args["title_li"] = ""
            #// 
            #// Filters the arguments for the Categories widget.
            #// 
            #// @since 2.8.0
            #// @since 4.9.0 Added the `$instance` parameter.
            #// 
            #// @param array $cat_args An array of Categories widget options.
            #// @param array $instance Array of settings for the current widget.
            #//
            wp_list_categories(apply_filters("widget_categories_args", cat_args, instance))
            php_print("     </ul>\n         ")
        # end if
        php_print(args["after_widget"])
    # end def widget
    #// 
    #// Handles updating settings for the current Categories widget instance.
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
        instance["count"] = 1 if (not php_empty(lambda : new_instance["count"])) else 0
        instance["hierarchical"] = 1 if (not php_empty(lambda : new_instance["hierarchical"])) else 0
        instance["dropdown"] = 1 if (not php_empty(lambda : new_instance["dropdown"])) else 0
        return instance
    # end def update
    #// 
    #// Outputs the settings form for the Categories widget.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $instance Current settings.
    #//
    def form(self, instance=None):
        
        #// Defaults.
        instance = wp_parse_args(instance, Array({"title": ""}))
        count = php_bool(instance["count"]) if (php_isset(lambda : instance["count"])) else False
        hierarchical = php_bool(instance["hierarchical"]) if (php_isset(lambda : instance["hierarchical"])) else False
        dropdown = php_bool(instance["dropdown"]) if (php_isset(lambda : instance["dropdown"])) else False
        php_print("     <p><label for=\"")
        php_print(self.get_field_id("title"))
        php_print("\">")
        _e("Title:")
        php_print("</label>\n       <input class=\"widefat\" id=\"")
        php_print(self.get_field_id("title"))
        php_print("\" name=\"")
        php_print(self.get_field_name("title"))
        php_print("\" type=\"text\" value=\"")
        php_print(esc_attr(instance["title"]))
        php_print("\" /></p>\n\n        <p><input type=\"checkbox\" class=\"checkbox\" id=\"")
        php_print(self.get_field_id("dropdown"))
        php_print("\" name=\"")
        php_print(self.get_field_name("dropdown"))
        php_print("\"")
        checked(dropdown)
        php_print(" />\n        <label for=\"")
        php_print(self.get_field_id("dropdown"))
        php_print("\">")
        _e("Display as dropdown")
        php_print("</label><br />\n\n       <input type=\"checkbox\" class=\"checkbox\" id=\"")
        php_print(self.get_field_id("count"))
        php_print("\" name=\"")
        php_print(self.get_field_name("count"))
        php_print("\"")
        checked(count)
        php_print(" />\n        <label for=\"")
        php_print(self.get_field_id("count"))
        php_print("\">")
        _e("Show post counts")
        php_print("</label><br />\n\n       <input type=\"checkbox\" class=\"checkbox\" id=\"")
        php_print(self.get_field_id("hierarchical"))
        php_print("\" name=\"")
        php_print(self.get_field_name("hierarchical"))
        php_print("\"")
        checked(hierarchical)
        php_print(" />\n        <label for=\"")
        php_print(self.get_field_id("hierarchical"))
        php_print("\">")
        _e("Show hierarchy")
        php_print("</label></p>\n       ")
    # end def form
# end class WP_Widget_Categories
