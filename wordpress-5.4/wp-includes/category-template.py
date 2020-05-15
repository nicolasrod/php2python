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
#// Taxonomy API: Core category-specific template tags
#// 
#// @package WordPress
#// @subpackage Template
#// @since 1.2.0
#// 
#// 
#// Retrieve category link URL.
#// 
#// @since 1.0.0
#// @see get_term_link()
#// 
#// @param int|object $category Category ID or object.
#// @return string Link on success, empty string if category does not exist.
#//
def get_category_link(category=None, *args_):
    
    if (not php_is_object(category)):
        category = int(category)
    # end if
    category = get_term_link(category)
    if is_wp_error(category):
        return ""
    # end if
    return category
# end def get_category_link
#// 
#// Retrieve category parents with separator.
#// 
#// @since 1.2.0
#// @since 4.8.0 The `$visited` parameter was deprecated and renamed to `$deprecated`.
#// 
#// @param int $id Category ID.
#// @param bool $link Optional, default is false. Whether to format with link.
#// @param string $separator Optional, default is '/'. How to separate categories.
#// @param bool $nicename Optional, default is false. Whether to use nice name for display.
#// @param array $deprecated Not used.
#// @return string|WP_Error A list of category parents on success, WP_Error on failure.
#//
def get_category_parents(id=None, link=False, separator="/", nicename=False, deprecated=Array(), *args_):
    
    if (not php_empty(lambda : deprecated)):
        _deprecated_argument(__FUNCTION__, "4.8.0")
    # end if
    format = "slug" if nicename else "name"
    args = Array({"separator": separator, "link": link, "format": format})
    return get_term_parents_list(id, "category", args)
# end def get_category_parents
#// 
#// Retrieve post categories.
#// 
#// This tag may be used outside The Loop by passing a post id as the parameter.
#// 
#// Note: This function only returns results from the default "category" taxonomy.
#// For custom taxonomies use get_the_terms().
#// 
#// @since 0.71
#// 
#// @param int $id Optional, default to current post ID. The post ID.
#// @return WP_Term[] Array of WP_Term objects, one for each category assigned to the post.
#//
def get_the_category(id=False, *args_):
    
    categories = get_the_terms(id, "category")
    if (not categories) or is_wp_error(categories):
        categories = Array()
    # end if
    categories = php_array_values(categories)
    for key in php_array_keys(categories):
        _make_cat_compat(categories[key])
    # end for
    #// 
    #// Filters the array of categories to return for a post.
    #// 
    #// @since 3.1.0
    #// @since 4.4.0 Added `$id` parameter.
    #// 
    #// @param WP_Term[] $categories An array of categories to return for the post.
    #// @param int|false $id         ID of the post.
    #//
    return apply_filters("get_the_categories", categories, id)
# end def get_the_category
#// 
#// Retrieve category name based on category ID.
#// 
#// @since 0.71
#// 
#// @param int $cat_ID Category ID.
#// @return string|WP_Error Category name on success, WP_Error on failure.
#//
def get_the_category_by_ID(cat_ID=None, *args_):
    
    #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.FunctionNameInvalid
    cat_ID = int(cat_ID)
    category = get_term(cat_ID)
    if is_wp_error(category):
        return category
    # end if
    return category.name if category else ""
# end def get_the_category_by_ID
#// 
#// Retrieve category list for a post in either HTML list or custom format.
#// 
#// @since 1.5.1
#// 
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// 
#// @param string $separator Optional. Separator between the categories. By default, the links are placed
#// in an unordered list. An empty string will result in the default behavior.
#// @param string $parents Optional. How to display the parents.
#// @param int $post_id Optional. Post ID to retrieve categories.
#// @return string
#//
def get_the_category_list(separator="", parents="", post_id=False, *args_):
    
    global wp_rewrite
    php_check_if_defined("wp_rewrite")
    if (not is_object_in_taxonomy(get_post_type(post_id), "category")):
        #// This filter is documented in wp-includes/category-template.php
        return apply_filters("the_category", "", separator, parents)
    # end if
    #// 
    #// Filters the categories before building the category list.
    #// 
    #// @since 4.4.0
    #// 
    #// @param WP_Term[] $categories An array of the post's categories.
    #// @param int|bool  $post_id    ID of the post we're retrieving categories for. When `false`, we assume the
    #// current post in the loop.
    #//
    categories = apply_filters("the_category_list", get_the_category(post_id), post_id)
    if php_empty(lambda : categories):
        #// This filter is documented in wp-includes/category-template.php
        return apply_filters("the_category", __("Uncategorized"), separator, parents)
    # end if
    rel = "rel=\"category tag\"" if php_is_object(wp_rewrite) and wp_rewrite.using_permalinks() else "rel=\"category\""
    thelist = ""
    if "" == separator:
        thelist += "<ul class=\"post-categories\">"
        for category in categories:
            thelist += "\n  <li>"
            for case in Switch(php_strtolower(parents)):
                if case("multiple"):
                    if category.parent:
                        thelist += get_category_parents(category.parent, True, separator)
                    # end if
                    thelist += "<a href=\"" + esc_url(get_category_link(category.term_id)) + "\" " + rel + ">" + category.name + "</a></li>"
                    break
                # end if
                if case("single"):
                    thelist += "<a href=\"" + esc_url(get_category_link(category.term_id)) + "\"  " + rel + ">"
                    if category.parent:
                        thelist += get_category_parents(category.parent, False, separator)
                    # end if
                    thelist += category.name + "</a></li>"
                    break
                # end if
                if case(""):
                    pass
                # end if
                if case():
                    thelist += "<a href=\"" + esc_url(get_category_link(category.term_id)) + "\" " + rel + ">" + category.name + "</a></li>"
                # end if
            # end for
        # end for
        thelist += "</ul>"
    else:
        i = 0
        for category in categories:
            if 0 < i:
                thelist += separator
            # end if
            for case in Switch(php_strtolower(parents)):
                if case("multiple"):
                    if category.parent:
                        thelist += get_category_parents(category.parent, True, separator)
                    # end if
                    thelist += "<a href=\"" + esc_url(get_category_link(category.term_id)) + "\" " + rel + ">" + category.name + "</a>"
                    break
                # end if
                if case("single"):
                    thelist += "<a href=\"" + esc_url(get_category_link(category.term_id)) + "\" " + rel + ">"
                    if category.parent:
                        thelist += get_category_parents(category.parent, False, separator)
                    # end if
                    thelist += str(category.name) + str("</a>")
                    break
                # end if
                if case(""):
                    pass
                # end if
                if case():
                    thelist += "<a href=\"" + esc_url(get_category_link(category.term_id)) + "\" " + rel + ">" + category.name + "</a>"
                # end if
            # end for
            i += 1
        # end for
    # end if
    #// 
    #// Filters the category or list of categories.
    #// 
    #// @since 1.2.0
    #// 
    #// @param string $thelist   List of categories for the current post.
    #// @param string $separator Separator used between the categories.
    #// @param string $parents   How to display the category parents. Accepts 'multiple',
    #// 'single', or empty.
    #//
    return apply_filters("the_category", thelist, separator, parents)
