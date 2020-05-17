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
#// WP_oEmbed_Controller class, used to provide an oEmbed endpoint.
#// 
#// @package WordPress
#// @subpackage Embeds
#// @since 4.4.0
#// 
#// 
#// oEmbed API endpoint controller.
#// 
#// Registers the API route and delivers the response data.
#// The output format (XML or JSON) is handled by the REST API.
#// 
#// @since 4.4.0
#//
class WP_oEmbed_Controller():
    #// 
    #// Register the oEmbed REST API route.
    #// 
    #// @since 4.4.0
    #//
    def register_routes(self):
        
        
        #// 
        #// Filters the maxwidth oEmbed parameter.
        #// 
        #// @since 4.4.0
        #// 
        #// @param int $maxwidth Maximum allowed width. Default 600.
        #//
        maxwidth_ = apply_filters("oembed_default_width", 600)
        register_rest_route("oembed/1.0", "/embed", Array(Array({"methods": WP_REST_Server.READABLE, "callback": Array(self, "get_item"), "args": Array({"url": Array({"required": True, "sanitize_callback": "esc_url_raw"})}, {"format": Array({"default": "json", "sanitize_callback": "wp_oembed_ensure_format"})}, {"maxwidth": Array({"default": maxwidth_, "sanitize_callback": "absint"})})})))
        register_rest_route("oembed/1.0", "/proxy", Array(Array({"methods": WP_REST_Server.READABLE, "callback": Array(self, "get_proxy_item"), "permission_callback": Array(self, "get_proxy_item_permissions_check"), "args": Array({"url": Array({"description": __("The URL of the resource for which to fetch oEmbed data."), "type": "string", "required": True, "sanitize_callback": "esc_url_raw"})}, {"format": Array({"description": __("The oEmbed format to use."), "type": "string", "default": "json", "enum": Array("json", "xml")})}, {"maxwidth": Array({"description": __("The maximum width of the embed frame in pixels."), "type": "integer", "default": maxwidth_, "sanitize_callback": "absint"})}, {"maxheight": Array({"description": __("The maximum height of the embed frame in pixels."), "type": "integer", "sanitize_callback": "absint"})}, {"discover": Array({"description": __("Whether to perform an oEmbed discovery request for non-whitelisted providers."), "type": "boolean", "default": True})})})))
    # end def register_routes
    #// 
    #// Callback for the embed API endpoint.
    #// 
    #// Returns the JSON object for the post.
    #// 
    #// @since 4.4.0
    #// 
    #// @param WP_REST_Request $request Full data about the request.
    #// @return array|WP_Error oEmbed response data or WP_Error on failure.
    #//
    def get_item(self, request_=None):
        
        
        post_id_ = url_to_postid(request_["url"])
        #// 
        #// Filters the determined post ID.
        #// 
        #// @since 4.4.0
        #// 
        #// @param int    $post_id The post ID.
        #// @param string $url     The requested URL.
        #//
        post_id_ = apply_filters("oembed_request_post_id", post_id_, request_["url"])
        data_ = get_oembed_response_data(post_id_, request_["maxwidth"])
        if (not data_):
            return php_new_class("WP_Error", lambda : WP_Error("oembed_invalid_url", get_status_header_desc(404), Array({"status": 404})))
        # end if
        return data_
    # end def get_item
    #// 
    #// Checks if current user can make a proxy oEmbed request.
    #// 
    #// @since 4.8.0
    #// 
    #// @return true|WP_Error True if the request has read access, WP_Error object otherwise.
    #//
    def get_proxy_item_permissions_check(self):
        
        
        if (not current_user_can("edit_posts")):
            return php_new_class("WP_Error", lambda : WP_Error("rest_forbidden", __("Sorry, you are not allowed to make proxied oEmbed requests."), Array({"status": rest_authorization_required_code()})))
        # end if
        return True
    # end def get_proxy_item_permissions_check
    #// 
    #// Callback for the proxy API endpoint.
    #// 
    #// Returns the JSON object for the proxied item.
    #// 
    #// @since 4.8.0
    #// 
    #// @see WP_oEmbed::get_html()
    #// @param WP_REST_Request $request Full data about the request.
    #// @return object|WP_Error oEmbed response data or WP_Error on failure.
    #//
    def get_proxy_item(self, request_=None):
        
        
        args_ = request_.get_params()
        args_["_wpnonce"] = None
        cache_key_ = "oembed_" + php_md5(serialize(args_))
        data_ = get_transient(cache_key_)
        if (not php_empty(lambda : data_)):
            return data_
        # end if
        url_ = request_["url"]
        args_["url"] = None
        #// Copy maxwidth/maxheight to width/height since WP_oEmbed::fetch() uses these arg names.
        if (php_isset(lambda : args_["maxwidth"])):
            args_["width"] = args_["maxwidth"]
        # end if
        if (php_isset(lambda : args_["maxheight"])):
            args_["height"] = args_["maxheight"]
        # end if
        #// Short-circuit process for URLs belonging to the current site.
        data_ = get_oembed_response_data_for_url(url_, args_)
        if data_:
            return data_
        # end if
        data_ = _wp_oembed_get_object().get_data(url_, args_)
        if False == data_:
            return php_new_class("WP_Error", lambda : WP_Error("oembed_invalid_url", get_status_header_desc(404), Array({"status": 404})))
        # end if
        #// This filter is documented in wp-includes/class-wp-oembed.php
        data_.html = apply_filters("oembed_result", _wp_oembed_get_object().data2html(data_, url_), url_, args_)
        #// 
        #// Filters the oEmbed TTL value (time to live).
        #// 
        #// Similar to the {@see 'oembed_ttl'} filter, but for the REST API
        #// oEmbed proxy endpoint.
        #// 
        #// @since 4.8.0
        #// 
        #// @param int    $time    Time to live (in seconds).
        #// @param string $url     The attempted embed URL.
        #// @param array  $args    An array of embed request arguments.
        #//
        ttl_ = apply_filters("rest_oembed_ttl", DAY_IN_SECONDS, url_, args_)
        set_transient(cache_key_, data_, ttl_)
        return data_
    # end def get_proxy_item
# end class WP_oEmbed_Controller
