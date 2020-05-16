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
#// Taxonomy API: Core category-specific functionality
#// 
#// @package WordPress
#// @subpackage Taxonomy
#// 
#// 
#// Retrieve list of category objects.
#// 
#// If you set the 'taxonomy' argument to 'link_category', the link categories
#// will be returned instead.
#// 
#// @since 2.1.0
#// @see get_terms() Type of arguments that can be changed.
#// 
#// @param string|array $args {
#// Optional. Arguments to retrieve categories. See get_terms() for additional options.
#// 
#// @type string $taxonomy Taxonomy to retrieve terms for. Default 'category'.
#// }
#// @return array List of category objects.
#//
def get_categories(args="", *args_):
    
    defaults = Array({"taxonomy": "category"})
    args = wp_parse_args(args, defaults)
    #// 
    #// Filters the taxonomy used to retrieve terms when calling get_categories().
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $taxonomy Taxonomy to retrieve terms from.
    #// @param array  $args     An array of arguments. See get_terms().
    #//
    args["taxonomy"] = apply_filters("get_categories_taxonomy", args["taxonomy"], args)
    #// Back compat.
    if (php_isset(lambda : args["type"])) and "link" == args["type"]:
        _deprecated_argument(__FUNCTION__, "3.0.0", php_sprintf(__("%1$s is deprecated. Use %2$s instead."), "<code>type => link</code>", "<code>taxonomy => link_category</code>"))
        args["taxonomy"] = "link_category"
    # end if
    categories = get_terms(args)
    if is_wp_error(categories):
        categories = Array()
    else:
        categories = categories
        for k in php_array_keys(categories):
            _make_cat_compat(categories[k])
        # end for
    # end if
    return categories
# end def get_categories
#// 
#// Retrieves category data given a category ID or category object.
#// 
#// If you pass the $category parameter an object, which is assumed to be the
#// category row object retrieved the database. It will cache the category data.
#// 
#// If you pass $category an integer of the category ID, then that category will
#// be retrieved from the database, if it isn't already cached, and pass it back.
#// 
#// If you look at get_term(), then both types will be passed through several
#// filters and finally sanitized based on the $filter parameter value.
#// 
#// @since 1.5.1
#// 
#// @param int|object $category Category ID or Category row object
#// @param string $output Optional. The required return type. One of OBJECT, ARRAY_A, or ARRAY_N, which correspond to a
#// WP_Term object, an associative array, or a numeric array, respectively. Default OBJECT.
#// @param string $filter Optional. Default is raw or no WordPress defined filter will applied.
#// @return object|array|WP_Error|null Category data in type defined by $output parameter.
#// WP_Error if $category is empty, null if it does not exist.
#//
def get_category(category=None, output=OBJECT, filter="raw", *args_):
    
    category = get_term(category, "category", output, filter)
    if is_wp_error(category):
        return category
    # end if
    _make_cat_compat(category)
    return category
