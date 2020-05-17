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
#// Customize API: WP_Customize_Nav_Menu_Auto_Add_Control class
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 4.4.0
#// 
#// 
#// Customize control to represent the auto_add field for a given menu.
#// 
#// @since 4.3.0
#// 
#// @see WP_Customize_Control
#//
class WP_Customize_Nav_Menu_Auto_Add_Control(WP_Customize_Control):
    #// 
    #// Type of control, used by JS.
    #// 
    #// @since 4.3.0
    #// @var string
    #//
    type = "nav_menu_auto_add"
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
        
        
        php_print("     <# var elementId = _.uniqueId( 'customize-nav-menu-auto-add-control-' ); #>\n       <span class=\"customize-control-title\">")
        _e("Menu Options")
        php_print("""</span>
        <span class=\"customize-inside-control-row\">
        <input id=\"{{ elementId }}\" type=\"checkbox\" class=\"auto_add\" />
        <label for=\"{{ elementId }}\">
        """)
        _e("Automatically add new top-level pages to this menu")
        php_print("         </label>\n      </span>\n       ")
    # end def content_template
# end class WP_Customize_Nav_Menu_Auto_Add_Control
