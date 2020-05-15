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
    namespaces = Array()
    endpoints = Array()
    route_options = Array()
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
    def error_to_response(self, error=None):
        
        error_data = error.get_error_data()
        if php_is_array(error_data) and (php_isset(lambda : error_data["status"])):
            status = error_data["status"]
        else:
            status = 500
        # end if
        errors = Array()
        for code,messages in error.errors:
            for message in messages:
                errors[-1] = Array({"code": code, "message": message, "data": error.get_error_data(code)})
            # end for
        # end for
        data = errors[0]
        if php_count(errors) > 1:
            #// Remove the primary error.
            php_array_shift(errors)
            data["additional_errors"] = errors
        # end if
        response = php_new_class("WP_REST_Response", lambda : WP_REST_Response(data, status))
        return response
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
    def json_error(self, code=None, message=None, status=None):
        
        if status:
            self.set_status(status)
        # end if
        error = compact("code", "message")
        return wp_json_encode(error)
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
    def serve_request(self, path=None):
        
        content_type = "application/javascript" if (php_isset(lambda : PHP_REQUEST["_jsonp"])) else "application/json"
        self.send_header("Content-Type", content_type + "; charset=" + get_option("blog_charset"))
        self.send_header("X-Robots-Tag", "noindex")
        api_root = get_rest_url()
        if (not php_empty(lambda : api_root)):
            self.send_header("Link", "<" + esc_url_raw(api_root) + ">; rel=\"https://api.w.org/\"")
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
        send_no_cache_headers = apply_filters("rest_send_nocache_headers", is_user_logged_in())
        if send_no_cache_headers:
            for header,header_value in wp_get_nocache_headers():
                if php_empty(lambda : header_value):
                    self.remove_header(header)
                else:
                    self.send_header(header, header_value)
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
        jsonp_enabled = apply_filters("rest_jsonp_enabled", True)
        jsonp_callback = None
        if (php_isset(lambda : PHP_REQUEST["_jsonp"])):
            if (not jsonp_enabled):
                php_print(self.json_error("rest_callback_disabled", __("JSONP support is disabled on this site."), 400))
                return False
            # end if
            jsonp_callback = PHP_REQUEST["_jsonp"]
            if (not wp_check_jsonp_callback(jsonp_callback)):
                php_print(self.json_error("rest_callback_invalid", __("Invalid JSONP callback function."), 400))
                return False
            # end if
        # end if
        if php_empty(lambda : path):
            if (php_isset(lambda : PHP_SERVER["PATH_INFO"])):
                path = PHP_SERVER["PATH_INFO"]
            else:
                path = "/"
            # end if
        # end if
        request = php_new_class("WP_REST_Request", lambda : WP_REST_Request(PHP_SERVER["REQUEST_METHOD"], path))
        request.set_query_params(wp_unslash(PHP_REQUEST))
        request.set_body_params(wp_unslash(PHP_POST))
        request.set_file_params(PHP_FILES)
        request.set_headers(self.get_headers(wp_unslash(PHP_SERVER)))
        request.set_body(self.get_raw_data())
        #// 
        #// HTTP method override for clients that can't use PUT/PATCH/DELETE. First, we check
        #// $_GET['_method']. If that is not set, we check for the HTTP_X_HTTP_METHOD_OVERRIDE
        #// header.
        #//
        if (php_isset(lambda : PHP_REQUEST["_method"])):
            request.set_method(PHP_REQUEST["_method"])
        elif (php_isset(lambda : PHP_SERVER["HTTP_X_HTTP_METHOD_OVERRIDE"])):
            request.set_method(PHP_SERVER["HTTP_X_HTTP_METHOD_OVERRIDE"])
        # end if
        result = self.check_authentication()
        if (not is_wp_error(result)):
            result = self.dispatch(request)
        # end if
        #// Normalize to either WP_Error or WP_REST_Response...
        result = rest_ensure_response(result)
        #// ...then convert WP_Error across.
        if is_wp_error(result):
            result = self.error_to_response(result)
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
        result = apply_filters("rest_post_dispatch", rest_ensure_response(result), self, request)
        #// Wrap the response in an envelope if asked for.
        if (php_isset(lambda : PHP_REQUEST["_envelope"])):
            result = self.envelope_response(result, (php_isset(lambda : PHP_REQUEST["_embed"])))
        # end if
        #// Send extra data from response objects.
        headers = result.get_headers()
        self.send_headers(headers)
        code = result.get_status()
        self.set_status(code)
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
        served = apply_filters("rest_pre_serve_request", False, result, request, self)
        if (not served):
            if "HEAD" == request.get_method():
                return None
            # end if
            #// Embed links inside the request.
            embed = rest_parse_embed_param(PHP_REQUEST["_embed"]) if (php_isset(lambda : PHP_REQUEST["_embed"])) else False
            result = self.response_to_data(result, embed)
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
            result = apply_filters("rest_pre_echo_response", result, self, request)
            #// The 204 response shouldn't have a body.
            if 204 == code or None == result:
                return None
            # end if
            result = wp_json_encode(result)
            json_error_message = self.get_json_last_error()
            if json_error_message:
                json_error_obj = php_new_class("WP_Error", lambda : WP_Error("rest_encode_error", json_error_message, Array({"status": 500})))
                result = self.error_to_response(json_error_obj)
                result = wp_json_encode(result.data[0])
            # end if
            if jsonp_callback:
                #// Prepend '/**/' to mitigate possible JSONP Flash attacks.
                #// https://miki.it/blog/2014/7/8/abusing-jsonp-with-rosetta-flash
                php_print("/**/" + jsonp_callback + "(" + result + ")")
            else:
                php_print(result)
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
    def response_to_data(self, response=None, embed=None):
        
        data = response.get_data()
        links = self.get_compact_response_links(response)
        if (not php_empty(lambda : links)):
            #// Convert links to part of the data.
            data["_links"] = links
        # end if
        if embed:
            self.embed_cache = Array()
            #// Determine if this is a numeric array.
            if wp_is_numeric_array(data):
                for key,item in data:
                    data[key] = self.embed_links(item, embed)
                # end for
            else:
                data = self.embed_links(data, embed)
            # end if
            self.embed_cache = Array()
        # end if
        return data
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
    def get_response_links(self, response=None):
        
        links = response.get_links()
        if php_empty(lambda : links):
            return Array()
        # end if
        #// Convert links to part of the data.
        data = Array()
        for rel,items in links:
            data[rel] = Array()
            for item in items:
                attributes = item["attributes"]
                attributes["href"] = item["href"]
                data[rel][-1] = attributes
            # end for
        # end for
        return data
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
    def get_compact_response_links(self, response=None):
        
        links = self.get_response_links(response)
        if php_empty(lambda : links):
            return Array()
        # end if
        curies = response.get_curies()
        used_curies = Array()
        for rel,items in links:
            #// Convert $rel URIs to their compact versions if they exist.
            for curie in curies:
                href_prefix = php_substr(curie["href"], 0, php_strpos(curie["href"], "{rel}"))
                if php_strpos(rel, href_prefix) != 0:
                    continue
                # end if
                #// Relation now changes from '$uri' to '$curie:$relation'.
                rel_regex = php_str_replace("\\{rel\\}", "(.+)", preg_quote(curie["href"], "!"))
                php_preg_match("!" + rel_regex + "!", rel, matches)
                if matches:
                    new_rel = curie["name"] + ":" + matches[1]
                    used_curies[curie["name"]] = curie
                    links[new_rel] = items
                    links[rel] = None
                    break
                # end if
            # end for
        # end for
        #// Push the curies onto the start of the links array.
        if used_curies:
            links["curies"] = php_array_values(used_curies)
        # end if
        return links
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
    def embed_links(self, data=None, embed=True):
        
        if php_empty(lambda : data["_links"]):
            return data
        # end if
        embedded = Array()
        for rel,links in data["_links"]:
            #// If a list of relations was specified, and the link relation is not in the whitelist, don't process the link.
            if php_is_array(embed) and (not php_in_array(rel, embed, True)):
                continue
            # end if
            embeds = Array()
            for item in links:
                #// Determine if the link is embeddable.
                if php_empty(lambda : item["embeddable"]):
                    #// Ensure we keep the same order.
                    embeds[-1] = Array()
                    continue
                # end if
                if (not php_array_key_exists(item["href"], self.embed_cache)):
                    #// Run through our internal routing and serve.
                    request = WP_REST_Request.from_url(item["href"])
                    if (not request):
                        embeds[-1] = Array()
                        continue
                    # end if
                    #// Embedded resources get passed context=embed.
                    if php_empty(lambda : request["context"]):
                        request["context"] = "embed"
                    # end if
                    response = self.dispatch(request)
                    #// This filter is documented in wp-includes/rest-api/class-wp-rest-server.php
                    response = apply_filters("rest_post_dispatch", rest_ensure_response(response), self, request)
                    self.embed_cache[item["href"]] = self.response_to_data(response, False)
                # end if
                embeds[-1] = self.embed_cache[item["href"]]
            # end for
            #// Determine if any real links were found.
            has_links = php_count(php_array_filter(embeds))
            if has_links:
                embedded[rel] = embeds
            # end if
        # end for
        if (not php_empty(lambda : embedded)):
            data["_embedded"] = embedded
        # end if
        return data
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
    def envelope_response(self, response=None, embed=None):
        
        envelope = Array({"body": self.response_to_data(response, embed), "status": response.get_status(), "headers": response.get_headers()})
        #// 
        #// Filters the enveloped form of a response.
        #// 
        #// @since 4.4.0
        #// 
        #// @param array            $envelope Envelope data.
        #// @param WP_REST_Response $response Original response data.
        #//
        envelope = apply_filters("rest_envelope_response", envelope, response)
        #// Ensure it's still a response and return.
        return rest_ensure_response(envelope)
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
    def register_route(self, namespace=None, route=None, route_args=None, override=False):
        
        if (not (php_isset(lambda : self.namespaces[namespace]))):
            self.namespaces[namespace] = Array()
            self.register_route(namespace, "/" + namespace, Array(Array({"methods": self.READABLE, "callback": Array(self, "get_namespace_index"), "args": Array({"namespace": Array({"default": namespace})}, {"context": Array({"default": "view"})})})))
        # end if
        #// Associative to avoid double-registration.
        self.namespaces[namespace][route] = True
        route_args["namespace"] = namespace
        if override or php_empty(lambda : self.endpoints[route]):
            self.endpoints[route] = route_args
        else:
            self.endpoints[route] = php_array_merge(self.endpoints[route], route_args)
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
    def get_routes(self, namespace=""):
        
        endpoints = self.endpoints
        if namespace:
            endpoints = wp_list_filter(endpoints, Array({"namespace": namespace}))
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
        endpoints = apply_filters("rest_endpoints", endpoints)
        #// Normalise the endpoints.
        defaults = Array({"methods": "", "accept_json": False, "accept_raw": False, "show_in_index": True, "args": Array()})
        for route,handlers in endpoints:
            if (php_isset(lambda : handlers["callback"])):
                #// Single endpoint, add one deeper.
                handlers = Array(handlers)
            # end if
            if (not (php_isset(lambda : self.route_options[route]))):
                self.route_options[route] = Array()
            # end if
            for key,handler in handlers:
                if (not php_is_numeric(key)):
                    #// Route option, move it to the options.
                    self.route_options[route][key] = handler
                    handlers[key] = None
                    continue
                # end if
                handler = wp_parse_args(handler, defaults)
                #// Allow comma-separated HTTP methods.
                if php_is_string(handler["methods"]):
                    methods = php_explode(",", handler["methods"])
                elif php_is_array(handler["methods"]):
                    methods = handler["methods"]
                else:
                    methods = Array()
                # end if
                handler["methods"] = Array()
                for method in methods:
                    method = php_strtoupper(php_trim(method))
                    handler["methods"][method] = True
                # end for
            # end for
        # end for
        return endpoints
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
    def get_route_options(self, route=None):
        
        if (not (php_isset(lambda : self.route_options[route]))):
            return None
        # end if
        return self.route_options[route]
    # end def get_route_options
    #// 
    #// Matches the request to a callback and call it.
    #// 
    #// @since 4.4.0
    #// 
    #// @param WP_REST_Request $request Request to attempt dispatching.
    #// @return WP_REST_Response Response returned by the callback.
    #//
    def dispatch(self, request=None):
        
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
        result = apply_filters("rest_pre_dispatch", None, self, request)
        if (not php_empty(lambda : result)):
            return result
        # end if
        method = request.get_method()
        path = request.get_route()
        with_namespace = Array()
        for namespace in self.get_namespaces():
            if 0 == php_strpos(trailingslashit(php_ltrim(path, "/")), namespace):
                with_namespace[-1] = self.get_routes(namespace)
            # end if
        # end for
        if with_namespace:
            routes = php_array_merge(with_namespace)
        else:
            routes = self.get_routes()
        # end if
        for route,handlers in routes:
            match = php_preg_match("@^" + route + "$@i", path, matches)
            if (not match):
                continue
            # end if
            args = Array()
            for param,value in matches:
                if (not php_is_int(param)):
                    args[param] = value
                # end if
            # end for
            for handler in handlers:
                callback = handler["callback"]
                response = None
                #// Fallback to GET method if no HEAD method is registered.
                checked_method = method
                if "HEAD" == method and php_empty(lambda : handler["methods"]["HEAD"]):
                    checked_method = "GET"
                # end if
                if php_empty(lambda : handler["methods"][checked_method]):
                    continue
                # end if
                if (not php_is_callable(callback)):
                    response = php_new_class("WP_Error", lambda : WP_Error("rest_invalid_handler", __("The handler for the route is invalid"), Array({"status": 500})))
                # end if
                if (not is_wp_error(response)):
                    args[0] = None
                    request.set_url_params(args)
                    request.set_attributes(handler)
                    defaults = Array()
                    for arg,options in handler["args"]:
                        if (php_isset(lambda : options["default"])):
                            defaults[arg] = options["default"]
                        # end if
                    # end for
                    request.set_default_params(defaults)
                    check_required = request.has_valid_params()
                    if is_wp_error(check_required):
                        response = check_required
                    else:
                        check_sanitized = request.sanitize_params()
                        if is_wp_error(check_sanitized):
                            response = check_sanitized
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
                response = apply_filters("rest_request_before_callbacks", response, handler, request)
                if (not is_wp_error(response)):
                    #// Check permission specified on the route.
                    if (not php_empty(lambda : handler["permission_callback"])):
                        permission = php_call_user_func(handler["permission_callback"], request)
                        if is_wp_error(permission):
                            response = permission
                        elif False == permission or None == permission:
                            response = php_new_class("WP_Error", lambda : WP_Error("rest_forbidden", __("Sorry, you are not allowed to do that."), Array({"status": rest_authorization_required_code()})))
                        # end if
                    # end if
                # end if
                if (not is_wp_error(response)):
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
                    dispatch_result = apply_filters("rest_dispatch_request", None, request, route, handler)
                    #// Allow plugins to halt the request via this filter.
                    if None != dispatch_result:
                        response = dispatch_result
                    else:
                        response = php_call_user_func(callback, request)
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
                response = apply_filters("rest_request_after_callbacks", response, handler, request)
                if is_wp_error(response):
                    response = self.error_to_response(response)
                else:
                    response = rest_ensure_response(response)
                # end if
                response.set_matched_route(route)
                response.set_matched_handler(handler)
                return response
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
        
        last_error_code = php_json_last_error()
        if JSON_ERROR_NONE == last_error_code or php_empty(lambda : last_error_code):
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
    def get_index(self, request=None):
        
        #// General site data.
        available = Array({"name": get_option("blogname"), "description": get_option("blogdescription"), "url": get_option("siteurl"), "home": home_url(), "gmt_offset": get_option("gmt_offset"), "timezone_string": get_option("timezone_string"), "namespaces": php_array_keys(self.namespaces), "authentication": Array(), "routes": self.get_data_for_routes(self.get_routes(), request["context"])})
        response = php_new_class("WP_REST_Response", lambda : WP_REST_Response(available))
        response.add_link("help", "http://v2.wp-api.org/")
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
        return apply_filters("rest_index", response)
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
    def get_namespace_index(self, request=None):
        
        namespace = request["namespace"]
        if (not (php_isset(lambda : self.namespaces[namespace]))):
            return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_namespace", __("The specified namespace could not be found."), Array({"status": 404})))
        # end if
        routes = self.namespaces[namespace]
        endpoints = php_array_intersect_key(self.get_routes(), routes)
        data = Array({"namespace": namespace, "routes": self.get_data_for_routes(endpoints, request["context"])})
        response = rest_ensure_response(data)
        #// Link to the root index.
        response.add_link("up", rest_url("/"))
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
        return apply_filters("rest_namespace_index", response, request)
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
    def get_data_for_routes(self, routes=None, context="view"):
        
        available = Array()
        #// Find the available routes.
        for route,callbacks in routes:
            data = self.get_data_for_route(route, callbacks, context)
            if php_empty(lambda : data):
                continue
            # end if
            #// 
            #// Filters the REST endpoint data.
            #// 
            #// @since 4.4.0
            #// 
            #// @param WP_REST_Request $request Request data. The namespace is passed as the 'namespace' parameter.
            #//
            available[route] = apply_filters("rest_endpoints_description", data)
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
        return apply_filters("rest_route_data", available, routes)
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
    def get_data_for_route(self, route=None, callbacks=None, context="view"):
        
        data = Array({"namespace": "", "methods": Array(), "endpoints": Array()})
        if (php_isset(lambda : self.route_options[route])):
            options = self.route_options[route]
            if (php_isset(lambda : options["namespace"])):
                data["namespace"] = options["namespace"]
            # end if
            if (php_isset(lambda : options["schema"])) and "help" == context:
                data["schema"] = php_call_user_func(options["schema"])
            # end if
        # end if
        route = php_preg_replace("#\\(\\?P<(\\w+?)>.*?\\)#", "{$1}", route)
        for callback in callbacks:
            #// Skip to the next route if any callback is hidden.
            if php_empty(lambda : callback["show_in_index"]):
                continue
            # end if
            data["methods"] = php_array_merge(data["methods"], php_array_keys(callback["methods"]))
            endpoint_data = Array({"methods": php_array_keys(callback["methods"])})
            if (php_isset(lambda : callback["args"])):
                endpoint_data["args"] = Array()
                for key,opts in callback["args"]:
                    arg_data = Array({"required": (not php_empty(lambda : opts["required"]))})
                    if (php_isset(lambda : opts["default"])):
                        arg_data["default"] = opts["default"]
                    # end if
                    if (php_isset(lambda : opts["enum"])):
                        arg_data["enum"] = opts["enum"]
                    # end if
                    if (php_isset(lambda : opts["description"])):
                        arg_data["description"] = opts["description"]
                    # end if
                    if (php_isset(lambda : opts["type"])):
                        arg_data["type"] = opts["type"]
                    # end if
                    if (php_isset(lambda : opts["items"])):
                        arg_data["items"] = opts["items"]
                    # end if
                    endpoint_data["args"][key] = arg_data
                # end for
            # end if
            data["endpoints"][-1] = endpoint_data
            #// For non-variable routes, generate links.
            if php_strpos(route, "{") == False:
                data["_links"] = Array({"self": Array(Array({"href": rest_url(route)}))})
            # end if
        # end for
        if php_empty(lambda : data["methods"]):
            #// No methods supported, hide the route.
            return None
        # end if
        return data
    # end def get_data_for_route
    #// 
    #// Sends an HTTP status code.
    #// 
    #// @since 4.4.0
    #// 
    #// @param int $code HTTP status.
    #//
    def set_status(self, code=None):
        
        status_header(code)
    # end def set_status
    #// 
    #// Sends an HTTP header.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $key Header key.
    #// @param string $value Header value.
    #//
    def send_header(self, key=None, value=None):
        
        #// 
        #// Sanitize as per RFC2616 (Section 4.2):
        #// 
        #// Any LWS that occurs between field-content MAY be replaced with a
        #// single SP before interpreting the field value or forwarding the
        #// message downstream.
        #//
        value = php_preg_replace("/\\s+/", " ", value)
        php_header(php_sprintf("%s: %s", key, value))
    # end def send_header
    #// 
    #// Sends multiple HTTP headers.
    #// 
    #// @since 4.4.0
    #// 
    #// @param array $headers Map of header name to header value.
    #//
    def send_headers(self, headers=None):
        
        for key,value in headers:
            self.send_header(key, value)
        # end for
    # end def send_headers
    #// 
    #// Removes an HTTP header from the current response.
    #// 
    #// @since 4.8.0
    #// 
    #// @param string $key Header key.
    #//
    def remove_header(self, key=None):
        
        php_header_remove(key)
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
        
        global HTTP_RAW_POST_DATA
        php_check_if_defined("HTTP_RAW_POST_DATA")
        #// 
        #// A bug in PHP < 5.2.2 makes $HTTP_RAW_POST_DATA not set by default,
        #// but we can do it ourself.
        #//
        if (not (php_isset(lambda : HTTP_RAW_POST_DATA))):
            HTTP_RAW_POST_DATA = php_file_get_contents("php://input")
        # end if
        return HTTP_RAW_POST_DATA
    # end def get_raw_data
    #// 
    #// Extracts headers from a PHP-style $_SERVER array.
    #// 
    #// @since 4.4.0
    #// 
    #// @param array $server Associative array similar to `$_SERVER`.
    #// @return array Headers extracted from the input.
    #//
    def get_headers(self, server=None):
        
        headers = Array()
        #// CONTENT_* headers are not prefixed with HTTP_.
        additional = Array({"CONTENT_LENGTH": True, "CONTENT_MD5": True, "CONTENT_TYPE": True})
        for key,value in server:
            if php_strpos(key, "HTTP_") == 0:
                headers[php_substr(key, 5)] = value
            elif "REDIRECT_HTTP_AUTHORIZATION" == key and php_empty(lambda : server["HTTP_AUTHORIZATION"]):
                #// 
                #// In some server configurations, the authorization header is passed in this alternate location.
                #// Since it would not be passed in in both places we do not check for both headers and resolve.
                #//
                headers["AUTHORIZATION"] = value
            elif (php_isset(lambda : additional[key])):
                headers[key] = value
            # end if
        # end for
        return headers
    # end def get_headers
# end class WP_REST_Server
