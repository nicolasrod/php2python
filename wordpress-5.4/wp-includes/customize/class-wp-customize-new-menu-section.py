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
#// Customize API: WP_Customize_New_Menu_Section class
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 4.4.0
#// @deprecated 4.9.0 This file is no longer used as of the menu creation UX introduced in #40104.
#//
_deprecated_file(php_basename(__FILE__), "4.9.0")
#// 
#// Customize Menu Section Class
#// 
#// @since 4.3.0
#// @deprecated 4.9.0 This class is no longer used as of the menu creation UX introduced in #40104.
#// 
#// @see WP_Customize_Section
#//
class WP_Customize_New_Menu_Section(WP_Customize_Section):
    type = "new_menu"
    #// 
    #// Constructor.
    #// 
    #// Any supplied $args override class property defaults.
    #// 
    #// @since 4.9.0
    #// @deprecated 4.9.0
    #// 
    #// @param WP_Customize_Manager $manager Customizer bootstrap instance.
    #// @param string               $id      A specific ID of the section.
    #// @param array                $args    Section arguments.
    #//
    def __init__(self, manager=None, id=None, args=Array()):
        
        _deprecated_function(__METHOD__, "4.9.0")
        super().__init__(manager, id, args)
    # end def __init__
    #// 
    #// Render the section, and the controls that have been added to it.
    #// 
    #// @since 4.3.0
    #// @deprecated 4.9.0
    #//
    def render(self):
        
        _deprecated_function(__METHOD__, "4.9.0")
        php_print("     <li id=\"accordion-section-")
        php_print(esc_attr(self.id))
        php_print("\" class=\"accordion-section-new-menu\">\n           <button type=\"button\" class=\"button add-new-menu-item add-menu-toggle\" aria-expanded=\"false\">\n               ")
        php_print(esc_html(self.title))
        php_print("""           </button>
        <ul class=\"new-menu-section-content\"></ul>
        </li>
        """)
    # end def render
# end class WP_Customize_New_Menu_Section
