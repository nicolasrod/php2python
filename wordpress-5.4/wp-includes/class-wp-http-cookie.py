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
#// HTTP API: WP_Http_Cookie class
#// 
#// @package WordPress
#// @subpackage HTTP
#// @since 4.4.0
#// 
#// 
#// Core class used to encapsulate a single cookie object for internal use.
#// 
#// Returned cookies are represented using this class, and when cookies are set, if they are not
#// already a WP_Http_Cookie() object, then they are turned into one.
#// 
#// @todo The WordPress convention is to use underscores instead of camelCase for function and method
#// names. Need to switch to use underscores instead for the methods.
#// 
#// @since 2.8.0
#//
class WP_Http_Cookie():
    #// 
    #// Cookie name.
    #// 
    #// @since 2.8.0
    #// @var string
    #//
    name = Array()
    #// 
    #// Cookie value.
    #// 
    #// @since 2.8.0
    #// @var string
    #//
    value = Array()
    #// 
    #// When the cookie expires. Unix timestamp or formatted date.
    #// 
    #// @since 2.8.0
    #// @var string|int|null
    #//
    expires = Array()
    #// 
    #// Cookie URL path.
    #// 
    #// @since 2.8.0
    #// @var string
    #//
    path = Array()
    #// 
    #// Cookie Domain.
    #// 
    #// @since 2.8.0
    #// @var string
    #//
    domain = Array()
    #// 
    #// host-only flag.
    #// 
    #// @since 5.2.0
    #// @var bool
    #//
    host_only = Array()
    #// 
    #// Sets up this cookie object.
    #// 
    #// The parameter $data should be either an associative array containing the indices names below
    #// or a header string detailing it.
    #// 
    #// @since 2.8.0
    #// @since 5.2.0 Added `host_only` to the `$data` parameter.
    #// 
    #// @param string|array $data {
    #// Raw cookie data as header string or data array.
    #// 
    #// @type string          $name      Cookie name.
    #// @type mixed           $value     Value. Should NOT already be urlencoded.
    #// @type string|int|null $expires   Optional. Unix timestamp or formatted date. Default null.
    #// @type string          $path      Optional. Path. Default '/'.
    #// @type string          $domain    Optional. Domain. Default host of parsed $requested_url.
    #// @type int             $port      Optional. Port. Default null.
    #// @type bool            $host_only Optional. host-only storage flag. Default true.
    #// }
    #// @param string       $requested_url The URL which the cookie was set on, used for default $domain
    #// and $port values.
    #//
    def __init__(self, data_=None, requested_url_=""):
        
        
        if requested_url_:
            arrURL_ = php_no_error(lambda: php_parse_url(requested_url_))
        # end if
        if (php_isset(lambda : arrURL_["host"])):
            self.domain = arrURL_["host"]
        # end if
        self.path = arrURL_["path"] if (php_isset(lambda : arrURL_["path"])) else "/"
        if "/" != php_substr(self.path, -1):
            self.path = php_dirname(self.path) + "/"
        # end if
        if php_is_string(data_):
            #// Assume it's a header string direct from a previous request.
            pairs_ = php_explode(";", data_)
            #// Special handling for first pair; name=value. Also be careful of "=" in value.
            name_ = php_trim(php_substr(pairs_[0], 0, php_strpos(pairs_[0], "=")))
            value_ = php_substr(pairs_[0], php_strpos(pairs_[0], "=") + 1)
            self.name = name_
            self.value = urldecode(value_)
            #// Removes name=value from items.
            php_array_shift(pairs_)
            #// Set everything else as a property.
            for pair_ in pairs_:
                pair_ = php_rtrim(pair_)
                #// Handle the cookie ending in ; which results in a empty final pair.
                if php_empty(lambda : pair_):
                    continue
                # end if
                key_, val_ = php_explode("=", pair_) if php_strpos(pair_, "=") else Array(pair_, "")
                key_ = php_strtolower(php_trim(key_))
                if "expires" == key_:
                    val_ = strtotime(val_)
                # end if
                self.key_ = val_
            # end for
        else:
            if (not (php_isset(lambda : data_["name"]))):
                return
            # end if
            #// Set properties based directly on parameters.
            for field_ in Array("name", "value", "path", "domain", "port", "host_only"):
                if (php_isset(lambda : data_[field_])):
                    self.field_ = data_[field_]
                # end if
            # end for
            if (php_isset(lambda : data_["expires"])):
                self.expires = data_["expires"] if php_is_int(data_["expires"]) else strtotime(data_["expires"])
            else:
                self.expires = None
            # end if
        # end if
    # end def __init__
    #// 
    #// Confirms that it's OK to send this cookie to the URL checked against.
    #// 
    #// Decision is based on RFC 2109/2965, so look there for details on validity.
    #// 
    #// @since 2.8.0
    #// 
    #// @param string $url URL you intend to send this cookie to
    #// @return bool true if allowed, false otherwise.
    #//
    def test(self, url_=None):
        
        
        if is_null(self.name):
            return False
        # end if
        #// Expires - if expired then nothing else matters.
        if (php_isset(lambda : self.expires)) and time() > self.expires:
            return False
        # end if
        #// Get details on the URL we're thinking about sending to.
        url_ = php_parse_url(url_)
        url_["port"] = url_["port"] if (php_isset(lambda : url_["port"])) else 443 if "https" == url_["scheme"] else 80
        url_["path"] = url_["path"] if (php_isset(lambda : url_["path"])) else "/"
        #// Values to use for comparison against the URL.
        path_ = self.path if (php_isset(lambda : self.path)) else "/"
        port_ = self.port if (php_isset(lambda : self.port)) else None
        domain_ = php_strtolower(self.domain) if (php_isset(lambda : self.domain)) else php_strtolower(url_["host"])
        if False == php_stripos(domain_, "."):
            domain_ += ".local"
        # end if
        #// Host - very basic check that the request URL ends with the domain restriction (minus leading dot).
        domain_ = php_substr(domain_, 1) if php_substr(domain_, 0, 1) == "." else domain_
        if php_substr(url_["host"], -php_strlen(domain_)) != domain_:
            return False
        # end if
        #// Port - supports "port-lists" in the format: "80,8000,8080".
        if (not php_empty(lambda : port_)) and (not php_in_array(url_["port"], php_explode(",", port_))):
            return False
        # end if
        #// Path - request path must start with path restriction.
        if php_substr(url_["path"], 0, php_strlen(path_)) != path_:
            return False
        # end if
        return True
    # end def test
    #// 
    #// Convert cookie name and value back to header string.
    #// 
    #// @since 2.8.0
    #// 
    #// @return string Header encoded cookie name and value.
    #//
    def getheadervalue(self):
        
        
        #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.MethodNameInvalid
        if (not (php_isset(lambda : self.name))) or (not (php_isset(lambda : self.value))):
            return ""
        # end if
        #// 
        #// Filters the header-encoded cookie value.
        #// 
        #// @since 3.4.0
        #// 
        #// @param string $value The cookie value.
        #// @param string $name  The cookie name.
        #//
        return self.name + "=" + apply_filters("wp_http_cookie_value", self.value, self.name)
    # end def getheadervalue
    #// 
    #// Retrieve cookie header for usage in the rest of the WordPress HTTP API.
    #// 
    #// @since 2.8.0
    #// 
    #// @return string
    #//
    def getfullheader(self):
        
        
        #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.MethodNameInvalid
        return "Cookie: " + self.getheadervalue()
    # end def getfullheader
    #// 
    #// Retrieves cookie attributes.
    #// 
    #// @since 4.6.0
    #// 
    #// @return array {
    #// List of attributes.
    #// 
    #// @type string|int|null $expires When the cookie expires. Unix timestamp or formatted date.
    #// @type string          $path    Cookie URL path.
    #// @type string          $domain  Cookie domain.
    #// }
    #//
    def get_attributes(self):
        
        
        return Array({"expires": self.expires, "path": self.path, "domain": self.domain})
    # end def get_attributes
# end class WP_Http_Cookie
