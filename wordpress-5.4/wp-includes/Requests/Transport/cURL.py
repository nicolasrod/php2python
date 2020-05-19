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
#// cURL HTTP transport
#// 
#// @package Requests
#// @subpackage Transport
#// 
#// 
#// cURL HTTP transport
#// 
#// @package Requests
#// @subpackage Transport
#//
class Requests_Transport_cURL(Requests_Transport):
    CURL_7_10_5 = 461317
    CURL_7_16_2 = 462850
    #// 
    #// Raw HTTP data
    #// 
    #// @var string
    #//
    headers = ""
    #// 
    #// Raw body data
    #// 
    #// @var string
    #//
    response_data = ""
    #// 
    #// Information on the current request
    #// 
    #// @var array cURL information array, see {@see https://secure.php.net/curl_getinfo}
    #//
    info = Array()
    #// 
    #// Version string
    #// 
    #// @var long
    #//
    version = Array()
    #// 
    #// cURL handle
    #// 
    #// @var resource
    #//
    handle = Array()
    #// 
    #// Hook dispatcher instance
    #// 
    #// @var Requests_Hooks
    #//
    hooks = Array()
    #// 
    #// Have we finished the headers yet?
    #// 
    #// @var boolean
    #//
    done_headers = False
    #// 
    #// If streaming to a file, keep the file pointer
    #// 
    #// @var resource
    #//
    stream_handle = Array()
    #// 
    #// How many bytes are in the response body?
    #// 
    #// @var int
    #//
    response_bytes = Array()
    #// 
    #// What's the maximum number of bytes we should keep?
    #// 
    #// @var int|bool Byte count, or false if no limit.
    #//
    response_byte_limit = Array()
    #// 
    #// Constructor
    #//
    def __init__(self):
        
        
        curl_ = curl_version()
        self.version = curl_["version_number"]
        self.handle = curl_init()
        curl_setopt(self.handle, CURLOPT_HEADER, False)
        curl_setopt(self.handle, CURLOPT_RETURNTRANSFER, 1)
        if self.version >= self.CURL_7_10_5:
            curl_setopt(self.handle, CURLOPT_ENCODING, "")
        # end if
        if php_defined("CURLOPT_PROTOCOLS"):
            curl_setopt(self.handle, CURLOPT_PROTOCOLS, CURLPROTO_HTTP | CURLPROTO_HTTPS)
        # end if
        if php_defined("CURLOPT_REDIR_PROTOCOLS"):
            curl_setopt(self.handle, CURLOPT_REDIR_PROTOCOLS, CURLPROTO_HTTP | CURLPROTO_HTTPS)
        # end if
    # end def __init__
    #// 
    #// Destructor
    #//
    def __del__(self):
        
        
        if is_resource(self.handle):
            curl_close(self.handle)
        # end if
    # end def __del__
    #// 
    #// Perform a request
    #// 
    #// @throws Requests_Exception On a cURL error (`curlerror`)
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
        
        self.hooks = options_["hooks"]
        self.setup_handle(url_, headers_, data_, options_)
        options_["hooks"].dispatch("curl.before_send", Array(self.handle))
        if options_["filename"] != False:
            self.stream_handle = fopen(options_["filename"], "wb")
        # end if
        self.response_data = ""
        self.response_bytes = 0
        self.response_byte_limit = False
        if options_["max_bytes"] != False:
            self.response_byte_limit = options_["max_bytes"]
        # end if
        if (php_isset(lambda : options_["verify"])):
            if options_["verify"] == False:
                curl_setopt(self.handle, CURLOPT_SSL_VERIFYHOST, 0)
                curl_setopt(self.handle, CURLOPT_SSL_VERIFYPEER, 0)
            elif php_is_string(options_["verify"]):
                curl_setopt(self.handle, CURLOPT_CAINFO, options_["verify"])
            # end if
        # end if
        if (php_isset(lambda : options_["verifyname"])) and options_["verifyname"] == False:
            curl_setopt(self.handle, CURLOPT_SSL_VERIFYHOST, 0)
        # end if
        curl_exec(self.handle)
        response_ = self.response_data
        options_["hooks"].dispatch("curl.after_send", Array())
        if curl_errno(self.handle) == 23 or curl_errno(self.handle) == 61:
            #// Reset encoding and try again
            curl_setopt(self.handle, CURLOPT_ENCODING, "none")
            self.response_data = ""
            self.response_bytes = 0
            curl_exec(self.handle)
            response_ = self.response_data
        # end if
        self.process_response(response_, options_)
        #// Need to remove the $this reference from the curl handle.
        #// Otherwise Requests_Transport_cURL wont be garbage collected and the curl_close() will never be called.
        curl_setopt(self.handle, CURLOPT_HEADERFUNCTION, None)
        curl_setopt(self.handle, CURLOPT_WRITEFUNCTION, None)
        return self.headers
    # end def request
    #// 
    #// Send multiple requests simultaneously
    #// 
    #// @param array $requests Request data
    #// @param array $options Global options
    #// @return array Array of Requests_Response objects (may contain Requests_Exception or string responses as well)
    #//
    def request_multiple(self, requests_=None, options_=None):
        
        
        #// If you're not requesting, we can't get any responses ¯\_(ツ)_/¯
        if php_empty(lambda : requests_):
            return Array()
        # end if
        multihandle_ = curl_multi_init()
        subrequests_ = Array()
        subhandles_ = Array()
        class_ = get_class(self)
        for id_,request_ in requests_.items():
            subrequests_[id_] = php_new_class(class_, lambda : {**locals(), **globals()}[class_]())
            subhandles_[id_] = subrequests_[id_].get_subrequest_handle(request_["url"], request_["headers"], request_["data"], request_["options"])
            request_["options"]["hooks"].dispatch("curl.before_multi_add", Array(subhandles_[id_]))
            curl_multi_add_handle(multihandle_, subhandles_[id_])
        # end for
        completed_ = 0
        responses_ = Array()
        request_["options"]["hooks"].dispatch("curl.before_multi_exec", Array(multihandle_))
        while True:
            active_ = False
            while True:
                status_ = curl_multi_exec(multihandle_, active_)
                
                if status_ == CURLM_CALL_MULTI_PERFORM:
                    break
                # end if
            # end while
            to_process_ = Array()
            #// Read the information as needed
            while True:
                done_ = curl_multi_info_read(multihandle_)
                if not (done_):
                    break
                # end if
                key_ = php_array_search(done_["handle"], subhandles_, True)
                if (not (php_isset(lambda : to_process_[key_]))):
                    to_process_[key_] = done_
                # end if
            # end while
            #// Parse the finished requests before we start getting the new ones
            for key_,done_ in to_process_.items():
                options_ = requests_[key_]["options"]
                if CURLE_OK != done_["result"]:
                    #// get error string for handle.
                    reason_ = curl_error(done_["handle"])
                    exception_ = php_new_class("Requests_Exception_Transport_cURL", lambda : Requests_Exception_Transport_cURL(reason_, Requests_Exception_Transport_cURL.EASY, done_["handle"], done_["result"]))
                    responses_[key_] = exception_
                    options_["hooks"].dispatch("transport.internal.parse_error", Array(responses_[key_], requests_[key_]))
                else:
                    responses_[key_] = subrequests_[key_].process_response(subrequests_[key_].response_data, options_)
                    options_["hooks"].dispatch("transport.internal.parse_response", Array(responses_[key_], requests_[key_]))
                # end if
                curl_multi_remove_handle(multihandle_, done_["handle"])
                curl_close(done_["handle"])
                if (not php_is_string(responses_[key_])):
                    options_["hooks"].dispatch("multiple.request.complete", Array(responses_[key_], key_))
                # end if
                completed_ += 1
            # end for
            
            if active_ or completed_ < php_count(subrequests_):
                break
            # end if
        # end while
        request_["options"]["hooks"].dispatch("curl.after_multi_exec", Array(multihandle_))
        curl_multi_close(multihandle_)
        return responses_
    # end def request_multiple
    #// 
    #// Get the cURL handle for use in a multi-request
    #// 
    #// @param string $url URL to request
    #// @param array $headers Associative array of request headers
    #// @param string|array $data Data to send either as the POST body, or as parameters in the URL for a GET/HEAD
    #// @param array $options Request options, see {@see Requests::response()} for documentation
    #// @return resource Subrequest's cURL handle
    #//
    def get_subrequest_handle(self, url_=None, headers_=None, data_=None, options_=None):
        
        
        self.setup_handle(url_, headers_, data_, options_)
        if options_["filename"] != False:
            self.stream_handle = fopen(options_["filename"], "wb")
        # end if
        self.response_data = ""
        self.response_bytes = 0
        self.response_byte_limit = False
        if options_["max_bytes"] != False:
            self.response_byte_limit = options_["max_bytes"]
        # end if
        self.hooks = options_["hooks"]
        return self.handle
    # end def get_subrequest_handle
    #// 
    #// Setup the cURL handle for the given data
    #// 
    #// @param string $url URL to request
    #// @param array $headers Associative array of request headers
    #// @param string|array $data Data to send either as the POST body, or as parameters in the URL for a GET/HEAD
    #// @param array $options Request options, see {@see Requests::response()} for documentation
    #//
    def setup_handle(self, url_=None, headers_=None, data_=None, options_=None):
        
        
        options_["hooks"].dispatch("curl.before_request", Array(self.handle))
        #// Force closing the connection for old versions of cURL (<7.22).
        if (not (php_isset(lambda : headers_["Connection"]))):
            headers_["Connection"] = "close"
        # end if
        headers_ = Requests.flatten(headers_)
        if (not php_empty(lambda : data_)):
            data_format_ = options_["data_format"]
            if data_format_ == "query":
                url_ = self.format_get(url_, data_)
                data_ = ""
            elif (not php_is_string(data_)):
                data_ = http_build_query(data_, None, "&")
            # end if
        # end if
        for case in Switch(options_["type"]):
            if case(Requests.POST):
                curl_setopt(self.handle, CURLOPT_POST, True)
                curl_setopt(self.handle, CURLOPT_POSTFIELDS, data_)
                break
            # end if
            if case(Requests.HEAD):
                curl_setopt(self.handle, CURLOPT_CUSTOMREQUEST, options_["type"])
                curl_setopt(self.handle, CURLOPT_NOBODY, True)
                break
            # end if
            if case(Requests.TRACE):
                curl_setopt(self.handle, CURLOPT_CUSTOMREQUEST, options_["type"])
                break
            # end if
            if case(Requests.PATCH):
                pass
            # end if
            if case(Requests.PUT):
                pass
            # end if
            if case(Requests.DELETE):
                pass
            # end if
            if case(Requests.OPTIONS):
                pass
            # end if
            if case():
                curl_setopt(self.handle, CURLOPT_CUSTOMREQUEST, options_["type"])
                if (not php_empty(lambda : data_)):
                    curl_setopt(self.handle, CURLOPT_POSTFIELDS, data_)
                # end if
            # end if
        # end for
        #// cURL requires a minimum timeout of 1 second when using the system
        #// DNS resolver, as it uses `alarm()`, which is second resolution only.
        #// There's no way to detect which DNS resolver is being used from our
        #// end, so we need to round up regardless of the supplied timeout.
        #// 
        #// https://github.com/curl/curl/blob/4f45240bc84a9aa648c8f7243be7b79e9f9323a5/lib/hostip.c#L606-L609
        timeout_ = php_max(options_["timeout"], 1)
        if php_is_int(timeout_) or self.version < self.CURL_7_16_2:
            curl_setopt(self.handle, CURLOPT_TIMEOUT, ceil(timeout_))
        else:
            curl_setopt(self.handle, CURLOPT_TIMEOUT_MS, round(timeout_ * 1000))
        # end if
        if php_is_int(options_["connect_timeout"]) or self.version < self.CURL_7_16_2:
            curl_setopt(self.handle, CURLOPT_CONNECTTIMEOUT, ceil(options_["connect_timeout"]))
        else:
            curl_setopt(self.handle, CURLOPT_CONNECTTIMEOUT_MS, round(options_["connect_timeout"] * 1000))
        # end if
        curl_setopt(self.handle, CURLOPT_URL, url_)
        curl_setopt(self.handle, CURLOPT_REFERER, url_)
        curl_setopt(self.handle, CURLOPT_USERAGENT, options_["useragent"])
        if (not php_empty(lambda : headers_)):
            curl_setopt(self.handle, CURLOPT_HTTPHEADER, headers_)
        # end if
        if options_["protocol_version"] == 1.1:
            curl_setopt(self.handle, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_1_1)
        else:
            curl_setopt(self.handle, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_1_0)
        # end if
        if True == options_["blocking"]:
            curl_setopt(self.handle, CURLOPT_HEADERFUNCTION, Array(self, "stream_headers"))
            curl_setopt(self.handle, CURLOPT_WRITEFUNCTION, Array(self, "stream_body"))
            curl_setopt(self.handle, CURLOPT_BUFFERSIZE, Requests.BUFFER_SIZE)
        # end if
    # end def setup_handle
    #// 
    #// Process a response
    #// 
    #// @param string $response Response data from the body
    #// @param array $options Request options
    #// @return string HTTP response data including headers
    #//
    def process_response(self, response_=None, options_=None):
        
        
        if options_["blocking"] == False:
            fake_headers_ = ""
            options_["hooks"].dispatch("curl.after_request", Array(fake_headers_))
            return False
        # end if
        if options_["filename"] != False:
            php_fclose(self.stream_handle)
            self.headers = php_trim(self.headers)
        else:
            self.headers += response_
        # end if
        if curl_errno(self.handle):
            error_ = php_sprintf("cURL error %s: %s", curl_errno(self.handle), curl_error(self.handle))
            raise php_new_class("Requests_Exception", lambda : Requests_Exception(error_, "curlerror", self.handle))
        # end if
        self.info = curl_getinfo(self.handle)
        options_["hooks"].dispatch("curl.after_request", Array(self.headers, self.info))
        return self.headers
    # end def process_response
    #// 
    #// Collect the headers as they are received
    #// 
    #// @param resource $handle cURL resource
    #// @param string $headers Header string
    #// @return integer Length of provided header
    #//
    def stream_headers(self, handle_=None, headers_=None):
        
        
        #// Why do we do this? cURL will send both the final response and any
        #// interim responses, such as a 100 Continue. We don't need that.
        #// (We may want to keep this somewhere just in case)
        if self.done_headers:
            self.headers = ""
            self.done_headers = False
        # end if
        self.headers += headers_
        if headers_ == "\r\n":
            self.done_headers = True
        # end if
        return php_strlen(headers_)
    # end def stream_headers
    #// 
    #// Collect data as it's received
    #// 
    #// @since 1.6.1
    #// 
    #// @param resource $handle cURL resource
    #// @param string $data Body data
    #// @return integer Length of provided data
    #//
    def stream_body(self, handle_=None, data_=None):
        
        
        self.hooks.dispatch("request.progress", Array(data_, self.response_bytes, self.response_byte_limit))
        data_length_ = php_strlen(data_)
        #// Are we limiting the response size?
        if self.response_byte_limit:
            if self.response_bytes == self.response_byte_limit:
                #// Already at maximum, move on
                return data_length_
            # end if
            if self.response_bytes + data_length_ > self.response_byte_limit:
                #// Limit the length
                limited_length_ = self.response_byte_limit - self.response_bytes
                data_ = php_substr(data_, 0, limited_length_)
            # end if
        # end if
        if self.stream_handle:
            fwrite(self.stream_handle, data_)
        else:
            self.response_data += data_
        # end if
        self.response_bytes += php_strlen(data_)
        return data_length_
    # end def stream_body
    #// 
    #// Format a URL given GET data
    #// 
    #// @param string $url
    #// @param array|object $data Data to build query using, see {@see https://secure.php.net/http_build_query}
    #// @return string URL with data
    #//
    def format_get(self, url_=None, data_=None):
        
        
        if (not php_empty(lambda : data_)):
            url_parts_ = php_parse_url(url_)
            if php_empty(lambda : url_parts_["query"]):
                query_ = url_parts_["query"]
            else:
                query_ = url_parts_["query"]
            # end if
            query_ += "&" + http_build_query(data_, None, "&")
            query_ = php_trim(query_, "&")
            if php_empty(lambda : url_parts_["query"]):
                url_ += "?" + query_
            else:
                url_ = php_str_replace(url_parts_["query"], query_, url_)
            # end if
        # end if
        return url_
    # end def format_get
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
        
        if (not php_function_exists("curl_init")) or (not php_function_exists("curl_exec")):
            return False
        # end if
        #// If needed, check that our installed curl version supports SSL
        if (php_isset(lambda : capabilities_["ssl"])) and capabilities_["ssl"]:
            curl_version_ = curl_version()
            if (not CURL_VERSION_SSL & curl_version_["features"]):
                return False
            # end if
        # end if
        return True
    # end def test
# end class Requests_Transport_cURL
