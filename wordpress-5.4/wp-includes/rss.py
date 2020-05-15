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
#// MagpieRSS: a simple RSS integration tool
#// 
#// A compiled file for RSS syndication
#// 
#// @author Kellan Elliott-McCrea <kellan@protest.net>
#// @version 0.51
#// @license GPL
#// 
#// @package External
#// @subpackage MagpieRSS
#// @deprecated 3.0.0 Use SimplePie instead.
#// 
#// 
#// Deprecated. Use SimplePie (class-simplepie.php) instead.
#//
_deprecated_file(php_basename(__FILE__), "3.0.0", WPINC + "/class-simplepie.php")
#// 
#// Fires before MagpieRSS is loaded, to optionally replace it.
#// 
#// @since 2.3.0
#// @deprecated 3.0.0
#//
do_action("load_feed_engine")
#// RSS feed constant.
php_define("RSS", "RSS")
php_define("ATOM", "Atom")
php_define("MAGPIE_USER_AGENT", "WordPress/" + PHP_GLOBALS["wp_version"])
class MagpieRSS():
    parser = Array()
    current_item = Array()
    items = Array()
    channel = Array()
    textinput = Array()
    image = Array()
    feed_type = Array()
    feed_version = Array()
    stack = Array()
    inchannel = False
    initem = False
    incontent = False
    intextinput = False
    inimage = False
    current_field = ""
    current_namespace = False
    _CONTENT_CONSTRUCTS = Array("content", "summary", "info", "title", "tagline", "copyright")
    #// 
    #// PHP5 constructor.
    #//
    def __init__(self, source=None):
        
        #// # Check if PHP xml isn't compiled
        #// #
        if (not php_function_exists("xml_parser_create")):
            return trigger_error("PHP's XML extension is not available. Please contact your hosting provider to enable PHP's XML extension.")
        # end if
        parser = xml_parser_create()
        self.parser = parser
        #// # pass in parser, and a reference to this object
        #// # set up handlers
        #// #
        xml_set_object(self.parser, self)
        xml_set_element_handler(self.parser, "feed_start_element", "feed_end_element")
        xml_set_character_data_handler(self.parser, "feed_cdata")
        status = xml_parse(self.parser, source)
        if (not status):
            errorcode = xml_get_error_code(self.parser)
            if errorcode != XML_ERROR_NONE:
                xml_error = xml_error_string(errorcode)
                error_line = xml_get_current_line_number(self.parser)
                error_col = xml_get_current_column_number(self.parser)
                errormsg = str(xml_error) + str(" at line ") + str(error_line) + str(", column ") + str(error_col)
                self.error(errormsg)
            # end if
        # end if
        xml_parser_free(self.parser)
        self.normalize()
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def magpierss(self, source=None):
        
        self.__init__(source)
    # end def magpierss
    def feed_start_element(self, p=None, element=None, attrs=None):
        
        el = element = php_strtolower(element)
        attrs = php_array_change_key_case(attrs, CASE_LOWER)
        #// check for a namespace, and split if found
        ns = False
        if php_strpos(element, ":"):
            ns, el = php_explode(":", element, 2)
        # end if
        if ns and ns != "rdf":
            self.current_namespace = ns
        # end if
        #// # if feed type isn't set, then this is first element of feed
        #// # identify feed from root element
        #// #
        if (not (php_isset(lambda : self.feed_type))):
            if el == "rdf":
                self.feed_type = RSS
                self.feed_version = "1.0"
            elif el == "rss":
                self.feed_type = RSS
                self.feed_version = attrs["version"]
            elif el == "feed":
                self.feed_type = ATOM
                self.feed_version = attrs["version"]
                self.inchannel = True
            # end if
            return
        # end if
        if el == "channel":
            self.inchannel = True
        elif el == "item" or el == "entry":
            self.initem = True
            if (php_isset(lambda : attrs["rdf:about"])):
                self.current_item["about"] = attrs["rdf:about"]
            # end if
            #// if we're in the default namespace of an RSS feed,
            #// record textinput or image fields
        elif self.feed_type == RSS and self.current_namespace == "" and el == "textinput":
            self.intextinput = True
        elif self.feed_type == RSS and self.current_namespace == "" and el == "image":
            self.inimage = True
            #// # handle atom content constructs
        elif self.feed_type == ATOM and php_in_array(el, self._CONTENT_CONSTRUCTS):
            #// avoid clashing w/ RSS mod_content
            if el == "content":
                el = "atom_content"
            # end if
            self.incontent = el
            #// if inside an Atom content construct (e.g. content or summary) field treat tags as text
        elif self.feed_type == ATOM and self.incontent:
            #// if tags are inlined, then flatten
            attrs_str = join(" ", php_array_map(Array("MagpieRSS", "map_attrs"), php_array_keys(attrs), php_array_values(attrs)))
            self.append_content(str("<") + str(element) + str(" ") + str(attrs_str) + str(">"))
            array_unshift(self.stack, el)
            #// Atom support many links per containging element.
            #// Magpie treats link elements of type rel='alternate'
            #// as being equivalent to RSS's simple link element.
            #//
        elif self.feed_type == ATOM and el == "link":
            if (php_isset(lambda : attrs["rel"])) and attrs["rel"] == "alternate":
                link_el = "link"
            else:
                link_el = "link_" + attrs["rel"]
            # end if
            self.append(link_el, attrs["href"])
        else:
            array_unshift(self.stack, el)
        # end if
    # end def feed_start_element
    def feed_cdata(self, p=None, text=None):
        
        if self.feed_type == ATOM and self.incontent:
            self.append_content(text)
        else:
            current_el = join("_", array_reverse(self.stack))
            self.append(current_el, text)
        # end if
    # end def feed_cdata
    def feed_end_element(self, p=None, el=None):
        
        el = php_strtolower(el)
        if el == "item" or el == "entry":
            self.items[-1] = self.current_item
            self.current_item = Array()
            self.initem = False
        elif self.feed_type == RSS and self.current_namespace == "" and el == "textinput":
            self.intextinput = False
        elif self.feed_type == RSS and self.current_namespace == "" and el == "image":
            self.inimage = False
        elif self.feed_type == ATOM and php_in_array(el, self._CONTENT_CONSTRUCTS):
            self.incontent = False
        elif el == "channel" or el == "feed":
            self.inchannel = False
        elif self.feed_type == ATOM and self.incontent:
            #// balance tags properly
            #// note: This may not actually be necessary
            if self.stack[0] == el:
                self.append_content(str("</") + str(el) + str(">"))
            else:
                self.append_content(str("<") + str(el) + str(" />"))
            # end if
            php_array_shift(self.stack)
        else:
            php_array_shift(self.stack)
        # end if
        self.current_namespace = False
    # end def feed_end_element
    def concat(self, str1=None, str2=""):
        
        if (not (php_isset(lambda : str1))):
            str1 = ""
        # end if
        str1 += str2
    # end def concat
    def append_content(self, text=None):
        
        if self.initem:
            self.concat(self.current_item[self.incontent], text)
        elif self.inchannel:
            self.concat(self.channel[self.incontent], text)
        # end if
    # end def append_content
    #// smart append - field and namespace aware
    def append(self, el=None, text=None):
        
        if (not el):
            return
        # end if
        if self.current_namespace:
            if self.initem:
                self.concat(self.current_item[self.current_namespace][el], text)
            elif self.inchannel:
                self.concat(self.channel[self.current_namespace][el], text)
            elif self.intextinput:
                self.concat(self.textinput[self.current_namespace][el], text)
            elif self.inimage:
                self.concat(self.image[self.current_namespace][el], text)
            # end if
        else:
            if self.initem:
                self.concat(self.current_item[el], text)
            elif self.intextinput:
                self.concat(self.textinput[el], text)
            elif self.inimage:
                self.concat(self.image[el], text)
            elif self.inchannel:
                self.concat(self.channel[el], text)
            # end if
        # end if
    # end def append
    def normalize(self):
        
        #// if atom populate rss fields
        if self.is_atom():
            self.channel["descripton"] = self.channel["tagline"]
            i = 0
            while i < php_count(self.items):
                
                item = self.items[i]
                if (php_isset(lambda : item["summary"])):
                    item["description"] = item["summary"]
                # end if
                if (php_isset(lambda : item["atom_content"])):
                    item["content"]["encoded"] = item["atom_content"]
                # end if
                self.items[i] = item
                i += 1
            # end while
        elif self.is_rss():
            self.channel["tagline"] = self.channel["description"]
            i = 0
            while i < php_count(self.items):
                
                item = self.items[i]
                if (php_isset(lambda : item["description"])):
                    item["summary"] = item["description"]
                # end if
                if (php_isset(lambda : item["content"]["encoded"])):
                    item["atom_content"] = item["content"]["encoded"]
                # end if
                self.items[i] = item
                i += 1
            # end while
        # end if
    # end def normalize
    def is_rss(self):
        
        if self.feed_type == RSS:
            return self.feed_version
        else:
            return False
        # end if
    # end def is_rss
    def is_atom(self):
        
        if self.feed_type == ATOM:
            return self.feed_version
        else:
            return False
        # end if
    # end def is_atom
    def map_attrs(self, k=None, v=None):
        
        return str(k) + str("=\"") + str(v) + str("\"")
    # end def map_attrs
    def error(self, errormsg=None, lvl=E_USER_WARNING):
        
        #// append PHP's error message if track_errors enabled
        if (php_isset(lambda : php_errormsg)):
            errormsg += str(" (") + str(php_errormsg) + str(")")
        # end if
        if MAGPIE_DEBUG:
            trigger_error(errormsg, lvl)
        else:
            php_error_log(errormsg, 0)
        # end if
    # end def error
