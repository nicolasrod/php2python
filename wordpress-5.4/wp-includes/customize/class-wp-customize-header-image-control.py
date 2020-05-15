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
#// Customize API: WP_Customize_Header_Image_Control class
#// 
#// @package WordPress
#// @subpackage Customize
#// @since 4.4.0
#// 
#// 
#// Customize Header Image Control class.
#// 
#// @since 3.4.0
#// 
#// @see WP_Customize_Image_Control
#//
class WP_Customize_Header_Image_Control(WP_Customize_Image_Control):
    type = "header"
    uploaded_headers = Array()
    default_headers = Array()
    #// 
    #// Constructor.
    #// 
    #// @since 3.4.0
    #// 
    #// @param WP_Customize_Manager $manager Customizer bootstrap instance.
    #//
    def __init__(self, manager=None):
        
        super().__init__(manager, "header_image", Array({"label": __("Header Image"), "settings": Array({"default": "header_image", "data": "header_image_data"})}, {"section": "header_image", "removed": "remove-header", "get_url": "get_header_image"}))
    # end def __init__
    #// 
    #//
    def enqueue(self):
        
        wp_enqueue_media()
        wp_enqueue_script("customize-views")
        self.prepare_control()
        wp_localize_script("customize-views", "_wpCustomizeHeader", Array({"data": Array({"width": absint(get_theme_support("custom-header", "width")), "height": absint(get_theme_support("custom-header", "height")), "flex-width": absint(get_theme_support("custom-header", "flex-width")), "flex-height": absint(get_theme_support("custom-header", "flex-height")), "currentImgSrc": self.get_current_image_src()})}, {"nonces": Array({"add": wp_create_nonce("header-add"), "remove": wp_create_nonce("header-remove")})}, {"uploads": self.uploaded_headers, "defaults": self.default_headers}))
        super().enqueue()
    # end def enqueue
    #// 
    #// @global Custom_Image_Header $custom_image_header
    #//
    def prepare_control(self):
        
        global custom_image_header
        php_check_if_defined("custom_image_header")
        if php_empty(lambda : custom_image_header):
            return
        # end if
        add_action("customize_controls_print_footer_scripts", Array(self, "print_header_image_template"))
        #// Process default headers and uploaded headers.
        custom_image_header.process_default_headers()
        self.default_headers = custom_image_header.get_default_header_images()
        self.uploaded_headers = custom_image_header.get_uploaded_header_images()
    # end def prepare_control
    #// 
    #//
    def print_header_image_template(self):
        
        php_print("""       <script type=\"text/template\" id=\"tmpl-header-choice\">
        <# if (data.random) { #>
        <button type=\"button\" class=\"button display-options random\">
        <span class=\"dashicons dashicons-randomize dice\"></span>
        <# if ( data.type === 'uploaded' ) { #>
        """)
        _e("Randomize uploaded headers")
        php_print("             <# } else if ( data.type === 'default' ) { #>\n                 ")
        _e("Randomize suggested headers")
        php_print("""               <# } #>
        </button>
        <# } else { #>
        <button type=\"button\" class=\"choice thumbnail\"
        data-customize-image-value=\"{{{data.header.url}}}\"
        data-customize-header-image-data=\"{{JSON.stringify(data.header)}}\">
        <span class=\"screen-reader-text\">""")
        _e("Set image")
        php_print("""</span>
        <img src=\"{{{data.header.thumbnail_url}}}\" alt=\"{{{data.header.alt_text || data.header.description}}}\">
        </button>
        <# if ( data.type === 'uploaded' ) { #>
        <button type=\"button\" class=\"dashicons dashicons-no close\"><span class=\"screen-reader-text\">""")
        _e("Remove image")
        php_print("""</span></button>
        <# } #>
        <# } #>
        </script>
        <script type=\"text/template\" id=\"tmpl-header-current\">
        <# if (data.choice) { #>
        <# if (data.random) { #>
        <div class=\"placeholder\">
        <span class=\"dashicons dashicons-randomize dice\"></span>
        <# if ( data.type === 'uploaded' ) { #>
        """)
        _e("Randomizing uploaded headers")
        php_print("             <# } else if ( data.type === 'default' ) { #>\n                 ")
        _e("Randomizing suggested headers")
        php_print("""               <# } #>
        </div>
        <# } else { #>
        <img src=\"{{{data.header.thumbnail_url}}}\" alt=\"{{{data.header.alt_text || data.header.description}}}\" />
        <# } #>
        <# } else { #>
        <div class=\"placeholder\">
        """)
        _e("No image set")
        php_print("""           </div>
        <# } #>
        </script>
        """)
    # end def print_header_image_template
    #// 
    #// @return string|void
    #//
    def get_current_image_src(self):
        
        src = self.value()
        if (php_isset(lambda : self.get_url)):
            src = php_call_user_func(self.get_url, src)
            return src
        # end if
    # end def get_current_image_src
    #// 
    #//
    def render_content(self):
        
        visibility = "" if self.get_current_image_src() else " style=\"display:none\" "
        width = absint(get_theme_support("custom-header", "width"))
        height = absint(get_theme_support("custom-header", "height"))
        php_print("     <div class=\"customize-control-content\">\n         ")
        if current_theme_supports("custom-header", "video"):
            php_print("<span class=\"customize-control-title\">" + self.label + "</span>")
        # end if
        php_print("         <div class=\"customize-control-notifications-container\"></div>\n           <p class=\"customizer-section-intro customize-control-description\">\n              ")
        if current_theme_supports("custom-header", "video"):
            _e("Click &#8220;Add new image&#8221; to upload an image file from your computer. Your theme works best with an image that matches the size of your video &#8212; you&#8217;ll be able to crop your image once you upload it for a perfect fit.")
        elif width and height:
            printf(__("Click &#8220;Add new image&#8221; to upload an image file from your computer. Your theme works best with an image with a header size of %s pixels &#8212; you&#8217;ll be able to crop your image once you upload it for a perfect fit."), php_sprintf("<strong>%s &times; %s</strong>", width, height))
        elif width:
            printf(__("Click &#8220;Add new image&#8221; to upload an image file from your computer. Your theme works best with an image with a header width of %s pixels &#8212; you&#8217;ll be able to crop your image once you upload it for a perfect fit."), php_sprintf("<strong>%s</strong>", width))
        else:
            printf(__("Click &#8220;Add new image&#8221; to upload an image file from your computer. Your theme works best with an image with a header height of %s pixels &#8212; you&#8217;ll be able to crop your image once you upload it for a perfect fit."), php_sprintf("<strong>%s</strong>", height))
        # end if
        php_print("""           </p>
        <div class=\"current\">
        <label for=\"header_image-button\">
        <span class=\"customize-control-title\">
        """)
        _e("Current header")
        php_print("""                   </span>
        </label>
        <div class=\"container\">
        </div>
        </div>
        <div class=\"actions\">
        """)
        if current_user_can("upload_files"):
            php_print("             <button type=\"button\"")
            php_print(visibility)
            php_print(" class=\"button remove\" aria-label=\"")
            esc_attr_e("Hide header image")
            php_print("\">")
            _e("Hide image")
            php_print("</button>\n              <button type=\"button\" class=\"button new\" id=\"header_image-button\" aria-label=\"")
            esc_attr_e("Add new header image")
            php_print("\">")
            _e("Add new image")
            php_print("</button>\n              ")
        # end if
        php_print("""           </div>
        <div class=\"choices\">
        <span class=\"customize-control-title header-previously-uploaded\">
        """)
        _ex("Previously uploaded", "custom headers")
        php_print("""               </span>
        <div class=\"uploaded\">
        <div class=\"list\">
        </div>
        </div>
        <span class=\"customize-control-title header-default\">
        """)
        _ex("Suggested", "custom headers")
        php_print("""               </span>
        <div class=\"default\">
        <div class=\"list\">
        </div>
        </div>
        </div>
        </div>
        """)
    # end def render_content
# end class WP_Customize_Header_Image_Control
