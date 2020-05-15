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
#// SVG icons related functions and filters
#// 
#// @package WordPress
#// @subpackage Twenty_Seventeen
#// @since Twenty Seventeen 1.0
#// 
#// 
#// Add SVG definitions to the footer.
#//
def twentyseventeen_include_svg_icons(*args_):
    
    #// Define SVG sprite file.
    svg_icons = get_parent_theme_file_path("/assets/images/svg-icons.svg")
    #// If it exists, include it.
    if php_file_exists(svg_icons):
        php_include_file(svg_icons, once=True)
    # end if
# end def twentyseventeen_include_svg_icons
add_action("wp_footer", "twentyseventeen_include_svg_icons", 9999)
#// 
#// Return SVG markup.
#// 
#// @param array $args {
#// Parameters needed to display an SVG.
#// 
#// @type string $icon  Required SVG icon filename.
#// @type string $title Optional SVG title.
#// @type string $desc  Optional SVG description.
#// }
#// @return string SVG markup.
#//
def twentyseventeen_get_svg(args=Array(), *args_):
    
    #// Make sure $args are an array.
    if php_empty(lambda : args):
        return __("Please define default parameters in the form of an array.", "twentyseventeen")
    # end if
    #// Define an icon.
    if False == php_array_key_exists("icon", args):
        return __("Please define an SVG icon filename.", "twentyseventeen")
    # end if
    #// Set defaults.
    defaults = Array({"icon": "", "title": "", "desc": "", "fallback": False})
    #// Parse args.
    args = wp_parse_args(args, defaults)
    #// Set aria hidden.
    aria_hidden = " aria-hidden=\"true\""
    #// Set ARIA.
    aria_labelledby = ""
    #// 
    #// Twenty Seventeen doesn't use the SVG title or description attributes; non-decorative icons are described with .screen-reader-text.
    #// 
    #// However, child themes can use the title and description to add information to non-decorative SVG icons to improve accessibility.
    #// 
    #// Example 1 with title: <?php echo twentyseventeen_get_svg( array( 'icon' => 'arrow-right', 'title' => __( 'This is the title', 'textdomain' ) ) ); ?>
    #// 
    #// Example 2 with title and description: <?php echo twentyseventeen_get_svg( array( 'icon' => 'arrow-right', 'title' => __( 'This is the title', 'textdomain' ), 'desc' => __( 'This is the description', 'textdomain' ) ) ); ?>
    #// 
    #// See https://www.paciellogroup.com/blog/2013/12/using-aria-enhance-svg-accessibility/.
    #//
    if args["title"]:
        aria_hidden = ""
        unique_id = twentyseventeen_unique_id()
        aria_labelledby = " aria-labelledby=\"title-" + unique_id + "\""
        if args["desc"]:
            aria_labelledby = " aria-labelledby=\"title-" + unique_id + " desc-" + unique_id + "\""
        # end if
    # end if
    #// Begin SVG markup.
    svg = "<svg class=\"icon icon-" + esc_attr(args["icon"]) + "\"" + aria_hidden + aria_labelledby + " role=\"img\">"
    #// Display the title.
    if args["title"]:
        svg += "<title id=\"title-" + unique_id + "\">" + esc_html(args["title"]) + "</title>"
        #// Display the desc only if the title is already set.
        if args["desc"]:
            svg += "<desc id=\"desc-" + unique_id + "\">" + esc_html(args["desc"]) + "</desc>"
        # end if
    # end if
    #// 
    #// Display the icon.
    #// 
    #// The whitespace around `<use>` is intentional - it is a work around to a keyboard navigation bug in Safari 10.
    #// 
    #// See https://core.trac.wordpress.org/ticket/38387.
    #//
    svg += " <use href=\"#icon-" + esc_html(args["icon"]) + "\" xlink:href=\"#icon-" + esc_html(args["icon"]) + "\"></use> "
    #// Add some markup to use as a fallback for browsers that do not support SVGs.
    if args["fallback"]:
        svg += "<span class=\"svg-fallback icon-" + esc_attr(args["icon"]) + "\"></span>"
    # end if
    svg += "</svg>"
    return svg