# end def get_the_category_list
#// 
#// Checks if the current post is within any of the given categories.
#// 
#// The given categories are checked against the post's categories' term_ids, names and slugs.
#// Categories given as integers will only be checked against the post's categories' term_ids.
#// 
#// Prior to v2.5 of WordPress, category names were not supported.
#// Prior to v2.7, category slugs were not supported.
#// Prior to v2.7, only one category could be compared: in_category( $single_category ).
#// Prior to v2.7, this function could only be used in the WordPress Loop.
#// As of 2.7, the function can be used anywhere if it is provided a post ID or post object.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 1.2.0
#// 
#// @param int|string|array $category Category ID, name or slug, or array of said.
#// @param int|object $post Optional. Post to check instead of the current post. (since 2.7.0)
#// @return bool True if the current post is in any of the given categories.
#//
def in_category(category=None, post=None, *args_):
    
    if php_empty(lambda : category):
        return False
    # end if
    return has_category(category, post)
# end def in_category
#// 
#// Display category list for a post in either HTML list or custom format.
#// 
#// @since 0.71
#// 
#// @param string $separator Optional. Separator between the categories. By default, the links are placed
#// in an unordered list. An empty string will result in the default behavior.
#// @param string $parents Optional. How to display the parents.
#// @param int $post_id Optional. Post ID to retrieve categories.
#//
def the_category(separator="", parents="", post_id=False, *args_):
    
    php_print(get_the_category_list(separator, parents, post_id))
# end def the_category
#// 
#// Retrieve category description.
#// 
#// @since 1.0.0
#// 
#// @param int $category Optional. Category ID. Will use global category ID by default.
#// @return string Category description, available.
#//
def category_description(category=0, *args_):
    
    return term_description(category)
# end def category_description
#// 
#// Display or retrieve the HTML dropdown list of categories.
#// 
#// The 'hierarchical' argument, which is disabled by default, will override the
#// depth argument, unless it is true. When the argument is false, it will
#// display all of the categories. When it is enabled it will use the value in
#// the 'depth' argument.
#// 
#// @since 2.1.0
#// @since 4.2.0 Introduced the `value_field` argument.
#// @since 4.6.0 Introduced the `required` argument.
#// 
#// @param array|string $args {
#// Optional. Array or string of arguments to generate a categories drop-down element. See WP_Term_Query::__construct()
#// for information on additional accepted arguments.
#// 
#// @type string       $show_option_all   Text to display for showing all categories. Default empty.
#// @type string       $show_option_none  Text to display for showing no categories. Default empty.
#// @type string       $option_none_value Value to use when no category is selected. Default empty.
#// @type string       $orderby           Which column to use for ordering categories. See get_terms() for a list
#// of accepted values. Default 'id' (term_id).
#// @type bool         $pad_counts        See get_terms() for an argument description. Default false.
#// @type bool|int     $show_count        Whether to include post counts. Accepts 0, 1, or their bool equivalents.
#// Default 0.
#// @type bool|int     $echo              Whether to echo or return the generated markup. Accepts 0, 1, or their
#// bool equivalents. Default 1.
#// @type bool|int     $hierarchical      Whether to traverse the taxonomy hierarchy. Accepts 0, 1, or their bool
#// equivalents. Default 0.
#// @type int          $depth             Maximum depth. Default 0.
#// @type int          $tab_index         Tab index for the select element. Default 0 (no tabindex).
#// @type string       $name              Value for the 'name' attribute of the select element. Default 'cat'.
#// @type string       $id                Value for the 'id' attribute of the select element. Defaults to the value
#// of `$name`.
#// @type string       $class             Value for the 'class' attribute of the select element. Default 'postform'.
#// @type int|string   $selected          Value of the option that should be selected. Default 0.
#// @type string       $value_field       Term field that should be used to populate the 'value' attribute
#// of the option elements. Accepts any valid term field: 'term_id', 'name',
#// 'slug', 'term_group', 'term_taxonomy_id', 'taxonomy', 'description',
#// 'parent', 'count'. Default 'term_id'.
#// @type string|array $taxonomy          Name of the category or categories to retrieve. Default 'category'.
#// @type bool         $hide_if_empty     True to skip generating markup if no categories are found.
#// Default false (create select element even if no categories are found).
#// @type bool         $required          Whether the `<select>` element should have the HTML5 'required' attribute.
#// Default false.
#// }
#// @return string HTML dropdown list of categories.
#//
def wp_dropdown_categories(args="", *args_):
    
    defaults = Array({"show_option_all": "", "show_option_none": "", "orderby": "id", "order": "ASC", "show_count": 0, "hide_empty": 1, "child_of": 0, "exclude": "", "echo": 1, "selected": 0, "hierarchical": 0, "name": "cat", "id": "", "class": "postform", "depth": 0, "tab_index": 0, "taxonomy": "category", "hide_if_empty": False, "option_none_value": -1, "value_field": "term_id", "required": False})
    defaults["selected"] = get_query_var("cat") if is_category() else 0
    #// Back compat.
    if (php_isset(lambda : args["type"])) and "link" == args["type"]:
        _deprecated_argument(__FUNCTION__, "3.0.0", php_sprintf(__("%1$s is deprecated. Use %2$s instead."), "<code>type => link</code>", "<code>taxonomy => link_category</code>"))
        args["taxonomy"] = "link_category"
    # end if
    #// Parse incoming $args into an array and merge it with $defaults.
    parsed_args = wp_parse_args(args, defaults)
    option_none_value = parsed_args["option_none_value"]
    if (not (php_isset(lambda : parsed_args["pad_counts"]))) and parsed_args["show_count"] and parsed_args["hierarchical"]:
        parsed_args["pad_counts"] = True
    # end if
    tab_index = parsed_args["tab_index"]
    tab_index_attribute = ""
    if int(tab_index) > 0:
        tab_index_attribute = str(" tabindex=\"") + str(tab_index) + str("\"")
    # end if
    #// Avoid clashes with the 'name' param of get_terms().
    get_terms_args = parsed_args
    get_terms_args["name"] = None
    categories = get_terms(get_terms_args)
    name = esc_attr(parsed_args["name"])
    class_ = esc_attr(parsed_args["class"])
    id = esc_attr(parsed_args["id"]) if parsed_args["id"] else name
    required = "required" if parsed_args["required"] else ""
    if (not parsed_args["hide_if_empty"]) or (not php_empty(lambda : categories)):
        output = str("<select ") + str(required) + str(" name='") + str(name) + str("' id='") + str(id) + str("' class='") + str(class_) + str("' ") + str(tab_index_attribute) + str(">\n")
    else:
        output = ""
    # end if
    if php_empty(lambda : categories) and (not parsed_args["hide_if_empty"]) and (not php_empty(lambda : parsed_args["show_option_none"])):
        #// 
        #// Filters a taxonomy drop-down display element.
        #// 
        #// A variety of taxonomy drop-down display elements can be modified
        #// just prior to display via this filter. Filterable arguments include
        #// 'show_option_none', 'show_option_all', and various forms of the
        #// term name.
        #// 
        #// @since 1.2.0
        #// 
        #// @see wp_dropdown_categories()
        #// 
        #// @param string       $element  Category name.
        #// @param WP_Term|null $category The category object, or null if there's no corresponding category.
        #//
        show_option_none = apply_filters("list_cats", parsed_args["show_option_none"], None)
        output += " <option value='" + esc_attr(option_none_value) + str("' selected='selected'>") + str(show_option_none) + str("</option>\n")
    # end if
    if (not php_empty(lambda : categories)):
        if parsed_args["show_option_all"]:
            #// This filter is documented in wp-includes/category-template.php
            show_option_all = apply_filters("list_cats", parsed_args["show_option_all"], None)
            selected = " selected='selected'" if "0" == php_strval(parsed_args["selected"]) else ""
            output += str(" <option value='0'") + str(selected) + str(">") + str(show_option_all) + str("</option>\n")
        # end if
        if parsed_args["show_option_none"]:
            #// This filter is documented in wp-includes/category-template.php
            show_option_none = apply_filters("list_cats", parsed_args["show_option_none"], None)
            selected = selected(option_none_value, parsed_args["selected"], False)
            output += " <option value='" + esc_attr(option_none_value) + str("'") + str(selected) + str(">") + str(show_option_none) + str("</option>\n")
        # end if
        if parsed_args["hierarchical"]:
            depth = parsed_args["depth"]
            pass
        else:
            depth = -1
            pass
        # end if
        output += walk_category_dropdown_tree(categories, depth, parsed_args)
    # end if
    if (not parsed_args["hide_if_empty"]) or (not php_empty(lambda : categories)):
        output += "</select>\n"
    # end if
    #// 
    #// Filters the taxonomy drop-down output.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string $output      HTML output.
    #// @param array  $parsed_args Arguments used to build the drop-down.
    #//
    output = apply_filters("wp_dropdown_cats", output, parsed_args)
    if parsed_args["echo"]:
        php_print(output)
    # end if
    return output
