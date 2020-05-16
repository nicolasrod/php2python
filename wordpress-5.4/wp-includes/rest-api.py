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
#// REST API functions.
#// 
#// @package WordPress
#// @subpackage REST_API
#// @since 4.4.0
#// 
#// 
#// Version number for our API.
#// 
#// @var string
#//
php_define("REST_API_VERSION", "2.0")
#// 
#// Registers a REST API route.
#// 
#// Note: Do not use before the {@see 'rest_api_init'} hook.
#// 
#// @since 4.4.0
#// @since 5.1.0 Added a _doing_it_wrong() notice when not called on or after the rest_api_init hook.
#// 
#// @param string $namespace The first URL segment after core prefix. Should be unique to your package/plugin.
#// @param string $route     The base URL for route you are adding.
#// @param array  $args      Optional. Either an array of options for the endpoint, or an array of arrays for
#// multiple methods. Default empty array.
#// @param bool   $override  Optional. If the route already exists, should we override it? True overrides,
#// false merges (with newer overriding if duplicate keys exist). Default false.
#// @return bool True on success, false on error.
#//
def register_rest_route(namespace=None, route=None, args=Array(), override=False, *args_):
    
    if php_empty(lambda : namespace):
        #// 
        #// Non-namespaced routes are not allowed, with the exception of the main
        #// and namespace indexes. If you really need to register a
        #// non-namespaced route, call `WP_REST_Server::register_route` directly.
        #//
        _doing_it_wrong("register_rest_route", __("Routes must be namespaced with plugin or theme name and version."), "4.4.0")
        return False
    elif php_empty(lambda : route):
        _doing_it_wrong("register_rest_route", __("Route must be specified."), "4.4.0")
        return False
    # end if
    if (not did_action("rest_api_init")):
        _doing_it_wrong("register_rest_route", php_sprintf(__("REST API routes must be registered on the %s action."), "<code>rest_api_init</code>"), "5.1.0")
    # end if
    if (php_isset(lambda : args["args"])):
        common_args = args["args"]
        args["args"] = None
    else:
        common_args = Array()
    # end if
    if (php_isset(lambda : args["callback"])):
        #// Upgrade a single set to multiple.
        args = Array(args)
    # end if
    defaults = Array({"methods": "GET", "callback": None, "args": Array()})
    for key,arg_group in args:
        if (not php_is_numeric(key)):
            continue
        # end if
        arg_group = php_array_merge(defaults, arg_group)
        arg_group["args"] = php_array_merge(common_args, arg_group["args"])
    # end for
    full_route = "/" + php_trim(namespace, "/") + "/" + php_trim(route, "/")
    rest_get_server().register_route(namespace, full_route, args, override)
    return True
# end def register_rest_route
#// 
#// Registers a new field on an existing WordPress object type.
#// 
#// @since 4.7.0
#// 
#// @global array $wp_rest_additional_fields Holds registered fields, organized
#// by object type.
#// 
#// @param string|array $object_type Object(s) the field is being registered
#// to, "post"|"term"|"comment" etc.
#// @param string $attribute         The attribute name.
#// @param array  $args {
#// Optional. An array of arguments used to handle the registered field.
#// 
#// @type callable|null $get_callback    Optional. The callback function used to retrieve the field value. Default is
#// 'null', the field will not be returned in the response. The function will
#// be passed the prepared object data.
#// @type callable|null $update_callback Optional. The callback function used to set and update the field value. Default
#// is 'null', the value cannot be set or updated. The function will be passed
#// the model object, like WP_Post.
#// @type array|null $schema             Optional. The callback function used to create the schema for this field.
#// Default is 'null', no schema entry will be returned.
#// }
#//
def register_rest_field(object_type=None, attribute=None, args=Array(), *args_):
    
    defaults = Array({"get_callback": None, "update_callback": None, "schema": None})
    args = wp_parse_args(args, defaults)
    global wp_rest_additional_fields
    php_check_if_defined("wp_rest_additional_fields")
    object_types = object_type
    for object_type in object_types:
        wp_rest_additional_fields[object_type][attribute] = args
    # end for
# end def register_rest_field
#// 
#// Registers rewrite rules for the API.
#// 
#// @since 4.4.0
#// 
#// @see rest_api_register_rewrites()
#// @global WP $wp Current WordPress environment instance.
#//
def rest_api_init(*args_):
    
    rest_api_register_rewrites()
    global wp
    php_check_if_defined("wp")
    wp.add_query_var("rest_route")
# end def rest_api_init
#// 
#// Adds REST rewrite rules.
#// 
#// @since 4.4.0
#// 
#// @see add_rewrite_rule()
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#//
def rest_api_register_rewrites(*args_):
    
    global wp_rewrite
    php_check_if_defined("wp_rewrite")
    add_rewrite_rule("^" + rest_get_url_prefix() + "/?$", "index.php?rest_route=/", "top")
    add_rewrite_rule("^" + rest_get_url_prefix() + "/(.*)?", "index.php?rest_route=/$matches[1]", "top")
    add_rewrite_rule("^" + wp_rewrite.index + "/" + rest_get_url_prefix() + "/?$", "index.php?rest_route=/", "top")
    add_rewrite_rule("^" + wp_rewrite.index + "/" + rest_get_url_prefix() + "/(.*)?", "index.php?rest_route=/$matches[1]", "top")
# end def rest_api_register_rewrites
#// 
#// Registers the default REST API filters.
#// 
#// Attached to the {@see 'rest_api_init'} action
#// to make testing and disabling these filters easier.
#// 
#// @since 4.4.0
#//
def rest_api_default_filters(*args_):
    
    #// Deprecated reporting.
    add_action("deprecated_function_run", "rest_handle_deprecated_function", 10, 3)
    add_filter("deprecated_function_trigger_error", "__return_false")
    add_action("deprecated_argument_run", "rest_handle_deprecated_argument", 10, 3)
    add_filter("deprecated_argument_trigger_error", "__return_false")
    #// Default serving.
    add_filter("rest_pre_serve_request", "rest_send_cors_headers")
    add_filter("rest_post_dispatch", "rest_send_allow_header", 10, 3)
    add_filter("rest_post_dispatch", "rest_filter_response_fields", 10, 3)
    add_filter("rest_pre_dispatch", "rest_handle_options_request", 10, 3)