# end class MagpieRSS
if (not php_function_exists("fetch_rss")):
    #// 
    #// Build Magpie object based on RSS from URL.
    #// 
    #// @since 1.5.0
    #// @package External
    #// @subpackage MagpieRSS
    #// 
    #// @param string $url URL to retrieve feed
    #// @return bool|MagpieRSS false on failure or MagpieRSS object on success.
    #//
    def fetch_rss(url=None, *args_):
        
        #// initialize constants
        init()
        if (not (php_isset(lambda : url))):
            #// error("fetch_rss called without a url");
            return False
        # end if
        #// if cache is disabled
        if (not MAGPIE_CACHE_ON):
            #// fetch file, and parse it
            resp = _fetch_remote_file(url)
            if is_success(resp.status):
                return _response_to_rss(resp)
            else:
                #// error("Failed to fetch $url and cache is off");
                return False
            # end if
        else:
            #// Flow
            #// 1. check cache
            #// 2. if there is a hit, make sure it's fresh
            #// 3. if cached obj fails freshness check, fetch remote
            #// 4. if remote fails, return stale object, or error
            cache = php_new_class("RSSCache", lambda : RSSCache(MAGPIE_CACHE_DIR, MAGPIE_CACHE_AGE))
            if MAGPIE_DEBUG and cache.ERROR:
                debug(cache.ERROR, E_USER_WARNING)
            # end if
            cache_status = 0
            #// response of check_cache
            request_headers = Array()
            #// HTTP headers to send with fetch
            rss = 0
            #// parsed RSS object
            errormsg = 0
            #// errors, if any
            if (not cache.ERROR):
                #// return cache HIT, MISS, or STALE
                cache_status = cache.check_cache(url)
            # end if
            #// if object cached, and cache is fresh, return cached obj
            if cache_status == "HIT":
                rss = cache.get(url)
                if (php_isset(lambda : rss)) and rss:
                    rss.from_cache = 1
                    if MAGPIE_DEBUG > 1:
                        debug("MagpieRSS: Cache HIT", E_USER_NOTICE)
                    # end if
                    return rss
                # end if
            # end if
            #// else attempt a conditional get
            #// set up headers
            if cache_status == "STALE":
                rss = cache.get(url)
                if (php_isset(lambda : rss.etag)) and rss.last_modified:
                    request_headers["If-None-Match"] = rss.etag
                    request_headers["If-Last-Modified"] = rss.last_modified
                # end if
            # end if
            resp = _fetch_remote_file(url, request_headers)
            if (php_isset(lambda : resp)) and resp:
                if resp.status == "304":
                    #// we have the most current copy
                    if MAGPIE_DEBUG > 1:
                        debug(str("Got 304 for ") + str(url))
                    # end if
                    #// reset cache on 304 (at minutillo insistent prodding)
                    cache.set(url, rss)
                    return rss
                elif is_success(resp.status):
                    rss = _response_to_rss(resp)
                    if rss:
                        if MAGPIE_DEBUG > 1:
                            debug("Fetch successful")
                        # end if
                        #// add object to cache
                        cache.set(url, rss)
                        return rss
                    # end if
                else:
                    errormsg = str("Failed to fetch ") + str(url) + str(". ")
                    if resp.error:
                        #// # compensate for Snoopy's annoying habbit to tacking
                        #// # on '\n'
                        http_error = php_substr(resp.error, 0, -2)
                        errormsg += str("(HTTP Error: ") + str(http_error) + str(")")
                    else:
                        errormsg += "(HTTP Response: " + resp.response_code + ")"
                    # end if
                # end if
            else:
                errormsg = "Unable to retrieve RSS file for unknown reasons."
            # end if
            #// else fetch failed
            #// attempt to return cached object
            if rss:
                if MAGPIE_DEBUG:
                    debug(str("Returning STALE object for ") + str(url))
                # end if
                return rss
            # end if
            #// else we totally failed
            #// error( $errormsg );
            return False
        # end if
        pass
    # end def fetch_rss
    pass
