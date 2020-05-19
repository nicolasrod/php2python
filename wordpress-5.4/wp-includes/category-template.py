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
def get_category_link(category_=None, *_args_):
    
    
    if (not php_is_object(category_)):
        category_ = php_int(category_)
    # end if
    category_ = get_term_link(category_)
    if is_wp_error(category_):
        return ""
    # end if
    return category_
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
def get_category_parents(id_=None, link_=None, separator_="/", nicename_=None, deprecated_=None, *_args_):
    if link_ is None:
        link_ = False
    # end if
    if nicename_ is None:
        nicename_ = False
    # end if
    if deprecated_ is None:
        deprecated_ = Array()
    # end if
    
    if (not php_empty(lambda : deprecated_)):
        _deprecated_argument(__FUNCTION__, "4.8.0")
    # end if
    format_ = "slug" if nicename_ else "name"
    args_ = Array({"separator": separator_, "link": link_, "format": format_})
    return get_term_parents_list(id_, "category", args_)
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
def get_the_category(id_=None, *_args_):
    if id_ is None:
        id_ = False
    # end if
    
    categories_ = get_the_terms(id_, "category")
    if (not categories_) or is_wp_error(categories_):
        categories_ = Array()
    # end if
    categories_ = php_array_values(categories_)
    for key_ in php_array_keys(categories_):
        _make_cat_compat(categories_[key_])
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
    return apply_filters("get_the_categories", categories_, id_)
# end def get_the_category
#// 
#// Retrieve category name based on category ID.
#// 
#// @since 0.71
#// 
#// @param int $cat_ID Category ID.
#// @return string|WP_Error Category name on success, WP_Error on failure.
#//
def get_the_category_by_ID(cat_ID_=None, *_args_):
    
    
    #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.FunctionNameInvalid
    cat_ID_ = php_int(cat_ID_)
    category_ = get_term(cat_ID_)
    if is_wp_error(category_):
        return category_
    # end if
    return category_.name if category_ else ""
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
def get_the_category_list(separator_="", parents_="", post_id_=None, *_args_):
    if post_id_ is None:
        post_id_ = False
    # end if
    
    global wp_rewrite_
    php_check_if_defined("wp_rewrite_")
    if (not is_object_in_taxonomy(get_post_type(post_id_), "category")):
        #// This filter is documented in wp-includes/category-template.php
        return apply_filters("the_category", "", separator_, parents_)
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
    categories_ = apply_filters("the_category_list", get_the_category(post_id_), post_id_)
    if php_empty(lambda : categories_):
        #// This filter is documented in wp-includes/category-template.php
        return apply_filters("the_category", __("Uncategorized"), separator_, parents_)
    # end if
    rel_ = "rel=\"category tag\"" if php_is_object(wp_rewrite_) and wp_rewrite_.using_permalinks() else "rel=\"category\""
    thelist_ = ""
    if "" == separator_:
        thelist_ += "<ul class=\"post-categories\">"
        for category_ in categories_:
            thelist_ += "\n <li>"
            for case in Switch(php_strtolower(parents_)):
                if case("multiple"):
                    if category_.parent:
                        thelist_ += get_category_parents(category_.parent, True, separator_)
                    # end if
                    thelist_ += "<a href=\"" + esc_url(get_category_link(category_.term_id)) + "\" " + rel_ + ">" + category_.name + "</a></li>"
                    break
                # end if
                if case("single"):
                    thelist_ += "<a href=\"" + esc_url(get_category_link(category_.term_id)) + "\"  " + rel_ + ">"
                    if category_.parent:
                        thelist_ += get_category_parents(category_.parent, False, separator_)
                    # end if
                    thelist_ += category_.name + "</a></li>"
                    break
                # end if
                if case(""):
                    pass
                # end if
                if case():
                    thelist_ += "<a href=\"" + esc_url(get_category_link(category_.term_id)) + "\" " + rel_ + ">" + category_.name + "</a></li>"
                # end if
            # end for
        # end for
        thelist_ += "</ul>"
    else:
        i_ = 0
        for category_ in categories_:
            if 0 < i_:
                thelist_ += separator_
            # end if
            for case in Switch(php_strtolower(parents_)):
                if case("multiple"):
                    if category_.parent:
                        thelist_ += get_category_parents(category_.parent, True, separator_)
                    # end if
                    thelist_ += "<a href=\"" + esc_url(get_category_link(category_.term_id)) + "\" " + rel_ + ">" + category_.name + "</a>"
                    break
                # end if
                if case("single"):
                    thelist_ += "<a href=\"" + esc_url(get_category_link(category_.term_id)) + "\" " + rel_ + ">"
                    if category_.parent:
                        thelist_ += get_category_parents(category_.parent, False, separator_)
                    # end if
                    thelist_ += str(category_.name) + str("</a>")
                    break
                # end if
                if case(""):
                    pass
                # end if
                if case():
                    thelist_ += "<a href=\"" + esc_url(get_category_link(category_.term_id)) + "\" " + rel_ + ">" + category_.name + "</a>"
                # end if
            # end for
            i_ += 1
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
    return apply_filters("the_category", thelist_, separator_, parents_)
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
def in_category(category_=None, post_=None, *_args_):
    if post_ is None:
        post_ = None
    # end if
    
    if php_empty(lambda : category_):
        return False
    # end if
    return has_category(category_, post_)
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
def the_category(separator_="", parents_="", post_id_=None, *_args_):
    if post_id_ is None:
        post_id_ = False
    # end if
    
    php_print(get_the_category_list(separator_, parents_, post_id_))
