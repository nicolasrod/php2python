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
#// Customize API: WP_Customize_Nav_Menu_Locations_Control class
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 4.9.0
#// 
#// 
#// Customize Nav Menu Locations Control Class.
#// 
#// @since 4.9.0
#// 
#// @see WP_Customize_Control
#//
class WP_Customize_Nav_Menu_Locations_Control(WP_Customize_Control):
    type = "nav_menu_locations"
    #// 
    #// Don't render the control's content - it uses a JS template instead.
    #// 
    #// @since 4.9.0
    #//
    def render_content(self):
        
        pass
    # end def render_content
    #// 
    #// JS/Underscore template for the control UI.
    #// 
    #// @since 4.9.0
    #//
    def content_template(self):
        
        if current_theme_supports("menus"):
            php_print("""           <# var elementId; #>
            <ul class=\"menu-location-settings\">
            <li class=\"customize-control assigned-menu-locations-title\">
            <span class=\"customize-control-title\">{{ wp.customize.Menus.data.l10n.locationsTitle }}</span>
            <# if ( data.isCreating ) { #>
            <p>
            """)
            php_print(_x("Where do you want this menu to appear?", "menu locations"))
            php_print("                         <em class=\"new-menu-locations-widget-note\">\n                             ")
            printf(_x("(If you plan to use a menu <a href=\"%1$s\" %2$s>widget%3$s</a>, skip this step.)", "menu locations"), __("https://wordpress.org/support/article/wordpress-widgets/"), " class=\"external-link\" target=\"_blank\"", php_sprintf("<span class=\"screen-reader-text\"> %s</span>", __("(opens in a new tab)")))
            php_print("""                           </em>
            </p>
            <# } else { #>
            <p>""")
            php_print(_x("Here&#8217;s where this menu appears. If you&#8217;d like to change that, pick another location.", "menu locations"))
            php_print("""</p>
            <# } #>
            </li>
            """)
            for location,description in get_registered_nav_menus():
                php_print("""                   <# elementId = _.uniqueId( 'customize-nav-menu-control-location-' ); #>
                <li class=\"customize-control customize-control-checkbox assigned-menu-location\">
                <span class=\"customize-inside-control-row\">
                <input id=\"{{ elementId }}\" type=\"checkbox\" data-menu-id=\"{{ data.menu_id }}\" data-location-id=\"""")
                php_print(esc_attr(location))
                php_print("\" class=\"menu-location\" />\n                          <label for=\"{{ elementId }}\">\n                               ")
                php_print(description)
                php_print("                             <span class=\"theme-location-set\">\n                                   ")
                printf(_x("(Current: %s)", "menu location"), "<span class=\"current-menu-location-name-" + esc_attr(location) + "\"></span>")
                php_print("""                               </span>
                </label>
                </span>
                </li>
                """)
            # end for
            php_print("         </ul>\n         ")
        # end if
    # end def content_template
# end class WP_Customize_Nav_Menu_Locations_Control
