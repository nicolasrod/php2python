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
#// Customize API: WP_Customize_Color_Control class
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 4.4.0
#// 
#// 
#// Customize Color Control class.
#// 
#// @since 3.4.0
#// 
#// @see WP_Customize_Control
#//
class WP_Customize_Color_Control(WP_Customize_Control):
    #// 
    #// Type.
    #// 
    #// @var string
    #//
    type = "color"
    #// 
    #// Statuses.
    #// 
    #// @var array
    #//
    statuses = Array()
    #// 
    #// Mode.
    #// 
    #// @since 4.7.0
    #// @var string
    #//
    mode = "full"
    #// 
    #// Constructor.
    #// 
    #// @since 3.4.0
    #// 
    #// @see WP_Customize_Control::__construct()
    #// 
    #// @param WP_Customize_Manager $manager Customizer bootstrap instance.
    #// @param string               $id      Control ID.
    #// @param array                $args    Optional. Arguments to override class property defaults.
    #// See WP_Customize_Control::__construct() for information
    #// on accepted arguments. Default empty array.
    #//
    def __init__(self, manager_=None, id_=None, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        self.statuses = Array({"": __("Default")})
        super().__init__(manager_, id_, args_)
    # end def __init__
    #// 
    #// Enqueue scripts/styles for the color picker.
    #// 
    #// @since 3.4.0
    #//
    def enqueue(self):
        
        
        wp_enqueue_script("wp-color-picker")
        wp_enqueue_style("wp-color-picker")
    # end def enqueue
    #// 
    #// Refresh the parameters passed to the JavaScript via JSON.
    #// 
    #// @since 3.4.0
    #// @uses WP_Customize_Control::to_json()
    #//
    def to_json(self):
        
        
        super().to_json()
        self.json["statuses"] = self.statuses
        self.json["defaultValue"] = self.setting.default
        self.json["mode"] = self.mode
    # end def to_json
    #// 
    #// Don't render the control content from PHP, as it's rendered via JS on load.
    #// 
    #// @since 3.4.0
    #//
    def render_content(self):
        
        
        pass
    # end def render_content
    #// 
    #// Render a JS template for the content of the color picker control.
    #// 
    #// @since 4.1.0
    #//
    def content_template(self):
        
        
        php_print("""       <# var defaultValue = '#RRGGBB', defaultValueAttr = '',
        isHueSlider = data.mode === 'hue';
    if ( data.defaultValue && _.isString( data.defaultValue ) && ! isHueSlider ) {
    if ( '#' !== data.defaultValue.substring( 0, 1 ) ) {
        defaultValue = '#' + data.defaultValue;
        } else {
        defaultValue = data.defaultValue;
        }
        defaultValueAttr = ' data-default-color=' + defaultValue; // Quotes added automatically.
        } #>
        <# if ( data.label ) { #>
        <span class=\"customize-control-title\">{{{ data.label }}}</span>
        <# } #>
        <# if ( data.description ) { #>
        <span class=\"description customize-control-description\">{{{ data.description }}}</span>
        <# } #>
        <div class=\"customize-control-content\">
        <label><span class=\"screen-reader-text\">{{{ data.label }}}</span>
        <# if ( isHueSlider ) { #>
        <input class=\"color-picker-hue\" type=\"text\" data-type=\"hue\" />
        <# } else { #>
        <input class=\"color-picker-hex\" type=\"text\" maxlength=\"7\" placeholder=\"{{ defaultValue }}\" {{ defaultValueAttr }} />
        <# } #>
        </label>
        </div>
        """)
    # end def content_template
# end class WP_Customize_Color_Control
