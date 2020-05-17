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
#// Customize API: WP_Customize_Site_Icon_Control class
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 4.4.0
#// 
#// 
#// Customize Site Icon control class.
#// 
#// Used only for custom functionality in JavaScript.
#// 
#// @since 4.3.0
#// 
#// @see WP_Customize_Cropped_Image_Control
#//
class WP_Customize_Site_Icon_Control(WP_Customize_Cropped_Image_Control):
    #// 
    #// Control type.
    #// 
    #// @since 4.3.0
    #// @var string
    #//
    type = "site_icon"
    #// 
    #// Constructor.
    #// 
    #// @since 4.3.0
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
        
        super().__init__(manager_, id_, args_)
        add_action("customize_controls_print_styles", "wp_site_icon", 99)
    # end def __init__
    #// 
    #// Renders a JS template for the content of the site icon control.
    #// 
    #// @since 4.5.0
    #//
    def content_template(self):
        
        
        php_print("""       <# if ( data.label ) { #>
        <span class=\"customize-control-title\">{{ data.label }}</span>
        <# } #>
        <# if ( data.description ) { #>
        <span class=\"description customize-control-description\">{{{ data.description }}}</span>
        <# } #>
        <# if ( data.attachment && data.attachment.id ) { #>
        <div class=\"attachment-media-view\">
        <# if ( data.attachment.sizes ) { #>
        <div class=\"site-icon-preview wp-clearfix\">
        <div class=\"favicon-preview\">
        <img src=\"""")
        php_print(esc_url(admin_url("images/" + "browser-rtl.png" if is_rtl() else "browser.png")))
        php_print("""\" class=\"browser-preview\" width=\"182\" alt=\"\" />
        <div class=\"favicon\">
        <img src=\"{{ data.attachment.sizes.full ? data.attachment.sizes.full.url : data.attachment.url }}\" alt=\"""")
        esc_attr_e("Preview as a browser icon")
        php_print("\"/>\n                           </div>\n                            <span class=\"browser-title\" aria-hidden=\"true\"><# print( '")
        bloginfo("name")
        php_print("' ) #></span>\n                      </div>\n                        <img class=\"app-icon-preview\" src=\"{{ data.attachment.sizes.full ? data.attachment.sizes.full.url : data.attachment.url }}\" alt=\"")
        esc_attr_e("Preview as an app icon")
        php_print("""\"/>
        </div>
        <# } #>
        <div class=\"actions\">
        <# if ( data.canUpload ) { #>
        <button type=\"button\" class=\"button remove-button\">""")
        php_print(self.button_labels["remove"])
        php_print("</button>\n                      <button type=\"button\" class=\"button upload-button\">")
        php_print(self.button_labels["change"])
        php_print("""</button>
        <# } #>
        </div>
        </div>
        <# } else { #>
        <div class=\"attachment-media-view\">
        <# if ( data.canUpload ) { #>
        <button type=\"button\" class=\"upload-button button-add-media\">""")
        php_print(self.button_labels["site_icon"])
        php_print("""</button>
        <# } #>
        <div class=\"actions\">
        <# if ( data.defaultAttachment ) { #>
        <button type=\"button\" class=\"button default-button\">""")
        php_print(self.button_labels["default"])
        php_print("""</button>
        <# } #>
        </div>
        </div>
        <# } #>
        """)
    # end def content_template
# end class WP_Customize_Site_Icon_Control
