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
    #// item currently being parsed
    items = Array()
    #// collection of parsed items
    channel = Array()
    #// hash of channel fields
    textinput = Array()
    image = Array()
    feed_type = Array()
    feed_version = Array()
    #// parser variables
    stack = Array()
    #// parser stack
    inchannel = False
    initem = False
    incontent = False
    #// if in Atom <content mode="xml"> field
    intextinput = False
    inimage = False
    current_field = ""
    current_namespace = False
    #// var $ERROR = "";
    _CONTENT_CONSTRUCTS = Array("content", "summary", "info", "title", "tagline", "copyright")
    #// 
    #// PHP5 constructor.
    #//
    def __init__(self, source_=None):
        
        
        #// # Check if PHP xml isn't compiled
        #// #
        if (not php_function_exists("xml_parser_create")):
            return trigger_error("PHP's XML extension is not available. Please contact your hosting provider to enable PHP's XML extension.")
        # end if
        parser_ = xml_parser_create()
        self.parser = parser_
        #// # pass in parser, and a reference to this object
        #// # set up handlers
        #// #
        xml_set_object(self.parser, self)
        xml_set_element_handler(self.parser, "feed_start_element", "feed_end_element")
        xml_set_character_data_handler(self.parser, "feed_cdata")
        status_ = xml_parse(self.parser, source_)
        if (not status_):
            errorcode_ = xml_get_error_code(self.parser)
            if errorcode_ != XML_ERROR_NONE:
                xml_error_ = xml_error_string(errorcode_)
                error_line_ = xml_get_current_line_number(self.parser)
                error_col_ = xml_get_current_column_number(self.parser)
                errormsg_ = str(xml_error_) + str(" at line ") + str(error_line_) + str(", column ") + str(error_col_)
                self.error(errormsg_)
            # end if
        # end if
        xml_parser_free(self.parser)
        self.normalize()
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def magpierss(self, source_=None):
        
        
        self.__init__(source_)
    # end def magpierss
    def feed_start_element(self, p_=None, element_=None, attrs_=None):
        
        
        el_ = element_ = php_strtolower(element_)
        attrs_ = php_array_change_key_case(attrs_, CASE_LOWER)
        #// check for a namespace, and split if found
        ns_ = False
        if php_strpos(element_, ":"):
            ns_, el_ = php_explode(":", element_, 2)
        # end if
        if ns_ and ns_ != "rdf":
            self.current_namespace = ns_
        # end if
        #// # if feed type isn't set, then this is first element of feed
        #// # identify feed from root element
        #// #
        if (not (php_isset(lambda : self.feed_type))):
            if el_ == "rdf":
                self.feed_type = RSS
                self.feed_version = "1.0"
            elif el_ == "rss":
                self.feed_type = RSS
                self.feed_version = attrs_["version"]
            elif el_ == "feed":
                self.feed_type = ATOM
                self.feed_version = attrs_["version"]
                self.inchannel = True
            # end if
            return
        # end if
        if el_ == "channel":
            self.inchannel = True
        elif el_ == "item" or el_ == "entry":
            self.initem = True
            if (php_isset(lambda : attrs_["rdf:about"])):
                self.current_item["about"] = attrs_["rdf:about"]
            # end if
            #// if we're in the default namespace of an RSS feed,
            #// record textinput or image fields
        elif self.feed_type == RSS and self.current_namespace == "" and el_ == "textinput":
            self.intextinput = True
        elif self.feed_type == RSS and self.current_namespace == "" and el_ == "image":
            self.inimage = True
            #// # handle atom content constructs
        elif self.feed_type == ATOM and php_in_array(el_, self._CONTENT_CONSTRUCTS):
            #// avoid clashing w/ RSS mod_content
            if el_ == "content":
                el_ = "atom_content"
            # end if
            self.incontent = el_
            #// if inside an Atom content construct (e.g. content or summary) field treat tags as text
        elif self.feed_type == ATOM and self.incontent:
            #// if tags are inlined, then flatten
            attrs_str_ = join(" ", php_array_map(Array("MagpieRSS", "map_attrs"), php_array_keys(attrs_), php_array_values(attrs_)))
            self.append_content(str("<") + str(element_) + str(" ") + str(attrs_str_) + str(">"))
            array_unshift(self.stack, el_)
            #// Atom support many links per containging element.
            #// Magpie treats link elements of type rel='alternate'
            #// as being equivalent to RSS's simple link element.
            #//
        elif self.feed_type == ATOM and el_ == "link":
            if (php_isset(lambda : attrs_["rel"])) and attrs_["rel"] == "alternate":
                link_el_ = "link"
            else:
                link_el_ = "link_" + attrs_["rel"]
            # end if
            self.append(link_el_, attrs_["href"])
        else:
            array_unshift(self.stack, el_)
        # end if
    # end def feed_start_element
    def feed_cdata(self, p_=None, text_=None):
        
        
        if self.feed_type == ATOM and self.incontent:
            self.append_content(text_)
        else:
            current_el_ = join("_", array_reverse(self.stack))
            self.append(current_el_, text_)
        # end if
    # end def feed_cdata
    def feed_end_element(self, p_=None, el_=None):
        
        
        el_ = php_strtolower(el_)
        if el_ == "item" or el_ == "entry":
            self.items[-1] = self.current_item
            self.current_item = Array()
            self.initem = False
        elif self.feed_type == RSS and self.current_namespace == "" and el_ == "textinput":
            self.intextinput = False
        elif self.feed_type == RSS and self.current_namespace == "" and el_ == "image":
            self.inimage = False
        elif self.feed_type == ATOM and php_in_array(el_, self._CONTENT_CONSTRUCTS):
            self.incontent = False
        elif el_ == "channel" or el_ == "feed":
            self.inchannel = False
        elif self.feed_type == ATOM and self.incontent:
            #// balance tags properly
            #// note: This may not actually be necessary
            if self.stack[0] == el_:
                self.append_content(str("</") + str(el_) + str(">"))
            else:
                self.append_content(str("<") + str(el_) + str(" />"))
            # end if
            php_array_shift(self.stack)
        else:
            php_array_shift(self.stack)
        # end if
        self.current_namespace = False
    # end def feed_end_element
    def concat(self, str1_=None, str2_=""):
        
        
        if (not (php_isset(lambda : str1_))):
            str1_ = ""
        # end if
        str1_ += str2_
    # end def concat
    def append_content(self, text_=None):
        
        
        if self.initem:
            self.concat(self.current_item[self.incontent], text_)
        elif self.inchannel:
            self.concat(self.channel[self.incontent], text_)
        # end if
    # end def append_content
    #// smart append - field and namespace aware
    def append(self, el_=None, text_=None):
        
        
        if (not el_):
            return
        # end if
        if self.current_namespace:
            if self.initem:
                self.concat(self.current_item[self.current_namespace][el_], text_)
            elif self.inchannel:
                self.concat(self.channel[self.current_namespace][el_], text_)
            elif self.intextinput:
                self.concat(self.textinput[self.current_namespace][el_], text_)
            elif self.inimage:
                self.concat(self.image[self.current_namespace][el_], text_)
            # end if
        else:
            if self.initem:
                self.concat(self.current_item[el_], text_)
            elif self.intextinput:
                self.concat(self.textinput[el_], text_)
            elif self.inimage:
                self.concat(self.image[el_], text_)
            elif self.inchannel:
                self.concat(self.channel[el_], text_)
            # end if
        # end if
    # end def append
    def normalize(self):
        
        
        #// if atom populate rss fields
        if self.is_atom():
            self.channel["descripton"] = self.channel["tagline"]
            i_ = 0
            while i_ < php_count(self.items):
                
                item_ = self.items[i_]
                if (php_isset(lambda : item_["summary"])):
                    item_["description"] = item_["summary"]
                # end if
                if (php_isset(lambda : item_["atom_content"])):
                    item_["content"]["encoded"] = item_["atom_content"]
                # end if
                self.items[i_] = item_
                i_ += 1
            # end while
        elif self.is_rss():
            self.channel["tagline"] = self.channel["description"]
            i_ = 0
            while i_ < php_count(self.items):
                
                item_ = self.items[i_]
                if (php_isset(lambda : item_["description"])):
                    item_["summary"] = item_["description"]
                # end if
                if (php_isset(lambda : item_["content"]["encoded"])):
                    item_["atom_content"] = item_["content"]["encoded"]
                # end if
                self.items[i_] = item_
                i_ += 1
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
    def map_attrs(self, k_=None, v_=None):
        
        
        return str(k_) + str("=\"") + str(v_) + str("\"")
    # end def map_attrs
    def error(self, errormsg_=None, lvl_=None):
        if lvl_ is None:
            lvl_ = E_USER_WARNING
        # end if
        
        #// append PHP's error message if track_errors enabled
        if (php_isset(lambda : php_errormsg_)):
            errormsg_ += str(" (") + str(php_errormsg_) + str(")")
        # end if
        if MAGPIE_DEBUG:
            trigger_error(errormsg_, lvl_)
        else:
            php_error_log(errormsg_, 0)
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
    def fetch_rss(url_=None, *_args_):
        
        
        #// initialize constants
        init()
        if (not (php_isset(lambda : url_))):
            #// error("fetch_rss called without a url");
            return False
        # end if
        #// if cache is disabled
        if (not MAGPIE_CACHE_ON):
            #// fetch file, and parse it
            resp_ = _fetch_remote_file(url_)
            if is_success(resp_.status):
                return _response_to_rss(resp_)
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
            cache_ = php_new_class("RSSCache", lambda : RSSCache(MAGPIE_CACHE_DIR, MAGPIE_CACHE_AGE))
            if MAGPIE_DEBUG and cache_.ERROR:
                debug(cache_.ERROR, E_USER_WARNING)
            # end if
            cache_status_ = 0
            #// response of check_cache
            request_headers_ = Array()
            #// HTTP headers to send with fetch
            rss_ = 0
            #// parsed RSS object
            errormsg_ = 0
            #// errors, if any
            if (not cache_.ERROR):
                #// return cache HIT, MISS, or STALE
                cache_status_ = cache_.check_cache(url_)
            # end if
            #// if object cached, and cache is fresh, return cached obj
            if cache_status_ == "HIT":
                rss_ = cache_.get(url_)
                if (php_isset(lambda : rss_)) and rss_:
                    rss_.from_cache = 1
                    if MAGPIE_DEBUG > 1:
                        debug("MagpieRSS: Cache HIT", E_USER_NOTICE)
                    # end if
                    return rss_
                # end if
            # end if
            #// else attempt a conditional get
            #// set up headers
            if cache_status_ == "STALE":
                rss_ = cache_.get(url_)
                if (php_isset(lambda : rss_.etag)) and rss_.last_modified:
                    request_headers_["If-None-Match"] = rss_.etag
                    request_headers_["If-Last-Modified"] = rss_.last_modified
                # end if
            # end if
            resp_ = _fetch_remote_file(url_, request_headers_)
            if (php_isset(lambda : resp_)) and resp_:
                if resp_.status == "304":
                    #// we have the most current copy
                    if MAGPIE_DEBUG > 1:
                        debug(str("Got 304 for ") + str(url_))
                    # end if
                    #// reset cache on 304 (at minutillo insistent prodding)
                    cache_.set(url_, rss_)
                    return rss_
                elif is_success(resp_.status):
                    rss_ = _response_to_rss(resp_)
                    if rss_:
                        if MAGPIE_DEBUG > 1:
                            debug("Fetch successful")
                        # end if
                        #// add object to cache
                        cache_.set(url_, rss_)
                        return rss_
                    # end if
                else:
                    errormsg_ = str("Failed to fetch ") + str(url_) + str(". ")
                    if resp_.error:
                        #// # compensate for Snoopy's annoying habbit to tacking
                        #// # on '\n'
                        http_error_ = php_substr(resp_.error, 0, -2)
                        errormsg_ += str("(HTTP Error: ") + str(http_error_) + str(")")
                    else:
                        errormsg_ += "(HTTP Response: " + resp_.response_code + ")"
                    # end if
                # end if
            else:
                errormsg_ = "Unable to retrieve RSS file for unknown reasons."
            # end if
            #// else fetch failed
            #// attempt to return cached object
            if rss_:
                if MAGPIE_DEBUG:
                    debug(str("Returning STALE object for ") + str(url_))
                # end if
                return rss_
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
def _fetch_remote_file(url_=None, headers_="", *_args_):
    
    
    resp_ = wp_safe_remote_request(url_, Array({"headers": headers_, "timeout": MAGPIE_FETCH_TIME_OUT}))
    if is_wp_error(resp_):
        error_ = php_array_shift(resp_.errors)
        resp_ = php_new_class("stdClass", lambda : stdClass())
        resp_.status = 500
        resp_.response_code = 500
        resp_.error = error_[0] + "\n"
        #// \n = Snoopy compatibility
        return resp_
    # end if
    #// Snoopy returns headers unprocessed.
    #// Also note, WP_HTTP lowercases all keys, Snoopy did not.
    return_headers_ = Array()
    for key_,value_ in wp_remote_retrieve_headers(resp_):
        if (not php_is_array(value_)):
            return_headers_[-1] = str(key_) + str(": ") + str(value_)
        else:
            for v_ in value_:
                return_headers_[-1] = str(key_) + str(": ") + str(v_)
            # end for
        # end if
    # end for
    response_ = php_new_class("stdClass", lambda : stdClass())
    response_.status = wp_remote_retrieve_response_code(resp_)
    response_.response_code = wp_remote_retrieve_response_code(resp_)
    response_.headers = return_headers_
    response_.results = wp_remote_retrieve_body(resp_)
    return response_
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
def _response_to_rss(resp_=None, *_args_):
    
    
    rss_ = php_new_class("MagpieRSS", lambda : MagpieRSS(resp_.results))
    #// if RSS parsed successfully
    if rss_ and (not (php_isset(lambda : rss_.ERROR))) or (not rss_.ERROR):
        #// find Etag, and Last-Modified
        for h_ in resp_.headers:
            #// 2003-03-02 - Nicola Asuni (www.tecnick.com) - fixed bug "Undefined offset: 1"
            if php_strpos(h_, ": "):
                field_, val_ = php_explode(": ", h_, 2)
            else:
                field_ = h_
                val_ = ""
            # end if
            if field_ == "etag":
                rss_.etag = val_
            # end if
            if field_ == "last-modified":
                rss_.last_modified = val_
            # end if
        # end for
        return rss_
    else:
        errormsg_ = "Failed to parse RSS file."
        if rss_:
            errormsg_ += " (" + rss_.ERROR + ")"
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
def init(*_args_):
    
    
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
        ua_ = "WordPress/" + PHP_GLOBALS["wp_version"]
        if MAGPIE_CACHE_ON:
            ua_ = ua_ + ")"
        else:
            ua_ = ua_ + "; No cache)"
        # end if
        php_define("MAGPIE_USER_AGENT", ua_)
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
def is_info(sc_=None, *_args_):
    
    
    return sc_ >= 100 and sc_ < 200
