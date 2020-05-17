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
#// WordPress Bookmark Administration API
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// 
#// Add a link to using values provided in $_POST.
#// 
#// @since 2.0.0
#// 
#// @return int|WP_Error Value 0 or WP_Error on failure. The link ID on success.
#//
def add_link(*_args_):
    
    
    return edit_link()
# end def add_link
#// 
#// Updates or inserts a link using values provided in $_POST.
#// 
#// @since 2.0.0
#// 
#// @param int $link_id Optional. ID of the link to edit. Default 0.
#// @return int|WP_Error Value 0 or WP_Error on failure. The link ID on success.
#//
def edit_link(link_id_=0, *_args_):
    
    global PHP_POST
    if (not current_user_can("manage_links")):
        wp_die("<h1>" + __("You need a higher level of permission.") + "</h1>" + "<p>" + __("Sorry, you are not allowed to edit the links for this site.") + "</p>", 403)
    # end if
    PHP_POST["link_url"] = esc_html(PHP_POST["link_url"])
    PHP_POST["link_url"] = esc_url(PHP_POST["link_url"])
    PHP_POST["link_name"] = esc_html(PHP_POST["link_name"])
    PHP_POST["link_image"] = esc_html(PHP_POST["link_image"])
    PHP_POST["link_rss"] = esc_url(PHP_POST["link_rss"])
    if (not (php_isset(lambda : PHP_POST["link_visible"]))) or "N" != PHP_POST["link_visible"]:
        PHP_POST["link_visible"] = "Y"
    # end if
    if (not php_empty(lambda : link_id_)):
        PHP_POST["link_id"] = link_id_
        return wp_update_link(PHP_POST)
    else:
        return wp_insert_link(PHP_POST)
    # end if
# end def edit_link
#// 
#// Retrieves the default link for editing.
#// 
#// @since 2.0.0
#// 
#// @return stdClass Default link object.
#//
def get_default_link_to_edit(*_args_):
    
    
    link_ = php_new_class("stdClass", lambda : stdClass())
    if (php_isset(lambda : PHP_REQUEST["linkurl"])):
        link_.link_url = esc_url(wp_unslash(PHP_REQUEST["linkurl"]))
    else:
        link_.link_url = ""
    # end if
    if (php_isset(lambda : PHP_REQUEST["name"])):
        link_.link_name = esc_attr(wp_unslash(PHP_REQUEST["name"]))
    else:
        link_.link_name = ""
    # end if
    link_.link_visible = "Y"
    return link_
