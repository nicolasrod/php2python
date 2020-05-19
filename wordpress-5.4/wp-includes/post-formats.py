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
#// Post format functions.
#// 
#// @package WordPress
#// @subpackage Post
#// 
#// 
#// Retrieve the format slug for a post
#// 
#// @since 3.1.0
#// 
#// @param int|object|null $post Post ID or post object. Optional, default is the current post from the loop.
#// @return string|false The format if successful. False otherwise.
#//
def get_post_format(post_=None, *_args_):
    if post_ is None:
        post_ = None
    # end if
    
    post_ = get_post(post_)
    if (not post_):
        return False
    # end if
    if (not post_type_supports(post_.post_type, "post-formats")):
        return False
    # end if
    _format_ = get_the_terms(post_.ID, "post_format")
    if php_empty(lambda : _format_):
        return False
    # end if
    format_ = reset(_format_)
    return php_str_replace("post-format-", "", format_.slug)
# end def get_post_format
#// 
#// Check if a post has any of the given formats, or any format.
#// 
#// @since 3.1.0
#// 
#// @param string|array     $format Optional. The format or formats to check.
#// @param WP_Post|int|null $post   Optional. The post to check. If not supplied, defaults to the current post if used in the loop.
#// @return bool True if the post has any of the given formats (or any format, if no format specified), false otherwise.
#//
def has_post_format(format_=None, post_=None, *_args_):
    if format_ is None:
        format_ = Array()
    # end if
    if post_ is None:
        post_ = None
    # end if
    
    prefixed_ = Array()
    if format_:
        for single_ in format_:
            prefixed_[-1] = "post-format-" + sanitize_key(single_)
        # end for
    # end if
    return has_term(prefixed_, "post_format", post_)
# end def has_post_format
#// 
#// Assign a format to a post
#// 
#// @since 3.1.0
#// 
#// @param int|object $post   The post for which to assign a format.
#// @param string     $format A format to assign. Use an empty string or array to remove all formats from the post.
#// @return array|WP_Error|false WP_Error on error. Array of affected term IDs on success.
#//
def set_post_format(post_=None, format_=None, *_args_):
    
    
    post_ = get_post(post_)
    if (not post_):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_post", __("Invalid post.")))
    # end if
    if (not php_empty(lambda : format_)):
        format_ = sanitize_key(format_)
        if "standard" == format_ or (not php_in_array(format_, get_post_format_slugs())):
            format_ = ""
        else:
            format_ = "post-format-" + format_
        # end if
    # end if
    return wp_set_post_terms(post_.ID, format_, "post_format")
# end def set_post_format
#// 
#// Returns an array of post format slugs to their translated and pretty display versions
#// 
#// @since 3.1.0
#// 
#// @return string[] Array of post format labels keyed by format slug.
#//
def get_post_format_strings(*_args_):
    
    
    strings_ = Array({"standard": _x("Standard", "Post format"), "aside": _x("Aside", "Post format"), "chat": _x("Chat", "Post format"), "gallery": _x("Gallery", "Post format"), "link": _x("Link", "Post format"), "image": _x("Image", "Post format"), "quote": _x("Quote", "Post format"), "status": _x("Status", "Post format"), "video": _x("Video", "Post format"), "audio": _x("Audio", "Post format")})
    return strings_
# end def get_post_format_strings
#// 
#// Retrieves the array of post format slugs.
#// 
#// @since 3.1.0
#// 
#// @return string[] The array of post format slugs as both keys and values.
#//
def get_post_format_slugs(*_args_):
    
    
    slugs_ = php_array_keys(get_post_format_strings())
    return php_array_combine(slugs_, slugs_)
# end def get_post_format_slugs
#// 
#// Returns a pretty, translated version of a post format slug
#// 
#// @since 3.1.0
#// 
#// @param string $slug A post format slug.
#// @return string The translated post format name.
#//
def get_post_format_string(slug_=None, *_args_):
    
    
    strings_ = get_post_format_strings()
    if (not slug_):
        return strings_["standard"]
    else:
        return strings_[slug_] if (php_isset(lambda : strings_[slug_])) else ""
    # end if
