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
#// API for easily embedding rich media such as videos and images into content.
#// 
#// @package WordPress
#// @subpackage Embed
#// @since 2.9.0
#//
class WP_Embed():
    handlers = Array()
    post_ID = Array()
    usecache = True
    linkifunknown = True
    last_attr = Array()
    last_url = ""
    return_false_on_fail = False
    #// 
    #// Constructor
    #//
    def __init__(self):
        
        #// Hack to get the [embed] shortcode to run before wpautop().
        add_filter("the_content", Array(self, "run_shortcode"), 8)
        add_filter("widget_text_content", Array(self, "run_shortcode"), 8)
        #// Shortcode placeholder for strip_shortcodes().
        add_shortcode("embed", "__return_false")
        #// Attempts to embed all URLs in a post.
        add_filter("the_content", Array(self, "autoembed"), 8)
        add_filter("widget_text_content", Array(self, "autoembed"), 8)
        #// After a post is saved, cache oEmbed items via Ajax.
        add_action("edit_form_advanced", Array(self, "maybe_run_ajax_cache"))
        add_action("edit_page_form", Array(self, "maybe_run_ajax_cache"))
    # end def __init__
    #// 
    #// Process the [embed] shortcode.
    #// 
    #// Since the [embed] shortcode needs to be run earlier than other shortcodes,
    #// this function removes all existing shortcodes, registers the [embed] shortcode,
    #// calls do_shortcode(), and then re-registers the old shortcodes.
    #// 
    #// @global array $shortcode_tags
    #// 
    #// @param string $content Content to parse
    #// @return string Content with shortcode parsed
    #//
    def run_shortcode(self, content=None):
        
        global shortcode_tags
        php_check_if_defined("shortcode_tags")
        #// Back up current registered shortcodes and clear them all out.
        orig_shortcode_tags = shortcode_tags
        remove_all_shortcodes()
        add_shortcode("embed", Array(self, "shortcode"))
        #// Do the shortcode (only the [embed] one is registered).
        content = do_shortcode(content, True)
        #// Put the original shortcodes back.
        shortcode_tags = orig_shortcode_tags
        return content
    # end def run_shortcode
    #// 
    #// If a post/page was saved, then output JavaScript to make
    #// an Ajax request that will call WP_Embed::cache_oembed().
    #//
    def maybe_run_ajax_cache(self):
        
        post = get_post()
        if (not post) or php_empty(lambda : PHP_REQUEST["message"]):
            return
        # end if
        php_print("<script type=\"text/javascript\">\n  jQuery(document).ready(function($){\n       $.get(\"")
        php_print(admin_url("admin-ajax.php?action=oembed-cache&post=" + post.ID, "relative"))
        php_print("""\");
        });
        </script>
        """)
    # end def maybe_run_ajax_cache
    #// 
    #// Registers an embed handler.
    #// 
    #// Do not use this function directly, use wp_embed_register_handler() instead.
    #// 
    #// This function should probably also only be used for sites that do not support oEmbed.
    #// 
    #// @param string $id An internal ID/name for the handler. Needs to be unique.
    #// @param string $regex The regex that will be used to see if this handler should be used for a URL.
    #// @param callable $callback The callback function that will be called if the regex is matched.
    #// @param int $priority Optional. Used to specify the order in which the registered handlers will be tested (default: 10). Lower numbers correspond with earlier testing, and handlers with the same priority are tested in the order in which they were added to the action.
    #//
    def register_handler(self, id=None, regex=None, callback=None, priority=10):
        
        self.handlers[priority][id] = Array({"regex": regex, "callback": callback})
    # end def register_handler
    #// 
    #// Unregisters a previously-registered embed handler.
    #// 
    #// Do not use this function directly, use wp_embed_unregister_handler() instead.
    #// 
    #// @param string $id The handler ID that should be removed.
    #// @param int $priority Optional. The priority of the handler to be removed (default: 10).
    #//
    def unregister_handler(self, id=None, priority=10):
        
        self.handlers[priority][id] = None
    # end def unregister_handler
    #// 
    #// The do_shortcode() callback function.
    #// 
    #// Attempts to convert a URL into embed HTML. Starts by checking the URL against the regex of
    #// the registered embed handlers. If none of the regex matches and it's enabled, then the URL
    #// will be given to the WP_oEmbed class.
    #// 
    #// @param array $attr {
    #// Shortcode attributes. Optional.
    #// 
    #// @type int $width  Width of the embed in pixels.
    #// @type int $height Height of the embed in pixels.
    #// }
    #// @param string $url The URL attempting to be embedded.
    #// @return string|false The embed HTML on success, otherwise the original URL.
    #// `->maybe_make_link()` can return false on failure.
    #//
    def shortcode(self, attr=None, url=""):
        
        post = get_post()
        if php_empty(lambda : url) and (not php_empty(lambda : attr["src"])):
            url = attr["src"]
        # end if
        self.last_url = url
        if php_empty(lambda : url):
            self.last_attr = attr
            return ""
        # end if
        rawattr = attr
        attr = wp_parse_args(attr, wp_embed_defaults(url))
        self.last_attr = attr
        #// KSES converts & into &amp; and we need to undo this.
        #// See https://core.trac.wordpress.org/ticket/11311
        url = php_str_replace("&amp;", "&", url)
        #// Look for known internal handlers.
        ksort(self.handlers)
        for priority,handlers in self.handlers:
            for id,handler in handlers:
                if php_preg_match(handler["regex"], url, matches) and php_is_callable(handler["callback"]):
                    return_ = php_call_user_func(handler["callback"], matches, attr, url, rawattr)
                    if False != return_:
                        #// 
                        #// Filters the returned embed HTML.
                        #// 
                        #// @since 2.9.0
                        #// 
                        #// @see WP_Embed::shortcode()
                        #// 
                        #// @param string|false $return The HTML result of the shortcode, or false on failure.
                        #// @param string       $url    The embed URL.
                        #// @param array        $attr   An array of shortcode attributes.
                        #//
                        return apply_filters("embed_handler_html", return_, url, attr)
                    # end if
                # end if
            # end for
        # end for
        post_ID = post.ID if (not php_empty(lambda : post.ID)) else None
        #// Potentially set by WP_Embed::cache_oembed().
        if (not php_empty(lambda : self.post_ID)):
            post_ID = self.post_ID
        # end if
        #// Check for a cached result (stored as custom post or in the post meta).
        key_suffix = php_md5(url + serialize(attr))
        cachekey = "_oembed_" + key_suffix
        cachekey_time = "_oembed_time_" + key_suffix
        #// 
        #// Filters the oEmbed TTL value (time to live).
        #// 
        #// @since 4.0.0
        #// 
        #// @param int    $time    Time to live (in seconds).
        #// @param string $url     The attempted embed URL.
        #// @param array  $attr    An array of shortcode attributes.
        #// @param int    $post_ID Post ID.
        #//
        ttl = apply_filters("oembed_ttl", DAY_IN_SECONDS, url, attr, post_ID)
        cache = ""
        cache_time = 0
        cached_post_id = self.find_oembed_post_id(key_suffix)
        if post_ID:
            cache = get_post_meta(post_ID, cachekey, True)
            cache_time = get_post_meta(post_ID, cachekey_time, True)
            if (not cache_time):
                cache_time = 0
            # end if
        elif cached_post_id:
            cached_post = get_post(cached_post_id)
            cache = cached_post.post_content
            cache_time = strtotime(cached_post.post_modified_gmt)
        # end if
        cached_recently = time() - cache_time < ttl
        if self.usecache or cached_recently:
            #// Failures are cached. Serve one if we're using the cache.
            if "{{unknown}}" == cache:
                return self.maybe_make_link(url)
            # end if
            if (not php_empty(lambda : cache)):
                #// 
                #// Filters the cached oEmbed HTML.
                #// 
                #// @since 2.9.0
                #// 
                #// @see WP_Embed::shortcode()
                #// 
                #// @param string|false $cache   The cached HTML result, stored in post meta.
                #// @param string       $url     The attempted embed URL.
                #// @param array        $attr    An array of shortcode attributes.
                #// @param int          $post_ID Post ID.
                #//
                return apply_filters("embed_oembed_html", cache, url, attr, post_ID)
            # end if
        # end if
        #// 
        #// Filters whether to inspect the given URL for discoverable link tags.
        #// 
        #// @since 2.9.0
        #// @since 4.4.0 The default value changed to true.
        #// 
        #// @see WP_oEmbed::discover()
        #// 
        #// @param bool $enable Whether to enable `<link>` tag discovery. Default true.
        #//
        attr["discover"] = apply_filters("embed_oembed_discover", True)
        #// Use oEmbed to get the HTML.
        html = wp_oembed_get(url, attr)
        if post_ID:
            if html:
                update_post_meta(post_ID, cachekey, html)
                update_post_meta(post_ID, cachekey_time, time())
            elif (not cache):
                update_post_meta(post_ID, cachekey, "{{unknown}}")
            # end if
        else:
            has_kses = False != has_filter("content_save_pre", "wp_filter_post_kses")
            if has_kses:
                #// Prevent KSES from corrupting JSON in post_content.
                kses_remove_filters()
            # end if
            insert_post_args = Array({"post_name": key_suffix, "post_status": "publish", "post_type": "oembed_cache"})
            if html:
                if cached_post_id:
                    wp_update_post(wp_slash(Array({"ID": cached_post_id, "post_content": html})))
                else:
                    wp_insert_post(wp_slash(php_array_merge(insert_post_args, Array({"post_content": html}))))
                # end if
            elif (not cache):
                wp_insert_post(wp_slash(php_array_merge(insert_post_args, Array({"post_content": "{{unknown}}"}))))
            # end if
            if has_kses:
                kses_init_filters()
            # end if
        # end if
        #// If there was a result, return it.
        if html:
            #// This filter is documented in wp-includes/class-wp-embed.php
            return apply_filters("embed_oembed_html", html, url, attr, post_ID)
        # end if
        #// Still unknown.
        return self.maybe_make_link(url)
    # end def shortcode
    #// 
    #// Delete all oEmbed caches. Unused by core as of 4.0.0.
    #// 
    #// @param int $post_ID Post ID to delete the caches for.
    #//
    def delete_oembed_caches(self, post_ID=None):
        
        post_metas = get_post_custom_keys(post_ID)
        if php_empty(lambda : post_metas):
            return
        # end if
        for post_meta_key in post_metas:
            if "_oembed_" == php_substr(post_meta_key, 0, 8):
                delete_post_meta(post_ID, post_meta_key)
            # end if
        # end for
    # end def delete_oembed_caches
    #// 
    #// Triggers a caching of all oEmbed results.
    #// 
    #// @param int $post_ID Post ID to do the caching for.
    #//
    def cache_oembed(self, post_ID=None):
        
        post = get_post(post_ID)
        post_types = get_post_types(Array({"show_ui": True}))
        #// 
        #// Filters the array of post types to cache oEmbed results for.
        #// 
        #// @since 2.9.0
        #// 
        #// @param string[] $post_types Array of post type names to cache oEmbed results for. Defaults to post types with `show_ui` set to true.
        #//
        if php_empty(lambda : post.ID) or (not php_in_array(post.post_type, apply_filters("embed_cache_oembed_types", post_types))):
            return
        # end if
        #// Trigger a caching.
        if (not php_empty(lambda : post.post_content)):
            self.post_ID = post.ID
            self.usecache = False
            content = self.run_shortcode(post.post_content)
            self.autoembed(content)
            self.usecache = True
        # end if
    # end def cache_oembed
    #// 
    #// Passes any unlinked URLs that are on their own line to WP_Embed::shortcode() for potential embedding.
    #// 
    #// @see WP_Embed::autoembed_callback()
    #// 
    #// @param string $content The content to be searched.
    #// @return string Potentially modified $content.
    #//
    def autoembed(self, content=None):
        
        #// Replace line breaks from all HTML elements with placeholders.
        content = wp_replace_in_html_tags(content, Array({"\n": "<!-- wp-line-break -->"}))
        if php_preg_match("#(^|\\s|>)https?://#i", content):
            #// Find URLs on their own line.
            content = preg_replace_callback("|^(\\s*)(https?://[^\\s<>\"]+)(\\s*)$|im", Array(self, "autoembed_callback"), content)
            #// Find URLs in their own paragraph.
            content = preg_replace_callback("|(<p(?: [^>]*)?>\\s*)(https?://[^\\s<>\"]+)(\\s*<\\/p>)|i", Array(self, "autoembed_callback"), content)
        # end if
        #// Put the line breaks back.
        return php_str_replace("<!-- wp-line-break -->", "\n", content)
    # end def autoembed
    #// 
    #// Callback function for WP_Embed::autoembed().
    #// 
    #// @param array $match A regex match array.
    #// @return string The embed HTML on success, otherwise the original URL.
    #//
    def autoembed_callback(self, match=None):
        
        oldval = self.linkifunknown
        self.linkifunknown = False
        return_ = self.shortcode(Array(), match[2])
        self.linkifunknown = oldval
        return match[1] + return_ + match[3]
    # end def autoembed_callback
    #// 
    #// Conditionally makes a hyperlink based on an internal class variable.
    #// 
    #// @param string $url URL to potentially be linked.
    #// @return string|false Linked URL or the original URL. False if 'return_false_on_fail' is true.
    #//
    def maybe_make_link(self, url=None):
        
        if self.return_false_on_fail:
            return False
        # end if
        output = "<a href=\"" + esc_url(url) + "\">" + esc_html(url) + "</a>" if self.linkifunknown else url
        #// 
        #// Filters the returned, maybe-linked embed URL.
        #// 
        #// @since 2.9.0
        #// 
        #// @param string $output The linked or original URL.
        #// @param string $url    The original URL.
        #//
        return apply_filters("embed_maybe_make_link", output, url)
    # end def maybe_make_link
    #// 
    #// Find the oEmbed cache post ID for a given cache key.
    #// 
    #// @since 4.9.0
    #// 
    #// @param string $cache_key oEmbed cache key.
    #// @return int|null Post ID on success, null on failure.
    #//
    def find_oembed_post_id(self, cache_key=None):
        
        cache_group = "oembed_cache_post"
        oembed_post_id = wp_cache_get(cache_key, cache_group)
        if oembed_post_id and "oembed_cache" == get_post_type(oembed_post_id):
            return oembed_post_id
        # end if
        oembed_post_query = php_new_class("WP_Query", lambda : WP_Query(Array({"post_type": "oembed_cache", "post_status": "publish", "name": cache_key, "posts_per_page": 1, "no_found_rows": True, "cache_results": True, "update_post_meta_cache": False, "update_post_term_cache": False, "lazy_load_term_meta": False})))
        if (not php_empty(lambda : oembed_post_query.posts)):
            #// Note: 'fields' => 'ids' is not being used in order to cache the post object as it will be needed.
            oembed_post_id = oembed_post_query.posts[0].ID
            wp_cache_set(cache_key, oembed_post_id, cache_group)
            return oembed_post_id
        # end if
        return None
    # end def find_oembed_post_id
# end class WP_Embed