# end def the_category
#// 
#// Retrieve category description.
#// 
#// @since 1.0.0
#// 
#// @param int $category Optional. Category ID. Will use global category ID by default.
#// @return string Category description, available.
#//
def category_description(category_=0, *_args_):
    
    
    return term_description(category_)
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
def wp_dropdown_categories(args_="", *_args_):
    
    
    defaults_ = Array({"show_option_all": "", "show_option_none": "", "orderby": "id", "order": "ASC", "show_count": 0, "hide_empty": 1, "child_of": 0, "exclude": "", "echo": 1, "selected": 0, "hierarchical": 0, "name": "cat", "id": "", "class": "postform", "depth": 0, "tab_index": 0, "taxonomy": "category", "hide_if_empty": False, "option_none_value": -1, "value_field": "term_id", "required": False})
    defaults_["selected"] = get_query_var("cat") if is_category() else 0
    #// Back compat.
    if (php_isset(lambda : args_["type"])) and "link" == args_["type"]:
        _deprecated_argument(__FUNCTION__, "3.0.0", php_sprintf(__("%1$s is deprecated. Use %2$s instead."), "<code>type => link</code>", "<code>taxonomy => link_category</code>"))
        args_["taxonomy"] = "link_category"
    # end if
    #// Parse incoming $args into an array and merge it with $defaults.
    parsed_args_ = wp_parse_args(args_, defaults_)
    option_none_value_ = parsed_args_["option_none_value"]
    if (not (php_isset(lambda : parsed_args_["pad_counts"]))) and parsed_args_["show_count"] and parsed_args_["hierarchical"]:
        parsed_args_["pad_counts"] = True
    # end if
    tab_index_ = parsed_args_["tab_index"]
    tab_index_attribute_ = ""
    if php_int(tab_index_) > 0:
        tab_index_attribute_ = str(" tabindex=\"") + str(tab_index_) + str("\"")
    # end if
    #// Avoid clashes with the 'name' param of get_terms().
    get_terms_args_ = parsed_args_
    get_terms_args_["name"] = None
    categories_ = get_terms(get_terms_args_)
    name_ = esc_attr(parsed_args_["name"])
    class_ = esc_attr(parsed_args_["class"])
    id_ = esc_attr(parsed_args_["id"]) if parsed_args_["id"] else name_
    required_ = "required" if parsed_args_["required"] else ""
    if (not parsed_args_["hide_if_empty"]) or (not php_empty(lambda : categories_)):
        output_ = str("<select ") + str(required_) + str(" name='") + str(name_) + str("' id='") + str(id_) + str("' class='") + str(class_) + str("' ") + str(tab_index_attribute_) + str(">\n")
    else:
        output_ = ""
    # end if
    if php_empty(lambda : categories_) and (not parsed_args_["hide_if_empty"]) and (not php_empty(lambda : parsed_args_["show_option_none"])):
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
        show_option_none_ = apply_filters("list_cats", parsed_args_["show_option_none"], None)
        output_ += "    <option value='" + esc_attr(option_none_value_) + str("' selected='selected'>") + str(show_option_none_) + str("</option>\n")
    # end if
    if (not php_empty(lambda : categories_)):
        if parsed_args_["show_option_all"]:
            #// This filter is documented in wp-includes/category-template.php
            show_option_all_ = apply_filters("list_cats", parsed_args_["show_option_all"], None)
            selected_ = " selected='selected'" if "0" == php_strval(parsed_args_["selected"]) else ""
            output_ += str("    <option value='0'") + str(selected_) + str(">") + str(show_option_all_) + str("</option>\n")
        # end if
        if parsed_args_["show_option_none"]:
            #// This filter is documented in wp-includes/category-template.php
            show_option_none_ = apply_filters("list_cats", parsed_args_["show_option_none"], None)
            selected_ = selected(option_none_value_, parsed_args_["selected"], False)
            output_ += "    <option value='" + esc_attr(option_none_value_) + str("'") + str(selected_) + str(">") + str(show_option_none_) + str("</option>\n")
        # end if
        if parsed_args_["hierarchical"]:
            depth_ = parsed_args_["depth"]
            pass
        else:
            depth_ = -1
            pass
        # end if
        output_ += walk_category_dropdown_tree(categories_, depth_, parsed_args_)
    # end if
    if (not parsed_args_["hide_if_empty"]) or (not php_empty(lambda : categories_)):
        output_ += "</select>\n"
    # end if
    #// 
    #// Filters the taxonomy drop-down output.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string $output      HTML output.
    #// @param array  $parsed_args Arguments used to build the drop-down.
    #//
    output_ = apply_filters("wp_dropdown_cats", output_, parsed_args_)
    if parsed_args_["echo"]:
        php_print(output_)
    # end if
    return output_
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
def wp_list_categories(args_="", *_args_):
    
    
    defaults_ = Array({"child_of": 0, "current_category": 0, "depth": 0, "echo": 1, "exclude": "", "exclude_tree": "", "feed": "", "feed_image": "", "feed_type": "", "hide_empty": 1, "hide_title_if_empty": False, "hierarchical": True, "order": "ASC", "orderby": "name", "separator": "<br />", "show_count": 0, "show_option_all": "", "show_option_none": __("No categories"), "style": "list", "taxonomy": "category", "title_li": __("Categories"), "use_desc_for_title": 1})
    parsed_args_ = wp_parse_args(args_, defaults_)
    if (not (php_isset(lambda : parsed_args_["pad_counts"]))) and parsed_args_["show_count"] and parsed_args_["hierarchical"]:
        parsed_args_["pad_counts"] = True
    # end if
    #// Descendants of exclusions should be excluded too.
    if True == parsed_args_["hierarchical"]:
        exclude_tree_ = Array()
        if parsed_args_["exclude_tree"]:
            exclude_tree_ = php_array_merge(exclude_tree_, wp_parse_id_list(parsed_args_["exclude_tree"]))
        # end if
        if parsed_args_["exclude"]:
            exclude_tree_ = php_array_merge(exclude_tree_, wp_parse_id_list(parsed_args_["exclude"]))
        # end if
        parsed_args_["exclude_tree"] = exclude_tree_
        parsed_args_["exclude"] = ""
    # end if
    if (not (php_isset(lambda : parsed_args_["class"]))):
        parsed_args_["class"] = "categories" if "category" == parsed_args_["taxonomy"] else parsed_args_["taxonomy"]
    # end if
    if (not taxonomy_exists(parsed_args_["taxonomy"])):
        return False
    # end if
    show_option_all_ = parsed_args_["show_option_all"]
    show_option_none_ = parsed_args_["show_option_none"]
    categories_ = get_categories(parsed_args_)
    output_ = ""
    if parsed_args_["title_li"] and "list" == parsed_args_["style"] and (not php_empty(lambda : categories_)) or (not parsed_args_["hide_title_if_empty"]):
        output_ = "<li class=\"" + esc_attr(parsed_args_["class"]) + "\">" + parsed_args_["title_li"] + "<ul>"
    # end if
    if php_empty(lambda : categories_):
        if (not php_empty(lambda : show_option_none_)):
            if "list" == parsed_args_["style"]:
                output_ += "<li class=\"cat-item-none\">" + show_option_none_ + "</li>"
            else:
                output_ += show_option_none_
            # end if
        # end if
    else:
        if (not php_empty(lambda : show_option_all_)):
            posts_page_ = ""
            #// For taxonomies that belong only to custom post types, point to a valid archive.
            taxonomy_object_ = get_taxonomy(parsed_args_["taxonomy"])
            if (not php_in_array("post", taxonomy_object_.object_type)) and (not php_in_array("page", taxonomy_object_.object_type)):
                for object_type_ in taxonomy_object_.object_type:
                    _object_type_ = get_post_type_object(object_type_)
                    #// Grab the first one.
                    if (not php_empty(lambda : _object_type_.has_archive)):
                        posts_page_ = get_post_type_archive_link(object_type_)
                        break
                    # end if
                # end for
            # end if
            #// Fallback for the 'All' link is the posts page.
            if (not posts_page_):
                if "page" == get_option("show_on_front") and get_option("page_for_posts"):
                    posts_page_ = get_permalink(get_option("page_for_posts"))
                else:
                    posts_page_ = home_url("/")
                # end if
            # end if
            posts_page_ = esc_url(posts_page_)
            if "list" == parsed_args_["style"]:
                output_ += str("<li class='cat-item-all'><a href='") + str(posts_page_) + str("'>") + str(show_option_all_) + str("</a></li>")
            else:
                output_ += str("<a href='") + str(posts_page_) + str("'>") + str(show_option_all_) + str("</a>")
            # end if
        # end if
        if php_empty(lambda : parsed_args_["current_category"]) and is_category() or is_tax() or is_tag():
            current_term_object_ = get_queried_object()
            if current_term_object_ and parsed_args_["taxonomy"] == current_term_object_.taxonomy:
                parsed_args_["current_category"] = get_queried_object_id()
            # end if
        # end if
        if parsed_args_["hierarchical"]:
            depth_ = parsed_args_["depth"]
        else:
            depth_ = -1
            pass
        # end if
        output_ += walk_category_tree(categories_, depth_, parsed_args_)
    # end if
    if parsed_args_["title_li"] and "list" == parsed_args_["style"] and (not php_empty(lambda : categories_)) or (not parsed_args_["hide_title_if_empty"]):
        output_ += "</ul></li>"
    # end if
    #// 
    #// Filters the HTML output of a taxonomy list.
    #// 
    #// @since 2.1.0
    #// 
    #// @param string $output HTML output.
    #// @param array  $args   An array of taxonomy-listing arguments.
    #//
    html_ = apply_filters("wp_list_categories", output_, args_)
    if parsed_args_["echo"]:
        php_print(html_)
    else:
        return html_
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
def wp_tag_cloud(args_="", *_args_):
    
    
    defaults_ = Array({"smallest": 8, "largest": 22, "unit": "pt", "number": 45, "format": "flat", "separator": "\n", "orderby": "name", "order": "ASC", "exclude": "", "include": "", "link": "view", "taxonomy": "post_tag", "post_type": "", "echo": True, "show_count": 0})
    args_ = wp_parse_args(args_, defaults_)
    tags_ = get_terms(php_array_merge(args_, Array({"orderby": "count", "order": "DESC"})))
    #// Always query top tags.
    if php_empty(lambda : tags_) or is_wp_error(tags_):
        return
    # end if
    for key_,tag_ in tags_.items():
        if "edit" == args_["link"]:
            link_ = get_edit_term_link(tag_.term_id, tag_.taxonomy, args_["post_type"])
        else:
            link_ = get_term_link(php_intval(tag_.term_id), tag_.taxonomy)
        # end if
        if is_wp_error(link_):
            return
        # end if
        tags_[key_].link = link_
        tags_[key_].id = tag_.term_id
    # end for
    #// Here's where those top tags get sorted according to $args.
    return_ = wp_generate_tag_cloud(tags_, args_)
    #// 
    #// Filters the tag cloud output.
    #// 
    #// @since 2.3.0
    #// 
    #// @param string|array $return Tag cloud as a string or an array, depending on 'format' argument.
    #// @param array        $args   An array of tag cloud arguments.
    #//
    return_ = apply_filters("wp_tag_cloud", return_, args_)
    if "array" == args_["format"] or php_empty(lambda : args_["echo"]):
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
def default_topic_count_scale(count_=None, *_args_):
    
    
    return round(log10(count_ + 1) * 100)
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
def wp_generate_tag_cloud(tags_=None, args_="", *_args_):
    
    
    defaults_ = Array({"smallest": 8, "largest": 22, "unit": "pt", "number": 0, "format": "flat", "separator": "\n", "orderby": "name", "order": "ASC", "topic_count_text": None, "topic_count_text_callback": None, "topic_count_scale_callback": "default_topic_count_scale", "filter": 1, "show_count": 0})
    args_ = wp_parse_args(args_, defaults_)
    return_ = Array() if "array" == args_["format"] else ""
    if php_empty(lambda : tags_):
        return return_
    # end if
    #// Juggle topic counts.
    if (php_isset(lambda : args_["topic_count_text"])):
        #// First look for nooped plural support via topic_count_text.
        translate_nooped_plural_ = args_["topic_count_text"]
    elif (not php_empty(lambda : args_["topic_count_text_callback"])):
        #// Look for the alternative callback style. Ignore the previous default.
        if "default_topic_count_text" == args_["topic_count_text_callback"]:
            #// translators: %s: Number of items (tags).
            translate_nooped_plural_ = _n_noop("%s item", "%s items")
        else:
            translate_nooped_plural_ = False
        # end if
    elif (php_isset(lambda : args_["single_text"])) and (php_isset(lambda : args_["multiple_text"])):
        #// If no callback exists, look for the old-style single_text and multiple_text arguments.
        #// phpcs:ignore WordPress.WP.I18n.NonSingularStringLiteralSingle,WordPress.WP.I18n.NonSingularStringLiteralPlural
        translate_nooped_plural_ = _n_noop(args_["single_text"], args_["multiple_text"])
    else:
        #// This is the default for when no callback, plural, or argument is passed in.
        #// translators: %s: Number of items (tags).
        translate_nooped_plural_ = _n_noop("%s item", "%s items")
    # end if
    #// 
    #// Filters how the items in a tag cloud are sorted.
    #// 
    #// @since 2.8.0
    #// 
    #// @param WP_Term[] $tags Ordered array of terms.
    #// @param array     $args An array of tag cloud arguments.
    #//
    tags_sorted_ = apply_filters("tag_cloud_sort", tags_, args_)
    if php_empty(lambda : tags_sorted_):
        return return_
    # end if
    if tags_sorted_ != tags_:
        tags_ = tags_sorted_
        tags_sorted_ = None
    else:
        if "RAND" == args_["order"]:
            shuffle(tags_)
        else:
            #// SQL cannot save you; this is a second (potentially different) sort on a subset of data.
            if "name" == args_["orderby"]:
                uasort(tags_, "_wp_object_name_sort_cb")
            else:
                uasort(tags_, "_wp_object_count_sort_cb")
            # end if
            if "DESC" == args_["order"]:
                tags_ = array_reverse(tags_, True)
            # end if
        # end if
    # end if
    if args_["number"] > 0:
        tags_ = php_array_slice(tags_, 0, args_["number"])
    # end if
    counts_ = Array()
    real_counts_ = Array()
    #// For the alt tag.
    for key_,tag_ in tags_.items():
        real_counts_[key_] = tag_.count
        counts_[key_] = php_call_user_func(args_["topic_count_scale_callback"], tag_.count)
    # end for
    min_count_ = php_min(counts_)
    spread_ = php_max(counts_) - min_count_
    if spread_ <= 0:
        spread_ = 1
    # end if
    font_spread_ = args_["largest"] - args_["smallest"]
    if font_spread_ < 0:
        font_spread_ = 1
    # end if
    font_step_ = font_spread_ / spread_
    aria_label_ = False
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
    if args_["show_count"] or 0 != font_spread_:
        aria_label_ = True
    # end if
    #// Assemble the data that will be used to generate the tag cloud markup.
    tags_data_ = Array()
    for key_,tag_ in tags_.items():
        tag_id_ = tag_.id if (php_isset(lambda : tag_.id)) else key_
        count_ = counts_[key_]
        real_count_ = real_counts_[key_]
        if translate_nooped_plural_:
            formatted_count_ = php_sprintf(translate_nooped_plural(translate_nooped_plural_, real_count_), number_format_i18n(real_count_))
        else:
            formatted_count_ = php_call_user_func(args_["topic_count_text_callback"], real_count_, tag_, args_)
        # end if
        tags_data_[-1] = Array({"id": tag_id_, "url": tag_.link if "#" != tag_.link else "#", "role": "" if "#" != tag_.link else " role=\"button\"", "name": tag_.name, "formatted_count": formatted_count_, "slug": tag_.slug, "real_count": real_count_, "class": "tag-cloud-link tag-link-" + tag_id_, "font_size": args_["smallest"] + count_ - min_count_ * font_step_, "aria_label": php_sprintf(" aria-label=\"%1$s (%2$s)\"", esc_attr(tag_.name), esc_attr(formatted_count_)) if aria_label_ else "", "show_count": "<span class=\"tag-link-count\"> (" + real_count_ + ")</span>" if args_["show_count"] else ""})
    # end for
    #// 
    #// Filters the data used to generate the tag cloud.
    #// 
    #// @since 4.3.0
    #// 
    #// @param array $tags_data An array of term data for term used to generate the tag cloud.
    #//
    tags_data_ = apply_filters("wp_generate_tag_cloud_data", tags_data_)
    a_ = Array()
    #// Generate the output links array.
    for key_,tag_data_ in tags_data_.items():
        class_ = tag_data_["class"] + " tag-link-position-" + key_ + 1
        a_[-1] = php_sprintf("<a href=\"%1$s\"%2$s class=\"%3$s\" style=\"font-size: %4$s;\"%5$s>%6$s%7$s</a>", esc_url(tag_data_["url"]), tag_data_["role"], esc_attr(class_), esc_attr(php_str_replace(",", ".", tag_data_["font_size"]) + args_["unit"]), tag_data_["aria_label"], esc_html(tag_data_["name"]), tag_data_["show_count"])
    # end for
    for case in Switch(args_["format"]):
        if case("array"):
            return_ = a_
            break
        # end if
        if case("list"):
            #// 
            #// Force role="list", as some browsers (sic: Safari 10) don't expose to assistive
            #// technologies the default role when the list is styled with `list-style: none`.
            #// Note: this is redundant but doesn't harm.
            #//
            return_ = "<ul class='wp-tag-cloud' role='list'>\n  <li>"
            return_ += join("</li>\n    <li>", a_)
            return_ += "</li>\n</ul>\n"
            break
        # end if
        if case():
            return_ = join(args_["separator"], a_)
            break
        # end if
    # end for
    if args_["filter"]:
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
        return apply_filters("wp_generate_tag_cloud", return_, tags_, args_)
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
def _wp_object_name_sort_cb(a_=None, b_=None, *_args_):
    
    
    return strnatcasecmp(a_.name, b_.name)
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
def _wp_object_count_sort_cb(a_=None, b_=None, *_args_):
    
    
    return a_.count > b_.count
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
def walk_category_tree(*args_):
    
    
    #// The user's options are the third parameter.
    if php_empty(lambda : args_[2]["walker"]) or (not type(args_[2]["walker"]).__name__ == "Walker"):
        walker_ = php_new_class("Walker_Category", lambda : Walker_Category())
    else:
        walker_ = args_[2]["walker"]
    # end if
    return walker_.walk(args_)
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
def walk_category_dropdown_tree(*args_):
    
    
    #// The user's options are the third parameter.
    if php_empty(lambda : args_[2]["walker"]) or (not type(args_[2]["walker"]).__name__ == "Walker"):
        walker_ = php_new_class("Walker_CategoryDropdown", lambda : Walker_CategoryDropdown())
    else:
        walker_ = args_[2]["walker"]
    # end if
    return walker_.walk(args_)
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
def get_tag_link(tag_=None, *_args_):
    
    
    return get_category_link(tag_)