# end def get_default_link_to_edit
#// 
#// Deletes a specified link from the database.
#// 
#// @since 2.0.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int $link_id ID of the link to delete
#// @return true Always true.
#//
def wp_delete_link(link_id_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    #// 
    #// Fires before a link is deleted.
    #// 
    #// @since 2.0.0
    #// 
    #// @param int $link_id ID of the link to delete.
    #//
    do_action("delete_link", link_id_)
    wp_delete_object_term_relationships(link_id_, "link_category")
    wpdb_.delete(wpdb_.links, Array({"link_id": link_id_}))
    #// 
    #// Fires after a link has been deleted.
    #// 
    #// @since 2.2.0
    #// 
    #// @param int $link_id ID of the deleted link.
    #//
    do_action("deleted_link", link_id_)
    clean_bookmark_cache(link_id_)
    return True
# end def wp_delete_link
#// 
#// Retrieves the link category IDs associated with the link specified.
#// 
#// @since 2.1.0
#// 
#// @param int $link_id Link ID to look up.
#// @return int[] The IDs of the requested link's categories.
#//
def wp_get_link_cats(link_id_=0, *_args_):
    
    
    cats_ = wp_get_object_terms(link_id_, "link_category", Array({"fields": "ids"}))
    return array_unique(cats_)
# end def wp_get_link_cats
#// 
#// Retrieves link data based on its ID.
#// 
#// @since 2.0.0
#// 
#// @param int|stdClass $link Link ID or object to retrieve.
#// @return object Link object for editing.
#//
def get_link_to_edit(link_=None, *_args_):
    
    
    return get_bookmark(link_, OBJECT, "edit")
# end def get_link_to_edit
#// 
#// Inserts/updates links into/in the database.
#// 
#// @since 2.0.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param array $linkdata Elements that make up the link to insert.
#// @param bool  $wp_error Optional. Whether to return a WP_Error object on failure. Default false.
#// @return int|WP_Error Value 0 or WP_Error on failure. The link ID on success.
#//
def wp_insert_link(linkdata_=None, wp_error_=None, *_args_):
    if wp_error_ is None:
        wp_error_ = False
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    defaults_ = Array({"link_id": 0, "link_name": "", "link_url": "", "link_rating": 0})
    parsed_args_ = wp_parse_args(linkdata_, defaults_)
    parsed_args_ = wp_unslash(sanitize_bookmark(parsed_args_, "db"))
    link_id_ = parsed_args_["link_id"]
    link_name_ = parsed_args_["link_name"]
    link_url_ = parsed_args_["link_url"]
    update_ = False
    if (not php_empty(lambda : link_id_)):
        update_ = True
    # end if
    if php_trim(link_name_) == "":
        if php_trim(link_url_) != "":
            link_name_ = link_url_
        else:
            return 0
        # end if
    # end if
    if php_trim(link_url_) == "":
        return 0
    # end if
    link_rating_ = parsed_args_["link_rating"] if (not php_empty(lambda : parsed_args_["link_rating"])) else 0
    link_image_ = parsed_args_["link_image"] if (not php_empty(lambda : parsed_args_["link_image"])) else ""
    link_target_ = parsed_args_["link_target"] if (not php_empty(lambda : parsed_args_["link_target"])) else ""
    link_visible_ = parsed_args_["link_visible"] if (not php_empty(lambda : parsed_args_["link_visible"])) else "Y"
    link_owner_ = parsed_args_["link_owner"] if (not php_empty(lambda : parsed_args_["link_owner"])) else get_current_user_id()
    link_notes_ = parsed_args_["link_notes"] if (not php_empty(lambda : parsed_args_["link_notes"])) else ""
    link_description_ = parsed_args_["link_description"] if (not php_empty(lambda : parsed_args_["link_description"])) else ""
    link_rss_ = parsed_args_["link_rss"] if (not php_empty(lambda : parsed_args_["link_rss"])) else ""
    link_rel_ = parsed_args_["link_rel"] if (not php_empty(lambda : parsed_args_["link_rel"])) else ""
    link_category_ = parsed_args_["link_category"] if (not php_empty(lambda : parsed_args_["link_category"])) else Array()
    #// Make sure we set a valid category.
    if (not php_is_array(link_category_)) or 0 == php_count(link_category_):
        link_category_ = Array(get_option("default_link_category"))
    # end if
    if update_:
        if False == wpdb_.update(wpdb_.links, php_compact("link_url", "link_name", "link_image", "link_target", "link_description", "link_visible", "link_owner", "link_rating", "link_rel", "link_notes", "link_rss"), php_compact("link_id")):
            if wp_error_:
                return php_new_class("WP_Error", lambda : WP_Error("db_update_error", __("Could not update link in the database"), wpdb_.last_error))
            else:
                return 0
            # end if
        # end if
    else:
        if False == wpdb_.insert(wpdb_.links, php_compact("link_url", "link_name", "link_image", "link_target", "link_description", "link_visible", "link_owner", "link_rating", "link_rel", "link_notes", "link_rss")):
            if wp_error_:
                return php_new_class("WP_Error", lambda : WP_Error("db_insert_error", __("Could not insert link into the database"), wpdb_.last_error))
            else:
                return 0
            # end if
        # end if
        link_id_ = php_int(wpdb_.insert_id)
    # end if
    wp_set_link_cats(link_id_, link_category_)
    if update_:
        #// 
        #// Fires after a link was updated in the database.
        #// 
        #// @since 2.0.0
        #// 
        #// @param int $link_id ID of the link that was updated.
        #//
        do_action("edit_link", link_id_)
    else:
        #// 
        #// Fires after a link was added to the database.
        #// 
        #// @since 2.0.0
        #// 
        #// @param int $link_id ID of the link that was added.
        #//
        do_action("add_link", link_id_)
    # end if
    clean_bookmark_cache(link_id_)
    return link_id_
# end def wp_insert_link
#// 
#// Update link with the specified link categories.
#// 
#// @since 2.1.0
#// 
#// @param int   $link_id         ID of the link to update.
#// @param int[] $link_categories Array of link category IDs to add the link to.
#//
def wp_set_link_cats(link_id_=0, link_categories_=None, *_args_):
    if link_categories_ is None:
        link_categories_ = Array()
    # end if
    
    #// If $link_categories isn't already an array, make it one:
    if (not php_is_array(link_categories_)) or 0 == php_count(link_categories_):
        link_categories_ = Array(get_option("default_link_category"))
    # end if
    link_categories_ = php_array_map("intval", link_categories_)
    link_categories_ = array_unique(link_categories_)
    wp_set_object_terms(link_id_, link_categories_, "link_category")
    clean_bookmark_cache(link_id_)
# end def wp_set_link_cats
#// 
#// Updates a link in the database.
#// 
#// @since 2.0.0
#// 
#// @param array $linkdata Link data to update.
#// @return int|WP_Error Value 0 or WP_Error on failure. The updated link ID on success.
#//
def wp_update_link(linkdata_=None, *_args_):
    
    
    link_id_ = php_int(linkdata_["link_id"])
    link_ = get_bookmark(link_id_, ARRAY_A)
    #// Escape data pulled from DB.
    link_ = wp_slash(link_)
    #// Passed link category list overwrites existing category list if not empty.
    if (php_isset(lambda : linkdata_["link_category"])) and php_is_array(linkdata_["link_category"]) and 0 != php_count(linkdata_["link_category"]):
        link_cats_ = linkdata_["link_category"]
    else:
        link_cats_ = link_["link_category"]
    # end if
    #// Merge old and new fields with new fields overwriting old ones.
    linkdata_ = php_array_merge(link_, linkdata_)
    linkdata_["link_category"] = link_cats_
    return wp_insert_link(linkdata_)
# end def wp_update_link
#// 
#// Outputs the 'disabled' message for the WordPress Link Manager.
#// 
#// @since 3.5.0
#// @access private
#// 
#// @global string $pagenow
#//
def wp_link_manager_disabled_message(*_args_):
    
    
    global pagenow_
    php_check_if_defined("pagenow_")
    if "link-manager.php" != pagenow_ and "link-add.php" != pagenow_ and "link.php" != pagenow_:
        return
    # end if
    add_filter("pre_option_link_manager_enabled", "__return_true", 100)
    really_can_manage_links_ = current_user_can("manage_links")
    remove_filter("pre_option_link_manager_enabled", "__return_true", 100)
    if really_can_manage_links_ and current_user_can("install_plugins"):
        link_ = network_admin_url("plugin-install.php?tab=search&amp;s=Link+Manager")
        #// translators: %s: URL to install the Link Manager plugin.
        wp_die(php_sprintf(__("If you are looking to use the link manager, please install the <a href=\"%s\">Link Manager</a> plugin."), link_))
    # end if
    wp_die(__("Sorry, you are not allowed to edit the links for this site."))
# end def wp_link_manager_disabled_message
