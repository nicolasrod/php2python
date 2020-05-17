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
#// Twenty Twenty functions and definitions
#// 
#// @link https://developer.wordpress.org/themes/basics/theme-functions
#// 
#// @package WordPress
#// @subpackage Twenty_Twenty
#// @since Twenty Twenty 1.0
#// 
#// 
#// Table of Contents:
#// Theme Support
#// Required Files
#// Register Styles
#// Register Scripts
#// Register Menus
#// Custom Logo
#// WP Body Open
#// Register Sidebars
#// Enqueue Block Editor Assets
#// Enqueue Classic Editor Styles
#// Block Editor Settings
#// 
#// 
#// Sets up theme defaults and registers support for various WordPress features.
#// 
#// Note that this function is hooked into the after_setup_theme hook, which
#// runs before the init hook. The init hook is too late for some features, such
#// as indicating support for post thumbnails.
#//
def twentytwenty_theme_support(*_args_):
    
    
    #// Add default posts and comments RSS feed links to head.
    add_theme_support("automatic-feed-links")
    #// Custom background color.
    add_theme_support("custom-background", Array({"default-color": "f5efe0"}))
    #// Set content-width.
    global content_width_
    php_check_if_defined("content_width_")
    if (not (php_isset(lambda : content_width_))):
        content_width_ = 580
    # end if
    #// 
    #// Enable support for Post Thumbnails on posts and pages.
    #// 
    #// @link https://developer.wordpress.org/themes/functionality/featured-images-post-thumbnails
    #//
    add_theme_support("post-thumbnails")
    #// Set post thumbnail size.
    set_post_thumbnail_size(1200, 9999)
    #// Add custom image size used in Cover Template.
    add_image_size("twentytwenty-fullscreen", 1980, 9999)
    #// Custom logo.
    logo_width_ = 120
    logo_height_ = 90
    #// If the retina setting is active, double the recommended width and height.
    if get_theme_mod("retina_logo", False):
        logo_width_ = floor(logo_width_ * 2)
        logo_height_ = floor(logo_height_ * 2)
    # end if
    add_theme_support("custom-logo", Array({"height": logo_height_, "width": logo_width_, "flex-height": True, "flex-width": True}))
    #// 
    #// Let WordPress manage the document title.
    #// By adding theme support, we declare that this theme does not use a
    #// hard-coded <title> tag in the document head, and expect WordPress to
    #// provide it for us.
    #//
    add_theme_support("title-tag")
    #// 
    #// Switch default core markup for search form, comment form, and comments
    #// to output valid HTML5.
    #//
    add_theme_support("html5", Array("search-form", "comment-form", "comment-list", "gallery", "caption", "script", "style"))
    #// 
    #// Make theme available for translation.
    #// Translations can be filed in the /languages/ directory.
    #// If you're building a theme based on Twenty Twenty, use a find and replace
    #// to change 'twentytwenty' to the name of your theme in all the template files.
    #//
    load_theme_textdomain("twentytwenty")
    #// Add support for full and wide align images.
    add_theme_support("align-wide")
    #// Add support for responsive embeds.
    add_theme_support("responsive-embeds")
    #// 
    #// Adds starter content to highlight the theme on fresh sites.
    #// This is done conditionally to avoid loading the starter content on every
    #// page load, as it is a one-off operation only needed once in the customizer.
    #//
    if is_customize_preview():
        php_include_file(get_template_directory() + "/inc/starter-content.php", once=False)
        add_theme_support("starter-content", twentytwenty_get_starter_content())
    # end if
    #// Add theme support for selective refresh for widgets.
    add_theme_support("customize-selective-refresh-widgets")
    #// 
    #// Adds `async` and `defer` support for scripts registered or enqueued
    #// by the theme.
    #//
    loader_ = php_new_class("TwentyTwenty_Script_Loader", lambda : TwentyTwenty_Script_Loader())
    add_filter("script_loader_tag", Array(loader_, "filter_script_loader_tag"), 10, 2)
