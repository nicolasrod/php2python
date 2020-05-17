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
def register_rest_route(namespace_=None, route_=None, args_=None, override_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    if override_ is None:
        override_ = False
    # end if
    
    if php_empty(lambda : namespace_):
        #// 
        #// Non-namespaced routes are not allowed, with the exception of the main
        #// and namespace indexes. If you really need to register a
        #// non-namespaced route, call `WP_REST_Server::register_route` directly.
        #//
        _doing_it_wrong("register_rest_route", __("Routes must be namespaced with plugin or theme name and version."), "4.4.0")
        return False
    elif php_empty(lambda : route_):
        _doing_it_wrong("register_rest_route", __("Route must be specified."), "4.4.0")
        return False
    # end if
    if (not did_action("rest_api_init")):
        _doing_it_wrong("register_rest_route", php_sprintf(__("REST API routes must be registered on the %s action."), "<code>rest_api_init</code>"), "5.1.0")
    # end if
    if (php_isset(lambda : args_["args"])):
        common_args_ = args_["args"]
        args_["args"] = None
    else:
        common_args_ = Array()
    # end if
    if (php_isset(lambda : args_["callback"])):
        #// Upgrade a single set to multiple.
        args_ = Array(args_)
    # end if
    defaults_ = Array({"methods": "GET", "callback": None, "args": Array()})
    for key_,arg_group_ in args_:
        if (not php_is_numeric(key_)):
            continue
        # end if
        arg_group_ = php_array_merge(defaults_, arg_group_)
        arg_group_["args"] = php_array_merge(common_args_, arg_group_["args"])
    # end for
    full_route_ = "/" + php_trim(namespace_, "/") + "/" + php_trim(route_, "/")
    rest_get_server().register_route(namespace_, full_route_, args_, override_)
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
def register_rest_field(object_type_=None, attribute_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    defaults_ = Array({"get_callback": None, "update_callback": None, "schema": None})
    args_ = wp_parse_args(args_, defaults_)
    global wp_rest_additional_fields_
    php_check_if_defined("wp_rest_additional_fields_")
    object_types_ = object_type_
    for object_type_ in object_types_:
        wp_rest_additional_fields_[object_type_][attribute_] = args_
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
def rest_api_init(*_args_):
    
    
    rest_api_register_rewrites()
    global wp_
    php_check_if_defined("wp_")
    wp_.add_query_var("rest_route")
# end def rest_api_init
#// 
#// Adds REST rewrite rules.
#// 
#// @since 4.4.0
#// 
#// @see add_rewrite_rule()
#// @global WP_Rewrite $wp_rewrite WordPress rewrite component.
#//
def rest_api_register_rewrites(*_args_):
    
    
    global wp_rewrite_
    php_check_if_defined("wp_rewrite_")
    add_rewrite_rule("^" + rest_get_url_prefix() + "/?$", "index.php?rest_route=/", "top")
    add_rewrite_rule("^" + rest_get_url_prefix() + "/(.*)?", "index.php?rest_route=/$matches[1]", "top")
    add_rewrite_rule("^" + wp_rewrite_.index + "/" + rest_get_url_prefix() + "/?$", "index.php?rest_route=/", "top")
    add_rewrite_rule("^" + wp_rewrite_.index + "/" + rest_get_url_prefix() + "/(.*)?", "index.php?rest_route=/$matches[1]", "top")
# end def rest_api_register_rewrites
#// 
#// Registers the default REST API filters.
#// 
#// Attached to the {@see 'rest_api_init'} action
#// to make testing and disabling these filters easier.
#// 
#// @since 4.4.0
#//
def rest_api_default_filters(*_args_):
    
    
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
def create_initial_rest_routes(*_args_):
    
    
    for post_type_ in get_post_types(Array({"show_in_rest": True}), "objects"):
        controller_ = post_type_.get_rest_controller()
        if (not controller_):
            continue
        # end if
        controller_.register_routes()
        if post_type_supports(post_type_.name, "revisions"):
            revisions_controller_ = php_new_class("WP_REST_Revisions_Controller", lambda : WP_REST_Revisions_Controller(post_type_.name))
            revisions_controller_.register_routes()
        # end if
        if "attachment" != post_type_.name:
            autosaves_controller_ = php_new_class("WP_REST_Autosaves_Controller", lambda : WP_REST_Autosaves_Controller(post_type_.name))
            autosaves_controller_.register_routes()
        # end if
    # end for
    #// Post types.
    controller_ = php_new_class("WP_REST_Post_Types_Controller", lambda : WP_REST_Post_Types_Controller())
    controller_.register_routes()
    #// Post statuses.
    controller_ = php_new_class("WP_REST_Post_Statuses_Controller", lambda : WP_REST_Post_Statuses_Controller())
    controller_.register_routes()
    #// Taxonomies.
    controller_ = php_new_class("WP_REST_Taxonomies_Controller", lambda : WP_REST_Taxonomies_Controller())
    controller_.register_routes()
    #// Terms.
    for taxonomy_ in get_taxonomies(Array({"show_in_rest": True}), "object"):
        class_ = taxonomy_.rest_controller_class if (not php_empty(lambda : taxonomy_.rest_controller_class)) else "WP_REST_Terms_Controller"
        if (not php_class_exists(class_)):
            continue
        # end if
        controller_ = php_new_class(class_, lambda : {**locals(), **globals()}[class_](taxonomy_.name))
        if (not is_subclass_of(controller_, "WP_REST_Controller")):
            continue
        # end if
        controller_.register_routes()
    # end for
    #// Users.
    controller_ = php_new_class("WP_REST_Users_Controller", lambda : WP_REST_Users_Controller())
    controller_.register_routes()
    #// Comments.
    controller_ = php_new_class("WP_REST_Comments_Controller", lambda : WP_REST_Comments_Controller())
    controller_.register_routes()
    #// 
    #// Filters the search handlers to use in the REST search controller.
    #// 
    #// @since 5.0.0
    #// 
    #// @param array $search_handlers List of search handlers to use in the controller. Each search
    #// handler instance must extend the `WP_REST_Search_Handler` class.
    #// Default is only a handler for posts.
    #//
    search_handlers_ = apply_filters("wp_rest_search_handlers", Array(php_new_class("WP_REST_Post_Search_Handler", lambda : WP_REST_Post_Search_Handler())))
    controller_ = php_new_class("WP_REST_Search_Controller", lambda : WP_REST_Search_Controller(search_handlers_))
    controller_.register_routes()
    #// Block Renderer.
    controller_ = php_new_class("WP_REST_Block_Renderer_Controller", lambda : WP_REST_Block_Renderer_Controller())
    controller_.register_routes()
    #// Settings.
    controller_ = php_new_class("WP_REST_Settings_Controller", lambda : WP_REST_Settings_Controller())
    controller_.register_routes()
    #// Themes.
    controller_ = php_new_class("WP_REST_Themes_Controller", lambda : WP_REST_Themes_Controller())
    controller_.register_routes()
# end def create_initial_rest_routes
#// 
#// Loads the REST API.
#// 
#// @since 4.4.0
#// 
#// @global WP $wp Current WordPress environment instance.
#//
def rest_api_loaded(*_args_):
    
    
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
    server_ = rest_get_server()
    #// Fire off the request.
    route_ = untrailingslashit(PHP_GLOBALS["wp"].query_vars["rest_route"])
    if php_empty(lambda : route_):
        route_ = "/"
    # end if
    server_.serve_request(route_)
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
def rest_get_url_prefix(*_args_):
    
    
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
def get_rest_url(blog_id_=None, path_="/", scheme_="rest", *_args_):
    
    
    if php_empty(lambda : path_):
        path_ = "/"
    # end if
    path_ = "/" + php_ltrim(path_, "/")
    if is_multisite() and get_blog_option(blog_id_, "permalink_structure") or get_option("permalink_structure"):
        global wp_rewrite_
        php_check_if_defined("wp_rewrite_")
        if wp_rewrite_.using_index_permalinks():
            url_ = get_home_url(blog_id_, wp_rewrite_.index + "/" + rest_get_url_prefix(), scheme_)
        else:
            url_ = get_home_url(blog_id_, rest_get_url_prefix(), scheme_)
        # end if
        url_ += path_
    else:
        url_ = trailingslashit(get_home_url(blog_id_, "", scheme_))
        #// nginx only allows HTTP/1.0 methods when redirecting from / to /index.php.
        #// To work around this, we manually add index.php to the URL, avoiding the redirect.
        if "index.php" != php_substr(url_, 9):
            url_ += "index.php"
        # end if
        url_ = add_query_arg("rest_route", path_, url_)
    # end if
    if is_ssl() and (php_isset(lambda : PHP_SERVER["SERVER_NAME"])):
        #// If the current host is the same as the REST URL host, force the REST URL scheme to HTTPS.
        if php_parse_url(get_home_url(blog_id_), PHP_URL_HOST) == PHP_SERVER["SERVER_NAME"]:
            url_ = set_url_scheme(url_, "https")
        # end if
    # end if
    if is_admin() and force_ssl_admin():
        #// 
        #// In this situation the home URL may be http:, and `is_ssl()` may be false,
        #// but the admin is served over https: (one way or another), so REST API usage
        #// will be blocked by browsers unless it is also served over HTTPS.
        #//
        url_ = set_url_scheme(url_, "https")
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
    return apply_filters("rest_url", url_, path_, blog_id_, scheme_)
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
def rest_url(path_="", scheme_="rest", *_args_):
    
    
    return get_rest_url(None, path_, scheme_)
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
def rest_do_request(request_=None, *_args_):
    
    
    request_ = rest_ensure_request(request_)
    return rest_get_server().dispatch(request_)
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
def rest_get_server(*_args_):
    
    
    #// @var WP_REST_Server $wp_rest_server
    global wp_rest_server_
    php_check_if_defined("wp_rest_server_")
    if php_empty(lambda : wp_rest_server_):
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
        wp_rest_server_class_ = apply_filters("wp_rest_server_class", "WP_REST_Server")
        wp_rest_server_ = php_new_class(wp_rest_server_class_, lambda : {**locals(), **globals()}[wp_rest_server_class_]())
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
        do_action("rest_api_init", wp_rest_server_)
    # end if
    return wp_rest_server_
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
def rest_ensure_request(request_=None, *_args_):
    
    
    if type(request_).__name__ == "WP_REST_Request":
        return request_
    # end if
    if php_is_string(request_):
        return php_new_class("WP_REST_Request", lambda : WP_REST_Request("GET", request_))
    # end if
    return php_new_class("WP_REST_Request", lambda : WP_REST_Request("GET", "", request_))
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
def rest_ensure_response(response_=None, *_args_):
    
    
    if is_wp_error(response_):
        return response_
    # end if
    if type(response_).__name__ == "WP_HTTP_Response":
        return response_
    # end if
    return php_new_class("WP_REST_Response", lambda : WP_REST_Response(response_))
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
def rest_handle_deprecated_function(function_=None, replacement_=None, version_=None, *_args_):
    
    
    if (not WP_DEBUG) or php_headers_sent():
        return
    # end if
    if (not php_empty(lambda : replacement_)):
        #// translators: 1: Function name, 2: WordPress version number, 3: New function name.
        string_ = php_sprintf(__("%1$s (since %2$s; use %3$s instead)"), function_, version_, replacement_)
    else:
        #// translators: 1: Function name, 2: WordPress version number.
        string_ = php_sprintf(__("%1$s (since %2$s; no alternative available)"), function_, version_)
    # end if
    php_header(php_sprintf("X-WP-DeprecatedFunction: %s", string_))
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
def rest_handle_deprecated_argument(function_=None, message_=None, version_=None, *_args_):
    
    
    if (not WP_DEBUG) or php_headers_sent():
        return
    # end if
    if (not php_empty(lambda : message_)):
        #// translators: 1: Function name, 2: WordPress version number, 3: Error message.
        string_ = php_sprintf(__("%1$s (since %2$s; %3$s)"), function_, version_, message_)
    else:
        #// translators: 1: Function name, 2: WordPress version number.
        string_ = php_sprintf(__("%1$s (since %2$s; no alternative available)"), function_, version_)
    # end if
    php_header(php_sprintf("X-WP-DeprecatedParam: %s", string_))
# end def rest_handle_deprecated_argument
#// 
#// Sends Cross-Origin Resource Sharing headers with API requests.
#// 
#// @since 4.4.0
#// 
#// @param mixed $value Response data.
#// @return mixed Response data.
#//
def rest_send_cors_headers(value_=None, *_args_):
    
    
    origin_ = get_http_origin()
    if origin_:
        #// Requests from file:// and data: URLs send "Origin: null".
        if "null" != origin_:
            origin_ = esc_url_raw(origin_)
        # end if
        php_header("Access-Control-Allow-Origin: " + origin_)
        php_header("Access-Control-Allow-Methods: OPTIONS, GET, POST, PUT, PATCH, DELETE")
        php_header("Access-Control-Allow-Credentials: true")
        php_header("Vary: Origin", False)
    elif (not php_headers_sent()) and "GET" == PHP_SERVER["REQUEST_METHOD"] and (not is_user_logged_in()):
        php_header("Vary: Origin", False)
    # end if
    return value_
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
def rest_handle_options_request(response_=None, handler_=None, request_=None, *_args_):
    
    
    if (not php_empty(lambda : response_)) or request_.get_method() != "OPTIONS":
        return response_
    # end if
    response_ = php_new_class("WP_REST_Response", lambda : WP_REST_Response())
    data_ = Array()
    for route_,endpoints_ in handler_.get_routes():
        match_ = php_preg_match("@^" + route_ + "$@i", request_.get_route(), matches_)
        if (not match_):
            continue
        # end if
        args_ = Array()
        for param_,value_ in matches_:
            if (not php_is_int(param_)):
                args_[param_] = value_
            # end if
        # end for
        for endpoint_ in endpoints_:
            args_[0] = None
            request_.set_url_params(args_)
            request_.set_attributes(endpoint_)
        # end for
        data_ = handler_.get_data_for_route(route_, endpoints_, "help")
        response_.set_matched_route(route_)
        break
    # end for
    response_.set_data(data_)
    return response_
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
def rest_send_allow_header(response_=None, server_=None, request_=None, *_args_):
    
    
    matched_route_ = response_.get_matched_route()
    if (not matched_route_):
        return response_
    # end if
    routes_ = server_.get_routes()
    allowed_methods_ = Array()
    #// Get the allowed methods across the routes.
    for _handler_ in routes_[matched_route_]:
        for handler_method_,value_ in _handler_["methods"]:
            if (not php_empty(lambda : _handler_["permission_callback"])):
                permission_ = php_call_user_func(_handler_["permission_callback"], request_)
                allowed_methods_[handler_method_] = True == permission_
            else:
                allowed_methods_[handler_method_] = True
            # end if
        # end for
    # end for
    #// Strip out all the methods that are not allowed (false values).
    allowed_methods_ = php_array_filter(allowed_methods_)
    if allowed_methods_:
        response_.header("Allow", php_implode(", ", php_array_map("strtoupper", php_array_keys(allowed_methods_))))
    # end if
    return response_
# end def rest_send_allow_header
#// 
#// Recursively computes the intersection of arrays using keys for comparison.
#// 
#// @param  array $array1 The array with master keys to check.
#// @param  array $array2 An array to compare keys against.
#// 
#// @return array An associative array containing all the entries of array1 which have keys that are present in all arguments.
#//
def _rest_array_intersect_key_recursive(array1_=None, array2_=None, *_args_):
    
    
    array1_ = php_array_intersect_key(array1_, array2_)
    for key_,value_ in array1_:
        if php_is_array(value_) and php_is_array(array2_[key_]):
            array1_[key_] = _rest_array_intersect_key_recursive(value_, array2_[key_])
        # end if
    # end for
    return array1_
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
def rest_filter_response_fields(response_=None, server_=None, request_=None, *_args_):
    
    
    if (not (php_isset(lambda : request_["_fields"]))) or response_.is_error():
        return response_
    # end if
    data_ = response_.get_data()
    fields_ = wp_parse_list(request_["_fields"])
    if 0 == php_count(fields_):
        return response_
    # end if
    #// Trim off outside whitespace from the comma delimited list.
    fields_ = php_array_map("trim", fields_)
    #// Create nested array of accepted field hierarchy.
    fields_as_keyed_ = Array()
    for field_ in fields_:
        parts_ = php_explode(".", field_)
        ref_ = fields_as_keyed_
        while True:
            
            if not (php_count(parts_) > 1):
                break
            # end if
            next_ = php_array_shift(parts_)
            if (php_isset(lambda : ref_[next_])) and True == ref_[next_]:
                break
            # end if
            ref_[next_] = ref_[next_] if (php_isset(lambda : ref_[next_])) else Array()
            ref_ = ref_[next_]
        # end while
        last_ = php_array_shift(parts_)
        ref_[last_] = True
    # end for
    if wp_is_numeric_array(data_):
        new_data_ = Array()
        for item_ in data_:
            new_data_[-1] = _rest_array_intersect_key_recursive(item_, fields_as_keyed_)
        # end for
    else:
        new_data_ = _rest_array_intersect_key_recursive(data_, fields_as_keyed_)
    # end if
    response_.set_data(new_data_)
    return response_
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
def rest_is_field_included(field_=None, fields_=None, *_args_):
    
    
    if php_in_array(field_, fields_, True):
        return True
    # end if
    for accepted_field_ in fields_:
        #// Check to see if $field is the parent of any item in $fields.
        #// A field "parent" should be accepted if "parent.child" is accepted.
        if php_strpos(accepted_field_, str(field_) + str(".")) == 0:
            return True
        # end if
        #// Conversely, if "parent" is accepted, all "parent.child" fields
        #// should also be accepted.
        if php_strpos(field_, str(accepted_field_) + str(".")) == 0:
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
def rest_output_rsd(*_args_):
    
    
    api_root_ = get_rest_url()
    if php_empty(lambda : api_root_):
        return
    # end if
    php_print(" <api name=\"WP-API\" blogID=\"1\" preferred=\"false\" apiLink=\"")
    php_print(esc_url(api_root_))
    php_print("\" />\n  ")
# end def rest_output_rsd
#// 
#// Outputs the REST API link tag into page header.
#// 
#// @since 4.4.0
#// 
#// @see get_rest_url()
#//
def rest_output_link_wp_head(*_args_):
    
    
    api_root_ = get_rest_url()
    if php_empty(lambda : api_root_):
        return
    # end if
    php_print("<link rel='https://api.w.org/' href='" + esc_url(api_root_) + "' />\n")
# end def rest_output_link_wp_head
#// 
#// Sends a Link header for the REST API.
#// 
#// @since 4.4.0
#//
def rest_output_link_header(*_args_):
    
    
    if php_headers_sent():
        return
    # end if
    api_root_ = get_rest_url()
    if php_empty(lambda : api_root_):
        return
    # end if
    php_header("Link: <" + esc_url_raw(api_root_) + ">; rel=\"https://api.w.org/\"", False)
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
def rest_cookie_check_errors(result_=None, *_args_):
    
    
    if (not php_empty(lambda : result_)):
        return result_
    # end if
    global wp_rest_auth_cookie_
    php_check_if_defined("wp_rest_auth_cookie_")
    #// 
    #// Is cookie authentication being used? (If we get an auth
    #// error, but we're still logged in, another authentication
    #// must have been used).
    #//
    if True != wp_rest_auth_cookie_ and is_user_logged_in():
        return result_
    # end if
    #// Determine if there is a nonce.
    nonce_ = None
    if (php_isset(lambda : PHP_REQUEST["_wpnonce"])):
        nonce_ = PHP_REQUEST["_wpnonce"]
    elif (php_isset(lambda : PHP_SERVER["HTTP_X_WP_NONCE"])):
        nonce_ = PHP_SERVER["HTTP_X_WP_NONCE"]
    # end if
    if None == nonce_:
        #// No nonce at all, so act as if it's an unauthenticated request.
        wp_set_current_user(0)
        return True
    # end if
    #// Check the nonce.
    result_ = wp_verify_nonce(nonce_, "wp_rest")
    if (not result_):
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
def rest_cookie_collect_status(*_args_):
    
    
    global wp_rest_auth_cookie_
    php_check_if_defined("wp_rest_auth_cookie_")
    status_type_ = current_action()
    if "auth_cookie_valid" != status_type_:
        wp_rest_auth_cookie_ = php_substr(status_type_, 12)
        return
    # end if
    wp_rest_auth_cookie_ = True
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
def rest_parse_date(date_=None, force_utc_=None, *_args_):
    if force_utc_ is None:
        force_utc_ = False
    # end if
    
    if force_utc_:
        date_ = php_preg_replace("/[+-]\\d+:?\\d+$/", "+00:00", date_)
    # end if
    regex_ = "#^\\d{4}-\\d{2}-\\d{2}[Tt ]\\d{2}:\\d{2}:\\d{2}(?:\\.\\d+)?(?:Z|[+-]\\d{2}(?::\\d{2})?)?$#"
    if (not php_preg_match(regex_, date_, matches_)):
        return False
    # end if
    return strtotime(date_)
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
def rest_get_date_with_gmt(date_=None, is_utc_=None, *_args_):
    if is_utc_ is None:
        is_utc_ = False
    # end if
    
    #// 
    #// Whether or not the original date actually has a timezone string
    #// changes the way we need to do timezone conversion.
    #// Store this info before parsing the date, and use it later.
    #//
    has_timezone_ = php_preg_match("#(Z|[+-]\\d{2}(:\\d{2})?)$#", date_)
    date_ = rest_parse_date(date_)
    if php_empty(lambda : date_):
        return None
    # end if
    #// 
    #// At this point $date could either be a local date (if we were passed
    #// a *local* date without a timezone offset) or a UTC date (otherwise).
    #// Timezone conversion needs to be handled differently between these two cases.
    #//
    if (not is_utc_) and (not has_timezone_):
        local_ = gmdate("Y-m-d H:i:s", date_)
        utc_ = get_gmt_from_date(local_)
    else:
        utc_ = gmdate("Y-m-d H:i:s", date_)
        local_ = get_date_from_gmt(utc_)
    # end if
    return Array(local_, utc_)
# end def rest_get_date_with_gmt
#// 
#// Returns a contextual HTTP error code for authorization failure.
#// 
#// @since 4.7.0
#// 
#// @return integer 401 if the user is not logged in, 403 if the user is logged in.
#//
def rest_authorization_required_code(*_args_):
    
    
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
def rest_validate_request_arg(value_=None, request_=None, param_=None, *_args_):
    
    
    attributes_ = request_.get_attributes()
    if (not (php_isset(lambda : attributes_["args"][param_]))) or (not php_is_array(attributes_["args"][param_])):
        return True
    # end if
    args_ = attributes_["args"][param_]
    return rest_validate_value_from_schema(value_, args_, param_)
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
def rest_sanitize_request_arg(value_=None, request_=None, param_=None, *_args_):
    
    
    attributes_ = request_.get_attributes()
    if (not (php_isset(lambda : attributes_["args"][param_]))) or (not php_is_array(attributes_["args"][param_])):
        return value_
    # end if
    args_ = attributes_["args"][param_]
    return rest_sanitize_value_from_schema(value_, args_)
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
def rest_parse_request_arg(value_=None, request_=None, param_=None, *_args_):
    
    
    is_valid_ = rest_validate_request_arg(value_, request_, param_)
    if is_wp_error(is_valid_):
        return is_valid_
    # end if
    value_ = rest_sanitize_request_arg(value_, request_, param_)
    return value_
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
def rest_is_ip_address(ip_=None, *_args_):
    
    
    ipv4_pattern_ = "/^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/"
    if (not php_preg_match(ipv4_pattern_, ip_)) and (not Requests_IPv6.check_ipv6(ip_)):
        return False
    # end if
    return ip_
# end def rest_is_ip_address
#// 
#// Changes a boolean-like value into the proper boolean value.
#// 
#// @since 4.7.0
#// 
#// @param bool|string|int $value The value being evaluated.
#// @return boolean Returns the proper associated boolean value.
#//
def rest_sanitize_boolean(value_=None, *_args_):
    
    
    #// String values are translated to `true`; make sure 'false' is false.
    if php_is_string(value_):
        value_ = php_strtolower(value_)
        if php_in_array(value_, Array("false", "0"), True):
            value_ = False
        # end if
    # end if
    #// Everything else will map nicely to boolean.
    return php_bool(value_)
# end def rest_sanitize_boolean
#// 
#// Determines if a given value is boolean-like.
#// 
#// @since 4.7.0
#// 
#// @param bool|string $maybe_bool The value being evaluated.
#// @return boolean True if a boolean, otherwise false.
#//
def rest_is_boolean(maybe_bool_=None, *_args_):
    
    
    if php_is_bool(maybe_bool_):
        return True
    # end if
    if php_is_string(maybe_bool_):
        maybe_bool_ = php_strtolower(maybe_bool_)
        valid_boolean_values_ = Array("false", "true", "0", "1")
        return php_in_array(maybe_bool_, valid_boolean_values_, True)
    # end if
    if php_is_int(maybe_bool_):
        return php_in_array(maybe_bool_, Array(0, 1), True)
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
def rest_get_avatar_urls(id_or_email_=None, *_args_):
    
    
    avatar_sizes_ = rest_get_avatar_sizes()
    urls_ = Array()
    for size_ in avatar_sizes_:
        urls_[size_] = get_avatar_url(id_or_email_, Array({"size": size_}))
    # end for
    return urls_
# end def rest_get_avatar_urls
#// 
#// Retrieves the pixel sizes for avatars.
#// 
#// @since 4.7.0
#// 
#// @return int[] List of pixel sizes for avatars. Default `[ 24, 48, 96 ]`.
#//
def rest_get_avatar_sizes(*_args_):
    
    
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
def rest_validate_value_from_schema(value_=None, args_=None, param_="", *_args_):
    
    
    if php_is_array(args_["type"]):
        for type_ in args_["type"]:
            type_args_ = args_
            type_args_["type"] = type_
            if True == rest_validate_value_from_schema(value_, type_args_, param_):
                return True
            # end if
        # end for
        #// translators: 1: Parameter, 2: List of types.
        return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s is not of type %2$s."), param_, php_implode(",", args_["type"]))))
    # end if
    if "array" == args_["type"]:
        if (not is_null(value_)):
            value_ = wp_parse_list(value_)
        # end if
        if (not wp_is_numeric_array(value_)):
            #// translators: 1: Parameter, 2: Type name.
            return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s is not of type %2$s."), param_, "array")))
        # end if
        for index_,v_ in value_:
            is_valid_ = rest_validate_value_from_schema(v_, args_["items"], param_ + "[" + index_ + "]")
            if is_wp_error(is_valid_):
                return is_valid_
            # end if
        # end for
    # end if
    if "object" == args_["type"]:
        if "" == value_:
            value_ = Array()
        # end if
        if type(value_).__name__ == "stdClass":
            value_ = value_
        # end if
        if type(value_).__name__ == "JsonSerializable":
            value_ = value_.jsonserialize()
        # end if
        if (not php_is_array(value_)):
            #// translators: 1: Parameter, 2: Type name.
            return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s is not of type %2$s."), param_, "object")))
        # end if
        for property_,v_ in value_:
            if (php_isset(lambda : args_["properties"][property_])):
                is_valid_ = rest_validate_value_from_schema(v_, args_["properties"][property_], param_ + "[" + property_ + "]")
                if is_wp_error(is_valid_):
                    return is_valid_
                # end if
            elif (php_isset(lambda : args_["additionalProperties"])):
                if False == args_["additionalProperties"]:
                    #// translators: %s: Property of an object.
                    return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s is not a valid property of Object."), property_)))
                # end if
                if php_is_array(args_["additionalProperties"]):
                    is_valid_ = rest_validate_value_from_schema(v_, args_["additionalProperties"], param_ + "[" + property_ + "]")
                    if is_wp_error(is_valid_):
                        return is_valid_
                    # end if
                # end if
            # end if
        # end for
    # end if
    if "null" == args_["type"]:
        if None != value_:
            #// translators: 1: Parameter, 2: Type name.
            return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s is not of type %2$s."), param_, "null")))
        # end if
        return True
    # end if
    if (not php_empty(lambda : args_["enum"])):
        if (not php_in_array(value_, args_["enum"], True)):
            #// translators: 1: Parameter, 2: List of valid values.
            return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s is not one of %2$s."), param_, php_implode(", ", args_["enum"]))))
        # end if
    # end if
    if php_in_array(args_["type"], Array("integer", "number")) and (not php_is_numeric(value_)):
        #// translators: 1: Parameter, 2: Type name.
        return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s is not of type %2$s."), param_, args_["type"])))
    # end if
    if "integer" == args_["type"] and round(floatval(value_)) != floatval(value_):
        #// translators: 1: Parameter, 2: Type name.
        return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s is not of type %2$s."), param_, "integer")))
    # end if
    if "boolean" == args_["type"] and (not rest_is_boolean(value_)):
        #// translators: 1: Parameter, 2: Type name.
        return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s is not of type %2$s."), param_, "boolean")))
    # end if
    if "string" == args_["type"] and (not php_is_string(value_)):
        #// translators: 1: Parameter, 2: Type name.
        return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s is not of type %2$s."), param_, "string")))
    # end if
    if (php_isset(lambda : args_["format"])):
        for case in Switch(args_["format"]):
            if case("date-time"):
                if (not rest_parse_date(value_)):
                    return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_date", __("Invalid date.")))
                # end if
                break
            # end if
            if case("email"):
                if (not is_email(value_)):
                    return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_email", __("Invalid email address.")))
                # end if
                break
            # end if
            if case("ip"):
                if (not rest_is_ip_address(value_)):
                    #// translators: %s: IP address.
                    return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%s is not a valid IP address."), param_)))
                # end if
                break
            # end if
        # end for
    # end if
    if php_in_array(args_["type"], Array("number", "integer"), True) and (php_isset(lambda : args_["minimum"])) or (php_isset(lambda : args_["maximum"])):
        if (php_isset(lambda : args_["minimum"])) and (not (php_isset(lambda : args_["maximum"]))):
            if (not php_empty(lambda : args_["exclusiveMinimum"])) and value_ <= args_["minimum"]:
                #// translators: 1: Parameter, 2: Minimum number.
                return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s must be greater than %2$d"), param_, args_["minimum"])))
            elif php_empty(lambda : args_["exclusiveMinimum"]) and value_ < args_["minimum"]:
                #// translators: 1: Parameter, 2: Minimum number.
                return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s must be greater than or equal to %2$d"), param_, args_["minimum"])))
            # end if
        elif (php_isset(lambda : args_["maximum"])) and (not (php_isset(lambda : args_["minimum"]))):
            if (not php_empty(lambda : args_["exclusiveMaximum"])) and value_ >= args_["maximum"]:
                #// translators: 1: Parameter, 2: Maximum number.
                return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s must be less than %2$d"), param_, args_["maximum"])))
            elif php_empty(lambda : args_["exclusiveMaximum"]) and value_ > args_["maximum"]:
                #// translators: 1: Parameter, 2: Maximum number.
                return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s must be less than or equal to %2$d"), param_, args_["maximum"])))
            # end if
        elif (php_isset(lambda : args_["maximum"])) and (php_isset(lambda : args_["minimum"])):
            if (not php_empty(lambda : args_["exclusiveMinimum"])) and (not php_empty(lambda : args_["exclusiveMaximum"])):
                if value_ >= args_["maximum"] or value_ <= args_["minimum"]:
                    #// translators: 1: Parameter, 2: Minimum number, 3: Maximum number.
                    return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s must be between %2$d (exclusive) and %3$d (exclusive)"), param_, args_["minimum"], args_["maximum"])))
                # end if
            elif php_empty(lambda : args_["exclusiveMinimum"]) and (not php_empty(lambda : args_["exclusiveMaximum"])):
                if value_ >= args_["maximum"] or value_ < args_["minimum"]:
                    #// translators: 1: Parameter, 2: Minimum number, 3: Maximum number.
                    return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s must be between %2$d (inclusive) and %3$d (exclusive)"), param_, args_["minimum"], args_["maximum"])))
                # end if
            elif (not php_empty(lambda : args_["exclusiveMinimum"])) and php_empty(lambda : args_["exclusiveMaximum"]):
                if value_ > args_["maximum"] or value_ <= args_["minimum"]:
                    #// translators: 1: Parameter, 2: Minimum number, 3: Maximum number.
                    return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s must be between %2$d (exclusive) and %3$d (inclusive)"), param_, args_["minimum"], args_["maximum"])))
                # end if
            elif php_empty(lambda : args_["exclusiveMinimum"]) and php_empty(lambda : args_["exclusiveMaximum"]):
                if value_ > args_["maximum"] or value_ < args_["minimum"]:
                    #// translators: 1: Parameter, 2: Minimum number, 3: Maximum number.
                    return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("%1$s must be between %2$d (inclusive) and %3$d (inclusive)"), param_, args_["minimum"], args_["maximum"])))
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
def rest_sanitize_value_from_schema(value_=None, args_=None, *_args_):
    
    
    if php_is_array(args_["type"]):
        #// Determine which type the value was validated against,
        #// and use that type when performing sanitization.
        validated_type_ = ""
        for type_ in args_["type"]:
            type_args_ = args_
            type_args_["type"] = type_
            if (not is_wp_error(rest_validate_value_from_schema(value_, type_args_))):
                validated_type_ = type_
                break
            # end if
        # end for
        if (not validated_type_):
            return None
        # end if
        args_["type"] = validated_type_
    # end if
    if "array" == args_["type"]:
        if php_empty(lambda : args_["items"]):
            return value_
        # end if
        value_ = wp_parse_list(value_)
        for index_,v_ in value_:
            value_[index_] = rest_sanitize_value_from_schema(v_, args_["items"])
        # end for
        #// Normalize to numeric array so nothing unexpected is in the keys.
        value_ = php_array_values(value_)
        return value_
    # end if
    if "object" == args_["type"]:
        if type(value_).__name__ == "stdClass":
            value_ = value_
        # end if
        if type(value_).__name__ == "JsonSerializable":
            value_ = value_.jsonserialize()
        # end if
        if (not php_is_array(value_)):
            return Array()
        # end if
        for property_,v_ in value_:
            if (php_isset(lambda : args_["properties"][property_])):
                value_[property_] = rest_sanitize_value_from_schema(v_, args_["properties"][property_])
            elif (php_isset(lambda : args_["additionalProperties"])):
                if False == args_["additionalProperties"]:
                    value_[property_] = None
                elif php_is_array(args_["additionalProperties"]):
                    value_[property_] = rest_sanitize_value_from_schema(v_, args_["additionalProperties"])
                # end if
            # end if
        # end for
        return value_
    # end if
    if "null" == args_["type"]:
        return None
    # end if
    if "integer" == args_["type"]:
        return php_int(value_)
    # end if
    if "number" == args_["type"]:
        return php_float(value_)
    # end if
    if "boolean" == args_["type"]:
        return rest_sanitize_boolean(value_)
    # end if
    if (php_isset(lambda : args_["format"])):
        for case in Switch(args_["format"]):
            if case("date-time"):
                return sanitize_text_field(value_)
            # end if
            if case("email"):
                #// sanitize_email() validates, which would be unexpected.
                return sanitize_text_field(value_)
            # end if
            if case("uri"):
                return esc_url_raw(value_)
            # end if
            if case("ip"):
                return sanitize_text_field(value_)
            # end if
        # end for
    # end if
    if "string" == args_["type"]:
        return php_strval(value_)
    # end if
    return value_
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
def rest_preload_api_request(memo_=None, path_=None, *_args_):
    
    
    #// array_reduce() doesn't support passing an array in PHP 5.2,
    #// so we need to make sure we start with one.
    if (not php_is_array(memo_)):
        memo_ = Array()
    # end if
    if php_empty(lambda : path_):
        return memo_
    # end if
    method_ = "GET"
    if php_is_array(path_) and 2 == php_count(path_):
        method_ = php_end(path_)
        path_ = reset(path_)
        if (not php_in_array(method_, Array("GET", "OPTIONS"), True)):
            method_ = "GET"
        # end if
    # end if
    path_parts_ = php_parse_url(path_)
    if False == path_parts_:
        return memo_
    # end if
    request_ = php_new_class("WP_REST_Request", lambda : WP_REST_Request(method_, path_parts_["path"]))
    if (not php_empty(lambda : path_parts_["query"])):
        parse_str(path_parts_["query"], query_params_)
        request_.set_query_params(query_params_)
    # end if
    response_ = rest_do_request(request_)
    if 200 == response_.status:
        server_ = rest_get_server()
        data_ = response_.get_data()
        links_ = server_.get_compact_response_links(response_)
        if (not php_empty(lambda : links_)):
            data_["_links"] = links_
        # end if
        if "OPTIONS" == method_:
            response_ = rest_send_allow_header(response_, server_, request_)
            memo_[method_][path_] = Array({"body": data_, "headers": response_.headers})
        else:
            memo_[path_] = Array({"body": data_, "headers": response_.headers})
        # end if
    # end if
    return memo_
# end def rest_preload_api_request
#// 
#// Parses the "_embed" parameter into the list of resources to embed.
#// 
#// @since 5.4.0
#// 
#// @param string|array $embed Raw "_embed" parameter value.
#// @return true|string[] Either true to embed all embeds, or a list of relations to embed.
#//
def rest_parse_embed_param(embed_=None, *_args_):
    
    
    if (not embed_) or "true" == embed_ or "1" == embed_:
        return True
    # end if
    rels_ = wp_parse_list(embed_)
    if (not rels_):
        return True
    # end if
    return rels_
# end def rest_parse_embed_param
