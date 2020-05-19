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
#// Deprecated functions from past WordPress versions. You shouldn't use these
#// functions and look for the alternatives instead. The functions will be
#// removed in a later version.
#// 
#// @package WordPress
#// @subpackage Deprecated
#// 
#// 
#// Deprecated functions come here to die.
#// 
#// 
#// Retrieves all post data for a given post.
#// 
#// @since 0.71
#// @deprecated 1.5.1 Use get_post()
#// @see get_post()
#// 
#// @param int $postid Post ID.
#// @return array Post data.
#//
def get_postdata(postid_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "1.5.1", "get_post()")
    post_ = get_post(postid_)
    postdata_ = Array({"ID": post_.ID, "Author_ID": post_.post_author, "Date": post_.post_date, "Content": post_.post_content, "Excerpt": post_.post_excerpt, "Title": post_.post_title, "Category": post_.post_category, "post_status": post_.post_status, "comment_status": post_.comment_status, "ping_status": post_.ping_status, "post_password": post_.post_password, "to_ping": post_.to_ping, "pinged": post_.pinged, "post_type": post_.post_type, "post_name": post_.post_name})
    return postdata_
# end def get_postdata
#// 
#// Sets up the WordPress Loop.
#// 
#// Use The Loop instead.
#// 
#// @link https://developer.wordpress.org/themes/basics/the-loop
#// 
#// @since 1.0.1
#// @deprecated 1.5.0
#//
def start_wp(*_args_):
    
    
    global wp_query_
    php_check_if_defined("wp_query_")
    _deprecated_function(__FUNCTION__, "1.5.0", __("new WordPress Loop"))
    #// Since the old style loop is being used, advance the query iterator here.
    wp_query_.next_post()
    setup_postdata(get_post())
# end def start_wp
#// 
#// Returns or prints a category ID.
#// 
#// @since 0.71
#// @deprecated 0.71 Use get_the_category()
#// @see get_the_category()
#// 
#// @param bool $echo Optional. Whether to echo the output. Default true.
#// @return int Category ID.
#//
def the_category_ID(echo_=None, *_args_):
    if echo_ is None:
        echo_ = True
    # end if
    
    _deprecated_function(__FUNCTION__, "0.71", "get_the_category()")
    #// Grab the first cat in the list.
    categories_ = get_the_category()
    cat_ = categories_[0].term_id
    if echo_:
        php_print(cat_)
    # end if
    return cat_
# end def the_category_ID
#// 
#// Prints a category with optional text before and after.
#// 
#// @since 0.71
#// @deprecated 0.71 Use get_the_category_by_ID()
#// @see get_the_category_by_ID()
#// 
#// @param string $before Optional. Text to display before the category. Default empty.
#// @param string $after  Optional. Text to display after the category. Default empty.
#//
def the_category_head(before_="", after_="", *_args_):
    
    
    global currentcat_
    global previouscat_
    php_check_if_defined("currentcat_","previouscat_")
    _deprecated_function(__FUNCTION__, "0.71", "get_the_category_by_ID()")
    #// Grab the first cat in the list.
    categories_ = get_the_category()
    currentcat_ = categories_[0].category_id
    if currentcat_ != previouscat_:
        php_print(before_)
        php_print(get_the_category_by_ID(currentcat_))
        php_print(after_)
        previouscat_ = currentcat_
    # end if