# end if
#// 
#// Retrieve URL headers and content using WP HTTP Request API.
#// 
#// @since 1.5.0
#// @package External
#// @subpackage MagpieRSS
#// 
#// @param string $url URL to retrieve
#// @param array $headers Optional. Headers to send to the URL.
#// @return Snoopy style response
#//
def _fetch_remote_file(url=None, headers="", *args_):
    
    resp = wp_safe_remote_request(url, Array({"headers": headers, "timeout": MAGPIE_FETCH_TIME_OUT}))
    if is_wp_error(resp):
        error = php_array_shift(resp.errors)
        resp = php_new_class("stdClass", lambda : stdClass())
        resp.status = 500
        resp.response_code = 500
        resp.error = error[0] + "\n"
        #// \n = Snoopy compatibility
        return resp
    # end if
    #// Snoopy returns headers unprocessed.
    #// Also note, WP_HTTP lowercases all keys, Snoopy did not.
    return_headers = Array()
    for key,value in wp_remote_retrieve_headers(resp):
        if (not php_is_array(value)):
            return_headers[-1] = str(key) + str(": ") + str(value)
        else:
            for v in value:
                return_headers[-1] = str(key) + str(": ") + str(v)
            # end for
        # end if
    # end for
    response = php_new_class("stdClass", lambda : stdClass())
    response.status = wp_remote_retrieve_response_code(resp)
    response.response_code = wp_remote_retrieve_response_code(resp)
    response.headers = return_headers
    response.results = wp_remote_retrieve_body(resp)
    return response
