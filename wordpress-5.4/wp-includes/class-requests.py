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
#// Requests for PHP
#// 
#// Inspired by Requests for Python.
#// 
#// Based on concepts from SimplePie_File, RequestCore and WP_Http.
#// 
#// @package Requests
#// 
#// 
#// Requests for PHP
#// 
#// Inspired by Requests for Python.
#// 
#// Based on concepts from SimplePie_File, RequestCore and WP_Http.
#// 
#// @package Requests
#//
class Requests():
    POST = "POST"
    PUT = "PUT"
    GET = "GET"
    HEAD = "HEAD"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"
    PATCH = "PATCH"
    BUFFER_SIZE = 1160
    VERSION = "1.7-3470169"
    transports = Array()
    transport = Array()
    certificate_path = Array()
    #// 
    #// This is a static class, do not instantiate it
    #// 
    #// @codeCoverageIgnore
    #//
    def __init__(self):
        
        pass
    # end def __init__
    #// 
    #// Autoloader for Requests
    #// 
    #// Register this with {@see register_autoloader()} if you'd like to avoid
    #// having to create your own.
    #// 
    #// (You can also use `spl_autoload_register` directly if you'd prefer.)
    #// 
    #// @codeCoverageIgnore
    #// 
    #// @param string $class Class name to load
    #//
    @classmethod
    def autoloader(self, class_=None):
        
        #// Check that the class starts with "Requests"
        if php_strpos(class_, "Requests") != 0:
            return
        # end if
        file = php_str_replace("_", "/", class_)
        if php_file_exists(php_dirname(__FILE__) + "/" + file + ".php"):
            php_include_file(php_dirname(__FILE__) + "/" + file + ".php", once=True)
        # end if
    # end def autoloader
    #// 
    #// Register the built-in autoloader
    #// 
    #// @codeCoverageIgnore
    #//
    @classmethod
    def register_autoloader(self):
        
        php_spl_autoload_register(Array("Requests", "autoloader"))
    # end def register_autoloader
    #// 
    #// Register a transport
    #// 
    #// @param string $transport Transport class to add, must support the Requests_Transport interface
    #//
    @classmethod
    def add_transport(self, transport=None):
        
        if php_empty(lambda : self.transports):
            self.transports = Array("Requests_Transport_cURL", "Requests_Transport_fsockopen")
        # end if
        self.transports = php_array_merge(self.transports, Array(transport))
    # end def add_transport
    #// 
    #// Get a working transport
    #// 
    #// @throws Requests_Exception If no valid transport is found (`notransport`)
    #// @return Requests_Transport
    #//
    def get_transport(self, capabilities=Array()):
        
        #// Caching code, don't bother testing coverage
        #// @codeCoverageIgnoreStart
        #// array of capabilities as a string to be used as an array key
        ksort(capabilities)
        cap_string = serialize(capabilities)
        #// Don't search for a transport if it's already been done for these $capabilities
        if (php_isset(lambda : self.transport[cap_string])) and self.transport[cap_string] != None:
            return php_new_class(self.transport[cap_string], lambda : {**locals(), **globals()}[self.transport[cap_string]]())
        # end if
        #// @codeCoverageIgnoreEnd
        if php_empty(lambda : self.transports):
            self.transports = Array("Requests_Transport_cURL", "Requests_Transport_fsockopen")
        # end if
        #// Find us a working transport
        for class_ in self.transports:
            if (not php_class_exists(class_)):
                continue
            # end if
            result = php_call_user_func(Array(class_, "test"), capabilities)
            if result:
                self.transport[cap_string] = class_
                break
            # end if
        # end for
        if self.transport[cap_string] == None:
            raise php_new_class("Requests_Exception", lambda : Requests_Exception("No working transports found", "notransport", self.transports))
        # end if
        return php_new_class(self.transport[cap_string], lambda : {**locals(), **globals()}[self.transport[cap_string]]())
    # end def get_transport
    #// #@+
    #// @see request()
    #// @param string $url
    #// @param array $headers
    #// @param array $options
    #// @return Requests_Response
    #// 
    #// 
    #// Send a GET request
    #//
    @classmethod
    def get(self, url=None, headers=Array(), options=Array()):
        
        return self.request(url, headers, None, self.GET, options)
    # end def get
    #// 
    #// Send a HEAD request
    #//
    @classmethod
    def head(self, url=None, headers=Array(), options=Array()):
        
        return self.request(url, headers, None, self.HEAD, options)
    # end def head
    #// 
    #// Send a DELETE request
    #//
    @classmethod
    def delete(self, url=None, headers=Array(), options=Array()):
        
        return self.request(url, headers, None, self.DELETE, options)
    # end def delete
    #// 
    #// Send a TRACE request
    #//
    @classmethod
    def trace(self, url=None, headers=Array(), options=Array()):
        
        return self.request(url, headers, None, self.TRACE, options)
    # end def trace
    #// #@-
    #// #@+
    #// @see request()
    #// @param string $url
    #// @param array $headers
    #// @param array $data
    #// @param array $options
    #// @return Requests_Response
    #// 
    #// 
    #// Send a POST request
    #//
    @classmethod
    def post(self, url=None, headers=Array(), data=Array(), options=Array()):
        
        return self.request(url, headers, data, self.POST, options)
    # end def post
    #// 
    #// Send a PUT request
    #//
    @classmethod
    def put(self, url=None, headers=Array(), data=Array(), options=Array()):
        
        return self.request(url, headers, data, self.PUT, options)
    # end def put
    #// 
    #// Send an OPTIONS request
    #//
    @classmethod
    def options(self, url=None, headers=Array(), data=Array(), options=Array()):
        
        return self.request(url, headers, data, self.OPTIONS, options)
    # end def options
    #// 
    #// Send a PATCH request
    #// 
    #// Note: Unlike {@see post} and {@see put}, `$headers` is required, as the
    #// specification recommends that should send an ETag
    #// 
    #// @link https://tools.ietf.org/html/rfc5789
    #//
    @classmethod
    def patch(self, url=None, headers=None, data=Array(), options=Array()):
        
        return self.request(url, headers, data, self.PATCH, options)
    # end def patch
    #// #@-
    #// 
    #// Main interface for HTTP requests
    #// 
    #// This method initiates a request and sends it via a transport before
    #// parsing.
    #// 
    #// The `$options` parameter takes an associative array with the following
    #// options:
    #// 
    #// - `timeout`: How long should we wait for a response?
    #// Note: for cURL, a minimum of 1 second applies, as DNS resolution
    #// operates at second-resolution only.
    #// (float, seconds with a millisecond precision, default: 10, example: 0.01)
    #// - `connect_timeout`: How long should we wait while trying to connect?
    #// (float, seconds with a millisecond precision, default: 10, example: 0.01)
    #// - `useragent`: Useragent to send to the server
    #// (string, default: php-requests/$version)
    #// - `follow_redirects`: Should we follow 3xx redirects?
    #// (boolean, default: true)
    #// - `redirects`: How many times should we redirect before erroring?
    #// (integer, default: 10)
    #// - `blocking`: Should we block processing on this request?
    #// (boolean, default: true)
    #// - `filename`: File to stream the body to instead.
    #// (string|boolean, default: false)
    #// - `auth`: Authentication handler or array of user/password details to use
    #// for Basic authentication
    #// (Requests_Auth|array|boolean, default: false)
    #// - `proxy`: Proxy details to use for proxy by-passing and authentication
    #// (Requests_Proxy|array|string|boolean, default: false)
    #// - `max_bytes`: Limit for the response body size.
    #// (integer|boolean, default: false)
    #// - `idn`: Enable IDN parsing
    #// (boolean, default: true)
    #// - `transport`: Custom transport. Either a class name, or a
    #// transport object. Defaults to the first working transport from
    #// {@see getTransport()}
    #// (string|Requests_Transport, default: {@see getTransport()})
    #// - `hooks`: Hooks handler.
    #// (Requests_Hooker, default: new Requests_Hooks())
    #// - `verify`: Should we verify SSL certificates? Allows passing in a custom
    #// certificate file as a string. (Using true uses the system-wide root
    #// certificate store instead, but this may have different behaviour
    #// across transports.)
    #// (string|boolean, default: library/Requests/Transport/cacert.pem)
    #// - `verifyname`: Should we verify the common name in the SSL certificate?
    #// (boolean: default, true)
    #// - `data_format`: How should we send the `$data` parameter?
    #// (string, one of 'query' or 'body', default: 'query' for
    #// HEAD/GET/DELETE, 'body' for POST/PUT/OPTIONS/PATCH)
    #// 
    #// @throws Requests_Exception On invalid URLs (`nonhttp`)
    #// 
    #// @param string $url URL to request
    #// @param array $headers Extra headers to send with the request
    #// @param array|null $data Data to send either as a query string for GET/HEAD requests, or in the body for POST requests
    #// @param string $type HTTP request type (use Requests constants)
    #// @param array $options Options for the request (see description for more information)
    #// @return Requests_Response
    #//
    @classmethod
    def request(self, url=None, headers=Array(), data=Array(), type=self.GET, options=Array()):
        
        if php_empty(lambda : options["type"]):
            options["type"] = type
        # end if
        options = php_array_merge(self.get_default_options(), options)
        self.set_defaults(url, headers, data, type, options)
        options["hooks"].dispatch("requests.before_request", Array(url, headers, data, type, options))
        if (not php_empty(lambda : options["transport"])):
            transport = options["transport"]
            if php_is_string(options["transport"]):
                transport = php_new_class(transport, lambda : {**locals(), **globals()}[transport]())
            # end if
        else:
            need_ssl = 0 == php_stripos(url, "https://")
            capabilities = Array({"ssl": need_ssl})
            transport = self.get_transport(capabilities)
        # end if
        response = transport.request(url, headers, data, options)
        options["hooks"].dispatch("requests.before_parse", Array(response, url, headers, data, type, options))
        return self.parse_response(response, url, headers, data, options)
    # end def request
    #// 
    #// Send multiple HTTP requests simultaneously
    #// 
    #// The `$requests` parameter takes an associative or indexed array of
    #// request fields. The key of each request can be used to match up the
    #// request with the returned data, or with the request passed into your
    #// `multiple.request.complete` callback.
    #// 
    #// The request fields value is an associative array with the following keys:
    #// 
    #// - `url`: Request URL Same as the `$url` parameter to
    #// {@see Requests::request}
    #// (string, required)
    #// - `headers`: Associative array of header fields. Same as the `$headers`
    #// parameter to {@see Requests::request}
    #// (array, default: `array()`)
    #// - `data`: Associative array of data fields or a string. Same as the
    #// `$data` parameter to {@see Requests::request}
    #// (array|string, default: `array()`)
    #// - `type`: HTTP request type (use Requests constants). Same as the `$type`
    #// parameter to {@see Requests::request}
    #// (string, default: `Requests::GET`)
    #// - `cookies`: Associative array of cookie name to value, or cookie jar.
    #// (array|Requests_Cookie_Jar)
    #// 
    #// If the `$options` parameter is specified, individual requests will
    #// inherit options from it. This can be used to use a single hooking system,
    #// or set all the types to `Requests::POST`, for example.
    #// 
    #// In addition, the `$options` parameter takes the following global options:
    #// 
    #// - `complete`: A callback for when a request is complete. Takes two
    #// parameters, a Requests_Response/Requests_Exception reference, and the
    #// ID from the request array (Note: this can also be overridden on a
    #// per-request basis, although that's a little silly)
    #// (callback)
    #// 
    #// @param array $requests Requests data (see description for more information)
    #// @param array $options Global and default options (see {@see Requests::request})
    #// @return array Responses (either Requests_Response or a Requests_Exception object)
    #//
    @classmethod
    def request_multiple(self, requests=None, options=Array()):
        
        options = php_array_merge(self.get_default_options(True), options)
        if (not php_empty(lambda : options["hooks"])):
            options["hooks"].register("transport.internal.parse_response", Array("Requests", "parse_multiple"))
            if (not php_empty(lambda : options["complete"])):
                options["hooks"].register("multiple.request.complete", options["complete"])
            # end if
        # end if
        for id,request in requests:
            if (not (php_isset(lambda : request["headers"]))):
                request["headers"] = Array()
            # end if
            if (not (php_isset(lambda : request["data"]))):
                request["data"] = Array()
            # end if
            if (not (php_isset(lambda : request["type"]))):
                request["type"] = self.GET
            # end if
            if (not (php_isset(lambda : request["options"]))):
                request["options"] = options
                request["options"]["type"] = request["type"]
            else:
                if php_empty(lambda : request["options"]["type"]):
                    request["options"]["type"] = request["type"]
                # end if
                request["options"] = php_array_merge(options, request["options"])
            # end if
            self.set_defaults(request["url"], request["headers"], request["data"], request["type"], request["options"])
            #// Ensure we only hook in once
            if request["options"]["hooks"] != options["hooks"]:
                request["options"]["hooks"].register("transport.internal.parse_response", Array("Requests", "parse_multiple"))
                if (not php_empty(lambda : request["options"]["complete"])):
                    request["options"]["hooks"].register("multiple.request.complete", request["options"]["complete"])
                # end if
            # end if
        # end for
        request = None
        if (not php_empty(lambda : options["transport"])):
            transport = options["transport"]
            if php_is_string(options["transport"]):
                transport = php_new_class(transport, lambda : {**locals(), **globals()}[transport]())
            # end if
        else:
            transport = self.get_transport()
        # end if
        responses = transport.request_multiple(requests, options)
        for id,response in responses:
            #// If our hook got messed with somehow, ensure we end up with the
            #// correct response
            if php_is_string(response):
                request = requests[id]
                self.parse_multiple(response, request)
                request["options"]["hooks"].dispatch("multiple.request.complete", Array(response, id))
            # end if
        # end for
        return responses
    # end def request_multiple
    #// 
    #// Get the default options
    #// 
    #// @see Requests::request() for values returned by this method
    #// @param boolean $multirequest Is this a multirequest?
    #// @return array Default option values
    #//
    def get_default_options(self, multirequest=False):
        
        defaults = Array({"timeout": 10, "connect_timeout": 10, "useragent": "php-requests/" + self.VERSION, "protocol_version": 1.1, "redirected": 0, "redirects": 10, "follow_redirects": True, "blocking": True, "type": self.GET, "filename": False, "auth": False, "proxy": False, "cookies": False, "max_bytes": False, "idn": True, "hooks": None, "transport": None, "verify": Requests.get_certificate_path(), "verifyname": True})
        if multirequest != False:
            defaults["complete"] = None
        # end if
        return defaults
    # end def get_default_options
    #// 
    #// Get default certificate path.
    #// 
    #// @return string Default certificate path.
    #//
    @classmethod
    def get_certificate_path(self):
        
        if (not php_empty(lambda : Requests.certificate_path)):
            return Requests.certificate_path
        # end if
        return php_dirname(__FILE__) + "/Requests/Transport/cacert.pem"
    # end def get_certificate_path
    #// 
    #// Set default certificate path.
    #// 
    #// @param string $path Certificate path, pointing to a PEM file.
    #//
    @classmethod
    def set_certificate_path(self, path=None):
        
        Requests.certificate_path = path
    # end def set_certificate_path
    #// 
    #// Set the default values
    #// 
    #// @param string $url URL to request
    #// @param array $headers Extra headers to send with the request
    #// @param array|null $data Data to send either as a query string for GET/HEAD requests, or in the body for POST requests
    #// @param string $type HTTP request type
    #// @param array $options Options for the request
    #// @return array $options
    #//
    def set_defaults(self, url=None, headers=None, data=None, type=None, options=None):
        
        if (not php_preg_match("/^http(s)?:\\/\\//i", url, matches)):
            raise php_new_class("Requests_Exception", lambda : Requests_Exception("Only HTTP(S) requests are handled.", "nonhttp", url))
        # end if
        if php_empty(lambda : options["hooks"]):
            options["hooks"] = php_new_class("Requests_Hooks", lambda : Requests_Hooks())
        # end if
        if php_is_array(options["auth"]):
            options["auth"] = php_new_class("Requests_Auth_Basic", lambda : Requests_Auth_Basic(options["auth"]))
        # end if
        if options["auth"] != False:
            options["auth"].register(options["hooks"])
        # end if
        if php_is_string(options["proxy"]) or php_is_array(options["proxy"]):
            options["proxy"] = php_new_class("Requests_Proxy_HTTP", lambda : Requests_Proxy_HTTP(options["proxy"]))
        # end if
        if options["proxy"] != False:
            options["proxy"].register(options["hooks"])
        # end if
        if php_is_array(options["cookies"]):
            options["cookies"] = php_new_class("Requests_Cookie_Jar", lambda : Requests_Cookie_Jar(options["cookies"]))
        elif php_empty(lambda : options["cookies"]):
            options["cookies"] = php_new_class("Requests_Cookie_Jar", lambda : Requests_Cookie_Jar())
        # end if
        if options["cookies"] != False:
            options["cookies"].register(options["hooks"])
        # end if
        if options["idn"] != False:
            iri = php_new_class("Requests_IRI", lambda : Requests_IRI(url))
            iri.host = Requests_IDNAEncoder.encode(iri.ihost)
            url = iri.uri
        # end if
        #// Massage the type to ensure we support it.
        type = php_strtoupper(type)
        if (not (php_isset(lambda : options["data_format"]))):
            if php_in_array(type, Array(self.HEAD, self.GET, self.DELETE)):
                options["data_format"] = "query"
            else:
                options["data_format"] = "body"
            # end if
        # end if
    # end def set_defaults
    #// 
    #// HTTP response parser
    #// 
    #// @throws Requests_Exception On missing head/body separator (`requests.no_crlf_separator`)
    #// @throws Requests_Exception On missing head/body separator (`noversion`)
    #// @throws Requests_Exception On missing head/body separator (`toomanyredirects`)
    #// 
    #// @param string $headers Full response text including headers and body
    #// @param string $url Original request URL
    #// @param array $req_headers Original $headers array passed to {@link request()}, in case we need to follow redirects
    #// @param array $req_data Original $data array passed to {@link request()}, in case we need to follow redirects
    #// @param array $options Original $options array passed to {@link request()}, in case we need to follow redirects
    #// @return Requests_Response
    #//
    def parse_response(self, headers=None, url=None, req_headers=None, req_data=None, options=None):
        
        return_ = php_new_class("Requests_Response", lambda : Requests_Response())
        if (not options["blocking"]):
            return return_
        # end if
        return_.raw = headers
        return_.url = url
        if (not options["filename"]):
            pos = php_strpos(headers, "\r\n\r\n")
            if pos == False:
                raise php_new_class("Requests_Exception", lambda : Requests_Exception("Missing header/body separator", "requests.no_crlf_separator"))
            # end if
            headers = php_substr(return_.raw, 0, pos)
            return_.body = php_substr(return_.raw, pos + php_strlen("\n\r\n\r"))
        else:
            return_.body = ""
        # end if
        #// Pretend CRLF = LF for compatibility (RFC 2616, section 19.3)
        headers = php_str_replace("\r\n", "\n", headers)
        #// Unfold headers (replace [CRLF] 1*( SP | HT ) with SP) as per RFC 2616 (section 2.2)
        headers = php_preg_replace("/\\n[ \\t]/", " ", headers)
        headers = php_explode("\n", headers)
        php_preg_match("#^HTTP/(1\\.\\d)[ \\t]+(\\d+)#i", php_array_shift(headers), matches)
        if php_empty(lambda : matches):
            raise php_new_class("Requests_Exception", lambda : Requests_Exception("Response could not be parsed", "noversion", headers))
        # end if
        return_.protocol_version = float(matches[1])
        return_.status_code = int(matches[2])
        if return_.status_code >= 200 and return_.status_code < 300:
            return_.success = True
        # end if
        for header in headers:
            key, value = php_explode(":", header, 2)
            value = php_trim(value)
            php_preg_replace("#(\\s+)#i", " ", value)
            return_.headers[key] = value
        # end for
        if (php_isset(lambda : return_.headers["transfer-encoding"])):
            return_.body = self.decode_chunked(return_.body)
            return_.headers["transfer-encoding"] = None
        # end if
        if (php_isset(lambda : return_.headers["content-encoding"])):
            return_.body = self.decompress(return_.body)
        # end if
        #// fsockopen and cURL compatibility
        if (php_isset(lambda : return_.headers["connection"])):
            return_.headers["connection"] = None
        # end if
        options["hooks"].dispatch("requests.before_redirect_check", Array(return_, req_headers, req_data, options))
        if return_.is_redirect() and options["follow_redirects"] == True:
            if (php_isset(lambda : return_.headers["location"])) and options["redirected"] < options["redirects"]:
                if return_.status_code == 303:
                    options["type"] = self.GET
                # end if
                options["redirected"] += 1
                location = return_.headers["location"]
                if php_strpos(location, "http://") != 0 and php_strpos(location, "https://") != 0:
                    #// relative redirect, for compatibility make it absolute
                    location = Requests_IRI.absolutize(url, location)
                    location = location.uri
                # end if
                hook_args = Array(location, req_headers, req_data, options, return_)
                options["hooks"].dispatch("requests.before_redirect", hook_args)
                redirected = self.request(location, req_headers, req_data, options["type"], options)
                redirected.history[-1] = return_
                return redirected
            elif options["redirected"] >= options["redirects"]:
                raise php_new_class("Requests_Exception", lambda : Requests_Exception("Too many redirects", "toomanyredirects", return_))
            # end if
        # end if
        return_.redirects = options["redirected"]
        options["hooks"].dispatch("requests.after_request", Array(return_, req_headers, req_data, options))
        return return_
    # end def parse_response
    #// 
    #// Callback for `transport.internal.parse_response`
    #// 
    #// Internal use only. Converts a raw HTTP response to a Requests_Response
    #// while still executing a multiple request.
    #// 
    #// @param string $response Full response text including headers and body (will be overwritten with Response instance)
    #// @param array $request Request data as passed into {@see Requests::request_multiple()}
    #// @return null `$response` is either set to a Requests_Response instance, or a Requests_Exception object
    #//
    @classmethod
    def parse_multiple(self, response=None, request=None):
        
        try: 
            url = request["url"]
            headers = request["headers"]
            data = request["data"]
            options = request["options"]
            response = self.parse_response(response, url, headers, data, options)
        except Requests_Exception as e:
            response = e
        # end try
    # end def parse_multiple
    #// 
    #// Decoded a chunked body as per RFC 2616
    #// 
    #// @see https://tools.ietf.org/html/rfc2616#section-3.6.1
    #// @param string $data Chunked body
    #// @return string Decoded body
    #//
    def decode_chunked(self, data=None):
        
        if (not php_preg_match("/^([0-9a-f]+)(?:;(?:[\\w-]*)(?:=(?:(?:[\\w-]*)*|\"(?:[^\\r\\n])*\"))?)*\\r\\n/i", php_trim(data))):
            return data
        # end if
        decoded = ""
        encoded = data
        while True:
            
            if not (True):
                break
            # end if
            is_chunked = bool(php_preg_match("/^([0-9a-f]+)(?:;(?:[\\w-]*)(?:=(?:(?:[\\w-]*)*|\"(?:[^\\r\\n])*\"))?)*\\r\\n/i", encoded, matches))
            if (not is_chunked):
                #// Looks like it's not chunked after all
                return data
            # end if
            length = hexdec(php_trim(matches[1]))
            if length == 0:
                #// Ignore trailer headers
                return decoded
            # end if
            chunk_length = php_strlen(matches[0])
            decoded += php_substr(encoded, chunk_length, length)
            encoded = php_substr(encoded, chunk_length + length + 2)
            if php_trim(encoded) == "0" or php_empty(lambda : encoded):
                return decoded
            # end if
        # end while
        pass
    # end def decode_chunked
    #// @codeCoverageIgnoreEnd
    #// 
    #// Convert a key => value array to a 'key: value' array for headers
    #// 
    #// @param array $array Dictionary of header values
    #// @return string[] List of headers
    #//
    @classmethod
    def flatten(self, array=None):
        
        return_ = Array()
        for key,value in array:
            return_[-1] = php_sprintf("%s: %s", key, value)
        # end for
        return return_
    # end def flatten
    #// 
    #// Convert a key => value array to a 'key: value' array for headers
    #// 
    #// @codeCoverageIgnore
    #// @deprecated Misspelling of {@see Requests::flatten}
    #// @param array $array Dictionary of header values
    #// @return string[] List of headers
    #//
    @classmethod
    def flattern(self, array=None):
        
        return self.flatten(array)
    # end def flattern
    #// 
    #// Decompress an encoded body
    #// 
    #// Implements gzip, compress and deflate. Guesses which it is by attempting
    #// to decode.
    #// 
    #// @param string $data Compressed data in one of the above formats
    #// @return string Decompressed string
    #//
    @classmethod
    def decompress(self, data=None):
        
        if php_substr(data, 0, 2) != "" and php_substr(data, 0, 2) != "x":
            #// Not actually compressed. Probably cURL ruining this for us.
            return data
        # end if
        decoded = php_no_error(lambda: gzdecode(data))
        if php_function_exists("gzdecode") and decoded != False:
            return decoded
        elif php_function_exists("gzinflate") and php_no_error(lambda: gzinflate(data)) != False:
            decoded = php_no_error(lambda: gzinflate(data))
            return decoded
        elif self.compatible_gzinflate(data) != False:
            decoded = self.compatible_gzinflate(data)
            return decoded
        elif php_function_exists("gzuncompress") and php_no_error(lambda: gzuncompress(data)) != False:
            decoded = php_no_error(lambda: gzuncompress(data))
            return decoded
        # end if
        return data
    # end def decompress
    #// 
    #// Decompression of deflated string while staying compatible with the majority of servers.
    #// 
    #// Certain Servers will return deflated data with headers which PHP's gzinflate()
    #// function cannot handle out of the box. The following function has been created from
    #// various snippets on the gzinflate() PHP documentation.
    #// 
    #// Warning: Magic numbers within. Due to the potential different formats that the compressed
    #// data may be returned in, some "magic offsets" are needed to ensure proper decompression
    #// takes place. For a simple progmatic way to determine the magic offset in use, see:
    #// https://core.trac.wordpress.org/ticket/18273
    #// 
    #// @since 2.8.1
    #// @link https://core.trac.wordpress.org/ticket/18273
    #// @link https://secure.php.net/manual/en/function.gzinflate.php#70875
    #// @link https://secure.php.net/manual/en/function.gzinflate.php#77336
    #// 
    #// @param string $gzData String to decompress.
    #// @return string|bool False on failure.
    #//
    @classmethod
    def compatible_gzinflate(self, gzData=None):
        
        #// Compressed data might contain a full zlib header, if so strip it for
        #// gzinflate()
        if php_substr(gzData, 0, 3) == "":
            i = 10
            flg = php_ord(php_substr(gzData, 3, 1))
            if flg > 0:
                if flg & 4:
                    xlen = unpack("v", php_substr(gzData, i, 2))
                    i = i + 2 + xlen
                # end if
                if flg & 8:
                    i = php_strpos(gzData, " ", i) + 1
                # end if
                if flg & 16:
                    i = php_strpos(gzData, " ", i) + 1
                # end if
                if flg & 2:
                    i = i + 2
                # end if
            # end if
            decompressed = self.compatible_gzinflate(php_substr(gzData, i))
            if False != decompressed:
                return decompressed
            # end if
        # end if
        #// If the data is Huffman Encoded, we must first strip the leading 2
        #// byte Huffman marker for gzinflate()
        #// The response is Huffman coded by many compressors such as
        #// java.util.zip.Deflater, Ruby’s Zlib::Deflate, and .NET's
        #// System.IO.Compression.DeflateStream.
        #// 
        #// See https://decompres.blogspot.com/ for a quick explanation of this
        #// data type
        huffman_encoded = False
        #// low nibble of first byte should be 0x08
        first_nibble = unpack("h", gzData)
        #// First 2 bytes should be divisible by 0x1F
        first_two_bytes = unpack("n", gzData)
        if 8 == first_nibble and 0 == first_two_bytes % 31:
            huffman_encoded = True
        # end if
        if huffman_encoded:
            decompressed = php_no_error(lambda: gzinflate(php_substr(gzData, 2)))
            if False != decompressed:
                return decompressed
            # end if
        # end if
        if "PK" == php_substr(gzData, 0, 4):
            #// ZIP file format header
            #// Offset 6: 2 bytes, General-purpose field
            #// Offset 26: 2 bytes, filename length
            #// Offset 28: 2 bytes, optional field length
            #// Offset 30: Filename field, followed by optional field, followed
            #// immediately by data
            general_purpose_flag = unpack("v", php_substr(gzData, 6, 2))
            #// If the file has been compressed on the fly, 0x08 bit is set of
            #// the general purpose field. We can use this to differentiate
            #// between a compressed document, and a ZIP file
            zip_compressed_on_the_fly = 8 == 8 & general_purpose_flag
            if (not zip_compressed_on_the_fly):
                #// Don't attempt to decode a compressed zip file
                return gzData
            # end if
            #// Determine the first byte of data, based on the above ZIP header
            #// offsets:
            first_file_start = array_sum(unpack("v2", php_substr(gzData, 26, 4)))
            decompressed = php_no_error(lambda: gzinflate(php_substr(gzData, 30 + first_file_start)))
            if False != decompressed:
                return decompressed
            # end if
            return False
        # end if
        #// Finally fall back to straight gzinflate
        decompressed = php_no_error(lambda: gzinflate(gzData))
        if False != decompressed:
            return decompressed
        # end if
        #// Fallback for all above failing, not expected, but included for
        #// debugging and preventing regressions and to track stats
        decompressed = php_no_error(lambda: gzinflate(php_substr(gzData, 2)))
        if False != decompressed:
            return decompressed
        # end if
        return False
    # end def compatible_gzinflate
    @classmethod
    def match_domain(self, host=None, reference=None):
        
        #// Check for a direct match
        if host == reference:
            return True
        # end if
        #// Calculate the valid wildcard match if the host is not an IP address
        #// Also validates that the host has 3 parts or more, as per Firefox's
        #// ruleset.
        parts = php_explode(".", host)
        if ip2long(host) == False and php_count(parts) >= 3:
            parts[0] = "*"
            wildcard = php_implode(".", parts)
            if wildcard == reference:
                return True
            # end if
        # end if
        return False
    # end def match_domain
# end class Requests