# end def get_category
#// 
#// Retrieve category based on URL containing the category slug.
#// 
#// Breaks the $category_path parameter up to get the category slug.
#// 
#// Tries to find the child path and will return it. If it doesn't find a
#// match, then it will return the first category matching slug, if $full_match,
#// is set to false. If it does not, then it will return null.
#// 
#// It is also possible that it will return a WP_Error object on failure. Check
#// for it when using this function.
#// 
#// @since 2.1.0
#// 
#// @param string $category_path URL containing category slugs.
#// @param bool   $full_match    Optional. Whether full path should be matched.
#// @param string $output        Optional. The required return type. One of OBJECT, ARRAY_A, or ARRAY_N, which correspond to
#// a WP_Term object, an associative array, or a numeric array, respectively. Default OBJECT.
#// @return WP_Term|array|WP_Error|null Type is based on $output value.
#//
def get_category_by_path(category_path=None, full_match=True, output=OBJECT, *args_):
    
    category_path = rawurlencode(urldecode(category_path))
    category_path = php_str_replace("%2F", "/", category_path)
    category_path = php_str_replace("%20", " ", category_path)
    category_paths = "/" + php_trim(category_path, "/")
    leaf_path = sanitize_title(php_basename(category_paths))
    category_paths = php_explode("/", category_paths)
    full_path = ""
    for pathdir in category_paths:
        full_path += "/" if "" != pathdir else "" + sanitize_title(pathdir)
    # end for
    categories = get_terms(Array({"taxonomy": "category", "get": "all", "slug": leaf_path}))
    if php_empty(lambda : categories):
        return
    # end if
    for category in categories:
        path = "/" + leaf_path
        curcategory = category
        while True:
            
            if not (0 != curcategory.parent and curcategory.parent != curcategory.term_id):
                break
            # end if
            curcategory = get_term(curcategory.parent, "category")
            if is_wp_error(curcategory):
                return curcategory
            # end if
            path = "/" + curcategory.slug + path
        # end while
        if path == full_path:
            category = get_term(category.term_id, "category", output)
            _make_cat_compat(category)
            return category
        # end if
    # end for
    #// If full matching is not required, return the first cat that matches the leaf.
    if (not full_match):
        category = get_term(reset(categories).term_id, "category", output)
        _make_cat_compat(category)
        return category
    # end if
# end def get_category_by_path
#// 
#// Retrieve category object by category slug.
#// 
#// @since 2.3.0
#// 
#// @param string $slug The category slug.
#// @return object Category data object
#//
def get_category_by_slug(slug=None, *args_):
    
    category = get_term_by("slug", slug, "category")
    if category:
        _make_cat_compat(category)
    # end if
    return category
# end def get_category_by_slug
#// 
#// Retrieve the ID of a category from its name.
#// 
#// @since 1.0.0
#// 
#// @param string $cat_name Category name.
#// @return int 0, if failure and ID of category on success.
#//
def get_cat_ID(cat_name=None, *args_):
    
    #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.FunctionNameInvalid
    cat = get_term_by("name", cat_name, "category")
    if cat:
        return cat.term_id
    # end if
    return 0
# end def get_cat_ID
#// 
#// Retrieve the name of a category from its ID.
#// 
#// @since 1.0.0
#// 
#// @param int $cat_id Category ID
#// @return string Category name, or an empty string if category doesn't exist.
#//
def get_cat_name(cat_id=None, *args_):
    
    cat_id = php_int(cat_id)
    category = get_term(cat_id, "category")
    if (not category) or is_wp_error(category):
        return ""
    # end if
    return category.name
# end def get_cat_name
#// 
#// Check if a category is an ancestor of another category.
#// 
#// You can use either an id or the category object for both parameters. If you
#// use an integer the category will be retrieved.
#// 
#// @since 2.1.0
#// 
#// @param int|object $cat1 ID or object to check if this is the parent category.
#// @param int|object $cat2 The child category.
#// @return bool Whether $cat2 is child of $cat1
#//
def cat_is_ancestor_of(cat1=None, cat2=None, *args_):
    
    return term_is_ancestor_of(cat1, cat2, "category")
# end def cat_is_ancestor_of
#// 
#// Sanitizes category data based on context.
#// 
#// @since 2.3.0
#// 
#// @param object|array $category Category data
#// @param string $context Optional. Default is 'display'.
#// @return object|array Same type as $category with sanitized data for safe use.
#//
def sanitize_category(category=None, context="display", *args_):
    
    return sanitize_term(category, "category", context)
# end def sanitize_category
#// 
#// Sanitizes data in single category key field.
#// 
#// @since 2.3.0
#// 
#// @param string $field Category key to sanitize
#// @param mixed $value Category value to sanitize
#// @param int $cat_id Category ID
#// @param string $context What filter to use, 'raw', 'display', etc.
#// @return mixed Same type as $value after $value has been sanitized.
#//
def sanitize_category_field(field=None, value=None, cat_id=None, context=None, *args_):
    
    return sanitize_term_field(field, value, cat_id, "category", context)