# end def the_category_head
#// 
#// Prints a link to the previous post.
#// 
#// @since 1.5.0
#// @deprecated 2.0.0 Use previous_post_link()
#// @see previous_post_link()
#// 
#// @param string $format
#// @param string $previous
#// @param string $title
#// @param string $in_same_cat
#// @param int    $limitprev
#// @param string $excluded_categories
#//
def previous_post(format_="%", previous_="previous post: ", title_="yes", in_same_cat_="no", limitprev_=1, excluded_categories_="", *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.0.0", "previous_post_link()")
    if php_empty(lambda : in_same_cat_) or "no" == in_same_cat_:
        in_same_cat_ = False
    else:
        in_same_cat_ = True
    # end if
    post_ = get_previous_post(in_same_cat_, excluded_categories_)
    if (not post_):
        return
    # end if
    string_ = "<a href=\"" + get_permalink(post_.ID) + "\">" + previous_
    if "yes" == title_:
        string_ += apply_filters("the_title", post_.post_title, post_.ID)
    # end if
    string_ += "</a>"
    format_ = php_str_replace("%", string_, format_)
    php_print(format_)
# end def previous_post
#// 
#// Prints link to the next post.
#// 
#// @since 0.71
#// @deprecated 2.0.0 Use next_post_link()
#// @see next_post_link()
#// 
#// @param string $format
#// @param string $next
#// @param string $title
#// @param string $in_same_cat
#// @param int $limitnext
#// @param string $excluded_categories
#//
def next_post(format_="%", next_="next post: ", title_="yes", in_same_cat_="no", limitnext_=1, excluded_categories_="", *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.0.0", "next_post_link()")
    if php_empty(lambda : in_same_cat_) or "no" == in_same_cat_:
        in_same_cat_ = False
    else:
        in_same_cat_ = True
    # end if
    post_ = get_next_post(in_same_cat_, excluded_categories_)
    if (not post_):
        return
    # end if
    string_ = "<a href=\"" + get_permalink(post_.ID) + "\">" + next_
    if "yes" == title_:
        string_ += apply_filters("the_title", post_.post_title, post_.ID)
    # end if
    string_ += "</a>"
    format_ = php_str_replace("%", string_, format_)
    php_print(format_)
# end def next_post
#// 
#// Whether user can create a post.
#// 
#// @since 1.5.0
#// @deprecated 2.0.0 Use current_user_can()
#// @see current_user_can()
#// 
#// @param int $user_id
#// @param int $blog_id Not Used
#// @param int $category_id Not Used
#// @return bool
#//
def user_can_create_post(user_id_=None, blog_id_=1, category_id_="None", *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.0.0", "current_user_can()")
    author_data_ = get_userdata(user_id_)
    return author_data_.user_level > 1
# end def user_can_create_post
#// 
#// Whether user can create a post.
#// 
#// @since 1.5.0
#// @deprecated 2.0.0 Use current_user_can()
#// @see current_user_can()
#// 
#// @param int $user_id
#// @param int $blog_id Not Used
#// @param int $category_id Not Used
#// @return bool
#//
def user_can_create_draft(user_id_=None, blog_id_=1, category_id_="None", *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.0.0", "current_user_can()")
    author_data_ = get_userdata(user_id_)
    return author_data_.user_level >= 1
# end def user_can_create_draft
#// 
#// Whether user can edit a post.
#// 
#// @since 1.5.0
#// @deprecated 2.0.0 Use current_user_can()
#// @see current_user_can()
#// 
#// @param int $user_id
#// @param int $post_id
#// @param int $blog_id Not Used
#// @return bool
#//
def user_can_edit_post(user_id_=None, post_id_=None, blog_id_=1, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.0.0", "current_user_can()")
    author_data_ = get_userdata(user_id_)
    post_ = get_post(post_id_)
    post_author_data_ = get_userdata(post_.post_author)
    if user_id_ == post_author_data_.ID and (not post_.post_status == "publish" and author_data_.user_level < 2) or author_data_.user_level > post_author_data_.user_level or author_data_.user_level >= 10:
        return True
    else:
        return False
    # end if
# end def user_can_edit_post
#// 
#// Whether user can delete a post.
#// 
#// @since 1.5.0
#// @deprecated 2.0.0 Use current_user_can()
#// @see current_user_can()
#// 
#// @param int $user_id
#// @param int $post_id
#// @param int $blog_id Not Used
#// @return bool
#//
def user_can_delete_post(user_id_=None, post_id_=None, blog_id_=1, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.0.0", "current_user_can()")
    #// Right now if one can edit, one can delete.
    return user_can_edit_post(user_id_, post_id_, blog_id_)
# end def user_can_delete_post
#// 
#// Whether user can set new posts' dates.
#// 
#// @since 1.5.0
#// @deprecated 2.0.0 Use current_user_can()
#// @see current_user_can()
#// 
#// @param int $user_id
#// @param int $blog_id Not Used
#// @param int $category_id Not Used
#// @return bool
#//
def user_can_set_post_date(user_id_=None, blog_id_=1, category_id_="None", *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.0.0", "current_user_can()")
    author_data_ = get_userdata(user_id_)
    return author_data_.user_level > 4 and user_can_create_post(user_id_, blog_id_, category_id_)
# end def user_can_set_post_date
#// 
#// Whether user can delete a post.
#// 
#// @since 1.5.0
#// @deprecated 2.0.0 Use current_user_can()
#// @see current_user_can()
#// 
#// @param int $user_id
#// @param int $post_id
#// @param int $blog_id Not Used
#// @return bool returns true if $user_id can edit $post_id's date
#//
def user_can_edit_post_date(user_id_=None, post_id_=None, blog_id_=1, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.0.0", "current_user_can()")
    author_data_ = get_userdata(user_id_)
    return author_data_.user_level > 4 and user_can_edit_post(user_id_, post_id_, blog_id_)
# end def user_can_edit_post_date
#// 
#// Whether user can delete a post.
#// 
#// @since 1.5.0
#// @deprecated 2.0.0 Use current_user_can()
#// @see current_user_can()
#// 
#// @param int $user_id
#// @param int $post_id
#// @param int $blog_id Not Used
#// @return bool returns true if $user_id can edit $post_id's comments
#//
def user_can_edit_post_comments(user_id_=None, post_id_=None, blog_id_=1, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.0.0", "current_user_can()")
    #// Right now if one can edit a post, one can edit comments made on it.
    return user_can_edit_post(user_id_, post_id_, blog_id_)
# end def user_can_edit_post_comments
#// 
#// Whether user can delete a post.
#// 
#// @since 1.5.0
#// @deprecated 2.0.0 Use current_user_can()
#// @see current_user_can()
#// 
#// @param int $user_id
#// @param int $post_id
#// @param int $blog_id Not Used
#// @return bool returns true if $user_id can delete $post_id's comments
#//
def user_can_delete_post_comments(user_id_=None, post_id_=None, blog_id_=1, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.0.0", "current_user_can()")
    #// Right now if one can edit comments, one can delete comments.
    return user_can_edit_post_comments(user_id_, post_id_, blog_id_)
# end def user_can_delete_post_comments
#// 
#// Can user can edit other user.
#// 
#// @since 1.5.0
#// @deprecated 2.0.0 Use current_user_can()
#// @see current_user_can()
#// 
#// @param int $user_id
#// @param int $other_user
#// @return bool
#//
def user_can_edit_user(user_id_=None, other_user_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.0.0", "current_user_can()")
    user_ = get_userdata(user_id_)
    other_ = get_userdata(other_user_)
    if user_.user_level > other_.user_level or user_.user_level > 8 or user_.ID == other_.ID:
        return True
    else:
        return False
    # end if
# end def user_can_edit_user
#// 
#// Gets the links associated with category $cat_name.
#// 
#// @since 0.71
#// @deprecated 2.1.0 Use get_bookmarks()
#// @see get_bookmarks()
#// 
#// @param string $cat_name Optional. The category name to use. If no match is found uses all.
#// @param string $before Optional. The html to output before the link.
#// @param string $after Optional. The html to output after the link.
#// @param string $between Optional. The html to output between the link/image and its description. Not used if no image or $show_images is true.
#// @param bool $show_images Optional. Whether to show images (if defined).
#// @param string $orderby Optional. The order to output the links. E.g. 'id', 'name', 'url', 'description' or 'rating'. Or maybe owner.
#// If you start the name with an underscore the order will be reversed. You can also specify 'rand' as the order which will return links in a
#// random order.
#// @param bool $show_description Optional. Whether to show the description if show_images=false/not defined.
#// @param bool $show_rating Optional. Show rating stars/chars.
#// @param int $limit       Optional. Limit to X entries. If not specified, all entries are shown.
#// @param int $show_updated Optional. Whether to show last updated timestamp
#//
def get_linksbyname(cat_name_="noname", before_="", after_="<br />", between_=" ", show_images_=None, orderby_="id", show_description_=None, show_rating_=None, limit_=None, show_updated_=0, *_args_):
    if show_images_ is None:
        show_images_ = True
    # end if
    if show_description_ is None:
        show_description_ = True
    # end if
    if show_rating_ is None:
        show_rating_ = False
    # end if
    if limit_ is None:
        limit_ = -1
    # end if
    
    _deprecated_function(__FUNCTION__, "2.1.0", "get_bookmarks()")
    cat_id_ = -1
    cat_ = get_term_by("name", cat_name_, "link_category")
    if cat_:
        cat_id_ = cat_.term_id
    # end if
    get_links(cat_id_, before_, after_, between_, show_images_, orderby_, show_description_, show_rating_, limit_, show_updated_)
# end def get_linksbyname
#// 
#// Gets the links associated with the named category.
#// 
#// @since 1.0.1
#// @deprecated 2.1.0 Use wp_list_bookmarks()
#// @see wp_list_bookmarks()
#// 
#// @param string $category The category to use.
#// @param string $args
#// @return string|null
#//
def wp_get_linksbyname(category_=None, args_="", *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.1.0", "wp_list_bookmarks()")
    defaults_ = Array({"after": "<br />", "before": "", "categorize": 0, "category_after": "", "category_before": "", "category_name": category_, "show_description": 1, "title_li": ""})
    parsed_args_ = wp_parse_args(args_, defaults_)
    return wp_list_bookmarks(parsed_args_)
# end def wp_get_linksbyname
#// 
#// Gets an array of link objects associated with category $cat_name.
#// 
#// $links = get_linkobjectsbyname( 'fred' );
#// foreach ( $links as $link ) {
#// echo '<li>' . $link->link_name . '</li>';
#// }
#// 
#// @since 1.0.1
#// @deprecated 2.1.0 Use get_bookmarks()
#// @see get_bookmarks()
#// 
#// @param string $cat_name The category name to use. If no match is found uses all.
#// @param string $orderby The order to output the links. E.g. 'id', 'name', 'url', 'description', or 'rating'.
#// Or maybe owner. If you start the name with an underscore the order will be reversed. You can also
#// specify 'rand' as the order which will return links in a random order.
#// @param int $limit Limit to X entries. If not specified, all entries are shown.
#// @return array
#//
def get_linkobjectsbyname(cat_name_="noname", orderby_="name", limit_=None, *_args_):
    if limit_ is None:
        limit_ = -1
    # end if
    
    _deprecated_function(__FUNCTION__, "2.1.0", "get_bookmarks()")
    cat_id_ = -1
    cat_ = get_term_by("name", cat_name_, "link_category")
    if cat_:
        cat_id_ = cat_.term_id
    # end if
    return get_linkobjects(cat_id_, orderby_, limit_)
# end def get_linkobjectsbyname
#// 
#// Gets an array of link objects associated with category n.
#// 
#// Usage:
#// 
#// $links = get_linkobjects(1);
#// if ($links) {
#// foreach ($links as $link) {
#// echo '<li>'.$link->link_name.'<br />'.$link->link_description.'</li>';
#// }
#// }
#// 
#// Fields are:
#// 
#// - link_id
#// - link_url
#// - link_name
#// - link_image
#// - link_target
#// - link_category
#// - link_description
#// - link_visible
#// - link_owner
#// - link_rating
#// - link_updated
#// - link_rel
#// - link_notes
#// 
#// @since 1.0.1
#// @deprecated 2.1.0 Use get_bookmarks()
#// @see get_bookmarks()
#// 
#// @param int $category The category to use. If no category supplied uses all
#// @param string $orderby the order to output the links. E.g. 'id', 'name', 'url',
#// 'description', or 'rating'. Or maybe owner. If you start the name with an
#// underscore the order will be reversed. You can also specify 'rand' as the
#// order which will return links in a random order.
#// @param int $limit Limit to X entries. If not specified, all entries are shown.
#// @return array
#//
def get_linkobjects(category_=0, orderby_="name", limit_=0, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.1.0", "get_bookmarks()")
    links_ = get_bookmarks(Array({"category": category_, "orderby": orderby_, "limit": limit_}))
    links_array_ = Array()
    for link_ in links_:
        links_array_[-1] = link_
    # end for
    return links_array_
# end def get_linkobjects
#// 
#// Gets the links associated with category 'cat_name' and display rating stars/chars.
#// 
#// @since 0.71
#// @deprecated 2.1.0 Use get_bookmarks()
#// @see get_bookmarks()
#// 
#// @param string $cat_name The category name to use. If no match is found uses all
#// @param string $before The html to output before the link
#// @param string $after The html to output after the link
#// @param string $between The html to output between the link/image and its description. Not used if no image or show_images is true
#// @param bool $show_images Whether to show images (if defined).
#// @param string $orderby the order to output the links. E.g. 'id', 'name', 'url',
#// 'description', or 'rating'. Or maybe owner. If you start the name with an
#// underscore the order will be reversed. You can also specify 'rand' as the
#// order which will return links in a random order.
#// @param bool $show_description Whether to show the description if show_images=false/not defined
#// @param int $limit Limit to X entries. If not specified, all entries are shown.
#// @param int $show_updated Whether to show last updated timestamp
#//
def get_linksbyname_withrating(cat_name_="noname", before_="", after_="<br />", between_=" ", show_images_=None, orderby_="id", show_description_=None, limit_=None, show_updated_=0, *_args_):
    if show_images_ is None:
        show_images_ = True
    # end if
    if show_description_ is None:
        show_description_ = True
    # end if
    if limit_ is None:
        limit_ = -1
    # end if
    
    _deprecated_function(__FUNCTION__, "2.1.0", "get_bookmarks()")
    get_linksbyname(cat_name_, before_, after_, between_, show_images_, orderby_, show_description_, True, limit_, show_updated_)
# end def get_linksbyname_withrating
#// 
#// Gets the links associated with category n and display rating stars/chars.
#// 
#// @since 0.71
#// @deprecated 2.1.0 Use get_bookmarks()
#// @see get_bookmarks()
#// 
#// @param int $category The category to use. If no category supplied uses all
#// @param string $before The html to output before the link
#// @param string $after The html to output after the link
#// @param string $between The html to output between the link/image and its description. Not used if no image or show_images == true
#// @param bool $show_images Whether to show images (if defined).
#// @param string $orderby The order to output the links. E.g. 'id', 'name', 'url',
#// 'description', or 'rating'. Or maybe owner. If you start the name with an
#// underscore the order will be reversed. You can also specify 'rand' as the
#// order which will return links in a random order.
#// @param bool $show_description Whether to show the description if show_images=false/not defined.
#// @param int $limit Limit to X entries. If not specified, all entries are shown.
#// @param int $show_updated Whether to show last updated timestamp
#//
def get_links_withrating(category_=None, before_="", after_="<br />", between_=" ", show_images_=None, orderby_="id", show_description_=None, limit_=None, show_updated_=0, *_args_):
    if category_ is None:
        category_ = -1
    # end if
    if show_images_ is None:
        show_images_ = True
    # end if
    if show_description_ is None:
        show_description_ = True
    # end if
    if limit_ is None:
        limit_ = -1
    # end if
    
    _deprecated_function(__FUNCTION__, "2.1.0", "get_bookmarks()")
    get_links(category_, before_, after_, between_, show_images_, orderby_, show_description_, True, limit_, show_updated_)
# end def get_links_withrating
#// 
#// Gets the auto_toggle setting.
#// 
#// @since 0.71
#// @deprecated 2.1.0
#// 
#// @param int $id The category to get. If no category supplied uses 0
#// @return int Only returns 0.
#//
def get_autotoggle(id_=0, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.1.0")
    return 0
# end def get_autotoggle
#// 
#// Lists categories.
#// 
#// @since 0.71
#// @deprecated 2.1.0 Use wp_list_categories()
#// @see wp_list_categories()
#// 
#// @param int $optionall
#// @param string $all
#// @param string $sort_column
#// @param string $sort_order
#// @param string $file
#// @param bool $list
#// @param int $optiondates
#// @param int $optioncount
#// @param int $hide_empty
#// @param int $use_desc_for_title
#// @param bool $children
#// @param int $child_of
#// @param int $categories
#// @param int $recurse
#// @param string $feed
#// @param string $feed_image
#// @param string $exclude
#// @param bool $hierarchical
#// @return null|false
#//
def list_cats(optionall_=1, all_="All", sort_column_="ID", sort_order_="asc", file_="", list_=None, optiondates_=0, optioncount_=0, hide_empty_=1, use_desc_for_title_=1, children_=None, child_of_=0, categories_=0, recurse_=0, feed_="", feed_image_="", exclude_="", hierarchical_=None, *_args_):
    if list_ is None:
        list_ = True
    # end if
    if children_ is None:
        children_ = False
    # end if
    if hierarchical_ is None:
        hierarchical_ = False
    # end if
    
    _deprecated_function(__FUNCTION__, "2.1.0", "wp_list_categories()")
    query_ = php_compact("optionall_", "all_", "sort_column_", "sort_order_", "file_", "list_", "optiondates_", "optioncount_", "hide_empty_", "use_desc_for_title_", "children_", "child_of_", "categories_", "recurse_", "feed_", "feed_image_", "exclude_", "hierarchical_")
    return wp_list_cats(query_)
# end def list_cats
#// 
#// Lists categories.
#// 
#// @since 1.2.0
#// @deprecated 2.1.0 Use wp_list_categories()
#// @see wp_list_categories()
#// 
#// @param string|array $args
#// @return null|string|false
#//
def wp_list_cats(args_="", *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.1.0", "wp_list_categories()")
    parsed_args_ = wp_parse_args(args_)
    #// Map to new names.
    if (php_isset(lambda : parsed_args_["optionall"])) and (php_isset(lambda : parsed_args_["all"])):
        parsed_args_["show_option_all"] = parsed_args_["all"]
    # end if
    if (php_isset(lambda : parsed_args_["sort_column"])):
        parsed_args_["orderby"] = parsed_args_["sort_column"]
    # end if
    if (php_isset(lambda : parsed_args_["sort_order"])):
        parsed_args_["order"] = parsed_args_["sort_order"]
    # end if
    if (php_isset(lambda : parsed_args_["optiondates"])):
        parsed_args_["show_last_update"] = parsed_args_["optiondates"]
    # end if
    if (php_isset(lambda : parsed_args_["optioncount"])):
        parsed_args_["show_count"] = parsed_args_["optioncount"]
    # end if
    if (php_isset(lambda : parsed_args_["list"])):
        parsed_args_["style"] = "list" if parsed_args_["list"] else "break"
    # end if
    parsed_args_["title_li"] = ""
    return wp_list_categories(parsed_args_)
# end def wp_list_cats
#// 
#// Deprecated method for generating a drop-down of categories.
#// 
#// @since 0.71
#// @deprecated 2.1.0 Use wp_dropdown_categories()
#// @see wp_dropdown_categories()
#// 
#// @param int $optionall
#// @param string $all
#// @param string $orderby
#// @param string $order
#// @param int $show_last_update
#// @param int $show_count
#// @param int $hide_empty
#// @param bool $optionnone
#// @param int $selected
#// @param int $exclude
#// @return string
#//
def dropdown_cats(optionall_=1, all_="All", orderby_="ID", order_="asc", show_last_update_=0, show_count_=0, hide_empty_=1, optionnone_=None, selected_=0, exclude_=0, *_args_):
    if optionnone_ is None:
        optionnone_ = False
    # end if
    
    _deprecated_function(__FUNCTION__, "2.1.0", "wp_dropdown_categories()")
    show_option_all_ = ""
    if optionall_:
        show_option_all_ = all_
    # end if
    show_option_none_ = ""
    if optionnone_:
        show_option_none_ = __("None")
    # end if
    vars_ = php_compact("show_option_all_", "show_option_none_", "orderby_", "order_", "show_last_update_", "show_count_", "hide_empty_", "selected_", "exclude_")
    query_ = add_query_arg(vars_, "")
    return wp_dropdown_categories(query_)
# end def dropdown_cats
#// 
#// Lists authors.
#// 
#// @since 1.2.0
#// @deprecated 2.1.0 Use wp_list_authors()
#// @see wp_list_authors()
#// 
#// @param bool $optioncount
#// @param bool $exclude_admin
#// @param bool $show_fullname
#// @param bool $hide_empty
#// @param string $feed
#// @param string $feed_image
#// @return null|string
#//
def list_authors(optioncount_=None, exclude_admin_=None, show_fullname_=None, hide_empty_=None, feed_="", feed_image_="", *_args_):
    if optioncount_ is None:
        optioncount_ = False
    # end if
    if exclude_admin_ is None:
        exclude_admin_ = True
    # end if
    if show_fullname_ is None:
        show_fullname_ = False
    # end if
    if hide_empty_ is None:
        hide_empty_ = True
    # end if
    
    _deprecated_function(__FUNCTION__, "2.1.0", "wp_list_authors()")
    args_ = php_compact("optioncount_", "exclude_admin_", "show_fullname_", "hide_empty_", "feed_", "feed_image_")
    return wp_list_authors(args_)
# end def list_authors
#// 
#// Retrieves a list of post categories.
#// 
#// @since 1.0.1
#// @deprecated 2.1.0 Use wp_get_post_categories()
#// @see wp_get_post_categories()
#// 
#// @param int $blogid Not Used
#// @param int $post_ID
#// @return array
#//
def wp_get_post_cats(blogid_="1", post_ID_=0, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.1.0", "wp_get_post_categories()")
    return wp_get_post_categories(post_ID_)
# end def wp_get_post_cats
#// 
#// Sets the categories that the post id belongs to.
#// 
#// @since 1.0.1
#// @deprecated 2.1.0
#// @deprecated Use wp_set_post_categories()
#// @see wp_set_post_categories()
#// 
#// @param int $blogid Not used
#// @param int $post_ID
#// @param array $post_categories
#// @return bool|mixed
#//
def wp_set_post_cats(blogid_="1", post_ID_=0, post_categories_=None, *_args_):
    if post_categories_ is None:
        post_categories_ = Array()
    # end if
    
    _deprecated_function(__FUNCTION__, "2.1.0", "wp_set_post_categories()")
    return wp_set_post_categories(post_ID_, post_categories_)
# end def wp_set_post_cats
#// 
#// Retrieves a list of archives.
#// 
#// @since 0.71
#// @deprecated 2.1.0 Use wp_get_archives()
#// @see wp_get_archives()
#// 
#// @param string $type
#// @param string $limit
#// @param string $format
#// @param string $before
#// @param string $after
#// @param bool $show_post_count
#// @return string|null
#//
def get_archives(type_="", limit_="", format_="html", before_="", after_="", show_post_count_=None, *_args_):
    if show_post_count_ is None:
        show_post_count_ = False
    # end if
    
    _deprecated_function(__FUNCTION__, "2.1.0", "wp_get_archives()")
    args_ = php_compact("type_", "limit_", "format_", "before_", "after_", "show_post_count_")
    return wp_get_archives(args_)
# end def get_archives
#// 
#// Returns or Prints link to the author's posts.
#// 
#// @since 1.2.0
#// @deprecated 2.1.0 Use get_author_posts_url()
#// @see get_author_posts_url()
#// 
#// @param bool $echo
#// @param int $author_id
#// @param string $author_nicename Optional.
#// @return string|null
#//
def get_author_link(echo_=None, author_id_=None, author_nicename_="", *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.1.0", "get_author_posts_url()")
    link_ = get_author_posts_url(author_id_, author_nicename_)
    if echo_:
        php_print(link_)
    # end if
    return link_
# end def get_author_link
#// 
#// Print list of pages based on arguments.
#// 
#// @since 0.71
#// @deprecated 2.1.0 Use wp_link_pages()
#// @see wp_link_pages()
#// 
#// @param string $before
#// @param string $after
#// @param string $next_or_number
#// @param string $nextpagelink
#// @param string $previouspagelink
#// @param string $pagelink
#// @param string $more_file
#// @return string
#//
def link_pages(before_="<br />", after_="<br />", next_or_number_="number", nextpagelink_="next page", previouspagelink_="previous page", pagelink_="%", more_file_="", *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.1.0", "wp_link_pages()")
    args_ = php_compact("before_", "after_", "next_or_number_", "nextpagelink_", "previouspagelink_", "pagelink_", "more_file_")
    return wp_link_pages(args_)
# end def link_pages
#// 
#// Get value based on option.
#// 
#// @since 0.71
#// @deprecated 2.1.0 Use get_option()
#// @see get_option()
#// 
#// @param string $option
#// @return string
#//
def get_settings(option_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.1.0", "get_option()")
    return get_option(option_)
# end def get_settings
#// 
#// Print the permalink of the current post in the loop.
#// 
#// @since 0.71
#// @deprecated 1.2.0 Use the_permalink()
#// @see the_permalink()
#//
def permalink_link(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "1.2.0", "the_permalink()")
    the_permalink()
# end def permalink_link
#// 
#// Print the permalink to the RSS feed.
#// 
#// @since 0.71
#// @deprecated 2.3.0 Use the_permalink_rss()
#// @see the_permalink_rss()
#// 
#// @param string $deprecated
#//
def permalink_single_rss(deprecated_="", *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.3.0", "the_permalink_rss()")
    the_permalink_rss()
# end def permalink_single_rss
#// 
#// Gets the links associated with category.
#// 
#// @since 1.0.1
#// @deprecated 2.1.0 Use wp_list_bookmarks()
#// @see wp_list_bookmarks()
#// 
#// @param string $args a query string
#// @return null|string
#//
def wp_get_links(args_="", *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.1.0", "wp_list_bookmarks()")
    if php_strpos(args_, "=") == False:
        cat_id_ = args_
        args_ = add_query_arg("category", cat_id_, args_)
    # end if
    defaults_ = Array({"after": "<br />", "before": "", "between": " ", "categorize": 0, "category": "", "echo": True, "limit": -1, "orderby": "name", "show_description": True, "show_images": True, "show_rating": False, "show_updated": True, "title_li": ""})
    parsed_args_ = wp_parse_args(args_, defaults_)
    return wp_list_bookmarks(parsed_args_)
# end def wp_get_links
#// 
#// Gets the links associated with category by id.
#// 
#// @since 0.71
#// @deprecated 2.1.0 Use get_bookmarks()
#// @see get_bookmarks()
#// 
#// @param int $category The category to use. If no category supplied uses all
#// @param string $before the html to output before the link
#// @param string $after the html to output after the link
#// @param string $between the html to output between the link/image and its description.
#// Not used if no image or show_images == true
#// @param bool $show_images whether to show images (if defined).
#// @param string $orderby the order to output the links. E.g. 'id', 'name', 'url',
#// 'description', or 'rating'. Or maybe owner. If you start the name with an
#// underscore the order will be reversed. You can also specify 'rand' as the order
#// which will return links in a random order.
#// @param bool $show_description whether to show the description if show_images=false/not defined.
#// @param bool $show_rating show rating stars/chars
#// @param int $limit Limit to X entries. If not specified, all entries are shown.
#// @param int $show_updated whether to show last updated timestamp
#// @param bool $echo whether to echo the results, or return them instead
#// @return null|string
#//
def get_links(category_=None, before_="", after_="<br />", between_=" ", show_images_=None, orderby_="name", show_description_=None, show_rating_=None, limit_=None, show_updated_=1, echo_=None, *_args_):
    if category_ is None:
        category_ = -1
    # end if
    if show_images_ is None:
        show_images_ = True
    # end if
    if show_description_ is None:
        show_description_ = True
    # end if
    if show_rating_ is None:
        show_rating_ = False
    # end if
    if limit_ is None:
        limit_ = -1
    # end if
    if echo_ is None:
        echo_ = True
    # end if
    
    _deprecated_function(__FUNCTION__, "2.1.0", "get_bookmarks()")
    order_ = "ASC"
    if php_substr(orderby_, 0, 1) == "_":
        order_ = "DESC"
        orderby_ = php_substr(orderby_, 1)
    # end if
    if category_ == -1:
        #// get_bookmarks() uses '' to signify all categories.
        category_ = ""
    # end if
    results_ = get_bookmarks(Array({"category": category_, "orderby": orderby_, "order": order_, "show_updated": show_updated_, "limit": limit_}))
    if (not results_):
        return
    # end if
    output_ = ""
    for row_ in results_:
        if (not (php_isset(lambda : row_.recently_updated))):
            row_.recently_updated = False
        # end if
        output_ += before_
        if show_updated_ and row_.recently_updated:
            output_ += get_option("links_recently_updated_prepend")
        # end if
        the_link_ = "#"
        if (not php_empty(lambda : row_.link_url)):
            the_link_ = esc_url(row_.link_url)
        # end if
        rel_ = row_.link_rel
        if "" != rel_:
            rel_ = " rel=\"" + rel_ + "\""
        # end if
        desc_ = esc_attr(sanitize_bookmark_field("link_description", row_.link_description, row_.link_id, "display"))
        name_ = esc_attr(sanitize_bookmark_field("link_name", row_.link_name, row_.link_id, "display"))
        title_ = desc_
        if show_updated_:
            if php_substr(row_.link_updated_f, 0, 2) != "00":
                title_ += " (" + __("Last updated") + " " + gmdate(get_option("links_updated_date_format"), row_.link_updated_f + get_option("gmt_offset") * HOUR_IN_SECONDS) + ")"
            # end if
        # end if
        if "" != title_:
            title_ = " title=\"" + title_ + "\""
        # end if
        alt_ = " alt=\"" + name_ + "\""
        target_ = row_.link_target
        if "" != target_:
            target_ = " target=\"" + target_ + "\""
        # end if
        output_ += "<a href=\"" + the_link_ + "\"" + rel_ + title_ + target_ + ">"
        if row_.link_image != None and show_images_:
            if php_strpos(row_.link_image, "http") != False:
                output_ += str("<img src=\"") + str(row_.link_image) + str("\" ") + str(alt_) + str(" ") + str(title_) + str(" />")
            else:
                #// If it's a relative path.
                output_ += "<img src=\"" + get_option("siteurl") + str(row_.link_image) + str("\" ") + str(alt_) + str(" ") + str(title_) + str(" />")
            # end if
        else:
            output_ += name_
        # end if
        output_ += "</a>"
        if show_updated_ and row_.recently_updated:
            output_ += get_option("links_recently_updated_append")
        # end if
        if show_description_ and "" != desc_:
            output_ += between_ + desc_
        # end if
        if show_rating_:
            output_ += between_ + get_linkrating(row_)
        # end if
        output_ += str(after_) + str("\n")
    # end for
    #// End while.
    if (not echo_):
        return output_
    # end if
    php_print(output_)
# end def get_links
#// 
#// Output entire list of links by category.
#// 
#// Output a list of all links, listed by category, using the settings in
#// $wpdb->linkcategories and output it as a nested HTML unordered list.
#// 
#// @since 1.0.1
#// @deprecated 2.1.0 Use wp_list_bookmarks()
#// @see wp_list_bookmarks()
#// 
#// @param string $order Sort link categories by 'name' or 'id'
#//
def get_links_list(order_="name", *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.1.0", "wp_list_bookmarks()")
    order_ = php_strtolower(order_)
    #// Handle link category sorting.
    direction_ = "ASC"
    if "_" == php_substr(order_, 0, 1):
        direction_ = "DESC"
        order_ = php_substr(order_, 1)
    # end if
    if (not (php_isset(lambda : direction_))):
        direction_ = ""
    # end if
    cats_ = get_categories(Array({"type": "link", "orderby": order_, "order": direction_, "hierarchical": 0}))
    #// Display each category.
    if cats_:
        for cat_ in cats_:
            #// Handle each category.
            #// Display the category name.
            php_print("  <li id=\"linkcat-" + cat_.term_id + "\" class=\"linkcat\"><h2>" + apply_filters("link_category", cat_.name) + "</h2>\n <ul>\n")
            #// Call get_links() with all the appropriate params.
            get_links(cat_.term_id, "<li>", "</li>", "\n", True, "name", False)
            #// Close the last category.
            php_print("""
            </ul>
            </li>
            """)
        # end for
    # end if
# end def get_links_list
#// 
#// Show the link to the links popup and the number of links.
#// 
#// @since 0.71
#// @deprecated 2.1.0
#// 
#// @param string $text the text of the link
#// @param int $width the width of the popup window
#// @param int $height the height of the popup window
#// @param string $file the page to open in the popup window
#// @param bool $count the number of links in the db
#//
def links_popup_script(text_="Links", width_=400, height_=400, file_="links.all.php", count_=None, *_args_):
    if count_ is None:
        count_ = True
    # end if
    
    _deprecated_function(__FUNCTION__, "2.1.0")
# end def links_popup_script
#// 
#// Legacy function that retrieved the value of a link's link_rating field.
#// 
#// @since 1.0.1
#// @deprecated 2.1.0 Use sanitize_bookmark_field()
#// @see sanitize_bookmark_field()
#// 
#// @param object $link Link object.
#// @return mixed Value of the 'link_rating' field, false otherwise.
#//
def get_linkrating(link_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.1.0", "sanitize_bookmark_field()")
    return sanitize_bookmark_field("link_rating", link_.link_rating, link_.link_id, "display")
# end def get_linkrating
#// 
#// Gets the name of category by id.
#// 
#// @since 0.71
#// @deprecated 2.1.0 Use get_category()
#// @see get_category()
#// 
#// @param int $id The category to get. If no category supplied uses 0
#// @return string
#//
def get_linkcatname(id_=0, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.1.0", "get_category()")
    id_ = php_int(id_)
    if php_empty(lambda : id_):
        return ""
    # end if
    cats_ = wp_get_link_cats(id_)
    if php_empty(lambda : cats_) or (not php_is_array(cats_)):
        return ""
    # end if
    cat_id_ = php_int(cats_[0])
    #// Take the first cat.
    cat_ = get_category(cat_id_)
    return cat_.name
# end def get_linkcatname
#// 
#// Print RSS comment feed link.
#// 
#// @since 1.0.1
#// @deprecated 2.5.0 Use post_comments_feed_link()
#// @see post_comments_feed_link()
#// 
#// @param string $link_text
#//
def comments_rss_link(link_text_="Comments RSS", *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.5.0", "post_comments_feed_link()")
    post_comments_feed_link(link_text_)
# end def comments_rss_link
#// 
#// Print/Return link to category RSS2 feed.
#// 
#// @since 1.2.0
#// @deprecated 2.5.0 Use get_category_feed_link()
#// @see get_category_feed_link()
#// 
#// @param bool $echo
#// @param int $cat_ID
#// @return string
#//
def get_category_rss_link(echo_=None, cat_ID_=1, *_args_):
    if echo_ is None:
        echo_ = False
    # end if
    
    _deprecated_function(__FUNCTION__, "2.5.0", "get_category_feed_link()")
    link_ = get_category_feed_link(cat_ID_, "rss2")
    if echo_:
        php_print(link_)
    # end if
    return link_
# end def get_category_rss_link
#// 
#// Print/Return link to author RSS feed.
#// 
#// @since 1.2.0
#// @deprecated 2.5.0 Use get_author_feed_link()
#// @see get_author_feed_link()
#// 
#// @param bool $echo
#// @param int $author_id
#// @return string
#//
def get_author_rss_link(echo_=None, author_id_=1, *_args_):
    if echo_ is None:
        echo_ = False
    # end if
    
    _deprecated_function(__FUNCTION__, "2.5.0", "get_author_feed_link()")
    link_ = get_author_feed_link(author_id_)
    if echo_:
        php_print(link_)
    # end if
    return link_
# end def get_author_rss_link
#// 
#// Return link to the post RSS feed.
#// 
#// @since 1.5.0
#// @deprecated 2.2.0 Use get_post_comments_feed_link()
#// @see get_post_comments_feed_link()
#// 
#// @return string
#//
def comments_rss(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.2.0", "get_post_comments_feed_link()")
    return esc_url(get_post_comments_feed_link())
# end def comments_rss
#// 
#// An alias of wp_create_user().
#// 
#// @since 2.0.0
#// @deprecated 2.0.0 Use wp_create_user()
#// @see wp_create_user()
#// 
#// @param string $username The user's username.
#// @param string $password The user's password.
#// @param string $email    The user's email.
#// @return int The new user's ID.
#//
def create_user(username_=None, password_=None, email_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.0.0", "wp_create_user()")
    return wp_create_user(username_, password_, email_)
# end def create_user
#// 
#// Unused function.
#// 
#// @deprecated 2.5.0
#//
def gzip_compression(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.5.0")
    return False
# end def gzip_compression
#// 
#// Retrieve an array of comment data about comment $comment_ID.
#// 
#// @since 0.71
#// @deprecated 2.7.0 Use get_comment()
#// @see get_comment()
#// 
#// @param int $comment_ID The ID of the comment
#// @param int $no_cache Whether to use the cache (cast to bool)
#// @param bool $include_unapproved Whether to include unapproved comments
#// @return array The comment data
#//
def get_commentdata(comment_ID_=None, no_cache_=0, include_unapproved_=None, *_args_):
    if include_unapproved_ is None:
        include_unapproved_ = False
    # end if
    
    _deprecated_function(__FUNCTION__, "2.7.0", "get_comment()")
    return get_comment(comment_ID_, ARRAY_A)
# end def get_commentdata
#// 
#// Retrieve the category name by the category ID.
#// 
#// @since 0.71
#// @deprecated 2.8.0 Use get_cat_name()
#// @see get_cat_name()
#// 
#// @param int $cat_ID Category ID
#// @return string category name
#//
def get_catname(cat_ID_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.8.0", "get_cat_name()")
    return get_cat_name(cat_ID_)
# end def get_catname
#// 
#// Retrieve category children list separated before and after the term IDs.
#// 
#// @since 1.2.0
#// @deprecated 2.8.0 Use get_term_children()
#// @see get_term_children()
#// 
#// @param int $id Category ID to retrieve children.
#// @param string $before Optional. Prepend before category term ID.
#// @param string $after Optional, default is empty string. Append after category term ID.
#// @param array $visited Optional. Category Term IDs that have already been added.
#// @return string
#//
def get_category_children(id_=None, before_="/", after_="", visited_=None, *_args_):
    if visited_ is None:
        visited_ = Array()
    # end if
    
    _deprecated_function(__FUNCTION__, "2.8.0", "get_term_children()")
    if 0 == id_:
        return ""
    # end if
    chain_ = ""
    #// TODO: Consult hierarchy
    cat_ids_ = get_all_category_ids()
    for cat_id_ in cat_ids_:
        if cat_id_ == id_:
            continue
        # end if
        category_ = get_category(cat_id_)
        if is_wp_error(category_):
            return category_
        # end if
        if category_.parent == id_ and (not php_in_array(category_.term_id, visited_)):
            visited_[-1] = category_.term_id
            chain_ += before_ + category_.term_id + after_
            chain_ += get_category_children(category_.term_id, before_, after_)
        # end if
    # end for
    return chain_
# end def get_category_children
#// 
#// Retrieves all category IDs.
#// 
#// @since 2.0.0
#// @deprecated 4.0.0 Use get_terms()
#// @see get_terms()
#// 
#// @link https://developer.wordpress.org/reference/functions/get_all_category_ids
#// 
#// @return object List of all of the category IDs.
#//
def get_all_category_ids(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "4.0.0", "get_terms()")
    cat_ids_ = get_terms(Array({"taxonomy": "category", "fields": "ids", "get": "all"}))
    return cat_ids_
# end def get_all_category_ids
#// 
#// Retrieve the description of the author of the current post.
#// 
#// @since 1.5.0
#// @deprecated 2.8.0 Use get_the_author_meta()
#// @see get_the_author_meta()
#// 
#// @return string The author's description.
#//
def get_the_author_description(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.8.0", "get_the_author_meta('description')")
    return get_the_author_meta("description")
# end def get_the_author_description
#// 
#// Display the description of the author of the current post.
#// 
#// @since 1.0.0
#// @deprecated 2.8.0 Use the_author_meta()
#// @see the_author_meta()
#//
def the_author_description(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.8.0", "the_author_meta('description')")
    the_author_meta("description")
# end def the_author_description
#// 
#// Retrieve the login name of the author of the current post.
#// 
#// @since 1.5.0
#// @deprecated 2.8.0 Use get_the_author_meta()
#// @see get_the_author_meta()
#// 
#// @return string The author's login name (username).
#//
def get_the_author_login(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.8.0", "get_the_author_meta('login')")
    return get_the_author_meta("login")
# end def get_the_author_login
#// 
#// Display the login name of the author of the current post.
#// 
#// @since 0.71
#// @deprecated 2.8.0 Use the_author_meta()
#// @see the_author_meta()
#//
def the_author_login(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.8.0", "the_author_meta('login')")
    the_author_meta("login")
# end def the_author_login
#// 
#// Retrieve the first name of the author of the current post.
#// 
#// @since 1.5.0
#// @deprecated 2.8.0 Use get_the_author_meta()
#// @see get_the_author_meta()
#// 
#// @return string The author's first name.
#//
def get_the_author_firstname(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.8.0", "get_the_author_meta('first_name')")
    return get_the_author_meta("first_name")
# end def get_the_author_firstname
#// 
#// Display the first name of the author of the current post.
#// 
#// @since 0.71
#// @deprecated 2.8.0 Use the_author_meta()
#// @see the_author_meta()
#//
def the_author_firstname(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.8.0", "the_author_meta('first_name')")
    the_author_meta("first_name")
# end def the_author_firstname
#// 
#// Retrieve the last name of the author of the current post.
#// 
#// @since 1.5.0
#// @deprecated 2.8.0 Use get_the_author_meta()
#// @see get_the_author_meta()
#// 
#// @return string The author's last name.
#//
def get_the_author_lastname(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.8.0", "get_the_author_meta('last_name')")
    return get_the_author_meta("last_name")
# end def get_the_author_lastname
#// 
#// Display the last name of the author of the current post.
#// 
#// @since 0.71
#// @deprecated 2.8.0 Use the_author_meta()
#// @see the_author_meta()
#//
def the_author_lastname(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.8.0", "the_author_meta('last_name')")
    the_author_meta("last_name")
# end def the_author_lastname
#// 
#// Retrieve the nickname of the author of the current post.
#// 
#// @since 1.5.0
#// @deprecated 2.8.0 Use get_the_author_meta()
#// @see get_the_author_meta()
#// 
#// @return string The author's nickname.
#//
def get_the_author_nickname(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.8.0", "get_the_author_meta('nickname')")
    return get_the_author_meta("nickname")
# end def get_the_author_nickname
#// 
#// Display the nickname of the author of the current post.
#// 
#// @since 0.71
#// @deprecated 2.8.0 Use the_author_meta()
#// @see the_author_meta()
#//
def the_author_nickname(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.8.0", "the_author_meta('nickname')")
    the_author_meta("nickname")
# end def the_author_nickname
#// 
#// Retrieve the email of the author of the current post.
#// 
#// @since 1.5.0
#// @deprecated 2.8.0 Use get_the_author_meta()
#// @see get_the_author_meta()
#// 
#// @return string The author's username.
#//
def get_the_author_email(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.8.0", "get_the_author_meta('email')")
    return get_the_author_meta("email")
# end def get_the_author_email
#// 
#// Display the email of the author of the current post.
#// 
#// @since 0.71
#// @deprecated 2.8.0 Use the_author_meta()
#// @see the_author_meta()
#//
def the_author_email(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.8.0", "the_author_meta('email')")
    the_author_meta("email")
# end def the_author_email
#// 
#// Retrieve the ICQ number of the author of the current post.
#// 
#// @since 1.5.0
#// @deprecated 2.8.0 Use get_the_author_meta()
#// @see get_the_author_meta()
#// 
#// @return string The author's ICQ number.
#//
def get_the_author_icq(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.8.0", "get_the_author_meta('icq')")
    return get_the_author_meta("icq")
# end def get_the_author_icq
#// 
#// Display the ICQ number of the author of the current post.
#// 
#// @since 0.71
#// @deprecated 2.8.0 Use the_author_meta()
#// @see the_author_meta()
#//
def the_author_icq(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.8.0", "the_author_meta('icq')")
    the_author_meta("icq")
# end def the_author_icq
#// 
#// Retrieve the Yahoo! IM name of the author of the current post.
#// 
#// @since 1.5.0
#// @deprecated 2.8.0 Use get_the_author_meta()
#// @see get_the_author_meta()
#// 
#// @return string The author's Yahoo! IM name.
#//
def get_the_author_yim(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.8.0", "get_the_author_meta('yim')")
    return get_the_author_meta("yim")
# end def get_the_author_yim
#// 
#// Display the Yahoo! IM name of the author of the current post.
#// 
#// @since 0.71
#// @deprecated 2.8.0 Use the_author_meta()
#// @see the_author_meta()
#//
def the_author_yim(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.8.0", "the_author_meta('yim')")
    the_author_meta("yim")
# end def the_author_yim
#// 
#// Retrieve the MSN address of the author of the current post.
#// 
#// @since 1.5.0
#// @deprecated 2.8.0 Use get_the_author_meta()
#// @see get_the_author_meta()
#// 
#// @return string The author's MSN address.
#//
def get_the_author_msn(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.8.0", "get_the_author_meta('msn')")
    return get_the_author_meta("msn")
# end def get_the_author_msn
#// 
#// Display the MSN address of the author of the current post.
#// 
#// @since 0.71
#// @deprecated 2.8.0 Use the_author_meta()
#// @see the_author_meta()
#//
def the_author_msn(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.8.0", "the_author_meta('msn')")
    the_author_meta("msn")
# end def the_author_msn
#// 
#// Retrieve the AIM address of the author of the current post.
#// 
#// @since 1.5.0
#// @deprecated 2.8.0 Use get_the_author_meta()
#// @see get_the_author_meta()
#// 
#// @return string The author's AIM address.
#//
def get_the_author_aim(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.8.0", "get_the_author_meta('aim')")
    return get_the_author_meta("aim")
# end def get_the_author_aim
#// 
#// Display the AIM address of the author of the current post.
#// 
#// @since 0.71
#// @deprecated 2.8.0 Use the_author_meta('aim')
#// @see the_author_meta()
#//
def the_author_aim(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.8.0", "the_author_meta('aim')")
    the_author_meta("aim")
# end def the_author_aim
#// 
#// Retrieve the specified author's preferred display name.
#// 
#// @since 1.0.0
#// @deprecated 2.8.0 Use get_the_author_meta()
#// @see get_the_author_meta()
#// 
#// @param int $auth_id The ID of the author.
#// @return string The author's display name.
#//
def get_author_name(auth_id_=None, *_args_):
    if auth_id_ is None:
        auth_id_ = False
    # end if
    
    _deprecated_function(__FUNCTION__, "2.8.0", "get_the_author_meta('display_name')")
    return get_the_author_meta("display_name", auth_id_)
# end def get_author_name
#// 
#// Retrieve the URL to the home page of the author of the current post.
#// 
#// @since 1.5.0
#// @deprecated 2.8.0 Use get_the_author_meta()
#// @see get_the_author_meta()
#// 
#// @return string The URL to the author's page.
#//
def get_the_author_url(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.8.0", "get_the_author_meta('url')")
    return get_the_author_meta("url")
# end def get_the_author_url
#// 
#// Display the URL to the home page of the author of the current post.
#// 
#// @since 0.71
#// @deprecated 2.8.0 Use the_author_meta()
#// @see the_author_meta()
#//
def the_author_url(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.8.0", "the_author_meta('url')")
    the_author_meta("url")
# end def the_author_url
#// 
#// Retrieve the ID of the author of the current post.
#// 
#// @since 1.5.0
#// @deprecated 2.8.0 Use get_the_author_meta()
#// @see get_the_author_meta()
#// 
#// @return string|int The author's ID.
#//
def get_the_author_ID(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.8.0", "get_the_author_meta('ID')")
    return get_the_author_meta("ID")
# end def get_the_author_ID
#// 
#// Display the ID of the author of the current post.
#// 
#// @since 0.71
#// @deprecated 2.8.0 Use the_author_meta()
#// @see the_author_meta()
#//
def the_author_ID(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.8.0", "the_author_meta('ID')")
    the_author_meta("ID")
# end def the_author_ID
#// 
#// Display the post content for the feed.
#// 
#// For encoding the html or the $encode_html parameter, there are three possible
#// values. '0' will make urls footnotes and use make_url_footnote(). '1' will
#// encode special characters and automatically display all of the content. The
#// value of '2' will strip all HTML tags from the content.
#// 
#// Also note that you cannot set the amount of words and not set the html
#// encoding. If that is the case, then the html encoding will default to 2,
#// which will strip all HTML tags.
#// 
#// To restrict the amount of words of the content, you can use the cut
#// parameter. If the content is less than the amount, then there won't be any
#// dots added to the end. If there is content left over, then dots will be added
#// and the rest of the content will be removed.
#// 
#// @since 0.71
#// 
#// @deprecated 2.9.0 Use the_content_feed()
#// @see the_content_feed()
#// 
#// @param string $more_link_text Optional. Text to display when more content is available but not displayed.
#// @param int $stripteaser Optional. Default is 0.
#// @param string $more_file Optional.
#// @param int $cut Optional. Amount of words to keep for the content.
#// @param int $encode_html Optional. How to encode the content.
#//
def the_content_rss(more_link_text_="(more...)", stripteaser_=0, more_file_="", cut_=0, encode_html_=0, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.9.0", "the_content_feed()")
    content_ = get_the_content(more_link_text_, stripteaser_)
    #// 
    #// Filters the post content in the context of an RSS feed.
    #// 
    #// @since 0.71
    #// 
    #// @param string $content Content of the current post.
    #//
    content_ = apply_filters("the_content_rss", content_)
    if cut_ and (not encode_html_):
        encode_html_ = 2
    # end if
    if 1 == encode_html_:
        content_ = esc_html(content_)
        cut_ = 0
    elif 0 == encode_html_:
        content_ = make_url_footnote(content_)
    elif 2 == encode_html_:
        content_ = strip_tags(content_)
    # end if
    if cut_:
        blah_ = php_explode(" ", content_)
        if php_count(blah_) > cut_:
            k_ = cut_
            use_dotdotdot_ = 1
        else:
            k_ = php_count(blah_)
            use_dotdotdot_ = 0
        # end if
        #// @todo Check performance, might be faster to use array slice instead.
        i_ = 0
        while i_ < k_:
            
            excerpt_ += blah_[i_] + " "
            i_ += 1
        # end while
        excerpt_ += "..." if use_dotdotdot_ else ""
        content_ = excerpt_
    # end if
    content_ = php_str_replace("]]>", "]]&gt;", content_)
    php_print(content_)
# end def the_content_rss
#// 
#// Strip HTML and put links at the bottom of stripped content.
#// 
#// Searches for all of the links, strips them out of the content, and places
#// them at the bottom of the content with numbers.
#// 
#// @since 0.71
#// @deprecated 2.9.0
#// 
#// @param string $content Content to get links
#// @return string HTML stripped out of content with links at the bottom.
#//
def make_url_footnote(content_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.9.0", "")
    preg_match_all("/<a(.+?)href=\\\"(.+?)\\\"(.*?)>(.+?)<\\/a>/", content_, matches_)
    links_summary_ = "\n"
    i_ = 0
    c_ = php_count(matches_[0])
    while i_ < c_:
        
        link_match_ = matches_[0][i_]
        link_number_ = "[" + i_ + 1 + "]"
        link_url_ = matches_[2][i_]
        link_text_ = matches_[4][i_]
        content_ = php_str_replace(link_match_, link_text_ + " " + link_number_, content_)
        link_url_ = get_option("home") + link_url_ if php_strtolower(php_substr(link_url_, 0, 7)) != "http://" and php_strtolower(php_substr(link_url_, 0, 8)) != "https://" else link_url_
        links_summary_ += "\n" + link_number_ + " " + link_url_
        i_ += 1
    # end while
    content_ = strip_tags(content_)
    content_ += links_summary_
    return content_
# end def make_url_footnote
#// 
#// Retrieve translated string with vertical bar context
#// 
#// Quite a few times, there will be collisions with similar translatable text
#// found in more than two places but with different translated context.
#// 
#// In order to use the separate contexts, the _c() function is used and the
#// translatable string uses a pipe ('|') which has the context the string is in.
#// 
#// When the translated string is returned, it is everything before the pipe, not
#// including the pipe character. If there is no pipe in the translated text then
#// everything is returned.
#// 
#// @since 2.2.0
#// @deprecated 2.9.0 Use _x()
#// @see _x()
#// 
#// @param string $text Text to translate
#// @param string $domain Optional. Domain to retrieve the translated text
#// @return string Translated context string without pipe
#//
def _c(text_=None, domain_="default", *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.9.0", "_x()")
    return before_last_bar(translate(text_, domain_))
# end def _c
#// 
#// Translates $text like translate(), but assumes that the text
#// contains a context after its last vertical bar.
#// 
#// @since 2.5.0
#// @deprecated 3.0.0 Use _x()
#// @see _x()
#// 
#// @param string $text Text to translate
#// @param string $domain Domain to retrieve the translated text
#// @return string Translated text
#//
def translate_with_context(text_=None, domain_="default", *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.9.0", "_x()")
    return before_last_bar(translate(text_, domain_))
# end def translate_with_context
#// 
#// Legacy version of _n(), which supports contexts.
#// 
#// Strips everything from the translation after the last bar.
#// 
#// @since 2.7.0
#// @deprecated 3.0.0 Use _nx()
#// @see _nx()
#// 
#// @param string $single The text to be used if the number is singular.
#// @param string $plural The text to be used if the number is plural.
#// @param int    $number The number to compare against to use either the singular or plural form.
#// @param string $domain Optional. Text domain. Unique identifier for retrieving translated strings.
#// Default 'default'.
#// @return string The translated singular or plural form.
#//
def _nc(single_=None, plural_=None, number_=None, domain_="default", *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.9.0", "_nx()")
    return before_last_bar(_n(single_, plural_, number_, domain_))
# end def _nc
#// 
#// Retrieve the plural or single form based on the amount.
#// 
#// @since 1.2.0
#// @deprecated 2.8.0 Use _n()
#// @see _n()
#//
def __ngettext(*args_):
    
    
    #// phpcs:ignore PHPCompatibility.FunctionNameRestrictions.ReservedFunctionNames.FunctionDoubleUnderscore
    _deprecated_function(__FUNCTION__, "2.8.0", "_n()")
    return _n(args_)
# end def __ngettext
#// 
#// Register plural strings in POT file, but don't translate them.
#// 
#// @since 2.5.0
#// @deprecated 2.8.0 Use _n_noop()
#// @see _n_noop()
#//
def __ngettext_noop(*args_):
    
    
    #// phpcs:ignore PHPCompatibility.FunctionNameRestrictions.ReservedFunctionNames.FunctionDoubleUnderscore
    _deprecated_function(__FUNCTION__, "2.8.0", "_n_noop()")
    return _n_noop(args_)
# end def __ngettext_noop
#// 
#// Retrieve all autoload options, or all options if no autoloaded ones exist.
#// 
#// @since 1.0.0
#// @deprecated 3.0.0 Use wp_load_alloptions())
#// @see wp_load_alloptions()
#// 
#// @return array List of all options.
#//
def get_alloptions(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.0.0", "wp_load_alloptions()")
    return wp_load_alloptions()
# end def get_alloptions
#// 
#// Retrieve HTML content of attachment image with link.
#// 
#// @since 2.0.0
#// @deprecated 2.5.0 Use wp_get_attachment_link()
#// @see wp_get_attachment_link()
#// 
#// @param int $id Optional. Post ID.
#// @param bool $fullsize Optional, default is false. Whether to use full size image.
#// @param array $max_dims Optional. Max image dimensions.
#// @param bool $permalink Optional, default is false. Whether to include permalink to image.
#// @return string
#//
def get_the_attachment_link(id_=0, fullsize_=None, max_dims_=None, permalink_=None, *_args_):
    if fullsize_ is None:
        fullsize_ = False
    # end if
    if max_dims_ is None:
        max_dims_ = False
    # end if
    if permalink_ is None:
        permalink_ = False
    # end if
    
    _deprecated_function(__FUNCTION__, "2.5.0", "wp_get_attachment_link()")
    id_ = php_int(id_)
    _post_ = get_post(id_)
    url_ = wp_get_attachment_url(_post_.ID)
    if "attachment" != _post_.post_type or (not url_):
        return __("Missing Attachment")
    # end if
    if permalink_:
        url_ = get_attachment_link(_post_.ID)
    # end if
    post_title_ = esc_attr(_post_.post_title)
    innerHTML_ = get_attachment_innerHTML(_post_.ID, fullsize_, max_dims_)
    return str("<a href='") + str(url_) + str("' title='") + str(post_title_) + str("'>") + str(innerHTML_) + str("</a>")
# end def get_the_attachment_link
#// 
#// Retrieve icon URL and Path.
#// 
#// @since 2.1.0
#// @deprecated 2.5.0 Use wp_get_attachment_image_src()
#// @see wp_get_attachment_image_src()
#// 
#// @param int $id Optional. Post ID.
#// @param bool $fullsize Optional, default to false. Whether to have full image.
#// @return array Icon URL and full path to file, respectively.
#//
def get_attachment_icon_src(id_=0, fullsize_=None, *_args_):
    if fullsize_ is None:
        fullsize_ = False
    # end if
    
    _deprecated_function(__FUNCTION__, "2.5.0", "wp_get_attachment_image_src()")
    id_ = php_int(id_)
    post_ = get_post(id_)
    if (not post_):
        return False
    # end if
    file_ = get_attached_file(post_.ID)
    src_ = wp_get_attachment_thumb_url(post_.ID)
    if (not fullsize_) and src_:
        #// We have a thumbnail desired, specified and existing.
        src_file_ = wp_basename(src_)
    elif wp_attachment_is_image(post_.ID):
        #// We have an image without a thumbnail.
        src_ = wp_get_attachment_url(post_.ID)
        src_file_ = file_
    elif wp_mime_type_icon(post_.ID):
        src_ = wp_mime_type_icon(post_.ID)
        #// No thumb, no image. We'll look for a mime-related icon instead.
        icon_dir_ = apply_filters("icon_dir", get_template_directory() + "/images")
        src_file_ = icon_dir_ + "/" + wp_basename(src_)
    # end if
    if (not (php_isset(lambda : src_))) or (not src_):
        return False
    # end if
    return Array(src_, src_file_)
# end def get_attachment_icon_src
#// 
#// Retrieve HTML content of icon attachment image element.
#// 
#// @since 2.0.0
#// @deprecated 2.5.0 Use wp_get_attachment_image()
#// @see wp_get_attachment_image()
#// 
#// @param int $id Optional. Post ID.
#// @param bool $fullsize Optional, default to false. Whether to have full size image.
#// @param array $max_dims Optional. Dimensions of image.
#// @return string|false HTML content.
#//
def get_attachment_icon(id_=0, fullsize_=None, max_dims_=None, *_args_):
    if fullsize_ is None:
        fullsize_ = False
    # end if
    if max_dims_ is None:
        max_dims_ = False
    # end if
    
    _deprecated_function(__FUNCTION__, "2.5.0", "wp_get_attachment_image()")
    id_ = php_int(id_)
    post_ = get_post(id_)
    if (not post_):
        return False
    # end if
    src_ = get_attachment_icon_src(post_.ID, fullsize_)
    if (not src_):
        return False
    # end if
    src_, src_file_ = src_
    #// Do we need to constrain the image?
    max_dims_ = apply_filters("attachment_max_dims", max_dims_)
    if max_dims_ and php_file_exists(src_file_):
        imagesize_ = php_no_error(lambda: getimagesize(src_file_))
        if imagesize_[0] > max_dims_[0] or imagesize_[1] > max_dims_[1]:
            actual_aspect_ = imagesize_[0] / imagesize_[1]
            desired_aspect_ = max_dims_[0] / max_dims_[1]
            if actual_aspect_ >= desired_aspect_:
                height_ = actual_aspect_ * max_dims_[0]
                constraint_ = str("width='") + str(max_dims_[0]) + str("' ")
                post_.iconsize = Array(max_dims_[0], height_)
            else:
                width_ = max_dims_[1] / actual_aspect_
                constraint_ = str("height='") + str(max_dims_[1]) + str("' ")
                post_.iconsize = Array(width_, max_dims_[1])
            # end if
        else:
            post_.iconsize = Array(imagesize_[0], imagesize_[1])
            constraint_ = ""
        # end if
    else:
        constraint_ = ""
    # end if
    post_title_ = esc_attr(post_.post_title)
    icon_ = str("<img src='") + str(src_) + str("' title='") + str(post_title_) + str("' alt='") + str(post_title_) + str("' ") + str(constraint_) + str("/>")
    return apply_filters("attachment_icon", icon_, post_.ID)
# end def get_attachment_icon
#// 
#// Retrieve HTML content of image element.
#// 
#// @since 2.0.0
#// @deprecated 2.5.0 Use wp_get_attachment_image()
#// @see wp_get_attachment_image()
#// 
#// @param int $id Optional. Post ID.
#// @param bool $fullsize Optional, default to false. Whether to have full size image.
#// @param array $max_dims Optional. Dimensions of image.
#// @return string|false
#//
def get_attachment_innerHTML(id_=0, fullsize_=None, max_dims_=None, *_args_):
    if fullsize_ is None:
        fullsize_ = False
    # end if
    if max_dims_ is None:
        max_dims_ = False
    # end if
    
    _deprecated_function(__FUNCTION__, "2.5.0", "wp_get_attachment_image()")
    id_ = php_int(id_)
    post_ = get_post(id_)
    if (not post_):
        return False
    # end if
    innerHTML_ = get_attachment_icon(post_.ID, fullsize_, max_dims_)
    if innerHTML_:
        return innerHTML_
    # end if
    innerHTML_ = esc_attr(post_.post_title)
    return apply_filters("attachment_innerHTML", innerHTML_, post_.ID)
# end def get_attachment_innerHTML
#// 
#// Retrieves bookmark data based on ID.
#// 
#// @since 2.0.0
#// @deprecated 2.1.0 Use get_bookmark()
#// @see get_bookmark()
#// 
#// @param int    $bookmark_id ID of link
#// @param string $output      Optional. Type of output. Accepts OBJECT, ARRAY_N, or ARRAY_A.
#// Default OBJECT.
#// @param string $filter      Optional. How to filter the link for output. Accepts 'raw', 'edit',
#// 'attribute', 'js', 'db', or 'display'. Default 'raw'.
#// @return object|array Bookmark object or array, depending on the type specified by `$output`.
#//
def get_link(bookmark_id_=None, output_=None, filter_="raw", *_args_):
    if output_ is None:
        output_ = OBJECT
    # end if
    
    _deprecated_function(__FUNCTION__, "2.1.0", "get_bookmark()")
    return get_bookmark(bookmark_id_, output_, filter_)
# end def get_link
#// 
#// Performs esc_url() for database or redirect usage.
#// 
#// @since 2.3.1
#// @deprecated 2.8.0 Use esc_url_raw()
#// @see esc_url_raw()
#// 
#// @param string $url The URL to be cleaned.
#// @param array $protocols An array of acceptable protocols.
#// @return string The cleaned URL.
#//
def sanitize_url(url_=None, protocols_=None, *_args_):
    if protocols_ is None:
        protocols_ = None
    # end if
    
    _deprecated_function(__FUNCTION__, "2.8.0", "esc_url_raw()")
    return esc_url_raw(url_, protocols_)
# end def sanitize_url
#// 
#// Checks and cleans a URL.
#// 
#// A number of characters are removed from the URL. If the URL is for displaying
#// (the default behaviour) ampersands are also replaced. The 'clean_url' filter
#// is applied to the returned cleaned URL.
#// 
#// @since 1.2.0
#// @deprecated 3.0.0 Use esc_url()
#// @see esc_url()
#// 
#// @param string $url The URL to be cleaned.
#// @param array $protocols Optional. An array of acceptable protocols.
#// @param string $context Optional. How the URL will be used. Default is 'display'.
#// @return string The cleaned $url after the {@see 'clean_url'} filter is applied.
#//
def clean_url(url_=None, protocols_=None, context_="display", *_args_):
    if protocols_ is None:
        protocols_ = None
    # end if
    
    if context_ == "db":
        _deprecated_function("clean_url( $context = 'db' )", "3.0.0", "esc_url_raw()")
    else:
        _deprecated_function(__FUNCTION__, "3.0.0", "esc_url()")
    # end if
    return esc_url(url_, protocols_, context_)
# end def clean_url
#// 
#// Escape single quotes, specialchar double quotes, and fix line endings.
#// 
#// The filter {@see 'js_escape'} is also applied by esc_js().
#// 
#// @since 2.0.4
#// @deprecated 2.8.0 Use esc_js()
#// @see esc_js()
#// 
#// @param string $text The text to be escaped.
#// @return string Escaped text.
#//
def js_escape(text_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.8.0", "esc_js()")
    return esc_js(text_)
# end def js_escape
#// 
#// Legacy escaping for HTML blocks.
#// 
#// @deprecated 2.8.0 Use esc_html()
#// @see esc_html()
#// 
#// @param string       $string        String to escape.
#// @param string       $quote_style   Unused.
#// @param false|string $charset       Unused.
#// @param false        $double_encode Whether to double encode. Unused.
#// @return string Escaped `$string`.
#//
def wp_specialchars(string_=None, quote_style_=None, charset_=None, double_encode_=None, *_args_):
    if quote_style_ is None:
        quote_style_ = ENT_NOQUOTES
    # end if
    if charset_ is None:
        charset_ = False
    # end if
    if double_encode_ is None:
        double_encode_ = False
    # end if
    
    _deprecated_function(__FUNCTION__, "2.8.0", "esc_html()")
    if php_func_num_args() > 1:
        #// Maintain back-compat for people passing additional arguments.
        return _wp_specialchars(string_, quote_style_, charset_, double_encode_)
    else:
        return esc_html(string_)
    # end if
# end def wp_specialchars
#// 
#// Escaping for HTML attributes.
#// 
#// @since 2.0.6
#// @deprecated 2.8.0 Use esc_attr()
#// @see esc_attr()
#// 
#// @param string $text
#// @return string
#//
def attribute_escape(text_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.8.0", "esc_attr()")
    return esc_attr(text_)
# end def attribute_escape
#// 
#// Register widget for sidebar with backward compatibility.
#// 
#// Allows $name to be an array that accepts either three elements to grab the
#// first element and the third for the name or just uses the first element of
#// the array for the name.
#// 
#// Passes to wp_register_sidebar_widget() after argument list and backward
#// compatibility is complete.
#// 
#// @since 2.2.0
#// @deprecated 2.8.0 Use wp_register_sidebar_widget()
#// @see wp_register_sidebar_widget()
#// 
#// @param string|int $name            Widget ID.
#// @param callable   $output_callback Run when widget is called.
#// @param string     $classname       Optional. Classname widget option. Default empty.
#// @param mixed      ...$params       Widget parameters.
#//
def register_sidebar_widget(name_=None, output_callback_=None, classname_="", *params_):
    
    
    _deprecated_function(__FUNCTION__, "2.8.0", "wp_register_sidebar_widget()")
    #// Compat.
    if php_is_array(name_):
        if php_count(name_) == 3:
            name_ = php_sprintf(name_[0], name_[2])
        else:
            name_ = name_[0]
        # end if
    # end if
    id_ = sanitize_title(name_)
    options_ = Array()
    if (not php_empty(lambda : classname_)) and php_is_string(classname_):
        options_["classname"] = classname_
    # end if
    wp_register_sidebar_widget(id_, name_, output_callback_, options_, params_)
# end def register_sidebar_widget
#// 
#// Serves as an alias of wp_unregister_sidebar_widget().
#// 
#// @since 2.2.0
#// @deprecated 2.8.0 Use wp_unregister_sidebar_widget()
#// @see wp_unregister_sidebar_widget()
#// 
#// @param int|string $id Widget ID.
#//
def unregister_sidebar_widget(id_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.8.0", "wp_unregister_sidebar_widget()")
    return wp_unregister_sidebar_widget(id_)
# end def unregister_sidebar_widget
#// 
#// Registers widget control callback for customizing options.
#// 
#// Allows $name to be an array that accepts either three elements to grab the
#// first element and the third for the name or just uses the first element of
#// the array for the name.
#// 
#// Passes to wp_register_widget_control() after the argument list has
#// been compiled.
#// 
#// @since 2.2.0
#// @deprecated 2.8.0 Use wp_register_widget_control()
#// @see wp_register_widget_control()
#// 
#// @param int|string $name             Sidebar ID.
#// @param callable   $control_callback Widget control callback to display and process form.
#// @param int        $width            Widget width.
#// @param int        $height           Widget height.
#// @param mixed      ...$params        Widget parameters.
#//
def register_widget_control(name_=None, control_callback_=None, width_="", height_="", *params_):
    
    
    _deprecated_function(__FUNCTION__, "2.8.0", "wp_register_widget_control()")
    #// Compat.
    if php_is_array(name_):
        if php_count(name_) == 3:
            name_ = php_sprintf(name_[0], name_[2])
        else:
            name_ = name_[0]
        # end if
    # end if
    id_ = sanitize_title(name_)
    options_ = Array()
    if (not php_empty(lambda : width_)):
        options_["width"] = width_
    # end if
    if (not php_empty(lambda : height_)):
        options_["height"] = height_
    # end if
    wp_register_widget_control(id_, name_, control_callback_, options_, params_)
# end def register_widget_control
#// 
#// Alias of wp_unregister_widget_control().
#// 
#// @since 2.2.0
#// @deprecated 2.8.0 Use wp_unregister_widget_control()
#// @see wp_unregister_widget_control()
#// 
#// @param int|string $id Widget ID.
#//
def unregister_widget_control(id_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "2.8.0", "wp_unregister_widget_control()")
    return wp_unregister_widget_control(id_)
# end def unregister_widget_control
#// 
#// Remove user meta data.
#// 
#// @since 2.0.0
#// @deprecated 3.0.0 Use delete_user_meta()
#// @see delete_user_meta()
#// 
#// @param int $user_id User ID.
#// @param string $meta_key Metadata key.
#// @param mixed $meta_value Metadata value.
#// @return bool True deletion completed and false if user_id is not a number.
#//
def delete_usermeta(user_id_=None, meta_key_=None, meta_value_="", *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.0.0", "delete_user_meta()")
    global wpdb_
    php_check_if_defined("wpdb_")
    if (not php_is_numeric(user_id_)):
        return False
    # end if
    meta_key_ = php_preg_replace("|[^a-z0-9_]|i", "", meta_key_)
    if php_is_array(meta_value_) or php_is_object(meta_value_):
        meta_value_ = serialize(meta_value_)
    # end if
    meta_value_ = php_trim(meta_value_)
    cur_ = wpdb_.get_row(wpdb_.prepare(str("SELECT * FROM ") + str(wpdb_.usermeta) + str(" WHERE user_id = %d AND meta_key = %s"), user_id_, meta_key_))
    if cur_ and cur_.umeta_id:
        do_action("delete_usermeta", cur_.umeta_id, user_id_, meta_key_, meta_value_)
    # end if
    if (not php_empty(lambda : meta_value_)):
        wpdb_.query(wpdb_.prepare(str("DELETE FROM ") + str(wpdb_.usermeta) + str(" WHERE user_id = %d AND meta_key = %s AND meta_value = %s"), user_id_, meta_key_, meta_value_))
    else:
        wpdb_.query(wpdb_.prepare(str("DELETE FROM ") + str(wpdb_.usermeta) + str(" WHERE user_id = %d AND meta_key = %s"), user_id_, meta_key_))
    # end if
    clean_user_cache(user_id_)
    wp_cache_delete(user_id_, "user_meta")
    if cur_ and cur_.umeta_id:
        do_action("deleted_usermeta", cur_.umeta_id, user_id_, meta_key_, meta_value_)
    # end if
    return True
# end def delete_usermeta
#// 
#// Retrieve user metadata.
#// 
#// If $user_id is not a number, then the function will fail over with a 'false'
#// boolean return value. Other returned values depend on whether there is only
#// one item to be returned, which be that single item type. If there is more
#// than one metadata value, then it will be list of metadata values.
#// 
#// @since 2.0.0
#// @deprecated 3.0.0 Use get_user_meta()
#// @see get_user_meta()
#// 
#// @param int $user_id User ID
#// @param string $meta_key Optional. Metadata key.
#// @return mixed
#//
def get_usermeta(user_id_=None, meta_key_="", *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.0.0", "get_user_meta()")
    global wpdb_
    php_check_if_defined("wpdb_")
    user_id_ = php_int(user_id_)
    if (not user_id_):
        return False
    # end if
    if (not php_empty(lambda : meta_key_)):
        meta_key_ = php_preg_replace("|[^a-z0-9_]|i", "", meta_key_)
        user_ = wp_cache_get(user_id_, "users")
        #// Check the cached user object.
        if False != user_ and (php_isset(lambda : user_.meta_key_)):
            metas_ = Array(user_.meta_key_)
        else:
            metas_ = wpdb_.get_col(wpdb_.prepare(str("SELECT meta_value FROM ") + str(wpdb_.usermeta) + str(" WHERE user_id = %d AND meta_key = %s"), user_id_, meta_key_))
        # end if
    else:
        metas_ = wpdb_.get_col(wpdb_.prepare(str("SELECT meta_value FROM ") + str(wpdb_.usermeta) + str(" WHERE user_id = %d"), user_id_))
    # end if
    if php_empty(lambda : metas_):
        if php_empty(lambda : meta_key_):
            return Array()
        else:
            return ""
        # end if
    # end if
    metas_ = php_array_map("maybe_unserialize", metas_)
    if php_count(metas_) == 1:
        return metas_[0]
    else:
        return metas_
    # end if
# end def get_usermeta
#// 
#// Update metadata of user.
#// 
#// There is no need to serialize values, they will be serialized if it is
#// needed. The metadata key can only be a string with underscores. All else will
#// be removed.
#// 
#// Will remove the metadata, if the meta value is empty.
#// 
#// @since 2.0.0
#// @deprecated 3.0.0 Use update_user_meta()
#// @see update_user_meta()
#// 
#// @param int $user_id User ID
#// @param string $meta_key Metadata key.
#// @param mixed $meta_value Metadata value.
#// @return bool True on successful update, false on failure.
#//
def update_usermeta(user_id_=None, meta_key_=None, meta_value_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.0.0", "update_user_meta()")
    global wpdb_
    php_check_if_defined("wpdb_")
    if (not php_is_numeric(user_id_)):
        return False
    # end if
    meta_key_ = php_preg_replace("|[^a-z0-9_]|i", "", meta_key_)
    #// @todo Might need fix because usermeta data is assumed to be already escaped
    if php_is_string(meta_value_):
        meta_value_ = stripslashes(meta_value_)
    # end if
    meta_value_ = maybe_serialize(meta_value_)
    if php_empty(lambda : meta_value_):
        return delete_usermeta(user_id_, meta_key_)
    # end if
    cur_ = wpdb_.get_row(wpdb_.prepare(str("SELECT * FROM ") + str(wpdb_.usermeta) + str(" WHERE user_id = %d AND meta_key = %s"), user_id_, meta_key_))
    if cur_:
        do_action("update_usermeta", cur_.umeta_id, user_id_, meta_key_, meta_value_)
    # end if
    if (not cur_):
        wpdb_.insert(wpdb_.usermeta, php_compact("user_id_", "meta_key_", "meta_value_"))
    elif cur_.meta_value != meta_value_:
        wpdb_.update(wpdb_.usermeta, php_compact("meta_value_"), php_compact("user_id_", "meta_key_"))
    else:
        return False
    # end if
    clean_user_cache(user_id_)
    wp_cache_delete(user_id_, "user_meta")
    if (not cur_):
        do_action("added_usermeta", wpdb_.insert_id, user_id_, meta_key_, meta_value_)
    else:
        do_action("updated_usermeta", cur_.umeta_id, user_id_, meta_key_, meta_value_)
    # end if
    return True
# end def update_usermeta
#// 
#// Get users for the site.
#// 
#// For setups that use the multisite feature. Can be used outside of the
#// multisite feature.
#// 
#// @since 2.2.0
#// @deprecated 3.1.0 Use get_users()
#// @see get_users()
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// 
#// @param int $id Site ID.
#// @return array List of users that are part of that site ID
#//
def get_users_of_blog(id_="", *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.1.0", "get_users()")
    global wpdb_
    php_check_if_defined("wpdb_")
    if php_empty(lambda : id_):
        id_ = get_current_blog_id()
    # end if
    blog_prefix_ = wpdb_.get_blog_prefix(id_)
    users_ = wpdb_.get_results(str("SELECT user_id, user_id AS ID, user_login, display_name, user_email, meta_value FROM ") + str(wpdb_.users) + str(", ") + str(wpdb_.usermeta) + str(" WHERE ") + str(wpdb_.users) + str(".ID = ") + str(wpdb_.usermeta) + str(".user_id AND meta_key = '") + str(blog_prefix_) + str("capabilities' ORDER BY ") + str(wpdb_.usermeta) + str(".user_id"))
    return users_
# end def get_users_of_blog
#// 
#// Enable/disable automatic general feed link outputting.
#// 
#// @since 2.8.0
#// @deprecated 3.0.0 Use add_theme_support()
#// @see add_theme_support()
#// 
#// @param bool $add Optional, default is true. Add or remove links. Defaults to true.
#//
def automatic_feed_links(add_=None, *_args_):
    if add_ is None:
        add_ = True
    # end if
    
    _deprecated_function(__FUNCTION__, "3.0.0", "add_theme_support( 'automatic-feed-links' )")
    if add_:
        add_theme_support("automatic-feed-links")
    else:
        remove_action("wp_head", "feed_links_extra", 3)
    # end if
    pass
# end def automatic_feed_links
#// 
#// Retrieve user data based on field.
#// 
#// @since 1.5.0
#// @deprecated 3.0.0 Use get_the_author_meta()
#// @see get_the_author_meta()
#// 
#// @param string    $field User meta field.
#// @param false|int $user Optional. User ID to retrieve the field for. Default false (current user).
#// @return string The author's field from the current author's DB object.
#//
def get_profile(field_=None, user_=None, *_args_):
    if user_ is None:
        user_ = False
    # end if
    
    _deprecated_function(__FUNCTION__, "3.0.0", "get_the_author_meta()")
    if user_:
        user_ = get_user_by("login", user_)
        user_ = user_.ID
    # end if
    return get_the_author_meta(field_, user_)
# end def get_profile
#// 
#// Retrieves the number of posts a user has written.
#// 
#// @since 0.71
#// @deprecated 3.0.0 Use count_user_posts()
#// @see count_user_posts()
#// 
#// @param int $userid User to count posts for.
#// @return int Number of posts the given user has written.
#//
def get_usernumposts(userid_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.0.0", "count_user_posts()")
    return count_user_posts(userid_)
# end def get_usernumposts
#// 
#// Callback used to change %uXXXX to &#YYY; syntax
#// 
#// @since 2.8.0
#// @access private
#// @deprecated 3.0.0
#// 
#// @param array $matches Single Match
#// @return string An HTML entity
#//
def funky_javascript_callback(matches_=None, *_args_):
    
    
    return "&#" + base_convert(matches_[1], 16, 10) + ";"
# end def funky_javascript_callback
#// 
#// Fixes JavaScript bugs in browsers.
#// 
#// Converts unicode characters to HTML numbered entities.
#// 
#// @since 1.5.0
#// @deprecated 3.0.0
#// 
#// @global $is_macIE
#// @global $is_winIE
#// 
#// @param string $text Text to be made safe.
#// @return string Fixed text.
#//
def funky_javascript_fix(text_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.0.0")
    #// Fixes for browsers' JavaScript bugs.
    global is_macIE_
    global is_winIE_
    php_check_if_defined("is_macIE_","is_winIE_")
    if is_winIE_ or is_macIE_:
        text_ = preg_replace_callback("/\\%u([0-9A-F]{4,4})/", "funky_javascript_callback", text_)
    # end if
    return text_
# end def funky_javascript_fix
#// 
#// Checks that the taxonomy name exists.
#// 
#// @since 2.3.0
#// @deprecated 3.0.0 Use taxonomy_exists()
#// @see taxonomy_exists()
#// 
#// @param string $taxonomy Name of taxonomy object
#// @return bool Whether the taxonomy exists.
#//
def is_taxonomy(taxonomy_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.0.0", "taxonomy_exists()")
    return taxonomy_exists(taxonomy_)
# end def is_taxonomy
#// 
#// Check if Term exists.
#// 
#// @since 2.3.0
#// @deprecated 3.0.0 Use term_exists()
#// @see term_exists()
#// 
#// @param int|string $term The term to check
#// @param string $taxonomy The taxonomy name to use
#// @param int $parent ID of parent term under which to confine the exists search.
#// @return mixed Get the term id or Term Object, if exists.
#//
def is_term(term_=None, taxonomy_="", parent_=0, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.0.0", "term_exists()")
    return term_exists(term_, taxonomy_, parent_)
# end def is_term
#// 
#// Determines whether the current admin page is generated by a plugin.
#// 
#// Use global $plugin_page and/or get_plugin_page_hookname() hooks.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 1.5.0
#// @deprecated 3.1.0
#// 
#// @global $plugin_page
#// 
#// @return bool
#//
def is_plugin_page(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.1.0")
    global plugin_page_
    php_check_if_defined("plugin_page_")
    if (php_isset(lambda : plugin_page_)):
        return True
    # end if
    return False
# end def is_plugin_page
#// 
#// Update the categories cache.
#// 
#// This function does not appear to be used anymore or does not appear to be
#// needed. It might be a legacy function left over from when there was a need
#// for updating the category cache.
#// 
#// @since 1.5.0
#// @deprecated 3.1.0
#// 
#// @return bool Always return True
#//
def update_category_cache(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.1.0")
    return True
# end def update_category_cache
#// 
#// Check for PHP timezone support
#// 
#// @since 2.9.0
#// @deprecated 3.2.0
#// 
#// @return bool
#//
def wp_timezone_supported(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.2.0")
    return True
# end def wp_timezone_supported
#// 
#// Displays an editor: TinyMCE, HTML, or both.
#// 
#// @since 2.1.0
#// @deprecated 3.3.0 Use wp_editor()
#// @see wp_editor()
#// 
#// @param string $content       Textarea content.
#// @param string $id            Optional. HTML ID attribute value. Default 'content'.
#// @param string $prev_id       Optional. Unused.
#// @param bool   $media_buttons Optional. Whether to display media buttons. Default true.
#// @param int    $tab_index     Optional. Unused.
#// @param bool   $extended      Optional. Unused.
#//
def the_editor(content_=None, id_="content", prev_id_="title", media_buttons_=None, tab_index_=2, extended_=None, *_args_):
    if media_buttons_ is None:
        media_buttons_ = True
    # end if
    if extended_ is None:
        extended_ = True
    # end if
    
    _deprecated_function(__FUNCTION__, "3.3.0", "wp_editor()")
    wp_editor(content_, id_, Array({"media_buttons": media_buttons_}))
# end def the_editor
#// 
#// Perform the query to get the $metavalues array(s) needed by _fill_user and _fill_many_users
#// 
#// @since 3.0.0
#// @deprecated 3.3.0
#// 
#// @param array $ids User ID numbers list.
#// @return array of arrays. The array is indexed by user_id, containing $metavalues object arrays.
#//
def get_user_metavalues(ids_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.3.0")
    objects_ = Array()
    ids_ = php_array_map("intval", ids_)
    for id_ in ids_:
        objects_[id_] = Array()
    # end for
    metas_ = update_meta_cache("user", ids_)
    for id_,meta_ in metas_.items():
        for key_,metavalues_ in meta_.items():
            for value_ in metavalues_:
                objects_[id_][-1] = Array({"user_id": id_, "meta_key": key_, "meta_value": value_})
            # end for
        # end for
    # end for
    return objects_
# end def get_user_metavalues
#// 
#// Sanitize every user field.
#// 
#// If the context is 'raw', then the user object or array will get minimal santization of the int fields.
#// 
#// @since 2.3.0
#// @deprecated 3.3.0
#// 
#// @param object|array $user The User Object or Array
#// @param string $context Optional, default is 'display'. How to sanitize user fields.
#// @return object|array The now sanitized User Object or Array (will be the same type as $user)
#//
def sanitize_user_object(user_=None, context_="display", *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.3.0")
    if php_is_object(user_):
        if (not (php_isset(lambda : user_.ID))):
            user_.ID = 0
        # end if
        if (not type(user_).__name__ == "WP_User"):
            vars_ = get_object_vars(user_)
            for field_ in php_array_keys(vars_):
                if php_is_string(user_.field_) or php_is_numeric(user_.field_):
                    user_.field_ = sanitize_user_field(field_, user_.field_, user_.ID, context_)
                # end if
            # end for
        # end if
        user_.filter = context_
    else:
        if (not (php_isset(lambda : user_["ID"]))):
            user_["ID"] = 0
        # end if
        for field_ in php_array_keys(user_):
            user_[field_] = sanitize_user_field(field_, user_[field_], user_["ID"], context_)
        # end for
        user_["filter"] = context_
    # end if
    return user_
# end def sanitize_user_object
#// 
#// Get boundary post relational link.
#// 
#// Can either be start or end post relational link.
#// 
#// @since 2.8.0
#// @deprecated 3.3.0
#// 
#// @param string $title Optional. Link title format.
#// @param bool $in_same_cat Optional. Whether link should be in a same category.
#// @param string $excluded_categories Optional. Excluded categories IDs.
#// @param bool $start Optional, default is true. Whether to display link to first or last post.
#// @return string
#//
def get_boundary_post_rel_link(title_="%title", in_same_cat_=None, excluded_categories_="", start_=None, *_args_):
    if in_same_cat_ is None:
        in_same_cat_ = False
    # end if
    if start_ is None:
        start_ = True
    # end if
    
    _deprecated_function(__FUNCTION__, "3.3.0")
    posts_ = get_boundary_post(in_same_cat_, excluded_categories_, start_)
    #// If there is no post, stop.
    if php_empty(lambda : posts_):
        return
    # end if
    #// Even though we limited get_posts() to return only 1 item it still returns an array of objects.
    post_ = posts_[0]
    if php_empty(lambda : post_.post_title):
        post_.post_title = __("First Post") if start_ else __("Last Post")
    # end if
    date_ = mysql2date(get_option("date_format"), post_.post_date)
    title_ = php_str_replace("%title", post_.post_title, title_)
    title_ = php_str_replace("%date", date_, title_)
    title_ = apply_filters("the_title", title_, post_.ID)
    link_ = "<link rel='start' title='" if start_ else "<link rel='end' title='"
    link_ += esc_attr(title_)
    link_ += "' href='" + get_permalink(post_) + "' />\n"
    boundary_ = "start" if start_ else "end"
    return apply_filters(str(boundary_) + str("_post_rel_link"), link_)
# end def get_boundary_post_rel_link
#// 
#// Display relational link for the first post.
#// 
#// @since 2.8.0
#// @deprecated 3.3.0
#// 
#// @param string $title Optional. Link title format.
#// @param bool $in_same_cat Optional. Whether link should be in a same category.
#// @param string $excluded_categories Optional. Excluded categories IDs.
#//
def start_post_rel_link(title_="%title", in_same_cat_=None, excluded_categories_="", *_args_):
    if in_same_cat_ is None:
        in_same_cat_ = False
    # end if
    
    _deprecated_function(__FUNCTION__, "3.3.0")
    php_print(get_boundary_post_rel_link(title_, in_same_cat_, excluded_categories_, True))
# end def start_post_rel_link
#// 
#// Get site index relational link.
#// 
#// @since 2.8.0
#// @deprecated 3.3.0
#// 
#// @return string
#//
def get_index_rel_link(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.3.0")
    link_ = "<link rel='index' title='" + esc_attr(get_bloginfo("name", "display")) + "' href='" + esc_url(user_trailingslashit(get_bloginfo("url", "display"))) + "' />\n"
    return apply_filters("index_rel_link", link_)
# end def get_index_rel_link
#// 
#// Display relational link for the site index.
#// 
#// @since 2.8.0
#// @deprecated 3.3.0
#//
def index_rel_link(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.3.0")
    php_print(get_index_rel_link())
# end def index_rel_link
#// 
#// Get parent post relational link.
#// 
#// @since 2.8.0
#// @deprecated 3.3.0
#// 
#// @param string $title Optional. Link title format. Default '%title'.
#// @return string
#//
def get_parent_post_rel_link(title_="%title", *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.3.0")
    if (not php_empty(lambda : PHP_GLOBALS["post"])) and (not php_empty(lambda : PHP_GLOBALS["post"].post_parent)):
        post_ = get_post(PHP_GLOBALS["post"].post_parent)
    # end if
    if php_empty(lambda : post_):
        return
    # end if
    date_ = mysql2date(get_option("date_format"), post_.post_date)
    title_ = php_str_replace("%title", post_.post_title, title_)
    title_ = php_str_replace("%date", date_, title_)
    title_ = apply_filters("the_title", title_, post_.ID)
    link_ = "<link rel='up' title='"
    link_ += esc_attr(title_)
    link_ += "' href='" + get_permalink(post_) + "' />\n"
    return apply_filters("parent_post_rel_link", link_)
# end def get_parent_post_rel_link
#// 
#// Display relational link for parent item
#// 
#// @since 2.8.0
#// @deprecated 3.3.0
#// 
#// @param string $title Optional. Link title format. Default '%title'.
#//
def parent_post_rel_link(title_="%title", *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.3.0")
    php_print(get_parent_post_rel_link(title_))
# end def parent_post_rel_link
#// 
#// Add the "Dashboard"/"Visit Site" menu.
#// 
#// @since 3.2.0
#// @deprecated 3.3.0
#// 
#// @param WP_Admin_Bar $wp_admin_bar WP_Admin_Bar instance.
#//
def wp_admin_bar_dashboard_view_site_menu(wp_admin_bar_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.3.0")
    user_id_ = get_current_user_id()
    if 0 != user_id_:
        if is_admin():
            wp_admin_bar_.add_menu(Array({"id": "view-site", "title": __("Visit Site"), "href": home_url()}))
        elif is_multisite():
            wp_admin_bar_.add_menu(Array({"id": "dashboard", "title": __("Dashboard"), "href": get_dashboard_url(user_id_)}))
        else:
            wp_admin_bar_.add_menu(Array({"id": "dashboard", "title": __("Dashboard"), "href": admin_url()}))
        # end if
    # end if
# end def wp_admin_bar_dashboard_view_site_menu
#// 
#// Checks if the current user belong to a given site.
#// 
#// @since MU (3.0.0)
#// @deprecated 3.3.0 Use is_user_member_of_blog()
#// @see is_user_member_of_blog()
#// 
#// @param int $blog_id Site ID
#// @return bool True if the current users belong to $blog_id, false if not.
#//
def is_blog_user(blog_id_=0, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.3.0", "is_user_member_of_blog()")
    return is_user_member_of_blog(get_current_user_id(), blog_id_)
# end def is_blog_user
#// 
#// Open the file handle for debugging.
#// 
#// @since 0.71
#// @deprecated 3.4.0 Use error_log()
#// @see error_log()
#// 
#// @link https://www.php.net/manual/en/function.error-log.php
#// 
#// @param string $filename File name.
#// @param string $mode     Type of access you required to the stream.
#// @return false Always false.
#//
def debug_fopen(filename_=None, mode_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.4.0", "error_log()")
    return False
# end def debug_fopen
#// 
#// Write contents to the file used for debugging.
#// 
#// @since 0.71
#// @deprecated 3.4.0 Use error_log()
#// @see error_log()
#// 
#// @link https://www.php.net/manual/en/function.error-log.php
#// 
#// @param mixed  $fp     Unused.
#// @param string $string Message to log.
#//
def debug_fwrite(fp_=None, string_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.4.0", "error_log()")
    if (not php_empty(lambda : PHP_GLOBALS["debug"])):
        php_error_log(string_)
    # end if
# end def debug_fwrite
#// 
#// Close the debugging file handle.
#// 
#// @since 0.71
#// @deprecated 3.4.0 Use error_log()
#// @see error_log()
#// 
#// @link https://www.php.net/manual/en/function.error-log.php
#// 
#// @param mixed $fp Unused.
#//
def debug_fclose(fp_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.4.0", "error_log()")
# end def debug_fclose
#// 
#// Retrieve list of themes with theme data in theme directory.
#// 
#// The theme is broken, if it doesn't have a parent theme and is missing either
#// style.css and, or index.php. If the theme has a parent theme then it is
#// broken, if it is missing style.css; index.php is optional.
#// 
#// @since 1.5.0
#// @deprecated 3.4.0 Use wp_get_themes()
#// @see wp_get_themes()
#// 
#// @return array Theme list with theme data.
#//
def get_themes(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.4.0", "wp_get_themes()")
    global wp_themes_
    php_check_if_defined("wp_themes_")
    if (php_isset(lambda : wp_themes_)):
        return wp_themes_
    # end if
    themes_ = wp_get_themes()
    wp_themes_ = Array()
    for theme_ in themes_:
        name_ = theme_.get("Name")
        if (php_isset(lambda : wp_themes_[name_])):
            wp_themes_[name_ + "/" + theme_.get_stylesheet()] = theme_
        else:
            wp_themes_[name_] = theme_
        # end if
    # end for
    return wp_themes_
# end def get_themes
#// 
#// Retrieve theme data.
#// 
#// @since 1.5.0
#// @deprecated 3.4.0 Use wp_get_theme()
#// @see wp_get_theme()
#// 
#// @param string $theme Theme name.
#// @return array|null Null, if theme name does not exist. Theme data, if exists.
#//
def get_theme(theme_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.4.0", "wp_get_theme( $stylesheet )")
    themes_ = get_themes()
    if php_is_array(themes_) and php_array_key_exists(theme_, themes_):
        return themes_[theme_]
    # end if
    return None
# end def get_theme
#// 
#// Retrieve current theme name.
#// 
#// @since 1.5.0
#// @deprecated 3.4.0 Use wp_get_theme()
#// @see wp_get_theme()
#// 
#// @return string
#//
def get_current_theme(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.4.0", "wp_get_theme()")
    theme_ = get_option("current_theme")
    if theme_:
        return theme_
    # end if
    return wp_get_theme().get("Name")
# end def get_current_theme
#// 
#// Accepts matches array from preg_replace_callback in wpautop() or a string.
#// 
#// Ensures that the contents of a `<pre>...</pre>` HTML block are not
#// converted into paragraphs or line-breaks.
#// 
#// @since 1.2.0
#// @deprecated 3.4.0
#// 
#// @param array|string $matches The array or string
#// @return string The pre block without paragraph/line-break conversion.
#//
def clean_pre(matches_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.4.0")
    if php_is_array(matches_):
        text_ = matches_[1] + matches_[2] + "</pre>"
    else:
        text_ = matches_
    # end if
    text_ = php_str_replace(Array("<br />", "<br/>", "<br>"), Array("", "", ""), text_)
    text_ = php_str_replace("<p>", "\n", text_)
    text_ = php_str_replace("</p>", "", text_)
    return text_
# end def clean_pre
#// 
#// Add callbacks for image header display.
#// 
#// @since 2.1.0
#// @deprecated 3.4.0 Use add_theme_support()
#// @see add_theme_support()
#// 
#// @param callable $wp_head_callback Call on the {@see 'wp_head'} action.
#// @param callable $admin_head_callback Call on custom header administration screen.
#// @param callable $admin_preview_callback Output a custom header image div on the custom header administration screen. Optional.
#//
def add_custom_image_header(wp_head_callback_=None, admin_head_callback_=None, admin_preview_callback_="", *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.4.0", "add_theme_support( 'custom-header', $args )")
    args_ = Array({"wp-head-callback": wp_head_callback_, "admin-head-callback": admin_head_callback_})
    if admin_preview_callback_:
        args_["admin-preview-callback"] = admin_preview_callback_
    # end if
    return add_theme_support("custom-header", args_)
# end def add_custom_image_header
#// 
#// Remove image header support.
#// 
#// @since 3.1.0
#// @deprecated 3.4.0 Use remove_theme_support()
#// @see remove_theme_support()
#// 
#// @return null|bool Whether support was removed.
#//
def remove_custom_image_header(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.4.0", "remove_theme_support( 'custom-header' )")
    return remove_theme_support("custom-header")
# end def remove_custom_image_header
#// 
#// Add callbacks for background image display.
#// 
#// @since 3.0.0
#// @deprecated 3.4.0 Use add_theme_support()
#// @see add_theme_support()
#// 
#// @param callable $wp_head_callback Call on the {@see 'wp_head'} action.
#// @param callable $admin_head_callback Call on custom background administration screen.
#// @param callable $admin_preview_callback Output a custom background image div on the custom background administration screen. Optional.
#//
def add_custom_background(wp_head_callback_="", admin_head_callback_="", admin_preview_callback_="", *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.4.0", "add_theme_support( 'custom-background', $args )")
    args_ = Array()
    if wp_head_callback_:
        args_["wp-head-callback"] = wp_head_callback_
    # end if
    if admin_head_callback_:
        args_["admin-head-callback"] = admin_head_callback_
    # end if
    if admin_preview_callback_:
        args_["admin-preview-callback"] = admin_preview_callback_
    # end if
    return add_theme_support("custom-background", args_)
# end def add_custom_background
#// 
#// Remove custom background support.
#// 
#// @since 3.1.0
#// @deprecated 3.4.0 Use add_custom_background()
#// @see add_custom_background()
#// 
#// @return null|bool Whether support was removed.
#//
def remove_custom_background(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.4.0", "remove_theme_support( 'custom-background' )")
    return remove_theme_support("custom-background")
# end def remove_custom_background
#// 
#// Retrieve theme data from parsed theme file.
#// 
#// @since 1.5.0
#// @deprecated 3.4.0 Use wp_get_theme()
#// @see wp_get_theme()
#// 
#// @param string $theme_file Theme file path.
#// @return array Theme data.
#//
def get_theme_data(theme_file_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.4.0", "wp_get_theme()")
    theme_ = php_new_class("WP_Theme", lambda : WP_Theme(wp_basename(php_dirname(theme_file_)), php_dirname(php_dirname(theme_file_))))
    theme_data_ = Array({"Name": theme_.get("Name"), "URI": theme_.display("ThemeURI", True, False), "Description": theme_.display("Description", True, False), "Author": theme_.display("Author", True, False), "AuthorURI": theme_.display("AuthorURI", True, False), "Version": theme_.get("Version"), "Template": theme_.get("Template"), "Status": theme_.get("Status"), "Tags": theme_.get("Tags"), "Title": theme_.get("Name"), "AuthorName": theme_.get("Author")})
    for extra_header_ in apply_filters("extra_theme_headers", Array()):
        if (not (php_isset(lambda : theme_data_[extra_header_]))):
            theme_data_[extra_header_] = theme_.get(extra_header_)
        # end if
    # end for
    return theme_data_
# end def get_theme_data
#// 
#// Alias of update_post_cache().
#// 
#// @see update_post_cache() Posts and pages are the same, alias is intentional
#// 
#// @since 1.5.1
#// @deprecated 3.4.0 Use update_post_cache()
#// @see update_post_cache()
#// 
#// @param array $pages list of page objects
#//
def update_page_cache(pages_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.4.0", "update_post_cache()")
    update_post_cache(pages_)
# end def update_page_cache
#// 
#// Will clean the page in the cache.
#// 
#// Clean (read: delete) page from cache that matches $id. Will also clean cache
#// associated with 'all_page_ids' and 'get_pages'.
#// 
#// @since 2.0.0
#// @deprecated 3.4.0 Use clean_post_cache
#// @see clean_post_cache()
#// 
#// @param int $id Page ID to clean
#//
def clean_page_cache(id_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.4.0", "clean_post_cache()")
    clean_post_cache(id_)
# end def clean_page_cache
#// 
#// Retrieve nonce action "Are you sure" message.
#// 
#// Deprecated in 3.4.1 and 3.5.0. Backported to 3.3.3.
#// 
#// @since 2.0.4
#// @deprecated 3.4.1 Use wp_nonce_ays()
#// @see wp_nonce_ays()
#// 
#// @param string $action Nonce action.
#// @return string Are you sure message.
#//
def wp_explain_nonce(action_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.4.1", "wp_nonce_ays()")
    return __("Are you sure you want to do this?")
# end def wp_explain_nonce
#// 
#// Display "sticky" CSS class, if a post is sticky.
#// 
#// @since 2.7.0
#// @deprecated 3.5.0 Use post_class()
#// @see post_class()
#// 
#// @param int $post_id An optional post ID.
#//
def sticky_class(post_id_=None, *_args_):
    if post_id_ is None:
        post_id_ = None
    # end if
    
    _deprecated_function(__FUNCTION__, "3.5.0", "post_class()")
    if is_sticky(post_id_):
        php_print(" sticky")
    # end if
# end def sticky_class
#// 
#// Retrieve post ancestors.
#// 
#// This is no longer needed as WP_Post lazy-loads the ancestors
#// property with get_post_ancestors().
#// 
#// @since 2.3.4
#// @deprecated 3.5.0 Use get_post_ancestors()
#// @see get_post_ancestors()
#// 
#// @param WP_Post $post Post object, passed by reference (unused).
#//
def _get_post_ancestors(post_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.5.0")
# end def _get_post_ancestors
#// 
#// Load an image from a string, if PHP supports it.
#// 
#// @since 2.1.0
#// @deprecated 3.5.0 Use wp_get_image_editor()
#// @see wp_get_image_editor()
#// 
#// @param string $file Filename of the image to load.
#// @return resource The resulting image resource on success, Error string on failure.
#//
def wp_load_image(file_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.5.0", "wp_get_image_editor()")
    if php_is_numeric(file_):
        file_ = get_attached_file(file_)
    # end if
    if (not php_is_file(file_)):
        #// translators: %s: File name.
        return php_sprintf(__("File &#8220;%s&#8221; doesn&#8217;t exist?"), file_)
    # end if
    if (not php_function_exists("imagecreatefromstring")):
        return __("The GD image library is not installed.")
    # end if
    #// Set artificially high because GD uses uncompressed images in memory.
    wp_raise_memory_limit("image")
    image_ = imagecreatefromstring(php_file_get_contents(file_))
    if (not php_is_resource(image_)):
        #// translators: %s: File name.
        return php_sprintf(__("File &#8220;%s&#8221; is not an image."), file_)
    # end if
    return image_
# end def wp_load_image
#// 
#// Scale down an image to fit a particular size and save a new copy of the image.
#// 
#// The PNG transparency will be preserved using the function, as well as the
#// image type. If the file going in is PNG, then the resized image is going to
#// be PNG. The only supported image types are PNG, GIF, and JPEG.
#// 
#// Some functionality requires API to exist, so some PHP version may lose out
#// support. This is not the fault of WordPress (where functionality is
#// downgraded, not actual defects), but of your PHP version.
#// 
#// @since 2.5.0
#// @deprecated 3.5.0 Use wp_get_image_editor()
#// @see wp_get_image_editor()
#// 
#// @param string $file Image file path.
#// @param int $max_w Maximum width to resize to.
#// @param int $max_h Maximum height to resize to.
#// @param bool $crop Optional. Whether to crop image or resize.
#// @param string $suffix Optional. File suffix.
#// @param string $dest_path Optional. New image file path.
#// @param int $jpeg_quality Optional, default is 90. Image quality percentage.
#// @return mixed WP_Error on failure. String with new destination path.
#//
def image_resize(file_=None, max_w_=None, max_h_=None, crop_=None, suffix_=None, dest_path_=None, jpeg_quality_=90, *_args_):
    if crop_ is None:
        crop_ = False
    # end if
    if suffix_ is None:
        suffix_ = None
    # end if
    if dest_path_ is None:
        dest_path_ = None
    # end if
    
    _deprecated_function(__FUNCTION__, "3.5.0", "wp_get_image_editor()")
    editor_ = wp_get_image_editor(file_)
    if is_wp_error(editor_):
        return editor_
    # end if
    editor_.set_quality(jpeg_quality_)
    resized_ = editor_.resize(max_w_, max_h_, crop_)
    if is_wp_error(resized_):
        return resized_
    # end if
    dest_file_ = editor_.generate_filename(suffix_, dest_path_)
    saved_ = editor_.save(dest_file_)
    if is_wp_error(saved_):
        return saved_
    # end if
    return dest_file_
# end def image_resize
#// 
#// Retrieve a single post, based on post ID.
#// 
#// Has categories in 'post_category' property or key. Has tags in 'tags_input'
#// property or key.
#// 
#// @since 1.0.0
#// @deprecated 3.5.0 Use get_post()
#// @see get_post()
#// 
#// @param int $postid Post ID.
#// @param string $mode How to return result, either OBJECT, ARRAY_N, or ARRAY_A.
#// @return WP_Post|null Post object or array holding post contents and information
#//
def wp_get_single_post(postid_=0, mode_=None, *_args_):
    if mode_ is None:
        mode_ = OBJECT
    # end if
    
    _deprecated_function(__FUNCTION__, "3.5.0", "get_post()")
    return get_post(postid_, mode_)
# end def wp_get_single_post
#// 
#// Check that the user login name and password is correct.
#// 
#// @since 0.71
#// @deprecated 3.5.0 Use wp_authenticate()
#// @see wp_authenticate()
#// 
#// @param string $user_login User name.
#// @param string $user_pass User password.
#// @return bool False if does not authenticate, true if username and password authenticates.
#//
def user_pass_ok(user_login_=None, user_pass_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.5.0", "wp_authenticate()")
    user_ = wp_authenticate(user_login_, user_pass_)
    if is_wp_error(user_):
        return False
    # end if
    return True
# end def user_pass_ok
#// 
#// Callback formerly fired on the save_post hook. No longer needed.
#// 
#// @since 2.3.0
#// @deprecated 3.5.0
#//
def _save_post_hook(*_args_):
    
    
    pass
# end def _save_post_hook
#// 
#// Check if the installed version of GD supports particular image type
#// 
#// @since 2.9.0
#// @deprecated 3.5.0 Use wp_image_editor_supports()
#// @see wp_image_editor_supports()
#// 
#// @param string $mime_type
#// @return bool
#//
def gd_edit_image_support(mime_type_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.5.0", "wp_image_editor_supports()")
    if php_function_exists("imagetypes"):
        for case in Switch(mime_type_):
            if case("image/jpeg"):
                return imagetypes() & IMG_JPG != 0
            # end if
            if case("image/png"):
                return imagetypes() & IMG_PNG != 0
            # end if
            if case("image/gif"):
                return imagetypes() & IMG_GIF != 0
            # end if
        # end for
    else:
        for case in Switch(mime_type_):
            if case("image/jpeg"):
                return php_function_exists("imagecreatefromjpeg")
            # end if
            if case("image/png"):
                return php_function_exists("imagecreatefrompng")
            # end if
            if case("image/gif"):
                return php_function_exists("imagecreatefromgif")
            # end if
        # end for
    # end if
    return False
# end def gd_edit_image_support
#// 
#// Converts an integer byte value to a shorthand byte value.
#// 
#// @since 2.3.0
#// @deprecated 3.6.0 Use size_format()
#// @see size_format()
#// 
#// @param int $bytes An integer byte value.
#// @return string A shorthand byte value.
#//
def wp_convert_bytes_to_hr(bytes_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.6.0", "size_format()")
    units_ = Array({0: "B", 1: "KB", 2: "MB", 3: "GB", 4: "TB"})
    log_ = log(bytes_, KB_IN_BYTES)
    power_ = php_int(log_)
    size_ = KB_IN_BYTES ^ log_ - power_
    if (not is_nan(size_)) and php_array_key_exists(power_, units_):
        unit_ = units_[power_]
    else:
        size_ = bytes_
        unit_ = units_[0]
    # end if
    return size_ + unit_
# end def wp_convert_bytes_to_hr
#// 
#// Formerly used internally to tidy up the search terms.
#// 
#// @since 2.9.0
#// @access private
#// @deprecated 3.7.0
#// 
#// @param string $t Search terms to "tidy", e.g. trim.
#// @return string Trimmed search terms.
#//
def _search_terms_tidy(t_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.7.0")
    return php_trim(t_, "\"'\n\r ")
# end def _search_terms_tidy
#// 
#// Determine if TinyMCE is available.
#// 
#// Checks to see if the user has deleted the tinymce files to slim down
#// their WordPress installation.
#// 
#// @since 2.1.0
#// @deprecated 3.9.0
#// 
#// @return bool Whether TinyMCE exists.
#//
def rich_edit_exists(*_args_):
    
    
    global wp_rich_edit_exists_
    php_check_if_defined("wp_rich_edit_exists_")
    _deprecated_function(__FUNCTION__, "3.9.0")
    if (not (php_isset(lambda : wp_rich_edit_exists_))):
        wp_rich_edit_exists_ = php_file_exists(ABSPATH + WPINC + "/js/tinymce/tinymce.js")
    # end if
    return wp_rich_edit_exists_
# end def rich_edit_exists
#// 
#// Old callback for tag link tooltips.
#// 
#// @since 2.7.0
#// @access private
#// @deprecated 3.9.0
#// 
#// @param int $count Number of topics.
#// @return int Number of topics.
#//
def default_topic_count_text(count_=None, *_args_):
    
    
    return count_
# end def default_topic_count_text
#// 
#// Formerly used to escape strings before inserting into the DB.
#// 
#// Has not performed this function for many, many years. Use wpdb::prepare() instead.
#// 
#// @since 0.71
#// @deprecated 3.9.0
#// 
#// @param string $content The text to format.
#// @return string The very same text.
#//
def format_to_post(content_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "3.9.0")
    return content_
# end def format_to_post
#// 
#// Formerly used to escape strings before searching the DB. It was poorly documented and never worked as described.
#// 
#// @since 2.5.0
#// @deprecated 4.0.0 Use wpdb::esc_like()
#// @see wpdb::esc_like()
#// 
#// @param string $text The text to be escaped.
#// @return string text, safe for inclusion in LIKE query.
#//
def like_escape(text_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "4.0.0", "wpdb::esc_like()")
    return php_str_replace(Array("%", "_"), Array("\\%", "\\_"), text_)
# end def like_escape
#// 
#// Determines if the URL can be accessed over SSL.
#// 
#// Determines if the URL can be accessed over SSL by using the WordPress HTTP API to access
#// the URL using https as the scheme.
#// 
#// @since 2.5.0
#// @deprecated 4.0.0
#// 
#// @param string $url The URL to test.
#// @return bool Whether SSL access is available.
#//
def url_is_accessable_via_ssl(url_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "4.0.0")
    response_ = wp_remote_get(set_url_scheme(url_, "https"))
    if (not is_wp_error(response_)):
        status_ = wp_remote_retrieve_response_code(response_)
        if 200 == status_ or 401 == status_:
            return True
        # end if
    # end if
    return False
# end def url_is_accessable_via_ssl
#// 
#// Start preview theme output buffer.
#// 
#// Will only perform task if the user has permissions and template and preview
#// query variables exist.
#// 
#// @since 2.6.0
#// @deprecated 4.3.0
#//
def preview_theme(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "4.3.0")
# end def preview_theme
#// 
#// Private function to modify the current template when previewing a theme
#// 
#// @since 2.9.0
#// @deprecated 4.3.0
#// @access private
#// 
#// @return string
#//
def _preview_theme_template_filter(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "4.3.0")
    return ""
# end def _preview_theme_template_filter
#// 
#// Private function to modify the current stylesheet when previewing a theme
#// 
#// @since 2.9.0
#// @deprecated 4.3.0
#// @access private
#// 
#// @return string
#//
def _preview_theme_stylesheet_filter(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "4.3.0")
    return ""
# end def _preview_theme_stylesheet_filter
#// 
#// Callback function for ob_start() to capture all links in the theme.
#// 
#// @since 2.6.0
#// @deprecated 4.3.0
#// @access private
#// 
#// @param string $content
#// @return string
#//
def preview_theme_ob_filter(content_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "4.3.0")
    return content_
# end def preview_theme_ob_filter
#// 
#// Manipulates preview theme links in order to control and maintain location.
#// 
#// Callback function for preg_replace_callback() to accept and filter matches.
#// 
#// @since 2.6.0
#// @deprecated 4.3.0
#// @access private
#// 
#// @param array $matches
#// @return string
#//
def preview_theme_ob_filter_callback(matches_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "4.3.0")
    return ""
# end def preview_theme_ob_filter_callback
#// 
#// Formats text for the rich text editor.
#// 
#// The {@see 'richedit_pre'} filter is applied here. If $text is empty the filter will
#// be applied to an empty string.
#// 
#// @since 2.0.0
#// @deprecated 4.3.0 Use format_for_editor()
#// @see format_for_editor()
#// 
#// @param string $text The text to be formatted.
#// @return string The formatted text after filter is applied.
#//
def wp_richedit_pre(text_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "4.3.0", "format_for_editor()")
    if php_empty(lambda : text_):
        #// 
        #// Filters text returned for the rich text editor.
        #// 
        #// This filter is first evaluated, and the value returned, if an empty string
        #// is passed to wp_richedit_pre(). If an empty string is passed, it results
        #// in a break tag and line feed.
        #// 
        #// If a non-empty string is passed, the filter is evaluated on the wp_richedit_pre()
        #// return after being formatted.
        #// 
        #// @since 2.0.0
        #// @deprecated 4.3.0
        #// 
        #// @param string $output Text for the rich text editor.
        #//
        return apply_filters("richedit_pre", "")
    # end if
    output_ = convert_chars(text_)
    output_ = wpautop(output_)
    output_ = htmlspecialchars(output_, ENT_NOQUOTES, get_option("blog_charset"))
    #// This filter is documented in wp-includes/deprecated.php
    return apply_filters("richedit_pre", output_)
# end def wp_richedit_pre
#// 
#// Formats text for the HTML editor.
#// 
#// Unless $output is empty it will pass through htmlspecialchars before the
#// {@see 'htmledit_pre'} filter is applied.
#// 
#// @since 2.5.0
#// @deprecated 4.3.0 Use format_for_editor()
#// @see format_for_editor()
#// 
#// @param string $output The text to be formatted.
#// @return string Formatted text after filter applied.
#//
def wp_htmledit_pre(output_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "4.3.0", "format_for_editor()")
    if (not php_empty(lambda : output_)):
        output_ = htmlspecialchars(output_, ENT_NOQUOTES, get_option("blog_charset"))
    # end if
    #// Convert only '< > &'.
    #// 
    #// Filters the text before it is formatted for the HTML editor.
    #// 
    #// @since 2.5.0
    #// @deprecated 4.3.0
    #// 
    #// @param string $output The HTML-formatted text.
    #//
    return apply_filters("htmledit_pre", output_)
# end def wp_htmledit_pre
#// 
#// Retrieve permalink from post ID.
#// 
#// @since 1.0.0
#// @deprecated 4.4.0 Use get_permalink()
#// @see get_permalink()
#// 
#// @param int|WP_Post $post_id Optional. Post ID or WP_Post object. Default is global $post.
#// @return string|false
#//
def post_permalink(post_id_=0, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "4.4.0", "get_permalink()")
    return get_permalink(post_id_)
# end def post_permalink
#// 
#// Perform a HTTP HEAD or GET request.
#// 
#// If $file_path is a writable filename, this will do a GET request and write
#// the file to that path.
#// 
#// @since 2.5.0
#// @deprecated 4.4.0 Use WP_Http
#// @see WP_Http
#// 
#// @param string      $url       URL to fetch.
#// @param string|bool $file_path Optional. File path to write request to. Default false.
#// @param int         $red       Optional. The number of Redirects followed, Upon 5 being hit,
#// returns false. Default 1.
#// @return bool|string False on failure and string of headers if HEAD request.
#//
def wp_get_http(url_=None, file_path_=None, red_=1, *_args_):
    if file_path_ is None:
        file_path_ = False
    # end if
    
    _deprecated_function(__FUNCTION__, "4.4.0", "WP_Http")
    php_no_error(lambda: set_time_limit(60))
    if red_ > 5:
        return False
    # end if
    options_ = Array()
    options_["redirection"] = 5
    if False == file_path_:
        options_["method"] = "HEAD"
    else:
        options_["method"] = "GET"
    # end if
    response_ = wp_safe_remote_request(url_, options_)
    if is_wp_error(response_):
        return False
    # end if
    headers_ = wp_remote_retrieve_headers(response_)
    headers_["response"] = wp_remote_retrieve_response_code(response_)
    #// WP_HTTP no longer follows redirects for HEAD requests.
    if "HEAD" == options_["method"] and php_in_array(headers_["response"], Array(301, 302)) and (php_isset(lambda : headers_["location"])):
        red_ += 1
        red_ += 1
        return wp_get_http(headers_["location"], file_path_, red_)
    # end if
    if False == file_path_:
        return headers_
    # end if
    #// GET request - write it to the supplied filename.
    out_fp_ = fopen(file_path_, "w")
    if (not out_fp_):
        return headers_
    # end if
    fwrite(out_fp_, wp_remote_retrieve_body(response_))
    php_fclose(out_fp_)
    clearstatcache()
    return headers_
# end def wp_get_http
#// 
#// Whether SSL login should be forced.
#// 
#// @since 2.6.0
#// @deprecated 4.4.0 Use force_ssl_admin()
#// @see force_ssl_admin()
#// 
#// @param string|bool $force Optional Whether to force SSL login. Default null.
#// @return bool True if forced, false if not forced.
#//
def force_ssl_login(force_=None, *_args_):
    if force_ is None:
        force_ = None
    # end if
    
    _deprecated_function(__FUNCTION__, "4.4.0", "force_ssl_admin()")
    return force_ssl_admin(force_)
# end def force_ssl_login
#// 
#// Retrieve path of comment popup template in current or parent template.
#// 
#// @since 1.5.0
#// @deprecated 4.5.0
#// 
#// @return string Full path to comments popup template file.
#//
def get_comments_popup_template(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "4.5.0")
    return ""
# end def get_comments_popup_template
#// 
#// Determines whether the current URL is within the comments popup window.
#// 
#// For more information on this and similar theme functions, check out
#// the {@link https://developer.wordpress.org/themes/basics/conditional-tags
#// Conditional Tags} article in the Theme Developer Handbook.
#// 
#// @since 1.5.0
#// @deprecated 4.5.0
#// 
#// @return bool
#//
def is_comments_popup(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "4.5.0")
    return False
# end def is_comments_popup
#// 
#// Display the JS popup script to show a comment.
#// 
#// @since 0.71
#// @deprecated 4.5.0
#//
def comments_popup_script(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "4.5.0")
# end def comments_popup_script
#// 
#// Adds element attributes to open links in new tabs.
#// 
#// @since 0.71
#// @deprecated 4.5.0
#// 
#// @param string $text Content to replace links to open in a new tab.
#// @return string Content that has filtered links.
#//
def popuplinks(text_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "4.5.0")
    text_ = php_preg_replace("/<a (.+?)>/i", "<a $1 target='_blank' rel='external'>", text_)
    return text_
# end def popuplinks
#// 
#// The Google Video embed handler callback.
#// 
#// Deprecated function that previously assisted in turning Google Video URLs
#// into embeds but that service has since been shut down.
#// 
#// @since 2.9.0
#// @deprecated 4.6.0
#// 
#// @return string An empty string.
#//
def wp_embed_handler_googlevideo(matches_=None, attr_=None, url_=None, rawattr_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "4.6.0")
    return ""
# end def wp_embed_handler_googlevideo
#// 
#// Retrieve path of paged template in current or parent template.
#// 
#// @since 1.5.0
#// @deprecated 4.7.0 The paged.php template is no longer part of the theme template hierarchy.
#// 
#// @return string Full path to paged template file.
#//
def get_paged_template(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "4.7.0")
    return get_query_template("paged")
# end def get_paged_template
#// 
#// Removes the HTML JavaScript entities found in early versions of Netscape 4.
#// 
#// Previously, this function was pulled in from the original
#// import of kses and removed a specific vulnerability only
#// existent in early version of Netscape 4. However, this
#// vulnerability never affected any other browsers and can
#// be considered safe for the modern web.
#// 
#// The regular expression which sanitized this vulnerability
#// has been removed in consideration of the performance and
#// energy demands it placed, now merely passing through its
#// input to the return.
#// 
#// @since 1.0.0
#// @deprecated 4.7.0 Officially dropped security support for Netscape 4.
#// 
#// @param string $string
#// @return string
#//
def wp_kses_js_entities(string_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "4.7.0")
    return php_preg_replace("%&\\s*\\{[^}]*(\\}\\s*;?|$)%", "", string_)
# end def wp_kses_js_entities
#// 
#// Sort categories by ID.
#// 
#// Used by usort() as a callback, should not be used directly. Can actually be
#// used to sort any term object.
#// 
#// @since 2.3.0
#// @deprecated 4.7.0 Use wp_list_sort()
#// @access private
#// 
#// @param object $a
#// @param object $b
#// @return int
#//
def _usort_terms_by_ID(a_=None, b_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "4.7.0", "wp_list_sort()")
    if a_.term_id > b_.term_id:
        return 1
    elif a_.term_id < b_.term_id:
        return -1
    else:
        return 0
    # end if
# end def _usort_terms_by_ID
#// 
#// Sort categories by name.
#// 
#// Used by usort() as a callback, should not be used directly. Can actually be
#// used to sort any term object.
#// 
#// @since 2.3.0
#// @deprecated 4.7.0 Use wp_list_sort()
#// @access private
#// 
#// @param object $a
#// @param object $b
#// @return int
#//
def _usort_terms_by_name(a_=None, b_=None, *_args_):
    
    
    _deprecated_function(__FUNCTION__, "4.7.0", "wp_list_sort()")
    return strcmp(a_.name, b_.name)
# end def _usort_terms_by_name
#// 
#// Sort menu items by the desired key.
#// 
#// @since 3.0.0
#// @deprecated 4.7.0 Use wp_list_sort()
#// @access private
#// 
#// @global string $_menu_item_sort_prop
#// 
#// @param object $a The first object to compare
#// @param object $b The second object to compare
#// @return int -1, 0, or 1 if $a is considered to be respectively less than, equal to, or greater than $b.
#//
def _sort_nav_menu_items(a_=None, b_=None, *_args_):
    
    
    global _menu_item_sort_prop_
    php_check_if_defined("_menu_item_sort_prop_")
    _deprecated_function(__FUNCTION__, "4.7.0", "wp_list_sort()")
    if php_empty(lambda : _menu_item_sort_prop_):
        return 0
    # end if
    if (not (php_isset(lambda : a_._menu_item_sort_prop_))) or (not (php_isset(lambda : b_._menu_item_sort_prop_))):
        return 0
    # end if
    _a_ = php_int(a_._menu_item_sort_prop_)
    _b_ = php_int(b_._menu_item_sort_prop_)
    if a_._menu_item_sort_prop_ == b_._menu_item_sort_prop_:
        return 0
    elif _a_ == a_._menu_item_sort_prop_ and _b_ == b_._menu_item_sort_prop_:
        return -1 if _a_ < _b_ else 1
    else:
        return strcmp(a_._menu_item_sort_prop_, b_._menu_item_sort_prop_)
    # end if
# end def _sort_nav_menu_items
#// 
#// Retrieves the Press This bookmarklet link.
#// 
#// @since 2.6.0
#// @deprecated 4.9.0
#// 
#//
def get_shortcut_link(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "4.9.0")
    link_ = ""
    #// 
    #// Filters the Press This bookmarklet link.
    #// 
    #// @since 2.6.0
    #// @deprecated 4.9.0
    #// 
    #// @param string $link The Press This bookmarklet link.
    #//
    return apply_filters("shortcut_link", link_)
# end def get_shortcut_link
#// 
#// Ajax handler for saving a post from Press This.
#// 
#// @since 4.2.0
#// @deprecated 4.9.0
#//
def wp_ajax_press_this_save_post(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "4.9.0")
    if is_plugin_active("press-this/press-this-plugin.php"):
        php_include_file(WP_PLUGIN_DIR + "/press-this/class-wp-press-this-plugin.php", once=False)
        wp_press_this_ = php_new_class("WP_Press_This_Plugin", lambda : WP_Press_This_Plugin())
        wp_press_this_.save_post()
    else:
        wp_send_json_error(Array({"errorMessage": __("The Press This plugin is required.")}))
    # end if
# end def wp_ajax_press_this_save_post
#// 
#// Ajax handler for creating new category from Press This.
#// 
#// @since 4.2.0
#// @deprecated 4.9.0
#//
def wp_ajax_press_this_add_category(*_args_):
    
    
    _deprecated_function(__FUNCTION__, "4.9.0")
    if is_plugin_active("press-this/press-this-plugin.php"):
        php_include_file(WP_PLUGIN_DIR + "/press-this/class-wp-press-this-plugin.php", once=False)
        wp_press_this_ = php_new_class("WP_Press_This_Plugin", lambda : WP_Press_This_Plugin())
        wp_press_this_.add_category()
    else:
        wp_send_json_error(Array({"errorMessage": __("The Press This plugin is required.")}))
    # end if
# end def wp_ajax_press_this_add_category
