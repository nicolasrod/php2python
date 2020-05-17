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
#// Customize API: WP_Customize_Nav_Menu_Location_Control class
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 4.4.0
#// 
#// 
#// Customize Menu Location Control Class.
#// 
#// This custom control is only needed for JS.
#// 
#// @since 4.3.0
#// 
#// @see WP_Customize_Control
#//
class WP_Customize_Nav_Menu_Location_Control(WP_Customize_Control):
    #// 
    #// Control type.
    #// 
    #// @since 4.3.0
    #// @var string
    #//
    type = "nav_menu_location"
    #// 
    #// Location ID.
    #// 
    #// @since 4.3.0
    #// @var string
    #//
    location_id = ""
    #// 
    #// Refresh the parameters passed to JavaScript via JSON.
    #// 
    #// @since 4.3.0
    #// 
    #// @see WP_Customize_Control::to_json()
    #//
    def to_json(self):
        
        
        super().to_json()
        self.json["locationId"] = self.location_id
    # end def to_json
    #// 
    #// Render content just like a normal select control.
    #// 
    #// @since 4.3.0
    #// @since 4.9.0 Added a button to create menus.
    #//
    def render_content(self):
        
        
        if php_empty(lambda : self.choices):
            return
        # end if
        value_hidden_class_ = ""
        no_value_hidden_class_ = ""
        if self.value():
            value_hidden_class_ = " hidden"
        else:
            no_value_hidden_class_ = " hidden"
        # end if
        php_print("     <label>\n           ")
        if (not php_empty(lambda : self.label)):
            php_print("         <span class=\"customize-control-title\">")
            php_print(esc_html(self.label))
            php_print("</span>\n            ")
        # end if
        php_print("\n           ")
        if (not php_empty(lambda : self.description)):
            php_print("         <span class=\"description customize-control-description\">")
            php_print(self.description)
            php_print("</span>\n            ")
        # end if
        php_print("\n           <select ")
        self.link()
        php_print(">\n              ")
        for value_,label_ in self.choices:
            php_print("<option value=\"" + esc_attr(value_) + "\"" + selected(self.value(), value_, False) + ">" + label_ + "</option>")
        # end for
        php_print("         </select>\n     </label>\n      <button type=\"button\" class=\"button-link create-menu")
        php_print(value_hidden_class_)
        php_print("\" data-location-id=\"")
        php_print(esc_attr(self.location_id))
        php_print("\" aria-label=\"")
        esc_attr_e("Create a menu for this location")
        php_print("\">")
        _e("+ Create New Menu")
        php_print("</button>\n      <button type=\"button\" class=\"button-link edit-menu")
        php_print(no_value_hidden_class_)
        php_print("\" aria-label=\"")
        esc_attr_e("Edit selected menu")
        php_print("\">")
        _e("Edit Menu")
        php_print("</button>\n      ")
    # end def render_content
# end class WP_Customize_Nav_Menu_Location_Control