# end def is_info
def is_success(sc_=None, *_args_):
    
    
    return sc_ >= 200 and sc_ < 300
# end def is_success
def is_redirect(sc_=None, *_args_):
    
    
    return sc_ >= 300 and sc_ < 400
# end def is_redirect
def is_error(sc_=None, *_args_):
    
    
    return sc_ >= 400 and sc_ < 600
# end def is_error
def is_client_error(sc_=None, *_args_):
    
    
    return sc_ >= 400 and sc_ < 500
# end def is_client_error
def is_server_error(sc_=None, *_args_):
    
    
    return sc_ >= 500 and sc_ < 600
# end def is_server_error
class RSSCache():
    BASE_CACHE = Array()
    #// where the cache files are stored
    MAX_AGE = 43200
    #// when are files stale, default twelve hours
    ERROR = ""
    #// accumulate error messages
    #// 
    #// PHP5 constructor.
    #//
    def __init__(self, base_="", age_=""):
        
        
        self.BASE_CACHE = WP_CONTENT_DIR + "/cache"
        if base_:
            self.BASE_CACHE = base_
        # end if
        if age_:
            self.MAX_AGE = age_
        # end if
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def rsscache(self, base_="", age_=""):
        
        
        self.__init__(base_, age_)
    # end def rsscache
    #// =======================================================================*\
