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
    headers = ""
    body = ""
    max_body_length = False
    stream_handle = False
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
    def request(self, url=None, args=Array()):
        
        defaults = Array({"method": "GET", "timeout": 5, "redirection": 5, "httpversion": "1.0", "blocking": True, "headers": Array(), "body": None, "cookies": Array()})
        parsed_args = wp_parse_args(args, defaults)
        if (php_isset(lambda : parsed_args["headers"]["User-Agent"])):
            parsed_args["user-agent"] = parsed_args["headers"]["User-Agent"]
            parsed_args["headers"]["User-Agent"] = None
        elif (php_isset(lambda : parsed_args["headers"]["user-agent"])):
            parsed_args["user-agent"] = parsed_args["headers"]["user-agent"]
            parsed_args["headers"]["user-agent"] = None
        # end if
        #// Construct Cookie: header if any cookies are set.
        WP_Http.buildcookieheader(parsed_args)
        handle = curl_init()
        #// cURL offers really easy proxy support.
        proxy = php_new_class("WP_HTTP_Proxy", lambda : WP_HTTP_Proxy())
        if proxy.is_enabled() and proxy.send_through_proxy(url):
            curl_setopt(handle, CURLOPT_PROXYTYPE, CURLPROXY_HTTP)
            curl_setopt(handle, CURLOPT_PROXY, proxy.host())
            curl_setopt(handle, CURLOPT_PROXYPORT, proxy.port())
            if proxy.use_authentication():
                curl_setopt(handle, CURLOPT_PROXYAUTH, CURLAUTH_ANY)
                curl_setopt(handle, CURLOPT_PROXYUSERPWD, proxy.authentication())
            # end if
        # end if
        is_local = (php_isset(lambda : parsed_args["local"])) and parsed_args["local"]
        ssl_verify = (php_isset(lambda : parsed_args["sslverify"])) and parsed_args["sslverify"]
        if is_local:
            #// This filter is documented in wp-includes/class-wp-http-streams.php
            ssl_verify = apply_filters("https_local_ssl_verify", ssl_verify, url)
        elif (not is_local):
            #// This filter is documented in wp-includes/class-http.php
            ssl_verify = apply_filters("https_ssl_verify", ssl_verify, url)
        # end if
        #// 
        #// CURLOPT_TIMEOUT and CURLOPT_CONNECTTIMEOUT expect integers. Have to use ceil since.
        #// a value of 0 will allow an unlimited timeout.
        #//
        timeout = php_int(ceil(parsed_args["timeout"]))
        curl_setopt(handle, CURLOPT_CONNECTTIMEOUT, timeout)
        curl_setopt(handle, CURLOPT_TIMEOUT, timeout)
        curl_setopt(handle, CURLOPT_URL, url)
        curl_setopt(handle, CURLOPT_RETURNTRANSFER, True)
        curl_setopt(handle, CURLOPT_SSL_VERIFYHOST, 2 if True == ssl_verify else False)
        curl_setopt(handle, CURLOPT_SSL_VERIFYPEER, ssl_verify)
        if ssl_verify:
            curl_setopt(handle, CURLOPT_CAINFO, parsed_args["sslcertificates"])
        # end if
        curl_setopt(handle, CURLOPT_USERAGENT, parsed_args["user-agent"])
        #// 
        #// The option doesn't work with safe mode or when open_basedir is set, and there's
        #// a bug #17490 with redirected POST requests, so handle redirections outside Curl.
        #//
        curl_setopt(handle, CURLOPT_FOLLOWLOCATION, False)
        curl_setopt(handle, CURLOPT_PROTOCOLS, CURLPROTO_HTTP | CURLPROTO_HTTPS)
        for case in Switch(parsed_args["method"]):
            if case("HEAD"):
                curl_setopt(handle, CURLOPT_NOBODY, True)
                break
            # end if
            if case("POST"):
                curl_setopt(handle, CURLOPT_POST, True)
                curl_setopt(handle, CURLOPT_POSTFIELDS, parsed_args["body"])
                break
            # end if
            if case("PUT"):
                curl_setopt(handle, CURLOPT_CUSTOMREQUEST, "PUT")
                curl_setopt(handle, CURLOPT_POSTFIELDS, parsed_args["body"])
                break
            # end if
            if case():
                curl_setopt(handle, CURLOPT_CUSTOMREQUEST, parsed_args["method"])
                if (not is_null(parsed_args["body"])):
                    curl_setopt(handle, CURLOPT_POSTFIELDS, parsed_args["body"])
                # end if
                break
            # end if
        # end for
        if True == parsed_args["blocking"]:
            curl_setopt(handle, CURLOPT_HEADERFUNCTION, Array(self, "stream_headers"))
            curl_setopt(handle, CURLOPT_WRITEFUNCTION, Array(self, "stream_body"))
        # end if
        curl_setopt(handle, CURLOPT_HEADER, False)
        if (php_isset(lambda : parsed_args["limit_response_size"])):
            self.max_body_length = php_intval(parsed_args["limit_response_size"])
        else:
            self.max_body_length = False
        # end if
        #// If streaming to a file open a file handle, and setup our curl streaming handler.
        if parsed_args["stream"]:
            if (not WP_DEBUG):
                self.stream_handle = php_no_error(lambda: fopen(parsed_args["filename"], "w+"))
            else:
                self.stream_handle = fopen(parsed_args["filename"], "w+")
            # end if
            if (not self.stream_handle):
                return php_new_class("WP_Error", lambda : WP_Error("http_request_failed", php_sprintf(__("Could not open handle for %1$s to %2$s."), "fopen()", parsed_args["filename"])))
            # end if
        else:
            self.stream_handle = False
        # end if
        if (not php_empty(lambda : parsed_args["headers"])):
            #// cURL expects full header strings in each element.
            headers = Array()
            for name,value in parsed_args["headers"]:
                headers[-1] = str(name) + str(": ") + str(value)
            # end for
            curl_setopt(handle, CURLOPT_HTTPHEADER, headers)
        # end if
        if "1.0" == parsed_args["httpversion"]:
            curl_setopt(handle, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_1_0)
        else:
            curl_setopt(handle, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_1_1)
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
        do_action_ref_array("http_api_curl", Array(handle, parsed_args, url))
        #// We don't need to return the body, so don't. Just execute request and return.
        if (not parsed_args["blocking"]):
            curl_exec(handle)
            curl_error = curl_error(handle)
            if curl_error:
                curl_close(handle)
                return php_new_class("WP_Error", lambda : WP_Error("http_request_failed", curl_error))
            # end if
            if php_in_array(curl_getinfo(handle, CURLINFO_HTTP_CODE), Array(301, 302)):
                curl_close(handle)
                return php_new_class("WP_Error", lambda : WP_Error("http_request_failed", __("Too many redirects.")))
            # end if
            curl_close(handle)
            return Array({"headers": Array(), "body": "", "response": Array({"code": False, "message": False})}, {"cookies": Array()})
        # end if
        curl_exec(handle)
        theHeaders = WP_Http.processheaders(self.headers, url)
        theBody = self.body
        bytes_written_total = self.bytes_written_total
        self.headers = ""
        self.body = ""
        self.bytes_written_total = 0
        curl_error = curl_errno(handle)
        #// If an error occurred, or, no response.
        if curl_error or 0 == php_strlen(theBody) and php_empty(lambda : theHeaders["headers"]):
            if CURLE_WRITE_ERROR == curl_error:
                if (not self.max_body_length) or self.max_body_length != bytes_written_total:
                    if parsed_args["stream"]:
                        curl_close(handle)
                        php_fclose(self.stream_handle)
                        return php_new_class("WP_Error", lambda : WP_Error("http_request_failed", __("Failed to write request to temporary file.")))
                    else:
                        curl_close(handle)
                        return php_new_class("WP_Error", lambda : WP_Error("http_request_failed", curl_error(handle)))
                    # end if
                # end if
            else:
                curl_error = curl_error(handle)
                if curl_error:
                    curl_close(handle)
                    return php_new_class("WP_Error", lambda : WP_Error("http_request_failed", curl_error))
                # end if
            # end if
            if php_in_array(curl_getinfo(handle, CURLINFO_HTTP_CODE), Array(301, 302)):
                curl_close(handle)
                return php_new_class("WP_Error", lambda : WP_Error("http_request_failed", __("Too many redirects.")))
            # end if
        # end if
        curl_close(handle)
        if parsed_args["stream"]:
            php_fclose(self.stream_handle)
        # end if
        response = Array({"headers": theHeaders["headers"], "body": None, "response": theHeaders["response"], "cookies": theHeaders["cookies"], "filename": parsed_args["filename"]})
        #// Handle redirects.
        redirect_response = WP_HTTP.handle_redirects(url, parsed_args, response)
        if False != redirect_response:
            return redirect_response
        # end if
        if True == parsed_args["decompress"] and True == WP_Http_Encoding.should_decode(theHeaders["headers"]):
            theBody = WP_Http_Encoding.decompress(theBody)
        # end if
        response["body"] = theBody
        return response
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
    def stream_headers(self, handle=None, headers=None):
        
        self.headers += headers
        return php_strlen(headers)
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
    def stream_body(self, handle=None, data=None):
        
        data_length = php_strlen(data)
        if self.max_body_length and self.bytes_written_total + data_length > self.max_body_length:
            data_length = self.max_body_length - self.bytes_written_total
            data = php_substr(data, 0, data_length)
        # end if
        if self.stream_handle:
            bytes_written = fwrite(self.stream_handle, data)
        else:
            self.body += data
            bytes_written = data_length
        # end if
        self.bytes_written_total += bytes_written
        #// Upon event of this function returning less than strlen( $data ) curl will error with CURLE_WRITE_ERROR.
        return bytes_written
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
    def test(self, args=Array()):
        
        if (not php_function_exists("curl_init")) or (not php_function_exists("curl_exec")):
            return False
        # end if
        is_ssl = (php_isset(lambda : args["ssl"])) and args["ssl"]
        if is_ssl:
            curl_version = curl_version()
            #// Check whether this cURL version support SSL requests.
            if (not CURL_VERSION_SSL & curl_version["features"]):
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
        return apply_filters("use_curl_transport", True, args)
    # end def test
# end class WP_Http_Curl
