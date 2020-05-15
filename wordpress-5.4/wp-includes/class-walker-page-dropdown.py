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
#// Post API: Walker_PageDropdown class
#// 
#// @package WordPress
#// @subpackage Post
#// @since 4.4.0
#// 
#// 
#// Core class used to create an HTML drop-down list of pages.
#// 
#// @since 2.1.0
#// 
#// @see Walker
#//
class Walker_PageDropdown(Walker):
    tree_type = "page"
    db_fields = Array({"parent": "post_parent", "id": "ID"})
    #// 
    #// Starts the element output.
    #// 
    #// @since 2.1.0
    #// 
    #// @see Walker::start_el()
    #// 
    #// @param string  $output Used to append additional content. Passed by reference.
    #// @param WP_Post $page   Page data object.
    #// @param int     $depth  Optional. Depth of page in reference to parent pages. Used for padding.
    #// Default 0.
    #// @param array   $args   Optional. Uses 'selected' argument for selected page to set selected HTML
    #// attribute for option element. Uses 'value_field' argument to fill "value"
    #// attribute. See wp_dropdown_pages(). Default empty array.
    #// @param int     $id     Optional. ID of the current page. Default 0 (unused).
    #//
    def start_el(self, output=None, page=None, depth=0, args=Array(), id=0):
        
        pad = php_str_repeat("&nbsp;", depth * 3)
        if (not (php_isset(lambda : args["value_field"]))) or (not (php_isset(lambda : page.args["value_field"]))):
            args["value_field"] = "ID"
        # end if
        output += str(" <option class=\"level-") + str(depth) + str("\" value=\"") + esc_attr(page.args["value_field"]) + "\""
        if page.ID == args["selected"]:
            output += " selected=\"selected\""
        # end if
        output += ">"
        title = page.post_title
        if "" == title:
            #// translators: %d: ID of a post.
            title = php_sprintf(__("#%d (no title)"), page.ID)
        # end if
        #// 
        #// Filters the page title when creating an HTML drop-down list of pages.
        #// 
        #// @since 3.1.0
        #// 
        #// @param string  $title Page title.
        #// @param WP_Post $page  Page data object.
        #//
        title = apply_filters("list_pages", title, page)
        output += pad + esc_html(title)
        output += "</option>\n"
    # end def start_el
# end class Walker_PageDropdown
