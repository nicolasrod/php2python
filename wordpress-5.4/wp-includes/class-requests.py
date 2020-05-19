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
    #// 
    #// Registered transport classes
    #// 
    #// @var array
    #//
    transports = Array()
    #// 
    #// Selected transport name
    #// 
    #// Use {@see get_transport()} instead
    #// 
    #// @var array
    #//
    transport = Array()
    #// 
    #// Default certificate path.
    #// 
    #// @see Requests::get_certificate_path()
    #// @see Requests::set_certificate_path()
    #// 
    #// @var string
    #//
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
        file_ = php_str_replace("_", "/", class_)
        if php_file_exists(php_dirname(__FILE__) + "/" + file_ + ".php"):
            php_include_file(php_dirname(__FILE__) + "/" + file_ + ".php", once=True)
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
    def add_transport(self, transport_=None):
        
        
        if php_empty(lambda : self.transports):
            self.transports = Array("Requests_Transport_cURL", "Requests_Transport_fsockopen")
        # end if
        self.transports = php_array_merge(self.transports, Array(transport_))
    # end def add_transport
    #// 
    #// Get a working transport
    #// 
    #// @throws Requests_Exception If no valid transport is found (`notransport`)
    #// @return Requests_Transport
    #//
    def get_transport(self, capabilities_=None):
        if capabilities_ is None:
            capabilities_ = Array()
        # end if
        
        #// Caching code, don't bother testing coverage
        #// @codeCoverageIgnoreStart
        #// array of capabilities as a string to be used as an array key
        php_ksort(capabilities_)
        cap_string_ = serialize(capabilities_)
        #// Don't search for a transport if it's already been done for these $capabilities
        if (php_isset(lambda : self.transport[cap_string_])) and self.transport[cap_string_] != None:
            return php_new_class(self.transport[cap_string_], lambda : {**locals(), **globals()}[self.transport[cap_string_]]())
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
            result_ = php_call_user_func(Array(class_, "test"), capabilities_)
            if result_:
                self.transport[cap_string_] = class_
                break
            # end if
        # end for
        if self.transport[cap_string_] == None:
            raise php_new_class("Requests_Exception", lambda : Requests_Exception("No working transports found", "notransport", self.transports))
        # end if
        return php_new_class(self.transport[cap_string_], lambda : {**locals(), **globals()}[self.transport[cap_string_]]())
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
    def get(self, url_=None, headers_=None, options_=None):
        if headers_ is None:
            headers_ = Array()
        # end if
        if options_ is None:
            options_ = Array()
        # end if
        
        return self.request(url_, headers_, None, self.GET, options_)
    # end def get
    #// 
    #// Send a HEAD request
    #//
    @classmethod
    def head(self, url_=None, headers_=None, options_=None):
        if headers_ is None:
            headers_ = Array()
        # end if
        if options_ is None:
            options_ = Array()
        # end if
        
        return self.request(url_, headers_, None, self.HEAD, options_)
    # end def head
    #// 
    #// Send a DELETE request
    #//
    @classmethod
    def delete(self, url_=None, headers_=None, options_=None):
        if headers_ is None:
            headers_ = Array()
        # end if
        if options_ is None:
            options_ = Array()
        # end if
        
        return self.request(url_, headers_, None, self.DELETE, options_)
    # end def delete
    #// 
    #// Send a TRACE request
    #//
    @classmethod
    def trace(self, url_=None, headers_=None, options_=None):
        if headers_ is None:
            headers_ = Array()
        # end if
        if options_ is None:
            options_ = Array()
        # end if
        
        return self.request(url_, headers_, None, self.TRACE, options_)
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
    def post(self, url_=None, headers_=None, data_=None, options_=None):
        if headers_ is None:
            headers_ = Array()
        # end if
        if data_ is None:
            data_ = Array()
        # end if
        if options_ is None:
            options_ = Array()
        # end if
        
        return self.request(url_, headers_, data_, self.POST, options_)
    # end def post
    #// 
    #// Send a PUT request
    #//
    @classmethod
    def put(self, url_=None, headers_=None, data_=None, options_=None):
        if headers_ is None:
            headers_ = Array()
        # end if
        if data_ is None:
            data_ = Array()
        # end if
        if options_ is None:
            options_ = Array()
        # end if
        
        return self.request(url_, headers_, data_, self.PUT, options_)
    # end def put
    #// 
    #// Send an OPTIONS request
    #//
    @classmethod
    def options(self, url_=None, headers_=None, data_=None, options_=None):
        if headers_ is None:
            headers_ = Array()
        # end if
        if data_ is None:
            data_ = Array()
        # end if
        if options_ is None:
            options_ = Array()
        # end if
        
        return self.request(url_, headers_, data_, self.OPTIONS, options_)
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
    def patch(self, url_=None, headers_=None, data_=None, options_=None):
        if data_ is None:
            data_ = Array()
        # end if
        if options_ is None:
            options_ = Array()
        # end if
        
        return self.request(url_, headers_, data_, self.PATCH, options_)
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
    def request(self, url_=None, headers_=None, data_=None, type_=None, options_=None):
        if headers_ is None:
            headers_ = Array()
        # end if
        if data_ is None:
            data_ = Array()
        # end if
        if type_ is None:
            type_ = self.GET
        # end if
        if options_ is None:
            options_ = Array()
        # end if
        
        if php_empty(lambda : options_["type"]):
            options_["type"] = type_
        # end if
        options_ = php_array_merge(self.get_default_options(), options_)
        self.set_defaults(url_, headers_, data_, type_, options_)
        options_["hooks"].dispatch("requests.before_request", Array(url_, headers_, data_, type_, options_))
        if (not php_empty(lambda : options_["transport"])):
            transport_ = options_["transport"]
            if php_is_string(options_["transport"]):
                transport_ = php_new_class(transport_, lambda : {**locals(), **globals()}[transport_]())
            # end if
        else:
            need_ssl_ = 0 == php_stripos(url_, "https://")
            capabilities_ = Array({"ssl": need_ssl_})
            transport_ = self.get_transport(capabilities_)
        # end if
        response_ = transport_.request(url_, headers_, data_, options_)
        options_["hooks"].dispatch("requests.before_parse", Array(response_, url_, headers_, data_, type_, options_))
        return self.parse_response(response_, url_, headers_, data_, options_)
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
    def request_multiple(self, requests_=None, options_=None):
        if options_ is None:
            options_ = Array()
        # end if
        
        options_ = php_array_merge(self.get_default_options(True), options_)
        if (not php_empty(lambda : options_["hooks"])):
            options_["hooks"].register("transport.internal.parse_response", Array("Requests", "parse_multiple"))
            if (not php_empty(lambda : options_["complete"])):
                options_["hooks"].register("multiple.request.complete", options_["complete"])
            # end if
        # end if
        for id_,request_ in requests_.items():
            if (not (php_isset(lambda : request_["headers"]))):
                request_["headers"] = Array()
            # end if
            if (not (php_isset(lambda : request_["data"]))):
                request_["data"] = Array()
            # end if
            if (not (php_isset(lambda : request_["type"]))):
                request_["type"] = self.GET
            # end if
            if (not (php_isset(lambda : request_["options"]))):
                request_["options"] = options_
                request_["options"]["type"] = request_["type"]
            else:
                if php_empty(lambda : request_["options"]["type"]):
                    request_["options"]["type"] = request_["type"]
                # end if
                request_["options"] = php_array_merge(options_, request_["options"])
            # end if
            self.set_defaults(request_["url"], request_["headers"], request_["data"], request_["type"], request_["options"])
            #// Ensure we only hook in once
            if request_["options"]["hooks"] != options_["hooks"]:
                request_["options"]["hooks"].register("transport.internal.parse_response", Array("Requests", "parse_multiple"))
                if (not php_empty(lambda : request_["options"]["complete"])):
                    request_["options"]["hooks"].register("multiple.request.complete", request_["options"]["complete"])
                # end if
            # end if
        # end for
        request_ = None
        if (not php_empty(lambda : options_["transport"])):
            transport_ = options_["transport"]
            if php_is_string(options_["transport"]):
                transport_ = php_new_class(transport_, lambda : {**locals(), **globals()}[transport_]())
            # end if
        else:
            transport_ = self.get_transport()
        # end if
        responses_ = transport_.request_multiple(requests_, options_)
        for id_,response_ in responses_.items():
            #// If our hook got messed with somehow, ensure we end up with the
            #// correct response
            if php_is_string(response_):
                request_ = requests_[id_]
                self.parse_multiple(response_, request_)
                request_["options"]["hooks"].dispatch("multiple.request.complete", Array(response_, id_))
            # end if
        # end for
        return responses_
    # end def request_multiple
    #// 
    #// Get the default options
    #// 
    #// @see Requests::request() for values returned by this method
    #// @param boolean $multirequest Is this a multirequest?
    #// @return array Default option values
    #//
    def get_default_options(self, multirequest_=None):
        if multirequest_ is None:
            multirequest_ = False
        # end if
        
        defaults_ = Array({"timeout": 10, "connect_timeout": 10, "useragent": "php-requests/" + self.VERSION, "protocol_version": 1.1, "redirected": 0, "redirects": 10, "follow_redirects": True, "blocking": True, "type": self.GET, "filename": False, "auth": False, "proxy": False, "cookies": False, "max_bytes": False, "idn": True, "hooks": None, "transport": None, "verify": Requests.get_certificate_path(), "verifyname": True})
        if multirequest_ != False:
            defaults_["complete"] = None
        # end if
        return defaults_
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
    def set_certificate_path(self, path_=None):
        
        
        Requests.certificate_path = path_
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
    def set_defaults(self, url_=None, headers_=None, data_=None, type_=None, options_=None):
        
        
        if (not php_preg_match("/^http(s)?:\\/\\//i", url_, matches_)):
            raise php_new_class("Requests_Exception", lambda : Requests_Exception("Only HTTP(S) requests are handled.", "nonhttp", url_))
        # end if
        if php_empty(lambda : options_["hooks"]):
            options_["hooks"] = php_new_class("Requests_Hooks", lambda : Requests_Hooks())
        # end if
        if php_is_array(options_["auth"]):
            options_["auth"] = php_new_class("Requests_Auth_Basic", lambda : Requests_Auth_Basic(options_["auth"]))
        # end if
        if options_["auth"] != False:
            options_["auth"].register(options_["hooks"])
        # end if
        if php_is_string(options_["proxy"]) or php_is_array(options_["proxy"]):
            options_["proxy"] = php_new_class("Requests_Proxy_HTTP", lambda : Requests_Proxy_HTTP(options_["proxy"]))
        # end if
        if options_["proxy"] != False:
            options_["proxy"].register(options_["hooks"])
        # end if
        if php_is_array(options_["cookies"]):
            options_["cookies"] = php_new_class("Requests_Cookie_Jar", lambda : Requests_Cookie_Jar(options_["cookies"]))
        elif php_empty(lambda : options_["cookies"]):
            options_["cookies"] = php_new_class("Requests_Cookie_Jar", lambda : Requests_Cookie_Jar())
        # end if
        if options_["cookies"] != False:
            options_["cookies"].register(options_["hooks"])
        # end if
        if options_["idn"] != False:
            iri_ = php_new_class("Requests_IRI", lambda : Requests_IRI(url_))
            iri_.host = Requests_IDNAEncoder.encode(iri_.ihost)
            url_ = iri_.uri
        # end if
        #// Massage the type to ensure we support it.
        type_ = php_strtoupper(type_)
        if (not (php_isset(lambda : options_["data_format"]))):
            if php_in_array(type_, Array(self.HEAD, self.GET, self.DELETE)):
                options_["data_format"] = "query"
            else:
                options_["data_format"] = "body"
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
    def parse_response(self, headers_=None, url_=None, req_headers_=None, req_data_=None, options_=None):
        
        
        return_ = php_new_class("Requests_Response", lambda : Requests_Response())
        if (not options_["blocking"]):
            return return_
        # end if
        return_.raw = headers_
        return_.url = url_
        if (not options_["filename"]):
            pos_ = php_strpos(headers_, "\r\n\r\n")
            if pos_ == False:
                raise php_new_class("Requests_Exception", lambda : Requests_Exception("Missing header/body separator", "requests.no_crlf_separator"))
            # end if
            headers_ = php_substr(return_.raw, 0, pos_)
            return_.body = php_substr(return_.raw, pos_ + php_strlen("\n\r\n\r"))
        else:
            return_.body = ""
        # end if
        #// Pretend CRLF = LF for compatibility (RFC 2616, section 19.3)
        headers_ = php_str_replace("\r\n", "\n", headers_)
        #// Unfold headers (replace [CRLF] 1*( SP | HT ) with SP) as per RFC 2616 (section 2.2)
        headers_ = php_preg_replace("/\\n[ \\t]/", " ", headers_)
        headers_ = php_explode("\n", headers_)
        php_preg_match("#^HTTP/(1\\.\\d)[ \\t]+(\\d+)#i", php_array_shift(headers_), matches_)
        if php_empty(lambda : matches_):
            raise php_new_class("Requests_Exception", lambda : Requests_Exception("Response could not be parsed", "noversion", headers_))
        # end if
        return_.protocol_version = php_float(matches_[1])
        return_.status_code = php_int(matches_[2])
        if return_.status_code >= 200 and return_.status_code < 300:
            return_.success = True
        # end if
        for header_ in headers_:
            key_, value_ = php_explode(":", header_, 2)
            value_ = php_trim(value_)
            php_preg_replace("#(\\s+)#i", " ", value_)
            return_.headers[key_] = value_
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
        options_["hooks"].dispatch("requests.before_redirect_check", Array(return_, req_headers_, req_data_, options_))
        if return_.is_redirect() and options_["follow_redirects"] == True:
            if (php_isset(lambda : return_.headers["location"])) and options_["redirected"] < options_["redirects"]:
                if return_.status_code == 303:
                    options_["type"] = self.GET
                # end if
                options_["redirected"] += 1
                location_ = return_.headers["location"]
                if php_strpos(location_, "http://") != 0 and php_strpos(location_, "https://") != 0:
                    #// relative redirect, for compatibility make it absolute
                    location_ = Requests_IRI.absolutize(url_, location_)
                    location_ = location_.uri
                # end if
                hook_args_ = Array(location_, req_headers_, req_data_, options_, return_)
                options_["hooks"].dispatch("requests.before_redirect", hook_args_)
                redirected_ = self.request(location_, req_headers_, req_data_, options_["type"], options_)
                redirected_.history[-1] = return_
                return redirected_
            elif options_["redirected"] >= options_["redirects"]:
                raise php_new_class("Requests_Exception", lambda : Requests_Exception("Too many redirects", "toomanyredirects", return_))
            # end if
        # end if
        return_.redirects = options_["redirected"]
        options_["hooks"].dispatch("requests.after_request", Array(return_, req_headers_, req_data_, options_))
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
    def parse_multiple(self, response_=None, request_=None):
        
        
        try: 
            url_ = request_["url"]
            headers_ = request_["headers"]
            data_ = request_["data"]
            options_ = request_["options"]
            response_ = self.parse_response(response_, url_, headers_, data_, options_)
        except Requests_Exception as e_:
            response_ = e_
        # end try
    # end def parse_multiple
    #// 
    #// Decoded a chunked body as per RFC 2616
    #// 
    #// @see https://tools.ietf.org/html/rfc2616#section-3.6.1
    #// @param string $data Chunked body
    #// @return string Decoded body
    #//
    def decode_chunked(self, data_=None):
        
        
        if (not php_preg_match("/^([0-9a-f]+)(?:;(?:[\\w-]*)(?:=(?:(?:[\\w-]*)*|\"(?:[^\\r\\n])*\"))?)*\\r\\n/i", php_trim(data_))):
            return data_
        # end if
        decoded_ = ""
        encoded_ = data_
        while True:
            
            if not (True):
                break
            # end if
            is_chunked_ = php_bool(php_preg_match("/^([0-9a-f]+)(?:;(?:[\\w-]*)(?:=(?:(?:[\\w-]*)*|\"(?:[^\\r\\n])*\"))?)*\\r\\n/i", encoded_, matches_))
            if (not is_chunked_):
                #// Looks like it's not chunked after all
                return data_
            # end if
            length_ = hexdec(php_trim(matches_[1]))
            if length_ == 0:
                #// Ignore trailer headers
                return decoded_
            # end if
            chunk_length_ = php_strlen(matches_[0])
            decoded_ += php_substr(encoded_, chunk_length_, length_)
            encoded_ = php_substr(encoded_, chunk_length_ + length_ + 2)
            if php_trim(encoded_) == "0" or php_empty(lambda : encoded_):
                return decoded_
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
    def flatten(self, array_=None):
        
        
        return_ = Array()
        for key_,value_ in array_.items():
            return_[-1] = php_sprintf("%s: %s", key_, value_)
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
    def flattern(self, array_=None):
        
        
        return self.flatten(array_)
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
    def decompress(self, data_=None):
        
        
        if php_substr(data_, 0, 2) != "" and php_substr(data_, 0, 2) != "x":
            #// Not actually compressed. Probably cURL ruining this for us.
            return data_
        # end if
        decoded_ = php_no_error(lambda: gzdecode(data_))
        if php_function_exists("gzdecode") and decoded_ != False:
            return decoded_
        elif php_function_exists("gzinflate") and php_no_error(lambda: gzinflate(data_)) != False:
            decoded_ = php_no_error(lambda: gzinflate(data_))
            return decoded_
        elif self.compatible_gzinflate(data_) != False:
            decoded_ = self.compatible_gzinflate(data_)
            return decoded_
        elif php_function_exists("gzuncompress") and php_no_error(lambda: gzuncompress(data_)) != False:
            decoded_ = php_no_error(lambda: gzuncompress(data_))
            return decoded_
        # end if
        return data_
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
    def compatible_gzinflate(self, gzData_=None):
        
        
        #// Compressed data might contain a full zlib header, if so strip it for
        #// gzinflate()
        if php_substr(gzData_, 0, 3) == "":
            i_ = 10
            flg_ = php_ord(php_substr(gzData_, 3, 1))
            if flg_ > 0:
                if flg_ & 4:
                    xlen_ = unpack("v", php_substr(gzData_, i_, 2))
                    i_ = i_ + 2 + xlen_
                # end if
                if flg_ & 8:
                    i_ = php_strpos(gzData_, " ", i_) + 1
                # end if
                if flg_ & 16:
                    i_ = php_strpos(gzData_, " ", i_) + 1
                # end if
                if flg_ & 2:
                    i_ = i_ + 2
                # end if
            # end if
            decompressed_ = self.compatible_gzinflate(php_substr(gzData_, i_))
            if False != decompressed_:
                return decompressed_
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
        huffman_encoded_ = False
        #// low nibble of first byte should be 0x08
        first_nibble_ = unpack("h", gzData_)
        #// First 2 bytes should be divisible by 0x1F
        first_two_bytes_ = unpack("n", gzData_)
        if 8 == first_nibble_ and 0 == first_two_bytes_ % 31:
            huffman_encoded_ = True
        # end if
        if huffman_encoded_:
            decompressed_ = php_no_error(lambda: gzinflate(php_substr(gzData_, 2)))
            if False != decompressed_:
                return decompressed_
            # end if
        # end if
        if "PK" == php_substr(gzData_, 0, 4):
            #// ZIP file format header
            #// Offset 6: 2 bytes, General-purpose field
            #// Offset 26: 2 bytes, filename length
            #// Offset 28: 2 bytes, optional field length
            #// Offset 30: Filename field, followed by optional field, followed
            #// immediately by data
            general_purpose_flag_ = unpack("v", php_substr(gzData_, 6, 2))
            #// If the file has been compressed on the fly, 0x08 bit is set of
            #// the general purpose field. We can use this to differentiate
            #// between a compressed document, and a ZIP file
            zip_compressed_on_the_fly_ = 8 == 8 & general_purpose_flag_
            if (not zip_compressed_on_the_fly_):
                #// Don't attempt to decode a compressed zip file
                return gzData_
            # end if
            #// Determine the first byte of data, based on the above ZIP header
            #// offsets:
            first_file_start_ = array_sum(unpack("v2", php_substr(gzData_, 26, 4)))
            decompressed_ = php_no_error(lambda: gzinflate(php_substr(gzData_, 30 + first_file_start_)))
            if False != decompressed_:
                return decompressed_
            # end if
            return False
        # end if
        #// Finally fall back to straight gzinflate
        decompressed_ = php_no_error(lambda: gzinflate(gzData_))
        if False != decompressed_:
            return decompressed_
        # end if
        #// Fallback for all above failing, not expected, but included for
        #// debugging and preventing regressions and to track stats
        decompressed_ = php_no_error(lambda: gzinflate(php_substr(gzData_, 2)))
        if False != decompressed_:
            return decompressed_
        # end if
        return False
    # end def compatible_gzinflate
    @classmethod
    def match_domain(self, host_=None, reference_=None):
        
        
        #// Check for a direct match
        if host_ == reference_:
            return True
        # end if
        #// Calculate the valid wildcard match if the host is not an IP address
        #// Also validates that the host has 3 parts or more, as per Firefox's
        #// ruleset.
        parts_ = php_explode(".", host_)
        if ip2long(host_) == False and php_count(parts_) >= 3:
            parts_[0] = "*"
            wildcard_ = php_implode(".", parts_)
            if wildcard_ == reference_:
                return True
            # end if
        # end if
        return False
    # end def match_domain
# end class Requests
