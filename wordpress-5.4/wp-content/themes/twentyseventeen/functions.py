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
#// Twenty Seventeen functions and definitions
#// 
#// @link https://developer.wordpress.org/themes/basics/theme-functions
#// 
#// @package WordPress
#// @subpackage Twenty_Seventeen
#// @since Twenty Seventeen 1.0
#// 
#// 
#// Twenty Seventeen only works in WordPress 4.7 or later.
#//
if php_version_compare(PHP_GLOBALS["wp_version"], "4.7-alpha", "<"):
    php_include_file(get_template_directory() + "/inc/back-compat.php", once=False)
    sys.exit(-1)
# end if
#// 
#// Sets up theme defaults and registers support for various WordPress features.
#// 
#// Note that this function is hooked into the after_setup_theme hook, which
#// runs before the init hook. The init hook is too late for some features, such
#// as indicating support for post thumbnails.
#//
def twentyseventeen_setup(*args_):
    global PHP_GLOBALS
    #// 
    #// Make theme available for translation.
    #// Translations can be filed at WordPress.org. See: https://translate.wordpress.org/projects/wp-themes/twentyseventeen
    #// If you're building a theme based on Twenty Seventeen, use a find and replace
    #// to change 'twentyseventeen' to the name of your theme in all the template files.
    #//
    load_theme_textdomain("twentyseventeen")
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
    add_image_size("twentyseventeen-featured-image", 2000, 1200, True)
    add_image_size("twentyseventeen-thumbnail-avatar", 100, 100, True)
    #// Set the default content width.
    PHP_GLOBALS["content_width"] = 525
    #// This theme uses wp_nav_menu() in two locations.
    register_nav_menus(Array({"top": __("Top Menu", "twentyseventeen"), "social": __("Social Links Menu", "twentyseventeen")}))
    #// 
    #// Switch default core markup for search form, comment form, and comments
    #// to output valid HTML5.
    #//
    add_theme_support("html5", Array("comment-form", "comment-list", "gallery", "caption", "script", "style"))
    #// 
    #// Enable support for Post Formats.
    #// 
    #// See: https://wordpress.org/support/article/post-formats
    #//
    add_theme_support("post-formats", Array("aside", "image", "video", "quote", "link", "gallery", "audio"))
    #// Add theme support for Custom Logo.
    add_theme_support("custom-logo", Array({"width": 250, "height": 250, "flex-width": True}))
    #// Add theme support for selective refresh for widgets.
    add_theme_support("customize-selective-refresh-widgets")
    #// 
    #// This theme styles the visual editor to resemble the theme style,
    #// specifically font, colors, and column width.
    #//
    add_editor_style(Array("assets/css/editor-style.css", twentyseventeen_fonts_url()))
    #// Load regular editor styles into the new block-based editor.
    add_theme_support("editor-styles")
    #// Load default block styles.
    add_theme_support("wp-block-styles")
    #// Add support for responsive embeds.
    add_theme_support("responsive-embeds")
    #// Define and register starter content to showcase the theme on new sites.
    starter_content = Array({"widgets": Array({"sidebar-1": Array("text_business_info", "search", "text_about"), "sidebar-2": Array("text_business_info"), "sidebar-3": Array("text_about", "search")})}, {"posts": Array("home", {"about": Array({"thumbnail": "{{image-sandwich}}"})}, {"contact": Array({"thumbnail": "{{image-espresso}}"})}, {"blog": Array({"thumbnail": "{{image-coffee}}"})}, {"homepage-section": Array({"thumbnail": "{{image-espresso}}"})})}, {"attachments": Array({"image-espresso": Array({"post_title": _x("Espresso", "Theme starter content", "twentyseventeen"), "file": "assets/images/espresso.jpg"})}, {"image-sandwich": Array({"post_title": _x("Sandwich", "Theme starter content", "twentyseventeen"), "file": "assets/images/sandwich.jpg"})}, {"image-coffee": Array({"post_title": _x("Coffee", "Theme starter content", "twentyseventeen"), "file": "assets/images/coffee.jpg"})})}, {"options": Array({"show_on_front": "page", "page_on_front": "{{home}}"}, {"page_for_posts": "{{blog}}"})}, {"theme_mods": Array({"panel_1": "{{homepage-section}}"}, {"panel_2": "{{about}}"}, {"panel_3": "{{blog}}"}, {"panel_4": "{{contact}}"})}, {"nav_menus": Array({"top": Array({"name": __("Top Menu", "twentyseventeen"), "items": Array("link_home", "page_about", "page_blog", "page_contact")})}, {"social": Array({"name": __("Social Links Menu", "twentyseventeen"), "items": Array("link_yelp", "link_facebook", "link_twitter", "link_instagram", "link_email")})})})
    #// 
    #// Filters Twenty Seventeen array of starter content.
    #// 
    #// @since Twenty Seventeen 1.1
    #// 
    #// @param array $starter_content Array of starter content.
    #//
    starter_content = apply_filters("twentyseventeen_starter_content", starter_content)
    add_theme_support("starter-content", starter_content)