#// Function:   set
    #// Purpose:    add an item to the cache, keyed on url
    #// Input:      url from which the rss file was fetched
    #// Output:     true on success
    #// \*=======================================================================
    def set(self, url_=None, rss_=None):
        
        
        cache_option_ = "rss_" + self.file_name(url_)
        set_transient(cache_option_, rss_, self.MAX_AGE)
        return cache_option_
    # end def set
    #// =======================================================================*\
#// Function:   get
    #// Purpose:    fetch an item from the cache
    #// Input:      url from which the rss file was fetched
    #// Output:     cached object on HIT, false on MISS
    #// \*=======================================================================
    def get(self, url_=None):
        
        
        self.ERROR = ""
        cache_option_ = "rss_" + self.file_name(url_)
        rss_ = get_transient(cache_option_)
        if (not rss_):
            self.debug(str("Cache doesn't contain: ") + str(url_) + str(" (cache option: ") + str(cache_option_) + str(")"))
            return 0
        # end if
        return rss_
    # end def get
    #// =======================================================================*\
#// Function:   check_cache
    #// Purpose:    check a url for membership in the cache
    #// and whether the object is older then MAX_AGE (ie. STALE)
    #// Input:      url from which the rss file was fetched
    #// Output:     cached object on HIT, false on MISS
    #// \*=======================================================================
    def check_cache(self, url_=None):
        
        
        self.ERROR = ""
        cache_option_ = "rss_" + self.file_name(url_)
        if get_transient(cache_option_):
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
    def serialize(self, rss_=None):
        
        
        return serialize(rss_)
    # end def serialize
    #// =======================================================================*\
