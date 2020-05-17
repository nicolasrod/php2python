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
#// SVG icons related functions and filters
#// 
#// @package WordPress
#// @subpackage Twenty_Seventeen
#// @since Twenty Seventeen 1.0
#// 
#// 
#// Add SVG definitions to the footer.
#//
def twentyseventeen_include_svg_icons(*_args_):
    
    
    #// Define SVG sprite file.
    svg_icons_ = get_parent_theme_file_path("/assets/images/svg-icons.svg")
    #// If it exists, include it.
    if php_file_exists(svg_icons_):
        php_include_file(svg_icons_, once=True)
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
def twentyseventeen_get_svg(args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    #// Make sure $args are an array.
    if php_empty(lambda : args_):
        return __("Please define default parameters in the form of an array.", "twentyseventeen")
    # end if
    #// Define an icon.
    if False == php_array_key_exists("icon", args_):
        return __("Please define an SVG icon filename.", "twentyseventeen")
    # end if
    #// Set defaults.
    defaults_ = Array({"icon": "", "title": "", "desc": "", "fallback": False})
    #// Parse args.
    args_ = wp_parse_args(args_, defaults_)
    #// Set aria hidden.
    aria_hidden_ = " aria-hidden=\"true\""
    #// Set ARIA.
    aria_labelledby_ = ""
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
    if args_["title"]:
        aria_hidden_ = ""
        unique_id_ = twentyseventeen_unique_id()
        aria_labelledby_ = " aria-labelledby=\"title-" + unique_id_ + "\""
        if args_["desc"]:
            aria_labelledby_ = " aria-labelledby=\"title-" + unique_id_ + " desc-" + unique_id_ + "\""
        # end if
    # end if
    #// Begin SVG markup.
    svg_ = "<svg class=\"icon icon-" + esc_attr(args_["icon"]) + "\"" + aria_hidden_ + aria_labelledby_ + " role=\"img\">"
    #// Display the title.
    if args_["title"]:
        svg_ += "<title id=\"title-" + unique_id_ + "\">" + esc_html(args_["title"]) + "</title>"
        #// Display the desc only if the title is already set.
        if args_["desc"]:
            svg_ += "<desc id=\"desc-" + unique_id_ + "\">" + esc_html(args_["desc"]) + "</desc>"
        # end if
    # end if
    #// 
    #// Display the icon.
    #// 
    #// The whitespace around `<use>` is intentional - it is a work around to a keyboard navigation bug in Safari 10.
    #// 
    #// See https://core.trac.wordpress.org/ticket/38387.
    #//
    svg_ += " <use href=\"#icon-" + esc_html(args_["icon"]) + "\" xlink:href=\"#icon-" + esc_html(args_["icon"]) + "\"></use> "
    #// Add some markup to use as a fallback for browsers that do not support SVGs.
    if args_["fallback"]:
        svg_ += "<span class=\"svg-fallback icon-" + esc_attr(args_["icon"]) + "\"></span>"
    # end if
    svg_ += "</svg>"
    return svg_
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
def twentyseventeen_nav_menu_social_icons(item_output_=None, item_=None, depth_=None, args_=None, *_args_):
    
    
    #// Get supported social icons.
    social_icons_ = twentyseventeen_social_links_icons()
    #// Change SVG icon inside social links menu if there is supported URL.
    if "social" == args_.theme_location:
        for attr_,value_ in social_icons_:
            if False != php_strpos(item_output_, attr_):
                item_output_ = php_str_replace(args_.link_after, "</span>" + twentyseventeen_get_svg(Array({"icon": esc_attr(value_)})), item_output_)
            # end if
        # end for
    # end if
    return item_output_
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
def twentyseventeen_dropdown_icon_to_menu_link(title_=None, item_=None, args_=None, depth_=None, *_args_):
    
    
    if "top" == args_.theme_location:
        for value_ in item_.classes:
            if "menu-item-has-children" == value_ or "page_item_has_children" == value_:
                title_ = title_ + twentyseventeen_get_svg(Array({"icon": "angle-down"}))
            # end if
        # end for
    # end if
    return title_
# end def twentyseventeen_dropdown_icon_to_menu_link
add_filter("nav_menu_item_title", "twentyseventeen_dropdown_icon_to_menu_link", 10, 4)
#// 
#// Returns an array of supported social links (URL and icon name).
#// 
#// @return array $social_links_icons
#//
def twentyseventeen_social_links_icons(*_args_):
    
    
    #// Supported social links icons.
    social_links_icons_ = Array({"behance.net": "behance", "codepen.io": "codepen", "deviantart.com": "deviantart", "digg.com": "digg", "docker.com": "dockerhub", "dribbble.com": "dribbble", "dropbox.com": "dropbox", "facebook.com": "facebook", "flickr.com": "flickr", "foursquare.com": "foursquare", "plus.google.com": "google-plus", "github.com": "github", "instagram.com": "instagram", "linkedin.com": "linkedin", "mailto:": "envelope-o", "medium.com": "medium", "pinterest.com": "pinterest-p", "pscp.tv": "periscope", "getpocket.com": "get-pocket", "reddit.com": "reddit-alien", "skype.com": "skype", "skype:": "skype", "slideshare.net": "slideshare", "snapchat.com": "snapchat-ghost", "soundcloud.com": "soundcloud", "spotify.com": "spotify", "stumbleupon.com": "stumbleupon", "tumblr.com": "tumblr", "twitch.tv": "twitch", "twitter.com": "twitter", "vimeo.com": "vimeo", "vine.co": "vine", "vk.com": "vk", "wordpress.org": "wordpress", "wordpress.com": "wordpress", "yelp.com": "yelp", "youtube.com": "youtube"})
    #// 
    #// Filter Twenty Seventeen social links icons.
    #// 
    #// @since Twenty Seventeen 1.0
    #// 
    #// @param array $social_links_icons Array of social links icons.
    #//
    return apply_filters("twentyseventeen_social_links_icons", social_links_icons_)
# end def twentyseventeen_social_links_icons