# end def get_tag_link
#// 
#// Retrieve the tags for a post.
#// 
#// @since 2.3.0
#// 
#// @param int $id Post ID.
#// @return array|false|WP_Error Array of tag objects on success, false on failure.
#//
def get_the_tags(id_=0, *_args_):
    
    
    #// 
    #// Filters the array of tags for the given post.
    #// 
    #// @since 2.3.0
    #// 
    #// @see get_the_terms()
    #// 
    #// @param WP_Term[] $terms An array of tags for the given post.
    #//
    return apply_filters("get_the_tags", get_the_terms(id_, "post_tag"))
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
def get_the_tag_list(before_="", sep_="", after_="", id_=0, *_args_):
    
    
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
    return apply_filters("the_tags", get_the_term_list(id_, "post_tag", before_, sep_, after_), before_, sep_, after_, id_)
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
def the_tags(before_=None, sep_=", ", after_="", *_args_):
    if before_ is None:
        before_ = None
    # end if
    
    if None == before_:
        before_ = __("Tags: ")
    # end if
    the_tags_ = get_the_tag_list(before_, sep_, after_)
    if (not is_wp_error(the_tags_)):
        php_print(the_tags_)
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
def tag_description(tag_=0, *_args_):
    
    
    return term_description(tag_)
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
def term_description(term_=0, deprecated_=None, *_args_):
    if deprecated_ is None:
        deprecated_ = None
    # end if
    
    if (not term_) and is_tax() or is_tag() or is_category():
        term_ = get_queried_object()
        if term_:
            term_ = term_.term_id
        # end if
    # end if
    description_ = get_term_field("description", term_)
    return "" if is_wp_error(description_) else description_
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
def get_the_terms(post_=None, taxonomy_=None, *_args_):
    
    
    post_ = get_post(post_)
    if (not post_):
        return False
    # end if
    terms_ = get_object_term_cache(post_.ID, taxonomy_)
    if False == terms_:
        terms_ = wp_get_object_terms(post_.ID, taxonomy_)
        if (not is_wp_error(terms_)):
            term_ids_ = wp_list_pluck(terms_, "term_id")
            wp_cache_add(post_.ID, term_ids_, taxonomy_ + "_relationships")
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
    terms_ = apply_filters("get_the_terms", terms_, post_.ID, taxonomy_)
    if php_empty(lambda : terms_):
        return False
    # end if
    return terms_
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
def get_the_term_list(id_=None, taxonomy_=None, before_="", sep_="", after_="", *_args_):
    
    
    terms_ = get_the_terms(id_, taxonomy_)
    if is_wp_error(terms_):
        return terms_
    # end if
    if php_empty(lambda : terms_):
        return False
    # end if
    links_ = Array()
    for term_ in terms_:
        link_ = get_term_link(term_, taxonomy_)
        if is_wp_error(link_):
            return link_
        # end if
        links_[-1] = "<a href=\"" + esc_url(link_) + "\" rel=\"tag\">" + term_.name + "</a>"
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
    term_links_ = apply_filters(str("term_links-") + str(taxonomy_), links_)
    #// phpcs:ignore WordPress.NamingConventions.ValidHookName.UseUnderscores
    return before_ + join(sep_, term_links_) + after_
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
def get_term_parents_list(term_id_=None, taxonomy_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    list_ = ""
    term_ = get_term(term_id_, taxonomy_)
    if is_wp_error(term_):
        return term_
    # end if
    if (not term_):
        return list_
    # end if
    term_id_ = term_.term_id
    defaults_ = Array({"format": "name", "separator": "/", "link": True, "inclusive": True})
    args_ = wp_parse_args(args_, defaults_)
    for bool_ in Array("link", "inclusive"):
        args_[bool_] = wp_validate_boolean(args_[bool_])
    # end for
    parents_ = get_ancestors(term_id_, taxonomy_, "taxonomy")
    if args_["inclusive"]:
        array_unshift(parents_, term_id_)
    # end if
    for term_id_ in array_reverse(parents_):
        parent_ = get_term(term_id_, taxonomy_)
        name_ = parent_.slug if "slug" == args_["format"] else parent_.name
        if args_["link"]:
            list_ += "<a href=\"" + esc_url(get_term_link(parent_.term_id, taxonomy_)) + "\">" + name_ + "</a>" + args_["separator"]
        else:
            list_ += name_ + args_["separator"]
        # end if
    # end for
    return list_
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
def the_terms(id_=None, taxonomy_=None, before_="", sep_=", ", after_="", *_args_):
    
    
    term_list_ = get_the_term_list(id_, taxonomy_, before_, sep_, after_)
    if is_wp_error(term_list_):
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
    php_print(apply_filters("the_terms", term_list_, taxonomy_, before_, sep_, after_))
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
def has_category(category_="", post_=None, *_args_):
    if post_ is None:
        post_ = None
    # end if
    
    return has_term(category_, "category", post_)
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
def has_tag(tag_="", post_=None, *_args_):
    if post_ is None:
        post_ = None
    # end if
    
    return has_term(tag_, "post_tag", post_)
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
def has_term(term_="", taxonomy_="", post_=None, *_args_):
    if post_ is None:
        post_ = None
    # end if
    
    post_ = get_post(post_)
    if (not post_):
        return False
    # end if
    r_ = is_object_in_term(post_.ID, taxonomy_, term_)
    if is_wp_error(r_):
        return False
    # end if
    return r_
# end def has_term
