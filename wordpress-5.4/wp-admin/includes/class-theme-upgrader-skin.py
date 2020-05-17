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
#// Upgrader API: Theme_Upgrader_Skin class
#// 
#// @package WordPress
#// @subpackage Upgrader
#// @since 4.6.0
#// 
#// 
#// Theme Upgrader Skin for WordPress Theme Upgrades.
#// 
#// @since 2.8.0
#// @since 4.6.0 Moved to its own file from wp-admin/includes/class-wp-upgrader-skins.php.
#// 
#// @see WP_Upgrader_Skin
#//
class Theme_Upgrader_Skin(WP_Upgrader_Skin):
    theme = ""
    #// 
    #// @param array $args
    #//
    def __init__(self, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        defaults_ = Array({"url": "", "theme": "", "nonce": "", "title": __("Update Theme")})
        args_ = wp_parse_args(args_, defaults_)
        self.theme = args_["theme"]
        super().__init__(args_)
    # end def __init__
    #// 
    #//
    def after(self):
        
        
        self.decrement_update_count("theme")
        update_actions_ = Array()
        theme_info_ = self.upgrader.theme_info()
        if theme_info_:
            name_ = theme_info_.display("Name")
            stylesheet_ = self.upgrader.result["destination_name"]
            template_ = theme_info_.get_template()
            activate_link_ = add_query_arg(Array({"action": "activate", "template": urlencode(template_), "stylesheet": urlencode(stylesheet_)}), admin_url("themes.php"))
            activate_link_ = wp_nonce_url(activate_link_, "switch-theme_" + stylesheet_)
            customize_url_ = add_query_arg(Array({"theme": urlencode(stylesheet_), "return": urlencode(admin_url("themes.php"))}), admin_url("customize.php"))
            if get_stylesheet() == stylesheet_:
                if current_user_can("edit_theme_options") and current_user_can("customize"):
                    update_actions_["preview"] = php_sprintf("<a href=\"%s\" class=\"hide-if-no-customize load-customize\">" + "<span aria-hidden=\"true\">%s</span><span class=\"screen-reader-text\">%s</span></a>", esc_url(customize_url_), __("Customize"), php_sprintf(__("Customize &#8220;%s&#8221;"), name_))
                # end if
            elif current_user_can("switch_themes"):
                if current_user_can("edit_theme_options") and current_user_can("customize"):
                    update_actions_["preview"] = php_sprintf("<a href=\"%s\" class=\"hide-if-no-customize load-customize\">" + "<span aria-hidden=\"true\">%s</span><span class=\"screen-reader-text\">%s</span></a>", esc_url(customize_url_), __("Live Preview"), php_sprintf(__("Live Preview &#8220;%s&#8221;"), name_))
                # end if
                update_actions_["activate"] = php_sprintf("<a href=\"%s\" class=\"activatelink\">" + "<span aria-hidden=\"true\">%s</span><span class=\"screen-reader-text\">%s</span></a>", esc_url(activate_link_), __("Activate"), php_sprintf(__("Activate &#8220;%s&#8221;"), name_))
            # end if
            if (not self.result) or is_wp_error(self.result) or is_network_admin():
                update_actions_["preview"] = None
                update_actions_["activate"] = None
            # end if
        # end if
        update_actions_["themes_page"] = php_sprintf("<a href=\"%s\" target=\"_parent\">%s</a>", self_admin_url("themes.php"), __("Return to Themes page"))
        #// 
        #// Filters the list of action links available following a single theme update.
        #// 
        #// @since 2.8.0
        #// 
        #// @param string[] $update_actions Array of theme action links.
        #// @param string   $theme          Theme directory name.
        #//
        update_actions_ = apply_filters("update_theme_complete_actions", update_actions_, self.theme)
        if (not php_empty(lambda : update_actions_)):
            self.feedback(php_implode(" | ", update_actions_))
        # end if
    # end def after
# end class Theme_Upgrader_Skin
