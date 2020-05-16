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
#// WordPress Taxonomy Administration API.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// 
#// Category.
#// 
#// 
#// Check whether a category exists.
#// 
#// @since 2.0.0
#// 
#// @see term_exists()
#// 
#// @param int|string $cat_name Category name.
#// @param int        $parent   Optional. ID of parent term.
#// @return mixed
#//
def category_exists(cat_name=None, parent=None, *args_):
    
    id = term_exists(cat_name, "category", parent)
    if php_is_array(id):
        id = id["term_id"]
    # end if
    return id
# end def category_exists
#// 
#// Get category object for given ID and 'edit' filter context.
#// 
#// @since 2.0.0
#// 
#// @param int $id
#// @return object
#//
def get_category_to_edit(id=None, *args_):
    
    category = get_term(id, "category", OBJECT, "edit")
    _make_cat_compat(category)
    return category
# end def get_category_to_edit
#// 
#// Add a new category to the database if it does not already exist.
#// 
#// @since 2.0.0
#// 
#// @param int|string $cat_name
#// @param int        $parent
#// @return int|WP_Error
#//
def wp_create_category(cat_name=None, parent=0, *args_):
    
    id = category_exists(cat_name, parent)
    if id:
        return id
    # end if
    return wp_insert_category(Array({"cat_name": cat_name, "category_parent": parent}))
# end def wp_create_category
#// 
#// Create categories for the given post.
#// 
#// @since 2.0.0
#// 
#// @param string[] $categories Array of category names to create.
#// @param int      $post_id    Optional. The post ID. Default empty.
#// @return int[] Array of IDs of categories assigned to the given post.
#//
def wp_create_categories(categories=None, post_id="", *args_):
    
    cat_ids = Array()
    for category in categories:
        id = category_exists(category)
        if id:
            cat_ids[-1] = id
        else:
            id = wp_create_category(category)
            if id:
                cat_ids[-1] = id
            # end if
        # end if
    # end for
    if post_id:
        wp_set_post_categories(post_id, cat_ids)
    # end if
    return cat_ids
# end def wp_create_categories
#// 
#// Updates an existing Category or creates a new Category.
#// 
#// @since 2.0.0
#// @since 2.5.0 $wp_error parameter was added.
#// @since 3.0.0 The 'taxonomy' argument was added.
#// 
#// @param array $catarr {
#// Array of arguments for inserting a new category.
#// 
#// @type int        $cat_ID               Category ID. A non-zero value updates an existing category.
#// Default 0.
#// @type string     $taxonomy             Taxonomy slug. Default 'category'.
#// @type string     $cat_name             Category name. Default empty.
#// @type string     $category_description Category description. Default empty.
#// @type string     $category_nicename    Category nice (display) name. Default empty.
#// @type int|string $category_parent      Category parent ID. Default empty.
#// }
#// @param bool  $wp_error Optional. Default false.
#// @return int|object The ID number of the new or updated Category on success. Zero or a WP_Error on failure,
#// depending on param $wp_error.
#//
def wp_insert_category(catarr=None, wp_error=False, *args_):
    
    cat_defaults = Array({"cat_ID": 0, "taxonomy": "category", "cat_name": "", "category_description": "", "category_nicename": "", "category_parent": ""})
    catarr = wp_parse_args(catarr, cat_defaults)
    if php_trim(catarr["cat_name"]) == "":
        if (not wp_error):
            return 0
        else:
            return php_new_class("WP_Error", lambda : WP_Error("cat_name", __("You did not enter a category name.")))
        # end if
    # end if
    catarr["cat_ID"] = php_int(catarr["cat_ID"])
    #// Are we updating or creating?
    update = (not php_empty(lambda : catarr["cat_ID"]))
    name = catarr["cat_name"]
    description = catarr["category_description"]
    slug = catarr["category_nicename"]
    parent = php_int(catarr["category_parent"])
    if parent < 0:
        parent = 0
    # end if
    if php_empty(lambda : parent) or (not term_exists(parent, catarr["taxonomy"])) or catarr["cat_ID"] and term_is_ancestor_of(catarr["cat_ID"], parent, catarr["taxonomy"]):
        parent = 0
    # end if
    args = compact("name", "slug", "parent", "description")
    if update:
        catarr["cat_ID"] = wp_update_term(catarr["cat_ID"], catarr["taxonomy"], args)
    else:
        catarr["cat_ID"] = wp_insert_term(catarr["cat_name"], catarr["taxonomy"], args)
    # end if
    if is_wp_error(catarr["cat_ID"]):
        if wp_error:
            return catarr["cat_ID"]
        else:
            return 0
        # end if
    # end if
    return catarr["cat_ID"]["term_id"]
