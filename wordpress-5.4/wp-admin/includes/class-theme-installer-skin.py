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
#// Upgrader API: Theme_Installer_Skin class
#// 
#// @package WordPress
#// @subpackage Upgrader
#// @since 4.6.0
#// 
#// 
#// Theme Installer Skin for the WordPress Theme Installer.
#// 
#// @since 2.8.0
#// @since 4.6.0 Moved to its own file from wp-admin/includes/class-wp-upgrader-skins.php.
#// 
#// @see WP_Upgrader_Skin
#//
class Theme_Installer_Skin(WP_Upgrader_Skin):
    api = Array()
    type = Array()
    #// 
    #// @param array $args
    #//
    def __init__(self, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        defaults_ = Array({"type": "web", "url": "", "theme": "", "nonce": "", "title": ""})
        args_ = wp_parse_args(args_, defaults_)
        self.type = args_["type"]
        self.api = args_["api"] if (php_isset(lambda : args_["api"])) else Array()
        super().__init__(args_)
    # end def __init__
    #// 
    #//
    def before(self):
        
        
        if (not php_empty(lambda : self.api)):
            self.upgrader.strings["process_success"] = php_sprintf(self.upgrader.strings["process_success_specific"], self.api.name, self.api.version)
        # end if
    # end def before
    #// 
    #//
    def after(self):
        
        
        if php_empty(lambda : self.upgrader.result["destination_name"]):
            return
        # end if
        theme_info_ = self.upgrader.theme_info()
        if php_empty(lambda : theme_info_):
            return
        # end if
        name_ = theme_info_.display("Name")
        stylesheet_ = self.upgrader.result["destination_name"]
        template_ = theme_info_.get_template()
        activate_link_ = add_query_arg(Array({"action": "activate", "template": urlencode(template_), "stylesheet": urlencode(stylesheet_)}), admin_url("themes.php"))
        activate_link_ = wp_nonce_url(activate_link_, "switch-theme_" + stylesheet_)
        install_actions_ = Array()
        if current_user_can("edit_theme_options") and current_user_can("customize"):
            customize_url_ = add_query_arg(Array({"theme": urlencode(stylesheet_), "return": urlencode(admin_url("theme-install.php" if "web" == self.type else "themes.php"))}), admin_url("customize.php"))
            install_actions_["preview"] = php_sprintf("<a href=\"%s\" class=\"hide-if-no-customize load-customize\">" + "<span aria-hidden=\"true\">%s</span><span class=\"screen-reader-text\">%s</span></a>", esc_url(customize_url_), __("Live Preview"), php_sprintf(__("Live Preview &#8220;%s&#8221;"), name_))
        # end if
        install_actions_["activate"] = php_sprintf("<a href=\"%s\" class=\"activatelink\">" + "<span aria-hidden=\"true\">%s</span><span class=\"screen-reader-text\">%s</span></a>", esc_url(activate_link_), __("Activate"), php_sprintf(__("Activate &#8220;%s&#8221;"), name_))
        if is_network_admin() and current_user_can("manage_network_themes"):
            install_actions_["network_enable"] = php_sprintf("<a href=\"%s\" target=\"_parent\">%s</a>", esc_url(wp_nonce_url("themes.php?action=enable&amp;theme=" + urlencode(stylesheet_), "enable-theme_" + stylesheet_)), __("Network Enable"))
        # end if
        if "web" == self.type:
            install_actions_["themes_page"] = php_sprintf("<a href=\"%s\" target=\"_parent\">%s</a>", self_admin_url("theme-install.php"), __("Return to Theme Installer"))
        elif current_user_can("switch_themes") or current_user_can("edit_theme_options"):
            install_actions_["themes_page"] = php_sprintf("<a href=\"%s\" target=\"_parent\">%s</a>", self_admin_url("themes.php"), __("Return to Themes page"))
        # end if
        if (not self.result) or is_wp_error(self.result) or is_network_admin() or (not current_user_can("switch_themes")):
            install_actions_["activate"] = None
            install_actions_["preview"] = None
        # end if
        #// 
        #// Filters the list of action links available following a single theme installation.
        #// 
        #// @since 2.8.0
        #// 
        #// @param string[] $install_actions Array of theme action links.
        #// @param object   $api             Object containing WordPress.org API theme data.
        #// @param string   $stylesheet      Theme directory name.
        #// @param WP_Theme $theme_info      Theme object.
        #//
        install_actions_ = apply_filters("install_theme_complete_actions", install_actions_, self.api, stylesheet_, theme_info_)
        if (not php_empty(lambda : install_actions_)):
            self.feedback(php_implode(" | ", install_actions_))
        # end if
    # end def after
# end class Theme_Installer_Skin