# end def rest_api_default_filters
#// 
#// Registers default REST API routes.
#// 
#// @since 4.7.0
#//
def create_initial_rest_routes(*args_):
    
    for post_type in get_post_types(Array({"show_in_rest": True}), "objects"):
        controller = post_type.get_rest_controller()
        if (not controller):
            continue
        # end if
        controller.register_routes()
        if post_type_supports(post_type.name, "revisions"):
            revisions_controller = php_new_class("WP_REST_Revisions_Controller", lambda : WP_REST_Revisions_Controller(post_type.name))
            revisions_controller.register_routes()
        # end if
        if "attachment" != post_type.name:
            autosaves_controller = php_new_class("WP_REST_Autosaves_Controller", lambda : WP_REST_Autosaves_Controller(post_type.name))
            autosaves_controller.register_routes()
        # end if
    # end for
    #// Post types.
    controller = php_new_class("WP_REST_Post_Types_Controller", lambda : WP_REST_Post_Types_Controller())
    controller.register_routes()
    #// Post statuses.
    controller = php_new_class("WP_REST_Post_Statuses_Controller", lambda : WP_REST_Post_Statuses_Controller())
    controller.register_routes()
    #// Taxonomies.
    controller = php_new_class("WP_REST_Taxonomies_Controller", lambda : WP_REST_Taxonomies_Controller())
    controller.register_routes()
    #// Terms.
    for taxonomy in get_taxonomies(Array({"show_in_rest": True}), "object"):
        class_ = taxonomy.rest_controller_class if (not php_empty(lambda : taxonomy.rest_controller_class)) else "WP_REST_Terms_Controller"
        if (not php_class_exists(class_)):
            continue
        # end if
        controller = php_new_class(class_, lambda : {**locals(), **globals()}[class_](taxonomy.name))
        if (not is_subclass_of(controller, "WP_REST_Controller")):
            continue
        # end if
        controller.register_routes()
    # end for
    #// Users.
    controller = php_new_class("WP_REST_Users_Controller", lambda : WP_REST_Users_Controller())
    controller.register_routes()
    #// Comments.
    controller = php_new_class("WP_REST_Comments_Controller", lambda : WP_REST_Comments_Controller())
    controller.register_routes()
    #// 
    #// Filters the search handlers to use in the REST search controller.
    #// 
    #// @since 5.0.0
    #// 
    #// @param array $search_handlers List of search handlers to use in the controller. Each search
    #// handler instance must extend the `WP_REST_Search_Handler` class.
    #// Default is only a handler for posts.
    #//
    search_handlers = apply_filters("wp_rest_search_handlers", Array(php_new_class("WP_REST_Post_Search_Handler", lambda : WP_REST_Post_Search_Handler())))
    controller = php_new_class("WP_REST_Search_Controller", lambda : WP_REST_Search_Controller(search_handlers))
    controller.register_routes()
    #// Block Renderer.
    controller = php_new_class("WP_REST_Block_Renderer_Controller", lambda : WP_REST_Block_Renderer_Controller())
    controller.register_routes()
    #// Settings.
    controller = php_new_class("WP_REST_Settings_Controller", lambda : WP_REST_Settings_Controller())
    controller.register_routes()
    #// Themes.
    controller = php_new_class("WP_REST_Themes_Controller", lambda : WP_REST_Themes_Controller())
    controller.register_routes()
# end def create_initial_rest_routes
#// 
#// Loads the REST API.
#// 
#// @since 4.4.0
#// 
#// @global WP $wp Current WordPress environment instance.
#//
def rest_api_loaded(*args_):
    
    if php_empty(lambda : PHP_GLOBALS["wp"].query_vars["rest_route"]):
        return
    # end if
    #// 
    #// Whether this is a REST Request.
    #// 
    #// @since 4.4.0
    #// @var bool
    #//
    php_define("REST_REQUEST", True)
    #// Initialize the server.
    server = rest_get_server()
    #// Fire off the request.
    route = untrailingslashit(PHP_GLOBALS["wp"].query_vars["rest_route"])
    if php_empty(lambda : route):
        route = "/"
    # end if
    server.serve_request(route)
    #// We're done.
    php_exit(0)
# end def rest_api_loaded
#// 
#// Retrieves the URL prefix for any API resource.
#// 
#// @since 4.4.0
#// 
#// @return string Prefix.
#//
def rest_get_url_prefix(*args_):
    
    #// 
    #// Filters the REST URL prefix.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $prefix URL prefix. Default 'wp-json'.
    #//
    return apply_filters("rest_url_prefix", "wp-json")
# end def rest_get_url_prefix
#// 
#// Retrieves the URL to a REST endpoint on a site.
#// 
#// Note: The returned URL is NOT escaped.
#// 
#// @since 4.4.0
#// 
#// @todo Check if this is even necessary
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#// 
#// @param int    $blog_id Optional. Blog ID. Default of null returns URL for current blog.
#// @param string $path    Optional. REST route. Default '/'.
#// @param string $scheme  Optional. Sanitization scheme. Default 'rest'.
#// @return string Full URL to the endpoint.
#//
def get_rest_url(blog_id=None, path="/", scheme="rest", *args_):
    
    if php_empty(lambda : path):
        path = "/"
    # end if
    path = "/" + php_ltrim(path, "/")
    if is_multisite() and get_blog_option(blog_id, "permalink_structure") or get_option("permalink_structure"):
        global wp_rewrite
        php_check_if_defined("wp_rewrite")
        if wp_rewrite.using_index_permalinks():
            url = get_home_url(blog_id, wp_rewrite.index + "/" + rest_get_url_prefix(), scheme)
        else:
            url = get_home_url(blog_id, rest_get_url_prefix(), scheme)
        # end if
        url += path
    else:
        url = trailingslashit(get_home_url(blog_id, "", scheme))
        #// nginx only allows HTTP/1.0 methods when redirecting from / to /index.php.
        #// To work around this, we manually add index.php to the URL, avoiding the redirect.
        if "index.php" != php_substr(url, 9):
            url += "index.php"
        # end if
        url = add_query_arg("rest_route", path, url)
    # end if
    if is_ssl() and (php_isset(lambda : PHP_SERVER["SERVER_NAME"])):
        #// If the current host is the same as the REST URL host, force the REST URL scheme to HTTPS.
        if php_parse_url(get_home_url(blog_id), PHP_URL_HOST) == PHP_SERVER["SERVER_NAME"]:
            url = set_url_scheme(url, "https")
        # end if
    # end if
    if is_admin() and force_ssl_admin():
        #// 
        #// In this situation the home URL may be http:, and `is_ssl()` may be false,
        #// but the admin is served over https: (one way or another), so REST API usage
        #// will be blocked by browsers unless it is also served over HTTPS.
        #//
        url = set_url_scheme(url, "https")
    # end if
    #// 
    #// Filters the REST URL.
    #// 
    #// Use this filter to adjust the url returned by the get_rest_url() function.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $url     REST URL.
    #// @param string $path    REST route.
    #// @param int    $blog_id Blog ID.
    #// @param string $scheme  Sanitization scheme.
    #//
    return apply_filters("rest_url", url, path, blog_id, scheme)