# end def wp_dropdown_categories
#// 
#// Display or retrieve the HTML list of categories.
#// 
#// @since 2.1.0
#// @since 4.4.0 Introduced the `hide_title_if_empty` and `separator` arguments.
#// @since 4.4.0 The `current_category` argument was modified to optionally accept an array of values.
#// 
#// @param array|string $args {
#// Array of optional arguments. See get_categories(), get_terms(), and WP_Term_Query::__construct()
#// for information on additional accepted arguments.
#// 
#// @type int|array    $current_category      ID of category, or array of IDs of categories, that should get the
#// 'current-cat' class. Default 0.
#// @type int          $depth                 Category depth. Used for tab indentation. Default 0.
#// @type bool|int     $echo                  Whether to echo or return the generated markup. Accepts 0, 1, or their
#// bool equivalents. Default 1.
#// @type array|string $exclude               Array or comma/space-separated string of term IDs to exclude.
#// If `$hierarchical` is true, descendants of `$exclude` terms will also
#// be excluded; see `$exclude_tree`. See get_terms().
#// Default empty string.
#// @type array|string $exclude_tree          Array or comma/space-separated string of term IDs to exclude, along
#// with their descendants. See get_terms(). Default empty string.
#// @type string       $feed                  Text to use for the feed link. Default 'Feed for all posts filed
#// under [cat name]'.
#// @type string       $feed_image            URL of an image to use for the feed link. Default empty string.
#// @type string       $feed_type             Feed type. Used to build feed link. See get_term_feed_link().
#// Default empty string (default feed).
#// @type bool         $hide_title_if_empty   Whether to hide the `$title_li` element if there are no terms in
#// the list. Default false (title will always be shown).
#// @type string       $separator             Separator between links. Default '<br />'.
#// @type bool|int     $show_count            Whether to include post counts. Accepts 0, 1, or their bool equivalents.
#// Default 0.
#// @type string       $show_option_all       Text to display for showing all categories. Default empty string.
#// @type string       $show_option_none      Text to display for the 'no categories' option.
#// Default 'No categories'.
#// @type string       $style                 The style used to display the categories list. If 'list', categories
#// will be output as an unordered list. If left empty or another value,
#// categories will be output separated by `<br>` tags. Default 'list'.
#// @type string       $title_li              Text to use for the list title `<li>` element. Pass an empty string
#// to disable. Default 'Categories'.
#// @type bool|int     $use_desc_for_title    Whether to use the category description as the title attribute.
#// Accepts 0, 1, or their bool equivalents. Default 1.
#// }
#// @return void|string|false Void if 'echo' argument is true, HTML list of categories if 'echo' is false.
#// False if the taxonomy does not exist.
#//
def wp_list_categories(args="", *args_):
    
    defaults = Array({"child_of": 0, "current_category": 0, "depth": 0, "echo": 1, "exclude": "", "exclude_tree": "", "feed": "", "feed_image": "", "feed_type": "", "hide_empty": 1, "hide_title_if_empty": False, "hierarchical": True, "order": "ASC", "orderby": "name", "separator": "<br />", "show_count": 0, "show_option_all": "", "show_option_none": __("No categories"), "style": "list", "taxonomy": "category", "title_li": __("Categories"), "use_desc_for_title": 1})
    parsed_args = wp_parse_args(args, defaults)
    if (not (php_isset(lambda : parsed_args["pad_counts"]))) and parsed_args["show_count"] and parsed_args["hierarchical"]:
        parsed_args["pad_counts"] = True
    # end if
    #// Descendants of exclusions should be excluded too.
    if True == parsed_args["hierarchical"]:
        exclude_tree = Array()
        if parsed_args["exclude_tree"]:
            exclude_tree = php_array_merge(exclude_tree, wp_parse_id_list(parsed_args["exclude_tree"]))
        # end if
        if parsed_args["exclude"]:
            exclude_tree = php_array_merge(exclude_tree, wp_parse_id_list(parsed_args["exclude"]))
        # end if
        parsed_args["exclude_tree"] = exclude_tree
        parsed_args["exclude"] = ""
    # end if
    if (not (php_isset(lambda : parsed_args["class"]))):
        parsed_args["class"] = "categories" if "category" == parsed_args["taxonomy"] else parsed_args["taxonomy"]
    # end if
    if (not taxonomy_exists(parsed_args["taxonomy"])):
        return False
    # end if
    show_option_all = parsed_args["show_option_all"]
    show_option_none = parsed_args["show_option_none"]
    categories = get_categories(parsed_args)
    output = ""
    if parsed_args["title_li"] and "list" == parsed_args["style"] and (not php_empty(lambda : categories)) or (not parsed_args["hide_title_if_empty"]):
        output = "<li class=\"" + esc_attr(parsed_args["class"]) + "\">" + parsed_args["title_li"] + "<ul>"
    # end if
    if php_empty(lambda : categories):
        if (not php_empty(lambda : show_option_none)):
            if "list" == parsed_args["style"]:
                output += "<li class=\"cat-item-none\">" + show_option_none + "</li>"
            else:
                output += show_option_none
            # end if
        # end if
    else:
        if (not php_empty(lambda : show_option_all)):
            posts_page = ""
            #// For taxonomies that belong only to custom post types, point to a valid archive.
            taxonomy_object = get_taxonomy(parsed_args["taxonomy"])
            if (not php_in_array("post", taxonomy_object.object_type)) and (not php_in_array("page", taxonomy_object.object_type)):
                for object_type in taxonomy_object.object_type:
                    _object_type = get_post_type_object(object_type)
                    #// Grab the first one.
                    if (not php_empty(lambda : _object_type.has_archive)):
                        posts_page = get_post_type_archive_link(object_type)
                        break
                    # end if
                # end for
            # end if
            #// Fallback for the 'All' link is the posts page.
            if (not posts_page):
                if "page" == get_option("show_on_front") and get_option("page_for_posts"):
                    posts_page = get_permalink(get_option("page_for_posts"))
                else:
                    posts_page = home_url("/")
                # end if
            # end if
            posts_page = esc_url(posts_page)
            if "list" == parsed_args["style"]:
                output += str("<li class='cat-item-all'><a href='") + str(posts_page) + str("'>") + str(show_option_all) + str("</a></li>")
            else:
                output += str("<a href='") + str(posts_page) + str("'>") + str(show_option_all) + str("</a>")
            # end if
        # end if
        if php_empty(lambda : parsed_args["current_category"]) and is_category() or is_tax() or is_tag():
            current_term_object = get_queried_object()
            if current_term_object and parsed_args["taxonomy"] == current_term_object.taxonomy:
                parsed_args["current_category"] = get_queried_object_id()
            # end if
        # end if
        if parsed_args["hierarchical"]:
            depth = parsed_args["depth"]
        else:
            depth = -1
            pass
        # end if
        output += walk_category_tree(categories, depth, parsed_args)
    # end if
    if parsed_args["title_li"] and "list" == parsed_args["style"] and (not php_empty(lambda : categories)) or (not parsed_args["hide_title_if_empty"]):
        output += "</ul></li>"
    # end if
    #// 
    #// Filters the HTML output of a taxonomy list.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string $output HTML output.
    #// @param array  $args   An array of taxonomy-listing arguments.
    #//
    html = apply_filters("wp_list_categories", output, args)
    if parsed_args["echo"]:
        php_print(html)
    else:
        return html
    # end if
