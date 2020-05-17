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
#// Bookmark Template Functions for usage in Themes
#// 
#// @package WordPress
#// @subpackage Template
#// 
#// 
#// The formatted output of a list of bookmarks.
#// 
#// The $bookmarks array must contain bookmark objects and will be iterated over
#// to retrieve the bookmark to be used in the output.
#// 
#// The output is formatted as HTML with no way to change that format. However,
#// what is between, before, and after can be changed. The link itself will be
#// HTML.
#// 
#// This function is used internally by wp_list_bookmarks() and should not be
#// used by themes.
#// 
#// @since 2.1.0
#// @access private
#// 
#// @param array $bookmarks List of bookmarks to traverse.
#// @param string|array $args {
#// Optional. Bookmarks arguments.
#// 
#// @type int|bool $show_updated     Whether to show the time the bookmark was last updated.
#// Accepts 1|true or 0|false. Default 0|false.
#// @type int|bool $show_description Whether to show the bookmark description. Accepts 1|true,
#// Accepts 1|true or 0|false. Default 0|false.
#// @type int|bool $show_images      Whether to show the link image if available. Accepts 1|true
#// or 0|false. Default 1|true.
#// @type int|bool $show_name        Whether to show link name if available. Accepts 1|true or
#// 0|false. Default 0|false.
#// @type string   $before           The HTML or text to prepend to each bookmark. Default `<li>`.
#// @type string   $after            The HTML or text to append to each bookmark. Default `</li>`.
#// @type string   $link_before      The HTML or text to prepend to each bookmark inside the anchor
#// tags. Default empty.
#// @type string   $link_after       The HTML or text to append to each bookmark inside the anchor
#// tags. Default empty.
#// @type string   $between          The string for use in between the link, description, and image.
#// Default "\n".
#// @type int|bool $show_rating      Whether to show the link rating. Accepts 1|true or 0|false.
#// Default 0|false.
#// 
#// }
#// @return string Formatted output in HTML
#//
def _walk_bookmarks(bookmarks_=None, args_="", *_args_):
    
    
    defaults_ = Array({"show_updated": 0, "show_description": 0, "show_images": 1, "show_name": 0, "before": "<li>", "after": "</li>", "between": "\n", "show_rating": 0, "link_before": "", "link_after": ""})
    parsed_args_ = wp_parse_args(args_, defaults_)
    output_ = ""
    #// Blank string to start with.
    for bookmark_ in bookmarks_:
        if (not (php_isset(lambda : bookmark_.recently_updated))):
            bookmark_.recently_updated = False
        # end if
        output_ += parsed_args_["before"]
        if parsed_args_["show_updated"] and bookmark_.recently_updated:
            output_ += "<em>"
        # end if
        the_link_ = "#"
        if (not php_empty(lambda : bookmark_.link_url)):
            the_link_ = esc_url(bookmark_.link_url)
        # end if
        desc_ = esc_attr(sanitize_bookmark_field("link_description", bookmark_.link_description, bookmark_.link_id, "display"))
        name_ = esc_attr(sanitize_bookmark_field("link_name", bookmark_.link_name, bookmark_.link_id, "display"))
        title_ = desc_
        if parsed_args_["show_updated"]:
            if "00" != php_substr(bookmark_.link_updated_f, 0, 2):
                title_ += " ("
                title_ += php_sprintf(__("Last updated: %s"), gmdate(get_option("links_updated_date_format"), bookmark_.link_updated_f + get_option("gmt_offset") * HOUR_IN_SECONDS))
                title_ += ")"
            # end if
        # end if
        alt_ = " alt=\"" + name_ + " " + title_ if parsed_args_["show_description"] else "" + "\""
        if "" != title_:
            title_ = " title=\"" + title_ + "\""
        # end if
        rel_ = bookmark_.link_rel
        if "" != rel_:
            rel_ = " rel=\"" + esc_attr(rel_) + "\""
        # end if
        target_ = bookmark_.link_target
        if "" != target_:
            target_ = " target=\"" + target_ + "\""
        # end if
        output_ += "<a href=\"" + the_link_ + "\"" + rel_ + title_ + target_ + ">"
        output_ += parsed_args_["link_before"]
        if None != bookmark_.link_image and parsed_args_["show_images"]:
            if php_strpos(bookmark_.link_image, "http") == 0:
                output_ += str("<img src=\"") + str(bookmark_.link_image) + str("\" ") + str(alt_) + str(" ") + str(title_) + str(" />")
            else:
                #// If it's a relative path.
                output_ += "<img src=\"" + get_option("siteurl") + str(bookmark_.link_image) + str("\" ") + str(alt_) + str(" ") + str(title_) + str(" />")
            # end if
            if parsed_args_["show_name"]:
                output_ += str(" ") + str(name_)
            # end if
        else:
            output_ += name_
        # end if
        output_ += parsed_args_["link_after"]
        output_ += "</a>"
        if parsed_args_["show_updated"] and bookmark_.recently_updated:
            output_ += "</em>"
        # end if
        if parsed_args_["show_description"] and "" != desc_:
            output_ += parsed_args_["between"] + desc_
        # end if
        if parsed_args_["show_rating"]:
            output_ += parsed_args_["between"] + sanitize_bookmark_field("link_rating", bookmark_.link_rating, bookmark_.link_id, "display")
        # end if
        output_ += parsed_args_["after"] + "\n"
    # end for
    #// End while.
    return output_