# end def get_rest_url
#// 
#// Retrieves the URL to a REST endpoint.
#// 
#// Note: The returned URL is NOT escaped.
#// 
#// @since 4.4.0
#// 
#// @param string $path   Optional. REST route. Default empty.
#// @param string $scheme Optional. Sanitization scheme. Default 'rest'.
#// @return string Full URL to the endpoint.
#//
def rest_url(path="", scheme="rest", *args_):
    
    return get_rest_url(None, path, scheme)
# end def rest_url
#// 
#// Do a REST request.
#// 
#// Used primarily to route internal requests through WP_REST_Server.
#// 
#// @since 4.4.0
#// 
#// @param WP_REST_Request|string $request Request.
#// @return WP_REST_Response REST response.
#//
def rest_do_request(request=None, *args_):
    
    request = rest_ensure_request(request)
    return rest_get_server().dispatch(request)
# end def rest_do_request
#// 
#// Retrieves the current REST server instance.
#// 
#// Instantiates a new instance if none exists already.
#// 
#// @since 4.5.0
#// 
#// @global WP_REST_Server $wp_rest_server REST server instance.
#// 
#// @return WP_REST_Server REST server instance.
#//
def rest_get_server(*args_):
    
    #// @var WP_REST_Server $wp_rest_server
    global wp_rest_server
    php_check_if_defined("wp_rest_server")
    if php_empty(lambda : wp_rest_server):
        #// 
        #// Filters the REST Server Class.
        #// 
        #// This filter allows you to adjust the server class used by the API, using a
        #// different class to handle requests.
        #// 
        #// @since 4.4.0
        #// 
        #// @param string $class_name The name of the server class. Default 'WP_REST_Server'.
        #//
        wp_rest_server_class = apply_filters("wp_rest_server_class", "WP_REST_Server")
        wp_rest_server = php_new_class(wp_rest_server_class, lambda : {**locals(), **globals()}[wp_rest_server_class]())
        #// 
        #// Fires when preparing to serve an API request.
        #// 
        #// Endpoint objects should be created and register their hooks on this action rather
        #// than another action to ensure they're only loaded when needed.
        #// 
        #// @since 4.4.0
        #// 
        #// @param WP_REST_Server $wp_rest_server Server object.
        #//
        do_action("rest_api_init", wp_rest_server)
    # end if
    return wp_rest_server
# end def rest_get_server
#// 
#// Ensures request arguments are a request object (for consistency).
#// 
#// @since 4.4.0
#// @since 5.3.0 Accept string argument for the request path.
#// 
#// @param array|string|WP_REST_Request $request Request to check.
#// @return WP_REST_Request REST request instance.
#//
def rest_ensure_request(request=None, *args_):
    
    if type(request).__name__ == "WP_REST_Request":
        return request
    # end if
    if php_is_string(request):
        return php_new_class("WP_REST_Request", lambda : WP_REST_Request("GET", request))
    # end if
    return php_new_class("WP_REST_Request", lambda : WP_REST_Request("GET", "", request))
# end def rest_ensure_request
#// 
#// Ensures a REST response is a response object (for consistency).
#// 
#// This implements WP_HTTP_Response, allowing usage of `set_status`/`header`/etc
#// without needing to double-check the object. Will also allow WP_Error to indicate error
#// responses, so users should immediately check for this value.
#// 
#// @since 4.4.0
#// 
#// @param WP_HTTP_Response|WP_Error|mixed $response Response to check.
#// @return WP_REST_Response|mixed If response generated an error, WP_Error, if response
#// is already an instance, WP_HTTP_Response, otherwise
#// returns a new WP_REST_Response instance.
#//
def rest_ensure_response(response=None, *args_):
    
    if is_wp_error(response):
        return response
    # end if
    if type(response).__name__ == "WP_HTTP_Response":
        return response
    # end if
    return php_new_class("WP_REST_Response", lambda : WP_REST_Response(response))
# end def rest_ensure_response
#// 
#// Handles _deprecated_function() errors.
#// 
#// @since 4.4.0
#// 
#// @param string $function    The function that was called.
#// @param string $replacement The function that should have been called.
#// @param string $version     Version.
#//
def rest_handle_deprecated_function(function=None, replacement=None, version=None, *args_):
    
    if (not WP_DEBUG) or php_headers_sent():
        return
    # end if
    if (not php_empty(lambda : replacement)):
        #// translators: 1: Function name, 2: WordPress version number, 3: New function name.
        string = php_sprintf(__("%1$s (since %2$s; use %3$s instead)"), function, version, replacement)
    else:
        #// translators: 1: Function name, 2: WordPress version number.
        string = php_sprintf(__("%1$s (since %2$s; no alternative available)"), function, version)
    # end if
    php_header(php_sprintf("X-WP-DeprecatedFunction: %s", string))
# end def rest_handle_deprecated_function
#// 
#// Handles _deprecated_argument() errors.
#// 
#// @since 4.4.0
#// 
#// @param string $function    The function that was called.
#// @param string $message     A message regarding the change.
#// @param string $version     Version.
#//
def rest_handle_deprecated_argument(function=None, message=None, version=None, *args_):
    
    if (not WP_DEBUG) or php_headers_sent():
        return
    # end if
    if (not php_empty(lambda : message)):
        #// translators: 1: Function name, 2: WordPress version number, 3: Error message.
        string = php_sprintf(__("%1$s (since %2$s; %3$s)"), function, version, message)
    else:
        #// translators: 1: Function name, 2: WordPress version number.
        string = php_sprintf(__("%1$s (since %2$s; no alternative available)"), function, version)
    # end if
    php_header(php_sprintf("X-WP-DeprecatedParam: %s", string))
