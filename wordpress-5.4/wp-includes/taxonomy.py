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
#// Core Taxonomy API
#// 
#// @package WordPress
#// @subpackage Taxonomy
#// 
#// 
#// Taxonomy registration.
#// 
#// 
#// Creates the initial taxonomies.
#// 
#// This function fires twice: in wp-settings.php before plugins are loaded (for
#// backward compatibility reasons), and again on the {@see 'init'} action. We must
#// avoid registering rewrite rules before the {@see 'init'} action.
#// 
#// @since 2.8.0
#// 
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#//
def create_initial_taxonomies(*args_):
    
    global wp_rewrite
    php_check_if_defined("wp_rewrite")
    if (not did_action("init")):
        rewrite = Array({"category": False, "post_tag": False, "post_format": False})
    else:
        #// 
        #// Filters the post formats rewrite base.
        #// 
        #// @since 3.1.0
        #// 
        #// @param string $context Context of the rewrite base. Default 'type'.
        #//
        post_format_base = apply_filters("post_format_rewrite_base", "type")
        rewrite = Array({"category": Array({"hierarchical": True, "slug": get_option("category_base") if get_option("category_base") else "category", "with_front": (not get_option("category_base")) or wp_rewrite.using_index_permalinks(), "ep_mask": EP_CATEGORIES})}, {"post_tag": Array({"hierarchical": False, "slug": get_option("tag_base") if get_option("tag_base") else "tag", "with_front": (not get_option("tag_base")) or wp_rewrite.using_index_permalinks(), "ep_mask": EP_TAGS})}, {"post_format": Array({"slug": post_format_base}) if post_format_base else False})
    # end if
    register_taxonomy("category", "post", Array({"hierarchical": True, "query_var": "category_name", "rewrite": rewrite["category"], "public": True, "show_ui": True, "show_admin_column": True, "_builtin": True, "capabilities": Array({"manage_terms": "manage_categories", "edit_terms": "edit_categories", "delete_terms": "delete_categories", "assign_terms": "assign_categories"})}, {"show_in_rest": True, "rest_base": "categories", "rest_controller_class": "WP_REST_Terms_Controller"}))
    register_taxonomy("post_tag", "post", Array({"hierarchical": False, "query_var": "tag", "rewrite": rewrite["post_tag"], "public": True, "show_ui": True, "show_admin_column": True, "_builtin": True, "capabilities": Array({"manage_terms": "manage_post_tags", "edit_terms": "edit_post_tags", "delete_terms": "delete_post_tags", "assign_terms": "assign_post_tags"})}, {"show_in_rest": True, "rest_base": "tags", "rest_controller_class": "WP_REST_Terms_Controller"}))
    register_taxonomy("nav_menu", "nav_menu_item", Array({"public": False, "hierarchical": False, "labels": Array({"name": __("Navigation Menus"), "singular_name": __("Navigation Menu")})}, {"query_var": False, "rewrite": False, "show_ui": False, "_builtin": True, "show_in_nav_menus": False}))
    register_taxonomy("link_category", "link", Array({"hierarchical": False, "labels": Array({"name": __("Link Categories"), "singular_name": __("Link Category"), "search_items": __("Search Link Categories"), "popular_items": None, "all_items": __("All Link Categories"), "edit_item": __("Edit Link Category"), "update_item": __("Update Link Category"), "add_new_item": __("Add New Link Category"), "new_item_name": __("New Link Category Name"), "separate_items_with_commas": None, "add_or_remove_items": None, "choose_from_most_used": None, "back_to_items": __("&larr; Back to Link Categories")})}, {"capabilities": Array({"manage_terms": "manage_links", "edit_terms": "manage_links", "delete_terms": "manage_links", "assign_terms": "manage_links"})}, {"query_var": False, "rewrite": False, "public": False, "show_ui": True, "_builtin": True}))
    register_taxonomy("post_format", "post", Array({"public": True, "hierarchical": False, "labels": Array({"name": _x("Formats", "post format"), "singular_name": _x("Format", "post format")})}, {"query_var": True, "rewrite": rewrite["post_format"], "show_ui": False, "_builtin": True, "show_in_nav_menus": current_theme_supports("post-formats")}))
# end def create_initial_taxonomies
#// 
#// Retrieves a list of registered taxonomy names or objects.
#// 
#// @since 3.0.0
#// 
#// @global array $wp_taxonomies The registered taxonomies.
#// 
#// @param array  $args     Optional. An array of `key => value` arguments to match against the taxonomy objects.
#// Default empty array.
#// @param string $output   Optional. The type of output to return in the array. Accepts either taxonomy 'names'
#// or 'objects'. Default 'names'.
#// @param string $operator Optional. The logical operation to perform. Accepts 'and' or 'or'. 'or' means only
#// one element from the array needs to match; 'and' means all elements must match.
#// Default 'and'.
#// @return string[]|WP_Taxonomy[] An array of taxonomy names or objects.
#//
def get_taxonomies(args=Array(), output="names", operator="and", *args_):
    
    global wp_taxonomies
    php_check_if_defined("wp_taxonomies")
    field = "name" if "names" == output else False
    return wp_filter_object_list(wp_taxonomies, args, operator, field)
# end def get_taxonomies
#// 
#// Return the names or objects of the taxonomies which are registered for the requested object or object type, such as
#// a post object or post type name.
#// 
#// Example:
#// 
#// $taxonomies = get_object_taxonomies( 'post' );
#// 
#// This results in:
#// 
#// Array( 'category', 'post_tag' )
#// 
#// @since 2.3.0
#// 
#// @global array $wp_taxonomies The registered taxonomies.
#// 
#// @param string|string[]|WP_Post $object Name of the type of taxonomy object, or an object (row from posts)
#// @param string                  $output Optional. The type of output to return in the array. Accepts either
#// 'names' or 'objects'. Default 'names'.
#// @return string[]|WP_Taxonomy[] The names or objects of all taxonomies of `$object_type`.
#//
def get_object_taxonomies(object=None, output="names", *args_):
    
    global wp_taxonomies
    php_check_if_defined("wp_taxonomies")
    if php_is_object(object):
        if "attachment" == object.post_type:
            return get_attachment_taxonomies(object, output)
        # end if
        object = object.post_type
    # end if
    object = object
    taxonomies = Array()
    for tax_name,tax_obj in wp_taxonomies:
        if php_array_intersect(object, tax_obj.object_type):
            if "names" == output:
                taxonomies[-1] = tax_name
            else:
                taxonomies[tax_name] = tax_obj
            # end if
        # end if
    # end for
    return taxonomies
# end def get_object_taxonomies
#// 
#// Retrieves the taxonomy object of $taxonomy.
#// 
#// The get_taxonomy function will first check that the parameter string given
#// is a taxonomy object and if it is, it will return it.
#// 
#// @since 2.3.0
#// 
#// @global array $wp_taxonomies The registered taxonomies.
#// 
#// @param string $taxonomy Name of taxonomy object to return.
#// @return WP_Taxonomy|false The Taxonomy Object or false if $taxonomy doesn't exist.
#//
def get_taxonomy(taxonomy=None, *args_):
    
    global wp_taxonomies
    php_check_if_defined("wp_taxonomies")
    if (not taxonomy_exists(taxonomy)):
        return False
    # end if
    return wp_taxonomies[taxonomy]
# end def get_taxonomy
#// 
#// Determines whether the taxonomy name exists.
#// 
#// Formerly is_taxonomy(), introduced in 2.3.0.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 3.0.0
#// 
#// @global array $wp_taxonomies The registered taxonomies.
#// 
#// @param string $taxonomy Name of taxonomy object.
#// @return bool Whether the taxonomy exists.
#//
def taxonomy_exists(taxonomy=None, *args_):
    
    global wp_taxonomies
    php_check_if_defined("wp_taxonomies")
    return (php_isset(lambda : wp_taxonomies[taxonomy]))
# end def taxonomy_exists
#// 
#// Determines whether the taxonomy object is hierarchical.
#// 
#// Checks to make sure that the taxonomy is an object first. Then Gets the
#// object, and finally returns the hierarchical value in the object.
#// 
#// A false return value might also mean that the taxonomy does not exist.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 2.3.0
#// 
#// @param string $taxonomy Name of taxonomy object.
#// @return bool Whether the taxonomy is hierarchical.
#//
def is_taxonomy_hierarchical(taxonomy=None, *args_):
    
    if (not taxonomy_exists(taxonomy)):
        return False
    # end if
    taxonomy = get_taxonomy(taxonomy)
    return taxonomy.hierarchical
# end def is_taxonomy_hierarchical
#// 
#// Creates or modifies a taxonomy object.
#// 
#// Note: Do not use before the {@see 'init'} hook.
#// 
#// A simple function for creating or modifying a taxonomy object based on
#// the parameters given. If modifying an existing taxonomy object, note
#// that the `$object_type` value from the original registration will be
#// overwritten.
#// 
#// @since 2.3.0
#// @since 4.2.0 Introduced `show_in_quick_edit` argument.
#// @since 4.4.0 The `show_ui` argument is now enforced on the term editing screen.
#// @since 4.4.0 The `public` argument now controls whether the taxonomy can be queried on the front end.
#// @since 4.5.0 Introduced `publicly_queryable` argument.
#// @since 4.7.0 Introduced `show_in_rest`, 'rest_base' and 'rest_controller_class'
#// arguments to register the Taxonomy in REST API.
#// @since 5.1.0 Introduced `meta_box_sanitize_cb` argument.
#// @since 5.4.0 Added the registered taxonomy object as a return value.
#// 
#// @global array $wp_taxonomies Registered taxonomies.
#// 
#// @param string       $taxonomy    Taxonomy key, must not exceed 32 characters.
#// @param array|string $object_type Object type or array of object types with which the taxonomy should be associated.
#// @param array|string $args        {
#// Optional. Array or query string of arguments for registering a taxonomy.
#// 
#// @type array         $labels                An array of labels for this taxonomy. By default, Tag labels are
#// used for non-hierarchical taxonomies, and Category labels are used
#// for hierarchical taxonomies. See accepted values in
#// get_taxonomy_labels(). Default empty array.
#// @type string        $description           A short descriptive summary of what the taxonomy is for. Default empty.
#// @type bool          $public                Whether a taxonomy is intended for use publicly either via
#// the admin interface or by front-end users. The default settings
#// of `$publicly_queryable`, `$show_ui`, and `$show_in_nav_menus`
#// are inherited from `$public`.
#// @type bool          $publicly_queryable    Whether the taxonomy is publicly queryable.
#// If not set, the default is inherited from `$public`
#// @type bool          $hierarchical          Whether the taxonomy is hierarchical. Default false.
#// @type bool          $show_ui               Whether to generate and allow a UI for managing terms in this taxonomy in
#// the admin. If not set, the default is inherited from `$public`
#// (default true).
#// @type bool          $show_in_menu          Whether to show the taxonomy in the admin menu. If true, the taxonomy is
#// shown as a submenu of the object type menu. If false, no menu is shown.
#// `$show_ui` must be true. If not set, default is inherited from `$show_ui`
#// (default true).
#// @type bool          $show_in_nav_menus     Makes this taxonomy available for selection in navigation menus. If not
#// set, the default is inherited from `$public` (default true).
#// @type bool          $show_in_rest          Whether to include the taxonomy in the REST API. Set this to true
#// for the taxonomy to be available in the block editor.
#// @type string        $rest_base             To change the base url of REST API route. Default is $taxonomy.
#// @type string        $rest_controller_class REST API Controller class name. Default is 'WP_REST_Terms_Controller'.
#// @type bool          $show_tagcloud         Whether to list the taxonomy in the Tag Cloud Widget controls. If not set,
#// the default is inherited from `$show_ui` (default true).
#// @type bool          $show_in_quick_edit    Whether to show the taxonomy in the quick/bulk edit panel. It not set,
#// the default is inherited from `$show_ui` (default true).
#// @type bool          $show_admin_column     Whether to display a column for the taxonomy on its post type listing
#// screens. Default false.
#// @type bool|callable $meta_box_cb           Provide a callback function for the meta box display. If not set,
#// post_categories_meta_box() is used for hierarchical taxonomies, and
#// post_tags_meta_box() is used for non-hierarchical. If false, no meta
#// box is shown.
#// @type callable      $meta_box_sanitize_cb  Callback function for sanitizing taxonomy data saved from a meta
#// box. If no callback is defined, an appropriate one is determined
#// based on the value of `$meta_box_cb`.
#// @type array         $capabilities {
#// Array of capabilities for this taxonomy.
#// 
#// @type string $manage_terms Default 'manage_categories'.
#// @type string $edit_terms   Default 'manage_categories'.
#// @type string $delete_terms Default 'manage_categories'.
#// @type string $assign_terms Default 'edit_posts'.
#// }
#// @type bool|array    $rewrite {
#// Triggers the handling of rewrites for this taxonomy. Default true, using $taxonomy as slug. To prevent
#// rewrite, set to false. To specify rewrite rules, an array can be passed with any of these keys:
#// 
#// @type string $slug         Customize the permastruct slug. Default `$taxonomy` key.
#// @type bool   $with_front   Should the permastruct be prepended with WP_Rewrite::$front. Default true.
#// @type bool   $hierarchical Either hierarchical rewrite tag or not. Default false.
#// @type int    $ep_mask      Assign an endpoint mask. Default `EP_NONE`.
#// }
#// @type string|bool   $query_var             Sets the query var key for this taxonomy. Default `$taxonomy` key. If
#// false, a taxonomy cannot be loaded at `?{query_var}={term_slug}`. If a
#// string, the query `?{query_var}={term_slug}` will be valid.
#// @type callable      $update_count_callback Works much like a hook, in that it will be called when the count is
#// updated. Default _update_post_term_count() for taxonomies attached
#// to post types, which confirms that the objects are published before
#// counting them. Default _update_generic_term_count() for taxonomies
#// attached to other object types, such as users.
#// @type bool          $_builtin              This taxonomy is a "built-in" taxonomy. INTERNAL USE ONLY!
#// Default false.
#// }
#// @return WP_Taxonomy|WP_Error The registered taxonomy object on success, WP_Error object on failure.
#//
def register_taxonomy(taxonomy=None, object_type=None, args=Array(), *args_):
    
    global wp_taxonomies
    php_check_if_defined("wp_taxonomies")
    if (not php_is_array(wp_taxonomies)):
        wp_taxonomies = Array()
    # end if
    args = wp_parse_args(args)
    if php_empty(lambda : taxonomy) or php_strlen(taxonomy) > 32:
        _doing_it_wrong(__FUNCTION__, __("Taxonomy names must be between 1 and 32 characters in length."), "4.2.0")
        return php_new_class("WP_Error", lambda : WP_Error("taxonomy_length_invalid", __("Taxonomy names must be between 1 and 32 characters in length.")))
    # end if
    taxonomy_object = php_new_class("WP_Taxonomy", lambda : WP_Taxonomy(taxonomy, object_type, args))
    taxonomy_object.add_rewrite_rules()
    wp_taxonomies[taxonomy] = taxonomy_object
    taxonomy_object.add_hooks()
    #// 
    #// Fires after a taxonomy is registered.
    #// 
    #// @since 3.3.0
    #// 
    #// @param string       $taxonomy    Taxonomy slug.
    #// @param array|string $object_type Object type or array of object types.
    #// @param array        $args        Array of taxonomy registration arguments.
    #//
    do_action("registered_taxonomy", taxonomy, object_type, taxonomy_object)
    return taxonomy_object
# end def register_taxonomy
#// 
#// Unregisters a taxonomy.
#// 
#// Can not be used to unregister built-in taxonomies.
#// 
#// @since 4.5.0
#// 
#// @global WP    $wp            Current WordPress environment instance.
#// @global array $wp_taxonomies List of taxonomies.
#// 
#// @param string $taxonomy Taxonomy name.
#// @return bool|WP_Error True on success, WP_Error on failure or if the taxonomy doesn't exist.
#//
def unregister_taxonomy(taxonomy=None, *args_):
    
    if (not taxonomy_exists(taxonomy)):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_taxonomy", __("Invalid taxonomy.")))
    # end if
    taxonomy_object = get_taxonomy(taxonomy)
    #// Do not allow unregistering internal taxonomies.
    if taxonomy_object._builtin:
        return php_new_class("WP_Error", lambda : WP_Error("invalid_taxonomy", __("Unregistering a built-in taxonomy is not allowed.")))
    # end if
    global wp_taxonomies
    php_check_if_defined("wp_taxonomies")
    taxonomy_object.remove_rewrite_rules()
    taxonomy_object.remove_hooks()
    wp_taxonomies[taxonomy] = None
    #// 
    #// Fires after a taxonomy is unregistered.
    #// 
    #// @since 4.5.0
    #// 
    #// @param string $taxonomy Taxonomy name.
    #//
    do_action("unregistered_taxonomy", taxonomy)
    return True
# end def unregister_taxonomy
#// 
#// Builds an object with all taxonomy labels out of a taxonomy object.
#// 
#// @since 3.0.0
#// @since 4.3.0 Added the `no_terms` label.
#// @since 4.4.0 Added the `items_list_navigation` and `items_list` labels.
#// @since 4.9.0 Added the `most_used` and `back_to_items` labels.
#// 
#// @param WP_Taxonomy $tax Taxonomy object.
#// @return object {
#// Taxonomy labels object. The first default value is for non-hierarchical taxonomies
#// (like tags) and the second one is for hierarchical taxonomies (like categories).
#// 
#// @type string $name                       General name for the taxonomy, usually plural. The same
#// as and overridden by `$tax->label`. Default 'Tags'/'Categories'.
#// @type string $singular_name              Name for one object of this taxonomy. Default 'Tag'/'Category'.
#// @type string $search_items               Default 'Search Tags'/'Search Categories'.
#// @type string $popular_items              This label is only used for non-hierarchical taxonomies.
#// Default 'Popular Tags'.
#// @type string $all_items                  Default 'All Tags'/'All Categories'.
#// @type string $parent_item                This label is only used for hierarchical taxonomies. Default
#// 'Parent Category'.
#// @type string $parent_item_colon          The same as `parent_item`, but with colon `:` in the end.
#// @type string $edit_item                  Default 'Edit Tag'/'Edit Category'.
#// @type string $view_item                  Default 'View Tag'/'View Category'.
#// @type string $update_item                Default 'Update Tag'/'Update Category'.
#// @type string $add_new_item               Default 'Add New Tag'/'Add New Category'.
#// @type string $new_item_name              Default 'New Tag Name'/'New Category Name'.
#// @type string $separate_items_with_commas This label is only used for non-hierarchical taxonomies. Default
#// 'Separate tags with commas', used in the meta box.
#// @type string $add_or_remove_items        This label is only used for non-hierarchical taxonomies. Default
#// 'Add or remove tags', used in the meta box when JavaScript
#// is disabled.
#// @type string $choose_from_most_used      This label is only used on non-hierarchical taxonomies. Default
#// 'Choose from the most used tags', used in the meta box.
#// @type string $not_found                  Default 'No tags found'/'No categories found', used in
#// the meta box and taxonomy list table.
#// @type string $no_terms                   Default 'No tags'/'No categories', used in the posts and media
#// list tables.
#// @type string $items_list_navigation      Label for the table pagination hidden heading.
#// @type string $items_list                 Label for the table hidden heading.
#// @type string $most_used                  Title for the Most Used tab. Default 'Most Used'.
#// @type string $back_to_items              Label displayed after a term has been updated.
#// }
#//
def get_taxonomy_labels(tax=None, *args_):
    
    tax.labels = tax.labels
    if (php_isset(lambda : tax.helps)) and php_empty(lambda : tax.labels["separate_items_with_commas"]):
        tax.labels["separate_items_with_commas"] = tax.helps
    # end if
    if (php_isset(lambda : tax.no_tagcloud)) and php_empty(lambda : tax.labels["not_found"]):
        tax.labels["not_found"] = tax.no_tagcloud
    # end if
    nohier_vs_hier_defaults = Array({"name": Array(_x("Tags", "taxonomy general name"), _x("Categories", "taxonomy general name")), "singular_name": Array(_x("Tag", "taxonomy singular name"), _x("Category", "taxonomy singular name")), "search_items": Array(__("Search Tags"), __("Search Categories")), "popular_items": Array(__("Popular Tags"), None), "all_items": Array(__("All Tags"), __("All Categories")), "parent_item": Array(None, __("Parent Category")), "parent_item_colon": Array(None, __("Parent Category:")), "edit_item": Array(__("Edit Tag"), __("Edit Category")), "view_item": Array(__("View Tag"), __("View Category")), "update_item": Array(__("Update Tag"), __("Update Category")), "add_new_item": Array(__("Add New Tag"), __("Add New Category")), "new_item_name": Array(__("New Tag Name"), __("New Category Name")), "separate_items_with_commas": Array(__("Separate tags with commas"), None), "add_or_remove_items": Array(__("Add or remove tags"), None), "choose_from_most_used": Array(__("Choose from the most used tags"), None), "not_found": Array(__("No tags found."), __("No categories found.")), "no_terms": Array(__("No tags"), __("No categories")), "items_list_navigation": Array(__("Tags list navigation"), __("Categories list navigation")), "items_list": Array(__("Tags list"), __("Categories list")), "most_used": Array(_x("Most Used", "tags"), _x("Most Used", "categories")), "back_to_items": Array(__("&larr; Back to Tags"), __("&larr; Back to Categories"))})
    nohier_vs_hier_defaults["menu_name"] = nohier_vs_hier_defaults["name"]
    labels = _get_custom_object_labels(tax, nohier_vs_hier_defaults)
    taxonomy = tax.name
    default_labels = copy.deepcopy(labels)
    #// 
    #// Filters the labels of a specific taxonomy.
    #// 
    #// The dynamic portion of the hook name, `$taxonomy`, refers to the taxonomy slug.
    #// 
    #// @since 4.4.0
    #// 
    #// @see get_taxonomy_labels() for the full list of taxonomy labels.
    #// 
    #// @param object $labels Object with labels for the taxonomy as member variables.
    #//
    labels = apply_filters(str("taxonomy_labels_") + str(taxonomy), labels)
    #// Ensure that the filtered labels contain all required default values.
    labels = php_array_merge(default_labels, labels)
    return labels