# end def wp_insert_category
#// 
#// Aliases wp_insert_category() with minimal args.
#// 
#// If you want to update only some fields of an existing category, call this
#// function with only the new values set inside $catarr.
#// 
#// @since 2.0.0
#// 
#// @param array $catarr The 'cat_ID' value is required. All other keys are optional.
#// @return int|bool The ID number of the new or updated Category on success. Zero or FALSE on failure.
#//
def wp_update_category(catarr=None, *args_):
    
    cat_ID = php_int(catarr["cat_ID"])
    if (php_isset(lambda : catarr["category_parent"])) and cat_ID == catarr["category_parent"]:
        return False
    # end if
    #// First, get all of the original fields.
    category = get_term(cat_ID, "category", ARRAY_A)
    _make_cat_compat(category)
    #// Escape data pulled from DB.
    category = wp_slash(category)
    #// Merge old and new fields with new fields overwriting old ones.
    catarr = php_array_merge(category, catarr)
    return wp_insert_category(catarr)
# end def wp_update_category
#// 
#// Tags.
#// 
#// 
#// Check whether a post tag with a given name exists.
#// 
#// @since 2.3.0
#// 
#// @param int|string $tag_name
#// @return mixed
#//
def tag_exists(tag_name=None, *args_):
    
    return term_exists(tag_name, "post_tag")
# end def tag_exists
#// 
#// Add a new tag to the database if it does not already exist.
#// 
#// @since 2.3.0
#// 
#// @param int|string $tag_name
#// @return array|WP_Error
#//
def wp_create_tag(tag_name=None, *args_):
    
    return wp_create_term(tag_name, "post_tag")
# end def wp_create_tag
#// 
#// Get comma-separated list of tags available to edit.
#// 
#// @since 2.3.0
#// 
#// @param int    $post_id
#// @param string $taxonomy Optional. The taxonomy for which to retrieve terms. Default 'post_tag'.
#// @return string|bool|WP_Error
#//
def get_tags_to_edit(post_id=None, taxonomy="post_tag", *args_):
    
    return get_terms_to_edit(post_id, taxonomy)
# end def get_tags_to_edit
#// 
#// Get comma-separated list of terms available to edit for the given post ID.
#// 
#// @since 2.8.0
#// 
#// @param int    $post_id
#// @param string $taxonomy Optional. The taxonomy for which to retrieve terms. Default 'post_tag'.
#// @return string|bool|WP_Error
#//
def get_terms_to_edit(post_id=None, taxonomy="post_tag", *args_):
    
    post_id = php_int(post_id)
    if (not post_id):
        return False
    # end if
    terms = get_object_term_cache(post_id, taxonomy)
    if False == terms:
        terms = wp_get_object_terms(post_id, taxonomy)
        wp_cache_add(post_id, wp_list_pluck(terms, "term_id"), taxonomy + "_relationships")
    # end if
    if (not terms):
        return False
    # end if
    if is_wp_error(terms):
        return terms
    # end if
    term_names = Array()
    for term in terms:
        term_names[-1] = term.name
    # end for
    terms_to_edit = esc_attr(join(",", term_names))
    #// 
    #// Filters the comma-separated list of terms available to edit.
    #// 
    #// @since 2.8.0
    #// 
    #// @see get_terms_to_edit()
    #// 
    #// @param string $terms_to_edit A comma-separated list of term names.
    #// @param string $taxonomy      The taxonomy name for which to retrieve terms.
    #//
    terms_to_edit = apply_filters("terms_to_edit", terms_to_edit, taxonomy)
    return terms_to_edit
# end def get_terms_to_edit
#// 
#// Add a new term to the database if it does not already exist.
#// 
#// @since 2.8.0
#// 
#// @param int|string $tag_name
#// @param string $taxonomy Optional. The taxonomy for which to retrieve terms. Default 'post_tag'.
#// @return array|WP_Error
#//
def wp_create_term(tag_name=None, taxonomy="post_tag", *args_):
    
    id = term_exists(tag_name, taxonomy)
    if id:
        return id
    # end if
    return wp_insert_term(tag_name, taxonomy)
# end def wp_create_term