# end def rest_handle_deprecated_argument
#// 
#// Sends Cross-Origin Resource Sharing headers with API requests.
#// 
#// @since 4.4.0
#// 
#// @param mixed $value Response data.
#// @return mixed Response data.
#//
def rest_send_cors_headers(value=None, *args_):
    
    origin = get_http_origin()
    if origin:
        #// Requests from file:// and data: URLs send "Origin: null".
        if "null" != origin:
            origin = esc_url_raw(origin)
        # end if
        php_header("Access-Control-Allow-Origin: " + origin)
        php_header("Access-Control-Allow-Methods: OPTIONS, GET, POST, PUT, PATCH, DELETE")
        php_header("Access-Control-Allow-Credentials: true")
        php_header("Vary: Origin", False)
    elif (not php_headers_sent()) and "GET" == PHP_SERVER["REQUEST_METHOD"] and (not is_user_logged_in()):
        php_header("Vary: Origin", False)
    # end if
    return value
# end def rest_send_cors_headers
#// 
#// Handles OPTIONS requests for the server.
#// 
#// This is handled outside of the server code, as it doesn't obey normal route
#// mapping.
#// 
#// @since 4.4.0
#// 
#// @param mixed           $response Current response, either response or `null` to indicate pass-through.
#// @param WP_REST_Server  $handler  ResponseHandler instance (usually WP_REST_Server).
#// @param WP_REST_Request $request  The request that was used to make current response.
#// @return WP_REST_Response Modified response, either response or `null` to indicate pass-through.
#//
def rest_handle_options_request(response=None, handler=None, request=None, *args_):
    
    if (not php_empty(lambda : response)) or request.get_method() != "OPTIONS":
        return response
    # end if
    response = php_new_class("WP_REST_Response", lambda : WP_REST_Response())
    data = Array()
    for route,endpoints in handler.get_routes():
        match = php_preg_match("@^" + route + "$@i", request.get_route(), matches)
        if (not match):
            continue
        # end if
        args = Array()
        for param,value in matches:
            if (not php_is_int(param)):
                args[param] = value
            # end if
        # end for
        for endpoint in endpoints:
            args[0] = None
            request.set_url_params(args)
            request.set_attributes(endpoint)
        # end for
        data = handler.get_data_for_route(route, endpoints, "help")
        response.set_matched_route(route)
        break
    # end for
    response.set_data(data)
    return response
# end def rest_handle_options_request
#// 
#// Sends the "Allow" header to state all methods that can be sent to the current route.
#// 
#// @since 4.4.0
#// 
#// @param WP_REST_Response $response Current response being served.
#// @param WP_REST_Server   $server   ResponseHandler instance (usually WP_REST_Server).
#// @param WP_REST_Request  $request  The request that was used to make current response.
#// @return WP_REST_Response Response to be served, with "Allow" header if route has allowed methods.
#//
def rest_send_allow_header(response=None, server=None, request=None, *args_):
    
    matched_route = response.get_matched_route()
    if (not matched_route):
        return response
    # end if
    routes = server.get_routes()
    allowed_methods = Array()
    #// Get the allowed methods across the routes.
    for _handler in routes[matched_route]:
        for handler_method,value in _handler["methods"]:
            if (not php_empty(lambda : _handler["permission_callback"])):
                permission = php_call_user_func(_handler["permission_callback"], request)
                allowed_methods[handler_method] = True == permission
            else:
                allowed_methods[handler_method] = True
            # end if
        # end for
    # end for
    #// Strip out all the methods that are not allowed (false values).
    allowed_methods = php_array_filter(allowed_methods)
    if allowed_methods:
        response.header("Allow", php_implode(", ", php_array_map("strtoupper", php_array_keys(allowed_methods))))
    # end if
    return response
# end def rest_send_allow_header
#// 
#// Recursively computes the intersection of arrays using keys for comparison.
#// 
#// @param  array $array1 The array with master keys to check.
#// @param  array $array2 An array to compare keys against.
#// 
#// @return array An associative array containing all the entries of array1 which have keys that are present in all arguments.
#//
def _rest_array_intersect_key_recursive(array1=None, array2=None, *args_):
    
    array1 = php_array_intersect_key(array1, array2)
    for key,value in array1:
        if php_is_array(value) and php_is_array(array2[key]):
            array1[key] = _rest_array_intersect_key_recursive(value, array2[key])
        # end if
    # end for
    return array1
# end def _rest_array_intersect_key_recursive
#// 
#// Filter the API response to include only a white-listed set of response object fields.
#// 
#// @since 4.8.0
#// 
#// @param WP_REST_Response $response Current response being served.
#// @param WP_REST_Server   $server   ResponseHandler instance (usually WP_REST_Server).
#// @param WP_REST_Request  $request  The request that was used to make current response.
#// 
#// @return WP_REST_Response Response to be served, trimmed down to contain a subset of fields.
#//
def rest_filter_response_fields(response=None, server=None, request=None, *args_):
    
    if (not (php_isset(lambda : request["_fields"]))) or response.is_error():
        return response
    # end if
    data = response.get_data()
    fields = wp_parse_list(request["_fields"])
    if 0 == php_count(fields):
        return response
    # end if
    #// Trim off outside whitespace from the comma delimited list.
    fields = php_array_map("trim", fields)
    #// Create nested array of accepted field hierarchy.
    fields_as_keyed = Array()
    for field in fields:
        parts = php_explode(".", field)
        ref = fields_as_keyed
        while True:
            
            if not (php_count(parts) > 1):
                break
            # end if
            next = php_array_shift(parts)
            if (php_isset(lambda : ref[next])) and True == ref[next]:
                break
            # end if
            ref[next] = ref[next] if (php_isset(lambda : ref[next])) else Array()
            ref = ref[next]
        # end while
        last = php_array_shift(parts)
        ref[last] = True
    # end for
    if wp_is_numeric_array(data):
        new_data = Array()
        for item in data:
            new_data[-1] = _rest_array_intersect_key_recursive(item, fields_as_keyed)
        # end for
    else:
        new_data = _rest_array_intersect_key_recursive(data, fields_as_keyed)
    # end if
    response.set_data(new_data)
    return response
