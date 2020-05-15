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
#// Used for feed auto-discovery
#// 
#// 
#// This class can be overloaded with {@see SimplePie::set_locator_class()}
#// 
#// @package SimplePie
#//
class SimplePie_Locator():
    useragent = Array()
    timeout = Array()
    file = Array()
    local = Array()
    elsewhere = Array()
    cached_entities = Array()
    http_base = Array()
    base = Array()
    base_location = 0
    checked_feeds = 0
    max_checked_feeds = 10
    registry = Array()
    def __init__(self, file=None, timeout=10, useragent=None, max_checked_feeds=10):
        
        self.file = file
        self.useragent = useragent
        self.timeout = timeout
        self.max_checked_feeds = max_checked_feeds
        if php_class_exists("DOMDocument"):
            self.dom = php_new_class("DOMDocument", lambda : DOMDocument())
            set_error_handler(Array("SimplePie_Misc", "silence_errors"))
            self.dom.loadhtml(self.file.body)
            restore_error_handler()
        else:
            self.dom = None
        # end if
    # end def __init__
    def set_registry(self, registry=None):
        
        self.registry = registry
    # end def set_registry
    def find(self, type=SIMPLEPIE_LOCATOR_ALL, working=None):
        
        if self.is_feed(self.file):
            return self.file
        # end if
        if self.file.method & SIMPLEPIE_FILE_SOURCE_REMOTE:
            sniffer = self.registry.create("Content_Type_Sniffer", Array(self.file))
            if sniffer.get_type() != "text/html":
                return None
            # end if
        # end if
        if type & (1 << (SIMPLEPIE_LOCATOR_NONE).bit_length()) - 1 - SIMPLEPIE_LOCATOR_NONE:
            self.get_base()
        # end if
        working = self.autodiscovery()
        if type & SIMPLEPIE_LOCATOR_AUTODISCOVERY and working:
            return working[0]
        # end if
        if type & SIMPLEPIE_LOCATOR_LOCAL_EXTENSION | SIMPLEPIE_LOCATOR_LOCAL_BODY | SIMPLEPIE_LOCATOR_REMOTE_EXTENSION | SIMPLEPIE_LOCATOR_REMOTE_BODY and self.get_links():
            working = self.extension(self.local)
            if type & SIMPLEPIE_LOCATOR_LOCAL_EXTENSION and working:
                return working
            # end if
            working = self.body(self.local)
            if type & SIMPLEPIE_LOCATOR_LOCAL_BODY and working:
                return working
            # end if
            working = self.extension(self.elsewhere)
            if type & SIMPLEPIE_LOCATOR_REMOTE_EXTENSION and working:
                return working
            # end if
            working = self.body(self.elsewhere)
            if type & SIMPLEPIE_LOCATOR_REMOTE_BODY and working:
                return working
            # end if
        # end if
        return None
    # end def find
    def is_feed(self, file=None):
        
        if file.method & SIMPLEPIE_FILE_SOURCE_REMOTE:
            sniffer = self.registry.create("Content_Type_Sniffer", Array(file))
            sniffed = sniffer.get_type()
            if php_in_array(sniffed, Array("application/rss+xml", "application/rdf+xml", "text/rdf", "application/atom+xml", "text/xml", "application/xml")):
                return True
            else:
                return False
            # end if
        elif file.method & SIMPLEPIE_FILE_SOURCE_LOCAL:
            return True
        else:
            return False
        # end if
    # end def is_feed
    def get_base(self):
        
        if self.dom == None:
            raise php_new_class("SimplePie_Exception", lambda : SimplePie_Exception("DOMDocument not found, unable to use locator"))
        # end if
        self.http_base = self.file.url
        self.base = self.http_base
        elements = self.dom.getelementsbytagname("base")
        for element in elements:
            if element.hasattribute("href"):
                base = self.registry.call("Misc", "absolutize_url", Array(php_trim(element.getattribute("href")), self.http_base))
                if base == False:
                    continue
                # end if
                self.base = base
                self.base_location = element.getlineno() if php_method_exists(element, "getLineNo") else 0
                break
            # end if
        # end for
    # end def get_base
    def autodiscovery(self):
        
        done = Array()
        feeds = Array()
        feeds = php_array_merge(feeds, self.search_elements_by_tag("link", done, feeds))
        feeds = php_array_merge(feeds, self.search_elements_by_tag("a", done, feeds))
        feeds = php_array_merge(feeds, self.search_elements_by_tag("area", done, feeds))
        if (not php_empty(lambda : feeds)):
            return php_array_values(feeds)
        else:
            return None
        # end if
    # end def autodiscovery
    def search_elements_by_tag(self, name=None, done=None, feeds=None):
        
        if self.dom == None:
            raise php_new_class("SimplePie_Exception", lambda : SimplePie_Exception("DOMDocument not found, unable to use locator"))
        # end if
        links = self.dom.getelementsbytagname(name)
        for link in links:
            if self.checked_feeds == self.max_checked_feeds:
                break
            # end if
            if link.hasattribute("href") and link.hasattribute("rel"):
                rel = array_unique(self.registry.call("Misc", "space_seperated_tokens", Array(php_strtolower(link.getattribute("rel")))))
                line = link.getlineno() if php_method_exists(link, "getLineNo") else 1
                if self.base_location < line:
                    href = self.registry.call("Misc", "absolutize_url", Array(php_trim(link.getattribute("href")), self.base))
                else:
                    href = self.registry.call("Misc", "absolutize_url", Array(php_trim(link.getattribute("href")), self.http_base))
                # end if
                if href == False:
                    continue
                # end if
                if (not php_in_array(href, done)) and php_in_array("feed", rel) or php_in_array("alternate", rel) and (not php_in_array("stylesheet", rel)) and link.hasattribute("type") and php_in_array(php_strtolower(self.registry.call("Misc", "parse_mime", Array(link.getattribute("type")))), Array("application/rss+xml", "application/atom+xml")) and (not (php_isset(lambda : feeds[href]))):
                    self.checked_feeds += 1
                    headers = Array({"Accept": "application/atom+xml, application/rss+xml, application/rdf+xml;q=0.9, application/xml;q=0.8, text/xml;q=0.8, text/html;q=0.7, unknown/unknown;q=0.1, application/unknown;q=0.1, */*;q=0.1"})
                    feed = self.registry.create("File", Array(href, self.timeout, 5, headers, self.useragent))
                    if feed.success and feed.method & SIMPLEPIE_FILE_SOURCE_REMOTE == 0 or feed.status_code == 200 or feed.status_code > 206 and feed.status_code < 300 and self.is_feed(feed):
                        feeds[href] = feed
                    # end if
                # end if
                done[-1] = href
            # end if
        # end for
        return feeds
    # end def search_elements_by_tag
    def get_links(self):
        
        if self.dom == None:
            raise php_new_class("SimplePie_Exception", lambda : SimplePie_Exception("DOMDocument not found, unable to use locator"))
        # end if
        links = self.dom.getelementsbytagname("a")
        for link in links:
            if link.hasattribute("href"):
                href = php_trim(link.getattribute("href"))
                parsed = self.registry.call("Misc", "parse_url", Array(href))
                if parsed["scheme"] == "" or php_preg_match("/^(http(s)|feed)?$/i", parsed["scheme"]):
                    if php_method_exists(link, "getLineNo") and self.base_location < link.getlineno():
                        href = self.registry.call("Misc", "absolutize_url", Array(php_trim(link.getattribute("href")), self.base))
                    else:
                        href = self.registry.call("Misc", "absolutize_url", Array(php_trim(link.getattribute("href")), self.http_base))
                    # end if
                    if href == False:
                        continue
                    # end if
                    current = self.registry.call("Misc", "parse_url", Array(self.file.url))
                    if parsed["authority"] == "" or parsed["authority"] == current["authority"]:
                        self.local[-1] = href
                    else:
                        self.elsewhere[-1] = href
                    # end if
                # end if
            # end if
        # end for
        self.local = array_unique(self.local)
        self.elsewhere = array_unique(self.elsewhere)
        if (not php_empty(lambda : self.local)) or (not php_empty(lambda : self.elsewhere)):
            return True
        # end if
        return None
    # end def get_links
    def extension(self, array=None):
        
        for key,value in array:
            if self.checked_feeds == self.max_checked_feeds:
                break
            # end if
            if php_in_array(php_strtolower(strrchr(value, ".")), Array(".rss", ".rdf", ".atom", ".xml")):
                self.checked_feeds += 1
                headers = Array({"Accept": "application/atom+xml, application/rss+xml, application/rdf+xml;q=0.9, application/xml;q=0.8, text/xml;q=0.8, text/html;q=0.7, unknown/unknown;q=0.1, application/unknown;q=0.1, */*;q=0.1"})
                feed = self.registry.create("File", Array(value, self.timeout, 5, headers, self.useragent))
                if feed.success and feed.method & SIMPLEPIE_FILE_SOURCE_REMOTE == 0 or feed.status_code == 200 or feed.status_code > 206 and feed.status_code < 300 and self.is_feed(feed):
                    return feed
                else:
                    array[key] = None
                # end if
            # end if
        # end for
        return None
    # end def extension
    def body(self, array=None):
        
        for key,value in array:
            if self.checked_feeds == self.max_checked_feeds:
                break
            # end if
            if php_preg_match("/(rss|rdf|atom|xml)/i", value):
                self.checked_feeds += 1
                headers = Array({"Accept": "application/atom+xml, application/rss+xml, application/rdf+xml;q=0.9, application/xml;q=0.8, text/xml;q=0.8, text/html;q=0.7, unknown/unknown;q=0.1, application/unknown;q=0.1, */*;q=0.1"})
                feed = self.registry.create("File", Array(value, self.timeout, 5, None, self.useragent))
                if feed.success and feed.method & SIMPLEPIE_FILE_SOURCE_REMOTE == 0 or feed.status_code == 200 or feed.status_code > 206 and feed.status_code < 300 and self.is_feed(feed):
                    return feed
                else:
                    array[key] = None
                # end if
            # end if
        # end for
        return None
    # end def body
# end class SimplePie_Locator
