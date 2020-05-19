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
    #// 
    #// When a URL cannot be embedded, return false instead of returning a link
    #// or the URL.
    #// 
    #// Bypasses the {@see 'embed_maybe_make_link'} filter.
    #// 
    #// @var bool
    #//
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
    def run_shortcode(self, content_=None):
        
        
        global shortcode_tags_
        php_check_if_defined("shortcode_tags_")
        #// Back up current registered shortcodes and clear them all out.
        orig_shortcode_tags_ = shortcode_tags_
        remove_all_shortcodes()
        add_shortcode("embed", Array(self, "shortcode"))
        #// Do the shortcode (only the [embed] one is registered).
        content_ = do_shortcode(content_, True)
        #// Put the original shortcodes back.
        shortcode_tags_ = orig_shortcode_tags_
        return content_
    # end def run_shortcode
    #// 
    #// If a post/page was saved, then output JavaScript to make
    #// an Ajax request that will call WP_Embed::cache_oembed().
    #//
    def maybe_run_ajax_cache(self):
        
        
        post_ = get_post()
        if (not post_) or php_empty(lambda : PHP_REQUEST["message"]):
            return
        # end if
        php_print("<script type=\"text/javascript\">\n  jQuery(document).ready(function($){\n       $.get(\"")
        php_print(admin_url("admin-ajax.php?action=oembed-cache&post=" + post_.ID, "relative"))
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
    def register_handler(self, id_=None, regex_=None, callback_=None, priority_=10):
        
        
        self.handlers[priority_][id_] = Array({"regex": regex_, "callback": callback_})
    # end def register_handler
    #// 
    #// Unregisters a previously-registered embed handler.
    #// 
    #// Do not use this function directly, use wp_embed_unregister_handler() instead.
    #// 
    #// @param string $id The handler ID that should be removed.
    #// @param int $priority Optional. The priority of the handler to be removed (default: 10).
    #//
    def unregister_handler(self, id_=None, priority_=10):
        
        
        self.handlers[priority_][id_] = None
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
    def shortcode(self, attr_=None, url_=""):
        
        
        post_ = get_post()
        if php_empty(lambda : url_) and (not php_empty(lambda : attr_["src"])):
            url_ = attr_["src"]
        # end if
        self.last_url = url_
        if php_empty(lambda : url_):
            self.last_attr = attr_
            return ""
        # end if
        rawattr_ = attr_
        attr_ = wp_parse_args(attr_, wp_embed_defaults(url_))
        self.last_attr = attr_
        #// KSES converts & into &amp; and we need to undo this.
        #// See https://core.trac.wordpress.org/ticket/11311
        url_ = php_str_replace("&amp;", "&", url_)
        #// Look for known internal handlers.
        php_ksort(self.handlers)
        for priority_,handlers_ in self.handlers.items():
            for id_,handler_ in handlers_.items():
                if php_preg_match(handler_["regex"], url_, matches_) and php_is_callable(handler_["callback"]):
                    return_ = php_call_user_func(handler_["callback"], matches_, attr_, url_, rawattr_)
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
                        return apply_filters("embed_handler_html", return_, url_, attr_)
                    # end if
                # end if
            # end for
        # end for
        post_ID_ = post_.ID if (not php_empty(lambda : post_.ID)) else None
        #// Potentially set by WP_Embed::cache_oembed().
        if (not php_empty(lambda : self.post_ID)):
            post_ID_ = self.post_ID
        # end if
        #// Check for a cached result (stored as custom post or in the post meta).
        key_suffix_ = php_md5(url_ + serialize(attr_))
        cachekey_ = "_oembed_" + key_suffix_
        cachekey_time_ = "_oembed_time_" + key_suffix_
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
        ttl_ = apply_filters("oembed_ttl", DAY_IN_SECONDS, url_, attr_, post_ID_)
        cache_ = ""
        cache_time_ = 0
        cached_post_id_ = self.find_oembed_post_id(key_suffix_)
        if post_ID_:
            cache_ = get_post_meta(post_ID_, cachekey_, True)
            cache_time_ = get_post_meta(post_ID_, cachekey_time_, True)
            if (not cache_time_):
                cache_time_ = 0
            # end if
        elif cached_post_id_:
            cached_post_ = get_post(cached_post_id_)
            cache_ = cached_post_.post_content
            cache_time_ = strtotime(cached_post_.post_modified_gmt)
        # end if
        cached_recently_ = time() - cache_time_ < ttl_
        if self.usecache or cached_recently_:
            #// Failures are cached. Serve one if we're using the cache.
            if "{{unknown}}" == cache_:
                return self.maybe_make_link(url_)
            # end if
            if (not php_empty(lambda : cache_)):
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
                return apply_filters("embed_oembed_html", cache_, url_, attr_, post_ID_)
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
        attr_["discover"] = apply_filters("embed_oembed_discover", True)
        #// Use oEmbed to get the HTML.
        html_ = wp_oembed_get(url_, attr_)
        if post_ID_:
            if html_:
                update_post_meta(post_ID_, cachekey_, html_)
                update_post_meta(post_ID_, cachekey_time_, time())
            elif (not cache_):
                update_post_meta(post_ID_, cachekey_, "{{unknown}}")
            # end if
        else:
            has_kses_ = False != has_filter("content_save_pre", "wp_filter_post_kses")
            if has_kses_:
                #// Prevent KSES from corrupting JSON in post_content.
                kses_remove_filters()
            # end if
            insert_post_args_ = Array({"post_name": key_suffix_, "post_status": "publish", "post_type": "oembed_cache"})
            if html_:
                if cached_post_id_:
                    wp_update_post(wp_slash(Array({"ID": cached_post_id_, "post_content": html_})))
                else:
                    wp_insert_post(wp_slash(php_array_merge(insert_post_args_, Array({"post_content": html_}))))
                # end if
            elif (not cache_):
                wp_insert_post(wp_slash(php_array_merge(insert_post_args_, Array({"post_content": "{{unknown}}"}))))
            # end if
            if has_kses_:
                kses_init_filters()
            # end if
        # end if
        #// If there was a result, return it.
        if html_:
            #// This filter is documented in wp-includes/class-wp-embed.php
            return apply_filters("embed_oembed_html", html_, url_, attr_, post_ID_)
        # end if
        #// Still unknown.
        return self.maybe_make_link(url_)
    # end def shortcode
    #// 
    #// Delete all oEmbed caches. Unused by core as of 4.0.0.
    #// 
    #// @param int $post_ID Post ID to delete the caches for.
    #//
    def delete_oembed_caches(self, post_ID_=None):
        
        
        post_metas_ = get_post_custom_keys(post_ID_)
        if php_empty(lambda : post_metas_):
            return
        # end if
        for post_meta_key_ in post_metas_:
            if "_oembed_" == php_substr(post_meta_key_, 0, 8):
                delete_post_meta(post_ID_, post_meta_key_)
            # end if
        # end for
    # end def delete_oembed_caches
    #// 
    #// Triggers a caching of all oEmbed results.
    #// 
    #// @param int $post_ID Post ID to do the caching for.
    #//
    def cache_oembed(self, post_ID_=None):
        
        
        post_ = get_post(post_ID_)
        post_types_ = get_post_types(Array({"show_ui": True}))
        #// 
        #// Filters the array of post types to cache oEmbed results for.
        #// 
        #// @since 2.9.0
        #// 
        #// @param string[] $post_types Array of post type names to cache oEmbed results for. Defaults to post types with `show_ui` set to true.
        #//
        if php_empty(lambda : post_.ID) or (not php_in_array(post_.post_type, apply_filters("embed_cache_oembed_types", post_types_))):
            return
        # end if
        #// Trigger a caching.
        if (not php_empty(lambda : post_.post_content)):
            self.post_ID = post_.ID
            self.usecache = False
            content_ = self.run_shortcode(post_.post_content)
            self.autoembed(content_)
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
    def autoembed(self, content_=None):
        
        
        #// Replace line breaks from all HTML elements with placeholders.
        content_ = wp_replace_in_html_tags(content_, Array({"\n": "<!-- wp-line-break -->"}))
        if php_preg_match("#(^|\\s|>)https?://#i", content_):
            #// Find URLs on their own line.
            content_ = preg_replace_callback("|^(\\s*)(https?://[^\\s<>\"]+)(\\s*)$|im", Array(self, "autoembed_callback"), content_)
            #// Find URLs in their own paragraph.
            content_ = preg_replace_callback("|(<p(?: [^>]*)?>\\s*)(https?://[^\\s<>\"]+)(\\s*<\\/p>)|i", Array(self, "autoembed_callback"), content_)
        # end if
        #// Put the line breaks back.
        return php_str_replace("<!-- wp-line-break -->", "\n", content_)
    # end def autoembed
    #// 
    #// Callback function for WP_Embed::autoembed().
    #// 
    #// @param array $match A regex match array.
    #// @return string The embed HTML on success, otherwise the original URL.
    #//
    def autoembed_callback(self, match_=None):
        
        
        oldval_ = self.linkifunknown
        self.linkifunknown = False
        return_ = self.shortcode(Array(), match_[2])
        self.linkifunknown = oldval_
        return match_[1] + return_ + match_[3]
    # end def autoembed_callback
    #// 
    #// Conditionally makes a hyperlink based on an internal class variable.
    #// 
    #// @param string $url URL to potentially be linked.
    #// @return string|false Linked URL or the original URL. False if 'return_false_on_fail' is true.
    #//
    def maybe_make_link(self, url_=None):
        
        
        if self.return_false_on_fail:
            return False
        # end if
        output_ = "<a href=\"" + esc_url(url_) + "\">" + esc_html(url_) + "</a>" if self.linkifunknown else url_
        #// 
        #// Filters the returned, maybe-linked embed URL.
        #// 
        #// @since 2.9.0
        #// 
        #// @param string $output The linked or original URL.
        #// @param string $url    The original URL.
        #//
        return apply_filters("embed_maybe_make_link", output_, url_)
    # end def maybe_make_link
    #// 
    #// Find the oEmbed cache post ID for a given cache key.
    #// 
    #// @since 4.9.0
    #// 
    #// @param string $cache_key oEmbed cache key.
    #// @return int|null Post ID on success, null on failure.
    #//
    def find_oembed_post_id(self, cache_key_=None):
        
        
        cache_group_ = "oembed_cache_post"
        oembed_post_id_ = wp_cache_get(cache_key_, cache_group_)
        if oembed_post_id_ and "oembed_cache" == get_post_type(oembed_post_id_):
            return oembed_post_id_
        # end if
        oembed_post_query_ = php_new_class("WP_Query", lambda : WP_Query(Array({"post_type": "oembed_cache", "post_status": "publish", "name": cache_key_, "posts_per_page": 1, "no_found_rows": True, "cache_results": True, "update_post_meta_cache": False, "update_post_term_cache": False, "lazy_load_term_meta": False})))
        if (not php_empty(lambda : oembed_post_query_.posts)):
            #// Note: 'fields' => 'ids' is not being used in order to cache the post object as it will be needed.
            oembed_post_id_ = oembed_post_query_.posts[0].ID
            wp_cache_set(cache_key_, oembed_post_id_, cache_group_)
            return oembed_post_id_
        # end if
        return None
    # end def find_oembed_post_id
# end class WP_Embed
