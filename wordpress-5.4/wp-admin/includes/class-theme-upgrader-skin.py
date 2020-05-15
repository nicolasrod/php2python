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
    def __init__(self, args=Array()):
        
        defaults = Array({"url": "", "theme": "", "nonce": "", "title": __("Update Theme")})
        args = wp_parse_args(args, defaults)
        self.theme = args["theme"]
        super().__init__(args)
    # end def __init__
    #// 
    #//
    def after(self):
        
        self.decrement_update_count("theme")
        update_actions = Array()
        theme_info = self.upgrader.theme_info()
        if theme_info:
            name = theme_info.display("Name")
            stylesheet = self.upgrader.result["destination_name"]
            template = theme_info.get_template()
            activate_link = add_query_arg(Array({"action": "activate", "template": urlencode(template), "stylesheet": urlencode(stylesheet)}), admin_url("themes.php"))
            activate_link = wp_nonce_url(activate_link, "switch-theme_" + stylesheet)
            customize_url = add_query_arg(Array({"theme": urlencode(stylesheet), "return": urlencode(admin_url("themes.php"))}), admin_url("customize.php"))
            if get_stylesheet() == stylesheet:
                if current_user_can("edit_theme_options") and current_user_can("customize"):
                    update_actions["preview"] = php_sprintf("<a href=\"%s\" class=\"hide-if-no-customize load-customize\">" + "<span aria-hidden=\"true\">%s</span><span class=\"screen-reader-text\">%s</span></a>", esc_url(customize_url), __("Customize"), php_sprintf(__("Customize &#8220;%s&#8221;"), name))
                # end if
            elif current_user_can("switch_themes"):
                if current_user_can("edit_theme_options") and current_user_can("customize"):
                    update_actions["preview"] = php_sprintf("<a href=\"%s\" class=\"hide-if-no-customize load-customize\">" + "<span aria-hidden=\"true\">%s</span><span class=\"screen-reader-text\">%s</span></a>", esc_url(customize_url), __("Live Preview"), php_sprintf(__("Live Preview &#8220;%s&#8221;"), name))
                # end if
                update_actions["activate"] = php_sprintf("<a href=\"%s\" class=\"activatelink\">" + "<span aria-hidden=\"true\">%s</span><span class=\"screen-reader-text\">%s</span></a>", esc_url(activate_link), __("Activate"), php_sprintf(__("Activate &#8220;%s&#8221;"), name))
            # end if
            if (not self.result) or is_wp_error(self.result) or is_network_admin():
                update_actions["preview"] = None
                update_actions["activate"] = None
            # end if
        # end if
        update_actions["themes_page"] = php_sprintf("<a href=\"%s\" target=\"_parent\">%s</a>", self_admin_url("themes.php"), __("Return to Themes page"))
        #// 
        #// Filters the list of action links available following a single theme update.
        #// 
        #// @since 2.8.0
        #// 
        #// @param string[] $update_actions Array of theme action links.
        #// @param string   $theme          Theme directory name.
        #//
        update_actions = apply_filters("update_theme_complete_actions", update_actions, self.theme)
        if (not php_empty(lambda : update_actions)):
            self.feedback(php_implode(" | ", update_actions))
        # end if
    # end def after
# end class Theme_Upgrader_Skin
