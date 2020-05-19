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
#// Customize API: WP_Customize_Nav_Menu_Control class
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 4.4.0
#// 
#// 
#// Customize Nav Menu Control Class.
#// 
#// @since 4.3.0
#// 
#// @see WP_Customize_Control
#//
class WP_Customize_Nav_Menu_Control(WP_Customize_Control):
    #// 
    #// Control type.
    #// 
    #// @since 4.3.0
    #// @var string
    #//
    type = "nav_menu"
    #// 
    #// Don't render the control's content - it uses a JS template instead.
    #// 
    #// @since 4.3.0
    #//
    def render_content(self):
        
        
        pass
    # end def render_content
    #// 
    #// JS/Underscore template for the control UI.
    #// 
    #// @since 4.3.0
    #//
    def content_template(self):
        
        
        add_items_ = __("Add Items")
        php_print("     <p class=\"new-menu-item-invitation\">\n            ")
        php_printf(__("Time to add some links! Click &#8220;%s&#8221; to start putting pages, categories, and custom links in your menu. Add as many things as you&#8217;d like."), add_items_)
        php_print("     </p>\n      <div class=\"customize-control-nav_menu-buttons\">\n            <button type=\"button\" class=\"button add-new-menu-item\" aria-label=\"")
        esc_attr_e("Add or remove menu items")
        php_print("\" aria-expanded=\"false\" aria-controls=\"available-menu-items\">\n             ")
        php_print(add_items_)
        php_print("         </button>\n         <button type=\"button\" class=\"button-link reorder-toggle\" aria-label=\"")
        esc_attr_e("Reorder menu items")
        php_print("\" aria-describedby=\"reorder-items-desc-{{ data.menu_id }}\">\n             <span class=\"reorder\">")
        _e("Reorder")
        php_print("</span>\n                <span class=\"reorder-done\">")
        _e("Done")
        php_print("""</span>
        </button>
        </div>
        <p class=\"screen-reader-text\" id=\"reorder-items-desc-{{ data.menu_id }}\">""")
        _e("When in reorder mode, additional controls to reorder menu items will be available in the items list above.")
        php_print("</p>\n       ")
    # end def content_template
    #// 
    #// Return parameters for this control.
    #// 
    #// @since 4.3.0
    #// 
    #// @return array Exported parameters.
    #//
    def json(self):
        
        
        exported_ = super().json()
        exported_["menu_id"] = self.setting.term_id
        return exported_
    # end def json
# end class WP_Customize_Nav_Menu_Control