# end def _fetch_remote_file
#// 
#// Retrieve
#// 
#// @since 1.5.0
#// @package External
#// @subpackage MagpieRSS
#// 
#// @param array $resp
#// @return MagpieRSS|bool
#//
def _response_to_rss(resp=None, *args_):
    
    rss = php_new_class("MagpieRSS", lambda : MagpieRSS(resp.results))
    #// if RSS parsed successfully
    if rss and (not (php_isset(lambda : rss.ERROR))) or (not rss.ERROR):
        #// find Etag, and Last-Modified
        for h in resp.headers:
            #// 2003-03-02 - Nicola Asuni (www.tecnick.com) - fixed bug "Undefined offset: 1"
            if php_strpos(h, ": "):
                field, val = php_explode(": ", h, 2)
            else:
                field = h
                val = ""
            # end if
            if field == "etag":
                rss.etag = val
            # end if
            if field == "last-modified":
                rss.last_modified = val
            # end if
        # end for
        return rss
    else:
        errormsg = "Failed to parse RSS file."
        if rss:
            errormsg += " (" + rss.ERROR + ")"
        # end if
        #// error($errormsg);
        return False
    # end if
    pass
# end def _response_to_rss
#// 
#// Set up constants with default values, unless user overrides.
#// 
#// @since 1.5.0
#// @package External
#// @subpackage MagpieRSS
#//
def init(*args_):
    
    if php_defined("MAGPIE_INITALIZED"):
        return
    else:
        php_define("MAGPIE_INITALIZED", 1)
    # end if
    if (not php_defined("MAGPIE_CACHE_ON")):
        php_define("MAGPIE_CACHE_ON", 1)
    # end if
    if (not php_defined("MAGPIE_CACHE_DIR")):
        php_define("MAGPIE_CACHE_DIR", "./cache")
    # end if
    if (not php_defined("MAGPIE_CACHE_AGE")):
        php_define("MAGPIE_CACHE_AGE", 60 * 60)
        pass
    # end if
    if (not php_defined("MAGPIE_CACHE_FRESH_ONLY")):
        php_define("MAGPIE_CACHE_FRESH_ONLY", 0)
    # end if
    if (not php_defined("MAGPIE_DEBUG")):
        php_define("MAGPIE_DEBUG", 0)
    # end if
    if (not php_defined("MAGPIE_USER_AGENT")):
        ua = "WordPress/" + PHP_GLOBALS["wp_version"]
        if MAGPIE_CACHE_ON:
            ua = ua + ")"
        else:
            ua = ua + "; No cache)"
        # end if
        php_define("MAGPIE_USER_AGENT", ua)
    # end if
    if (not php_defined("MAGPIE_FETCH_TIME_OUT")):
        php_define("MAGPIE_FETCH_TIME_OUT", 2)
        pass
    # end if
    #// use gzip encoding to fetch rss files if supported?
    if (not php_defined("MAGPIE_USE_GZIP")):
        php_define("MAGPIE_USE_GZIP", True)
    # end if