# end def wp_list_categories
#// 
#// Displays a tag cloud.
#// 
#// @since 2.3.0
#// @since 4.8.0 Added the `show_count` argument.
#// 
#// @param array|string $args {
#// Optional. Array or string of arguments for displaying a tag cloud. See wp_generate_tag_cloud()
#// and get_terms() for the full lists of arguments that can be passed in `$args`.
#// 
#// @type int    $number    The number of tags to display. Accepts any positive integer
#// or zero to return all. Default 0 (all tags).
#// @type string $link      Whether to display term editing links or term permalinks.
#// Accepts 'edit' and 'view'. Default 'view'.
#// @type string $post_type The post type. Used to highlight the proper post type menu
#// on the linked edit page. Defaults to the first post type
#// associated with the taxonomy.
#// @type bool   $echo      Whether or not to echo the return value. Default true.
#// }
#// @return void|string|array Void if 'echo' argument is true, or on failure. Otherwise, tag cloud
#// as a string or an array, depending on 'format' argument.
#//
def wp_tag_cloud(args="", *args_):
    
    defaults = Array({"smallest": 8, "largest": 22, "unit": "pt", "number": 45, "format": "flat", "separator": "\n", "orderby": "name", "order": "ASC", "exclude": "", "include": "", "link": "view", "taxonomy": "post_tag", "post_type": "", "echo": True, "show_count": 0})
    args = wp_parse_args(args, defaults)
    tags = get_terms(php_array_merge(args, Array({"orderby": "count", "order": "DESC"})))
    #// Always query top tags.
    if php_empty(lambda : tags) or is_wp_error(tags):
        return
    # end if
    for key,tag in tags:
        if "edit" == args["link"]:
            link = get_edit_term_link(tag.term_id, tag.taxonomy, args["post_type"])
        else:
            link = get_term_link(php_intval(tag.term_id), tag.taxonomy)
        # end if
        if is_wp_error(link):
            return
        # end if
        tags[key].link = link
        tags[key].id = tag.term_id
    # end for
    #// Here's where those top tags get sorted according to $args.
    return_ = wp_generate_tag_cloud(tags, args)
    #// 
    #// Filters the tag cloud output.
    #// 
    #// @since 2.3.0
    #// 
    #// @param string|array $return Tag cloud as a string or an array, depending on 'format' argument.
    #// @param array        $args   An array of tag cloud arguments.
    #//
    return_ = apply_filters("wp_tag_cloud", return_, args)
    if "array" == args["format"] or php_empty(lambda : args["echo"]):
        return return_
    # end if
    php_print(return_)