# end def twentyseventeen_get_svg
#// 
#// Display SVG icons in social links menu.
#// 
#// @param  string  $item_output The menu item output.
#// @param  WP_Post $item        Menu item object.
#// @param  int     $depth       Depth of the menu.
#// @param  array   $args        wp_nav_menu() arguments.
#// @return string  $item_output The menu item output with social icon.
#//
def twentyseventeen_nav_menu_social_icons(item_output=None, item=None, depth=None, args=None, *args_):
    
    #// Get supported social icons.
    social_icons = twentyseventeen_social_links_icons()
    #// Change SVG icon inside social links menu if there is supported URL.
    if "social" == args.theme_location:
        for attr,value in social_icons:
            if False != php_strpos(item_output, attr):
                item_output = php_str_replace(args.link_after, "</span>" + twentyseventeen_get_svg(Array({"icon": esc_attr(value)})), item_output)
            # end if
        # end for
    # end if
    return item_output
# end def twentyseventeen_nav_menu_social_icons
add_filter("walker_nav_menu_start_el", "twentyseventeen_nav_menu_social_icons", 10, 4)
#// 
#// Add dropdown icon if menu item has children.
#// 
#// @param  string  $title The menu item's title.
#// @param  WP_Post $item  The current menu item.
#// @param  array   $args  An array of wp_nav_menu() arguments.
#// @param  int     $depth Depth of menu item. Used for padding.
#// @return string  $title The menu item's title with dropdown icon.
#//
def twentyseventeen_dropdown_icon_to_menu_link(title=None, item=None, args=None, depth=None, *args_):
    
    if "top" == args.theme_location:
        for value in item.classes:
            if "menu-item-has-children" == value or "page_item_has_children" == value:
                title = title + twentyseventeen_get_svg(Array({"icon": "angle-down"}))
            # end if
        # end for
    # end if
    return title
# end def twentyseventeen_dropdown_icon_to_menu_link
add_filter("nav_menu_item_title", "twentyseventeen_dropdown_icon_to_menu_link", 10, 4)
#// 
#// Returns an array of supported social links (URL and icon name).
#// 
#// @return array $social_links_icons
#//
def twentyseventeen_social_links_icons(*args_):
    
    #// Supported social links icons.
    social_links_icons = Array({"behance.net": "behance", "codepen.io": "codepen", "deviantart.com": "deviantart", "digg.com": "digg", "docker.com": "dockerhub", "dribbble.com": "dribbble", "dropbox.com": "dropbox", "facebook.com": "facebook", "flickr.com": "flickr", "foursquare.com": "foursquare", "plus.google.com": "google-plus", "github.com": "github", "instagram.com": "instagram", "linkedin.com": "linkedin", "mailto:": "envelope-o", "medium.com": "medium", "pinterest.com": "pinterest-p", "pscp.tv": "periscope", "getpocket.com": "get-pocket", "reddit.com": "reddit-alien", "skype.com": "skype", "skype:": "skype", "slideshare.net": "slideshare", "snapchat.com": "snapchat-ghost", "soundcloud.com": "soundcloud", "spotify.com": "spotify", "stumbleupon.com": "stumbleupon", "tumblr.com": "tumblr", "twitch.tv": "twitch", "twitter.com": "twitter", "vimeo.com": "vimeo", "vine.co": "vine", "vk.com": "vk", "wordpress.org": "wordpress", "wordpress.com": "wordpress", "yelp.com": "yelp", "youtube.com": "youtube"})
    #// 
    #// Filter Twenty Seventeen social links icons.
    #// 
    #// @since Twenty Seventeen 1.0
    #// 
    #// @param array $social_links_icons Array of social links icons.
    #//
    return apply_filters("twentyseventeen_social_links_icons", social_links_icons)
# end def twentyseventeen_social_links_icons
