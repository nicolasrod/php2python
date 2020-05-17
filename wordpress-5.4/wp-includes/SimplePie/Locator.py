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
    file_ = Array()
    local = Array()
    elsewhere = Array()
    cached_entities = Array()
    http_base = Array()
    base = Array()
    base_location = 0
    checked_feeds = 0
    max_checked_feeds = 10
    registry = Array()
    def __init__(self, file_=None, timeout_=10, useragent_=None, max_checked_feeds_=10):
        if useragent_ is None:
            useragent_ = None
        # end if
        
        self.file_ = file_
        self.useragent = useragent_
        self.timeout = timeout_
        self.max_checked_feeds = max_checked_feeds_
        if php_class_exists("DOMDocument"):
            self.dom = php_new_class("DOMDocument", lambda : DOMDocument())
            set_error_handler(Array("SimplePie_Misc", "silence_errors"))
            self.dom.loadhtml(self.file_.body)
            restore_error_handler()
        else:
            self.dom = None
        # end if
    # end def __init__
    def set_registry(self, registry_=None):
        
        
        self.registry = registry_
    # end def set_registry
    def find(self, type_=None, working_=None):
        if type_ is None:
            type_ = SIMPLEPIE_LOCATOR_ALL
        # end if
        
        if self.is_feed(self.file_):
            return self.file_
        # end if
        if self.file_.method & SIMPLEPIE_FILE_SOURCE_REMOTE:
            sniffer_ = self.registry.create("Content_Type_Sniffer", Array(self.file_))
            if sniffer_.get_type() != "text/html":
                return None
            # end if
        # end if
        if type_ & (1 << (SIMPLEPIE_LOCATOR_NONE).bit_length()) - 1 - SIMPLEPIE_LOCATOR_NONE:
            self.get_base()
        # end if
        working_ = self.autodiscovery()
        if type_ & SIMPLEPIE_LOCATOR_AUTODISCOVERY and working_:
            return working_[0]
        # end if
        if type_ & SIMPLEPIE_LOCATOR_LOCAL_EXTENSION | SIMPLEPIE_LOCATOR_LOCAL_BODY | SIMPLEPIE_LOCATOR_REMOTE_EXTENSION | SIMPLEPIE_LOCATOR_REMOTE_BODY and self.get_links():
            working_ = self.extension(self.local)
            if type_ & SIMPLEPIE_LOCATOR_LOCAL_EXTENSION and working_:
                return working_
            # end if
            working_ = self.body(self.local)
            if type_ & SIMPLEPIE_LOCATOR_LOCAL_BODY and working_:
                return working_
            # end if
            working_ = self.extension(self.elsewhere)
            if type_ & SIMPLEPIE_LOCATOR_REMOTE_EXTENSION and working_:
                return working_
            # end if
            working_ = self.body(self.elsewhere)
            if type_ & SIMPLEPIE_LOCATOR_REMOTE_BODY and working_:
                return working_
            # end if
        # end if
        return None
    # end def find
    def is_feed(self, file_=None):
        
        
        if file_.method & SIMPLEPIE_FILE_SOURCE_REMOTE:
            sniffer_ = self.registry.create("Content_Type_Sniffer", Array(file_))
            sniffed_ = sniffer_.get_type()
            if php_in_array(sniffed_, Array("application/rss+xml", "application/rdf+xml", "text/rdf", "application/atom+xml", "text/xml", "application/xml")):
                return True
            else:
                return False
            # end if
        elif file_.method & SIMPLEPIE_FILE_SOURCE_LOCAL:
            return True
        else:
            return False
        # end if
    # end def is_feed
    def get_base(self):
        
        
        if self.dom == None:
            raise php_new_class("SimplePie_Exception", lambda : SimplePie_Exception("DOMDocument not found, unable to use locator"))
        # end if
        self.http_base = self.file_.url
        self.base = self.http_base
        elements_ = self.dom.getelementsbytagname("base")
        for element_ in elements_:
            if element_.hasattribute("href"):
                base_ = self.registry.call("Misc", "absolutize_url", Array(php_trim(element_.getattribute("href")), self.http_base))
                if base_ == False:
                    continue
                # end if
                self.base = base_
                self.base_location = element_.getlineno() if php_method_exists(element_, "getLineNo") else 0
                break
            # end if
        # end for
    # end def get_base
    def autodiscovery(self):
        
        
        done_ = Array()
        feeds_ = Array()
        feeds_ = php_array_merge(feeds_, self.search_elements_by_tag("link", done_, feeds_))
        feeds_ = php_array_merge(feeds_, self.search_elements_by_tag("a", done_, feeds_))
        feeds_ = php_array_merge(feeds_, self.search_elements_by_tag("area", done_, feeds_))
        if (not php_empty(lambda : feeds_)):
            return php_array_values(feeds_)
        else:
            return None
        # end if
    # end def autodiscovery
    def search_elements_by_tag(self, name_=None, done_=None, feeds_=None):
        
        
        if self.dom == None:
            raise php_new_class("SimplePie_Exception", lambda : SimplePie_Exception("DOMDocument not found, unable to use locator"))
        # end if
        links_ = self.dom.getelementsbytagname(name_)
        for link_ in links_:
            if self.checked_feeds == self.max_checked_feeds:
                break
            # end if
            if link_.hasattribute("href") and link_.hasattribute("rel"):
                rel_ = array_unique(self.registry.call("Misc", "space_seperated_tokens", Array(php_strtolower(link_.getattribute("rel")))))
                line_ = link_.getlineno() if php_method_exists(link_, "getLineNo") else 1
                if self.base_location < line_:
                    href_ = self.registry.call("Misc", "absolutize_url", Array(php_trim(link_.getattribute("href")), self.base))
                else:
                    href_ = self.registry.call("Misc", "absolutize_url", Array(php_trim(link_.getattribute("href")), self.http_base))
                # end if
                if href_ == False:
                    continue
                # end if
                if (not php_in_array(href_, done_)) and php_in_array("feed", rel_) or php_in_array("alternate", rel_) and (not php_in_array("stylesheet", rel_)) and link_.hasattribute("type") and php_in_array(php_strtolower(self.registry.call("Misc", "parse_mime", Array(link_.getattribute("type")))), Array("application/rss+xml", "application/atom+xml")) and (not (php_isset(lambda : feeds_[href_]))):
                    self.checked_feeds += 1
                    headers_ = Array({"Accept": "application/atom+xml, application/rss+xml, application/rdf+xml;q=0.9, application/xml;q=0.8, text/xml;q=0.8, text/html;q=0.7, unknown/unknown;q=0.1, application/unknown;q=0.1, */*;q=0.1"})
                    feed_ = self.registry.create("File", Array(href_, self.timeout, 5, headers_, self.useragent))
                    if feed_.success and feed_.method & SIMPLEPIE_FILE_SOURCE_REMOTE == 0 or feed_.status_code == 200 or feed_.status_code > 206 and feed_.status_code < 300 and self.is_feed(feed_):
                        feeds_[href_] = feed_
                    # end if
                # end if
                done_[-1] = href_
            # end if
        # end for
        return feeds_
    # end def search_elements_by_tag
    def get_links(self):
        
        
        if self.dom == None:
            raise php_new_class("SimplePie_Exception", lambda : SimplePie_Exception("DOMDocument not found, unable to use locator"))
        # end if
        links_ = self.dom.getelementsbytagname("a")
        for link_ in links_:
            if link_.hasattribute("href"):
                href_ = php_trim(link_.getattribute("href"))
                parsed_ = self.registry.call("Misc", "parse_url", Array(href_))
                if parsed_["scheme"] == "" or php_preg_match("/^(http(s)|feed)?$/i", parsed_["scheme"]):
                    if php_method_exists(link_, "getLineNo") and self.base_location < link_.getlineno():
                        href_ = self.registry.call("Misc", "absolutize_url", Array(php_trim(link_.getattribute("href")), self.base))
                    else:
                        href_ = self.registry.call("Misc", "absolutize_url", Array(php_trim(link_.getattribute("href")), self.http_base))
                    # end if
                    if href_ == False:
                        continue
                    # end if
                    current_ = self.registry.call("Misc", "parse_url", Array(self.file_.url))
                    if parsed_["authority"] == "" or parsed_["authority"] == current_["authority"]:
                        self.local[-1] = href_
                    else:
                        self.elsewhere[-1] = href_
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
    def extension(self, array_=None):
        
        
        for key_,value_ in array_:
            if self.checked_feeds == self.max_checked_feeds:
                break
            # end if
            if php_in_array(php_strtolower(strrchr(value_, ".")), Array(".rss", ".rdf", ".atom", ".xml")):
                self.checked_feeds += 1
                headers_ = Array({"Accept": "application/atom+xml, application/rss+xml, application/rdf+xml;q=0.9, application/xml;q=0.8, text/xml;q=0.8, text/html;q=0.7, unknown/unknown;q=0.1, application/unknown;q=0.1, */*;q=0.1"})
                feed_ = self.registry.create("File", Array(value_, self.timeout, 5, headers_, self.useragent))
                if feed_.success and feed_.method & SIMPLEPIE_FILE_SOURCE_REMOTE == 0 or feed_.status_code == 200 or feed_.status_code > 206 and feed_.status_code < 300 and self.is_feed(feed_):
                    return feed_
                else:
                    array_[key_] = None
                # end if
            # end if
        # end for
        return None
    # end def extension
    def body(self, array_=None):
        
        
        for key_,value_ in array_:
            if self.checked_feeds == self.max_checked_feeds:
                break
            # end if
            if php_preg_match("/(rss|rdf|atom|xml)/i", value_):
                self.checked_feeds += 1
                headers_ = Array({"Accept": "application/atom+xml, application/rss+xml, application/rdf+xml;q=0.9, application/xml;q=0.8, text/xml;q=0.8, text/html;q=0.7, unknown/unknown;q=0.1, application/unknown;q=0.1, */*;q=0.1"})
                feed_ = self.registry.create("File", Array(value_, self.timeout, 5, None, self.useragent))
                if feed_.success and feed_.method & SIMPLEPIE_FILE_SOURCE_REMOTE == 0 or feed_.status_code == 200 or feed_.status_code > 206 and feed_.status_code < 300 and self.is_feed(feed_):
                    return feed_
                else:
                    array_[key_] = None
                # end if
            # end if
        # end for
        return None
    # end def body
# end class SimplePie_Locator