# end def wp_tag_cloud
#// 
#// Default topic count scaling for tag links.
#// 
#// @since 2.9.0
#// 
#// @param int $count Number of posts with that tag.
#// @return int Scaled count.
#//
def default_topic_count_scale(count=None, *args_):
    
    return round(log10(count + 1) * 100)
# end def default_topic_count_scale
#// 
#// Generates a tag cloud (heatmap) from provided data.
#// 
#// @todo Complete functionality.
#// @since 2.3.0
#// @since 4.8.0 Added the `show_count` argument.
#// 
#// @param WP_Term[]    $tags Array of WP_Term objects to generate the tag cloud for.
#// @param string|array $args {
#// Optional. Array or string of arguments for generating a tag cloud.
#// 
#// @type int      $smallest                   Smallest font size used to display tags. Paired
#// with the value of `$unit`, to determine CSS text
#// size unit. Default 8 (pt).
#// @type int      $largest                    Largest font size used to display tags. Paired
#// with the value of `$unit`, to determine CSS text
#// size unit. Default 22 (pt).
#// @type string   $unit                       CSS text size unit to use with the `$smallest`
#// and `$largest` values. Accepts any valid CSS text
#// size unit. Default 'pt'.
#// @type int      $number                     The number of tags to return. Accepts any
#// positive integer or zero to return all.
#// Default 0.
#// @type string   $format                     Format to display the tag cloud in. Accepts 'flat'
#// (tags separated with spaces), 'list' (tags displayed
#// in an unordered list), or 'array' (returns an array).
#// Default 'flat'.
#// @type string   $separator                  HTML or text to separate the tags. Default "\n" (newline).
#// @type string   $orderby                    Value to order tags by. Accepts 'name' or 'count'.
#// Default 'name'. The {@see 'tag_cloud_sort'} filter
#// can also affect how tags are sorted.
#// @type string   $order                      How to order the tags. Accepts 'ASC' (ascending),
#// 'DESC' (descending), or 'RAND' (random). Default 'ASC'.
#// @type int|bool $filter                     Whether to enable filtering of the final output
#// via {@see 'wp_generate_tag_cloud'}. Default 1|true.
#// @type string   $topic_count_text           Nooped plural text from _n_noop() to supply to
#// tag counts. Default null.
#// @type callable $topic_count_text_callback  Callback used to generate nooped plural text for
#// tag counts based on the count. Default null.
#// @type callable $topic_count_scale_callback Callback used to determine the tag count scaling
#// value. Default default_topic_count_scale().
#// @type bool|int $show_count                 Whether to display the tag counts. Default 0. Accepts
#// 0, 1, or their bool equivalents.
#// }
#// @return string|array Tag cloud as a string or an array, depending on 'format' argument.
#//
def wp_generate_tag_cloud(tags=None, args="", *args_):
    
    defaults = Array({"smallest": 8, "largest": 22, "unit": "pt", "number": 0, "format": "flat", "separator": "\n", "orderby": "name", "order": "ASC", "topic_count_text": None, "topic_count_text_callback": None, "topic_count_scale_callback": "default_topic_count_scale", "filter": 1, "show_count": 0})
    args = wp_parse_args(args, defaults)
    return_ = Array() if "array" == args["format"] else ""
    if php_empty(lambda : tags):
        return return_
    # end if
    #// Juggle topic counts.
    if (php_isset(lambda : args["topic_count_text"])):
        #// First look for nooped plural support via topic_count_text.
        translate_nooped_plural = args["topic_count_text"]
    elif (not php_empty(lambda : args["topic_count_text_callback"])):
        #// Look for the alternative callback style. Ignore the previous default.
        if "default_topic_count_text" == args["topic_count_text_callback"]:
            #// translators: %s: Number of items (tags).
            translate_nooped_plural = _n_noop("%s item", "%s items")
        else:
            translate_nooped_plural = False
        # end if
    elif (php_isset(lambda : args["single_text"])) and (php_isset(lambda : args["multiple_text"])):
        #// If no callback exists, look for the old-style single_text and multiple_text arguments.
        #// phpcs:ignore WordPress.WP.I18n.NonSingularStringLiteralSingle,WordPress.WP.I18n.NonSingularStringLiteralPlural
        translate_nooped_plural = _n_noop(args["single_text"], args["multiple_text"])
    else:
        #// This is the default for when no callback, plural, or argument is passed in.
        #// translators: %s: Number of items (tags).
        translate_nooped_plural = _n_noop("%s item", "%s items")
    # end if
    #// 
    #// Filters how the items in a tag cloud are sorted.
    #// 
    #// @since 2.8.0
    #// 
    #// @param WP_Term[] $tags Ordered array of terms.
    #// @param array     $args An array of tag cloud arguments.
    #//
    tags_sorted = apply_filters("tag_cloud_sort", tags, args)
    if php_empty(lambda : tags_sorted):
        return return_
    # end if
    if tags_sorted != tags:
        tags = tags_sorted
        tags_sorted = None
    else:
        if "RAND" == args["order"]:
            shuffle(tags)
        else:
            #// SQL cannot save you; this is a second (potentially different) sort on a subset of data.
            if "name" == args["orderby"]:
                uasort(tags, "_wp_object_name_sort_cb")
            else:
                uasort(tags, "_wp_object_count_sort_cb")
            # end if
            if "DESC" == args["order"]:
                tags = array_reverse(tags, True)
            # end if
        # end if
    # end if
    if args["number"] > 0:
        tags = php_array_slice(tags, 0, args["number"])
    # end if
    counts = Array()
    real_counts = Array()
    #// For the alt tag.
    for key,tag in tags:
        real_counts[key] = tag.count
        counts[key] = php_call_user_func(args["topic_count_scale_callback"], tag.count)
    # end for
    min_count = php_min(counts)
    spread = php_max(counts) - min_count
    if spread <= 0:
        spread = 1
    # end if
    font_spread = args["largest"] - args["smallest"]
    if font_spread < 0:
        font_spread = 1
    # end if
    font_step = font_spread / spread
    aria_label = False
    #// 
    #// Determine whether to output an 'aria-label' attribute with the tag name and count.
    #// When tags have a different font size, they visually convey an important information
    #// that should be available to assistive technologies too. On the other hand, sometimes
    #// themes set up the Tag Cloud to display all tags with the same font size (setting
    #// the 'smallest' and 'largest' arguments to the same value).
    #// In order to always serve the same content to all users, the 'aria-label' gets printed out:
    #// - when tags have a different size
    #// - when the tag count is displayed (for example when users check the checkbox in the
    #// Tag Cloud widget), regardless of the tags font size
    #//
    if args["show_count"] or 0 != font_spread:
        aria_label = True
    # end if
    #// Assemble the data that will be used to generate the tag cloud markup.
    tags_data = Array()
    for key,tag in tags:
        tag_id = tag.id if (php_isset(lambda : tag.id)) else key
        count = counts[key]
        real_count = real_counts[key]
        if translate_nooped_plural:
            formatted_count = php_sprintf(translate_nooped_plural(translate_nooped_plural, real_count), number_format_i18n(real_count))
        else:
            formatted_count = php_call_user_func(args["topic_count_text_callback"], real_count, tag, args)
        # end if
        tags_data[-1] = Array({"id": tag_id, "url": tag.link if "#" != tag.link else "#", "role": "" if "#" != tag.link else " role=\"button\"", "name": tag.name, "formatted_count": formatted_count, "slug": tag.slug, "real_count": real_count, "class": "tag-cloud-link tag-link-" + tag_id, "font_size": args["smallest"] + count - min_count * font_step, "aria_label": php_sprintf(" aria-label=\"%1$s (%2$s)\"", esc_attr(tag.name), esc_attr(formatted_count)) if aria_label else "", "show_count": "<span class=\"tag-link-count\"> (" + real_count + ")</span>" if args["show_count"] else ""})
    # end for
    #// 
    #// Filters the data used to generate the tag cloud.
    #// 
    #// @since 4.3.0
    #// 
    #// @param array $tags_data An array of term data for term used to generate the tag cloud.
    #//
    tags_data = apply_filters("wp_generate_tag_cloud_data", tags_data)
    a = Array()
    #// Generate the output links array.
    for key,tag_data in tags_data:
        class_ = tag_data["class"] + " tag-link-position-" + key + 1
        a[-1] = php_sprintf("<a href=\"%1$s\"%2$s class=\"%3$s\" style=\"font-size: %4$s;\"%5$s>%6$s%7$s</a>", esc_url(tag_data["url"]), tag_data["role"], esc_attr(class_), esc_attr(php_str_replace(",", ".", tag_data["font_size"]) + args["unit"]), tag_data["aria_label"], esc_html(tag_data["name"]), tag_data["show_count"])
    # end for
    for case in Switch(args["format"]):
        if case("array"):
            return_ = a
            break
        # end if
        if case("list"):
            #// 
            #// Force role="list", as some browsers (sic: Safari 10) don't expose to assistive
            #// technologies the default role when the list is styled with `list-style: none`.
            #// Note: this is redundant but doesn't harm.
            #//
            return_ = "<ul class='wp-tag-cloud' role='list'>\n  <li>"
            return_ += join("</li>\n    <li>", a)
            return_ += "</li>\n</ul>\n"
            break
        # end if
        if case():
            return_ = join(args["separator"], a)
            break
        # end if
    # end for
    if args["filter"]:
        #// 
        #// Filters the generated output of a tag cloud.
        #// 
        #// The filter is only evaluated if a true value is passed
        #// to the $filter argument in wp_generate_tag_cloud().
        #// 
        #// @since 2.3.0
        #// 
        #// @see wp_generate_tag_cloud()
        #// 
        #// @param array|string $return String containing the generated HTML tag cloud output
        #// or an array of tag links if the 'format' argument
        #// equals 'array'.
        #// @param WP_Term[]    $tags   An array of terms used in the tag cloud.
        #// @param array        $args   An array of wp_generate_tag_cloud() arguments.
        #//
        return apply_filters("wp_generate_tag_cloud", return_, tags, args)
    else:
        return return_
    # end if
