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
def category_exists(cat_name_=None, parent_=None, *_args_):
    if parent_ is None:
        parent_ = None
    # end if
    
    id_ = term_exists(cat_name_, "category", parent_)
    if php_is_array(id_):
        id_ = id_["term_id"]
    # end if
    return id_
# end def category_exists
#// 
#// Get category object for given ID and 'edit' filter context.
#// 
#// @since 2.0.0
#// 
#// @param int $id
#// @return object
#//
def get_category_to_edit(id_=None, *_args_):
    
    
    category_ = get_term(id_, "category", OBJECT, "edit")
    _make_cat_compat(category_)
    return category_
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
def wp_create_category(cat_name_=None, parent_=0, *_args_):
    
    
    id_ = category_exists(cat_name_, parent_)
    if id_:
        return id_
    # end if
    return wp_insert_category(Array({"cat_name": cat_name_, "category_parent": parent_}))
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
def wp_create_categories(categories_=None, post_id_="", *_args_):
    
    
    cat_ids_ = Array()
    for category_ in categories_:
        id_ = category_exists(category_)
        if id_:
            cat_ids_[-1] = id_
        else:
            id_ = wp_create_category(category_)
            if id_:
                cat_ids_[-1] = id_
            # end if
        # end if
    # end for
    if post_id_:
        wp_set_post_categories(post_id_, cat_ids_)
    # end if
    return cat_ids_
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
def wp_insert_category(catarr_=None, wp_error_=None, *_args_):
    if wp_error_ is None:
        wp_error_ = False
    # end if
    
    cat_defaults_ = Array({"cat_ID": 0, "taxonomy": "category", "cat_name": "", "category_description": "", "category_nicename": "", "category_parent": ""})
    catarr_ = wp_parse_args(catarr_, cat_defaults_)
    if php_trim(catarr_["cat_name"]) == "":
        if (not wp_error_):
            return 0
        else:
            return php_new_class("WP_Error", lambda : WP_Error("cat_name", __("You did not enter a category name.")))
        # end if
    # end if
    catarr_["cat_ID"] = php_int(catarr_["cat_ID"])
    #// Are we updating or creating?
    update_ = (not php_empty(lambda : catarr_["cat_ID"]))
    name_ = catarr_["cat_name"]
    description_ = catarr_["category_description"]
    slug_ = catarr_["category_nicename"]
    parent_ = php_int(catarr_["category_parent"])
    if parent_ < 0:
        parent_ = 0
    # end if
    if php_empty(lambda : parent_) or (not term_exists(parent_, catarr_["taxonomy"])) or catarr_["cat_ID"] and term_is_ancestor_of(catarr_["cat_ID"], parent_, catarr_["taxonomy"]):
        parent_ = 0
    # end if
    args_ = php_compact("name_", "slug_", "parent_", "description_")
    if update_:
        catarr_["cat_ID"] = wp_update_term(catarr_["cat_ID"], catarr_["taxonomy"], args_)
    else:
        catarr_["cat_ID"] = wp_insert_term(catarr_["cat_name"], catarr_["taxonomy"], args_)
    # end if
    if is_wp_error(catarr_["cat_ID"]):
        if wp_error_:
            return catarr_["cat_ID"]
        else:
            return 0
        # end if
    # end if
    return catarr_["cat_ID"]["term_id"]
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
def wp_update_category(catarr_=None, *_args_):
    
    
    cat_ID_ = php_int(catarr_["cat_ID"])
    if (php_isset(lambda : catarr_["category_parent"])) and cat_ID_ == catarr_["category_parent"]:
        return False
    # end if
    #// First, get all of the original fields.
    category_ = get_term(cat_ID_, "category", ARRAY_A)
    _make_cat_compat(category_)
    #// Escape data pulled from DB.
    category_ = wp_slash(category_)
    #// Merge old and new fields with new fields overwriting old ones.
    catarr_ = php_array_merge(category_, catarr_)
    return wp_insert_category(catarr_)
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
def tag_exists(tag_name_=None, *_args_):
    
    
    return term_exists(tag_name_, "post_tag")
# end def tag_exists
#// 
#// Add a new tag to the database if it does not already exist.
#// 
#// @since 2.3.0
#// 
#// @param int|string $tag_name
#// @return array|WP_Error
#//
def wp_create_tag(tag_name_=None, *_args_):
    
    
    return wp_create_term(tag_name_, "post_tag")
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
def get_tags_to_edit(post_id_=None, taxonomy_="post_tag", *_args_):
    
    
    return get_terms_to_edit(post_id_, taxonomy_)
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
def get_terms_to_edit(post_id_=None, taxonomy_="post_tag", *_args_):
    
    
    post_id_ = php_int(post_id_)
    if (not post_id_):
        return False
    # end if
    terms_ = get_object_term_cache(post_id_, taxonomy_)
    if False == terms_:
        terms_ = wp_get_object_terms(post_id_, taxonomy_)
        wp_cache_add(post_id_, wp_list_pluck(terms_, "term_id"), taxonomy_ + "_relationships")
    # end if
    if (not terms_):
        return False
    # end if
    if is_wp_error(terms_):
        return terms_
    # end if
    term_names_ = Array()
    for term_ in terms_:
        term_names_[-1] = term_.name
    # end for
    terms_to_edit_ = esc_attr(php_join(",", term_names_))
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
    terms_to_edit_ = apply_filters("terms_to_edit", terms_to_edit_, taxonomy_)
    return terms_to_edit_
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
def wp_create_term(tag_name_=None, taxonomy_="post_tag", *_args_):
    
    
    id_ = term_exists(tag_name_, taxonomy_)
    if id_:
        return id_
    # end if
    return wp_insert_term(tag_name_, taxonomy_)
# end def wp_create_term
