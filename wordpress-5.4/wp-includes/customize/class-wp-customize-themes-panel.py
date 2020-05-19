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
#// Customize API: WP_Customize_Themes_Panel class
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 4.9.0
#// 
#// 
#// Customize Themes Panel Class
#// 
#// @since 4.9.0
#// 
#// @see WP_Customize_Panel
#//
class WP_Customize_Themes_Panel(WP_Customize_Panel):
    #// 
    #// Panel type.
    #// 
    #// @since 4.9.0
    #// @var string
    #//
    type = "themes"
    #// 
    #// An Underscore (JS) template for rendering this panel's container.
    #// 
    #// The themes panel renders a custom panel heading with the current theme and a switch themes button.
    #// 
    #// @see WP_Customize_Panel::print_template()
    #// 
    #// @since 4.9.0
    #//
    def render_template(self):
        
        
        php_print("     <li id=\"accordion-section-{{ data.id }}\" class=\"accordion-section control-panel-themes\">\n          <h3 class=\"accordion-section-title\">\n                ")
        if self.manager.is_theme_active():
            php_print("<span class=\"customize-action\">" + __("Active theme") + "</span> {{ data.title }}")
        else:
            php_print("<span class=\"customize-action\">" + __("Previewing theme") + "</span> {{ data.title }}")
        # end if
        php_print("\n               ")
        if current_user_can("switch_themes"):
            php_print("                 <button type=\"button\" class=\"button change-theme\" aria-label=\"")
            esc_attr_e("Change theme")
            php_print("\">")
            _ex("Change", "theme")
            php_print("</button>\n              ")
        # end if
        php_print("""           </h3>
        <ul class=\"accordion-sub-container control-panel-content\"></ul>
        </li>
        """)
    # end def render_template
    #// 
    #// An Underscore (JS) template for this panel's content (but not its container).
    #// 
    #// Class variables for this panel class are available in the `data` JS object;
    #// export custom variables by overriding WP_Customize_Panel::json().
    #// 
    #// @since 4.9.0
    #// 
    #// @see WP_Customize_Panel::print_template()
    #//
    def content_template(self):
        
        
        php_print("     <li class=\"panel-meta customize-info accordion-section <# if ( ! data.description ) { #> cannot-expand<# } #>\">\n         <button class=\"customize-panel-back\" tabindex=\"-1\" type=\"button\"><span class=\"screen-reader-text\">")
        _e("Back")
        php_print("""</span></button>
        <div class=\"accordion-section-title\">
        <span class=\"preview-notice\">
        """)
        php_printf(__("You are browsing %s"), "<strong class=\"panel-title\">" + __("Themes") + "</strong>")
        pass
        php_print("             </span>\n               ")
        if current_user_can("install_themes") and (not is_multisite()):
            php_print("                 <# if ( data.description ) { #>\n                       <button class=\"customize-help-toggle dashicons dashicons-editor-help\" type=\"button\" aria-expanded=\"false\"><span class=\"screen-reader-text\">")
            _e("Help")
            php_print("</span></button>\n                   <# } #>\n               ")
        # end if
        php_print("         </div>\n            ")
        if current_user_can("install_themes") and (not is_multisite()):
            php_print("""               <# if ( data.description ) { #>
            <div class=\"description customize-panel-description\">
            {{{ data.description }}}
            </div>
            <# } #>
            """)
        # end if
        php_print("""
        <div class=\"customize-control-notifications-container\"></div>
        </li>
        <li class=\"customize-themes-full-container-container\">
        <div class=\"customize-themes-full-container\">
        <div class=\"customize-themes-notifications\"></div>
        </div>
        </li>
        """)
    # end def content_template
# end class WP_Customize_Themes_Panel