# end def wp_generate_tag_cloud
#// 
#// Serves as a callback for comparing objects based on name.
#// 
#// Used with `uasort()`.
#// 
#// @since 3.1.0
#// @access private
#// 
#// @param object $a The first object to compare.
#// @param object $b The second object to compare.
#// @return int Negative number if `$a->name` is less than `$b->name`, zero if they are equal,
#// or greater than zero if `$a->name` is greater than `$b->name`.
#//
def _wp_object_name_sort_cb(a=None, b=None, *args_):
    
    return strnatcasecmp(a.name, b.name)
# end def _wp_object_name_sort_cb
#// 
#// Serves as a callback for comparing objects based on count.
#// 
#// Used with `uasort()`.
#// 
#// @since 3.1.0
#// @access private
#// 
#// @param object $a The first object to compare.
#// @param object $b The second object to compare.
#// @return bool Whether the count value for `$a` is greater than the count value for `$b`.
#//
def _wp_object_count_sort_cb(a=None, b=None, *args_):
    
    return a.count > b.count
# end def _wp_object_count_sort_cb
#// 
#// Helper functions.
#// 
#// 
#// Retrieve HTML list content for category list.
#// 
#// @since 2.1.0
#// @since 5.3.0 Formalized the existing `...$args` parameter by adding it
#// to the function signature.
#// 
#// @uses Walker_Category to create HTML list content.
#// @see Walker::walk() for parameters and return description.
#// 
#// @param mixed ...$args Elements array, maximum hierarchical depth and optional additional arguments.
#// @return string
#//
def walk_category_tree(*args):
    
    #// The user's options are the third parameter.
    if php_empty(lambda : args[2]["walker"]) or (not type(args[2]["walker"]).__name__ == "Walker"):
        walker = php_new_class("Walker_Category", lambda : Walker_Category())
    else:
        walker = args[2]["walker"]
    # end if
    return walker.walk(args)
