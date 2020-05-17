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
        arrURL_ = php_parse_url(url_)
        connect_host_ = arrURL_["host"]
        secure_transport_ = "ssl" == arrURL_["scheme"] or "https" == arrURL_["scheme"]
        if (not (php_isset(lambda : arrURL_["port"]))):
            if "ssl" == arrURL_["scheme"] or "https" == arrURL_["scheme"]:
                arrURL_["port"] = 443
                secure_transport_ = True
            else:
                arrURL_["port"] = 80
            # end if
        # end if
        #// Always pass a path, defaulting to the root in cases such as http://example.com.
        if (not (php_isset(lambda : arrURL_["path"]))):
            arrURL_["path"] = "/"
        # end if
        if (php_isset(lambda : parsed_args_["headers"]["Host"])) or (php_isset(lambda : parsed_args_["headers"]["host"])):
            if (php_isset(lambda : parsed_args_["headers"]["Host"])):
                arrURL_["host"] = parsed_args_["headers"]["Host"]
            else:
                arrURL_["host"] = parsed_args_["headers"]["host"]
            # end if
            parsed_args_["headers"]["Host"] = None
            parsed_args_["headers"]["host"] = None
        # end if
        #// 
        #// Certain versions of PHP have issues with 'localhost' and IPv6, It attempts to connect
        #// to ::1, which fails when the server is not set up for it. For compatibility, always
        #// connect to the IPv4 address.
        #//
        if "localhost" == php_strtolower(connect_host_):
            connect_host_ = "127.0.0.1"
        # end if
        connect_host_ = "ssl://" + connect_host_ if secure_transport_ else "tcp://" + connect_host_
        is_local_ = (php_isset(lambda : parsed_args_["local"])) and parsed_args_["local"]
        ssl_verify_ = (php_isset(lambda : parsed_args_["sslverify"])) and parsed_args_["sslverify"]
        if is_local_:
            #// 
            #// Filters whether SSL should be verified for local requests.
            #// 
            #// @since 2.8.0
            #// @since 5.1.0 The `$url` parameter was added.
            #// 
            #// @param bool   $ssl_verify Whether to verify the SSL connection. Default true.
            #// @param string $url        The request URL.
            #//
            ssl_verify_ = apply_filters("https_local_ssl_verify", ssl_verify_, url_)
        elif (not is_local_):
            #// This filter is documented in wp-includes/class-http.php
            ssl_verify_ = apply_filters("https_ssl_verify", ssl_verify_, url_)
        # end if
        proxy_ = php_new_class("WP_HTTP_Proxy", lambda : WP_HTTP_Proxy())
        context_ = stream_context_create(Array({"ssl": Array({"verify_peer": ssl_verify_, "capture_peer_cert": ssl_verify_, "SNI_enabled": True, "cafile": parsed_args_["sslcertificates"], "allow_self_signed": (not ssl_verify_)})}))
        timeout_ = php_int(floor(parsed_args_["timeout"]))
        utimeout_ = 0 if timeout_ == parsed_args_["timeout"] else 1000000 * parsed_args_["timeout"] % 1000000
        connect_timeout_ = php_max(timeout_, 1)
        #// Store error number.
        connection_error_ = None
        #// Store error string.
        connection_error_str_ = None
        if (not WP_DEBUG):
            #// In the event that the SSL connection fails, silence the many PHP warnings.
            if secure_transport_:
                error_reporting_ = php_error_reporting(0)
            # end if
            if proxy_.is_enabled() and proxy_.send_through_proxy(url_):
                #// phpcs:ignore WordPress.PHP.NoSilencedErrors.Discouraged
                handle_ = php_no_error(lambda: stream_socket_client("tcp://" + proxy_.host() + ":" + proxy_.port(), connection_error_, connection_error_str_, connect_timeout_, STREAM_CLIENT_CONNECT, context_))
            else:
                #// phpcs:ignore WordPress.PHP.NoSilencedErrors.Discouraged
                handle_ = php_no_error(lambda: stream_socket_client(connect_host_ + ":" + arrURL_["port"], connection_error_, connection_error_str_, connect_timeout_, STREAM_CLIENT_CONNECT, context_))
            # end if
            if secure_transport_:
                php_error_reporting(error_reporting_)
            # end if
        else:
            if proxy_.is_enabled() and proxy_.send_through_proxy(url_):
                handle_ = stream_socket_client("tcp://" + proxy_.host() + ":" + proxy_.port(), connection_error_, connection_error_str_, connect_timeout_, STREAM_CLIENT_CONNECT, context_)
            else:
                handle_ = stream_socket_client(connect_host_ + ":" + arrURL_["port"], connection_error_, connection_error_str_, connect_timeout_, STREAM_CLIENT_CONNECT, context_)
            # end if
        # end if
        if False == handle_:
            #// SSL connection failed due to expired/invalid cert, or, OpenSSL configuration is broken.
            if secure_transport_ and 0 == connection_error_ and "" == connection_error_str_:
                return php_new_class("WP_Error", lambda : WP_Error("http_request_failed", __("The SSL certificate for the host could not be verified.")))
            # end if
            return php_new_class("WP_Error", lambda : WP_Error("http_request_failed", connection_error_ + ": " + connection_error_str_))
        # end if
        #// Verify that the SSL certificate is valid for this request.
        if secure_transport_ and ssl_verify_ and (not proxy_.is_enabled()):
            if (not self.verify_ssl_certificate(handle_, arrURL_["host"])):
                return php_new_class("WP_Error", lambda : WP_Error("http_request_failed", __("The SSL certificate for the host could not be verified.")))
            # end if
        # end if
        stream_set_timeout(handle_, timeout_, utimeout_)
        if proxy_.is_enabled() and proxy_.send_through_proxy(url_):
            #// Some proxies require full URL in this field.
            requestPath_ = url_
        else:
            requestPath_ = arrURL_["path"] + "?" + arrURL_["query"] if (php_isset(lambda : arrURL_["query"])) else ""
        # end if
        strHeaders_ = php_strtoupper(parsed_args_["method"]) + " " + requestPath_ + " HTTP/" + parsed_args_["httpversion"] + "\r\n"
        include_port_in_host_header_ = proxy_.is_enabled() and proxy_.send_through_proxy(url_) or "http" == arrURL_["scheme"] and 80 != arrURL_["port"] or "https" == arrURL_["scheme"] and 443 != arrURL_["port"]
        if include_port_in_host_header_:
            strHeaders_ += "Host: " + arrURL_["host"] + ":" + arrURL_["port"] + "\r\n"
        else:
            strHeaders_ += "Host: " + arrURL_["host"] + "\r\n"
        # end if
        if (php_isset(lambda : parsed_args_["user-agent"])):
            strHeaders_ += "User-agent: " + parsed_args_["user-agent"] + "\r\n"
        # end if
        if php_is_array(parsed_args_["headers"]):
            for header_,headerValue_ in parsed_args_["headers"]:
                strHeaders_ += header_ + ": " + headerValue_ + "\r\n"
            # end for
        else:
            strHeaders_ += parsed_args_["headers"]
        # end if
        if proxy_.use_authentication():
            strHeaders_ += proxy_.authentication_header() + "\r\n"
        # end if
        strHeaders_ += "\r\n"
        if (not php_is_null(parsed_args_["body"])):
            strHeaders_ += parsed_args_["body"]
        # end if
        fwrite(handle_, strHeaders_)
        if (not parsed_args_["blocking"]):
            stream_set_blocking(handle_, 0)
            php_fclose(handle_)
            return Array({"headers": Array(), "body": "", "response": Array({"code": False, "message": False})}, {"cookies": Array()})
        # end if
        strResponse_ = ""
        bodyStarted_ = False
        keep_reading_ = True
        block_size_ = 4096
        if (php_isset(lambda : parsed_args_["limit_response_size"])):
            block_size_ = php_min(block_size_, parsed_args_["limit_response_size"])
        # end if
        #// If streaming to a file setup the file handle.
        if parsed_args_["stream"]:
            if (not WP_DEBUG):
                stream_handle_ = php_no_error(lambda: fopen(parsed_args_["filename"], "w+"))
            else:
                stream_handle_ = fopen(parsed_args_["filename"], "w+")
            # end if
            if (not stream_handle_):
                return php_new_class("WP_Error", lambda : WP_Error("http_request_failed", php_sprintf(__("Could not open handle for %1$s to %2$s."), "fopen()", parsed_args_["filename"])))
            # end if
            bytes_written_ = 0
            while True:
                
                if not ((not php_feof(handle_)) and keep_reading_):
                    break
                # end if
                block_ = fread(handle_, block_size_)
                if (not bodyStarted_):
                    strResponse_ += block_
                    if php_strpos(strResponse_, "\r\n\r\n"):
                        process_ = WP_Http.processresponse(strResponse_)
                        bodyStarted_ = True
                        block_ = process_["body"]
                        strResponse_ = None
                        process_["body"] = ""
                    # end if
                # end if
                this_block_size_ = php_strlen(block_)
                if (php_isset(lambda : parsed_args_["limit_response_size"])) and bytes_written_ + this_block_size_ > parsed_args_["limit_response_size"]:
                    this_block_size_ = parsed_args_["limit_response_size"] - bytes_written_
                    block_ = php_substr(block_, 0, this_block_size_)
                # end if
                bytes_written_to_file_ = fwrite(stream_handle_, block_)
                if bytes_written_to_file_ != this_block_size_:
                    php_fclose(handle_)
                    php_fclose(stream_handle_)
                    return php_new_class("WP_Error", lambda : WP_Error("http_request_failed", __("Failed to write request to temporary file.")))
                # end if
                bytes_written_ += bytes_written_to_file_
                keep_reading_ = (not (php_isset(lambda : parsed_args_["limit_response_size"]))) or bytes_written_ < parsed_args_["limit_response_size"]
            # end while
            php_fclose(stream_handle_)
        else:
            header_length_ = 0
            while True:
                
                if not ((not php_feof(handle_)) and keep_reading_):
                    break
                # end if
                block_ = fread(handle_, block_size_)
                strResponse_ += block_
                if (not bodyStarted_) and php_strpos(strResponse_, "\r\n\r\n"):
                    header_length_ = php_strpos(strResponse_, "\r\n\r\n") + 4
                    bodyStarted_ = True
                # end if
                keep_reading_ = (not bodyStarted_) or (not (php_isset(lambda : parsed_args_["limit_response_size"]))) or php_strlen(strResponse_) < header_length_ + parsed_args_["limit_response_size"]
            # end while
            process_ = WP_Http.processresponse(strResponse_)
            strResponse_ = None
        # end if
        php_fclose(handle_)
        arrHeaders_ = WP_Http.processheaders(process_["headers"], url_)
        response_ = Array({"headers": arrHeaders_["headers"], "body": None, "response": arrHeaders_["response"], "cookies": arrHeaders_["cookies"], "filename": parsed_args_["filename"]})
        #// Handle redirects.
        redirect_response_ = WP_Http.handle_redirects(url_, parsed_args_, response_)
        if False != redirect_response_:
            return redirect_response_
        # end if
        #// If the body was chunk encoded, then decode it.
        if (not php_empty(lambda : process_["body"])) and (php_isset(lambda : arrHeaders_["headers"]["transfer-encoding"])) and "chunked" == arrHeaders_["headers"]["transfer-encoding"]:
            process_["body"] = WP_Http.chunktransferdecode(process_["body"])
        # end if
        if True == parsed_args_["decompress"] and True == WP_Http_Encoding.should_decode(arrHeaders_["headers"]):
            process_["body"] = WP_Http_Encoding.decompress(process_["body"])
        # end if
        if (php_isset(lambda : parsed_args_["limit_response_size"])) and php_strlen(process_["body"]) > parsed_args_["limit_response_size"]:
            process_["body"] = php_substr(process_["body"], 0, parsed_args_["limit_response_size"])
        # end if
        response_["body"] = process_["body"]
        return response_
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
    def verify_ssl_certificate(self, stream_=None, host_=None):
        
        
        context_options_ = stream_context_get_options(stream_)
        if php_empty(lambda : context_options_["ssl"]["peer_certificate"]):
            return False
        # end if
        cert_ = openssl_x509_parse(context_options_["ssl"]["peer_certificate"])
        if (not cert_):
            return False
        # end if
        #// 
        #// If the request is being made to an IP address, we'll validate against IP fields
        #// in the cert (if they exist)
        #//
        host_type_ = "ip" if WP_Http.is_ip_address(host_) else "dns"
        certificate_hostnames_ = Array()
        if (not php_empty(lambda : cert_["extensions"]["subjectAltName"])):
            match_against_ = php_preg_split("/,\\s*/", cert_["extensions"]["subjectAltName"])
            for match_ in match_against_:
                match_type_, match_host_ = php_explode(":", match_)
                if php_strtolower(php_trim(match_type_)) == host_type_:
                    #// IP: or DNS:
                    certificate_hostnames_[-1] = php_strtolower(php_trim(match_host_))
                # end if
            # end for
        elif (not php_empty(lambda : cert_["subject"]["CN"])):
            #// Only use the CN when the certificate includes no subjectAltName extension.
            certificate_hostnames_[-1] = php_strtolower(cert_["subject"]["CN"])
        # end if
        #// Exact hostname/IP matches.
        if php_in_array(php_strtolower(host_), certificate_hostnames_):
            return True
        # end if
        #// IP's can't be wildcards, Stop processing.
        if "ip" == host_type_:
            return False
        # end if
        #// Test to see if the domain is at least 2 deep for wildcard support.
        if php_substr_count(host_, ".") < 2:
            return False
        # end if
        #// Wildcard subdomains certs (*.example.com) are valid for a.example.com but not a.b.example.com.
        wildcard_host_ = php_preg_replace("/^[^.]+\\./", "*.", host_)
        return php_in_array(php_strtolower(wildcard_host_), certificate_hostnames_)
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
    def test(self, args_=None):
        if args_ is None:
            args_ = Array()
        # end if
        
        if (not php_function_exists("stream_socket_client")):
            return False
        # end if
        is_ssl_ = (php_isset(lambda : args_["ssl"])) and args_["ssl"]
        if is_ssl_:
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
        return apply_filters("use_streams_transport", True, args_)
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