# end def rest_filter_response_fields
#// 
#// Given an array of fields to include in a response, some of which may be
#// `nested.fields`, determine whether the provided field should be included
#// in the response body.
#// 
#// If a parent field is passed in, the presence of any nested field within
#// that parent will cause the method to return `true`. For example "title"
#// will return true if any of `title`, `title.raw` or `title.rendered` is
#// provided.
#// 
#// @since 5.3.0
#// 
#// @param string $field  A field to test for inclusion in the response body.
#// @param array  $fields An array of string fields supported by the endpoint.
#// @return bool Whether to include the field or not.
#//
def rest_is_field_included(field=None, fields=None, *args_):
    
    if php_in_array(field, fields, True):
        return True
    # end if
    for accepted_field in fields:
        #// Check to see if $field is the parent of any item in $fields.
        #// A field "parent" should be accepted if "parent.child" is accepted.
        if php_strpos(accepted_field, str(field) + str(".")) == 0:
            return True
        # end if
        #// Conversely, if "parent" is accepted, all "parent.child" fields
        #// should also be accepted.
        if php_strpos(field, str(accepted_field) + str(".")) == 0:
            return True
        # end if
    # end for
    return False
# end def rest_is_field_included
#// 
#// Adds the REST API URL to the WP RSD endpoint.
#// 
#// @since 4.4.0
#// 
#// @see get_rest_url()
#//
def rest_output_rsd(*args_):
    
    api_root = get_rest_url()
    if php_empty(lambda : api_root):
        return
    # end if
    php_print(" <api name=\"WP-API\" blogID=\"1\" preferred=\"false\" apiLink=\"")
    php_print(esc_url(api_root))
    php_print("\" />\n  ")
# end def rest_output_rsd
#// 
#// Outputs the REST API link tag into page header.
#// 
#// @since 4.4.0
#// 
#// @see get_rest_url()
#//
def rest_output_link_wp_head(*args_):
    
    api_root = get_rest_url()
    if php_empty(lambda : api_root):
        return
    # end if
    php_print("<link rel='https://api.w.org/' href='" + esc_url(api_root) + "' />\n")
# end def rest_output_link_wp_head
#// 
#// Sends a Link header for the REST API.
#// 
#// @since 4.4.0
#//
def rest_output_link_header(*args_):
    
    if php_headers_sent():
        return
    # end if
    api_root = get_rest_url()
    if php_empty(lambda : api_root):
        return
    # end if
    php_header("Link: <" + esc_url_raw(api_root) + ">; rel=\"https://api.w.org/\"", False)
# end def rest_output_link_header
#// 
#// Checks for errors when using cookie-based authentication.
#// 
#// WordPress' built-in cookie authentication is always active
#// for logged in users. However, the API has to check nonces
#// for each request to ensure users are not vulnerable to CSRF.
#// 
#// @since 4.4.0
#// 
#// @global mixed          $wp_rest_auth_cookie
#// 
#// @param WP_Error|mixed $result Error from another authentication handler,
#// null if we should handle it, or another value if not.
#// @return WP_Error|mixed|bool WP_Error if the cookie is invalid, the $result, otherwise true.
#//
def rest_cookie_check_errors(result=None, *args_):
    
    if (not php_empty(lambda : result)):
        return result
    # end if
    global wp_rest_auth_cookie
    php_check_if_defined("wp_rest_auth_cookie")
    #// 
    #// Is cookie authentication being used? (If we get an auth
    #// error, but we're still logged in, another authentication
    #// must have been used).
    #//
    if True != wp_rest_auth_cookie and is_user_logged_in():
        return result
    # end if
    #// Determine if there is a nonce.
    nonce = None
    if (php_isset(lambda : PHP_REQUEST["_wpnonce"])):
        nonce = PHP_REQUEST["_wpnonce"]
    elif (php_isset(lambda : PHP_SERVER["HTTP_X_WP_NONCE"])):
        nonce = PHP_SERVER["HTTP_X_WP_NONCE"]
    # end if
    if None == nonce:
        #// No nonce at all, so act as if it's an unauthenticated request.
        wp_set_current_user(0)
        return True
    # end if
    #// Check the nonce.
    result = wp_verify_nonce(nonce, "wp_rest")
    if (not result):
        return php_new_class("WP_Error", lambda : WP_Error("rest_cookie_invalid_nonce", __("Cookie nonce is invalid"), Array({"status": 403})))
    # end if
    #// Send a refreshed nonce in header.
    rest_get_server().send_header("X-WP-Nonce", wp_create_nonce("wp_rest"))
    return True
# end def rest_cookie_check_errors
#// 
#// Collects cookie authentication status.
#// 
#// Collects errors from wp_validate_auth_cookie for use by rest_cookie_check_errors.
#// 
#// @since 4.4.0
#// 
#// @see current_action()
#// @global mixed $wp_rest_auth_cookie
#//
def rest_cookie_collect_status(*args_):
    
    global wp_rest_auth_cookie
    php_check_if_defined("wp_rest_auth_cookie")
    status_type = current_action()
    if "auth_cookie_valid" != status_type:
        wp_rest_auth_cookie = php_substr(status_type, 12)
        return
    # end if
    wp_rest_auth_cookie = True
# end def rest_cookie_collect_status
#// 
#// Parses an RFC3339 time into a Unix timestamp.
#// 
#// @since 4.4.0
#// 
#// @param string $date      RFC3339 timestamp.
#// @param bool   $force_utc Optional. Whether to force UTC timezone instead of using
#// the timestamp's timezone. Default false.
#// @return int Unix timestamp.
#//
def rest_parse_date(date=None, force_utc=False, *args_):
    
    if force_utc:
        date = php_preg_replace("/[+-]\\d+:?\\d+$/", "+00:00", date)
    # end if
    regex = "#^\\d{4}-\\d{2}-\\d{2}[Tt ]\\d{2}:\\d{2}:\\d{2}(?:\\.\\d+)?(?:Z|[+-]\\d{2}(?::\\d{2})?)?$#"
    if (not php_preg_match(regex, date, matches)):
        return False
    # end if
    return strtotime(date)
