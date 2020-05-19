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
#// REST API: WP_REST_Request class
#// 
#// @package WordPress
#// @subpackage REST_API
#// @since 4.4.0
#// 
#// 
#// Core class used to implement a REST request object.
#// 
#// Contains data from the request, to be passed to the callback.
#// 
#// Note: This implements ArrayAccess, and acts as an array of parameters when
#// used in that manner. It does not use ArrayObject (as we cannot rely on SPL),
#// so be aware it may have non-array behaviour in some cases.
#// 
#// Note: When using features provided by ArrayAccess, be aware that WordPress deliberately
#// does not distinguish between arguments of the same name for different request methods.
#// For instance, in a request with `GET id=1` and `POST id=2`, `$request['id']` will equal
#// 2 (`POST`) not 1 (`GET`). For more precision between request methods, use
#// WP_REST_Request::get_body_params(), WP_REST_Request::get_url_params(), etc.
#// 
#// @since 4.4.0
#// 
#// @link https://www.php.net/manual/en/class.arrayaccess.php
#//
class WP_REST_Request(ArrayAccess):
    #// 
    #// HTTP method.
    #// 
    #// @since 4.4.0
    #// @var string
    #//
    method = ""
    #// 
    #// Parameters passed to the request.
    #// 
    #// These typically come from the `$_GET`, `$_POST` and `$_FILES`
    #// superglobals when being created from the global scope.
    #// 
    #// @since 4.4.0
    #// @var array Contains GET, POST and FILES keys mapping to arrays of data.
    #//
    params = Array()
    #// 
    #// HTTP headers for the request.
    #// 
    #// @since 4.4.0
    #// @var array Map of key to value. Key is always lowercase, as per HTTP specification.
    #//
    headers = Array()
    #// 
    #// Body data.
    #// 
    #// @since 4.4.0
    #// @var string Binary data from the request.
    #//
    body = None
    #// 
    #// Route matched for the request.
    #// 
    #// @since 4.4.0
    #// @var string
    #//
    route = Array()
    #// 
    #// Attributes (options) for the route that was matched.
    #// 
    #// This is the options array used when the route was registered, typically
    #// containing the callback as well as the valid methods for the route.
    #// 
    #// @since 4.4.0
    #// @var array Attributes for the request.
    #//
    attributes = Array()
    #// 
    #// Used to determine if the JSON data has been parsed yet.
    #// 
    #// Allows lazy-parsing of JSON data where possible.
    #// 
    #// @since 4.4.0
    #// @var bool
    #//
    parsed_json = False
    #// 
    #// Used to determine if the body data has been parsed yet.
    #// 
    #// @since 4.4.0
    #// @var bool
    #//
    parsed_body = False
    #// 
    #// Constructor.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $method     Optional. Request method. Default empty.
    #// @param string $route      Optional. Request route. Default empty.
    #// @param array  $attributes Optional. Request attributes. Default empty array.
    #//
    def __init__(self, method_="", route_="", attributes_=None):
        if attributes_ is None:
            attributes_ = Array()
        # end if
        
        self.params = Array({"URL": Array(), "GET": Array(), "POST": Array(), "FILES": Array(), "JSON": None, "defaults": Array()})
        self.set_method(method_)
        self.set_route(route_)
        self.set_attributes(attributes_)
    # end def __init__
    #// 
    #// Retrieves the HTTP method for the request.
    #// 
    #// @since 4.4.0
    #// 
    #// @return string HTTP method.
    #//
    def get_method(self):
        
        
        return self.method
    # end def get_method
    #// 
    #// Sets HTTP method for the request.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $method HTTP method.
    #//
    def set_method(self, method_=None):
        
        
        self.method = php_strtoupper(method_)
    # end def set_method
    #// 
    #// Retrieves all headers from the request.
    #// 
    #// @since 4.4.0
    #// 
    #// @return array Map of key to value. Key is always lowercase, as per HTTP specification.
    #//
    def get_headers(self):
        
        
        return self.headers
    # end def get_headers
    #// 
    #// Canonicalizes the header name.
    #// 
    #// Ensures that header names are always treated the same regardless of
    #// source. Header names are always case insensitive.
    #// 
    #// Note that we treat `-` (dashes) and `_` (underscores) as the same
    #// character, as per header parsing rules in both Apache and nginx.
    #// 
    #// @link https://stackoverflow.com/q/18185366
    #// @link https://www.nginx.com/resources/wiki/start/topics/tutorials/config_pitfalls/#missing-disappearing-http-headers
    #// @link https://nginx.org/en/docs/http/ngx_http_core_module.html#underscores_in_headers
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $key Header name.
    #// @return string Canonicalized name.
    #//
    @classmethod
    def canonicalize_header_name(self, key_=None):
        
        
        key_ = php_strtolower(key_)
        key_ = php_str_replace("-", "_", key_)
        return key_
    # end def canonicalize_header_name
    #// 
    #// Retrieves the given header from the request.
    #// 
    #// If the header has multiple values, they will be concatenated with a comma
    #// as per the HTTP specification. Be aware that some non-compliant headers
    #// (notably cookie headers) cannot be joined this way.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $key Header name, will be canonicalized to lowercase.
    #// @return string|null String value if set, null otherwise.
    #//
    def get_header(self, key_=None):
        
        
        key_ = self.canonicalize_header_name(key_)
        if (not (php_isset(lambda : self.headers[key_]))):
            return None
        # end if
        return php_implode(",", self.headers[key_])
    # end def get_header
    #// 
    #// Retrieves header values from the request.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $key Header name, will be canonicalized to lowercase.
    #// @return array|null List of string values if set, null otherwise.
    #//
    def get_header_as_array(self, key_=None):
        
        
        key_ = self.canonicalize_header_name(key_)
        if (not (php_isset(lambda : self.headers[key_]))):
            return None
        # end if
        return self.headers[key_]
    # end def get_header_as_array
    #// 
    #// Sets the header on request.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $key   Header name.
    #// @param string $value Header value, or list of values.
    #//
    def set_header(self, key_=None, value_=None):
        
        
        key_ = self.canonicalize_header_name(key_)
        value_ = value_
        self.headers[key_] = value_
    # end def set_header
    #// 
    #// Appends a header value for the given header.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $key   Header name.
    #// @param string $value Header value, or list of values.
    #//
    def add_header(self, key_=None, value_=None):
        
        
        key_ = self.canonicalize_header_name(key_)
        value_ = value_
        if (not (php_isset(lambda : self.headers[key_]))):
            self.headers[key_] = Array()
        # end if
        self.headers[key_] = php_array_merge(self.headers[key_], value_)
    # end def add_header
    #// 
    #// Removes all values for a header.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $key Header name.
    #//
    def remove_header(self, key_=None):
        
        
        key_ = self.canonicalize_header_name(key_)
        self.headers[key_] = None
    # end def remove_header
    #// 
    #// Sets headers on the request.
    #// 
    #// @since 4.4.0
    #// 
    #// @param array $headers  Map of header name to value.
    #// @param bool  $override If true, replace the request's headers. Otherwise, merge with existing.
    #//
    def set_headers(self, headers_=None, override_=None):
        if override_ is None:
            override_ = True
        # end if
        
        if True == override_:
            self.headers = Array()
        # end if
        for key_,value_ in headers_.items():
            self.set_header(key_, value_)
        # end for
    # end def set_headers
    #// 
    #// Retrieves the content-type of the request.
    #// 
    #// @since 4.4.0
    #// 
    #// @return array|null Map containing 'value' and 'parameters' keys
    #// or null when no valid content-type header was
    #// available.
    #//
    def get_content_type(self):
        
        
        value_ = self.get_header("content-type")
        if php_empty(lambda : value_):
            return None
        # end if
        parameters_ = ""
        if php_strpos(value_, ";"):
            value_, parameters_ = php_explode(";", value_, 2)
        # end if
        value_ = php_strtolower(value_)
        if False == php_strpos(value_, "/"):
            return None
        # end if
        #// Parse type and subtype out.
        type_, subtype_ = php_explode("/", value_, 2)
        data_ = php_compact("value_", "type_", "subtype_", "parameters_")
        data_ = php_array_map("trim", data_)
        return data_
    # end def get_content_type
    #// 
    #// Retrieves the parameter priority order.
    #// 
    #// Used when checking parameters in get_param().
    #// 
    #// @since 4.4.0
    #// 
    #// @return string[] Array of types to check, in order of priority.
    #//
    def get_parameter_order(self):
        
        
        order_ = Array()
        content_type_ = self.get_content_type()
        if (php_isset(lambda : content_type_["value"])) and "application/json" == content_type_["value"]:
            order_[-1] = "JSON"
        # end if
        self.parse_json_params()
        #// Ensure we parse the body data.
        body_ = self.get_body()
        if "POST" != self.method and (not php_empty(lambda : body_)):
            self.parse_body_params()
        # end if
        accepts_body_data_ = Array("POST", "PUT", "PATCH", "DELETE")
        if php_in_array(self.method, accepts_body_data_, True):
            order_[-1] = "POST"
        # end if
        order_[-1] = "GET"
        order_[-1] = "URL"
        order_[-1] = "defaults"
        #// 
        #// Filters the parameter order.
        #// 
        #// The order affects which parameters are checked when using get_param() and family.
        #// This acts similarly to PHP's `request_order` setting.
        #// 
        #// @since 4.4.0
        #// 
        #// @param string[]        $order Array of types to check, in order of priority.
        #// @param WP_REST_Request $this  The request object.
        #//
        return apply_filters("rest_request_parameter_order", order_, self)
    # end def get_parameter_order
    #// 
    #// Retrieves a parameter from the request.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $key Parameter name.
    #// @return mixed|null Value if set, null otherwise.
    #//
    def get_param(self, key_=None):
        
        
        order_ = self.get_parameter_order()
        for type_ in order_:
            #// Determine if we have the parameter for this type.
            if (php_isset(lambda : self.params[type_][key_])):
                return self.params[type_][key_]
            # end if
        # end for
        return None
    # end def get_param
    #// 
    #// Checks if a parameter exists in the request.
    #// 
    #// This allows distinguishing between an omitted parameter,
    #// and a parameter specifically set to null.
    #// 
    #// @since 5.3.0
    #// 
    #// @param string $key Parameter name.
    #// 
    #// @return bool True if a param exists for the given key.
    #//
    def has_param(self, key_=None):
        
        
        order_ = self.get_parameter_order()
        for type_ in order_:
            if php_array_key_exists(key_, self.params[type_]):
                return True
            # end if
        # end for
        return False
    # end def has_param
    #// 
    #// Sets a parameter on the request.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $key   Parameter name.
    #// @param mixed  $value Parameter value.
    #//
    def set_param(self, key_=None, value_=None):
        
        
        order_ = self.get_parameter_order()
        self.params[order_[0]][key_] = value_
    # end def set_param
    #// 
    #// Retrieves merged parameters from the request.
    #// 
    #// The equivalent of get_param(), but returns all parameters for the request.
    #// Handles merging all the available values into a single array.
    #// 
    #// @since 4.4.0
    #// 
    #// @return array Map of key to value.
    #//
    def get_params(self):
        
        
        order_ = self.get_parameter_order()
        order_ = php_array_reverse(order_, True)
        params_ = Array()
        for type_ in order_:
            #// array_merge() / the "+" operator will mess up
            #// numeric keys, so instead do a manual foreach.
            for key_,value_ in self.params[type_].items():
                params_[key_] = value_
            # end for
        # end for
        return params_
    # end def get_params
    #// 
    #// Retrieves parameters from the route itself.
    #// 
    #// These are parsed from the URL using the regex.
    #// 
    #// @since 4.4.0
    #// 
    #// @return array Parameter map of key to value.
    #//
    def get_url_params(self):
        
        
        return self.params["URL"]
    # end def get_url_params
    #// 
    #// Sets parameters from the route.
    #// 
    #// Typically, this is set after parsing the URL.
    #// 
    #// @since 4.4.0
    #// 
    #// @param array $params Parameter map of key to value.
    #//
    def set_url_params(self, params_=None):
        
        
        self.params["URL"] = params_
    # end def set_url_params
    #// 
    #// Retrieves parameters from the query string.
    #// 
    #// These are the parameters you'd typically find in `$_GET`.
    #// 
    #// @since 4.4.0
    #// 
    #// @return array Parameter map of key to value
    #//
    def get_query_params(self):
        
        
        return self.params["GET"]
    # end def get_query_params
    #// 
    #// Sets parameters from the query string.
    #// 
    #// Typically, this is set from `$_GET`.
    #// 
    #// @since 4.4.0
    #// 
    #// @param array $params Parameter map of key to value.
    #//
    def set_query_params(self, params_=None):
        
        
        self.params["GET"] = params_
    # end def set_query_params
    #// 
    #// Retrieves parameters from the body.
    #// 
    #// These are the parameters you'd typically find in `$_POST`.
    #// 
    #// @since 4.4.0
    #// 
    #// @return array Parameter map of key to value.
    #//
    def get_body_params(self):
        
        
        return self.params["POST"]
    # end def get_body_params
    #// 
    #// Sets parameters from the body.
    #// 
    #// Typically, this is set from `$_POST`.
    #// 
    #// @since 4.4.0
    #// 
    #// @param array $params Parameter map of key to value.
    #//
    def set_body_params(self, params_=None):
        
        
        self.params["POST"] = params_
    # end def set_body_params
    #// 
    #// Retrieves multipart file parameters from the body.
    #// 
    #// These are the parameters you'd typically find in `$_FILES`.
    #// 
    #// @since 4.4.0
    #// 
    #// @return array Parameter map of key to value
    #//
    def get_file_params(self):
        
        
        return self.params["FILES"]
    # end def get_file_params
    #// 
    #// Sets multipart file parameters from the body.
    #// 
    #// Typically, this is set from `$_FILES`.
    #// 
    #// @since 4.4.0
    #// 
    #// @param array $params Parameter map of key to value.
    #//
    def set_file_params(self, params_=None):
        
        
        self.params["FILES"] = params_
    # end def set_file_params
    #// 
    #// Retrieves the default parameters.
    #// 
    #// These are the parameters set in the route registration.
    #// 
    #// @since 4.4.0
    #// 
    #// @return array Parameter map of key to value
    #//
    def get_default_params(self):
        
        
        return self.params["defaults"]
    # end def get_default_params
    #// 
    #// Sets default parameters.
    #// 
    #// These are the parameters set in the route registration.
    #// 
    #// @since 4.4.0
    #// 
    #// @param array $params Parameter map of key to value.
    #//
    def set_default_params(self, params_=None):
        
        
        self.params["defaults"] = params_
    # end def set_default_params
    #// 
    #// Retrieves the request body content.
    #// 
    #// @since 4.4.0
    #// 
    #// @return string Binary data from the request body.
    #//
    def get_body(self):
        
        
        return self.body
    # end def get_body
    #// 
    #// Sets body content.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $data Binary data from the request body.
    #//
    def set_body(self, data_=None):
        
        
        self.body = data_
        #// Enable lazy parsing.
        self.parsed_json = False
        self.parsed_body = False
        self.params["JSON"] = None
    # end def set_body
    #// 
    #// Retrieves the parameters from a JSON-formatted body.
    #// 
    #// @since 4.4.0
    #// 
    #// @return array Parameter map of key to value.
    #//
    def get_json_params(self):
        
        
        #// Ensure the parameters have been parsed out.
        self.parse_json_params()
        return self.params["JSON"]
    # end def get_json_params
    #// 
    #// Parses the JSON parameters.
    #// 
    #// Avoids parsing the JSON data until we need to access it.
    #// 
    #// @since 4.4.0
    #// @since 4.7.0 Returns error instance if value cannot be decoded.
    #// @return true|WP_Error True if the JSON data was passed or no JSON data was provided, WP_Error if invalid JSON was passed.
    #//
    def parse_json_params(self):
        
        
        if self.parsed_json:
            return True
        # end if
        self.parsed_json = True
        #// Check that we actually got JSON.
        content_type_ = self.get_content_type()
        if php_empty(lambda : content_type_) or "application/json" != content_type_["value"]:
            return True
        # end if
        body_ = self.get_body()
        if php_empty(lambda : body_):
            return True
        # end if
        params_ = php_json_decode(body_, True)
        #// 
        #// Check for a parsing error.
        #//
        if None == params_ and JSON_ERROR_NONE != php_json_last_error():
            #// Ensure subsequent calls receive error instance.
            self.parsed_json = False
            error_data_ = Array({"status": WP_Http.BAD_REQUEST, "json_error_code": php_json_last_error(), "json_error_message": json_last_error_msg()})
            return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_json", __("Invalid JSON body passed."), error_data_))
        # end if
        self.params["JSON"] = params_
        return True
    # end def parse_json_params
    #// 
    #// Parses the request body parameters.
    #// 
    #// Parses out URL-encoded bodies for request methods that aren't supported
    #// natively by PHP. In PHP 5.x, only POST has these parsed automatically.
    #// 
    #// @since 4.4.0
    #//
    def parse_body_params(self):
        
        
        if self.parsed_body:
            return
        # end if
        self.parsed_body = True
        #// 
        #// Check that we got URL-encoded. Treat a missing content-type as
        #// URL-encoded for maximum compatibility.
        #//
        content_type_ = self.get_content_type()
        if (not php_empty(lambda : content_type_)) and "application/x-www-form-urlencoded" != content_type_["value"]:
            return
        # end if
        parse_str(self.get_body(), params_)
        #// 
        #// Add to the POST parameters stored internally. If a user has already
        #// set these manually (via `set_body_params`), don't override them.
        #//
        self.params["POST"] = php_array_merge(params_, self.params["POST"])
    # end def parse_body_params
    #// 
    #// Retrieves the route that matched the request.
    #// 
    #// @since 4.4.0
    #// 
    #// @return string Route matching regex.
    #//
    def get_route(self):
        
        
        return self.route
    # end def get_route
    #// 
    #// Sets the route that matched the request.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $route Route matching regex.
    #//
    def set_route(self, route_=None):
        
        
        self.route = route_
    # end def set_route
    #// 
    #// Retrieves the attributes for the request.
    #// 
    #// These are the options for the route that was matched.
    #// 
    #// @since 4.4.0
    #// 
    #// @return array Attributes for the request.
    #//
    def get_attributes(self):
        
        
        return self.attributes
    # end def get_attributes
    #// 
    #// Sets the attributes for the request.
    #// 
    #// @since 4.4.0
    #// 
    #// @param array $attributes Attributes for the request.
    #//
    def set_attributes(self, attributes_=None):
        
        
        self.attributes = attributes_
    # end def set_attributes
    #// 
    #// Sanitizes (where possible) the params on the request.
    #// 
    #// This is primarily based off the sanitize_callback param on each registered
    #// argument.
    #// 
    #// @since 4.4.0
    #// 
    #// @return true|WP_Error True if parameters were sanitized, WP_Error if an error occurred during sanitization.
    #//
    def sanitize_params(self):
        
        
        attributes_ = self.get_attributes()
        #// No arguments set, skip sanitizing.
        if php_empty(lambda : attributes_["args"]):
            return True
        # end if
        order_ = self.get_parameter_order()
        invalid_params_ = Array()
        for type_ in order_:
            if php_empty(lambda : self.params[type_]):
                continue
            # end if
            for key_,value_ in self.params[type_].items():
                if (not (php_isset(lambda : attributes_["args"][key_]))):
                    continue
                # end if
                param_args_ = attributes_["args"][key_]
                #// If the arg has a type but no sanitize_callback attribute, default to rest_parse_request_arg.
                if (not php_array_key_exists("sanitize_callback", param_args_)) and (not php_empty(lambda : param_args_["type"])):
                    param_args_["sanitize_callback"] = "rest_parse_request_arg"
                # end if
                #// If there's still no sanitize_callback, nothing to do here.
                if php_empty(lambda : param_args_["sanitize_callback"]):
                    continue
                # end if
                sanitized_value_ = php_call_user_func(param_args_["sanitize_callback"], value_, self, key_)
                if is_wp_error(sanitized_value_):
                    invalid_params_[key_] = sanitized_value_.get_error_message()
                else:
                    self.params[type_][key_] = sanitized_value_
                # end if
            # end for
        # end for
        if invalid_params_:
            return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("Invalid parameter(s): %s"), php_implode(", ", php_array_keys(invalid_params_))), Array({"status": 400, "params": invalid_params_})))
        # end if
        return True
    # end def sanitize_params
    #// 
    #// Checks whether this request is valid according to its attributes.
    #// 
    #// @since 4.4.0
    #// 
    #// @return bool|WP_Error True if there are no parameters to validate or if all pass validation,
    #// WP_Error if required parameters are missing.
    #//
    def has_valid_params(self):
        
        
        #// If JSON data was passed, check for errors.
        json_error_ = self.parse_json_params()
        if is_wp_error(json_error_):
            return json_error_
        # end if
        attributes_ = self.get_attributes()
        required_ = Array()
        #// No arguments set, skip validation.
        if php_empty(lambda : attributes_["args"]):
            return True
        # end if
        for key_,arg_ in attributes_["args"].items():
            param_ = self.get_param(key_)
            if (php_isset(lambda : arg_["required"])) and True == arg_["required"] and None == param_:
                required_[-1] = key_
            # end if
        # end for
        if (not php_empty(lambda : required_)):
            return php_new_class("WP_Error", lambda : WP_Error("rest_missing_callback_param", php_sprintf(__("Missing parameter(s): %s"), php_implode(", ", required_)), Array({"status": 400, "params": required_})))
        # end if
        #// 
        #// Check the validation callbacks for each registered arg.
        #// 
        #// This is done after required checking as required checking is cheaper.
        #//
        invalid_params_ = Array()
        for key_,arg_ in attributes_["args"].items():
            param_ = self.get_param(key_)
            if None != param_ and (not php_empty(lambda : arg_["validate_callback"])):
                valid_check_ = php_call_user_func(arg_["validate_callback"], param_, self, key_)
                if False == valid_check_:
                    invalid_params_[key_] = __("Invalid parameter.")
                # end if
                if is_wp_error(valid_check_):
                    invalid_params_[key_] = valid_check_.get_error_message()
                # end if
            # end if
        # end for
        if invalid_params_:
            return php_new_class("WP_Error", lambda : WP_Error("rest_invalid_param", php_sprintf(__("Invalid parameter(s): %s"), php_implode(", ", php_array_keys(invalid_params_))), Array({"status": 400, "params": invalid_params_})))
        # end if
        return True
    # end def has_valid_params
    #// 
    #// Checks if a parameter is set.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $offset Parameter name.
    #// @return bool Whether the parameter is set.
    #//
    def offsetexists(self, offset_=None):
        
        
        order_ = self.get_parameter_order()
        for type_ in order_:
            if (php_isset(lambda : self.params[type_][offset_])):
                return True
            # end if
        # end for
        return False
    # end def offsetexists
    #// 
    #// Retrieves a parameter from the request.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $offset Parameter name.
    #// @return mixed|null Value if set, null otherwise.
    #//
    def offsetget(self, offset_=None):
        
        
        return self.get_param(offset_)
    # end def offsetget
    #// 
    #// Sets a parameter on the request.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $offset Parameter name.
    #// @param mixed  $value  Parameter value.
    #//
    def offsetset(self, offset_=None, value_=None):
        
        
        self.set_param(offset_, value_)
    # end def offsetset
    #// 
    #// Removes a parameter from the request.
    #// 
    #// @since 4.4.0
    #// 
    #// @param string $offset Parameter name.
    #//
    def offsetunset(self, offset_=None):
        
        
        order_ = self.get_parameter_order()
        #// Remove the offset from every group.
        for type_ in order_:
            self.params[type_][offset_] = None
        # end for
    # end def offsetunset
    #// 
    #// Retrieves a WP_REST_Request object from a full URL.
    #// 
    #// @since 4.5.0
    #// 
    #// @param string $url URL with protocol, domain, path and query args.
    #// @return WP_REST_Request|false WP_REST_Request object on success, false on failure.
    #//
    @classmethod
    def from_url(self, url_=None):
        
        
        bits_ = php_parse_url(url_)
        query_params_ = Array()
        if (not php_empty(lambda : bits_["query"])):
            wp_parse_str(bits_["query"], query_params_)
        # end if
        api_root_ = rest_url()
        if get_option("permalink_structure") and 0 == php_strpos(url_, api_root_):
            #// Pretty permalinks on, and URL is under the API root.
            api_url_part_ = php_substr(url_, php_strlen(untrailingslashit(api_root_)))
            route_ = php_parse_url(api_url_part_, PHP_URL_PATH)
        elif (not php_empty(lambda : query_params_["rest_route"])):
            #// ?rest_route=... set directly.
            route_ = query_params_["rest_route"]
            query_params_["rest_route"] = None
        # end if
        request_ = False
        if (not php_empty(lambda : route_)):
            request_ = php_new_class("WP_REST_Request", lambda : WP_REST_Request("GET", route_))
            request_.set_query_params(query_params_)
        # end if
        #// 
        #// Filters the request generated from a URL.
        #// 
        #// @since 4.5.0
        #// 
        #// @param WP_REST_Request|false $request Generated request object, or false if URL
        #// could not be parsed.
        #// @param string                $url     URL the request was generated from.
        #//
        return apply_filters("rest_request_from_url", request_, url_)
    # end def from_url
# end class WP_REST_Request
