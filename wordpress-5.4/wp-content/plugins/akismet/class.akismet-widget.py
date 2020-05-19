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
    def form(self, instance_=None):
        
        
        if instance_ and (php_isset(lambda : instance_["title"])):
            title_ = instance_["title"]
        else:
            title_ = __("Spam Blocked", "akismet")
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
        php_print(esc_attr(title_))
        php_print("""\" />
        </p>
        """)
    # end def form
    def update(self, new_instance_=None, old_instance_=None):
        
        
        instance_["title"] = strip_tags(new_instance_["title"])
        return instance_
    # end def update
    def widget(self, args_=None, instance_=None):
        
        
        count_ = get_option("akismet_spam_count")
        if (not (php_isset(lambda : instance_["title"]))):
            instance_["title"] = __("Spam Blocked", "akismet")
        # end if
        php_print(args_["before_widget"])
        if (not php_empty(lambda : instance_["title"])):
            php_print(args_["before_title"])
            php_print(esc_html(instance_["title"]))
            php_print(args_["after_title"])
        # end if
        php_print("\n   <div class=\"a-stats\">\n       <a href=\"https://akismet.com\" target=\"_blank\" title=\"\">")
        php_printf(_n("<strong class=\"count\">%1$s spam</strong> blocked by <strong>Akismet</strong>", "<strong class=\"count\">%1$s spam</strong> blocked by <strong>Akismet</strong>", count_, "akismet"), number_format_i18n(count_))
        php_print("""</a>
        </div>
        """)
        php_print(args_["after_widget"])
    # end def widget
# end class Akismet_Widget
def akismet_register_widgets(*_args_):
    
    
    register_widget("Akismet_Widget")
# end def akismet_register_widgets
add_action("widgets_init", "akismet_register_widgets")