#// Function:   unserialize
    #// \*=======================================================================
    def unserialize(self, data_=None):
        
        
        return unserialize(data_)
    # end def unserialize
    #// =======================================================================*\
#// Function:   file_name
    #// Purpose:    map url to location in cache
    #// Input:      url from which the rss file was fetched
    #// Output:     a file name
    #// \*=======================================================================
    def file_name(self, url_=None):
        
        
        return php_md5(url_)
    # end def file_name
    #// =======================================================================*\
#// Function:   error
    #// Purpose:    register error
    #// \*=======================================================================
    def error(self, errormsg_=None, lvl_=None):
        if lvl_ is None:
            lvl_ = E_USER_WARNING
        # end if
        
        #// append PHP's error message if track_errors enabled
        if (php_isset(lambda : php_errormsg_)):
            errormsg_ += str(" (") + str(php_errormsg_) + str(")")
        # end if
        self.ERROR = errormsg_
        if MAGPIE_DEBUG:
            trigger_error(errormsg_, lvl_)
        else:
            php_error_log(errormsg_, 0)
        # end if
    # end def error
    def debug(self, debugmsg_=None, lvl_=None):
        if lvl_ is None:
            lvl_ = E_USER_NOTICE
        # end if
        
        if MAGPIE_DEBUG:
            self.error(str("MagpieRSS [debug] ") + str(debugmsg_), lvl_)
        # end if
    # end def debug