# end def twentyseventeen_setup
add_action("after_setup_theme", "twentyseventeen_setup")
#// 
#// Set the content width in pixels, based on the theme's design and stylesheet.
#// 
#// Priority 0 to make it available to lower priority callbacks.
#// 
#// @global int $content_width
#//
def twentyseventeen_content_width(*args_):
    global PHP_GLOBALS
    content_width = PHP_GLOBALS["content_width"]
    #// Get layout.
    page_layout = get_theme_mod("page_layout")
    #// Check if layout is one column.
    if "one-column" == page_layout:
        if twentyseventeen_is_frontpage():
            content_width = 644
        elif is_page():
            content_width = 740
        # end if
    # end if
    #// Check if is single post and there is no sidebar.
    if is_single() and (not is_active_sidebar("sidebar-1")):
        content_width = 740
    # end if
    #// 
    #// Filter Twenty Seventeen content width of the theme.
    #// 
    #// @since Twenty Seventeen 1.0
    #// 
    #// @param int $content_width Content width in pixels.
    #//
    PHP_GLOBALS["content_width"] = apply_filters("twentyseventeen_content_width", content_width)
# end def twentyseventeen_content_width
add_action("template_redirect", "twentyseventeen_content_width", 0)
#// 
#// Register custom fonts.
#//
def twentyseventeen_fonts_url(*args_):
    
    fonts_url = ""
    #// 
    #// translators: If there are characters in your language that are not supported
    #// by Libre Franklin, translate this to 'off'. Do not translate into your own language.
    #//
    libre_franklin = _x("on", "Libre Franklin font: on or off", "twentyseventeen")
    if "off" != libre_franklin:
        font_families = Array()
        font_families[-1] = "Libre Franklin:300,300i,400,400i,600,600i,800,800i"
        query_args = Array({"family": urlencode(php_implode("|", font_families)), "subset": urlencode("latin,latin-ext"), "display": urlencode("fallback")})
        fonts_url = add_query_arg(query_args, "https://fonts.googleapis.com/css")
    # end if
    return esc_url_raw(fonts_url)
# end def twentyseventeen_fonts_url
#// 
#// Add preconnect for Google Fonts.
#// 
#// @since Twenty Seventeen 1.0
#// 
#// @param array  $urls           URLs to print for resource hints.
#// @param string $relation_type  The relation type the URLs are printed.
#// @return array $urls           URLs to print for resource hints.
#//
def twentyseventeen_resource_hints(urls=None, relation_type=None, *args_):
    
    if wp_style_is("twentyseventeen-fonts", "queue") and "preconnect" == relation_type:
        urls[-1] = Array({"href": "https://fonts.gstatic.com"}, "crossorigin")
    # end if
    return urls
# end def twentyseventeen_resource_hints
add_filter("wp_resource_hints", "twentyseventeen_resource_hints", 10, 2)
#// 
#// Register widget area.
#// 
#// @link https://developer.wordpress.org/themes/functionality/sidebars/#registering-a-sidebar
#//
def twentyseventeen_widgets_init(*args_):
    
    register_sidebar(Array({"name": __("Blog Sidebar", "twentyseventeen"), "id": "sidebar-1", "description": __("Add widgets here to appear in your sidebar on blog posts and archive pages.", "twentyseventeen"), "before_widget": "<section id=\"%1$s\" class=\"widget %2$s\">", "after_widget": "</section>", "before_title": "<h2 class=\"widget-title\">", "after_title": "</h2>"}))
    register_sidebar(Array({"name": __("Footer 1", "twentyseventeen"), "id": "sidebar-2", "description": __("Add widgets here to appear in your footer.", "twentyseventeen"), "before_widget": "<section id=\"%1$s\" class=\"widget %2$s\">", "after_widget": "</section>", "before_title": "<h2 class=\"widget-title\">", "after_title": "</h2>"}))
    register_sidebar(Array({"name": __("Footer 2", "twentyseventeen"), "id": "sidebar-3", "description": __("Add widgets here to appear in your footer.", "twentyseventeen"), "before_widget": "<section id=\"%1$s\" class=\"widget %2$s\">", "after_widget": "</section>", "before_title": "<h2 class=\"widget-title\">", "after_title": "</h2>"}))
