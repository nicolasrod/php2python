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
#// Navigation Menu API: Walker_Nav_Menu_Edit class
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 4.4.0
#// 
#// 
#// Create HTML list of nav menu input items.
#// 
#// @since 3.0.0
#// 
#// @see Walker_Nav_Menu
#//
class Walker_Nav_Menu_Edit(Walker_Nav_Menu):
    #// 
    #// Starts the list before the elements are added.
    #// 
    #// @see Walker_Nav_Menu::start_lvl()
    #// 
    #// @since 3.0.0
    #// 
    #// @param string   $output Passed by reference.
    #// @param int      $depth  Depth of menu item. Used for padding.
    #// @param stdClass $args   Not used.
    #//
    def start_lvl(self, output=None, depth=0, args=None):
        
        pass
    # end def start_lvl
    #// 
    #// Ends the list of after the elements are added.
    #// 
    #// @see Walker_Nav_Menu::end_lvl()
    #// 
    #// @since 3.0.0
    #// 
    #// @param string   $output Passed by reference.
    #// @param int      $depth  Depth of menu item. Used for padding.
    #// @param stdClass $args   Not used.
    #//
    def end_lvl(self, output=None, depth=0, args=None):
        
        pass
    # end def end_lvl
    #// 
    #// Start the element output.
    #// 
    #// @see Walker_Nav_Menu::start_el()
    #// @since 3.0.0
    #// 
    #// @global int $_wp_nav_menu_max_depth
    #// 
    #// @param string   $output Used to append additional content (passed by reference).
    #// @param WP_Post  $item   Menu item data object.
    #// @param int      $depth  Depth of menu item. Used for padding.
    #// @param stdClass $args   Not used.
    #// @param int      $id     Not used.
    #//
    def start_el(self, output=None, item=None, depth=0, args=None, id=0):
        
        global _wp_nav_menu_max_depth
        php_check_if_defined("_wp_nav_menu_max_depth")
        _wp_nav_menu_max_depth = depth if depth > _wp_nav_menu_max_depth else _wp_nav_menu_max_depth
        ob_start()
        item_id = esc_attr(item.ID)
        removed_args = Array("action", "customlink-tab", "edit-menu-item", "menu-item", "page-tab", "_wpnonce")
        original_title = False
        if "taxonomy" == item.type:
            original_object = get_term(int(item.object_id), item.object)
            if original_object and (not is_wp_error(original_title)):
                original_title = original_object.name
            # end if
        elif "post_type" == item.type:
            original_object = get_post(item.object_id)
            if original_object:
                original_title = get_the_title(original_object.ID)
            # end if
        elif "post_type_archive" == item.type:
            original_object = get_post_type_object(item.object)
            if original_object:
                original_title = original_object.labels.archives
            # end if
        # end if
        classes = Array("menu-item menu-item-depth-" + depth, "menu-item-" + esc_attr(item.object), "menu-item-edit-" + "active" if (php_isset(lambda : PHP_REQUEST["edit-menu-item"])) and item_id == PHP_REQUEST["edit-menu-item"] else "inactive")
        title = item.title
        if (not php_empty(lambda : item._invalid)):
            classes[-1] = "menu-item-invalid"
            #// translators: %s: Title of an invalid menu item.
            title = php_sprintf(__("%s (Invalid)"), item.title)
        elif (php_isset(lambda : item.post_status)) and "draft" == item.post_status:
            classes[-1] = "pending"
            #// translators: %s: Title of a menu item in draft status.
            title = php_sprintf(__("%s (Pending)"), item.title)
        # end if
        title = title if (not (php_isset(lambda : item.label))) or "" == item.label else item.label
        submenu_text = ""
        if 0 == depth:
            submenu_text = "style=\"display: none;\""
        # end if
        php_print("     <li id=\"menu-item-")
        php_print(item_id)
        php_print("\" class=\"")
        php_print(php_implode(" ", classes))
        php_print("""\">
        <div class=\"menu-item-bar\">
        <div class=\"menu-item-handle\">
        <span class=\"item-title\"><span class=\"menu-item-title\">""")
        php_print(esc_html(title))
        php_print("</span> <span class=\"is-submenu\" ")
        php_print(submenu_text)
        php_print(">")
        _e("sub item")
        php_print("</span></span>\n                 <span class=\"item-controls\">\n                        <span class=\"item-type\">")
        php_print(esc_html(item.type_label))
        php_print("</span>\n                        <span class=\"item-order hide-if-js\">\n                            ")
        printf("<a href=\"%s\" class=\"item-move-up\" aria-label=\"%s\">&#8593;</a>", wp_nonce_url(add_query_arg(Array({"action": "move-up-menu-item", "menu-item": item_id}), remove_query_arg(removed_args, admin_url("nav-menus.php"))), "move-menu_item"), esc_attr__("Move up"))
        php_print("                         |\n                         ")
        printf("<a href=\"%s\" class=\"item-move-down\" aria-label=\"%s\">&#8595;</a>", wp_nonce_url(add_query_arg(Array({"action": "move-down-menu-item", "menu-item": item_id}), remove_query_arg(removed_args, admin_url("nav-menus.php"))), "move-menu_item"), esc_attr__("Move down"))
        php_print("                     </span>\n                       ")
        if (php_isset(lambda : PHP_REQUEST["edit-menu-item"])) and item_id == PHP_REQUEST["edit-menu-item"]:
            edit_url = admin_url("nav-menus.php")
        else:
            edit_url = add_query_arg(Array({"edit-menu-item": item_id}), remove_query_arg(removed_args, admin_url("nav-menus.php#menu-item-settings-" + item_id)))
        # end if
        printf("<a class=\"item-edit\" id=\"edit-%s\" href=\"%s\" aria-label=\"%s\"><span class=\"screen-reader-text\">%s</span></a>", item_id, edit_url, esc_attr__("Edit menu item"), __("Edit"))
        php_print("""                   </span>
        </div>
        </div>
        <div class=\"menu-item-settings wp-clearfix\" id=\"menu-item-settings-""")
        php_print(item_id)
        php_print("\">\n                ")
        if "custom" == item.type:
            php_print("                 <p class=\"field-url description description-wide\">\n                      <label for=\"edit-menu-item-url-")
            php_print(item_id)
            php_print("\">\n                            ")
            _e("URL")
            php_print("<br />\n                         <input type=\"text\" id=\"edit-menu-item-url-")
            php_print(item_id)
            php_print("\" class=\"widefat code edit-menu-item-url\" name=\"menu-item-url[")
            php_print(item_id)
            php_print("]\" value=\"")
            php_print(esc_attr(item.url))
            php_print("""\" />
            </label>
            </p>
            """)
        # end if
        php_print("             <p class=\"description description-wide\">\n                    <label for=\"edit-menu-item-title-")
        php_print(item_id)
        php_print("\">\n                        ")
        _e("Navigation Label")
        php_print("<br />\n                     <input type=\"text\" id=\"edit-menu-item-title-")
        php_print(item_id)
        php_print("\" class=\"widefat edit-menu-item-title\" name=\"menu-item-title[")
        php_print(item_id)
        php_print("]\" value=\"")
        php_print(esc_attr(item.title))
        php_print("""\" />
        </label>
        </p>
        <p class=\"field-title-attribute field-attr-title description description-wide\">
        <label for=\"edit-menu-item-attr-title-""")
        php_print(item_id)
        php_print("\">\n                        ")
        _e("Title Attribute")
        php_print("<br />\n                     <input type=\"text\" id=\"edit-menu-item-attr-title-")
        php_print(item_id)
        php_print("\" class=\"widefat edit-menu-item-attr-title\" name=\"menu-item-attr-title[")
        php_print(item_id)
        php_print("]\" value=\"")
        php_print(esc_attr(item.post_excerpt))
        php_print("""\" />
        </label>
        </p>
        <p class=\"field-link-target description\">
        <label for=\"edit-menu-item-target-""")
        php_print(item_id)
        php_print("\">\n                        <input type=\"checkbox\" id=\"edit-menu-item-target-")
        php_print(item_id)
        php_print("\" value=\"_blank\" name=\"menu-item-target[")
        php_print(item_id)
        php_print("]\"")
        checked(item.target, "_blank")
        php_print(" />\n                        ")
        _e("Open link in a new tab")
        php_print("""                   </label>
        </p>
        <p class=\"field-css-classes description description-thin\">
        <label for=\"edit-menu-item-classes-""")
        php_print(item_id)
        php_print("\">\n                        ")
        _e("CSS Classes (optional)")
        php_print("<br />\n                     <input type=\"text\" id=\"edit-menu-item-classes-")
        php_print(item_id)
        php_print("\" class=\"widefat code edit-menu-item-classes\" name=\"menu-item-classes[")
        php_print(item_id)
        php_print("]\" value=\"")
        php_print(esc_attr(php_implode(" ", item.classes)))
        php_print("""\" />
        </label>
        </p>
        <p class=\"field-xfn description description-thin\">
        <label for=\"edit-menu-item-xfn-""")
        php_print(item_id)
        php_print("\">\n                        ")
        _e("Link Relationship (XFN)")
        php_print("<br />\n                     <input type=\"text\" id=\"edit-menu-item-xfn-")
        php_print(item_id)
        php_print("\" class=\"widefat code edit-menu-item-xfn\" name=\"menu-item-xfn[")
        php_print(item_id)
        php_print("]\" value=\"")
        php_print(esc_attr(item.xfn))
        php_print("""\" />
        </label>
        </p>
        <p class=\"field-description description description-wide\">
        <label for=\"edit-menu-item-description-""")
        php_print(item_id)
        php_print("\">\n                        ")
        _e("Description")
        php_print("<br />\n                     <textarea id=\"edit-menu-item-description-")
        php_print(item_id)
        php_print("\" class=\"widefat edit-menu-item-description\" rows=\"3\" cols=\"20\" name=\"menu-item-description[")
        php_print(item_id)
        php_print("]\">")
        php_print(esc_html(item.description))
        pass
        php_print("</textarea>\n                        <span class=\"description\">")
        _e("The description will be displayed in the menu if the current theme supports it.")
        php_print("""</span>
        </label>
        </p>
        """)
        #// 
        #// Fires just before the move buttons of a nav menu item in the menu editor.
        #// 
        #// @since 5.4.0
        #// 
        #// @param int      $item_id Menu item ID.
        #// @param WP_Post  $item    Menu item data object.
        #// @param int      $depth   Depth of menu item. Used for padding.
        #// @param stdClass $args    An object of menu item arguments.
        #// @param int      $id      Nav menu ID.
        #//
        do_action("wp_nav_menu_item_custom_fields", item_id, item, depth, args, id)
        php_print("\n               <fieldset class=\"field-move hide-if-no-js description description-wide\">\n                    <span class=\"field-move-visual-label\" aria-hidden=\"true\">")
        _e("Move")
        php_print("</span>\n                    <button type=\"button\" class=\"button-link menus-move menus-move-up\" data-dir=\"up\">")
        _e("Up one")
        php_print("</button>\n                  <button type=\"button\" class=\"button-link menus-move menus-move-down\" data-dir=\"down\">")
        _e("Down one")
        php_print("""</button>
        <button type=\"button\" class=\"button-link menus-move menus-move-left\" data-dir=\"left\"></button>
        <button type=\"button\" class=\"button-link menus-move menus-move-right\" data-dir=\"right\"></button>
        <button type=\"button\" class=\"button-link menus-move menus-move-top\" data-dir=\"top\">""")
        _e("To the top")
        php_print("""</button>
        </fieldset>
        <div class=\"menu-item-actions description-wide submitbox\">
        """)
        if "custom" != item.type and False != original_title:
            php_print("                     <p class=\"link-to-original\">\n                            ")
            #// translators: %s: Link to menu item's original object.
            printf(__("Original: %s"), "<a href=\"" + esc_attr(item.url) + "\">" + esc_html(original_title) + "</a>")
            php_print("                     </p>\n                  ")
        # end if
        php_print("\n                   ")
        printf("<a class=\"item-delete submitdelete deletion\" id=\"delete-%s\" href=\"%s\">%s</a>", item_id, wp_nonce_url(add_query_arg(Array({"action": "delete-menu-item", "menu-item": item_id}), admin_url("nav-menus.php")), "delete-menu_item_" + item_id), __("Remove"))
        php_print("                 <span class=\"meta-sep hide-if-no-js\"> | </span>\n                 ")
        printf("<a class=\"item-cancel submitcancel hide-if-no-js\" id=\"cancel-%s\" href=\"%s#menu-item-settings-%s\">%s</a>", item_id, esc_url(add_query_arg(Array({"edit-menu-item": item_id, "cancel": time()}), admin_url("nav-menus.php"))), item_id, __("Cancel"))
        php_print("             </div>\n\n              <input class=\"menu-item-data-db-id\" type=\"hidden\" name=\"menu-item-db-id[")
        php_print(item_id)
        php_print("]\" value=\"")
        php_print(item_id)
        php_print("\" />\n              <input class=\"menu-item-data-object-id\" type=\"hidden\" name=\"menu-item-object-id[")
        php_print(item_id)
        php_print("]\" value=\"")
        php_print(esc_attr(item.object_id))
        php_print("\" />\n              <input class=\"menu-item-data-object\" type=\"hidden\" name=\"menu-item-object[")
        php_print(item_id)
        php_print("]\" value=\"")
        php_print(esc_attr(item.object))
        php_print("\" />\n              <input class=\"menu-item-data-parent-id\" type=\"hidden\" name=\"menu-item-parent-id[")
        php_print(item_id)
        php_print("]\" value=\"")
        php_print(esc_attr(item.menu_item_parent))
        php_print("\" />\n              <input class=\"menu-item-data-position\" type=\"hidden\" name=\"menu-item-position[")
        php_print(item_id)
        php_print("]\" value=\"")
        php_print(esc_attr(item.menu_order))
        php_print("\" />\n              <input class=\"menu-item-data-type\" type=\"hidden\" name=\"menu-item-type[")
        php_print(item_id)
        php_print("]\" value=\"")
        php_print(esc_attr(item.type))
        php_print("""\" />
        </div><!-- .menu-item-settings-->
        <ul class=\"menu-item-transport\"></ul>
        """)
        output += ob_get_clean()
    # end def start_el
# end class Walker_Nav_Menu_Edit
