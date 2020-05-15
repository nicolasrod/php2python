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
#// Cookie storage object
#// 
#// @package Requests
#// @subpackage Cookies
#// 
#// 
#// Cookie storage object
#// 
#// @package Requests
#// @subpackage Cookies
#//
class Requests_Cookie():
    name = Array()
    value = Array()
    attributes = Array()
    flags = Array()
    reference_time = 0
    #// 
    #// Create a new cookie object
    #// 
    #// @param string $name
    #// @param string $value
    #// @param array|Requests_Utility_CaseInsensitiveDictionary $attributes Associative array of attribute data
    #//
    def __init__(self, name=None, value=None, attributes=Array(), flags=Array(), reference_time=None):
        
        self.name = name
        self.value = value
        self.attributes = attributes
        default_flags = Array({"creation": time(), "last-access": time(), "persistent": False, "host-only": True})
        self.flags = php_array_merge(default_flags, flags)
        self.reference_time = time()
        if reference_time != None:
            self.reference_time = reference_time
        # end if
        self.normalize()
    # end def __init__
    #// 
    #// Check if a cookie is expired.
    #// 
    #// Checks the age against $this->reference_time to determine if the cookie
    #// is expired.
    #// 
    #// @return boolean True if expired, false if time is valid.
    #//
    def is_expired(self):
        
        #// RFC6265, s. 4.1.2.2:
        #// If a cookie has both the Max-Age and the Expires attribute, the Max-
        #// Age attribute has precedence and controls the expiration date of the
        #// cookie.
        if (php_isset(lambda : self.attributes["max-age"])):
            max_age = self.attributes["max-age"]
            return max_age < self.reference_time
        # end if
        if (php_isset(lambda : self.attributes["expires"])):
            expires = self.attributes["expires"]
            return expires < self.reference_time
        # end if
        return False
    # end def is_expired
    #// 
    #// Check if a cookie is valid for a given URI
    #// 
    #// @param Requests_IRI $uri URI to check
    #// @return boolean Whether the cookie is valid for the given URI
    #//
    def uri_matches(self, uri=None):
        
        if (not self.domain_matches(uri.host)):
            return False
        # end if
        if (not self.path_matches(uri.path)):
            return False
        # end if
        return php_empty(lambda : self.attributes["secure"]) or uri.scheme == "https"
    # end def uri_matches
    #// 
    #// Check if a cookie is valid for a given domain
    #// 
    #// @param string $string Domain to check
    #// @return boolean Whether the cookie is valid for the given domain
    #//
    def domain_matches(self, string=None):
        
        if (not (php_isset(lambda : self.attributes["domain"]))):
            #// Cookies created manually; cookies created by Requests will set
            #// the domain to the requested domain
            return True
        # end if
        domain_string = self.attributes["domain"]
        if domain_string == string:
            #// The domain string and the string are identical.
            return True
        # end if
        #// If the cookie is marked as host-only and we don't have an exact
        #// match, reject the cookie
        if self.flags["host-only"] == True:
            return False
        # end if
        if php_strlen(string) <= php_strlen(domain_string):
            #// For obvious reasons, the string cannot be a suffix if the domain
            #// is shorter than the domain string
            return False
        # end if
        if php_substr(string, -1 * php_strlen(domain_string)) != domain_string:
            #// The domain string should be a suffix of the string.
            return False
        # end if
        prefix = php_substr(string, 0, php_strlen(string) - php_strlen(domain_string))
        if php_substr(prefix, -1) != ".":
            #// The last character of the string that is not included in the
            #// domain string should be a %x2E (".") character.
            return False
        # end if
        #// The string should be a host name (i.e., not an IP address).
        return (not php_preg_match("#^(.+\\.)\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}$#", string))
    # end def domain_matches
    #// 
    #// Check if a cookie is valid for a given path
    #// 
    #// From the path-match check in RFC 6265 section 5.1.4
    #// 
    #// @param string $request_path Path to check
    #// @return boolean Whether the cookie is valid for the given path
    #//
    def path_matches(self, request_path=None):
        
        if php_empty(lambda : request_path):
            #// Normalize empty path to root
            request_path = "/"
        # end if
        if (not (php_isset(lambda : self.attributes["path"]))):
            #// Cookies created manually; cookies created by Requests will set
            #// the path to the requested path
            return True
        # end if
        cookie_path = self.attributes["path"]
        if cookie_path == request_path:
            #// The cookie-path and the request-path are identical.
            return True
        # end if
        if php_strlen(request_path) > php_strlen(cookie_path) and php_substr(request_path, 0, php_strlen(cookie_path)) == cookie_path:
            if php_substr(cookie_path, -1) == "/":
                #// The cookie-path is a prefix of the request-path, and the last
                #// character of the cookie-path is %x2F ("/").
                return True
            # end if
            if php_substr(request_path, php_strlen(cookie_path), 1) == "/":
                #// The cookie-path is a prefix of the request-path, and the
                #// first character of the request-path that is not included in
                #// the cookie-path is a %x2F ("/") character.
                return True
            # end if
        # end if
        return False
    # end def path_matches
    #// 
    #// Normalize cookie and attributes
    #// 
    #// @return boolean Whether the cookie was successfully normalized
    #//
    def normalize(self):
        
        for key,value in self.attributes:
            orig_value = value
            value = self.normalize_attribute(key, value)
            if value == None:
                self.attributes[key] = None
                continue
            # end if
            if value != orig_value:
                self.attributes[key] = value
            # end if
        # end for
        return True
    # end def normalize
    #// 
    #// Parse an individual cookie attribute
    #// 
    #// Handles parsing individual attributes from the cookie values.
    #// 
    #// @param string $name Attribute name
    #// @param string|boolean $value Attribute value (string value, or true if empty/flag)
    #// @return mixed Value if available, or null if the attribute value is invalid (and should be skipped)
    #//
    def normalize_attribute(self, name=None, value=None):
        
        for case in Switch(php_strtolower(name)):
            if case("expires"):
                #// Expiration parsing, as per RFC 6265 section 5.2.1
                if php_is_int(value):
                    return value
                # end if
                expiry_time = strtotime(value)
                if expiry_time == False:
                    return None
                # end if
                return expiry_time
            # end if
            if case("max-age"):
                #// Expiration parsing, as per RFC 6265 section 5.2.2
                if php_is_int(value):
                    return value
                # end if
                #// Check that we have a valid age
                if (not php_preg_match("/^-?\\d+$/", value)):
                    return None
                # end if
                delta_seconds = int(value)
                if delta_seconds <= 0:
                    expiry_time = 0
                else:
                    expiry_time = self.reference_time + delta_seconds
                # end if
                return expiry_time
            # end if
            if case("domain"):
                #// Domains are not required as per RFC 6265 section 5.2.3
                if php_empty(lambda : value):
                    return None
                # end if
                #// Domain normalization, as per RFC 6265 section 5.2.3
                if value[0] == ".":
                    value = php_substr(value, 1)
                # end if
                return value
            # end if
            if case():
                return value
            # end if
        # end for
    # end def normalize_attribute
    #// 
    #// Format a cookie for a Cookie header
    #// 
    #// This is used when sending cookies to a server.
    #// 
    #// @return string Cookie formatted for Cookie header
    #//
    def format_for_header(self):
        
        return php_sprintf("%s=%s", self.name, self.value)
    # end def format_for_header
    #// 
    #// Format a cookie for a Cookie header
    #// 
    #// @codeCoverageIgnore
    #// @deprecated Use {@see Requests_Cookie::format_for_header}
    #// @return string
    #//
    def formatforheader(self):
        
        return self.format_for_header()
    # end def formatforheader
    #// 
    #// Format a cookie for a Set-Cookie header
    #// 
    #// This is used when sending cookies to clients. This isn't really
    #// applicable to client-side usage, but might be handy for debugging.
    #// 
    #// @return string Cookie formatted for Set-Cookie header
    #//
    def format_for_set_cookie(self):
        
        header_value = self.format_for_header()
        if (not php_empty(lambda : self.attributes)):
            parts = Array()
            for key,value in self.attributes:
                #// Ignore non-associative attributes
                if php_is_numeric(key):
                    parts[-1] = value
                else:
                    parts[-1] = php_sprintf("%s=%s", key, value)
                # end if
            # end for
            header_value += "; " + php_implode("; ", parts)
        # end if
        return header_value
    # end def format_for_set_cookie
    #// 
    #// Format a cookie for a Set-Cookie header
    #// 
    #// @codeCoverageIgnore
    #// @deprecated Use {@see Requests_Cookie::format_for_set_cookie}
    #// @return string
    #//
    def formatforsetcookie(self):
        
        return self.format_for_set_cookie()
    # end def formatforsetcookie
    #// 
    #// Get the cookie value
    #// 
    #// Attributes and other data can be accessed via methods.
    #//
    def __tostring(self):
        
        return self.value
    # end def __tostring
    #// 
    #// Parse a cookie string into a cookie object
    #// 
    #// Based on Mozilla's parsing code in Firefox and related projects, which
    #// is an intentional deviation from RFC 2109 and RFC 2616. RFC 6265
    #// specifies some of this handling, but not in a thorough manner.
    #// 
    #// @param string Cookie header value (from a Set-Cookie header)
    #// @return Requests_Cookie Parsed cookie object
    #//
    @classmethod
    def parse(self, string=None, name="", reference_time=None):
        
        parts = php_explode(";", string)
        kvparts = php_array_shift(parts)
        if (not php_empty(lambda : name)):
            value = string
        elif php_strpos(kvparts, "=") == False:
            #// Some sites might only have a value without the equals separator.
            #// Deviate from RFC 6265 and pretend it was actually a blank name
            #// (`=foo`)
            #// 
            #// https://bugzilla.mozilla.org/show_bug.cgi?id=169091
            name = ""
            value = kvparts
        else:
            name, value = php_explode("=", kvparts, 2)
        # end if
        name = php_trim(name)
        value = php_trim(value)
        #// Attribute key are handled case-insensitively
        attributes = php_new_class("Requests_Utility_CaseInsensitiveDictionary", lambda : Requests_Utility_CaseInsensitiveDictionary())
        if (not php_empty(lambda : parts)):
            for part in parts:
                if php_strpos(part, "=") == False:
                    part_key = part
                    part_value = True
                else:
                    part_key, part_value = php_explode("=", part, 2)
                    part_value = php_trim(part_value)
                # end if
                part_key = php_trim(part_key)
                attributes[part_key] = part_value
            # end for
        # end if
        return php_new_class("Requests_Cookie", lambda : Requests_Cookie(name, value, attributes, Array(), reference_time))
    # end def parse
    #// 
    #// Parse all Set-Cookie headers from request headers
    #// 
    #// @param Requests_Response_Headers $headers Headers to parse from
    #// @param Requests_IRI|null $origin URI for comparing cookie origins
    #// @param int|null $time Reference time for expiration calculation
    #// @return array
    #//
    @classmethod
    def parse_from_headers(self, headers=None, origin=None, time=None):
        
        cookie_headers = headers.getvalues("Set-Cookie")
        if php_empty(lambda : cookie_headers):
            return Array()
        # end if
        cookies = Array()
        for header in cookie_headers:
            parsed = self.parse(header, "", time)
            #// Default domain/path attributes
            if php_empty(lambda : parsed.attributes["domain"]) and (not php_empty(lambda : origin)):
                parsed.attributes["domain"] = origin.host
                parsed.flags["host-only"] = True
            else:
                parsed.flags["host-only"] = False
            # end if
            path_is_valid = (not php_empty(lambda : parsed.attributes["path"])) and parsed.attributes["path"][0] == "/"
            if (not path_is_valid) and (not php_empty(lambda : origin)):
                path = origin.path
                #// Default path normalization as per RFC 6265 section 5.1.4
                if php_substr(path, 0, 1) != "/":
                    #// If the uri-path is empty or if the first character of
                    #// the uri-path is not a %x2F ("/") character, output
                    #// %x2F ("/") and skip the remaining steps.
                    path = "/"
                elif php_substr_count(path, "/") == 1:
                    #// If the uri-path contains no more than one %x2F ("/")
                    #// character, output %x2F ("/") and skip the remaining
                    #// step.
                    path = "/"
                else:
                    #// Output the characters of the uri-path from the first
                    #// character up to, but not including, the right-most
                    #// %x2F ("/").
                    path = php_substr(path, 0, php_strrpos(path, "/"))
                # end if
                parsed.attributes["path"] = path
            # end if
            #// Reject invalid cookie domains
            if (not php_empty(lambda : origin)) and (not parsed.domain_matches(origin.host)):
                continue
            # end if
            cookies[parsed.name] = parsed
        # end for
        return cookies
    # end def parse_from_headers
    #// 
    #// Parse all Set-Cookie headers from request headers
    #// 
    #// @codeCoverageIgnore
    #// @deprecated Use {@see Requests_Cookie::parse_from_headers}
    #// @return string
    #//
    @classmethod
    def parsefromheaders(self, headers=None):
        
        return self.parse_from_headers(headers)
    # end def parsefromheaders
# end class Requests_Cookie
