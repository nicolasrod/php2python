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
#// fsockopen HTTP transport
#// 
#// @package Requests
#// @subpackage Transport
#// 
#// 
#// fsockopen HTTP transport
#// 
#// @package Requests
#// @subpackage Transport
#//
class Requests_Transport_fsockopen(Requests_Transport):
    SECOND_IN_MICROSECONDS = 1000000
    headers = ""
    info = Array()
    max_bytes = False
    connect_error = ""
    #// 
    #// Perform a request
    #// 
    #// @throws Requests_Exception On failure to connect to socket (`fsockopenerror`)
    #// @throws Requests_Exception On socket timeout (`timeout`)
    #// 
    #// @param string $url URL to request
    #// @param array $headers Associative array of request headers
    #// @param string|array $data Data to send either as the POST body, or as parameters in the URL for a GET/HEAD
    #// @param array $options Request options, see {@see Requests::response()} for documentation
    #// @return string Raw HTTP result
    #//
    def request(self, url=None, headers=Array(), data=Array(), options=Array()):
        
        options["hooks"].dispatch("fsockopen.before_request")
        url_parts = php_parse_url(url)
        if php_empty(lambda : url_parts):
            raise php_new_class("Requests_Exception", lambda : Requests_Exception("Invalid URL.", "invalidurl", url))
        # end if
        host = url_parts["host"]
        context = stream_context_create()
        verifyname = False
        case_insensitive_headers = php_new_class("Requests_Utility_CaseInsensitiveDictionary", lambda : Requests_Utility_CaseInsensitiveDictionary(headers))
        #// HTTPS support
        if (php_isset(lambda : url_parts["scheme"])) and php_strtolower(url_parts["scheme"]) == "https":
            remote_socket = "ssl://" + host
            if (not (php_isset(lambda : url_parts["port"]))):
                url_parts["port"] = 443
            # end if
            context_options = Array({"verify_peer": True, "capture_peer_cert": True})
            verifyname = True
            #// SNI, if enabled (OpenSSL >=0.9.8j)
            if php_defined("OPENSSL_TLSEXT_SERVER_NAME") and OPENSSL_TLSEXT_SERVER_NAME:
                context_options["SNI_enabled"] = True
                if (php_isset(lambda : options["verifyname"])) and options["verifyname"] == False:
                    context_options["SNI_enabled"] = False
                # end if
            # end if
            if (php_isset(lambda : options["verify"])):
                if options["verify"] == False:
                    context_options["verify_peer"] = False
                elif php_is_string(options["verify"]):
                    context_options["cafile"] = options["verify"]
                # end if
            # end if
            if (php_isset(lambda : options["verifyname"])) and options["verifyname"] == False:
                context_options["verify_peer_name"] = False
                verifyname = False
            # end if
            stream_context_set_option(context, Array({"ssl": context_options}))
        else:
            remote_socket = "tcp://" + host
        # end if
        self.max_bytes = options["max_bytes"]
        if (not (php_isset(lambda : url_parts["port"]))):
            url_parts["port"] = 80
        # end if
        remote_socket += ":" + url_parts["port"]
        set_error_handler(Array(self, "connect_error_handler"), E_WARNING | E_NOTICE)
        options["hooks"].dispatch("fsockopen.remote_socket", Array(remote_socket))
        socket = stream_socket_client(remote_socket, errno, errstr, ceil(options["connect_timeout"]), STREAM_CLIENT_CONNECT, context)
        restore_error_handler()
        if verifyname and (not self.verify_certificate_from_context(host, context)):
            raise php_new_class("Requests_Exception", lambda : Requests_Exception("SSL certificate did not match the requested domain name", "ssl.no_match"))
        # end if
        if (not socket):
            if errno == 0:
                raise php_new_class("Requests_Exception", lambda : Requests_Exception(php_rtrim(self.connect_error), "fsockopen.connect_error"))
            # end if
            raise php_new_class("Requests_Exception", lambda : Requests_Exception(errstr, "fsockopenerror", None, errno))
        # end if
        data_format = options["data_format"]
        if data_format == "query":
            path = self.format_get(url_parts, data)
            data = ""
        else:
            path = self.format_get(url_parts, Array())
        # end if
        options["hooks"].dispatch("fsockopen.remote_host_path", Array(path, url))
        request_body = ""
        out = php_sprintf("%s %s HTTP/%.1F\r\n", options["type"], path, options["protocol_version"])
        if options["type"] != Requests.TRACE:
            if php_is_array(data):
                request_body = http_build_query(data, None, "&")
            else:
                request_body = data
            # end if
            if (not php_empty(lambda : data)):
                if (not (php_isset(lambda : case_insensitive_headers["Content-Length"]))):
                    headers["Content-Length"] = php_strlen(request_body)
                # end if
                if (not (php_isset(lambda : case_insensitive_headers["Content-Type"]))):
                    headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
                # end if
            # end if
        # end if
        if (not (php_isset(lambda : case_insensitive_headers["Host"]))):
            out += php_sprintf("Host: %s", url_parts["host"])
            if "http" == php_strtolower(url_parts["scheme"]) and url_parts["port"] != 80 or "https" == php_strtolower(url_parts["scheme"]) and url_parts["port"] != 443:
                out += ":" + url_parts["port"]
            # end if
            out += "\r\n"
        # end if
        if (not (php_isset(lambda : case_insensitive_headers["User-Agent"]))):
            out += php_sprintf("User-Agent: %s\r\n", options["useragent"])
        # end if
        accept_encoding = self.accept_encoding()
        if (not (php_isset(lambda : case_insensitive_headers["Accept-Encoding"]))) and (not php_empty(lambda : accept_encoding)):
            out += php_sprintf("Accept-Encoding: %s\r\n", accept_encoding)
        # end if
        headers = Requests.flatten(headers)
        if (not php_empty(lambda : headers)):
            out += php_implode("\r\n", headers) + "\r\n"
        # end if
        options["hooks"].dispatch("fsockopen.after_headers", Array(out))
        if php_substr(out, -2) != "\r\n":
            out += "\r\n"
        # end if
        if (not (php_isset(lambda : case_insensitive_headers["Connection"]))):
            out += "Connection: Close\r\n"
        # end if
        out += "\r\n" + request_body
        options["hooks"].dispatch("fsockopen.before_send", Array(out))
        fwrite(socket, out)
        options["hooks"].dispatch("fsockopen.after_send", Array(out))
        if (not options["blocking"]):
            php_fclose(socket)
            fake_headers = ""
            options["hooks"].dispatch("fsockopen.after_request", Array(fake_headers))
            return ""
        # end if
        timeout_sec = php_int(floor(options["timeout"]))
        if timeout_sec == options["timeout"]:
            timeout_msec = 0
        else:
            timeout_msec = self.SECOND_IN_MICROSECONDS * options["timeout"] % self.SECOND_IN_MICROSECONDS
        # end if
        stream_set_timeout(socket, timeout_sec, timeout_msec)
        response = body = headers = ""
        self.info = stream_get_meta_data(socket)
        size = 0
        doingbody = False
        download = False
        if options["filename"]:
            download = fopen(options["filename"], "wb")
        # end if
        while True:
            
            if not ((not php_feof(socket))):
                break
            # end if
            self.info = stream_get_meta_data(socket)
            if self.info["timed_out"]:
                raise php_new_class("Requests_Exception", lambda : Requests_Exception("fsocket timed out", "timeout"))
            # end if
            block = fread(socket, Requests.BUFFER_SIZE)
            if (not doingbody):
                response += block
                if php_strpos(response, "\r\n\r\n"):
                    headers, block = php_explode("\r\n\r\n", response, 2)
                    doingbody = True
                # end if
            # end if
            #// Are we in body mode now?
            if doingbody:
                options["hooks"].dispatch("request.progress", Array(block, size, self.max_bytes))
                data_length = php_strlen(block)
                if self.max_bytes:
                    #// Have we already hit a limit?
                    if size == self.max_bytes:
                        continue
                    # end if
                    if size + data_length > self.max_bytes:
                        #// Limit the length
                        limited_length = self.max_bytes - size
                        block = php_substr(block, 0, limited_length)
                    # end if
                # end if
                size += php_strlen(block)
                if download:
                    fwrite(download, block)
                else:
                    body += block
                # end if
            # end if
        # end while
        self.headers = headers
        if download:
            php_fclose(download)
        else:
            self.headers += "\r\n\r\n" + body
        # end if
        php_fclose(socket)
        options["hooks"].dispatch("fsockopen.after_request", Array(self.headers, self.info))
        return self.headers
    # end def request
    #// 
    #// Send multiple requests simultaneously
    #// 
    #// @param array $requests Request data (array of 'url', 'headers', 'data', 'options') as per {@see Requests_Transport::request}
    #// @param array $options Global options, see {@see Requests::response()} for documentation
    #// @return array Array of Requests_Response objects (may contain Requests_Exception or string responses as well)
    #//
    def request_multiple(self, requests=None, options=None):
        
        responses = Array()
        class_ = get_class(self)
        for id,request in requests:
            try: 
                handler = php_new_class(class_, lambda : {**locals(), **globals()}[class_]())
                responses[id] = handler.request(request["url"], request["headers"], request["data"], request["options"])
                request["options"]["hooks"].dispatch("transport.internal.parse_response", Array(responses[id], request))
            except Requests_Exception as e:
                responses[id] = e
            # end try
            if (not php_is_string(responses[id])):
                request["options"]["hooks"].dispatch("multiple.request.complete", Array(responses[id], id))
            # end if
        # end for
        return responses
    # end def request_multiple
    #// 
    #// Retrieve the encodings we can accept
    #// 
    #// @return string Accept-Encoding header value
    #//
    def accept_encoding(self):
        
        type = Array()
        if php_function_exists("gzinflate"):
            type[-1] = "deflate;q=1.0"
        # end if
        if php_function_exists("gzuncompress"):
            type[-1] = "compress;q=0.5"
        # end if
        type[-1] = "gzip;q=0.5"
        return php_implode(", ", type)
    # end def accept_encoding
    #// 
    #// Format a URL given GET data
    #// 
    #// @param array $url_parts
    #// @param array|object $data Data to build query using, see {@see https://secure.php.net/http_build_query}
    #// @return string URL with data
    #//
    def format_get(self, url_parts=None, data=None):
        
        if (not php_empty(lambda : data)):
            if php_empty(lambda : url_parts["query"]):
                url_parts["query"] = ""
            # end if
            url_parts["query"] += "&" + http_build_query(data, None, "&")
            url_parts["query"] = php_trim(url_parts["query"], "&")
        # end if
        if (php_isset(lambda : url_parts["path"])):
            if (php_isset(lambda : url_parts["query"])):
                get = url_parts["path"] + "?" + url_parts["query"]
            else:
                get = url_parts["path"]
            # end if
        else:
            get = "/"
        # end if
        return get
    # end def format_get
    #// 
    #// Error handler for stream_socket_client()
    #// 
    #// @param int $errno Error number (e.g. E_WARNING)
    #// @param string $errstr Error message
    #//
    def connect_error_handler(self, errno=None, errstr=None):
        
        #// Double-check we can handle it
        if errno & E_WARNING == 0 and errno & E_NOTICE == 0:
            #// Return false to indicate the default error handler should engage
            return False
        # end if
        self.connect_error += errstr + "\n"
        return True
    # end def connect_error_handler
    #// 
    #// Verify the certificate against common name and subject alternative names
    #// 
    #// Unfortunately, PHP doesn't check the certificate against the alternative
    #// names, leading things like 'https://www.github.com/' to be invalid.
    #// Instead
    #// 
    #// @see https://tools.ietf.org/html/rfc2818#section-3.1 RFC2818, Section 3.1
    #// 
    #// @throws Requests_Exception On failure to connect via TLS (`fsockopen.ssl.connect_error`)
    #// @throws Requests_Exception On not obtaining a match for the host (`fsockopen.ssl.no_match`)
    #// @param string $host Host name to verify against
    #// @param resource $context Stream context
    #// @return bool
    #//
    def verify_certificate_from_context(self, host=None, context=None):
        
        meta = stream_context_get_options(context)
        #// If we don't have SSL options, then we couldn't make the connection at
        #// all
        if php_empty(lambda : meta) or php_empty(lambda : meta["ssl"]) or php_empty(lambda : meta["ssl"]["peer_certificate"]):
            raise php_new_class("Requests_Exception", lambda : Requests_Exception(php_rtrim(self.connect_error), "ssl.connect_error"))
        # end if
        cert = openssl_x509_parse(meta["ssl"]["peer_certificate"])
        return Requests_SSL.verify_certificate(host, cert)
    # end def verify_certificate_from_context
    #// 
    #// Whether this transport is valid
    #// 
    #// @codeCoverageIgnore
    #// @return boolean True if the transport is valid, false otherwise.
    #//
    @classmethod
    def test(self, capabilities=Array()):
        
        if (not php_function_exists("fsockopen")):
            return False
        # end if
        #// If needed, check that streams support SSL
        if (php_isset(lambda : capabilities["ssl"])) and capabilities["ssl"]:
            if (not php_extension_loaded("openssl")) or (not php_function_exists("openssl_x509_parse")):
                return False
            # end if
            #// Currently broken, thanks to https://github.com/facebook/hhvm/issues/2156
            if php_defined("HHVM_VERSION"):
                return False
            # end if
        # end if
        return True
    # end def test
# end class Requests_Transport_fsockopen
