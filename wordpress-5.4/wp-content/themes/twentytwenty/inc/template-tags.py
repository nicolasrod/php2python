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
#// Custom template tags for this theme.
#// 
#// @package WordPress
#// @subpackage Twenty_Twenty
#// @since Twenty Twenty 1.0
#// 
#// 
#// Table of Contents:
#// Logo & Description
#// Comments
#// Post Meta
#// Menus
#// Classes
#// Archives
#// Miscellaneous
#// 
#// 
#// Logo & Description
#// 
#// 
#// Displays the site logo, either text or image.
#// 
#// @param array   $args Arguments for displaying the site logo either as an image or text.
#// @param boolean $echo Echo or return the HTML.
#// 
#// @return string $html Compiled HTML based on our arguments.
#//
def twentytwenty_site_logo(args_=None, echo_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    if echo_ is None:
        echo_ = True
    # end if
    
    logo_ = get_custom_logo()
    site_title_ = get_bloginfo("name")
    contents_ = ""
    classname_ = ""
    defaults_ = Array({"logo": "%1$s<span class=\"screen-reader-text\">%2$s</span>", "logo_class": "site-logo", "title": "<a href=\"%1$s\">%2$s</a>", "title_class": "site-title", "home_wrap": "<h1 class=\"%1$s\">%2$s</h1>", "single_wrap": "<div class=\"%1$s faux-heading\">%2$s</div>", "condition": is_front_page() or is_home() and (not is_page())})
    args_ = wp_parse_args(args_, defaults_)
    #// 
    #// Filters the arguments for `twentytwenty_site_logo()`.
    #// 
    #// @param array  $args     Parsed arguments.
    #// @param array  $defaults Function's default arguments.
    #//
    args_ = apply_filters("twentytwenty_site_logo_args", args_, defaults_)
    if has_custom_logo():
        contents_ = php_sprintf(args_["logo"], logo_, esc_html(site_title_))
        classname_ = args_["logo_class"]
    else:
        contents_ = php_sprintf(args_["title"], esc_url(get_home_url(None, "/")), esc_html(site_title_))
        classname_ = args_["title_class"]
    # end if
    wrap_ = "home_wrap" if args_["condition"] else "single_wrap"
    html_ = php_sprintf(args_[wrap_], classname_, contents_)
    #// 
    #// Filters the arguments for `twentytwenty_site_logo()`.
    #// 
    #// @param string $html      Compiled html based on our arguments.
    #// @param array  $args      Parsed arguments.
    #// @param string $classname Class name based on current view, home or single.
    #// @param string $contents  HTML for site title or logo.
    #//
    html_ = apply_filters("twentytwenty_site_logo", html_, args_, classname_, contents_)
    if (not echo_):
        return html_
    # end if
    php_print(html_)
    pass
# end def twentytwenty_site_logo
#// 
#// Displays the site description.
#// 
#// @param boolean $echo Echo or return the html.
#// 
#// @return string $html The HTML to display.
#//
def twentytwenty_site_description(echo_=None, *_args_):
    if echo_ is None:
        echo_ = True
    # end if
    
    description_ = get_bloginfo("description")
    if (not description_):
        return
    # end if
    wrapper_ = "<div class=\"site-description\">%s</div><!-- .site-description -->"
    html_ = php_sprintf(wrapper_, esc_html(description_))
    #// 
    #// Filters the html for the site description.
    #// 
    #// @since Twenty Twenty 1.0
    #// 
    #// @param string $html         The HTML to display.
    #// @param string $description  Site description via `bloginfo()`.
    #// @param string $wrapper      The format used in case you want to reuse it in a `sprintf()`.
    #//
    html_ = apply_filters("twentytwenty_site_description", html_, description_, wrapper_)
    if (not echo_):
        return html_
    # end if
    php_print(html_)
    pass
# end def twentytwenty_site_description
#// 
#// Comments
#// 
#// 
#// Check if the specified comment is written by the author of the post commented on.
#// 
#// @param object $comment Comment data.
#// 
#// @return bool
#//
def twentytwenty_is_comment_by_post_author(comment_=None, *_args_):
    if comment_ is None:
        comment_ = None
    # end if
    
    if php_is_object(comment_) and comment_.user_id > 0:
        user_ = get_userdata(comment_.user_id)
        post_ = get_post(comment_.comment_post_ID)
        if (not php_empty(lambda : user_)) and (not php_empty(lambda : post_)):
            return comment_.user_id == post_.post_author
        # end if
    # end if
    return False
# end def twentytwenty_is_comment_by_post_author
#// 
#// Filter comment reply link to not JS scroll.
#// Filter the comment reply link to add a class indicating it should not use JS slow-scroll, as it
#// makes it scroll to the wrong position on the page.
#// 
#// @param string $link Link to the top of the page.
#// 
#// @return string $link Link to the top of the page.
#//
def twentytwenty_filter_comment_reply_link(link_=None, *_args_):
    
    
    link_ = php_str_replace("class='", "class='do-not-scroll ", link_)
    return link_
# end def twentytwenty_filter_comment_reply_link
add_filter("comment_reply_link", "twentytwenty_filter_comment_reply_link")
#// 
#// Post Meta
#// 
#// 
#// Get and Output Post Meta.
#// If it's a single post, output the post meta values specified in the Customizer settings.
#// 
#// @param int    $post_id The ID of the post for which the post meta should be output.
#// @param string $location Which post meta location to output – single or preview.
#//
def twentytwenty_the_post_meta(post_id_=None, location_="single-top", *_args_):
    if post_id_ is None:
        post_id_ = None
    # end if
    
    php_print(twentytwenty_get_post_meta(post_id_, location_))
    pass
# end def twentytwenty_the_post_meta
#// 
#// Filters the edit post link to add an icon and use the post meta structure.
#// 
#// @param string $link    Anchor tag for the edit link.
#// @param int    $post_id Post ID.
#// @param string $text    Anchor text.
#//
def twentytwenty_edit_post_link(link_=None, post_id_=None, text_=None, *_args_):
    
    
    if is_admin():
        return link_
    # end if
    edit_url_ = get_edit_post_link(post_id_)
    if (not edit_url_):
        return
    # end if
    text_ = php_sprintf(wp_kses(__("Edit <span class=\"screen-reader-text\">%s</span>", "twentytwenty"), Array({"span": Array({"class": Array()})})), get_the_title(post_id_))
    return "<div class=\"post-meta-wrapper post-meta-edit-link-wrapper\"><ul class=\"post-meta\"><li class=\"post-edit meta-wrapper\"><span class=\"meta-icon\">" + twentytwenty_get_theme_svg("edit") + "</span><span class=\"meta-text\"><a href=\"" + esc_url(edit_url_) + "\">" + text_ + "</a></span></li></ul><!-- .post-meta --></div><!-- .post-meta-wrapper -->"
# end def twentytwenty_edit_post_link
add_filter("edit_post_link", "twentytwenty_edit_post_link", 10, 3)
#// 
#// Get the post meta.
#// 
#// @param int    $post_id The ID of the post.
#// @param string $location The location where the meta is shown.
#//
def twentytwenty_get_post_meta(post_id_=None, location_="single-top", *_args_):
    if post_id_ is None:
        post_id_ = None
    # end if
    
    #// Require post ID.
    if (not post_id_):
        return
    # end if
    #// 
    #// Filters post types array
    #// 
    #// This filter can be used to hide post meta information of post, page or custom post type registerd by child themes or plugins
    #// 
    #// @since Twenty Twenty 1.0
    #// 
    #// @param array Array of post types
    #//
    disallowed_post_types_ = apply_filters("twentytwenty_disallowed_post_types_for_meta_output", Array("page"))
    #// Check whether the post type is allowed to output post meta.
    if php_in_array(get_post_type(post_id_), disallowed_post_types_, True):
        return
    # end if
    post_meta_wrapper_classes_ = ""
    post_meta_classes_ = ""
    #// Get the post meta settings for the location specified.
    if "single-top" == location_:
        #// 
        #// Filters post meta info visibility
        #// 
        #// Use this filter to hide post meta information like Author, Post date, Comments, Is sticky status
        #// 
        #// @since Twenty Twenty 1.0
        #// 
        #// @param array $args {
        #// @type string 'author'
        #// @type string 'post-date'
        #// @type string 'comments'
        #// @type string 'sticky'
        #// }
        #//
        post_meta_ = apply_filters("twentytwenty_post_meta_location_single_top", Array("author", "post-date", "comments", "sticky"))
        post_meta_wrapper_classes_ = " post-meta-single post-meta-single-top"
    elif "single-bottom" == location_:
        #// 
        #// Filters post tags visibility
        #// 
        #// Use this filter to hide post tags
        #// 
        #// @since Twenty Twenty 1.0
        #// 
        #// @param array $args {
        #// @type string 'tags'
        #// }
        #//
        post_meta_ = apply_filters("twentytwenty_post_meta_location_single_bottom", Array("tags"))
        post_meta_wrapper_classes_ = " post-meta-single post-meta-single-bottom"
    # end if
    #// If the post meta setting has the value 'empty', it's explicitly empty and the default post meta shouldn't be output.
    if post_meta_ and (not php_in_array("empty", post_meta_, True)):
        #// Make sure we don't output an empty container.
        has_meta_ = False
        global post_
        php_check_if_defined("post_")
        the_post_ = get_post(post_id_)
        setup_postdata(the_post_)
        ob_start()
        php_print("\n       <div class=\"post-meta-wrapper")
        php_print(esc_attr(post_meta_wrapper_classes_))
        php_print("\">\n\n          <ul class=\"post-meta")
        php_print(esc_attr(post_meta_classes_))
        php_print("\">\n\n              ")
        #// 
        #// Fires before post meta html display.
        #// 
        #// Allow output of additional post meta info to be added by child themes and plugins.
        #// 
        #// @since Twenty Twenty 1.0
        #// @since Twenty Twenty 1.1 Added the `$post_meta` and `$location` parameters.
        #// 
        #// @param int    $post_id   Post ID.
        #// @param array  $post_meta An array of post meta information.
        #// @param string $location  The location where the meta is shown.
        #// Accepts 'single-top' or 'single-bottom'.
        #//
        do_action("twentytwenty_start_of_post_meta_list", post_id_, post_meta_, location_)
        #// Author.
        if php_in_array("author", post_meta_, True):
            has_meta_ = True
            php_print("                 <li class=\"post-author meta-wrapper\">\n                       <span class=\"meta-icon\">\n                            <span class=\"screen-reader-text\">")
            _e("Post author", "twentytwenty")
            php_print("</span>\n                            ")
            twentytwenty_the_theme_svg("user")
            php_print("                     </span>\n                       <span class=\"meta-text\">\n                            ")
            printf(__("By %s", "twentytwenty"), "<a href=\"" + esc_url(get_author_posts_url(get_the_author_meta("ID"))) + "\">" + esc_html(get_the_author_meta("display_name")) + "</a>")
            php_print("                     </span>\n                   </li>\n                 ")
        # end if
        #// Post date.
        if php_in_array("post-date", post_meta_, True):
            has_meta_ = True
            php_print("                 <li class=\"post-date meta-wrapper\">\n                     <span class=\"meta-icon\">\n                            <span class=\"screen-reader-text\">")
            _e("Post date", "twentytwenty")
            php_print("</span>\n                            ")
            twentytwenty_the_theme_svg("calendar")
            php_print("                     </span>\n                       <span class=\"meta-text\">\n                            <a href=\"")
            the_permalink()
            php_print("\">")
            the_time(get_option("date_format"))
            php_print("""</a>
            </span>
            </li>
            """)
        # end if
        #// Categories.
        if php_in_array("categories", post_meta_, True) and has_category():
            has_meta_ = True
            php_print("                 <li class=\"post-categories meta-wrapper\">\n                       <span class=\"meta-icon\">\n                            <span class=\"screen-reader-text\">")
            _e("Categories", "twentytwenty")
            php_print("</span>\n                            ")
            twentytwenty_the_theme_svg("folder")
            php_print("                     </span>\n                       <span class=\"meta-text\">\n                            ")
            _ex("In", "A string that is output before one or more categories", "twentytwenty")
            php_print(" ")
            the_category(", ")
            php_print("                     </span>\n                   </li>\n                 ")
        # end if
        #// Tags.
        if php_in_array("tags", post_meta_, True) and has_tag():
            has_meta_ = True
            php_print("                 <li class=\"post-tags meta-wrapper\">\n                     <span class=\"meta-icon\">\n                            <span class=\"screen-reader-text\">")
            _e("Tags", "twentytwenty")
            php_print("</span>\n                            ")
            twentytwenty_the_theme_svg("tag")
            php_print("                     </span>\n                       <span class=\"meta-text\">\n                            ")
            the_tags("", ", ", "")
            php_print("                     </span>\n                   </li>\n                 ")
        # end if
        #// Comments link.
        if php_in_array("comments", post_meta_, True) and (not post_password_required()) and comments_open() or get_comments_number():
            has_meta_ = True
            php_print("                 <li class=\"post-comment-link meta-wrapper\">\n                     <span class=\"meta-icon\">\n                            ")
            twentytwenty_the_theme_svg("comment")
            php_print("                     </span>\n                       <span class=\"meta-text\">\n                            ")
            comments_popup_link()
            php_print("                     </span>\n                   </li>\n                 ")
        # end if
        #// Sticky.
        if php_in_array("sticky", post_meta_, True) and is_sticky():
            has_meta_ = True
            php_print("                 <li class=\"post-sticky meta-wrapper\">\n                       <span class=\"meta-icon\">\n                            ")
            twentytwenty_the_theme_svg("bookmark")
            php_print("                     </span>\n                       <span class=\"meta-text\">\n                            ")
            _e("Sticky post", "twentytwenty")
            php_print("                     </span>\n                   </li>\n                 ")
        # end if
        #// 
        #// Fires after post meta html display.
        #// 
        #// Allow output of additional post meta info to be added by child themes and plugins.
        #// 
        #// @since Twenty Twenty 1.0
        #// @since Twenty Twenty 1.1 Added the `$post_meta` and `$location` parameters.
        #// 
        #// @param int    $post_id   Post ID.
        #// @param array  $post_meta An array of post meta information.
        #// @param string $location  The location where the meta is shown.
        #// Accepts 'single-top' or 'single-bottom'.
        #//
        do_action("twentytwenty_end_of_post_meta_list", post_id_, post_meta_, location_)
        php_print("""
        </ul><!-- .post-meta -->
        </div><!-- .post-meta-wrapper -->
        """)
        wp_reset_postdata()
        meta_output_ = ob_get_clean()
        #// If there is meta to output, return it.
        if has_meta_ and meta_output_:
            return meta_output_
        # end if
    # end if
# end def twentytwenty_get_post_meta
#// 
#// Menus
#// 
#// 
#// Filter Classes of wp_list_pages items to match menu items.
#// Filter the class applied to wp_list_pages() items with children to match the menu class, to simplify.
#// styling of sub levels in the fallback. Only applied if the match_menu_classes argument is set.
#// 
#// @param array  $css_class CSS Class names.
#// @param string $item Comment.
#// @param int    $depth Depth of the current comment.
#// @param array  $args An array of arguments.
#// @param string $current_page Whether or not the item is the current item.
#// 
#// @return array $css_class CSS Class names.
#//
def twentytwenty_filter_wp_list_pages_item_classes(css_class_=None, item_=None, depth_=None, args_=None, current_page_=None, *_args_):
    
    
    #// Only apply to wp_list_pages() calls with match_menu_classes set to true.
    match_menu_classes_ = (php_isset(lambda : args_["match_menu_classes"]))
    if (not match_menu_classes_):
        return css_class_
    # end if
    #// Add current menu item class.
    if php_in_array("current_page_item", css_class_, True):
        css_class_[-1] = "current-menu-item"
    # end if
    #// Add menu item has children class.
    if php_in_array("page_item_has_children", css_class_, True):
        css_class_[-1] = "menu-item-has-children"
    # end if
    return css_class_
# end def twentytwenty_filter_wp_list_pages_item_classes
add_filter("page_css_class", "twentytwenty_filter_wp_list_pages_item_classes", 10, 5)
#// 
#// Add a Sub Nav Toggle to the Expanded Menu and Mobile Menu.
#// 
#// @param stdClass $args An array of arguments.
#// @param string   $item Menu item.
#// @param int      $depth Depth of the current menu item.
#// 
#// @return stdClass $args An object of wp_nav_menu() arguments.
#//
def twentytwenty_add_sub_toggles_to_main_menu(args_=None, item_=None, depth_=None, *_args_):
    
    
    #// Add sub menu toggles to the Expanded Menu with toggles.
    if (php_isset(lambda : args_.show_toggles)) and args_.show_toggles:
        #// Wrap the menu item link contents in a div, used for positioning.
        args_.before = "<div class=\"ancestor-wrapper\">"
        args_.after = ""
        #// Add a toggle to items with children.
        if php_in_array("menu-item-has-children", item_.classes, True):
            toggle_target_string_ = ".menu-modal .menu-item-" + item_.ID + " > .sub-menu"
            toggle_duration_ = twentytwenty_toggle_duration()
            #// Add the sub menu toggle.
            args_.after += "<button class=\"toggle sub-menu-toggle fill-children-current-color\" data-toggle-target=\"" + toggle_target_string_ + "\" data-toggle-type=\"slidetoggle\" data-toggle-duration=\"" + absint(toggle_duration_) + "\" aria-expanded=\"false\"><span class=\"screen-reader-text\">" + __("Show sub menu", "twentytwenty") + "</span>" + twentytwenty_get_theme_svg("chevron-down") + "</button>"
        # end if
        #// Close the wrapper.
        args_.after += "</div><!-- .ancestor-wrapper -->"
        pass
    elif "primary" == args_.theme_location:
        if php_in_array("menu-item-has-children", item_.classes, True):
            args_.after = "<span class=\"icon\"></span>"
        else:
            args_.after = ""
        # end if
    # end if
    return args_
# end def twentytwenty_add_sub_toggles_to_main_menu
add_filter("nav_menu_item_args", "twentytwenty_add_sub_toggles_to_main_menu", 10, 3)
#// 
#// Display SVG icons in social links menu.
#// 
#// @param  string  $item_output The menu item output.
#// @param  WP_Post $item        Menu item object.
#// @param  int     $depth       Depth of the menu.
#// @param  array   $args        wp_nav_menu() arguments.
#// @return string  $item_output The menu item output with social icon.
#//
def twentytwenty_nav_menu_social_icons(item_output_=None, item_=None, depth_=None, args_=None, *_args_):
    
    
    #// Change SVG icon inside social links menu if there is supported URL.
    if "social" == args_.theme_location:
        svg_ = TwentyTwenty_SVG_Icons.get_social_link_svg(item_.url)
        if php_empty(lambda : svg_):
            svg_ = twentytwenty_get_theme_svg("link")
        # end if
        item_output_ = php_str_replace(args_.link_after, "</span>" + svg_, item_output_)
    # end if
    return item_output_
# end def twentytwenty_nav_menu_social_icons
add_filter("walker_nav_menu_start_el", "twentytwenty_nav_menu_social_icons", 10, 4)
#// 
#// Classes
#// 
#// 
#// Add No-JS Class.
#// If we're missing JavaScript support, the HTML element will have a no-js class.
#//
def twentytwenty_no_js_class(*_args_):
    
    
    php_print(" <script>document.documentElement.className = document.documentElement.className.replace( 'no-js', 'js' );</script>\n    ")
# end def twentytwenty_no_js_class
add_action("wp_head", "twentytwenty_no_js_class")
#// 
#// Add conditional body classes.
#// 
#// @param array $classes Classes added to the body tag.
#// 
#// @return array $classes Classes added to the body tag.
#//
def twentytwenty_body_classes(classes_=None, *_args_):
    
    
    global post_
    php_check_if_defined("post_")
    post_type_ = post_.post_type if (php_isset(lambda : post_)) else False
    #// Check whether we're singular.
    if is_singular():
        classes_[-1] = "singular"
    # end if
    #// Check whether the current page should have an overlay header.
    if is_page_template(Array("templates/template-cover.php")):
        classes_[-1] = "overlay-header"
    # end if
    #// Check whether the current page has full-width content.
    if is_page_template(Array("templates/template-full-width.php")):
        classes_[-1] = "has-full-width-content"
    # end if
    #// Check for enabled search.
    if True == get_theme_mod("enable_header_search", True):
        classes_[-1] = "enable-search-modal"
    # end if
    #// Check for post thumbnail.
    if is_singular() and has_post_thumbnail():
        classes_[-1] = "has-post-thumbnail"
    elif is_singular():
        classes_[-1] = "missing-post-thumbnail"
    # end if
    #// Check whether we're in the customizer preview.
    if is_customize_preview():
        classes_[-1] = "customizer-preview"
    # end if
    #// Check if posts have single pagination.
    if is_single() and get_next_post() or get_previous_post():
        classes_[-1] = "has-single-pagination"
    else:
        classes_[-1] = "has-no-pagination"
    # end if
    #// Check if we're showing comments.
    if post_ and "post" == post_type_ or comments_open() or get_comments_number() and (not post_password_required()):
        classes_[-1] = "showing-comments"
    else:
        classes_[-1] = "not-showing-comments"
    # end if
    #// Check if avatars are visible.
    classes_[-1] = "show-avatars" if get_option("show_avatars") else "hide-avatars"
    #// Slim page template class names (class = name - file suffix).
    if is_page_template():
        classes_[-1] = php_basename(get_page_template_slug(), ".php")
    # end if
    #// Check for the elements output in the top part of the footer.
    has_footer_menu_ = has_nav_menu("footer")
    has_social_menu_ = has_nav_menu("social")
    has_sidebar_1_ = is_active_sidebar("sidebar-1")
    has_sidebar_2_ = is_active_sidebar("sidebar-2")
    #// Add a class indicating whether those elements are output.
    if has_footer_menu_ or has_social_menu_ or has_sidebar_1_ or has_sidebar_2_:
        classes_[-1] = "footer-top-visible"
    else:
        classes_[-1] = "footer-top-hidden"
    # end if
    #// Get header/footer background color.
    header_footer_background_ = get_theme_mod("header_footer_background_color", "#ffffff")
    header_footer_background_ = php_strtolower("#" + php_ltrim(header_footer_background_, "#"))
    #// Get content background color.
    background_color_ = get_theme_mod("background_color", "f5efe0")
    background_color_ = php_strtolower("#" + php_ltrim(background_color_, "#"))
    #// Add extra class if main background and header/footer background are the same color.
    if background_color_ == header_footer_background_:
        classes_[-1] = "reduced-spacing"
    # end if
    return classes_
# end def twentytwenty_body_classes
add_filter("body_class", "twentytwenty_body_classes")
#// 
#// Archives
#// 
#// 
#// Filters the archive title and styles the word before the first colon.
#// 
#// @param string $title Current archive title.
#// 
#// @return string $title Current archive title.
#//
def twentytwenty_get_the_archive_title(title_=None, *_args_):
    
    
    regex_ = apply_filters("twentytwenty_get_the_archive_title_regex", Array({"pattern": "/(\\A[^\\:]+\\:)/", "replacement": "<span class=\"color-accent\">$1</span>"}))
    if php_empty(lambda : regex_):
        return title_
    # end if
    return php_preg_replace(regex_["pattern"], regex_["replacement"], title_)
# end def twentytwenty_get_the_archive_title
add_filter("get_the_archive_title", "twentytwenty_get_the_archive_title")
#// 
#// Miscellaneous
#// 
#// 
#// Toggle animation duration in milliseconds.
#// 
#// @return integer Duration in milliseconds
#//
def twentytwenty_toggle_duration(*_args_):
    
    
    #// 
    #// Filters the animation duration/speed used usually for submenu toggles.
    #// 
    #// @since Twenty Twenty 1.0
    #// 
    #// @param integer $duration Duration in milliseconds.
    #//
    duration_ = apply_filters("twentytwenty_toggle_duration", 250)
    return duration_
# end def twentytwenty_toggle_duration
#// 
#// Get unique ID.
#// 
#// This is a PHP implementation of Underscore's uniqueId method. A static variable
#// contains an integer that is incremented with each call. This number is returned
#// with the optional prefix. As such the returned value is not universally unique,
#// but it is unique across the life of the PHP process.
#// 
#// @see wp_unique_id() Themes requiring WordPress 5.0.3 and greater should use this instead.
#// 
#// @staticvar int $id_counter
#// 
#// @param string $prefix Prefix for the returned ID.
#// @return string Unique ID.
#//
def twentytwenty_unique_id(prefix_="", *_args_):
    
    
    id_counter_ = 0
    if php_function_exists("wp_unique_id"):
        return wp_unique_id(prefix_)
    # end if
    id_counter_ += 1
    id_counter_ += 1
    return prefix_ + php_str(id_counter_)
# end def twentytwenty_unique_id