# end def get_taxonomy_labels
#// 
#// Add an already registered taxonomy to an object type.
#// 
#// @since 3.0.0
#// 
#// @global array $wp_taxonomies The registered taxonomies.
#// 
#// @param string $taxonomy    Name of taxonomy object.
#// @param string $object_type Name of the object type.
#// @return bool True if successful, false if not.
#//
def register_taxonomy_for_object_type(taxonomy=None, object_type=None, *args_):
    
    global wp_taxonomies
    php_check_if_defined("wp_taxonomies")
    if (not (php_isset(lambda : wp_taxonomies[taxonomy]))):
        return False
    # end if
    if (not get_post_type_object(object_type)):
        return False
    # end if
    if (not php_in_array(object_type, wp_taxonomies[taxonomy].object_type)):
        wp_taxonomies[taxonomy].object_type[-1] = object_type
    # end if
    #// Filter out empties.
    wp_taxonomies[taxonomy].object_type = php_array_filter(wp_taxonomies[taxonomy].object_type)
    #// 
    #// Fires after a taxonomy is registered for an object type.
    #// 
    #// @since 5.1.0
    #// 
    #// @param string $taxonomy    Taxonomy name.
    #// @param string $object_type Name of the object type.
    #//
    do_action("registered_taxonomy_for_object_type", taxonomy, object_type)
    return True
# end def register_taxonomy_for_object_type
#// 
#// Remove an already registered taxonomy from an object type.
#// 
#// @since 3.7.0
#// 
#// @global array $wp_taxonomies The registered taxonomies.
#// 
#// @param string $taxonomy    Name of taxonomy object.
#// @param string $object_type Name of the object type.
#// @return bool True if successful, false if not.
#//
def unregister_taxonomy_for_object_type(taxonomy=None, object_type=None, *args_):
    
    global wp_taxonomies
    php_check_if_defined("wp_taxonomies")
    if (not (php_isset(lambda : wp_taxonomies[taxonomy]))):
        return False
    # end if
    if (not get_post_type_object(object_type)):
        return False
    # end if
    key = php_array_search(object_type, wp_taxonomies[taxonomy].object_type, True)
    if False == key:
        return False
    # end if
    wp_taxonomies[taxonomy].object_type[key] = None
    #// 
    #// Fires after a taxonomy is unregistered for an object type.
    #// 
    #// @since 5.1.0
    #// 
    #// @param string $taxonomy    Taxonomy name.
    #// @param string $object_type Name of the object type.
    #//
    do_action("unregistered_taxonomy_for_object_type", taxonomy, object_type)
    return True