# end def twentyseventeen_widgets_init
add_action("widgets_init", "twentyseventeen_widgets_init")
#// 
#// Replaces "[...]" (appended to automatically generated excerpts) with ... and
#// a 'Continue reading' link.
#// 
#// @since Twenty Seventeen 1.0
#// 
#// @param string $link Link to single post/page.
#// @return string 'Continue reading' link prepended with an ellipsis.
#//
def twentyseventeen_excerpt_more(link=None, *args_):
    
    if is_admin():
        return link
    # end if
    link = php_sprintf("<p class=\"link-more\"><a href=\"%1$s\" class=\"more-link\">%2$s</a></p>", esc_url(get_permalink(get_the_ID())), php_sprintf(__("Continue reading<span class=\"screen-reader-text\"> \"%s\"</span>", "twentyseventeen"), get_the_title(get_the_ID())))
    return " &hellip; " + link
# end def twentyseventeen_excerpt_more
add_filter("excerpt_more", "twentyseventeen_excerpt_more")
#// 
#// Handles JavaScript detection.
#// 
#// Adds a `js` class to the root `<html>` element when JavaScript is detected.
#// 
#// @since Twenty Seventeen 1.0
#//
def twentyseventeen_javascript_detection(*args_):
    
    php_print("<script>(function(html){html.className = html.className.replace(/\\bno-js\\b/,'js')})(document.documentElement);</script>\n")
# end def twentyseventeen_javascript_detection
add_action("wp_head", "twentyseventeen_javascript_detection", 0)
#// 
#// Add a pingback url auto-discovery header for singularly identifiable articles.
#//
def twentyseventeen_pingback_header(*args_):
    
    if is_singular() and pings_open():
        printf("<link rel=\"pingback\" href=\"%s\">" + "\n", esc_url(get_bloginfo("pingback_url")))
    # end if
# end def twentyseventeen_pingback_header
add_action("wp_head", "twentyseventeen_pingback_header")
#// 
#// Display custom color CSS.
#//
def twentyseventeen_colors_css_wrap(*args_):
    
    if "custom" != get_theme_mod("colorscheme") and (not is_customize_preview()):
        return
    # end if
    php_include_file(get_parent_theme_file_path("/inc/color-patterns.php"), once=True)
    hue = absint(get_theme_mod("colorscheme_hue", 250))
    customize_preview_data_hue = ""
    if is_customize_preview():
        customize_preview_data_hue = "data-hue=\"" + hue + "\""
    # end if
    php_print(" <style type=\"text/css\" id=\"custom-theme-colors\" ")
    php_print(customize_preview_data_hue)
    php_print(">\n      ")
    php_print(twentyseventeen_custom_colors_css())
    php_print(" </style>\n  ")
