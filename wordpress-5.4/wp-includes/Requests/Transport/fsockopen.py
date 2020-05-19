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
    #// 
    #// Raw HTTP data
    #// 
    #// @var string
    #//
    headers = ""
    #// 
    #// Stream metadata
    #// 
    #// @var array Associative array of properties, see {@see https://secure.php.net/stream_get_meta_data}
    #//
    info = Array()
    #// 
    #// What's the maximum number of bytes we should keep?
    #// 
    #// @var int|bool Byte count, or false if no limit.
    #//
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
    def request(self, url_=None, headers_=None, data_=None, options_=None):
        if headers_ is None:
            headers_ = Array()
        # end if
        if data_ is None:
            data_ = Array()
        # end if
        if options_ is None:
            options_ = Array()
        # end if
        
        options_["hooks"].dispatch("fsockopen.before_request")
        url_parts_ = php_parse_url(url_)
        if php_empty(lambda : url_parts_):
            raise php_new_class("Requests_Exception", lambda : Requests_Exception("Invalid URL.", "invalidurl", url_))
        # end if
        host_ = url_parts_["host"]
        context_ = stream_context_create()
        verifyname_ = False
        case_insensitive_headers_ = php_new_class("Requests_Utility_CaseInsensitiveDictionary", lambda : Requests_Utility_CaseInsensitiveDictionary(headers_))
        #// HTTPS support
        if (php_isset(lambda : url_parts_["scheme"])) and php_strtolower(url_parts_["scheme"]) == "https":
            remote_socket_ = "ssl://" + host_
            if (not (php_isset(lambda : url_parts_["port"]))):
                url_parts_["port"] = 443
            # end if
            context_options_ = Array({"verify_peer": True, "capture_peer_cert": True})
            verifyname_ = True
            #// SNI, if enabled (OpenSSL >=0.9.8j)
            if php_defined("OPENSSL_TLSEXT_SERVER_NAME") and OPENSSL_TLSEXT_SERVER_NAME:
                context_options_["SNI_enabled"] = True
                if (php_isset(lambda : options_["verifyname"])) and options_["verifyname"] == False:
                    context_options_["SNI_enabled"] = False
                # end if
            # end if
            if (php_isset(lambda : options_["verify"])):
                if options_["verify"] == False:
                    context_options_["verify_peer"] = False
                elif php_is_string(options_["verify"]):
                    context_options_["cafile"] = options_["verify"]
                # end if
            # end if
            if (php_isset(lambda : options_["verifyname"])) and options_["verifyname"] == False:
                context_options_["verify_peer_name"] = False
                verifyname_ = False
            # end if
            stream_context_set_option(context_, Array({"ssl": context_options_}))
        else:
            remote_socket_ = "tcp://" + host_
        # end if
        self.max_bytes = options_["max_bytes"]
        if (not (php_isset(lambda : url_parts_["port"]))):
            url_parts_["port"] = 80
        # end if
        remote_socket_ += ":" + url_parts_["port"]
        set_error_handler(Array(self, "connect_error_handler"), E_WARNING | E_NOTICE)
        options_["hooks"].dispatch("fsockopen.remote_socket", Array(remote_socket_))
        socket_ = stream_socket_client(remote_socket_, errno_, errstr_, ceil(options_["connect_timeout"]), STREAM_CLIENT_CONNECT, context_)
        restore_error_handler()
        if verifyname_ and (not self.verify_certificate_from_context(host_, context_)):
            raise php_new_class("Requests_Exception", lambda : Requests_Exception("SSL certificate did not match the requested domain name", "ssl.no_match"))
        # end if
        if (not socket_):
            if errno_ == 0:
                raise php_new_class("Requests_Exception", lambda : Requests_Exception(php_rtrim(self.connect_error), "fsockopen.connect_error"))
            # end if
            raise php_new_class("Requests_Exception", lambda : Requests_Exception(errstr_, "fsockopenerror", None, errno_))
        # end if
        data_format_ = options_["data_format"]
        if data_format_ == "query":
            path_ = self.format_get(url_parts_, data_)
            data_ = ""
        else:
            path_ = self.format_get(url_parts_, Array())
        # end if
        options_["hooks"].dispatch("fsockopen.remote_host_path", Array(path_, url_))
        request_body_ = ""
        out_ = php_sprintf("%s %s HTTP/%.1F\r\n", options_["type"], path_, options_["protocol_version"])
        if options_["type"] != Requests.TRACE:
            if php_is_array(data_):
                request_body_ = http_build_query(data_, None, "&")
            else:
                request_body_ = data_
            # end if
            if (not php_empty(lambda : data_)):
                if (not (php_isset(lambda : case_insensitive_headers_["Content-Length"]))):
                    headers_["Content-Length"] = php_strlen(request_body_)
                # end if
                if (not (php_isset(lambda : case_insensitive_headers_["Content-Type"]))):
                    headers_["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
                # end if
            # end if
        # end if
        if (not (php_isset(lambda : case_insensitive_headers_["Host"]))):
            out_ += php_sprintf("Host: %s", url_parts_["host"])
            if "http" == php_strtolower(url_parts_["scheme"]) and url_parts_["port"] != 80 or "https" == php_strtolower(url_parts_["scheme"]) and url_parts_["port"] != 443:
                out_ += ":" + url_parts_["port"]
            # end if
            out_ += "\r\n"
        # end if
        if (not (php_isset(lambda : case_insensitive_headers_["User-Agent"]))):
            out_ += php_sprintf("User-Agent: %s\r\n", options_["useragent"])
        # end if
        accept_encoding_ = self.accept_encoding()
        if (not (php_isset(lambda : case_insensitive_headers_["Accept-Encoding"]))) and (not php_empty(lambda : accept_encoding_)):
            out_ += php_sprintf("Accept-Encoding: %s\r\n", accept_encoding_)
        # end if
        headers_ = Requests.flatten(headers_)
        if (not php_empty(lambda : headers_)):
            out_ += php_implode("\r\n", headers_) + "\r\n"
        # end if
        options_["hooks"].dispatch("fsockopen.after_headers", Array(out_))
        if php_substr(out_, -2) != "\r\n":
            out_ += "\r\n"
        # end if
        if (not (php_isset(lambda : case_insensitive_headers_["Connection"]))):
            out_ += "Connection: Close\r\n"
        # end if
        out_ += "\r\n" + request_body_
        options_["hooks"].dispatch("fsockopen.before_send", Array(out_))
        fwrite(socket_, out_)
        options_["hooks"].dispatch("fsockopen.after_send", Array(out_))
        if (not options_["blocking"]):
            php_fclose(socket_)
            fake_headers_ = ""
            options_["hooks"].dispatch("fsockopen.after_request", Array(fake_headers_))
            return ""
        # end if
        timeout_sec_ = php_int(floor(options_["timeout"]))
        if timeout_sec_ == options_["timeout"]:
            timeout_msec_ = 0
        else:
            timeout_msec_ = self.SECOND_IN_MICROSECONDS * options_["timeout"] % self.SECOND_IN_MICROSECONDS
        # end if
        stream_set_timeout(socket_, timeout_sec_, timeout_msec_)
        response_ = body_ = headers_ = ""
        self.info = stream_get_meta_data(socket_)
        size_ = 0
        doingbody_ = False
        download_ = False
        if options_["filename"]:
            download_ = fopen(options_["filename"], "wb")
        # end if
        while True:
            
            if not ((not php_feof(socket_))):
                break
            # end if
            self.info = stream_get_meta_data(socket_)
            if self.info["timed_out"]:
                raise php_new_class("Requests_Exception", lambda : Requests_Exception("fsocket timed out", "timeout"))
            # end if
            block_ = fread(socket_, Requests.BUFFER_SIZE)
            if (not doingbody_):
                response_ += block_
                if php_strpos(response_, "\r\n\r\n"):
                    headers_, block_ = php_explode("\r\n\r\n", response_, 2)
                    doingbody_ = True
                # end if
            # end if
            #// Are we in body mode now?
            if doingbody_:
                options_["hooks"].dispatch("request.progress", Array(block_, size_, self.max_bytes))
                data_length_ = php_strlen(block_)
                if self.max_bytes:
                    #// Have we already hit a limit?
                    if size_ == self.max_bytes:
                        continue
                    # end if
                    if size_ + data_length_ > self.max_bytes:
                        #// Limit the length
                        limited_length_ = self.max_bytes - size_
                        block_ = php_substr(block_, 0, limited_length_)
                    # end if
                # end if
                size_ += php_strlen(block_)
                if download_:
                    fwrite(download_, block_)
                else:
                    body_ += block_
                # end if
            # end if
        # end while
        self.headers = headers_
        if download_:
            php_fclose(download_)
        else:
            self.headers += "\r\n\r\n" + body_
        # end if
        php_fclose(socket_)
        options_["hooks"].dispatch("fsockopen.after_request", Array(self.headers, self.info))
        return self.headers
    # end def request
    #// 
    #// Send multiple requests simultaneously
    #// 
    #// @param array $requests Request data (array of 'url', 'headers', 'data', 'options') as per {@see Requests_Transport::request}
    #// @param array $options Global options, see {@see Requests::response()} for documentation
    #// @return array Array of Requests_Response objects (may contain Requests_Exception or string responses as well)
    #//
    def request_multiple(self, requests_=None, options_=None):
        
        
        responses_ = Array()
        class_ = get_class(self)
        for id_,request_ in requests_.items():
            try: 
                handler_ = php_new_class(class_, lambda : {**locals(), **globals()}[class_]())
                responses_[id_] = handler_.request(request_["url"], request_["headers"], request_["data"], request_["options"])
                request_["options"]["hooks"].dispatch("transport.internal.parse_response", Array(responses_[id_], request_))
            except Requests_Exception as e_:
                responses_[id_] = e_
            # end try
            if (not php_is_string(responses_[id_])):
                request_["options"]["hooks"].dispatch("multiple.request.complete", Array(responses_[id_], id_))
            # end if
        # end for
        return responses_
    # end def request_multiple
    #// 
    #// Retrieve the encodings we can accept
    #// 
    #// @return string Accept-Encoding header value
    #//
    def accept_encoding(self):
        
        
        type_ = Array()
        if php_function_exists("gzinflate"):
            type_[-1] = "deflate;q=1.0"
        # end if
        if php_function_exists("gzuncompress"):
            type_[-1] = "compress;q=0.5"
        # end if
        type_[-1] = "gzip;q=0.5"
        return php_implode(", ", type_)
    # end def accept_encoding
    #// 
    #// Format a URL given GET data
    #// 
    #// @param array $url_parts
    #// @param array|object $data Data to build query using, see {@see https://secure.php.net/http_build_query}
    #// @return string URL with data
    #//
    def format_get(self, url_parts_=None, data_=None):
        
        
        if (not php_empty(lambda : data_)):
            if php_empty(lambda : url_parts_["query"]):
                url_parts_["query"] = ""
            # end if
            url_parts_["query"] += "&" + http_build_query(data_, None, "&")
            url_parts_["query"] = php_trim(url_parts_["query"], "&")
        # end if
        if (php_isset(lambda : url_parts_["path"])):
            if (php_isset(lambda : url_parts_["query"])):
                get_ = url_parts_["path"] + "?" + url_parts_["query"]
            else:
                get_ = url_parts_["path"]
            # end if
        else:
            get_ = "/"
        # end if
        return get_
    # end def format_get
    #// 
    #// Error handler for stream_socket_client()
    #// 
    #// @param int $errno Error number (e.g. E_WARNING)
    #// @param string $errstr Error message
    #//
    def connect_error_handler(self, errno_=None, errstr_=None):
        
        
        #// Double-check we can handle it
        if errno_ & E_WARNING == 0 and errno_ & E_NOTICE == 0:
            #// Return false to indicate the default error handler should engage
            return False
        # end if
        self.connect_error += errstr_ + "\n"
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
    def verify_certificate_from_context(self, host_=None, context_=None):
        
        
        meta_ = stream_context_get_options(context_)
        #// If we don't have SSL options, then we couldn't make the connection at
        #// all
        if php_empty(lambda : meta_) or php_empty(lambda : meta_["ssl"]) or php_empty(lambda : meta_["ssl"]["peer_certificate"]):
            raise php_new_class("Requests_Exception", lambda : Requests_Exception(php_rtrim(self.connect_error), "ssl.connect_error"))
        # end if
        cert_ = openssl_x509_parse(meta_["ssl"]["peer_certificate"])
        return Requests_SSL.verify_certificate(host_, cert_)
    # end def verify_certificate_from_context
    #// 
    #// Whether this transport is valid
    #// 
    #// @codeCoverageIgnore
    #// @return boolean True if the transport is valid, false otherwise.
    #//
    @classmethod
    def test(self, capabilities_=None):
        if capabilities_ is None:
            capabilities_ = Array()
        # end if
        
        if (not php_function_exists("fsockopen")):
            return False
        # end if
        #// If needed, check that streams support SSL
        if (php_isset(lambda : capabilities_["ssl"])) and capabilities_["ssl"]:
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
