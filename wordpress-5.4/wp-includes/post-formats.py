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
def get_post_format(post=None, *args_):
    
    post = get_post(post)
    if (not post):
        return False
    # end if
    if (not post_type_supports(post.post_type, "post-formats")):
        return False
    # end if
    _format = get_the_terms(post.ID, "post_format")
    if php_empty(lambda : _format):
        return False
    # end if
    format = reset(_format)
    return php_str_replace("post-format-", "", format.slug)
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
def has_post_format(format=Array(), post=None, *args_):
    
    prefixed = Array()
    if format:
        for single in format:
            prefixed[-1] = "post-format-" + sanitize_key(single)
        # end for
    # end if
    return has_term(prefixed, "post_format", post)
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
def set_post_format(post=None, format=None, *args_):
    
    post = get_post(post)
    if (not post):
        return php_new_class("WP_Error", lambda : WP_Error("invalid_post", __("Invalid post.")))
    # end if
    if (not php_empty(lambda : format)):
        format = sanitize_key(format)
        if "standard" == format or (not php_in_array(format, get_post_format_slugs())):
            format = ""
        else:
            format = "post-format-" + format
        # end if
    # end if
    return wp_set_post_terms(post.ID, format, "post_format")
# end def set_post_format
#// 
#// Returns an array of post format slugs to their translated and pretty display versions
#// 
#// @since 3.1.0
#// 
#// @return string[] Array of post format labels keyed by format slug.
#//
def get_post_format_strings(*args_):
    
    strings = Array({"standard": _x("Standard", "Post format"), "aside": _x("Aside", "Post format"), "chat": _x("Chat", "Post format"), "gallery": _x("Gallery", "Post format"), "link": _x("Link", "Post format"), "image": _x("Image", "Post format"), "quote": _x("Quote", "Post format"), "status": _x("Status", "Post format"), "video": _x("Video", "Post format"), "audio": _x("Audio", "Post format")})
    return strings
# end def get_post_format_strings
#// 
#// Retrieves the array of post format slugs.
#// 
#// @since 3.1.0
#// 
#// @return string[] The array of post format slugs as both keys and values.
#//
def get_post_format_slugs(*args_):
    
    slugs = php_array_keys(get_post_format_strings())
    return php_array_combine(slugs, slugs)
# end def get_post_format_slugs
#// 
#// Returns a pretty, translated version of a post format slug
#// 
#// @since 3.1.0
#// 
#// @param string $slug A post format slug.
#// @return string The translated post format name.
#//
def get_post_format_string(slug=None, *args_):
    
    strings = get_post_format_strings()
    if (not slug):
        return strings["standard"]
    else:
        return strings[slug] if (php_isset(lambda : strings[slug])) else ""
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
def get_post_format_link(format=None, *args_):
    
    term = get_term_by("slug", "post-format-" + format, "post_format")
    if (not term) or is_wp_error(term):
        return False
    # end if
    return get_term_link(term)
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
def _post_format_request(qvs=None, *args_):
    
    if (not (php_isset(lambda : qvs["post_format"]))):
        return qvs
    # end if
    slugs = get_post_format_slugs()
    if (php_isset(lambda : slugs[qvs["post_format"]])):
        qvs["post_format"] = "post-format-" + slugs[qvs["post_format"]]
    # end if
    tax = get_taxonomy("post_format")
    if (not is_admin()):
        qvs["post_type"] = tax.object_type
    # end if
    return qvs
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
def _post_format_link(link=None, term=None, taxonomy=None, *args_):
    
    global wp_rewrite
    php_check_if_defined("wp_rewrite")
    if "post_format" != taxonomy:
        return link
    # end if
    if wp_rewrite.get_extra_permastruct(taxonomy):
        return php_str_replace(str("/") + str(term.slug), "/" + php_str_replace("post-format-", "", term.slug), link)
    else:
        link = remove_query_arg("post_format", link)
        return add_query_arg("post_format", php_str_replace("post-format-", "", term.slug), link)
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
def _post_format_get_term(term=None, *args_):
    
    if (php_isset(lambda : term.slug)):
        term.name = get_post_format_string(php_str_replace("post-format-", "", term.slug))
    # end if
    return term
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
def _post_format_get_terms(terms=None, taxonomies=None, args=None, *args_):
    
    if php_in_array("post_format", taxonomies):
        if (php_isset(lambda : args["fields"])) and "names" == args["fields"]:
            for order,name in terms:
                terms[order] = get_post_format_string(php_str_replace("post-format-", "", name))
            # end for
        else:
            for order,term in terms:
                if (php_isset(lambda : term.taxonomy)) and "post_format" == term.taxonomy:
                    terms[order].name = get_post_format_string(php_str_replace("post-format-", "", term.slug))
                # end if
            # end for
        # end if
    # end if
    return terms
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
def _post_format_wp_get_object_terms(terms=None, *args_):
    
    for order,term in terms:
        if (php_isset(lambda : term.taxonomy)) and "post_format" == term.taxonomy:
            terms[order].name = get_post_format_string(php_str_replace("post-format-", "", term.slug))
        # end if
    # end for
    return terms
# end def _post_format_wp_get_object_terms
