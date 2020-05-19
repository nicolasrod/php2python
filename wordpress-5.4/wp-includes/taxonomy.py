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
def create_initial_taxonomies(*_args_):
    
    
    global wp_rewrite_
    php_check_if_defined("wp_rewrite_")
    if (not did_action("init")):
        rewrite_ = Array({"category": False, "post_tag": False, "post_format": False})
    else:
        #// 
        #// Filters the post formats rewrite base.
        #// 
        #// @since 3.1.0
        #// 
        #// @param string $context Context of the rewrite base. Default 'type'.
        #//
        post_format_base_ = apply_filters("post_format_rewrite_base", "type")
        rewrite_ = Array({"category": Array({"hierarchical": True, "slug": get_option("category_base") if get_option("category_base") else "category", "with_front": (not get_option("category_base")) or wp_rewrite_.using_index_permalinks(), "ep_mask": EP_CATEGORIES})}, {"post_tag": Array({"hierarchical": False, "slug": get_option("tag_base") if get_option("tag_base") else "tag", "with_front": (not get_option("tag_base")) or wp_rewrite_.using_index_permalinks(), "ep_mask": EP_TAGS})}, {"post_format": Array({"slug": post_format_base_}) if post_format_base_ else False})
    # end if
    register_taxonomy("category", "post", Array({"hierarchical": True, "query_var": "category_name", "rewrite": rewrite_["category"], "public": True, "show_ui": True, "show_admin_column": True, "_builtin": True, "capabilities": Array({"manage_terms": "manage_categories", "edit_terms": "edit_categories", "delete_terms": "delete_categories", "assign_terms": "assign_categories"})}, {"show_in_rest": True, "rest_base": "categories", "rest_controller_class": "WP_REST_Terms_Controller"}))
    register_taxonomy("post_tag", "post", Array({"hierarchical": False, "query_var": "tag", "rewrite": rewrite_["post_tag"], "public": True, "show_ui": True, "show_admin_column": True, "_builtin": True, "capabilities": Array({"manage_terms": "manage_post_tags", "edit_terms": "edit_post_tags", "delete_terms": "delete_post_tags", "assign_terms": "assign_post_tags"})}, {"show_in_rest": True, "rest_base": "tags", "rest_controller_class": "WP_REST_Terms_Controller"}))
    register_taxonomy("nav_menu", "nav_menu_item", Array({"public": False, "hierarchical": False, "labels": Array({"name": __("Navigation Menus"), "singular_name": __("Navigation Menu")})}, {"query_var": False, "rewrite": False, "show_ui": False, "_builtin": True, "show_in_nav_menus": False}))
    register_taxonomy("link_category", "link", Array({"hierarchical": False, "labels": Array({"name": __("Link Categories"), "singular_name": __("Link Category"), "search_items": __("Search Link Categories"), "popular_items": None, "all_items": __("All Link Categories"), "edit_item": __("Edit Link Category"), "update_item": __("Update Link Category"), "add_new_item": __("Add New Link Category"), "new_item_name": __("New Link Category Name"), "separate_items_with_commas": None, "add_or_remove_items": None, "choose_from_most_used": None, "back_to_items": __("&larr; Back to Link Categories")})}, {"capabilities": Array({"manage_terms": "manage_links", "edit_terms": "manage_links", "delete_terms": "manage_links", "assign_terms": "manage_links"})}, {"query_var": False, "rewrite": False, "public": False, "show_ui": True, "_builtin": True}))
    register_taxonomy("post_format", "post", Array({"public": True, "hierarchical": False, "labels": Array({"name": _x("Formats", "post format"), "singular_name": _x("Format", "post format")})}, {"query_var": True, "rewrite": rewrite_["post_format"], "show_ui": False, "_builtin": True, "show_in_nav_menus": current_theme_supports("post-formats")}))
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
def get_taxonomies(args_=None, output_="names", operator_="and", *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    global wp_taxonomies_
    php_check_if_defined("wp_taxonomies_")
    field_ = "name" if "names" == output_ else False
    return wp_filter_object_list(wp_taxonomies_, args_, operator_, field_)
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
def get_object_taxonomies(object_=None, output_="names", *_args_):
    
    
    global wp_taxonomies_
    php_check_if_defined("wp_taxonomies_")
    if php_is_object(object_):
        if "attachment" == object_.post_type:
            return get_attachment_taxonomies(object_, output_)
        # end if
        object_ = object_.post_type
    # end if
    object_ = object_
    taxonomies_ = Array()
    for tax_name_,tax_obj_ in wp_taxonomies_.items():
        if php_array_intersect(object_, tax_obj_.object_type):
            if "names" == output_:
                taxonomies_[-1] = tax_name_
            else:
                taxonomies_[tax_name_] = tax_obj_
            # end if
        # end if
    # end for
    return taxonomies_
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
def get_taxonomy(taxonomy_=None, *_args_):
    
    
    global wp_taxonomies_
    php_check_if_defined("wp_taxonomies_")
    if (not taxonomy_exists(taxonomy_)):
        return False
    # end if
    return wp_taxonomies_[taxonomy_]
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
def taxonomy_exists(taxonomy_=None, *_args_):
    
    
    global wp_taxonomies_
    php_check_if_defined("wp_taxonomies_")
    return (php_isset(lambda : wp_taxonomies_[taxonomy_]))
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
def is_taxonomy_hierarchical(taxonomy_=None, *_args_):
    
    
    if (not taxonomy_exists(taxonomy_)):
        return False
    # end if
    taxonomy_ = get_taxonomy(taxonomy_)
    return taxonomy_.hierarchical
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
def register_taxonomy(taxonomy_=None, object_type_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    global wp_taxonomies_
    php_check_if_defined("wp_taxonomies_")
    if (not php_is_array(wp_taxonomies_)):
        wp_taxonomies_ = Array()
    # end if
    args_ = wp_parse_args(args_)
    if php_empty(lambda : taxonomy_) or php_strlen(taxonomy_) > 32:
        _doing_it_wrong(__FUNCTION__, __("Taxonomy names must be between 1 and 32 characters in length."), "4.2.0")
        return php_new_class("WP_Error", lambda : WP_Error("taxonomy_length_invalid", __("Taxonomy names must be between 1 and 32 characters in length.")))
    # end if
    taxonomy_object_ = php_new_class("WP_Taxonomy", lambda : WP_Taxonomy(taxonomy_, object_type_, args_))
    taxonomy_object_.add_rewrite_rules()
    wp_taxonomies_[taxonomy_] = taxonomy_object_
    taxonomy_object_.add_hooks()
    #// 
    #// Fires after a taxonomy is registered.
    #// 
    #// @since 3.3.0
    #// 
    #// @param string       $taxonomy    Taxonomy slug.
    #// @param array|string $object_type Object type or array of object types.
    #// @param array        $args        Array of taxonomy registration arguments.
    #//
    do_action("registered_taxonomy", taxonomy_, object_type_, taxonomy_object_)
    return taxonomy_object_
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
def unregister_taxonomy(taxonomy_=None, *_args_):
    
    
    if (not taxonomy_exists(taxonomy_)):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_taxonomy", __("Invalid taxonomy.")))
    # end if
    taxonomy_object_ = get_taxonomy(taxonomy_)
    #// Do not allow unregistering internal taxonomies.
    if taxonomy_object_._builtin:
        return php_new_class("WP_Error", lambda : WP_Error("invalid_taxonomy", __("Unregistering a built-in taxonomy is not allowed.")))
    # end if
    global wp_taxonomies_
    php_check_if_defined("wp_taxonomies_")
    taxonomy_object_.remove_rewrite_rules()
    taxonomy_object_.remove_hooks()
    wp_taxonomies_[taxonomy_] = None
    #// 
    #// Fires after a taxonomy is unregistered.
    #// 
    #// @since 4.5.0
    #// 
    #// @param string $taxonomy Taxonomy name.
    #//
    do_action("unregistered_taxonomy", taxonomy_)
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
def get_taxonomy_labels(tax_=None, *_args_):
    
    
    tax_.labels = tax_.labels
    if (php_isset(lambda : tax_.helps)) and php_empty(lambda : tax_.labels["separate_items_with_commas"]):
        tax_.labels["separate_items_with_commas"] = tax_.helps
    # end if
    if (php_isset(lambda : tax_.no_tagcloud)) and php_empty(lambda : tax_.labels["not_found"]):
        tax_.labels["not_found"] = tax_.no_tagcloud
    # end if
    nohier_vs_hier_defaults_ = Array({"name": Array(_x("Tags", "taxonomy general name"), _x("Categories", "taxonomy general name")), "singular_name": Array(_x("Tag", "taxonomy singular name"), _x("Category", "taxonomy singular name")), "search_items": Array(__("Search Tags"), __("Search Categories")), "popular_items": Array(__("Popular Tags"), None), "all_items": Array(__("All Tags"), __("All Categories")), "parent_item": Array(None, __("Parent Category")), "parent_item_colon": Array(None, __("Parent Category:")), "edit_item": Array(__("Edit Tag"), __("Edit Category")), "view_item": Array(__("View Tag"), __("View Category")), "update_item": Array(__("Update Tag"), __("Update Category")), "add_new_item": Array(__("Add New Tag"), __("Add New Category")), "new_item_name": Array(__("New Tag Name"), __("New Category Name")), "separate_items_with_commas": Array(__("Separate tags with commas"), None), "add_or_remove_items": Array(__("Add or remove tags"), None), "choose_from_most_used": Array(__("Choose from the most used tags"), None), "not_found": Array(__("No tags found."), __("No categories found.")), "no_terms": Array(__("No tags"), __("No categories")), "items_list_navigation": Array(__("Tags list navigation"), __("Categories list navigation")), "items_list": Array(__("Tags list"), __("Categories list")), "most_used": Array(_x("Most Used", "tags"), _x("Most Used", "categories")), "back_to_items": Array(__("&larr; Back to Tags"), __("&larr; Back to Categories"))})
    nohier_vs_hier_defaults_["menu_name"] = nohier_vs_hier_defaults_["name"]
    labels_ = _get_custom_object_labels(tax_, nohier_vs_hier_defaults_)
    taxonomy_ = tax_.name
    default_labels_ = copy.deepcopy(labels_)
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
    labels_ = apply_filters(str("taxonomy_labels_") + str(taxonomy_), labels_)
    #// Ensure that the filtered labels contain all required default values.
    labels_ = php_array_merge(default_labels_, labels_)
    return labels_
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
def register_taxonomy_for_object_type(taxonomy_=None, object_type_=None, *_args_):
    
    
    global wp_taxonomies_
    php_check_if_defined("wp_taxonomies_")
    if (not (php_isset(lambda : wp_taxonomies_[taxonomy_]))):
        return False
    # end if
    if (not get_post_type_object(object_type_)):
        return False
    # end if
    if (not php_in_array(object_type_, wp_taxonomies_[taxonomy_].object_type)):
        wp_taxonomies_[taxonomy_].object_type[-1] = object_type_
    # end if
    #// Filter out empties.
    wp_taxonomies_[taxonomy_].object_type = php_array_filter(wp_taxonomies_[taxonomy_].object_type)
    #// 
    #// Fires after a taxonomy is registered for an object type.
    #// 
    #// @since 5.1.0
    #// 
    #// @param string $taxonomy    Taxonomy name.
    #// @param string $object_type Name of the object type.
    #//
    do_action("registered_taxonomy_for_object_type", taxonomy_, object_type_)
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
def unregister_taxonomy_for_object_type(taxonomy_=None, object_type_=None, *_args_):
    
    
    global wp_taxonomies_
    php_check_if_defined("wp_taxonomies_")
    if (not (php_isset(lambda : wp_taxonomies_[taxonomy_]))):
        return False
    # end if
    if (not get_post_type_object(object_type_)):
        return False
    # end if
    key_ = php_array_search(object_type_, wp_taxonomies_[taxonomy_].object_type, True)
    if False == key_:
        return False
    # end if
    wp_taxonomies_[taxonomy_].object_type[key_] = None
    #// 
    #// Fires after a taxonomy is unregistered for an object type.
    #// 
    #// @since 5.1.0
    #// 
    #// @param string $taxonomy    Taxonomy name.
    #// @param string $object_type Name of the object type.
    #//
    do_action("unregistered_taxonomy_for_object_type", taxonomy_, object_type_)
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
def get_objects_in_term(term_ids_=None, taxonomies_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if (not php_is_array(term_ids_)):
        term_ids_ = Array(term_ids_)
    # end if
    if (not php_is_array(taxonomies_)):
        taxonomies_ = Array(taxonomies_)
    # end if
    for taxonomy_ in taxonomies_:
        if (not taxonomy_exists(taxonomy_)):
            return php_new_class("WP_Error", lambda : WP_Error("invalid_taxonomy", __("Invalid taxonomy.")))
        # end if
    # end for
    defaults_ = Array({"order": "ASC"})
    args_ = wp_parse_args(args_, defaults_)
    order_ = "DESC" if "desc" == php_strtolower(args_["order"]) else "ASC"
    term_ids_ = php_array_map("intval", term_ids_)
    taxonomies_ = "'" + php_implode("', '", php_array_map("esc_sql", taxonomies_)) + "'"
    term_ids_ = "'" + php_implode("', '", term_ids_) + "'"
    sql_ = str("SELECT tr.object_id FROM ") + str(wpdb_.term_relationships) + str(" AS tr INNER JOIN ") + str(wpdb_.term_taxonomy) + str(" AS tt ON tr.term_taxonomy_id = tt.term_taxonomy_id WHERE tt.taxonomy IN (") + str(taxonomies_) + str(") AND tt.term_id IN (") + str(term_ids_) + str(") ORDER BY tr.object_id ") + str(order_)
    last_changed_ = wp_cache_get_last_changed("terms")
    cache_key_ = "get_objects_in_term:" + php_md5(sql_) + str(":") + str(last_changed_)
    cache_ = wp_cache_get(cache_key_, "terms")
    if False == cache_:
        object_ids_ = wpdb_.get_col(sql_)
        wp_cache_set(cache_key_, object_ids_, "terms")
    else:
        object_ids_ = cache_
    # end if
    if (not object_ids_):
        return Array()
    # end if
    return object_ids_
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
def get_tax_sql(tax_query_=None, primary_table_=None, primary_id_column_=None, *_args_):
    
    
    tax_query_obj_ = php_new_class("WP_Tax_Query", lambda : WP_Tax_Query(tax_query_))
    return tax_query_obj_.get_sql(primary_table_, primary_id_column_)
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
def get_term(term_=None, taxonomy_="", output_=None, filter_="raw", *_args_):
    if output_ is None:
        output_ = OBJECT
    # end if
    
    if php_empty(lambda : term_):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_term", __("Empty Term.")))
    # end if
    if taxonomy_ and (not taxonomy_exists(taxonomy_)):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_taxonomy", __("Invalid taxonomy.")))
    # end if
    if type(term_).__name__ == "WP_Term":
        _term_ = term_
    elif php_is_object(term_):
        if php_empty(lambda : term_.filter) or "raw" == term_.filter:
            _term_ = sanitize_term(term_, taxonomy_, "raw")
            _term_ = php_new_class("WP_Term", lambda : WP_Term(_term_))
        else:
            _term_ = WP_Term.get_instance(term_.term_id)
        # end if
    else:
        _term_ = WP_Term.get_instance(term_, taxonomy_)
    # end if
    if is_wp_error(_term_):
        return _term_
    elif (not _term_):
        return None
    # end if
    #// Ensure for filters that this is not empty.
    taxonomy_ = _term_.taxonomy
    #// 
    #// Filters a taxonomy term object.
    #// 
    #// @since 2.3.0
    #// @since 4.4.0 `$_term` is now a `WP_Term` object.
    #// 
    #// @param WP_Term $_term    Term object.
    #// @param string  $taxonomy The taxonomy slug.
    #//
    _term_ = apply_filters("get_term", _term_, taxonomy_)
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
    _term_ = apply_filters(str("get_") + str(taxonomy_), _term_, taxonomy_)
    #// Bail if a filter callback has changed the type of the `$_term` object.
    if (not type(_term_).__name__ == "WP_Term"):
        return _term_
    # end if
    #// Sanitize term, according to the specified filter.
    _term_.filter(filter_)
    if ARRAY_A == output_:
        return _term_.to_array()
    elif ARRAY_N == output_:
        return php_array_values(_term_.to_array())
    # end if
    return _term_
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
def get_term_by(field_=None, value_=None, taxonomy_="", output_=None, filter_="raw", *_args_):
    if output_ is None:
        output_ = OBJECT
    # end if
    
    #// 'term_taxonomy_id' lookups don't require taxonomy checks.
    if "term_taxonomy_id" != field_ and (not taxonomy_exists(taxonomy_)):
        return False
    # end if
    #// No need to perform a query for empty 'slug' or 'name'.
    if "slug" == field_ or "name" == field_:
        value_ = php_str(value_)
        if 0 == php_strlen(value_):
            return False
        # end if
    # end if
    if "id" == field_ or "term_id" == field_:
        term_ = get_term(php_int(value_), taxonomy_, output_, filter_)
        if is_wp_error(term_) or None == term_:
            term_ = False
        # end if
        return term_
    # end if
    args_ = Array({"get": "all", "number": 1, "taxonomy": taxonomy_, "update_term_meta_cache": False, "orderby": "none", "suppress_filter": True})
    for case in Switch(field_):
        if case("slug"):
            args_["slug"] = value_
            break
        # end if
        if case("name"):
            args_["name"] = value_
            break
        # end if
        if case("term_taxonomy_id"):
            args_["term_taxonomy_id"] = value_
            args_["taxonomy"] = None
            break
        # end if
        if case():
            return False
        # end if
    # end for
    terms_ = get_terms(args_)
    if is_wp_error(terms_) or php_empty(lambda : terms_):
        return False
    # end if
    term_ = php_array_shift(terms_)
    #// In the case of 'term_taxonomy_id', override the provided `$taxonomy` with whatever we find in the DB.
    if "term_taxonomy_id" == field_:
        taxonomy_ = term_.taxonomy
    # end if
    return get_term(term_, taxonomy_, output_, filter_)
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
def get_term_children(term_id_=None, taxonomy_=None, *_args_):
    
    
    if (not taxonomy_exists(taxonomy_)):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_taxonomy", __("Invalid taxonomy.")))
    # end if
    term_id_ = php_intval(term_id_)
    terms_ = _get_term_hierarchy(taxonomy_)
    if (not (php_isset(lambda : terms_[term_id_]))):
        return Array()
    # end if
    children_ = terms_[term_id_]
    for child_ in terms_[term_id_]:
        if term_id_ == child_:
            continue
        # end if
        if (php_isset(lambda : terms_[child_])):
            children_ = php_array_merge(children_, get_term_children(child_, taxonomy_))
        # end if
    # end for
    return children_
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
def get_term_field(field_=None, term_=None, taxonomy_="", context_="display", *_args_):
    
    
    term_ = get_term(term_, taxonomy_)
    if is_wp_error(term_):
        return term_
    # end if
    if (not php_is_object(term_)):
        return ""
    # end if
    if (not (php_isset(lambda : term_.field_))):
        return ""
    # end if
    return sanitize_term_field(field_, term_.field_, term_.term_id, term_.taxonomy, context_)
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
def get_term_to_edit(id_=None, taxonomy_=None, *_args_):
    
    
    term_ = get_term(id_, taxonomy_)
    if is_wp_error(term_):
        return term_
    # end if
    if (not php_is_object(term_)):
        return ""
    # end if
    return sanitize_term(term_, taxonomy_, "edit")
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
def get_terms(args_=None, deprecated_="", *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    term_query_ = php_new_class("WP_Term_Query", lambda : WP_Term_Query())
    defaults_ = Array({"suppress_filter": False})
    #// 
    #// Legacy argument format ($taxonomy, $args) takes precedence.
    #// 
    #// We detect legacy argument format by checking if
    #// (a) a second non-empty parameter is passed, or
    #// (b) the first parameter shares no keys with the default array (ie, it's a list of taxonomies)
    #//
    _args_ = wp_parse_args(args_)
    key_intersect_ = php_array_intersect_key(term_query_.query_var_defaults, _args_)
    do_legacy_args_ = deprecated_ or php_empty(lambda : key_intersect_)
    if do_legacy_args_:
        taxonomies_ = args_
        args_ = wp_parse_args(deprecated_, defaults_)
        args_["taxonomy"] = taxonomies_
    else:
        args_ = wp_parse_args(args_, defaults_)
        if (php_isset(lambda : args_["taxonomy"])) and None != args_["taxonomy"]:
            args_["taxonomy"] = args_["taxonomy"]
        # end if
    # end if
    if (not php_empty(lambda : args_["taxonomy"])):
        for taxonomy_ in args_["taxonomy"]:
            if (not taxonomy_exists(taxonomy_)):
                return php_new_class("WP_Error", lambda : WP_Error("invalid_taxonomy", __("Invalid taxonomy.")))
            # end if
        # end for
    # end if
    #// Don't pass suppress_filter to WP_Term_Query.
    suppress_filter_ = args_["suppress_filter"]
    args_["suppress_filter"] = None
    terms_ = term_query_.query(args_)
    #// Count queries are not filtered, for legacy reasons.
    if (not php_is_array(terms_)):
        return terms_
    # end if
    if suppress_filter_:
        return terms_
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
    return apply_filters("get_terms", terms_, term_query_.query_vars["taxonomy"], term_query_.query_vars, term_query_)
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
def add_term_meta(term_id_=None, meta_key_=None, meta_value_=None, unique_=None, *_args_):
    if unique_ is None:
        unique_ = False
    # end if
    
    if wp_term_is_shared(term_id_):
        return php_new_class("WP_Error", lambda : WP_Error("ambiguous_term_id", __("Term meta cannot be added to terms that are shared between taxonomies."), term_id_))
    # end if
    return add_metadata("term", term_id_, meta_key_, meta_value_, unique_)
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
def delete_term_meta(term_id_=None, meta_key_=None, meta_value_="", *_args_):
    
    
    return delete_metadata("term", term_id_, meta_key_, meta_value_)
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
def get_term_meta(term_id_=None, key_="", single_=None, *_args_):
    if single_ is None:
        single_ = False
    # end if
    
    return get_metadata("term", term_id_, key_, single_)
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
def update_term_meta(term_id_=None, meta_key_=None, meta_value_=None, prev_value_="", *_args_):
    
    
    if wp_term_is_shared(term_id_):
        return php_new_class("WP_Error", lambda : WP_Error("ambiguous_term_id", __("Term meta cannot be added to terms that are shared between taxonomies."), term_id_))
    # end if
    return update_metadata("term", term_id_, meta_key_, meta_value_, prev_value_)
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
def update_termmeta_cache(term_ids_=None, *_args_):
    
    
    return update_meta_cache("term", term_ids_)
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
def has_term_meta(term_id_=None, *_args_):
    
    
    check_ = wp_check_term_meta_support_prefilter(None)
    if None != check_:
        return check_
    # end if
    global wpdb_
    php_check_if_defined("wpdb_")
    return wpdb_.get_results(wpdb_.prepare(str("SELECT meta_key, meta_value, meta_id, term_id FROM ") + str(wpdb_.termmeta) + str(" WHERE term_id = %d ORDER BY meta_key,meta_id"), term_id_), ARRAY_A)
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
def register_term_meta(taxonomy_=None, meta_key_=None, args_=None, *_args_):
    
    
    args_["object_subtype"] = taxonomy_
    return register_meta("term", meta_key_, args_)
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
def unregister_term_meta(taxonomy_=None, meta_key_=None, *_args_):
    
    
    return unregister_meta_key("term", meta_key_, taxonomy_)
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
def term_exists(term_=None, taxonomy_="", parent_=None, *_args_):
    if parent_ is None:
        parent_ = None
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    select_ = str("SELECT term_id FROM ") + str(wpdb_.terms) + str(" as t WHERE ")
    tax_select_ = str("SELECT tt.term_id, tt.term_taxonomy_id FROM ") + str(wpdb_.terms) + str(" AS t INNER JOIN ") + str(wpdb_.term_taxonomy) + str(" as tt ON tt.term_id = t.term_id WHERE ")
    if php_is_int(term_):
        if 0 == term_:
            return 0
        # end if
        where_ = "t.term_id = %d"
        if (not php_empty(lambda : taxonomy_)):
            #// phpcs:ignore WordPress.DB.PreparedSQLPlaceholders.ReplacementsWrongNumber
            return wpdb_.get_row(wpdb_.prepare(tax_select_ + where_ + " AND tt.taxonomy = %s", term_, taxonomy_), ARRAY_A)
        else:
            return wpdb_.get_var(wpdb_.prepare(select_ + where_, term_))
        # end if
    # end if
    term_ = php_trim(wp_unslash(term_))
    slug_ = sanitize_title(term_)
    where_ = "t.slug = %s"
    else_where_ = "t.name = %s"
    where_fields_ = Array(slug_)
    else_where_fields_ = Array(term_)
    orderby_ = "ORDER BY t.term_id ASC"
    limit_ = "LIMIT 1"
    if (not php_empty(lambda : taxonomy_)):
        if php_is_numeric(parent_):
            parent_ = php_int(parent_)
            where_fields_[-1] = parent_
            else_where_fields_[-1] = parent_
            where_ += " AND tt.parent = %d"
            else_where_ += " AND tt.parent = %d"
        # end if
        where_fields_[-1] = taxonomy_
        else_where_fields_[-1] = taxonomy_
        result_ = wpdb_.get_row(wpdb_.prepare(str("SELECT tt.term_id, tt.term_taxonomy_id FROM ") + str(wpdb_.terms) + str(" AS t INNER JOIN ") + str(wpdb_.term_taxonomy) + str(" as tt ON tt.term_id = t.term_id WHERE ") + str(where_) + str(" AND tt.taxonomy = %s ") + str(orderby_) + str(" ") + str(limit_), where_fields_), ARRAY_A)
        if result_:
            return result_
        # end if
        return wpdb_.get_row(wpdb_.prepare(str("SELECT tt.term_id, tt.term_taxonomy_id FROM ") + str(wpdb_.terms) + str(" AS t INNER JOIN ") + str(wpdb_.term_taxonomy) + str(" as tt ON tt.term_id = t.term_id WHERE ") + str(else_where_) + str(" AND tt.taxonomy = %s ") + str(orderby_) + str(" ") + str(limit_), else_where_fields_), ARRAY_A)
    # end if
    #// phpcs:ignore WordPress.DB.PreparedSQLPlaceholders.UnfinishedPrepare
    result_ = wpdb_.get_var(wpdb_.prepare(str("SELECT term_id FROM ") + str(wpdb_.terms) + str(" as t WHERE ") + str(where_) + str(" ") + str(orderby_) + str(" ") + str(limit_), where_fields_))
    if result_:
        return result_
    # end if
    #// phpcs:ignore WordPress.DB.PreparedSQLPlaceholders.UnfinishedPrepare
    return wpdb_.get_var(wpdb_.prepare(str("SELECT term_id FROM ") + str(wpdb_.terms) + str(" as t WHERE ") + str(else_where_) + str(" ") + str(orderby_) + str(" ") + str(limit_), else_where_fields_))
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
def term_is_ancestor_of(term1_=None, term2_=None, taxonomy_=None, *_args_):
    
    
    if (not (php_isset(lambda : term1_.term_id))):
        term1_ = get_term(term1_, taxonomy_)
    # end if
    if (not (php_isset(lambda : term2_.parent))):
        term2_ = get_term(term2_, taxonomy_)
    # end if
    if php_empty(lambda : term1_.term_id) or php_empty(lambda : term2_.parent):
        return False
    # end if
    if term2_.parent == term1_.term_id:
        return True
    # end if
    return term_is_ancestor_of(term1_, get_term(term2_.parent, taxonomy_), taxonomy_)
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
def sanitize_term(term_=None, taxonomy_=None, context_="display", *_args_):
    
    
    fields_ = Array("term_id", "name", "description", "slug", "count", "parent", "term_group", "term_taxonomy_id", "object_id")
    do_object_ = php_is_object(term_)
    term_id_ = term_.term_id if do_object_ else term_["term_id"] if (php_isset(lambda : term_["term_id"])) else 0
    for field_ in fields_:
        if do_object_:
            if (php_isset(lambda : term_.field_)):
                term_.field_ = sanitize_term_field(field_, term_.field_, term_id_, taxonomy_, context_)
            # end if
        else:
            if (php_isset(lambda : term_[field_])):
                term_[field_] = sanitize_term_field(field_, term_[field_], term_id_, taxonomy_, context_)
            # end if
        # end if
    # end for
    if do_object_:
        term_.filter = context_
    else:
        term_["filter"] = context_
    # end if
    return term_
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
def sanitize_term_field(field_=None, value_=None, term_id_=None, taxonomy_=None, context_=None, *_args_):
    
    
    int_fields_ = Array("parent", "term_id", "count", "term_group", "term_taxonomy_id", "object_id")
    if php_in_array(field_, int_fields_):
        value_ = php_int(value_)
        if value_ < 0:
            value_ = 0
        # end if
    # end if
    context_ = php_strtolower(context_)
    if "raw" == context_:
        return value_
    # end if
    if "edit" == context_:
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
        value_ = apply_filters(str("edit_term_") + str(field_), value_, term_id_, taxonomy_)
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
        value_ = apply_filters(str("edit_") + str(taxonomy_) + str("_") + str(field_), value_, term_id_)
        if "description" == field_:
            value_ = esc_html(value_)
            pass
        else:
            value_ = esc_attr(value_)
        # end if
    elif "db" == context_:
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
        value_ = apply_filters(str("pre_term_") + str(field_), value_, taxonomy_)
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
        value_ = apply_filters(str("pre_") + str(taxonomy_) + str("_") + str(field_), value_)
        #// Back compat filters.
        if "slug" == field_:
            #// 
            #// Filters the category nicename before it is sanitized.
            #// 
            #// Use the {@see 'pre_$taxonomy_$field'} hook instead.
            #// 
            #// @since 2.0.3
            #// 
            #// @param string $value The category nicename.
            #//
            value_ = apply_filters("pre_category_nicename", value_)
        # end if
    elif "rss" == context_:
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
        value_ = apply_filters(str("term_") + str(field_) + str("_rss"), value_, taxonomy_)
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
        value_ = apply_filters(str(taxonomy_) + str("_") + str(field_) + str("_rss"), value_)
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
        value_ = apply_filters(str("term_") + str(field_), value_, term_id_, taxonomy_, context_)
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
        value_ = apply_filters(str(taxonomy_) + str("_") + str(field_), value_, term_id_, context_)
    # end if
    if "attribute" == context_:
        value_ = esc_attr(value_)
    elif "js" == context_:
        value_ = esc_js(value_)
    # end if
    return value_
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
def wp_count_terms(taxonomy_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    defaults_ = Array({"taxonomy": taxonomy_, "hide_empty": False})
    args_ = wp_parse_args(args_, defaults_)
    #// Backward compatibility.
    if (php_isset(lambda : args_["ignore_empty"])):
        args_["hide_empty"] = args_["ignore_empty"]
        args_["ignore_empty"] = None
    # end if
    args_["fields"] = "count"
    return get_terms(args_)
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
def wp_delete_object_term_relationships(object_id_=None, taxonomies_=None, *_args_):
    
    
    object_id_ = php_int(object_id_)
    if (not php_is_array(taxonomies_)):
        taxonomies_ = Array(taxonomies_)
    # end if
    for taxonomy_ in taxonomies_:
        term_ids_ = wp_get_object_terms(object_id_, taxonomy_, Array({"fields": "ids"}))
        term_ids_ = php_array_map("intval", term_ids_)
        wp_remove_object_terms(object_id_, term_ids_, taxonomy_)
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
def wp_delete_term(term_=None, taxonomy_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    term_ = php_int(term_)
    ids_ = term_exists(term_, taxonomy_)
    if (not ids_):
        return False
    # end if
    if is_wp_error(ids_):
        return ids_
    # end if
    tt_id_ = ids_["term_taxonomy_id"]
    defaults_ = Array()
    if "category" == taxonomy_:
        defaults_["default"] = php_int(get_option("default_category"))
        if defaults_["default"] == term_:
            return 0
            pass
        # end if
    # end if
    args_ = wp_parse_args(args_, defaults_)
    if (php_isset(lambda : args_["default"])):
        default_ = php_int(args_["default"])
        if (not term_exists(default_, taxonomy_)):
            default_ = None
        # end if
    # end if
    if (php_isset(lambda : args_["force_default"])):
        force_default_ = args_["force_default"]
    # end if
    #// 
    #// Fires when deleting a term, before any modifications are made to posts or terms.
    #// 
    #// @since 4.1.0
    #// 
    #// @param int    $term     Term ID.
    #// @param string $taxonomy Taxonomy Name.
    #//
    do_action("pre_delete_term", term_, taxonomy_)
    #// Update children to point to new parent.
    if is_taxonomy_hierarchical(taxonomy_):
        term_obj_ = get_term(term_, taxonomy_)
        if is_wp_error(term_obj_):
            return term_obj_
        # end if
        parent_ = term_obj_.parent
        edit_ids_ = wpdb_.get_results(str("SELECT term_id, term_taxonomy_id FROM ") + str(wpdb_.term_taxonomy) + str(" WHERE `parent` = ") + php_int(term_obj_.term_id))
        edit_tt_ids_ = wp_list_pluck(edit_ids_, "term_taxonomy_id")
        #// 
        #// Fires immediately before a term to delete's children are reassigned a parent.
        #// 
        #// @since 2.9.0
        #// 
        #// @param array $edit_tt_ids An array of term taxonomy IDs for the given term.
        #//
        do_action("edit_term_taxonomies", edit_tt_ids_)
        wpdb_.update(wpdb_.term_taxonomy, php_compact("parent_"), Array({"parent": term_obj_.term_id}) + php_compact("taxonomy_"))
        #// Clean the cache for all child terms.
        edit_term_ids_ = wp_list_pluck(edit_ids_, "term_id")
        clean_term_cache(edit_term_ids_, taxonomy_)
        #// 
        #// Fires immediately after a term to delete's children are reassigned a parent.
        #// 
        #// @since 2.9.0
        #// 
        #// @param array $edit_tt_ids An array of term taxonomy IDs for the given term.
        #//
        do_action("edited_term_taxonomies", edit_tt_ids_)
    # end if
    #// Get the term before deleting it or its term relationships so we can pass to actions below.
    deleted_term_ = get_term(term_, taxonomy_)
    object_ids_ = wpdb_.get_col(wpdb_.prepare(str("SELECT object_id FROM ") + str(wpdb_.term_relationships) + str(" WHERE term_taxonomy_id = %d"), tt_id_))
    for object_id_ in object_ids_:
        terms_ = wp_get_object_terms(object_id_, taxonomy_, Array({"fields": "ids", "orderby": "none"}))
        if 1 == php_count(terms_) and (php_isset(lambda : default_)):
            terms_ = Array(default_)
        else:
            terms_ = php_array_diff(terms_, Array(term_))
            if (php_isset(lambda : default_)) and (php_isset(lambda : force_default_)) and force_default_:
                terms_ = php_array_merge(terms_, Array(default_))
            # end if
        # end if
        terms_ = php_array_map("intval", terms_)
        wp_set_object_terms(object_id_, terms_, taxonomy_)
    # end for
    #// Clean the relationship caches for all object types using this term.
    tax_object_ = get_taxonomy(taxonomy_)
    for object_type_ in tax_object_.object_type:
        clean_object_term_cache(object_ids_, object_type_)
    # end for
    term_meta_ids_ = wpdb_.get_col(wpdb_.prepare(str("SELECT meta_id FROM ") + str(wpdb_.termmeta) + str(" WHERE term_id = %d "), term_))
    for mid_ in term_meta_ids_:
        delete_metadata_by_mid("term", mid_)
    # end for
    #// 
    #// Fires immediately before a term taxonomy ID is deleted.
    #// 
    #// @since 2.9.0
    #// 
    #// @param int $tt_id Term taxonomy ID.
    #//
    do_action("delete_term_taxonomy", tt_id_)
    wpdb_.delete(wpdb_.term_taxonomy, Array({"term_taxonomy_id": tt_id_}))
    #// 
    #// Fires immediately after a term taxonomy ID is deleted.
    #// 
    #// @since 2.9.0
    #// 
    #// @param int $tt_id Term taxonomy ID.
    #//
    do_action("deleted_term_taxonomy", tt_id_)
    #// Delete the term if no taxonomies use it.
    if (not wpdb_.get_var(wpdb_.prepare(str("SELECT COUNT(*) FROM ") + str(wpdb_.term_taxonomy) + str(" WHERE term_id = %d"), term_))):
        wpdb_.delete(wpdb_.terms, Array({"term_id": term_}))
    # end if
    clean_term_cache(term_, taxonomy_)
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
    do_action("delete_term", term_, tt_id_, taxonomy_, deleted_term_, object_ids_)
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
    do_action(str("delete_") + str(taxonomy_), term_, tt_id_, deleted_term_, object_ids_)
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
def wp_delete_category(cat_ID_=None, *_args_):
    
    
    return wp_delete_term(cat_ID_, "category")
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
def wp_get_object_terms(object_ids_=None, taxonomies_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    if php_empty(lambda : object_ids_) or php_empty(lambda : taxonomies_):
        return Array()
    # end if
    if (not php_is_array(taxonomies_)):
        taxonomies_ = Array(taxonomies_)
    # end if
    for taxonomy_ in taxonomies_:
        if (not taxonomy_exists(taxonomy_)):
            return php_new_class("WP_Error", lambda : WP_Error("invalid_taxonomy", __("Invalid taxonomy.")))
        # end if
    # end for
    if (not php_is_array(object_ids_)):
        object_ids_ = Array(object_ids_)
    # end if
    object_ids_ = php_array_map("intval", object_ids_)
    args_ = wp_parse_args(args_)
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
    args_ = apply_filters("wp_get_object_terms_args", args_, object_ids_, taxonomies_)
    #// 
    #// When one or more queried taxonomies is registered with an 'args' array,
    #// those params override the `$args` passed to this function.
    #//
    terms_ = Array()
    if php_count(taxonomies_) > 1:
        for index_,taxonomy_ in taxonomies_.items():
            t_ = get_taxonomy(taxonomy_)
            if (php_isset(lambda : t_.args)) and php_is_array(t_.args) and php_array_merge(args_, t_.args) != args_:
                taxonomies_[index_] = None
                terms_ = php_array_merge(terms_, wp_get_object_terms(object_ids_, taxonomy_, php_array_merge(args_, t_.args)))
            # end if
        # end for
    else:
        t_ = get_taxonomy(taxonomies_[0])
        if (php_isset(lambda : t_.args)) and php_is_array(t_.args):
            args_ = php_array_merge(args_, t_.args)
        # end if
    # end if
    args_["taxonomy"] = taxonomies_
    args_["object_ids"] = object_ids_
    #// Taxonomies registered without an 'args' param are handled here.
    if (not php_empty(lambda : taxonomies_)):
        terms_from_remaining_taxonomies_ = get_terms(args_)
        #// Array keys should be preserved for values of $fields that use term_id for keys.
        if (not php_empty(lambda : args_["fields"])) and 0 == php_strpos(args_["fields"], "id=>"):
            terms_ = terms_ + terms_from_remaining_taxonomies_
        else:
            terms_ = php_array_merge(terms_, terms_from_remaining_taxonomies_)
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
    terms_ = apply_filters("get_object_terms", terms_, object_ids_, taxonomies_, args_)
    object_ids_ = php_implode(",", object_ids_)
    taxonomies_ = "'" + php_implode("', '", php_array_map("esc_sql", taxonomies_)) + "'"
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
    return apply_filters("wp_get_object_terms", terms_, object_ids_, taxonomies_, args_)
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
def wp_insert_term(term_=None, taxonomy_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if (not taxonomy_exists(taxonomy_)):
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
    term_ = apply_filters("pre_insert_term", term_, taxonomy_)
    if is_wp_error(term_):
        return term_
    # end if
    if php_is_int(term_) and 0 == term_:
        return php_new_class("WP_Error", lambda : WP_Error("invalid_term_id", __("Invalid term ID.")))
    # end if
    if "" == php_trim(term_):
        return php_new_class("WP_Error", lambda : WP_Error("empty_term_name", __("A name is required for this term.")))
    # end if
    defaults_ = Array({"alias_of": "", "description": "", "parent": 0, "slug": ""})
    args_ = wp_parse_args(args_, defaults_)
    if args_["parent"] > 0 and (not term_exists(php_int(args_["parent"]))):
        return php_new_class("WP_Error", lambda : WP_Error("missing_parent", __("Parent term does not exist.")))
    # end if
    args_["name"] = term_
    args_["taxonomy"] = taxonomy_
    #// Coerce null description to strings, to avoid database errors.
    args_["description"] = php_str(args_["description"])
    args_ = sanitize_term(args_, taxonomy_, "db")
    #// expected_slashed ($name)
    name_ = wp_unslash(args_["name"])
    description_ = wp_unslash(args_["description"])
    parent_ = php_int(args_["parent"])
    slug_provided_ = (not php_empty(lambda : args_["slug"]))
    if (not slug_provided_):
        slug_ = sanitize_title(name_)
    else:
        slug_ = args_["slug"]
    # end if
    term_group_ = 0
    if args_["alias_of"]:
        alias_ = get_term_by("slug", args_["alias_of"], taxonomy_)
        if (not php_empty(lambda : alias_.term_group)):
            #// The alias we want is already in a group, so let's use that one.
            term_group_ = alias_.term_group
        elif (not php_empty(lambda : alias_.term_id)):
            #// 
            #// The alias is not in a group, so we create a new one
            #// and add the alias to it.
            #//
            term_group_ = wpdb_.get_var(str("SELECT MAX(term_group) FROM ") + str(wpdb_.terms)) + 1
            wp_update_term(alias_.term_id, taxonomy_, Array({"term_group": term_group_}))
        # end if
    # end if
    #// 
    #// Prevent the creation of terms with duplicate names at the same level of a taxonomy hierarchy,
    #// unless a unique slug has been explicitly provided.
    #//
    name_matches_ = get_terms(Array({"taxonomy": taxonomy_, "name": name_, "hide_empty": False, "parent": args_["parent"], "update_term_meta_cache": False}))
    #// 
    #// The `name` match in `get_terms()` doesn't differentiate accented characters,
    #// so we do a stricter comparison here.
    #//
    name_match_ = None
    if name_matches_:
        for _match_ in name_matches_:
            if php_strtolower(name_) == php_strtolower(_match_.name):
                name_match_ = _match_
                break
            # end if
        # end for
    # end if
    if name_match_:
        slug_match_ = get_term_by("slug", slug_, taxonomy_)
        if (not slug_provided_) or name_match_.slug == slug_ or slug_match_:
            if is_taxonomy_hierarchical(taxonomy_):
                siblings_ = get_terms(Array({"taxonomy": taxonomy_, "get": "all", "parent": parent_, "update_term_meta_cache": False}))
                existing_term_ = None
                if (not slug_provided_) or name_match_.slug == slug_ and php_in_array(name_, wp_list_pluck(siblings_, "name")):
                    existing_term_ = name_match_
                elif slug_match_ and php_in_array(slug_, wp_list_pluck(siblings_, "slug")):
                    existing_term_ = slug_match_
                # end if
                if existing_term_:
                    return php_new_class("WP_Error", lambda : WP_Error("term_exists", __("A term with the name provided already exists with this parent."), existing_term_.term_id))
                # end if
            else:
                return php_new_class("WP_Error", lambda : WP_Error("term_exists", __("A term with the name provided already exists in this taxonomy."), name_match_.term_id))
            # end if
        # end if
    # end if
    slug_ = wp_unique_term_slug(slug_, args_)
    data_ = php_compact("name_", "slug_", "term_group_")
    #// 
    #// Filters term data before it is inserted into the database.
    #// 
    #// @since 4.7.0
    #// 
    #// @param array  $data     Term data to be inserted.
    #// @param string $taxonomy Taxonomy slug.
    #// @param array  $args     Arguments passed to wp_insert_term().
    #//
    data_ = apply_filters("wp_insert_term_data", data_, taxonomy_, args_)
    if False == wpdb_.insert(wpdb_.terms, data_):
        return php_new_class("WP_Error", lambda : WP_Error("db_insert_error", __("Could not insert term into the database."), wpdb_.last_error))
    # end if
    term_id_ = php_int(wpdb_.insert_id)
    #// Seems unreachable. However, is used in the case that a term name is provided, which sanitizes to an empty string.
    if php_empty(lambda : slug_):
        slug_ = sanitize_title(slug_, term_id_)
        #// This action is documented in wp-includes/taxonomy.php
        do_action("edit_terms", term_id_, taxonomy_)
        wpdb_.update(wpdb_.terms, php_compact("slug_"), php_compact("term_id_"))
        #// This action is documented in wp-includes/taxonomy.php
        do_action("edited_terms", term_id_, taxonomy_)
    # end if
    tt_id_ = wpdb_.get_var(wpdb_.prepare(str("SELECT tt.term_taxonomy_id FROM ") + str(wpdb_.term_taxonomy) + str(" AS tt INNER JOIN ") + str(wpdb_.terms) + str(" AS t ON tt.term_id = t.term_id WHERE tt.taxonomy = %s AND t.term_id = %d"), taxonomy_, term_id_))
    if (not php_empty(lambda : tt_id_)):
        return Array({"term_id": term_id_, "term_taxonomy_id": tt_id_})
    # end if
    if False == wpdb_.insert(wpdb_.term_taxonomy, php_compact("term_id_", "taxonomy_", "description_", "parent_") + Array({"count": 0})):
        return php_new_class("WP_Error", lambda : WP_Error("db_insert_error", __("Could not insert term taxonomy into the database."), wpdb_.last_error))
    # end if
    tt_id_ = php_int(wpdb_.insert_id)
    #// 
    #// Sanity check: if we just created a term with the same parent + taxonomy + slug but a higher term_id than
    #// an existing term, then we have unwittingly created a duplicate term. Delete the dupe, and use the term_id
    #// and term_taxonomy_id of the older term instead. Then return out of the function so that the "create" hooks
    #// are not fired.
    #//
    duplicate_term_ = wpdb_.get_row(wpdb_.prepare(str("SELECT t.term_id, t.slug, tt.term_taxonomy_id, tt.taxonomy FROM ") + str(wpdb_.terms) + str(" t INNER JOIN ") + str(wpdb_.term_taxonomy) + str(" tt ON ( tt.term_id = t.term_id ) WHERE t.slug = %s AND tt.parent = %d AND tt.taxonomy = %s AND t.term_id < %d AND tt.term_taxonomy_id != %d"), slug_, parent_, taxonomy_, term_id_, tt_id_))
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
    duplicate_term_ = apply_filters("wp_insert_term_duplicate_term_check", duplicate_term_, term_, taxonomy_, args_, tt_id_)
    if duplicate_term_:
        wpdb_.delete(wpdb_.terms, Array({"term_id": term_id_}))
        wpdb_.delete(wpdb_.term_taxonomy, Array({"term_taxonomy_id": tt_id_}))
        term_id_ = php_int(duplicate_term_.term_id)
        tt_id_ = php_int(duplicate_term_.term_taxonomy_id)
        clean_term_cache(term_id_, taxonomy_)
        return Array({"term_id": term_id_, "term_taxonomy_id": tt_id_})
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
    do_action("create_term", term_id_, tt_id_, taxonomy_)
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
    do_action(str("create_") + str(taxonomy_), term_id_, tt_id_)
    #// 
    #// Filters the term ID after a new term is created.
    #// 
    #// @since 2.3.0
    #// 
    #// @param int $term_id Term ID.
    #// @param int $tt_id   Taxonomy term ID.
    #//
    term_id_ = apply_filters("term_id_filter", term_id_, tt_id_)
    clean_term_cache(term_id_, taxonomy_)
    #// 
    #// Fires after a new term is created, and after the term cache has been cleaned.
    #// 
    #// @since 2.3.0
    #// 
    #// @param int    $term_id  Term ID.
    #// @param int    $tt_id    Term taxonomy ID.
    #// @param string $taxonomy Taxonomy slug.
    #//
    do_action("created_term", term_id_, tt_id_, taxonomy_)
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
    do_action(str("created_") + str(taxonomy_), term_id_, tt_id_)
    return Array({"term_id": term_id_, "term_taxonomy_id": tt_id_})
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
def wp_set_object_terms(object_id_=None, terms_=None, taxonomy_=None, append_=None, *_args_):
    if append_ is None:
        append_ = False
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    object_id_ = php_int(object_id_)
    if (not taxonomy_exists(taxonomy_)):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_taxonomy", __("Invalid taxonomy.")))
    # end if
    if (not php_is_array(terms_)):
        terms_ = Array(terms_)
    # end if
    if (not append_):
        old_tt_ids_ = wp_get_object_terms(object_id_, taxonomy_, Array({"fields": "tt_ids", "orderby": "none", "update_term_meta_cache": False}))
    else:
        old_tt_ids_ = Array()
    # end if
    tt_ids_ = Array()
    term_ids_ = Array()
    new_tt_ids_ = Array()
    for term_ in terms_:
        if "" == php_trim(term_):
            continue
        # end if
        term_info_ = term_exists(term_, taxonomy_)
        if (not term_info_):
            #// Skip if a non-existent term ID is passed.
            if php_is_int(term_):
                continue
            # end if
            term_info_ = wp_insert_term(term_, taxonomy_)
        # end if
        if is_wp_error(term_info_):
            return term_info_
        # end if
        term_ids_[-1] = term_info_["term_id"]
        tt_id_ = term_info_["term_taxonomy_id"]
        tt_ids_[-1] = tt_id_
        if wpdb_.get_var(wpdb_.prepare(str("SELECT term_taxonomy_id FROM ") + str(wpdb_.term_relationships) + str(" WHERE object_id = %d AND term_taxonomy_id = %d"), object_id_, tt_id_)):
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
        do_action("add_term_relationship", object_id_, tt_id_, taxonomy_)
        wpdb_.insert(wpdb_.term_relationships, Array({"object_id": object_id_, "term_taxonomy_id": tt_id_}))
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
        do_action("added_term_relationship", object_id_, tt_id_, taxonomy_)
        new_tt_ids_[-1] = tt_id_
    # end for
    if new_tt_ids_:
        wp_update_term_count(new_tt_ids_, taxonomy_)
    # end if
    if (not append_):
        delete_tt_ids_ = php_array_diff(old_tt_ids_, tt_ids_)
        if delete_tt_ids_:
            in_delete_tt_ids_ = "'" + php_implode("', '", delete_tt_ids_) + "'"
            delete_term_ids_ = wpdb_.get_col(wpdb_.prepare(str("SELECT tt.term_id FROM ") + str(wpdb_.term_taxonomy) + str(" AS tt WHERE tt.taxonomy = %s AND tt.term_taxonomy_id IN (") + str(in_delete_tt_ids_) + str(")"), taxonomy_))
            delete_term_ids_ = php_array_map("intval", delete_term_ids_)
            remove_ = wp_remove_object_terms(object_id_, delete_term_ids_, taxonomy_)
            if is_wp_error(remove_):
                return remove_
            # end if
        # end if
    # end if
    t_ = get_taxonomy(taxonomy_)
    if (not append_) and (php_isset(lambda : t_.sort)) and t_.sort:
        values_ = Array()
        term_order_ = 0
        final_tt_ids_ = wp_get_object_terms(object_id_, taxonomy_, Array({"fields": "tt_ids", "update_term_meta_cache": False}))
        for tt_id_ in tt_ids_:
            if php_in_array(tt_id_, final_tt_ids_):
                term_order_ += 1
                term_order_ += 1
                values_[-1] = wpdb_.prepare("(%d, %d, %d)", object_id_, tt_id_, term_order_)
            # end if
        # end for
        if values_:
            if False == wpdb_.query(str("INSERT INTO ") + str(wpdb_.term_relationships) + str(" (object_id, term_taxonomy_id, term_order) VALUES ") + join(",", values_) + " ON DUPLICATE KEY UPDATE term_order = VALUES(term_order)"):
                return php_new_class("WP_Error", lambda : WP_Error("db_insert_error", __("Could not insert term relationship into the database."), wpdb_.last_error))
            # end if
        # end if
    # end if
    wp_cache_delete(object_id_, taxonomy_ + "_relationships")
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
    do_action("set_object_terms", object_id_, terms_, tt_ids_, taxonomy_, append_, old_tt_ids_)
    return tt_ids_
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
def wp_add_object_terms(object_id_=None, terms_=None, taxonomy_=None, *_args_):
    
    
    return wp_set_object_terms(object_id_, terms_, taxonomy_, True)
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
def wp_remove_object_terms(object_id_=None, terms_=None, taxonomy_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    object_id_ = php_int(object_id_)
    if (not taxonomy_exists(taxonomy_)):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_taxonomy", __("Invalid taxonomy.")))
    # end if
    if (not php_is_array(terms_)):
        terms_ = Array(terms_)
    # end if
    tt_ids_ = Array()
    for term_ in terms_:
        if "" == php_trim(term_):
            continue
        # end if
        term_info_ = term_exists(term_, taxonomy_)
        if (not term_info_):
            #// Skip if a non-existent term ID is passed.
            if php_is_int(term_):
                continue
            # end if
        # end if
        if is_wp_error(term_info_):
            return term_info_
        # end if
        tt_ids_[-1] = term_info_["term_taxonomy_id"]
    # end for
    if tt_ids_:
        in_tt_ids_ = "'" + php_implode("', '", tt_ids_) + "'"
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
        do_action("delete_term_relationships", object_id_, tt_ids_, taxonomy_)
        deleted_ = wpdb_.query(wpdb_.prepare(str("DELETE FROM ") + str(wpdb_.term_relationships) + str(" WHERE object_id = %d AND term_taxonomy_id IN (") + str(in_tt_ids_) + str(")"), object_id_))
        wp_cache_delete(object_id_, taxonomy_ + "_relationships")
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
        do_action("deleted_term_relationships", object_id_, tt_ids_, taxonomy_)
        wp_update_term_count(tt_ids_, taxonomy_)
        return php_bool(deleted_)
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
def wp_unique_term_slug(slug_=None, term_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    needs_suffix_ = True
    original_slug_ = slug_
    #// As of 4.1, duplicate slugs are allowed as long as they're in different taxonomies.
    if (not term_exists(slug_)) or get_option("db_version") >= 30133 and (not get_term_by("slug", slug_, term_.taxonomy)):
        needs_suffix_ = False
    # end if
    #// 
    #// If the taxonomy supports hierarchy and the term has a parent, make the slug unique
    #// by incorporating parent slugs.
    #//
    parent_suffix_ = ""
    if needs_suffix_ and is_taxonomy_hierarchical(term_.taxonomy) and (not php_empty(lambda : term_.parent)):
        the_parent_ = term_.parent
        while True:
            
            if not ((not php_empty(lambda : the_parent_))):
                break
            # end if
            parent_term_ = get_term(the_parent_, term_.taxonomy)
            if is_wp_error(parent_term_) or php_empty(lambda : parent_term_):
                break
            # end if
            parent_suffix_ += "-" + parent_term_.slug
            if (not term_exists(slug_ + parent_suffix_)):
                break
            # end if
            if php_empty(lambda : parent_term_.parent):
                break
            # end if
            the_parent_ = parent_term_.parent
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
    if apply_filters("wp_unique_term_slug_is_bad_slug", needs_suffix_, slug_, term_):
        if parent_suffix_:
            slug_ += parent_suffix_
        # end if
        if (not php_empty(lambda : term_.term_id)):
            query_ = wpdb_.prepare(str("SELECT slug FROM ") + str(wpdb_.terms) + str(" WHERE slug = %s AND term_id != %d"), slug_, term_.term_id)
        else:
            query_ = wpdb_.prepare(str("SELECT slug FROM ") + str(wpdb_.terms) + str(" WHERE slug = %s"), slug_)
        # end if
        if wpdb_.get_var(query_):
            #// phpcs:ignore WordPress.DB.PreparedSQL.NotPrepared
            num_ = 2
            while True:
                alt_slug_ = slug_ + str("-") + str(num_)
                num_ += 1
                slug_check_ = wpdb_.get_var(wpdb_.prepare(str("SELECT slug FROM ") + str(wpdb_.terms) + str(" WHERE slug = %s"), alt_slug_))
                
                if slug_check_:
                    break
                # end if
            # end while
            slug_ = alt_slug_
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
    return apply_filters("wp_unique_term_slug", slug_, term_, original_slug_)
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
def wp_update_term(term_id_=None, taxonomy_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if (not taxonomy_exists(taxonomy_)):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_taxonomy", __("Invalid taxonomy.")))
    # end if
    term_id_ = php_int(term_id_)
    #// First, get all of the original args.
    term_ = get_term(term_id_, taxonomy_)
    if is_wp_error(term_):
        return term_
    # end if
    if (not term_):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_term", __("Empty Term.")))
    # end if
    term_ = term_.data
    #// Escape data pulled from DB.
    term_ = wp_slash(term_)
    #// Merge old and new args with new args overwriting old ones.
    args_ = php_array_merge(term_, args_)
    defaults_ = Array({"alias_of": "", "description": "", "parent": 0, "slug": ""})
    args_ = wp_parse_args(args_, defaults_)
    args_ = sanitize_term(args_, taxonomy_, "db")
    parsed_args_ = args_
    #// expected_slashed ($name)
    name_ = wp_unslash(args_["name"])
    description_ = wp_unslash(args_["description"])
    parsed_args_["name"] = name_
    parsed_args_["description"] = description_
    if "" == php_trim(name_):
        return php_new_class("WP_Error", lambda : WP_Error("empty_term_name", __("A name is required for this term.")))
    # end if
    if parsed_args_["parent"] > 0 and (not term_exists(php_int(parsed_args_["parent"]))):
        return php_new_class("WP_Error", lambda : WP_Error("missing_parent", __("Parent term does not exist.")))
    # end if
    empty_slug_ = False
    if php_empty(lambda : args_["slug"]):
        empty_slug_ = True
        slug_ = sanitize_title(name_)
    else:
        slug_ = args_["slug"]
    # end if
    parsed_args_["slug"] = slug_
    term_group_ = parsed_args_["term_group"] if (php_isset(lambda : parsed_args_["term_group"])) else 0
    if args_["alias_of"]:
        alias_ = get_term_by("slug", args_["alias_of"], taxonomy_)
        if (not php_empty(lambda : alias_.term_group)):
            #// The alias we want is already in a group, so let's use that one.
            term_group_ = alias_.term_group
        elif (not php_empty(lambda : alias_.term_id)):
            #// 
            #// The alias is not in a group, so we create a new one
            #// and add the alias to it.
            #//
            term_group_ = wpdb_.get_var(str("SELECT MAX(term_group) FROM ") + str(wpdb_.terms)) + 1
            wp_update_term(alias_.term_id, taxonomy_, Array({"term_group": term_group_}))
        # end if
        parsed_args_["term_group"] = term_group_
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
    parent_ = php_int(apply_filters("wp_update_term_parent", args_["parent"], term_id_, taxonomy_, parsed_args_, args_))
    #// Check for duplicate slug.
    duplicate_ = get_term_by("slug", slug_, taxonomy_)
    if duplicate_ and duplicate_.term_id != term_id_:
        #// If an empty slug was passed or the parent changed, reset the slug to something unique.
        #// Otherwise, bail.
        if empty_slug_ or parent_ != php_int(term_["parent"]):
            slug_ = wp_unique_term_slug(slug_, args_)
        else:
            #// translators: %s: Taxonomy term slug.
            return php_new_class("WP_Error", lambda : WP_Error("duplicate_term_slug", php_sprintf(__("The slug &#8220;%s&#8221; is already in use by another term."), slug_)))
        # end if
    # end if
    tt_id_ = php_int(wpdb_.get_var(wpdb_.prepare(str("SELECT tt.term_taxonomy_id FROM ") + str(wpdb_.term_taxonomy) + str(" AS tt INNER JOIN ") + str(wpdb_.terms) + str(" AS t ON tt.term_id = t.term_id WHERE tt.taxonomy = %s AND t.term_id = %d"), taxonomy_, term_id_)))
    #// Check whether this is a shared term that needs splitting.
    _term_id_ = _split_shared_term(term_id_, tt_id_)
    if (not is_wp_error(_term_id_)):
        term_id_ = _term_id_
    # end if
    #// 
    #// Fires immediately before the given terms are edited.
    #// 
    #// @since 2.9.0
    #// 
    #// @param int    $term_id  Term ID.
    #// @param string $taxonomy Taxonomy slug.
    #//
    do_action("edit_terms", term_id_, taxonomy_)
    data_ = php_compact("name_", "slug_", "term_group_")
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
    data_ = apply_filters("wp_update_term_data", data_, term_id_, taxonomy_, args_)
    wpdb_.update(wpdb_.terms, data_, php_compact("term_id_"))
    if php_empty(lambda : slug_):
        slug_ = sanitize_title(name_, term_id_)
        wpdb_.update(wpdb_.terms, php_compact("slug_"), php_compact("term_id_"))
    # end if
    #// 
    #// Fires immediately after the given terms are edited.
    #// 
    #// @since 2.9.0
    #// 
    #// @param int    $term_id  Term ID
    #// @param string $taxonomy Taxonomy slug.
    #//
    do_action("edited_terms", term_id_, taxonomy_)
    #// 
    #// Fires immediate before a term-taxonomy relationship is updated.
    #// 
    #// @since 2.9.0
    #// 
    #// @param int    $tt_id    Term taxonomy ID.
    #// @param string $taxonomy Taxonomy slug.
    #//
    do_action("edit_term_taxonomy", tt_id_, taxonomy_)
    wpdb_.update(wpdb_.term_taxonomy, php_compact("term_id_", "taxonomy_", "description_", "parent_"), Array({"term_taxonomy_id": tt_id_}))
    #// 
    #// Fires immediately after a term-taxonomy relationship is updated.
    #// 
    #// @since 2.9.0
    #// 
    #// @param int    $tt_id    Term taxonomy ID.
    #// @param string $taxonomy Taxonomy slug.
    #//
    do_action("edited_term_taxonomy", tt_id_, taxonomy_)
    #// 
    #// Fires after a term has been updated, but before the term cache has been cleaned.
    #// 
    #// @since 2.3.0
    #// 
    #// @param int    $term_id  Term ID.
    #// @param int    $tt_id    Term taxonomy ID.
    #// @param string $taxonomy Taxonomy slug.
    #//
    do_action("edit_term", term_id_, tt_id_, taxonomy_)
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
    do_action(str("edit_") + str(taxonomy_), term_id_, tt_id_)
    #// This filter is documented in wp-includes/taxonomy.php
    term_id_ = apply_filters("term_id_filter", term_id_, tt_id_)
    clean_term_cache(term_id_, taxonomy_)
    #// 
    #// Fires after a term has been updated, and the term cache has been cleaned.
    #// 
    #// @since 2.3.0
    #// 
    #// @param int    $term_id  Term ID.
    #// @param int    $tt_id    Term taxonomy ID.
    #// @param string $taxonomy Taxonomy slug.
    #//
    do_action("edited_term", term_id_, tt_id_, taxonomy_)
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
    do_action(str("edited_") + str(taxonomy_), term_id_, tt_id_)
    return Array({"term_id": term_id_, "term_taxonomy_id": tt_id_})
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
def wp_defer_term_counting(defer_=None, *_args_):
    if defer_ is None:
        defer_ = None
    # end if
    
    _defer_ = False
    if php_is_bool(defer_):
        _defer_ = defer_
        #// Flush any deferred counts.
        if (not defer_):
            wp_update_term_count(None, None, True)
        # end if
    # end if
    return _defer_
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
def wp_update_term_count(terms_=None, taxonomy_=None, do_deferred_=None, *_args_):
    if do_deferred_ is None:
        do_deferred_ = False
    # end if
    
    _deferred_ = Array()
    if do_deferred_:
        for tax_ in php_array_keys(_deferred_):
            wp_update_term_count_now(_deferred_[tax_], tax_)
            _deferred_[tax_] = None
        # end for
    # end if
    if php_empty(lambda : terms_):
        return False
    # end if
    if (not php_is_array(terms_)):
        terms_ = Array(terms_)
    # end if
    if wp_defer_term_counting():
        if (not (php_isset(lambda : _deferred_[taxonomy_]))):
            _deferred_[taxonomy_] = Array()
        # end if
        _deferred_[taxonomy_] = array_unique(php_array_merge(_deferred_[taxonomy_], terms_))
        return True
    # end if
    return wp_update_term_count_now(terms_, taxonomy_)
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
def wp_update_term_count_now(terms_=None, taxonomy_=None, *_args_):
    
    
    terms_ = php_array_map("intval", terms_)
    taxonomy_ = get_taxonomy(taxonomy_)
    if (not php_empty(lambda : taxonomy_.update_count_callback)):
        php_call_user_func(taxonomy_.update_count_callback, terms_, taxonomy_)
    else:
        object_types_ = taxonomy_.object_type
        for object_type_ in object_types_:
            if 0 == php_strpos(object_type_, "attachment:"):
                object_type_ = php_explode(":", object_type_)
            # end if
        # end for
        if php_array_filter(object_types_, "post_type_exists") == object_types_:
            #// Only post types are attached to this taxonomy.
            _update_post_term_count(terms_, taxonomy_)
        else:
            #// Default count updater.
            _update_generic_term_count(terms_, taxonomy_)
        # end if
    # end if
    clean_term_cache(terms_, "", False)
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
def clean_object_term_cache(object_ids_=None, object_type_=None, *_args_):
    
    
    global _wp_suspend_cache_invalidation_
    php_check_if_defined("_wp_suspend_cache_invalidation_")
    if (not php_empty(lambda : _wp_suspend_cache_invalidation_)):
        return
    # end if
    if (not php_is_array(object_ids_)):
        object_ids_ = Array(object_ids_)
    # end if
    taxonomies_ = get_object_taxonomies(object_type_)
    for id_ in object_ids_:
        for taxonomy_ in taxonomies_:
            wp_cache_delete(id_, str(taxonomy_) + str("_relationships"))
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
    do_action("clean_object_term_cache", object_ids_, object_type_)
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
def clean_term_cache(ids_=None, taxonomy_="", clean_taxonomy_=None, *_args_):
    if clean_taxonomy_ is None:
        clean_taxonomy_ = True
    # end if
    
    global wpdb_
    global _wp_suspend_cache_invalidation_
    php_check_if_defined("wpdb_","_wp_suspend_cache_invalidation_")
    if (not php_empty(lambda : _wp_suspend_cache_invalidation_)):
        return
    # end if
    if (not php_is_array(ids_)):
        ids_ = Array(ids_)
    # end if
    taxonomies_ = Array()
    #// If no taxonomy, assume tt_ids.
    if php_empty(lambda : taxonomy_):
        tt_ids_ = php_array_map("intval", ids_)
        tt_ids_ = php_implode(", ", tt_ids_)
        terms_ = wpdb_.get_results(str("SELECT term_id, taxonomy FROM ") + str(wpdb_.term_taxonomy) + str(" WHERE term_taxonomy_id IN (") + str(tt_ids_) + str(")"))
        ids_ = Array()
        for term_ in terms_:
            taxonomies_[-1] = term_.taxonomy
            ids_[-1] = term_.term_id
            wp_cache_delete(term_.term_id, "terms")
        # end for
        taxonomies_ = array_unique(taxonomies_)
    else:
        taxonomies_ = Array(taxonomy_)
        for taxonomy_ in taxonomies_:
            for id_ in ids_:
                wp_cache_delete(id_, "terms")
            # end for
        # end for
    # end if
    for taxonomy_ in taxonomies_:
        if clean_taxonomy_:
            clean_taxonomy_cache(taxonomy_)
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
        do_action("clean_term_cache", ids_, taxonomy_, clean_taxonomy_)
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
def clean_taxonomy_cache(taxonomy_=None, *_args_):
    
    
    wp_cache_delete("all_ids", taxonomy_)
    wp_cache_delete("get", taxonomy_)
    #// Regenerate cached hierarchy.
    delete_option(str(taxonomy_) + str("_children"))
    _get_term_hierarchy(taxonomy_)
    #// 
    #// Fires after a taxonomy's caches have been cleaned.
    #// 
    #// @since 4.9.0
    #// 
    #// @param string $taxonomy Taxonomy slug.
    #//
    do_action("clean_taxonomy_cache", taxonomy_)
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
def get_object_term_cache(id_=None, taxonomy_=None, *_args_):
    
    
    _term_ids_ = wp_cache_get(id_, str(taxonomy_) + str("_relationships"))
    #// We leave the priming of relationship caches to upstream functions.
    if False == _term_ids_:
        return False
    # end if
    #// Backward compatibility for if a plugin is putting objects into the cache, rather than IDs.
    term_ids_ = Array()
    for term_id_ in _term_ids_:
        if php_is_numeric(term_id_):
            term_ids_[-1] = php_intval(term_id_)
        elif (php_isset(lambda : term_id_.term_id)):
            term_ids_[-1] = php_intval(term_id_.term_id)
        # end if
    # end for
    #// Fill the term objects.
    _prime_term_caches(term_ids_)
    terms_ = Array()
    for term_id_ in term_ids_:
        term_ = get_term(term_id_, taxonomy_)
        if is_wp_error(term_):
            return term_
        # end if
        terms_[-1] = term_
    # end for
    return terms_
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
def update_object_term_cache(object_ids_=None, object_type_=None, *_args_):
    
    
    if php_empty(lambda : object_ids_):
        return
    # end if
    if (not php_is_array(object_ids_)):
        object_ids_ = php_explode(",", object_ids_)
    # end if
    object_ids_ = php_array_map("intval", object_ids_)
    taxonomies_ = get_object_taxonomies(object_type_)
    ids_ = Array()
    for id_ in object_ids_:
        for taxonomy_ in taxonomies_:
            if False == wp_cache_get(id_, str(taxonomy_) + str("_relationships")):
                ids_[-1] = id_
                break
            # end if
        # end for
    # end for
    if php_empty(lambda : ids_):
        return False
    # end if
    terms_ = wp_get_object_terms(ids_, taxonomies_, Array({"fields": "all_with_object_id", "orderby": "name", "update_term_meta_cache": False}))
    object_terms_ = Array()
    for term_ in terms_:
        object_terms_[term_.object_id][term_.taxonomy][-1] = term_.term_id
    # end for
    for id_ in ids_:
        for taxonomy_ in taxonomies_:
            if (not (php_isset(lambda : object_terms_[id_][taxonomy_]))):
                if (not (php_isset(lambda : object_terms_[id_]))):
                    object_terms_[id_] = Array()
                # end if
                object_terms_[id_][taxonomy_] = Array()
            # end if
        # end for
    # end for
    for id_,value_ in object_terms_.items():
        for taxonomy_,terms_ in value_.items():
            wp_cache_add(id_, terms_, str(taxonomy_) + str("_relationships"))
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
def update_term_cache(terms_=None, taxonomy_="", *_args_):
    
    
    for term_ in terms_:
        #// Create a copy in case the array was passed by reference.
        _term_ = copy.deepcopy(term_)
        _term_.object_id = None
        wp_cache_add(term_.term_id, _term_, "terms")
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
def _get_term_hierarchy(taxonomy_=None, *_args_):
    
    
    if (not is_taxonomy_hierarchical(taxonomy_)):
        return Array()
    # end if
    children_ = get_option(str(taxonomy_) + str("_children"))
    if php_is_array(children_):
        return children_
    # end if
    children_ = Array()
    terms_ = get_terms(Array({"taxonomy": taxonomy_, "get": "all", "orderby": "id", "fields": "id=>parent", "update_term_meta_cache": False}))
    for term_id_,parent_ in terms_.items():
        if parent_ > 0:
            children_[parent_][-1] = term_id_
        # end if
    # end for
    update_option(str(taxonomy_) + str("_children"), children_)
    return children_
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
def _get_term_children(term_id_=None, terms_=None, taxonomy_=None, ancestors_=None, *_args_):
    if ancestors_ is None:
        ancestors_ = Array()
    # end if
    
    empty_array_ = Array()
    if php_empty(lambda : terms_):
        return empty_array_
    # end if
    term_id_ = php_int(term_id_)
    term_list_ = Array()
    has_children_ = _get_term_hierarchy(taxonomy_)
    if term_id_ and (not (php_isset(lambda : has_children_[term_id_]))):
        return empty_array_
    # end if
    #// Include the term itself in the ancestors array, so we can properly detect when a loop has occurred.
    if php_empty(lambda : ancestors_):
        ancestors_[term_id_] = 1
    # end if
    for term_ in terms_:
        use_id_ = False
        if (not php_is_object(term_)):
            term_ = get_term(term_, taxonomy_)
            if is_wp_error(term_):
                return term_
            # end if
            use_id_ = True
        # end if
        #// Don't recurse if we've already identified the term as a child - this indicates a loop.
        if (php_isset(lambda : ancestors_[term_.term_id])):
            continue
        # end if
        if php_int(term_.parent) == term_id_:
            if use_id_:
                term_list_[-1] = term_.term_id
            else:
                term_list_[-1] = term_
            # end if
            if (not (php_isset(lambda : has_children_[term_.term_id]))):
                continue
            # end if
            ancestors_[term_.term_id] = 1
            children_ = _get_term_children(term_.term_id, terms_, taxonomy_, ancestors_)
            if children_:
                term_list_ = php_array_merge(term_list_, children_)
            # end if
        # end if
    # end for
    return term_list_
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
def _pad_term_counts(terms_=None, taxonomy_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    #// This function only works for hierarchical taxonomies like post categories.
    if (not is_taxonomy_hierarchical(taxonomy_)):
        return
    # end if
    term_hier_ = _get_term_hierarchy(taxonomy_)
    if php_empty(lambda : term_hier_):
        return
    # end if
    term_items_ = Array()
    terms_by_id_ = Array()
    term_ids_ = Array()
    for key_,term_ in terms_.items():
        terms_by_id_[term_.term_id] = terms_[key_]
        term_ids_[term_.term_taxonomy_id] = term_.term_id
    # end for
    #// Get the object and term ids and stick them in a lookup table.
    tax_obj_ = get_taxonomy(taxonomy_)
    object_types_ = esc_sql(tax_obj_.object_type)
    results_ = wpdb_.get_results(str("SELECT object_id, term_taxonomy_id FROM ") + str(wpdb_.term_relationships) + str(" INNER JOIN ") + str(wpdb_.posts) + str(" ON object_id = ID WHERE term_taxonomy_id IN (") + php_implode(",", php_array_keys(term_ids_)) + ") AND post_type IN ('" + php_implode("', '", object_types_) + "') AND post_status = 'publish'")
    for row_ in results_:
        id_ = term_ids_[row_.term_taxonomy_id]
        term_items_[id_][row_.object_id] += 1
        term_items_[id_][row_.object_id] += 1
        term_items_[id_][row_.object_id] = term_items_[id_][row_.object_id] if (php_isset(lambda : term_items_[id_][row_.object_id])) else 1
    # end for
    #// Touch every ancestor's lookup row for each post in each term.
    for term_id_ in term_ids_:
        child_ = term_id_
        ancestors_ = Array()
        while True:
            parent_ = terms_by_id_[child_].parent
            if not ((not php_empty(lambda : terms_by_id_[child_])) and parent_):
                break
            # end if
            ancestors_[-1] = child_
            if (not php_empty(lambda : term_items_[term_id_])):
                for item_id_,touches_ in term_items_[term_id_].items():
                    term_items_[parent_][item_id_] += 1
                    term_items_[parent_][item_id_] += 1
                    term_items_[parent_][item_id_] += 1
                    term_items_[parent_][item_id_] = term_items_[parent_][item_id_] if (php_isset(lambda : term_items_[parent_][item_id_])) else 1
                # end for
            # end if
            child_ = parent_
            if php_in_array(parent_, ancestors_):
                break
            # end if
        # end while
    # end for
    #// Transfer the touched cells.
    for id_,items_ in term_items_.items():
        if (php_isset(lambda : terms_by_id_[id_])):
            terms_by_id_[id_].count = php_count(items_)
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
def _prime_term_caches(term_ids_=None, update_meta_cache_=None, *_args_):
    if update_meta_cache_ is None:
        update_meta_cache_ = True
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    non_cached_ids_ = _get_non_cached_ids(term_ids_, "terms")
    if (not php_empty(lambda : non_cached_ids_)):
        fresh_terms_ = wpdb_.get_results(php_sprintf(str("SELECT t.*, tt.* FROM ") + str(wpdb_.terms) + str(" AS t INNER JOIN ") + str(wpdb_.term_taxonomy) + str(" AS tt ON t.term_id = tt.term_id WHERE t.term_id IN (%s)"), join(",", php_array_map("intval", non_cached_ids_))))
        update_term_cache(fresh_terms_, update_meta_cache_)
        if update_meta_cache_:
            update_termmeta_cache(non_cached_ids_)
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
def _update_post_term_count(terms_=None, taxonomy_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    object_types_ = taxonomy_.object_type
    for object_type_ in object_types_:
        object_type_ = php_explode(":", object_type_)
    # end for
    object_types_ = array_unique(object_types_)
    check_attachments_ = php_array_search("attachment", object_types_)
    if False != check_attachments_:
        object_types_[check_attachments_] = None
        check_attachments_ = True
    # end if
    if object_types_:
        object_types_ = esc_sql(php_array_filter(object_types_, "post_type_exists"))
    # end if
    for term_ in terms_:
        count_ = 0
        #// Attachments can be 'inherit' status, we need to base count off the parent's status if so.
        if check_attachments_:
            count_ += php_int(wpdb_.get_var(wpdb_.prepare(str("SELECT COUNT(*) FROM ") + str(wpdb_.term_relationships) + str(", ") + str(wpdb_.posts) + str(" p1 WHERE p1.ID = ") + str(wpdb_.term_relationships) + str(".object_id AND ( post_status = 'publish' OR ( post_status = 'inherit' AND post_parent > 0 AND ( SELECT post_status FROM ") + str(wpdb_.posts) + str(" WHERE ID = p1.post_parent ) = 'publish' ) ) AND post_type = 'attachment' AND term_taxonomy_id = %d"), term_)))
        # end if
        if object_types_:
            #// phpcs:ignore WordPress.DB.PreparedSQLPlaceholders.QuotedDynamicPlaceholderGeneration
            count_ += php_int(wpdb_.get_var(wpdb_.prepare(str("SELECT COUNT(*) FROM ") + str(wpdb_.term_relationships) + str(", ") + str(wpdb_.posts) + str(" WHERE ") + str(wpdb_.posts) + str(".ID = ") + str(wpdb_.term_relationships) + str(".object_id AND post_status = 'publish' AND post_type IN ('") + php_implode("', '", object_types_) + "') AND term_taxonomy_id = %d", term_)))
        # end if
        #// This action is documented in wp-includes/taxonomy.php
        do_action("edit_term_taxonomy", term_, taxonomy_.name)
        wpdb_.update(wpdb_.term_taxonomy, php_compact("count_"), Array({"term_taxonomy_id": term_}))
        #// This action is documented in wp-includes/taxonomy.php
        do_action("edited_term_taxonomy", term_, taxonomy_.name)
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
def _update_generic_term_count(terms_=None, taxonomy_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    for term_ in terms_:
        count_ = wpdb_.get_var(wpdb_.prepare(str("SELECT COUNT(*) FROM ") + str(wpdb_.term_relationships) + str(" WHERE term_taxonomy_id = %d"), term_))
        #// This action is documented in wp-includes/taxonomy.php
        do_action("edit_term_taxonomy", term_, taxonomy_.name)
        wpdb_.update(wpdb_.term_taxonomy, php_compact("count_"), Array({"term_taxonomy_id": term_}))
        #// This action is documented in wp-includes/taxonomy.php
        do_action("edited_term_taxonomy", term_, taxonomy_.name)
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
def _split_shared_term(term_id_=None, term_taxonomy_id_=None, record_=None, *_args_):
    if record_ is None:
        record_ = True
    # end if
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if php_is_object(term_id_):
        shared_term_ = term_id_
        term_id_ = php_intval(shared_term_.term_id)
    # end if
    if php_is_object(term_taxonomy_id_):
        term_taxonomy_ = term_taxonomy_id_
        term_taxonomy_id_ = php_intval(term_taxonomy_.term_taxonomy_id)
    # end if
    #// If there are no shared term_taxonomy rows, there's nothing to do here.
    shared_tt_count_ = php_int(wpdb_.get_var(wpdb_.prepare(str("SELECT COUNT(*) FROM ") + str(wpdb_.term_taxonomy) + str(" tt WHERE tt.term_id = %d AND tt.term_taxonomy_id != %d"), term_id_, term_taxonomy_id_)))
    if (not shared_tt_count_):
        return term_id_
    # end if
    #// 
    #// Verify that the term_taxonomy_id passed to the function is actually associated with the term_id.
    #// If there's a mismatch, it may mean that the term is already split. Return the actual term_id from the db.
    #//
    check_term_id_ = php_int(wpdb_.get_var(wpdb_.prepare(str("SELECT term_id FROM ") + str(wpdb_.term_taxonomy) + str(" WHERE term_taxonomy_id = %d"), term_taxonomy_id_)))
    if check_term_id_ != term_id_:
        return check_term_id_
    # end if
    #// Pull up data about the currently shared slug, which we'll use to populate the new one.
    if php_empty(lambda : shared_term_):
        shared_term_ = wpdb_.get_row(wpdb_.prepare(str("SELECT t.* FROM ") + str(wpdb_.terms) + str(" t WHERE t.term_id = %d"), term_id_))
    # end if
    new_term_data_ = Array({"name": shared_term_.name, "slug": shared_term_.slug, "term_group": shared_term_.term_group})
    if False == wpdb_.insert(wpdb_.terms, new_term_data_):
        return php_new_class("WP_Error", lambda : WP_Error("db_insert_error", __("Could not split shared term."), wpdb_.last_error))
    # end if
    new_term_id_ = php_int(wpdb_.insert_id)
    #// Update the existing term_taxonomy to point to the newly created term.
    wpdb_.update(wpdb_.term_taxonomy, Array({"term_id": new_term_id_}), Array({"term_taxonomy_id": term_taxonomy_id_}))
    #// Reassign child terms to the new parent.
    if php_empty(lambda : term_taxonomy_):
        term_taxonomy_ = wpdb_.get_row(wpdb_.prepare(str("SELECT * FROM ") + str(wpdb_.term_taxonomy) + str(" WHERE term_taxonomy_id = %d"), term_taxonomy_id_))
    # end if
    children_tt_ids_ = wpdb_.get_col(wpdb_.prepare(str("SELECT term_taxonomy_id FROM ") + str(wpdb_.term_taxonomy) + str(" WHERE parent = %d AND taxonomy = %s"), term_id_, term_taxonomy_.taxonomy))
    if (not php_empty(lambda : children_tt_ids_)):
        for child_tt_id_ in children_tt_ids_:
            wpdb_.update(wpdb_.term_taxonomy, Array({"parent": new_term_id_}), Array({"term_taxonomy_id": child_tt_id_}))
            clean_term_cache(php_int(child_tt_id_), "", False)
        # end for
    else:
        #// If the term has no children, we must force its taxonomy cache to be rebuilt separately.
        clean_term_cache(new_term_id_, term_taxonomy_.taxonomy, False)
    # end if
    clean_term_cache(term_id_, term_taxonomy_.taxonomy, False)
    #// 
    #// Taxonomy cache clearing is delayed to avoid race conditions that may occur when
    #// regenerating the taxonomy's hierarchy tree.
    #//
    taxonomies_to_clean_ = Array(term_taxonomy_.taxonomy)
    #// Clean the cache for term taxonomies formerly shared with the current term.
    shared_term_taxonomies_ = wpdb_.get_col(wpdb_.prepare(str("SELECT taxonomy FROM ") + str(wpdb_.term_taxonomy) + str(" WHERE term_id = %d"), term_id_))
    taxonomies_to_clean_ = php_array_merge(taxonomies_to_clean_, shared_term_taxonomies_)
    for taxonomy_to_clean_ in taxonomies_to_clean_:
        clean_taxonomy_cache(taxonomy_to_clean_)
    # end for
    #// Keep a record of term_ids that have been split, keyed by old term_id. See wp_get_split_term().
    if record_:
        split_term_data_ = get_option("_split_terms", Array())
        if (not (php_isset(lambda : split_term_data_[term_id_]))):
            split_term_data_[term_id_] = Array()
        # end if
        split_term_data_[term_id_][term_taxonomy_.taxonomy] = new_term_id_
        update_option("_split_terms", split_term_data_)
    # end if
    #// If we've just split the final shared term, set the "finished" flag.
    shared_terms_exist_ = wpdb_.get_results(str("SELECT tt.term_id, t.*, count(*) as term_tt_count FROM ") + str(wpdb_.term_taxonomy) + str(" tt\n       LEFT JOIN ") + str(wpdb_.terms) + str(""" t ON t.term_id = tt.term_id\n         GROUP BY t.term_id\n        HAVING term_tt_count > 1\n      LIMIT 1"""))
    if (not shared_terms_exist_):
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
    do_action("split_shared_term", term_id_, new_term_id_, term_taxonomy_id_, term_taxonomy_.taxonomy)
    return new_term_id_
# end def _split_shared_term
#// 
#// Splits a batch of shared taxonomy terms.
#// 
#// @since 4.3.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#//
def _wp_batch_split_terms(*_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    lock_name_ = "term_split.lock"
    #// Try to lock.
    lock_result_ = wpdb_.query(wpdb_.prepare(str("INSERT IGNORE INTO `") + str(wpdb_.options) + str("` ( `option_name`, `option_value`, `autoload` ) VALUES (%s, %s, 'no') /* LOCK */"), lock_name_, time()))
    if (not lock_result_):
        lock_result_ = get_option(lock_name_)
        #// Bail if we were unable to create a lock, or if the existing lock is still valid.
        if (not lock_result_) or lock_result_ > time() - HOUR_IN_SECONDS:
            wp_schedule_single_event(time() + 5 * MINUTE_IN_SECONDS, "wp_split_shared_term_batch")
            return
        # end if
    # end if
    #// Update the lock, as by this point we've definitely got a lock, just need to fire the actions.
    update_option(lock_name_, time())
    #// Get a list of shared terms (those with more than one associated row in term_taxonomy).
    shared_terms_ = wpdb_.get_results(str("SELECT tt.term_id, t.*, count(*) as term_tt_count FROM ") + str(wpdb_.term_taxonomy) + str(" tt\n         LEFT JOIN ") + str(wpdb_.terms) + str(""" t ON t.term_id = tt.term_id\n         GROUP BY t.term_id\n        HAVING term_tt_count > 1\n      LIMIT 10"""))
    #// No more terms, we're done here.
    if (not shared_terms_):
        update_option("finished_splitting_shared_terms", True)
        delete_option(lock_name_)
        return
    # end if
    #// Shared terms found? We'll need to run this script again.
    wp_schedule_single_event(time() + 2 * MINUTE_IN_SECONDS, "wp_split_shared_term_batch")
    #// Rekey shared term array for faster lookups.
    _shared_terms_ = Array()
    for shared_term_ in shared_terms_:
        term_id_ = php_intval(shared_term_.term_id)
        _shared_terms_[term_id_] = shared_term_
    # end for
    shared_terms_ = _shared_terms_
    #// Get term taxonomy data for all shared terms.
    shared_term_ids_ = php_implode(",", php_array_keys(shared_terms_))
    shared_tts_ = wpdb_.get_results(str("SELECT * FROM ") + str(wpdb_.term_taxonomy) + str(" WHERE `term_id` IN (") + str(shared_term_ids_) + str(")"))
    #// Split term data recording is slow, so we do it just once, outside the loop.
    split_term_data_ = get_option("_split_terms", Array())
    skipped_first_term_ = Array()
    taxonomies_ = Array()
    for shared_tt_ in shared_tts_:
        term_id_ = php_intval(shared_tt_.term_id)
        #// Don't split the first tt belonging to a given term_id.
        if (not (php_isset(lambda : skipped_first_term_[term_id_]))):
            skipped_first_term_[term_id_] = 1
            continue
        # end if
        if (not (php_isset(lambda : split_term_data_[term_id_]))):
            split_term_data_[term_id_] = Array()
        # end if
        #// Keep track of taxonomies whose hierarchies need flushing.
        if (not (php_isset(lambda : taxonomies_[shared_tt_.taxonomy]))):
            taxonomies_[shared_tt_.taxonomy] = 1
        # end if
        #// Split the term.
        split_term_data_[term_id_][shared_tt_.taxonomy] = _split_shared_term(shared_terms_[term_id_], shared_tt_, False)
    # end for
    #// Rebuild the cached hierarchy for each affected taxonomy.
    for tax_ in php_array_keys(taxonomies_):
        delete_option(str(tax_) + str("_children"))
        _get_term_hierarchy(tax_)
    # end for
    update_option("_split_terms", split_term_data_)
    delete_option(lock_name_)
# end def _wp_batch_split_terms
#// 
#// In order to avoid the _wp_batch_split_terms() job being accidentally removed,
#// check that it's still scheduled while we haven't finished splitting terms.
#// 
#// @ignore
#// @since 4.3.0
#//
def _wp_check_for_scheduled_split_terms(*_args_):
    
    
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
def _wp_check_split_default_terms(term_id_=None, new_term_id_=None, term_taxonomy_id_=None, taxonomy_=None, *_args_):
    
    
    if "category" != taxonomy_:
        return
    # end if
    for option_ in Array("default_category", "default_link_category", "default_email_category"):
        if php_int(get_option(option_, -1)) == term_id_:
            update_option(option_, new_term_id_)
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
def _wp_check_split_terms_in_menus(term_id_=None, new_term_id_=None, term_taxonomy_id_=None, taxonomy_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    post_ids_ = wpdb_.get_col(wpdb_.prepare(str("SELECT m1.post_id\n        FROM ") + str(wpdb_.postmeta) + str(" AS m1\n           INNER JOIN ") + str(wpdb_.postmeta) + str(" AS m2 ON ( m2.post_id = m1.post_id )\n          INNER JOIN ") + str(wpdb_.postmeta) + str(""" AS m3 ON ( m3.post_id = m1.post_id )\n        WHERE ( m1.meta_key = '_menu_item_type' AND m1.meta_value = 'taxonomy' )\n          AND ( m2.meta_key = '_menu_item_object' AND m2.meta_value = %s )\n          AND ( m3.meta_key = '_menu_item_object_id' AND m3.meta_value = %d )"""), taxonomy_, term_id_))
    if post_ids_:
        for post_id_ in post_ids_:
            update_post_meta(post_id_, "_menu_item_object_id", new_term_id_, term_id_)
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
def _wp_check_split_nav_menu_terms(term_id_=None, new_term_id_=None, term_taxonomy_id_=None, taxonomy_=None, *_args_):
    
    
    if "nav_menu" != taxonomy_:
        return
    # end if
    #// Update menu locations.
    locations_ = get_nav_menu_locations()
    for location_,menu_id_ in locations_.items():
        if term_id_ == menu_id_:
            locations_[location_] = new_term_id_
        # end if
    # end for
    set_theme_mod("nav_menu_locations", locations_)
# end def _wp_check_split_nav_menu_terms
#// 
#// Get data about terms that previously shared a single term_id, but have since been split.
#// 
#// @since 4.2.0
#// 
#// @param int $old_term_id Term ID. This is the old, pre-split term ID.
#// @return array Array of new term IDs, keyed by taxonomy.
#//
def wp_get_split_terms(old_term_id_=None, *_args_):
    
    
    split_terms_ = get_option("_split_terms", Array())
    terms_ = Array()
    if (php_isset(lambda : split_terms_[old_term_id_])):
        terms_ = split_terms_[old_term_id_]
    # end if
    return terms_
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
def wp_get_split_term(old_term_id_=None, taxonomy_=None, *_args_):
    
    
    split_terms_ = wp_get_split_terms(old_term_id_)
    term_id_ = False
    if (php_isset(lambda : split_terms_[taxonomy_])):
        term_id_ = php_int(split_terms_[taxonomy_])
    # end if
    return term_id_
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
def wp_term_is_shared(term_id_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    if get_option("finished_splitting_shared_terms"):
        return False
    # end if
    tt_count_ = wpdb_.get_var(wpdb_.prepare(str("SELECT COUNT(*) FROM ") + str(wpdb_.term_taxonomy) + str(" WHERE term_id = %d"), term_id_))
    return tt_count_ > 1
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
def get_term_link(term_=None, taxonomy_="", *_args_):
    
    
    global wp_rewrite_
    php_check_if_defined("wp_rewrite_")
    if (not php_is_object(term_)):
        if php_is_int(term_):
            term_ = get_term(term_, taxonomy_)
        else:
            term_ = get_term_by("slug", term_, taxonomy_)
        # end if
    # end if
    if (not php_is_object(term_)):
        term_ = php_new_class("WP_Error", lambda : WP_Error("invalid_term", __("Empty Term.")))
    # end if
    if is_wp_error(term_):
        return term_
    # end if
    taxonomy_ = term_.taxonomy
    termlink_ = wp_rewrite_.get_extra_permastruct(taxonomy_)
    #// 
    #// Filters the permalink structure for a terms before token replacement occurs.
    #// 
    #// @since 4.9.0
    #// 
    #// @param string  $termlink The permalink structure for the term's taxonomy.
    #// @param WP_Term $term     The term object.
    #//
    termlink_ = apply_filters("pre_term_link", termlink_, term_)
    slug_ = term_.slug
    t_ = get_taxonomy(taxonomy_)
    if php_empty(lambda : termlink_):
        if "category" == taxonomy_:
            termlink_ = "?cat=" + term_.term_id
        elif t_.query_var:
            termlink_ = str("?") + str(t_.query_var) + str("=") + str(slug_)
        else:
            termlink_ = str("?taxonomy=") + str(taxonomy_) + str("&term=") + str(slug_)
        # end if
        termlink_ = home_url(termlink_)
    else:
        if t_.rewrite["hierarchical"]:
            hierarchical_slugs_ = Array()
            ancestors_ = get_ancestors(term_.term_id, taxonomy_, "taxonomy")
            for ancestor_ in ancestors_:
                ancestor_term_ = get_term(ancestor_, taxonomy_)
                hierarchical_slugs_[-1] = ancestor_term_.slug
            # end for
            hierarchical_slugs_ = array_reverse(hierarchical_slugs_)
            hierarchical_slugs_[-1] = slug_
            termlink_ = php_str_replace(str("%") + str(taxonomy_) + str("%"), php_implode("/", hierarchical_slugs_), termlink_)
        else:
            termlink_ = php_str_replace(str("%") + str(taxonomy_) + str("%"), slug_, termlink_)
        # end if
        termlink_ = home_url(user_trailingslashit(termlink_, "category"))
    # end if
    #// Back compat filters.
    if "post_tag" == taxonomy_:
        #// 
        #// Filters the tag link.
        #// 
        #// @since 2.3.0
        #// @deprecated 2.5.0 Use {@see 'term_link'} instead.
        #// 
        #// @param string $termlink Tag link URL.
        #// @param int    $term_id  Term ID.
        #//
        termlink_ = apply_filters_deprecated("tag_link", Array(termlink_, term_.term_id), "2.5.0", "term_link")
    elif "category" == taxonomy_:
        #// 
        #// Filters the category link.
        #// 
        #// @since 1.5.0
        #// @deprecated 2.5.0 Use {@see 'term_link'} instead.
        #// 
        #// @param string $termlink Category link URL.
        #// @param int    $term_id  Term ID.
        #//
        termlink_ = apply_filters_deprecated("category_link", Array(termlink_, term_.term_id), "2.5.0", "term_link")
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
    return apply_filters("term_link", termlink_, term_, taxonomy_)
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
def the_taxonomies(args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    defaults_ = Array({"post": 0, "before": "", "sep": " ", "after": ""})
    parsed_args_ = wp_parse_args(args_, defaults_)
    php_print(parsed_args_["before"] + join(parsed_args_["sep"], get_the_taxonomies(parsed_args_["post"], parsed_args_)) + parsed_args_["after"])
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
def get_the_taxonomies(post_=0, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    post_ = get_post(post_)
    args_ = wp_parse_args(args_, Array({"template": __("%s: %l."), "term_template": "<a href=\"%1$s\">%2$s</a>"}))
    taxonomies_ = Array()
    if (not post_):
        return taxonomies_
    # end if
    for taxonomy_ in get_object_taxonomies(post_):
        t_ = get_taxonomy(taxonomy_)
        if php_empty(lambda : t_["label"]):
            t_["label"] = taxonomy_
        # end if
        if php_empty(lambda : t_["args"]):
            t_["args"] = Array()
        # end if
        if php_empty(lambda : t_["template"]):
            t_["template"] = args_["template"]
        # end if
        if php_empty(lambda : t_["term_template"]):
            t_["term_template"] = args_["term_template"]
        # end if
        terms_ = get_object_term_cache(post_.ID, taxonomy_)
        if False == terms_:
            terms_ = wp_get_object_terms(post_.ID, taxonomy_, t_["args"])
        # end if
        links_ = Array()
        for term_ in terms_:
            links_[-1] = wp_sprintf(t_["term_template"], esc_attr(get_term_link(term_)), term_.name)
        # end for
        if links_:
            taxonomies_[taxonomy_] = wp_sprintf(t_["template"], t_["label"], links_, terms_)
        # end if
    # end for
    return taxonomies_
# end def get_the_taxonomies
#// 
#// Retrieve all taxonomy names for the given post.
#// 
#// @since 2.5.0
#// 
#// @param int|WP_Post $post Optional. Post ID or WP_Post object. Default is global $post.
#// @return string[] An array of all taxonomy names for the given post.
#//
def get_post_taxonomies(post_=0, *_args_):
    
    
    post_ = get_post(post_)
    return get_object_taxonomies(post_)
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
def is_object_in_term(object_id_=None, taxonomy_=None, terms_=None, *_args_):
    if terms_ is None:
        terms_ = None
    # end if
    
    object_id_ = php_int(object_id_)
    if (not object_id_):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_object", __("Invalid object ID.")))
    # end if
    object_terms_ = get_object_term_cache(object_id_, taxonomy_)
    if False == object_terms_:
        object_terms_ = wp_get_object_terms(object_id_, taxonomy_, Array({"update_term_meta_cache": False}))
        if is_wp_error(object_terms_):
            return object_terms_
        # end if
        wp_cache_set(object_id_, wp_list_pluck(object_terms_, "term_id"), str(taxonomy_) + str("_relationships"))
    # end if
    if is_wp_error(object_terms_):
        return object_terms_
    # end if
    if php_empty(lambda : object_terms_):
        return False
    # end if
    if php_empty(lambda : terms_):
        return (not php_empty(lambda : object_terms_))
    # end if
    terms_ = terms_
    ints_ = php_array_filter(terms_, "is_int")
    if ints_:
        strs_ = php_array_diff(terms_, ints_)
    else:
        strs_ = terms_
    # end if
    for object_term_ in object_terms_:
        #// If term is an int, check against term_ids only.
        if ints_ and php_in_array(object_term_.term_id, ints_):
            return True
        # end if
        if strs_:
            #// Only check numeric strings against term_id, to avoid false matches due to type juggling.
            numeric_strs_ = php_array_map("intval", php_array_filter(strs_, "is_numeric"))
            if php_in_array(object_term_.term_id, numeric_strs_, True):
                return True
            # end if
            if php_in_array(object_term_.name, strs_):
                return True
            # end if
            if php_in_array(object_term_.slug, strs_):
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
def is_object_in_taxonomy(object_type_=None, taxonomy_=None, *_args_):
    
    
    taxonomies_ = get_object_taxonomies(object_type_)
    if php_empty(lambda : taxonomies_):
        return False
    # end if
    return php_in_array(taxonomy_, taxonomies_)
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
def get_ancestors(object_id_=0, object_type_="", resource_type_="", *_args_):
    
    
    object_id_ = php_int(object_id_)
    ancestors_ = Array()
    if php_empty(lambda : object_id_):
        #// This filter is documented in wp-includes/taxonomy.php
        return apply_filters("get_ancestors", ancestors_, object_id_, object_type_, resource_type_)
    # end if
    if (not resource_type_):
        if is_taxonomy_hierarchical(object_type_):
            resource_type_ = "taxonomy"
        elif post_type_exists(object_type_):
            resource_type_ = "post_type"
        # end if
    # end if
    if "taxonomy" == resource_type_:
        term_ = get_term(object_id_, object_type_)
        while True:
            
            if not ((not is_wp_error(term_)) and (not php_empty(lambda : term_.parent)) and (not php_in_array(term_.parent, ancestors_))):
                break
            # end if
            ancestors_[-1] = php_int(term_.parent)
            term_ = get_term(term_.parent, object_type_)
        # end while
    elif "post_type" == resource_type_:
        ancestors_ = get_post_ancestors(object_id_)
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
    return apply_filters("get_ancestors", ancestors_, object_id_, object_type_, resource_type_)
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
def wp_get_term_taxonomy_parent_id(term_id_=None, taxonomy_=None, *_args_):
    
    
    term_ = get_term(term_id_, taxonomy_)
    if (not term_) or is_wp_error(term_):
        return False
    # end if
    return php_int(term_.parent)
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
def wp_check_term_hierarchy_for_loops(parent_=None, term_id_=None, taxonomy_=None, *_args_):
    
    
    #// Nothing fancy here - bail.
    if (not parent_):
        return 0
    # end if
    #// Can't be its own parent.
    if parent_ == term_id_:
        return 0
    # end if
    #// Now look for larger loops.
    loop_ = wp_find_hierarchy_loop("wp_get_term_taxonomy_parent_id", term_id_, parent_, Array(taxonomy_))
    if (not loop_):
        return parent_
        pass
    # end if
    #// Setting $parent to the given value causes a loop.
    if (php_isset(lambda : loop_[term_id_])):
        return 0
    # end if
    #// There's a loop, but it doesn't contain $term_id. Break the loop.
    for loop_member_ in php_array_keys(loop_):
        wp_update_term(loop_member_, taxonomy_, Array({"parent": 0}))
    # end for
    return parent_
# end def wp_check_term_hierarchy_for_loops
#// 
#// Determines whether a taxonomy is considered "viewable".
#// 
#// @since 5.1.0
#// 
#// @param string|WP_Taxonomy $taxonomy Taxonomy name or object.
#// @return bool Whether the taxonomy should be considered viewable.
#//
def is_taxonomy_viewable(taxonomy_=None, *_args_):
    
    
    if php_is_scalar(taxonomy_):
        taxonomy_ = get_taxonomy(taxonomy_)
        if (not taxonomy_):
            return False
        # end if
    # end if
    return taxonomy_.publicly_queryable
# end def is_taxonomy_viewable
#// 
#// Sets the last changed time for the 'terms' cache group.
#// 
#// @since 5.0.0
#//
def wp_cache_set_terms_last_changed(*_args_):
    
    
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
def wp_check_term_meta_support_prefilter(check_=None, *_args_):
    
    
    if get_option("db_version") < 34370:
        return False
    # end if
    return check_
# end def wp_check_term_meta_support_prefilter
