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
        
        
        widget_ops_ = Array({"classname": "widget_recent_comments", "description": __("Your site&#8217;s most recent comments."), "customize_selective_refresh": True})
        super().__init__("recent-comments", __("Recent Comments"), widget_ops_)
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
        type_attr_ = "" if current_theme_supports("html5", "style") else " type=\"text/css\""
        php_printf("<style%s>.recentcomments a{display:inline !important;padding:0 !important;margin:0 !important;}</style>", type_attr_)
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
    def widget(self, args_=None, instance_=None):
        
        
        first_instance_ = True
        if (not (php_isset(lambda : args_["widget_id"]))):
            args_["widget_id"] = self.id
        # end if
        output_ = ""
        title_ = instance_["title"] if (not php_empty(lambda : instance_["title"])) else __("Recent Comments")
        #// This filter is documented in wp-includes/widgets/class-wp-widget-pages.php
        title_ = apply_filters("widget_title", title_, instance_, self.id_base)
        number_ = absint(instance_["number"]) if (not php_empty(lambda : instance_["number"])) else 5
        if (not number_):
            number_ = 5
        # end if
        comments_ = get_comments(apply_filters("widget_comments_args", Array({"number": number_, "status": "approve", "post_status": "publish"}), instance_))
        output_ += args_["before_widget"]
        if title_:
            output_ += args_["before_title"] + title_ + args_["after_title"]
        # end if
        recent_comments_id_ = "recentcomments" if first_instance_ else str("recentcomments-") + str(self.number)
        first_instance_ = False
        output_ += "<ul id=\"" + esc_attr(recent_comments_id_) + "\">"
        if php_is_array(comments_) and comments_:
            #// Prime cache for associated posts. (Prime post term cache if we need it for permalinks.)
            post_ids_ = array_unique(wp_list_pluck(comments_, "comment_post_ID"))
            _prime_post_caches(post_ids_, php_strpos(get_option("permalink_structure"), "%category%"), False)
            for comment_ in comments_:
                output_ += "<li class=\"recentcomments\">"
                output_ += php_sprintf(_x("%1$s on %2$s", "widgets"), "<span class=\"comment-author-link\">" + get_comment_author_link(comment_) + "</span>", "<a href=\"" + esc_url(get_comment_link(comment_)) + "\">" + get_the_title(comment_.comment_post_ID) + "</a>")
                output_ += "</li>"
            # end for
        # end if
        output_ += "</ul>"
        output_ += args_["after_widget"]
        php_print(output_)
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
    def update(self, new_instance_=None, old_instance_=None):
        
        
        instance_ = old_instance_
        instance_["title"] = sanitize_text_field(new_instance_["title"])
        instance_["number"] = absint(new_instance_["number"])
        return instance_
    # end def update
    #// 
    #// Outputs the settings form for the Recent Comments widget.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $instance Current settings.
    #//
    def form(self, instance_=None):
        
        
        title_ = instance_["title"] if (php_isset(lambda : instance_["title"])) else ""
        number_ = absint(instance_["number"]) if (php_isset(lambda : instance_["number"])) else 5
        php_print("     <p><label for=\"")
        php_print(self.get_field_id("title"))
        php_print("\">")
        _e("Title:")
        php_print("</label>\n       <input class=\"widefat\" id=\"")
        php_print(self.get_field_id("title"))
        php_print("\" name=\"")
        php_print(self.get_field_name("title"))
        php_print("\" type=\"text\" value=\"")
        php_print(esc_attr(title_))
        php_print("\" /></p>\n\n        <p><label for=\"")
        php_print(self.get_field_id("number"))
        php_print("\">")
        _e("Number of comments to show:")
        php_print("</label>\n       <input class=\"tiny-text\" id=\"")
        php_print(self.get_field_id("number"))
        php_print("\" name=\"")
        php_print(self.get_field_name("number"))
        php_print("\" type=\"number\" step=\"1\" min=\"1\" value=\"")
        php_print(number_)
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
        
        
        _deprecated_function(inspect.currentframe().f_code.co_name, "4.4.0")
    # end def flush_widget_cache
# end class WP_Widget_Recent_Comments
