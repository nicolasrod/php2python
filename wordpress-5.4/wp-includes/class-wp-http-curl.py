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
#// HTTP API: WP_Http_Curl class
#// 
#// @package WordPress
#// @subpackage HTTP
#// @since 4.4.0
#// 
#// 
#// Core class used to integrate Curl as an HTTP transport.
#// 
#// HTTP request method uses Curl extension to retrieve the url.
#// 
#// Requires the Curl extension to be installed.
#// 
#// @since 2.7.0
#//
class WP_Http_Curl():
    #// 
    #// Temporary header storage for during requests.
    #// 
    #// @since 3.2.0
    #// @var string
    #//
    headers = ""
    #// 
    #// Temporary body storage for during requests.
    #// 
    #// @since 3.6.0
    #// @var string
    #//
    body = ""
    #// 
    #// The maximum amount of data to receive from the remote server.
    #// 
    #// @since 3.6.0
    #// @var int|false
    #//
    max_body_length = False
    #// 
    #// The file resource used for streaming to file.
    #// 
    #// @since 3.6.0
    #// @var resource|false
    #//
    stream_handle = False
    #// 
    #// The total bytes written in the current request.
    #// 
    #// @since 4.1.0
    #// @var int
    #//
    bytes_written_total = 0
    #// 
    #// Send a HTTP request to a URI using cURL extension.
    #// 
    #// @since 2.7.0
    #// 
    #// @param string $url The request URL.
    #// @param string|array $args Optional. Override the defaults.
    #// @return array|WP_Error Array containing 'headers', 'body', 'response', 'cookies', 'filename'. A WP_Error instance upon error
    #//
    def request(self, url_=None, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        defaults_ = Array({"method": "GET", "timeout": 5, "redirection": 5, "httpversion": "1.0", "blocking": True, "headers": Array(), "body": None, "cookies": Array()})
        parsed_args_ = wp_parse_args(args_, defaults_)
        if (php_isset(lambda : parsed_args_["headers"]["User-Agent"])):
            parsed_args_["user-agent"] = parsed_args_["headers"]["User-Agent"]
            parsed_args_["headers"]["User-Agent"] = None
        elif (php_isset(lambda : parsed_args_["headers"]["user-agent"])):
            parsed_args_["user-agent"] = parsed_args_["headers"]["user-agent"]
            parsed_args_["headers"]["user-agent"] = None
        # end if
        #// Construct Cookie: header if any cookies are set.
        WP_Http.buildcookieheader(parsed_args_)
        handle_ = curl_init()
        #// cURL offers really easy proxy support.
        proxy_ = php_new_class("WP_HTTP_Proxy", lambda : WP_HTTP_Proxy())
        if proxy_.is_enabled() and proxy_.send_through_proxy(url_):
            curl_setopt(handle_, CURLOPT_PROXYTYPE, CURLPROXY_HTTP)
            curl_setopt(handle_, CURLOPT_PROXY, proxy_.host())
            curl_setopt(handle_, CURLOPT_PROXYPORT, proxy_.port())
            if proxy_.use_authentication():
                curl_setopt(handle_, CURLOPT_PROXYAUTH, CURLAUTH_ANY)
                curl_setopt(handle_, CURLOPT_PROXYUSERPWD, proxy_.authentication())
            # end if
        # end if
        is_local_ = (php_isset(lambda : parsed_args_["local"])) and parsed_args_["local"]
        ssl_verify_ = (php_isset(lambda : parsed_args_["sslverify"])) and parsed_args_["sslverify"]
        if is_local_:
            #// This filter is documented in wp-includes/class-wp-http-streams.php
            ssl_verify_ = apply_filters("https_local_ssl_verify", ssl_verify_, url_)
        elif (not is_local_):
            #// This filter is documented in wp-includes/class-http.php
            ssl_verify_ = apply_filters("https_ssl_verify", ssl_verify_, url_)
        # end if
        #// 
        #// CURLOPT_TIMEOUT and CURLOPT_CONNECTTIMEOUT expect integers. Have to use ceil since.
        #// a value of 0 will allow an unlimited timeout.
        #//
        timeout_ = php_int(ceil(parsed_args_["timeout"]))
        curl_setopt(handle_, CURLOPT_CONNECTTIMEOUT, timeout_)
        curl_setopt(handle_, CURLOPT_TIMEOUT, timeout_)
        curl_setopt(handle_, CURLOPT_URL, url_)
        curl_setopt(handle_, CURLOPT_RETURNTRANSFER, True)
        curl_setopt(handle_, CURLOPT_SSL_VERIFYHOST, 2 if True == ssl_verify_ else False)
        curl_setopt(handle_, CURLOPT_SSL_VERIFYPEER, ssl_verify_)
        if ssl_verify_:
            curl_setopt(handle_, CURLOPT_CAINFO, parsed_args_["sslcertificates"])
        # end if
        curl_setopt(handle_, CURLOPT_USERAGENT, parsed_args_["user-agent"])
        #// 
        #// The option doesn't work with safe mode or when open_basedir is set, and there's
        #// a bug #17490 with redirected POST requests, so handle redirections outside Curl.
        #//
        curl_setopt(handle_, CURLOPT_FOLLOWLOCATION, False)
        curl_setopt(handle_, CURLOPT_PROTOCOLS, CURLPROTO_HTTP | CURLPROTO_HTTPS)
        for case in Switch(parsed_args_["method"]):
            if case("HEAD"):
                curl_setopt(handle_, CURLOPT_NOBODY, True)
                break
            # end if
            if case("POST"):
                curl_setopt(handle_, CURLOPT_POST, True)
                curl_setopt(handle_, CURLOPT_POSTFIELDS, parsed_args_["body"])
                break
            # end if
            if case("PUT"):
                curl_setopt(handle_, CURLOPT_CUSTOMREQUEST, "PUT")
                curl_setopt(handle_, CURLOPT_POSTFIELDS, parsed_args_["body"])
                break
            # end if
            if case():
                curl_setopt(handle_, CURLOPT_CUSTOMREQUEST, parsed_args_["method"])
                if (not php_is_null(parsed_args_["body"])):
                    curl_setopt(handle_, CURLOPT_POSTFIELDS, parsed_args_["body"])
                # end if
                break
            # end if
        # end for
        if True == parsed_args_["blocking"]:
            curl_setopt(handle_, CURLOPT_HEADERFUNCTION, Array(self, "stream_headers"))
            curl_setopt(handle_, CURLOPT_WRITEFUNCTION, Array(self, "stream_body"))
        # end if
        curl_setopt(handle_, CURLOPT_HEADER, False)
        if (php_isset(lambda : parsed_args_["limit_response_size"])):
            self.max_body_length = php_intval(parsed_args_["limit_response_size"])
        else:
            self.max_body_length = False
        # end if
        #// If streaming to a file open a file handle, and setup our curl streaming handler.
        if parsed_args_["stream"]:
            if (not WP_DEBUG):
                self.stream_handle = php_no_error(lambda: fopen(parsed_args_["filename"], "w+"))
            else:
                self.stream_handle = fopen(parsed_args_["filename"], "w+")
            # end if
            if (not self.stream_handle):
                return php_new_class("WP_Error", lambda : WP_Error("http_request_failed", php_sprintf(__("Could not open handle for %1$s to %2$s."), "fopen()", parsed_args_["filename"])))
            # end if
        else:
            self.stream_handle = False
        # end if
        if (not php_empty(lambda : parsed_args_["headers"])):
            #// cURL expects full header strings in each element.
            headers_ = Array()
            for name_,value_ in parsed_args_["headers"].items():
                headers_[-1] = str(name_) + str(": ") + str(value_)
            # end for
            curl_setopt(handle_, CURLOPT_HTTPHEADER, headers_)
        # end if
        if "1.0" == parsed_args_["httpversion"]:
            curl_setopt(handle_, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_1_0)
        else:
            curl_setopt(handle_, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_1_1)
        # end if
        #// 
        #// Fires before the cURL request is executed.
        #// 
        #// Cookies are not currently handled by the HTTP API. This action allows
        #// plugins to handle cookies themselves.
        #// 
        #// @since 2.8.0
        #// 
        #// @param resource $handle      The cURL handle returned by curl_init() (passed by reference).
        #// @param array    $parsed_args The HTTP request arguments.
        #// @param string   $url         The request URL.
        #//
        do_action_ref_array("http_api_curl", Array(handle_, parsed_args_, url_))
        #// We don't need to return the body, so don't. Just execute request and return.
        if (not parsed_args_["blocking"]):
            curl_exec(handle_)
            curl_error_ = curl_error(handle_)
            if curl_error_:
                curl_close(handle_)
                return php_new_class("WP_Error", lambda : WP_Error("http_request_failed", curl_error_))
            # end if
            if php_in_array(curl_getinfo(handle_, CURLINFO_HTTP_CODE), Array(301, 302)):
                curl_close(handle_)
                return php_new_class("WP_Error", lambda : WP_Error("http_request_failed", __("Too many redirects.")))
            # end if
            curl_close(handle_)
            return Array({"headers": Array(), "body": "", "response": Array({"code": False, "message": False})}, {"cookies": Array()})
        # end if
        curl_exec(handle_)
        theHeaders_ = WP_Http.processheaders(self.headers, url_)
        theBody_ = self.body
        bytes_written_total_ = self.bytes_written_total
        self.headers = ""
        self.body = ""
        self.bytes_written_total = 0
        curl_error_ = curl_errno(handle_)
        #// If an error occurred, or, no response.
        if curl_error_ or 0 == php_strlen(theBody_) and php_empty(lambda : theHeaders_["headers"]):
            if CURLE_WRITE_ERROR == curl_error_:
                if (not self.max_body_length) or self.max_body_length != bytes_written_total_:
                    if parsed_args_["stream"]:
                        curl_close(handle_)
                        php_fclose(self.stream_handle)
                        return php_new_class("WP_Error", lambda : WP_Error("http_request_failed", __("Failed to write request to temporary file.")))
                    else:
                        curl_close(handle_)
                        return php_new_class("WP_Error", lambda : WP_Error("http_request_failed", curl_error(handle_)))
                    # end if
                # end if
            else:
                curl_error_ = curl_error(handle_)
                if curl_error_:
                    curl_close(handle_)
                    return php_new_class("WP_Error", lambda : WP_Error("http_request_failed", curl_error_))
                # end if
            # end if
            if php_in_array(curl_getinfo(handle_, CURLINFO_HTTP_CODE), Array(301, 302)):
                curl_close(handle_)
                return php_new_class("WP_Error", lambda : WP_Error("http_request_failed", __("Too many redirects.")))
            # end if
        # end if
        curl_close(handle_)
        if parsed_args_["stream"]:
            php_fclose(self.stream_handle)
        # end if
        response_ = Array({"headers": theHeaders_["headers"], "body": None, "response": theHeaders_["response"], "cookies": theHeaders_["cookies"], "filename": parsed_args_["filename"]})
        #// Handle redirects.
        redirect_response_ = WP_HTTP.handle_redirects(url_, parsed_args_, response_)
        if False != redirect_response_:
            return redirect_response_
        # end if
        if True == parsed_args_["decompress"] and True == WP_Http_Encoding.should_decode(theHeaders_["headers"]):
            theBody_ = WP_Http_Encoding.decompress(theBody_)
        # end if
        response_["body"] = theBody_
        return response_
    # end def request
    #// 
    #// Grabs the headers of the cURL request.
    #// 
    #// Each header is sent individually to this callback, so we append to the `$header` property
    #// for temporary storage
    #// 
    #// @since 3.2.0
    #// 
    #// @param resource $handle  cURL handle.
    #// @param string   $headers cURL request headers.
    #// @return int Length of the request headers.
    #//
    def stream_headers(self, handle_=None, headers_=None):
        
        
        self.headers += headers_
        return php_strlen(headers_)
    # end def stream_headers
    #// 
    #// Grabs the body of the cURL request.
    #// 
    #// The contents of the document are passed in chunks, so we append to the `$body`
    #// property for temporary storage. Returning a length shorter than the length of
    #// `$data` passed in will cause cURL to abort the request with `CURLE_WRITE_ERROR`.
    #// 
    #// @since 3.6.0
    #// 
    #// @param resource $handle  cURL handle.
    #// @param string   $data    cURL request body.
    #// @return int Total bytes of data written.
    #//
    def stream_body(self, handle_=None, data_=None):
        
        
        data_length_ = php_strlen(data_)
        if self.max_body_length and self.bytes_written_total + data_length_ > self.max_body_length:
            data_length_ = self.max_body_length - self.bytes_written_total
            data_ = php_substr(data_, 0, data_length_)
        # end if
        if self.stream_handle:
            bytes_written_ = fwrite(self.stream_handle, data_)
        else:
            self.body += data_
            bytes_written_ = data_length_
        # end if
        self.bytes_written_total += bytes_written_
        #// Upon event of this function returning less than strlen( $data ) curl will error with CURLE_WRITE_ERROR.
        return bytes_written_
    # end def stream_body
    #// 
    #// Determines whether this class can be used for retrieving a URL.
    #// 
    #// @since 2.7.0
    #// 
    #// @param array $args Optional. Array of request arguments. Default empty array.
    #// @return bool False means this class can not be used, true means it can.
    #//
    @classmethod
    def test(self, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        if (not php_function_exists("curl_init")) or (not php_function_exists("curl_exec")):
            return False
        # end if
        is_ssl_ = (php_isset(lambda : args_["ssl"])) and args_["ssl"]
        if is_ssl_:
            curl_version_ = curl_version()
            #// Check whether this cURL version support SSL requests.
            if (not CURL_VERSION_SSL & curl_version_["features"]):
                return False
            # end if
        # end if
        #// 
        #// Filters whether cURL can be used as a transport for retrieving a URL.
        #// 
        #// @since 2.7.0
        #// 
        #// @param bool  $use_class Whether the class can be used. Default true.
        #// @param array $args      An array of request arguments.
        #//
        return apply_filters("use_curl_transport", True, args_)
    # end def test
# end class WP_Http_Curl
