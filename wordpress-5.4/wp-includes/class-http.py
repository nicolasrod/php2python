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
#// HTTP API: WP_Http class
#// 
#// @package WordPress
#// @subpackage HTTP
#// @since 2.7.0
#//
if (not php_class_exists("Requests")):
    php_include_file(ABSPATH + WPINC + "/class-requests.php", once=False)
    Requests.register_autoloader()
    Requests.set_certificate_path(ABSPATH + WPINC + "/certificates/ca-bundle.crt")
# end if
#// 
#// Core class used for managing HTTP transports and making HTTP requests.
#// 
#// This class is used to consistently make outgoing HTTP requests easy for developers
#// while still being compatible with the many PHP configurations under which
#// WordPress runs.
#// 
#// Debugging includes several actions, which pass different variables for debugging the HTTP API.
#// 
#// @since 2.7.0
#//
class WP_Http():
    HTTP_CONTINUE = 100
    SWITCHING_PROTOCOLS = 101
    PROCESSING = 102
    EARLY_HINTS = 103
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NON_AUTHORITATIVE_INFORMATION = 203
    NO_CONTENT = 204
    RESET_CONTENT = 205
    PARTIAL_CONTENT = 206
    MULTI_STATUS = 207
    IM_USED = 226
    MULTIPLE_CHOICES = 300
    MOVED_PERMANENTLY = 301
    FOUND = 302
    SEE_OTHER = 303
    NOT_MODIFIED = 304
    USE_PROXY = 305
    RESERVED = 306
    TEMPORARY_REDIRECT = 307
    PERMANENT_REDIRECT = 308
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    PAYMENT_REQUIRED = 402
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    NOT_ACCEPTABLE = 406
    PROXY_AUTHENTICATION_REQUIRED = 407
    REQUEST_TIMEOUT = 408
    CONFLICT = 409
    GONE = 410
    LENGTH_REQUIRED = 411
    PRECONDITION_FAILED = 412
    REQUEST_ENTITY_TOO_LARGE = 413
    REQUEST_URI_TOO_LONG = 414
    UNSUPPORTED_MEDIA_TYPE = 415
    REQUESTED_RANGE_NOT_SATISFIABLE = 416
    EXPECTATION_FAILED = 417
    IM_A_TEAPOT = 418
    MISDIRECTED_REQUEST = 421
    UNPROCESSABLE_ENTITY = 422
    LOCKED = 423
    FAILED_DEPENDENCY = 424
    UPGRADE_REQUIRED = 426
    PRECONDITION_REQUIRED = 428
    TOO_MANY_REQUESTS = 429
    REQUEST_HEADER_FIELDS_TOO_LARGE = 431
    UNAVAILABLE_FOR_LEGAL_REASONS = 451
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504
    HTTP_VERSION_NOT_SUPPORTED = 505
    VARIANT_ALSO_NEGOTIATES = 506
    INSUFFICIENT_STORAGE = 507
    NOT_EXTENDED = 510
    NETWORK_AUTHENTICATION_REQUIRED = 511
    #// 
    #// Send an HTTP request to a URI.
    #// 
    #// Please note: The only URI that are supported in the HTTP Transport implementation
    #// are the HTTP and HTTPS protocols.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string       $url  The request URL.
    #// @param string|array $args {
    #// Optional. Array or string of HTTP request arguments.
    #// 
    #// @type string       $method              Request method. Accepts 'GET', 'POST', 'HEAD', 'PUT', 'DELETE',
    #// 'TRACE', 'OPTIONS', or 'PATCH'.
    #// Some transports technically allow others, but should not be
    #// assumed. Default 'GET'.
    #// @type float        $timeout             How long the connection should stay open in seconds. Default 5.
    #// @type int          $redirection         Number of allowed redirects. Not supported by all transports
    #// Default 5.
    #// @type string       $httpversion         Version of the HTTP protocol to use. Accepts '1.0' and '1.1'.
    #// Default '1.0'.
    #// @type string       $user-agent          User-agent value sent.
    #// Default 'WordPress/' . get_bloginfo( 'version' ) . '; ' . get_bloginfo( 'url' ).
    #// @type bool         $reject_unsafe_urls  Whether to pass URLs through wp_http_validate_url().
    #// Default false.
    #// @type bool         $blocking            Whether the calling code requires the result of the request.
    #// If set to false, the request will be sent to the remote server,
    #// and processing returned to the calling code immediately, the caller
    #// will know if the request succeeded or failed, but will not receive
    #// any response from the remote server. Default true.
    #// @type string|array $headers             Array or string of headers to send with the request.
    #// Default empty array.
    #// @type array        $cookies             List of cookies to send with the request. Default empty array.
    #// @type string|array $body                Body to send with the request. Default null.
    #// @type bool         $compress            Whether to compress the $body when sending the request.
    #// Default false.
    #// @type bool         $decompress          Whether to decompress a compressed response. If set to false and
    #// compressed content is returned in the response anyway, it will
    #// need to be separately decompressed. Default true.
    #// @type bool         $sslverify           Whether to verify SSL for the request. Default true.
    #// @type string       $sslcertificates     Absolute path to an SSL certificate .crt file.
    #// Default ABSPATH . WPINC . '/certificates/ca-bundle.crt'.
    #// @type bool         $stream              Whether to stream to a file. If set to true and no filename was
    #// given, it will be droped it in the WP temp dir and its name will
    #// be set using the basename of the URL. Default false.
    #// @type string       $filename            Filename of the file to write to when streaming. $stream must be
    #// set to true. Default null.
    #// @type int          $limit_response_size Size in bytes to limit the response to. Default null.
    #// 
    #// }
    #// @return array|WP_Error Array containing 'headers', 'body', 'response', 'cookies', 'filename'.
    #// A WP_Error instance upon error.
    #//
    def request(self, url_=None, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        defaults_ = Array({"method": "GET", "timeout": apply_filters("http_request_timeout", 5, url_), "redirection": apply_filters("http_request_redirection_count", 5, url_), "httpversion": apply_filters("http_request_version", "1.0", url_), "user-agent": apply_filters("http_headers_useragent", "WordPress/" + get_bloginfo("version") + "; " + get_bloginfo("url"), url_), "reject_unsafe_urls": apply_filters("http_request_reject_unsafe_urls", False, url_), "blocking": True, "headers": Array(), "cookies": Array(), "body": None, "compress": False, "decompress": True, "sslverify": True, "sslcertificates": ABSPATH + WPINC + "/certificates/ca-bundle.crt", "stream": False, "filename": None, "limit_response_size": None})
        #// Pre-parse for the HEAD checks.
        args_ = wp_parse_args(args_)
        #// By default, HEAD requests do not cause redirections.
        if (php_isset(lambda : args_["method"])) and "HEAD" == args_["method"]:
            defaults_["redirection"] = 0
        # end if
        parsed_args_ = wp_parse_args(args_, defaults_)
        #// 
        #// Filters the arguments used in an HTTP request.
        #// 
        #// @since 2.7.0
        #// 
        #// @param array  $parsed_args An array of HTTP request arguments.
        #// @param string $url         The request URL.
        #//
        parsed_args_ = apply_filters("http_request_args", parsed_args_, url_)
        #// The transports decrement this, store a copy of the original value for loop purposes.
        if (not (php_isset(lambda : parsed_args_["_redirection"]))):
            parsed_args_["_redirection"] = parsed_args_["redirection"]
        # end if
        #// 
        #// Filters whether to preempt an HTTP request's return value.
        #// 
        #// Returning a non-false value from the filter will short-circuit the HTTP request and return
        #// early with that value. A filter should return either:
        #// 
        #// - An array containing 'headers', 'body', 'response', 'cookies', and 'filename' elements
        #// - A WP_Error instance
        #// - boolean false (to avoid short-circuiting the response)
        #// 
        #// Returning any other value may result in unexpected behaviour.
        #// 
        #// @since 2.9.0
        #// 
        #// @param false|array|WP_Error $preempt     Whether to preempt an HTTP request's return value. Default false.
        #// @param array                $parsed_args HTTP request arguments.
        #// @param string               $url         The request URL.
        #//
        pre_ = apply_filters("pre_http_request", False, parsed_args_, url_)
        if False != pre_:
            return pre_
        # end if
        if php_function_exists("wp_kses_bad_protocol"):
            if parsed_args_["reject_unsafe_urls"]:
                url_ = wp_http_validate_url(url_)
            # end if
            if url_:
                url_ = wp_kses_bad_protocol(url_, Array("http", "https", "ssl"))
            # end if
        # end if
        arrURL_ = php_no_error(lambda: php_parse_url(url_))
        if php_empty(lambda : url_) or php_empty(lambda : arrURL_["scheme"]):
            response_ = php_new_class("WP_Error", lambda : WP_Error("http_request_failed", __("A valid URL was not provided.")))
            #// This action is documented in wp-includes/class-http.php
            do_action("http_api_debug", response_, "response", "Requests", parsed_args_, url_)
            return response_
        # end if
        if self.block_request(url_):
            response_ = php_new_class("WP_Error", lambda : WP_Error("http_request_not_executed", __("User has blocked requests through HTTP.")))
            #// This action is documented in wp-includes/class-http.php
            do_action("http_api_debug", response_, "response", "Requests", parsed_args_, url_)
            return response_
        # end if
        #// If we are streaming to a file but no filename was given drop it in the WP temp dir
        #// and pick its name using the basename of the $url.
        if parsed_args_["stream"]:
            if php_empty(lambda : parsed_args_["filename"]):
                parsed_args_["filename"] = get_temp_dir() + php_basename(url_)
            # end if
            #// Force some settings if we are streaming to a file and check for existence
            #// and perms of destination directory.
            parsed_args_["blocking"] = True
            if (not wp_is_writable(php_dirname(parsed_args_["filename"]))):
                response_ = php_new_class("WP_Error", lambda : WP_Error("http_request_failed", __("Destination directory for file streaming does not exist or is not writable.")))
                #// This action is documented in wp-includes/class-http.php
                do_action("http_api_debug", response_, "response", "Requests", parsed_args_, url_)
                return response_
            # end if
        # end if
        if php_is_null(parsed_args_["headers"]):
            parsed_args_["headers"] = Array()
        # end if
        #// WP allows passing in headers as a string, weirdly.
        if (not php_is_array(parsed_args_["headers"])):
            processedHeaders_ = WP_Http.processheaders(parsed_args_["headers"])
            parsed_args_["headers"] = processedHeaders_["headers"]
        # end if
        #// Setup arguments.
        headers_ = parsed_args_["headers"]
        data_ = parsed_args_["body"]
        type_ = parsed_args_["method"]
        options_ = Array({"timeout": parsed_args_["timeout"], "useragent": parsed_args_["user-agent"], "blocking": parsed_args_["blocking"], "hooks": php_new_class("WP_HTTP_Requests_Hooks", lambda : WP_HTTP_Requests_Hooks(url_, parsed_args_))})
        #// Ensure redirects follow browser behaviour.
        options_["hooks"].register("requests.before_redirect", Array(get_class(), "browser_redirect_compatibility"))
        #// Validate redirected URLs.
        if php_function_exists("wp_kses_bad_protocol") and parsed_args_["reject_unsafe_urls"]:
            options_["hooks"].register("requests.before_redirect", Array(get_class(), "validate_redirects"))
        # end if
        if parsed_args_["stream"]:
            options_["filename"] = parsed_args_["filename"]
        # end if
        if php_empty(lambda : parsed_args_["redirection"]):
            options_["follow_redirects"] = False
        else:
            options_["redirects"] = parsed_args_["redirection"]
        # end if
        #// Use byte limit, if we can.
        if (php_isset(lambda : parsed_args_["limit_response_size"])):
            options_["max_bytes"] = parsed_args_["limit_response_size"]
        # end if
        #// If we've got cookies, use and convert them to Requests_Cookie.
        if (not php_empty(lambda : parsed_args_["cookies"])):
            options_["cookies"] = WP_Http.normalize_cookies(parsed_args_["cookies"])
        # end if
        #// SSL certificate handling.
        if (not parsed_args_["sslverify"]):
            options_["verify"] = False
            options_["verifyname"] = False
        else:
            options_["verify"] = parsed_args_["sslcertificates"]
        # end if
        #// All non-GET/HEAD requests should put the arguments in the form body.
        if "HEAD" != type_ and "GET" != type_:
            options_["data_format"] = "body"
        # end if
        #// 
        #// Filters whether SSL should be verified for non-local requests.
        #// 
        #// @since 2.8.0
        #// @since 5.1.0 The `$url` parameter was added.
        #// 
        #// @param bool   $ssl_verify Whether to verify the SSL connection. Default true.
        #// @param string $url        The request URL.
        #//
        options_["verify"] = apply_filters("https_ssl_verify", options_["verify"], url_)
        #// Check for proxies.
        proxy_ = php_new_class("WP_HTTP_Proxy", lambda : WP_HTTP_Proxy())
        if proxy_.is_enabled() and proxy_.send_through_proxy(url_):
            options_["proxy"] = php_new_class("Requests_Proxy_HTTP", lambda : Requests_Proxy_HTTP(proxy_.host() + ":" + proxy_.port()))
            if proxy_.use_authentication():
                options_["proxy"].use_authentication = True
                options_["proxy"].user = proxy_.username()
                options_["proxy"].pass_ = proxy_.password()
            # end if
        # end if
        #// Avoid issues where mbstring.func_overload is enabled.
        mbstring_binary_safe_encoding()
        try: 
            requests_response_ = Requests.request(url_, headers_, data_, type_, options_)
            #// Convert the response into an array.
            http_response_ = php_new_class("WP_HTTP_Requests_Response", lambda : WP_HTTP_Requests_Response(requests_response_, parsed_args_["filename"]))
            response_ = http_response_.to_array()
            #// Add the original object to the array.
            response_["http_response"] = http_response_
        except Requests_Exception as e_:
            response_ = php_new_class("WP_Error", lambda : WP_Error("http_request_failed", e_.getmessage()))
        # end try
        reset_mbstring_encoding()
        #// 
        #// Fires after an HTTP API response is received and before the response is returned.
        #// 
        #// @since 2.8.0
        #// 
        #// @param array|WP_Error $response    HTTP response or WP_Error object.
        #// @param string         $context     Context under which the hook is fired.
        #// @param string         $class       HTTP transport used.
        #// @param array          $parsed_args HTTP request arguments.
        #// @param string         $url         The request URL.
        #//
        do_action("http_api_debug", response_, "response", "Requests", parsed_args_, url_)
        if is_wp_error(response_):
            return response_
        # end if
        if (not parsed_args_["blocking"]):
            return Array({"headers": Array(), "body": "", "response": Array({"code": False, "message": False})}, {"cookies": Array(), "http_response": None})
        # end if
        #// 
        #// Filters the HTTP API response immediately before the response is returned.
        #// 
        #// @since 2.9.0
        #// 
        #// @param array  $response    HTTP response.
        #// @param array  $parsed_args HTTP request arguments.
        #// @param string $url         The request URL.
        #//
        return apply_filters("http_response", response_, parsed_args_, url_)
    # end def request
    #// 
    #// Normalizes cookies for using in Requests.
    #// 
    #// @since 4.6.0
    #// 
    #// @param array $cookies Array of cookies to send with the request.
    #// @return Requests_Cookie_Jar Cookie holder object.
    #//
    @classmethod
    def normalize_cookies(self, cookies_=None):
        
        
        cookie_jar_ = php_new_class("Requests_Cookie_Jar", lambda : Requests_Cookie_Jar())
        for name_,value_ in cookies_.items():
            if type(value_).__name__ == "WP_Http_Cookie":
                cookie_jar_[value_.name] = php_new_class("Requests_Cookie", lambda : Requests_Cookie(value_.name, value_.value, value_.get_attributes(), Array({"host-only": value_.host_only})))
            elif php_is_scalar(value_):
                cookie_jar_[name_] = php_new_class("Requests_Cookie", lambda : Requests_Cookie(name_, value_))
            # end if
        # end for
        return cookie_jar_
    # end def normalize_cookies
    #// 
    #// Match redirect behaviour to browser handling.
    #// 
    #// Changes 302 redirects from POST to GET to match browser handling. Per
    #// RFC 7231, user agents can deviate from the strict reading of the
    #// specification for compatibility purposes.
    #// 
    #// @since 4.6.0
    #// 
    #// @param string            $location URL to redirect to.
    #// @param array             $headers  Headers for the redirect.
    #// @param string|array      $data     Body to send with the request.
    #// @param array             $options  Redirect request options.
    #// @param Requests_Response $original Response object.
    #//
    @classmethod
    def browser_redirect_compatibility(self, location_=None, headers_=None, data_=None, options_=None, original_=None):
        
        
        #// Browser compatibility.
        if 302 == original_.status_code:
            options_["type"] = Requests.GET
        # end if
    # end def browser_redirect_compatibility
    #// 
    #// Validate redirected URLs.
    #// 
    #// @since 4.7.5
    #// 
    #// @throws Requests_Exception On unsuccessful URL validation.
    #// @param string $location URL to redirect to.
    #//
    @classmethod
    def validate_redirects(self, location_=None):
        
        
        if (not wp_http_validate_url(location_)):
            raise php_new_class("Requests_Exception", lambda : Requests_Exception(__("A valid URL was not provided."), "wp_http.redirect_failed_validation"))
        # end if
    # end def validate_redirects
    #// 
    #// Tests which transports are capable of supporting the request.
    #// 
    #// @since 3.2.0
    #// 
    #// @param array $args Request arguments.
    #// @param string $url URL to Request.
    #// 
    #// @return string|false Class name for the first transport that claims to support the request.
    #// False if no transport claims to support the request.
    #//
    def _get_first_available_transport(self, args_=None, url_=None):
        if url_ is None:
            url_ = None
        # end if
        
        transports_ = Array("curl", "streams")
        #// 
        #// Filters which HTTP transports are available and in what order.
        #// 
        #// @since 3.7.0
        #// 
        #// @param string[] $transports Array of HTTP transports to check. Default array contains
        #// 'curl' and 'streams', in that order.
        #// @param array    $args       HTTP request arguments.
        #// @param string   $url        The URL to request.
        #//
        request_order_ = apply_filters("http_api_transports", transports_, args_, url_)
        #// Loop over each transport on each HTTP request looking for one which will serve this request's needs.
        for transport_ in request_order_:
            if php_in_array(transport_, transports_):
                transport_ = ucfirst(transport_)
            # end if
            class_ = "WP_Http_" + transport_
            #// Check to see if this transport is a possibility, calls the transport statically.
            if (not php_call_user_func(Array(class_, "test"), args_, url_)):
                continue
            # end if
            return class_
        # end for
        return False
    # end def _get_first_available_transport
    #// 
    #// Dispatches a HTTP request to a supporting transport.
    #// 
    #// Tests each transport in order to find a transport which matches the request arguments.
    #// Also caches the transport instance to be used later.
    #// 
    #// The order for requests is cURL, and then PHP Streams.
    #// 
    #// @since 3.2.0
    #// @deprecated 5.1.0 Use WP_Http::request()
    #// @see WP_Http::request()
    #// 
    #// @staticvar array $transports
    #// 
    #// @param string $url URL to Request.
    #// @param array $args Request arguments.
    #// @return array|WP_Error Array containing 'headers', 'body', 'response', 'cookies', 'filename'.
    #// A WP_Error instance upon error.
    #//
    def _dispatch_request(self, url_=None, args_=None):
        
        
        transports_ = Array()
        class_ = self._get_first_available_transport(args_, url_)
        if (not class_):
            return php_new_class("WP_Error", lambda : WP_Error("http_failure", __("There are no HTTP transports available which can complete the requested request.")))
        # end if
        #// Transport claims to support request, instantiate it and give it a whirl.
        if php_empty(lambda : transports_[class_]):
            transports_[class_] = php_new_class(class_, lambda : {**locals(), **globals()}[class_]())
        # end if
        response_ = transports_[class_].request(url_, args_)
        #// This action is documented in wp-includes/class-http.php
        do_action("http_api_debug", response_, "response", class_, args_, url_)
        if is_wp_error(response_):
            return response_
        # end if
        #// This filter is documented in wp-includes/class-http.php
        return apply_filters("http_response", response_, args_, url_)
    # end def _dispatch_request
    #// 
    #// Uses the POST HTTP method.
    #// 
    #// Used for sending data that is expected to be in the body.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string       $url  The request URL.
    #// @param string|array $args Optional. Override the defaults.
    #// @return array|WP_Error Array containing 'headers', 'body', 'response', 'cookies', 'filename'.
    #// A WP_Error instance upon error.
    #//
    def post(self, url_=None, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        defaults_ = Array({"method": "POST"})
        parsed_args_ = wp_parse_args(args_, defaults_)
        return self.request(url_, parsed_args_)
    # end def post
    #// 
    #// Uses the GET HTTP method.
    #// 
    #// Used for sending data that is expected to be in the body.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $url The request URL.
    #// @param string|array $args Optional. Override the defaults.
    #// @return array|WP_Error Array containing 'headers', 'body', 'response', 'cookies', 'filename'.
    #// A WP_Error instance upon error.
    #//
    def get(self, url_=None, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        defaults_ = Array({"method": "GET"})
        parsed_args_ = wp_parse_args(args_, defaults_)
        return self.request(url_, parsed_args_)
    # end def get
    #// 
    #// Uses the HEAD HTTP method.
    #// 
    #// Used for sending data that is expected to be in the body.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $url The request URL.
    #// @param string|array $args Optional. Override the defaults.
    #// @return array|WP_Error Array containing 'headers', 'body', 'response', 'cookies', 'filename'.
    #// A WP_Error instance upon error.
    #//
    def head(self, url_=None, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        defaults_ = Array({"method": "HEAD"})
        parsed_args_ = wp_parse_args(args_, defaults_)
        return self.request(url_, parsed_args_)
    # end def head
    #// 
    #// Parses the responses and splits the parts into headers and body.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $strResponse The full response string.
    #// @return array {
    #// Array with response headers and body.
    #// 
    #// @type string $headers HTTP response headers.
    #// @type string $body    HTTP response body.
    #// }
    #//
    @classmethod
    def processresponse(self, strResponse_=None):
        
        
        #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.MethodNameInvalid
        res_ = php_explode("\r\n\r\n", strResponse_, 2)
        return Array({"headers": res_[0], "body": res_[1] if (php_isset(lambda : res_[1])) else ""})
    # end def processresponse
    #// 
    #// Transform header string into an array.
    #// 
    #// If an array is given, then it is assumed to be raw header data with numeric keys with the
    #// headers as the values. No headers must be passed that were already processed.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string|array $headers
    #// @param string $url The URL that was requested.
    #// @return array Processed string headers. If duplicate headers are encountered,
    #// then a numbered array is returned as the value of that header-key.
    #//
    @classmethod
    def processheaders(self, headers_=None, url_=""):
        
        
        #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.MethodNameInvalid
        #// Split headers, one per array element.
        if php_is_string(headers_):
            #// Tolerate line terminator: CRLF = LF (RFC 2616 19.3).
            headers_ = php_str_replace("\r\n", "\n", headers_)
            #// 
            #// Unfold folded header fields. LWS = [CRLF] 1*( SP | HT ) <US-ASCII SP, space (32)>,
            #// <US-ASCII HT, horizontal-tab (9)> (RFC 2616 2.2).
            #//
            headers_ = php_preg_replace("/\\n[ \\t]/", " ", headers_)
            #// Create the headers array.
            headers_ = php_explode("\n", headers_)
        # end if
        response_ = Array({"code": 0, "message": ""})
        #// 
        #// If a redirection has taken place, The headers for each page request may have been passed.
        #// In this case, determine the final HTTP header and parse from there.
        #//
        i_ = php_count(headers_) - 1
        while i_ >= 0:
            
            if (not php_empty(lambda : headers_[i_])) and False == php_strpos(headers_[i_], ":"):
                headers_ = array_splice(headers_, i_)
                break
            # end if
            i_ -= 1
        # end while
        cookies_ = Array()
        newheaders_ = Array()
        for tempheader_ in headers_:
            if php_empty(lambda : tempheader_):
                continue
            # end if
            if False == php_strpos(tempheader_, ":"):
                stack_ = php_explode(" ", tempheader_, 3)
                stack_[-1] = ""
                response_["code"], response_["message"] = stack_
                continue
            # end if
            key_, value_ = php_explode(":", tempheader_, 2)
            key_ = php_strtolower(key_)
            value_ = php_trim(value_)
            if (php_isset(lambda : newheaders_[key_])):
                if (not php_is_array(newheaders_[key_])):
                    newheaders_[key_] = Array(newheaders_[key_])
                # end if
                newheaders_[key_][-1] = value_
            else:
                newheaders_[key_] = value_
            # end if
            if "set-cookie" == key_:
                cookies_[-1] = php_new_class("WP_Http_Cookie", lambda : WP_Http_Cookie(value_, url_))
            # end if
        # end for
        #// Cast the Response Code to an int.
        response_["code"] = php_intval(response_["code"])
        return Array({"response": response_, "headers": newheaders_, "cookies": cookies_})
    # end def processheaders
    #// 
    #// Takes the arguments for a ::request() and checks for the cookie array.
    #// 
    #// If it's found, then it upgrades any basic name => value pairs to WP_Http_Cookie instances,
    #// which are each parsed into strings and added to the Cookie: header (within the arguments array).
    #// Edits the array by reference.
    #// 
    #// @since 2.8.0
    #// 
    #// @param array $r Full array of args passed into ::request()
    #//
    @classmethod
    def buildcookieheader(self, r_=None):
        
        
        #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.MethodNameInvalid
        if (not php_empty(lambda : r_["cookies"])):
            #// Upgrade any name => value cookie pairs to WP_HTTP_Cookie instances.
            for name_,value_ in r_["cookies"].items():
                if (not php_is_object(value_)):
                    r_["cookies"][name_] = php_new_class("WP_Http_Cookie", lambda : WP_Http_Cookie(Array({"name": name_, "value": value_})))
                # end if
            # end for
            cookies_header_ = ""
            for cookie_ in r_["cookies"]:
                cookies_header_ += cookie_.getheadervalue() + "; "
            # end for
            cookies_header_ = php_substr(cookies_header_, 0, -2)
            r_["headers"]["cookie"] = cookies_header_
        # end if
    # end def buildcookieheader
    #// 
    #// Decodes chunk transfer-encoding, based off the HTTP 1.1 specification.
    #// 
    #// Based off the HTTP http_encoding_dechunk function.
    #// 
    #// @link https://tools.ietf.org/html/rfc2616#section-19.4.6 Process for chunked decoding.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $body Body content.
    #// @return string Chunked decoded body on success or raw body on failure.
    #//
    @classmethod
    def chunktransferdecode(self, body_=None):
        
        
        #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.MethodNameInvalid
        #// The body is not chunked encoded or is malformed.
        if (not php_preg_match("/^([0-9a-f]+)[^\\r\\n]*\\r\\n/i", php_trim(body_))):
            return body_
        # end if
        parsed_body_ = ""
        #// We'll be altering $body, so need a backup in case of error.
        body_original_ = body_
        while True:
            
            if not (True):
                break
            # end if
            has_chunk_ = php_bool(php_preg_match("/^([0-9a-f]+)[^\\r\\n]*\\r\\n/i", body_, match_))
            if (not has_chunk_) or php_empty(lambda : match_[1]):
                return body_original_
            # end if
            length_ = hexdec(match_[1])
            chunk_length_ = php_strlen(match_[0])
            #// Parse out the chunk of data.
            parsed_body_ += php_substr(body_, chunk_length_, length_)
            #// Remove the chunk from the raw data.
            body_ = php_substr(body_, length_ + chunk_length_)
            #// End of the document.
            if "0" == php_trim(body_):
                return parsed_body_
            # end if
        # end while
    # end def chunktransferdecode
    #// 
    #// Determines whether an HTTP API request to the given URL should be blocked.
    #// 
    #// Those who are behind a proxy and want to prevent access to certain hosts may do so. This will
    #// prevent plugins from working and core functionality, if you don't include `api.wordpress.org`.
    #// 
    #// You block external URL requests by defining `WP_HTTP_BLOCK_EXTERNAL` as true in your `wp-config.php`
    #// file and this will only allow localhost and your site to make requests. The constant
    #// `WP_ACCESSIBLE_HOSTS` will allow additional hosts to go through for requests. The format of the
    #// `WP_ACCESSIBLE_HOSTS` constant is a comma separated list of hostnames to allow, wildcard domains
    #// are supported, eg `*.wordpress.org` will allow for all subdomains of `wordpress.org` to be contacted.
    #// 
    #// @since 2.8.0
    #// @link https://core.trac.wordpress.org/ticket/8927 Allow preventing external requests.
    #// @link https://core.trac.wordpress.org/ticket/14636 Allow wildcard domains in WP_ACCESSIBLE_HOSTS
    #// 
    #// @staticvar array|null $accessible_hosts
    #// @staticvar array      $wildcard_regex
    #// 
    #// @param string $uri URI of url.
    #// @return bool True to block, false to allow.
    #//
    def block_request(self, uri_=None):
        
        
        #// We don't need to block requests, because nothing is blocked.
        if (not php_defined("WP_HTTP_BLOCK_EXTERNAL")) or (not WP_HTTP_BLOCK_EXTERNAL):
            return False
        # end if
        check_ = php_parse_url(uri_)
        if (not check_):
            return True
        # end if
        home_ = php_parse_url(get_option("siteurl"))
        #// Don't block requests back to ourselves by default.
        if "localhost" == check_["host"] or (php_isset(lambda : home_["host"])) and home_["host"] == check_["host"]:
            #// 
            #// Filters whether to block local HTTP API requests.
            #// 
            #// A local request is one to `localhost` or to the same host as the site itself.
            #// 
            #// @since 2.8.0
            #// 
            #// @param bool $block Whether to block local requests. Default false.
            #//
            return apply_filters("block_local_requests", False)
        # end if
        if (not php_defined("WP_ACCESSIBLE_HOSTS")):
            return True
        # end if
        accessible_hosts_ = None
        wildcard_regex_ = Array()
        if None == accessible_hosts_:
            accessible_hosts_ = php_preg_split("|,\\s*|", WP_ACCESSIBLE_HOSTS)
            if False != php_strpos(WP_ACCESSIBLE_HOSTS, "*"):
                wildcard_regex_ = Array()
                for host_ in accessible_hosts_:
                    wildcard_regex_[-1] = php_str_replace("\\*", ".+", preg_quote(host_, "/"))
                # end for
                wildcard_regex_ = "/^(" + php_implode("|", wildcard_regex_) + ")$/i"
            # end if
        # end if
        if (not php_empty(lambda : wildcard_regex_)):
            return (not php_preg_match(wildcard_regex_, check_["host"]))
        else:
            return (not php_in_array(check_["host"], accessible_hosts_))
            pass
        # end if
    # end def block_request
    #// 
    #// Used as a wrapper for PHP's parse_url() function that handles edgecases in < PHP 5.4.7.
    #// 
    #// @deprecated 4.4.0 Use wp_parse_url()
    #// @see wp_parse_url()
    #// 
    #// @param string $url The URL to parse.
    #// @return bool|array False on failure; Array of URL components on success;
    #// See parse_url()'s return values.
    #//
    def parse_url(self, url_=None):
        
        
        _deprecated_function(__METHOD__, "4.4.0", "wp_parse_url()")
        return wp_parse_url(url_)
    # end def parse_url
    #// 
    #// Converts a relative URL to an absolute URL relative to a given URL.
    #// 
    #// If an Absolute URL is provided, no processing of that URL is done.
    #// 
    #// @since 3.4.0
    #// 
    #// @param string $maybe_relative_path The URL which might be relative.
    #// @param string $url                 The URL which $maybe_relative_path is relative to.
    #// @return string An Absolute URL, in a failure condition where the URL cannot be parsed, the relative URL will be returned.
    #//
    @classmethod
    def make_absolute_url(self, maybe_relative_path_=None, url_=None):
        
        
        if php_empty(lambda : url_):
            return maybe_relative_path_
        # end if
        url_parts_ = wp_parse_url(url_)
        if (not url_parts_):
            return maybe_relative_path_
        # end if
        relative_url_parts_ = wp_parse_url(maybe_relative_path_)
        if (not relative_url_parts_):
            return maybe_relative_path_
        # end if
        #// Check for a scheme on the 'relative' URL.
        if (not php_empty(lambda : relative_url_parts_["scheme"])):
            return maybe_relative_path_
        # end if
        absolute_path_ = url_parts_["scheme"] + "://"
        #// Schemeless URLs will make it this far, so we check for a host in the relative URL
        #// and convert it to a protocol-URL.
        if (php_isset(lambda : relative_url_parts_["host"])):
            absolute_path_ += relative_url_parts_["host"]
            if (php_isset(lambda : relative_url_parts_["port"])):
                absolute_path_ += ":" + relative_url_parts_["port"]
            # end if
        else:
            absolute_path_ += url_parts_["host"]
            if (php_isset(lambda : url_parts_["port"])):
                absolute_path_ += ":" + url_parts_["port"]
            # end if
        # end if
        #// Start off with the absolute URL path.
        path_ = url_parts_["path"] if (not php_empty(lambda : url_parts_["path"])) else "/"
        #// If it's a root-relative path, then great.
        if (not php_empty(lambda : relative_url_parts_["path"])) and "/" == relative_url_parts_["path"][0]:
            path_ = relative_url_parts_["path"]
            pass
        elif (not php_empty(lambda : relative_url_parts_["path"])):
            #// Strip off any file components from the absolute path.
            path_ = php_substr(path_, 0, php_strrpos(path_, "/") + 1)
            #// Build the new path.
            path_ += relative_url_parts_["path"]
            #// Strip all /path/../ out of the path.
            while True:
                
                if not (php_strpos(path_, "../") > 1):
                    break
                # end if
                path_ = php_preg_replace("![^/]+/\\.\\./!", "", path_)
            # end while
            #// Strip any final leading ../ from the path.
            path_ = php_preg_replace("!^/(\\.\\./)+!", "", path_)
        # end if
        #// Add the query string.
        if (not php_empty(lambda : relative_url_parts_["query"])):
            path_ += "?" + relative_url_parts_["query"]
        # end if
        return absolute_path_ + "/" + php_ltrim(path_, "/")
    # end def make_absolute_url
    #// 
    #// Handles an HTTP redirect and follows it if appropriate.
    #// 
    #// @since 3.7.0
    #// 
    #// @param string $url      The URL which was requested.
    #// @param array  $args     The arguments which were used to make the request.
    #// @param array  $response The response of the HTTP request.
    #// @return array|false|WP_Error An HTTP API response array if the redirect is successfully followed,
    #// false if no redirect is present, or a WP_Error object if there's an error.
    #//
    @classmethod
    def handle_redirects(self, url_=None, args_=None, response_=None):
        
        
        #// If no redirects are present, or, redirects were not requested, perform no action.
        if (not (php_isset(lambda : response_["headers"]["location"]))) or 0 == args_["_redirection"]:
            return False
        # end if
        #// Only perform redirections on redirection http codes.
        if response_["response"]["code"] > 399 or response_["response"]["code"] < 300:
            return False
        # end if
        #// Don't redirect if we've run out of redirects.
        if args_["redirection"] <= 0:
            return php_new_class("WP_Error", lambda : WP_Error("http_request_failed", __("Too many redirects.")))
        # end if
        args_["redirection"] -= 1
        redirect_location_ = response_["headers"]["location"]
        #// If there were multiple Location headers, use the last header specified.
        if php_is_array(redirect_location_):
            redirect_location_ = php_array_pop(redirect_location_)
        # end if
        redirect_location_ = WP_Http.make_absolute_url(redirect_location_, url_)
        #// POST requests should not POST to a redirected location.
        if "POST" == args_["method"]:
            if php_in_array(response_["response"]["code"], Array(302, 303)):
                args_["method"] = "GET"
            # end if
        # end if
        #// Include valid cookies in the redirect process.
        if (not php_empty(lambda : response_["cookies"])):
            for cookie_ in response_["cookies"]:
                if cookie_.test(redirect_location_):
                    args_["cookies"][-1] = cookie_
                # end if
            # end for
        # end if
        return wp_remote_request(redirect_location_, args_)
    # end def handle_redirects
    #// 
    #// Determines if a specified string represents an IP address or not.
    #// 
    #// This function also detects the type of the IP address, returning either
    #// '4' or '6' to represent a IPv4 and IPv6 address respectively.
    #// This does not verify if the IP is a valid IP, only that it appears to be
    #// an IP address.
    #// 
    #// @link http://home.deds.nl/~aeron/regex/ for IPv6 regex.
    #// 
    #// @since 3.7.0
    #// 
    #// @param string $maybe_ip A suspected IP address.
    #// @return integer|bool Upon success, '4' or '6' to represent a IPv4 or IPv6 address, false upon failure
    #//
    @classmethod
    def is_ip_address(self, maybe_ip_=None):
        
        
        if php_preg_match("/^\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}$/", maybe_ip_):
            return 4
        # end if
        if False != php_strpos(maybe_ip_, ":") and php_preg_match("/^(((?=.*(::))(?!.*\\3.+\\3))\\3?|([\\dA-F]{1,4}(\\3|:\\b|$)|\\2))(?4){5}((?4){2}|(((2[0-4]|1\\d|[1-9])?\\d|25[0-5])\\.?\\b){4})$/i", php_trim(maybe_ip_, " []")):
            return 6
        # end if
        return False
    # end def is_ip_address
# end class WP_Http
