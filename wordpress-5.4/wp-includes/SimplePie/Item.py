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
#// Manages all item-related data
#// 
#// Used by {@see SimplePie::get_item()} and {@see SimplePie::get_items()}
#// 
#// This class can be overloaded with {@see SimplePie::set_item_class()}
#// 
#// @package SimplePie
#// @subpackage API
#//
class SimplePie_Item():
    feed = Array()
    data = Array()
    registry = Array()
    #// 
    #// Create a new item object
    #// 
    #// This is usually used by {@see SimplePie::get_items} and
    #// {@see SimplePie::get_item}. Avoid creating this manually.
    #// 
    #// @param SimplePie $feed Parent feed
    #// @param array $data Raw data
    #//
    def __init__(self, feed=None, data=None):
        
        self.feed = feed
        self.data = data
    # end def __init__
    #// 
    #// Set the registry handler
    #// 
    #// This is usually used by {@see SimplePie_Registry::create}
    #// 
    #// @since 1.3
    #// @param SimplePie_Registry $registry
    #//
    def set_registry(self, registry=None):
        
        self.registry = registry
    # end def set_registry
    #// 
    #// Get a string representation of the item
    #// 
    #// @return string
    #//
    def __tostring(self):
        
        return php_md5(serialize(self.data))
    # end def __tostring
    #// 
    #// Remove items that link back to this before destroying this object
    #//
    def __del__(self):
        
        if php_version_compare(PHP_VERSION, "5.3", "<") or (not php_gc_enabled()) and (not php_ini_get("zend.ze1_compatibility_mode")):
            self.feed = None
        # end if
    # end def __del__
    #// 
    #// Get data for an item-level element
    #// 
    #// This method allows you to get access to ANY element/attribute that is a
    #// sub-element of the item/entry tag.
    #// 
    #// See {@see SimplePie::get_feed_tags()} for a description of the return value
    #// 
    #// @since 1.0
    #// @see http://simplepie.org/wiki/faq/supported_xml_namespaces
    #// @param string $namespace The URL of the XML namespace of the elements you're trying to access
    #// @param string $tag Tag name
    #// @return array
    #//
    def get_item_tags(self, namespace=None, tag=None):
        
        if (php_isset(lambda : self.data["child"][namespace][tag])):
            return self.data["child"][namespace][tag]
        else:
            return None
        # end if
    # end def get_item_tags
    #// 
    #// Get the base URL value from the parent feed
    #// 
    #// Uses `<xml:base>`
    #// 
    #// @param array $element
    #// @return string
    #//
    def get_base(self, element=Array()):
        
        return self.feed.get_base(element)
    # end def get_base
    #// 
    #// Sanitize feed data
    #// 
    #// @access private
    #// @see SimplePie::sanitize()
    #// @param string $data Data to sanitize
    #// @param int $type One of the SIMPLEPIE_CONSTRUCT_* constants
    #// @param string $base Base URL to resolve URLs against
    #// @return string Sanitized data
    #//
    def sanitize(self, data=None, type=None, base=""):
        
        return self.feed.sanitize(data, type, base)
    # end def sanitize
    #// 
    #// Get the parent feed
    #// 
    #// Note: this may not work as you think for multifeeds!
    #// 
    #// @link http://simplepie.org/faq/typical_multifeed_gotchas#missing_data_from_feed
    #// @since 1.0
    #// @return SimplePie
    #//
    def get_feed(self):
        
        return self.feed
    # end def get_feed
    #// 
    #// Get the unique identifier for the item
    #// 
    #// This is usually used when writing code to check for new items in a feed.
    #// 
    #// Uses `<atom:id>`, `<guid>`, `<dc:identifier>` or the `about` attribute
    #// for RDF. If none of these are supplied (or `$hash` is true), creates an
    #// MD5 hash based on the permalink and title. If either of those are not
    #// supplied, creates a hash based on the full feed data.
    #// 
    #// @since Beta 2
    #// @param boolean $hash Should we force using a hash instead of the supplied ID?
    #// @return string
    #//
    def get_id(self, hash=False):
        
        if (not hash):
            return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "id")
            if return_:
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
            elif self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "id"):
                return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "id")
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
            elif self.get_item_tags(SIMPLEPIE_NAMESPACE_RSS_20, "guid"):
                return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_RSS_20, "guid")
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
            elif self.get_item_tags(SIMPLEPIE_NAMESPACE_DC_11, "identifier"):
                return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_DC_11, "identifier")
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
            elif self.get_item_tags(SIMPLEPIE_NAMESPACE_DC_10, "identifier"):
                return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_DC_10, "identifier")
                return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
            elif (php_isset(lambda : self.data["attribs"][SIMPLEPIE_NAMESPACE_RDF]["about"])):
                return self.sanitize(self.data["attribs"][SIMPLEPIE_NAMESPACE_RDF]["about"], SIMPLEPIE_CONSTRUCT_TEXT)
            elif self.get_permalink() != None:
                return_ = self.get_permalink()
                return return_
            elif self.get_title() != None:
                return_ = self.get_title()
                return return_
            # end if
        # end if
        if self.get_permalink() != None or self.get_title() != None:
            return php_md5(self.get_permalink() + self.get_title())
        else:
            return php_md5(serialize(self.data))
        # end if
    # end def get_id
    #// 
    #// Get the title of the item
    #// 
    #// Uses `<atom:title>`, `<title>` or `<dc:title>`
    #// 
    #// @since Beta 2 (previously called `get_item_title` since 0.8)
    #// @return string|null
    #//
    def get_title(self):
        
        if (not (php_isset(lambda : self.data["title"]))):
            return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "title")
            if return_:
                self.data["title"] = self.sanitize(return_[0]["data"], self.registry.call("Misc", "atom_10_construct_type", Array(return_[0]["attribs"])), self.get_base(return_[0]))
            elif self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "title"):
                return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "title")
                self.data["title"] = self.sanitize(return_[0]["data"], self.registry.call("Misc", "atom_03_construct_type", Array(return_[0]["attribs"])), self.get_base(return_[0]))
            elif self.get_item_tags(SIMPLEPIE_NAMESPACE_RSS_10, "title"):
                return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_RSS_10, "title")
                self.data["title"] = self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_MAYBE_HTML, self.get_base(return_[0]))
            elif self.get_item_tags(SIMPLEPIE_NAMESPACE_RSS_090, "title"):
                return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_RSS_090, "title")
                self.data["title"] = self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_MAYBE_HTML, self.get_base(return_[0]))
            elif self.get_item_tags(SIMPLEPIE_NAMESPACE_RSS_20, "title"):
                return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_RSS_20, "title")
                self.data["title"] = self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_MAYBE_HTML, self.get_base(return_[0]))
            elif self.get_item_tags(SIMPLEPIE_NAMESPACE_DC_11, "title"):
                return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_DC_11, "title")
                self.data["title"] = self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
            elif self.get_item_tags(SIMPLEPIE_NAMESPACE_DC_10, "title"):
                return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_DC_10, "title")
                self.data["title"] = self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
            else:
                self.data["title"] = None
            # end if
        # end if
        return self.data["title"]
    # end def get_title
    #// 
    #// Get the content for the item
    #// 
    #// Prefers summaries over full content , but will return full content if a
    #// summary does not exist.
    #// 
    #// To prefer full content instead, use {@see get_content}
    #// 
    #// Uses `<atom:summary>`, `<description>`, `<dc:description>` or
    #// `<itunes:subtitle>`
    #// 
    #// @since 0.8
    #// @param boolean $description_only Should we avoid falling back to the content?
    #// @return string|null
    #//
    def get_description(self, description_only=False):
        
        return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "summary")
        if return_:
            return self.sanitize(return_[0]["data"], self.registry.call("Misc", "atom_10_construct_type", Array(return_[0]["attribs"])), self.get_base(return_[0]))
        elif self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "summary"):
            return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "summary")
            return self.sanitize(return_[0]["data"], self.registry.call("Misc", "atom_03_construct_type", Array(return_[0]["attribs"])), self.get_base(return_[0]))
        elif self.get_item_tags(SIMPLEPIE_NAMESPACE_RSS_10, "description"):
            return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_RSS_10, "description")
            return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_MAYBE_HTML, self.get_base(return_[0]))
        elif self.get_item_tags(SIMPLEPIE_NAMESPACE_RSS_20, "description"):
            return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_RSS_20, "description")
            return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_HTML, self.get_base(return_[0]))
        elif self.get_item_tags(SIMPLEPIE_NAMESPACE_DC_11, "description"):
            return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_DC_11, "description")
            return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
        elif self.get_item_tags(SIMPLEPIE_NAMESPACE_DC_10, "description"):
            return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_DC_10, "description")
            return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
        elif self.get_item_tags(SIMPLEPIE_NAMESPACE_ITUNES, "summary"):
            return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_ITUNES, "summary")
            return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_HTML, self.get_base(return_[0]))
        elif self.get_item_tags(SIMPLEPIE_NAMESPACE_ITUNES, "subtitle"):
            return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_ITUNES, "subtitle")
            return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
        elif self.get_item_tags(SIMPLEPIE_NAMESPACE_RSS_090, "description"):
            return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_RSS_090, "description")
            return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_HTML)
        elif (not description_only):
            return self.get_content(True)
        else:
            return None
        # end if
    # end def get_description
    #// 
    #// Get the content for the item
    #// 
    #// Prefers full content over summaries, but will return a summary if full
    #// content does not exist.
    #// 
    #// To prefer summaries instead, use {@see get_description}
    #// 
    #// Uses `<atom:content>` or `<content:encoded>` (RSS 1.0 Content Module)
    #// 
    #// @since 1.0
    #// @param boolean $content_only Should we avoid falling back to the description?
    #// @return string|null
    #//
    def get_content(self, content_only=False):
        
        return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "content")
        if return_:
            return self.sanitize(return_[0]["data"], self.registry.call("Misc", "atom_10_content_construct_type", Array(return_[0]["attribs"])), self.get_base(return_[0]))
        elif self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "content"):
            return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "content")
            return self.sanitize(return_[0]["data"], self.registry.call("Misc", "atom_03_construct_type", Array(return_[0]["attribs"])), self.get_base(return_[0]))
        elif self.get_item_tags(SIMPLEPIE_NAMESPACE_RSS_10_MODULES_CONTENT, "encoded"):
            return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_RSS_10_MODULES_CONTENT, "encoded")
            return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_HTML, self.get_base(return_[0]))
        elif (not content_only):
            return self.get_description(True)
        else:
            return None
        # end if
    # end def get_content
    #// 
    #// Get a category for the item
    #// 
    #// @since Beta 3 (previously called `get_categories()` since Beta 2)
    #// @param int $key The category that you want to return.  Remember that arrays begin with 0, not 1
    #// @return SimplePie_Category|null
    #//
    def get_category(self, key=0):
        
        categories = self.get_categories()
        if (php_isset(lambda : categories[key])):
            return categories[key]
        else:
            return None
        # end if
    # end def get_category
    #// 
    #// Get all categories for the item
    #// 
    #// Uses `<atom:category>`, `<category>` or `<dc:subject>`
    #// 
    #// @since Beta 3
    #// @return array|null List of {@see SimplePie_Category} objects
    #//
    def get_categories(self):
        
        categories = Array()
        for category in self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "category"):
            term = None
            scheme = None
            label = None
            if (php_isset(lambda : category["attribs"][""]["term"])):
                term = self.sanitize(category["attribs"][""]["term"], SIMPLEPIE_CONSTRUCT_TEXT)
            # end if
            if (php_isset(lambda : category["attribs"][""]["scheme"])):
                scheme = self.sanitize(category["attribs"][""]["scheme"], SIMPLEPIE_CONSTRUCT_TEXT)
            # end if
            if (php_isset(lambda : category["attribs"][""]["label"])):
                label = self.sanitize(category["attribs"][""]["label"], SIMPLEPIE_CONSTRUCT_TEXT)
            # end if
            categories[-1] = self.registry.create("Category", Array(term, scheme, label))
        # end for
        for category in self.get_item_tags(SIMPLEPIE_NAMESPACE_RSS_20, "category"):
            #// This is really the label, but keep this as the term also for BC.
            #// Label will also work on retrieving because that falls back to term.
            term = self.sanitize(category["data"], SIMPLEPIE_CONSTRUCT_TEXT)
            if (php_isset(lambda : category["attribs"][""]["domain"])):
                scheme = self.sanitize(category["attribs"][""]["domain"], SIMPLEPIE_CONSTRUCT_TEXT)
            else:
                scheme = None
            # end if
            categories[-1] = self.registry.create("Category", Array(term, scheme, None))
        # end for
        for category in self.get_item_tags(SIMPLEPIE_NAMESPACE_DC_11, "subject"):
            categories[-1] = self.registry.create("Category", Array(self.sanitize(category["data"], SIMPLEPIE_CONSTRUCT_TEXT), None, None))
        # end for
        for category in self.get_item_tags(SIMPLEPIE_NAMESPACE_DC_10, "subject"):
            categories[-1] = self.registry.create("Category", Array(self.sanitize(category["data"], SIMPLEPIE_CONSTRUCT_TEXT), None, None))
        # end for
        if (not php_empty(lambda : categories)):
            return array_unique(categories)
        else:
            return None
        # end if
    # end def get_categories
    #// 
    #// Get an author for the item
    #// 
    #// @since Beta 2
    #// @param int $key The author that you want to return.  Remember that arrays begin with 0, not 1
    #// @return SimplePie_Author|null
    #//
    def get_author(self, key=0):
        
        authors = self.get_authors()
        if (php_isset(lambda : authors[key])):
            return authors[key]
        else:
            return None
        # end if
    # end def get_author
    #// 
    #// Get a contributor for the item
    #// 
    #// @since 1.1
    #// @param int $key The contrbutor that you want to return.  Remember that arrays begin with 0, not 1
    #// @return SimplePie_Author|null
    #//
    def get_contributor(self, key=0):
        
        contributors = self.get_contributors()
        if (php_isset(lambda : contributors[key])):
            return contributors[key]
        else:
            return None
        # end if
    # end def get_contributor
    #// 
    #// Get all contributors for the item
    #// 
    #// Uses `<atom:contributor>`
    #// 
    #// @since 1.1
    #// @return array|null List of {@see SimplePie_Author} objects
    #//
    def get_contributors(self):
        
        contributors = Array()
        for contributor in self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "contributor"):
            name = None
            uri = None
            email = None
            if (php_isset(lambda : contributor["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["name"][0]["data"])):
                name = self.sanitize(contributor["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["name"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
            # end if
            if (php_isset(lambda : contributor["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["uri"][0]["data"])):
                uri = self.sanitize(contributor["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["uri"][0]["data"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(contributor["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["uri"][0]))
            # end if
            if (php_isset(lambda : contributor["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["email"][0]["data"])):
                email = self.sanitize(contributor["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["email"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
            # end if
            if name != None or email != None or uri != None:
                contributors[-1] = self.registry.create("Author", Array(name, uri, email))
            # end if
        # end for
        for contributor in self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "contributor"):
            name = None
            url = None
            email = None
            if (php_isset(lambda : contributor["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["name"][0]["data"])):
                name = self.sanitize(contributor["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["name"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
            # end if
            if (php_isset(lambda : contributor["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["url"][0]["data"])):
                url = self.sanitize(contributor["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["url"][0]["data"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(contributor["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["url"][0]))
            # end if
            if (php_isset(lambda : contributor["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["email"][0]["data"])):
                email = self.sanitize(contributor["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["email"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
            # end if
            if name != None or email != None or url != None:
                contributors[-1] = self.registry.create("Author", Array(name, url, email))
            # end if
        # end for
        if (not php_empty(lambda : contributors)):
            return array_unique(contributors)
        else:
            return None
        # end if
    # end def get_contributors
    #// 
    #// Get all authors for the item
    #// 
    #// Uses `<atom:author>`, `<author>`, `<dc:creator>` or `<itunes:author>`
    #// 
    #// @since Beta 2
    #// @return array|null List of {@see SimplePie_Author} objects
    #//
    def get_authors(self):
        
        authors = Array()
        for author in self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "author"):
            name = None
            uri = None
            email = None
            if (php_isset(lambda : author["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["name"][0]["data"])):
                name = self.sanitize(author["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["name"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
            # end if
            if (php_isset(lambda : author["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["uri"][0]["data"])):
                uri = self.sanitize(author["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["uri"][0]["data"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(author["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["uri"][0]))
            # end if
            if (php_isset(lambda : author["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["email"][0]["data"])):
                email = self.sanitize(author["child"][SIMPLEPIE_NAMESPACE_ATOM_10]["email"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
            # end if
            if name != None or email != None or uri != None:
                authors[-1] = self.registry.create("Author", Array(name, uri, email))
            # end if
        # end for
        author = self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "author")
        if author:
            name = None
            url = None
            email = None
            if (php_isset(lambda : author[0]["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["name"][0]["data"])):
                name = self.sanitize(author[0]["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["name"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
            # end if
            if (php_isset(lambda : author[0]["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["url"][0]["data"])):
                url = self.sanitize(author[0]["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["url"][0]["data"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(author[0]["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["url"][0]))
            # end if
            if (php_isset(lambda : author[0]["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["email"][0]["data"])):
                email = self.sanitize(author[0]["child"][SIMPLEPIE_NAMESPACE_ATOM_03]["email"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
            # end if
            if name != None or email != None or url != None:
                authors[-1] = self.registry.create("Author", Array(name, url, email))
            # end if
        # end if
        author = self.get_item_tags(SIMPLEPIE_NAMESPACE_RSS_20, "author")
        if author:
            authors[-1] = self.registry.create("Author", Array(None, None, self.sanitize(author[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)))
        # end if
        for author in self.get_item_tags(SIMPLEPIE_NAMESPACE_DC_11, "creator"):
            authors[-1] = self.registry.create("Author", Array(self.sanitize(author["data"], SIMPLEPIE_CONSTRUCT_TEXT), None, None))
        # end for
        for author in self.get_item_tags(SIMPLEPIE_NAMESPACE_DC_10, "creator"):
            authors[-1] = self.registry.create("Author", Array(self.sanitize(author["data"], SIMPLEPIE_CONSTRUCT_TEXT), None, None))
        # end for
        for author in self.get_item_tags(SIMPLEPIE_NAMESPACE_ITUNES, "author"):
            authors[-1] = self.registry.create("Author", Array(self.sanitize(author["data"], SIMPLEPIE_CONSTRUCT_TEXT), None, None))
        # end for
        if (not php_empty(lambda : authors)):
            return array_unique(authors)
        elif self.get_source() and source.get_authors():
            source = self.get_source()
            authors = source.get_authors()
            return authors
        elif self.feed.get_authors():
            authors = self.feed.get_authors()
            return authors
        else:
            return None
        # end if
    # end def get_authors
    #// 
    #// Get the copyright info for the item
    #// 
    #// Uses `<atom:rights>` or `<dc:rights>`
    #// 
    #// @since 1.1
    #// @return string
    #//
    def get_copyright(self):
        
        return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "rights")
        if return_:
            return self.sanitize(return_[0]["data"], self.registry.call("Misc", "atom_10_construct_type", Array(return_[0]["attribs"])), self.get_base(return_[0]))
        elif self.get_item_tags(SIMPLEPIE_NAMESPACE_DC_11, "rights"):
            return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_DC_11, "rights")
            return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
        elif self.get_item_tags(SIMPLEPIE_NAMESPACE_DC_10, "rights"):
            return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_DC_10, "rights")
            return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
        else:
            return None
        # end if
    # end def get_copyright
    #// 
    #// Get the posting date/time for the item
    #// 
    #// Uses `<atom:published>`, `<atom:updated>`, `<atom:issued>`,
    #// `<atom:modified>`, `<pubDate>` or `<dc:date>`
    #// 
    #// Note: obeys PHP's timezone setting. To get a UTC date/time, use
    #// {@see get_gmdate}
    #// 
    #// @since Beta 2 (previously called `get_item_date` since 0.8)
    #// 
    #// @param string $date_format Supports any PHP date format from {@see http://php.net/date} (empty for the raw data)
    #// @return int|string|null
    #//
    def get_date(self, date_format="j F Y, g:i a"):
        
        if (not (php_isset(lambda : self.data["date"]))):
            return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "published")
            if return_:
                self.data["date"]["raw"] = return_[0]["data"]
            elif self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "updated"):
                return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "updated")
                self.data["date"]["raw"] = return_[0]["data"]
            elif self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "issued"):
                return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "issued")
                self.data["date"]["raw"] = return_[0]["data"]
            elif self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "created"):
                return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "created")
                self.data["date"]["raw"] = return_[0]["data"]
            elif self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "modified"):
                return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "modified")
                self.data["date"]["raw"] = return_[0]["data"]
            elif self.get_item_tags(SIMPLEPIE_NAMESPACE_RSS_20, "pubDate"):
                return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_RSS_20, "pubDate")
                self.data["date"]["raw"] = return_[0]["data"]
            elif self.get_item_tags(SIMPLEPIE_NAMESPACE_DC_11, "date"):
                return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_DC_11, "date")
                self.data["date"]["raw"] = return_[0]["data"]
            elif self.get_item_tags(SIMPLEPIE_NAMESPACE_DC_10, "date"):
                return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_DC_10, "date")
                self.data["date"]["raw"] = return_[0]["data"]
            # end if
            if (not php_empty(lambda : self.data["date"]["raw"])):
                parser = self.registry.call("Parse_Date", "get")
                self.data["date"]["parsed"] = parser.parse(self.data["date"]["raw"])
            else:
                self.data["date"] = None
            # end if
        # end if
        if self.data["date"]:
            date_format = str(date_format)
            for case in Switch(date_format):
                if case(""):
                    return self.sanitize(self.data["date"]["raw"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
                if case("U"):
                    return self.data["date"]["parsed"]
                # end if
                if case():
                    return date(date_format, self.data["date"]["parsed"])
                # end if
            # end for
        else:
            return None
        # end if
    # end def get_date
    #// 
    #// Get the update date/time for the item
    #// 
    #// Uses `<atom:updated>`
    #// 
    #// Note: obeys PHP's timezone setting. To get a UTC date/time, use
    #// {@see get_gmdate}
    #// 
    #// @param string $date_format Supports any PHP date format from {@see http://php.net/date} (empty for the raw data)
    #// @return int|string|null
    #//
    def get_updated_date(self, date_format="j F Y, g:i a"):
        
        if (not (php_isset(lambda : self.data["updated"]))):
            return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "updated")
            if return_:
                self.data["updated"]["raw"] = return_[0]["data"]
            # end if
            if (not php_empty(lambda : self.data["updated"]["raw"])):
                parser = self.registry.call("Parse_Date", "get")
                self.data["updated"]["parsed"] = parser.parse(self.data["date"]["raw"])
            else:
                self.data["updated"] = None
            # end if
        # end if
        if self.data["updated"]:
            date_format = str(date_format)
            for case in Switch(date_format):
                if case(""):
                    return self.sanitize(self.data["updated"]["raw"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
                if case("U"):
                    return self.data["updated"]["parsed"]
                # end if
                if case():
                    return date(date_format, self.data["updated"]["parsed"])
                # end if
            # end for
        else:
            return None
        # end if
    # end def get_updated_date
    #// 
    #// Get the localized posting date/time for the item
    #// 
    #// Returns the date formatted in the localized language. To display in
    #// languages other than the server's default, you need to change the locale
    #// with {@link http://php.net/setlocale setlocale()}. The available
    #// localizations depend on which ones are installed on your web server.
    #// 
    #// @since 1.0
    #// 
    #// @param string $date_format Supports any PHP date format from {@see http://php.net/strftime} (empty for the raw data)
    #// @return int|string|null
    #//
    def get_local_date(self, date_format="%c"):
        
        if (not date_format):
            return self.sanitize(self.get_date(""), SIMPLEPIE_CONSTRUCT_TEXT)
        elif self.get_date("U") != None and date != False:
            date = self.get_date("U")
            return strftime(date_format, date)
        else:
            return None
        # end if
    # end def get_local_date
    #// 
    #// Get the posting date/time for the item (UTC time)
    #// 
    #// @see get_date
    #// @param string $date_format Supports any PHP date format from {@see http://php.net/date}
    #// @return int|string|null
    #//
    def get_gmdate(self, date_format="j F Y, g:i a"):
        
        date = self.get_date("U")
        if date == None:
            return None
        # end if
        return gmdate(date_format, date)
    # end def get_gmdate
    #// 
    #// Get the update date/time for the item (UTC time)
    #// 
    #// @see get_updated_date
    #// @param string $date_format Supports any PHP date format from {@see http://php.net/date}
    #// @return int|string|null
    #//
    def get_updated_gmdate(self, date_format="j F Y, g:i a"):
        
        date = self.get_updated_date("U")
        if date == None:
            return None
        # end if
        return gmdate(date_format, date)
    # end def get_updated_gmdate
    #// 
    #// Get the permalink for the item
    #// 
    #// Returns the first link available with a relationship of "alternate".
    #// Identical to {@see get_link()} with key 0
    #// 
    #// @see get_link
    #// @since 0.8
    #// @return string|null Permalink URL
    #//
    def get_permalink(self):
        
        link = self.get_link()
        enclosure = self.get_enclosure(0)
        if link != None:
            return link
        elif enclosure != None:
            return enclosure.get_link()
        else:
            return None
        # end if
    # end def get_permalink
    #// 
    #// Get a single link for the item
    #// 
    #// @since Beta 3
    #// @param int $key The link that you want to return.  Remember that arrays begin with 0, not 1
    #// @param string $rel The relationship of the link to return
    #// @return string|null Link URL
    #//
    def get_link(self, key=0, rel="alternate"):
        
        links = self.get_links(rel)
        if links[key] != None:
            return links[key]
        else:
            return None
        # end if
    # end def get_link
    #// 
    #// Get all links for the item
    #// 
    #// Uses `<atom:link>`, `<link>` or `<guid>`
    #// 
    #// @since Beta 2
    #// @param string $rel The relationship of links to return
    #// @return array|null Links found for the item (strings)
    #//
    def get_links(self, rel="alternate"):
        
        if (not (php_isset(lambda : self.data["links"]))):
            self.data["links"] = Array()
            for link in self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "link"):
                if (php_isset(lambda : link["attribs"][""]["href"])):
                    link_rel = link["attribs"][""]["rel"] if (php_isset(lambda : link["attribs"][""]["rel"])) else "alternate"
                    self.data["links"][link_rel][-1] = self.sanitize(link["attribs"][""]["href"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(link))
                # end if
            # end for
            for link in self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "link"):
                if (php_isset(lambda : link["attribs"][""]["href"])):
                    link_rel = link["attribs"][""]["rel"] if (php_isset(lambda : link["attribs"][""]["rel"])) else "alternate"
                    self.data["links"][link_rel][-1] = self.sanitize(link["attribs"][""]["href"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(link))
                # end if
            # end for
            links = self.get_item_tags(SIMPLEPIE_NAMESPACE_RSS_10, "link")
            if links:
                self.data["links"]["alternate"][-1] = self.sanitize(links[0]["data"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(links[0]))
            # end if
            links = self.get_item_tags(SIMPLEPIE_NAMESPACE_RSS_090, "link")
            if links:
                self.data["links"]["alternate"][-1] = self.sanitize(links[0]["data"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(links[0]))
            # end if
            links = self.get_item_tags(SIMPLEPIE_NAMESPACE_RSS_20, "link")
            if links:
                self.data["links"]["alternate"][-1] = self.sanitize(links[0]["data"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(links[0]))
            # end if
            links = self.get_item_tags(SIMPLEPIE_NAMESPACE_RSS_20, "guid")
            if links:
                if (not (php_isset(lambda : links[0]["attribs"][""]["isPermaLink"]))) or php_strtolower(php_trim(links[0]["attribs"][""]["isPermaLink"])) == "true":
                    self.data["links"]["alternate"][-1] = self.sanitize(links[0]["data"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(links[0]))
                # end if
            # end if
            keys = php_array_keys(self.data["links"])
            for key in keys:
                if self.registry.call("Misc", "is_isegment_nz_nc", Array(key)):
                    if (php_isset(lambda : self.data["links"][SIMPLEPIE_IANA_LINK_RELATIONS_REGISTRY + key])):
                        self.data["links"][SIMPLEPIE_IANA_LINK_RELATIONS_REGISTRY + key] = php_array_merge(self.data["links"][key], self.data["links"][SIMPLEPIE_IANA_LINK_RELATIONS_REGISTRY + key])
                        self.data["links"][key] = self.data["links"][SIMPLEPIE_IANA_LINK_RELATIONS_REGISTRY + key]
                    else:
                        self.data["links"][SIMPLEPIE_IANA_LINK_RELATIONS_REGISTRY + key] = self.data["links"][key]
                    # end if
                elif php_substr(key, 0, 41) == SIMPLEPIE_IANA_LINK_RELATIONS_REGISTRY:
                    self.data["links"][php_substr(key, 41)] = self.data["links"][key]
                # end if
                self.data["links"][key] = array_unique(self.data["links"][key])
            # end for
        # end if
        if (php_isset(lambda : self.data["links"][rel])):
            return self.data["links"][rel]
        else:
            return None
        # end if
    # end def get_links
    #// 
    #// Get an enclosure from the item
    #// 
    #// Supports the <enclosure> RSS tag, as well as Media RSS and iTunes RSS.
    #// 
    #// @since Beta 2
    #// @todo Add ability to prefer one type of content over another (in a media group).
    #// @param int $key The enclosure that you want to return.  Remember that arrays begin with 0, not 1
    #// @return SimplePie_Enclosure|null
    #//
    def get_enclosure(self, key=0, prefer=None):
        
        enclosures = self.get_enclosures()
        if (php_isset(lambda : enclosures[key])):
            return enclosures[key]
        else:
            return None
        # end if
    # end def get_enclosure
    #// 
    #// Get all available enclosures (podcasts, etc.)
    #// 
    #// Supports the <enclosure> RSS tag, as well as Media RSS and iTunes RSS.
    #// 
    #// At this point, we're pretty much assuming that all enclosures for an item
    #// are the same content.  Anything else is too complicated to
    #// properly support.
    #// 
    #// @since Beta 2
    #// @todo Add support for end-user defined sorting of enclosures by type/handler (so we can prefer the faster-loading FLV over MP4).
    #// @todo If an element exists at a level, but it's value is empty, we should fall back to the value from the parent (if it exists).
    #// @return array|null List of SimplePie_Enclosure items
    #//
    def get_enclosures(self):
        
        if (not (php_isset(lambda : self.data["enclosures"]))):
            self.data["enclosures"] = Array()
            #// Elements
            captions_parent = None
            categories_parent = None
            copyrights_parent = None
            credits_parent = None
            description_parent = None
            duration_parent = None
            hashes_parent = None
            keywords_parent = None
            player_parent = None
            ratings_parent = None
            restrictions_parent = None
            thumbnails_parent = None
            title_parent = None
            #// Let's do the channel and item-level ones first, and just re-use them if we need to.
            parent = self.get_feed()
            #// CAPTIONS
            captions = self.get_item_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "text")
            if captions:
                for caption in captions:
                    caption_type = None
                    caption_lang = None
                    caption_startTime = None
                    caption_endTime = None
                    caption_text = None
                    if (php_isset(lambda : caption["attribs"][""]["type"])):
                        caption_type = self.sanitize(caption["attribs"][""]["type"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : caption["attribs"][""]["lang"])):
                        caption_lang = self.sanitize(caption["attribs"][""]["lang"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : caption["attribs"][""]["start"])):
                        caption_startTime = self.sanitize(caption["attribs"][""]["start"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : caption["attribs"][""]["end"])):
                        caption_endTime = self.sanitize(caption["attribs"][""]["end"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : caption["data"])):
                        caption_text = self.sanitize(caption["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    captions_parent[-1] = self.registry.create("Caption", Array(caption_type, caption_lang, caption_startTime, caption_endTime, caption_text))
                # end for
            elif parent.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "text"):
                captions = parent.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "text")
                for caption in captions:
                    caption_type = None
                    caption_lang = None
                    caption_startTime = None
                    caption_endTime = None
                    caption_text = None
                    if (php_isset(lambda : caption["attribs"][""]["type"])):
                        caption_type = self.sanitize(caption["attribs"][""]["type"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : caption["attribs"][""]["lang"])):
                        caption_lang = self.sanitize(caption["attribs"][""]["lang"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : caption["attribs"][""]["start"])):
                        caption_startTime = self.sanitize(caption["attribs"][""]["start"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : caption["attribs"][""]["end"])):
                        caption_endTime = self.sanitize(caption["attribs"][""]["end"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : caption["data"])):
                        caption_text = self.sanitize(caption["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    captions_parent[-1] = self.registry.create("Caption", Array(caption_type, caption_lang, caption_startTime, caption_endTime, caption_text))
                # end for
            # end if
            if php_is_array(captions_parent):
                captions_parent = php_array_values(array_unique(captions_parent))
            # end if
            #// CATEGORIES
            for category in self.get_item_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "category"):
                term = None
                scheme = None
                label = None
                if (php_isset(lambda : category["data"])):
                    term = self.sanitize(category["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
                if (php_isset(lambda : category["attribs"][""]["scheme"])):
                    scheme = self.sanitize(category["attribs"][""]["scheme"], SIMPLEPIE_CONSTRUCT_TEXT)
                else:
                    scheme = "http://search.yahoo.com/mrss/category_schema"
                # end if
                if (php_isset(lambda : category["attribs"][""]["label"])):
                    label = self.sanitize(category["attribs"][""]["label"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
                categories_parent[-1] = self.registry.create("Category", Array(term, scheme, label))
            # end for
            for category in parent.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "category"):
                term = None
                scheme = None
                label = None
                if (php_isset(lambda : category["data"])):
                    term = self.sanitize(category["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
                if (php_isset(lambda : category["attribs"][""]["scheme"])):
                    scheme = self.sanitize(category["attribs"][""]["scheme"], SIMPLEPIE_CONSTRUCT_TEXT)
                else:
                    scheme = "http://search.yahoo.com/mrss/category_schema"
                # end if
                if (php_isset(lambda : category["attribs"][""]["label"])):
                    label = self.sanitize(category["attribs"][""]["label"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
                categories_parent[-1] = self.registry.create("Category", Array(term, scheme, label))
            # end for
            for category in parent.get_channel_tags(SIMPLEPIE_NAMESPACE_ITUNES, "category"):
                term = None
                scheme = "http://www.itunes.com/dtds/podcast-1.0.dtd"
                label = None
                if (php_isset(lambda : category["attribs"][""]["text"])):
                    label = self.sanitize(category["attribs"][""]["text"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
                categories_parent[-1] = self.registry.create("Category", Array(term, scheme, label))
                if (php_isset(lambda : category["child"][SIMPLEPIE_NAMESPACE_ITUNES]["category"])):
                    for subcategory in category["child"][SIMPLEPIE_NAMESPACE_ITUNES]["category"]:
                        if (php_isset(lambda : subcategory["attribs"][""]["text"])):
                            label = self.sanitize(subcategory["attribs"][""]["text"], SIMPLEPIE_CONSTRUCT_TEXT)
                        # end if
                        categories_parent[-1] = self.registry.create("Category", Array(term, scheme, label))
                    # end for
                # end if
            # end for
            if php_is_array(categories_parent):
                categories_parent = php_array_values(array_unique(categories_parent))
            # end if
            #// COPYRIGHT
            copyright = self.get_item_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "copyright")
            if copyright:
                copyright_url = None
                copyright_label = None
                if (php_isset(lambda : copyright[0]["attribs"][""]["url"])):
                    copyright_url = self.sanitize(copyright[0]["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
                if (php_isset(lambda : copyright[0]["data"])):
                    copyright_label = self.sanitize(copyright[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
                copyrights_parent = self.registry.create("Copyright", Array(copyright_url, copyright_label))
            elif parent.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "copyright"):
                copyright = parent.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "copyright")
                copyright_url = None
                copyright_label = None
                if (php_isset(lambda : copyright[0]["attribs"][""]["url"])):
                    copyright_url = self.sanitize(copyright[0]["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
                if (php_isset(lambda : copyright[0]["data"])):
                    copyright_label = self.sanitize(copyright[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
                copyrights_parent = self.registry.create("Copyright", Array(copyright_url, copyright_label))
            # end if
            #// CREDITS
            credits = self.get_item_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "credit")
            if credits:
                for credit in credits:
                    credit_role = None
                    credit_scheme = None
                    credit_name = None
                    if (php_isset(lambda : credit["attribs"][""]["role"])):
                        credit_role = self.sanitize(credit["attribs"][""]["role"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : credit["attribs"][""]["scheme"])):
                        credit_scheme = self.sanitize(credit["attribs"][""]["scheme"], SIMPLEPIE_CONSTRUCT_TEXT)
                    else:
                        credit_scheme = "urn:ebu"
                    # end if
                    if (php_isset(lambda : credit["data"])):
                        credit_name = self.sanitize(credit["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    credits_parent[-1] = self.registry.create("Credit", Array(credit_role, credit_scheme, credit_name))
                # end for
            elif parent.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "credit"):
                credits = parent.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "credit")
                for credit in credits:
                    credit_role = None
                    credit_scheme = None
                    credit_name = None
                    if (php_isset(lambda : credit["attribs"][""]["role"])):
                        credit_role = self.sanitize(credit["attribs"][""]["role"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : credit["attribs"][""]["scheme"])):
                        credit_scheme = self.sanitize(credit["attribs"][""]["scheme"], SIMPLEPIE_CONSTRUCT_TEXT)
                    else:
                        credit_scheme = "urn:ebu"
                    # end if
                    if (php_isset(lambda : credit["data"])):
                        credit_name = self.sanitize(credit["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    credits_parent[-1] = self.registry.create("Credit", Array(credit_role, credit_scheme, credit_name))
                # end for
            # end if
            if php_is_array(credits_parent):
                credits_parent = php_array_values(array_unique(credits_parent))
            # end if
            #// DESCRIPTION
            description_parent = self.get_item_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "description")
            if description_parent:
                if (php_isset(lambda : description_parent[0]["data"])):
                    description_parent = self.sanitize(description_parent[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
            elif parent.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "description"):
                description_parent = parent.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "description")
                if (php_isset(lambda : description_parent[0]["data"])):
                    description_parent = self.sanitize(description_parent[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
            # end if
            #// DURATION
            duration_parent = self.get_item_tags(SIMPLEPIE_NAMESPACE_ITUNES, "duration")
            if duration_parent:
                seconds = None
                minutes = None
                hours = None
                if (php_isset(lambda : duration_parent[0]["data"])):
                    temp = php_explode(":", self.sanitize(duration_parent[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT))
                    if sizeof(temp) > 0:
                        seconds = int(php_array_pop(temp))
                    # end if
                    if sizeof(temp) > 0:
                        minutes = int(php_array_pop(temp))
                        seconds += minutes * 60
                    # end if
                    if sizeof(temp) > 0:
                        hours = int(php_array_pop(temp))
                        seconds += hours * 3600
                    # end if
                    temp = None
                    duration_parent = seconds
                # end if
            # end if
            #// HASHES
            hashes_iterator = self.get_item_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "hash")
            if hashes_iterator:
                for hash in hashes_iterator:
                    value = None
                    algo = None
                    if (php_isset(lambda : hash["data"])):
                        value = self.sanitize(hash["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : hash["attribs"][""]["algo"])):
                        algo = self.sanitize(hash["attribs"][""]["algo"], SIMPLEPIE_CONSTRUCT_TEXT)
                    else:
                        algo = "md5"
                    # end if
                    hashes_parent[-1] = algo + ":" + value
                # end for
            elif parent.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "hash"):
                hashes_iterator = parent.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "hash")
                for hash in hashes_iterator:
                    value = None
                    algo = None
                    if (php_isset(lambda : hash["data"])):
                        value = self.sanitize(hash["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : hash["attribs"][""]["algo"])):
                        algo = self.sanitize(hash["attribs"][""]["algo"], SIMPLEPIE_CONSTRUCT_TEXT)
                    else:
                        algo = "md5"
                    # end if
                    hashes_parent[-1] = algo + ":" + value
                # end for
            # end if
            if php_is_array(hashes_parent):
                hashes_parent = php_array_values(array_unique(hashes_parent))
            # end if
            #// KEYWORDS
            keywords = self.get_item_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "keywords")
            if keywords:
                if (php_isset(lambda : keywords[0]["data"])):
                    temp = php_explode(",", self.sanitize(keywords[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT))
                    for word in temp:
                        keywords_parent[-1] = php_trim(word)
                    # end for
                # end if
                temp = None
            elif self.get_item_tags(SIMPLEPIE_NAMESPACE_ITUNES, "keywords"):
                keywords = self.get_item_tags(SIMPLEPIE_NAMESPACE_ITUNES, "keywords")
                if (php_isset(lambda : keywords[0]["data"])):
                    temp = php_explode(",", self.sanitize(keywords[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT))
                    for word in temp:
                        keywords_parent[-1] = php_trim(word)
                    # end for
                # end if
                temp = None
            elif parent.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "keywords"):
                keywords = parent.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "keywords")
                if (php_isset(lambda : keywords[0]["data"])):
                    temp = php_explode(",", self.sanitize(keywords[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT))
                    for word in temp:
                        keywords_parent[-1] = php_trim(word)
                    # end for
                # end if
                temp = None
            elif parent.get_channel_tags(SIMPLEPIE_NAMESPACE_ITUNES, "keywords"):
                keywords = parent.get_channel_tags(SIMPLEPIE_NAMESPACE_ITUNES, "keywords")
                if (php_isset(lambda : keywords[0]["data"])):
                    temp = php_explode(",", self.sanitize(keywords[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT))
                    for word in temp:
                        keywords_parent[-1] = php_trim(word)
                    # end for
                # end if
                temp = None
            # end if
            if php_is_array(keywords_parent):
                keywords_parent = php_array_values(array_unique(keywords_parent))
            # end if
            #// PLAYER
            player_parent = self.get_item_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "player")
            if player_parent:
                if (php_isset(lambda : player_parent[0]["attribs"][""]["url"])):
                    player_parent = self.sanitize(player_parent[0]["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_IRI)
                # end if
            elif parent.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "player"):
                player_parent = parent.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "player")
                if (php_isset(lambda : player_parent[0]["attribs"][""]["url"])):
                    player_parent = self.sanitize(player_parent[0]["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_IRI)
                # end if
            # end if
            #// RATINGS
            ratings = self.get_item_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "rating")
            if ratings:
                for rating in ratings:
                    rating_scheme = None
                    rating_value = None
                    if (php_isset(lambda : rating["attribs"][""]["scheme"])):
                        rating_scheme = self.sanitize(rating["attribs"][""]["scheme"], SIMPLEPIE_CONSTRUCT_TEXT)
                    else:
                        rating_scheme = "urn:simple"
                    # end if
                    if (php_isset(lambda : rating["data"])):
                        rating_value = self.sanitize(rating["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    ratings_parent[-1] = self.registry.create("Rating", Array(rating_scheme, rating_value))
                # end for
            elif self.get_item_tags(SIMPLEPIE_NAMESPACE_ITUNES, "explicit"):
                ratings = self.get_item_tags(SIMPLEPIE_NAMESPACE_ITUNES, "explicit")
                for rating in ratings:
                    rating_scheme = "urn:itunes"
                    rating_value = None
                    if (php_isset(lambda : rating["data"])):
                        rating_value = self.sanitize(rating["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    ratings_parent[-1] = self.registry.create("Rating", Array(rating_scheme, rating_value))
                # end for
            elif parent.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "rating"):
                ratings = parent.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "rating")
                for rating in ratings:
                    rating_scheme = None
                    rating_value = None
                    if (php_isset(lambda : rating["attribs"][""]["scheme"])):
                        rating_scheme = self.sanitize(rating["attribs"][""]["scheme"], SIMPLEPIE_CONSTRUCT_TEXT)
                    else:
                        rating_scheme = "urn:simple"
                    # end if
                    if (php_isset(lambda : rating["data"])):
                        rating_value = self.sanitize(rating["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    ratings_parent[-1] = self.registry.create("Rating", Array(rating_scheme, rating_value))
                # end for
            elif parent.get_channel_tags(SIMPLEPIE_NAMESPACE_ITUNES, "explicit"):
                ratings = parent.get_channel_tags(SIMPLEPIE_NAMESPACE_ITUNES, "explicit")
                for rating in ratings:
                    rating_scheme = "urn:itunes"
                    rating_value = None
                    if (php_isset(lambda : rating["data"])):
                        rating_value = self.sanitize(rating["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    ratings_parent[-1] = self.registry.create("Rating", Array(rating_scheme, rating_value))
                # end for
            # end if
            if php_is_array(ratings_parent):
                ratings_parent = php_array_values(array_unique(ratings_parent))
            # end if
            #// RESTRICTIONS
            restrictions = self.get_item_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "restriction")
            if restrictions:
                for restriction in restrictions:
                    restriction_relationship = None
                    restriction_type = None
                    restriction_value = None
                    if (php_isset(lambda : restriction["attribs"][""]["relationship"])):
                        restriction_relationship = self.sanitize(restriction["attribs"][""]["relationship"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : restriction["attribs"][""]["type"])):
                        restriction_type = self.sanitize(restriction["attribs"][""]["type"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : restriction["data"])):
                        restriction_value = self.sanitize(restriction["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    restrictions_parent[-1] = self.registry.create("Restriction", Array(restriction_relationship, restriction_type, restriction_value))
                # end for
            elif self.get_item_tags(SIMPLEPIE_NAMESPACE_ITUNES, "block"):
                restrictions = self.get_item_tags(SIMPLEPIE_NAMESPACE_ITUNES, "block")
                for restriction in restrictions:
                    restriction_relationship = "allow"
                    restriction_type = None
                    restriction_value = "itunes"
                    if (php_isset(lambda : restriction["data"])) and php_strtolower(restriction["data"]) == "yes":
                        restriction_relationship = "deny"
                    # end if
                    restrictions_parent[-1] = self.registry.create("Restriction", Array(restriction_relationship, restriction_type, restriction_value))
                # end for
            elif parent.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "restriction"):
                restrictions = parent.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "restriction")
                for restriction in restrictions:
                    restriction_relationship = None
                    restriction_type = None
                    restriction_value = None
                    if (php_isset(lambda : restriction["attribs"][""]["relationship"])):
                        restriction_relationship = self.sanitize(restriction["attribs"][""]["relationship"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : restriction["attribs"][""]["type"])):
                        restriction_type = self.sanitize(restriction["attribs"][""]["type"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : restriction["data"])):
                        restriction_value = self.sanitize(restriction["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    restrictions_parent[-1] = self.registry.create("Restriction", Array(restriction_relationship, restriction_type, restriction_value))
                # end for
            elif parent.get_channel_tags(SIMPLEPIE_NAMESPACE_ITUNES, "block"):
                restrictions = parent.get_channel_tags(SIMPLEPIE_NAMESPACE_ITUNES, "block")
                for restriction in restrictions:
                    restriction_relationship = "allow"
                    restriction_type = None
                    restriction_value = "itunes"
                    if (php_isset(lambda : restriction["data"])) and php_strtolower(restriction["data"]) == "yes":
                        restriction_relationship = "deny"
                    # end if
                    restrictions_parent[-1] = self.registry.create("Restriction", Array(restriction_relationship, restriction_type, restriction_value))
                # end for
            # end if
            if php_is_array(restrictions_parent):
                restrictions_parent = php_array_values(array_unique(restrictions_parent))
            else:
                restrictions_parent = Array(php_new_class("SimplePie_Restriction", lambda : SimplePie_Restriction("allow", None, "default")))
            # end if
            #// THUMBNAILS
            thumbnails = self.get_item_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "thumbnail")
            if thumbnails:
                for thumbnail in thumbnails:
                    if (php_isset(lambda : thumbnail["attribs"][""]["url"])):
                        thumbnails_parent[-1] = self.sanitize(thumbnail["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_IRI)
                    # end if
                # end for
            elif parent.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "thumbnail"):
                thumbnails = parent.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "thumbnail")
                for thumbnail in thumbnails:
                    if (php_isset(lambda : thumbnail["attribs"][""]["url"])):
                        thumbnails_parent[-1] = self.sanitize(thumbnail["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_IRI)
                    # end if
                # end for
            # end if
            #// TITLES
            title_parent = self.get_item_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "title")
            if title_parent:
                if (php_isset(lambda : title_parent[0]["data"])):
                    title_parent = self.sanitize(title_parent[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
            elif parent.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "title"):
                title_parent = parent.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "title")
                if (php_isset(lambda : title_parent[0]["data"])):
                    title_parent = self.sanitize(title_parent[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
            # end if
            parent = None
            #// Attributes
            bitrate = None
            channels = None
            duration = None
            expression = None
            framerate = None
            height = None
            javascript = None
            lang = None
            length = None
            medium = None
            samplingrate = None
            type = None
            url = None
            width = None
            #// Elements
            captions = None
            categories = None
            copyrights = None
            credits = None
            description = None
            hashes = None
            keywords = None
            player = None
            ratings = None
            restrictions = None
            thumbnails = None
            title = None
            #// If we have media:group tags, loop through them.
            for group in self.get_item_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "group"):
                if (php_isset(lambda : group["child"])) and (php_isset(lambda : group["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["content"])):
                    #// If we have media:content tags, loop through them.
                    for content in group["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["content"]:
                        if (php_isset(lambda : content["attribs"][""]["url"])):
                            #// Attributes
                            bitrate = None
                            channels = None
                            duration = None
                            expression = None
                            framerate = None
                            height = None
                            javascript = None
                            lang = None
                            length = None
                            medium = None
                            samplingrate = None
                            type = None
                            url = None
                            width = None
                            #// Elements
                            captions = None
                            categories = None
                            copyrights = None
                            credits = None
                            description = None
                            hashes = None
                            keywords = None
                            player = None
                            ratings = None
                            restrictions = None
                            thumbnails = None
                            title = None
                            #// Start checking the attributes of media:content
                            if (php_isset(lambda : content["attribs"][""]["bitrate"])):
                                bitrate = self.sanitize(content["attribs"][""]["bitrate"], SIMPLEPIE_CONSTRUCT_TEXT)
                            # end if
                            if (php_isset(lambda : content["attribs"][""]["channels"])):
                                channels = self.sanitize(content["attribs"][""]["channels"], SIMPLEPIE_CONSTRUCT_TEXT)
                            # end if
                            if (php_isset(lambda : content["attribs"][""]["duration"])):
                                duration = self.sanitize(content["attribs"][""]["duration"], SIMPLEPIE_CONSTRUCT_TEXT)
                            else:
                                duration = duration_parent
                            # end if
                            if (php_isset(lambda : content["attribs"][""]["expression"])):
                                expression = self.sanitize(content["attribs"][""]["expression"], SIMPLEPIE_CONSTRUCT_TEXT)
                            # end if
                            if (php_isset(lambda : content["attribs"][""]["framerate"])):
                                framerate = self.sanitize(content["attribs"][""]["framerate"], SIMPLEPIE_CONSTRUCT_TEXT)
                            # end if
                            if (php_isset(lambda : content["attribs"][""]["height"])):
                                height = self.sanitize(content["attribs"][""]["height"], SIMPLEPIE_CONSTRUCT_TEXT)
                            # end if
                            if (php_isset(lambda : content["attribs"][""]["lang"])):
                                lang = self.sanitize(content["attribs"][""]["lang"], SIMPLEPIE_CONSTRUCT_TEXT)
                            # end if
                            if (php_isset(lambda : content["attribs"][""]["fileSize"])):
                                length = ceil(content["attribs"][""]["fileSize"])
                            # end if
                            if (php_isset(lambda : content["attribs"][""]["medium"])):
                                medium = self.sanitize(content["attribs"][""]["medium"], SIMPLEPIE_CONSTRUCT_TEXT)
                            # end if
                            if (php_isset(lambda : content["attribs"][""]["samplingrate"])):
                                samplingrate = self.sanitize(content["attribs"][""]["samplingrate"], SIMPLEPIE_CONSTRUCT_TEXT)
                            # end if
                            if (php_isset(lambda : content["attribs"][""]["type"])):
                                type = self.sanitize(content["attribs"][""]["type"], SIMPLEPIE_CONSTRUCT_TEXT)
                            # end if
                            if (php_isset(lambda : content["attribs"][""]["width"])):
                                width = self.sanitize(content["attribs"][""]["width"], SIMPLEPIE_CONSTRUCT_TEXT)
                            # end if
                            url = self.sanitize(content["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_IRI)
                            #// Checking the other optional media: elements. Priority: media:content, media:group, item, channel
                            #// CAPTIONS
                            if (php_isset(lambda : content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["text"])):
                                for caption in content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["text"]:
                                    caption_type = None
                                    caption_lang = None
                                    caption_startTime = None
                                    caption_endTime = None
                                    caption_text = None
                                    if (php_isset(lambda : caption["attribs"][""]["type"])):
                                        caption_type = self.sanitize(caption["attribs"][""]["type"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : caption["attribs"][""]["lang"])):
                                        caption_lang = self.sanitize(caption["attribs"][""]["lang"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : caption["attribs"][""]["start"])):
                                        caption_startTime = self.sanitize(caption["attribs"][""]["start"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : caption["attribs"][""]["end"])):
                                        caption_endTime = self.sanitize(caption["attribs"][""]["end"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : caption["data"])):
                                        caption_text = self.sanitize(caption["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    captions[-1] = self.registry.create("Caption", Array(caption_type, caption_lang, caption_startTime, caption_endTime, caption_text))
                                # end for
                                if php_is_array(captions):
                                    captions = php_array_values(array_unique(captions))
                                # end if
                            elif (php_isset(lambda : group["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["text"])):
                                for caption in group["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["text"]:
                                    caption_type = None
                                    caption_lang = None
                                    caption_startTime = None
                                    caption_endTime = None
                                    caption_text = None
                                    if (php_isset(lambda : caption["attribs"][""]["type"])):
                                        caption_type = self.sanitize(caption["attribs"][""]["type"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : caption["attribs"][""]["lang"])):
                                        caption_lang = self.sanitize(caption["attribs"][""]["lang"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : caption["attribs"][""]["start"])):
                                        caption_startTime = self.sanitize(caption["attribs"][""]["start"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : caption["attribs"][""]["end"])):
                                        caption_endTime = self.sanitize(caption["attribs"][""]["end"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : caption["data"])):
                                        caption_text = self.sanitize(caption["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    captions[-1] = self.registry.create("Caption", Array(caption_type, caption_lang, caption_startTime, caption_endTime, caption_text))
                                # end for
                                if php_is_array(captions):
                                    captions = php_array_values(array_unique(captions))
                                # end if
                            else:
                                captions = captions_parent
                            # end if
                            #// CATEGORIES
                            if (php_isset(lambda : content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["category"])):
                                for category in content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["category"]:
                                    term = None
                                    scheme = None
                                    label = None
                                    if (php_isset(lambda : category["data"])):
                                        term = self.sanitize(category["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : category["attribs"][""]["scheme"])):
                                        scheme = self.sanitize(category["attribs"][""]["scheme"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    else:
                                        scheme = "http://search.yahoo.com/mrss/category_schema"
                                    # end if
                                    if (php_isset(lambda : category["attribs"][""]["label"])):
                                        label = self.sanitize(category["attribs"][""]["label"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    categories[-1] = self.registry.create("Category", Array(term, scheme, label))
                                # end for
                            # end if
                            if (php_isset(lambda : group["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["category"])):
                                for category in group["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["category"]:
                                    term = None
                                    scheme = None
                                    label = None
                                    if (php_isset(lambda : category["data"])):
                                        term = self.sanitize(category["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : category["attribs"][""]["scheme"])):
                                        scheme = self.sanitize(category["attribs"][""]["scheme"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    else:
                                        scheme = "http://search.yahoo.com/mrss/category_schema"
                                    # end if
                                    if (php_isset(lambda : category["attribs"][""]["label"])):
                                        label = self.sanitize(category["attribs"][""]["label"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    categories[-1] = self.registry.create("Category", Array(term, scheme, label))
                                # end for
                            # end if
                            if php_is_array(categories) and php_is_array(categories_parent):
                                categories = php_array_values(array_unique(php_array_merge(categories, categories_parent)))
                            elif php_is_array(categories):
                                categories = php_array_values(array_unique(categories))
                            elif php_is_array(categories_parent):
                                categories = php_array_values(array_unique(categories_parent))
                            # end if
                            #// COPYRIGHTS
                            if (php_isset(lambda : content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["copyright"])):
                                copyright_url = None
                                copyright_label = None
                                if (php_isset(lambda : content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["copyright"][0]["attribs"][""]["url"])):
                                    copyright_url = self.sanitize(content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["copyright"][0]["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                if (php_isset(lambda : content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["copyright"][0]["data"])):
                                    copyright_label = self.sanitize(content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["copyright"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                copyrights = self.registry.create("Copyright", Array(copyright_url, copyright_label))
                            elif (php_isset(lambda : group["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["copyright"])):
                                copyright_url = None
                                copyright_label = None
                                if (php_isset(lambda : group["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["copyright"][0]["attribs"][""]["url"])):
                                    copyright_url = self.sanitize(group["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["copyright"][0]["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                if (php_isset(lambda : group["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["copyright"][0]["data"])):
                                    copyright_label = self.sanitize(group["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["copyright"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                copyrights = self.registry.create("Copyright", Array(copyright_url, copyright_label))
                            else:
                                copyrights = copyrights_parent
                            # end if
                            #// CREDITS
                            if (php_isset(lambda : content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["credit"])):
                                for credit in content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["credit"]:
                                    credit_role = None
                                    credit_scheme = None
                                    credit_name = None
                                    if (php_isset(lambda : credit["attribs"][""]["role"])):
                                        credit_role = self.sanitize(credit["attribs"][""]["role"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : credit["attribs"][""]["scheme"])):
                                        credit_scheme = self.sanitize(credit["attribs"][""]["scheme"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    else:
                                        credit_scheme = "urn:ebu"
                                    # end if
                                    if (php_isset(lambda : credit["data"])):
                                        credit_name = self.sanitize(credit["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    credits[-1] = self.registry.create("Credit", Array(credit_role, credit_scheme, credit_name))
                                # end for
                                if php_is_array(credits):
                                    credits = php_array_values(array_unique(credits))
                                # end if
                            elif (php_isset(lambda : group["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["credit"])):
                                for credit in group["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["credit"]:
                                    credit_role = None
                                    credit_scheme = None
                                    credit_name = None
                                    if (php_isset(lambda : credit["attribs"][""]["role"])):
                                        credit_role = self.sanitize(credit["attribs"][""]["role"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : credit["attribs"][""]["scheme"])):
                                        credit_scheme = self.sanitize(credit["attribs"][""]["scheme"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    else:
                                        credit_scheme = "urn:ebu"
                                    # end if
                                    if (php_isset(lambda : credit["data"])):
                                        credit_name = self.sanitize(credit["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    credits[-1] = self.registry.create("Credit", Array(credit_role, credit_scheme, credit_name))
                                # end for
                                if php_is_array(credits):
                                    credits = php_array_values(array_unique(credits))
                                # end if
                            else:
                                credits = credits_parent
                            # end if
                            #// DESCRIPTION
                            if (php_isset(lambda : content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["description"])):
                                description = self.sanitize(content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["description"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                            elif (php_isset(lambda : group["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["description"])):
                                description = self.sanitize(group["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["description"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                            else:
                                description = description_parent
                            # end if
                            #// HASHES
                            if (php_isset(lambda : content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["hash"])):
                                for hash in content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["hash"]:
                                    value = None
                                    algo = None
                                    if (php_isset(lambda : hash["data"])):
                                        value = self.sanitize(hash["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : hash["attribs"][""]["algo"])):
                                        algo = self.sanitize(hash["attribs"][""]["algo"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    else:
                                        algo = "md5"
                                    # end if
                                    hashes[-1] = algo + ":" + value
                                # end for
                                if php_is_array(hashes):
                                    hashes = php_array_values(array_unique(hashes))
                                # end if
                            elif (php_isset(lambda : group["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["hash"])):
                                for hash in group["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["hash"]:
                                    value = None
                                    algo = None
                                    if (php_isset(lambda : hash["data"])):
                                        value = self.sanitize(hash["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : hash["attribs"][""]["algo"])):
                                        algo = self.sanitize(hash["attribs"][""]["algo"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    else:
                                        algo = "md5"
                                    # end if
                                    hashes[-1] = algo + ":" + value
                                # end for
                                if php_is_array(hashes):
                                    hashes = php_array_values(array_unique(hashes))
                                # end if
                            else:
                                hashes = hashes_parent
                            # end if
                            #// KEYWORDS
                            if (php_isset(lambda : content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["keywords"])):
                                if (php_isset(lambda : content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["keywords"][0]["data"])):
                                    temp = php_explode(",", self.sanitize(content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["keywords"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT))
                                    for word in temp:
                                        keywords[-1] = php_trim(word)
                                    # end for
                                    temp = None
                                # end if
                                if php_is_array(keywords):
                                    keywords = php_array_values(array_unique(keywords))
                                # end if
                            elif (php_isset(lambda : group["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["keywords"])):
                                if (php_isset(lambda : group["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["keywords"][0]["data"])):
                                    temp = php_explode(",", self.sanitize(group["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["keywords"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT))
                                    for word in temp:
                                        keywords[-1] = php_trim(word)
                                    # end for
                                    temp = None
                                # end if
                                if php_is_array(keywords):
                                    keywords = php_array_values(array_unique(keywords))
                                # end if
                            else:
                                keywords = keywords_parent
                            # end if
                            #// PLAYER
                            if (php_isset(lambda : content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["player"])):
                                player = self.sanitize(content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["player"][0]["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_IRI)
                            elif (php_isset(lambda : group["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["player"])):
                                player = self.sanitize(group["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["player"][0]["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_IRI)
                            else:
                                player = player_parent
                            # end if
                            #// RATINGS
                            if (php_isset(lambda : content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["rating"])):
                                for rating in content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["rating"]:
                                    rating_scheme = None
                                    rating_value = None
                                    if (php_isset(lambda : rating["attribs"][""]["scheme"])):
                                        rating_scheme = self.sanitize(rating["attribs"][""]["scheme"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    else:
                                        rating_scheme = "urn:simple"
                                    # end if
                                    if (php_isset(lambda : rating["data"])):
                                        rating_value = self.sanitize(rating["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    ratings[-1] = self.registry.create("Rating", Array(rating_scheme, rating_value))
                                # end for
                                if php_is_array(ratings):
                                    ratings = php_array_values(array_unique(ratings))
                                # end if
                            elif (php_isset(lambda : group["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["rating"])):
                                for rating in group["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["rating"]:
                                    rating_scheme = None
                                    rating_value = None
                                    if (php_isset(lambda : rating["attribs"][""]["scheme"])):
                                        rating_scheme = self.sanitize(rating["attribs"][""]["scheme"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    else:
                                        rating_scheme = "urn:simple"
                                    # end if
                                    if (php_isset(lambda : rating["data"])):
                                        rating_value = self.sanitize(rating["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    ratings[-1] = self.registry.create("Rating", Array(rating_scheme, rating_value))
                                # end for
                                if php_is_array(ratings):
                                    ratings = php_array_values(array_unique(ratings))
                                # end if
                            else:
                                ratings = ratings_parent
                            # end if
                            #// RESTRICTIONS
                            if (php_isset(lambda : content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["restriction"])):
                                for restriction in content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["restriction"]:
                                    restriction_relationship = None
                                    restriction_type = None
                                    restriction_value = None
                                    if (php_isset(lambda : restriction["attribs"][""]["relationship"])):
                                        restriction_relationship = self.sanitize(restriction["attribs"][""]["relationship"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : restriction["attribs"][""]["type"])):
                                        restriction_type = self.sanitize(restriction["attribs"][""]["type"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : restriction["data"])):
                                        restriction_value = self.sanitize(restriction["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    restrictions[-1] = self.registry.create("Restriction", Array(restriction_relationship, restriction_type, restriction_value))
                                # end for
                                if php_is_array(restrictions):
                                    restrictions = php_array_values(array_unique(restrictions))
                                # end if
                            elif (php_isset(lambda : group["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["restriction"])):
                                for restriction in group["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["restriction"]:
                                    restriction_relationship = None
                                    restriction_type = None
                                    restriction_value = None
                                    if (php_isset(lambda : restriction["attribs"][""]["relationship"])):
                                        restriction_relationship = self.sanitize(restriction["attribs"][""]["relationship"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : restriction["attribs"][""]["type"])):
                                        restriction_type = self.sanitize(restriction["attribs"][""]["type"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : restriction["data"])):
                                        restriction_value = self.sanitize(restriction["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    restrictions[-1] = self.registry.create("Restriction", Array(restriction_relationship, restriction_type, restriction_value))
                                # end for
                                if php_is_array(restrictions):
                                    restrictions = php_array_values(array_unique(restrictions))
                                # end if
                            else:
                                restrictions = restrictions_parent
                            # end if
                            #// THUMBNAILS
                            if (php_isset(lambda : content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["thumbnail"])):
                                for thumbnail in content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["thumbnail"]:
                                    thumbnails[-1] = self.sanitize(thumbnail["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_IRI)
                                # end for
                                if php_is_array(thumbnails):
                                    thumbnails = php_array_values(array_unique(thumbnails))
                                # end if
                            elif (php_isset(lambda : group["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["thumbnail"])):
                                for thumbnail in group["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["thumbnail"]:
                                    thumbnails[-1] = self.sanitize(thumbnail["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_IRI)
                                # end for
                                if php_is_array(thumbnails):
                                    thumbnails = php_array_values(array_unique(thumbnails))
                                # end if
                            else:
                                thumbnails = thumbnails_parent
                            # end if
                            #// TITLES
                            if (php_isset(lambda : content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["title"])):
                                title = self.sanitize(content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["title"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                            elif (php_isset(lambda : group["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["title"])):
                                title = self.sanitize(group["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["title"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                            else:
                                title = title_parent
                            # end if
                            self.data["enclosures"][-1] = self.registry.create("Enclosure", Array(url, type, length, None, bitrate, captions, categories, channels, copyrights, credits, description, duration, expression, framerate, hashes, height, keywords, lang, medium, player, ratings, restrictions, samplingrate, thumbnails, title, width))
                        # end if
                    # end for
                # end if
            # end for
            #// If we have standalone media:content tags, loop through them.
            if (php_isset(lambda : self.data["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["content"])):
                for content in self.data["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["content"]:
                    if (php_isset(lambda : content["attribs"][""]["url"])) or (php_isset(lambda : content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["player"])):
                        #// Attributes
                        bitrate = None
                        channels = None
                        duration = None
                        expression = None
                        framerate = None
                        height = None
                        javascript = None
                        lang = None
                        length = None
                        medium = None
                        samplingrate = None
                        type = None
                        url = None
                        width = None
                        #// Elements
                        captions = None
                        categories = None
                        copyrights = None
                        credits = None
                        description = None
                        hashes = None
                        keywords = None
                        player = None
                        ratings = None
                        restrictions = None
                        thumbnails = None
                        title = None
                        #// Start checking the attributes of media:content
                        if (php_isset(lambda : content["attribs"][""]["bitrate"])):
                            bitrate = self.sanitize(content["attribs"][""]["bitrate"], SIMPLEPIE_CONSTRUCT_TEXT)
                        # end if
                        if (php_isset(lambda : content["attribs"][""]["channels"])):
                            channels = self.sanitize(content["attribs"][""]["channels"], SIMPLEPIE_CONSTRUCT_TEXT)
                        # end if
                        if (php_isset(lambda : content["attribs"][""]["duration"])):
                            duration = self.sanitize(content["attribs"][""]["duration"], SIMPLEPIE_CONSTRUCT_TEXT)
                        else:
                            duration = duration_parent
                        # end if
                        if (php_isset(lambda : content["attribs"][""]["expression"])):
                            expression = self.sanitize(content["attribs"][""]["expression"], SIMPLEPIE_CONSTRUCT_TEXT)
                        # end if
                        if (php_isset(lambda : content["attribs"][""]["framerate"])):
                            framerate = self.sanitize(content["attribs"][""]["framerate"], SIMPLEPIE_CONSTRUCT_TEXT)
                        # end if
                        if (php_isset(lambda : content["attribs"][""]["height"])):
                            height = self.sanitize(content["attribs"][""]["height"], SIMPLEPIE_CONSTRUCT_TEXT)
                        # end if
                        if (php_isset(lambda : content["attribs"][""]["lang"])):
                            lang = self.sanitize(content["attribs"][""]["lang"], SIMPLEPIE_CONSTRUCT_TEXT)
                        # end if
                        if (php_isset(lambda : content["attribs"][""]["fileSize"])):
                            length = ceil(content["attribs"][""]["fileSize"])
                        # end if
                        if (php_isset(lambda : content["attribs"][""]["medium"])):
                            medium = self.sanitize(content["attribs"][""]["medium"], SIMPLEPIE_CONSTRUCT_TEXT)
                        # end if
                        if (php_isset(lambda : content["attribs"][""]["samplingrate"])):
                            samplingrate = self.sanitize(content["attribs"][""]["samplingrate"], SIMPLEPIE_CONSTRUCT_TEXT)
                        # end if
                        if (php_isset(lambda : content["attribs"][""]["type"])):
                            type = self.sanitize(content["attribs"][""]["type"], SIMPLEPIE_CONSTRUCT_TEXT)
                        # end if
                        if (php_isset(lambda : content["attribs"][""]["width"])):
                            width = self.sanitize(content["attribs"][""]["width"], SIMPLEPIE_CONSTRUCT_TEXT)
                        # end if
                        if (php_isset(lambda : content["attribs"][""]["url"])):
                            url = self.sanitize(content["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_IRI)
                        # end if
                        #// Checking the other optional media: elements. Priority: media:content, media:group, item, channel
                        #// CAPTIONS
                        if (php_isset(lambda : content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["text"])):
                            for caption in content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["text"]:
                                caption_type = None
                                caption_lang = None
                                caption_startTime = None
                                caption_endTime = None
                                caption_text = None
                                if (php_isset(lambda : caption["attribs"][""]["type"])):
                                    caption_type = self.sanitize(caption["attribs"][""]["type"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                if (php_isset(lambda : caption["attribs"][""]["lang"])):
                                    caption_lang = self.sanitize(caption["attribs"][""]["lang"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                if (php_isset(lambda : caption["attribs"][""]["start"])):
                                    caption_startTime = self.sanitize(caption["attribs"][""]["start"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                if (php_isset(lambda : caption["attribs"][""]["end"])):
                                    caption_endTime = self.sanitize(caption["attribs"][""]["end"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                if (php_isset(lambda : caption["data"])):
                                    caption_text = self.sanitize(caption["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                captions[-1] = self.registry.create("Caption", Array(caption_type, caption_lang, caption_startTime, caption_endTime, caption_text))
                            # end for
                            if php_is_array(captions):
                                captions = php_array_values(array_unique(captions))
                            # end if
                        else:
                            captions = captions_parent
                        # end if
                        #// CATEGORIES
                        if (php_isset(lambda : content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["category"])):
                            for category in content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["category"]:
                                term = None
                                scheme = None
                                label = None
                                if (php_isset(lambda : category["data"])):
                                    term = self.sanitize(category["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                if (php_isset(lambda : category["attribs"][""]["scheme"])):
                                    scheme = self.sanitize(category["attribs"][""]["scheme"], SIMPLEPIE_CONSTRUCT_TEXT)
                                else:
                                    scheme = "http://search.yahoo.com/mrss/category_schema"
                                # end if
                                if (php_isset(lambda : category["attribs"][""]["label"])):
                                    label = self.sanitize(category["attribs"][""]["label"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                categories[-1] = self.registry.create("Category", Array(term, scheme, label))
                            # end for
                        # end if
                        if php_is_array(categories) and php_is_array(categories_parent):
                            categories = php_array_values(array_unique(php_array_merge(categories, categories_parent)))
                        elif php_is_array(categories):
                            categories = php_array_values(array_unique(categories))
                        elif php_is_array(categories_parent):
                            categories = php_array_values(array_unique(categories_parent))
                        else:
                            categories = None
                        # end if
                        #// COPYRIGHTS
                        if (php_isset(lambda : content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["copyright"])):
                            copyright_url = None
                            copyright_label = None
                            if (php_isset(lambda : content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["copyright"][0]["attribs"][""]["url"])):
                                copyright_url = self.sanitize(content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["copyright"][0]["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_TEXT)
                            # end if
                            if (php_isset(lambda : content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["copyright"][0]["data"])):
                                copyright_label = self.sanitize(content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["copyright"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                            # end if
                            copyrights = self.registry.create("Copyright", Array(copyright_url, copyright_label))
                        else:
                            copyrights = copyrights_parent
                        # end if
                        #// CREDITS
                        if (php_isset(lambda : content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["credit"])):
                            for credit in content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["credit"]:
                                credit_role = None
                                credit_scheme = None
                                credit_name = None
                                if (php_isset(lambda : credit["attribs"][""]["role"])):
                                    credit_role = self.sanitize(credit["attribs"][""]["role"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                if (php_isset(lambda : credit["attribs"][""]["scheme"])):
                                    credit_scheme = self.sanitize(credit["attribs"][""]["scheme"], SIMPLEPIE_CONSTRUCT_TEXT)
                                else:
                                    credit_scheme = "urn:ebu"
                                # end if
                                if (php_isset(lambda : credit["data"])):
                                    credit_name = self.sanitize(credit["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                credits[-1] = self.registry.create("Credit", Array(credit_role, credit_scheme, credit_name))
                            # end for
                            if php_is_array(credits):
                                credits = php_array_values(array_unique(credits))
                            # end if
                        else:
                            credits = credits_parent
                        # end if
                        #// DESCRIPTION
                        if (php_isset(lambda : content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["description"])):
                            description = self.sanitize(content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["description"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                        else:
                            description = description_parent
                        # end if
                        #// HASHES
                        if (php_isset(lambda : content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["hash"])):
                            for hash in content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["hash"]:
                                value = None
                                algo = None
                                if (php_isset(lambda : hash["data"])):
                                    value = self.sanitize(hash["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                if (php_isset(lambda : hash["attribs"][""]["algo"])):
                                    algo = self.sanitize(hash["attribs"][""]["algo"], SIMPLEPIE_CONSTRUCT_TEXT)
                                else:
                                    algo = "md5"
                                # end if
                                hashes[-1] = algo + ":" + value
                            # end for
                            if php_is_array(hashes):
                                hashes = php_array_values(array_unique(hashes))
                            # end if
                        else:
                            hashes = hashes_parent
                        # end if
                        #// KEYWORDS
                        if (php_isset(lambda : content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["keywords"])):
                            if (php_isset(lambda : content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["keywords"][0]["data"])):
                                temp = php_explode(",", self.sanitize(content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["keywords"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT))
                                for word in temp:
                                    keywords[-1] = php_trim(word)
                                # end for
                                temp = None
                            # end if
                            if php_is_array(keywords):
                                keywords = php_array_values(array_unique(keywords))
                            # end if
                        else:
                            keywords = keywords_parent
                        # end if
                        #// PLAYER
                        if (php_isset(lambda : content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["player"])):
                            player = self.sanitize(content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["player"][0]["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_IRI)
                        else:
                            player = player_parent
                        # end if
                        #// RATINGS
                        if (php_isset(lambda : content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["rating"])):
                            for rating in content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["rating"]:
                                rating_scheme = None
                                rating_value = None
                                if (php_isset(lambda : rating["attribs"][""]["scheme"])):
                                    rating_scheme = self.sanitize(rating["attribs"][""]["scheme"], SIMPLEPIE_CONSTRUCT_TEXT)
                                else:
                                    rating_scheme = "urn:simple"
                                # end if
                                if (php_isset(lambda : rating["data"])):
                                    rating_value = self.sanitize(rating["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                ratings[-1] = self.registry.create("Rating", Array(rating_scheme, rating_value))
                            # end for
                            if php_is_array(ratings):
                                ratings = php_array_values(array_unique(ratings))
                            # end if
                        else:
                            ratings = ratings_parent
                        # end if
                        #// RESTRICTIONS
                        if (php_isset(lambda : content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["restriction"])):
                            for restriction in content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["restriction"]:
                                restriction_relationship = None
                                restriction_type = None
                                restriction_value = None
                                if (php_isset(lambda : restriction["attribs"][""]["relationship"])):
                                    restriction_relationship = self.sanitize(restriction["attribs"][""]["relationship"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                if (php_isset(lambda : restriction["attribs"][""]["type"])):
                                    restriction_type = self.sanitize(restriction["attribs"][""]["type"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                if (php_isset(lambda : restriction["data"])):
                                    restriction_value = self.sanitize(restriction["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                restrictions[-1] = self.registry.create("Restriction", Array(restriction_relationship, restriction_type, restriction_value))
                            # end for
                            if php_is_array(restrictions):
                                restrictions = php_array_values(array_unique(restrictions))
                            # end if
                        else:
                            restrictions = restrictions_parent
                        # end if
                        #// THUMBNAILS
                        if (php_isset(lambda : content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["thumbnail"])):
                            for thumbnail in content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["thumbnail"]:
                                thumbnails[-1] = self.sanitize(thumbnail["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_IRI)
                            # end for
                            if php_is_array(thumbnails):
                                thumbnails = php_array_values(array_unique(thumbnails))
                            # end if
                        else:
                            thumbnails = thumbnails_parent
                        # end if
                        #// TITLES
                        if (php_isset(lambda : content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["title"])):
                            title = self.sanitize(content["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["title"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                        else:
                            title = title_parent
                        # end if
                        self.data["enclosures"][-1] = self.registry.create("Enclosure", Array(url, type, length, None, bitrate, captions, categories, channels, copyrights, credits, description, duration, expression, framerate, hashes, height, keywords, lang, medium, player, ratings, restrictions, samplingrate, thumbnails, title, width))
                    # end if
                # end for
            # end if
            for link in self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "link"):
                if (php_isset(lambda : link["attribs"][""]["href"])) and (not php_empty(lambda : link["attribs"][""]["rel"])) and link["attribs"][""]["rel"] == "enclosure":
                    #// Attributes
                    bitrate = None
                    channels = None
                    duration = None
                    expression = None
                    framerate = None
                    height = None
                    javascript = None
                    lang = None
                    length = None
                    medium = None
                    samplingrate = None
                    type = None
                    url = None
                    width = None
                    url = self.sanitize(link["attribs"][""]["href"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(link))
                    if (php_isset(lambda : link["attribs"][""]["type"])):
                        type = self.sanitize(link["attribs"][""]["type"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : link["attribs"][""]["length"])):
                        length = ceil(link["attribs"][""]["length"])
                    # end if
                    #// Since we don't have group or content for these, we'll just pass the '*_parent' variables directly to the constructor
                    self.data["enclosures"][-1] = self.registry.create("Enclosure", Array(url, type, length, None, bitrate, captions_parent, categories_parent, channels, copyrights_parent, credits_parent, description_parent, duration_parent, expression, framerate, hashes_parent, height, keywords_parent, lang, medium, player_parent, ratings_parent, restrictions_parent, samplingrate, thumbnails_parent, title_parent, width))
                # end if
            # end for
            for link in self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "link"):
                if (php_isset(lambda : link["attribs"][""]["href"])) and (not php_empty(lambda : link["attribs"][""]["rel"])) and link["attribs"][""]["rel"] == "enclosure":
                    #// Attributes
                    bitrate = None
                    channels = None
                    duration = None
                    expression = None
                    framerate = None
                    height = None
                    javascript = None
                    lang = None
                    length = None
                    medium = None
                    samplingrate = None
                    type = None
                    url = None
                    width = None
                    url = self.sanitize(link["attribs"][""]["href"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(link))
                    if (php_isset(lambda : link["attribs"][""]["type"])):
                        type = self.sanitize(link["attribs"][""]["type"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : link["attribs"][""]["length"])):
                        length = ceil(link["attribs"][""]["length"])
                    # end if
                    #// Since we don't have group or content for these, we'll just pass the '*_parent' variables directly to the constructor
                    self.data["enclosures"][-1] = self.registry.create("Enclosure", Array(url, type, length, None, bitrate, captions_parent, categories_parent, channels, copyrights_parent, credits_parent, description_parent, duration_parent, expression, framerate, hashes_parent, height, keywords_parent, lang, medium, player_parent, ratings_parent, restrictions_parent, samplingrate, thumbnails_parent, title_parent, width))
                # end if
            # end for
            enclosure = self.get_item_tags(SIMPLEPIE_NAMESPACE_RSS_20, "enclosure")
            if enclosure:
                if (php_isset(lambda : enclosure[0]["attribs"][""]["url"])):
                    #// Attributes
                    bitrate = None
                    channels = None
                    duration = None
                    expression = None
                    framerate = None
                    height = None
                    javascript = None
                    lang = None
                    length = None
                    medium = None
                    samplingrate = None
                    type = None
                    url = None
                    width = None
                    url = self.sanitize(enclosure[0]["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(enclosure[0]))
                    if (php_isset(lambda : enclosure[0]["attribs"][""]["type"])):
                        type = self.sanitize(enclosure[0]["attribs"][""]["type"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : enclosure[0]["attribs"][""]["length"])):
                        length = ceil(enclosure[0]["attribs"][""]["length"])
                    # end if
                    #// Since we don't have group or content for these, we'll just pass the '*_parent' variables directly to the constructor
                    self.data["enclosures"][-1] = self.registry.create("Enclosure", Array(url, type, length, None, bitrate, captions_parent, categories_parent, channels, copyrights_parent, credits_parent, description_parent, duration_parent, expression, framerate, hashes_parent, height, keywords_parent, lang, medium, player_parent, ratings_parent, restrictions_parent, samplingrate, thumbnails_parent, title_parent, width))
                # end if
            # end if
            if sizeof(self.data["enclosures"]) == 0 and url or type or length or bitrate or captions_parent or categories_parent or channels or copyrights_parent or credits_parent or description_parent or duration_parent or expression or framerate or hashes_parent or height or keywords_parent or lang or medium or player_parent or ratings_parent or restrictions_parent or samplingrate or thumbnails_parent or title_parent or width:
                #// Since we don't have group or content for these, we'll just pass the '*_parent' variables directly to the constructor
                self.data["enclosures"][-1] = self.registry.create("Enclosure", Array(url, type, length, None, bitrate, captions_parent, categories_parent, channels, copyrights_parent, credits_parent, description_parent, duration_parent, expression, framerate, hashes_parent, height, keywords_parent, lang, medium, player_parent, ratings_parent, restrictions_parent, samplingrate, thumbnails_parent, title_parent, width))
            # end if
            self.data["enclosures"] = php_array_values(array_unique(self.data["enclosures"]))
        # end if
        if (not php_empty(lambda : self.data["enclosures"])):
            return self.data["enclosures"]
        else:
            return None
        # end if
    # end def get_enclosures
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
        
        return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_W3C_BASIC_GEO, "lat")
        if return_:
            return float(return_[0]["data"])
        elif self.get_item_tags(SIMPLEPIE_NAMESPACE_GEORSS, "point") and php_preg_match("/^((?:-)?[0-9]+(?:\\.[0-9]+)) ((?:-)?[0-9]+(?:\\.[0-9]+))$/", php_trim(return_[0]["data"]), match):
            return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_GEORSS, "point")
            return float(match[1])
        else:
            return None
        # end if
    # end def get_latitude
    #// 
    #// Get the longitude coordinates for the item
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
        
        return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_W3C_BASIC_GEO, "long")
        if return_:
            return float(return_[0]["data"])
        elif self.get_item_tags(SIMPLEPIE_NAMESPACE_W3C_BASIC_GEO, "lon"):
            return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_W3C_BASIC_GEO, "lon")
            return float(return_[0]["data"])
        elif self.get_item_tags(SIMPLEPIE_NAMESPACE_GEORSS, "point") and php_preg_match("/^((?:-)?[0-9]+(?:\\.[0-9]+)) ((?:-)?[0-9]+(?:\\.[0-9]+))$/", php_trim(return_[0]["data"]), match):
            return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_GEORSS, "point")
            return float(match[2])
        else:
            return None
        # end if
    # end def get_longitude
    #// 
    #// Get the `<atom:source>` for the item
    #// 
    #// @since 1.1
    #// @return SimplePie_Source|null
    #//
    def get_source(self):
        
        return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "source")
        if return_:
            return self.registry.create("Source", Array(self, return_[0]))
        else:
            return None
        # end if
    # end def get_source
# end class SimplePie_Item