# end def get_post_format_string
#// 
#// Returns a link to a post format index.
#// 
#// @since 3.1.0
#// 
#// @param string $format The post format slug.
#// @return string|WP_Error|false The post format term link.
#//
def get_post_format_link(format_=None, *_args_):
    
    
    term_ = get_term_by("slug", "post-format-" + format_, "post_format")
    if (not term_) or is_wp_error(term_):
        return False
    # end if
    return get_term_link(term_)
# end def get_post_format_link
#// 
#// Filters the request to allow for the format prefix.
#// 
#// @access private
#// @since 3.1.0
#// 
#// @param array $qvs
#// @return array
#//
def _post_format_request(qvs_=None, *_args_):
    
    
    if (not (php_isset(lambda : qvs_["post_format"]))):
        return qvs_
    # end if
    slugs_ = get_post_format_slugs()
    if (php_isset(lambda : slugs_[qvs_["post_format"]])):
        qvs_["post_format"] = "post-format-" + slugs_[qvs_["post_format"]]
    # end if
    tax_ = get_taxonomy("post_format")
    if (not is_admin()):
        qvs_["post_type"] = tax_.object_type
    # end if
    return qvs_
# end def _post_format_request
#// 
#// Filters the post format term link to remove the format prefix.
#// 
#// @access private
#// @since 3.1.0
#// 
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// 
#// @param string $link
#// @param object $term
#// @param string $taxonomy
#// @return string
#//
def _post_format_link(link_=None, term_=None, taxonomy_=None, *_args_):
    
    
    global wp_rewrite_
    php_check_if_defined("wp_rewrite_")
    if "post_format" != taxonomy_:
        return link_
    # end if
    if wp_rewrite_.get_extra_permastruct(taxonomy_):
        return php_str_replace(str("/") + str(term_.slug), "/" + php_str_replace("post-format-", "", term_.slug), link_)
    else:
        link_ = remove_query_arg("post_format", link_)
        return add_query_arg("post_format", php_str_replace("post-format-", "", term_.slug), link_)
    # end if
# end def _post_format_link
#// 
#// Remove the post format prefix from the name property of the term object created by get_term().
#// 
#// @access private
#// @since 3.1.0
#// 
#// @param object $term
#// @return object
#//
def _post_format_get_term(term_=None, *_args_):
    
    
    if (php_isset(lambda : term_.slug)):
        term_.name = get_post_format_string(php_str_replace("post-format-", "", term_.slug))
    # end if
    return term_
# end def _post_format_get_term
#// 
#// Remove the post format prefix from the name property of the term objects created by get_terms().
#// 
#// @access private
#// @since 3.1.0
#// 
#// @param array        $terms
#// @param string|array $taxonomies
#// @param array        $args
#// @return array
#//
def _post_format_get_terms(terms_=None, taxonomies_=None, args_=None, *_args_):
    
    
    if php_in_array("post_format", taxonomies_):
        if (php_isset(lambda : args_["fields"])) and "names" == args_["fields"]:
            for order_,name_ in terms_.items():
                terms_[order_] = get_post_format_string(php_str_replace("post-format-", "", name_))
            # end for
        else:
            for order_,term_ in terms_.items():
                if (php_isset(lambda : term_.taxonomy)) and "post_format" == term_.taxonomy:
                    terms_[order_].name = get_post_format_string(php_str_replace("post-format-", "", term_.slug))
                # end if
            # end for
        # end if
    # end if
    return terms_
# end def _post_format_get_terms
#// 
#// Remove the post format prefix from the name property of the term objects created by wp_get_object_terms().
#// 
#// @access private
#// @since 3.1.0
#// 
#// @param array $terms
#// @return array
#//
def _post_format_wp_get_object_terms(terms_=None, *_args_):
    
    
    for order_,term_ in terms_.items():
        if (php_isset(lambda : term_.taxonomy)) and "post_format" == term_.taxonomy:
            terms_[order_].name = get_post_format_string(php_str_replace("post-format-", "", term_.slug))
        # end if
    # end for
    return terms_
# end def _post_format_wp_get_object_terms
