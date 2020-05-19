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
#// Customize API: WP_Customize_New_Menu_Control class
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 4.4.0
#// @deprecated 4.9.0 This file is no longer used as of the menu creation UX introduced in #40104.
#//
_deprecated_file(php_basename(__FILE__), "4.9.0")
#// 
#// Customize control class for new menus.
#// 
#// @since 4.3.0
#// @deprecated 4.9.0 This class is no longer used as of the menu creation UX introduced in #40104.
#// 
#// @see WP_Customize_Control
#//
class WP_Customize_New_Menu_Control(WP_Customize_Control):
    #// 
    #// Control type.
    #// 
    #// @since 4.3.0
    #// @var string
    #//
    type = "new_menu"
    #// 
    #// Constructor.
    #// 
    #// @since 4.9.0
    #// @deprecated 4.9.0
    #// 
    #// @see WP_Customize_Control::__construct()
    #// 
    #// @param WP_Customize_Manager $manager Customizer bootstrap instance.
    #// @param string               $id      The control ID.
    #// @param array                $args    Optional. Arguments to override class property defaults.
    #// See WP_Customize_Control::__construct() for information
    #// on accepted arguments. Default empty array.
    #//
    def __init__(self, manager_=None, id_=None, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        _deprecated_function(inspect.currentframe().f_code.co_name, "4.9.0")
        super().__init__(manager_, id_, args_)
    # end def __init__
    #// 
    #// Render the control's content.
    #// 
    #// @since 4.3.0
    #// @deprecated 4.9.0
    #//
    def render_content(self):
        
        
        _deprecated_function(inspect.currentframe().f_code.co_name, "4.9.0")
        php_print("     <button type=\"button\" class=\"button button-primary\" id=\"create-new-menu-submit\">")
        _e("Create Menu")
        php_print("</button>\n      <span class=\"spinner\"></span>\n       ")
    # end def render_content
# end class WP_Customize_New_Menu_Control