# end def rest_parse_date
#// 
#// Parses a date into both its local and UTC equivalent, in MySQL datetime format.
#// 
#// @since 4.4.0
#// 
#// @see rest_parse_date()
#// 
#// @param string $date   RFC3339 timestamp.
#// @param bool   $is_utc Whether the provided date should be interpreted as UTC. Default false.
#// @return array|null Local and UTC datetime strings, in MySQL datetime format (Y-m-d H:i:s),
#// null on failure.
#//
def rest_get_date_with_gmt(date=None, is_utc=False, *args_):
    
    #// 
    #// Whether or not the original date actually has a timezone string
    #// changes the way we need to do timezone conversion.
    #// Store this info before parsing the date, and use it later.
    #//
    has_timezone = php_preg_match("#(Z|[+-]\\d{2}(:\\d{2})?)$#", date)
    date = rest_parse_date(date)
    if php_empty(lambda : date):
        return None
    # end if
    #// 
    #// At this point $date could either be a local date (if we were passed
    #// a *local* date without a timezone offset) or a UTC date (otherwise).
    #// Timezone conversion needs to be handled differently between these two cases.
    #//
    if (not is_utc) and (not has_timezone):
        local = gmdate("Y-m-d H:i:s", date)
        utc = get_gmt_from_date(local)
    else:
        utc = gmdate("Y-m-d H:i:s", date)
        local = get_date_from_gmt(utc)
    # end if
    return Array(local, utc)
# end def rest_get_date_with_gmt
#// 
#// Returns a contextual HTTP error code for authorization failure.
#// 
#// @since 4.7.0
#// 
#// @return integer 401 if the user is not logged in, 403 if the user is logged in.
#//
def rest_authorization_required_code(*args_):
    
    return 403 if is_user_logged_in() else 401
# end def rest_authorization_required_code
#// 
#// Validate a request argument based on details registered to the route.
#// 
#// @since 4.7.0
#// 
#// @param  mixed            $value
#// @param  WP_REST_Request  $request
#// @param  string           $param
#// @return true|WP_Error
#//
def rest_validate_request_arg(value=None, request=None, param=None, *args_):
    
    attributes = request.get_attributes()
    if (not (php_isset(lambda : attributes["args"][param]))) or (not php_is_array(attributes["args"][param])):
        return True
    # end if
    args = attributes["args"][param]
    return rest_validate_value_from_schema(value, args, param)
# end def rest_validate_request_arg
#// 
#// Sanitize a request argument based on details registered to the route.
#// 
#// @since 4.7.0
#// 
#// @param  mixed            $value
#// @param  WP_REST_Request  $request
#// @param  string           $param
#// @return mixed
#//
def rest_sanitize_request_arg(value=None, request=None, param=None, *args_):
    
    attributes = request.get_attributes()
    if (not (php_isset(lambda : attributes["args"][param]))) or (not php_is_array(attributes["args"][param])):
        return value
    # end if
    args = attributes["args"][param]
    return rest_sanitize_value_from_schema(value, args)
# end def rest_sanitize_request_arg
#// 
#// Parse a request argument based on details registered to the route.
#// 
#// Runs a validation check and sanitizes the value, primarily to be used via
#// the `sanitize_callback` arguments in the endpoint args registration.
#// 
#// @since 4.7.0
#// 
#// @param  mixed            $value
#// @param  WP_REST_Request  $request
#// @param  string           $param
#// @return mixed
#//
def rest_parse_request_arg(value=None, request=None, param=None, *args_):
    
    is_valid = rest_validate_request_arg(value, request, param)
    if is_wp_error(is_valid):
        return is_valid
    # end if
    value = rest_sanitize_request_arg(value, request, param)
    return value
# end def rest_parse_request_arg
#// 
#// Determines if an IP address is valid.
#// 
#// Handles both IPv4 and IPv6 addresses.
#// 
#// @since 4.7.0
#// 
#// @param  string $ip IP address.
#// @return string|false The valid IP address, otherwise false.
#//
def rest_is_ip_address(ip=None, *args_):
    
    ipv4_pattern = "/^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/"
    if (not php_preg_match(ipv4_pattern, ip)) and (not Requests_IPv6.check_ipv6(ip)):
        return False
    # end if
    return ip
# end def rest_is_ip_address
#// 
#// Changes a boolean-like value into the proper boolean value.
#// 
#// @since 4.7.0
#// 
#// @param bool|string|int $value The value being evaluated.
#// @return boolean Returns the proper associated boolean value.
#//
def rest_sanitize_boolean(value=None, *args_):
    
    #// String values are translated to `true`; make sure 'false' is false.
    if php_is_string(value):
        value = php_strtolower(value)
        if php_in_array(value, Array("false", "0"), True):
            value = False
        # end if
    # end if
    #// Everything else will map nicely to boolean.
    return php_bool(value)
# end def rest_sanitize_boolean
#// 
#// Determines if a given value is boolean-like.
#// 
#// @since 4.7.0
#// 
#// @param bool|string $maybe_bool The value being evaluated.
#// @return boolean True if a boolean, otherwise false.
#//
def rest_is_boolean(maybe_bool=None, *args_):
    
    if php_is_bool(maybe_bool):
        return True
    # end if
    if php_is_string(maybe_bool):
        maybe_bool = php_strtolower(maybe_bool)
        valid_boolean_values = Array("false", "true", "0", "1")
        return php_in_array(maybe_bool, valid_boolean_values, True)
    # end if
    if php_is_int(maybe_bool):
        return php_in_array(maybe_bool, Array(0, 1), True)
    # end if
    return False
# end def rest_is_boolean
#// 
#// Retrieves the avatar urls in various sizes.
#// 
#// @since 4.7.0
#// 
#// @see get_avatar_url()
#// 
#// @param mixed $id_or_email The Gravatar to retrieve a URL for. Accepts a user_id, gravatar md5 hash,
#// user email, WP_User object, WP_Post object, or WP_Comment object.
#// @return array Avatar URLs keyed by size. Each value can be a URL string or boolean false.
#//
def rest_get_avatar_urls(id_or_email=None, *args_):
    
    avatar_sizes = rest_get_avatar_sizes()
    urls = Array()
    for size in avatar_sizes:
        urls[size] = get_avatar_url(id_or_email, Array({"size": size}))
    # end for
    return urls
# end def rest_get_avatar_urls
#// 
#// Retrieves the pixel sizes for avatars.
#// 
#// @since 4.7.0
#// 
#// @return int[] List of pixel sizes for avatars. Default `[ 24, 48, 96 ]`.
#//
def rest_get_avatar_sizes(*args_):
    
    #// 
    #// Filters the REST avatar sizes.
    #// 
    #// Use this filter to adjust the array of sizes returned by the
    #// `rest_get_avatar_sizes` function.
    #// 
    #// @since 4.4.0
    #// 
    #// @param int[] $sizes An array of int values that are the pixel sizes for avatars.
    #// Default `[ 24, 48, 96 ]`.
    #//
    return apply_filters("rest_avatar_sizes", Array(24, 48, 96))