# end def twentyseventeen_colors_css_wrap
add_action("wp_head", "twentyseventeen_colors_css_wrap")
#// 
#// Enqueues scripts and styles.
#//
def twentyseventeen_scripts(*args_):
    
    #// Add custom fonts, used in the main stylesheet.
    wp_enqueue_style("twentyseventeen-fonts", twentyseventeen_fonts_url(), Array(), None)
    #// Theme stylesheet.
    wp_enqueue_style("twentyseventeen-style", get_stylesheet_uri(), Array(), "20190507")
    #// Theme block stylesheet.
    wp_enqueue_style("twentyseventeen-block-style", get_theme_file_uri("/assets/css/blocks.css"), Array("twentyseventeen-style"), "20190105")
    #// Load the dark colorscheme.
    if "dark" == get_theme_mod("colorscheme", "light") or is_customize_preview():
        wp_enqueue_style("twentyseventeen-colors-dark", get_theme_file_uri("/assets/css/colors-dark.css"), Array("twentyseventeen-style"), "20190408")
    # end if
    #// Load the Internet Explorer 9 specific stylesheet, to fix display issues in the Customizer.
    if is_customize_preview():
        wp_enqueue_style("twentyseventeen-ie9", get_theme_file_uri("/assets/css/ie9.css"), Array("twentyseventeen-style"), "20161202")
        wp_style_add_data("twentyseventeen-ie9", "conditional", "IE 9")
    # end if
    #// Load the Internet Explorer 8 specific stylesheet.
    wp_enqueue_style("twentyseventeen-ie8", get_theme_file_uri("/assets/css/ie8.css"), Array("twentyseventeen-style"), "20161202")
    wp_style_add_data("twentyseventeen-ie8", "conditional", "lt IE 9")
    #// Load the html5 shiv.
    wp_enqueue_script("html5", get_theme_file_uri("/assets/js/html5.js"), Array(), "20161020")
    wp_script_add_data("html5", "conditional", "lt IE 9")
    wp_enqueue_script("twentyseventeen-skip-link-focus-fix", get_theme_file_uri("/assets/js/skip-link-focus-fix.js"), Array(), "20161114", True)
    twentyseventeen_l10n = Array({"quote": twentyseventeen_get_svg(Array({"icon": "quote-right"}))})
    if has_nav_menu("top"):
        wp_enqueue_script("twentyseventeen-navigation", get_theme_file_uri("/assets/js/navigation.js"), Array("jquery"), "20161203", True)
        twentyseventeen_l10n["expand"] = __("Expand child menu", "twentyseventeen")
        twentyseventeen_l10n["collapse"] = __("Collapse child menu", "twentyseventeen")
        twentyseventeen_l10n["icon"] = twentyseventeen_get_svg(Array({"icon": "angle-down", "fallback": True}))
    # end if
    wp_enqueue_script("twentyseventeen-global", get_theme_file_uri("/assets/js/global.js"), Array("jquery"), "20190121", True)
    wp_enqueue_script("jquery-scrollto", get_theme_file_uri("/assets/js/jquery.scrollTo.js"), Array("jquery"), "2.1.2", True)
    wp_localize_script("twentyseventeen-skip-link-focus-fix", "twentyseventeenScreenReaderText", twentyseventeen_l10n)
    if is_singular() and comments_open() and get_option("thread_comments"):
        wp_enqueue_script("comment-reply")
    # end if
# end def twentyseventeen_scripts
add_action("wp_enqueue_scripts", "twentyseventeen_scripts")
#// 
#// Enqueues styles for the block-based editor.
#// 
#// @since Twenty Seventeen 1.8
#//
def twentyseventeen_block_editor_styles(*args_):
    
    #// Block styles.
    wp_enqueue_style("twentyseventeen-block-editor-style", get_theme_file_uri("/assets/css/editor-blocks.css"), Array(), "20190328")
    #// Add custom fonts.
    wp_enqueue_style("twentyseventeen-fonts", twentyseventeen_fonts_url(), Array(), None)
# end def twentyseventeen_block_editor_styles
add_action("enqueue_block_editor_assets", "twentyseventeen_block_editor_styles")
#// 
#// Add custom image sizes attribute to enhance responsive image functionality
#// for content images.
#// 
#// @since Twenty Seventeen 1.0
#// 
#// @param string $sizes A source size value for use in a 'sizes' attribute.
#// @param array  $size  Image size. Accepts an array of width and height
#// values in pixels (in that order).
#// @return string A source size value for use in a content image 'sizes' attribute.
#//
def twentyseventeen_content_image_sizes_attr(sizes=None, size=None, *args_):
    
    width = size[0]
    if 740 <= width:
        sizes = "(max-width: 706px) 89vw, (max-width: 767px) 82vw, 740px"
    # end if
    if is_active_sidebar("sidebar-1") or is_archive() or is_search() or is_home() or is_page():
        if (not is_page() and "one-column" == get_theme_mod("page_options")) and 767 <= width:
            sizes = "(max-width: 767px) 89vw, (max-width: 1000px) 54vw, (max-width: 1071px) 543px, 580px"
        # end if
    # end if
    return sizes
