#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
if (not php_class_exists("SimplePie", False)):
    #// Load classes we will need.
    php_include_file(ABSPATH + WPINC + "/SimplePie/Misc.php", once=False)
    php_include_file(ABSPATH + WPINC + "/SimplePie/Cache.php", once=False)
    php_include_file(ABSPATH + WPINC + "/SimplePie/File.php", once=False)
    php_include_file(ABSPATH + WPINC + "/SimplePie/Sanitize.php", once=False)
    php_include_file(ABSPATH + WPINC + "/SimplePie/Registry.php", once=False)
    php_include_file(ABSPATH + WPINC + "/SimplePie/IRI.php", once=False)
    php_include_file(ABSPATH + WPINC + "/SimplePie/Locator.php", once=False)
    php_include_file(ABSPATH + WPINC + "/SimplePie/Content/Type/Sniffer.php", once=False)
    php_include_file(ABSPATH + WPINC + "/SimplePie/XML/Declaration/Parser.php", once=False)
    php_include_file(ABSPATH + WPINC + "/SimplePie/Parser.php", once=False)
    php_include_file(ABSPATH + WPINC + "/SimplePie/Item.php", once=False)
    php_include_file(ABSPATH + WPINC + "/SimplePie/Parse/Date.php", once=False)
    php_include_file(ABSPATH + WPINC + "/SimplePie/Author.php", once=False)
    #// 
    #// WordPress autoloader for SimplePie.
    #// 
    #// @since 3.5.0
    #//
    def wp_simplepie_autoload(class_=None, *_args_):
        
        
        if 0 != php_strpos(class_, "SimplePie_"):
            return
        # end if
        file_ = ABSPATH + WPINC + "/" + php_str_replace("_", "/", class_) + ".php"
        php_include_file(file_, once=False)
    # end def wp_simplepie_autoload
    #// 
    #// We autoload classes we may not need.
    #//
    php_spl_autoload_register("wp_simplepie_autoload")
    #// 
    #// SimplePie
    #// 
    #// A PHP-Based RSS and Atom Feed Framework.
    #// Takes the hard work out of managing a complete RSS/Atom solution.
    #// 
    #// Copyright (c) 2004-2012, Ryan Parman, Geoffrey Sneddon, Ryan McCue, and contributors
    #// All rights reserved.
    #// 
    #// Redistribution and use in source and binary forms, with or without modification, are
    #// permitted provided that the following conditions are met:
    #// 
    #// Redistributions of source code must retain the above copyright notice, this list of
    #// conditions and the following disclaimer.
    #// 
    #// Redistributions in binary form must reproduce the above copyright notice, this list
    #// of conditions and the following disclaimer in the documentation and/or other materials
    #// provided with the distribution.
    #// 
    #// Neither the name of the SimplePie Team nor the names of its contributors may be used
    #// to endorse or promote products derived from this software without specific prior
    #// written permission.
    #// 
    #// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS
    #// OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
    #// AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS
    #// AND CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
    #// CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    #// SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
    #// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
    #// OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
    #// POSSIBILITY OF SUCH DAMAGE.
    #// 
    #// @package SimplePie
    #// @version 1.3.1
    #// @copyright 2004-2012 Ryan Parman, Geoffrey Sneddon, Ryan McCue
    #// @author Ryan Parman
    #// @author Geoffrey Sneddon
    #// @author Ryan McCue
    #// @link http://simplepie.org/ SimplePie
    #// @license http://www.opensource.org/licenses/bsd-license.php BSD License
    #// 
    #// 
    #// SimplePie Name
    #//
    php_define("SIMPLEPIE_NAME", "SimplePie")
    #// 
    #// SimplePie Version
    #//
    php_define("SIMPLEPIE_VERSION", "1.3.1")
    #// 
    #// SimplePie Build
    #// @todo Hardcode for release (there's no need to have to call SimplePie_Misc::get_build() only every load of simplepie.inc)
    #//
    php_define("SIMPLEPIE_BUILD", gmdate("YmdHis", SimplePie_Misc.get_build()))
    #// 
    #// SimplePie Website URL
    #//
    php_define("SIMPLEPIE_URL", "http://simplepie.org")
    #// 
    #// SimplePie Useragent
    #// @see SimplePie::set_useragent()
    #//
    php_define("SIMPLEPIE_USERAGENT", SIMPLEPIE_NAME + "/" + SIMPLEPIE_VERSION + " (Feed Parser; " + SIMPLEPIE_URL + "; Allow like Gecko) Build/" + SIMPLEPIE_BUILD)
    #// 
    #// SimplePie Linkback
    #//
    php_define("SIMPLEPIE_LINKBACK", "<a href=\"" + SIMPLEPIE_URL + "\" title=\"" + SIMPLEPIE_NAME + " " + SIMPLEPIE_VERSION + "\">" + SIMPLEPIE_NAME + "</a>")
    #// 
    #// No Autodiscovery
    #// @see SimplePie::set_autodiscovery_level()
    #//
    php_define("SIMPLEPIE_LOCATOR_NONE", 0)
    #// 
    #// Feed Link Element Autodiscovery
    #// @see SimplePie::set_autodiscovery_level()
    #//
    php_define("SIMPLEPIE_LOCATOR_AUTODISCOVERY", 1)
    #// 
    #// Local Feed Extension Autodiscovery
    #// @see SimplePie::set_autodiscovery_level()
    #//
    php_define("SIMPLEPIE_LOCATOR_LOCAL_EXTENSION", 2)
    #// 
    #// Local Feed Body Autodiscovery
    #// @see SimplePie::set_autodiscovery_level()
    #//
    php_define("SIMPLEPIE_LOCATOR_LOCAL_BODY", 4)
    #// 
    #// Remote Feed Extension Autodiscovery
    #// @see SimplePie::set_autodiscovery_level()
    #//
    php_define("SIMPLEPIE_LOCATOR_REMOTE_EXTENSION", 8)
    #// 
    #// Remote Feed Body Autodiscovery
    #// @see SimplePie::set_autodiscovery_level()
    #//
    php_define("SIMPLEPIE_LOCATOR_REMOTE_BODY", 16)
    #// 
    #// All Feed Autodiscovery
    #// @see SimplePie::set_autodiscovery_level()
    #//
    php_define("SIMPLEPIE_LOCATOR_ALL", 31)
    #// 
    #// No known feed type
    #//
    php_define("SIMPLEPIE_TYPE_NONE", 0)
    #// 
    #// RSS 0.90
    #//
    php_define("SIMPLEPIE_TYPE_RSS_090", 1)
    #// 
    #// RSS 0.91 (Netscape)
    #//
    php_define("SIMPLEPIE_TYPE_RSS_091_NETSCAPE", 2)
    #// 
    #// RSS 0.91 (Userland)
    #//
    php_define("SIMPLEPIE_TYPE_RSS_091_USERLAND", 4)
    #// 
    #// RSS 0.91 (both Netscape and Userland)
    #//
    php_define("SIMPLEPIE_TYPE_RSS_091", 6)
    #// 
    #// RSS 0.92
    #//
    php_define("SIMPLEPIE_TYPE_RSS_092", 8)
    #// 
    #// RSS 0.93
    #//
    php_define("SIMPLEPIE_TYPE_RSS_093", 16)
    #// 
    #// RSS 0.94
    #//
    php_define("SIMPLEPIE_TYPE_RSS_094", 32)
    #// 
    #// RSS 1.0
    #//
    php_define("SIMPLEPIE_TYPE_RSS_10", 64)
    #// 
    #// RSS 2.0
    #//
    php_define("SIMPLEPIE_TYPE_RSS_20", 128)
    #// 
    #// RDF-based RSS
    #//
    php_define("SIMPLEPIE_TYPE_RSS_RDF", 65)
    #// 
    #// Non-RDF-based RSS (truly intended as syndication format)
    #//
    php_define("SIMPLEPIE_TYPE_RSS_SYNDICATION", 190)
    #// 
    #// All RSS
    #//
    php_define("SIMPLEPIE_TYPE_RSS_ALL", 255)
    #// 
    #// Atom 0.3
    #//
    php_define("SIMPLEPIE_TYPE_ATOM_03", 256)
    #// 
    #// Atom 1.0
    #//
    php_define("SIMPLEPIE_TYPE_ATOM_10", 512)
    #// 
    #// All Atom
    #//
    php_define("SIMPLEPIE_TYPE_ATOM_ALL", 768)
    #// 
    #// All feed types
    #//
    php_define("SIMPLEPIE_TYPE_ALL", 1023)
    #// 
    #// No construct
    #//
    php_define("SIMPLEPIE_CONSTRUCT_NONE", 0)
    #// 
    #// Text construct
    #//
    php_define("SIMPLEPIE_CONSTRUCT_TEXT", 1)
    #// 
    #// HTML construct
    #//
    php_define("SIMPLEPIE_CONSTRUCT_HTML", 2)
    #// 
    #// XHTML construct
    #//
    php_define("SIMPLEPIE_CONSTRUCT_XHTML", 4)
    #// 
    #// base64-encoded construct
    #//
    php_define("SIMPLEPIE_CONSTRUCT_BASE64", 8)
    #// 
    #// IRI construct
    #//
    php_define("SIMPLEPIE_CONSTRUCT_IRI", 16)
    #// 
    #// A construct that might be HTML
    #//
    php_define("SIMPLEPIE_CONSTRUCT_MAYBE_HTML", 32)
    #// 
    #// All constructs
    #//
    php_define("SIMPLEPIE_CONSTRUCT_ALL", 63)
    #// 
    #// Don't change case
    #//
    php_define("SIMPLEPIE_SAME_CASE", 1)
    #// 
    #// Change to lowercase
    #//
    php_define("SIMPLEPIE_LOWERCASE", 2)
    #// 
    #// Change to uppercase
    #//
    php_define("SIMPLEPIE_UPPERCASE", 4)
    #// 
    #// PCRE for HTML attributes
    #//
    php_define("SIMPLEPIE_PCRE_HTML_ATTRIBUTE", "((?:[\\x09\\x0A\\x0B\\x0C\\x0D\\x20]+[^\\x09\\x0A\\x0B\\x0C\\x0D\\x20\\x2F\\x3E][^\\x09\\x0A\\x0B\\x0C\\x0D\\x20\\x2F\\x3D\\x3E]*(?:[\\x09\\x0A\\x0B\\x0C\\x0D\\x20]*=[\\x09\\x0A\\x0B\\x0C\\x0D\\x20]*(?:\"(?:[^\"]*)\"|'(?:[^']*)'|(?:[^\\x09\\x0A\\x0B\\x0C\\x0D\\x20\\x22\\x27\\x3E][^\\x09\\x0A\\x0B\\x0C\\x0D\\x20\\x3E]*)?))?)*)[\\x09\\x0A\\x0B\\x0C\\x0D\\x20]*")
    #// 
    #// PCRE for XML attributes
    #//
    php_define("SIMPLEPIE_PCRE_XML_ATTRIBUTE", "((?:\\s+(?:(?:[^\\s:]+:)?[^\\s:]+)\\s*=\\s*(?:\"(?:[^\"]*)\"|'(?:[^']*)'))*)\\s*")
    #// 
    #// XML Namespace
    #//
    php_define("SIMPLEPIE_NAMESPACE_XML", "http://www.w3.org/XML/1998/namespace")
    #// 
    #// Atom 1.0 Namespace
    #//
    php_define("SIMPLEPIE_NAMESPACE_ATOM_10", "http://www.w3.org/2005/Atom")
    #// 
    #// Atom 0.3 Namespace
    #//
    php_define("SIMPLEPIE_NAMESPACE_ATOM_03", "http://purl.org/atom/ns#")
    #// 
    #// RDF Namespace
    #//
    php_define("SIMPLEPIE_NAMESPACE_RDF", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    #// 
    #// RSS 0.90 Namespace
    #//
    php_define("SIMPLEPIE_NAMESPACE_RSS_090", "http://my.netscape.com/rdf/simple/0.9/")
    #// 
    #// RSS 1.0 Namespace
    #//
    php_define("SIMPLEPIE_NAMESPACE_RSS_10", "http://purl.org/rss/1.0/")
    #// 
    #// RSS 1.0 Content Module Namespace
    #//
    php_define("SIMPLEPIE_NAMESPACE_RSS_10_MODULES_CONTENT", "http://purl.org/rss/1.0/modules/content/")
    #// 
    #// RSS 2.0 Namespace
    #// (Stupid, I know, but I'm certain it will confuse people less with support.)
    #//
    php_define("SIMPLEPIE_NAMESPACE_RSS_20", "")
    #// 
    #// DC 1.0 Namespace
    #//
    php_define("SIMPLEPIE_NAMESPACE_DC_10", "http://purl.org/dc/elements/1.0/")
    #// 
    #// DC 1.1 Namespace
    #//
    php_define("SIMPLEPIE_NAMESPACE_DC_11", "http://purl.org/dc/elements/1.1/")
    #// 
    #// W3C Basic Geo (WGS84 lat/long) Vocabulary Namespace
    #//
    php_define("SIMPLEPIE_NAMESPACE_W3C_BASIC_GEO", "http://www.w3.org/2003/01/geo/wgs84_pos#")
    #// 
    #// GeoRSS Namespace
    #//
    php_define("SIMPLEPIE_NAMESPACE_GEORSS", "http://www.georss.org/georss")
    #// 
    #// Media RSS Namespace
    #//
    php_define("SIMPLEPIE_NAMESPACE_MEDIARSS", "http://search.yahoo.com/mrss/")
    #// 
    #// Wrong Media RSS Namespace. Caused by a long-standing typo in the spec.
    #//
    php_define("SIMPLEPIE_NAMESPACE_MEDIARSS_WRONG", "http://search.yahoo.com/mrss")
    #// 
    #// Wrong Media RSS Namespace #2. New namespace introduced in Media RSS 1.5.
    #//
    php_define("SIMPLEPIE_NAMESPACE_MEDIARSS_WRONG2", "http://video.search.yahoo.com/mrss")
    #// 
    #// Wrong Media RSS Namespace #3. A possible typo of the Media RSS 1.5 namespace.
    #//
    php_define("SIMPLEPIE_NAMESPACE_MEDIARSS_WRONG3", "http://video.search.yahoo.com/mrss/")
    #// 
    #// Wrong Media RSS Namespace #4. New spec location after the RSS Advisory Board takes it over, but not a valid namespace.
    #//
    php_define("SIMPLEPIE_NAMESPACE_MEDIARSS_WRONG4", "http://www.rssboard.org/media-rss")
    #// 
    #// Wrong Media RSS Namespace #5. A possible typo of the RSS Advisory Board URL.
    #//
    php_define("SIMPLEPIE_NAMESPACE_MEDIARSS_WRONG5", "http://www.rssboard.org/media-rss/")
    #// 
    #// iTunes RSS Namespace
    #//
    php_define("SIMPLEPIE_NAMESPACE_ITUNES", "http://www.itunes.com/dtds/podcast-1.0.dtd")
    #// 
    #// XHTML Namespace
    #//
    php_define("SIMPLEPIE_NAMESPACE_XHTML", "http://www.w3.org/1999/xhtml")
    #// 
    #// IANA Link Relations Registry
    #//
    php_define("SIMPLEPIE_IANA_LINK_RELATIONS_REGISTRY", "http://www.iana.org/assignments/relation/")
    #// 
    #// No file source
    #//
    php_define("SIMPLEPIE_FILE_SOURCE_NONE", 0)
    #// 
    #// Remote file source
    #//
    php_define("SIMPLEPIE_FILE_SOURCE_REMOTE", 1)
    #// 
    #// Local file source
    #//
    php_define("SIMPLEPIE_FILE_SOURCE_LOCAL", 2)
    #// 
    #// fsockopen() file source
    #//
    php_define("SIMPLEPIE_FILE_SOURCE_FSOCKOPEN", 4)
    #// 
    #// cURL file source
    #//
    php_define("SIMPLEPIE_FILE_SOURCE_CURL", 8)
    #// 
    #// file_get_contents() file source
    #//
    php_define("SIMPLEPIE_FILE_SOURCE_FILE_GET_CONTENTS", 16)
    #// 
    #// SimplePie
    #// 
    #// @package SimplePie
    #// @subpackage API
    #//
    class SimplePie():
        #// 
        #// @var array Raw data
        #// @access private
        #//
        data = Array()
        #// 
        #// @var mixed Error string
        #// @access private
        #//
        error = Array()
        #// 
        #// @var object Instance of SimplePie_Sanitize (or other class)
        #// @see SimplePie::set_sanitize_class()
        #// @access private
        #//
        sanitize = Array()
        #// 
        #// @var string SimplePie Useragent
        #// @see SimplePie::set_useragent()
        #// @access private
        #//
        useragent = SIMPLEPIE_USERAGENT
        #// 
        #// @var string Feed URL
        #// @see SimplePie::set_feed_url()
        #// @access private
        #//
        feed_url = Array()
        #// 
        #// @var object Instance of SimplePie_File to use as a feed
        #// @see SimplePie::set_file()
        #// @access private
        #//
        file_ = Array()
        #// 
        #// @var string Raw feed data
        #// @see SimplePie::set_raw_data()
        #// @access private
        #//
        raw_data = Array()
        #// 
        #// @var int Timeout for fetching remote files
        #// @see SimplePie::set_timeout()
        #// @access private
        #//
        timeout = 10
        #// 
        #// @var bool Forces fsockopen() to be used for remote files instead
        #// of cURL, even if a new enough version is installed
        #// @see SimplePie::force_fsockopen()
        #// @access private
        #//
        force_fsockopen = False
        #// 
        #// @var bool Force the given data/URL to be treated as a feed no matter what
        #// it appears like
        #// @see SimplePie::force_feed()
        #// @access private
        #//
        force_feed = False
        #// 
        #// @var bool Enable/Disable Caching
        #// @see SimplePie::enable_cache()
        #// @access private
        #//
        cache = True
        #// 
        #// @var int Cache duration (in seconds)
        #// @see SimplePie::set_cache_duration()
        #// @access private
        #//
        cache_duration = 3600
        #// 
        #// @var int Auto-discovery cache duration (in seconds)
        #// @see SimplePie::set_autodiscovery_cache_duration()
        #// @access private
        #//
        autodiscovery_cache_duration = 604800
        #// 7 Days.
        #// 
        #// @var string Cache location (relative to executing script)
        #// @see SimplePie::set_cache_location()
        #// @access private
        #//
        cache_location = "./cache"
        #// 
        #// @var string Function that creates the cache filename
        #// @see SimplePie::set_cache_name_function()
        #// @access private
        #//
        cache_name_function = "md5"
        #// 
        #// @var bool Reorder feed by date descending
        #// @see SimplePie::enable_order_by_date()
        #// @access private
        #//
        order_by_date = True
        #// 
        #// @var mixed Force input encoding to be set to the follow value
        #// (false, or anything type-cast to false, disables this feature)
        #// @see SimplePie::set_input_encoding()
        #// @access private
        #//
        input_encoding = False
        #// 
        #// @var int Feed Autodiscovery Level
        #// @see SimplePie::set_autodiscovery_level()
        #// @access private
        #//
        autodiscovery = SIMPLEPIE_LOCATOR_ALL
        #// 
        #// Class registry object
        #// 
        #// @var SimplePie_Registry
        #//
        registry = Array()
        #// 
        #// @var int Maximum number of feeds to check with autodiscovery
        #// @see SimplePie::set_max_checked_feeds()
        #// @access private
        #//
        max_checked_feeds = 10
        #// 
        #// @var array All the feeds found during the autodiscovery process
        #// @see SimplePie::get_all_discovered_feeds()
        #// @access private
        #//
        all_discovered_feeds = Array()
        #// 
        #// @var string Web-accessible path to the handler_image.php file.
        #// @see SimplePie::set_image_handler()
        #// @access private
        #//
        image_handler = ""
        #// 
        #// @var array Stores the URLs when multiple feeds are being initialized.
        #// @see SimplePie::set_feed_url()
        #// @access private
        #//
        multifeed_url = Array()
        #// 
        #// @var array Stores SimplePie objects when multiple feeds initialized.
        #// @access private
        #//
        multifeed_objects = Array()
        #// 
        #// @var array Stores the get_object_vars() array for use with multifeeds.
        #// @see SimplePie::set_feed_url()
        #// @access private
        #//
        config_settings = None
        #// 
        #// @var integer Stores the number of items to return per-feed with multifeeds.
        #// @see SimplePie::set_item_limit()
        #// @access private
        #//
        item_limit = 0
        #// 
        #// @var array Stores the default attributes to be stripped by strip_attributes().
        #// @see SimplePie::strip_attributes()
        #// @access private
        #//
        strip_attributes = Array("bgsound", "class", "expr", "id", "style", "onclick", "onerror", "onfinish", "onmouseover", "onmouseout", "onfocus", "onblur", "lowsrc", "dynsrc")
        #// 
        #// @var array Stores the default tags to be stripped by strip_htmltags().
        #// @see SimplePie::strip_htmltags()
        #// @access private
        #//
        strip_htmltags = Array("base", "blink", "body", "doctype", "embed", "font", "form", "frame", "frameset", "html", "iframe", "input", "marquee", "meta", "noscript", "object", "param", "script", "style")
        #// 
        #// The SimplePie class contains feed level data and options
        #// 
        #// To use SimplePie, create the SimplePie object with no parameters. You can
        #// then set configuration options using the provided methods. After setting
        #// them, you must initialise the feed using $feed->init(). At that point the
        #// object's methods and properties will be available to you.
        #// 
        #// Previously, it was possible to pass in the feed URL along with cache
        #// options directly into the constructor. This has been removed as of 1.3 as
        #// it caused a lot of confusion.
        #// 
        #// @since 1.0 Preview Release
        #//
        def __init__(self):
            
            
            if php_version_compare(PHP_VERSION, "5.2", "<"):
                trigger_error("PHP 4.x, 5.0 and 5.1 are no longer supported. Please upgrade to PHP 5.2 or newer.")
                php_exit(0)
            # end if
            #// Other objects, instances created here so we can set options on them
            self.sanitize = php_new_class("SimplePie_Sanitize", lambda : SimplePie_Sanitize())
            self.registry = php_new_class("SimplePie_Registry", lambda : SimplePie_Registry())
            if php_func_num_args() > 0:
                level_ = E_USER_DEPRECATED if php_defined("E_USER_DEPRECATED") else E_USER_WARNING
                trigger_error("Passing parameters to the constructor is no longer supported. Please use set_feed_url(), set_cache_location(), and set_cache_location() directly.", level_)
                args_ = php_func_get_args()
                for case in Switch(php_count(args_)):
                    if case(3):
                        self.set_cache_duration(args_[2])
                    # end if
                    if case(2):
                        self.set_cache_location(args_[1])
                    # end if
                    if case(1):
                        self.set_feed_url(args_[0])
                        self.init()
                    # end if
                # end for
            # end if
        # end def __init__
        #// 
        #// Used for converting object to a string
        #//
        def __tostring(self):
            
            
            return php_md5(serialize(self.data))
        # end def __tostring
        #// 
        #// Remove items that link back to this before destroying this object
        #//
        def __del__(self):
            
            
            if php_version_compare(PHP_VERSION, "5.3", "<") or (not php_gc_enabled()) and (not php_ini_get("zend.ze1_compatibility_mode")):
                if (not php_empty(lambda : self.data["items"])):
                    for item_ in self.data["items"]:
                        item_.__del__()
                    # end for
                    item_ = None
                    self.data["items"] = None
                # end if
                if (not php_empty(lambda : self.data["ordered_items"])):
                    for item_ in self.data["ordered_items"]:
                        item_.__del__()
                    # end for
                    item_ = None
                    self.data["ordered_items"] = None
                # end if
            # end if
        # end def __del__
        #// 
        #// Force the given data/URL to be treated as a feed
        #// 
        #// This tells SimplePie to ignore the content-type provided by the server.
        #// Be careful when using this option, as it will also disable autodiscovery.
        #// 
        #// @since 1.1
        #// @param bool $enable Force the given data/URL to be treated as a feed
        #//
        def force_feed(self, enable_=None):
            if enable_ is None:
                enable_ = False
            # end if
            
            self.force_feed = php_bool(enable_)
        # end def force_feed
        #// 
        #// Set the URL of the feed you want to parse
        #// 
        #// This allows you to enter the URL of the feed you want to parse, or the
        #// website you want to try to use auto-discovery on. This takes priority
        #// over any set raw data.
        #// 
        #// You can set multiple feeds to mash together by passing an array instead
        #// of a string for the $url. Remember that with each additional feed comes
        #// additional processing and resources.
        #// 
        #// @since 1.0 Preview Release
        #// @see set_raw_data()
        #// @param string|array $url This is the URL (or array of URLs) that you want to parse.
        #//
        def set_feed_url(self, url_=None):
            
            
            self.multifeed_url = Array()
            if php_is_array(url_):
                for value_ in url_:
                    self.multifeed_url[-1] = self.registry.call("Misc", "fix_protocol", Array(value_, 1))
                # end for
            else:
                self.feed_url = self.registry.call("Misc", "fix_protocol", Array(url_, 1))
            # end if
        # end def set_feed_url
        #// 
        #// Set an instance of {@see SimplePie_File} to use as a feed
        #// 
        #// @param SimplePie_File &$file
        #// @return bool True on success, false on failure
        #//
        def set_file(self, file_=None):
            
            
            if type(file_).__name__ == "SimplePie_File":
                self.feed_url = file_.url
                self.file_ = file_
                return True
            # end if
            return False
        # end def set_file
        #// 
        #// Set the raw XML data to parse
        #// 
        #// Allows you to use a string of RSS/Atom data instead of a remote feed.
        #// 
        #// If you have a feed available as a string in PHP, you can tell SimplePie
        #// to parse that data string instead of a remote feed. Any set feed URL
        #// takes precedence.
        #// 
        #// @since 1.0 Beta 3
        #// @param string $data RSS or Atom data as a string.
        #// @see set_feed_url()
        #//
        def set_raw_data(self, data_=None):
            
            
            self.raw_data = data_
        # end def set_raw_data
        #// 
        #// Set the the default timeout for fetching remote feeds
        #// 
        #// This allows you to change the maximum time the feed's server to respond
        #// and send the feed back.
        #// 
        #// @since 1.0 Beta 3
        #// @param int $timeout The maximum number of seconds to spend waiting to retrieve a feed.
        #//
        def set_timeout(self, timeout_=10):
            
            
            self.timeout = php_int(timeout_)
        # end def set_timeout
        #// 
        #// Force SimplePie to use fsockopen() instead of cURL
        #// 
        #// @since 1.0 Beta 3
        #// @param bool $enable Force fsockopen() to be used
        #//
        def force_fsockopen(self, enable_=None):
            if enable_ is None:
                enable_ = False
            # end if
            
            self.force_fsockopen = php_bool(enable_)
        # end def force_fsockopen
        #// 
        #// Enable/disable caching in SimplePie.
        #// 
        #// This option allows you to disable caching all-together in SimplePie.
        #// However, disabling the cache can lead to longer load times.
        #// 
        #// @since 1.0 Preview Release
        #// @param bool $enable Enable caching
        #//
        def enable_cache(self, enable_=None):
            if enable_ is None:
                enable_ = True
            # end if
            
            self.cache = php_bool(enable_)
        # end def enable_cache
        #// 
        #// Set the length of time (in seconds) that the contents of a feed will be
        #// cached
        #// 
        #// @param int $seconds The feed content cache duration
        #//
        def set_cache_duration(self, seconds_=3600):
            
            
            self.cache_duration = php_int(seconds_)
        # end def set_cache_duration
        #// 
        #// Set the length of time (in seconds) that the autodiscovered feed URL will
        #// be cached
        #// 
        #// @param int $seconds The autodiscovered feed URL cache duration.
        #//
        def set_autodiscovery_cache_duration(self, seconds_=604800):
            
            
            self.autodiscovery_cache_duration = php_int(seconds_)
        # end def set_autodiscovery_cache_duration
        #// 
        #// Set the file system location where the cached files should be stored
        #// 
        #// @param string $location The file system location.
        #//
        def set_cache_location(self, location_="./cache"):
            
            
            self.cache_location = php_str(location_)
        # end def set_cache_location
        #// 
        #// Set whether feed items should be sorted into reverse chronological order
        #// 
        #// @param bool $enable Sort as reverse chronological order.
        #//
        def enable_order_by_date(self, enable_=None):
            if enable_ is None:
                enable_ = True
            # end if
            
            self.order_by_date = php_bool(enable_)
        # end def enable_order_by_date
        #// 
        #// Set the character encoding used to parse the feed
        #// 
        #// This overrides the encoding reported by the feed, however it will fall
        #// back to the normal encoding detection if the override fails
        #// 
        #// @param string $encoding Character encoding
        #//
        def set_input_encoding(self, encoding_=None):
            if encoding_ is None:
                encoding_ = False
            # end if
            
            if encoding_:
                self.input_encoding = php_str(encoding_)
            else:
                self.input_encoding = False
            # end if
        # end def set_input_encoding
        #// 
        #// Set how much feed autodiscovery to do
        #// 
        #// @see SIMPLEPIE_LOCATOR_NONE
        #// @see SIMPLEPIE_LOCATOR_AUTODISCOVERY
        #// @see SIMPLEPIE_LOCATOR_LOCAL_EXTENSION
        #// @see SIMPLEPIE_LOCATOR_LOCAL_BODY
        #// @see SIMPLEPIE_LOCATOR_REMOTE_EXTENSION
        #// @see SIMPLEPIE_LOCATOR_REMOTE_BODY
        #// @see SIMPLEPIE_LOCATOR_ALL
        #// @param int $level Feed Autodiscovery Level (level can be a combination of the above constants, see bitwise OR operator)
        #//
        def set_autodiscovery_level(self, level_=None):
            if level_ is None:
                level_ = SIMPLEPIE_LOCATOR_ALL
            # end if
            
            self.autodiscovery = php_int(level_)
        # end def set_autodiscovery_level
        #// 
        #// Get the class registry
        #// 
        #// Use this to override SimplePie's default classes
        #// @see SimplePie_Registry
        #// @return SimplePie_Registry
        #//
        def get_registry(self):
            
            
            return self.registry
        # end def get_registry
        #// #@+
        #// Useful when you are overloading or extending SimplePie's default classes.
        #// 
        #// @deprecated Use {@see get_registry()} instead
        #// @link http://php.net/manual/en/language.oop5.basic.php#language.oop5.basic.extends PHP5 extends documentation
        #// @param string $class Name of custom class
        #// @return boolean True on success, false otherwise
        #// 
        #// 
        #// Set which class SimplePie uses for caching
        #//
        def set_cache_class(self, class_="SimplePie_Cache"):
            
            
            return self.registry.register("Cache", class_, True)
        # end def set_cache_class
        #// 
        #// Set which class SimplePie uses for auto-discovery
        #//
        def set_locator_class(self, class_="SimplePie_Locator"):
            
            
            return self.registry.register("Locator", class_, True)
        # end def set_locator_class
        #// 
        #// Set which class SimplePie uses for XML parsing
        #//
        def set_parser_class(self, class_="SimplePie_Parser"):
            
            
            return self.registry.register("Parser", class_, True)
        # end def set_parser_class
        #// 
        #// Set which class SimplePie uses for remote file fetching
        #//
        def set_file_class(self, class_="SimplePie_File"):
            
            
            return self.registry.register("File", class_, True)
        # end def set_file_class
        #// 
        #// Set which class SimplePie uses for data sanitization
        #//
        def set_sanitize_class(self, class_="SimplePie_Sanitize"):
            
            
            return self.registry.register("Sanitize", class_, True)
        # end def set_sanitize_class
        #// 
        #// Set which class SimplePie uses for handling feed items
        #//
        def set_item_class(self, class_="SimplePie_Item"):
            
            
            return self.registry.register("Item", class_, True)
        # end def set_item_class
        #// 
        #// Set which class SimplePie uses for handling author data
        #//
        def set_author_class(self, class_="SimplePie_Author"):
            
            
            return self.registry.register("Author", class_, True)
        # end def set_author_class
        #// 
        #// Set which class SimplePie uses for handling category data
        #//
        def set_category_class(self, class_="SimplePie_Category"):
            
            
            return self.registry.register("Category", class_, True)
        # end def set_category_class
        #// 
        #// Set which class SimplePie uses for feed enclosures
        #//
        def set_enclosure_class(self, class_="SimplePie_Enclosure"):
            
            
            return self.registry.register("Enclosure", class_, True)
        # end def set_enclosure_class
        #// 
        #// Set which class SimplePie uses for `<media:text>` captions
        #//
        def set_caption_class(self, class_="SimplePie_Caption"):
            
            
            return self.registry.register("Caption", class_, True)
        # end def set_caption_class
        #// 
        #// Set which class SimplePie uses for `<media:copyright>`
        #//
        def set_copyright_class(self, class_="SimplePie_Copyright"):
            
            
            return self.registry.register("Copyright", class_, True)
        # end def set_copyright_class
        #// 
        #// Set which class SimplePie uses for `<media:credit>`
        #//
        def set_credit_class(self, class_="SimplePie_Credit"):
            
            
            return self.registry.register("Credit", class_, True)
        # end def set_credit_class
        #// 
        #// Set which class SimplePie uses for `<media:rating>`
        #//
        def set_rating_class(self, class_="SimplePie_Rating"):
            
            
            return self.registry.register("Rating", class_, True)
        # end def set_rating_class
        #// 
        #// Set which class SimplePie uses for `<media:restriction>`
        #//
        def set_restriction_class(self, class_="SimplePie_Restriction"):
            
            
            return self.registry.register("Restriction", class_, True)
        # end def set_restriction_class
        #// 
        #// Set which class SimplePie uses for content-type sniffing
        #//
        def set_content_type_sniffer_class(self, class_="SimplePie_Content_Type_Sniffer"):
            
            
            return self.registry.register("Content_Type_Sniffer", class_, True)
        # end def set_content_type_sniffer_class
        #// 
        #// Set which class SimplePie uses item sources
        #//
        def set_source_class(self, class_="SimplePie_Source"):
            
            
            return self.registry.register("Source", class_, True)
        # end def set_source_class
        #// #@-
        #// 
        #// Set the user agent string
        #// 
        #// @param string $ua New user agent string.
        #//
        def set_useragent(self, ua_=None):
            if ua_ is None:
                ua_ = SIMPLEPIE_USERAGENT
            # end if
            
            self.useragent = php_str(ua_)
        # end def set_useragent
        #// 
        #// Set callback function to create cache filename with
        #// 
        #// @param mixed $function Callback function
        #//
        def set_cache_name_function(self, function_="md5"):
            
            
            if php_is_callable(function_):
                self.cache_name_function = function_
            # end if
        # end def set_cache_name_function
        #// 
        #// Set options to make SP as fast as possible
        #// 
        #// Forgoes a substantial amount of data sanitization in favor of speed. This
        #// turns SimplePie into a dumb parser of feeds.
        #// 
        #// @param bool $set Whether to set them or not
        #//
        def set_stupidly_fast(self, set_=None):
            if set_ is None:
                set_ = False
            # end if
            
            if set_:
                self.enable_order_by_date(False)
                self.remove_div(False)
                self.strip_comments(False)
                self.strip_htmltags(False)
                self.strip_attributes(False)
                self.set_image_handler(False)
            # end if
        # end def set_stupidly_fast
        #// 
        #// Set maximum number of feeds to check with autodiscovery
        #// 
        #// @param int $max Maximum number of feeds to check
        #//
        def set_max_checked_feeds(self, max_=10):
            
            
            self.max_checked_feeds = php_int(max_)
        # end def set_max_checked_feeds
        def remove_div(self, enable_=None):
            if enable_ is None:
                enable_ = True
            # end if
            
            self.sanitize.remove_div(enable_)
        # end def remove_div
        def strip_htmltags(self, tags_="", encode_=None):
            
            
            if tags_ == "":
                tags_ = self.strip_htmltags
            # end if
            self.sanitize.strip_htmltags(tags_)
            if encode_ != None:
                self.sanitize.encode_instead_of_strip(tags_)
            # end if
        # end def strip_htmltags
        def encode_instead_of_strip(self, enable_=None):
            if enable_ is None:
                enable_ = True
            # end if
            
            self.sanitize.encode_instead_of_strip(enable_)
        # end def encode_instead_of_strip
        def strip_attributes(self, attribs_=""):
            
            
            if attribs_ == "":
                attribs_ = self.strip_attributes
            # end if
            self.sanitize.strip_attributes(attribs_)
        # end def strip_attributes
        #// 
        #// Set the output encoding
        #// 
        #// Allows you to override SimplePie's output to match that of your webpage.
        #// This is useful for times when your webpages are not being served as
        #// UTF-8.  This setting will be obeyed by {@see handle_content_type()}, and
        #// is similar to {@see set_input_encoding()}.
        #// 
        #// It should be noted, however, that not all character encodings can support
        #// all characters.  If your page is being served as ISO-8859-1 and you try
        #// to display a Japanese feed, you'll likely see garbled characters.
        #// Because of this, it is highly recommended to ensure that your webpages
        #// are served as UTF-8.
        #// 
        #// The number of supported character encodings depends on whether your web
        #// host supports {@link http://php.net/mbstring mbstring},
        #// {@link http://php.net/iconv iconv}, or both. See
        #// {@link http://simplepie.org/wiki/faq/Supported_Character_Encodings} for
        #// more information.
        #// 
        #// @param string $encoding
        #//
        def set_output_encoding(self, encoding_="UTF-8"):
            
            
            self.sanitize.set_output_encoding(encoding_)
        # end def set_output_encoding
        def strip_comments(self, strip_=None):
            if strip_ is None:
                strip_ = False
            # end if
            
            self.sanitize.strip_comments(strip_)
        # end def strip_comments
        #// 
        #// Set element/attribute key/value pairs of HTML attributes
        #// containing URLs that need to be resolved relative to the feed
        #// 
        #// Defaults to |a|@href, |area|@href, |blockquote|@cite, |del|@cite,
        #// |form|@action, |img|@longdesc, |img|@src, |input|@src, |ins|@cite,
        #// |q|@cite
        #// 
        #// @since 1.0
        #// @param array|null $element_attribute Element/attribute key/value pairs, null for default
        #//
        def set_url_replacements(self, element_attribute_=None):
            
            
            self.sanitize.set_url_replacements(element_attribute_)
        # end def set_url_replacements
        #// 
        #// Set the handler to enable the display of cached images.
        #// 
        #// @param str $page Web-accessible path to the handler_image.php file.
        #// @param str $qs The query string that the value should be passed to.
        #//
        def set_image_handler(self, page_=None, qs_="i"):
            if page_ is None:
                page_ = False
            # end if
            
            if page_ != False:
                self.sanitize.set_image_handler(page_ + "?" + qs_ + "=")
            else:
                self.image_handler = ""
            # end if
        # end def set_image_handler
        #// 
        #// Set the limit for items returned per-feed with multifeeds
        #// 
        #// @param integer $limit The maximum number of items to return.
        #//
        def set_item_limit(self, limit_=0):
            
            
            self.item_limit = php_int(limit_)
        # end def set_item_limit
        #// 
        #// Initialize the feed object
        #// 
        #// This is what makes everything happen.  Period.  This is where all of the
        #// configuration options get processed, feeds are fetched, cached, and
        #// parsed, and all of that other good stuff.
        #// 
        #// @return boolean True if successful, false otherwise
        #//
        def init(self):
            
            
            #// Check absolute bare minimum requirements.
            if (not php_extension_loaded("xml")) or (not php_extension_loaded("pcre")):
                return False
                #// Then check the xml extension is sane (i.e., libxml 2.7.x issue on PHP < 5.2.9 and libxml 2.7.0 to 2.7.2 on any version) if we don't have xmlreader.
            elif (not php_extension_loaded("xmlreader")):
                xml_is_sane_ = None
                if xml_is_sane_ == None:
                    parser_check_ = xml_parser_create()
                    xml_parse_into_struct(parser_check_, "<foo>&amp;</foo>", values_)
                    xml_parser_free(parser_check_)
                    xml_is_sane_ = (php_isset(lambda : values_[0]["value"]))
                # end if
                if (not xml_is_sane_):
                    return False
                # end if
            # end if
            if php_method_exists(self.sanitize, "set_registry"):
                self.sanitize.set_registry(self.registry)
            # end if
            #// Pass whatever was set with config options over to the sanitizer.
            #// Pass the classes in for legacy support; new classes should use the registry instead
            self.sanitize.pass_cache_data(self.cache, self.cache_location, self.cache_name_function, self.registry.get_class("Cache"))
            self.sanitize.pass_file_data(self.registry.get_class("File"), self.timeout, self.useragent, self.force_fsockopen)
            if (not php_empty(lambda : self.multifeed_url)):
                i_ = 0
                success_ = 0
                self.multifeed_objects = Array()
                self.error = Array()
                for url_ in self.multifeed_url:
                    self.multifeed_objects[i_] = copy.deepcopy(self)
                    self.multifeed_objects[i_].set_feed_url(url_)
                    single_success_ = self.multifeed_objects[i_].init()
                    success_ |= single_success_
                    if (not single_success_):
                        self.error[i_] = self.multifeed_objects[i_].error()
                    # end if
                    i_ += 1
                # end for
                return php_bool(success_)
            elif self.feed_url == None and self.raw_data == None:
                return False
            # end if
            self.error = None
            self.data = Array()
            self.multifeed_objects = Array()
            cache_ = False
            if self.feed_url != None:
                parsed_feed_url_ = self.registry.call("Misc", "parse_url", Array(self.feed_url))
                #// Decide whether to enable caching
                if self.cache and parsed_feed_url_["scheme"] != "":
                    cache_ = self.registry.call("Cache", "get_handler", Array(self.cache_location, php_call_user_func(self.cache_name_function, self.feed_url), "spc"))
                # end if
                #// Fetch the data via SimplePie_File into $this->raw_data
                fetched_ = self.fetch_data(cache_)
                if fetched_ == True:
                    return True
                elif fetched_ == False:
                    return False
                # end if
                headers_, sniffed_ = fetched_
            # end if
            #// Set up array of possible encodings
            encodings_ = Array()
            #// First check to see if input has been overridden.
            if self.input_encoding != False:
                encodings_[-1] = self.input_encoding
            # end if
            application_types_ = Array("application/xml", "application/xml-dtd", "application/xml-external-parsed-entity")
            text_types_ = Array("text/xml", "text/xml-external-parsed-entity")
            #// RFC 3023 (only applies to sniffed content)
            if (php_isset(lambda : sniffed_)):
                if php_in_array(sniffed_, application_types_) or php_substr(sniffed_, 0, 12) == "application/" and php_substr(sniffed_, -4) == "+xml":
                    if (php_isset(lambda : headers_["content-type"])) and php_preg_match("/;\\x20?charset=([^;]*)/i", headers_["content-type"], charset_):
                        encodings_[-1] = php_strtoupper(charset_[1])
                    # end if
                    encodings_ = php_array_merge(encodings_, self.registry.call("Misc", "xml_encoding", Array(self.raw_data, self.registry)))
                    encodings_[-1] = "UTF-8"
                elif php_in_array(sniffed_, text_types_) or php_substr(sniffed_, 0, 5) == "text/" and php_substr(sniffed_, -4) == "+xml":
                    if (php_isset(lambda : headers_["content-type"])) and php_preg_match("/;\\x20?charset=([^;]*)/i", headers_["content-type"], charset_):
                        encodings_[-1] = charset_[1]
                    # end if
                    encodings_[-1] = "US-ASCII"
                    #// Text MIME-type default
                elif php_substr(sniffed_, 0, 5) == "text/":
                    encodings_[-1] = "US-ASCII"
                # end if
            # end if
            #// Fallback to XML 1.0 Appendix F.1/UTF-8/ISO-8859-1
            encodings_ = php_array_merge(encodings_, self.registry.call("Misc", "xml_encoding", Array(self.raw_data, self.registry)))
            encodings_[-1] = "UTF-8"
            encodings_[-1] = "ISO-8859-1"
            #// There's no point in trying an encoding twice
            encodings_ = array_unique(encodings_)
            #// Loop through each possible encoding, till we return something, or run out of possibilities
            for encoding_ in encodings_:
                #// Change the encoding to UTF-8 (as we always use UTF-8 internally)
                utf8_data_ = self.registry.call("Misc", "change_encoding", Array(self.raw_data, encoding_, "UTF-8"))
                if utf8_data_:
                    #// Create new parser
                    parser_ = self.registry.create("Parser")
                    #// If it's parsed fine
                    if parser_.parse(utf8_data_, "UTF-8"):
                        self.data = parser_.get_data()
                        if (not self.get_type() & (1 << (SIMPLEPIE_TYPE_NONE).bit_length()) - 1 - SIMPLEPIE_TYPE_NONE):
                            self.error = str("A feed could not be found at ") + str(self.feed_url) + str(". This does not appear to be a valid RSS or Atom feed.")
                            self.registry.call("Misc", "error", Array(self.error, E_USER_NOTICE, __FILE__, 0))
                            return False
                        # end if
                        if (php_isset(lambda : headers_)):
                            self.data["headers"] = headers_
                        # end if
                        self.data["build"] = SIMPLEPIE_BUILD
                        #// Cache the file if caching is enabled
                        if cache_ and (not cache_.save(self)):
                            trigger_error(str(self.cache_location) + str(" is not writeable. Make sure you've set the correct relative or absolute path, and that the location is server-writable."), E_USER_WARNING)
                        # end if
                        return True
                    # end if
                # end if
            # end for
            if (php_isset(lambda : parser_)):
                #// We have an error, just set SimplePie_Misc::error to it and quit
                self.error = php_sprintf("This XML document is invalid, likely due to invalid characters. XML error: %s at line %d, column %d", parser_.get_error_string(), parser_.get_current_line(), parser_.get_current_column())
            else:
                self.error = "The data could not be converted to UTF-8. You MUST have either the iconv or mbstring extension installed. Upgrading to PHP 5.x (which includes iconv) is highly recommended."
            # end if
            self.registry.call("Misc", "error", Array(self.error, E_USER_NOTICE, __FILE__, 0))
            return False
        # end def init
        #// 
        #// Fetch the data via SimplePie_File
        #// 
        #// If the data is already cached, attempt to fetch it from there instead
        #// @param SimplePie_Cache|false $cache Cache handler, or false to not load from the cache
        #// @return array|true Returns true if the data was loaded from the cache, or an array of HTTP headers and sniffed type
        #//
        def fetch_data(self, cache_=None):
            
            
            #// If it's enabled, use the cache
            if cache_:
                #// Load the Cache
                self.data = cache_.load()
                if (not php_empty(lambda : self.data)):
                    #// If the cache is for an outdated build of SimplePie
                    if (not (php_isset(lambda : self.data["build"]))) or self.data["build"] != SIMPLEPIE_BUILD:
                        cache_.unlink()
                        self.data = Array()
                        #// If we've hit a collision just rerun it with caching disabled
                    elif (php_isset(lambda : self.data["url"])) and self.data["url"] != self.feed_url:
                        cache_ = False
                        self.data = Array()
                        #// If we've got a non feed_url stored (if the page isn't actually a feed, or is a redirect) use that URL.
                    elif (php_isset(lambda : self.data["feed_url"])):
                        #// If the autodiscovery cache is still valid use it.
                        if cache_.mtime() + self.autodiscovery_cache_duration > time():
                            #// Do not need to do feed autodiscovery yet.
                            if self.data["feed_url"] != self.data["url"]:
                                self.set_feed_url(self.data["feed_url"])
                                return self.init()
                            # end if
                            cache_.unlink()
                            self.data = Array()
                        # end if
                        #// Check if the cache has been updated
                    elif cache_.mtime() + self.cache_duration < time():
                        #// If we have last-modified and/or etag set
                        if (php_isset(lambda : self.data["headers"]["last-modified"])) or (php_isset(lambda : self.data["headers"]["etag"])):
                            headers_ = Array({"Accept": "application/atom+xml, application/rss+xml, application/rdf+xml;q=0.9, application/xml;q=0.8, text/xml;q=0.8, text/html;q=0.7, unknown/unknown;q=0.1, application/unknown;q=0.1, */*;q=0.1"})
                            if (php_isset(lambda : self.data["headers"]["last-modified"])):
                                headers_["if-modified-since"] = self.data["headers"]["last-modified"]
                            # end if
                            if (php_isset(lambda : self.data["headers"]["etag"])):
                                headers_["if-none-match"] = self.data["headers"]["etag"]
                            # end if
                            file_ = self.registry.create("File", Array(self.feed_url, self.timeout / 10, 5, headers_, self.useragent, self.force_fsockopen))
                            if file_.success:
                                if file_.status_code == 304:
                                    cache_.touch()
                                    return True
                                # end if
                            else:
                                file_ = None
                            # end if
                        # end if
                    else:
                        self.raw_data = False
                        return True
                    # end if
                else:
                    cache_.unlink()
                    self.data = Array()
                # end if
            # end if
            #// If we don't already have the file (it'll only exist if we've opened it to check if the cache has been modified), open it.
            if (not (php_isset(lambda : file_))):
                if type(self.file_).__name__ == "SimplePie_File" and self.file_.url == self.feed_url:
                    file_ = self.file_
                else:
                    headers_ = Array({"Accept": "application/atom+xml, application/rss+xml, application/rdf+xml;q=0.9, application/xml;q=0.8, text/xml;q=0.8, text/html;q=0.7, unknown/unknown;q=0.1, application/unknown;q=0.1, */*;q=0.1"})
                    file_ = self.registry.create("File", Array(self.feed_url, self.timeout, 5, headers_, self.useragent, self.force_fsockopen))
                # end if
            # end if
            #// If the file connection has an error, set SimplePie::error to that and quit
            if (not file_.success) and (not file_.method & SIMPLEPIE_FILE_SOURCE_REMOTE == 0 or file_.status_code == 200 or file_.status_code > 206 and file_.status_code < 300):
                self.error = file_.error
                return (not php_empty(lambda : self.data))
            # end if
            if (not self.force_feed):
                #// Check if the supplied URL is a feed, if it isn't, look for it.
                locate_ = self.registry.create("Locator", Array(file_, self.timeout, self.useragent, self.max_checked_feeds))
                if (not locate_.is_feed(file_)):
                    file_ = None
                    try: 
                        file_ = locate_.find(self.autodiscovery, self.all_discovered_feeds)
                        if (not file_):
                            self.error = str("A feed could not be found at ") + str(self.feed_url) + str(". A feed with an invalid mime type may fall victim to this error, or ") + SIMPLEPIE_NAME + " was unable to auto-discover it.. Use force_feed() if you are certain this URL is a real feed."
                            self.registry.call("Misc", "error", Array(self.error, E_USER_NOTICE, __FILE__, 0))
                            return False
                        # end if
                    except SimplePie_Exception as e_:
                        #// This is usually because DOMDocument doesn't exist
                        self.error = e_.getmessage()
                        self.registry.call("Misc", "error", Array(self.error, E_USER_NOTICE, e_.getfile(), e_.getline()))
                        return False
                    # end try
                    if cache_:
                        self.data = Array({"url": self.feed_url, "feed_url": file_.url, "build": SIMPLEPIE_BUILD})
                        if (not cache_.save(self)):
                            trigger_error(str(self.cache_location) + str(" is not writeable. Make sure you've set the correct relative or absolute path, and that the location is server-writable."), E_USER_WARNING)
                        # end if
                        cache_ = self.registry.call("Cache", "get_handler", Array(self.cache_location, php_call_user_func(self.cache_name_function, file_.url), "spc"))
                    # end if
                    self.feed_url = file_.url
                # end if
                locate_ = None
            # end if
            self.raw_data = file_.body
            headers_ = file_.headers
            sniffer_ = self.registry.create("Content_Type_Sniffer", Array(file_))
            sniffed_ = sniffer_.get_type()
            return Array(headers_, sniffed_)
        # end def fetch_data
        #// 
        #// Get the error message for the occurred error.
        #// 
        #// @return string|array Error message, or array of messages for multifeeds
        #//
        def error(self):
            
            
            return self.error
        # end def error
        #// 
        #// Get the raw XML
        #// 
        #// This is the same as the old `$feed->enable_xml_dump(true)`, but returns
        #// the data instead of printing it.
        #// 
        #// @return string|boolean Raw XML data, false if the cache is used
        #//
        def get_raw_data(self):
            
            
            return self.raw_data
        # end def get_raw_data
        #// 
        #// Get the character encoding used for output
        #// 
        #// @since Preview Release
        #// @return string
        #//
        def get_encoding(self):
            
            
            return self.sanitize.output_encoding
        # end def get_encoding
        #// 
        #// Send the content-type header with correct encoding
        #// 
        #// This method ensures that the SimplePie-enabled page is being served with
        #// the correct {@link http://www.iana.org/assignments/media-types/ mime-type}
        #// and character encoding HTTP headers (character encoding determined by the
        #// {@see set_output_encoding} config option).
        #// 
        #// This won't work properly if any content or whitespace has already been
        #// sent to the browser, because it relies on PHP's
        #// {@link http://php.net/header header()} function, and these are the
        #// circumstances under which the function works.
        #// 
        #// Because it's setting these settings for the entire page (as is the nature
        #// of HTTP headers), this should only be used once per page (again, at the
        #// top).
        #// 
        #// @param string $mime MIME type to serve the page as
        #//
        def handle_content_type(self, mime_="text/html"):
            
            
            if (not php_headers_sent()):
                header_ = str("Content-type: ") + str(mime_) + str(";")
                if self.get_encoding():
                    header_ += " charset=" + self.get_encoding()
                else:
                    header_ += " charset=UTF-8"
                # end if
                php_header(header_)
            # end if
        # end def handle_content_type
        #// 
        #// Get the type of the feed
        #// 
        #// This returns a SIMPLEPIE_TYPE_* constant, which can be tested against
        #// using {@link http://php.net/language.operators.bitwise bitwise operators}
        #// 
        #// @since 0.8 (usage changed to using constants in 1.0)
        #// @see SIMPLEPIE_TYPE_NONE Unknown.
        #// @see SIMPLEPIE_TYPE_RSS_090 RSS 0.90.
        #// @see SIMPLEPIE_TYPE_RSS_091_NETSCAPE RSS 0.91 (Netscape).
        #// @see SIMPLEPIE_TYPE_RSS_091_USERLAND RSS 0.91 (Userland).
        #// @see SIMPLEPIE_TYPE_RSS_091 RSS 0.91.
        #// @see SIMPLEPIE_TYPE_RSS_092 RSS 0.92.
        #// @see SIMPLEPIE_TYPE_RSS_093 RSS 0.93.
        #// @see SIMPLEPIE_TYPE_RSS_094 RSS 0.94.
        #// @see SIMPLEPIE_TYPE_RSS_10 RSS 1.0.
        #// @see SIMPLEPIE_TYPE_RSS_20 RSS 2.0.x.
        #// @see SIMPLEPIE_TYPE_RSS_RDF RDF-based RSS.
        #// @see SIMPLEPIE_TYPE_RSS_SYNDICATION Non-RDF-based RSS (truly intended as syndication format).
        #// @see SIMPLEPIE_TYPE_RSS_ALL Any version of RSS.
        #// @see SIMPLEPIE_TYPE_ATOM_03 Atom 0.3.
        #// @see SIMPLEPIE_TYPE_ATOM_10 Atom 1.0.
        #// @see SIMPLEPIE_TYPE_ATOM_ALL Any version of Atom.
        #// @see SIMPLEPIE_TYPE_ALL Any known/supported feed type.
        #// @return int SIMPLEPIE_TYPE_* constant
        #//
        def get_type(self):
            
            
            if (not (php_isset(lambda : self.data["type"]))):
                self.data["type"] = SIMPLEPIE_TYPE_ALL
                if (php_isset(lambda : self.data["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["feed"])):
                    self.data["type"] &= SIMPLEPIE_TYPE_ATOM_10
                elif (php_isset(lambda : self.data["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["feed"])):
                    self.data["type"] &= SIMPLEPIE_TYPE_ATOM_03
                elif (php_isset(lambda : self.data["child"][SIMPLEPIE_NAMESPACE_RDF]["RDF"])):
                    if (php_isset(lambda : self.data["child"][SIMPLEPIE_NAMESPACE_RDF]["RDF"][0]["child"][SIMPLEPIE_NAMESPACE_RSS_10]["channel"])) or (php_isset(lambda : self.data["child"][SIMPLEPIE_NAMESPACE_RDF]["RDF"][0]["child"][SIMPLEPIE_NAMESPACE_RSS_10]["image"])) or (php_isset(lambda : self.data["child"][SIMPLEPIE_NAMESPACE_RDF]["RDF"][0]["child"][SIMPLEPIE_NAMESPACE_RSS_10]["item"])) or (php_isset(lambda : self.data["child"][SIMPLEPIE_NAMESPACE_RDF]["RDF"][0]["child"][SIMPLEPIE_NAMESPACE_RSS_10]["textinput"])):
                        self.data["type"] &= SIMPLEPIE_TYPE_RSS_10
                    # end if
                    if (php_isset(lambda : self.data["child"][SIMPLEPIE_NAMESPACE_RDF]["RDF"][0]["child"][SIMPLEPIE_NAMESPACE_RSS_090]["channel"])) or (php_isset(lambda : self.data["child"][SIMPLEPIE_NAMESPACE_RDF]["RDF"][0]["child"][SIMPLEPIE_NAMESPACE_RSS_090]["image"])) or (php_isset(lambda : self.data["child"][SIMPLEPIE_NAMESPACE_RDF]["RDF"][0]["child"][SIMPLEPIE_NAMESPACE_RSS_090]["item"])) or (php_isset(lambda : self.data["child"][SIMPLEPIE_NAMESPACE_RDF]["RDF"][0]["child"][SIMPLEPIE_NAMESPACE_RSS_090]["textinput"])):
                        self.data["type"] &= SIMPLEPIE_TYPE_RSS_090
                    # end if
                elif (php_isset(lambda : self.data["child"][SIMPLEPIE_NAMESPACE_RSS_20]["rss"])):
                    self.data["type"] &= SIMPLEPIE_TYPE_RSS_ALL
                    if (php_isset(lambda : self.data["child"][SIMPLEPIE_NAMESPACE_RSS_20]["rss"][0]["attribs"][""]["version"])):
                        for case in Switch(php_trim(self.data["child"][SIMPLEPIE_NAMESPACE_RSS_20]["rss"][0]["attribs"][""]["version"])):
                            if case("0.91"):
                                self.data["type"] &= SIMPLEPIE_TYPE_RSS_091
                                if (php_isset(lambda : self.data["child"][SIMPLEPIE_NAMESPACE_RSS_20]["rss"][0]["child"][SIMPLEPIE_NAMESPACE_RSS_20]["skiphours"]["hour"][0]["data"])):
                                    for case in Switch(php_trim(self.data["child"][SIMPLEPIE_NAMESPACE_RSS_20]["rss"][0]["child"][SIMPLEPIE_NAMESPACE_RSS_20]["skiphours"]["hour"][0]["data"])):
                                        if case("0"):
                                            self.data["type"] &= SIMPLEPIE_TYPE_RSS_091_NETSCAPE
                                            break
                                        # end if
                                        if case("24"):
                                            self.data["type"] &= SIMPLEPIE_TYPE_RSS_091_USERLAND
                                            break
                                        # end if
                                    # end for
                                # end if
                                break
                            # end if
                            if case("0.92"):
                                self.data["type"] &= SIMPLEPIE_TYPE_RSS_092
                                break
                            # end if
                            if case("0.93"):
                                self.data["type"] &= SIMPLEPIE_TYPE_RSS_093
                                break
                            # end if
                            if case("0.94"):
                                self.data["type"] &= SIMPLEPIE_TYPE_RSS_094
                                break
                            # end if
                            if case("2.0"):
                                self.data["type"] &= SIMPLEPIE_TYPE_RSS_20
                                break
                            # end if
                        # end for
                    # end if
                else:
                    self.data["type"] = SIMPLEPIE_TYPE_NONE
                # end if
            # end if
            return self.data["type"]
        # end def get_type
        #// 
        #// Get the URL for the feed
        #// 
        #// May or may not be different from the URL passed to {@see set_feed_url()},
        #// depending on whether auto-discovery was used.
        #// 
        #// @since Preview Release (previously called `get_feed_url()` since SimplePie 0.8.)
        #// @todo If we have a perm redirect we should return the new URL
        #// @todo When we make the above change, let's support <itunes:new-feed-url> as well
        #// @todo Also, |atom:link|@rel=self
        #// @return string|null
        #//
        def subscribe_url(self):
            
            
            if self.feed_url != None:
                return self.sanitize(self.feed_url, SIMPLEPIE_CONSTRUCT_IRI)
            else:
                return None
            # end if
        # end def subscribe_url
        #// 
        #// Get data for an feed-level element
        #// 
        #// This method allows you to get access to ANY element/attribute that is a
        #// sub-element of the opening feed tag.
        #// 
        #// The return value is an indexed array of elements matching the given
        #// namespace and tag name. Each element has `attribs`, `data` and `child`
        #// subkeys. For `attribs` and `child`, these contain namespace subkeys.
        #// `attribs` then has one level of associative name => value data (where
        #// `value` is a string) after the namespace. `child` has tag-indexed keys
        #// after the namespace, each member of which is an indexed array matching
        #// this same format.
        #// 
        #// For example:
        #// <pre>
        #// This is probably a bad example because we already support
        #// <media:content> natively, but it shows you how to parse through
        #// the nodes.
        #// $group = $item->get_item_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, 'group');
        #// $content = $group[0]['child'][SIMPLEPIE_NAMESPACE_MEDIARSS]['content'];
        #// $file = $content[0]['attribs']['']['url'];
        #// echo $file;
        #// </pre>
        #// 
        #// @since 1.0
        #// @see http://simplepie.org/wiki/faq/supported_xml_namespaces
        #// @param string $namespace The URL of the XML namespace of the elements you're trying to access
        #// @param string $tag Tag name
        #// @return array
        #//
        def get_feed_tags(self, namespace_=None, tag_=None):
            
            
            type_ = self.get_type()
            if type_ & SIMPLEPIE_TYPE_ATOM_10:
                if (php_isset(lambda : self.data["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["feed"][0]["child"][namespace_][tag_])):
                    return self.data["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["feed"][0]["child"][namespace_][tag_]
                # end if
            # end if
            if type_ & SIMPLEPIE_TYPE_ATOM_03:
                if (php_isset(lambda : self.data["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["feed"][0]["child"][namespace_][tag_])):
                    return self.data["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["feed"][0]["child"][namespace_][tag_]
                # end if
            # end if
            if type_ & SIMPLEPIE_TYPE_RSS_RDF:
                if (php_isset(lambda : self.data["child"][SIMPLEPIE_NAMESPACE_RDF]["RDF"][0]["child"][namespace_][tag_])):
                    return self.data["child"][SIMPLEPIE_NAMESPACE_RDF]["RDF"][0]["child"][namespace_][tag_]
                # end if
            # end if
            if type_ & SIMPLEPIE_TYPE_RSS_SYNDICATION:
                if (php_isset(lambda : self.data["child"][SIMPLEPIE_NAMESPACE_RSS_20]["rss"][0]["child"][namespace_][tag_])):
                    return self.data["child"][SIMPLEPIE_NAMESPACE_RSS_20]["rss"][0]["child"][namespace_][tag_]
                # end if
            # end if
            return None
        # end def get_feed_tags
        #// 
        #// Get data for an channel-level element
        #// 
        #// This method allows you to get access to ANY element/attribute in the
        #// channel/header section of the feed.
        #// 
        #// See {@see SimplePie::get_feed_tags()} for a description of the return value
        #// 
        #// @since 1.0
        #// @see http://simplepie.org/wiki/faq/supported_xml_namespaces
        #// @param string $namespace The URL of the XML namespace of the elements you're trying to access
        #// @param string $tag Tag name
        #// @return array
        #//
        def get_channel_tags(self, namespace_=None, tag_=None):
            
            
            type_ = self.get_type()
            if type_ & SIMPLEPIE_TYPE_ATOM_ALL:
                return_ = self.get_feed_tags(namespace_, tag_)
                if return_:
                    return return_
                # end if
            # end if
            if type_ & SIMPLEPIE_TYPE_RSS_10:
                channel_ = self.get_feed_tags(SIMPLEPIE_NAMESPACE_RSS_10, "channel")
                if channel_:
                    if (php_isset(lambda : channel_[0]["child"][namespace_][tag_])):
                        return channel_[0]["child"][namespace_][tag_]
                    # end if
                # end if
            # end if
            if type_ & SIMPLEPIE_TYPE_RSS_090:
                channel_ = self.get_feed_tags(SIMPLEPIE_NAMESPACE_RSS_090, "channel")
                if channel_:
                    if (php_isset(lambda : channel_[0]["child"][namespace_][tag_])):
                        return channel_[0]["child"][namespace_][tag_]
                    # end if
                # end if
            # end if
            if type_ & SIMPLEPIE_TYPE_RSS_SYNDICATION:
                channel_ = self.get_feed_tags(SIMPLEPIE_NAMESPACE_RSS_20, "channel")
                if channel_:
                    if (php_isset(lambda : channel_[0]["child"][namespace_][tag_])):
                        return channel_[0]["child"][namespace_][tag_]
                    # end if
                # end if
            # end if
            return None
        # end def get_channel_tags
        #// 
        #// Get data for an channel-level element
        #// 
        #// This method allows you to get access to ANY element/attribute in the
        #// image/logo section of the feed.
        #// 
        #// See {@see SimplePie::get_feed_tags()} for a description of the return value
        #// 
        #// @since 1.0
        #// @see http://simplepie.org/wiki/faq/supported_xml_namespaces
        #// @param string $namespace The URL of the XML namespace of the elements you're trying to access
        #// @param string $tag Tag name
        #// @return array
        #//
        def get_image_tags(self, namespace_=None, tag_=None):
            
            
            type_ = self.get_type()
            if type_ & SIMPLEPIE_TYPE_RSS_10:
                image_ = self.get_feed_tags(SIMPLEPIE_NAMESPACE_RSS_10, "image")
                if image_:
                    if (php_isset(lambda : image_[0]["child"][namespace_][tag_])):
                        return image_[0]["child"][namespace_][tag_]
                    # end if
                # end if
            # end if
            if type_ & SIMPLEPIE_TYPE_RSS_090:
                image_ = self.get_feed_tags(SIMPLEPIE_NAMESPACE_RSS_090, "image")
                if image_:
                    if (php_isset(lambda : image_[0]["child"][namespace_][tag_])):
                        return image_[0]["child"][namespace_][tag_]
                    # end if
                # end if
            # end if
            if type_ & SIMPLEPIE_TYPE_RSS_SYNDICATION:
                image_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_RSS_20, "image")
                if image_:
                    if (php_isset(lambda : image_[0]["child"][namespace_][tag_])):
                        return image_[0]["child"][namespace_][tag_]
                    # end if
                # end if
            # end if
            return None
        # end def get_image_tags
        #// 
        #// Get the base URL value from the feed
        #// 
        #// Uses `<xml:base>` if available, otherwise uses the first link in the
        #// feed, or failing that, the URL of the feed itself.
        #// 
        #// @see get_link
        #// @see subscribe_url
        #// 
        #// @param array $element
        #// @return string
        #//
        def get_base(self, element_=None):
            if element_ is None:
                element_ = Array()
            # end if
            
            if (not self.get_type() & SIMPLEPIE_TYPE_RSS_SYNDICATION) and (not php_empty(lambda : element_["xml_base_explicit"])) and (php_isset(lambda : element_["xml_base"])):
                return element_["xml_base"]
            elif self.get_link() != None:
                return self.get_link()
            else:
                return self.subscribe_url()
            # end if
        # end def get_base
        #// 
        #// Sanitize feed data
        #// 
        #// @access private
        #// @see SimplePie_Sanitize::sanitize()
        #// @param string $data Data to sanitize
        #// @param int $type One of the SIMPLEPIE_CONSTRUCT_* constants
        #// @param string $base Base URL to resolve URLs against
        #// @return string Sanitized data
        #//
        def sanitize(self, data_=None, type_=None, base_=""):
            
            
            return self.sanitize.sanitize(data_, type_, base_)
        # end def sanitize
        #// 
        #// Get the title of the feed
        #// 
        #// Uses `<atom:title>`, `<title>` or `<dc:title>`
        #// 
        #// @since 1.0 (previously called `get_feed_title` since 0.8)
        #// @return string|null
        #//
        def get_title(self):
            
            
            return_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "title")
            if return_:
                return self.sanitize(return_[0]["data"], self.registry.call("Misc", "atom_10_construct_type", Array(return_[0]["attribs"])), self.get_base(return_[0]))
            elif self.get_channel_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "title"):
                return_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "title")
                return self.sanitize(return_[0]["data"], self.registry.call("Misc", "atom_03_construct_type", Array(return_[0]["attribs"])), self.get_base(return_[0]))
            elif self.get_channel_tags(SIMPLEPIE_NAMESPACE_RSS_10, "title"):
                return_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_RSS_10, "title")
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_MAYBE_HTML, self.get_base(return_[0]))
            elif self.get_channel_tags(SIMPLEPIE_NAMESPACE_RSS_090, "title"):
                return_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_RSS_090, "title")
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_MAYBE_HTML, self.get_base(return_[0]))
            elif self.get_channel_tags(SIMPLEPIE_NAMESPACE_RSS_20, "title"):
                return_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_RSS_20, "title")
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_MAYBE_HTML, self.get_base(return_[0]))
            elif self.get_channel_tags(SIMPLEPIE_NAMESPACE_DC_11, "title"):
                return_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_DC_11, "title")
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
            elif self.get_channel_tags(SIMPLEPIE_NAMESPACE_DC_10, "title"):
                return_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_DC_10, "title")
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
            else:
                return None
            # end if
        # end def get_title
        #// 
        #// Get a category for the feed
        #// 
        #// @since Unknown
        #// @param int $key The category that you want to return.  Remember that arrays begin with 0, not 1
        #// @return SimplePie_Category|null
        #//
        def get_category(self, key_=0):
            
            
            categories_ = self.get_categories()
            if (php_isset(lambda : categories_[key_])):
                return categories_[key_]
            else:
                return None
            # end if
        # end def get_category
        #// 
        #// Get all categories for the feed
        #// 
        #// Uses `<atom:category>`, `<category>` or `<dc:subject>`
        #// 
        #// @since Unknown
        #// @return array|null List of {@see SimplePie_Category} objects
        #//
        def get_categories(self):
            
            
            categories_ = Array()
            for category_ in self.get_channel_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "category"):
                term_ = None
                scheme_ = None
                label_ = None
                if (php_isset(lambda : category_["attribs"][""]["term"])):
                    term_ = self.sanitize(category_["attribs"][""]["term"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
                if (php_isset(lambda : category_["attribs"][""]["scheme"])):
                    scheme_ = self.sanitize(category_["attribs"][""]["scheme"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
                if (php_isset(lambda : category_["attribs"][""]["label"])):
                    label_ = self.sanitize(category_["attribs"][""]["label"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
                categories_[-1] = self.registry.create("Category", Array(term_, scheme_, label_))
            # end for
            for category_ in self.get_channel_tags(SIMPLEPIE_NAMESPACE_RSS_20, "category"):
                #// This is really the label, but keep this as the term also for BC.
                #// Label will also work on retrieving because that falls back to term.
                term_ = self.sanitize(category_["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                if (php_isset(lambda : category_["attribs"][""]["domain"])):
                    scheme_ = self.sanitize(category_["attribs"][""]["domain"], SIMPLEPIE_CONSTRUCT_TEXT)
                else:
                    scheme_ = None
                # end if
                categories_[-1] = self.registry.create("Category", Array(term_, scheme_, None))
            # end for
            for category_ in self.get_channel_tags(SIMPLEPIE_NAMESPACE_DC_11, "subject"):
                categories_[-1] = self.registry.create("Category", Array(self.sanitize(category_["data"], SIMPLEPIE_CONSTRUCT_TEXT), None, None))
            # end for
            for category_ in self.get_channel_tags(SIMPLEPIE_NAMESPACE_DC_10, "subject"):
                categories_[-1] = self.registry.create("Category", Array(self.sanitize(category_["data"], SIMPLEPIE_CONSTRUCT_TEXT), None, None))
            # end for
            if (not php_empty(lambda : categories_)):
                return array_unique(categories_)
            else:
                return None
            # end if
        # end def get_categories
        #// 
        #// Get an author for the feed
        #// 
        #// @since 1.1
        #// @param int $key The author that you want to return.  Remember that arrays begin with 0, not 1
        #// @return SimplePie_Author|null
        #//
        def get_author(self, key_=0):
            
            
            authors_ = self.get_authors()
            if (php_isset(lambda : authors_[key_])):
                return authors_[key_]
            else:
                return None
            # end if
        # end def get_author
        #// 
        #// Get all authors for the feed
        #// 
        #// Uses `<atom:author>`, `<author>`, `<dc:creator>` or `<itunes:author>`
        #// 
        #// @since 1.1
        #// @return array|null List of {@see SimplePie_Author} objects
        #//
        def get_authors(self):
            
            
            authors_ = Array()
            for author_ in self.get_channel_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "author"):
                name_ = None
                uri_ = None
                email_ = None
                if (php_isset(lambda : author_["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["name"][0]["data"])):
                    name_ = self.sanitize(author_["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["name"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
                if (php_isset(lambda : author_["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["uri"][0]["data"])):
                    uri_ = self.sanitize(author_["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["uri"][0]["data"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(author_["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["uri"][0]))
                # end if
                if (php_isset(lambda : author_["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["email"][0]["data"])):
                    email_ = self.sanitize(author_["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["email"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
                if name_ != None or email_ != None or uri_ != None:
                    authors_[-1] = self.registry.create("Author", Array(name_, uri_, email_))
                # end if
            # end for
            author_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "author")
            if author_:
                name_ = None
                url_ = None
                email_ = None
                if (php_isset(lambda : author_[0]["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["name"][0]["data"])):
                    name_ = self.sanitize(author_[0]["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["name"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
                if (php_isset(lambda : author_[0]["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["url"][0]["data"])):
                    url_ = self.sanitize(author_[0]["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["url"][0]["data"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(author_[0]["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["url"][0]))
                # end if
                if (php_isset(lambda : author_[0]["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["email"][0]["data"])):
                    email_ = self.sanitize(author_[0]["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["email"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
                if name_ != None or email_ != None or url_ != None:
                    authors_[-1] = self.registry.create("Author", Array(name_, url_, email_))
                # end if
            # end if
            for author_ in self.get_channel_tags(SIMPLEPIE_NAMESPACE_DC_11, "creator"):
                authors_[-1] = self.registry.create("Author", Array(self.sanitize(author_["data"], SIMPLEPIE_CONSTRUCT_TEXT), None, None))
            # end for
            for author_ in self.get_channel_tags(SIMPLEPIE_NAMESPACE_DC_10, "creator"):
                authors_[-1] = self.registry.create("Author", Array(self.sanitize(author_["data"], SIMPLEPIE_CONSTRUCT_TEXT), None, None))
            # end for
            for author_ in self.get_channel_tags(SIMPLEPIE_NAMESPACE_ITUNES, "author"):
                authors_[-1] = self.registry.create("Author", Array(self.sanitize(author_["data"], SIMPLEPIE_CONSTRUCT_TEXT), None, None))
            # end for
            if (not php_empty(lambda : authors_)):
                return array_unique(authors_)
            else:
                return None
            # end if
        # end def get_authors
        #// 
        #// Get a contributor for the feed
        #// 
        #// @since 1.1
        #// @param int $key The contrbutor that you want to return.  Remember that arrays begin with 0, not 1
        #// @return SimplePie_Author|null
        #//
        def get_contributor(self, key_=0):
            
            
            contributors_ = self.get_contributors()
            if (php_isset(lambda : contributors_[key_])):
                return contributors_[key_]
            else:
                return None
            # end if
        # end def get_contributor
        #// 
        #// Get all contributors for the feed
        #// 
        #// Uses `<atom:contributor>`
        #// 
        #// @since 1.1
        #// @return array|null List of {@see SimplePie_Author} objects
        #//
        def get_contributors(self):
            
            
            contributors_ = Array()
            for contributor_ in self.get_channel_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "contributor"):
                name_ = None
                uri_ = None
                email_ = None
                if (php_isset(lambda : contributor_["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["name"][0]["data"])):
                    name_ = self.sanitize(contributor_["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["name"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
                if (php_isset(lambda : contributor_["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["uri"][0]["data"])):
                    uri_ = self.sanitize(contributor_["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["uri"][0]["data"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(contributor_["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["uri"][0]))
                # end if
                if (php_isset(lambda : contributor_["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["email"][0]["data"])):
                    email_ = self.sanitize(contributor_["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["email"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
                if name_ != None or email_ != None or uri_ != None:
                    contributors_[-1] = self.registry.create("Author", Array(name_, uri_, email_))
                # end if
            # end for
            for contributor_ in self.get_channel_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "contributor"):
                name_ = None
                url_ = None
                email_ = None
                if (php_isset(lambda : contributor_["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["name"][0]["data"])):
                    name_ = self.sanitize(contributor_["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["name"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
                if (php_isset(lambda : contributor_["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["url"][0]["data"])):
                    url_ = self.sanitize(contributor_["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["url"][0]["data"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(contributor_["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["url"][0]))
                # end if
                if (php_isset(lambda : contributor_["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["email"][0]["data"])):
                    email_ = self.sanitize(contributor_["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["email"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
                if name_ != None or email_ != None or url_ != None:
                    contributors_[-1] = self.registry.create("Author", Array(name_, url_, email_))
                # end if
            # end for
            if (not php_empty(lambda : contributors_)):
                return array_unique(contributors_)
            else:
                return None
            # end if
        # end def get_contributors
        #// 
        #// Get a single link for the feed
        #// 
        #// @since 1.0 (previously called `get_feed_link` since Preview Release, `get_feed_permalink()` since 0.8)
        #// @param int $key The link that you want to return.  Remember that arrays begin with 0, not 1
        #// @param string $rel The relationship of the link to return
        #// @return string|null Link URL
        #//
        def get_link(self, key_=0, rel_="alternate"):
            
            
            links_ = self.get_links(rel_)
            if (php_isset(lambda : links_[key_])):
                return links_[key_]
            else:
                return None
            # end if
        # end def get_link
        #// 
        #// Get the permalink for the item
        #// 
        #// Returns the first link available with a relationship of "alternate".
        #// Identical to {@see get_link()} with key 0
        #// 
        #// @see get_link
        #// @since 1.0 (previously called `get_feed_link` since Preview Release, `get_feed_permalink()` since 0.8)
        #// @internal Added for parity between the parent-level and the item/entry-level.
        #// @return string|null Link URL
        #//
        def get_permalink(self):
            
            
            return self.get_link(0)
        # end def get_permalink
        #// 
        #// Get all links for the feed
        #// 
        #// Uses `<atom:link>` or `<link>`
        #// 
        #// @since Beta 2
        #// @param string $rel The relationship of links to return
        #// @return array|null Links found for the feed (strings)
        #//
        def get_links(self, rel_="alternate"):
            
            
            if (not (php_isset(lambda : self.data["links"]))):
                self.data["links"] = Array()
                links_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "link")
                if links_:
                    for link_ in links_:
                        if (php_isset(lambda : link_["attribs"][""]["href"])):
                            link_rel_ = link_["attribs"][""]["rel"] if (php_isset(lambda : link_["attribs"][""]["rel"])) else "alternate"
                            self.data["links"][link_rel_][-1] = self.sanitize(link_["attribs"][""]["href"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(link_))
                        # end if
                    # end for
                # end if
                links_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "link")
                if links_:
                    for link_ in links_:
                        if (php_isset(lambda : link_["attribs"][""]["href"])):
                            link_rel_ = link_["attribs"][""]["rel"] if (php_isset(lambda : link_["attribs"][""]["rel"])) else "alternate"
                            self.data["links"][link_rel_][-1] = self.sanitize(link_["attribs"][""]["href"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(link_))
                        # end if
                    # end for
                # end if
                links_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_RSS_10, "link")
                if links_:
                    self.data["links"]["alternate"][-1] = self.sanitize(links_[0]["data"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(links_[0]))
                # end if
                links_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_RSS_090, "link")
                if links_:
                    self.data["links"]["alternate"][-1] = self.sanitize(links_[0]["data"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(links_[0]))
                # end if
                links_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_RSS_20, "link")
                if links_:
                    self.data["links"]["alternate"][-1] = self.sanitize(links_[0]["data"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(links_[0]))
                # end if
                keys_ = php_array_keys(self.data["links"])
                for key_ in keys_:
                    if self.registry.call("Misc", "is_isegment_nz_nc", Array(key_)):
                        if (php_isset(lambda : self.data["links"][SIMPLEPIE_IANA_LINK_RELATIONS_REGISTRY + key_])):
                            self.data["links"][SIMPLEPIE_IANA_LINK_RELATIONS_REGISTRY + key_] = php_array_merge(self.data["links"][key_], self.data["links"][SIMPLEPIE_IANA_LINK_RELATIONS_REGISTRY + key_])
                            self.data["links"][key_] = self.data["links"][SIMPLEPIE_IANA_LINK_RELATIONS_REGISTRY + key_]
                        else:
                            self.data["links"][SIMPLEPIE_IANA_LINK_RELATIONS_REGISTRY + key_] = self.data["links"][key_]
                        # end if
                    elif php_substr(key_, 0, 41) == SIMPLEPIE_IANA_LINK_RELATIONS_REGISTRY:
                        self.data["links"][php_substr(key_, 41)] = self.data["links"][key_]
                    # end if
                    self.data["links"][key_] = array_unique(self.data["links"][key_])
                # end for
            # end if
            if (php_isset(lambda : self.data["links"][rel_])):
                return self.data["links"][rel_]
            else:
                return None
            # end if
        # end def get_links
        def get_all_discovered_feeds(self):
            
            
            return self.all_discovered_feeds
        # end def get_all_discovered_feeds
        #// 
        #// Get the content for the item
        #// 
        #// Uses `<atom:subtitle>`, `<atom:tagline>`, `<description>`,
        #// `<dc:description>`, `<itunes:summary>` or `<itunes:subtitle>`
        #// 
        #// @since 1.0 (previously called `get_feed_description()` since 0.8)
        #// @return string|null
        #//
        def get_description(self):
            
            
            return_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "subtitle")
            if return_:
                return self.sanitize(return_[0]["data"], self.registry.call("Misc", "atom_10_construct_type", Array(return_[0]["attribs"])), self.get_base(return_[0]))
            elif self.get_channel_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "tagline"):
                return_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "tagline")
                return self.sanitize(return_[0]["data"], self.registry.call("Misc", "atom_03_construct_type", Array(return_[0]["attribs"])), self.get_base(return_[0]))
            elif self.get_channel_tags(SIMPLEPIE_NAMESPACE_RSS_10, "description"):
                return_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_RSS_10, "description")
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_MAYBE_HTML, self.get_base(return_[0]))
            elif self.get_channel_tags(SIMPLEPIE_NAMESPACE_RSS_090, "description"):
                return_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_RSS_090, "description")
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_MAYBE_HTML, self.get_base(return_[0]))
            elif self.get_channel_tags(SIMPLEPIE_NAMESPACE_RSS_20, "description"):
                return_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_RSS_20, "description")
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_HTML, self.get_base(return_[0]))
            elif self.get_channel_tags(SIMPLEPIE_NAMESPACE_DC_11, "description"):
                return_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_DC_11, "description")
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
            elif self.get_channel_tags(SIMPLEPIE_NAMESPACE_DC_10, "description"):
                return_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_DC_10, "description")
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
            elif self.get_channel_tags(SIMPLEPIE_NAMESPACE_ITUNES, "summary"):
                return_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_ITUNES, "summary")
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_HTML, self.get_base(return_[0]))
            elif self.get_channel_tags(SIMPLEPIE_NAMESPACE_ITUNES, "subtitle"):
                return_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_ITUNES, "subtitle")
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_HTML, self.get_base(return_[0]))
            else:
                return None
            # end if
        # end def get_description
        #// 
        #// Get the copyright info for the feed
        #// 
        #// Uses `<atom:rights>`, `<atom:copyright>` or `<dc:rights>`
        #// 
        #// @since 1.0 (previously called `get_feed_copyright()` since 0.8)
        #// @return string|null
        #//
        def get_copyright(self):
            
            
            return_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "rights")
            if return_:
                return self.sanitize(return_[0]["data"], self.registry.call("Misc", "atom_10_construct_type", Array(return_[0]["attribs"])), self.get_base(return_[0]))
            elif self.get_channel_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "copyright"):
                return_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "copyright")
                return self.sanitize(return_[0]["data"], self.registry.call("Misc", "atom_03_construct_type", Array(return_[0]["attribs"])), self.get_base(return_[0]))
            elif self.get_channel_tags(SIMPLEPIE_NAMESPACE_RSS_20, "copyright"):
                return_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_RSS_20, "copyright")
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
            elif self.get_channel_tags(SIMPLEPIE_NAMESPACE_DC_11, "rights"):
                return_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_DC_11, "rights")
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
            elif self.get_channel_tags(SIMPLEPIE_NAMESPACE_DC_10, "rights"):
                return_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_DC_10, "rights")
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
            else:
                return None
            # end if
        # end def get_copyright
        #// 
        #// Get the language for the feed
        #// 
        #// Uses `<language>`, `<dc:language>`, or @xml_lang
        #// 
        #// @since 1.0 (previously called `get_feed_language()` since 0.8)
        #// @return string|null
        #//
        def get_language(self):
            
            
            return_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_RSS_20, "language")
            if return_:
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
            elif self.get_channel_tags(SIMPLEPIE_NAMESPACE_DC_11, "language"):
                return_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_DC_11, "language")
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
            elif self.get_channel_tags(SIMPLEPIE_NAMESPACE_DC_10, "language"):
                return_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_DC_10, "language")
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
            elif (php_isset(lambda : self.data["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["feed"][0]["xml_lang"])):
                return self.sanitize(self.data["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["feed"][0]["xml_lang"], SIMPLEPIE_CONSTRUCT_TEXT)
            elif (php_isset(lambda : self.data["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["feed"][0]["xml_lang"])):
                return self.sanitize(self.data["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["feed"][0]["xml_lang"], SIMPLEPIE_CONSTRUCT_TEXT)
            elif (php_isset(lambda : self.data["child"][SIMPLEPIE_NAMESPACE_RDF]["RDF"][0]["xml_lang"])):
                return self.sanitize(self.data["child"][SIMPLEPIE_NAMESPACE_RDF]["RDF"][0]["xml_lang"], SIMPLEPIE_CONSTRUCT_TEXT)
            elif (php_isset(lambda : self.data["headers"]["content-language"])):
                return self.sanitize(self.data["headers"]["content-language"], SIMPLEPIE_CONSTRUCT_TEXT)
            else:
                return None
            # end if
        # end def get_language
        #// 
        #// Get the latitude coordinates for the item
        #// 
        #// Compatible with the W3C WGS84 Basic Geo and GeoRSS specifications
        #// 
        #// Uses `<geo:lat>` or `<georss:point>`
        #// 
        #// @since 1.0
        #// @link http://www.w3.org/2003/01/geo/ W3C WGS84 Basic Geo
        #// @link http://www.georss.org/ GeoRSS
        #// @return string|null
        #//
        def get_latitude(self):
            
            
            return_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_W3C_BASIC_GEO, "lat")
            if return_:
                return php_float(return_[0]["data"])
            elif self.get_channel_tags(SIMPLEPIE_NAMESPACE_GEORSS, "point") and php_preg_match("/^((?:-)?[0-9]+(?:\\.[0-9]+)) ((?:-)?[0-9]+(?:\\.[0-9]+))$/", php_trim(return_[0]["data"]), match_):
                return_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_GEORSS, "point")
                return php_float(match_[1])
            else:
                return None
            # end if
        # end def get_latitude
        #// 
        #// Get the longitude coordinates for the feed
        #// 
        #// Compatible with the W3C WGS84 Basic Geo and GeoRSS specifications
        #// 
        #// Uses `<geo:long>`, `<geo:lon>` or `<georss:point>`
        #// 
        #// @since 1.0
        #// @link http://www.w3.org/2003/01/geo/ W3C WGS84 Basic Geo
        #// @link http://www.georss.org/ GeoRSS
        #// @return string|null
        #//
        def get_longitude(self):
            
            
            return_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_W3C_BASIC_GEO, "long")
            if return_:
                return php_float(return_[0]["data"])
            elif self.get_channel_tags(SIMPLEPIE_NAMESPACE_W3C_BASIC_GEO, "lon"):
                return_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_W3C_BASIC_GEO, "lon")
                return php_float(return_[0]["data"])
            elif self.get_channel_tags(SIMPLEPIE_NAMESPACE_GEORSS, "point") and php_preg_match("/^((?:-)?[0-9]+(?:\\.[0-9]+)) ((?:-)?[0-9]+(?:\\.[0-9]+))$/", php_trim(return_[0]["data"]), match_):
                return_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_GEORSS, "point")
                return php_float(match_[2])
            else:
                return None
            # end if
        # end def get_longitude
        #// 
        #// Get the feed logo's title
        #// 
        #// RSS 0.9.0, 1.0 and 2.0 feeds are allowed to have a "feed logo" title.
        #// 
        #// Uses `<image><title>` or `<image><dc:title>`
        #// 
        #// @return string|null
        #//
        def get_image_title(self):
            
            
            return_ = self.get_image_tags(SIMPLEPIE_NAMESPACE_RSS_10, "title")
            if return_:
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
            elif self.get_image_tags(SIMPLEPIE_NAMESPACE_RSS_090, "title"):
                return_ = self.get_image_tags(SIMPLEPIE_NAMESPACE_RSS_090, "title")
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
            elif self.get_image_tags(SIMPLEPIE_NAMESPACE_RSS_20, "title"):
                return_ = self.get_image_tags(SIMPLEPIE_NAMESPACE_RSS_20, "title")
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
            elif self.get_image_tags(SIMPLEPIE_NAMESPACE_DC_11, "title"):
                return_ = self.get_image_tags(SIMPLEPIE_NAMESPACE_DC_11, "title")
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
            elif self.get_image_tags(SIMPLEPIE_NAMESPACE_DC_10, "title"):
                return_ = self.get_image_tags(SIMPLEPIE_NAMESPACE_DC_10, "title")
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
            else:
                return None
            # end if
        # end def get_image_title
        #// 
        #// Get the feed logo's URL
        #// 
        #// RSS 0.9.0, 2.0, Atom 1.0, and feeds with iTunes RSS tags are allowed to
        #// have a "feed logo" URL. This points directly to the image itself.
        #// 
        #// Uses `<itunes:image>`, `<atom:logo>`, `<atom:icon>`,
        #// `<image><title>` or `<image><dc:title>`
        #// 
        #// @return string|null
        #//
        def get_image_url(self):
            
            
            return_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_ITUNES, "image")
            if return_:
                return self.sanitize(return_[0]["attribs"][""]["href"], SIMPLEPIE_CONSTRUCT_IRI)
            elif self.get_channel_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "logo"):
                return_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "logo")
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(return_[0]))
            elif self.get_channel_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "icon"):
                return_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "icon")
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(return_[0]))
            elif self.get_image_tags(SIMPLEPIE_NAMESPACE_RSS_10, "url"):
                return_ = self.get_image_tags(SIMPLEPIE_NAMESPACE_RSS_10, "url")
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(return_[0]))
            elif self.get_image_tags(SIMPLEPIE_NAMESPACE_RSS_090, "url"):
                return_ = self.get_image_tags(SIMPLEPIE_NAMESPACE_RSS_090, "url")
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(return_[0]))
            elif self.get_image_tags(SIMPLEPIE_NAMESPACE_RSS_20, "url"):
                return_ = self.get_image_tags(SIMPLEPIE_NAMESPACE_RSS_20, "url")
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(return_[0]))
            else:
                return None
            # end if
        # end def get_image_url
        #// 
        #// Get the feed logo's link
        #// 
        #// RSS 0.9.0, 1.0 and 2.0 feeds are allowed to have a "feed logo" link. This
        #// points to a human-readable page that the image should link to.
        #// 
        #// Uses `<itunes:image>`, `<atom:logo>`, `<atom:icon>`,
        #// `<image><title>` or `<image><dc:title>`
        #// 
        #// @return string|null
        #//
        def get_image_link(self):
            
            
            return_ = self.get_image_tags(SIMPLEPIE_NAMESPACE_RSS_10, "link")
            if return_:
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(return_[0]))
            elif self.get_image_tags(SIMPLEPIE_NAMESPACE_RSS_090, "link"):
                return_ = self.get_image_tags(SIMPLEPIE_NAMESPACE_RSS_090, "link")
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(return_[0]))
            elif self.get_image_tags(SIMPLEPIE_NAMESPACE_RSS_20, "link"):
                return_ = self.get_image_tags(SIMPLEPIE_NAMESPACE_RSS_20, "link")
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(return_[0]))
            else:
                return None
            # end if
        # end def get_image_link
        #// 
        #// Get the feed logo's link
        #// 
        #// RSS 2.0 feeds are allowed to have a "feed logo" width.
        #// 
        #// Uses `<image><width>` or defaults to 88.0 if no width is specified and
        #// the feed is an RSS 2.0 feed.
        #// 
        #// @return int|float|null
        #//
        def get_image_width(self):
            
            
            return_ = self.get_image_tags(SIMPLEPIE_NAMESPACE_RSS_20, "width")
            if return_:
                return round(return_[0]["data"])
            elif self.get_type() & SIMPLEPIE_TYPE_RSS_SYNDICATION and self.get_image_tags(SIMPLEPIE_NAMESPACE_RSS_20, "url"):
                return 88
            else:
                return None
            # end if
        # end def get_image_width
        #// 
        #// Get the feed logo's height
        #// 
        #// RSS 2.0 feeds are allowed to have a "feed logo" height.
        #// 
        #// Uses `<image><height>` or defaults to 31.0 if no height is specified and
        #// the feed is an RSS 2.0 feed.
        #// 
        #// @return int|float|null
        #//
        def get_image_height(self):
            
            
            return_ = self.get_image_tags(SIMPLEPIE_NAMESPACE_RSS_20, "height")
            if return_:
                return round(return_[0]["data"])
            elif self.get_type() & SIMPLEPIE_TYPE_RSS_SYNDICATION and self.get_image_tags(SIMPLEPIE_NAMESPACE_RSS_20, "url"):
                return 31
            else:
                return None
            # end if
        # end def get_image_height
        #// 
        #// Get the number of items in the feed
        #// 
        #// This is well-suited for {@link http://php.net/for for()} loops with
        #// {@see get_item()}
        #// 
        #// @param int $max Maximum value to return. 0 for no limit
        #// @return int Number of items in the feed
        #//
        def get_item_quantity(self, max_=0):
            
            
            max_ = php_int(max_)
            qty_ = php_count(self.get_items())
            if max_ == 0:
                return qty_
            else:
                return max_ if qty_ > max_ else qty_
            # end if
        # end def get_item_quantity
        #// 
        #// Get a single item from the feed
        #// 
        #// This is better suited for {@link http://php.net/for for()} loops, whereas
        #// {@see get_items()} is better suited for
        #// {@link http://php.net/foreach foreach()} loops.
        #// 
        #// @see get_item_quantity()
        #// @since Beta 2
        #// @param int $key The item that you want to return.  Remember that arrays begin with 0, not 1
        #// @return SimplePie_Item|null
        #//
        def get_item(self, key_=0):
            
            
            items_ = self.get_items()
            if (php_isset(lambda : items_[key_])):
                return items_[key_]
            else:
                return None
            # end if
        # end def get_item
        #// 
        #// Get all items from the feed
        #// 
        #// This is better suited for {@link http://php.net/for for()} loops, whereas
        #// {@see get_items()} is better suited for
        #// {@link http://php.net/foreach foreach()} loops.
        #// 
        #// @see get_item_quantity
        #// @since Beta 2
        #// @param int $start Index to start at
        #// @param int $end Number of items to return. 0 for all items after `$start`
        #// @return array|null List of {@see SimplePie_Item} objects
        #//
        def get_items(self, start_=0, end_=0):
            
            
            if (not (php_isset(lambda : self.data["items"]))):
                if (not php_empty(lambda : self.multifeed_objects)):
                    self.data["items"] = SimplePie.merge_items(self.multifeed_objects, start_, end_, self.item_limit)
                else:
                    self.data["items"] = Array()
                    items_ = self.get_feed_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "entry")
                    if items_:
                        keys_ = php_array_keys(items_)
                        for key_ in keys_:
                            self.data["items"][-1] = self.registry.create("Item", Array(self, items_[key_]))
                        # end for
                    # end if
                    items_ = self.get_feed_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "entry")
                    if items_:
                        keys_ = php_array_keys(items_)
                        for key_ in keys_:
                            self.data["items"][-1] = self.registry.create("Item", Array(self, items_[key_]))
                        # end for
                    # end if
                    items_ = self.get_feed_tags(SIMPLEPIE_NAMESPACE_RSS_10, "item")
                    if items_:
                        keys_ = php_array_keys(items_)
                        for key_ in keys_:
                            self.data["items"][-1] = self.registry.create("Item", Array(self, items_[key_]))
                        # end for
                    # end if
                    items_ = self.get_feed_tags(SIMPLEPIE_NAMESPACE_RSS_090, "item")
                    if items_:
                        keys_ = php_array_keys(items_)
                        for key_ in keys_:
                            self.data["items"][-1] = self.registry.create("Item", Array(self, items_[key_]))
                        # end for
                    # end if
                    items_ = self.get_channel_tags(SIMPLEPIE_NAMESPACE_RSS_20, "item")
                    if items_:
                        keys_ = php_array_keys(items_)
                        for key_ in keys_:
                            self.data["items"][-1] = self.registry.create("Item", Array(self, items_[key_]))
                        # end for
                    # end if
                # end if
            # end if
            if (not php_empty(lambda : self.data["items"])):
                #// If we want to order it by date, check if all items have a date, and then sort it
                if self.order_by_date and php_empty(lambda : self.multifeed_objects):
                    if (not (php_isset(lambda : self.data["ordered_items"]))):
                        do_sort_ = True
                        for item_ in self.data["items"]:
                            if (not item_.get_date("U")):
                                do_sort_ = False
                                break
                            # end if
                        # end for
                        item_ = None
                        self.data["ordered_items"] = self.data["items"]
                        if do_sort_:
                            usort(self.data["ordered_items"], Array(get_class(self), "sort_items"))
                        # end if
                    # end if
                    items_ = self.data["ordered_items"]
                else:
                    items_ = self.data["items"]
                # end if
                #// Slice the data as desired
                if end_ == 0:
                    return php_array_slice(items_, start_)
                else:
                    return php_array_slice(items_, start_, end_)
                # end if
            else:
                return Array()
            # end if
        # end def get_items
        #// 
        #// Set the favicon handler
        #// 
        #// @deprecated Use your own favicon handling instead
        #//
        def set_favicon_handler(self, page_=None, qs_="i"):
            if page_ is None:
                page_ = False
            # end if
            
            level_ = E_USER_DEPRECATED if php_defined("E_USER_DEPRECATED") else E_USER_WARNING
            trigger_error("Favicon handling has been removed, please use your own handling", level_)
            return False
        # end def set_favicon_handler
        #// 
        #// Get the favicon for the current feed
        #// 
        #// @deprecated Use your own favicon handling instead
        #//
        def get_favicon(self):
            
            
            level_ = E_USER_DEPRECATED if php_defined("E_USER_DEPRECATED") else E_USER_WARNING
            trigger_error("Favicon handling has been removed, please use your own handling", level_)
            url_ = self.get_link()
            if url_ != None:
                return "http://g.etfv.co/" + urlencode(url_)
            # end if
            return False
        # end def get_favicon
        #// 
        #// Magic method handler
        #// 
        #// @param string $method Method name
        #// @param array $args Arguments to the method
        #// @return mixed
        #//
        def __call(self, method_=None, args_=None):
            
            
            if php_strpos(method_, "subscribe_") == 0:
                level_ = E_USER_DEPRECATED if php_defined("E_USER_DEPRECATED") else E_USER_WARNING
                trigger_error("subscribe_*() has been deprecated, implement the callback yourself", level_)
                return ""
            # end if
            if method_ == "enable_xml_dump":
                level_ = E_USER_DEPRECATED if php_defined("E_USER_DEPRECATED") else E_USER_WARNING
                trigger_error("enable_xml_dump() has been deprecated, use get_raw_data() instead", level_)
                return False
            # end if
            class_ = get_class(self)
            trace_ = debug_backtrace()
            file_ = trace_[0]["file"]
            line_ = trace_[0]["line"]
            trigger_error(str("Call to undefined method ") + str(class_) + str("::") + str(method_) + str("() in ") + str(file_) + str(" on line ") + str(line_), E_USER_ERROR)
        # end def __call
        #// 
        #// Sorting callback for items
        #// 
        #// @access private
        #// @param SimplePie $a
        #// @param SimplePie $b
        #// @return boolean
        #//
        @classmethod
        def sort_items(self, a_=None, b_=None):
            
            
            return a_.get_date("U") <= b_.get_date("U")
        # end def sort_items
        #// 
        #// Merge items from several feeds into one
        #// 
        #// If you're merging multiple feeds together, they need to all have dates
        #// for the items or else SimplePie will refuse to sort them.
        #// 
        #// @link http://simplepie.org/wiki/tutorial/sort_multiple_feeds_by_time_and_date#if_feeds_require_separate_per-feed_settings
        #// @param array $urls List of SimplePie feed objects to merge
        #// @param int $start Starting item
        #// @param int $end Number of items to return
        #// @param int $limit Maximum number of items per feed
        #// @return array
        #//
        @classmethod
        def merge_items(self, urls_=None, start_=0, end_=0, limit_=0):
            
            
            if php_is_array(urls_) and sizeof(urls_) > 0:
                items_ = Array()
                for arg_ in urls_:
                    if type(arg_).__name__ == "SimplePie":
                        items_ = php_array_merge(items_, arg_.get_items(0, limit_))
                    else:
                        trigger_error("Arguments must be SimplePie objects", E_USER_WARNING)
                    # end if
                # end for
                do_sort_ = True
                for item_ in items_:
                    if (not item_.get_date("U")):
                        do_sort_ = False
                        break
                    # end if
                # end for
                item_ = None
                if do_sort_:
                    usort(items_, Array(get_class(urls_[0]), "sort_items"))
                # end if
                if end_ == 0:
                    return php_array_slice(items_, start_)
                else:
                    return php_array_slice(items_, start_, end_)
                # end if
            else:
                trigger_error("Cannot merge zero SimplePie objects", E_USER_WARNING)
                return Array()
            # end if
        # end def merge_items
    # end class SimplePie
# end if
