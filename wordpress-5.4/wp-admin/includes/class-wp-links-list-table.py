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
#// List Table API: WP_Links_List_Table class
#// 
#// @package WordPress
#// @subpackage Administration
#// @since 3.1.0
#// 
#// 
#// Core class used to implement displaying links in a list table.
#// 
#// @since 3.1.0
#// @access private
#// 
#// @see WP_List_Tsble
#//
class WP_Links_List_Table(WP_List_Table):
    #// 
    #// Constructor.
    #// 
    #// @since 3.1.0
    #// 
    #// @see WP_List_Table::__construct() for more information on default arguments.
    #// 
    #// @param array $args An associative array of arguments.
    #//
    def __init__(self, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        super().__init__(Array({"plural": "bookmarks", "screen": args_["screen"] if (php_isset(lambda : args_["screen"])) else None}))
    # end def __init__
    #// 
    #// @return bool
    #//
    def ajax_user_can(self):
        
        
        return current_user_can("manage_links")
    # end def ajax_user_can
    #// 
    #// @global int    $cat_id
    #// @global string $s
    #// @global string $orderby
    #// @global string $order
    #//
    def prepare_items(self):
        
        
        global cat_id_
        global s_
        global orderby_
        global order_
        php_check_if_defined("cat_id_","s_","orderby_","order_")
        wp_reset_vars(Array("action", "cat_id", "link_id", "orderby", "order", "s"))
        args_ = Array({"hide_invisible": 0, "hide_empty": 0})
        if "all" != cat_id_:
            args_["category"] = cat_id_
        # end if
        if (not php_empty(lambda : s_)):
            args_["search"] = s_
        # end if
        if (not php_empty(lambda : orderby_)):
            args_["orderby"] = orderby_
        # end if
        if (not php_empty(lambda : order_)):
            args_["order"] = order_
        # end if
        self.items = get_bookmarks(args_)
    # end def prepare_items
    #// 
    #//
    def no_items(self):
        
        
        _e("No links found.")
    # end def no_items
    #// 
    #// @return array
    #//
    def get_bulk_actions(self):
        
        
        actions_ = Array()
        actions_["delete"] = __("Delete")
        return actions_
    # end def get_bulk_actions
    #// 
    #// @global int $cat_id
    #// @param string $which
    #//
    def extra_tablenav(self, which_=None):
        
        
        global cat_id_
        php_check_if_defined("cat_id_")
        if "top" != which_:
            return
        # end if
        php_print("     <div class=\"alignleft actions\">\n     ")
        dropdown_options_ = Array({"selected": cat_id_, "name": "cat_id", "taxonomy": "link_category", "show_option_all": get_taxonomy("link_category").labels.all_items, "hide_empty": True, "hierarchical": 1, "show_count": 0, "orderby": "name"})
        php_print("<label class=\"screen-reader-text\" for=\"cat_id\">" + __("Filter by category") + "</label>")
        wp_dropdown_categories(dropdown_options_)
        submit_button(__("Filter"), "", "filter_action", False, Array({"id": "post-query-submit"}))
        php_print("     </div>\n        ")
    # end def extra_tablenav
    #// 
    #// @return array
    #//
    def get_columns(self):
        
        
        return Array({"cb": "<input type=\"checkbox\" />", "name": _x("Name", "link name"), "url": __("URL"), "categories": __("Categories"), "rel": __("Relationship"), "visible": __("Visible"), "rating": __("Rating")})
    # end def get_columns
    #// 
    #// @return array
    #//
    def get_sortable_columns(self):
        
        
        return Array({"name": "name", "url": "url", "visible": "visible", "rating": "rating"})
    # end def get_sortable_columns
    #// 
    #// Get the name of the default primary column.
    #// 
    #// @since 4.3.0
    #// 
    #// @return string Name of the default primary column, in this case, 'name'.
    #//
    def get_default_primary_column_name(self):
        
        
        return "name"
    # end def get_default_primary_column_name
    #// 
    #// Handles the checkbox column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param object $link The current link object.
    #//
    def column_cb(self, link_=None):
        
        
        php_print("     <label class=\"screen-reader-text\" for=\"cb-select-")
        php_print(link_.link_id)
        php_print("\">\n            ")
        #// translators: %s: Link name.
        php_printf(__("Select %s"), link_.link_name)
        php_print("     </label>\n      <input type=\"checkbox\" name=\"linkcheck[]\" id=\"cb-select-")
        php_print(link_.link_id)
        php_print("\" value=\"")
        php_print(esc_attr(link_.link_id))
        php_print("\" />\n      ")
    # end def column_cb
    #// 
    #// Handles the link name column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param object $link The current link object.
    #//
    def column_name(self, link_=None):
        
        
        edit_link_ = get_edit_bookmark_link(link_)
        php_printf("<strong><a class=\"row-title\" href=\"%s\" aria-label=\"%s\">%s</a></strong>", edit_link_, esc_attr(php_sprintf(__("Edit &#8220;%s&#8221;"), link_.link_name)), link_.link_name)
    # end def column_name
    #// 
    #// Handles the link URL column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param object $link The current link object.
    #//
    def column_url(self, link_=None):
        
        
        short_url_ = url_shorten(link_.link_url)
        php_print(str("<a href='") + str(link_.link_url) + str("'>") + str(short_url_) + str("</a>"))
    # end def column_url
    #// 
    #// Handles the link categories column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @global int $cat_id
    #// 
    #// @param object $link The current link object.
    #//
    def column_categories(self, link_=None):
        
        
        global cat_id_
        php_check_if_defined("cat_id_")
        cat_names_ = Array()
        for category_ in link_.link_category:
            cat_ = get_term(category_, "link_category", OBJECT, "display")
            if is_wp_error(cat_):
                php_print(cat_.get_error_message())
            # end if
            cat_name_ = cat_.name
            if php_int(cat_id_) != category_:
                cat_name_ = str("<a href='link-manager.php?cat_id=") + str(category_) + str("'>") + str(cat_name_) + str("</a>")
            # end if
            cat_names_[-1] = cat_name_
        # end for
        php_print(php_implode(", ", cat_names_))
    # end def column_categories
    #// 
    #// Handles the link relation column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param object $link The current link object.
    #//
    def column_rel(self, link_=None):
        
        
        php_print("<br />" if php_empty(lambda : link_.link_rel) else link_.link_rel)
    # end def column_rel
    #// 
    #// Handles the link visibility column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param object $link The current link object.
    #//
    def column_visible(self, link_=None):
        
        
        if "Y" == link_.link_visible:
            _e("Yes")
        else:
            _e("No")
        # end if
    # end def column_visible
    #// 
    #// Handles the link rating column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param object $link The current link object.
    #//
    def column_rating(self, link_=None):
        
        
        php_print(link_.link_rating)
    # end def column_rating
    #// 
    #// Handles the default column output.
    #// 
    #// @since 4.3.0
    #// 
    #// @param object $link        Link object.
    #// @param string $column_name Current column name.
    #//
    def column_default(self, link_=None, column_name_=None):
        
        
        #// 
        #// Fires for each registered custom link column.
        #// 
        #// @since 2.1.0
        #// 
        #// @param string $column_name Name of the custom column.
        #// @param int    $link_id     Link ID.
        #//
        do_action("manage_link_custom_column", column_name_, link_.link_id)
    # end def column_default
    def display_rows(self):
        
        
        for link_ in self.items:
            link_ = sanitize_bookmark(link_)
            link_.link_name = esc_attr(link_.link_name)
            link_.link_category = wp_get_link_cats(link_.link_id)
            php_print("     <tr id=\"link-")
            php_print(link_.link_id)
            php_print("\">\n            ")
            self.single_row_columns(link_)
            php_print("     </tr>\n         ")
        # end for
    # end def display_rows
    #// 
    #// Generates and displays row action links.
    #// 
    #// @since 4.3.0
    #// 
    #// @param object $link        Link being acted upon.
    #// @param string $column_name Current column name.
    #// @param string $primary     Primary column name.
    #// @return string Row actions output for links, or an empty string
    #// if the current column is not the primary column.
    #//
    def handle_row_actions(self, link_=None, column_name_=None, primary_=None):
        
        
        if primary_ != column_name_:
            return ""
        # end if
        edit_link_ = get_edit_bookmark_link(link_)
        actions_ = Array()
        actions_["edit"] = "<a href=\"" + edit_link_ + "\">" + __("Edit") + "</a>"
        actions_["delete"] = php_sprintf("<a class=\"submitdelete\" href=\"%s\" onclick=\"return confirm( '%s' );\">%s</a>", wp_nonce_url(str("link.php?action=delete&amp;link_id=") + str(link_.link_id), "delete-bookmark_" + link_.link_id), esc_js(php_sprintf(__("You are about to delete this link '%s'\n  'Cancel' to stop, 'OK' to delete."), link_.link_name)), __("Delete"))
        return self.row_actions(actions_)
    # end def handle_row_actions
# end class WP_Links_List_Table
