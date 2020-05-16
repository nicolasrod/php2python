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
    def __init__(self, fields=False):
        
        if fields:
            self.db_fields = fields
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
    def start_lvl(self, output=None, depth=0, args=None):
        
        indent = php_str_repeat("   ", depth)
        output += str("\n") + str(indent) + str("<ul class='children'>\n")
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
    def end_lvl(self, output=None, depth=0, args=None):
        
        indent = php_str_repeat("   ", depth)
        output += str("\n") + str(indent) + str("</ul>")
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
    def start_el(self, output=None, item=None, depth=0, args=None, id=0):
        
        global _nav_menu_placeholder,nav_menu_selected_id
        php_check_if_defined("_nav_menu_placeholder","nav_menu_selected_id")
        _nav_menu_placeholder = php_intval(_nav_menu_placeholder) - 1 if 0 > _nav_menu_placeholder else -1
        possible_object_id = item.object_id if (php_isset(lambda : item.post_type)) and "nav_menu_item" == item.post_type else _nav_menu_placeholder
        possible_db_id = php_int(item.ID) if (not php_empty(lambda : item.ID)) and 0 < possible_object_id else 0
        indent = php_str_repeat("   ", depth) if depth else ""
        output += indent + "<li>"
        output += "<label class=\"menu-item-title\">"
        output += "<input type=\"checkbox\"" + wp_nav_menu_disabled_check(nav_menu_selected_id, False) + " class=\"menu-item-checkbox"
        if (not php_empty(lambda : item.front_or_home)):
            output += " add-to-top"
        # end if
        output += "\" name=\"menu-item[" + possible_object_id + "][menu-item-object-id]\" value=\"" + esc_attr(item.object_id) + "\" /> "
        if (not php_empty(lambda : item.label)):
            title = item.label
        elif (php_isset(lambda : item.post_type)):
            #// This filter is documented in wp-includes/post-template.php
            title = apply_filters("the_title", item.post_title, item.ID)
        # end if
        output += esc_html(title) if (php_isset(lambda : title)) else esc_html(item.title)
        if php_empty(lambda : item.label) and (php_isset(lambda : item.post_type)) and "page" == item.post_type:
            #// Append post states.
            output += _post_states(item, False)
        # end if
        output += "</label>"
        #// Menu item hidden fields.
        output += "<input type=\"hidden\" class=\"menu-item-db-id\" name=\"menu-item[" + possible_object_id + "][menu-item-db-id]\" value=\"" + possible_db_id + "\" />"
        output += "<input type=\"hidden\" class=\"menu-item-object\" name=\"menu-item[" + possible_object_id + "][menu-item-object]\" value=\"" + esc_attr(item.object) + "\" />"
        output += "<input type=\"hidden\" class=\"menu-item-parent-id\" name=\"menu-item[" + possible_object_id + "][menu-item-parent-id]\" value=\"" + esc_attr(item.menu_item_parent) + "\" />"
        output += "<input type=\"hidden\" class=\"menu-item-type\" name=\"menu-item[" + possible_object_id + "][menu-item-type]\" value=\"" + esc_attr(item.type) + "\" />"
        output += "<input type=\"hidden\" class=\"menu-item-title\" name=\"menu-item[" + possible_object_id + "][menu-item-title]\" value=\"" + esc_attr(item.title) + "\" />"
        output += "<input type=\"hidden\" class=\"menu-item-url\" name=\"menu-item[" + possible_object_id + "][menu-item-url]\" value=\"" + esc_attr(item.url) + "\" />"
        output += "<input type=\"hidden\" class=\"menu-item-target\" name=\"menu-item[" + possible_object_id + "][menu-item-target]\" value=\"" + esc_attr(item.target) + "\" />"
        output += "<input type=\"hidden\" class=\"menu-item-attr-title\" name=\"menu-item[" + possible_object_id + "][menu-item-attr-title]\" value=\"" + esc_attr(item.attr_title) + "\" />"
        output += "<input type=\"hidden\" class=\"menu-item-classes\" name=\"menu-item[" + possible_object_id + "][menu-item-classes]\" value=\"" + esc_attr(php_implode(" ", item.classes)) + "\" />"
        output += "<input type=\"hidden\" class=\"menu-item-xfn\" name=\"menu-item[" + possible_object_id + "][menu-item-xfn]\" value=\"" + esc_attr(item.xfn) + "\" />"
    # end def start_el
# end class Walker_Nav_Menu_Checklist