# end def rest_get_avatar_sizes
#// 
#// Validate a value based on a schema.
#// 
#// @since 4.7.0
#// 
#// @param mixed  $value The value to validate.
#// @param array  $args  Schema array to use for validation.
#// @param string $param The parameter name, used in error messages.
#// @return true|WP_Error
#//
def rest_validate_value_from_schema(value=None, args=None, param="", *args_):
    
    if php_is_array(args["type"]):
        for type in args["type"]:
            type_args = args
            type_args["type"] = type
            if True == rest_validate_value_from_schema(value, type_args, param):
                return True
            # end if
        # end for
        #// translators: 1: Parameter, 2: List of types.
        return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s is not of type %2$s."), param, php_implode(",", args["type"]))))
    # end if
    if "array" == args["type"]:
        if (not is_null(value)):
            value = wp_parse_list(value)
        # end if
        if (not wp_is_numeric_array(value)):
            #// translators: 1: Parameter, 2: Type name.
            return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s is not of type %2$s."), param, "array")))
        # end if
        for index,v in value:
            is_valid = rest_validate_value_from_schema(v, args["items"], param + "[" + index + "]")
            if is_wp_error(is_valid):
                return is_valid
            # end if
        # end for
    # end if
    if "object" == args["type"]:
        if "" == value:
            value = Array()
        # end if
        if type(value).__name__ == "stdClass":
            value = value
        # end if
        if type(value).__name__ == "JsonSerializable":
            value = value.jsonserialize()
        # end if
        if (not php_is_array(value)):
            #// translators: 1: Parameter, 2: Type name.
            return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s is not of type %2$s."), param, "object")))
        # end if
        for property,v in value:
            if (php_isset(lambda : args["properties"][property])):
                is_valid = rest_validate_value_from_schema(v, args["properties"][property], param + "[" + property + "]")
                if is_wp_error(is_valid):
                    return is_valid
                # end if
            elif (php_isset(lambda : args["additionalProperties"])):
                if False == args["additionalProperties"]:
                    #// translators: %s: Property of an object.
                    return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s is not a valid property of Object."), property)))
                # end if
                if php_is_array(args["additionalProperties"]):
                    is_valid = rest_validate_value_from_schema(v, args["additionalProperties"], param + "[" + property + "]")
                    if is_wp_error(is_valid):
                        return is_valid
                    # end if
                # end if
            # end if
        # end for
    # end if
    if "null" == args["type"]:
        if None != value:
            #// translators: 1: Parameter, 2: Type name.
            return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s is not of type %2$s."), param, "null")))
        # end if
        return True
    # end if
    if (not php_empty(lambda : args["enum"])):
        if (not php_in_array(value, args["enum"], True)):
            #// translators: 1: Parameter, 2: List of valid values.
            return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s is not one of %2$s."), param, php_implode(", ", args["enum"]))))
        # end if
    # end if
    if php_in_array(args["type"], Array("integer", "number")) and (not php_is_numeric(value)):
        #// translators: 1: Parameter, 2: Type name.
        return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s is not of type %2$s."), param, args["type"])))
    # end if
    if "integer" == args["type"] and round(floatval(value)) != floatval(value):
        #// translators: 1: Parameter, 2: Type name.
        return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s is not of type %2$s."), param, "integer")))
    # end if
    if "boolean" == args["type"] and (not rest_is_boolean(value)):
        #// translators: 1: Parameter, 2: Type name.
        return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s is not of type %2$s."), param, "boolean")))
    # end if
    if "string" == args["type"] and (not php_is_string(value)):
        #// translators: 1: Parameter, 2: Type name.
        return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s is not of type %2$s."), param, "string")))
    # end if
    if (php_isset(lambda : args["format"])):
        for case in Switch(args["format"]):
            if case("date-time"):
                if (not rest_parse_date(value)):
                    return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_date", __("Invalid date.")))
                # end if
                break
            # end if
            if case("email"):
                if (not is_email(value)):
                    return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_email", __("Invalid email address.")))
                # end if
                break
            # end if
            if case("ip"):
                if (not rest_is_ip_address(value)):
                    #// translators: %s: IP address.
                    return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%s is not a valid IP address."), param)))
                # end if
                break
            # end if
        # end for
    # end if
    if php_in_array(args["type"], Array("number", "integer"), True) and (php_isset(lambda : args["minimum"])) or (php_isset(lambda : args["maximum"])):
        if (php_isset(lambda : args["minimum"])) and (not (php_isset(lambda : args["maximum"]))):
            if (not php_empty(lambda : args["exclusiveMinimum"])) and value <= args["minimum"]:
                #// translators: 1: Parameter, 2: Minimum number.
                return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s must be greater than %2$d"), param, args["minimum"])))
            elif php_empty(lambda : args["exclusiveMinimum"]) and value < args["minimum"]:
                #// translators: 1: Parameter, 2: Minimum number.
                return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s must be greater than or equal to %2$d"), param, args["minimum"])))
            # end if
        elif (php_isset(lambda : args["maximum"])) and (not (php_isset(lambda : args["minimum"]))):
            if (not php_empty(lambda : args["exclusiveMaximum"])) and value >= args["maximum"]:
                #// translators: 1: Parameter, 2: Maximum number.
                return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s must be less than %2$d"), param, args["maximum"])))
            elif php_empty(lambda : args["exclusiveMaximum"]) and value > args["maximum"]:
                #// translators: 1: Parameter, 2: Maximum number.
                return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s must be less than or equal to %2$d"), param, args["maximum"])))
            # end if
        elif (php_isset(lambda : args["maximum"])) and (php_isset(lambda : args["minimum"])):
            if (not php_empty(lambda : args["exclusiveMinimum"])) and (not php_empty(lambda : args["exclusiveMaximum"])):
                if value >= args["maximum"] or value <= args["minimum"]:
                    #// translators: 1: Parameter, 2: Minimum number, 3: Maximum number.
                    return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s must be between %2$d (exclusive) and %3$d (exclusive)"), param, args["minimum"], args["maximum"])))
                # end if
            elif php_empty(lambda : args["exclusiveMinimum"]) and (not php_empty(lambda : args["exclusiveMaximum"])):
                if value >= args["maximum"] or value < args["minimum"]:
                    #// translators: 1: Parameter, 2: Minimum number, 3: Maximum number.
                    return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s must be between %2$d (inclusive) and %3$d (exclusive)"), param, args["minimum"], args["maximum"])))
                # end if
            elif (not php_empty(lambda : args["exclusiveMinimum"])) and php_empty(lambda : args["exclusiveMaximum"]):
                if value > args["maximum"] or value <= args["minimum"]:
                    #// translators: 1: Parameter, 2: Minimum number, 3: Maximum number.
                    return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s must be between %2$d (exclusive) and %3$d (inclusive)"), param, args["minimum"], args["maximum"])))
                # end if
            elif php_empty(lambda : args["exclusiveMinimum"]) and php_empty(lambda : args["exclusiveMaximum"]):
                if value > args["maximum"] or value < args["minimum"]:
                    #// translators: 1: Parameter, 2: Minimum number, 3: Maximum number.
                    return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s must be between %2$d (inclusive) and %3$d (inclusive)"), param, args["minimum"], args["maximum"])))
                # end if
            # end if
        # end if
    # end if
    return True