# end def twentytwenty_theme_support
add_action("after_setup_theme", "twentytwenty_theme_support")
#// 
#// REQUIRED FILES
#// Include required files.
#//
php_include_file(get_template_directory() + "/inc/template-tags.php", once=False)
#// Handle SVG icons.
php_include_file(get_template_directory() + "/classes/class-twentytwenty-svg-icons.php", once=False)
php_include_file(get_template_directory() + "/inc/svg-icons.php", once=False)
#// Handle Customizer settings.
php_include_file(get_template_directory() + "/classes/class-twentytwenty-customize.php", once=False)
#// Require Separator Control class.
php_include_file(get_template_directory() + "/classes/class-twentytwenty-separator-control.php", once=False)
#// Custom comment walker.
php_include_file(get_template_directory() + "/classes/class-twentytwenty-walker-comment.php", once=False)
#// Custom page walker.
php_include_file(get_template_directory() + "/classes/class-twentytwenty-walker-page.php", once=False)
#// Custom script loader class.
php_include_file(get_template_directory() + "/classes/class-twentytwenty-script-loader.php", once=False)
#// Non-latin language handling.
php_include_file(get_template_directory() + "/classes/class-twentytwenty-non-latin-languages.php", once=False)
#// Custom CSS.
php_include_file(get_template_directory() + "/inc/custom-css.php", once=False)
#// 
#// Register and Enqueue Styles.
#//
def twentytwenty_register_styles(*_args_):
    
    
    theme_version_ = wp_get_theme().get("Version")
    wp_enqueue_style("twentytwenty-style", get_stylesheet_uri(), Array(), theme_version_)
    wp_style_add_data("twentytwenty-style", "rtl", "replace")
    #// Add output of Customizer settings as inline style.
    wp_add_inline_style("twentytwenty-style", twentytwenty_get_customizer_css("front-end"))
    #// Add print CSS.
    wp_enqueue_style("twentytwenty-print-style", get_template_directory_uri() + "/print.css", None, theme_version_, "print")
# end def twentytwenty_register_styles
add_action("wp_enqueue_scripts", "twentytwenty_register_styles")
#// 
#// Register and Enqueue Scripts.
#//
def twentytwenty_register_scripts(*_args_):
    
    
    theme_version_ = wp_get_theme().get("Version")
    if (not is_admin()) and is_singular() and comments_open() and get_option("thread_comments"):
        wp_enqueue_script("comment-reply")
    # end if
    wp_enqueue_script("twentytwenty-js", get_template_directory_uri() + "/assets/js/index.js", Array(), theme_version_, False)
    wp_script_add_data("twentytwenty-js", "async", True)
# end def twentytwenty_register_scripts
add_action("wp_enqueue_scripts", "twentytwenty_register_scripts")
#// 
#// Fix skip link focus in IE11.
#// 
#// This does not enqueue the script because it is tiny and because it is only for IE11,
#// thus it does not warrant having an entire dedicated blocking script being loaded.
#// 
#// @link https://git.io/vWdr2
#//
def twentytwenty_skip_link_focus_fix(*_args_):
    
    
    pass
    php_print("""   <script>
    /(trident|msie)/i.test(navigator.userAgent)&&document.getElementById&&window.addEventListener&&window.addEventListener(\"hashchange\",function(){var t,e=location.hash.substring(1);/^[A-z0-9_-]+$/.test(e)&&(t=document.getElementById(e))&&(/^(?:a|select|input|button|textarea)$/i.test(t.tagName)||(t.tabIndex=-1),t.focus())},!1);
    </script>
    """)
# end def twentytwenty_skip_link_focus_fix
add_action("wp_print_footer_scripts", "twentytwenty_skip_link_focus_fix")
#// Enqueue non-latin language styles
#// 
#// @since Twenty Twenty 1.0
#// 
#// @return void
#//
def twentytwenty_non_latin_languages(*_args_):
    
    
    custom_css_ = TwentyTwenty_Non_Latin_Languages.get_non_latin_css("front-end")
    if custom_css_:
        wp_add_inline_style("twentytwenty-style", custom_css_)
    # end if
# end def twentytwenty_non_latin_languages
add_action("wp_enqueue_scripts", "twentytwenty_non_latin_languages")
#// 
#// Register navigation menus uses wp_nav_menu in five places.
#//
def twentytwenty_menus(*_args_):
    
    
    locations_ = Array({"primary": __("Desktop Horizontal Menu", "twentytwenty"), "expanded": __("Desktop Expanded Menu", "twentytwenty"), "mobile": __("Mobile Menu", "twentytwenty"), "footer": __("Footer Menu", "twentytwenty"), "social": __("Social Menu", "twentytwenty")})
    register_nav_menus(locations_)
