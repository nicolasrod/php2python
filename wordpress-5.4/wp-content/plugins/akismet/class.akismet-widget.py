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
#// @package Akismet
#//
class Akismet_Widget(WP_Widget):
    def __init__(self):
        
        load_plugin_textdomain("akismet")
        super().__init__("akismet_widget", __("Akismet Widget", "akismet"), Array({"description": __("Display the number of spam comments Akismet has caught", "akismet")}))
        if is_active_widget(False, False, self.id_base):
            add_action("wp_head", Array(self, "css"))
        # end if
    # end def __init__
    def css(self):
        
        php_print("""
        <style type=\"text/css\">
        .a-stats {
        width: auto;
        }
        .a-stats a {
        background: #7CA821;
        background-image:-moz-linear-gradient(0% 100% 90deg,#5F8E14,#7CA821);
        background-image:-webkit-gradient(linear,0% 0,0% 100%,from(#7CA821),to(#5F8E14));
        border: 1px solid #5F8E14;
        border-radius:3px;
        color: #CFEA93;
        cursor: pointer;
        display: block;
        font-weight: normal;
        height: 100%;
        -moz-border-radius:3px;
        padding: 7px 0 8px;
        text-align: center;
        text-decoration: none;
        -webkit-border-radius:3px;
        width: 100%;
        }
        .a-stats a:hover {
        text-decoration: none;
        background-image:-moz-linear-gradient(0% 100% 90deg,#6F9C1B,#659417);
        background-image:-webkit-gradient(linear,0% 0,0% 100%,from(#659417),to(#6F9C1B));
        }
        .a-stats .count {
        color: #FFF;
        display: block;
        font-size: 15px;
        line-height: 16px;
        padding: 0 13px;
        white-space: nowrap;
        }
        </style>
        """)
    # end def css
    def form(self, instance=None):
        
        if instance and (php_isset(lambda : instance["title"])):
            title = instance["title"]
        else:
            title = __("Spam Blocked", "akismet")
        # end if
        php_print("\n       <p>\n       <label for=\"")
        php_print(self.get_field_id("title"))
        php_print("\">")
        esc_html_e("Title:", "akismet")
        php_print("</label>\n       <input class=\"widefat\" id=\"")
        php_print(self.get_field_id("title"))
        php_print("\" name=\"")
        php_print(self.get_field_name("title"))
        php_print("\" type=\"text\" value=\"")
        php_print(esc_attr(title))
        php_print("""\" />
        </p>
        """)
    # end def form
    def update(self, new_instance=None, old_instance=None):
        
        instance["title"] = strip_tags(new_instance["title"])
        return instance
    # end def update
    def widget(self, args=None, instance=None):
        
        count = get_option("akismet_spam_count")
        if (not (php_isset(lambda : instance["title"]))):
            instance["title"] = __("Spam Blocked", "akismet")
        # end if
        php_print(args["before_widget"])
        if (not php_empty(lambda : instance["title"])):
            php_print(args["before_title"])
            php_print(esc_html(instance["title"]))
            php_print(args["after_title"])
        # end if
        php_print("\n   <div class=\"a-stats\">\n       <a href=\"https://akismet.com\" target=\"_blank\" title=\"\">")
        printf(_n("<strong class=\"count\">%1$s spam</strong> blocked by <strong>Akismet</strong>", "<strong class=\"count\">%1$s spam</strong> blocked by <strong>Akismet</strong>", count, "akismet"), number_format_i18n(count))
        php_print("""</a>
        </div>
        """)
        php_print(args["after_widget"])
    # end def widget
# end class Akismet_Widget
def akismet_register_widgets(*args_):
    
    register_widget("Akismet_Widget")
# end def akismet_register_widgets
add_action("widgets_init", "akismet_register_widgets")
