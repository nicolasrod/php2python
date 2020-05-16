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
    def request(self, url=None, args=Array()):
        
        defaults = Array({"method": "GET", "timeout": apply_filters("http_request_timeout", 5, url), "redirection": apply_filters("http_request_redirection_count", 5, url), "httpversion": apply_filters("http_request_version", "1.0", url), "user-agent": apply_filters("http_headers_useragent", "WordPress/" + get_bloginfo("version") + "; " + get_bloginfo("url"), url), "reject_unsafe_urls": apply_filters("http_request_reject_unsafe_urls", False, url), "blocking": True, "headers": Array(), "cookies": Array(), "body": None, "compress": False, "decompress": True, "sslverify": True, "sslcertificates": ABSPATH + WPINC + "/certificates/ca-bundle.crt", "stream": False, "filename": None, "limit_response_size": None})
        #// Pre-parse for the HEAD checks.
        args = wp_parse_args(args)
        #// By default, HEAD requests do not cause redirections.
        if (php_isset(lambda : args["method"])) and "HEAD" == args["method"]:
            defaults["redirection"] = 0
        # end if
        parsed_args = wp_parse_args(args, defaults)
        #// 
        #// Filters the arguments used in an HTTP request.
        #// 
        #// @since 2.7.0
        #// 
        #// @param array  $parsed_args An array of HTTP request arguments.
        #// @param string $url         The request URL.
        #//
        parsed_args = apply_filters("http_request_args", parsed_args, url)
        #// The transports decrement this, store a copy of the original value for loop purposes.
        if (not (php_isset(lambda : parsed_args["_redirection"]))):
            parsed_args["_redirection"] = parsed_args["redirection"]
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
        pre = apply_filters("pre_http_request", False, parsed_args, url)
        if False != pre:
            return pre
        # end if
        if php_function_exists("wp_kses_bad_protocol"):
            if parsed_args["reject_unsafe_urls"]:
                url = wp_http_validate_url(url)
            # end if
            if url:
                url = wp_kses_bad_protocol(url, Array("http", "https", "ssl"))
            # end if
        # end if
        arrURL = php_no_error(lambda: php_parse_url(url))
        if php_empty(lambda : url) or php_empty(lambda : arrURL["scheme"]):
            response = php_new_class("WP_Error", lambda : WP_Error("http_request_failed", __("A valid URL was not provided.")))
            #// This action is documented in wp-includes/class-http.php
            do_action("http_api_debug", response, "response", "Requests", parsed_args, url)
            return response
        # end if
        if self.block_request(url):
            response = php_new_class("WP_Error", lambda : WP_Error("http_request_not_executed", __("User has blocked requests through HTTP.")))
            #// This action is documented in wp-includes/class-http.php
            do_action("http_api_debug", response, "response", "Requests", parsed_args, url)
            return response
        # end if
        #// If we are streaming to a file but no filename was given drop it in the WP temp dir
        #// and pick its name using the basename of the $url.
        if parsed_args["stream"]:
            if php_empty(lambda : parsed_args["filename"]):
                parsed_args["filename"] = get_temp_dir() + php_basename(url)
            # end if
            #// Force some settings if we are streaming to a file and check for existence
            #// and perms of destination directory.
            parsed_args["blocking"] = True
            if (not wp_is_writable(php_dirname(parsed_args["filename"]))):
                response = php_new_class("WP_Error", lambda : WP_Error("http_request_failed", __("Destination directory for file streaming does not exist or is not writable.")))
                #// This action is documented in wp-includes/class-http.php
                do_action("http_api_debug", response, "response", "Requests", parsed_args, url)
                return response
            # end if
        # end if
        if is_null(parsed_args["headers"]):
            parsed_args["headers"] = Array()
        # end if
        #// WP allows passing in headers as a string, weirdly.
        if (not php_is_array(parsed_args["headers"])):
            processedHeaders = WP_Http.processheaders(parsed_args["headers"])
            parsed_args["headers"] = processedHeaders["headers"]
        # end if
        #// Setup arguments.
        headers = parsed_args["headers"]
        data = parsed_args["body"]
        type = parsed_args["method"]
        options = Array({"timeout": parsed_args["timeout"], "useragent": parsed_args["user-agent"], "blocking": parsed_args["blocking"], "hooks": php_new_class("WP_HTTP_Requests_Hooks", lambda : WP_HTTP_Requests_Hooks(url, parsed_args))})
        #// Ensure redirects follow browser behaviour.
        options["hooks"].register("requests.before_redirect", Array(get_class(), "browser_redirect_compatibility"))
        #// Validate redirected URLs.
        if php_function_exists("wp_kses_bad_protocol") and parsed_args["reject_unsafe_urls"]:
            options["hooks"].register("requests.before_redirect", Array(get_class(), "validate_redirects"))
        # end if
        if parsed_args["stream"]:
            options["filename"] = parsed_args["filename"]
        # end if
        if php_empty(lambda : parsed_args["redirection"]):
            options["follow_redirects"] = False
        else:
            options["redirects"] = parsed_args["redirection"]
        # end if
        #// Use byte limit, if we can.
        if (php_isset(lambda : parsed_args["limit_response_size"])):
            options["max_bytes"] = parsed_args["limit_response_size"]
        # end if
        #// If we've got cookies, use and convert them to Requests_Cookie.
        if (not php_empty(lambda : parsed_args["cookies"])):
            options["cookies"] = WP_Http.normalize_cookies(parsed_args["cookies"])
        # end if
        #// SSL certificate handling.
        if (not parsed_args["sslverify"]):
            options["verify"] = False
            options["verifyname"] = False
        else:
            options["verify"] = parsed_args["sslcertificates"]
        # end if
        #// All non-GET/HEAD requests should put the arguments in the form body.
        if "HEAD" != type and "GET" != type:
            options["data_format"] = "body"
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
        options["verify"] = apply_filters("https_ssl_verify", options["verify"], url)
        #// Check for proxies.
        proxy = php_new_class("WP_HTTP_Proxy", lambda : WP_HTTP_Proxy())
        if proxy.is_enabled() and proxy.send_through_proxy(url):
            options["proxy"] = php_new_class("Requests_Proxy_HTTP", lambda : Requests_Proxy_HTTP(proxy.host() + ":" + proxy.port()))
            if proxy.use_authentication():
                options["proxy"].use_authentication = True
                options["proxy"].user = proxy.username()
                options["proxy"].pass_ = proxy.password()
            # end if
        # end if
        #// Avoid issues where mbstring.func_overload is enabled.
        mbstring_binary_safe_encoding()
        try: 
            requests_response = Requests.request(url, headers, data, type, options)
            #// Convert the response into an array.
            http_response = php_new_class("WP_HTTP_Requests_Response", lambda : WP_HTTP_Requests_Response(requests_response, parsed_args["filename"]))
            response = http_response.to_array()
            #// Add the original object to the array.
            response["http_response"] = http_response
        except Requests_Exception as e:
            response = php_new_class("WP_Error", lambda : WP_Error("http_request_failed", e.getmessage()))
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
        do_action("http_api_debug", response, "response", "Requests", parsed_args, url)
        if is_wp_error(response):
            return response
        # end if
        if (not parsed_args["blocking"]):
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
        return apply_filters("http_response", response, parsed_args, url)
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
    def normalize_cookies(self, cookies=None):
        
        cookie_jar = php_new_class("Requests_Cookie_Jar", lambda : Requests_Cookie_Jar())
        for name,value in cookies:
            if type(value).__name__ == "WP_Http_Cookie":
                cookie_jar[value.name] = php_new_class("Requests_Cookie", lambda : Requests_Cookie(value.name, value.value, value.get_attributes(), Array({"host-only": value.host_only})))
            elif is_scalar(value):
                cookie_jar[name] = php_new_class("Requests_Cookie", lambda : Requests_Cookie(name, value))
            # end if
        # end for
        return cookie_jar
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
    def browser_redirect_compatibility(self, location=None, headers=None, data=None, options=None, original=None):
        
        #// Browser compatibility.
        if 302 == original.status_code:
            options["type"] = Requests.GET
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
    def validate_redirects(self, location=None):
        
        if (not wp_http_validate_url(location)):
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
    def _get_first_available_transport(self, args=None, url=None):
        
        transports = Array("curl", "streams")
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
        request_order = apply_filters("http_api_transports", transports, args, url)
        #// Loop over each transport on each HTTP request looking for one which will serve this request's needs.
        for transport in request_order:
            if php_in_array(transport, transports):
                transport = ucfirst(transport)
            # end if
            class_ = "WP_Http_" + transport
            #// Check to see if this transport is a possibility, calls the transport statically.
            if (not php_call_user_func(Array(class_, "test"), args, url)):
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
    def _dispatch_request(self, url=None, args=None):
        
        transports = Array()
        class_ = self._get_first_available_transport(args, url)
        if (not class_):
            return php_new_class("WP_Error", lambda : WP_Error("http_failure", __("There are no HTTP transports available which can complete the requested request.")))
        # end if
        #// Transport claims to support request, instantiate it and give it a whirl.
        if php_empty(lambda : transports[class_]):
            transports[class_] = php_new_class(class_, lambda : {**locals(), **globals()}[class_]())
        # end if
        response = transports[class_].request(url, args)
        #// This action is documented in wp-includes/class-http.php
        do_action("http_api_debug", response, "response", class_, args, url)
        if is_wp_error(response):
            return response
        # end if
        #// This filter is documented in wp-includes/class-http.php
        return apply_filters("http_response", response, args, url)
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
    def post(self, url=None, args=Array()):
        
        defaults = Array({"method": "POST"})
        parsed_args = wp_parse_args(args, defaults)
        return self.request(url, parsed_args)
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
    def get(self, url=None, args=Array()):
        
        defaults = Array({"method": "GET"})
        parsed_args = wp_parse_args(args, defaults)
        return self.request(url, parsed_args)
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
    def head(self, url=None, args=Array()):
        
        defaults = Array({"method": "HEAD"})
        parsed_args = wp_parse_args(args, defaults)
        return self.request(url, parsed_args)
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
    def processresponse(self, strResponse=None):
        
        #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.MethodNameInvalid
        res = php_explode("\r\n\r\n", strResponse, 2)
        return Array({"headers": res[0], "body": res[1] if (php_isset(lambda : res[1])) else ""})
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
    def processheaders(self, headers=None, url=""):
        
        #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.MethodNameInvalid
        #// Split headers, one per array element.
        if php_is_string(headers):
            #// Tolerate line terminator: CRLF = LF (RFC 2616 19.3).
            headers = php_str_replace("\r\n", "\n", headers)
            #// 
            #// Unfold folded header fields. LWS = [CRLF] 1*( SP | HT ) <US-ASCII SP, space (32)>,
            #// <US-ASCII HT, horizontal-tab (9)> (RFC 2616 2.2).
            #//
            headers = php_preg_replace("/\\n[ \\t]/", " ", headers)
            #// Create the headers array.
            headers = php_explode("\n", headers)
        # end if
        response = Array({"code": 0, "message": ""})
        #// 
        #// If a redirection has taken place, The headers for each page request may have been passed.
        #// In this case, determine the final HTTP header and parse from there.
        #//
        i = php_count(headers) - 1
        while i >= 0:
            
            if (not php_empty(lambda : headers[i])) and False == php_strpos(headers[i], ":"):
                headers = array_splice(headers, i)
                break
            # end if
            i -= 1
        # end while
        cookies = Array()
        newheaders = Array()
        for tempheader in headers:
            if php_empty(lambda : tempheader):
                continue
            # end if
            if False == php_strpos(tempheader, ":"):
                stack = php_explode(" ", tempheader, 3)
                stack[-1] = ""
                response["code"], response["message"] = stack
                continue
            # end if
            key, value = php_explode(":", tempheader, 2)
            key = php_strtolower(key)
            value = php_trim(value)
            if (php_isset(lambda : newheaders[key])):
                if (not php_is_array(newheaders[key])):
                    newheaders[key] = Array(newheaders[key])
                # end if
                newheaders[key][-1] = value
            else:
                newheaders[key] = value
            # end if
            if "set-cookie" == key:
                cookies[-1] = php_new_class("WP_Http_Cookie", lambda : WP_Http_Cookie(value, url))
            # end if
        # end for
        #// Cast the Response Code to an int.
        response["code"] = php_intval(response["code"])
        return Array({"response": response, "headers": newheaders, "cookies": cookies})
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
    def buildcookieheader(self, r=None):
        
        #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.MethodNameInvalid
        if (not php_empty(lambda : r["cookies"])):
            #// Upgrade any name => value cookie pairs to WP_HTTP_Cookie instances.
            for name,value in r["cookies"]:
                if (not php_is_object(value)):
                    r["cookies"][name] = php_new_class("WP_Http_Cookie", lambda : WP_Http_Cookie(Array({"name": name, "value": value})))
                # end if
            # end for
            cookies_header = ""
            for cookie in r["cookies"]:
                cookies_header += cookie.getheadervalue() + "; "
            # end for
            cookies_header = php_substr(cookies_header, 0, -2)
            r["headers"]["cookie"] = cookies_header
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
    def chunktransferdecode(self, body=None):
        
        #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.MethodNameInvalid
        #// The body is not chunked encoded or is malformed.
        if (not php_preg_match("/^([0-9a-f]+)[^\\r\\n]*\\r\\n/i", php_trim(body))):
            return body
        # end if
        parsed_body = ""
        #// We'll be altering $body, so need a backup in case of error.
        body_original = body
        while True:
            
            if not (True):
                break
            # end if
            has_chunk = php_bool(php_preg_match("/^([0-9a-f]+)[^\\r\\n]*\\r\\n/i", body, match))
            if (not has_chunk) or php_empty(lambda : match[1]):
                return body_original
            # end if
            length = hexdec(match[1])
            chunk_length = php_strlen(match[0])
            #// Parse out the chunk of data.
            parsed_body += php_substr(body, chunk_length, length)
            #// Remove the chunk from the raw data.
            body = php_substr(body, length + chunk_length)
            #// End of the document.
            if "0" == php_trim(body):
                return parsed_body
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
    def block_request(self, uri=None):
        
        #// We don't need to block requests, because nothing is blocked.
        if (not php_defined("WP_HTTP_BLOCK_EXTERNAL")) or (not WP_HTTP_BLOCK_EXTERNAL):
            return False
        # end if
        check = php_parse_url(uri)
        if (not check):
            return True
        # end if
        home = php_parse_url(get_option("siteurl"))
        #// Don't block requests back to ourselves by default.
        if "localhost" == check["host"] or (php_isset(lambda : home["host"])) and home["host"] == check["host"]:
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
        accessible_hosts = None
        wildcard_regex = Array()
        if None == accessible_hosts:
            accessible_hosts = php_preg_split("|,\\s*|", WP_ACCESSIBLE_HOSTS)
            if False != php_strpos(WP_ACCESSIBLE_HOSTS, "*"):
                wildcard_regex = Array()
                for host in accessible_hosts:
                    wildcard_regex[-1] = php_str_replace("\\*", ".+", preg_quote(host, "/"))
                # end for
                wildcard_regex = "/^(" + php_implode("|", wildcard_regex) + ")$/i"
            # end if
        # end if
        if (not php_empty(lambda : wildcard_regex)):
            return (not php_preg_match(wildcard_regex, check["host"]))
        else:
            return (not php_in_array(check["host"], accessible_hosts))
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
    def parse_url(self, url=None):
        
        _deprecated_function(__METHOD__, "4.4.0", "wp_parse_url()")
        return wp_parse_url(url)
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
    def make_absolute_url(self, maybe_relative_path=None, url=None):
        
        if php_empty(lambda : url):
            return maybe_relative_path
        # end if
        url_parts = wp_parse_url(url)
        if (not url_parts):
            return maybe_relative_path
        # end if
        relative_url_parts = wp_parse_url(maybe_relative_path)
        if (not relative_url_parts):
            return maybe_relative_path
        # end if
        #// Check for a scheme on the 'relative' URL.
        if (not php_empty(lambda : relative_url_parts["scheme"])):
            return maybe_relative_path
        # end if
        absolute_path = url_parts["scheme"] + "://"
        #// Schemeless URLs will make it this far, so we check for a host in the relative URL
        #// and convert it to a protocol-URL.
        if (php_isset(lambda : relative_url_parts["host"])):
            absolute_path += relative_url_parts["host"]
            if (php_isset(lambda : relative_url_parts["port"])):
                absolute_path += ":" + relative_url_parts["port"]
            # end if
        else:
            absolute_path += url_parts["host"]
            if (php_isset(lambda : url_parts["port"])):
                absolute_path += ":" + url_parts["port"]
            # end if
        # end if
        #// Start off with the absolute URL path.
        path = url_parts["path"] if (not php_empty(lambda : url_parts["path"])) else "/"
        #// If it's a root-relative path, then great.
        if (not php_empty(lambda : relative_url_parts["path"])) and "/" == relative_url_parts["path"][0]:
            path = relative_url_parts["path"]
            pass
        elif (not php_empty(lambda : relative_url_parts["path"])):
            #// Strip off any file components from the absolute path.
            path = php_substr(path, 0, php_strrpos(path, "/") + 1)
            #// Build the new path.
            path += relative_url_parts["path"]
            #// Strip all /path/../ out of the path.
            while True:
                
                if not (php_strpos(path, "../") > 1):
                    break
                # end if
                path = php_preg_replace("![^/]+/\\.\\./!", "", path)
            # end while
            #// Strip any final leading ../ from the path.
            path = php_preg_replace("!^/(\\.\\./)+!", "", path)
        # end if
        #// Add the query string.
        if (not php_empty(lambda : relative_url_parts["query"])):
            path += "?" + relative_url_parts["query"]
        # end if
        return absolute_path + "/" + php_ltrim(path, "/")
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
    def handle_redirects(self, url=None, args=None, response=None):
        
        #// If no redirects are present, or, redirects were not requested, perform no action.
        if (not (php_isset(lambda : response["headers"]["location"]))) or 0 == args["_redirection"]:
            return False
        # end if
        #// Only perform redirections on redirection http codes.
        if response["response"]["code"] > 399 or response["response"]["code"] < 300:
            return False
        # end if
        #// Don't redirect if we've run out of redirects.
        if args["redirection"] <= 0:
            return php_new_class("WP_Error", lambda : WP_Error("http_request_failed", __("Too many redirects.")))
        # end if
        args["redirection"] -= 1
        redirect_location = response["headers"]["location"]
        #// If there were multiple Location headers, use the last header specified.
        if php_is_array(redirect_location):
            redirect_location = php_array_pop(redirect_location)
        # end if
        redirect_location = WP_Http.make_absolute_url(redirect_location, url)
        #// POST requests should not POST to a redirected location.
        if "POST" == args["method"]:
            if php_in_array(response["response"]["code"], Array(302, 303)):
                args["method"] = "GET"
            # end if
        # end if
        #// Include valid cookies in the redirect process.
        if (not php_empty(lambda : response["cookies"])):
            for cookie in response["cookies"]:
                if cookie.test(redirect_location):
                    args["cookies"][-1] = cookie
                # end if
            # end for
        # end if
        return wp_remote_request(redirect_location, args)
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
    def is_ip_address(self, maybe_ip=None):
        
        if php_preg_match("/^\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}$/", maybe_ip):
            return 4
        # end if
        if False != php_strpos(maybe_ip, ":") and php_preg_match("/^(((?=.*(::))(?!.*\\3.+\\3))\\3?|([\\dA-F]{1,4}(\\3|:\\b|$)|\\2))(?4){5}((?4){2}|(((2[0-4]|1\\d|[1-9])?\\d|25[0-5])\\.?\\b){4})$/i", php_trim(maybe_ip, " []")):
            return 6
        # end if
        return False
    # end def is_ip_address
# end class WP_Http