# end class RSSCache
if (not php_function_exists("parse_w3cdtf")):
    def parse_w3cdtf(date_str_=None, *_args_):
        
        
        #// # regex to match wc3dtf
        pat_ = "/(\\d{4})-(\\d{2})-(\\d{2})T(\\d{2}):(\\d{2})(:(\\d{2}))?(?:([-+])(\\d{2}):?(\\d{2})|(Z))?/"
        if php_preg_match(pat_, date_str_, match_):
            year_, month_, day_, hours_, minutes_, seconds_ = Array(match_[1], match_[2], match_[3], match_[4], match_[5], match_[7])
            #// # calc epoch for current date assuming GMT
            epoch_ = gmmktime(hours_, minutes_, seconds_, month_, day_, year_)
            offset_ = 0
            if match_[11] == "Z":
                pass
            else:
                tz_mod_, tz_hour_, tz_min_ = Array(match_[8], match_[9], match_[10])
                #// # zero out the variables
                if (not tz_hour_):
                    tz_hour_ = 0
                # end if
                if (not tz_min_):
                    tz_min_ = 0
                # end if
                offset_secs_ = tz_hour_ * 60 + tz_min_ * 60
                #// # is timezone ahead of GMT?  then subtract offset
                #// #
                if tz_mod_ == "+":
                    offset_secs_ = offset_secs_ * -1
                # end if
                offset_ = offset_secs_
            # end if
            epoch_ = epoch_ + offset_
            return epoch_
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
    def wp_rss(url_=None, num_items_=None, *_args_):
        if num_items_ is None:
            num_items_ = -1
        # end if
        
        rss_ = fetch_rss(url_)
        if rss_:
            php_print("<ul>")
            if num_items_ != -1:
                rss_.items = php_array_slice(rss_.items, 0, num_items_)
            # end if
            for item_ in rss_.items:
                printf("<li><a href=\"%1$s\" title=\"%2$s\">%3$s</a></li>", esc_url(item_["link"]), esc_attr(strip_tags(item_["description"])), esc_html(item_["title"]))
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
    def get_rss(url_=None, num_items_=5, *_args_):
        
        
        #// Like get posts, but for RSS
        rss_ = fetch_rss(url_)
        if rss_:
            rss_.items = php_array_slice(rss_.items, 0, num_items_)
            for item_ in rss_.items:
                php_print("<li>\n")
                php_print(str("<a href='") + str(item_["link"]) + str("' title='") + str(item_["description"]) + str("'>"))
                php_print(esc_html(item_["title"]))
                php_print("</a><br />\n")
                php_print("</li>\n")
            # end for
        else:
            return False
        # end if
    # end def get_rss
# end if
