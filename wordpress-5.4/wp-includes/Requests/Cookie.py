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
    #// 
    #// Cookie name.
    #// 
    #// @var string
    #//
    name = Array()
    #// 
    #// Cookie value.
    #// 
    #// @var string
    #//
    value = Array()
    #// 
    #// Cookie attributes
    #// 
    #// Valid keys are (currently) path, domain, expires, max-age, secure and
    #// httponly.
    #// 
    #// @var Requests_Utility_CaseInsensitiveDictionary|array Array-like object
    #//
    attributes = Array()
    #// 
    #// Cookie flags
    #// 
    #// Valid keys are (currently) creation, last-access, persistent and
    #// host-only.
    #// 
    #// @var array
    #//
    flags = Array()
    #// 
    #// Reference time for relative calculations
    #// 
    #// This is used in place of `time()` when calculating Max-Age expiration and
    #// checking time validity.
    #// 
    #// @var int
    #//
    reference_time = 0
    #// 
    #// Create a new cookie object
    #// 
    #// @param string $name
    #// @param string $value
    #// @param array|Requests_Utility_CaseInsensitiveDictionary $attributes Associative array of attribute data
    #//
    def __init__(self, name_=None, value_=None, attributes_=None, flags_=None, reference_time_=None):
        if attributes_ is None:
            attributes_ = Array()
        # end if
        if flags_ is None:
            flags_ = Array()
        # end if
        if reference_time_ is None:
            reference_time_ = None
        # end if
        
        self.name = name_
        self.value = value_
        self.attributes = attributes_
        default_flags_ = Array({"creation": time(), "last-access": time(), "persistent": False, "host-only": True})
        self.flags = php_array_merge(default_flags_, flags_)
        self.reference_time = time()
        if reference_time_ != None:
            self.reference_time = reference_time_
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
            max_age_ = self.attributes["max-age"]
            return max_age_ < self.reference_time
        # end if
        if (php_isset(lambda : self.attributes["expires"])):
            expires_ = self.attributes["expires"]
            return expires_ < self.reference_time
        # end if
        return False
    # end def is_expired
    #// 
    #// Check if a cookie is valid for a given URI
    #// 
    #// @param Requests_IRI $uri URI to check
    #// @return boolean Whether the cookie is valid for the given URI
    #//
    def uri_matches(self, uri_=None):
        
        
        if (not self.domain_matches(uri_.host)):
            return False
        # end if
        if (not self.path_matches(uri_.path)):
            return False
        # end if
        return php_empty(lambda : self.attributes["secure"]) or uri_.scheme == "https"
    # end def uri_matches
    #// 
    #// Check if a cookie is valid for a given domain
    #// 
    #// @param string $string Domain to check
    #// @return boolean Whether the cookie is valid for the given domain
    #//
    def domain_matches(self, string_=None):
        
        
        if (not (php_isset(lambda : self.attributes["domain"]))):
            #// Cookies created manually; cookies created by Requests will set
            #// the domain to the requested domain
            return True
        # end if
        domain_string_ = self.attributes["domain"]
        if domain_string_ == string_:
            #// The domain string and the string are identical.
            return True
        # end if
        #// If the cookie is marked as host-only and we don't have an exact
        #// match, reject the cookie
        if self.flags["host-only"] == True:
            return False
        # end if
        if php_strlen(string_) <= php_strlen(domain_string_):
            #// For obvious reasons, the string cannot be a suffix if the domain
            #// is shorter than the domain string
            return False
        # end if
        if php_substr(string_, -1 * php_strlen(domain_string_)) != domain_string_:
            #// The domain string should be a suffix of the string.
            return False
        # end if
        prefix_ = php_substr(string_, 0, php_strlen(string_) - php_strlen(domain_string_))
        if php_substr(prefix_, -1) != ".":
            #// The last character of the string that is not included in the
            #// domain string should be a %x2E (".") character.
            return False
        # end if
        #// The string should be a host name (i.e., not an IP address).
        return (not php_preg_match("#^(.+\\.)\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}$#", string_))
    # end def domain_matches
    #// 
    #// Check if a cookie is valid for a given path
    #// 
    #// From the path-match check in RFC 6265 section 5.1.4
    #// 
    #// @param string $request_path Path to check
    #// @return boolean Whether the cookie is valid for the given path
    #//
    def path_matches(self, request_path_=None):
        
        
        if php_empty(lambda : request_path_):
            #// Normalize empty path to root
            request_path_ = "/"
        # end if
        if (not (php_isset(lambda : self.attributes["path"]))):
            #// Cookies created manually; cookies created by Requests will set
            #// the path to the requested path
            return True
        # end if
        cookie_path_ = self.attributes["path"]
        if cookie_path_ == request_path_:
            #// The cookie-path and the request-path are identical.
            return True
        # end if
        if php_strlen(request_path_) > php_strlen(cookie_path_) and php_substr(request_path_, 0, php_strlen(cookie_path_)) == cookie_path_:
            if php_substr(cookie_path_, -1) == "/":
                #// The cookie-path is a prefix of the request-path, and the last
                #// character of the cookie-path is %x2F ("/").
                return True
            # end if
            if php_substr(request_path_, php_strlen(cookie_path_), 1) == "/":
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
        
        
        for key_,value_ in self.attributes.items():
            orig_value_ = value_
            value_ = self.normalize_attribute(key_, value_)
            if value_ == None:
                self.attributes[key_] = None
                continue
            # end if
            if value_ != orig_value_:
                self.attributes[key_] = value_
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
    def normalize_attribute(self, name_=None, value_=None):
        
        
        for case in Switch(php_strtolower(name_)):
            if case("expires"):
                #// Expiration parsing, as per RFC 6265 section 5.2.1
                if php_is_int(value_):
                    return value_
                # end if
                expiry_time_ = strtotime(value_)
                if expiry_time_ == False:
                    return None
                # end if
                return expiry_time_
            # end if
            if case("max-age"):
                #// Expiration parsing, as per RFC 6265 section 5.2.2
                if php_is_int(value_):
                    return value_
                # end if
                #// Check that we have a valid age
                if (not php_preg_match("/^-?\\d+$/", value_)):
                    return None
                # end if
                delta_seconds_ = php_int(value_)
                if delta_seconds_ <= 0:
                    expiry_time_ = 0
                else:
                    expiry_time_ = self.reference_time + delta_seconds_
                # end if
                return expiry_time_
            # end if
            if case("domain"):
                #// Domains are not required as per RFC 6265 section 5.2.3
                if php_empty(lambda : value_):
                    return None
                # end if
                #// Domain normalization, as per RFC 6265 section 5.2.3
                if value_[0] == ".":
                    value_ = php_substr(value_, 1)
                # end if
                return value_
            # end if
            if case():
                return value_
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
        
        
        header_value_ = self.format_for_header()
        if (not php_empty(lambda : self.attributes)):
            parts_ = Array()
            for key_,value_ in self.attributes.items():
                #// Ignore non-associative attributes
                if php_is_numeric(key_):
                    parts_[-1] = value_
                else:
                    parts_[-1] = php_sprintf("%s=%s", key_, value_)
                # end if
            # end for
            header_value_ += "; " + php_implode("; ", parts_)
        # end if
        return header_value_
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
    def parse(self, string_=None, name_="", reference_time_=None):
        if reference_time_ is None:
            reference_time_ = None
        # end if
        
        parts_ = php_explode(";", string_)
        kvparts_ = php_array_shift(parts_)
        if (not php_empty(lambda : name_)):
            value_ = string_
        elif php_strpos(kvparts_, "=") == False:
            #// Some sites might only have a value without the equals separator.
            #// Deviate from RFC 6265 and pretend it was actually a blank name
            #// (`=foo`)
            #// 
            #// https://bugzilla.mozilla.org/show_bug.cgi?id=169091
            name_ = ""
            value_ = kvparts_
        else:
            name_, value_ = php_explode("=", kvparts_, 2)
        # end if
        name_ = php_trim(name_)
        value_ = php_trim(value_)
        #// Attribute key are handled case-insensitively
        attributes_ = php_new_class("Requests_Utility_CaseInsensitiveDictionary", lambda : Requests_Utility_CaseInsensitiveDictionary())
        if (not php_empty(lambda : parts_)):
            for part_ in parts_:
                if php_strpos(part_, "=") == False:
                    part_key_ = part_
                    part_value_ = True
                else:
                    part_key_, part_value_ = php_explode("=", part_, 2)
                    part_value_ = php_trim(part_value_)
                # end if
                part_key_ = php_trim(part_key_)
                attributes_[part_key_] = part_value_
            # end for
        # end if
        return php_new_class("Requests_Cookie", lambda : Requests_Cookie(name_, value_, attributes_, Array(), reference_time_))
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
    def parse_from_headers(self, headers_=None, origin_=None, time_=None):
        if origin_ is None:
            origin_ = None
        # end if
        if time_ is None:
            time_ = None
        # end if
        
        cookie_headers_ = headers_.getvalues("Set-Cookie")
        if php_empty(lambda : cookie_headers_):
            return Array()
        # end if
        cookies_ = Array()
        for header_ in cookie_headers_:
            parsed_ = self.parse(header_, "", time_)
            #// Default domain/path attributes
            if php_empty(lambda : parsed_.attributes["domain"]) and (not php_empty(lambda : origin_)):
                parsed_.attributes["domain"] = origin_.host
                parsed_.flags["host-only"] = True
            else:
                parsed_.flags["host-only"] = False
            # end if
            path_is_valid_ = (not php_empty(lambda : parsed_.attributes["path"])) and parsed_.attributes["path"][0] == "/"
            if (not path_is_valid_) and (not php_empty(lambda : origin_)):
                path_ = origin_.path
                #// Default path normalization as per RFC 6265 section 5.1.4
                if php_substr(path_, 0, 1) != "/":
                    #// If the uri-path is empty or if the first character of
                    #// the uri-path is not a %x2F ("/") character, output
                    #// %x2F ("/") and skip the remaining steps.
                    path_ = "/"
                elif php_substr_count(path_, "/") == 1:
                    #// If the uri-path contains no more than one %x2F ("/")
                    #// character, output %x2F ("/") and skip the remaining
                    #// step.
                    path_ = "/"
                else:
                    #// Output the characters of the uri-path from the first
                    #// character up to, but not including, the right-most
                    #// %x2F ("/").
                    path_ = php_substr(path_, 0, php_strrpos(path_, "/"))
                # end if
                parsed_.attributes["path"] = path_
            # end if
            #// Reject invalid cookie domains
            if (not php_empty(lambda : origin_)) and (not parsed_.domain_matches(origin_.host)):
                continue
            # end if
            cookies_[parsed_.name] = parsed_
        # end for
        return cookies_
    # end def parse_from_headers
    #// 
    #// Parse all Set-Cookie headers from request headers
    #// 
    #// @codeCoverageIgnore
    #// @deprecated Use {@see Requests_Cookie::parse_from_headers}
    #// @return string
    #//
    @classmethod
    def parsefromheaders(self, headers_=None):
        
        
        return self.parse_from_headers(headers_)
    # end def parsefromheaders
# end class Requests_Cookie