# end def _walk_bookmarks
#// 
#// Retrieve or echo all of the bookmarks.
#// 
#// List of default arguments are as follows:
#// 
#// These options define how the Category name will appear before the category
#// links are displayed, if 'categorize' is 1. If 'categorize' is 0, then it will
#// display for only the 'title_li' string and only if 'title_li' is not empty.
#// 
#// @since 2.1.0
#// 
#// @see _walk_bookmarks()
#// 
#// @param string|array $args {
#// Optional. String or array of arguments to list bookmarks.
#// 
#// @type string   $orderby          How to order the links by. Accepts post fields. Default 'name'.
#// @type string   $order            Whether to order bookmarks in ascending or descending order.
#// Accepts 'ASC' (ascending) or 'DESC' (descending). Default 'ASC'.
#// @type int      $limit            Amount of bookmarks to display. Accepts 1+ or -1 for all.
#// Default -1.
#// @type string   $category         Comma-separated list of category ids to include links from.
#// Default empty.
#// @type string   $category_name    Category to retrieve links for by name. Default empty.
#// @type int|bool $hide_invisible   Whether to show or hide links marked as 'invisible'. Accepts
#// 1|true or 0|false. Default 1|true.
#// @type int|bool $show_updated     Whether to display the time the bookmark was last updated.
#// Accepts 1|true or 0|false. Default 0|false.
#// @type int|bool $echo             Whether to echo or return the formatted bookmarks. Accepts
#// 1|true (echo) or 0|false (return). Default 1|true.
#// @type int|bool $categorize       Whether to show links listed by category or in a single column.
#// Accepts 1|true (by category) or 0|false (one column). Default 1|true.
#// @type int|bool $show_description Whether to show the bookmark descriptions. Accepts 1|true or 0|false.
#// Default 0|false.
#// @type string   $title_li         What to show before the links appear. Default 'Bookmarks'.
#// @type string   $title_before     The HTML or text to prepend to the $title_li string. Default '<h2>'.
#// @type string   $title_after      The HTML or text to append to the $title_li string. Default '</h2>'.
#// @type string   $class            The CSS class to use for the $title_li. Default 'linkcat'.
#// @type string   $category_before  The HTML or text to prepend to $title_before if $categorize is true.
#// String must contain '%id' and '%class' to inherit the category ID and
#// the $class argument used for formatting in themes.
#// Default '<li id="%id" class="%class">'.
#// @type string   $category_after   The HTML or text to append to $title_after if $categorize is true.
#// Default '</li>'.
#// @type string   $category_orderby How to order the bookmark category based on term scheme if $categorize
#// is true. Default 'name'.
#// @type string   $category_order   Whether to order categories in ascending or descending order if
#// $categorize is true. Accepts 'ASC' (ascending) or 'DESC' (descending).
#// Default 'ASC'.
#// }
#// @return void|string Void if 'echo' argument is true, HTML list of bookmarks if 'echo' is false.
#//
def wp_list_bookmarks(args_="", *_args_):
    
    
    defaults_ = Array({"orderby": "name", "order": "ASC", "limit": -1, "category": "", "exclude_category": "", "category_name": "", "hide_invisible": 1, "show_updated": 0, "echo": 1, "categorize": 1, "title_li": __("Bookmarks"), "title_before": "<h2>", "title_after": "</h2>", "category_orderby": "name", "category_order": "ASC", "class": "linkcat", "category_before": "<li id=\"%id\" class=\"%class\">", "category_after": "</li>"})
    parsed_args_ = wp_parse_args(args_, defaults_)
    output_ = ""
    if (not php_is_array(parsed_args_["class"])):
        parsed_args_["class"] = php_explode(" ", parsed_args_["class"])
    # end if
    parsed_args_["class"] = php_array_map("sanitize_html_class", parsed_args_["class"])
    parsed_args_["class"] = php_trim(join(" ", parsed_args_["class"]))
    if parsed_args_["categorize"]:
        cats_ = get_terms(Array({"taxonomy": "link_category", "name__like": parsed_args_["category_name"], "include": parsed_args_["category"], "exclude": parsed_args_["exclude_category"], "orderby": parsed_args_["category_orderby"], "order": parsed_args_["category_order"], "hierarchical": 0}))
        if php_empty(lambda : cats_):
            parsed_args_["categorize"] = False
        # end if
    # end if
    if parsed_args_["categorize"]:
        #// Split the bookmarks into ul's for each category.
        for cat_ in cats_:
            params_ = php_array_merge(parsed_args_, Array({"category": cat_.term_id}))
            bookmarks_ = get_bookmarks(params_)
            if php_empty(lambda : bookmarks_):
                continue
            # end if
            output_ += php_str_replace(Array("%id", "%class"), Array(str("linkcat-") + str(cat_.term_id), parsed_args_["class"]), parsed_args_["category_before"])
            #// 
            #// Filters the category name.
            #// 
            #// @since 2.2.0
            #// 
            #// @param string $cat_name The category name.
            #//
            catname_ = apply_filters("link_category", cat_.name)
            output_ += parsed_args_["title_before"]
            output_ += catname_
            output_ += parsed_args_["title_after"]
            output_ += "\n  <ul class='xoxo blogroll'>\n"
            output_ += _walk_bookmarks(bookmarks_, parsed_args_)
            output_ += "\n  </ul>\n"
            output_ += parsed_args_["category_after"] + "\n"
        # end for
    else:
        #// Output one single list using title_li for the title.
        bookmarks_ = get_bookmarks(parsed_args_)
        if (not php_empty(lambda : bookmarks_)):
            if (not php_empty(lambda : parsed_args_["title_li"])):
                output_ += php_str_replace(Array("%id", "%class"), Array("linkcat-" + parsed_args_["category"], parsed_args_["class"]), parsed_args_["category_before"])
                output_ += parsed_args_["title_before"]
                output_ += parsed_args_["title_li"]
                output_ += parsed_args_["title_after"]
                output_ += "\n  <ul class='xoxo blogroll'>\n"
                output_ += _walk_bookmarks(bookmarks_, parsed_args_)
                output_ += "\n  </ul>\n"
                output_ += parsed_args_["category_after"] + "\n"
            else:
                output_ += _walk_bookmarks(bookmarks_, parsed_args_)
            # end if
        # end if
    # end if
    #// 
    #// Filters the bookmarks list before it is echoed or returned.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string $html The HTML list of bookmarks.
    #//
    html_ = apply_filters("wp_list_bookmarks", output_)
    if parsed_args_["echo"]:
        php_print(html_)
    else:
        return html_
    # end if
# end def wp_list_bookmarks
