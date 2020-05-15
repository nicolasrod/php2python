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
    headers = ""
    response_data = ""
    info = Array()
    version = Array()
    handle = Array()
    hooks = Array()
    done_headers = False
    stream_handle = Array()
    response_bytes = Array()
    response_byte_limit = Array()
    #// 
    #// Constructor
    #//
    def __init__(self):
        
        curl = curl_version()
        self.version = curl["version_number"]
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
    def request(self, url=None, headers=Array(), data=Array(), options=Array()):
        
        self.hooks = options["hooks"]
        self.setup_handle(url, headers, data, options)
        options["hooks"].dispatch("curl.before_send", Array(self.handle))
        if options["filename"] != False:
            self.stream_handle = fopen(options["filename"], "wb")
        # end if
        self.response_data = ""
        self.response_bytes = 0
        self.response_byte_limit = False
        if options["max_bytes"] != False:
            self.response_byte_limit = options["max_bytes"]
        # end if
        if (php_isset(lambda : options["verify"])):
            if options["verify"] == False:
                curl_setopt(self.handle, CURLOPT_SSL_VERIFYHOST, 0)
                curl_setopt(self.handle, CURLOPT_SSL_VERIFYPEER, 0)
            elif php_is_string(options["verify"]):
                curl_setopt(self.handle, CURLOPT_CAINFO, options["verify"])
            # end if
        # end if
        if (php_isset(lambda : options["verifyname"])) and options["verifyname"] == False:
            curl_setopt(self.handle, CURLOPT_SSL_VERIFYHOST, 0)
        # end if
        curl_exec(self.handle)
        response = self.response_data
        options["hooks"].dispatch("curl.after_send", Array())
        if curl_errno(self.handle) == 23 or curl_errno(self.handle) == 61:
            #// Reset encoding and try again
            curl_setopt(self.handle, CURLOPT_ENCODING, "none")
            self.response_data = ""
            self.response_bytes = 0
            curl_exec(self.handle)
            response = self.response_data
        # end if
        self.process_response(response, options)
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
    def request_multiple(self, requests=None, options=None):
        
        #// If you're not requesting, we can't get any responses ¯\_(ツ)_/¯
        if php_empty(lambda : requests):
            return Array()
        # end if
        multihandle = curl_multi_init()
        subrequests = Array()
        subhandles = Array()
        class_ = get_class(self)
        for id,request in requests:
            subrequests[id] = php_new_class(class_, lambda : {**locals(), **globals()}[class_]())
            subhandles[id] = subrequests[id].get_subrequest_handle(request["url"], request["headers"], request["data"], request["options"])
            request["options"]["hooks"].dispatch("curl.before_multi_add", Array(subhandles[id]))
            curl_multi_add_handle(multihandle, subhandles[id])
        # end for
        completed = 0
        responses = Array()
        request["options"]["hooks"].dispatch("curl.before_multi_exec", Array(multihandle))
        while True:
            active = False
            while True:
                status = curl_multi_exec(multihandle, active)
                
                if status == CURLM_CALL_MULTI_PERFORM:
                    break
                # end if
            # end while
            to_process = Array()
            #// Read the information as needed
            while True:
                done = curl_multi_info_read(multihandle)
                if not (done):
                    break
                # end if
                key = php_array_search(done["handle"], subhandles, True)
                if (not (php_isset(lambda : to_process[key]))):
                    to_process[key] = done
                # end if
            # end while
            #// Parse the finished requests before we start getting the new ones
            for key,done in to_process:
                options = requests[key]["options"]
                if CURLE_OK != done["result"]:
                    #// get error string for handle.
                    reason = curl_error(done["handle"])
                    exception = php_new_class("Requests_Exception_Transport_cURL", lambda : Requests_Exception_Transport_cURL(reason, Requests_Exception_Transport_cURL.EASY, done["handle"], done["result"]))
                    responses[key] = exception
                    options["hooks"].dispatch("transport.internal.parse_error", Array(responses[key], requests[key]))
                else:
                    responses[key] = subrequests[key].process_response(subrequests[key].response_data, options)
                    options["hooks"].dispatch("transport.internal.parse_response", Array(responses[key], requests[key]))
                # end if
                curl_multi_remove_handle(multihandle, done["handle"])
                curl_close(done["handle"])
                if (not php_is_string(responses[key])):
                    options["hooks"].dispatch("multiple.request.complete", Array(responses[key], key))
                # end if
                completed += 1
            # end for
            
            if active or completed < php_count(subrequests):
                break
            # end if
        # end while
        request["options"]["hooks"].dispatch("curl.after_multi_exec", Array(multihandle))
        curl_multi_close(multihandle)
        return responses
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
    def get_subrequest_handle(self, url=None, headers=None, data=None, options=None):
        
        self.setup_handle(url, headers, data, options)
        if options["filename"] != False:
            self.stream_handle = fopen(options["filename"], "wb")
        # end if
        self.response_data = ""
        self.response_bytes = 0
        self.response_byte_limit = False
        if options["max_bytes"] != False:
            self.response_byte_limit = options["max_bytes"]
        # end if
        self.hooks = options["hooks"]
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
    def setup_handle(self, url=None, headers=None, data=None, options=None):
        
        options["hooks"].dispatch("curl.before_request", Array(self.handle))
        #// Force closing the connection for old versions of cURL (<7.22).
        if (not (php_isset(lambda : headers["Connection"]))):
            headers["Connection"] = "close"
        # end if
        headers = Requests.flatten(headers)
        if (not php_empty(lambda : data)):
            data_format = options["data_format"]
            if data_format == "query":
                url = self.format_get(url, data)
                data = ""
            elif (not php_is_string(data)):
                data = http_build_query(data, None, "&")
            # end if
        # end if
        for case in Switch(options["type"]):
            if case(Requests.POST):
                curl_setopt(self.handle, CURLOPT_POST, True)
                curl_setopt(self.handle, CURLOPT_POSTFIELDS, data)
                break
            # end if
            if case(Requests.HEAD):
                curl_setopt(self.handle, CURLOPT_CUSTOMREQUEST, options["type"])
                curl_setopt(self.handle, CURLOPT_NOBODY, True)
                break
            # end if
            if case(Requests.TRACE):
                curl_setopt(self.handle, CURLOPT_CUSTOMREQUEST, options["type"])
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
                curl_setopt(self.handle, CURLOPT_CUSTOMREQUEST, options["type"])
                if (not php_empty(lambda : data)):
                    curl_setopt(self.handle, CURLOPT_POSTFIELDS, data)
                # end if
            # end if
        # end for
        #// cURL requires a minimum timeout of 1 second when using the system
        #// DNS resolver, as it uses `alarm()`, which is second resolution only.
        #// There's no way to detect which DNS resolver is being used from our
        #// end, so we need to round up regardless of the supplied timeout.
        #// 
        #// https://github.com/curl/curl/blob/4f45240bc84a9aa648c8f7243be7b79e9f9323a5/lib/hostip.c#L606-L609
        timeout = php_max(options["timeout"], 1)
        if php_is_int(timeout) or self.version < self.CURL_7_16_2:
            curl_setopt(self.handle, CURLOPT_TIMEOUT, ceil(timeout))
        else:
            curl_setopt(self.handle, CURLOPT_TIMEOUT_MS, round(timeout * 1000))
        # end if
        if php_is_int(options["connect_timeout"]) or self.version < self.CURL_7_16_2:
            curl_setopt(self.handle, CURLOPT_CONNECTTIMEOUT, ceil(options["connect_timeout"]))
        else:
            curl_setopt(self.handle, CURLOPT_CONNECTTIMEOUT_MS, round(options["connect_timeout"] * 1000))
        # end if
        curl_setopt(self.handle, CURLOPT_URL, url)
        curl_setopt(self.handle, CURLOPT_REFERER, url)
        curl_setopt(self.handle, CURLOPT_USERAGENT, options["useragent"])
        if (not php_empty(lambda : headers)):
            curl_setopt(self.handle, CURLOPT_HTTPHEADER, headers)
        # end if
        if options["protocol_version"] == 1.1:
            curl_setopt(self.handle, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_1_1)
        else:
            curl_setopt(self.handle, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_1_0)
        # end if
        if True == options["blocking"]:
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
    def process_response(self, response=None, options=None):
        
        if options["blocking"] == False:
            fake_headers = ""
            options["hooks"].dispatch("curl.after_request", Array(fake_headers))
            return False
        # end if
        if options["filename"] != False:
            php_fclose(self.stream_handle)
            self.headers = php_trim(self.headers)
        else:
            self.headers += response
        # end if
        if curl_errno(self.handle):
            error = php_sprintf("cURL error %s: %s", curl_errno(self.handle), curl_error(self.handle))
            raise php_new_class("Requests_Exception", lambda : Requests_Exception(error, "curlerror", self.handle))
        # end if
        self.info = curl_getinfo(self.handle)
        options["hooks"].dispatch("curl.after_request", Array(self.headers, self.info))
        return self.headers
    # end def process_response
    #// 
    #// Collect the headers as they are received
    #// 
    #// @param resource $handle cURL resource
    #// @param string $headers Header string
    #// @return integer Length of provided header
    #//
    def stream_headers(self, handle=None, headers=None):
        
        #// Why do we do this? cURL will send both the final response and any
        #// interim responses, such as a 100 Continue. We don't need that.
        #// (We may want to keep this somewhere just in case)
        if self.done_headers:
            self.headers = ""
            self.done_headers = False
        # end if
        self.headers += headers
        if headers == "\r\n":
            self.done_headers = True
        # end if
        return php_strlen(headers)
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
    def stream_body(self, handle=None, data=None):
        
        self.hooks.dispatch("request.progress", Array(data, self.response_bytes, self.response_byte_limit))
        data_length = php_strlen(data)
        #// Are we limiting the response size?
        if self.response_byte_limit:
            if self.response_bytes == self.response_byte_limit:
                #// Already at maximum, move on
                return data_length
            # end if
            if self.response_bytes + data_length > self.response_byte_limit:
                #// Limit the length
                limited_length = self.response_byte_limit - self.response_bytes
                data = php_substr(data, 0, limited_length)
            # end if
        # end if
        if self.stream_handle:
            fwrite(self.stream_handle, data)
        else:
            self.response_data += data
        # end if
        self.response_bytes += php_strlen(data)
        return data_length
    # end def stream_body
    #// 
    #// Format a URL given GET data
    #// 
    #// @param string $url
    #// @param array|object $data Data to build query using, see {@see https://secure.php.net/http_build_query}
    #// @return string URL with data
    #//
    def format_get(self, url=None, data=None):
        
        if (not php_empty(lambda : data)):
            url_parts = php_parse_url(url)
            if php_empty(lambda : url_parts["query"]):
                query = url_parts["query"]
            else:
                query = url_parts["query"]
            # end if
            query += "&" + http_build_query(data, None, "&")
            query = php_trim(query, "&")
            if php_empty(lambda : url_parts["query"]):
                url += "?" + query
            else:
                url = php_str_replace(url_parts["query"], query, url)
            # end if
        # end if
        return url
    # end def format_get
    #// 
    #// Whether this transport is valid
    #// 
    #// @codeCoverageIgnore
    #// @return boolean True if the transport is valid, false otherwise.
    #//
    @classmethod
    def test(self, capabilities=Array()):
        
        if (not php_function_exists("curl_init")) or (not php_function_exists("curl_exec")):
            return False
        # end if
        #// If needed, check that our installed curl version supports SSL
        if (php_isset(lambda : capabilities["ssl"])) and capabilities["ssl"]:
            curl_version = curl_version()
            if (not CURL_VERSION_SSL & curl_version["features"]):
                return False
            # end if
        # end if
        return True
    # end def test
# end class Requests_Transport_cURL
