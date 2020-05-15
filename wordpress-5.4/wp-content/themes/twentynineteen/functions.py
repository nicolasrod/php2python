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
#// Twenty Nineteen functions and definitions
#// 
#// @link https://developer.wordpress.org/themes/basics/theme-functions
#// 
#// @package WordPress
#// @subpackage Twenty_Nineteen
#// @since Twenty Nineteen 1.0
#// 
#// 
#// Twenty Nineteen only works in WordPress 4.7 or later.
#//
if php_version_compare(PHP_GLOBALS["wp_version"], "4.7", "<"):
    php_include_file(get_template_directory() + "/inc/back-compat.php", once=False)
    sys.exit(-1)
# end if
if (not php_function_exists("twentynineteen_setup")):
    #// 
    #// Sets up theme defaults and registers support for various WordPress features.
    #// 
    #// Note that this function is hooked into the after_setup_theme hook, which
    #// runs before the init hook. The init hook is too late for some features, such
    #// as indicating support for post thumbnails.
    #//
    def twentynineteen_setup(*args_):
        
        #// 
        #// Make theme available for translation.
        #// Translations can be filed in the /languages/ directory.
        #// If you're building a theme based on Twenty Nineteen, use a find and replace
        #// to change 'twentynineteen' to the name of your theme in all the template files.
        #//
        load_theme_textdomain("twentynineteen", get_template_directory() + "/languages")
        #// Add default posts and comments RSS feed links to head.
        add_theme_support("automatic-feed-links")
        #// 
        #// Let WordPress manage the document title.
        #// By adding theme support, we declare that this theme does not use a
        #// hard-coded <title> tag in the document head, and expect WordPress to
        #// provide it for us.
        #//
        add_theme_support("title-tag")
        #// 
        #// Enable support for Post Thumbnails on posts and pages.
        #// 
        #// @link https://developer.wordpress.org/themes/functionality/featured-images-post-thumbnails
        #//
        add_theme_support("post-thumbnails")
        set_post_thumbnail_size(1568, 9999)
        #// This theme uses wp_nav_menu() in two locations.
        register_nav_menus(Array({"menu-1": __("Primary", "twentynineteen"), "footer": __("Footer Menu", "twentynineteen"), "social": __("Social Links Menu", "twentynineteen")}))
        #// 
        #// Switch default core markup for search form, comment form, and comments
        #// to output valid HTML5.
        #//
        add_theme_support("html5", Array("search-form", "comment-form", "comment-list", "gallery", "caption", "script", "style"))
        #// 
        #// Add support for core custom logo.
        #// 
        #// @link https://codex.wordpress.org/Theme_Logo
        #//
        add_theme_support("custom-logo", Array({"height": 190, "width": 190, "flex-width": False, "flex-height": False}))
        #// Add theme support for selective refresh for widgets.
        add_theme_support("customize-selective-refresh-widgets")
        #// Add support for Block Styles.
        add_theme_support("wp-block-styles")
        #// Add support for full and wide align images.
        add_theme_support("align-wide")
        #// Add support for editor styles.
        add_theme_support("editor-styles")
        #// Enqueue editor styles.
        add_editor_style("style-editor.css")
        #// Add custom editor font sizes.
        add_theme_support("editor-font-sizes", Array(Array({"name": __("Small", "twentynineteen"), "shortName": __("S", "twentynineteen"), "size": 19.5, "slug": "small"}), Array({"name": __("Normal", "twentynineteen"), "shortName": __("M", "twentynineteen"), "size": 22, "slug": "normal"}), Array({"name": __("Large", "twentynineteen"), "shortName": __("L", "twentynineteen"), "size": 36.5, "slug": "large"}), Array({"name": __("Huge", "twentynineteen"), "shortName": __("XL", "twentynineteen"), "size": 49.5, "slug": "huge"})))
        #// Editor color palette.
        add_theme_support("editor-color-palette", Array(Array({"name": __("Blue", "twentynineteen") if "default" == get_theme_mod("primary_color") else None, "slug": "primary", "color": twentynineteen_hsl_hex(199 if "default" == get_theme_mod("primary_color") else get_theme_mod("primary_color_hue", 199), 100, 33)}), Array({"name": __("Dark Blue", "twentynineteen") if "default" == get_theme_mod("primary_color") else None, "slug": "secondary", "color": twentynineteen_hsl_hex(199 if "default" == get_theme_mod("primary_color") else get_theme_mod("primary_color_hue", 199), 100, 23)}), Array({"name": __("Dark Gray", "twentynineteen"), "slug": "dark-gray", "color": "#111"}), Array({"name": __("Light Gray", "twentynineteen"), "slug": "light-gray", "color": "#767676"}), Array({"name": __("White", "twentynineteen"), "slug": "white", "color": "#FFF"})))
        #// Add support for responsive embedded content.
        add_theme_support("responsive-embeds")
    # end def twentynineteen_setup
# end if
add_action("after_setup_theme", "twentynineteen_setup")
#// 
#// Register widget area.
#// 
#// @link https://developer.wordpress.org/themes/functionality/sidebars/#registering-a-sidebar
#//
def twentynineteen_widgets_init(*args_):
    
    register_sidebar(Array({"name": __("Footer", "twentynineteen"), "id": "sidebar-1", "description": __("Add widgets here to appear in your footer.", "twentynineteen"), "before_widget": "<section id=\"%1$s\" class=\"widget %2$s\">", "after_widget": "</section>", "before_title": "<h2 class=\"widget-title\">", "after_title": "</h2>"}))
