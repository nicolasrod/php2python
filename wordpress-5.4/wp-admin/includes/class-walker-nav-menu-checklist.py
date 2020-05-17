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
#// Navigation Menu API: Walker_Nav_Menu_Checklist class
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 4.4.0
#// 
#// 
#// Create HTML list of nav menu input items.
#// 
#// @since 3.0.0
#// @uses Walker_Nav_Menu
#//
class Walker_Nav_Menu_Checklist(Walker_Nav_Menu):
    #// 
    #// @param array $fields
    #//
    def __init__(self, fields_=None):
        if fields_ is None:
            fields_ = False
        # end if
        
        if fields_:
            self.db_fields = fields_
        # end if
    # end def __init__
    #// 
    #// Starts the list before the elements are added.
    #// 
    #// @see Walker_Nav_Menu::start_lvl()
    #// 
    #// @since 3.0.0
    #// 
    #// @param string   $output Used to append additional content (passed by reference).
    #// @param int      $depth  Depth of page. Used for padding.
    #// @param stdClass $args   Not used.
    #//
    def start_lvl(self, output_=None, depth_=0, args_=None):
        
        
        indent_ = php_str_repeat("  ", depth_)
        output_ += str("\n") + str(indent_) + str("<ul class='children'>\n")
    # end def start_lvl
    #// 
    #// Ends the list of after the elements are added.
    #// 
    #// @see Walker_Nav_Menu::end_lvl()
    #// 
    #// @since 3.0.0
    #// 
    #// @param string   $output Used to append additional content (passed by reference).
    #// @param int      $depth  Depth of page. Used for padding.
    #// @param stdClass $args   Not used.
    #//
    def end_lvl(self, output_=None, depth_=0, args_=None):
        
        
        indent_ = php_str_repeat("  ", depth_)
        output_ += str("\n") + str(indent_) + str("</ul>")
    # end def end_lvl
    #// 
    #// Start the element output.
    #// 
    #// @see Walker_Nav_Menu::start_el()
    #// 
    #// @since 3.0.0
    #// 
    #// @global int        $_nav_menu_placeholder
    #// @global int|string $nav_menu_selected_id
    #// 
    #// @param string   $output Used to append additional content (passed by reference).
    #// @param WP_Post  $item   Menu item data object.
    #// @param int      $depth  Depth of menu item. Used for padding.
    #// @param stdClass $args   Not used.
    #// @param int      $id     Not used.
    #//
    def start_el(self, output_=None, item_=None, depth_=0, args_=None, id_=0):
        
        
        global _nav_menu_placeholder_
        global nav_menu_selected_id_
        php_check_if_defined("_nav_menu_placeholder_","nav_menu_selected_id_")
        _nav_menu_placeholder_ = php_intval(_nav_menu_placeholder_) - 1 if 0 > _nav_menu_placeholder_ else -1
        possible_object_id_ = item_.object_id if (php_isset(lambda : item_.post_type)) and "nav_menu_item" == item_.post_type else _nav_menu_placeholder_
        possible_db_id_ = php_int(item_.ID) if (not php_empty(lambda : item_.ID)) and 0 < possible_object_id_ else 0
        indent_ = php_str_repeat("  ", depth_) if depth_ else ""
        output_ += indent_ + "<li>"
        output_ += "<label class=\"menu-item-title\">"
        output_ += "<input type=\"checkbox\"" + wp_nav_menu_disabled_check(nav_menu_selected_id_, False) + " class=\"menu-item-checkbox"
        if (not php_empty(lambda : item_.front_or_home)):
            output_ += " add-to-top"
        # end if
        output_ += "\" name=\"menu-item[" + possible_object_id_ + "][menu-item-object-id]\" value=\"" + esc_attr(item_.object_id) + "\" /> "
        if (not php_empty(lambda : item_.label)):
            title_ = item_.label
        elif (php_isset(lambda : item_.post_type)):
            #// This filter is documented in wp-includes/post-template.php
            title_ = apply_filters("the_title", item_.post_title, item_.ID)
        # end if
        output_ += esc_html(title_) if (php_isset(lambda : title_)) else esc_html(item_.title)
        if php_empty(lambda : item_.label) and (php_isset(lambda : item_.post_type)) and "page" == item_.post_type:
            #// Append post states.
            output_ += _post_states(item_, False)
        # end if
        output_ += "</label>"
        #// Menu item hidden fields.
        output_ += "<input type=\"hidden\" class=\"menu-item-db-id\" name=\"menu-item[" + possible_object_id_ + "][menu-item-db-id]\" value=\"" + possible_db_id_ + "\" />"
        output_ += "<input type=\"hidden\" class=\"menu-item-object\" name=\"menu-item[" + possible_object_id_ + "][menu-item-object]\" value=\"" + esc_attr(item_.object) + "\" />"
        output_ += "<input type=\"hidden\" class=\"menu-item-parent-id\" name=\"menu-item[" + possible_object_id_ + "][menu-item-parent-id]\" value=\"" + esc_attr(item_.menu_item_parent) + "\" />"
        output_ += "<input type=\"hidden\" class=\"menu-item-type\" name=\"menu-item[" + possible_object_id_ + "][menu-item-type]\" value=\"" + esc_attr(item_.type) + "\" />"
        output_ += "<input type=\"hidden\" class=\"menu-item-title\" name=\"menu-item[" + possible_object_id_ + "][menu-item-title]\" value=\"" + esc_attr(item_.title) + "\" />"
        output_ += "<input type=\"hidden\" class=\"menu-item-url\" name=\"menu-item[" + possible_object_id_ + "][menu-item-url]\" value=\"" + esc_attr(item_.url) + "\" />"
        output_ += "<input type=\"hidden\" class=\"menu-item-target\" name=\"menu-item[" + possible_object_id_ + "][menu-item-target]\" value=\"" + esc_attr(item_.target) + "\" />"
        output_ += "<input type=\"hidden\" class=\"menu-item-attr-title\" name=\"menu-item[" + possible_object_id_ + "][menu-item-attr-title]\" value=\"" + esc_attr(item_.attr_title) + "\" />"
        output_ += "<input type=\"hidden\" class=\"menu-item-classes\" name=\"menu-item[" + possible_object_id_ + "][menu-item-classes]\" value=\"" + esc_attr(php_implode(" ", item_.classes)) + "\" />"
        output_ += "<input type=\"hidden\" class=\"menu-item-xfn\" name=\"menu-item[" + possible_object_id_ + "][menu-item-xfn]\" value=\"" + esc_attr(item_.xfn) + "\" />"
    # end def start_el
# end class Walker_Nav_Menu_Checklist
