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
#// Customize API: WP_Customize_Background_Position_Control class
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 4.7.0
#// 
#// 
#// Customize Background Position Control class.
#// 
#// @since 4.7.0
#// 
#// @see WP_Customize_Control
#//
class WP_Customize_Background_Position_Control(WP_Customize_Control):
    #// 
    #// Type.
    #// 
    #// @since 4.7.0
    #// @var string
    #//
    type = "background_position"
    #// 
    #// Don't render the control content from PHP, as it's rendered via JS on load.
    #// 
    #// @since 4.7.0
    #//
    def render_content(self):
        
        
        pass
    # end def render_content
    #// 
    #// Render a JS template for the content of the position control.
    #// 
    #// @since 4.7.0
    #//
    def content_template(self):
        
        
        options_ = Array(Array({"left top": Array({"label": __("Top Left"), "icon": "dashicons dashicons-arrow-left-alt"})}, {"center top": Array({"label": __("Top"), "icon": "dashicons dashicons-arrow-up-alt"})}, {"right top": Array({"label": __("Top Right"), "icon": "dashicons dashicons-arrow-right-alt"})}), Array({"left center": Array({"label": __("Left"), "icon": "dashicons dashicons-arrow-left-alt"})}, {"center center": Array({"label": __("Center"), "icon": "background-position-center-icon"})}, {"right center": Array({"label": __("Right"), "icon": "dashicons dashicons-arrow-right-alt"})}), Array({"left bottom": Array({"label": __("Bottom Left"), "icon": "dashicons dashicons-arrow-left-alt"})}, {"center bottom": Array({"label": __("Bottom"), "icon": "dashicons dashicons-arrow-down-alt"})}, {"right bottom": Array({"label": __("Bottom Right"), "icon": "dashicons dashicons-arrow-right-alt"})}))
        php_print("""       <# if ( data.label ) { #>
        <span class=\"customize-control-title\">{{{ data.label }}}</span>
        <# } #>
        <# if ( data.description ) { #>
        <span class=\"description customize-control-description\">{{{ data.description }}}</span>
        <# } #>
        <div class=\"customize-control-content\">
        <fieldset>
        <legend class=\"screen-reader-text\"><span>""")
        _e("Image Position")
        php_print("</span></legend>\n               <div class=\"background-position-control\">\n               ")
        for group_ in options_:
            php_print("                 <div class=\"button-group\">\n                  ")
            for value_,input_ in group_:
                php_print("                     <label>\n                           <input class=\"screen-reader-text\" name=\"background-position\" type=\"radio\" value=\"")
                php_print(esc_attr(value_))
                php_print("\">\n                            <span class=\"button display-options position\"><span class=\"")
                php_print(esc_attr(input_["icon"]))
                php_print("\" aria-hidden=\"true\"></span></span>\n                         <span class=\"screen-reader-text\">")
                php_print(input_["label"])
                php_print("</span>\n                        </label>\n                  ")
            # end for
            php_print("                 </div>\n                ")
        # end for
        php_print("""               </div>
        </fieldset>
        </div>
        """)
    # end def content_template
# end class WP_Customize_Background_Position_Control