# end def rest_validate_value_from_schema
#// 
#// Sanitize a value based on a schema.
#// 
#// @since 4.7.0
#// 
#// @param mixed $value The value to sanitize.
#// @param array $args  Schema array to use for sanitization.
#// @return true|WP_Error
#//
def rest_sanitize_value_from_schema(value=None, args=None, *args_):
    
    if php_is_array(args["type"]):
        #// Determine which type the value was validated against,
        #// and use that type when performing sanitization.
        validated_type = ""
        for type in args["type"]:
            type_args = args
            type_args["type"] = type
            if (not is_wp_error(rest_validate_value_from_schema(value, type_args))):
                validated_type = type
                break
            # end if
        # end for
        if (not validated_type):
            return None
        # end if
        args["type"] = validated_type
    # end if
    if "array" == args["type"]:
        if php_empty(lambda : args["items"]):
            return value
        # end if
        value = wp_parse_list(value)
        for index,v in value:
            value[index] = rest_sanitize_value_from_schema(v, args["items"])
        # end for
        #// Normalize to numeric array so nothing unexpected is in the keys.
        value = php_array_values(value)
        return value
    # end if
    if "object" == args["type"]:
        if type(value).__name__ == "stdClass":
            value = value
        # end if
        if type(value).__name__ == "JsonSerializable":
            value = value.jsonserialize()
        # end if
        if (not php_is_array(value)):
            return Array()
        # end if
        for property,v in value:
            if (php_isset(lambda : args["properties"][property])):
                value[property] = rest_sanitize_value_from_schema(v, args["properties"][property])
            elif (php_isset(lambda : args["additionalProperties"])):
                if False == args["additionalProperties"]:
                    value[property] = None
                elif php_is_array(args["additionalProperties"]):
                    value[property] = rest_sanitize_value_from_schema(v, args["additionalProperties"])
                # end if
            # end if
        # end for
        return value
    # end if
    if "null" == args["type"]:
        return None
    # end if
    if "integer" == args["type"]:
        return php_int(value)
    # end if
    if "number" == args["type"]:
        return php_float(value)
    # end if
    if "boolean" == args["type"]:
        return rest_sanitize_boolean(value)
    # end if
    if (php_isset(lambda : args["format"])):
        for case in Switch(args["format"]):
            if case("date-time"):
                return sanitize_text_field(value)
            # end if
            if case("email"):
                #// sanitize_email() validates, which would be unexpected.
                return sanitize_text_field(value)
            # end if
            if case("uri"):
                return esc_url_raw(value)
            # end if
            if case("ip"):
                return sanitize_text_field(value)
            # end if
        # end for
    # end if
    if "string" == args["type"]:
        return php_strval(value)
    # end if
    return value
# end def rest_sanitize_value_from_schema
#// 
#// Append result of internal request to REST API for purpose of preloading data to be attached to a page.
#// Expected to be called in the context of `array_reduce`.
#// 
#// @since 5.0.0
#// 
#// @param  array  $memo Reduce accumulator.
#// @param  string $path REST API path to preload.
#// @return array        Modified reduce accumulator.
#//
def rest_preload_api_request(memo=None, path=None, *args_):
    
    #// array_reduce() doesn't support passing an array in PHP 5.2,
    #// so we need to make sure we start with one.
    if (not php_is_array(memo)):
        memo = Array()
    # end if
    if php_empty(lambda : path):
        return memo
    # end if
    method = "GET"
    if php_is_array(path) and 2 == php_count(path):
        method = php_end(path)
        path = reset(path)
        if (not php_in_array(method, Array("GET", "OPTIONS"), True)):
            method = "GET"
        # end if
    # end if
    path_parts = php_parse_url(path)
    if False == path_parts:
        return memo
    # end if
    request = php_new_class("WP_REST_Request", lambda : WP_REST_Request(method, path_parts["path"]))
    if (not php_empty(lambda : path_parts["query"])):
        parse_str(path_parts["query"], query_params)
        request.set_query_params(query_params)
    # end if
    response = rest_do_request(request)
    if 200 == response.status:
        server = rest_get_server()
        data = response.get_data()
        links = server.get_compact_response_links(response)
        if (not php_empty(lambda : links)):
            data["_links"] = links
        # end if
        if "OPTIONS" == method:
            response = rest_send_allow_header(response, server, request)
            memo[method][path] = Array({"body": data, "headers": response.headers})
        else:
            memo[path] = Array({"body": data, "headers": response.headers})
        # end if
    # end if
    return memo
# end def rest_preload_api_request
#// 
#// Parses the "_embed" parameter into the list of resources to embed.
#// 
#// @since 5.4.0
#// 
#// @param string|array $embed Raw "_embed" parameter value.
#// @return true|string[] Either true to embed all embeds, or a list of relations to embed.
#//
def rest_parse_embed_param(embed=None, *args_):
    
    if (not embed) or "true" == embed or "1" == embed:
        return True
    # end if
    rels = wp_parse_list(embed)
    if (not rels):
        return True
    # end if
    return rels
# end def rest_parse_embed_param
