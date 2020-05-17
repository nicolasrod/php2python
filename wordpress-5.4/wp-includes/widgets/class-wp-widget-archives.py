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
        
        
        widget_ops_ = Array({"classname": "widget_archive", "description": __("A monthly archive of your site&#8217;s Posts."), "customize_selective_refresh": True})
        super().__init__("archives", __("Archives"), widget_ops_)
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
    def widget(self, args_=None, instance_=None):
        
        
        title_ = instance_["title"] if (not php_empty(lambda : instance_["title"])) else __("Archives")
        #// This filter is documented in wp-includes/widgets/class-wp-widget-pages.php
        title_ = apply_filters("widget_title", title_, instance_, self.id_base)
        count_ = "1" if (not php_empty(lambda : instance_["count"])) else "0"
        dropdown_ = "1" if (not php_empty(lambda : instance_["dropdown"])) else "0"
        php_print(args_["before_widget"])
        if title_:
            php_print(args_["before_title"] + title_ + args_["after_title"])
        # end if
        if dropdown_:
            dropdown_id_ = str(self.id_base) + str("-dropdown-") + str(self.number)
            php_print("     <label class=\"screen-reader-text\" for=\"")
            php_print(esc_attr(dropdown_id_))
            php_print("\">")
            php_print(title_)
            php_print("</label>\n       <select id=\"")
            php_print(esc_attr(dropdown_id_))
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
            dropdown_args_ = apply_filters("widget_archives_dropdown_args", Array({"type": "monthly", "format": "option", "show_post_count": count_}), instance_)
            for case in Switch(dropdown_args_["type"]):
                if case("yearly"):
                    label_ = __("Select Year")
                    break
                # end if
                if case("monthly"):
                    label_ = __("Select Month")
                    break
                # end if
                if case("daily"):
                    label_ = __("Select Day")
                    break
                # end if
                if case("weekly"):
                    label_ = __("Select Week")
                    break
                # end if
                if case():
                    label_ = __("Select Post")
                    break
                # end if
            # end for
            type_attr_ = "" if current_theme_supports("html5", "script") else " type=\"text/javascript\""
            php_print("\n           <option value=\"\">")
            php_print(esc_attr(label_))
            php_print("</option>\n          ")
            wp_get_archives(dropdown_args_)
            php_print("""
            </select>
            <script""")
            php_print(type_attr_)
            php_print(""">
            /* <![CDATA[ */
            (function() {
            var dropdown = document.getElementById( \"""")
            php_print(esc_js(dropdown_id_))
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
            wp_get_archives(apply_filters("widget_archives_args", Array({"type": "monthly", "show_post_count": count_}), instance_))
            php_print("     </ul>\n         ")
        # end if
        php_print(args_["after_widget"])
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
    def update(self, new_instance_=None, old_instance_=None):
        
        
        instance_ = old_instance_
        new_instance_ = wp_parse_args(new_instance_, Array({"title": "", "count": 0, "dropdown": ""}))
        instance_["title"] = sanitize_text_field(new_instance_["title"])
        instance_["count"] = 1 if new_instance_["count"] else 0
        instance_["dropdown"] = 1 if new_instance_["dropdown"] else 0
        return instance_
    # end def update
    #// 
    #// Outputs the settings form for the Archives widget.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $instance Current settings.
    #//
    def form(self, instance_=None):
        
        
        instance_ = wp_parse_args(instance_, Array({"title": "", "count": 0, "dropdown": ""}))
        php_print("     <p><label for=\"")
        php_print(self.get_field_id("title"))
        php_print("\">")
        _e("Title:")
        php_print("</label> <input class=\"widefat\" id=\"")
        php_print(self.get_field_id("title"))
        php_print("\" name=\"")
        php_print(self.get_field_name("title"))
        php_print("\" type=\"text\" value=\"")
        php_print(esc_attr(instance_["title"]))
        php_print("\" /></p>\n      <p>\n           <input class=\"checkbox\" type=\"checkbox\"")
        checked(instance_["dropdown"])
        php_print(" id=\"")
        php_print(self.get_field_id("dropdown"))
        php_print("\" name=\"")
        php_print(self.get_field_name("dropdown"))
        php_print("\" /> <label for=\"")
        php_print(self.get_field_id("dropdown"))
        php_print("\">")
        _e("Display as dropdown")
        php_print("</label>\n           <br/>\n         <input class=\"checkbox\" type=\"checkbox\"")
        checked(instance_["count"])
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