# end def twentytwenty_menus
add_action("init", "twentytwenty_menus")
#// 
#// Get the information about the logo.
#// 
#// @param string $html The HTML output from get_custom_logo (core function).
#// 
#// @return string $html
#//
def twentytwenty_get_custom_logo(html_=None, *_args_):
    
    
    logo_id_ = get_theme_mod("custom_logo")
    if (not logo_id_):
        return html_
    # end if
    logo_ = wp_get_attachment_image_src(logo_id_, "full")
    if logo_:
        #// For clarity.
        logo_width_ = esc_attr(logo_[1])
        logo_height_ = esc_attr(logo_[2])
        #// If the retina logo setting is active, reduce the width/height by half.
        if get_theme_mod("retina_logo", False):
            logo_width_ = floor(logo_width_ / 2)
            logo_height_ = floor(logo_height_ / 2)
            search_ = Array("/width=\\\"\\d+\\\"/iU", "/height=\\\"\\d+\\\"/iU")
            replace_ = Array(str("width=\"") + str(logo_width_) + str("\""), str("height=\"") + str(logo_height_) + str("\""))
            #// Add a style attribute with the height, or append the height to the style attribute if the style attribute already exists.
            if php_strpos(html_, " style=") == False:
                search_[-1] = "/(src=)/"
                replace_[-1] = str("style=\"height: ") + str(logo_height_) + str("px;\" src=")
            else:
                search_[-1] = "/(style=\"[^\"]*)/"
                replace_[-1] = str("$1 height: ") + str(logo_height_) + str("px;")
            # end if
            html_ = php_preg_replace(search_, replace_, html_)
        # end if
    # end if
    return html_
# end def twentytwenty_get_custom_logo
add_filter("get_custom_logo", "twentytwenty_get_custom_logo")
if (not php_function_exists("wp_body_open")):
    #// 
    #// Shim for wp_body_open, ensuring backward compatibility with versions of WordPress older than 5.2.
    #//
    def wp_body_open(*_args_):
        
        
        do_action("wp_body_open")
    # end def wp_body_open
# end if
#// 
#// Include a skip to content link at the top of the page so that users can bypass the menu.
#//
def twentytwenty_skip_link(*_args_):
    
    
    php_print("<a class=\"skip-link screen-reader-text\" href=\"#site-content\">" + __("Skip to the content", "twentytwenty") + "</a>")
# end def twentytwenty_skip_link
add_action("wp_body_open", "twentytwenty_skip_link", 5)
#// 
#// Register widget areas.
#// 
#// @link https://developer.wordpress.org/themes/functionality/sidebars/#registering-a-sidebar
#//
def twentytwenty_sidebar_registration(*_args_):
    
    
    #// Arguments used in all register_sidebar() calls.
    shared_args_ = Array({"before_title": "<h2 class=\"widget-title subheading heading-size-3\">", "after_title": "</h2>", "before_widget": "<div class=\"widget %2$s\"><div class=\"widget-content\">", "after_widget": "</div></div>"})
    #// Footer #1.
    register_sidebar(php_array_merge(shared_args_, Array({"name": __("Footer #1", "twentytwenty"), "id": "sidebar-1", "description": __("Widgets in this area will be displayed in the first column in the footer.", "twentytwenty")})))
    #// Footer #2.
    register_sidebar(php_array_merge(shared_args_, Array({"name": __("Footer #2", "twentytwenty"), "id": "sidebar-2", "description": __("Widgets in this area will be displayed in the second column in the footer.", "twentytwenty")})))