# end def init
def is_info(sc=None, *args_):
    
    return sc >= 100 and sc < 200
# end def is_info
def is_success(sc=None, *args_):
    
    return sc >= 200 and sc < 300
# end def is_success
def is_redirect(sc=None, *args_):
    
    return sc >= 300 and sc < 400
# end def is_redirect
def is_error(sc=None, *args_):
    
    return sc >= 400 and sc < 600
# end def is_error
def is_client_error(sc=None, *args_):
    
    return sc >= 400 and sc < 500
# end def is_client_error
def is_server_error(sc=None, *args_):
    
    return sc >= 500 and sc < 600
# end def is_server_error
class RSSCache():
    BASE_CACHE = Array()
    MAX_AGE = 43200
    ERROR = ""
    #// accumulate error messages
    #// 
    #// PHP5 constructor.
    #//
    def __init__(self, base="", age=""):
        
        self.BASE_CACHE = WP_CONTENT_DIR + "/cache"
        if base:
            self.BASE_CACHE = base
        # end if
        if age:
            self.MAX_AGE = age
        # end if
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def rsscache(self, base="", age=""):
        
        self.__init__(base, age)
    # end def rsscache
    #// =======================================================================*\
#// Function:   set
    #// Purpose:    add an item to the cache, keyed on url
    #// Input:      url from which the rss file was fetched
    #// Output:     true on success
    #// \*=======================================================================
    def set(self, url=None, rss=None):
        
        cache_option = "rss_" + self.file_name(url)
        set_transient(cache_option, rss, self.MAX_AGE)
        return cache_option
    # end def set
    #// =======================================================================*\
#// Function:   get
    #// Purpose:    fetch an item from the cache
    #// Input:      url from which the rss file was fetched
    #// Output:     cached object on HIT, false on MISS
    #// \*=======================================================================
    def get(self, url=None):
        
        self.ERROR = ""
        cache_option = "rss_" + self.file_name(url)
        rss = get_transient(cache_option)
        if (not rss):
            self.debug(str("Cache doesn't contain: ") + str(url) + str(" (cache option: ") + str(cache_option) + str(")"))
            return 0
        # end if
        return rss
    # end def get
    #// =======================================================================*\
#// Function:   check_cache
    #// Purpose:    check a url for membership in the cache
    #// and whether the object is older then MAX_AGE (ie. STALE)
    #// Input:      url from which the rss file was fetched
    #// Output:     cached object on HIT, false on MISS
    #// \*=======================================================================
    def check_cache(self, url=None):
        
        self.ERROR = ""
        cache_option = "rss_" + self.file_name(url)
        if get_transient(cache_option):
            #// object exists and is current
            return "HIT"
        else:
            #// object does not exist
            return "MISS"
        # end if
    # end def check_cache
    #// =======================================================================*\
#// Function:   serialize
    #// \*=======================================================================
    def serialize(self, rss=None):
        
        return serialize(rss)
    # end def serialize
    #// =======================================================================*\
#// Function:   unserialize
    #// \*=======================================================================
    def unserialize(self, data=None):
        
        return unserialize(data)
    # end def unserialize
    #// =======================================================================*\
#// Function:   file_name
    #// Purpose:    map url to location in cache
    #// Input:      url from which the rss file was fetched
    #// Output:     a file name
    #// \*=======================================================================
    def file_name(self, url=None):
        
        return php_md5(url)
    # end def file_name
    #// =======================================================================*\
