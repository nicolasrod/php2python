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
#// Customize API: WP_Customize_Nav_Menus_Panel class
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 4.4.0
#// 
#// 
#// Customize Nav Menus Panel Class
#// 
#// Needed to add screen options.
#// 
#// @since 4.3.0
#// 
#// @see WP_Customize_Panel
#//
class WP_Customize_Nav_Menus_Panel(WP_Customize_Panel):
    type = "nav_menus"
    #// 
    #// Render screen options for Menus.
    #// 
    #// @since 4.3.0
    #//
    def render_screen_options(self):
        
        #// Adds the screen options.
        php_include_file(ABSPATH + "wp-admin/includes/nav-menu.php", once=True)
        add_filter("manage_nav-menus_columns", "wp_nav_menu_manage_columns")
        #// Display screen options.
        screen = WP_Screen.get("nav-menus.php")
        screen.render_screen_options(Array({"wrap": False}))
    # end def render_screen_options
    #// 
    #// Returns the advanced options for the nav menus page.
    #// 
    #// Link title attribute added as it's a relatively advanced concept for new users.
    #// 
    #// @since 4.3.0
    #// @deprecated 4.5.0 Deprecated in favor of wp_nav_menu_manage_columns().
    #//
    def wp_nav_menu_manage_columns(self):
        
        _deprecated_function(__METHOD__, "4.5.0", "wp_nav_menu_manage_columns")
        php_include_file(ABSPATH + "wp-admin/includes/nav-menu.php", once=True)
        return wp_nav_menu_manage_columns()
    # end def wp_nav_menu_manage_columns
    #// 
    #// An Underscore (JS) template for this panel's content (but not its container).
    #// 
    #// Class variables for this panel class are available in the `data` JS object;
    #// export custom variables by overriding WP_Customize_Panel::json().
    #// 
    #// @since 4.3.0
    #// 
    #// @see WP_Customize_Panel::print_template()
    #//
    def content_template(self):
        
        php_print("     <li class=\"panel-meta customize-info accordion-section <# if ( ! data.description ) { #> cannot-expand<# } #>\">\n         <button type=\"button\" class=\"customize-panel-back\" tabindex=\"-1\">\n               <span class=\"screen-reader-text\">")
        _e("Back")
        php_print("""</span>
        </button>
        <div class=\"accordion-section-title\">
        <span class=\"preview-notice\">
        """)
        #// translators: %s: The site/panel title in the Customizer.
        printf(__("You are customizing %s"), "<strong class=\"panel-title\">{{ data.title }}</strong>")
        php_print("             </span>\n               <button type=\"button\" class=\"customize-help-toggle dashicons dashicons-editor-help\" aria-expanded=\"false\">\n                  <span class=\"screen-reader-text\">")
        _e("Help")
        php_print("""</span>
        </button>
        <button type=\"button\" class=\"customize-screen-options-toggle\" aria-expanded=\"false\">
        <span class=\"screen-reader-text\">""")
        _e("Menu Options")
        php_print("""</span>
        </button>
        </div>
        <# if ( data.description ) { #>
        <div class=\"description customize-panel-description\">{{{ data.description }}}</div>
        <# } #>
        <div id=\"screen-options-wrap\">
        """)
        self.render_screen_options()
        php_print("         </div>\n        </li>\n     ")
        pass
        php_print("     <li class=\"customize-control-title customize-section-title-nav_menus-heading\">")
        _e("Menus")
        php_print("</li>\n      ")
    # end def content_template
# end class WP_Customize_Nav_Menus_Panel