# end def twentytwenty_sidebar_registration
add_action("widgets_init", "twentytwenty_sidebar_registration")
#// 
#// Enqueue supplemental block editor styles.
#//
def twentytwenty_block_editor_styles(*_args_):
    
    
    css_dependencies_ = Array()
    #// Enqueue the editor styles.
    wp_enqueue_style("twentytwenty-block-editor-styles", get_theme_file_uri("/assets/css/editor-style-block.css"), css_dependencies_, wp_get_theme().get("Version"), "all")
    wp_style_add_data("twentytwenty-block-editor-styles", "rtl", "replace")
    #// Add inline style from the Customizer.
    wp_add_inline_style("twentytwenty-block-editor-styles", twentytwenty_get_customizer_css("block-editor"))
    #// Add inline style for non-latin fonts.
    wp_add_inline_style("twentytwenty-block-editor-styles", TwentyTwenty_Non_Latin_Languages.get_non_latin_css("block-editor"))
    #// Enqueue the editor script.
    wp_enqueue_script("twentytwenty-block-editor-script", get_theme_file_uri("/assets/js/editor-script-block.js"), Array("wp-blocks", "wp-dom"), wp_get_theme().get("Version"), True)
# end def twentytwenty_block_editor_styles
add_action("enqueue_block_editor_assets", "twentytwenty_block_editor_styles", 1, 1)
#// 
#// Enqueue classic editor styles.
#//
def twentytwenty_classic_editor_styles(*_args_):
    
    
    classic_editor_styles_ = Array("/assets/css/editor-style-classic.css")
    add_editor_style(classic_editor_styles_)
# end def twentytwenty_classic_editor_styles
add_action("init", "twentytwenty_classic_editor_styles")
#// 
#// Output Customizer settings in the classic editor.
#// Adds styles to the head of the TinyMCE iframe. Kudos to @Otto42 for the original solution.
#// 
#// @param array $mce_init TinyMCE styles.
#// 
#// @return array $mce_init TinyMCE styles.
#//
def twentytwenty_add_classic_editor_customizer_styles(mce_init_=None, *_args_):
    
    
    styles_ = twentytwenty_get_customizer_css("classic-editor")
    if (not (php_isset(lambda : mce_init_["content_style"]))):
        mce_init_["content_style"] = styles_ + " "
    else:
        mce_init_["content_style"] += " " + styles_ + " "
    # end if
    return mce_init_
# end def twentytwenty_add_classic_editor_customizer_styles
add_filter("tiny_mce_before_init", "twentytwenty_add_classic_editor_customizer_styles")
#// 
#// Output non-latin font styles in the classic editor.
#// Adds styles to the head of the TinyMCE iframe. Kudos to @Otto42 for the original solution.
#// 
#// @param array $mce_init TinyMCE styles.
#// 
#// @return array $mce_init TinyMCE styles.
#//
def twentytwenty_add_classic_editor_non_latin_styles(mce_init_=None, *_args_):
    
    
    styles_ = TwentyTwenty_Non_Latin_Languages.get_non_latin_css("classic-editor")
    #// Return if there are no styles to add.
    if (not styles_):
        return mce_init_
    # end if
    if (not (php_isset(lambda : mce_init_["content_style"]))):
        mce_init_["content_style"] = styles_ + " "
    else:
        mce_init_["content_style"] += " " + styles_ + " "
    # end if
    return mce_init_
