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
    name = Array()
    value = Array()
    expires = Array()
    path = Array()
    domain = Array()
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
    def __init__(self, data=None, requested_url=""):
        
        if requested_url:
            arrURL = php_no_error(lambda: php_parse_url(requested_url))
        # end if
        if (php_isset(lambda : arrURL["host"])):
            self.domain = arrURL["host"]
        # end if
        self.path = arrURL["path"] if (php_isset(lambda : arrURL["path"])) else "/"
        if "/" != php_substr(self.path, -1):
            self.path = php_dirname(self.path) + "/"
        # end if
        if php_is_string(data):
            #// Assume it's a header string direct from a previous request.
            pairs = php_explode(";", data)
            #// Special handling for first pair; name=value. Also be careful of "=" in value.
            name = php_trim(php_substr(pairs[0], 0, php_strpos(pairs[0], "=")))
            value = php_substr(pairs[0], php_strpos(pairs[0], "=") + 1)
            self.name = name
            self.value = urldecode(value)
            #// Removes name=value from items.
            php_array_shift(pairs)
            #// Set everything else as a property.
            for pair in pairs:
                pair = php_rtrim(pair)
                #// Handle the cookie ending in ; which results in a empty final pair.
                if php_empty(lambda : pair):
                    continue
                # end if
                key, val = php_explode("=", pair) if php_strpos(pair, "=") else Array(pair, "")
                key = php_strtolower(php_trim(key))
                if "expires" == key:
                    val = strtotime(val)
                # end if
                self.key = val
            # end for
        else:
            if (not (php_isset(lambda : data["name"]))):
                return
            # end if
            #// Set properties based directly on parameters.
            for field in Array("name", "value", "path", "domain", "port", "host_only"):
                if (php_isset(lambda : data[field])):
                    self.field = data[field]
                # end if
            # end for
            if (php_isset(lambda : data["expires"])):
                self.expires = data["expires"] if php_is_int(data["expires"]) else strtotime(data["expires"])
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
    def test(self, url=None):
        
        if is_null(self.name):
            return False
        # end if
        #// Expires - if expired then nothing else matters.
        if (php_isset(lambda : self.expires)) and time() > self.expires:
            return False
        # end if
        #// Get details on the URL we're thinking about sending to.
        url = php_parse_url(url)
        url["port"] = url["port"] if (php_isset(lambda : url["port"])) else 443 if "https" == url["scheme"] else 80
        url["path"] = url["path"] if (php_isset(lambda : url["path"])) else "/"
        #// Values to use for comparison against the URL.
        path = self.path if (php_isset(lambda : self.path)) else "/"
        port = self.port if (php_isset(lambda : self.port)) else None
        domain = php_strtolower(self.domain) if (php_isset(lambda : self.domain)) else php_strtolower(url["host"])
        if False == php_stripos(domain, "."):
            domain += ".local"
        # end if
        #// Host - very basic check that the request URL ends with the domain restriction (minus leading dot).
        domain = php_substr(domain, 1) if php_substr(domain, 0, 1) == "." else domain
        if php_substr(url["host"], -php_strlen(domain)) != domain:
            return False
        # end if
        #// Port - supports "port-lists" in the format: "80,8000,8080".
        if (not php_empty(lambda : port)) and (not php_in_array(url["port"], php_explode(",", port))):
            return False
        # end if
        #// Path - request path must start with path restriction.
        if php_substr(url["path"], 0, php_strlen(path)) != path:
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
