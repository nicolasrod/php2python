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
#// Customize API: WP_Customize_Code_Editor_Control class
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 4.9.0
#// 
#// 
#// Customize Code Editor Control class.
#// 
#// @since 4.9.0
#// 
#// @see WP_Customize_Control
#//
class WP_Customize_Code_Editor_Control(WP_Customize_Control):
    type = "code_editor"
    code_type = ""
    editor_settings = Array()
    #// 
    #// Enqueue control related scripts/styles.
    #// 
    #// @since 4.9.0
    #//
    def enqueue(self):
        
        self.editor_settings = wp_enqueue_code_editor(php_array_merge(Array({"type": self.code_type, "codemirror": Array({"indentUnit": 2, "tabSize": 2})}), self.editor_settings))
    # end def enqueue
    #// 
    #// Refresh the parameters passed to the JavaScript via JSON.
    #// 
    #// @since 4.9.0
    #// @see WP_Customize_Control::json()
    #// 
    #// @return array Array of parameters passed to the JavaScript.
    #//
    def json(self):
        
        json = super().json()
        json["editor_settings"] = self.editor_settings
        json["input_attrs"] = self.input_attrs
        return json
    # end def json
    #// 
    #// Don't render the control content from PHP, as it's rendered via JS on load.
    #// 
    #// @since 4.9.0
    #//
    def render_content(self):
        
        pass
    # end def render_content
    #// 
    #// Render a JS template for control display.
    #// 
    #// @since 4.9.0
    #//
    def content_template(self):
        
        php_print("""       <# var elementIdPrefix = 'el' + String( Math.random() ); #>
        <# if ( data.label ) { #>
        <label for=\"{{ elementIdPrefix }}_editor\" class=\"customize-control-title\">
        {{ data.label }}
        </label>
        <# } #>
        <# if ( data.description ) { #>
        <span class=\"description customize-control-description\">{{{ data.description }}}</span>
        <# } #>
        <div class=\"customize-control-notifications-container\"></div>
        <textarea id=\"{{ elementIdPrefix }}_editor\"
        <# _.each( _.extend( { 'class': 'code' }, data.input_attrs ), function( value, key ) { #>
        {{{ key }}}=\"{{ value }}\"
        <# }); #>
        ></textarea>
        """)
    # end def content_template
# end class WP_Customize_Code_Editor_Control
