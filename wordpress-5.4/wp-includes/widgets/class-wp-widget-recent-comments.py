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
#// Widget API: WP_Widget_Recent_Comments class
#// 
#// @package WordPress
#// @subpackage Widgets
#// @since 4.4.0
#// 
#// 
#// Core class used to implement a Recent Comments widget.
#// 
#// @since 2.8.0
#// 
#// @see WP_Widget
#//
class WP_Widget_Recent_Comments(WP_Widget):
    #// 
    #// Sets up a new Recent Comments widget instance.
    #// 
    #// @since 2.8.0
    #//
    def __init__(self):
        
        widget_ops = Array({"classname": "widget_recent_comments", "description": __("Your site&#8217;s most recent comments."), "customize_selective_refresh": True})
        super().__init__("recent-comments", __("Recent Comments"), widget_ops)
        self.alt_option_name = "widget_recent_comments"
        if is_active_widget(False, False, self.id_base) or is_customize_preview():
            add_action("wp_head", Array(self, "recent_comments_style"))
        # end if
    # end def __init__
    #// 
    #// Outputs the default styles for the Recent Comments widget.
    #// 
    #// @since 2.8.0
    #//
    def recent_comments_style(self):
        
        #// 
        #// Filters the Recent Comments default widget styles.
        #// 
        #// @since 3.1.0
        #// 
        #// @param bool   $active  Whether the widget is active. Default true.
        #// @param string $id_base The widget ID.
        #//
        if (not current_theme_supports("widgets")) or (not apply_filters("show_recent_comments_widget_style", True, self.id_base)):
            return
        # end if
        type_attr = "" if current_theme_supports("html5", "style") else " type=\"text/css\""
        printf("<style%s>.recentcomments a{display:inline !important;padding:0 !important;margin:0 !important;}</style>", type_attr)
    # end def recent_comments_style
    #// 
    #// Outputs the content for the current Recent Comments widget instance.
    #// 
    #// @since 2.8.0
    #// @since 5.4.0 Creates a unique HTML ID for the `<ul>` element
    #// if more than one instance is displayed on the page.
    #// 
    #// @staticvar bool $first_instance
    #// 
    #// @param array $args     Display arguments including 'before_title', 'after_title',
    #// 'before_widget', and 'after_widget'.
    #// @param array $instance Settings for the current Recent Comments widget instance.
    #//
    def widget(self, args=None, instance=None):
        
        first_instance = True
        if (not (php_isset(lambda : args["widget_id"]))):
            args["widget_id"] = self.id
        # end if
        output = ""
        title = instance["title"] if (not php_empty(lambda : instance["title"])) else __("Recent Comments")
        #// This filter is documented in wp-includes/widgets/class-wp-widget-pages.php
        title = apply_filters("widget_title", title, instance, self.id_base)
        number = absint(instance["number"]) if (not php_empty(lambda : instance["number"])) else 5
        if (not number):
            number = 5
        # end if
        comments = get_comments(apply_filters("widget_comments_args", Array({"number": number, "status": "approve", "post_status": "publish"}), instance))
        output += args["before_widget"]
        if title:
            output += args["before_title"] + title + args["after_title"]
        # end if
        recent_comments_id = "recentcomments" if first_instance else str("recentcomments-") + str(self.number)
        first_instance = False
        output += "<ul id=\"" + esc_attr(recent_comments_id) + "\">"
        if php_is_array(comments) and comments:
            #// Prime cache for associated posts. (Prime post term cache if we need it for permalinks.)
            post_ids = array_unique(wp_list_pluck(comments, "comment_post_ID"))
            _prime_post_caches(post_ids, php_strpos(get_option("permalink_structure"), "%category%"), False)
            for comment in comments:
                output += "<li class=\"recentcomments\">"
                output += php_sprintf(_x("%1$s on %2$s", "widgets"), "<span class=\"comment-author-link\">" + get_comment_author_link(comment) + "</span>", "<a href=\"" + esc_url(get_comment_link(comment)) + "\">" + get_the_title(comment.comment_post_ID) + "</a>")
                output += "</li>"
            # end for
        # end if
        output += "</ul>"
        output += args["after_widget"]
        php_print(output)
    # end def widget
    #// 
    #// Handles updating settings for the current Recent Comments widget instance.
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
        instance["number"] = absint(new_instance["number"])
        return instance
    # end def update
    #// 
    #// Outputs the settings form for the Recent Comments widget.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $instance Current settings.
    #//
    def form(self, instance=None):
        
        title = instance["title"] if (php_isset(lambda : instance["title"])) else ""
        number = absint(instance["number"]) if (php_isset(lambda : instance["number"])) else 5
        php_print("     <p><label for=\"")
        php_print(self.get_field_id("title"))
        php_print("\">")
        _e("Title:")
        php_print("</label>\n       <input class=\"widefat\" id=\"")
        php_print(self.get_field_id("title"))
        php_print("\" name=\"")
        php_print(self.get_field_name("title"))
        php_print("\" type=\"text\" value=\"")
        php_print(esc_attr(title))
        php_print("\" /></p>\n\n        <p><label for=\"")
        php_print(self.get_field_id("number"))
        php_print("\">")
        _e("Number of comments to show:")
        php_print("</label>\n       <input class=\"tiny-text\" id=\"")
        php_print(self.get_field_id("number"))
        php_print("\" name=\"")
        php_print(self.get_field_name("number"))
        php_print("\" type=\"number\" step=\"1\" min=\"1\" value=\"")
        php_print(number)
        php_print("\" size=\"3\" /></p>\n       ")
    # end def form
    #// 
    #// Flushes the Recent Comments widget cache.
    #// 
    #// @since 2.8.0
    #// 
    #// @deprecated 4.4.0 Fragment caching was removed in favor of split queries.
    #//
    def flush_widget_cache(self):
        
        _deprecated_function(__METHOD__, "4.4.0")
    # end def flush_widget_cache
# end class WP_Widget_Recent_Comments