# end def unregister_taxonomy_for_object_type
#// 
#// Term API.
#// 
#// 
#// Retrieve object_ids of valid taxonomy and term.
#// 
#// The strings of $taxonomies must exist before this function will continue. On
#// failure of finding a valid taxonomy, it will return an WP_Error class, kind
#// of like Exceptions in PHP 5, except you can't catch them. Even so, you can
#// still test for the WP_Error class and get the error message.
#// 
#// The $terms aren't checked the same as $taxonomies, but still need to exist
#// for $object_ids to be returned.
#// 
#// It is possible to change the order that object_ids is returned by either
#// using PHP sort family functions or using the database by using $args with
#// either ASC or DESC array. The value should be in the key named 'order'.
#// 
#// @since 2.3.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int|array    $term_ids   Term id or array of term ids of terms that will be used.
#// @param string|array $taxonomies String of taxonomy name or Array of string values of taxonomy names.
#// @param array|string $args       Change the order of the object_ids, either ASC or DESC.
#// @return WP_Error|array If the taxonomy does not exist, then WP_Error will be returned. On success.
#// the array can be empty meaning that there are no $object_ids found or it will return the $object_ids found.
#//
def get_objects_in_term(term_ids=None, taxonomies=None, args=Array(), *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if (not php_is_array(term_ids)):
        term_ids = Array(term_ids)
    # end if
    if (not php_is_array(taxonomies)):
        taxonomies = Array(taxonomies)
    # end if
    for taxonomy in taxonomies:
        if (not taxonomy_exists(taxonomy)):
            return php_new_class("WP_Error", lambda : WP_Error("invalid_taxonomy", __("Invalid taxonomy.")))
        # end if
    # end for
    defaults = Array({"order": "ASC"})
    args = wp_parse_args(args, defaults)
    order = "DESC" if "desc" == php_strtolower(args["order"]) else "ASC"
    term_ids = php_array_map("intval", term_ids)
    taxonomies = "'" + php_implode("', '", php_array_map("esc_sql", taxonomies)) + "'"
    term_ids = "'" + php_implode("', '", term_ids) + "'"
    sql = str("SELECT tr.object_id FROM ") + str(wpdb.term_relationships) + str(" AS tr INNER JOIN ") + str(wpdb.term_taxonomy) + str(" AS tt ON tr.term_taxonomy_id = tt.term_taxonomy_id WHERE tt.taxonomy IN (") + str(taxonomies) + str(") AND tt.term_id IN (") + str(term_ids) + str(") ORDER BY tr.object_id ") + str(order)
    last_changed = wp_cache_get_last_changed("terms")
    cache_key = "get_objects_in_term:" + php_md5(sql) + str(":") + str(last_changed)
    cache = wp_cache_get(cache_key, "terms")
    if False == cache:
        object_ids = wpdb.get_col(sql)
        wp_cache_set(cache_key, object_ids, "terms")
    else:
        object_ids = cache
    # end if
    if (not object_ids):
        return Array()
    # end if
    return object_ids
# end def get_objects_in_term
#// 
#// Given a taxonomy query, generates SQL to be appended to a main query.
#// 
#// @since 3.1.0
#// 
#// @see WP_Tax_Query
#// 
#// @param array  $tax_query         A compact tax query
#// @param string $primary_table
#// @param string $primary_id_column
#// @return array
#//
def get_tax_sql(tax_query=None, primary_table=None, primary_id_column=None, *args_):
    
    tax_query_obj = php_new_class("WP_Tax_Query", lambda : WP_Tax_Query(tax_query))
    return tax_query_obj.get_sql(primary_table, primary_id_column)
# end def get_tax_sql
#// 
#// Get all Term data from database by Term ID.
#// 
#// The usage of the get_term function is to apply filters to a term object. It
#// is possible to get a term object from the database before applying the
#// filters.
#// 
#// $term ID must be part of $taxonomy, to get from the database. Failure, might
#// be able to be captured by the hooks. Failure would be the same value as $wpdb
#// returns for the get_row method.
#// 
#// There are two hooks, one is specifically for each term, named 'get_term', and
#// the second is for the taxonomy name, 'term_$taxonomy'. Both hooks gets the
#// term object, and the taxonomy name as parameters. Both hooks are expected to
#// return a Term object.
#// 
#// {@see 'get_term'} hook - Takes two parameters the term Object and the taxonomy name.
#// Must return term object. Used in get_term() as a catch-all filter for every
#// $term.
#// 
#// {@see 'get_$taxonomy'} hook - Takes two parameters the term Object and the taxonomy
#// name. Must return term object. $taxonomy will be the taxonomy name, so for
#// example, if 'category', it would be 'get_category' as the filter name. Useful
#// for custom taxonomies or plugging into default taxonomies.
#// 
#// @todo Better formatting for DocBlock
#// 
#// @since 2.3.0
#// @since 4.4.0 Converted to return a WP_Term object if `$output` is `OBJECT`.
#// The `$taxonomy` parameter was made optional.
#// 
#// @see sanitize_term_field() The $context param lists the available values for get_term_by() $filter param.
#// 
#// @param int|WP_Term|object $term If integer, term data will be fetched from the database, or from the cache if
#// available. If stdClass object (as in the results of a database query), will apply
#// filters and return a `WP_Term` object corresponding to the `$term` data. If `WP_Term`,
#// will return `$term`.
#// @param string     $taxonomy Optional. Taxonomy name that $term is part of.
#// @param string     $output   Optional. The required return type. One of OBJECT, ARRAY_A, or ARRAY_N, which correspond to
#// a WP_Term object, an associative array, or a numeric array, respectively. Default OBJECT.
#// @param string     $filter   Optional, default is raw or no WordPress defined filter will applied.
#// @return WP_Term|array|WP_Error|null Object of the type specified by `$output` on success. When `$output` is 'OBJECT',
#// a WP_Term instance is returned. If taxonomy does not exist, a WP_Error is
#// returned. Returns null for miscellaneous failure.
#//
def get_term(term=None, taxonomy="", output=OBJECT, filter="raw", *args_):
    
    if php_empty(lambda : term):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_term", __("Empty Term.")))
    # end if
    if taxonomy and (not taxonomy_exists(taxonomy)):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_taxonomy", __("Invalid taxonomy.")))
    # end if
    if type(term).__name__ == "WP_Term":
        _term = term
    elif php_is_object(term):
        if php_empty(lambda : term.filter) or "raw" == term.filter:
            _term = sanitize_term(term, taxonomy, "raw")
            _term = php_new_class("WP_Term", lambda : WP_Term(_term))
        else:
            _term = WP_Term.get_instance(term.term_id)
        # end if
    else:
        _term = WP_Term.get_instance(term, taxonomy)
    # end if
    if is_wp_error(_term):
        return _term
    elif (not _term):
        return None
    # end if
    #// Ensure for filters that this is not empty.
    taxonomy = _term.taxonomy
    #// 
    #// Filters a taxonomy term object.
    #// 
    #// @since 2.3.0
    #// @since 4.4.0 `$_term` is now a `WP_Term` object.
    #// 
    #// @param WP_Term $_term    Term object.
    #// @param string  $taxonomy The taxonomy slug.
    #//
    _term = apply_filters("get_term", _term, taxonomy)
    #// 
    #// Filters a taxonomy term object.
    #// 
    #// The dynamic portion of the filter name, `$taxonomy`, refers
    #// to the slug of the term's taxonomy.
    #// 
    #// @since 2.3.0
    #// @since 4.4.0 `$_term` is now a `WP_Term` object.
    #// 
    #// @param WP_Term $_term    Term object.
    #// @param string  $taxonomy The taxonomy slug.
    #//
    _term = apply_filters(str("get_") + str(taxonomy), _term, taxonomy)
    #// Bail if a filter callback has changed the type of the `$_term` object.
    if (not type(_term).__name__ == "WP_Term"):
        return _term
    # end if
    #// Sanitize term, according to the specified filter.
    _term.filter(filter)
    if ARRAY_A == output:
        return _term.to_array()
    elif ARRAY_N == output:
        return php_array_values(_term.to_array())
    # end if
    return _term
# end def get_term
#// 
#// Get all Term data from database by Term field and data.
#// 
#// Warning: $value is not escaped for 'name' $field. You must do it yourself, if
#// required.
#// 
#// The default $field is 'id', therefore it is possible to also use null for
#// field, but not recommended that you do so.
#// 
#// If $value does not exist, the return value will be false. If $taxonomy exists
#// and $field and $value combinations exist, the Term will be returned.
#// 
#// This function will always return the first term that matches the `$field`-
#// `$value`-`$taxonomy` combination specified in the parameters. If your query
#// is likely to match more than one term (as is likely to be the case when
#// `$field` is 'name', for example), consider using get_terms() instead; that
#// way, you will get all matching terms, and can provide your own logic for
#// deciding which one was intended.
#// 
#// @todo Better formatting for DocBlock.
#// 
#// @since 2.3.0
#// @since 4.4.0 `$taxonomy` is optional if `$field` is 'term_taxonomy_id'. Converted to return
#// a WP_Term object if `$output` is `OBJECT`.
#// 
#// @see sanitize_term_field() The $context param lists the available values for get_term_by() $filter param.
#// 
#// @param string     $field    Either 'slug', 'name', 'id' (term_id), or 'term_taxonomy_id'
#// @param string|int $value    Search for this term value
#// @param string     $taxonomy Taxonomy name. Optional, if `$field` is 'term_taxonomy_id'.
#// @param string     $output   Optional. The required return type. One of OBJECT, ARRAY_A, or ARRAY_N, which correspond to
#// a WP_Term object, an associative array, or a numeric array, respectively. Default OBJECT.
#// @param string     $filter   Optional, default is raw or no WordPress defined filter will applied.
#// @return WP_Term|array|false WP_Term instance (or array) on success. Will return false if `$taxonomy` does not exist
#// or `$term` was not found.
#//
def get_term_by(field=None, value=None, taxonomy="", output=OBJECT, filter="raw", *args_):
    
    #// 'term_taxonomy_id' lookups don't require taxonomy checks.
    if "term_taxonomy_id" != field and (not taxonomy_exists(taxonomy)):
        return False
    # end if
    #// No need to perform a query for empty 'slug' or 'name'.
    if "slug" == field or "name" == field:
        value = php_str(value)
        if 0 == php_strlen(value):
            return False
        # end if
    # end if
    if "id" == field or "term_id" == field:
        term = get_term(php_int(value), taxonomy, output, filter)
        if is_wp_error(term) or None == term:
            term = False
        # end if
        return term
    # end if
    args = Array({"get": "all", "number": 1, "taxonomy": taxonomy, "update_term_meta_cache": False, "orderby": "none", "suppress_filter": True})
    for case in Switch(field):
        if case("slug"):
            args["slug"] = value
            break
        # end if
        if case("name"):
            args["name"] = value
            break
        # end if
        if case("term_taxonomy_id"):
            args["term_taxonomy_id"] = value
            args["taxonomy"] = None
            break
        # end if
        if case():
            return False
        # end if
    # end for
    terms = get_terms(args)
    if is_wp_error(terms) or php_empty(lambda : terms):
        return False
    # end if
    term = php_array_shift(terms)
    #// In the case of 'term_taxonomy_id', override the provided `$taxonomy` with whatever we find in the DB.
    if "term_taxonomy_id" == field:
        taxonomy = term.taxonomy
    # end if
    return get_term(term, taxonomy, output, filter)
# end def get_term_by
#// 
#// Merge all term children into a single array of their IDs.
#// 
#// This recursive function will merge all of the children of $term into the same
#// array of term IDs. Only useful for taxonomies which are hierarchical.
#// 
#// Will return an empty array if $term does not exist in $taxonomy.
#// 
#// @since 2.3.0
#// 
#// @param int    $term_id  ID of Term to get children.
#// @param string $taxonomy Taxonomy Name.
#// @return array|WP_Error List of Term IDs. WP_Error returned if `$taxonomy` does not exist.
#//
def get_term_children(term_id=None, taxonomy=None, *args_):
    
    if (not taxonomy_exists(taxonomy)):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_taxonomy", __("Invalid taxonomy.")))
    # end if
    term_id = php_intval(term_id)
    terms = _get_term_hierarchy(taxonomy)
    if (not (php_isset(lambda : terms[term_id]))):
        return Array()
    # end if
    children = terms[term_id]
    for child in terms[term_id]:
        if term_id == child:
            continue
        # end if
        if (php_isset(lambda : terms[child])):
            children = php_array_merge(children, get_term_children(child, taxonomy))
        # end if
    # end for
    return children
# end def get_term_children
#// 
#// Get sanitized Term field.
#// 
#// The function is for contextual reasons and for simplicity of usage.
#// 
#// @since 2.3.0
#// @since 4.4.0 The `$taxonomy` parameter was made optional. `$term` can also now accept a WP_Term object.
#// 
#// @see sanitize_term_field()
#// 
#// @param string      $field    Term field to fetch.
#// @param int|WP_Term $term     Term ID or object.
#// @param string      $taxonomy Optional. Taxonomy Name. Default empty.
#// @param string      $context  Optional, default is display. Look at sanitize_term_field() for available options.
#// @return string|int|null|WP_Error Will return an empty string if $term is not an object or if $field is not set in $term.
#//
def get_term_field(field=None, term=None, taxonomy="", context="display", *args_):
    
    term = get_term(term, taxonomy)
    if is_wp_error(term):
        return term
    # end if
    if (not php_is_object(term)):
        return ""
    # end if
    if (not (php_isset(lambda : term.field))):
        return ""
    # end if
    return sanitize_term_field(field, term.field, term.term_id, term.taxonomy, context)
# end def get_term_field
#// 
#// Sanitizes Term for editing.
#// 
#// Return value is sanitize_term() and usage is for sanitizing the term for
#// editing. Function is for contextual and simplicity.
#// 
#// @since 2.3.0
#// 
#// @param int|object $id       Term ID or object.
#// @param string     $taxonomy Taxonomy name.
#// @return string|int|null|WP_Error Will return empty string if $term is not an object.
#//
def get_term_to_edit(id=None, taxonomy=None, *args_):
    
    term = get_term(id, taxonomy)
    if is_wp_error(term):
        return term
    # end if
    if (not php_is_object(term)):
        return ""
    # end if
    return sanitize_term(term, taxonomy, "edit")
# end def get_term_to_edit
#// 
#// Retrieve the terms in a given taxonomy or list of taxonomies.
#// 
#// You can fully inject any customizations to the query before it is sent, as
#// well as control the output with a filter.
#// 
#// The {@see 'get_terms'} filter will be called when the cache has the term and will
#// pass the found term along with the array of $taxonomies and array of $args.
#// This filter is also called before the array of terms is passed and will pass
#// the array of terms, along with the $taxonomies and $args.
#// 
#// The {@see 'list_terms_exclusions'} filter passes the compiled exclusions along with
#// the $args.
#// 
#// The {@see 'get_terms_orderby'} filter passes the `ORDER BY` clause for the query
#// along with the $args array.
#// 
#// Prior to 4.5.0, the first parameter of `get_terms()` was a taxonomy or list of taxonomies:
#// 
#// $terms = get_terms( 'post_tag', array(
#// 'hide_empty' => false,
#// ) );
#// 
#// Since 4.5.0, taxonomies should be passed via the 'taxonomy' argument in the `$args` array:
#// 
#// $terms = get_terms( array(
#// 'taxonomy' => 'post_tag',
#// 'hide_empty' => false,
#// ) );
#// 
#// @since 2.3.0
#// @since 4.2.0 Introduced 'name' and 'childless' parameters.
#// @since 4.4.0 Introduced the ability to pass 'term_id' as an alias of 'id' for the `orderby` parameter.
#// Introduced the 'meta_query' and 'update_term_meta_cache' parameters. Converted to return
#// a list of WP_Term objects.
#// @since 4.5.0 Changed the function signature so that the `$args` array can be provided as the first parameter.
#// Introduced 'meta_key' and 'meta_value' parameters. Introduced the ability to order results by metadata.
#// @since 4.8.0 Introduced 'suppress_filter' parameter.
#// 
#// @internal The `$deprecated` parameter is parsed for backward compatibility only.
#// 
#// @param array|string $args       Optional. Array or string of arguments. See WP_Term_Query::__construct()
#// for information on accepted arguments. Default empty.
#// @param array|string $deprecated Argument array, when using the legacy function parameter format. If present, this
#// parameter will be interpreted as `$args`, and the first function parameter will
#// be parsed as a taxonomy or array of taxonomies.
#// @return WP_Term[]|int|WP_Error List of WP_Term instances and their children. Will return WP_Error, if any of taxonomies
#// do not exist.
#//
def get_terms(args=Array(), deprecated="", *args_):
    
    term_query = php_new_class("WP_Term_Query", lambda : WP_Term_Query())
    defaults = Array({"suppress_filter": False})
    #// 
    #// Legacy argument format ($taxonomy, $args) takes precedence.
    #// 
    #// We detect legacy argument format by checking if
    #// (a) a second non-empty parameter is passed, or
    #// (b) the first parameter shares no keys with the default array (ie, it's a list of taxonomies)
    #//
    _args = wp_parse_args(args)
    key_intersect = php_array_intersect_key(term_query.query_var_defaults, _args)
    do_legacy_args = deprecated or php_empty(lambda : key_intersect)
    if do_legacy_args:
        taxonomies = args
        args = wp_parse_args(deprecated, defaults)
        args["taxonomy"] = taxonomies
    else:
        args = wp_parse_args(args, defaults)
        if (php_isset(lambda : args["taxonomy"])) and None != args["taxonomy"]:
            args["taxonomy"] = args["taxonomy"]
        # end if
    # end if
    if (not php_empty(lambda : args["taxonomy"])):
        for taxonomy in args["taxonomy"]:
            if (not taxonomy_exists(taxonomy)):
                return php_new_class("WP_Error", lambda : WP_Error("invalid_taxonomy", __("Invalid taxonomy.")))
            # end if
        # end for
    # end if
    #// Don't pass suppress_filter to WP_Term_Query.
    suppress_filter = args["suppress_filter"]
    args["suppress_filter"] = None
    terms = term_query.query(args)
    #// Count queries are not filtered, for legacy reasons.
    if (not php_is_array(terms)):
        return terms
    # end if
    if suppress_filter:
        return terms
    # end if
    #// 
    #// Filters the found terms.
    #// 
    #// @since 2.3.0
    #// @since 4.6.0 Added the `$term_query` parameter.
    #// 
    #// @param array         $terms      Array of found terms.
    #// @param array         $taxonomies An array of taxonomies.
    #// @param array         $args       An array of get_terms() arguments.
    #// @param WP_Term_Query $term_query The WP_Term_Query object.
    #//
    return apply_filters("get_terms", terms, term_query.query_vars["taxonomy"], term_query.query_vars, term_query)
# end def get_terms
#// 
#// Adds metadata to a term.
#// 
#// @since 4.4.0
#// 
#// @param int    $term_id    Term ID.
#// @param string $meta_key   Metadata name.
#// @param mixed  $meta_value Metadata value.
#// @param bool   $unique     Optional. Whether to bail if an entry with the same key is found for the term.
#// Default false.
#// @return int|WP_Error|bool Meta ID on success. WP_Error when term_id is ambiguous between taxonomies.
#// False on failure.
#//
def add_term_meta(term_id=None, meta_key=None, meta_value=None, unique=False, *args_):
    
    if wp_term_is_shared(term_id):
        return php_new_class("WP_Error", lambda : WP_Error("ambiguous_term_id", __("Term meta cannot be added to terms that are shared between taxonomies."), term_id))
    # end if
    return add_metadata("term", term_id, meta_key, meta_value, unique)
# end def add_term_meta
#// 
#// Removes metadata matching criteria from a term.
#// 
#// @since 4.4.0
#// 
#// @param int    $term_id    Term ID.
#// @param string $meta_key   Metadata name.
#// @param mixed  $meta_value Optional. Metadata value. If provided, rows will only be removed that match the value.
#// @return bool True on success, false on failure.
#//
def delete_term_meta(term_id=None, meta_key=None, meta_value="", *args_):
    
    return delete_metadata("term", term_id, meta_key, meta_value)
# end def delete_term_meta
#// 
#// Retrieves metadata for a term.
#// 
#// @since 4.4.0
#// 
#// @param int    $term_id Term ID.
#// @param string $key     Optional. The meta key to retrieve. If no key is provided, fetches all metadata for the term.
#// @param bool   $single  Whether to return a single value. If false, an array of all values matching the
#// `$term_id`/`$key` pair will be returned. Default: false.
#// @return mixed If `$single` is false, an array of metadata values. If `$single` is true, a single metadata value.
#//
def get_term_meta(term_id=None, key="", single=False, *args_):
    
    return get_metadata("term", term_id, key, single)
# end def get_term_meta
#// 
#// Updates term metadata.
#// 
#// Use the `$prev_value` parameter to differentiate between meta fields with the same key and term ID.
#// 
#// If the meta field for the term does not exist, it will be added.
#// 
#// @since 4.4.0
#// 
#// @param int    $term_id    Term ID.
#// @param string $meta_key   Metadata key.
#// @param mixed  $meta_value Metadata value.
#// @param mixed  $prev_value Optional. Previous value to check before removing.
#// @return int|WP_Error|bool Meta ID if the key didn't previously exist. True on successful update.
#// WP_Error when term_id is ambiguous between taxonomies. False on failure.
#//
def update_term_meta(term_id=None, meta_key=None, meta_value=None, prev_value="", *args_):
    
    if wp_term_is_shared(term_id):
        return php_new_class("WP_Error", lambda : WP_Error("ambiguous_term_id", __("Term meta cannot be added to terms that are shared between taxonomies."), term_id))
    # end if
    return update_metadata("term", term_id, meta_key, meta_value, prev_value)
# end def update_term_meta
#// 
#// Updates metadata cache for list of term IDs.
#// 
#// Performs SQL query to retrieve all metadata for the terms matching `$term_ids` and stores them in the cache.
#// Subsequent calls to `get_term_meta()` will not need to query the database.
#// 
#// @since 4.4.0
#// 
#// @param array $term_ids List of term IDs.
#// @return array|false Returns false if there is nothing to update. Returns an array of metadata on success.
#//
def update_termmeta_cache(term_ids=None, *args_):
    
    return update_meta_cache("term", term_ids)
# end def update_termmeta_cache
#// 
#// Get all meta data, including meta IDs, for the given term ID.
#// 
#// @since 4.9.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int $term_id Term ID.
#// @return array|false Array with meta data, or false when the meta table is not installed.
#//
def has_term_meta(term_id=None, *args_):
    
    check = wp_check_term_meta_support_prefilter(None)
    if None != check:
        return check
    # end if
    global wpdb
    php_check_if_defined("wpdb")
    return wpdb.get_results(wpdb.prepare(str("SELECT meta_key, meta_value, meta_id, term_id FROM ") + str(wpdb.termmeta) + str(" WHERE term_id = %d ORDER BY meta_key,meta_id"), term_id), ARRAY_A)
# end def has_term_meta
#// 
#// Registers a meta key for terms.
#// 
#// @since 4.9.8
#// 
#// @param string $taxonomy Taxonomy to register a meta key for. Pass an empty string
#// to register the meta key across all existing taxonomies.
#// @param string $meta_key The meta key to register.
#// @param array  $args     Data used to describe the meta key when registered. See
#// {@see register_meta()} for a list of supported arguments.
#// @return bool True if the meta key was successfully registered, false if not.
#//
def register_term_meta(taxonomy=None, meta_key=None, args=None, *args_):
    
    args["object_subtype"] = taxonomy
    return register_meta("term", meta_key, args)
# end def register_term_meta
#// 
#// Unregisters a meta key for terms.
#// 
#// @since 4.9.8
#// 
#// @param string $taxonomy Taxonomy the meta key is currently registered for. Pass
#// an empty string if the meta key is registered across all
#// existing taxonomies.
#// @param string $meta_key The meta key to unregister.
#// @return bool True on success, false if the meta key was not previously registered.
#//
def unregister_term_meta(taxonomy=None, meta_key=None, *args_):
    
    return unregister_meta_key("term", meta_key, taxonomy)
# end def unregister_term_meta
#// 
#// Determines whether a taxonomy term exists.
#// 
#// Formerly is_term(), introduced in 2.3.0.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 3.0.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int|string $term     The term to check. Accepts term ID, slug, or name.
#// @param string     $taxonomy Optional. The taxonomy name to use.
#// @param int        $parent   Optional. ID of parent term under which to confine the exists search.
#// @return mixed Returns null if the term does not exist.
#// Returns the term ID if no taxonomy is specified and the term ID exists.
#// Returns an array of the term ID and the term taxonomy ID if the taxonomy is specified and the pairing exists.
#// Returns 0 if term ID 0 is passed to the function.
#//
def term_exists(term=None, taxonomy="", parent=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    select = str("SELECT term_id FROM ") + str(wpdb.terms) + str(" as t WHERE ")
    tax_select = str("SELECT tt.term_id, tt.term_taxonomy_id FROM ") + str(wpdb.terms) + str(" AS t INNER JOIN ") + str(wpdb.term_taxonomy) + str(" as tt ON tt.term_id = t.term_id WHERE ")
    if php_is_int(term):
        if 0 == term:
            return 0
        # end if
        where = "t.term_id = %d"
        if (not php_empty(lambda : taxonomy)):
            #// phpcs:ignore WordPress.DB.PreparedSQLPlaceholders.ReplacementsWrongNumber
            return wpdb.get_row(wpdb.prepare(tax_select + where + " AND tt.taxonomy = %s", term, taxonomy), ARRAY_A)
        else:
            return wpdb.get_var(wpdb.prepare(select + where, term))
        # end if
    # end if
    term = php_trim(wp_unslash(term))
    slug = sanitize_title(term)
    where = "t.slug = %s"
    else_where = "t.name = %s"
    where_fields = Array(slug)
    else_where_fields = Array(term)
    orderby = "ORDER BY t.term_id ASC"
    limit = "LIMIT 1"
    if (not php_empty(lambda : taxonomy)):
        if php_is_numeric(parent):
            parent = php_int(parent)
            where_fields[-1] = parent
            else_where_fields[-1] = parent
            where += " AND tt.parent = %d"
            else_where += " AND tt.parent = %d"
        # end if
        where_fields[-1] = taxonomy
        else_where_fields[-1] = taxonomy
        result = wpdb.get_row(wpdb.prepare(str("SELECT tt.term_id, tt.term_taxonomy_id FROM ") + str(wpdb.terms) + str(" AS t INNER JOIN ") + str(wpdb.term_taxonomy) + str(" as tt ON tt.term_id = t.term_id WHERE ") + str(where) + str(" AND tt.taxonomy = %s ") + str(orderby) + str(" ") + str(limit), where_fields), ARRAY_A)
        if result:
            return result
        # end if
        return wpdb.get_row(wpdb.prepare(str("SELECT tt.term_id, tt.term_taxonomy_id FROM ") + str(wpdb.terms) + str(" AS t INNER JOIN ") + str(wpdb.term_taxonomy) + str(" as tt ON tt.term_id = t.term_id WHERE ") + str(else_where) + str(" AND tt.taxonomy = %s ") + str(orderby) + str(" ") + str(limit), else_where_fields), ARRAY_A)
    # end if
    #// phpcs:ignore WordPress.DB.PreparedSQLPlaceholders.UnfinishedPrepare
    result = wpdb.get_var(wpdb.prepare(str("SELECT term_id FROM ") + str(wpdb.terms) + str(" as t WHERE ") + str(where) + str(" ") + str(orderby) + str(" ") + str(limit), where_fields))
    if result:
        return result
    # end if
    #// phpcs:ignore WordPress.DB.PreparedSQLPlaceholders.UnfinishedPrepare
    return wpdb.get_var(wpdb.prepare(str("SELECT term_id FROM ") + str(wpdb.terms) + str(" as t WHERE ") + str(else_where) + str(" ") + str(orderby) + str(" ") + str(limit), else_where_fields))
# end def term_exists
#// 
#// Check if a term is an ancestor of another term.
#// 
#// You can use either an id or the term object for both parameters.
#// 
#// @since 3.4.0
#// 
#// @param int|object $term1    ID or object to check if this is the parent term.
#// @param int|object $term2    The child term.
#// @param string     $taxonomy Taxonomy name that $term1 and `$term2` belong to.
#// @return bool Whether `$term2` is a child of `$term1`.
#//
def term_is_ancestor_of(term1=None, term2=None, taxonomy=None, *args_):
    
    if (not (php_isset(lambda : term1.term_id))):
        term1 = get_term(term1, taxonomy)
    # end if
    if (not (php_isset(lambda : term2.parent))):
        term2 = get_term(term2, taxonomy)
    # end if
    if php_empty(lambda : term1.term_id) or php_empty(lambda : term2.parent):
        return False
    # end if
    if term2.parent == term1.term_id:
        return True
    # end if
    return term_is_ancestor_of(term1, get_term(term2.parent, taxonomy), taxonomy)
# end def term_is_ancestor_of
#// 
#// Sanitize Term all fields.
#// 
#// Relies on sanitize_term_field() to sanitize the term. The difference is that
#// this function will sanitize <strong>all</strong> fields. The context is based
#// on sanitize_term_field().
#// 
#// The $term is expected to be either an array or an object.
#// 
#// @since 2.3.0
#// 
#// @param array|object $term     The term to check.
#// @param string       $taxonomy The taxonomy name to use.
#// @param string       $context  Optional. Context in which to sanitize the term. Accepts 'edit', 'db',
#// 'display', 'attribute', or 'js'. Default 'display'.
#// @return array|object Term with all fields sanitized.
#//
def sanitize_term(term=None, taxonomy=None, context="display", *args_):
    
    fields = Array("term_id", "name", "description", "slug", "count", "parent", "term_group", "term_taxonomy_id", "object_id")
    do_object = php_is_object(term)
    term_id = term.term_id if do_object else term["term_id"] if (php_isset(lambda : term["term_id"])) else 0
    for field in fields:
        if do_object:
            if (php_isset(lambda : term.field)):
                term.field = sanitize_term_field(field, term.field, term_id, taxonomy, context)
            # end if
        else:
            if (php_isset(lambda : term[field])):
                term[field] = sanitize_term_field(field, term[field], term_id, taxonomy, context)
            # end if
        # end if
    # end for
    if do_object:
        term.filter = context
    else:
        term["filter"] = context
    # end if
    return term
# end def sanitize_term
#// 
#// Cleanse the field value in the term based on the context.
#// 
#// Passing a term field value through the function should be assumed to have
#// cleansed the value for whatever context the term field is going to be used.
#// 
#// If no context or an unsupported context is given, then default filters will
#// be applied.
#// 
#// There are enough filters for each context to support a custom filtering
#// without creating your own filter function. Simply create a function that
#// hooks into the filter you need.
#// 
#// @since 2.3.0
#// 
#// @param string $field    Term field to sanitize.
#// @param string $value    Search for this term value.
#// @param int    $term_id  Term ID.
#// @param string $taxonomy Taxonomy Name.
#// @param string $context  Context in which to sanitize the term field. Accepts 'edit', 'db', 'display',
#// 'attribute', or 'js'.
#// @return mixed Sanitized field.
#//
def sanitize_term_field(field=None, value=None, term_id=None, taxonomy=None, context=None, *args_):
    
    int_fields = Array("parent", "term_id", "count", "term_group", "term_taxonomy_id", "object_id")
    if php_in_array(field, int_fields):
        value = php_int(value)
        if value < 0:
            value = 0
        # end if
    # end if
    context = php_strtolower(context)
    if "raw" == context:
        return value
    # end if
    if "edit" == context:
        #// 
        #// Filters a term field to edit before it is sanitized.
        #// 
        #// The dynamic portion of the filter name, `$field`, refers to the term field.
        #// 
        #// @since 2.3.0
        #// 
        #// @param mixed $value     Value of the term field.
        #// @param int   $term_id   Term ID.
        #// @param string $taxonomy Taxonomy slug.
        #//
        value = apply_filters(str("edit_term_") + str(field), value, term_id, taxonomy)
        #// 
        #// Filters the taxonomy field to edit before it is sanitized.
        #// 
        #// The dynamic portions of the filter name, `$taxonomy` and `$field`, refer
        #// to the taxonomy slug and taxonomy field, respectively.
        #// 
        #// @since 2.3.0
        #// 
        #// @param mixed $value   Value of the taxonomy field to edit.
        #// @param int   $term_id Term ID.
        #//
        value = apply_filters(str("edit_") + str(taxonomy) + str("_") + str(field), value, term_id)
        if "description" == field:
            value = esc_html(value)
            pass
        else:
            value = esc_attr(value)
        # end if
    elif "db" == context:
        #// 
        #// Filters a term field value before it is sanitized.
        #// 
        #// The dynamic portion of the filter name, `$field`, refers to the term field.
        #// 
        #// @since 2.3.0
        #// 
        #// @param mixed  $value    Value of the term field.
        #// @param string $taxonomy Taxonomy slug.
        #//
        value = apply_filters(str("pre_term_") + str(field), value, taxonomy)
        #// 
        #// Filters a taxonomy field before it is sanitized.
        #// 
        #// The dynamic portions of the filter name, `$taxonomy` and `$field`, refer
        #// to the taxonomy slug and field name, respectively.
        #// 
        #// @since 2.3.0
        #// 
        #// @param mixed $value Value of the taxonomy field.
        #//
        value = apply_filters(str("pre_") + str(taxonomy) + str("_") + str(field), value)
        #// Back compat filters.
        if "slug" == field:
            #// 
            #// Filters the category nicename before it is sanitized.
            #// 
            #// Use the {@see 'pre_$taxonomy_$field'} hook instead.
            #// 
            #// @since 2.0.3
            #// 
            #// @param string $value The category nicename.
            #//
            value = apply_filters("pre_category_nicename", value)
        # end if
    elif "rss" == context:
        #// 
        #// Filters the term field for use in RSS.
        #// 
        #// The dynamic portion of the filter name, `$field`, refers to the term field.
        #// 
        #// @since 2.3.0
        #// 
        #// @param mixed  $value    Value of the term field.
        #// @param string $taxonomy Taxonomy slug.
        #//
        value = apply_filters(str("term_") + str(field) + str("_rss"), value, taxonomy)
        #// 
        #// Filters the taxonomy field for use in RSS.
        #// 
        #// The dynamic portions of the hook name, `$taxonomy`, and `$field`, refer
        #// to the taxonomy slug and field name, respectively.
        #// 
        #// @since 2.3.0
        #// 
        #// @param mixed $value Value of the taxonomy field.
        #//
        value = apply_filters(str(taxonomy) + str("_") + str(field) + str("_rss"), value)
    else:
        #// Use display filters by default.
        #// 
        #// Filters the term field sanitized for display.
        #// 
        #// The dynamic portion of the filter name, `$field`, refers to the term field name.
        #// 
        #// @since 2.3.0
        #// 
        #// @param mixed  $value    Value of the term field.
        #// @param int    $term_id  Term ID.
        #// @param string $taxonomy Taxonomy slug.
        #// @param string $context  Context to retrieve the term field value.
        #//
        value = apply_filters(str("term_") + str(field), value, term_id, taxonomy, context)
        #// 
        #// Filters the taxonomy field sanitized for display.
        #// 
        #// The dynamic portions of the filter name, `$taxonomy`, and `$field`, refer
        #// to the taxonomy slug and taxonomy field, respectively.
        #// 
        #// @since 2.3.0
        #// 
        #// @param mixed  $value   Value of the taxonomy field.
        #// @param int    $term_id Term ID.
        #// @param string $context Context to retrieve the taxonomy field value.
        #//
        value = apply_filters(str(taxonomy) + str("_") + str(field), value, term_id, context)
    # end if
    if "attribute" == context:
        value = esc_attr(value)
    elif "js" == context:
        value = esc_js(value)
    # end if
    return value
# end def sanitize_term_field
#// 
#// Count how many terms are in Taxonomy.
#// 
#// Default $args is 'hide_empty' which can be 'hide_empty=true' or array('hide_empty' => true).
#// 
#// @since 2.3.0
#// 
#// @param string       $taxonomy Taxonomy name.
#// @param array|string $args     Optional. Array of arguments that get passed to get_terms().
#// Default empty array.
#// @return array|int|WP_Error Number of terms in that taxonomy or WP_Error if the taxonomy does not exist.
#//
def wp_count_terms(taxonomy=None, args=Array(), *args_):
    
    defaults = Array({"taxonomy": taxonomy, "hide_empty": False})
    args = wp_parse_args(args, defaults)
    #// Backward compatibility.
    if (php_isset(lambda : args["ignore_empty"])):
        args["hide_empty"] = args["ignore_empty"]
        args["ignore_empty"] = None
    # end if
    args["fields"] = "count"
    return get_terms(args)
# end def wp_count_terms
#// 
#// Will unlink the object from the taxonomy or taxonomies.
#// 
#// Will remove all relationships between the object and any terms in
#// a particular taxonomy or taxonomies. Does not remove the term or
#// taxonomy itself.
#// 
#// @since 2.3.0
#// 
#// @param int          $object_id  The term Object Id that refers to the term.
#// @param string|array $taxonomies List of Taxonomy Names or single Taxonomy name.
#//
def wp_delete_object_term_relationships(object_id=None, taxonomies=None, *args_):
    
    object_id = php_int(object_id)
    if (not php_is_array(taxonomies)):
        taxonomies = Array(taxonomies)
    # end if
    for taxonomy in taxonomies:
        term_ids = wp_get_object_terms(object_id, taxonomy, Array({"fields": "ids"}))
        term_ids = php_array_map("intval", term_ids)
        wp_remove_object_terms(object_id, term_ids, taxonomy)
    # end for
# end def wp_delete_object_term_relationships
#// 
#// Removes a term from the database.
#// 
#// If the term is a parent of other terms, then the children will be updated to
#// that term's parent.
#// 
#// Metadata associated with the term will be deleted.
#// 
#// @since 2.3.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int          $term     Term ID.
#// @param string       $taxonomy Taxonomy Name.
#// @param array|string $args {
#// Optional. Array of arguments to override the default term ID. Default empty array.
#// 
#// @type int  $default       The term ID to make the default term. This will only override
#// the terms found if there is only one term found. Any other and
#// the found terms are used.
#// @type bool $force_default Optional. Whether to force the supplied term as default to be
#// assigned even if the object was not going to be term-less.
#// Default false.
#// }
#// @return bool|int|WP_Error True on success, false if term does not exist. Zero on attempted
#// deletion of default Category. WP_Error if the taxonomy does not exist.
#//
def wp_delete_term(term=None, taxonomy=None, args=Array(), *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    term = php_int(term)
    ids = term_exists(term, taxonomy)
    if (not ids):
        return False
    # end if
    if is_wp_error(ids):
        return ids
    # end if
    tt_id = ids["term_taxonomy_id"]
    defaults = Array()
    if "category" == taxonomy:
        defaults["default"] = php_int(get_option("default_category"))
        if defaults["default"] == term:
            return 0
            pass
        # end if
    # end if
    args = wp_parse_args(args, defaults)
    if (php_isset(lambda : args["default"])):
        default = php_int(args["default"])
        if (not term_exists(default, taxonomy)):
            default = None
        # end if
    # end if
    if (php_isset(lambda : args["force_default"])):
        force_default = args["force_default"]
    # end if
    #// 
    #// Fires when deleting a term, before any modifications are made to posts or terms.
    #// 
    #// @since 4.1.0
    #// 
    #// @param int    $term     Term ID.
    #// @param string $taxonomy Taxonomy Name.
    #//
    do_action("pre_delete_term", term, taxonomy)
    #// Update children to point to new parent.
    if is_taxonomy_hierarchical(taxonomy):
        term_obj = get_term(term, taxonomy)
        if is_wp_error(term_obj):
            return term_obj
        # end if
        parent = term_obj.parent
        edit_ids = wpdb.get_results(str("SELECT term_id, term_taxonomy_id FROM ") + str(wpdb.term_taxonomy) + str(" WHERE `parent` = ") + php_int(term_obj.term_id))
        edit_tt_ids = wp_list_pluck(edit_ids, "term_taxonomy_id")
        #// 
        #// Fires immediately before a term to delete's children are reassigned a parent.
        #// 
        #// @since 2.9.0
        #// 
        #// @param array $edit_tt_ids An array of term taxonomy IDs for the given term.
        #//
        do_action("edit_term_taxonomies", edit_tt_ids)
        wpdb.update(wpdb.term_taxonomy, compact("parent"), Array({"parent": term_obj.term_id}) + compact("taxonomy"))
        #// Clean the cache for all child terms.
        edit_term_ids = wp_list_pluck(edit_ids, "term_id")
        clean_term_cache(edit_term_ids, taxonomy)
        #// 
        #// Fires immediately after a term to delete's children are reassigned a parent.
        #// 
        #// @since 2.9.0
        #// 
        #// @param array $edit_tt_ids An array of term taxonomy IDs for the given term.
        #//
        do_action("edited_term_taxonomies", edit_tt_ids)
    # end if
    #// Get the term before deleting it or its term relationships so we can pass to actions below.
    deleted_term = get_term(term, taxonomy)
    object_ids = wpdb.get_col(wpdb.prepare(str("SELECT object_id FROM ") + str(wpdb.term_relationships) + str(" WHERE term_taxonomy_id = %d"), tt_id))
    for object_id in object_ids:
        terms = wp_get_object_terms(object_id, taxonomy, Array({"fields": "ids", "orderby": "none"}))
        if 1 == php_count(terms) and (php_isset(lambda : default)):
            terms = Array(default)
        else:
            terms = php_array_diff(terms, Array(term))
            if (php_isset(lambda : default)) and (php_isset(lambda : force_default)) and force_default:
                terms = php_array_merge(terms, Array(default))
            # end if
        # end if
        terms = php_array_map("intval", terms)
        wp_set_object_terms(object_id, terms, taxonomy)
    # end for
    #// Clean the relationship caches for all object types using this term.
    tax_object = get_taxonomy(taxonomy)
    for object_type in tax_object.object_type:
        clean_object_term_cache(object_ids, object_type)
    # end for
    term_meta_ids = wpdb.get_col(wpdb.prepare(str("SELECT meta_id FROM ") + str(wpdb.termmeta) + str(" WHERE term_id = %d "), term))
    for mid in term_meta_ids:
        delete_metadata_by_mid("term", mid)
    # end for
    #// 
    #// Fires immediately before a term taxonomy ID is deleted.
    #// 
    #// @since 2.9.0
    #// 
    #// @param int $tt_id Term taxonomy ID.
    #//
    do_action("delete_term_taxonomy", tt_id)
    wpdb.delete(wpdb.term_taxonomy, Array({"term_taxonomy_id": tt_id}))
    #// 
    #// Fires immediately after a term taxonomy ID is deleted.
    #// 
    #// @since 2.9.0
    #// 
    #// @param int $tt_id Term taxonomy ID.
    #//
    do_action("deleted_term_taxonomy", tt_id)
    #// Delete the term if no taxonomies use it.
    if (not wpdb.get_var(wpdb.prepare(str("SELECT COUNT(*) FROM ") + str(wpdb.term_taxonomy) + str(" WHERE term_id = %d"), term))):
        wpdb.delete(wpdb.terms, Array({"term_id": term}))
    # end if
    clean_term_cache(term, taxonomy)
    #// 
    #// Fires after a term is deleted from the database and the cache is cleaned.
    #// 
    #// @since 2.5.0
    #// @since 4.5.0 Introduced the `$object_ids` argument.
    #// 
    #// @param int     $term         Term ID.
    #// @param int     $tt_id        Term taxonomy ID.
    #// @param string  $taxonomy     Taxonomy slug.
    #// @param mixed   $deleted_term Copy of the already-deleted term, in the form specified
    #// by the parent function. WP_Error otherwise.
    #// @param array   $object_ids   List of term object IDs.
    #//
    do_action("delete_term", term, tt_id, taxonomy, deleted_term, object_ids)
    #// 
    #// Fires after a term in a specific taxonomy is deleted.
    #// 
    #// The dynamic portion of the hook name, `$taxonomy`, refers to the specific
    #// taxonomy the term belonged to.
    #// 
    #// @since 2.3.0
    #// @since 4.5.0 Introduced the `$object_ids` argument.
    #// 
    #// @param int     $term         Term ID.
    #// @param int     $tt_id        Term taxonomy ID.
    #// @param mixed   $deleted_term Copy of the already-deleted term, in the form specified
    #// by the parent function. WP_Error otherwise.
    #// @param array   $object_ids   List of term object IDs.
    #//
    do_action(str("delete_") + str(taxonomy), term, tt_id, deleted_term, object_ids)
    return True
# end def wp_delete_term
#// 
#// Deletes one existing category.
#// 
#// @since 2.0.0
#// 
#// @param int $cat_ID Category term ID.
#// @return bool|int|WP_Error Returns true if completes delete action; false if term doesn't exist;
#// Zero on attempted deletion of default Category; WP_Error object is also a possibility.
#//
def wp_delete_category(cat_ID=None, *args_):
    
    return wp_delete_term(cat_ID, "category")
# end def wp_delete_category
#// 
#// Retrieves the terms associated with the given object(s), in the supplied taxonomies.
#// 
#// @since 2.3.0
#// @since 4.2.0 Added support for 'taxonomy', 'parent', and 'term_taxonomy_id' values of `$orderby`.
#// Introduced `$parent` argument.
#// @since 4.4.0 Introduced `$meta_query` and `$update_term_meta_cache` arguments. When `$fields` is 'all' or
#// 'all_with_object_id', an array of `WP_Term` objects will be returned.
#// @since 4.7.0 Refactored to use WP_Term_Query, and to support any WP_Term_Query arguments.
#// 
#// @param int|int[]       $object_ids The ID(s) of the object(s) to retrieve.
#// @param string|string[] $taxonomies The taxonomy names to retrieve terms from.
#// @param array|string    $args       See WP_Term_Query::__construct() for supported arguments.
#// @return array|WP_Error The requested term data or empty array if no terms found.
#// WP_Error if any of the taxonomies don't exist.
#//
def wp_get_object_terms(object_ids=None, taxonomies=None, args=Array(), *args_):
    
    if php_empty(lambda : object_ids) or php_empty(lambda : taxonomies):
        return Array()
    # end if
    if (not php_is_array(taxonomies)):
        taxonomies = Array(taxonomies)
    # end if
    for taxonomy in taxonomies:
        if (not taxonomy_exists(taxonomy)):
            return php_new_class("WP_Error", lambda : WP_Error("invalid_taxonomy", __("Invalid taxonomy.")))
        # end if
    # end for
    if (not php_is_array(object_ids)):
        object_ids = Array(object_ids)
    # end if
    object_ids = php_array_map("intval", object_ids)
    args = wp_parse_args(args)
    #// 
    #// Filter arguments for retrieving object terms.
    #// 
    #// @since 4.9.0
    #// 
    #// @param array    $args       An array of arguments for retrieving terms for the given object(s).
    #// See {@see wp_get_object_terms()} for details.
    #// @param int[]    $object_ids Array of object IDs.
    #// @param string[] $taxonomies Array of taxonomy names to retrieve terms from.
    #//
    args = apply_filters("wp_get_object_terms_args", args, object_ids, taxonomies)
    #// 
    #// When one or more queried taxonomies is registered with an 'args' array,
    #// those params override the `$args` passed to this function.
    #//
    terms = Array()
    if php_count(taxonomies) > 1:
        for index,taxonomy in taxonomies:
            t = get_taxonomy(taxonomy)
            if (php_isset(lambda : t.args)) and php_is_array(t.args) and php_array_merge(args, t.args) != args:
                taxonomies[index] = None
                terms = php_array_merge(terms, wp_get_object_terms(object_ids, taxonomy, php_array_merge(args, t.args)))
            # end if
        # end for
    else:
        t = get_taxonomy(taxonomies[0])
        if (php_isset(lambda : t.args)) and php_is_array(t.args):
            args = php_array_merge(args, t.args)
        # end if
    # end if
    args["taxonomy"] = taxonomies
    args["object_ids"] = object_ids
    #// Taxonomies registered without an 'args' param are handled here.
    if (not php_empty(lambda : taxonomies)):
        terms_from_remaining_taxonomies = get_terms(args)
        #// Array keys should be preserved for values of $fields that use term_id for keys.
        if (not php_empty(lambda : args["fields"])) and 0 == php_strpos(args["fields"], "id=>"):
            terms = terms + terms_from_remaining_taxonomies
        else:
            terms = php_array_merge(terms, terms_from_remaining_taxonomies)
        # end if
    # end if
    #// 
    #// Filters the terms for a given object or objects.
    #// 
    #// @since 4.2.0
    #// 
    #// @param array    $terms      Array of terms for the given object or objects.
    #// @param int[]    $object_ids Array of object IDs for which terms were retrieved.
    #// @param string[] $taxonomies Array of taxonomy names from which terms were retrieved.
    #// @param array    $args       Array of arguments for retrieving terms for the given
    #// object(s). See wp_get_object_terms() for details.
    #//
    terms = apply_filters("get_object_terms", terms, object_ids, taxonomies, args)
    object_ids = php_implode(",", object_ids)
    taxonomies = "'" + php_implode("', '", php_array_map("esc_sql", taxonomies)) + "'"
    #// 
    #// Filters the terms for a given object or objects.
    #// 
    #// The `$taxonomies` parameter passed to this filter is formatted as a SQL fragment. The
    #// {@see 'get_object_terms'} filter is recommended as an alternative.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array    $terms      Array of terms for the given object or objects.
    #// @param int[]    $object_ids Array of object IDs for which terms were retrieved.
    #// @param string[] $taxonomies Array of taxonomy names from which terms were retrieved.
    #// @param array    $args       Array of arguments for retrieving terms for the given
    #// object(s). See wp_get_object_terms() for details.
    #//
    return apply_filters("wp_get_object_terms", terms, object_ids, taxonomies, args)
# end def wp_get_object_terms
#// 
#// Add a new term to the database.
#// 
#// A non-existent term is inserted in the following sequence:
#// 1. The term is added to the term table, then related to the taxonomy.
#// 2. If everything is correct, several actions are fired.
#// 3. The 'term_id_filter' is evaluated.
#// 4. The term cache is cleaned.
#// 5. Several more actions are fired.
#// 6. An array is returned containing the term_id and term_taxonomy_id.
#// 
#// If the 'slug' argument is not empty, then it is checked to see if the term
#// is invalid. If it is not a valid, existing term, it is added and the term_id
#// is given.
#// 
#// If the taxonomy is hierarchical, and the 'parent' argument is not empty,
#// the term is inserted and the term_id will be given.
#// 
#// Error handling:
#// If $taxonomy does not exist or $term is empty,
#// a WP_Error object will be returned.
#// 
#// If the term already exists on the same hierarchical level,
#// or the term slug and name are not unique, a WP_Error object will be returned.
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @since 2.3.0
#// 
#// @param string       $term     The term name to add or update.
#// @param string       $taxonomy The taxonomy to which to add the term.
#// @param array|string $args {
#// Optional. Array or string of arguments for inserting a term.
#// 
#// @type string $alias_of    Slug of the term to make this term an alias of.
#// Default empty string. Accepts a term slug.
#// @type string $description The term description. Default empty string.
#// @type int    $parent      The id of the parent term. Default 0.
#// @type string $slug        The term slug to use. Default empty string.
#// }
#// @return array|WP_Error An array containing the `term_id` and `term_taxonomy_id`,
#// WP_Error otherwise.
#//
def wp_insert_term(term=None, taxonomy=None, args=Array(), *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if (not taxonomy_exists(taxonomy)):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_taxonomy", __("Invalid taxonomy.")))
    # end if
    #// 
    #// Filters a term before it is sanitized and inserted into the database.
    #// 
    #// @since 3.0.0
    #// 
    #// @param string|WP_Error $term     The term name to add or update, or a WP_Error object if there's an error.
    #// @param string          $taxonomy Taxonomy slug.
    #//
    term = apply_filters("pre_insert_term", term, taxonomy)
    if is_wp_error(term):
        return term
    # end if
    if php_is_int(term) and 0 == term:
        return php_new_class("WP_Error", lambda : WP_Error("invalid_term_id", __("Invalid term ID.")))
    # end if
    if "" == php_trim(term):
        return php_new_class("WP_Error", lambda : WP_Error("empty_term_name", __("A name is required for this term.")))
    # end if
    defaults = Array({"alias_of": "", "description": "", "parent": 0, "slug": ""})
    args = wp_parse_args(args, defaults)
    if args["parent"] > 0 and (not term_exists(php_int(args["parent"]))):
        return php_new_class("WP_Error", lambda : WP_Error("missing_parent", __("Parent term does not exist.")))
    # end if
    args["name"] = term
    args["taxonomy"] = taxonomy
    #// Coerce null description to strings, to avoid database errors.
    args["description"] = php_str(args["description"])
    args = sanitize_term(args, taxonomy, "db")
    #// expected_slashed ($name)
    name = wp_unslash(args["name"])
    description = wp_unslash(args["description"])
    parent = php_int(args["parent"])
    slug_provided = (not php_empty(lambda : args["slug"]))
    if (not slug_provided):
        slug = sanitize_title(name)
    else:
        slug = args["slug"]
    # end if
    term_group = 0
    if args["alias_of"]:
        alias = get_term_by("slug", args["alias_of"], taxonomy)
        if (not php_empty(lambda : alias.term_group)):
            #// The alias we want is already in a group, so let's use that one.
            term_group = alias.term_group
        elif (not php_empty(lambda : alias.term_id)):
            #// 
            #// The alias is not in a group, so we create a new one
            #// and add the alias to it.
            #//
            term_group = wpdb.get_var(str("SELECT MAX(term_group) FROM ") + str(wpdb.terms)) + 1
            wp_update_term(alias.term_id, taxonomy, Array({"term_group": term_group}))
        # end if
    # end if
    #// 
    #// Prevent the creation of terms with duplicate names at the same level of a taxonomy hierarchy,
    #// unless a unique slug has been explicitly provided.
    #//
    name_matches = get_terms(Array({"taxonomy": taxonomy, "name": name, "hide_empty": False, "parent": args["parent"], "update_term_meta_cache": False}))
    #// 
    #// The `name` match in `get_terms()` doesn't differentiate accented characters,
    #// so we do a stricter comparison here.
    #//
    name_match = None
    if name_matches:
        for _match in name_matches:
            if php_strtolower(name) == php_strtolower(_match.name):
                name_match = _match
                break
            # end if
        # end for
    # end if
    if name_match:
        slug_match = get_term_by("slug", slug, taxonomy)
        if (not slug_provided) or name_match.slug == slug or slug_match:
            if is_taxonomy_hierarchical(taxonomy):
                siblings = get_terms(Array({"taxonomy": taxonomy, "get": "all", "parent": parent, "update_term_meta_cache": False}))
                existing_term = None
                if (not slug_provided) or name_match.slug == slug and php_in_array(name, wp_list_pluck(siblings, "name")):
                    existing_term = name_match
                elif slug_match and php_in_array(slug, wp_list_pluck(siblings, "slug")):
                    existing_term = slug_match
                # end if
                if existing_term:
                    return php_new_class("WP_Error", lambda : WP_Error("term_exists", __("A term with the name provided already exists with this parent."), existing_term.term_id))
                # end if
            else:
                return php_new_class("WP_Error", lambda : WP_Error("term_exists", __("A term with the name provided already exists in this taxonomy."), name_match.term_id))
            # end if
        # end if
    # end if
    slug = wp_unique_term_slug(slug, args)
    data = compact("name", "slug", "term_group")
    #// 
    #// Filters term data before it is inserted into the database.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array  $data     Term data to be inserted.
    #// @param string $taxonomy Taxonomy slug.
    #// @param array  $args     Arguments passed to wp_insert_term().
    #//
    data = apply_filters("wp_insert_term_data", data, taxonomy, args)
    if False == wpdb.insert(wpdb.terms, data):
        return php_new_class("WP_Error", lambda : WP_Error("db_insert_error", __("Could not insert term into the database."), wpdb.last_error))
    # end if
    term_id = php_int(wpdb.insert_id)
    #// Seems unreachable. However, is used in the case that a term name is provided, which sanitizes to an empty string.
    if php_empty(lambda : slug):
        slug = sanitize_title(slug, term_id)
        #// This action is documented in wp-includes/taxonomy.php
        do_action("edit_terms", term_id, taxonomy)
        wpdb.update(wpdb.terms, compact("slug"), compact("term_id"))
        #// This action is documented in wp-includes/taxonomy.php
        do_action("edited_terms", term_id, taxonomy)
    # end if
    tt_id = wpdb.get_var(wpdb.prepare(str("SELECT tt.term_taxonomy_id FROM ") + str(wpdb.term_taxonomy) + str(" AS tt INNER JOIN ") + str(wpdb.terms) + str(" AS t ON tt.term_id = t.term_id WHERE tt.taxonomy = %s AND t.term_id = %d"), taxonomy, term_id))
    if (not php_empty(lambda : tt_id)):
        return Array({"term_id": term_id, "term_taxonomy_id": tt_id})
    # end if
    if False == wpdb.insert(wpdb.term_taxonomy, compact("term_id", "taxonomy", "description", "parent") + Array({"count": 0})):
        return php_new_class("WP_Error", lambda : WP_Error("db_insert_error", __("Could not insert term taxonomy into the database."), wpdb.last_error))
    # end if
    tt_id = php_int(wpdb.insert_id)
    #// 
    #// Sanity check: if we just created a term with the same parent + taxonomy + slug but a higher term_id than
    #// an existing term, then we have unwittingly created a duplicate term. Delete the dupe, and use the term_id
    #// and term_taxonomy_id of the older term instead. Then return out of the function so that the "create" hooks
    #// are not fired.
    #//
    duplicate_term = wpdb.get_row(wpdb.prepare(str("SELECT t.term_id, t.slug, tt.term_taxonomy_id, tt.taxonomy FROM ") + str(wpdb.terms) + str(" t INNER JOIN ") + str(wpdb.term_taxonomy) + str(" tt ON ( tt.term_id = t.term_id ) WHERE t.slug = %s AND tt.parent = %d AND tt.taxonomy = %s AND t.term_id < %d AND tt.term_taxonomy_id != %d"), slug, parent, taxonomy, term_id, tt_id))
    #// 
    #// Filters the duplicate term check that takes place during term creation.
    #// 
    #// Term parent+taxonomy+slug combinations are meant to be unique, and wp_insert_term()
    #// performs a last-minute confirmation of this uniqueness before allowing a new term
    #// to be created. Plugins with different uniqueness requirements may use this filter
    #// to bypass or modify the duplicate-term check.
    #// 
    #// @since 5.1.0
    #// 
    #// @param object $duplicate_term Duplicate term row from terms table, if found.
    #// @param string $term           Term being inserted.
    #// @param string $taxonomy       Taxonomy name.
    #// @param array  $args           Term arguments passed to the function.
    #// @param int    $tt_id          term_taxonomy_id for the newly created term.
    #//
    duplicate_term = apply_filters("wp_insert_term_duplicate_term_check", duplicate_term, term, taxonomy, args, tt_id)
    if duplicate_term:
        wpdb.delete(wpdb.terms, Array({"term_id": term_id}))
        wpdb.delete(wpdb.term_taxonomy, Array({"term_taxonomy_id": tt_id}))
        term_id = php_int(duplicate_term.term_id)
        tt_id = php_int(duplicate_term.term_taxonomy_id)
        clean_term_cache(term_id, taxonomy)
        return Array({"term_id": term_id, "term_taxonomy_id": tt_id})
    # end if
    #// 
    #// Fires immediately after a new term is created, before the term cache is cleaned.
    #// 
    #// @since 2.3.0
    #// 
    #// @param int    $term_id  Term ID.
    #// @param int    $tt_id    Term taxonomy ID.
    #// @param string $taxonomy Taxonomy slug.
    #//
    do_action("create_term", term_id, tt_id, taxonomy)
    #// 
    #// Fires after a new term is created for a specific taxonomy.
    #// 
    #// The dynamic portion of the hook name, `$taxonomy`, refers
    #// to the slug of the taxonomy the term was created for.
    #// 
    #// @since 2.3.0
    #// 
    #// @param int $term_id Term ID.
    #// @param int $tt_id   Term taxonomy ID.
    #//
    do_action(str("create_") + str(taxonomy), term_id, tt_id)
    #// 
    #// Filters the term ID after a new term is created.
    #// 
    #// @since 2.3.0
    #// 
    #// @param int $term_id Term ID.
    #// @param int $tt_id   Taxonomy term ID.
    #//
    term_id = apply_filters("term_id_filter", term_id, tt_id)
    clean_term_cache(term_id, taxonomy)
    #// 
    #// Fires after a new term is created, and after the term cache has been cleaned.
    #// 
    #// @since 2.3.0
    #// 
    #// @param int    $term_id  Term ID.
    #// @param int    $tt_id    Term taxonomy ID.
    #// @param string $taxonomy Taxonomy slug.
    #//
    do_action("created_term", term_id, tt_id, taxonomy)
    #// 
    #// Fires after a new term in a specific taxonomy is created, and after the term
    #// cache has been cleaned.
    #// 
    #// The dynamic portion of the hook name, `$taxonomy`, refers to the taxonomy slug.
    #// 
    #// @since 2.3.0
    #// 
    #// @param int $term_id Term ID.
    #// @param int $tt_id   Term taxonomy ID.
    #//
    do_action(str("created_") + str(taxonomy), term_id, tt_id)
    return Array({"term_id": term_id, "term_taxonomy_id": tt_id})
# end def wp_insert_term
#// 
#// Create Term and Taxonomy Relationships.
#// 
#// Relates an object (post, link etc) to a term and taxonomy type. Creates the
#// term and taxonomy relationship if it doesn't already exist. Creates a term if
#// it doesn't exist (using the slug).
#// 
#// A relationship means that the term is grouped in or belongs to the taxonomy.
#// A term has no meaning until it is given context by defining which taxonomy it
#// exists under.
#// 
#// @since 2.3.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int              $object_id The object to relate to.
#// @param string|int|array $terms     A single term slug, single term id, or array of either term slugs or ids.
#// Will replace all existing related terms in this taxonomy. Passing an
#// empty value will remove all related terms.
#// @param string           $taxonomy  The context in which to relate the term to the object.
#// @param bool             $append    Optional. If false will delete difference of terms. Default false.
#// @return array|WP_Error Term taxonomy IDs of the affected terms or WP_Error on failure.
#//
def wp_set_object_terms(object_id=None, terms=None, taxonomy=None, append=False, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    object_id = php_int(object_id)
    if (not taxonomy_exists(taxonomy)):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_taxonomy", __("Invalid taxonomy.")))
    # end if
    if (not php_is_array(terms)):
        terms = Array(terms)
    # end if
    if (not append):
        old_tt_ids = wp_get_object_terms(object_id, taxonomy, Array({"fields": "tt_ids", "orderby": "none", "update_term_meta_cache": False}))
    else:
        old_tt_ids = Array()
    # end if
    tt_ids = Array()
    term_ids = Array()
    new_tt_ids = Array()
    for term in terms:
        if "" == php_trim(term):
            continue
        # end if
        term_info = term_exists(term, taxonomy)
        if (not term_info):
            #// Skip if a non-existent term ID is passed.
            if php_is_int(term):
                continue
            # end if
            term_info = wp_insert_term(term, taxonomy)
        # end if
        if is_wp_error(term_info):
            return term_info
        # end if
        term_ids[-1] = term_info["term_id"]
        tt_id = term_info["term_taxonomy_id"]
        tt_ids[-1] = tt_id
        if wpdb.get_var(wpdb.prepare(str("SELECT term_taxonomy_id FROM ") + str(wpdb.term_relationships) + str(" WHERE object_id = %d AND term_taxonomy_id = %d"), object_id, tt_id)):
            continue
        # end if
        #// 
        #// Fires immediately before an object-term relationship is added.
        #// 
        #// @since 2.9.0
        #// @since 4.7.0 Added the `$taxonomy` parameter.
        #// 
        #// @param int    $object_id Object ID.
        #// @param int    $tt_id     Term taxonomy ID.
        #// @param string $taxonomy  Taxonomy slug.
        #//
        do_action("add_term_relationship", object_id, tt_id, taxonomy)
        wpdb.insert(wpdb.term_relationships, Array({"object_id": object_id, "term_taxonomy_id": tt_id}))
        #// 
        #// Fires immediately after an object-term relationship is added.
        #// 
        #// @since 2.9.0
        #// @since 4.7.0 Added the `$taxonomy` parameter.
        #// 
        #// @param int    $object_id Object ID.
        #// @param int    $tt_id     Term taxonomy ID.
        #// @param string $taxonomy  Taxonomy slug.
        #//
        do_action("added_term_relationship", object_id, tt_id, taxonomy)
        new_tt_ids[-1] = tt_id
    # end for
    if new_tt_ids:
        wp_update_term_count(new_tt_ids, taxonomy)
    # end if
    if (not append):
        delete_tt_ids = php_array_diff(old_tt_ids, tt_ids)
        if delete_tt_ids:
            in_delete_tt_ids = "'" + php_implode("', '", delete_tt_ids) + "'"
            delete_term_ids = wpdb.get_col(wpdb.prepare(str("SELECT tt.term_id FROM ") + str(wpdb.term_taxonomy) + str(" AS tt WHERE tt.taxonomy = %s AND tt.term_taxonomy_id IN (") + str(in_delete_tt_ids) + str(")"), taxonomy))
            delete_term_ids = php_array_map("intval", delete_term_ids)
            remove = wp_remove_object_terms(object_id, delete_term_ids, taxonomy)
            if is_wp_error(remove):
                return remove
            # end if
        # end if
    # end if
    t = get_taxonomy(taxonomy)
    if (not append) and (php_isset(lambda : t.sort)) and t.sort:
        values = Array()
        term_order = 0
        final_tt_ids = wp_get_object_terms(object_id, taxonomy, Array({"fields": "tt_ids", "update_term_meta_cache": False}))
        for tt_id in tt_ids:
            if php_in_array(tt_id, final_tt_ids):
                term_order += 1
                values[-1] = wpdb.prepare("(%d, %d, %d)", object_id, tt_id, term_order)
            # end if
        # end for
        if values:
            if False == wpdb.query(str("INSERT INTO ") + str(wpdb.term_relationships) + str(" (object_id, term_taxonomy_id, term_order) VALUES ") + join(",", values) + " ON DUPLICATE KEY UPDATE term_order = VALUES(term_order)"):
                return php_new_class("WP_Error", lambda : WP_Error("db_insert_error", __("Could not insert term relationship into the database."), wpdb.last_error))
            # end if
        # end if
    # end if
    wp_cache_delete(object_id, taxonomy + "_relationships")
    wp_cache_delete("last_changed", "terms")
    #// 
    #// Fires after an object's terms have been set.
    #// 
    #// @since 2.8.0
    #// 
    #// @param int    $object_id  Object ID.
    #// @param array  $terms      An array of object terms.
    #// @param array  $tt_ids     An array of term taxonomy IDs.
    #// @param string $taxonomy   Taxonomy slug.
    #// @param bool   $append     Whether to append new terms to the old terms.
    #// @param array  $old_tt_ids Old array of term taxonomy IDs.
    #//
    do_action("set_object_terms", object_id, terms, tt_ids, taxonomy, append, old_tt_ids)
    return tt_ids
# end def wp_set_object_terms
#// 
#// Add term(s) associated with a given object.
#// 
#// @since 3.6.0
#// 
#// @param int              $object_id The ID of the object to which the terms will be added.
#// @param string|int|array $terms     The slug(s) or ID(s) of the term(s) to add.
#// @param array|string     $taxonomy  Taxonomy name.
#// @return array|WP_Error Term taxonomy IDs of the affected terms.
#//
def wp_add_object_terms(object_id=None, terms=None, taxonomy=None, *args_):
    
    return wp_set_object_terms(object_id, terms, taxonomy, True)
# end def wp_add_object_terms
#// 
#// Remove term(s) associated with a given object.
#// 
#// @since 3.6.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int              $object_id The ID of the object from which the terms will be removed.
#// @param string|int|array $terms     The slug(s) or ID(s) of the term(s) to remove.
#// @param array|string     $taxonomy  Taxonomy name.
#// @return bool|WP_Error True on success, false or WP_Error on failure.
#//
def wp_remove_object_terms(object_id=None, terms=None, taxonomy=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    object_id = php_int(object_id)
    if (not taxonomy_exists(taxonomy)):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_taxonomy", __("Invalid taxonomy.")))
    # end if
    if (not php_is_array(terms)):
        terms = Array(terms)
    # end if
    tt_ids = Array()
    for term in terms:
        if "" == php_trim(term):
            continue
        # end if
        term_info = term_exists(term, taxonomy)
        if (not term_info):
            #// Skip if a non-existent term ID is passed.
            if php_is_int(term):
                continue
            # end if
        # end if
        if is_wp_error(term_info):
            return term_info
        # end if
        tt_ids[-1] = term_info["term_taxonomy_id"]
    # end for
    if tt_ids:
        in_tt_ids = "'" + php_implode("', '", tt_ids) + "'"
        #// 
        #// Fires immediately before an object-term relationship is deleted.
        #// 
        #// @since 2.9.0
        #// @since 4.7.0 Added the `$taxonomy` parameter.
        #// 
        #// @param int   $object_id Object ID.
        #// @param array $tt_ids    An array of term taxonomy IDs.
        #// @param string $taxonomy  Taxonomy slug.
        #//
        do_action("delete_term_relationships", object_id, tt_ids, taxonomy)
        deleted = wpdb.query(wpdb.prepare(str("DELETE FROM ") + str(wpdb.term_relationships) + str(" WHERE object_id = %d AND term_taxonomy_id IN (") + str(in_tt_ids) + str(")"), object_id))
        wp_cache_delete(object_id, taxonomy + "_relationships")
        wp_cache_delete("last_changed", "terms")
        #// 
        #// Fires immediately after an object-term relationship is deleted.
        #// 
        #// @since 2.9.0
        #// @since 4.7.0 Added the `$taxonomy` parameter.
        #// 
        #// @param int    $object_id Object ID.
        #// @param array  $tt_ids    An array of term taxonomy IDs.
        #// @param string $taxonomy  Taxonomy slug.
        #//
        do_action("deleted_term_relationships", object_id, tt_ids, taxonomy)
        wp_update_term_count(tt_ids, taxonomy)
        return php_bool(deleted)
    # end if
    return False
# end def wp_remove_object_terms
#// 
#// Will make slug unique, if it isn't already.
#// 
#// The `$slug` has to be unique global to every taxonomy, meaning that one
#// taxonomy term can't have a matching slug with another taxonomy term. Each
#// slug has to be globally unique for every taxonomy.
#// 
#// The way this works is that if the taxonomy that the term belongs to is
#// hierarchical and has a parent, it will append that parent to the $slug.
#// 
#// If that still doesn't return a unique slug, then it tries to append a number
#// until it finds a number that is truly unique.
#// 
#// The only purpose for `$term` is for appending a parent, if one exists.
#// 
#// @since 2.3.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param string $slug The string that will be tried for a unique slug.
#// @param object $term The term object that the `$slug` will belong to.
#// @return string Will return a true unique slug.
#//
def wp_unique_term_slug(slug=None, term=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    needs_suffix = True
    original_slug = slug
    #// As of 4.1, duplicate slugs are allowed as long as they're in different taxonomies.
    if (not term_exists(slug)) or get_option("db_version") >= 30133 and (not get_term_by("slug", slug, term.taxonomy)):
        needs_suffix = False
    # end if
    #// 
    #// If the taxonomy supports hierarchy and the term has a parent, make the slug unique
    #// by incorporating parent slugs.
    #//
    parent_suffix = ""
    if needs_suffix and is_taxonomy_hierarchical(term.taxonomy) and (not php_empty(lambda : term.parent)):
        the_parent = term.parent
        while True:
            
            if not ((not php_empty(lambda : the_parent))):
                break
            # end if
            parent_term = get_term(the_parent, term.taxonomy)
            if is_wp_error(parent_term) or php_empty(lambda : parent_term):
                break
            # end if
            parent_suffix += "-" + parent_term.slug
            if (not term_exists(slug + parent_suffix)):
                break
            # end if
            if php_empty(lambda : parent_term.parent):
                break
            # end if
            the_parent = parent_term.parent
        # end while
    # end if
    #// If we didn't get a unique slug, try appending a number to make it unique.
    #// 
    #// Filters whether the proposed unique term slug is bad.
    #// 
    #// @since 4.3.0
    #// 
    #// @param bool   $needs_suffix Whether the slug needs to be made unique with a suffix.
    #// @param string $slug         The slug.
    #// @param object $term         Term object.
    #//
    if apply_filters("wp_unique_term_slug_is_bad_slug", needs_suffix, slug, term):
        if parent_suffix:
            slug += parent_suffix
        # end if
        if (not php_empty(lambda : term.term_id)):
            query = wpdb.prepare(str("SELECT slug FROM ") + str(wpdb.terms) + str(" WHERE slug = %s AND term_id != %d"), slug, term.term_id)
        else:
            query = wpdb.prepare(str("SELECT slug FROM ") + str(wpdb.terms) + str(" WHERE slug = %s"), slug)
        # end if
        if wpdb.get_var(query):
            #// phpcs:ignore WordPress.DB.PreparedSQL.NotPrepared
            num = 2
            while True:
                alt_slug = slug + str("-") + str(num)
                num += 1
                slug_check = wpdb.get_var(wpdb.prepare(str("SELECT slug FROM ") + str(wpdb.terms) + str(" WHERE slug = %s"), alt_slug))
                
                if slug_check:
                    break
                # end if
            # end while
            slug = alt_slug
        # end if
    # end if
    #// 
    #// Filters the unique term slug.
    #// 
    #// @since 4.3.0
    #// 
    #// @param string $slug          Unique term slug.
    #// @param object $term          Term object.
    #// @param string $original_slug Slug originally passed to the function for testing.
    #//
    return apply_filters("wp_unique_term_slug", slug, term, original_slug)
# end def wp_unique_term_slug
#// 
#// Update term based on arguments provided.
#// 
#// The $args will indiscriminately override all values with the same field name.
#// Care must be taken to not override important information need to update or
#// update will fail (or perhaps create a new term, neither would be acceptable).
#// 
#// Defaults will set 'alias_of', 'description', 'parent', and 'slug' if not
#// defined in $args already.
#// 
#// 'alias_of' will create a term group, if it doesn't already exist, and update
#// it for the $term.
#// 
#// If the 'slug' argument in $args is missing, then the 'name' in $args will be
#// used. It should also be noted that if you set 'slug' and it isn't unique then
#// a WP_Error will be passed back. If you don't pass any slug, then a unique one
#// will be created for you.
#// 
#// For what can be overrode in `$args`, check the term scheme can contain and stay
#// away from the term keys.
#// 
#// @since 2.3.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int          $term_id  The ID of the term
#// @param string       $taxonomy The context in which to relate the term to the object.
#// @param array|string $args     Optional. Array of get_terms() arguments. Default empty array.
#// @return array|WP_Error Returns Term ID and Taxonomy Term ID
#//
def wp_update_term(term_id=None, taxonomy=None, args=Array(), *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if (not taxonomy_exists(taxonomy)):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_taxonomy", __("Invalid taxonomy.")))
    # end if
    term_id = php_int(term_id)
    #// First, get all of the original args.
    term = get_term(term_id, taxonomy)
    if is_wp_error(term):
        return term
    # end if
    if (not term):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_term", __("Empty Term.")))
    # end if
    term = term.data
    #// Escape data pulled from DB.
    term = wp_slash(term)
    #// Merge old and new args with new args overwriting old ones.
    args = php_array_merge(term, args)
    defaults = Array({"alias_of": "", "description": "", "parent": 0, "slug": ""})
    args = wp_parse_args(args, defaults)
    args = sanitize_term(args, taxonomy, "db")
    parsed_args = args
    #// expected_slashed ($name)
    name = wp_unslash(args["name"])
    description = wp_unslash(args["description"])
    parsed_args["name"] = name
    parsed_args["description"] = description
    if "" == php_trim(name):
        return php_new_class("WP_Error", lambda : WP_Error("empty_term_name", __("A name is required for this term.")))
    # end if
    if parsed_args["parent"] > 0 and (not term_exists(php_int(parsed_args["parent"]))):
        return php_new_class("WP_Error", lambda : WP_Error("missing_parent", __("Parent term does not exist.")))
    # end if
    empty_slug = False
    if php_empty(lambda : args["slug"]):
        empty_slug = True
        slug = sanitize_title(name)
    else:
        slug = args["slug"]
    # end if
    parsed_args["slug"] = slug
    term_group = parsed_args["term_group"] if (php_isset(lambda : parsed_args["term_group"])) else 0
    if args["alias_of"]:
        alias = get_term_by("slug", args["alias_of"], taxonomy)
        if (not php_empty(lambda : alias.term_group)):
            #// The alias we want is already in a group, so let's use that one.
            term_group = alias.term_group
        elif (not php_empty(lambda : alias.term_id)):
            #// 
            #// The alias is not in a group, so we create a new one
            #// and add the alias to it.
            #//
            term_group = wpdb.get_var(str("SELECT MAX(term_group) FROM ") + str(wpdb.terms)) + 1
            wp_update_term(alias.term_id, taxonomy, Array({"term_group": term_group}))
        # end if
        parsed_args["term_group"] = term_group
    # end if
    #// 
    #// Filters the term parent.
    #// 
    #// Hook to this filter to see if it will cause a hierarchy loop.
    #// 
    #// @since 3.1.0
    #// 
    #// @param int    $parent      ID of the parent term.
    #// @param int    $term_id     Term ID.
    #// @param string $taxonomy    Taxonomy slug.
    #// @param array  $parsed_args An array of potentially altered update arguments for the given term.
    #// @param array  $args        An array of update arguments for the given term.
    #//
    parent = php_int(apply_filters("wp_update_term_parent", args["parent"], term_id, taxonomy, parsed_args, args))
    #// Check for duplicate slug.
    duplicate = get_term_by("slug", slug, taxonomy)
    if duplicate and duplicate.term_id != term_id:
        #// If an empty slug was passed or the parent changed, reset the slug to something unique.
        #// Otherwise, bail.
        if empty_slug or parent != php_int(term["parent"]):
            slug = wp_unique_term_slug(slug, args)
        else:
            #// translators: %s: Taxonomy term slug.
            return php_new_class("WP_Error", lambda : WP_Error("duplicate_term_slug", php_sprintf(__("The slug &#8220;%s&#8221; is already in use by another term."), slug)))
        # end if
    # end if
    tt_id = php_int(wpdb.get_var(wpdb.prepare(str("SELECT tt.term_taxonomy_id FROM ") + str(wpdb.term_taxonomy) + str(" AS tt INNER JOIN ") + str(wpdb.terms) + str(" AS t ON tt.term_id = t.term_id WHERE tt.taxonomy = %s AND t.term_id = %d"), taxonomy, term_id)))
    #// Check whether this is a shared term that needs splitting.
    _term_id = _split_shared_term(term_id, tt_id)
    if (not is_wp_error(_term_id)):
        term_id = _term_id
    # end if
    #// 
    #// Fires immediately before the given terms are edited.
    #// 
    #// @since 2.9.0
    #// 
    #// @param int    $term_id  Term ID.
    #// @param string $taxonomy Taxonomy slug.
    #//
    do_action("edit_terms", term_id, taxonomy)
    data = compact("name", "slug", "term_group")
    #// 
    #// Filters term data before it is updated in the database.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array  $data     Term data to be updated.
    #// @param int    $term_id  Term ID.
    #// @param string $taxonomy Taxonomy slug.
    #// @param array  $args     Arguments passed to wp_update_term().
    #//
    data = apply_filters("wp_update_term_data", data, term_id, taxonomy, args)
    wpdb.update(wpdb.terms, data, compact("term_id"))
    if php_empty(lambda : slug):
        slug = sanitize_title(name, term_id)
        wpdb.update(wpdb.terms, compact("slug"), compact("term_id"))
    # end if
    #// 
    #// Fires immediately after the given terms are edited.
    #// 
    #// @since 2.9.0
    #// 
    #// @param int    $term_id  Term ID
    #// @param string $taxonomy Taxonomy slug.
    #//
    do_action("edited_terms", term_id, taxonomy)
    #// 
    #// Fires immediate before a term-taxonomy relationship is updated.
    #// 
    #// @since 2.9.0
    #// 
    #// @param int    $tt_id    Term taxonomy ID.
    #// @param string $taxonomy Taxonomy slug.
    #//
    do_action("edit_term_taxonomy", tt_id, taxonomy)
    wpdb.update(wpdb.term_taxonomy, compact("term_id", "taxonomy", "description", "parent"), Array({"term_taxonomy_id": tt_id}))
    #// 
    #// Fires immediately after a term-taxonomy relationship is updated.
    #// 
    #// @since 2.9.0
    #// 
    #// @param int    $tt_id    Term taxonomy ID.
    #// @param string $taxonomy Taxonomy slug.
    #//
    do_action("edited_term_taxonomy", tt_id, taxonomy)
    #// 
    #// Fires after a term has been updated, but before the term cache has been cleaned.
    #// 
    #// @since 2.3.0
    #// 
    #// @param int    $term_id  Term ID.
    #// @param int    $tt_id    Term taxonomy ID.
    #// @param string $taxonomy Taxonomy slug.
    #//
    do_action("edit_term", term_id, tt_id, taxonomy)
    #// 
    #// Fires after a term in a specific taxonomy has been updated, but before the term
    #// cache has been cleaned.
    #// 
    #// The dynamic portion of the hook name, `$taxonomy`, refers to the taxonomy slug.
    #// 
    #// @since 2.3.0
    #// 
    #// @param int $term_id Term ID.
    #// @param int $tt_id   Term taxonomy ID.
    #//
    do_action(str("edit_") + str(taxonomy), term_id, tt_id)
    #// This filter is documented in wp-includes/taxonomy.php
    term_id = apply_filters("term_id_filter", term_id, tt_id)
    clean_term_cache(term_id, taxonomy)
    #// 
    #// Fires after a term has been updated, and the term cache has been cleaned.
    #// 
    #// @since 2.3.0
    #// 
    #// @param int    $term_id  Term ID.
    #// @param int    $tt_id    Term taxonomy ID.
    #// @param string $taxonomy Taxonomy slug.
    #//
    do_action("edited_term", term_id, tt_id, taxonomy)
    #// 
    #// Fires after a term for a specific taxonomy has been updated, and the term
    #// cache has been cleaned.
    #// 
    #// The dynamic portion of the hook name, `$taxonomy`, refers to the taxonomy slug.
    #// 
    #// @since 2.3.0
    #// 
    #// @param int $term_id Term ID.
    #// @param int $tt_id   Term taxonomy ID.
    #//
    do_action(str("edited_") + str(taxonomy), term_id, tt_id)
    return Array({"term_id": term_id, "term_taxonomy_id": tt_id})
# end def wp_update_term
#// 
#// Enable or disable term counting.
#// 
#// @since 2.5.0
#// 
#// @staticvar bool $_defer
#// 
#// @param bool $defer Optional. Enable if true, disable if false.
#// @return bool Whether term counting is enabled or disabled.
#//
def wp_defer_term_counting(defer=None, *args_):
    
    _defer = False
    if php_is_bool(defer):
        _defer = defer
        #// Flush any deferred counts.
        if (not defer):
            wp_update_term_count(None, None, True)
        # end if
    # end if
    return _defer
# end def wp_defer_term_counting
#// 
#// Updates the amount of terms in taxonomy.
#// 
#// If there is a taxonomy callback applied, then it will be called for updating
#// the count.
#// 
#// The default action is to count what the amount of terms have the relationship
#// of term ID. Once that is done, then update the database.
#// 
#// @since 2.3.0
#// 
#// @staticvar array $_deferred
#// 
#// @param int|array $terms       The term_taxonomy_id of the terms.
#// @param string    $taxonomy    The context of the term.
#// @param bool      $do_deferred Whether to flush the deferred term counts too. Default false.
#// @return bool If no terms will return false, and if successful will return true.
#//
def wp_update_term_count(terms=None, taxonomy=None, do_deferred=False, *args_):
    
    _deferred = Array()
    if do_deferred:
        for tax in php_array_keys(_deferred):
            wp_update_term_count_now(_deferred[tax], tax)
            _deferred[tax] = None
        # end for
    # end if
    if php_empty(lambda : terms):
        return False
    # end if
    if (not php_is_array(terms)):
        terms = Array(terms)
    # end if
    if wp_defer_term_counting():
        if (not (php_isset(lambda : _deferred[taxonomy]))):
            _deferred[taxonomy] = Array()
        # end if
        _deferred[taxonomy] = array_unique(php_array_merge(_deferred[taxonomy], terms))
        return True
    # end if
    return wp_update_term_count_now(terms, taxonomy)
# end def wp_update_term_count
#// 
#// Perform term count update immediately.
#// 
#// @since 2.5.0
#// 
#// @param array  $terms    The term_taxonomy_id of terms to update.
#// @param string $taxonomy The context of the term.
#// @return true Always true when complete.
#//
def wp_update_term_count_now(terms=None, taxonomy=None, *args_):
    
    terms = php_array_map("intval", terms)
    taxonomy = get_taxonomy(taxonomy)
    if (not php_empty(lambda : taxonomy.update_count_callback)):
        php_call_user_func(taxonomy.update_count_callback, terms, taxonomy)
    else:
        object_types = taxonomy.object_type
        for object_type in object_types:
            if 0 == php_strpos(object_type, "attachment:"):
                object_type = php_explode(":", object_type)
            # end if
        # end for
        if php_array_filter(object_types, "post_type_exists") == object_types:
            #// Only post types are attached to this taxonomy.
            _update_post_term_count(terms, taxonomy)
        else:
            #// Default count updater.
            _update_generic_term_count(terms, taxonomy)
        # end if
    # end if
    clean_term_cache(terms, "", False)
    return True
# end def wp_update_term_count_now
#// 
#// Cache.
#// 
#// 
#// Removes the taxonomy relationship to terms from the cache.
#// 
#// Will remove the entire taxonomy relationship containing term `$object_id`. The
#// term IDs have to exist within the taxonomy `$object_type` for the deletion to
#// take place.
#// 
#// @since 2.3.0
#// 
#// @global bool $_wp_suspend_cache_invalidation
#// 
#// @see get_object_taxonomies() for more on $object_type.
#// 
#// @param int|array    $object_ids  Single or list of term object ID(s).
#// @param array|string $object_type The taxonomy object type.
#//
def clean_object_term_cache(object_ids=None, object_type=None, *args_):
    
    global _wp_suspend_cache_invalidation
    php_check_if_defined("_wp_suspend_cache_invalidation")
    if (not php_empty(lambda : _wp_suspend_cache_invalidation)):
        return
    # end if
    if (not php_is_array(object_ids)):
        object_ids = Array(object_ids)
    # end if
    taxonomies = get_object_taxonomies(object_type)
    for id in object_ids:
        for taxonomy in taxonomies:
            wp_cache_delete(id, str(taxonomy) + str("_relationships"))
        # end for
    # end for
    #// 
    #// Fires after the object term cache has been cleaned.
    #// 
    #// @since 2.5.0
    #// 
    #// @param array  $object_ids An array of object IDs.
    #// @param string $object_type Object type.
    #//
    do_action("clean_object_term_cache", object_ids, object_type)
# end def clean_object_term_cache
#// 
#// Will remove all of the term ids from the cache.
#// 
#// @since 2.3.0
#// 
#// @global wpdb $wpdb                           WordPress database abstraction object.
#// @global bool $_wp_suspend_cache_invalidation
#// 
#// @param int|int[] $ids            Single or array of term IDs.
#// @param string    $taxonomy       Optional. Taxonomy slug. Can be empty, in which case the taxonomies of the passed
#// term IDs will be used. Default empty.
#// @param bool      $clean_taxonomy Optional. Whether to clean taxonomy wide caches (true), or just individual
#// term object caches (false). Default true.
#//
def clean_term_cache(ids=None, taxonomy="", clean_taxonomy=True, *args_):
    
    global wpdb,_wp_suspend_cache_invalidation
    php_check_if_defined("wpdb","_wp_suspend_cache_invalidation")
    if (not php_empty(lambda : _wp_suspend_cache_invalidation)):
        return
    # end if
    if (not php_is_array(ids)):
        ids = Array(ids)
    # end if
    taxonomies = Array()
    #// If no taxonomy, assume tt_ids.
    if php_empty(lambda : taxonomy):
        tt_ids = php_array_map("intval", ids)
        tt_ids = php_implode(", ", tt_ids)
        terms = wpdb.get_results(str("SELECT term_id, taxonomy FROM ") + str(wpdb.term_taxonomy) + str(" WHERE term_taxonomy_id IN (") + str(tt_ids) + str(")"))
        ids = Array()
        for term in terms:
            taxonomies[-1] = term.taxonomy
            ids[-1] = term.term_id
            wp_cache_delete(term.term_id, "terms")
        # end for
        taxonomies = array_unique(taxonomies)
    else:
        taxonomies = Array(taxonomy)
        for taxonomy in taxonomies:
            for id in ids:
                wp_cache_delete(id, "terms")
            # end for
        # end for
    # end if
    for taxonomy in taxonomies:
        if clean_taxonomy:
            clean_taxonomy_cache(taxonomy)
        # end if
        #// 
        #// Fires once after each taxonomy's term cache has been cleaned.
        #// 
        #// @since 2.5.0
        #// @since 4.5.0 Added the `$clean_taxonomy` parameter.
        #// 
        #// @param array  $ids            An array of term IDs.
        #// @param string $taxonomy       Taxonomy slug.
        #// @param bool   $clean_taxonomy Whether or not to clean taxonomy-wide caches
        #//
        do_action("clean_term_cache", ids, taxonomy, clean_taxonomy)
    # end for
    wp_cache_set("last_changed", php_microtime(), "terms")
# end def clean_term_cache
#// 
#// Clean the caches for a taxonomy.
#// 
#// @since 4.9.0
#// 
#// @param string $taxonomy Taxonomy slug.
#//
def clean_taxonomy_cache(taxonomy=None, *args_):
    
    wp_cache_delete("all_ids", taxonomy)
    wp_cache_delete("get", taxonomy)
    #// Regenerate cached hierarchy.
    delete_option(str(taxonomy) + str("_children"))
    _get_term_hierarchy(taxonomy)
    #// 
    #// Fires after a taxonomy's caches have been cleaned.
    #// 
    #// @since 4.9.0
    #// 
    #// @param string $taxonomy Taxonomy slug.
    #//
    do_action("clean_taxonomy_cache", taxonomy)
# end def clean_taxonomy_cache
#// 
#// Retrieves the cached term objects for the given object ID.
#// 
#// Upstream functions (like get_the_terms() and is_object_in_term()) are
#// responsible for populating the object-term relationship cache. The current
#// function only fetches relationship data that is already in the cache.
#// 
#// @since 2.3.0
#// @since 4.7.0 Returns a `WP_Error` object if there's an error with
#// any of the matched terms.
#// 
#// @param int    $id       Term object ID, for example a post, comment, or user ID.
#// @param string $taxonomy Taxonomy name.
#// @return bool|WP_Term[]|WP_Error Array of `WP_Term` objects, if cached.
#// False if cache is empty for `$taxonomy` and `$id`.
#// WP_Error if get_term() returns an error object for any term.
#//
def get_object_term_cache(id=None, taxonomy=None, *args_):
    
    _term_ids = wp_cache_get(id, str(taxonomy) + str("_relationships"))
    #// We leave the priming of relationship caches to upstream functions.
    if False == _term_ids:
        return False
    # end if
    #// Backward compatibility for if a plugin is putting objects into the cache, rather than IDs.
    term_ids = Array()
    for term_id in _term_ids:
        if php_is_numeric(term_id):
            term_ids[-1] = php_intval(term_id)
        elif (php_isset(lambda : term_id.term_id)):
            term_ids[-1] = php_intval(term_id.term_id)
        # end if
    # end for
    #// Fill the term objects.
    _prime_term_caches(term_ids)
    terms = Array()
    for term_id in term_ids:
        term = get_term(term_id, taxonomy)
        if is_wp_error(term):
            return term
        # end if
        terms[-1] = term
    # end for
    return terms
# end def get_object_term_cache
#// 
#// Updates the cache for the given term object ID(s).
#// 
#// Note: Due to performance concerns, great care should be taken to only update
#// term caches when necessary. Processing time can increase exponentially depending
#// on both the number of passed term IDs and the number of taxonomies those terms
#// belong to.
#// 
#// Caches will only be updated for terms not already cached.
#// 
#// @since 2.3.0
#// 
#// @param string|int[]    $object_ids  Comma-separated list or array of term object IDs.
#// @param string|string[] $object_type The taxonomy object type or array of the same.
#// @return void|false False if all of the terms in `$object_ids` are already cached.
#//
def update_object_term_cache(object_ids=None, object_type=None, *args_):
    
    if php_empty(lambda : object_ids):
        return
    # end if
    if (not php_is_array(object_ids)):
        object_ids = php_explode(",", object_ids)
    # end if
    object_ids = php_array_map("intval", object_ids)
    taxonomies = get_object_taxonomies(object_type)
    ids = Array()
    for id in object_ids:
        for taxonomy in taxonomies:
            if False == wp_cache_get(id, str(taxonomy) + str("_relationships")):
                ids[-1] = id
                break
            # end if
        # end for
    # end for
    if php_empty(lambda : ids):
        return False
    # end if
    terms = wp_get_object_terms(ids, taxonomies, Array({"fields": "all_with_object_id", "orderby": "name", "update_term_meta_cache": False}))
    object_terms = Array()
    for term in terms:
        object_terms[term.object_id][term.taxonomy][-1] = term.term_id
    # end for
    for id in ids:
        for taxonomy in taxonomies:
            if (not (php_isset(lambda : object_terms[id][taxonomy]))):
                if (not (php_isset(lambda : object_terms[id]))):
                    object_terms[id] = Array()
                # end if
                object_terms[id][taxonomy] = Array()
            # end if
        # end for
    # end for
    for id,value in object_terms:
        for taxonomy,terms in value:
            wp_cache_add(id, terms, str(taxonomy) + str("_relationships"))
        # end for
    # end for
# end def update_object_term_cache
#// 
#// Updates Terms to Taxonomy in cache.
#// 
#// @since 2.3.0
#// 
#// @param WP_Term[] $terms    Array of term objects to change.
#// @param string    $taxonomy Not used.
#//
def update_term_cache(terms=None, taxonomy="", *args_):
    
    for term in terms:
        #// Create a copy in case the array was passed by reference.
        _term = copy.deepcopy(term)
        _term.object_id = None
        wp_cache_add(term.term_id, _term, "terms")
    # end for
# end def update_term_cache
#// 
#// Private.
#// 
#// 
#// Retrieves children of taxonomy as Term IDs.
#// 
#// @access private
#// @since 2.3.0
#// 
#// @param string $taxonomy Taxonomy name.
#// @return array Empty if $taxonomy isn't hierarchical or returns children as Term IDs.
#//
def _get_term_hierarchy(taxonomy=None, *args_):
    
    if (not is_taxonomy_hierarchical(taxonomy)):
        return Array()
    # end if
    children = get_option(str(taxonomy) + str("_children"))
    if php_is_array(children):
        return children
    # end if
    children = Array()
    terms = get_terms(Array({"taxonomy": taxonomy, "get": "all", "orderby": "id", "fields": "id=>parent", "update_term_meta_cache": False}))
    for term_id,parent in terms:
        if parent > 0:
            children[parent][-1] = term_id
        # end if
    # end for
    update_option(str(taxonomy) + str("_children"), children)
    return children
# end def _get_term_hierarchy
#// 
#// Get the subset of $terms that are descendants of $term_id.
#// 
#// If `$terms` is an array of objects, then _get_term_children() returns an array of objects.
#// If `$terms` is an array of IDs, then _get_term_children() returns an array of IDs.
#// 
#// @access private
#// @since 2.3.0
#// 
#// @param int    $term_id   The ancestor term: all returned terms should be descendants of `$term_id`.
#// @param array  $terms     The set of terms - either an array of term objects or term IDs - from which those that
#// are descendants of $term_id will be chosen.
#// @param string $taxonomy  The taxonomy which determines the hierarchy of the terms.
#// @param array  $ancestors Optional. Term ancestors that have already been identified. Passed by reference, to keep
#// track of found terms when recursing the hierarchy. The array of located ancestors is used
#// to prevent infinite recursion loops. For performance, `term_ids` are used as array keys,
#// with 1 as value. Default empty array.
#// @return array|WP_Error The subset of $terms that are descendants of $term_id.
#//
def _get_term_children(term_id=None, terms=None, taxonomy=None, ancestors=Array(), *args_):
    
    empty_array = Array()
    if php_empty(lambda : terms):
        return empty_array
    # end if
    term_id = php_int(term_id)
    term_list = Array()
    has_children = _get_term_hierarchy(taxonomy)
    if term_id and (not (php_isset(lambda : has_children[term_id]))):
        return empty_array
    # end if
    #// Include the term itself in the ancestors array, so we can properly detect when a loop has occurred.
    if php_empty(lambda : ancestors):
        ancestors[term_id] = 1
    # end if
    for term in terms:
        use_id = False
        if (not php_is_object(term)):
            term = get_term(term, taxonomy)
            if is_wp_error(term):
                return term
            # end if
            use_id = True
        # end if
        #// Don't recurse if we've already identified the term as a child - this indicates a loop.
        if (php_isset(lambda : ancestors[term.term_id])):
            continue
        # end if
        if php_int(term.parent) == term_id:
            if use_id:
                term_list[-1] = term.term_id
            else:
                term_list[-1] = term
            # end if
            if (not (php_isset(lambda : has_children[term.term_id]))):
                continue
            # end if
            ancestors[term.term_id] = 1
            children = _get_term_children(term.term_id, terms, taxonomy, ancestors)
            if children:
                term_list = php_array_merge(term_list, children)
            # end if
        # end if
    # end for
    return term_list
# end def _get_term_children
#// 
#// Add count of children to parent count.
#// 
#// Recalculates term counts by including items from child terms. Assumes all
#// relevant children are already in the $terms argument.
#// 
#// @access private
#// @since 2.3.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param array  $terms    List of term objects (passed by reference).
#// @param string $taxonomy Term context.
#//
def _pad_term_counts(terms=None, taxonomy=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    #// This function only works for hierarchical taxonomies like post categories.
    if (not is_taxonomy_hierarchical(taxonomy)):
        return
    # end if
    term_hier = _get_term_hierarchy(taxonomy)
    if php_empty(lambda : term_hier):
        return
    # end if
    term_items = Array()
    terms_by_id = Array()
    term_ids = Array()
    for key,term in terms:
        terms_by_id[term.term_id] = terms[key]
        term_ids[term.term_taxonomy_id] = term.term_id
    # end for
    #// Get the object and term ids and stick them in a lookup table.
    tax_obj = get_taxonomy(taxonomy)
    object_types = esc_sql(tax_obj.object_type)
    results = wpdb.get_results(str("SELECT object_id, term_taxonomy_id FROM ") + str(wpdb.term_relationships) + str(" INNER JOIN ") + str(wpdb.posts) + str(" ON object_id = ID WHERE term_taxonomy_id IN (") + php_implode(",", php_array_keys(term_ids)) + ") AND post_type IN ('" + php_implode("', '", object_types) + "') AND post_status = 'publish'")
    for row in results:
        id = term_ids[row.term_taxonomy_id]
        term_items[id][row.object_id] += 1
        term_items[id][row.object_id] = term_items[id][row.object_id] if (php_isset(lambda : term_items[id][row.object_id])) else 1
    # end for
    #// Touch every ancestor's lookup row for each post in each term.
    for term_id in term_ids:
        child = term_id
        ancestors = Array()
        while True:
            parent = terms_by_id[child].parent
            if not ((not php_empty(lambda : terms_by_id[child])) and parent):
                break
            # end if
            ancestors[-1] = child
            if (not php_empty(lambda : term_items[term_id])):
                for item_id,touches in term_items[term_id]:
                    term_items[parent][item_id] += 1
                    term_items[parent][item_id] = term_items[parent][item_id] if (php_isset(lambda : term_items[parent][item_id])) else 1
                # end for
            # end if
            child = parent
            if php_in_array(parent, ancestors):
                break
            # end if
        # end while
    # end for
    #// Transfer the touched cells.
    for id,items in term_items:
        if (php_isset(lambda : terms_by_id[id])):
            terms_by_id[id].count = php_count(items)
        # end if
    # end for
# end def _pad_term_counts
#// 
#// Adds any terms from the given IDs to the cache that do not already exist in cache.
#// 
#// @since 4.6.0
#// @access private
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param array $term_ids          Array of term IDs.
#// @param bool  $update_meta_cache Optional. Whether to update the meta cache. Default true.
#//
def _prime_term_caches(term_ids=None, update_meta_cache=True, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    non_cached_ids = _get_non_cached_ids(term_ids, "terms")
    if (not php_empty(lambda : non_cached_ids)):
        fresh_terms = wpdb.get_results(php_sprintf(str("SELECT t.*, tt.* FROM ") + str(wpdb.terms) + str(" AS t INNER JOIN ") + str(wpdb.term_taxonomy) + str(" AS tt ON t.term_id = tt.term_id WHERE t.term_id IN (%s)"), join(",", php_array_map("intval", non_cached_ids))))
        update_term_cache(fresh_terms, update_meta_cache)
        if update_meta_cache:
            update_termmeta_cache(non_cached_ids)
        # end if
    # end if
# end def _prime_term_caches
#// 
#// Default callbacks.
#// 
#// 
#// Will update term count based on object types of the current taxonomy.
#// 
#// Private function for the default callback for post_tag and category
#// taxonomies.
#// 
#// @access private
#// @since 2.3.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int[]       $terms    List of Term taxonomy IDs.
#// @param WP_Taxonomy $taxonomy Current taxonomy object of terms.
#//
def _update_post_term_count(terms=None, taxonomy=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    object_types = taxonomy.object_type
    for object_type in object_types:
        object_type = php_explode(":", object_type)
    # end for
    object_types = array_unique(object_types)
    check_attachments = php_array_search("attachment", object_types)
    if False != check_attachments:
        object_types[check_attachments] = None
        check_attachments = True
    # end if
    if object_types:
        object_types = esc_sql(php_array_filter(object_types, "post_type_exists"))
    # end if
    for term in terms:
        count = 0
        #// Attachments can be 'inherit' status, we need to base count off the parent's status if so.
        if check_attachments:
            count += php_int(wpdb.get_var(wpdb.prepare(str("SELECT COUNT(*) FROM ") + str(wpdb.term_relationships) + str(", ") + str(wpdb.posts) + str(" p1 WHERE p1.ID = ") + str(wpdb.term_relationships) + str(".object_id AND ( post_status = 'publish' OR ( post_status = 'inherit' AND post_parent > 0 AND ( SELECT post_status FROM ") + str(wpdb.posts) + str(" WHERE ID = p1.post_parent ) = 'publish' ) ) AND post_type = 'attachment' AND term_taxonomy_id = %d"), term)))
        # end if
        if object_types:
            #// phpcs:ignore WordPress.DB.PreparedSQLPlaceholders.QuotedDynamicPlaceholderGeneration
            count += php_int(wpdb.get_var(wpdb.prepare(str("SELECT COUNT(*) FROM ") + str(wpdb.term_relationships) + str(", ") + str(wpdb.posts) + str(" WHERE ") + str(wpdb.posts) + str(".ID = ") + str(wpdb.term_relationships) + str(".object_id AND post_status = 'publish' AND post_type IN ('") + php_implode("', '", object_types) + "') AND term_taxonomy_id = %d", term)))
        # end if
        #// This action is documented in wp-includes/taxonomy.php
        do_action("edit_term_taxonomy", term, taxonomy.name)
        wpdb.update(wpdb.term_taxonomy, compact("count"), Array({"term_taxonomy_id": term}))
        #// This action is documented in wp-includes/taxonomy.php
        do_action("edited_term_taxonomy", term, taxonomy.name)
    # end for
# end def _update_post_term_count
#// 
#// Will update term count based on number of objects.
#// 
#// Default callback for the 'link_category' taxonomy.
#// 
#// @since 3.3.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int[]       $terms    List of term taxonomy IDs.
#// @param WP_Taxonomy $taxonomy Current taxonomy object of terms.
#//
def _update_generic_term_count(terms=None, taxonomy=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    for term in terms:
        count = wpdb.get_var(wpdb.prepare(str("SELECT COUNT(*) FROM ") + str(wpdb.term_relationships) + str(" WHERE term_taxonomy_id = %d"), term))
        #// This action is documented in wp-includes/taxonomy.php
        do_action("edit_term_taxonomy", term, taxonomy.name)
        wpdb.update(wpdb.term_taxonomy, compact("count"), Array({"term_taxonomy_id": term}))
        #// This action is documented in wp-includes/taxonomy.php
        do_action("edited_term_taxonomy", term, taxonomy.name)
    # end for
# end def _update_generic_term_count
#// 
#// Create a new term for a term_taxonomy item that currently shares its term
#// with another term_taxonomy.
#// 
#// @ignore
#// @since 4.2.0
#// @since 4.3.0 Introduced `$record` parameter. Also, `$term_id` and
#// `$term_taxonomy_id` can now accept objects.
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int|object $term_id          ID of the shared term, or the shared term object.
#// @param int|object $term_taxonomy_id ID of the term_taxonomy item to receive a new term, or the term_taxonomy object
#// (corresponding to a row from the term_taxonomy table).
#// @param bool       $record           Whether to record data about the split term in the options table. The recording
#// process has the potential to be resource-intensive, so during batch operations
#// it can be beneficial to skip inline recording and do it just once, after the
#// batch is processed. Only set this to `false` if you know what you are doing.
#// Default: true.
#// @return int|WP_Error When the current term does not need to be split (or cannot be split on the current
#// database schema), `$term_id` is returned. When the term is successfully split, the
#// new term_id is returned. A WP_Error is returned for miscellaneous errors.
#//
def _split_shared_term(term_id=None, term_taxonomy_id=None, record=True, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if php_is_object(term_id):
        shared_term = term_id
        term_id = php_intval(shared_term.term_id)
    # end if
    if php_is_object(term_taxonomy_id):
        term_taxonomy = term_taxonomy_id
        term_taxonomy_id = php_intval(term_taxonomy.term_taxonomy_id)
    # end if
    #// If there are no shared term_taxonomy rows, there's nothing to do here.
    shared_tt_count = php_int(wpdb.get_var(wpdb.prepare(str("SELECT COUNT(*) FROM ") + str(wpdb.term_taxonomy) + str(" tt WHERE tt.term_id = %d AND tt.term_taxonomy_id != %d"), term_id, term_taxonomy_id)))
    if (not shared_tt_count):
        return term_id
    # end if
    #// 
    #// Verify that the term_taxonomy_id passed to the function is actually associated with the term_id.
    #// If there's a mismatch, it may mean that the term is already split. Return the actual term_id from the db.
    #//
    check_term_id = php_int(wpdb.get_var(wpdb.prepare(str("SELECT term_id FROM ") + str(wpdb.term_taxonomy) + str(" WHERE term_taxonomy_id = %d"), term_taxonomy_id)))
    if check_term_id != term_id:
        return check_term_id
    # end if
    #// Pull up data about the currently shared slug, which we'll use to populate the new one.
    if php_empty(lambda : shared_term):
        shared_term = wpdb.get_row(wpdb.prepare(str("SELECT t.* FROM ") + str(wpdb.terms) + str(" t WHERE t.term_id = %d"), term_id))
    # end if
    new_term_data = Array({"name": shared_term.name, "slug": shared_term.slug, "term_group": shared_term.term_group})
    if False == wpdb.insert(wpdb.terms, new_term_data):
        return php_new_class("WP_Error", lambda : WP_Error("db_insert_error", __("Could not split shared term."), wpdb.last_error))
    # end if
    new_term_id = php_int(wpdb.insert_id)
    #// Update the existing term_taxonomy to point to the newly created term.
    wpdb.update(wpdb.term_taxonomy, Array({"term_id": new_term_id}), Array({"term_taxonomy_id": term_taxonomy_id}))
    #// Reassign child terms to the new parent.
    if php_empty(lambda : term_taxonomy):
        term_taxonomy = wpdb.get_row(wpdb.prepare(str("SELECT * FROM ") + str(wpdb.term_taxonomy) + str(" WHERE term_taxonomy_id = %d"), term_taxonomy_id))
    # end if
    children_tt_ids = wpdb.get_col(wpdb.prepare(str("SELECT term_taxonomy_id FROM ") + str(wpdb.term_taxonomy) + str(" WHERE parent = %d AND taxonomy = %s"), term_id, term_taxonomy.taxonomy))
    if (not php_empty(lambda : children_tt_ids)):
        for child_tt_id in children_tt_ids:
            wpdb.update(wpdb.term_taxonomy, Array({"parent": new_term_id}), Array({"term_taxonomy_id": child_tt_id}))
            clean_term_cache(php_int(child_tt_id), "", False)
        # end for
    else:
        #// If the term has no children, we must force its taxonomy cache to be rebuilt separately.
        clean_term_cache(new_term_id, term_taxonomy.taxonomy, False)
    # end if
    clean_term_cache(term_id, term_taxonomy.taxonomy, False)
    #// 
    #// Taxonomy cache clearing is delayed to avoid race conditions that may occur when
    #// regenerating the taxonomy's hierarchy tree.
    #//
    taxonomies_to_clean = Array(term_taxonomy.taxonomy)
    #// Clean the cache for term taxonomies formerly shared with the current term.
    shared_term_taxonomies = wpdb.get_col(wpdb.prepare(str("SELECT taxonomy FROM ") + str(wpdb.term_taxonomy) + str(" WHERE term_id = %d"), term_id))
    taxonomies_to_clean = php_array_merge(taxonomies_to_clean, shared_term_taxonomies)
    for taxonomy_to_clean in taxonomies_to_clean:
        clean_taxonomy_cache(taxonomy_to_clean)
    # end for
    #// Keep a record of term_ids that have been split, keyed by old term_id. See wp_get_split_term().
    if record:
        split_term_data = get_option("_split_terms", Array())
        if (not (php_isset(lambda : split_term_data[term_id]))):
            split_term_data[term_id] = Array()
        # end if
        split_term_data[term_id][term_taxonomy.taxonomy] = new_term_id
        update_option("_split_terms", split_term_data)
    # end if
    #// If we've just split the final shared term, set the "finished" flag.
    shared_terms_exist = wpdb.get_results(str("SELECT tt.term_id, t.*, count(*) as term_tt_count FROM ") + str(wpdb.term_taxonomy) + str(" tt\n      LEFT JOIN ") + str(wpdb.terms) + str(""" t ON t.term_id = tt.term_id\n      GROUP BY t.term_id\n        HAVING term_tt_count > 1\n      LIMIT 1"""))
    if (not shared_terms_exist):
        update_option("finished_splitting_shared_terms", True)
    # end if
    #// 
    #// Fires after a previously shared taxonomy term is split into two separate terms.
    #// 
    #// @since 4.2.0
    #// 
    #// @param int    $term_id          ID of the formerly shared term.
    #// @param int    $new_term_id      ID of the new term created for the $term_taxonomy_id.
    #// @param int    $term_taxonomy_id ID for the term_taxonomy row affected by the split.
    #// @param string $taxonomy         Taxonomy for the split term.
    #//
    do_action("split_shared_term", term_id, new_term_id, term_taxonomy_id, term_taxonomy.taxonomy)
    return new_term_id
# end def _split_shared_term
#// 
#// Splits a batch of shared taxonomy terms.
#// 
#// @since 4.3.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#//
def _wp_batch_split_terms(*args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    lock_name = "term_split.lock"
    #// Try to lock.
    lock_result = wpdb.query(wpdb.prepare(str("INSERT IGNORE INTO `") + str(wpdb.options) + str("` ( `option_name`, `option_value`, `autoload` ) VALUES (%s, %s, 'no') /* LOCK */"), lock_name, time()))
    if (not lock_result):
        lock_result = get_option(lock_name)
        #// Bail if we were unable to create a lock, or if the existing lock is still valid.
        if (not lock_result) or lock_result > time() - HOUR_IN_SECONDS:
            wp_schedule_single_event(time() + 5 * MINUTE_IN_SECONDS, "wp_split_shared_term_batch")
            return
        # end if
    # end if
    #// Update the lock, as by this point we've definitely got a lock, just need to fire the actions.
    update_option(lock_name, time())
    #// Get a list of shared terms (those with more than one associated row in term_taxonomy).
    shared_terms = wpdb.get_results(str("SELECT tt.term_id, t.*, count(*) as term_tt_count FROM ") + str(wpdb.term_taxonomy) + str(" tt\n        LEFT JOIN ") + str(wpdb.terms) + str(""" t ON t.term_id = tt.term_id\n      GROUP BY t.term_id\n        HAVING term_tt_count > 1\n      LIMIT 10"""))
    #// No more terms, we're done here.
    if (not shared_terms):
        update_option("finished_splitting_shared_terms", True)
        delete_option(lock_name)
        return
    # end if
    #// Shared terms found? We'll need to run this script again.
    wp_schedule_single_event(time() + 2 * MINUTE_IN_SECONDS, "wp_split_shared_term_batch")
    #// Rekey shared term array for faster lookups.
    _shared_terms = Array()
    for shared_term in shared_terms:
        term_id = php_intval(shared_term.term_id)
        _shared_terms[term_id] = shared_term
    # end for
    shared_terms = _shared_terms
    #// Get term taxonomy data for all shared terms.
    shared_term_ids = php_implode(",", php_array_keys(shared_terms))
    shared_tts = wpdb.get_results(str("SELECT * FROM ") + str(wpdb.term_taxonomy) + str(" WHERE `term_id` IN (") + str(shared_term_ids) + str(")"))
    #// Split term data recording is slow, so we do it just once, outside the loop.
    split_term_data = get_option("_split_terms", Array())
    skipped_first_term = Array()
    taxonomies = Array()
    for shared_tt in shared_tts:
        term_id = php_intval(shared_tt.term_id)
        #// Don't split the first tt belonging to a given term_id.
        if (not (php_isset(lambda : skipped_first_term[term_id]))):
            skipped_first_term[term_id] = 1
            continue
        # end if
        if (not (php_isset(lambda : split_term_data[term_id]))):
            split_term_data[term_id] = Array()
        # end if
        #// Keep track of taxonomies whose hierarchies need flushing.
        if (not (php_isset(lambda : taxonomies[shared_tt.taxonomy]))):
            taxonomies[shared_tt.taxonomy] = 1
        # end if
        #// Split the term.
        split_term_data[term_id][shared_tt.taxonomy] = _split_shared_term(shared_terms[term_id], shared_tt, False)
    # end for
    #// Rebuild the cached hierarchy for each affected taxonomy.
    for tax in php_array_keys(taxonomies):
        delete_option(str(tax) + str("_children"))
        _get_term_hierarchy(tax)
    # end for
    update_option("_split_terms", split_term_data)
    delete_option(lock_name)
# end def _wp_batch_split_terms
#// 
#// In order to avoid the _wp_batch_split_terms() job being accidentally removed,
#// check that it's still scheduled while we haven't finished splitting terms.
#// 
#// @ignore
#// @since 4.3.0
#//
def _wp_check_for_scheduled_split_terms(*args_):
    
    if (not get_option("finished_splitting_shared_terms")) and (not wp_next_scheduled("wp_split_shared_term_batch")):
        wp_schedule_single_event(time() + MINUTE_IN_SECONDS, "wp_split_shared_term_batch")
    # end if
# end def _wp_check_for_scheduled_split_terms
#// 
#// Check default categories when a term gets split to see if any of them need to be updated.
#// 
#// @ignore
#// @since 4.2.0
#// 
#// @param int    $term_id          ID of the formerly shared term.
#// @param int    $new_term_id      ID of the new term created for the $term_taxonomy_id.
#// @param int    $term_taxonomy_id ID for the term_taxonomy row affected by the split.
#// @param string $taxonomy         Taxonomy for the split term.
#//
def _wp_check_split_default_terms(term_id=None, new_term_id=None, term_taxonomy_id=None, taxonomy=None, *args_):
    
    if "category" != taxonomy:
        return
    # end if
    for option in Array("default_category", "default_link_category", "default_email_category"):
        if php_int(get_option(option, -1)) == term_id:
            update_option(option, new_term_id)
        # end if
    # end for
# end def _wp_check_split_default_terms
#// 
#// Check menu items when a term gets split to see if any of them need to be updated.
#// 
#// @ignore
#// @since 4.2.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int    $term_id          ID of the formerly shared term.
#// @param int    $new_term_id      ID of the new term created for the $term_taxonomy_id.
#// @param int    $term_taxonomy_id ID for the term_taxonomy row affected by the split.
#// @param string $taxonomy         Taxonomy for the split term.
#//
def _wp_check_split_terms_in_menus(term_id=None, new_term_id=None, term_taxonomy_id=None, taxonomy=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    post_ids = wpdb.get_col(wpdb.prepare(str("SELECT m1.post_id\n       FROM ") + str(wpdb.postmeta) + str(" AS m1\n            INNER JOIN ") + str(wpdb.postmeta) + str(" AS m2 ON ( m2.post_id = m1.post_id )\n           INNER JOIN ") + str(wpdb.postmeta) + str(""" AS m3 ON ( m3.post_id = m1.post_id )\n     WHERE ( m1.meta_key = '_menu_item_type' AND m1.meta_value = 'taxonomy' )\n          AND ( m2.meta_key = '_menu_item_object' AND m2.meta_value = %s )\n          AND ( m3.meta_key = '_menu_item_object_id' AND m3.meta_value = %d )"""), taxonomy, term_id))
    if post_ids:
        for post_id in post_ids:
            update_post_meta(post_id, "_menu_item_object_id", new_term_id, term_id)
        # end for
    # end if
# end def _wp_check_split_terms_in_menus
#// 
#// If the term being split is a nav_menu, change associations.
#// 
#// @ignore
#// @since 4.3.0
#// 
#// @param int    $term_id          ID of the formerly shared term.
#// @param int    $new_term_id      ID of the new term created for the $term_taxonomy_id.
#// @param int    $term_taxonomy_id ID for the term_taxonomy row affected by the split.
#// @param string $taxonomy         Taxonomy for the split term.
#//
def _wp_check_split_nav_menu_terms(term_id=None, new_term_id=None, term_taxonomy_id=None, taxonomy=None, *args_):
    
    if "nav_menu" != taxonomy:
        return
    # end if
    #// Update menu locations.
    locations = get_nav_menu_locations()
    for location,menu_id in locations:
        if term_id == menu_id:
            locations[location] = new_term_id
        # end if
    # end for
    set_theme_mod("nav_menu_locations", locations)
# end def _wp_check_split_nav_menu_terms
#// 
#// Get data about terms that previously shared a single term_id, but have since been split.
#// 
#// @since 4.2.0
#// 
#// @param int $old_term_id Term ID. This is the old, pre-split term ID.
#// @return array Array of new term IDs, keyed by taxonomy.
#//
def wp_get_split_terms(old_term_id=None, *args_):
    
    split_terms = get_option("_split_terms", Array())
    terms = Array()
    if (php_isset(lambda : split_terms[old_term_id])):
        terms = split_terms[old_term_id]
    # end if
    return terms
# end def wp_get_split_terms
#// 
#// Get the new term ID corresponding to a previously split term.
#// 
#// @since 4.2.0
#// 
#// @param int    $old_term_id Term ID. This is the old, pre-split term ID.
#// @param string $taxonomy    Taxonomy that the term belongs to.
#// @return int|false If a previously split term is found corresponding to the old term_id and taxonomy,
#// the new term_id will be returned. If no previously split term is found matching
#// the parameters, returns false.
#//
def wp_get_split_term(old_term_id=None, taxonomy=None, *args_):
    
    split_terms = wp_get_split_terms(old_term_id)
    term_id = False
    if (php_isset(lambda : split_terms[taxonomy])):
        term_id = php_int(split_terms[taxonomy])
    # end if
    return term_id
# end def wp_get_split_term
#// 
#// Determine whether a term is shared between multiple taxonomies.
#// 
#// Shared taxonomy terms began to be split in 4.3, but failed cron tasks or
#// other delays in upgrade routines may cause shared terms to remain.
#// 
#// @since 4.4.0
#// 
#// @param int $term_id Term ID.
#// @return bool Returns false if a term is not shared between multiple taxonomies or
#// if splitting shared taxonomy terms is finished.
#//
def wp_term_is_shared(term_id=None, *args_):
    
    global wpdb
    php_check_if_defined("wpdb")
    if get_option("finished_splitting_shared_terms"):
        return False
    # end if
    tt_count = wpdb.get_var(wpdb.prepare(str("SELECT COUNT(*) FROM ") + str(wpdb.term_taxonomy) + str(" WHERE term_id = %d"), term_id))
    return tt_count > 1
# end def wp_term_is_shared
#// 
#// Generate a permalink for a taxonomy term archive.
#// 
#// @since 2.5.0
#// 
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// 
#// @param WP_Term|int|string $term     The term object, ID, or slug whose link will be retrieved.
#// @param string             $taxonomy Optional. Taxonomy. Default empty.
#// @return string|WP_Error URL of the taxonomy term archive on success, WP_Error if term does not exist.
#//
def get_term_link(term=None, taxonomy="", *args_):
    
    global wp_rewrite
    php_check_if_defined("wp_rewrite")
    if (not php_is_object(term)):
        if php_is_int(term):
            term = get_term(term, taxonomy)
        else:
            term = get_term_by("slug", term, taxonomy)
        # end if
    # end if
    if (not php_is_object(term)):
        term = php_new_class("WP_Error", lambda : WP_Error("invalid_term", __("Empty Term.")))
    # end if
    if is_wp_error(term):
        return term
    # end if
    taxonomy = term.taxonomy
    termlink = wp_rewrite.get_extra_permastruct(taxonomy)
    #// 
    #// Filters the permalink structure for a terms before token replacement occurs.
    #// 
    #// @since 4.9.0
    #// 
    #// @param string  $termlink The permalink structure for the term's taxonomy.
    #// @param WP_Term $term     The term object.
    #//
    termlink = apply_filters("pre_term_link", termlink, term)
    slug = term.slug
    t = get_taxonomy(taxonomy)
    if php_empty(lambda : termlink):
        if "category" == taxonomy:
            termlink = "?cat=" + term.term_id
        elif t.query_var:
            termlink = str("?") + str(t.query_var) + str("=") + str(slug)
        else:
            termlink = str("?taxonomy=") + str(taxonomy) + str("&term=") + str(slug)
        # end if
        termlink = home_url(termlink)
    else:
        if t.rewrite["hierarchical"]:
            hierarchical_slugs = Array()
            ancestors = get_ancestors(term.term_id, taxonomy, "taxonomy")
            for ancestor in ancestors:
                ancestor_term = get_term(ancestor, taxonomy)
                hierarchical_slugs[-1] = ancestor_term.slug
            # end for
            hierarchical_slugs = array_reverse(hierarchical_slugs)
            hierarchical_slugs[-1] = slug
            termlink = php_str_replace(str("%") + str(taxonomy) + str("%"), php_implode("/", hierarchical_slugs), termlink)
        else:
            termlink = php_str_replace(str("%") + str(taxonomy) + str("%"), slug, termlink)
        # end if
        termlink = home_url(user_trailingslashit(termlink, "category"))
    # end if
    #// Back compat filters.
    if "post_tag" == taxonomy:
        #// 
        #// Filters the tag link.
        #// 
        #// @since 2.3.0
        #// @deprecated 2.5.0 Use {@see 'term_link'} instead.
        #// 
        #// @param string $termlink Tag link URL.
        #// @param int    $term_id  Term ID.
        #//
        termlink = apply_filters_deprecated("tag_link", Array(termlink, term.term_id), "2.5.0", "term_link")
    elif "category" == taxonomy:
        #// 
        #// Filters the category link.
        #// 
        #// @since 1.5.0
        #// @deprecated 2.5.0 Use {@see 'term_link'} instead.
        #// 
        #// @param string $termlink Category link URL.
        #// @param int    $term_id  Term ID.
        #//
        termlink = apply_filters_deprecated("category_link", Array(termlink, term.term_id), "2.5.0", "term_link")
    # end if
    #// 
    #// Filters the term link.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string  $termlink Term link URL.
    #// @param WP_Term $term     Term object.
    #// @param string  $taxonomy Taxonomy slug.
    #//
    return apply_filters("term_link", termlink, term, taxonomy)
# end def get_term_link
#// 
#// Display the taxonomies of a post with available options.
#// 
#// This function can be used within the loop to display the taxonomies for a
#// post without specifying the Post ID. You can also use it outside the Loop to
#// display the taxonomies for a specific post.
#// 
#// @since 2.5.0
#// 
#// @param array $args {
#// Arguments about which post to use and how to format the output. Shares all of the arguments
#// supported by get_the_taxonomies(), in addition to the following.
#// 
#// @type  int|WP_Post $post   Post ID or object to get taxonomies of. Default current post.
#// @type  string      $before Displays before the taxonomies. Default empty string.
#// @type  string      $sep    Separates each taxonomy. Default is a space.
#// @type  string      $after  Displays after the taxonomies. Default empty string.
#// }
#//
def the_taxonomies(args=Array(), *args_):
    
    defaults = Array({"post": 0, "before": "", "sep": " ", "after": ""})
    parsed_args = wp_parse_args(args, defaults)
    php_print(parsed_args["before"] + join(parsed_args["sep"], get_the_taxonomies(parsed_args["post"], parsed_args)) + parsed_args["after"])
# end def the_taxonomies
#// 
#// Retrieve all taxonomies associated with a post.
#// 
#// This function can be used within the loop. It will also return an array of
#// the taxonomies with links to the taxonomy and name.
#// 
#// @since 2.5.0
#// 
#// @param int|WP_Post $post Optional. Post ID or WP_Post object. Default is global $post.
#// @param array $args {
#// Optional. Arguments about how to format the list of taxonomies. Default empty array.
#// 
#// @type string $template      Template for displaying a taxonomy label and list of terms.
#// Default is "Label: Terms."
#// @type string $term_template Template for displaying a single term in the list. Default is the term name
#// linked to its archive.
#// }
#// @return array List of taxonomies.
#//
def get_the_taxonomies(post=0, args=Array(), *args_):
    
    post = get_post(post)
    args = wp_parse_args(args, Array({"template": __("%s: %l."), "term_template": "<a href=\"%1$s\">%2$s</a>"}))
    taxonomies = Array()
    if (not post):
        return taxonomies
    # end if
    for taxonomy in get_object_taxonomies(post):
        t = get_taxonomy(taxonomy)
        if php_empty(lambda : t["label"]):
            t["label"] = taxonomy
        # end if
        if php_empty(lambda : t["args"]):
            t["args"] = Array()
        # end if
        if php_empty(lambda : t["template"]):
            t["template"] = args["template"]
        # end if
        if php_empty(lambda : t["term_template"]):
            t["term_template"] = args["term_template"]
        # end if
        terms = get_object_term_cache(post.ID, taxonomy)
        if False == terms:
            terms = wp_get_object_terms(post.ID, taxonomy, t["args"])
        # end if
        links = Array()
        for term in terms:
            links[-1] = wp_sprintf(t["term_template"], esc_attr(get_term_link(term)), term.name)
        # end for
        if links:
            taxonomies[taxonomy] = wp_sprintf(t["template"], t["label"], links, terms)
        # end if
    # end for
    return taxonomies
# end def get_the_taxonomies
#// 
#// Retrieve all taxonomy names for the given post.
#// 
#// @since 2.5.0
#// 
#// @param int|WP_Post $post Optional. Post ID or WP_Post object. Default is global $post.
#// @return string[] An array of all taxonomy names for the given post.
#//
def get_post_taxonomies(post=0, *args_):
    
    post = get_post(post)
    return get_object_taxonomies(post)
# end def get_post_taxonomies
#// 
#// Determine if the given object is associated with any of the given terms.
#// 
#// The given terms are checked against the object's terms' term_ids, names and slugs.
#// Terms given as integers will only be checked against the object's terms' term_ids.
#// If no terms are given, determines if object is associated with any terms in the given taxonomy.
#// 
#// @since 2.7.0
#// 
#// @param int              $object_id ID of the object (post ID, link ID, ...).
#// @param string           $taxonomy  Single taxonomy name.
#// @param int|string|array $terms     Optional. Term term_id, name, slug or array of said. Default null.
#// @return bool|WP_Error WP_Error on input error.
#//
def is_object_in_term(object_id=None, taxonomy=None, terms=None, *args_):
    
    object_id = php_int(object_id)
    if (not object_id):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_object", __("Invalid object ID.")))
    # end if
    object_terms = get_object_term_cache(object_id, taxonomy)
    if False == object_terms:
        object_terms = wp_get_object_terms(object_id, taxonomy, Array({"update_term_meta_cache": False}))
        if is_wp_error(object_terms):
            return object_terms
        # end if
        wp_cache_set(object_id, wp_list_pluck(object_terms, "term_id"), str(taxonomy) + str("_relationships"))
    # end if
    if is_wp_error(object_terms):
        return object_terms
    # end if
    if php_empty(lambda : object_terms):
        return False
    # end if
    if php_empty(lambda : terms):
        return (not php_empty(lambda : object_terms))
    # end if
    terms = terms
    ints = php_array_filter(terms, "is_int")
    if ints:
        strs = php_array_diff(terms, ints)
    else:
        strs = terms
    # end if
    for object_term in object_terms:
        #// If term is an int, check against term_ids only.
        if ints and php_in_array(object_term.term_id, ints):
            return True
        # end if
        if strs:
            #// Only check numeric strings against term_id, to avoid false matches due to type juggling.
            numeric_strs = php_array_map("intval", php_array_filter(strs, "is_numeric"))
            if php_in_array(object_term.term_id, numeric_strs, True):
                return True
            # end if
            if php_in_array(object_term.name, strs):
                return True
            # end if
            if php_in_array(object_term.slug, strs):
                return True
            # end if
        # end if
    # end for
    return False
# end def is_object_in_term
#// 
#// Determine if the given object type is associated with the given taxonomy.
#// 
#// @since 3.0.0
#// 
#// @param string $object_type Object type string.
#// @param string $taxonomy    Single taxonomy name.
#// @return bool True if object is associated with the taxonomy, otherwise false.
#//
def is_object_in_taxonomy(object_type=None, taxonomy=None, *args_):
    
    taxonomies = get_object_taxonomies(object_type)
    if php_empty(lambda : taxonomies):
        return False
    # end if
    return php_in_array(taxonomy, taxonomies)
# end def is_object_in_taxonomy
#// 
#// Get an array of ancestor IDs for a given object.
#// 
#// @since 3.1.0
#// @since 4.1.0 Introduced the `$resource_type` argument.
#// 
#// @param int    $object_id     Optional. The ID of the object. Default 0.
#// @param string $object_type   Optional. The type of object for which we'll be retrieving
#// ancestors. Accepts a post type or a taxonomy name. Default empty.
#// @param string $resource_type Optional. Type of resource $object_type is. Accepts 'post_type'
#// or 'taxonomy'. Default empty.
#// @return int[] An array of IDs of ancestors from lowest to highest in the hierarchy.
#//
def get_ancestors(object_id=0, object_type="", resource_type="", *args_):
    
    object_id = php_int(object_id)
    ancestors = Array()
    if php_empty(lambda : object_id):
        #// This filter is documented in wp-includes/taxonomy.php
        return apply_filters("get_ancestors", ancestors, object_id, object_type, resource_type)
    # end if
    if (not resource_type):
        if is_taxonomy_hierarchical(object_type):
            resource_type = "taxonomy"
        elif post_type_exists(object_type):
            resource_type = "post_type"
        # end if
    # end if
    if "taxonomy" == resource_type:
        term = get_term(object_id, object_type)
        while True:
            
            if not ((not is_wp_error(term)) and (not php_empty(lambda : term.parent)) and (not php_in_array(term.parent, ancestors))):
                break
            # end if
            ancestors[-1] = php_int(term.parent)
            term = get_term(term.parent, object_type)
        # end while
    elif "post_type" == resource_type:
        ancestors = get_post_ancestors(object_id)
    # end if
    #// 
    #// Filters a given object's ancestors.
    #// 
    #// @since 3.1.0
    #// @since 4.1.1 Introduced the `$resource_type` parameter.
    #// 
    #// @param int[]  $ancestors     An array of IDs of object ancestors.
    #// @param int    $object_id     Object ID.
    #// @param string $object_type   Type of object.
    #// @param string $resource_type Type of resource $object_type is.
    #//
    return apply_filters("get_ancestors", ancestors, object_id, object_type, resource_type)
# end def get_ancestors
#// 
#// Returns the term's parent's term_ID.
#// 
#// @since 3.1.0
#// 
#// @param int    $term_id  Term ID.
#// @param string $taxonomy Taxonomy name.
#// @return int|false False on error.
#//
def wp_get_term_taxonomy_parent_id(term_id=None, taxonomy=None, *args_):
    
    term = get_term(term_id, taxonomy)
    if (not term) or is_wp_error(term):
        return False
    # end if
    return php_int(term.parent)
# end def wp_get_term_taxonomy_parent_id
#// 
#// Checks the given subset of the term hierarchy for hierarchy loops.
#// Prevents loops from forming and breaks those that it finds.
#// 
#// Attached to the {@see 'wp_update_term_parent'} filter.
#// 
#// @since 3.1.0
#// 
#// @param int    $parent   `term_id` of the parent for the term we're checking.
#// @param int    $term_id  The term we're checking.
#// @param string $taxonomy The taxonomy of the term we're checking.
#// 
#// @return int The new parent for the term.
#//
def wp_check_term_hierarchy_for_loops(parent=None, term_id=None, taxonomy=None, *args_):
    
    #// Nothing fancy here - bail.
    if (not parent):
        return 0
    # end if
    #// Can't be its own parent.
    if parent == term_id:
        return 0
    # end if
    #// Now look for larger loops.
    loop = wp_find_hierarchy_loop("wp_get_term_taxonomy_parent_id", term_id, parent, Array(taxonomy))
    if (not loop):
        return parent
        pass
    # end if
    #// Setting $parent to the given value causes a loop.
    if (php_isset(lambda : loop[term_id])):
        return 0
    # end if
    #// There's a loop, but it doesn't contain $term_id. Break the loop.
    for loop_member in php_array_keys(loop):
        wp_update_term(loop_member, taxonomy, Array({"parent": 0}))
    # end for
    return parent
# end def wp_check_term_hierarchy_for_loops
#// 
#// Determines whether a taxonomy is considered "viewable".
#// 
#// @since 5.1.0
#// 
#// @param string|WP_Taxonomy $taxonomy Taxonomy name or object.
#// @return bool Whether the taxonomy should be considered viewable.
#//
def is_taxonomy_viewable(taxonomy=None, *args_):
    
    if is_scalar(taxonomy):
        taxonomy = get_taxonomy(taxonomy)
        if (not taxonomy):
            return False
        # end if
    # end if
    return taxonomy.publicly_queryable
# end def is_taxonomy_viewable
#// 
#// Sets the last changed time for the 'terms' cache group.
#// 
#// @since 5.0.0
#//
def wp_cache_set_terms_last_changed(*args_):
    
    wp_cache_set("last_changed", php_microtime(), "terms")
# end def wp_cache_set_terms_last_changed
#// 
#// Aborts calls to term meta if it is not supported.
#// 
#// @since 5.0.0
#// 
#// @param mixed $check Skip-value for whether to proceed term meta function execution.
#// @return mixed Original value of $check, or false if term meta is not supported.
#//
def wp_check_term_meta_support_prefilter(check=None, *args_):
    
    if get_option("db_version") < 34370:
        return False
    # end if
    return check
# end def wp_check_term_meta_support_prefilter