# end def walk_category_tree
#// 
#// Retrieve HTML dropdown (select) content for category list.
#// 
#// @since 2.1.0
#// @since 5.3.0 Formalized the existing `...$args` parameter by adding it
#// to the function signature.
#// 
#// @uses Walker_CategoryDropdown to create HTML dropdown content.
#// @see Walker::walk() for parameters and return description.
#// 
#// @param mixed ...$args Elements array, maximum hierarchical depth and optional additional arguments.
#// @return string
#//
def walk_category_dropdown_tree(*args):
    
    #// The user's options are the third parameter.
    if php_empty(lambda : args[2]["walker"]) or (not type(args[2]["walker"]).__name__ == "Walker"):
        walker = php_new_class("Walker_CategoryDropdown", lambda : Walker_CategoryDropdown())
    else:
        walker = args[2]["walker"]
    # end if
    return walker.walk(args)
# end def walk_category_dropdown_tree
#// 
#// Tags.
#// 
#// 
#// Retrieve the link to the tag.
#// 
#// @since 2.3.0
#// @see get_term_link()
#// 
#// @param int|object $tag Tag ID or object.
#// @return string Link on success, empty string if tag does not exist.
#//
def get_tag_link(tag=None, *args_):
    
    return get_category_link(tag)
# end def get_tag_link
#// 
#// Retrieve the tags for a post.
#// 
#// @since 2.3.0
#// 
#// @param int $id Post ID.
#// @return array|false|WP_Error Array of tag objects on success, false on failure.
#//
def get_the_tags(id=0, *args_):
    
    #// 
    #// Filters the array of tags for the given post.
    #// 
    #// @since 2.3.0
    #// 
    #// @see get_the_terms()
    #// 
    #// @param WP_Term[] $terms An array of tags for the given post.
    #//
    return apply_filters("get_the_tags", get_the_terms(id, "post_tag"))
# end def get_the_tags
#// 
#// Retrieve the tags for a post formatted as a string.
#// 
#// @since 2.3.0
#// 
#// @param string $before Optional. Before tags.
#// @param string $sep Optional. Between tags.
#// @param string $after Optional. After tags.
#// @param int $id Optional. Post ID. Defaults to the current post.
#// @return string|false|WP_Error A list of tags on success, false if there are no terms, WP_Error on failure.
#//
def get_the_tag_list(before="", sep="", after="", id=0, *args_):
    
    #// 
    #// Filters the tags list for a given post.
    #// 
    #// @since 2.3.0
    #// 
    #// @param string $tag_list List of tags.
    #// @param string $before   String to use before tags.
    #// @param string $sep      String to use between the tags.
    #// @param string $after    String to use after tags.
    #// @param int    $id       Post ID.
    #//
    return apply_filters("the_tags", get_the_term_list(id, "post_tag", before, sep, after), before, sep, after, id)
# end def get_the_tag_list
#// 
#// Retrieve the tags for a post.
#// 
#// @since 2.3.0
#// 
#// @param string $before Optional. Before list.
#// @param string $sep Optional. Separate items using this.
#// @param string $after Optional. After list.
#//
def the_tags(before=None, sep=", ", after="", *args_):
    
    if None == before:
        before = __("Tags: ")
    # end if
    the_tags = get_the_tag_list(before, sep, after)
    if (not is_wp_error(the_tags)):
        php_print(the_tags)
    # end if
# end def the_tags
#// 
#// Retrieve tag description.
#// 
#// @since 2.8.0
#// 
#// @param int $tag Optional. Tag ID. Will use global tag ID by default.
#// @return string Tag description, available.
#//
def tag_description(tag=0, *args_):
    
    return term_description(tag)
# end def tag_description
#// 
#// Retrieve term description.
#// 
#// @since 2.8.0
#// @since 4.9.2 The `$taxonomy` parameter was deprecated.
#// 
#// @param int  $term       Optional. Term ID. Will use global term ID by default.
#// @param null $deprecated Deprecated argument.
#// @return string Term description, available.
#//
def term_description(term=0, deprecated=None, *args_):
    
    if (not term) and is_tax() or is_tag() or is_category():
        term = get_queried_object()
        if term:
            term = term.term_id
        # end if
    # end if
    description = get_term_field("description", term)
    return "" if is_wp_error(description) else description
# end def term_description
#// 
#// Retrieve the terms of the taxonomy that are attached to the post.
#// 
#// @since 2.5.0
#// 
#// @param int|WP_Post $post     Post ID or object.
#// @param string      $taxonomy Taxonomy name.
#// @return WP_Term[]|false|WP_Error Array of WP_Term objects on success, false if there are no terms
#// or the post does not exist, WP_Error on failure.
#//
def get_the_terms(post=None, taxonomy=None, *args_):
    
    post = get_post(post)
    if (not post):
        return False
    # end if
    terms = get_object_term_cache(post.ID, taxonomy)
    if False == terms:
        terms = wp_get_object_terms(post.ID, taxonomy)
        if (not is_wp_error(terms)):
            term_ids = wp_list_pluck(terms, "term_id")
            wp_cache_add(post.ID, term_ids, taxonomy + "_relationships")
        # end if
    # end if
    #// 
    #// Filters the list of terms attached to the given post.
    #// 
    #// @since 3.1.0
    #// 
    #// @param WP_Term[]|WP_Error $terms    Array of attached terms, or WP_Error on failure.
    #// @param int                $post_id  Post ID.
    #// @param string             $taxonomy Name of the taxonomy.
    #//
    terms = apply_filters("get_the_terms", terms, post.ID, taxonomy)
    if php_empty(lambda : terms):
        return False
    # end if
    return terms