# end def twentytwenty_add_classic_editor_non_latin_styles
add_filter("tiny_mce_before_init", "twentytwenty_add_classic_editor_non_latin_styles")
#// 
#// Block Editor Settings.
#// Add custom colors and font sizes to the block editor.
#//
def twentytwenty_block_editor_settings(*_args_):
    
    
    #// Block Editor Palette.
    editor_color_palette_ = Array(Array({"name": __("Accent Color", "twentytwenty"), "slug": "accent", "color": twentytwenty_get_color_for_area("content", "accent")}), Array({"name": __("Primary", "twentytwenty"), "slug": "primary", "color": twentytwenty_get_color_for_area("content", "text")}), Array({"name": __("Secondary", "twentytwenty"), "slug": "secondary", "color": twentytwenty_get_color_for_area("content", "secondary")}), Array({"name": __("Subtle Background", "twentytwenty"), "slug": "subtle-background", "color": twentytwenty_get_color_for_area("content", "borders")}))
    #// Add the background option.
    background_color_ = get_theme_mod("background_color")
    if (not background_color_):
        background_color_arr_ = get_theme_support("custom-background")
        background_color_ = background_color_arr_[0]["default-color"]
    # end if
    editor_color_palette_[-1] = Array({"name": __("Background Color", "twentytwenty"), "slug": "background", "color": "#" + background_color_})
    #// If we have accent colors, add them to the block editor palette.
    if editor_color_palette_:
        add_theme_support("editor-color-palette", editor_color_palette_)
    # end if
    #// Block Editor Font Sizes.
    add_theme_support("editor-font-sizes", Array(Array({"name": _x("Small", "Name of the small font size in the block editor", "twentytwenty"), "shortName": _x("S", "Short name of the small font size in the block editor.", "twentytwenty"), "size": 18, "slug": "small"}), Array({"name": _x("Regular", "Name of the regular font size in the block editor", "twentytwenty"), "shortName": _x("M", "Short name of the regular font size in the block editor.", "twentytwenty"), "size": 21, "slug": "normal"}), Array({"name": _x("Large", "Name of the large font size in the block editor", "twentytwenty"), "shortName": _x("L", "Short name of the large font size in the block editor.", "twentytwenty"), "size": 26.25, "slug": "large"}), Array({"name": _x("Larger", "Name of the larger font size in the block editor", "twentytwenty"), "shortName": _x("XL", "Short name of the larger font size in the block editor.", "twentytwenty"), "size": 32, "slug": "larger"})))
    #// If we have a dark background color then add support for dark editor style.
    #// We can determine if the background color is dark by checking if the text-color is white.
    if "#ffffff" == php_strtolower(twentytwenty_get_color_for_area("content", "text")):
        add_theme_support("dark-editor-style")
    # end if
# end def twentytwenty_block_editor_settings
add_action("after_setup_theme", "twentytwenty_block_editor_settings")
#// 
#// Overwrite default more tag with styling and screen reader markup.
#// 
#// @param string $html The default output HTML for the more tag.
#// 
#// @return string $html
#//
def twentytwenty_read_more_tag(html_=None, *_args_):
    
    
    return php_preg_replace("/<a(.*)>(.*)<\\/a>/iU", php_sprintf("<div class=\"read-more-button-wrap\"><a$1><span class=\"faux-button\">$2</span> <span class=\"screen-reader-text\">\"%1$s\"</span></a></div>", get_the_title(get_the_ID())), html_)
# end def twentytwenty_read_more_tag
add_filter("the_content_more_link", "twentytwenty_read_more_tag")
#// 
#// Enqueues scripts for customizer controls & settings.
#// 
#// @since Twenty Twenty 1.0
#// 
#// @return void
#//
def twentytwenty_customize_controls_enqueue_scripts(*_args_):
    
    
    theme_version_ = wp_get_theme().get("Version")
    #// Add main customizer js file.
    wp_enqueue_script("twentytwenty-customize", get_template_directory_uri() + "/assets/js/customize.js", Array("jquery"), theme_version_, False)
    #// Add script for color calculations.
    wp_enqueue_script("twentytwenty-color-calculations", get_template_directory_uri() + "/assets/js/color-calculations.js", Array("wp-color-picker"), theme_version_, False)
    #// Add script for controls.
    wp_enqueue_script("twentytwenty-customize-controls", get_template_directory_uri() + "/assets/js/customize-controls.js", Array("twentytwenty-color-calculations", "customize-controls", "underscore", "jquery"), theme_version_, False)
    wp_localize_script("twentytwenty-customize-controls", "twentyTwentyBgColors", twentytwenty_get_customizer_color_vars())
# end def twentytwenty_customize_controls_enqueue_scripts
add_action("customize_controls_enqueue_scripts", "twentytwenty_customize_controls_enqueue_scripts")
#// 
#// Enqueue scripts for the customizer preview.
#// 
#// @since Twenty Twenty 1.0
#// 
#// @return void
#//
def twentytwenty_customize_preview_init(*_args_):
    
    
    theme_version_ = wp_get_theme().get("Version")
    wp_enqueue_script("twentytwenty-customize-preview", get_theme_file_uri("/assets/js/customize-preview.js"), Array("customize-preview", "customize-selective-refresh", "jquery"), theme_version_, True)
    wp_localize_script("twentytwenty-customize-preview", "twentyTwentyBgColors", twentytwenty_get_customizer_color_vars())
    wp_localize_script("twentytwenty-customize-preview", "twentyTwentyPreviewEls", twentytwenty_get_elements_array())
    wp_add_inline_script("twentytwenty-customize-preview", php_sprintf("wp.customize.selectiveRefresh.partialConstructor[ %1$s ].prototype.attrs = %2$s;", wp_json_encode("cover_opacity"), wp_json_encode(twentytwenty_customize_opacity_range())))
