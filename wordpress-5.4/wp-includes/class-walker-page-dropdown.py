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
    #// 
    #// What the class handles.
    #// 
    #// @since 2.1.0
    #// @var string
    #// 
    #// @see Walker::$tree_type
    #//
    tree_type = "page"
    #// 
    #// Database fields to use.
    #// 
    #// @since 2.1.0
    #// @var array
    #// 
    #// @see Walker::$db_fields
    #// @todo Decouple this
    #//
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
    def start_el(self, output_=None, page_=None, depth_=0, args_=None, id_=0):
        if args_ is None:
            args_ = Array()
        # end if
        
        pad_ = php_str_repeat("&nbsp;", depth_ * 3)
        if (not (php_isset(lambda : args_["value_field"]))) or (not (php_isset(lambda : page_.args_["value_field"]))):
            args_["value_field"] = "ID"
        # end if
        output_ += str("    <option class=\"level-") + str(depth_) + str("\" value=\"") + esc_attr(page_.args_["value_field"]) + "\""
        if page_.ID == args_["selected"]:
            output_ += " selected=\"selected\""
        # end if
        output_ += ">"
        title_ = page_.post_title
        if "" == title_:
            #// translators: %d: ID of a post.
            title_ = php_sprintf(__("#%d (no title)"), page_.ID)
        # end if
        #// 
        #// Filters the page title when creating an HTML drop-down list of pages.
        #// 
        #// @since 3.1.0
        #// 
        #// @param string  $title Page title.
        #// @param WP_Post $page  Page data object.
        #//
        title_ = apply_filters("list_pages", title_, page_)
        output_ += pad_ + esc_html(title_)
        output_ += "</option>\n"
    # end def start_el
# end class Walker_PageDropdown
