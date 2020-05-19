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
#// REST API: WP_REST_Server class
#// 
#// @package WordPress
#// @subpackage REST_API
#// @since 4.4.0
#// 
#// 
#// Core class used to implement the WordPress REST API server.
#// 
#// @since 4.4.0
#//
class WP_REST_Server():
    READABLE = "GET"
    CREATABLE = "POST"
    EDITABLE = "POST, PUT, PATCH"
    DELETABLE = "DELETE"
    ALLMETHODS = "GET, POST, PUT, PATCH, DELETE"
    #// 
    #// Namespaces registered to the server.
    #// 
    #// @since 4.4.0
    #// @var array
    #//
    namespaces = Array()
    #// 
    #// Endpoints registered to the server.
    #// 
    #// @since 4.4.0
    #// @var array
    #//
    endpoints = Array()
    #// 
    #// Options defined for the routes.
    #// 
    #// @since 4.4.0
    #// @var array
    #//
    route_options = Array()
    #// 
    #// Caches embedded requests.
    #// 
    #// @since 5.4.0
    #// @var array
    #//
    embed_cache = Array()
    #// 
    #// Instantiates the REST server.
    #// 
    #// @since 4.4.0
    #//
    def __init__(self):
        
        
        self.endpoints = Array({"/": Array({"callback": Array(self, "get_index"), "methods": "GET", "args": Array({"context": Array({"default": "view"})})})})
    # end def __init__
    #// 
    #// Checks the authentication headers if supplied.
    #// 
    #// @since 4.4.0
    #// 
    #// @return WP_Error|null WP_Error indicates unsuccessful login, null indicates successful
    #// or no authentication provided
    #//
    def check_authentication(self):
        
        
        #// 
        #// Filters REST authentication errors.
        #// 
        #// This is used to pass a WP_Error from an authentication method back to
        #// the API.
        #// 
        #// Authentication methods should check first if they're being used, as
        #// multiple authentication methods can be enabled on a site (cookies,
        #// HTTP basic auth, OAuth). If the authentication method hooked in is
        #// not actually being attempted, null should be returned to indicate
        #// another authentication method should check instead. Similarly,
        #// callbacks should ensure the value is `null` before checking for
        #// errors.
        #// 
        #// A WP_Error instance can be returned if an error occurs, and this should
        #// match the format used by API methods internally (that is, the `status`
        #// data should be used). A callback can return `true` to indicate that
        #// the authentication method was used, and it succeeded.
        #// 
        #// @since 4.4.0
        #// 
        #// @param WP_Error|null|true $errors WP_Error if authentication error, null if authentication
        #// method wasn't used, true if authentication succeeded.
        #//
        return apply_filters("rest_authentication_errors", None)
    # end def check_authentication
    #// 
    #// Converts an error to a response object.
    #// 
    #// This iterates over all error codes and messages to change it into a flat
    #// array. This enables simpler client behaviour, as it is represented as a
    #// list in JSON rather than an object/map.
    #// 
    #// @since 4.4.0
    #// 
    #// @param WP_Error $error WP_Error instance.
    #// @return WP_REST_Response List of associative arrays with code and message keys.
    #//
    def error_to_response(self, error_=None):
        
        
        error_data_ = error_.get_error_data()
        if php_is_array(error_data_) and (php_isset(lambda : error_data_["status"])):
            status_ = error_data_["status"]
        else:
            status_ = 500
        # end if
        errors_ = Array()
        for code_,messages_ in error_.errors.items():
            for message_ in messages_:
                errors_[-1] = Array({"code": code_, "message": message_, "data": error_.get_error_data(code_)})
            # end for
        # end for
        data_ = errors_[0]
        if php_count(errors_) > 1:
            #// Remove the primary error.
            php_array_shift(errors_)
            data_["additional_errors"] = errors_
        # end if
        response_ = php_new_class("WP_REST_Response", lambda : WP_REST_Response(data_, status_))
        return response_
    # end def error_to_response
    #// 
    #// Retrieves an appropriate error representation in JSON.
    #// 
    #// Note: This should only be used in WP_REST_Server::serve_request(), as it
    #// cannot handle WP_Error internally. All callbacks and other internal methods
    #// should instead return a WP_Error with the data set to an array that includes
    #// a 'status' key, with the value being the HTTP status to send.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $code    WP_Error-style code.
    #// @param string $message Human-readable message.
    #// @param int    $status  Optional. HTTP status code to send. Default null.
    #// @return string JSON representation of the error
    #//
    def json_error(self, code_=None, message_=None, status_=None):
        if status_ is None:
            status_ = None
        # end if
        
        if status_:
            self.set_status(status_)
        # end if
        error_ = php_compact("code_", "message_")
        return wp_json_encode(error_)
    # end def json_error
    #// 
    #// Handles serving an API request.
    #// 
    #// Matches the current server URI to a route and runs the first matching
    #// callback then outputs a JSON representation of the returned value.
    #// 
    #// @since 4.4.0
    #// 
    #// @see WP_REST_Server::dispatch()
    #// 
    #// @param string $path Optional. The request route. If not set, `$_SERVER['PATH_INFO']` will be used.
    #// Default null.
    #// @return null|false Null if not served and a HEAD request, false otherwise.
    #//
    def serve_request(self, path_=None):
        if path_ is None:
            path_ = None
        # end if
        
        content_type_ = "application/javascript" if (php_isset(lambda : PHP_REQUEST["_jsonp"])) else "application/json"
        self.send_header("Content-Type", content_type_ + "; charset=" + get_option("blog_charset"))
        self.send_header("X-Robots-Tag", "noindex")
        api_root_ = get_rest_url()
        if (not php_empty(lambda : api_root_)):
            self.send_header("Link", "<" + esc_url_raw(api_root_) + ">; rel=\"https://api.w.org/\"")
        # end if
        #// 
        #// Mitigate possible JSONP Flash attacks.
        #// 
        #// https://miki.it/blog/2014/7/8/abusing-jsonp-with-rosetta-flash
        #//
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Access-Control-Expose-Headers", "X-WP-Total, X-WP-TotalPages")
        self.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type")
        #// 
        #// Send nocache headers on authenticated requests.
        #// 
        #// @since 4.4.0
        #// 
        #// @param bool $rest_send_nocache_headers Whether to send no-cache headers.
        #//
        send_no_cache_headers_ = apply_filters("rest_send_nocache_headers", is_user_logged_in())
        if send_no_cache_headers_:
            for header_,header_value_ in wp_get_nocache_headers().items():
                if php_empty(lambda : header_value_):
                    self.remove_header(header_)
                else:
                    self.send_header(header_, header_value_)
                # end if
            # end for
        # end if
        #// 
        #// Filters whether the REST API is enabled.
        #// 
        #// @since 4.4.0
        #// @deprecated 4.7.0 Use the {@see 'rest_authentication_errors'} filter to
        #// restrict access to the API.
        #// 
        #// @param bool $rest_enabled Whether the REST API is enabled. Default true.
        #//
        apply_filters_deprecated("rest_enabled", Array(True), "4.7.0", "rest_authentication_errors", php_sprintf(__("The REST API can no longer be completely disabled, the %s filter can be used to restrict access to the API, instead."), "rest_authentication_errors"))
        #// 
        #// Filters whether jsonp is enabled.
        #// 
        #// @since 4.4.0
        #// 
        #// @param bool $jsonp_enabled Whether jsonp is enabled. Default true.
        #//
        jsonp_enabled_ = apply_filters("rest_jsonp_enabled", True)
        jsonp_callback_ = None
        if (php_isset(lambda : PHP_REQUEST["_jsonp"])):
            if (not jsonp_enabled_):
                php_print(self.json_error("rest_callback_disabled", __("JSONP support is disabled on this site."), 400))
                return False
            # end if
            jsonp_callback_ = PHP_REQUEST["_jsonp"]
            if (not wp_check_jsonp_callback(jsonp_callback_)):
                php_print(self.json_error("rest_callback_invalid", __("Invalid JSONP callback function."), 400))
                return False
            # end if
        # end if
        if php_empty(lambda : path_):
            if (php_isset(lambda : PHP_SERVER["PATH_INFO"])):
                path_ = PHP_SERVER["PATH_INFO"]
            else:
                path_ = "/"
            # end if
        # end if
        request_ = php_new_class("WP_REST_Request", lambda : WP_REST_Request(PHP_SERVER["REQUEST_METHOD"], path_))
        request_.set_query_params(wp_unslash(PHP_REQUEST))
        request_.set_body_params(wp_unslash(PHP_POST))
        request_.set_file_params(PHP_FILES)
        request_.set_headers(self.get_headers(wp_unslash(PHP_SERVER)))
        request_.set_body(self.get_raw_data())
        #// 
        #// HTTP method override for clients that can't use PUT/PATCH/DELETE. First, we check
        #// $_GET['_method']. If that is not set, we check for the HTTP_X_HTTP_METHOD_OVERRIDE
        #// header.
        #//
        if (php_isset(lambda : PHP_REQUEST["_method"])):
            request_.set_method(PHP_REQUEST["_method"])
        elif (php_isset(lambda : PHP_SERVER["HTTP_X_HTTP_METHOD_OVERRIDE"])):
            request_.set_method(PHP_SERVER["HTTP_X_HTTP_METHOD_OVERRIDE"])
        # end if
        result_ = self.check_authentication()
        if (not is_wp_error(result_)):
            result_ = self.dispatch(request_)
        # end if
        #// Normalize to either WP_Error or WP_REST_Response...
        result_ = rest_ensure_response(result_)
        #// ...then convert WP_Error across.
        if is_wp_error(result_):
            result_ = self.error_to_response(result_)
        # end if
        #// 
        #// Filters the API response.
        #// 
        #// Allows modification of the response before returning.
        #// 
        #// @since 4.4.0
        #// @since 4.5.0 Applied to embedded responses.
        #// 
        #// @param WP_HTTP_Response $result  Result to send to the client. Usually a WP_REST_Response.
        #// @param WP_REST_Server   $this    Server instance.
        #// @param WP_REST_Request  $request Request used to generate the response.
        #//
        result_ = apply_filters("rest_post_dispatch", rest_ensure_response(result_), self, request_)
        #// Wrap the response in an envelope if asked for.
        if (php_isset(lambda : PHP_REQUEST["_envelope"])):
            result_ = self.envelope_response(result_, (php_isset(lambda : PHP_REQUEST["_embed"])))
        # end if
        #// Send extra data from response objects.
        headers_ = result_.get_headers()
        self.send_headers(headers_)
        code_ = result_.get_status()
        self.set_status(code_)
        #// 
        #// Filters whether the request has already been served.
        #// 
        #// Allow sending the request manually - by returning true, the API result
        #// will not be sent to the client.
        #// 
        #// @since 4.4.0
        #// 
        #// @param bool             $served  Whether the request has already been served.
        #// Default false.
        #// @param WP_HTTP_Response $result  Result to send to the client. Usually a WP_REST_Response.
        #// @param WP_REST_Request  $request Request used to generate the response.
        #// @param WP_REST_Server   $this    Server instance.
        #//
        served_ = apply_filters("rest_pre_serve_request", False, result_, request_, self)
        if (not served_):
            if "HEAD" == request_.get_method():
                return None
            # end if
            #// Embed links inside the request.
            embed_ = rest_parse_embed_param(PHP_REQUEST["_embed"]) if (php_isset(lambda : PHP_REQUEST["_embed"])) else False
            result_ = self.response_to_data(result_, embed_)
            #// 
            #// Filters the API response.
            #// 
            #// Allows modification of the response data after inserting
            #// embedded data (if any) and before echoing the response data.
            #// 
            #// @since 4.8.1
            #// 
            #// @param array            $result  Response data to send to the client.
            #// @param WP_REST_Server   $this    Server instance.
            #// @param WP_REST_Request  $request Request used to generate the response.
            #//
            result_ = apply_filters("rest_pre_echo_response", result_, self, request_)
            #// The 204 response shouldn't have a body.
            if 204 == code_ or None == result_:
                return None
            # end if
            result_ = wp_json_encode(result_)
            json_error_message_ = self.get_json_last_error()
            if json_error_message_:
                json_error_obj_ = php_new_class("WP_Error", lambda : WP_Error("rest_encode_error", json_error_message_, Array({"status": 500})))
                result_ = self.error_to_response(json_error_obj_)
                result_ = wp_json_encode(result_.data[0])
            # end if
            if jsonp_callback_:
                #// Prepend '/**/' to mitigate possible JSONP Flash attacks.
                #// https://miki.it/blog/2014/7/8/abusing-jsonp-with-rosetta-flash
                php_print("/**/" + jsonp_callback_ + "(" + result_ + ")")
            else:
                php_print(result_)
            # end if
        # end if
        return None
    # end def serve_request
    #// 
    #// Converts a response to data to send.
    #// 
    #// @since 4.4.0
    #// @since 5.4.0 The $embed parameter can now contain a list of link relations to include.
    #// 
    #// @param WP_REST_Response $response Response object.
    #// @param bool|string[]    $embed    Whether to embed all links, a filtered list of link relations, or no links.
    #// @return array {
    #// Data with sub-requests embedded.
    #// 
    #// @type array [$_links]    Links.
    #// @type array [$_embedded] Embeddeds.
    #// }
    #//
    def response_to_data(self, response_=None, embed_=None):
        
        
        data_ = response_.get_data()
        links_ = self.get_compact_response_links(response_)
        if (not php_empty(lambda : links_)):
            #// Convert links to part of the data.
            data_["_links"] = links_
        # end if
        if embed_:
            self.embed_cache = Array()
            #// Determine if this is a numeric array.
            if wp_is_numeric_array(data_):
                for key_,item_ in data_.items():
                    data_[key_] = self.embed_links(item_, embed_)
                # end for
            else:
                data_ = self.embed_links(data_, embed_)
            # end if
            self.embed_cache = Array()
        # end if
        return data_
    # end def response_to_data
    #// 
    #// Retrieves links from a response.
    #// 
    #// Extracts the links from a response into a structured hash, suitable for
    #// direct output.
    #// 
    #// @since 4.4.0
    #// 
    #// @param WP_REST_Response $response Response to extract links from.
    #// @return array Map of link relation to list of link hashes.
    #//
    @classmethod
    def get_response_links(self, response_=None):
        
        
        links_ = response_.get_links()
        if php_empty(lambda : links_):
            return Array()
        # end if
        #// Convert links to part of the data.
        data_ = Array()
        for rel_,items_ in links_.items():
            data_[rel_] = Array()
            for item_ in items_:
                attributes_ = item_["attributes"]
                attributes_["href"] = item_["href"]
                data_[rel_][-1] = attributes_
            # end for
        # end for
        return data_
    # end def get_response_links
    #// 
    #// Retrieves the CURIEs (compact URIs) used for relations.
    #// 
    #// Extracts the links from a response into a structured hash, suitable for
    #// direct output.
    #// 
    #// @since 4.5.0
    #// 
    #// @param WP_REST_Response $response Response to extract links from.
    #// @return array Map of link relation to list of link hashes.
    #//
    @classmethod
    def get_compact_response_links(self, response_=None):
        
        
        links_ = self.get_response_links(response_)
        if php_empty(lambda : links_):
            return Array()
        # end if
        curies_ = response_.get_curies()
        used_curies_ = Array()
        for rel_,items_ in links_.items():
            #// Convert $rel URIs to their compact versions if they exist.
            for curie_ in curies_:
                href_prefix_ = php_substr(curie_["href"], 0, php_strpos(curie_["href"], "{rel}"))
                if php_strpos(rel_, href_prefix_) != 0:
                    continue
                # end if
                #// Relation now changes from '$uri' to '$curie:$relation'.
                rel_regex_ = php_str_replace("\\{rel\\}", "(.+)", preg_quote(curie_["href"], "!"))
                php_preg_match("!" + rel_regex_ + "!", rel_, matches_)
                if matches_:
                    new_rel_ = curie_["name"] + ":" + matches_[1]
                    used_curies_[curie_["name"]] = curie_
                    links_[new_rel_] = items_
                    links_[rel_] = None
                    break
                # end if
            # end for
        # end for
        #// Push the curies onto the start of the links array.
        if used_curies_:
            links_["curies"] = php_array_values(used_curies_)
        # end if
        return links_
    # end def get_compact_response_links
    #// 
    #// Embeds the links from the data into the request.
    #// 
    #// @since 4.4.0
    #// @since 5.4.0 The $embed parameter can now contain a list of link relations to include.
    #// 
    #// @param array         $data  Data from the request.
    #// @param bool|string[] $embed Whether to embed all links or a filtered list of link relations.
    #// @return array {
    #// Data with sub-requests embedded.
    #// 
    #// @type array [$_links]    Links.
    #// @type array [$_embedded] Embeddeds.
    #// }
    #//
    def embed_links(self, data_=None, embed_=None):
        if embed_ is None:
            embed_ = True
        # end if
        
        if php_empty(lambda : data_["_links"]):
            return data_
        # end if
        embedded_ = Array()
        for rel_,links_ in data_["_links"].items():
            #// If a list of relations was specified, and the link relation is not in the whitelist, don't process the link.
            if php_is_array(embed_) and (not php_in_array(rel_, embed_, True)):
                continue
            # end if
            embeds_ = Array()
            for item_ in links_:
                #// Determine if the link is embeddable.
                if php_empty(lambda : item_["embeddable"]):
                    #// Ensure we keep the same order.
                    embeds_[-1] = Array()
                    continue
                # end if
                if (not php_array_key_exists(item_["href"], self.embed_cache)):
                    #// Run through our internal routing and serve.
                    request_ = WP_REST_Request.from_url(item_["href"])
                    if (not request_):
                        embeds_[-1] = Array()
                        continue
                    # end if
                    #// Embedded resources get passed context=embed.
                    if php_empty(lambda : request_["context"]):
                        request_["context"] = "embed"
                    # end if
                    response_ = self.dispatch(request_)
                    #// This filter is documented in wp-includes/rest-api/class-wp-rest-server.php
                    response_ = apply_filters("rest_post_dispatch", rest_ensure_response(response_), self, request_)
                    self.embed_cache[item_["href"]] = self.response_to_data(response_, False)
                # end if
                embeds_[-1] = self.embed_cache[item_["href"]]
            # end for
            #// Determine if any real links were found.
            has_links_ = php_count(php_array_filter(embeds_))
            if has_links_:
                embedded_[rel_] = embeds_
            # end if
        # end for
        if (not php_empty(lambda : embedded_)):
            data_["_embedded"] = embedded_
        # end if
        return data_
    # end def embed_links
    #// 
    #// Wraps the response in an envelope.
    #// 
    #// The enveloping technique is used to work around browser/client
    #// compatibility issues. Essentially, it converts the full HTTP response to
    #// data instead.
    #// 
    #// @since 4.4.0
    #// 
    #// @param WP_REST_Response $response Response object.
    #// @param bool             $embed    Whether links should be embedded.
    #// @return WP_REST_Response New response with wrapped data
    #//
    def envelope_response(self, response_=None, embed_=None):
        
        
        envelope_ = Array({"body": self.response_to_data(response_, embed_), "status": response_.get_status(), "headers": response_.get_headers()})
        #// 
        #// Filters the enveloped form of a response.
        #// 
        #// @since 4.4.0
        #// 
        #// @param array            $envelope Envelope data.
        #// @param WP_REST_Response $response Original response data.
        #//
        envelope_ = apply_filters("rest_envelope_response", envelope_, response_)
        #// Ensure it's still a response and return.
        return rest_ensure_response(envelope_)
    # end def envelope_response
    #// 
    #// Registers a route to the server.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $namespace  Namespace.
    #// @param string $route      The REST route.
    #// @param array  $route_args Route arguments.
    #// @param bool   $override   Optional. Whether the route should be overridden if it already exists.
    #// Default false.
    #//
    def register_route(self, namespace_=None, route_=None, route_args_=None, override_=None):
        if override_ is None:
            override_ = False
        # end if
        
        if (not (php_isset(lambda : self.namespaces[namespace_]))):
            self.namespaces[namespace_] = Array()
            self.register_route(namespace_, "/" + namespace_, Array(Array({"methods": self.READABLE, "callback": Array(self, "get_namespace_index"), "args": Array({"namespace": Array({"default": namespace_})}, {"context": Array({"default": "view"})})})))
        # end if
        #// Associative to avoid double-registration.
        self.namespaces[namespace_][route_] = True
        route_args_["namespace"] = namespace_
        if override_ or php_empty(lambda : self.endpoints[route_]):
            self.endpoints[route_] = route_args_
        else:
            self.endpoints[route_] = php_array_merge(self.endpoints[route_], route_args_)
        # end if
    # end def register_route
    #// 
    #// Retrieves the route map.
    #// 
    #// The route map is an associative array with path regexes as the keys. The
    #// value is an indexed array with the callback function/method as the first
    #// item, and a bitmask of HTTP methods as the second item (see the class
    #// constants).
    #// 
    #// Each route can be mapped to more than one callback by using an array of
    #// the indexed arrays. This allows mapping e.g. GET requests to one callback
    #// and POST requests to another.
    #// 
    #// Note that the path regexes (array keys) must have @ escaped, as this is
    #// used as the delimiter with preg_match()
    #// 
    #// @since 4.4.0
    #// @since 5.4.0 Add $namespace parameter.
    #// 
    #// @param string $namespace Optionally, only return routes in the given namespace.
    #// @return array `'/path/regex' => array( $callback, $bitmask )` or
    #// `'/path/regex' => array( array( $callback, $bitmask ), ...)`.
    #//
    def get_routes(self, namespace_=""):
        
        
        endpoints_ = self.endpoints
        if namespace_:
            endpoints_ = wp_list_filter(endpoints_, Array({"namespace": namespace_}))
        # end if
        #// 
        #// Filters the array of available endpoints.
        #// 
        #// @since 4.4.0
        #// 
        #// @param array $endpoints The available endpoints. An array of matching regex patterns, each mapped
        #// to an array of callbacks for the endpoint. These take the format
        #// `'/path/regex' => array( $callback, $bitmask )` or
        #// `'/path/regex' => array( array( $callback, $bitmask ).
        #//
        endpoints_ = apply_filters("rest_endpoints", endpoints_)
        #// Normalise the endpoints.
        defaults_ = Array({"methods": "", "accept_json": False, "accept_raw": False, "show_in_index": True, "args": Array()})
        for route_,handlers_ in endpoints_.items():
            if (php_isset(lambda : handlers_["callback"])):
                #// Single endpoint, add one deeper.
                handlers_ = Array(handlers_)
            # end if
            if (not (php_isset(lambda : self.route_options[route_]))):
                self.route_options[route_] = Array()
            # end if
            for key_,handler_ in handlers_.items():
                if (not php_is_numeric(key_)):
                    #// Route option, move it to the options.
                    self.route_options[route_][key_] = handler_
                    handlers_[key_] = None
                    continue
                # end if
                handler_ = wp_parse_args(handler_, defaults_)
                #// Allow comma-separated HTTP methods.
                if php_is_string(handler_["methods"]):
                    methods_ = php_explode(",", handler_["methods"])
                elif php_is_array(handler_["methods"]):
                    methods_ = handler_["methods"]
                else:
                    methods_ = Array()
                # end if
                handler_["methods"] = Array()
                for method_ in methods_:
                    method_ = php_strtoupper(php_trim(method_))
                    handler_["methods"][method_] = True
                # end for
            # end for
        # end for
        return endpoints_
    # end def get_routes
    #// 
    #// Retrieves namespaces registered on the server.
    #// 
    #// @since 4.4.0
    #// 
    #// @return string[] List of registered namespaces.
    #//
    def get_namespaces(self):
        
        
        return php_array_keys(self.namespaces)
    # end def get_namespaces
    #// 
    #// Retrieves specified options for a route.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $route Route pattern to fetch options for.
    #// @return array|null Data as an associative array if found, or null if not found.
    #//
    def get_route_options(self, route_=None):
        
        
        if (not (php_isset(lambda : self.route_options[route_]))):
            return None
        # end if
        return self.route_options[route_]
    # end def get_route_options
    #// 
    #// Matches the request to a callback and call it.
    #// 
    #// @since 4.4.0
    #// 
    #// @param WP_REST_Request $request Request to attempt dispatching.
    #// @return WP_REST_Response Response returned by the callback.
    #//
    def dispatch(self, request_=None):
        
        
        #// 
        #// Filters the pre-calculated result of a REST dispatch request.
        #// 
        #// Allow hijacking the request before dispatching by returning a non-empty. The returned value
        #// will be used to serve the request instead.
        #// 
        #// @since 4.4.0
        #// 
        #// @param mixed           $result  Response to replace the requested version with. Can be anything
        #// a normal endpoint can return, or null to not hijack the request.
        #// @param WP_REST_Server  $this    Server instance.
        #// @param WP_REST_Request $request Request used to generate the response.
        #//
        result_ = apply_filters("rest_pre_dispatch", None, self, request_)
        if (not php_empty(lambda : result_)):
            return result_
        # end if
        method_ = request_.get_method()
        path_ = request_.get_route()
        with_namespace_ = Array()
        for namespace_ in self.get_namespaces():
            if 0 == php_strpos(trailingslashit(php_ltrim(path_, "/")), namespace_):
                with_namespace_[-1] = self.get_routes(namespace_)
            # end if
        # end for
        if with_namespace_:
            routes_ = php_array_merge(with_namespace_)
        else:
            routes_ = self.get_routes()
        # end if
        for route_,handlers_ in routes_.items():
            match_ = php_preg_match("@^" + route_ + "$@i", path_, matches_)
            if (not match_):
                continue
            # end if
            args_ = Array()
            for param_,value_ in matches_.items():
                if (not php_is_int(param_)):
                    args_[param_] = value_
                # end if
            # end for
            for handler_ in handlers_:
                callback_ = handler_["callback"]
                response_ = None
                #// Fallback to GET method if no HEAD method is registered.
                checked_method_ = method_
                if "HEAD" == method_ and php_empty(lambda : handler_["methods"]["HEAD"]):
                    checked_method_ = "GET"
                # end if
                if php_empty(lambda : handler_["methods"][checked_method_]):
                    continue
                # end if
                if (not php_is_callable(callback_)):
                    response_ = php_new_class("WP_Error", lambda : WP_Error("rest_invalid_handler", __("The handler for the route is invalid"), Array({"status": 500})))
                # end if
                if (not is_wp_error(response_)):
                    args_[0] = None
                    request_.set_url_params(args_)
                    request_.set_attributes(handler_)
                    defaults_ = Array()
                    for arg_,options_ in handler_["args"].items():
                        if (php_isset(lambda : options_["default"])):
                            defaults_[arg_] = options_["default"]
                        # end if
                    # end for
                    request_.set_default_params(defaults_)
                    check_required_ = request_.has_valid_params()
                    if is_wp_error(check_required_):
                        response_ = check_required_
                    else:
                        check_sanitized_ = request_.sanitize_params()
                        if is_wp_error(check_sanitized_):
                            response_ = check_sanitized_
                        # end if
                    # end if
                # end if
                #// 
                #// Filters the response before executing any REST API callbacks.
                #// 
                #// Allows plugins to perform additional validation after a
                #// request is initialized and matched to a registered route,
                #// but before it is executed.
                #// 
                #// Note that this filter will not be called for requests that
                #// fail to authenticate or match to a registered route.
                #// 
                #// @since 4.7.0
                #// 
                #// @param WP_HTTP_Response|WP_Error $response Result to send to the client. Usually a WP_REST_Response or WP_Error.
                #// @param array                     $handler  Route handler used for the request.
                #// @param WP_REST_Request           $request  Request used to generate the response.
                #//
                response_ = apply_filters("rest_request_before_callbacks", response_, handler_, request_)
                if (not is_wp_error(response_)):
                    #// Check permission specified on the route.
                    if (not php_empty(lambda : handler_["permission_callback"])):
                        permission_ = php_call_user_func(handler_["permission_callback"], request_)
                        if is_wp_error(permission_):
                            response_ = permission_
                        elif False == permission_ or None == permission_:
                            response_ = php_new_class("WP_Error", lambda : WP_Error("rest_forbidden", __("Sorry, you are not allowed to do that."), Array({"status": rest_authorization_required_code()})))
                        # end if
                    # end if
                # end if
                if (not is_wp_error(response_)):
                    #// 
                    #// Filters the REST dispatch request result.
                    #// 
                    #// Allow plugins to override dispatching the request.
                    #// 
                    #// @since 4.4.0
                    #// @since 4.5.0 Added `$route` and `$handler` parameters.
                    #// 
                    #// @param mixed           $dispatch_result Dispatch result, will be used if not empty.
                    #// @param WP_REST_Request $request         Request used to generate the response.
                    #// @param string          $route           Route matched for the request.
                    #// @param array           $handler         Route handler used for the request.
                    #//
                    dispatch_result_ = apply_filters("rest_dispatch_request", None, request_, route_, handler_)
                    #// Allow plugins to halt the request via this filter.
                    if None != dispatch_result_:
                        response_ = dispatch_result_
                    else:
                        response_ = php_call_user_func(callback_, request_)
                    # end if
                # end if
                #// 
                #// Filters the response immediately after executing any REST API
                #// callbacks.
                #// 
                #// Allows plugins to perform any needed cleanup, for example,
                #// to undo changes made during the {@see 'rest_request_before_callbacks'}
                #// filter.
                #// 
                #// Note that this filter will not be called for requests that
                #// fail to authenticate or match to a registered route.
                #// 
                #// Note that an endpoint's `permission_callback` can still be
                #// called after this filter - see `rest_send_allow_header()`.
                #// 
                #// @since 4.7.0
                #// 
                #// @param WP_HTTP_Response|WP_Error $response Result to send to the client. Usually a WP_REST_Response or WP_Error.
                #// @param array                     $handler  Route handler used for the request.
                #// @param WP_REST_Request           $request  Request used to generate the response.
                #//
                response_ = apply_filters("rest_request_after_callbacks", response_, handler_, request_)
                if is_wp_error(response_):
                    response_ = self.error_to_response(response_)
                else:
                    response_ = rest_ensure_response(response_)
                # end if
                response_.set_matched_route(route_)
                response_.set_matched_handler(handler_)
                return response_
            # end for
        # end for
        return self.error_to_response(php_new_class("WP_Error", lambda : WP_Error("rest_no_route", __("No route was found matching the URL and request method"), Array({"status": 404}))))
    # end def dispatch
    #// 
    #// Returns if an error occurred during most recent JSON encode/decode.
    #// 
    #// Strings to be translated will be in format like
    #// "Encoding error: Maximum stack depth exceeded".
    #// 
    #// @since 4.4.0
    #// 
    #// @return bool|string Boolean false or string error message.
    #//
    def get_json_last_error(self):
        
        
        last_error_code_ = php_json_last_error()
        if JSON_ERROR_NONE == last_error_code_ or php_empty(lambda : last_error_code_):
            return False
        # end if
        return json_last_error_msg()
    # end def get_json_last_error
    #// 
    #// Retrieves the site index.
    #// 
    #// This endpoint describes the capabilities of the site.
    #// 
    #// @since 4.4.0
    #// 
    #// @param array $request {
    #// Request.
    #// 
    #// @type string $context Context.
    #// }
    #// @return WP_REST_Response The API root index data.
    #//
    def get_index(self, request_=None):
        
        
        #// General site data.
        available_ = Array({"name": get_option("blogname"), "description": get_option("blogdescription"), "url": get_option("siteurl"), "home": home_url(), "gmt_offset": get_option("gmt_offset"), "timezone_string": get_option("timezone_string"), "namespaces": php_array_keys(self.namespaces), "authentication": Array(), "routes": self.get_data_for_routes(self.get_routes(), request_["context"])})
        response_ = php_new_class("WP_REST_Response", lambda : WP_REST_Response(available_))
        response_.add_link("help", "http://v2.wp-api.org/")
        #// 
        #// Filters the API root index data.
        #// 
        #// This contains the data describing the API. This includes information
        #// about supported authentication schemes, supported namespaces, routes
        #// available on the API, and a small amount of data about the site.
        #// 
        #// @since 4.4.0
        #// 
        #// @param WP_REST_Response $response Response data.
        #//
        return apply_filters("rest_index", response_)
    # end def get_index
    #// 
    #// Retrieves the index for a namespace.
    #// 
    #// @since 4.4.0
    #// 
    #// @param WP_REST_Request $request REST request instance.
    #// @return WP_REST_Response|WP_Error WP_REST_Response instance if the index was found,
    #// WP_Error if the namespace isn't set.
    #//
    def get_namespace_index(self, request_=None):
        
        
        namespace_ = request_["namespace"]
        if (not (php_isset(lambda : self.namespaces[namespace_]))):
            return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_namespace", __("The specified namespace could not be found."), Array({"status": 404})))
        # end if
        routes_ = self.namespaces[namespace_]
        endpoints_ = php_array_intersect_key(self.get_routes(), routes_)
        data_ = Array({"namespace": namespace_, "routes": self.get_data_for_routes(endpoints_, request_["context"])})
        response_ = rest_ensure_response(data_)
        #// Link to the root index.
        response_.add_link("up", rest_url("/"))
        #// 
        #// Filters the namespace index data.
        #// 
        #// This typically is just the route data for the namespace, but you can
        #// add any data you'd like here.
        #// 
        #// @since 4.4.0
        #// 
        #// @param WP_REST_Response $response Response data.
        #// @param WP_REST_Request  $request  Request data. The namespace is passed as the 'namespace' parameter.
        #//
        return apply_filters("rest_namespace_index", response_, request_)
    # end def get_namespace_index
    #// 
    #// Retrieves the publicly-visible data for routes.
    #// 
    #// @since 4.4.0
    #// 
    #// @param array  $routes  Routes to get data for.
    #// @param string $context Optional. Context for data. Accepts 'view' or 'help'. Default 'view'.
    #// @return array[] Route data to expose in indexes, keyed by route.
    #//
    def get_data_for_routes(self, routes_=None, context_="view"):
        
        
        available_ = Array()
        #// Find the available routes.
        for route_,callbacks_ in routes_.items():
            data_ = self.get_data_for_route(route_, callbacks_, context_)
            if php_empty(lambda : data_):
                continue
            # end if
            #// 
            #// Filters the REST endpoint data.
            #// 
            #// @since 4.4.0
            #// 
            #// @param WP_REST_Request $request Request data. The namespace is passed as the 'namespace' parameter.
            #//
            available_[route_] = apply_filters("rest_endpoints_description", data_)
        # end for
        #// 
        #// Filters the publicly-visible data for routes.
        #// 
        #// This data is exposed on indexes and can be used by clients or
        #// developers to investigate the site and find out how to use it. It
        #// acts as a form of self-documentation.
        #// 
        #// @since 4.4.0
        #// 
        #// @param array[] $available Route data to expose in indexes, keyed by route.
        #// @param array   $routes    Internal route data as an associative array.
        #//
        return apply_filters("rest_route_data", available_, routes_)
    # end def get_data_for_routes
    #// 
    #// Retrieves publicly-visible data for the route.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $route     Route to get data for.
    #// @param array  $callbacks Callbacks to convert to data.
    #// @param string $context   Optional. Context for the data. Accepts 'view' or 'help'. Default 'view'.
    #// @return array|null Data for the route, or null if no publicly-visible data.
    #//
    def get_data_for_route(self, route_=None, callbacks_=None, context_="view"):
        
        
        data_ = Array({"namespace": "", "methods": Array(), "endpoints": Array()})
        if (php_isset(lambda : self.route_options[route_])):
            options_ = self.route_options[route_]
            if (php_isset(lambda : options_["namespace"])):
                data_["namespace"] = options_["namespace"]
            # end if
            if (php_isset(lambda : options_["schema"])) and "help" == context_:
                data_["schema"] = php_call_user_func(options_["schema"])
            # end if
        # end if
        route_ = php_preg_replace("#\\(\\?P<(\\w+?)>.*?\\)#", "{$1}", route_)
        for callback_ in callbacks_:
            #// Skip to the next route if any callback is hidden.
            if php_empty(lambda : callback_["show_in_index"]):
                continue
            # end if
            data_["methods"] = php_array_merge(data_["methods"], php_array_keys(callback_["methods"]))
            endpoint_data_ = Array({"methods": php_array_keys(callback_["methods"])})
            if (php_isset(lambda : callback_["args"])):
                endpoint_data_["args"] = Array()
                for key_,opts_ in callback_["args"].items():
                    arg_data_ = Array({"required": (not php_empty(lambda : opts_["required"]))})
                    if (php_isset(lambda : opts_["default"])):
                        arg_data_["default"] = opts_["default"]
                    # end if
                    if (php_isset(lambda : opts_["enum"])):
                        arg_data_["enum"] = opts_["enum"]
                    # end if
                    if (php_isset(lambda : opts_["description"])):
                        arg_data_["description"] = opts_["description"]
                    # end if
                    if (php_isset(lambda : opts_["type"])):
                        arg_data_["type"] = opts_["type"]
                    # end if
                    if (php_isset(lambda : opts_["items"])):
                        arg_data_["items"] = opts_["items"]
                    # end if
                    endpoint_data_["args"][key_] = arg_data_
                # end for
            # end if
            data_["endpoints"][-1] = endpoint_data_
            #// For non-variable routes, generate links.
            if php_strpos(route_, "{") == False:
                data_["_links"] = Array({"self": Array(Array({"href": rest_url(route_)}))})
            # end if
        # end for
        if php_empty(lambda : data_["methods"]):
            #// No methods supported, hide the route.
            return None
        # end if
        return data_
    # end def get_data_for_route
    #// 
    #// Sends an HTTP status code.
    #// 
    #// @since 4.4.0
    #// 
    #// @param int $code HTTP status.
    #//
    def set_status(self, code_=None):
        
        
        status_header(code_)
    # end def set_status
    #// 
    #// Sends an HTTP header.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $key Header key.
    #// @param string $value Header value.
    #//
    def send_header(self, key_=None, value_=None):
        
        
        #// 
        #// Sanitize as per RFC2616 (Section 4.2):
        #// 
        #// Any LWS that occurs between field-content MAY be replaced with a
        #// single SP before interpreting the field value or forwarding the
        #// message downstream.
        #//
        value_ = php_preg_replace("/\\s+/", " ", value_)
        php_header(php_sprintf("%s: %s", key_, value_))
    # end def send_header
    #// 
    #// Sends multiple HTTP headers.
    #// 
    #// @since 4.4.0
    #// 
    #// @param array $headers Map of header name to header value.
    #//
    def send_headers(self, headers_=None):
        
        
        for key_,value_ in headers_.items():
            self.send_header(key_, value_)
        # end for
    # end def send_headers
    #// 
    #// Removes an HTTP header from the current response.
    #// 
    #// @since 4.8.0
    #// 
    #// @param string $key Header key.
    #//
    def remove_header(self, key_=None):
        
        
        php_header_remove(key_)
    # end def remove_header
    #// 
    #// Retrieves the raw request entity (body).
    #// 
    #// @since 4.4.0
    #// 
    #// @global string $HTTP_RAW_POST_DATA Raw post data.
    #// 
    #// @return string Raw request data.
    #//
    @classmethod
    def get_raw_data(self):
        
        
        global HTTP_RAW_POST_DATA_
        php_check_if_defined("HTTP_RAW_POST_DATA_")
        #// 
        #// A bug in PHP < 5.2.2 makes $HTTP_RAW_POST_DATA not set by default,
        #// but we can do it ourself.
        #//
        if (not (php_isset(lambda : HTTP_RAW_POST_DATA_))):
            HTTP_RAW_POST_DATA_ = php_file_get_contents("php://input")
        # end if
        return HTTP_RAW_POST_DATA_
    # end def get_raw_data
    #// 
    #// Extracts headers from a PHP-style $_SERVER array.
    #// 
    #// @since 4.4.0
    #// 
    #// @param array $server Associative array similar to `$_SERVER`.
    #// @return array Headers extracted from the input.
    #//
    def get_headers(self, server_=None):
        
        
        headers_ = Array()
        #// CONTENT_* headers are not prefixed with HTTP_.
        additional_ = Array({"CONTENT_LENGTH": True, "CONTENT_MD5": True, "CONTENT_TYPE": True})
        for key_,value_ in server_.items():
            if php_strpos(key_, "HTTP_") == 0:
                headers_[php_substr(key_, 5)] = value_
            elif "REDIRECT_HTTP_AUTHORIZATION" == key_ and php_empty(lambda : server_["HTTP_AUTHORIZATION"]):
                #// 
                #// In some server configurations, the authorization header is passed in this alternate location.
                #// Since it would not be passed in in both places we do not check for both headers and resolve.
                #//
                headers_["AUTHORIZATION"] = value_
            elif (php_isset(lambda : additional_[key_])):
                headers_[key_] = value_
            # end if
        # end for
        return headers_
    # end def get_headers
# end class WP_REST_Server