# end def twentytwenty_customize_preview_init
add_action("customize_preview_init", "twentytwenty_customize_preview_init")
#// 
#// Get accessible color for an area.
#// 
#// @since Twenty Twenty 1.0
#// 
#// @param string $area The area we want to get the colors for.
#// @param string $context Can be 'text' or 'accent'.
#// @return string Returns a HEX color.
#//
def twentytwenty_get_color_for_area(area_="content", context_="text", *_args_):
    
    
    #// Get the value from the theme-mod.
    settings_ = get_theme_mod("accent_accessible_colors", Array({"content": Array({"text": "#000000", "accent": "#cd2653", "secondary": "#6d6d6d", "borders": "#dcd7ca"})}, {"header-footer": Array({"text": "#000000", "accent": "#cd2653", "secondary": "#6d6d6d", "borders": "#dcd7ca"})}))
    #// If we have a value return it.
    if (php_isset(lambda : settings_[area_])) and (php_isset(lambda : settings_[area_][context_])):
        return settings_[area_][context_]
    # end if
    #// Return false if the option doesn't exist.
    return False
# end def twentytwenty_get_color_for_area
#// 
#// Returns an array of variables for the customizer preview.
#// 
#// @since Twenty Twenty 1.0
#// 
#// @return array
#//
def twentytwenty_get_customizer_color_vars(*_args_):
    
    
    colors_ = Array({"content": Array({"setting": "background_color"})}, {"header-footer": Array({"setting": "header_footer_background_color"})})
    return colors_
