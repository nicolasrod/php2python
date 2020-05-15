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
#// Custom header implementation
#// 
#// @link https://codex.wordpress.org/Custom_Headers
#// 
#// @package WordPress
#// @subpackage Twenty_Seventeen
#// @since Twenty Seventeen 1.0
#// 
#// 
#// Set up the WordPress core custom header feature.
#// 
#// @uses twentyseventeen_header_style()
#//
def twentyseventeen_custom_header_setup(*args_):
    
    #// 
    #// Filter Twenty Seventeen custom-header support arguments.
    #// 
    #// @since Twenty Seventeen 1.0
    #// 
    #// @param array $args {
    #// An array of custom-header support arguments.
    #// 
    #// @type string $default-image          Default image of the header.
    #// @type int    $width                  Width in pixels of the custom header image. Default 954.
    #// @type int    $height                 Height in pixels of the custom header image. Default 1300.
    #// @type string $flex-height            Flex support for height of header.
    #// @type string $video                  Video support for header.
    #// @type string $wp-head-callback       Callback function used to styles the header image and text
    #// displayed on the blog.
    #// }
    #//
    add_theme_support("custom-header", apply_filters("twentyseventeen_custom_header_args", Array({"default-image": get_parent_theme_file_uri("/assets/images/header.jpg"), "width": 2000, "height": 1200, "flex-height": True, "video": True, "wp-head-callback": "twentyseventeen_header_style"})))
    register_default_headers(Array({"default-image": Array({"url": "%s/assets/images/header.jpg", "thumbnail_url": "%s/assets/images/header.jpg", "description": __("Default Header Image", "twentyseventeen")})}))
# end def twentyseventeen_custom_header_setup
add_action("after_setup_theme", "twentyseventeen_custom_header_setup")
if (not php_function_exists("twentyseventeen_header_style")):
    #// 
    #// Styles the header image and text displayed on the blog.
    #// 
    #// @see twentyseventeen_custom_header_setup().
    #//
    def twentyseventeen_header_style(*args_):
        
        header_text_color = get_header_textcolor()
        #// If no custom options for text are set, let's bail.
        #// get_header_textcolor() options: add_theme_support( 'custom-header' ) is default, hide text (returns 'blank') or any hex value.
        if get_theme_support("custom-header", "default-text-color") == header_text_color:
            return
        # end if
        pass
        php_print("     <style id=\"twentyseventeen-custom-header-styles\" type=\"text/css\">\n     ")
        #// Has the text been hidden?
        if "blank" == header_text_color:
            php_print("""       .site-title,
            .site-description {
            position: absolute;
            clip: rect(1px, 1px, 1px, 1px);
            }
            """)
            pass
        else:
            php_print("""       .site-title a,
            .colors-dark .site-title a,
            .colors-custom .site-title a,
            body.has-header-image .site-title a,
            body.has-header-video .site-title a,
            body.has-header-image.colors-dark .site-title a,
            body.has-header-video.colors-dark .site-title a,
            body.has-header-image.colors-custom .site-title a,
            body.has-header-video.colors-custom .site-title a,
            .site-description,
            .colors-dark .site-description,
            .colors-custom .site-description,
            body.has-header-image .site-description,
            body.has-header-video .site-description,
            body.has-header-image.colors-dark .site-description,
            body.has-header-video.colors-dark .site-description,
            body.has-header-image.colors-custom .site-description,
            body.has-header-video.colors-custom .site-description {
            color: #""")
            php_print(esc_attr(header_text_color))
            php_print(";\n      }\n ")
        # end if
        php_print(" </style>\n      ")
    # end def twentyseventeen_header_style
# end if
#// End of twentyseventeen_header_style().
#// 
#// Customize video play/pause button in the custom header.
#// 
#// @param array $settings Video settings.
#// @return array The filtered video settings.
#//
def twentyseventeen_video_controls(settings=None, *args_):
    
    settings["l10n"]["play"] = "<span class=\"screen-reader-text\">" + __("Play background video", "twentyseventeen") + "</span>" + twentyseventeen_get_svg(Array({"icon": "play"}))
    settings["l10n"]["pause"] = "<span class=\"screen-reader-text\">" + __("Pause background video", "twentyseventeen") + "</span>" + twentyseventeen_get_svg(Array({"icon": "pause"}))
    return settings
# end def twentyseventeen_video_controls
add_filter("header_video_settings", "twentyseventeen_video_controls")