# end def twentyseventeen_content_image_sizes_attr
add_filter("wp_calculate_image_sizes", "twentyseventeen_content_image_sizes_attr", 10, 2)
#// 
#// Filter the `sizes` value in the header image markup.
#// 
#// @since Twenty Seventeen 1.0
#// 
#// @param string $html   The HTML image tag markup being filtered.
#// @param object $header The custom header object returned by 'get_custom_header()'.
#// @param array  $attr   Array of the attributes for the image tag.
#// @return string The filtered header image HTML.
#//
def twentyseventeen_header_image_tag(html=None, header=None, attr=None, *args_):
    
    if (php_isset(lambda : attr["sizes"])):
        html = php_str_replace(attr["sizes"], "100vw", html)
    # end if
    return html
# end def twentyseventeen_header_image_tag
add_filter("get_header_image_tag", "twentyseventeen_header_image_tag", 10, 3)
#// 
#// Add custom image sizes attribute to enhance responsive image functionality
#// for post thumbnails.
#// 
#// @since Twenty Seventeen 1.0
#// 
#// @param array $attr       Attributes for the image markup.
#// @param int   $attachment Image attachment ID.
#// @param array $size       Registered image size or flat array of height and width dimensions.
#// @return array The filtered attributes for the image markup.
#//
def twentyseventeen_post_thumbnail_sizes_attr(attr=None, attachment=None, size=None, *args_):
    
    if is_archive() or is_search() or is_home():
        attr["sizes"] = "(max-width: 767px) 89vw, (max-width: 1000px) 54vw, (max-width: 1071px) 543px, 580px"
    else:
        attr["sizes"] = "100vw"
    # end if
    return attr
# end def twentyseventeen_post_thumbnail_sizes_attr
add_filter("wp_get_attachment_image_attributes", "twentyseventeen_post_thumbnail_sizes_attr", 10, 3)
#// 
#// Use front-page.php when Front page displays is set to a static page.
#// 
#// @since Twenty Seventeen 1.0
#// 
#// @param string $template front-page.php.
#// 
#// @return string The template to be used: blank if is_home() is true (defaults to index.php), else $template.
#//
def twentyseventeen_front_page_template(template=None, *args_):
    
    return "" if is_home() else template
# end def twentyseventeen_front_page_template
add_filter("frontpage_template", "twentyseventeen_front_page_template")
#// 
#// Modifies tag cloud widget arguments to display all tags in the same font size
#// and use list format for better accessibility.
#// 
#// @since Twenty Seventeen 1.4
#// 
#// @param array $args Arguments for tag cloud widget.
#// @return array The filtered arguments for tag cloud widget.
#//
def twentyseventeen_widget_tag_cloud_args(args=None, *args_):
    
    args["largest"] = 1
    args["smallest"] = 1
    args["unit"] = "em"
    args["format"] = "list"
    return args
# end def twentyseventeen_widget_tag_cloud_args
add_filter("widget_tag_cloud_args", "twentyseventeen_widget_tag_cloud_args")
#// 
#// Get unique ID.
#// 
#// This is a PHP implementation of Underscore's uniqueId method. A static variable
#// contains an integer that is incremented with each call. This number is returned
#// with the optional prefix. As such the returned value is not universally unique,
#// but it is unique across the life of the PHP process.
#// 
#// @since Twenty Seventeen 2.0
#// @see wp_unique_id() Themes requiring WordPress 5.0.3 and greater should use this instead.
#// 
#// @staticvar int $id_counter
#// 
#// @param string $prefix Prefix for the returned ID.
#// @return string Unique ID.
#//
def twentyseventeen_unique_id(prefix="", *args_):
    
    twentyseventeen_unique_id.id_counter = 0
    if php_function_exists("wp_unique_id"):
        return wp_unique_id(prefix)
    # end if
    twentyseventeen_unique_id.id_counter += 1
    return prefix + php_str(twentyseventeen_unique_id.id_counter)
# end def twentyseventeen_unique_id
#// 
#// Implement the Custom Header feature.
#//
php_include_file(get_parent_theme_file_path("/inc/custom-header.php"), once=False)
#// 
#// Custom template tags for this theme.
#//
php_include_file(get_parent_theme_file_path("/inc/template-tags.php"), once=False)
#// 
#// Additional features to allow styling of the templates.
#//
php_include_file(get_parent_theme_file_path("/inc/template-functions.php"), once=False)
#// 
#// Customizer additions.
#//
php_include_file(get_parent_theme_file_path("/inc/customizer.php"), once=False)
#// 
#// SVG icons functions and filters.
#//
php_include_file(get_parent_theme_file_path("/inc/icon-functions.php"), once=False)