# end def get_the_terms
#// 
#// Retrieve a post's terms as a list with specified format.
#// 
#// @since 2.5.0
#// 
#// @param int    $id       Post ID.
#// @param string $taxonomy Taxonomy name.
#// @param string $before   Optional. Before list.
#// @param string $sep      Optional. Separate items using this.
#// @param string $after    Optional. After list.
#// @return string|false|WP_Error A list of terms on success, false if there are no terms, WP_Error on failure.
#//
def get_the_term_list(id=None, taxonomy=None, before="", sep="", after="", *args_):
    
    terms = get_the_terms(id, taxonomy)
    if is_wp_error(terms):
        return terms
    # end if
    if php_empty(lambda : terms):
        return False
    # end if
    links = Array()
    for term in terms:
        link = get_term_link(term, taxonomy)
        if is_wp_error(link):
            return link
        # end if
        links[-1] = "<a href=\"" + esc_url(link) + "\" rel=\"tag\">" + term.name + "</a>"
    # end for
    #// 
    #// Filters the term links for a given taxonomy.
    #// 
    #// The dynamic portion of the filter name, `$taxonomy`, refers
    #// to the taxonomy slug.
    #// 
    #// @since 2.5.0
    #// 
    #// @param string[] $links An array of term links.
    #//
    term_links = apply_filters(str("term_links-") + str(taxonomy), links)
    #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
    return before + join(sep, term_links) + after
# end def get_the_term_list
#// 
#// Retrieve term parents with separator.
#// 
#// @since 4.8.0
#// 
#// @param int     $term_id  Term ID.
#// @param string  $taxonomy Taxonomy name.
#// @param string|array $args {
#// Array of optional arguments.
#// 
#// @type string $format    Use term names or slugs for display. Accepts 'name' or 'slug'.
#// Default 'name'.
#// @type string $separator Separator for between the terms. Default '/'.
#// @type bool   $link      Whether to format as a link. Default true.
#// @type bool   $inclusive Include the term to get the parents for. Default true.
#// }
#// @return string|WP_Error A list of term parents on success, WP_Error or empty string on failure.
#//
def get_term_parents_list(term_id=None, taxonomy=None, args=Array(), *args_):
    
    list = ""
    term = get_term(term_id, taxonomy)
    if is_wp_error(term):
        return term
    # end if
    if (not term):
        return list
    # end if
    term_id = term.term_id
    defaults = Array({"format": "name", "separator": "/", "link": True, "inclusive": True})
    args = wp_parse_args(args, defaults)
    for bool in Array("link", "inclusive"):
        args[bool] = wp_validate_boolean(args[bool])
    # end for
    parents = get_ancestors(term_id, taxonomy, "taxonomy")
    if args["inclusive"]:
        array_unshift(parents, term_id)
    # end if
    for term_id in array_reverse(parents):
        parent = get_term(term_id, taxonomy)
        name = parent.slug if "slug" == args["format"] else parent.name
        if args["link"]:
            list += "<a href=\"" + esc_url(get_term_link(parent.term_id, taxonomy)) + "\">" + name + "</a>" + args["separator"]
        else:
            list += name + args["separator"]
        # end if
    # end for
    return list
# end def get_term_parents_list
#// 
#// Display the terms in a list.
#// 
#// @since 2.5.0
#// 
#// @param int    $id       Post ID.
#// @param string $taxonomy Taxonomy name.
#// @param string $before   Optional. Before list.
#// @param string $sep      Optional. Separate items using this.
#// @param string $after    Optional. After list.
#// @return void|false Void on success, false on failure.
#//
def the_terms(id=None, taxonomy=None, before="", sep=", ", after="", *args_):
    
    term_list = get_the_term_list(id, taxonomy, before, sep, after)
    if is_wp_error(term_list):
        return False
    # end if
    #// 
    #// Filters the list of terms to display.
    #// 
    #// @since 2.9.0
    #// 
    #// @param string $term_list List of terms to display.
    #// @param string $taxonomy  The taxonomy name.
    #// @param string $before    String to use before the terms.
    #// @param string $sep       String to use between the terms.
    #// @param string $after     String to use after the terms.
    #//
    php_print(apply_filters("the_terms", term_list, taxonomy, before, sep, after))
# end def the_terms
#// 
#// Check if the current post has any of given category.
#// 
#// @since 3.1.0
#// 
#// @param string|int|array $category Optional. The category name/term_id/slug or array of them to check for.
#// @param int|object       $post     Optional. Post to check instead of the current post.
#// @return bool True if the current post has any of the given categories (or any category, if no category specified).
#//
def has_category(category="", post=None, *args_):
    
    return has_term(category, "category", post)
# end def has_category
#// 
#// Checks if the current post has any of given tags.
#// 
#// The given tags are checked against the post's tags' term_ids, names and slugs.
#// Tags given as integers will only be checked against the post's tags' term_ids.
#// If no tags are given, determines if post has any tags.
#// 
#// Prior to v2.7 of WordPress, tags given as integers would also be checked against the post's tags' names and slugs (in addition to term_ids)
#// Prior to v2.7, this function could only be used in the WordPress Loop.
#// As of 2.7, the function can be used anywhere if it is provided a post ID or post object.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 2.6.0
#// 
#// @param string|int|array $tag  Optional. The tag name/term_id/slug or array of them to check for.
#// @param int|object       $post Optional. Post to check instead of the current post. (since 2.7.0)
#// @return bool True if the current post has any of the given tags (or any tag, if no tag specified).
#//
def has_tag(tag="", post=None, *args_):
    
    return has_term(tag, "post_tag", post)
# end def has_tag
#// 
#// Check if the current post has any of given terms.
#// 
#// The given terms are checked against the post's terms' term_ids, names and slugs.
#// Terms given as integers will only be checked against the post's terms' term_ids.
#// If no terms are given, determines if post has any terms.
#// 
#// @since 3.1.0
#// 
#// @param string|int|array $term     Optional. The term name/term_id/slug or array of them to check for.
#// @param string           $taxonomy Taxonomy name.
#// @param int|WP_Post      $post     Optional. Post to check instead of the current post.
#// @return bool True if the current post has any of the given tags (or any tag, if no tag specified).
#//
def has_term(term="", taxonomy="", post=None, *args_):
    
    post = get_post(post)
    if (not post):
        return False
    # end if
    r = is_object_in_term(post.ID, taxonomy, term)
    if is_wp_error(r):
        return False
    # end if
    return r
# end def has_term
