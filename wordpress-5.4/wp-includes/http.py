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
#// Core HTTP Request API
#// 
#// Standardizes the HTTP requests for WordPress. Handles cookies, gzip encoding and decoding, chunk
#// decoding, if HTTP 1.1 and various other difficult HTTP protocol implementations.
#// 
#// @package WordPress
#// @subpackage HTTP
#// 
#// 
#// Returns the initialized WP_Http Object
#// 
#// @since 2.7.0
#// @access private
#// 
#// @staticvar WP_Http $http
#// 
#// @return WP_Http HTTP Transport object.
#//
def _wp_http_get_object(*_args_):
    
    
    http_ = None
    if is_null(http_):
        http_ = php_new_class("WP_Http", lambda : WP_Http())
    # end if
    return http_
# end def _wp_http_get_object
#// 
#// Retrieve the raw response from a safe HTTP request.
#// 
#// This function is ideal when the HTTP request is being made to an arbitrary
#// URL. The URL is validated to avoid redirection and request forgery attacks.
#// 
#// @since 3.6.0
#// 
#// @see wp_remote_request() For more information on the response array format.
#// @see WP_Http::request() For default arguments information.
#// 
#// @param string $url  URL to retrieve.
#// @param array  $args Optional. Request arguments. Default empty array.
#// @return array|WP_Error The response or WP_Error on failure.
#//
def wp_safe_remote_request(url_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    args_["reject_unsafe_urls"] = True
    http_ = _wp_http_get_object()
    return http_.request(url_, args_)
# end def wp_safe_remote_request
#// 
#// Retrieve the raw response from a safe HTTP request using the GET method.
#// 
#// This function is ideal when the HTTP request is being made to an arbitrary
#// URL. The URL is validated to avoid redirection and request forgery attacks.
#// 
#// @since 3.6.0
#// 
#// @see wp_remote_request() For more information on the response array format.
#// @see WP_Http::request() For default arguments information.
#// 
#// @param string $url  URL to retrieve.
#// @param array  $args Optional. Request arguments. Default empty array.
#// @return array|WP_Error The response or WP_Error on failure.
#//
def wp_safe_remote_get(url_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    args_["reject_unsafe_urls"] = True
    http_ = _wp_http_get_object()
    return http_.get(url_, args_)
# end def wp_safe_remote_get
#// 
#// Retrieve the raw response from a safe HTTP request using the POST method.
#// 
#// This function is ideal when the HTTP request is being made to an arbitrary
#// URL. The URL is validated to avoid redirection and request forgery attacks.
#// 
#// @since 3.6.0
#// 
#// @see wp_remote_request() For more information on the response array format.
#// @see WP_Http::request() For default arguments information.
#// 
#// @param string $url  URL to retrieve.
#// @param array  $args Optional. Request arguments. Default empty array.
#// @return array|WP_Error The response or WP_Error on failure.
#//
def wp_safe_remote_post(url_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    args_["reject_unsafe_urls"] = True
    http_ = _wp_http_get_object()
    return http_.post(url_, args_)
# end def wp_safe_remote_post
#// 
#// Retrieve the raw response from a safe HTTP request using the HEAD method.
#// 
#// This function is ideal when the HTTP request is being made to an arbitrary
#// URL. The URL is validated to avoid redirection and request forgery attacks.
#// 
#// @since 3.6.0
#// 
#// @see wp_remote_request() For more information on the response array format.
#// @see WP_Http::request() For default arguments information.
#// 
#// @param string $url  URL to retrieve.
#// @param array  $args Optional. Request arguments. Default empty array.
#// @return array|WP_Error The response or WP_Error on failure.
#//
def wp_safe_remote_head(url_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    args_["reject_unsafe_urls"] = True
    http_ = _wp_http_get_object()
    return http_.head(url_, args_)
# end def wp_safe_remote_head
#// 
#// Performs an HTTP request and returns its response.
#// 
#// There are other API functions available which abstract away the HTTP method:
#// 
#// - Default 'GET'  for wp_remote_get()
#// - Default 'POST' for wp_remote_post()
#// - Default 'HEAD' for wp_remote_head()
#// 
#// @since 2.7.0
#// 
#// @see WP_Http::request() For information on default arguments.
#// 
#// @param string $url  URL to retrieve.
#// @param array  $args Optional. Request arguments. Default empty array.
#// @return array|WP_Error {
#// The response array or a WP_Error on failure.
#// 
#// @type string[]                       $headers       Array of response headers keyed by their name.
#// @type string                         $body          Response body.
#// @type array                          $response      {
#// Data about the HTTP response.
#// 
#// @type int|false    $code    HTTP response code.
#// @type string|false $message HTTP response message.
#// }
#// @type WP_HTTP_Cookie[]               $cookies       Array of response cookies.
#// @type WP_HTTP_Requests_Response|null $http_response Raw HTTP response object.
#// }
#//
def wp_remote_request(url_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    http_ = _wp_http_get_object()
    return http_.request(url_, args_)
# end def wp_remote_request
#// 
#// Performs an HTTP request using the GET method and returns its response.
#// 
#// @since 2.7.0
#// 
#// @see wp_remote_request() For more information on the response array format.
#// @see WP_Http::request() For default arguments information.
#// 
#// @param string $url  URL to retrieve.
#// @param array  $args Optional. Request arguments. Default empty array.
#// @return array|WP_Error The response or WP_Error on failure.
#//
def wp_remote_get(url_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    http_ = _wp_http_get_object()
    return http_.get(url_, args_)
# end def wp_remote_get
#// 
#// Performs an HTTP request using the POST method and returns its response.
#// 
#// @since 2.7.0
#// 
#// @see wp_remote_request() For more information on the response array format.
#// @see WP_Http::request() For default arguments information.
#// 
#// @param string $url  URL to retrieve.
#// @param array  $args Optional. Request arguments. Default empty array.
#// @return array|WP_Error The response or WP_Error on failure.
#//
def wp_remote_post(url_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    http_ = _wp_http_get_object()
    return http_.post(url_, args_)
# end def wp_remote_post
#// 
#// Performs an HTTP request using the HEAD method and returns its response.
#// 
#// @since 2.7.0
#// 
#// @see wp_remote_request() For more information on the response array format.
#// @see WP_Http::request() For default arguments information.
#// 
#// @param string $url  URL to retrieve.
#// @param array  $args Optional. Request arguments. Default empty array.
#// @return array|WP_Error The response or WP_Error on failure.
#//
def wp_remote_head(url_=None, args_=None, *_args_):
    if args_ is None:
        args_ = Array()
    # end if
    
    http_ = _wp_http_get_object()
    return http_.head(url_, args_)
# end def wp_remote_head
#// 
#// Retrieve only the headers from the raw response.
#// 
#// @since 2.7.0
#// @since 4.6.0 Return value changed from an array to an Requests_Utility_CaseInsensitiveDictionary instance.
#// 
#// @see \Requests_Utility_CaseInsensitiveDictionary
#// 
#// @param array|WP_Error $response HTTP response.
#// @return array|\Requests_Utility_CaseInsensitiveDictionary The headers of the response. Empty array if incorrect parameter given.
#//
def wp_remote_retrieve_headers(response_=None, *_args_):
    
    
    if is_wp_error(response_) or (not (php_isset(lambda : response_["headers"]))):
        return Array()
    # end if
    return response_["headers"]
# end def wp_remote_retrieve_headers
#// 
#// Retrieve a single header by name from the raw response.
#// 
#// @since 2.7.0
#// 
#// @param array|WP_Error $response HTTP response.
#// @param string         $header   Header name to retrieve value from.
#// @return string The header value. Empty string on if incorrect parameter given, or if the header doesn't exist.
#//
def wp_remote_retrieve_header(response_=None, header_=None, *_args_):
    
    
    if is_wp_error(response_) or (not (php_isset(lambda : response_["headers"]))):
        return ""
    # end if
    if (php_isset(lambda : response_["headers"][header_])):
        return response_["headers"][header_]
    # end if
    return ""
# end def wp_remote_retrieve_header
#// 
#// Retrieve only the response code from the raw response.
#// 
#// Will return an empty array if incorrect parameter value is given.
#// 
#// @since 2.7.0
#// 
#// @param array|WP_Error $response HTTP response.
#// @return int|string The response code as an integer. Empty string on incorrect parameter given.
#//
def wp_remote_retrieve_response_code(response_=None, *_args_):
    
    
    if is_wp_error(response_) or (not (php_isset(lambda : response_["response"]))) or (not php_is_array(response_["response"])):
        return ""
    # end if
    return response_["response"]["code"]
# end def wp_remote_retrieve_response_code
#// 
#// Retrieve only the response message from the raw response.
#// 
#// Will return an empty array if incorrect parameter value is given.
#// 
#// @since 2.7.0
#// 
#// @param array|WP_Error $response HTTP response.
#// @return string The response message. Empty string on incorrect parameter given.
#//
def wp_remote_retrieve_response_message(response_=None, *_args_):
    
    
    if is_wp_error(response_) or (not (php_isset(lambda : response_["response"]))) or (not php_is_array(response_["response"])):
        return ""
    # end if
    return response_["response"]["message"]
# end def wp_remote_retrieve_response_message
#// 
#// Retrieve only the body from the raw response.
#// 
#// @since 2.7.0
#// 
#// @param array|WP_Error $response HTTP response.
#// @return string The body of the response. Empty string if no body or incorrect parameter given.
#//
def wp_remote_retrieve_body(response_=None, *_args_):
    
    
    if is_wp_error(response_) or (not (php_isset(lambda : response_["body"]))):
        return ""
    # end if
    return response_["body"]
# end def wp_remote_retrieve_body
#// 
#// Retrieve only the cookies from the raw response.
#// 
#// @since 4.4.0
#// 
#// @param array|WP_Error $response HTTP response.
#// @return WP_Http_Cookie[] An array of `WP_Http_Cookie` objects from the response. Empty array if there are none, or the response is a WP_Error.
#//
def wp_remote_retrieve_cookies(response_=None, *_args_):
    
    
    if is_wp_error(response_) or php_empty(lambda : response_["cookies"]):
        return Array()
    # end if
    return response_["cookies"]
# end def wp_remote_retrieve_cookies
#// 
#// Retrieve a single cookie by name from the raw response.
#// 
#// @since 4.4.0
#// 
#// @param array|WP_Error $response HTTP response.
#// @param string         $name     The name of the cookie to retrieve.
#// @return WP_Http_Cookie|string The `WP_Http_Cookie` object. Empty string if the cookie isn't present in the response.
#//
def wp_remote_retrieve_cookie(response_=None, name_=None, *_args_):
    
    
    cookies_ = wp_remote_retrieve_cookies(response_)
    if php_empty(lambda : cookies_):
        return ""
    # end if
    for cookie_ in cookies_:
        if cookie_.name == name_:
            return cookie_
        # end if
    # end for
    return ""
# end def wp_remote_retrieve_cookie
#// 
#// Retrieve a single cookie's value by name from the raw response.
#// 
#// @since 4.4.0
#// 
#// @param array|WP_Error $response HTTP response.
#// @param string         $name     The name of the cookie to retrieve.
#// @return string The value of the cookie. Empty string if the cookie isn't present in the response.
#//
def wp_remote_retrieve_cookie_value(response_=None, name_=None, *_args_):
    
    
    cookie_ = wp_remote_retrieve_cookie(response_, name_)
    if (not php_is_a(cookie_, "WP_Http_Cookie")):
        return ""
    # end if
    return cookie_.value
# end def wp_remote_retrieve_cookie_value
#// 
#// Determines if there is an HTTP Transport that can process this request.
#// 
#// @since 3.2.0
#// 
#// @param array  $capabilities Array of capabilities to test or a wp_remote_request() $args array.
#// @param string $url          Optional. If given, will check if the URL requires SSL and adds
#// that requirement to the capabilities array.
#// 
#// @return bool
#//
def wp_http_supports(capabilities_=None, url_=None, *_args_):
    if capabilities_ is None:
        capabilities_ = Array()
    # end if
    
    http_ = _wp_http_get_object()
    capabilities_ = wp_parse_args(capabilities_)
    count_ = php_count(capabilities_)
    #// If we have a numeric $capabilities array, spoof a wp_remote_request() associative $args array.
    if count_ and php_count(php_array_filter(php_array_keys(capabilities_), "is_numeric")) == count_:
        capabilities_ = php_array_combine(php_array_values(capabilities_), array_fill(0, count_, True))
    # end if
    if url_ and (not (php_isset(lambda : capabilities_["ssl"]))):
        scheme_ = php_parse_url(url_, PHP_URL_SCHEME)
        if "https" == scheme_ or "ssl" == scheme_:
            capabilities_["ssl"] = True
        # end if
    # end if
    return php_bool(http_._get_first_available_transport(capabilities_))
# end def wp_http_supports
#// 
#// Get the HTTP Origin of the current request.
#// 
#// @since 3.4.0
#// 
#// @return string URL of the origin. Empty string if no origin.
#//
def get_http_origin(*_args_):
    
    
    origin_ = ""
    if (not php_empty(lambda : PHP_SERVER["HTTP_ORIGIN"])):
        origin_ = PHP_SERVER["HTTP_ORIGIN"]
    # end if
    #// 
    #// Change the origin of an HTTP request.
    #// 
    #// @since 3.4.0
    #// 
    #// @param string $origin The original origin for the request.
    #//
    return apply_filters("http_origin", origin_)
# end def get_http_origin
#// 
#// Retrieve list of allowed HTTP origins.
#// 
#// @since 3.4.0
#// 
#// @return string[] Array of origin URLs.
#//
def get_allowed_http_origins(*_args_):
    
    
    admin_origin_ = php_parse_url(admin_url())
    home_origin_ = php_parse_url(home_url())
    #// @todo Preserve port?
    allowed_origins_ = array_unique(Array("http://" + admin_origin_["host"], "https://" + admin_origin_["host"], "http://" + home_origin_["host"], "https://" + home_origin_["host"]))
    #// 
    #// Change the origin types allowed for HTTP requests.
    #// 
    #// @since 3.4.0
    #// 
    #// @param string[] $allowed_origins {
    #// Array of default allowed HTTP origins.
    #// 
    #// @type string $0 Non-secure URL for admin origin.
    #// @type string $1 Secure URL for admin origin.
    #// @type string $2 Non-secure URL for home origin.
    #// @type string $3 Secure URL for home origin.
    #// }
    #//
    return apply_filters("allowed_http_origins", allowed_origins_)
# end def get_allowed_http_origins
#// 
#// Determines if the HTTP origin is an authorized one.
#// 
#// @since 3.4.0
#// 
#// @param null|string $origin Origin URL. If not provided, the value of get_http_origin() is used.
#// @return string Origin URL if allowed, empty string if not.
#//
def is_allowed_http_origin(origin_=None, *_args_):
    
    
    origin_arg_ = origin_
    if None == origin_:
        origin_ = get_http_origin()
    # end if
    if origin_ and (not php_in_array(origin_, get_allowed_http_origins())):
        origin_ = ""
    # end if
    #// 
    #// Change the allowed HTTP origin result.
    #// 
    #// @since 3.4.0
    #// 
    #// @param string $origin     Origin URL if allowed, empty string if not.
    #// @param string $origin_arg Original origin string passed into is_allowed_http_origin function.
    #//
    return apply_filters("allowed_http_origin", origin_, origin_arg_)
# end def is_allowed_http_origin
#// 
#// Send Access-Control-Allow-Origin and related headers if the current request
#// is from an allowed origin.
#// 
#// If the request is an OPTIONS request, the script exits with either access
#// control headers sent, or a 403 response if the origin is not allowed. For
#// other request methods, you will receive a return value.
#// 
#// @since 3.4.0
#// 
#// @return string|false Returns the origin URL if headers are sent. Returns false
#// if headers are not sent.
#//
def send_origin_headers(*_args_):
    
    
    origin_ = get_http_origin()
    if is_allowed_http_origin(origin_):
        php_header("Access-Control-Allow-Origin: " + origin_)
        php_header("Access-Control-Allow-Credentials: true")
        if "OPTIONS" == PHP_SERVER["REQUEST_METHOD"]:
            php_exit(0)
        # end if
        return origin_
    # end if
    if "OPTIONS" == PHP_SERVER["REQUEST_METHOD"]:
        status_header(403)
        php_exit(0)
    # end if
    return False
# end def send_origin_headers
#// 
#// Validate a URL for safe use in the HTTP API.
#// 
#// @since 3.5.2
#// 
#// @param string $url Request URL.
#// @return string|false URL or false on failure.
#//
def wp_http_validate_url(url_=None, *_args_):
    
    
    original_url_ = url_
    url_ = wp_kses_bad_protocol(url_, Array("http", "https"))
    if (not url_) or php_strtolower(url_) != php_strtolower(original_url_):
        return False
    # end if
    parsed_url_ = php_no_error(lambda: php_parse_url(url_))
    if (not parsed_url_) or php_empty(lambda : parsed_url_["host"]):
        return False
    # end if
    if (php_isset(lambda : parsed_url_["user"])) or (php_isset(lambda : parsed_url_["pass"])):
        return False
    # end if
    if False != strpbrk(parsed_url_["host"], ":#?[]"):
        return False
    # end if
    parsed_home_ = php_no_error(lambda: php_parse_url(get_option("home")))
    if (php_isset(lambda : parsed_home_["host"])):
        same_host_ = php_strtolower(parsed_home_["host"]) == php_strtolower(parsed_url_["host"])
    else:
        same_host_ = False
    # end if
    if (not same_host_):
        host_ = php_trim(parsed_url_["host"], ".")
        if php_preg_match("#^(([1-9]?\\d|1\\d\\d|25[0-5]|2[0-4]\\d)\\.){3}([1-9]?\\d|1\\d\\d|25[0-5]|2[0-4]\\d)$#", host_):
            ip_ = host_
        else:
            ip_ = gethostbyname(host_)
            if ip_ == host_:
                #// Error condition for gethostbyname().
                return False
            # end if
        # end if
        if ip_:
            parts_ = php_array_map("intval", php_explode(".", ip_))
            if 127 == parts_[0] or 10 == parts_[0] or 0 == parts_[0] or 172 == parts_[0] and 16 <= parts_[1] and 31 >= parts_[1] or 192 == parts_[0] and 168 == parts_[1]:
                #// If host appears local, reject unless specifically allowed.
                #// 
                #// Check if HTTP request is external or not.
                #// 
                #// Allows to change and allow external requests for the HTTP request.
                #// 
                #// @since 3.6.0
                #// 
                #// @param bool   $external Whether HTTP request is external or not.
                #// @param string $host     Host name of the requested URL.
                #// @param string $url      Requested URL.
                #//
                if (not apply_filters("http_request_host_is_external", False, host_, url_)):
                    return False
                # end if
            # end if
        # end if
    # end if
    if php_empty(lambda : parsed_url_["port"]):
        return url_
    # end if
    port_ = parsed_url_["port"]
    if 80 == port_ or 443 == port_ or 8080 == port_:
        return url_
    # end if
    if parsed_home_ and same_host_ and (php_isset(lambda : parsed_home_["port"])) and parsed_home_["port"] == port_:
        return url_
    # end if
    return False
# end def wp_http_validate_url
#// 
#// Whitelists allowed redirect hosts for safe HTTP requests as well.
#// 
#// Attached to the {@see 'http_request_host_is_external'} filter.
#// 
#// @since 3.6.0
#// 
#// @param bool   $is_external
#// @param string $host
#// @return bool
#//
def allowed_http_request_hosts(is_external_=None, host_=None, *_args_):
    
    
    if (not is_external_) and wp_validate_redirect("http://" + host_):
        is_external_ = True
    # end if
    return is_external_
# end def allowed_http_request_hosts
#// 
#// Whitelists any domain in a multisite installation for safe HTTP requests.
#// 
#// Attached to the {@see 'http_request_host_is_external'} filter.
#// 
#// @since 3.6.0
#// 
#// @global wpdb $wpdb WordPress database abstraction object.
#// @staticvar array $queried
#// 
#// @param bool   $is_external
#// @param string $host
#// @return bool
#//
def ms_allowed_http_request_hosts(is_external_=None, host_=None, *_args_):
    
    
    global wpdb_
    php_check_if_defined("wpdb_")
    queried_ = Array()
    if is_external_:
        return is_external_
    # end if
    if get_network().domain == host_:
        return True
    # end if
    if (php_isset(lambda : queried_[host_])):
        return queried_[host_]
    # end if
    queried_[host_] = php_bool(wpdb_.get_var(wpdb_.prepare(str("SELECT domain FROM ") + str(wpdb_.blogs) + str(" WHERE domain = %s LIMIT 1"), host_)))
    return queried_[host_]
# end def ms_allowed_http_request_hosts
#// 
#// A wrapper for PHP's parse_url() function that handles consistency in the return
#// values across PHP versions.
#// 
#// PHP 5.4.7 expanded parse_url()'s ability to handle non-absolute url's, including
#// schemeless and relative url's with :// in the path. This function works around
#// those limitations providing a standard output on PHP 5.2~5.4+.
#// 
#// Secondly, across various PHP versions, schemeless URLs starting containing a ":"
#// in the query are being handled inconsistently. This function works around those
#// differences as well.
#// 
#// Error suppression is used as prior to PHP 5.3.3, an E_WARNING would be generated
#// when URL parsing failed.
#// 
#// @since 4.4.0
#// @since 4.7.0 The `$component` parameter was added for parity with PHP's `parse_url()`.
#// 
#// @link https://www.php.net/manual/en/function.parse-url.php
#// 
#// @param string $url       The URL to parse.
#// @param int    $component The specific component to retrieve. Use one of the PHP
#// predefined constants to specify which one.
#// Defaults to -1 (= return all parts as an array).
#// @return mixed False on parse failure; Array of URL components on success;
#// When a specific component has been requested: null if the component
#// doesn't exist in the given URL; a string or - in the case of
#// PHP_URL_PORT - integer when it does. See parse_url()'s return values.
#//
def wp_parse_url(url_=None, component_=None, *_args_):
    if component_ is None:
        component_ = -1
    # end if
    
    to_unset_ = Array()
    url_ = php_strval(url_)
    if "//" == php_substr(url_, 0, 2):
        to_unset_[-1] = "scheme"
        url_ = "placeholder:" + url_
    elif "/" == php_substr(url_, 0, 1):
        to_unset_[-1] = "scheme"
        to_unset_[-1] = "host"
        url_ = "placeholder://placeholder" + url_
    # end if
    parts_ = php_no_error(lambda: php_parse_url(url_))
    if False == parts_:
        #// Parsing failure.
        return parts_
    # end if
    #// Remove the placeholder values.
    for key_ in to_unset_:
        parts_[key_] = None
    # end for
    return _get_component_from_parsed_url_array(parts_, component_)
# end def wp_parse_url
#// 
#// Retrieve a specific component from a parsed URL array.
#// 
#// @internal
#// 
#// @since 4.7.0
#// @access private
#// 
#// @link https://www.php.net/manual/en/function.parse-url.php
#// 
#// @param array|false $url_parts The parsed URL. Can be false if the URL failed to parse.
#// @param int         $component The specific component to retrieve. Use one of the PHP
#// predefined constants to specify which one.
#// Defaults to -1 (= return all parts as an array).
#// @return mixed False on parse failure; Array of URL components on success;
#// When a specific component has been requested: null if the component
#// doesn't exist in the given URL; a string or - in the case of
#// PHP_URL_PORT - integer when it does. See parse_url()'s return values.
#//
def _get_component_from_parsed_url_array(url_parts_=None, component_=None, *_args_):
    if component_ is None:
        component_ = -1
    # end if
    
    if -1 == component_:
        return url_parts_
    # end if
    key_ = _wp_translate_php_url_constant_to_key(component_)
    if False != key_ and php_is_array(url_parts_) and (php_isset(lambda : url_parts_[key_])):
        return url_parts_[key_]
    else:
        return None
    # end if
# end def _get_component_from_parsed_url_array
#// 
#// Translate a PHP_URL_* constant to the named array keys PHP uses.
#// 
#// @internal
#// 
#// @since 4.7.0
#// @access private
#// 
#// @link https://www.php.net/manual/en/url.constants.php
#// 
#// @param int $constant PHP_URL_* constant.
#// @return string|false The named key or false.
#//
def _wp_translate_php_url_constant_to_key(constant_=None, *_args_):
    
    
    translation_ = Array({PHP_URL_SCHEME: "scheme", PHP_URL_HOST: "host", PHP_URL_PORT: "port", PHP_URL_USER: "user", PHP_URL_PASS: "pass", PHP_URL_PATH: "path", PHP_URL_QUERY: "query", PHP_URL_FRAGMENT: "fragment"})
    if (php_isset(lambda : translation_[constant_])):
        return translation_[constant_]
    else:
        return False
    # end if
# end def _wp_translate_php_url_constant_to_key
