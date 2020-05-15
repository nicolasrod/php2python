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
#// Widget API: WP_Widget_Archives class
#// 
#// @package WordPress
#// @subpackage Widgets
#// @since 4.4.0
#// 
#// 
#// Core class used to implement the Archives widget.
#// 
#// @since 2.8.0
#// 
#// @see WP_Widget
#//
class WP_Widget_Archives(WP_Widget):
    #// 
    #// Sets up a new Archives widget instance.
    #// 
    #// @since 2.8.0
    #//
    def __init__(self):
        
        widget_ops = Array({"classname": "widget_archive", "description": __("A monthly archive of your site&#8217;s Posts."), "customize_selective_refresh": True})
        super().__init__("archives", __("Archives"), widget_ops)
    # end def __init__
    #// 
    #// Outputs the content for the current Archives widget instance.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $args     Display arguments including 'before_title', 'after_title',
    #// 'before_widget', and 'after_widget'.
    #// @param array $instance Settings for the current Archives widget instance.
    #//
    def widget(self, args=None, instance=None):
        
        title = instance["title"] if (not php_empty(lambda : instance["title"])) else __("Archives")
        #// This filter is documented in wp-includes/widgets/class-wp-widget-pages.php
        title = apply_filters("widget_title", title, instance, self.id_base)
        count = "1" if (not php_empty(lambda : instance["count"])) else "0"
        dropdown = "1" if (not php_empty(lambda : instance["dropdown"])) else "0"
        php_print(args["before_widget"])
        if title:
            php_print(args["before_title"] + title + args["after_title"])
        # end if
        if dropdown:
            dropdown_id = str(self.id_base) + str("-dropdown-") + str(self.number)
            php_print("     <label class=\"screen-reader-text\" for=\"")
            php_print(esc_attr(dropdown_id))
            php_print("\">")
            php_print(title)
            php_print("</label>\n       <select id=\"")
            php_print(esc_attr(dropdown_id))
            php_print("\" name=\"archive-dropdown\">\n          ")
            #// 
            #// Filters the arguments for the Archives widget drop-down.
            #// 
            #// @since 2.8.0
            #// @since 4.9.0 Added the `$instance` parameter.
            #// 
            #// @see wp_get_archives()
            #// 
            #// @param array $args     An array of Archives widget drop-down arguments.
            #// @param array $instance Settings for the current Archives widget instance.
            #//
            dropdown_args = apply_filters("widget_archives_dropdown_args", Array({"type": "monthly", "format": "option", "show_post_count": count}), instance)
            for case in Switch(dropdown_args["type"]):
                if case("yearly"):
                    label = __("Select Year")
                    break
                # end if
                if case("monthly"):
                    label = __("Select Month")
                    break
                # end if
                if case("daily"):
                    label = __("Select Day")
                    break
                # end if
                if case("weekly"):
                    label = __("Select Week")
                    break
                # end if
                if case():
                    label = __("Select Post")
                    break
                # end if
            # end for
            type_attr = "" if current_theme_supports("html5", "script") else " type=\"text/javascript\""
            php_print("\n           <option value=\"\">")
            php_print(esc_attr(label))
            php_print("</option>\n          ")
            wp_get_archives(dropdown_args)
            php_print("""
            </select>
            <script""")
            php_print(type_attr)
            php_print(""">
            /* <![CDATA[ */
            (function() {
            var dropdown = document.getElementById( \"""")
            php_print(esc_js(dropdown_id))
            php_print("""\" );
            function onSelectChange() {
        if ( dropdown.options[ dropdown.selectedIndex ].value !== '' ) {
            document.location.href = this.options[ this.selectedIndex ].value;
            }
            }
            dropdown.onchange = onSelectChange;
            })();
            /* ]]> */
            </script>
            """)
        else:
            php_print("     <ul>\n          ")
            wp_get_archives(apply_filters("widget_archives_args", Array({"type": "monthly", "show_post_count": count}), instance))
            php_print("     </ul>\n         ")
        # end if
        php_print(args["after_widget"])
    # end def widget
    #// 
    #// Handles updating settings for the current Archives widget instance.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $new_instance New settings for this instance as input by the user via
    #// WP_Widget_Archives::form().
    #// @param array $old_instance Old settings for this instance.
    #// @return array Updated settings to save.
    #//
    def update(self, new_instance=None, old_instance=None):
        
        instance = old_instance
        new_instance = wp_parse_args(new_instance, Array({"title": "", "count": 0, "dropdown": ""}))
        instance["title"] = sanitize_text_field(new_instance["title"])
        instance["count"] = 1 if new_instance["count"] else 0
        instance["dropdown"] = 1 if new_instance["dropdown"] else 0
        return instance
    # end def update
    #// 
    #// Outputs the settings form for the Archives widget.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $instance Current settings.
    #//
    def form(self, instance=None):
        
        instance = wp_parse_args(instance, Array({"title": "", "count": 0, "dropdown": ""}))
        php_print("     <p><label for=\"")
        php_print(self.get_field_id("title"))
        php_print("\">")
        _e("Title:")
        php_print("</label> <input class=\"widefat\" id=\"")
        php_print(self.get_field_id("title"))
        php_print("\" name=\"")
        php_print(self.get_field_name("title"))
        php_print("\" type=\"text\" value=\"")
        php_print(esc_attr(instance["title"]))
        php_print("\" /></p>\n      <p>\n           <input class=\"checkbox\" type=\"checkbox\"")
        checked(instance["dropdown"])
        php_print(" id=\"")
        php_print(self.get_field_id("dropdown"))
        php_print("\" name=\"")
        php_print(self.get_field_name("dropdown"))
        php_print("\" /> <label for=\"")
        php_print(self.get_field_id("dropdown"))
        php_print("\">")
        _e("Display as dropdown")
        php_print("</label>\n           <br/>\n         <input class=\"checkbox\" type=\"checkbox\"")
        checked(instance["count"])
        php_print(" id=\"")
        php_print(self.get_field_id("count"))
        php_print("\" name=\"")
        php_print(self.get_field_name("count"))
        php_print("\" /> <label for=\"")
        php_print(self.get_field_id("count"))
        php_print("\">")
        _e("Show post counts")
        php_print("</label>\n       </p>\n      ")
    # end def form
# end class WP_Widget_Archives