# end def sanitize_category_field
#// Tags
#// 
#// Retrieves all post tags.
#// 
#// @since 2.3.0
#// @see get_terms() For list of arguments to pass.
#// 
#// @param string|array $args Tag arguments to use when retrieving tags.
#// @return WP_Term[]|int $tags Array of 'post_tag' term objects, or a count thereof.
#//
def get_tags(args="", *args_):
    
    defaults = Array({"taxonomy": "post_tag"})
    args = wp_parse_args(args, defaults)
    tags = get_terms(args)
    if php_empty(lambda : tags):
        return_ = Array()
        return return_
    # end if
    #// 
    #// Filters the array of term objects returned for the 'post_tag' taxonomy.
    #// 
    #// @since 2.3.0
    #// 
    #// @param WP_Term[]|int $tags Array of 'post_tag' term objects, or a count thereof.
    #// @param array         $args An array of arguments. @see get_terms()
    #//
    tags = apply_filters("get_tags", tags, args)
    return tags
# end def get_tags
#// 
#// Retrieve post tag by tag ID or tag object.
#// 
#// If you pass the $tag parameter an object, which is assumed to be the tag row
#// object retrieved the database. It will cache the tag data.
#// 
#// If you pass $tag an integer of the tag ID, then that tag will
#// be retrieved from the database, if it isn't already cached, and pass it back.
#// 
#// If you look at get_term(), then both types will be passed through several
#// filters and finally sanitized based on the $filter parameter value.
#// 
#// @since 2.3.0
#// 
#// @param int|WP_Term|object $tag    A tag ID or object.
#// @param string             $output Optional. The required return type. One of OBJECT, ARRAY_A, or ARRAY_N, which correspond to
#// a WP_Term object, an associative array, or a numeric array, respectively. Default OBJECT.
#// @param string             $filter Optional. Default is raw or no WordPress defined filter will applied.
#// @return WP_Term|array|WP_Error|null Tag data in type defined by $output parameter. WP_Error if $tag is empty, null if it does not exist.
#//
def get_tag(tag=None, output=OBJECT, filter="raw", *args_):
    
    return get_term(tag, "post_tag", output, filter)
# end def get_tag
#// Cache
#// 
#// Remove the category cache data based on ID.
#// 
#// @since 2.1.0
#// 
#// @param int $id Category ID
#//
def clean_category_cache(id=None, *args_):
    
    clean_term_cache(id, "category")
# end def clean_category_cache
#// 
#// Update category structure to old pre-2.3 from new taxonomy structure.
#// 
#// This function was added for the taxonomy support to update the new category
#// structure with the old category one. This will maintain compatibility with
#// plugins and themes which depend on the old key or property names.
#// 
#// The parameter should only be passed a variable and not create the array or
#// object inline to the parameter. The reason for this is that parameter is
#// passed by reference and PHP will fail unless it has the variable.
#// 
#// There is no return value, because everything is updated on the variable you
#// pass to it. This is one of the features with using pass by reference in PHP.
#// 
#// @since 2.3.0
#// @since 4.4.0 The `$category` parameter now also accepts a WP_Term object.
#// @access private
#// 
#// @param array|object|WP_Term $category Category Row object or array
#//
def _make_cat_compat(category=None, *args_):
    
    if php_is_object(category) and (not is_wp_error(category)):
        category.cat_ID = category.term_id
        category.category_count = category.count
        category.category_description = category.description
        category.cat_name = category.name
        category.category_nicename = category.slug
        category.category_parent = category.parent
    elif php_is_array(category) and (php_isset(lambda : category["term_id"])):
        category["cat_ID"] = category["term_id"]
        category["category_count"] = category["count"]
        category["category_description"] = category["description"]
        category["cat_name"] = category["name"]
        category["category_nicename"] = category["slug"]
        category["category_parent"] = category["parent"]
    # end if
# end def _make_cat_compat