# end def twentytwenty_get_customizer_color_vars
#// 
#// Get an array of elements.
#// 
#// @since Twenty Twenty 1.0
#// 
#// @return array
#//
def twentytwenty_get_elements_array(*_args_):
    
    
    #// The array is formatted like this:
    #// [key-in-saved-setting][sub-key-in-setting][css-property] = [elements].
    elements_ = Array({"content": Array({"accent": Array({"color": Array(".color-accent", ".color-accent-hover:hover", ".color-accent-hover:focus", ":root .has-accent-color", ".has-drop-cap:not(:focus):first-letter", ".wp-block-button.is-style-outline", "a"), "border-color": Array("blockquote", ".border-color-accent", ".border-color-accent-hover:hover", ".border-color-accent-hover:focus"), "background-color": Array("button:not(.toggle)", ".button", ".faux-button", ".wp-block-button__link", ".wp-block-file .wp-block-file__button", "input[type=\"button\"]", "input[type=\"reset\"]", "input[type=\"submit\"]", ".bg-accent", ".bg-accent-hover:hover", ".bg-accent-hover:focus", ":root .has-accent-background-color", ".comment-reply-link"), "fill": Array(".fill-children-accent", ".fill-children-accent *")})}, {"background": Array({"color": Array(":root .has-background-color", "button", ".button", ".faux-button", ".wp-block-button__link", ".wp-block-file__button", "input[type=\"button\"]", "input[type=\"reset\"]", "input[type=\"submit\"]", ".wp-block-button", ".comment-reply-link", ".has-background.has-primary-background-color:not(.has-text-color)", ".has-background.has-primary-background-color *:not(.has-text-color)", ".has-background.has-accent-background-color:not(.has-text-color)", ".has-background.has-accent-background-color *:not(.has-text-color)"), "background-color": Array(":root .has-background-background-color")})}, {"text": Array({"color": Array("body", ".entry-title a", ":root .has-primary-color"), "background-color": Array(":root .has-primary-background-color")})}, {"secondary": Array({"color": Array("cite", "figcaption", ".wp-caption-text", ".post-meta", ".entry-content .wp-block-archives li", ".entry-content .wp-block-categories li", ".entry-content .wp-block-latest-posts li", ".wp-block-latest-comments__comment-date", ".wp-block-latest-posts__post-date", ".wp-block-embed figcaption", ".wp-block-image figcaption", ".wp-block-pullquote cite", ".comment-metadata", ".comment-respond .comment-notes", ".comment-respond .logged-in-as", ".pagination .dots", ".entry-content hr:not(.has-background)", "hr.styled-separator", ":root .has-secondary-color"), "background-color": Array(":root .has-secondary-background-color")})}, {"borders": Array({"border-color": Array("pre", "fieldset", "input", "textarea", "table", "table *", "hr"), "background-color": Array("caption", "code", "code", "kbd", "samp", ".wp-block-table.is-style-stripes tbody tr:nth-child(odd)", ":root .has-subtle-background-background-color"), "border-bottom-color": Array(".wp-block-table.is-style-stripes"), "border-top-color": Array(".wp-block-latest-posts.is-grid li"), "color": Array(":root .has-subtle-background-color")})})}, {"header-footer": Array({"accent": Array({"color": Array("body:not(.overlay-header) .primary-menu > li > a", "body:not(.overlay-header) .primary-menu > li > .icon", ".modal-menu a", ".footer-menu a, .footer-widgets a", "#site-footer .wp-block-button.is-style-outline", ".wp-block-pullquote:before", ".singular:not(.overlay-header) .entry-header a", ".archive-header a", ".header-footer-group .color-accent", ".header-footer-group .color-accent-hover:hover"), "background-color": Array(".social-icons a", "#site-footer button:not(.toggle)", "#site-footer .button", "#site-footer .faux-button", "#site-footer .wp-block-button__link", "#site-footer .wp-block-file__button", "#site-footer input[type=\"button\"]", "#site-footer input[type=\"reset\"]", "#site-footer input[type=\"submit\"]")})}, {"background": Array({"color": Array(".social-icons a", "body:not(.overlay-header) .primary-menu ul", ".header-footer-group button", ".header-footer-group .button", ".header-footer-group .faux-button", ".header-footer-group .wp-block-button:not(.is-style-outline) .wp-block-button__link", ".header-footer-group .wp-block-file__button", ".header-footer-group input[type=\"button\"]", ".header-footer-group input[type=\"reset\"]", ".header-footer-group input[type=\"submit\"]"), "background-color": Array("#site-header", ".footer-nav-widgets-wrapper", "#site-footer", ".menu-modal", ".menu-modal-inner", ".search-modal-inner", ".archive-header", ".singular .entry-header", ".singular .featured-media:before", ".wp-block-pullquote:before")})}, {"text": Array({"color": Array(".header-footer-group", "body:not(.overlay-header) #site-header .toggle", ".menu-modal .toggle"), "background-color": Array("body:not(.overlay-header) .primary-menu ul"), "border-bottom-color": Array("body:not(.overlay-header) .primary-menu > li > ul:after"), "border-left-color": Array("body:not(.overlay-header) .primary-menu ul ul:after")})}, {"secondary": Array({"color": Array(".site-description", "body:not(.overlay-header) .toggle-inner .toggle-text", ".widget .post-date", ".widget .rss-date", ".widget_archive li", ".widget_categories li", ".widget cite", ".widget_pages li", ".widget_meta li", ".widget_nav_menu li", ".powered-by-wordpress", ".to-the-top", ".singular .entry-header .post-meta", ".singular:not(.overlay-header) .entry-header .post-meta a")})}, {"borders": Array({"border-color": Array(".header-footer-group pre", ".header-footer-group fieldset", ".header-footer-group input", ".header-footer-group textarea", ".header-footer-group table", ".header-footer-group table *", ".footer-nav-widgets-wrapper", "#site-footer", ".menu-modal nav *", ".footer-widgets-outer-wrapper", ".footer-top"), "background-color": Array(".header-footer-group table caption", "body:not(.overlay-header) .header-inner .toggle-wrapper::before")})})})
    #// 
    #// Filters Twenty Twenty theme elements
    #// 
    #// @since Twenty Twenty 1.0
    #// 
    #// @param array Array of elements
    #//
    return apply_filters("twentytwenty_get_elements_array", elements_)
# end def twentytwenty_get_elements_array
