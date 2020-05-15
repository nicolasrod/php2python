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
#// Upgrader API: Language_Pack_Upgrader_Skin class
#// 
#// @package WordPress
#// @subpackage Upgrader
#// @since 4.6.0
#// 
#// 
#// Translation Upgrader Skin for WordPress Translation Upgrades.
#// 
#// @since 3.7.0
#// @since 4.6.0 Moved to its own file from wp-admin/includes/class-wp-upgrader-skins.php.
#// 
#// @see WP_Upgrader_Skin
#//
class Language_Pack_Upgrader_Skin(WP_Upgrader_Skin):
    language_update = None
    done_header = False
    done_footer = False
    display_footer_actions = True
    #// 
    #// @param array $args
    #//
    def __init__(self, args=Array()):
        
        defaults = Array({"url": "", "nonce": "", "title": __("Update Translations"), "skip_header_footer": False})
        args = wp_parse_args(args, defaults)
        if args["skip_header_footer"]:
            self.done_header = True
            self.done_footer = True
            self.display_footer_actions = False
        # end if
        super().__init__(args)
    # end def __init__
    #// 
    #//
    def before(self):
        
        name = self.upgrader.get_name_for_update(self.language_update)
        php_print("<div class=\"update-messages lp-show-latest\">")
        #// translators: 1: Project name (plugin, theme, or WordPress), 2: Language.
        printf("<h2>" + __("Updating translations for %1$s (%2$s)&#8230;") + "</h2>", name, self.language_update.language)
    # end def before
    #// 
    #// @param string|WP_Error $error
    #//
    def error(self, error=None):
        
        php_print("<div class=\"lp-error\">")
        super().error(error)
        php_print("</div>")
    # end def error
    #// 
    #//
    def after(self):
        
        php_print("</div>")
    # end def after
    #// 
    #//
    def bulk_footer(self):
        
        self.decrement_update_count("translation")
        update_actions = Array({"updates_page": php_sprintf("<a href=\"%s\" target=\"_parent\">%s</a>", self_admin_url("update-core.php"), __("Return to WordPress Updates page"))})
        #// 
        #// Filters the list of action links available following a translations update.
        #// 
        #// @since 3.7.0
        #// 
        #// @param string[] $update_actions Array of translations update links.
        #//
        update_actions = apply_filters("update_translations_complete_actions", update_actions)
        if update_actions and self.display_footer_actions:
            self.feedback(php_implode(" | ", update_actions))
        # end if
    # end def bulk_footer
# end class Language_Pack_Upgrader_Skin