# end def twentynineteen_widgets_init
add_action("widgets_init", "twentynineteen_widgets_init")
#// 
#// Set the content width in pixels, based on the theme's design and stylesheet.
#// 
#// Priority 0 to make it available to lower priority callbacks.
#// 
#// @global int $content_width Content width.
#//
def twentynineteen_content_width(*args_):
    global PHP_GLOBALS
    #// This variable is intended to be overruled from themes.
    #// Open WPCS issue: {@link https://github.com/WordPress-Coding-Standards/WordPress-Coding-Standards/issues/1043}.
    #// phpcs:ignore WordPress.NamingConventions.PrefixAllGlobals.NonPrefixedVariableFound
    PHP_GLOBALS["content_width"] = apply_filters("twentynineteen_content_width", 640)
# end def twentynineteen_content_width
add_action("after_setup_theme", "twentynineteen_content_width", 0)
#// 
#// Enqueue scripts and styles.
#//
def twentynineteen_scripts(*args_):
    
    wp_enqueue_style("twentynineteen-style", get_stylesheet_uri(), Array(), wp_get_theme().get("Version"))
    wp_style_add_data("twentynineteen-style", "rtl", "replace")
    if has_nav_menu("menu-1"):
        wp_enqueue_script("twentynineteen-priority-menu", get_theme_file_uri("/js/priority-menu.js"), Array(), "20181214", True)
        wp_enqueue_script("twentynineteen-touch-navigation", get_theme_file_uri("/js/touch-keyboard-navigation.js"), Array(), "20181231", True)
    # end if
    wp_enqueue_style("twentynineteen-print-style", get_template_directory_uri() + "/print.css", Array(), wp_get_theme().get("Version"), "print")
    if is_singular() and comments_open() and get_option("thread_comments"):
        wp_enqueue_script("comment-reply")
    # end if
# end def twentynineteen_scripts
add_action("wp_enqueue_scripts", "twentynineteen_scripts")
#// 
#// Fix skip link focus in IE11.
#// 
#// This does not enqueue the script because it is tiny and because it is only for IE11,
#// thus it does not warrant having an entire dedicated blocking script being loaded.
#// 
#// @link https://git.io/vWdr2
#//
def twentynineteen_skip_link_focus_fix(*args_):
    
    pass
    php_print("""   <script>
    /(trident|msie)/i.test(navigator.userAgent)&&document.getElementById&&window.addEventListener&&window.addEventListener(\"hashchange\",function(){var t,e=location.hash.substring(1);/^[A-z0-9_-]+$/.test(e)&&(t=document.getElementById(e))&&(/^(?:a|select|input|button|textarea)$/i.test(t.tagName)||(t.tabIndex=-1),t.focus())},!1);
    </script>
    """)
# end def twentynineteen_skip_link_focus_fix
add_action("wp_print_footer_scripts", "twentynineteen_skip_link_focus_fix")
#// 
#// Enqueue supplemental block editor styles.
#//
def twentynineteen_editor_customizer_styles(*args_):
    
    wp_enqueue_style("twentynineteen-editor-customizer-styles", get_theme_file_uri("/style-editor-customizer.css"), False, "1.1", "all")
    if "custom" == get_theme_mod("primary_color"):
        #// Include color patterns.
        php_include_file(get_parent_theme_file_path("/inc/color-patterns.php"), once=True)
        wp_add_inline_style("twentynineteen-editor-customizer-styles", twentynineteen_custom_colors_css())
    # end if
# end def twentynineteen_editor_customizer_styles
add_action("enqueue_block_editor_assets", "twentynineteen_editor_customizer_styles")
#// 
#// Display custom color CSS in customizer and on frontend.
#//
def twentynineteen_colors_css_wrap(*args_):
    
    #// Only include custom colors in customizer or frontend.
    if (not is_customize_preview()) and "default" == get_theme_mod("primary_color", "default") or is_admin():
        return
    # end if
    php_include_file(get_parent_theme_file_path("/inc/color-patterns.php"), once=True)
    primary_color = 199
    if "default" != get_theme_mod("primary_color", "default"):
        primary_color = get_theme_mod("primary_color_hue", 199)
    # end if
    php_print("\n   <style type=\"text/css\" id=\"custom-theme-colors\" ")
    php_print("data-hue=\"" + absint(primary_color) + "\"" if is_customize_preview() else "")
    php_print(">\n      ")
    php_print(twentynineteen_custom_colors_css())
    php_print(" </style>\n  ")
# end def twentynineteen_colors_css_wrap
add_action("wp_head", "twentynineteen_colors_css_wrap")
#// 
#// SVG Icons class.
#//
php_include_file(get_template_directory() + "/classes/class-twentynineteen-svg-icons.php", once=False)
#// 
#// Custom Comment Walker template.
#//
php_include_file(get_template_directory() + "/classes/class-twentynineteen-walker-comment.php", once=False)
#// 
#// Common theme functions.
#//
php_include_file(get_template_directory() + "/inc/helper-functions.php", once=False)
#// 
#// SVG Icons related functions.
#//
php_include_file(get_template_directory() + "/inc/icon-functions.php", once=False)
#// 
#// Enhance the theme by hooking into WordPress.
#//
php_include_file(get_template_directory() + "/inc/template-functions.php", once=False)
#// 
#// Custom template tags for the theme.
#//
php_include_file(get_template_directory() + "/inc/template-tags.php", once=False)
#// 
#// Customizer additions.
#//
php_include_file(get_template_directory() + "/inc/customizer.php", once=False)