#// Function:   error
    #// Purpose:    register error
    #// \*=======================================================================
    def error(self, errormsg=None, lvl=E_USER_WARNING):
        
        #// append PHP's error message if track_errors enabled
        if (php_isset(lambda : php_errormsg)):
            errormsg += str(" (") + str(php_errormsg) + str(")")
        # end if
        self.ERROR = errormsg
        if MAGPIE_DEBUG:
            trigger_error(errormsg, lvl)
        else:
            php_error_log(errormsg, 0)
        # end if
    # end def error
    def debug(self, debugmsg=None, lvl=E_USER_NOTICE):
        
        if MAGPIE_DEBUG:
            self.error(str("MagpieRSS [debug] ") + str(debugmsg), lvl)
        # end if
    # end def debug
# end class RSSCache
if (not php_function_exists("parse_w3cdtf")):
    def parse_w3cdtf(date_str=None, *args_):
        
        #// # regex to match wc3dtf
        pat = "/(\\d{4})-(\\d{2})-(\\d{2})T(\\d{2}):(\\d{2})(:(\\d{2}))?(?:([-+])(\\d{2}):?(\\d{2})|(Z))?/"
        if php_preg_match(pat, date_str, match):
            year, month, day, hours, minutes, seconds = Array(match[1], match[2], match[3], match[4], match[5], match[7])
            #// # calc epoch for current date assuming GMT
            epoch = gmmktime(hours, minutes, seconds, month, day, year)
            offset = 0
            if match[11] == "Z":
                pass
            else:
                tz_mod, tz_hour, tz_min = Array(match[8], match[9], match[10])
                #// # zero out the variables
                if (not tz_hour):
                    tz_hour = 0
                # end if
                if (not tz_min):
                    tz_min = 0
                # end if
                offset_secs = tz_hour * 60 + tz_min * 60
                #// # is timezone ahead of GMT?  then subtract offset
                #// #
                if tz_mod == "+":
                    offset_secs = offset_secs * -1
                # end if
                offset = offset_secs
            # end if
            epoch = epoch + offset
            return epoch
        else:
            return -1
        # end if
    # end def parse_w3cdtf
# end if
if (not php_function_exists("wp_rss")):
    #// 
    #// Display all RSS items in a HTML ordered list.
    #// 
    #// @since 1.5.0
    #// @package External
    #// @subpackage MagpieRSS
    #// 
    #// @param string $url URL of feed to display. Will not auto sense feed URL.
    #// @param int $num_items Optional. Number of items to display, default is all.
    #//
    def wp_rss(url=None, num_items=-1, *args_):
        
        rss = fetch_rss(url)
        if rss:
            php_print("<ul>")
            if num_items != -1:
                rss.items = php_array_slice(rss.items, 0, num_items)
            # end if
            for item in rss.items:
                printf("<li><a href=\"%1$s\" title=\"%2$s\">%3$s</a></li>", esc_url(item["link"]), esc_attr(strip_tags(item["description"])), esc_html(item["title"]))
            # end for
            php_print("</ul>")
        else:
            _e("An error has occurred, which probably means the feed is down. Try again later.")
        # end if
    # end def wp_rss
# end if
if (not php_function_exists("get_rss")):
    #// 
    #// Display RSS items in HTML list items.
    #// 
    #// You have to specify which HTML list you want, either ordered or unordered
    #// before using the function. You also have to specify how many items you wish
    #// to display. You can't display all of them like you can with wp_rss()
    #// function.
    #// 
    #// @since 1.5.0
    #// @package External
    #// @subpackage MagpieRSS
    #// 
    #// @param string $url URL of feed to display. Will not auto sense feed URL.
    #// @param int $num_items Optional. Number of items to display, default is all.
    #// @return bool False on failure.
    #//
    def get_rss(url=None, num_items=5, *args_):
        
        #// Like get posts, but for RSS
        rss = fetch_rss(url)
        if rss:
            rss.items = php_array_slice(rss.items, 0, num_items)
            for item in rss.items:
                php_print("<li>\n")
                php_print(str("<a href='") + str(item["link"]) + str("' title='") + str(item["description"]) + str("'>"))
                php_print(esc_html(item["title"]))
                php_print("</a><br />\n")
                php_print("</li>\n")
            # end for
        else:
            return False
        # end if
    # end def get_rss
# end if
