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
#// HTTP API: WP_Http_Streams class
#// 
#// @package WordPress
#// @subpackage HTTP
#// @since 4.4.0
#// 
#// 
#// Core class used to integrate PHP Streams as an HTTP transport.
#// 
#// @since 2.7.0
#// @since 3.7.0 Combined with the fsockopen transport and switched to `stream_socket_client()`.
#//
class WP_Http_Streams():
    #// 
    #// Send a HTTP request to a URI using PHP Streams.
    #// 
    #// @see WP_Http::request For default options descriptions.
    #// 
    #// @since 2.7.0
    #// @since 3.7.0 Combined with the fsockopen transport and switched to stream_socket_client().
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
        arrURL = php_parse_url(url)
        connect_host = arrURL["host"]
        secure_transport = "ssl" == arrURL["scheme"] or "https" == arrURL["scheme"]
        if (not (php_isset(lambda : arrURL["port"]))):
            if "ssl" == arrURL["scheme"] or "https" == arrURL["scheme"]:
                arrURL["port"] = 443
                secure_transport = True
            else:
                arrURL["port"] = 80
            # end if
        # end if
        #// Always pass a path, defaulting to the root in cases such as http://example.com.
        if (not (php_isset(lambda : arrURL["path"]))):
            arrURL["path"] = "/"
        # end if
        if (php_isset(lambda : parsed_args["headers"]["Host"])) or (php_isset(lambda : parsed_args["headers"]["host"])):
            if (php_isset(lambda : parsed_args["headers"]["Host"])):
                arrURL["host"] = parsed_args["headers"]["Host"]
            else:
                arrURL["host"] = parsed_args["headers"]["host"]
            # end if
            parsed_args["headers"]["Host"] = None
            parsed_args["headers"]["host"] = None
        # end if
        #// 
        #// Certain versions of PHP have issues with 'localhost' and IPv6, It attempts to connect
        #// to ::1, which fails when the server is not set up for it. For compatibility, always
        #// connect to the IPv4 address.
        #//
        if "localhost" == php_strtolower(connect_host):
            connect_host = "127.0.0.1"
        # end if
        connect_host = "ssl://" + connect_host if secure_transport else "tcp://" + connect_host
        is_local = (php_isset(lambda : parsed_args["local"])) and parsed_args["local"]
        ssl_verify = (php_isset(lambda : parsed_args["sslverify"])) and parsed_args["sslverify"]
        if is_local:
            #// 
            #// Filters whether SSL should be verified for local requests.
            #// 
            #// @since 2.8.0
            #// @since 5.1.0 The `$url` parameter was added.
            #// 
            #// @param bool   $ssl_verify Whether to verify the SSL connection. Default true.
            #// @param string $url        The request URL.
            #//
            ssl_verify = apply_filters("https_local_ssl_verify", ssl_verify, url)
        elif (not is_local):
            #// This filter is documented in wp-includes/class-http.php
            ssl_verify = apply_filters("https_ssl_verify", ssl_verify, url)
        # end if
        proxy = php_new_class("WP_HTTP_Proxy", lambda : WP_HTTP_Proxy())
        context = stream_context_create(Array({"ssl": Array({"verify_peer": ssl_verify, "capture_peer_cert": ssl_verify, "SNI_enabled": True, "cafile": parsed_args["sslcertificates"], "allow_self_signed": (not ssl_verify)})}))
        timeout = int(floor(parsed_args["timeout"]))
        utimeout = 0 if timeout == parsed_args["timeout"] else 1000000 * parsed_args["timeout"] % 1000000
        connect_timeout = php_max(timeout, 1)
        #// Store error number.
        connection_error = None
        #// Store error string.
        connection_error_str = None
        if (not WP_DEBUG):
            #// In the event that the SSL connection fails, silence the many PHP warnings.
            if secure_transport:
                error_reporting = php_error_reporting(0)
            # end if
            if proxy.is_enabled() and proxy.send_through_proxy(url):
                #// phpcs:ignore WordPress.PHP.NoSilencedErrors.Discouraged
                handle = php_no_error(lambda: stream_socket_client("tcp://" + proxy.host() + ":" + proxy.port(), connection_error, connection_error_str, connect_timeout, STREAM_CLIENT_CONNECT, context))
            else:
                #// phpcs:ignore WordPress.PHP.NoSilencedErrors.Discouraged
                handle = php_no_error(lambda: stream_socket_client(connect_host + ":" + arrURL["port"], connection_error, connection_error_str, connect_timeout, STREAM_CLIENT_CONNECT, context))
            # end if
            if secure_transport:
                php_error_reporting(error_reporting)
            # end if
        else:
            if proxy.is_enabled() and proxy.send_through_proxy(url):
                handle = stream_socket_client("tcp://" + proxy.host() + ":" + proxy.port(), connection_error, connection_error_str, connect_timeout, STREAM_CLIENT_CONNECT, context)
            else:
                handle = stream_socket_client(connect_host + ":" + arrURL["port"], connection_error, connection_error_str, connect_timeout, STREAM_CLIENT_CONNECT, context)
            # end if
        # end if
        if False == handle:
            #// SSL connection failed due to expired/invalid cert, or, OpenSSL configuration is broken.
            if secure_transport and 0 == connection_error and "" == connection_error_str:
                return php_new_class("WP_Error", lambda : WP_Error("http_request_failed", __("The SSL certificate for the host could not be verified.")))
            # end if
            return php_new_class("WP_Error", lambda : WP_Error("http_request_failed", connection_error + ": " + connection_error_str))
        # end if
        #// Verify that the SSL certificate is valid for this request.
        if secure_transport and ssl_verify and (not proxy.is_enabled()):
            if (not self.verify_ssl_certificate(handle, arrURL["host"])):
                return php_new_class("WP_Error", lambda : WP_Error("http_request_failed", __("The SSL certificate for the host could not be verified.")))
            # end if
        # end if
        stream_set_timeout(handle, timeout, utimeout)
        if proxy.is_enabled() and proxy.send_through_proxy(url):
            #// Some proxies require full URL in this field.
            requestPath = url
        else:
            requestPath = arrURL["path"] + "?" + arrURL["query"] if (php_isset(lambda : arrURL["query"])) else ""
        # end if
        strHeaders = php_strtoupper(parsed_args["method"]) + " " + requestPath + " HTTP/" + parsed_args["httpversion"] + "\r\n"
        include_port_in_host_header = proxy.is_enabled() and proxy.send_through_proxy(url) or "http" == arrURL["scheme"] and 80 != arrURL["port"] or "https" == arrURL["scheme"] and 443 != arrURL["port"]
        if include_port_in_host_header:
            strHeaders += "Host: " + arrURL["host"] + ":" + arrURL["port"] + "\r\n"
        else:
            strHeaders += "Host: " + arrURL["host"] + "\r\n"
        # end if
        if (php_isset(lambda : parsed_args["user-agent"])):
            strHeaders += "User-agent: " + parsed_args["user-agent"] + "\r\n"
        # end if
        if php_is_array(parsed_args["headers"]):
            for header,headerValue in parsed_args["headers"]:
                strHeaders += header + ": " + headerValue + "\r\n"
            # end for
        else:
            strHeaders += parsed_args["headers"]
        # end if
        if proxy.use_authentication():
            strHeaders += proxy.authentication_header() + "\r\n"
        # end if
        strHeaders += "\r\n"
        if (not php_is_null(parsed_args["body"])):
            strHeaders += parsed_args["body"]
        # end if
        fwrite(handle, strHeaders)
        if (not parsed_args["blocking"]):
            stream_set_blocking(handle, 0)
            php_fclose(handle)
            return Array({"headers": Array(), "body": "", "response": Array({"code": False, "message": False})}, {"cookies": Array()})
        # end if
        strResponse = ""
        bodyStarted = False
        keep_reading = True
        block_size = 4096
        if (php_isset(lambda : parsed_args["limit_response_size"])):
            block_size = php_min(block_size, parsed_args["limit_response_size"])
        # end if
        #// If streaming to a file setup the file handle.
        if parsed_args["stream"]:
            if (not WP_DEBUG):
                stream_handle = php_no_error(lambda: fopen(parsed_args["filename"], "w+"))
            else:
                stream_handle = fopen(parsed_args["filename"], "w+")
            # end if
            if (not stream_handle):
                return php_new_class("WP_Error", lambda : WP_Error("http_request_failed", php_sprintf(__("Could not open handle for %1$s to %2$s."), "fopen()", parsed_args["filename"])))
            # end if
            bytes_written = 0
            while True:
                
                if not ((not php_feof(handle)) and keep_reading):
                    break
                # end if
                block = fread(handle, block_size)
                if (not bodyStarted):
                    strResponse += block
                    if php_strpos(strResponse, "\r\n\r\n"):
                        process = WP_Http.processresponse(strResponse)
                        bodyStarted = True
                        block = process["body"]
                        strResponse = None
                        process["body"] = ""
                    # end if
                # end if
                this_block_size = php_strlen(block)
                if (php_isset(lambda : parsed_args["limit_response_size"])) and bytes_written + this_block_size > parsed_args["limit_response_size"]:
                    this_block_size = parsed_args["limit_response_size"] - bytes_written
                    block = php_substr(block, 0, this_block_size)
                # end if
                bytes_written_to_file = fwrite(stream_handle, block)
                if bytes_written_to_file != this_block_size:
                    php_fclose(handle)
                    php_fclose(stream_handle)
                    return php_new_class("WP_Error", lambda : WP_Error("http_request_failed", __("Failed to write request to temporary file.")))
                # end if
                bytes_written += bytes_written_to_file
                keep_reading = (not (php_isset(lambda : parsed_args["limit_response_size"]))) or bytes_written < parsed_args["limit_response_size"]
            # end while
            php_fclose(stream_handle)
        else:
            header_length = 0
            while True:
                
                if not ((not php_feof(handle)) and keep_reading):
                    break
                # end if
                block = fread(handle, block_size)
                strResponse += block
                if (not bodyStarted) and php_strpos(strResponse, "\r\n\r\n"):
                    header_length = php_strpos(strResponse, "\r\n\r\n") + 4
                    bodyStarted = True
                # end if
                keep_reading = (not bodyStarted) or (not (php_isset(lambda : parsed_args["limit_response_size"]))) or php_strlen(strResponse) < header_length + parsed_args["limit_response_size"]
            # end while
            process = WP_Http.processresponse(strResponse)
            strResponse = None
        # end if
        php_fclose(handle)
        arrHeaders = WP_Http.processheaders(process["headers"], url)
        response = Array({"headers": arrHeaders["headers"], "body": None, "response": arrHeaders["response"], "cookies": arrHeaders["cookies"], "filename": parsed_args["filename"]})
        #// Handle redirects.
        redirect_response = WP_Http.handle_redirects(url, parsed_args, response)
        if False != redirect_response:
            return redirect_response
        # end if
        #// If the body was chunk encoded, then decode it.
        if (not php_empty(lambda : process["body"])) and (php_isset(lambda : arrHeaders["headers"]["transfer-encoding"])) and "chunked" == arrHeaders["headers"]["transfer-encoding"]:
            process["body"] = WP_Http.chunktransferdecode(process["body"])
        # end if
        if True == parsed_args["decompress"] and True == WP_Http_Encoding.should_decode(arrHeaders["headers"]):
            process["body"] = WP_Http_Encoding.decompress(process["body"])
        # end if
        if (php_isset(lambda : parsed_args["limit_response_size"])) and php_strlen(process["body"]) > parsed_args["limit_response_size"]:
            process["body"] = php_substr(process["body"], 0, parsed_args["limit_response_size"])
        # end if
        response["body"] = process["body"]
        return response
    # end def request
    #// 
    #// Verifies the received SSL certificate against its Common Names and subjectAltName fields.
    #// 
    #// PHP's SSL verifications only verify that it's a valid Certificate, it doesn't verify if
    #// the certificate is valid for the hostname which was requested.
    #// This function verifies the requested hostname against certificate's subjectAltName field,
    #// if that is empty, or contains no DNS entries, a fallback to the Common Name field is used.
    #// 
    #// IP Address support is included if the request is being made to an IP address.
    #// 
    #// @since 3.7.0
    #// 
    #// @param stream $stream The PHP Stream which the SSL request is being made over
    #// @param string $host The hostname being requested
    #// @return bool If the cerficiate presented in $stream is valid for $host
    #//
    @classmethod
    def verify_ssl_certificate(self, stream=None, host=None):
        
        context_options = stream_context_get_options(stream)
        if php_empty(lambda : context_options["ssl"]["peer_certificate"]):
            return False
        # end if
        cert = openssl_x509_parse(context_options["ssl"]["peer_certificate"])
        if (not cert):
            return False
        # end if
        #// 
        #// If the request is being made to an IP address, we'll validate against IP fields
        #// in the cert (if they exist)
        #//
        host_type = "ip" if WP_Http.is_ip_address(host) else "dns"
        certificate_hostnames = Array()
        if (not php_empty(lambda : cert["extensions"]["subjectAltName"])):
            match_against = php_preg_split("/,\\s*/", cert["extensions"]["subjectAltName"])
            for match in match_against:
                match_type, match_host = php_explode(":", match)
                if php_strtolower(php_trim(match_type)) == host_type:
                    #// IP: or DNS:
                    certificate_hostnames[-1] = php_strtolower(php_trim(match_host))
                # end if
            # end for
        elif (not php_empty(lambda : cert["subject"]["CN"])):
            #// Only use the CN when the certificate includes no subjectAltName extension.
            certificate_hostnames[-1] = php_strtolower(cert["subject"]["CN"])
        # end if
        #// Exact hostname/IP matches.
        if php_in_array(php_strtolower(host), certificate_hostnames):
            return True
        # end if
        #// IP's can't be wildcards, Stop processing.
        if "ip" == host_type:
            return False
        # end if
        #// Test to see if the domain is at least 2 deep for wildcard support.
        if php_substr_count(host, ".") < 2:
            return False
        # end if
        #// Wildcard subdomains certs (*.example.com) are valid for a.example.com but not a.b.example.com.
        wildcard_host = php_preg_replace("/^[^.]+\\./", "*.", host)
        return php_in_array(php_strtolower(wildcard_host), certificate_hostnames)
    # end def verify_ssl_certificate
    #// 
    #// Determines whether this class can be used for retrieving a URL.
    #// 
    #// @since 2.7.0
    #// @since 3.7.0 Combined with the fsockopen transport and switched to stream_socket_client().
    #// 
    #// @param array $args Optional. Array of request arguments. Default empty array.
    #// @return bool False means this class can not be used, true means it can.
    #//
    @classmethod
    def test(self, args=Array()):
        
        if (not php_function_exists("stream_socket_client")):
            return False
        # end if
        is_ssl = (php_isset(lambda : args["ssl"])) and args["ssl"]
        if is_ssl:
            if (not php_extension_loaded("openssl")):
                return False
            # end if
            if (not php_function_exists("openssl_x509_parse")):
                return False
            # end if
        # end if
        #// 
        #// Filters whether streams can be used as a transport for retrieving a URL.
        #// 
        #// @since 2.7.0
        #// 
        #// @param bool  $use_class Whether the class can be used. Default true.
        #// @param array $args      Request arguments.
        #//
        return apply_filters("use_streams_transport", True, args)
    # end def test
# end class WP_Http_Streams
#// 
#// Deprecated HTTP Transport method which used fsockopen.
#// 
#// This class is not used, and is included for backward compatibility only.
#// All code should make use of WP_Http directly through its API.
#// 
#// @see WP_HTTP::request
#// 
#// @since 2.7.0
#// @deprecated 3.7.0 Please use WP_HTTP::request() directly
#//
class WP_HTTP_Fsockopen(WP_HTTP_Streams):
    pass
# end class WP_HTTP_Fsockopen
