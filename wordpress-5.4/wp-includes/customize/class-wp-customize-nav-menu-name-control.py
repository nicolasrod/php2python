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
#// Customize API: WP_Customize_Nav_Menu_Name_Control class
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 4.4.0
#// 
#// 
#// Customize control to represent the name field for a given menu.
#// 
#// @since 4.3.0
#// 
#// @see WP_Customize_Control
#//
class WP_Customize_Nav_Menu_Name_Control(WP_Customize_Control):
    #// 
    #// Type of control, used by JS.
    #// 
    #// @since 4.3.0
    #// @var string
    #//
    type = "nav_menu_name"
    #// 
    #// No-op since we're using JS template.
    #// 
    #// @since 4.3.0
    #//
    def render_content(self):
        
        
        pass
    # end def render_content
    #// 
    #// Render the Underscore template for this control.
    #// 
    #// @since 4.3.0
    #//
    def content_template(self):
        
        
        php_print("""       <label>
        <# if ( data.label ) { #>
        <span class=\"customize-control-title\">{{ data.label }}</span>
        <# } #>
        <input type=\"text\" class=\"menu-name-field live-update-section-title\"
        <# if ( data.description ) { #>
        aria-describedby=\"{{ data.section }}-description\"
        <# } #>
        />
        </label>
        <# if ( data.description ) { #>
        <p id=\"{{ data.section }}-description\">{{ data.description }}</p>
        <# } #>
        """)
    # end def content_template
# end class WP_Customize_Nav_Menu_Name_Control
