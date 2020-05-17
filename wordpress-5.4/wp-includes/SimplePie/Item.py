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
    #// 
    #// Parent feed
    #// 
    #// @access private
    #// @var SimplePie
    #//
    feed = Array()
    #// 
    #// Raw data
    #// 
    #// @access private
    #// @var array
    #//
    data = Array()
    #// 
    #// Registry object
    #// 
    #// @see set_registry
    #// @var SimplePie_Registry
    #//
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
    def __init__(self, feed_=None, data_=None):
        
        
        self.feed = feed_
        self.data = data_
    # end def __init__
    #// 
    #// Set the registry handler
    #// 
    #// This is usually used by {@see SimplePie_Registry::create}
    #// 
    #// @since 1.3
    #// @param SimplePie_Registry $registry
    #//
    def set_registry(self, registry_=None):
        
        
        self.registry = registry_
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
    def get_item_tags(self, namespace_=None, tag_=None):
        
        
        if (php_isset(lambda : self.data["child"][namespace_][tag_])):
            return self.data["child"][namespace_][tag_]
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
    def get_base(self, element_=None):
        if element_ is None:
            element_ = Array()
        # end if
        
        return self.feed.get_base(element_)
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
    def sanitize(self, data_=None, type_=None, base_=""):
        
        
        return self.feed.sanitize(data_, type_, base_)
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
    def get_id(self, hash_=None):
        if hash_ is None:
            hash_ = False
        # end if
        
        if (not hash_):
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
    def get_description(self, description_only_=None):
        if description_only_ is None:
            description_only_ = False
        # end if
        
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
        elif (not description_only_):
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
    def get_content(self, content_only_=None):
        if content_only_ is None:
            content_only_ = False
        # end if
        
        return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "content")
        if return_:
            return self.sanitize(return_[0]["data"], self.registry.call("Misc", "atom_10_content_construct_type", Array(return_[0]["attribs"])), self.get_base(return_[0]))
        elif self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "content"):
            return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "content")
            return self.sanitize(return_[0]["data"], self.registry.call("Misc", "atom_03_construct_type", Array(return_[0]["attribs"])), self.get_base(return_[0]))
        elif self.get_item_tags(SIMPLEPIE_NAMESPACE_RSS_10_MODULES_CONTENT, "encoded"):
            return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_RSS_10_MODULES_CONTENT, "encoded")
            return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_HTML, self.get_base(return_[0]))
        elif (not content_only_):
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
    def get_category(self, key_=0):
        
        
        categories_ = self.get_categories()
        if (php_isset(lambda : categories_[key_])):
            return categories_[key_]
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
        
        
        categories_ = Array()
        for category_ in self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "category"):
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
        for category_ in self.get_item_tags(SIMPLEPIE_NAMESPACE_RSS_20, "category"):
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
        for category_ in self.get_item_tags(SIMPLEPIE_NAMESPACE_DC_11, "subject"):
            categories_[-1] = self.registry.create("Category", Array(self.sanitize(category_["data"], SIMPLEPIE_CONSTRUCT_TEXT), None, None))
        # end for
        for category_ in self.get_item_tags(SIMPLEPIE_NAMESPACE_DC_10, "subject"):
            categories_[-1] = self.registry.create("Category", Array(self.sanitize(category_["data"], SIMPLEPIE_CONSTRUCT_TEXT), None, None))
        # end for
        if (not php_empty(lambda : categories_)):
            return array_unique(categories_)
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
    def get_author(self, key_=0):
        
        
        authors_ = self.get_authors()
        if (php_isset(lambda : authors_[key_])):
            return authors_[key_]
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
    def get_contributor(self, key_=0):
        
        
        contributors_ = self.get_contributors()
        if (php_isset(lambda : contributors_[key_])):
            return contributors_[key_]
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
        
        
        contributors_ = Array()
        for contributor_ in self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "contributor"):
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
        for contributor_ in self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "contributor"):
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
    #// Get all authors for the item
    #// 
    #// Uses `<atom:author>`, `<author>`, `<dc:creator>` or `<itunes:author>`
    #// 
    #// @since Beta 2
    #// @return array|null List of {@see SimplePie_Author} objects
    #//
    def get_authors(self):
        
        
        authors_ = Array()
        for author_ in self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "author"):
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
        author_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "author")
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
        author_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_RSS_20, "author")
        if author_:
            authors_[-1] = self.registry.create("Author", Array(None, None, self.sanitize(author_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)))
        # end if
        for author_ in self.get_item_tags(SIMPLEPIE_NAMESPACE_DC_11, "creator"):
            authors_[-1] = self.registry.create("Author", Array(self.sanitize(author_["data"], SIMPLEPIE_CONSTRUCT_TEXT), None, None))
        # end for
        for author_ in self.get_item_tags(SIMPLEPIE_NAMESPACE_DC_10, "creator"):
            authors_[-1] = self.registry.create("Author", Array(self.sanitize(author_["data"], SIMPLEPIE_CONSTRUCT_TEXT), None, None))
        # end for
        for author_ in self.get_item_tags(SIMPLEPIE_NAMESPACE_ITUNES, "author"):
            authors_[-1] = self.registry.create("Author", Array(self.sanitize(author_["data"], SIMPLEPIE_CONSTRUCT_TEXT), None, None))
        # end for
        if (not php_empty(lambda : authors_)):
            return array_unique(authors_)
        elif self.get_source() and source_.get_authors():
            source_ = self.get_source()
            authors_ = source_.get_authors()
            return authors_
        elif self.feed.get_authors():
            authors_ = self.feed.get_authors()
            return authors_
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
    def get_date(self, date_format_="j F Y, g:i a"):
        
        
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
                parser_ = self.registry.call("Parse_Date", "get")
                self.data["date"]["parsed"] = parser_.parse(self.data["date"]["raw"])
            else:
                self.data["date"] = None
            # end if
        # end if
        if self.data["date"]:
            date_format_ = php_str(date_format_)
            for case in Switch(date_format_):
                if case(""):
                    return self.sanitize(self.data["date"]["raw"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
                if case("U"):
                    return self.data["date"]["parsed"]
                # end if
                if case():
                    return date(date_format_, self.data["date"]["parsed"])
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
    def get_updated_date(self, date_format_="j F Y, g:i a"):
        
        
        if (not (php_isset(lambda : self.data["updated"]))):
            return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "updated")
            if return_:
                self.data["updated"]["raw"] = return_[0]["data"]
            # end if
            if (not php_empty(lambda : self.data["updated"]["raw"])):
                parser_ = self.registry.call("Parse_Date", "get")
                self.data["updated"]["parsed"] = parser_.parse(self.data["date"]["raw"])
            else:
                self.data["updated"] = None
            # end if
        # end if
        if self.data["updated"]:
            date_format_ = php_str(date_format_)
            for case in Switch(date_format_):
                if case(""):
                    return self.sanitize(self.data["updated"]["raw"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
                if case("U"):
                    return self.data["updated"]["parsed"]
                # end if
                if case():
                    return date(date_format_, self.data["updated"]["parsed"])
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
    def get_local_date(self, date_format_="%c"):
        
        
        if (not date_format_):
            return self.sanitize(self.get_date(""), SIMPLEPIE_CONSTRUCT_TEXT)
        elif self.get_date("U") != None and date_ != False:
            date_ = self.get_date("U")
            return strftime(date_format_, date_)
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
    def get_gmdate(self, date_format_="j F Y, g:i a"):
        
        
        date_ = self.get_date("U")
        if date_ == None:
            return None
        # end if
        return gmdate(date_format_, date_)
    # end def get_gmdate
    #// 
    #// Get the update date/time for the item (UTC time)
    #// 
    #// @see get_updated_date
    #// @param string $date_format Supports any PHP date format from {@see http://php.net/date}
    #// @return int|string|null
    #//
    def get_updated_gmdate(self, date_format_="j F Y, g:i a"):
        
        
        date_ = self.get_updated_date("U")
        if date_ == None:
            return None
        # end if
        return gmdate(date_format_, date_)
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
        
        
        link_ = self.get_link()
        enclosure_ = self.get_enclosure(0)
        if link_ != None:
            return link_
        elif enclosure_ != None:
            return enclosure_.get_link()
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
    def get_link(self, key_=0, rel_="alternate"):
        
        
        links_ = self.get_links(rel_)
        if links_[key_] != None:
            return links_[key_]
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
    def get_links(self, rel_="alternate"):
        
        
        if (not (php_isset(lambda : self.data["links"]))):
            self.data["links"] = Array()
            for link_ in self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "link"):
                if (php_isset(lambda : link_["attribs"][""]["href"])):
                    link_rel_ = link_["attribs"][""]["rel"] if (php_isset(lambda : link_["attribs"][""]["rel"])) else "alternate"
                    self.data["links"][link_rel_][-1] = self.sanitize(link_["attribs"][""]["href"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(link_))
                # end if
            # end for
            for link_ in self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "link"):
                if (php_isset(lambda : link_["attribs"][""]["href"])):
                    link_rel_ = link_["attribs"][""]["rel"] if (php_isset(lambda : link_["attribs"][""]["rel"])) else "alternate"
                    self.data["links"][link_rel_][-1] = self.sanitize(link_["attribs"][""]["href"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(link_))
                # end if
            # end for
            links_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_RSS_10, "link")
            if links_:
                self.data["links"]["alternate"][-1] = self.sanitize(links_[0]["data"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(links_[0]))
            # end if
            links_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_RSS_090, "link")
            if links_:
                self.data["links"]["alternate"][-1] = self.sanitize(links_[0]["data"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(links_[0]))
            # end if
            links_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_RSS_20, "link")
            if links_:
                self.data["links"]["alternate"][-1] = self.sanitize(links_[0]["data"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(links_[0]))
            # end if
            links_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_RSS_20, "guid")
            if links_:
                if (not (php_isset(lambda : links_[0]["attribs"][""]["isPermaLink"]))) or php_strtolower(php_trim(links_[0]["attribs"][""]["isPermaLink"])) == "true":
                    self.data["links"]["alternate"][-1] = self.sanitize(links_[0]["data"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(links_[0]))
                # end if
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
    def get_enclosure(self, key_=0, prefer_=None):
        
        
        enclosures_ = self.get_enclosures()
        if (php_isset(lambda : enclosures_[key_])):
            return enclosures_[key_]
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
            captions_parent_ = None
            categories_parent_ = None
            copyrights_parent_ = None
            credits_parent_ = None
            description_parent_ = None
            duration_parent_ = None
            hashes_parent_ = None
            keywords_parent_ = None
            player_parent_ = None
            ratings_parent_ = None
            restrictions_parent_ = None
            thumbnails_parent_ = None
            title_parent_ = None
            #// Let's do the channel and item-level ones first, and just re-use them if we need to.
            parent_ = self.get_feed()
            #// CAPTIONS
            captions_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "text")
            if captions_:
                for caption_ in captions_:
                    caption_type_ = None
                    caption_lang_ = None
                    caption_startTime_ = None
                    caption_endTime_ = None
                    caption_text_ = None
                    if (php_isset(lambda : caption_["attribs"][""]["type"])):
                        caption_type_ = self.sanitize(caption_["attribs"][""]["type"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : caption_["attribs"][""]["lang"])):
                        caption_lang_ = self.sanitize(caption_["attribs"][""]["lang"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : caption_["attribs"][""]["start"])):
                        caption_startTime_ = self.sanitize(caption_["attribs"][""]["start"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : caption_["attribs"][""]["end"])):
                        caption_endTime_ = self.sanitize(caption_["attribs"][""]["end"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : caption_["data"])):
                        caption_text_ = self.sanitize(caption_["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    captions_parent_[-1] = self.registry.create("Caption", Array(caption_type_, caption_lang_, caption_startTime_, caption_endTime_, caption_text_))
                # end for
            elif parent_.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "text"):
                captions_ = parent_.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "text")
                for caption_ in captions_:
                    caption_type_ = None
                    caption_lang_ = None
                    caption_startTime_ = None
                    caption_endTime_ = None
                    caption_text_ = None
                    if (php_isset(lambda : caption_["attribs"][""]["type"])):
                        caption_type_ = self.sanitize(caption_["attribs"][""]["type"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : caption_["attribs"][""]["lang"])):
                        caption_lang_ = self.sanitize(caption_["attribs"][""]["lang"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : caption_["attribs"][""]["start"])):
                        caption_startTime_ = self.sanitize(caption_["attribs"][""]["start"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : caption_["attribs"][""]["end"])):
                        caption_endTime_ = self.sanitize(caption_["attribs"][""]["end"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : caption_["data"])):
                        caption_text_ = self.sanitize(caption_["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    captions_parent_[-1] = self.registry.create("Caption", Array(caption_type_, caption_lang_, caption_startTime_, caption_endTime_, caption_text_))
                # end for
            # end if
            if php_is_array(captions_parent_):
                captions_parent_ = php_array_values(array_unique(captions_parent_))
            # end if
            #// CATEGORIES
            for category_ in self.get_item_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "category"):
                term_ = None
                scheme_ = None
                label_ = None
                if (php_isset(lambda : category_["data"])):
                    term_ = self.sanitize(category_["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
                if (php_isset(lambda : category_["attribs"][""]["scheme"])):
                    scheme_ = self.sanitize(category_["attribs"][""]["scheme"], SIMPLEPIE_CONSTRUCT_TEXT)
                else:
                    scheme_ = "http://search.yahoo.com/mrss/category_schema"
                # end if
                if (php_isset(lambda : category_["attribs"][""]["label"])):
                    label_ = self.sanitize(category_["attribs"][""]["label"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
                categories_parent_[-1] = self.registry.create("Category", Array(term_, scheme_, label_))
            # end for
            for category_ in parent_.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "category"):
                term_ = None
                scheme_ = None
                label_ = None
                if (php_isset(lambda : category_["data"])):
                    term_ = self.sanitize(category_["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
                if (php_isset(lambda : category_["attribs"][""]["scheme"])):
                    scheme_ = self.sanitize(category_["attribs"][""]["scheme"], SIMPLEPIE_CONSTRUCT_TEXT)
                else:
                    scheme_ = "http://search.yahoo.com/mrss/category_schema"
                # end if
                if (php_isset(lambda : category_["attribs"][""]["label"])):
                    label_ = self.sanitize(category_["attribs"][""]["label"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
                categories_parent_[-1] = self.registry.create("Category", Array(term_, scheme_, label_))
            # end for
            for category_ in parent_.get_channel_tags(SIMPLEPIE_NAMESPACE_ITUNES, "category"):
                term_ = None
                scheme_ = "http://www.itunes.com/dtds/podcast-1.0.dtd"
                label_ = None
                if (php_isset(lambda : category_["attribs"][""]["text"])):
                    label_ = self.sanitize(category_["attribs"][""]["text"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
                categories_parent_[-1] = self.registry.create("Category", Array(term_, scheme_, label_))
                if (php_isset(lambda : category_["child"][SIMPLEPIE_NAMESPACE_ITUNES]["category"])):
                    for subcategory_ in category_["child"][SIMPLEPIE_NAMESPACE_ITUNES]["category"]:
                        if (php_isset(lambda : subcategory_["attribs"][""]["text"])):
                            label_ = self.sanitize(subcategory_["attribs"][""]["text"], SIMPLEPIE_CONSTRUCT_TEXT)
                        # end if
                        categories_parent_[-1] = self.registry.create("Category", Array(term_, scheme_, label_))
                    # end for
                # end if
            # end for
            if php_is_array(categories_parent_):
                categories_parent_ = php_array_values(array_unique(categories_parent_))
            # end if
            #// COPYRIGHT
            copyright_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "copyright")
            if copyright_:
                copyright_url_ = None
                copyright_label_ = None
                if (php_isset(lambda : copyright_[0]["attribs"][""]["url"])):
                    copyright_url_ = self.sanitize(copyright_[0]["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
                if (php_isset(lambda : copyright_[0]["data"])):
                    copyright_label_ = self.sanitize(copyright_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
                copyrights_parent_ = self.registry.create("Copyright", Array(copyright_url_, copyright_label_))
            elif parent_.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "copyright"):
                copyright_ = parent_.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "copyright")
                copyright_url_ = None
                copyright_label_ = None
                if (php_isset(lambda : copyright_[0]["attribs"][""]["url"])):
                    copyright_url_ = self.sanitize(copyright_[0]["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
                if (php_isset(lambda : copyright_[0]["data"])):
                    copyright_label_ = self.sanitize(copyright_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
                copyrights_parent_ = self.registry.create("Copyright", Array(copyright_url_, copyright_label_))
            # end if
            #// CREDITS
            credits_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "credit")
            if credits_:
                for credit_ in credits_:
                    credit_role_ = None
                    credit_scheme_ = None
                    credit_name_ = None
                    if (php_isset(lambda : credit_["attribs"][""]["role"])):
                        credit_role_ = self.sanitize(credit_["attribs"][""]["role"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : credit_["attribs"][""]["scheme"])):
                        credit_scheme_ = self.sanitize(credit_["attribs"][""]["scheme"], SIMPLEPIE_CONSTRUCT_TEXT)
                    else:
                        credit_scheme_ = "urn:ebu"
                    # end if
                    if (php_isset(lambda : credit_["data"])):
                        credit_name_ = self.sanitize(credit_["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    credits_parent_[-1] = self.registry.create("Credit", Array(credit_role_, credit_scheme_, credit_name_))
                # end for
            elif parent_.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "credit"):
                credits_ = parent_.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "credit")
                for credit_ in credits_:
                    credit_role_ = None
                    credit_scheme_ = None
                    credit_name_ = None
                    if (php_isset(lambda : credit_["attribs"][""]["role"])):
                        credit_role_ = self.sanitize(credit_["attribs"][""]["role"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : credit_["attribs"][""]["scheme"])):
                        credit_scheme_ = self.sanitize(credit_["attribs"][""]["scheme"], SIMPLEPIE_CONSTRUCT_TEXT)
                    else:
                        credit_scheme_ = "urn:ebu"
                    # end if
                    if (php_isset(lambda : credit_["data"])):
                        credit_name_ = self.sanitize(credit_["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    credits_parent_[-1] = self.registry.create("Credit", Array(credit_role_, credit_scheme_, credit_name_))
                # end for
            # end if
            if php_is_array(credits_parent_):
                credits_parent_ = php_array_values(array_unique(credits_parent_))
            # end if
            #// DESCRIPTION
            description_parent_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "description")
            if description_parent_:
                if (php_isset(lambda : description_parent_[0]["data"])):
                    description_parent_ = self.sanitize(description_parent_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
            elif parent_.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "description"):
                description_parent_ = parent_.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "description")
                if (php_isset(lambda : description_parent_[0]["data"])):
                    description_parent_ = self.sanitize(description_parent_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
            # end if
            #// DURATION
            duration_parent_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_ITUNES, "duration")
            if duration_parent_:
                seconds_ = None
                minutes_ = None
                hours_ = None
                if (php_isset(lambda : duration_parent_[0]["data"])):
                    temp_ = php_explode(":", self.sanitize(duration_parent_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT))
                    if sizeof(temp_) > 0:
                        seconds_ = php_int(php_array_pop(temp_))
                    # end if
                    if sizeof(temp_) > 0:
                        minutes_ = php_int(php_array_pop(temp_))
                        seconds_ += minutes_ * 60
                    # end if
                    if sizeof(temp_) > 0:
                        hours_ = php_int(php_array_pop(temp_))
                        seconds_ += hours_ * 3600
                    # end if
                    temp_ = None
                    duration_parent_ = seconds_
                # end if
            # end if
            #// HASHES
            hashes_iterator_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "hash")
            if hashes_iterator_:
                for hash_ in hashes_iterator_:
                    value_ = None
                    algo_ = None
                    if (php_isset(lambda : hash_["data"])):
                        value_ = self.sanitize(hash_["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : hash_["attribs"][""]["algo"])):
                        algo_ = self.sanitize(hash_["attribs"][""]["algo"], SIMPLEPIE_CONSTRUCT_TEXT)
                    else:
                        algo_ = "md5"
                    # end if
                    hashes_parent_[-1] = algo_ + ":" + value_
                # end for
            elif parent_.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "hash"):
                hashes_iterator_ = parent_.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "hash")
                for hash_ in hashes_iterator_:
                    value_ = None
                    algo_ = None
                    if (php_isset(lambda : hash_["data"])):
                        value_ = self.sanitize(hash_["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : hash_["attribs"][""]["algo"])):
                        algo_ = self.sanitize(hash_["attribs"][""]["algo"], SIMPLEPIE_CONSTRUCT_TEXT)
                    else:
                        algo_ = "md5"
                    # end if
                    hashes_parent_[-1] = algo_ + ":" + value_
                # end for
            # end if
            if php_is_array(hashes_parent_):
                hashes_parent_ = php_array_values(array_unique(hashes_parent_))
            # end if
            #// KEYWORDS
            keywords_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "keywords")
            if keywords_:
                if (php_isset(lambda : keywords_[0]["data"])):
                    temp_ = php_explode(",", self.sanitize(keywords_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT))
                    for word_ in temp_:
                        keywords_parent_[-1] = php_trim(word_)
                    # end for
                # end if
                temp_ = None
            elif self.get_item_tags(SIMPLEPIE_NAMESPACE_ITUNES, "keywords"):
                keywords_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_ITUNES, "keywords")
                if (php_isset(lambda : keywords_[0]["data"])):
                    temp_ = php_explode(",", self.sanitize(keywords_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT))
                    for word_ in temp_:
                        keywords_parent_[-1] = php_trim(word_)
                    # end for
                # end if
                temp_ = None
            elif parent_.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "keywords"):
                keywords_ = parent_.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "keywords")
                if (php_isset(lambda : keywords_[0]["data"])):
                    temp_ = php_explode(",", self.sanitize(keywords_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT))
                    for word_ in temp_:
                        keywords_parent_[-1] = php_trim(word_)
                    # end for
                # end if
                temp_ = None
            elif parent_.get_channel_tags(SIMPLEPIE_NAMESPACE_ITUNES, "keywords"):
                keywords_ = parent_.get_channel_tags(SIMPLEPIE_NAMESPACE_ITUNES, "keywords")
                if (php_isset(lambda : keywords_[0]["data"])):
                    temp_ = php_explode(",", self.sanitize(keywords_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT))
                    for word_ in temp_:
                        keywords_parent_[-1] = php_trim(word_)
                    # end for
                # end if
                temp_ = None
            # end if
            if php_is_array(keywords_parent_):
                keywords_parent_ = php_array_values(array_unique(keywords_parent_))
            # end if
            #// PLAYER
            player_parent_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "player")
            if player_parent_:
                if (php_isset(lambda : player_parent_[0]["attribs"][""]["url"])):
                    player_parent_ = self.sanitize(player_parent_[0]["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_IRI)
                # end if
            elif parent_.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "player"):
                player_parent_ = parent_.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "player")
                if (php_isset(lambda : player_parent_[0]["attribs"][""]["url"])):
                    player_parent_ = self.sanitize(player_parent_[0]["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_IRI)
                # end if
            # end if
            #// RATINGS
            ratings_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "rating")
            if ratings_:
                for rating_ in ratings_:
                    rating_scheme_ = None
                    rating_value_ = None
                    if (php_isset(lambda : rating_["attribs"][""]["scheme"])):
                        rating_scheme_ = self.sanitize(rating_["attribs"][""]["scheme"], SIMPLEPIE_CONSTRUCT_TEXT)
                    else:
                        rating_scheme_ = "urn:simple"
                    # end if
                    if (php_isset(lambda : rating_["data"])):
                        rating_value_ = self.sanitize(rating_["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    ratings_parent_[-1] = self.registry.create("Rating", Array(rating_scheme_, rating_value_))
                # end for
            elif self.get_item_tags(SIMPLEPIE_NAMESPACE_ITUNES, "explicit"):
                ratings_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_ITUNES, "explicit")
                for rating_ in ratings_:
                    rating_scheme_ = "urn:itunes"
                    rating_value_ = None
                    if (php_isset(lambda : rating_["data"])):
                        rating_value_ = self.sanitize(rating_["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    ratings_parent_[-1] = self.registry.create("Rating", Array(rating_scheme_, rating_value_))
                # end for
            elif parent_.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "rating"):
                ratings_ = parent_.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "rating")
                for rating_ in ratings_:
                    rating_scheme_ = None
                    rating_value_ = None
                    if (php_isset(lambda : rating_["attribs"][""]["scheme"])):
                        rating_scheme_ = self.sanitize(rating_["attribs"][""]["scheme"], SIMPLEPIE_CONSTRUCT_TEXT)
                    else:
                        rating_scheme_ = "urn:simple"
                    # end if
                    if (php_isset(lambda : rating_["data"])):
                        rating_value_ = self.sanitize(rating_["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    ratings_parent_[-1] = self.registry.create("Rating", Array(rating_scheme_, rating_value_))
                # end for
            elif parent_.get_channel_tags(SIMPLEPIE_NAMESPACE_ITUNES, "explicit"):
                ratings_ = parent_.get_channel_tags(SIMPLEPIE_NAMESPACE_ITUNES, "explicit")
                for rating_ in ratings_:
                    rating_scheme_ = "urn:itunes"
                    rating_value_ = None
                    if (php_isset(lambda : rating_["data"])):
                        rating_value_ = self.sanitize(rating_["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    ratings_parent_[-1] = self.registry.create("Rating", Array(rating_scheme_, rating_value_))
                # end for
            # end if
            if php_is_array(ratings_parent_):
                ratings_parent_ = php_array_values(array_unique(ratings_parent_))
            # end if
            #// RESTRICTIONS
            restrictions_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "restriction")
            if restrictions_:
                for restriction_ in restrictions_:
                    restriction_relationship_ = None
                    restriction_type_ = None
                    restriction_value_ = None
                    if (php_isset(lambda : restriction_["attribs"][""]["relationship"])):
                        restriction_relationship_ = self.sanitize(restriction_["attribs"][""]["relationship"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : restriction_["attribs"][""]["type"])):
                        restriction_type_ = self.sanitize(restriction_["attribs"][""]["type"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : restriction_["data"])):
                        restriction_value_ = self.sanitize(restriction_["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    restrictions_parent_[-1] = self.registry.create("Restriction", Array(restriction_relationship_, restriction_type_, restriction_value_))
                # end for
            elif self.get_item_tags(SIMPLEPIE_NAMESPACE_ITUNES, "block"):
                restrictions_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_ITUNES, "block")
                for restriction_ in restrictions_:
                    restriction_relationship_ = "allow"
                    restriction_type_ = None
                    restriction_value_ = "itunes"
                    if (php_isset(lambda : restriction_["data"])) and php_strtolower(restriction_["data"]) == "yes":
                        restriction_relationship_ = "deny"
                    # end if
                    restrictions_parent_[-1] = self.registry.create("Restriction", Array(restriction_relationship_, restriction_type_, restriction_value_))
                # end for
            elif parent_.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "restriction"):
                restrictions_ = parent_.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "restriction")
                for restriction_ in restrictions_:
                    restriction_relationship_ = None
                    restriction_type_ = None
                    restriction_value_ = None
                    if (php_isset(lambda : restriction_["attribs"][""]["relationship"])):
                        restriction_relationship_ = self.sanitize(restriction_["attribs"][""]["relationship"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : restriction_["attribs"][""]["type"])):
                        restriction_type_ = self.sanitize(restriction_["attribs"][""]["type"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : restriction_["data"])):
                        restriction_value_ = self.sanitize(restriction_["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    restrictions_parent_[-1] = self.registry.create("Restriction", Array(restriction_relationship_, restriction_type_, restriction_value_))
                # end for
            elif parent_.get_channel_tags(SIMPLEPIE_NAMESPACE_ITUNES, "block"):
                restrictions_ = parent_.get_channel_tags(SIMPLEPIE_NAMESPACE_ITUNES, "block")
                for restriction_ in restrictions_:
                    restriction_relationship_ = "allow"
                    restriction_type_ = None
                    restriction_value_ = "itunes"
                    if (php_isset(lambda : restriction_["data"])) and php_strtolower(restriction_["data"]) == "yes":
                        restriction_relationship_ = "deny"
                    # end if
                    restrictions_parent_[-1] = self.registry.create("Restriction", Array(restriction_relationship_, restriction_type_, restriction_value_))
                # end for
            # end if
            if php_is_array(restrictions_parent_):
                restrictions_parent_ = php_array_values(array_unique(restrictions_parent_))
            else:
                restrictions_parent_ = Array(php_new_class("SimplePie_Restriction", lambda : SimplePie_Restriction("allow", None, "default")))
            # end if
            #// THUMBNAILS
            thumbnails_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "thumbnail")
            if thumbnails_:
                for thumbnail_ in thumbnails_:
                    if (php_isset(lambda : thumbnail_["attribs"][""]["url"])):
                        thumbnails_parent_[-1] = self.sanitize(thumbnail_["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_IRI)
                    # end if
                # end for
            elif parent_.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "thumbnail"):
                thumbnails_ = parent_.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "thumbnail")
                for thumbnail_ in thumbnails_:
                    if (php_isset(lambda : thumbnail_["attribs"][""]["url"])):
                        thumbnails_parent_[-1] = self.sanitize(thumbnail_["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_IRI)
                    # end if
                # end for
            # end if
            #// TITLES
            title_parent_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "title")
            if title_parent_:
                if (php_isset(lambda : title_parent_[0]["data"])):
                    title_parent_ = self.sanitize(title_parent_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
            elif parent_.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "title"):
                title_parent_ = parent_.get_channel_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "title")
                if (php_isset(lambda : title_parent_[0]["data"])):
                    title_parent_ = self.sanitize(title_parent_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                # end if
            # end if
            parent_ = None
            #// Attributes
            bitrate_ = None
            channels_ = None
            duration_ = None
            expression_ = None
            framerate_ = None
            height_ = None
            javascript_ = None
            lang_ = None
            length_ = None
            medium_ = None
            samplingrate_ = None
            type_ = None
            url_ = None
            width_ = None
            #// Elements
            captions_ = None
            categories_ = None
            copyrights_ = None
            credits_ = None
            description_ = None
            hashes_ = None
            keywords_ = None
            player_ = None
            ratings_ = None
            restrictions_ = None
            thumbnails_ = None
            title_ = None
            #// If we have media:group tags, loop through them.
            for group_ in self.get_item_tags(SIMPLEPIE_NAMESPACE_MEDIARSS, "group"):
                if (php_isset(lambda : group_["child"])) and (php_isset(lambda : group_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["content"])):
                    #// If we have media:content tags, loop through them.
                    for content_ in group_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["content"]:
                        if (php_isset(lambda : content_["attribs"][""]["url"])):
                            #// Attributes
                            bitrate_ = None
                            channels_ = None
                            duration_ = None
                            expression_ = None
                            framerate_ = None
                            height_ = None
                            javascript_ = None
                            lang_ = None
                            length_ = None
                            medium_ = None
                            samplingrate_ = None
                            type_ = None
                            url_ = None
                            width_ = None
                            #// Elements
                            captions_ = None
                            categories_ = None
                            copyrights_ = None
                            credits_ = None
                            description_ = None
                            hashes_ = None
                            keywords_ = None
                            player_ = None
                            ratings_ = None
                            restrictions_ = None
                            thumbnails_ = None
                            title_ = None
                            #// Start checking the attributes of media:content
                            if (php_isset(lambda : content_["attribs"][""]["bitrate"])):
                                bitrate_ = self.sanitize(content_["attribs"][""]["bitrate"], SIMPLEPIE_CONSTRUCT_TEXT)
                            # end if
                            if (php_isset(lambda : content_["attribs"][""]["channels"])):
                                channels_ = self.sanitize(content_["attribs"][""]["channels"], SIMPLEPIE_CONSTRUCT_TEXT)
                            # end if
                            if (php_isset(lambda : content_["attribs"][""]["duration"])):
                                duration_ = self.sanitize(content_["attribs"][""]["duration"], SIMPLEPIE_CONSTRUCT_TEXT)
                            else:
                                duration_ = duration_parent_
                            # end if
                            if (php_isset(lambda : content_["attribs"][""]["expression"])):
                                expression_ = self.sanitize(content_["attribs"][""]["expression"], SIMPLEPIE_CONSTRUCT_TEXT)
                            # end if
                            if (php_isset(lambda : content_["attribs"][""]["framerate"])):
                                framerate_ = self.sanitize(content_["attribs"][""]["framerate"], SIMPLEPIE_CONSTRUCT_TEXT)
                            # end if
                            if (php_isset(lambda : content_["attribs"][""]["height"])):
                                height_ = self.sanitize(content_["attribs"][""]["height"], SIMPLEPIE_CONSTRUCT_TEXT)
                            # end if
                            if (php_isset(lambda : content_["attribs"][""]["lang"])):
                                lang_ = self.sanitize(content_["attribs"][""]["lang"], SIMPLEPIE_CONSTRUCT_TEXT)
                            # end if
                            if (php_isset(lambda : content_["attribs"][""]["fileSize"])):
                                length_ = ceil(content_["attribs"][""]["fileSize"])
                            # end if
                            if (php_isset(lambda : content_["attribs"][""]["medium"])):
                                medium_ = self.sanitize(content_["attribs"][""]["medium"], SIMPLEPIE_CONSTRUCT_TEXT)
                            # end if
                            if (php_isset(lambda : content_["attribs"][""]["samplingrate"])):
                                samplingrate_ = self.sanitize(content_["attribs"][""]["samplingrate"], SIMPLEPIE_CONSTRUCT_TEXT)
                            # end if
                            if (php_isset(lambda : content_["attribs"][""]["type"])):
                                type_ = self.sanitize(content_["attribs"][""]["type"], SIMPLEPIE_CONSTRUCT_TEXT)
                            # end if
                            if (php_isset(lambda : content_["attribs"][""]["width"])):
                                width_ = self.sanitize(content_["attribs"][""]["width"], SIMPLEPIE_CONSTRUCT_TEXT)
                            # end if
                            url_ = self.sanitize(content_["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_IRI)
                            #// Checking the other optional media: elements. Priority: media:content, media:group, item, channel
                            #// CAPTIONS
                            if (php_isset(lambda : content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["text"])):
                                for caption_ in content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["text"]:
                                    caption_type_ = None
                                    caption_lang_ = None
                                    caption_startTime_ = None
                                    caption_endTime_ = None
                                    caption_text_ = None
                                    if (php_isset(lambda : caption_["attribs"][""]["type"])):
                                        caption_type_ = self.sanitize(caption_["attribs"][""]["type"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : caption_["attribs"][""]["lang"])):
                                        caption_lang_ = self.sanitize(caption_["attribs"][""]["lang"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : caption_["attribs"][""]["start"])):
                                        caption_startTime_ = self.sanitize(caption_["attribs"][""]["start"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : caption_["attribs"][""]["end"])):
                                        caption_endTime_ = self.sanitize(caption_["attribs"][""]["end"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : caption_["data"])):
                                        caption_text_ = self.sanitize(caption_["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    captions_[-1] = self.registry.create("Caption", Array(caption_type_, caption_lang_, caption_startTime_, caption_endTime_, caption_text_))
                                # end for
                                if php_is_array(captions_):
                                    captions_ = php_array_values(array_unique(captions_))
                                # end if
                            elif (php_isset(lambda : group_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["text"])):
                                for caption_ in group_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["text"]:
                                    caption_type_ = None
                                    caption_lang_ = None
                                    caption_startTime_ = None
                                    caption_endTime_ = None
                                    caption_text_ = None
                                    if (php_isset(lambda : caption_["attribs"][""]["type"])):
                                        caption_type_ = self.sanitize(caption_["attribs"][""]["type"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : caption_["attribs"][""]["lang"])):
                                        caption_lang_ = self.sanitize(caption_["attribs"][""]["lang"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : caption_["attribs"][""]["start"])):
                                        caption_startTime_ = self.sanitize(caption_["attribs"][""]["start"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : caption_["attribs"][""]["end"])):
                                        caption_endTime_ = self.sanitize(caption_["attribs"][""]["end"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : caption_["data"])):
                                        caption_text_ = self.sanitize(caption_["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    captions_[-1] = self.registry.create("Caption", Array(caption_type_, caption_lang_, caption_startTime_, caption_endTime_, caption_text_))
                                # end for
                                if php_is_array(captions_):
                                    captions_ = php_array_values(array_unique(captions_))
                                # end if
                            else:
                                captions_ = captions_parent_
                            # end if
                            #// CATEGORIES
                            if (php_isset(lambda : content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["category"])):
                                for category_ in content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["category"]:
                                    term_ = None
                                    scheme_ = None
                                    label_ = None
                                    if (php_isset(lambda : category_["data"])):
                                        term_ = self.sanitize(category_["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : category_["attribs"][""]["scheme"])):
                                        scheme_ = self.sanitize(category_["attribs"][""]["scheme"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    else:
                                        scheme_ = "http://search.yahoo.com/mrss/category_schema"
                                    # end if
                                    if (php_isset(lambda : category_["attribs"][""]["label"])):
                                        label_ = self.sanitize(category_["attribs"][""]["label"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    categories_[-1] = self.registry.create("Category", Array(term_, scheme_, label_))
                                # end for
                            # end if
                            if (php_isset(lambda : group_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["category"])):
                                for category_ in group_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["category"]:
                                    term_ = None
                                    scheme_ = None
                                    label_ = None
                                    if (php_isset(lambda : category_["data"])):
                                        term_ = self.sanitize(category_["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : category_["attribs"][""]["scheme"])):
                                        scheme_ = self.sanitize(category_["attribs"][""]["scheme"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    else:
                                        scheme_ = "http://search.yahoo.com/mrss/category_schema"
                                    # end if
                                    if (php_isset(lambda : category_["attribs"][""]["label"])):
                                        label_ = self.sanitize(category_["attribs"][""]["label"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    categories_[-1] = self.registry.create("Category", Array(term_, scheme_, label_))
                                # end for
                            # end if
                            if php_is_array(categories_) and php_is_array(categories_parent_):
                                categories_ = php_array_values(array_unique(php_array_merge(categories_, categories_parent_)))
                            elif php_is_array(categories_):
                                categories_ = php_array_values(array_unique(categories_))
                            elif php_is_array(categories_parent_):
                                categories_ = php_array_values(array_unique(categories_parent_))
                            # end if
                            #// COPYRIGHTS
                            if (php_isset(lambda : content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["copyright"])):
                                copyright_url_ = None
                                copyright_label_ = None
                                if (php_isset(lambda : content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["copyright"][0]["attribs"][""]["url"])):
                                    copyright_url_ = self.sanitize(content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["copyright"][0]["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                if (php_isset(lambda : content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["copyright"][0]["data"])):
                                    copyright_label_ = self.sanitize(content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["copyright"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                copyrights_ = self.registry.create("Copyright", Array(copyright_url_, copyright_label_))
                            elif (php_isset(lambda : group_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["copyright"])):
                                copyright_url_ = None
                                copyright_label_ = None
                                if (php_isset(lambda : group_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["copyright"][0]["attribs"][""]["url"])):
                                    copyright_url_ = self.sanitize(group_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["copyright"][0]["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                if (php_isset(lambda : group_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["copyright"][0]["data"])):
                                    copyright_label_ = self.sanitize(group_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["copyright"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                copyrights_ = self.registry.create("Copyright", Array(copyright_url_, copyright_label_))
                            else:
                                copyrights_ = copyrights_parent_
                            # end if
                            #// CREDITS
                            if (php_isset(lambda : content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["credit"])):
                                for credit_ in content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["credit"]:
                                    credit_role_ = None
                                    credit_scheme_ = None
                                    credit_name_ = None
                                    if (php_isset(lambda : credit_["attribs"][""]["role"])):
                                        credit_role_ = self.sanitize(credit_["attribs"][""]["role"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : credit_["attribs"][""]["scheme"])):
                                        credit_scheme_ = self.sanitize(credit_["attribs"][""]["scheme"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    else:
                                        credit_scheme_ = "urn:ebu"
                                    # end if
                                    if (php_isset(lambda : credit_["data"])):
                                        credit_name_ = self.sanitize(credit_["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    credits_[-1] = self.registry.create("Credit", Array(credit_role_, credit_scheme_, credit_name_))
                                # end for
                                if php_is_array(credits_):
                                    credits_ = php_array_values(array_unique(credits_))
                                # end if
                            elif (php_isset(lambda : group_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["credit"])):
                                for credit_ in group_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["credit"]:
                                    credit_role_ = None
                                    credit_scheme_ = None
                                    credit_name_ = None
                                    if (php_isset(lambda : credit_["attribs"][""]["role"])):
                                        credit_role_ = self.sanitize(credit_["attribs"][""]["role"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : credit_["attribs"][""]["scheme"])):
                                        credit_scheme_ = self.sanitize(credit_["attribs"][""]["scheme"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    else:
                                        credit_scheme_ = "urn:ebu"
                                    # end if
                                    if (php_isset(lambda : credit_["data"])):
                                        credit_name_ = self.sanitize(credit_["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    credits_[-1] = self.registry.create("Credit", Array(credit_role_, credit_scheme_, credit_name_))
                                # end for
                                if php_is_array(credits_):
                                    credits_ = php_array_values(array_unique(credits_))
                                # end if
                            else:
                                credits_ = credits_parent_
                            # end if
                            #// DESCRIPTION
                            if (php_isset(lambda : content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["description"])):
                                description_ = self.sanitize(content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["description"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                            elif (php_isset(lambda : group_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["description"])):
                                description_ = self.sanitize(group_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["description"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                            else:
                                description_ = description_parent_
                            # end if
                            #// HASHES
                            if (php_isset(lambda : content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["hash"])):
                                for hash_ in content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["hash"]:
                                    value_ = None
                                    algo_ = None
                                    if (php_isset(lambda : hash_["data"])):
                                        value_ = self.sanitize(hash_["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : hash_["attribs"][""]["algo"])):
                                        algo_ = self.sanitize(hash_["attribs"][""]["algo"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    else:
                                        algo_ = "md5"
                                    # end if
                                    hashes_[-1] = algo_ + ":" + value_
                                # end for
                                if php_is_array(hashes_):
                                    hashes_ = php_array_values(array_unique(hashes_))
                                # end if
                            elif (php_isset(lambda : group_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["hash"])):
                                for hash_ in group_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["hash"]:
                                    value_ = None
                                    algo_ = None
                                    if (php_isset(lambda : hash_["data"])):
                                        value_ = self.sanitize(hash_["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : hash_["attribs"][""]["algo"])):
                                        algo_ = self.sanitize(hash_["attribs"][""]["algo"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    else:
                                        algo_ = "md5"
                                    # end if
                                    hashes_[-1] = algo_ + ":" + value_
                                # end for
                                if php_is_array(hashes_):
                                    hashes_ = php_array_values(array_unique(hashes_))
                                # end if
                            else:
                                hashes_ = hashes_parent_
                            # end if
                            #// KEYWORDS
                            if (php_isset(lambda : content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["keywords"])):
                                if (php_isset(lambda : content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["keywords"][0]["data"])):
                                    temp_ = php_explode(",", self.sanitize(content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["keywords"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT))
                                    for word_ in temp_:
                                        keywords_[-1] = php_trim(word_)
                                    # end for
                                    temp_ = None
                                # end if
                                if php_is_array(keywords_):
                                    keywords_ = php_array_values(array_unique(keywords_))
                                # end if
                            elif (php_isset(lambda : group_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["keywords"])):
                                if (php_isset(lambda : group_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["keywords"][0]["data"])):
                                    temp_ = php_explode(",", self.sanitize(group_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["keywords"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT))
                                    for word_ in temp_:
                                        keywords_[-1] = php_trim(word_)
                                    # end for
                                    temp_ = None
                                # end if
                                if php_is_array(keywords_):
                                    keywords_ = php_array_values(array_unique(keywords_))
                                # end if
                            else:
                                keywords_ = keywords_parent_
                            # end if
                            #// PLAYER
                            if (php_isset(lambda : content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["player"])):
                                player_ = self.sanitize(content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["player"][0]["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_IRI)
                            elif (php_isset(lambda : group_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["player"])):
                                player_ = self.sanitize(group_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["player"][0]["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_IRI)
                            else:
                                player_ = player_parent_
                            # end if
                            #// RATINGS
                            if (php_isset(lambda : content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["rating"])):
                                for rating_ in content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["rating"]:
                                    rating_scheme_ = None
                                    rating_value_ = None
                                    if (php_isset(lambda : rating_["attribs"][""]["scheme"])):
                                        rating_scheme_ = self.sanitize(rating_["attribs"][""]["scheme"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    else:
                                        rating_scheme_ = "urn:simple"
                                    # end if
                                    if (php_isset(lambda : rating_["data"])):
                                        rating_value_ = self.sanitize(rating_["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    ratings_[-1] = self.registry.create("Rating", Array(rating_scheme_, rating_value_))
                                # end for
                                if php_is_array(ratings_):
                                    ratings_ = php_array_values(array_unique(ratings_))
                                # end if
                            elif (php_isset(lambda : group_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["rating"])):
                                for rating_ in group_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["rating"]:
                                    rating_scheme_ = None
                                    rating_value_ = None
                                    if (php_isset(lambda : rating_["attribs"][""]["scheme"])):
                                        rating_scheme_ = self.sanitize(rating_["attribs"][""]["scheme"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    else:
                                        rating_scheme_ = "urn:simple"
                                    # end if
                                    if (php_isset(lambda : rating_["data"])):
                                        rating_value_ = self.sanitize(rating_["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    ratings_[-1] = self.registry.create("Rating", Array(rating_scheme_, rating_value_))
                                # end for
                                if php_is_array(ratings_):
                                    ratings_ = php_array_values(array_unique(ratings_))
                                # end if
                            else:
                                ratings_ = ratings_parent_
                            # end if
                            #// RESTRICTIONS
                            if (php_isset(lambda : content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["restriction"])):
                                for restriction_ in content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["restriction"]:
                                    restriction_relationship_ = None
                                    restriction_type_ = None
                                    restriction_value_ = None
                                    if (php_isset(lambda : restriction_["attribs"][""]["relationship"])):
                                        restriction_relationship_ = self.sanitize(restriction_["attribs"][""]["relationship"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : restriction_["attribs"][""]["type"])):
                                        restriction_type_ = self.sanitize(restriction_["attribs"][""]["type"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : restriction_["data"])):
                                        restriction_value_ = self.sanitize(restriction_["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    restrictions_[-1] = self.registry.create("Restriction", Array(restriction_relationship_, restriction_type_, restriction_value_))
                                # end for
                                if php_is_array(restrictions_):
                                    restrictions_ = php_array_values(array_unique(restrictions_))
                                # end if
                            elif (php_isset(lambda : group_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["restriction"])):
                                for restriction_ in group_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["restriction"]:
                                    restriction_relationship_ = None
                                    restriction_type_ = None
                                    restriction_value_ = None
                                    if (php_isset(lambda : restriction_["attribs"][""]["relationship"])):
                                        restriction_relationship_ = self.sanitize(restriction_["attribs"][""]["relationship"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : restriction_["attribs"][""]["type"])):
                                        restriction_type_ = self.sanitize(restriction_["attribs"][""]["type"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    if (php_isset(lambda : restriction_["data"])):
                                        restriction_value_ = self.sanitize(restriction_["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                    # end if
                                    restrictions_[-1] = self.registry.create("Restriction", Array(restriction_relationship_, restriction_type_, restriction_value_))
                                # end for
                                if php_is_array(restrictions_):
                                    restrictions_ = php_array_values(array_unique(restrictions_))
                                # end if
                            else:
                                restrictions_ = restrictions_parent_
                            # end if
                            #// THUMBNAILS
                            if (php_isset(lambda : content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["thumbnail"])):
                                for thumbnail_ in content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["thumbnail"]:
                                    thumbnails_[-1] = self.sanitize(thumbnail_["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_IRI)
                                # end for
                                if php_is_array(thumbnails_):
                                    thumbnails_ = php_array_values(array_unique(thumbnails_))
                                # end if
                            elif (php_isset(lambda : group_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["thumbnail"])):
                                for thumbnail_ in group_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["thumbnail"]:
                                    thumbnails_[-1] = self.sanitize(thumbnail_["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_IRI)
                                # end for
                                if php_is_array(thumbnails_):
                                    thumbnails_ = php_array_values(array_unique(thumbnails_))
                                # end if
                            else:
                                thumbnails_ = thumbnails_parent_
                            # end if
                            #// TITLES
                            if (php_isset(lambda : content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["title"])):
                                title_ = self.sanitize(content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["title"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                            elif (php_isset(lambda : group_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["title"])):
                                title_ = self.sanitize(group_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["title"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                            else:
                                title_ = title_parent_
                            # end if
                            self.data["enclosures"][-1] = self.registry.create("Enclosure", Array(url_, type_, length_, None, bitrate_, captions_, categories_, channels_, copyrights_, credits_, description_, duration_, expression_, framerate_, hashes_, height_, keywords_, lang_, medium_, player_, ratings_, restrictions_, samplingrate_, thumbnails_, title_, width_))
                        # end if
                    # end for
                # end if
            # end for
            #// If we have standalone media:content tags, loop through them.
            if (php_isset(lambda : self.data["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["content"])):
                for content_ in self.data["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["content"]:
                    if (php_isset(lambda : content_["attribs"][""]["url"])) or (php_isset(lambda : content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["player"])):
                        #// Attributes
                        bitrate_ = None
                        channels_ = None
                        duration_ = None
                        expression_ = None
                        framerate_ = None
                        height_ = None
                        javascript_ = None
                        lang_ = None
                        length_ = None
                        medium_ = None
                        samplingrate_ = None
                        type_ = None
                        url_ = None
                        width_ = None
                        #// Elements
                        captions_ = None
                        categories_ = None
                        copyrights_ = None
                        credits_ = None
                        description_ = None
                        hashes_ = None
                        keywords_ = None
                        player_ = None
                        ratings_ = None
                        restrictions_ = None
                        thumbnails_ = None
                        title_ = None
                        #// Start checking the attributes of media:content
                        if (php_isset(lambda : content_["attribs"][""]["bitrate"])):
                            bitrate_ = self.sanitize(content_["attribs"][""]["bitrate"], SIMPLEPIE_CONSTRUCT_TEXT)
                        # end if
                        if (php_isset(lambda : content_["attribs"][""]["channels"])):
                            channels_ = self.sanitize(content_["attribs"][""]["channels"], SIMPLEPIE_CONSTRUCT_TEXT)
                        # end if
                        if (php_isset(lambda : content_["attribs"][""]["duration"])):
                            duration_ = self.sanitize(content_["attribs"][""]["duration"], SIMPLEPIE_CONSTRUCT_TEXT)
                        else:
                            duration_ = duration_parent_
                        # end if
                        if (php_isset(lambda : content_["attribs"][""]["expression"])):
                            expression_ = self.sanitize(content_["attribs"][""]["expression"], SIMPLEPIE_CONSTRUCT_TEXT)
                        # end if
                        if (php_isset(lambda : content_["attribs"][""]["framerate"])):
                            framerate_ = self.sanitize(content_["attribs"][""]["framerate"], SIMPLEPIE_CONSTRUCT_TEXT)
                        # end if
                        if (php_isset(lambda : content_["attribs"][""]["height"])):
                            height_ = self.sanitize(content_["attribs"][""]["height"], SIMPLEPIE_CONSTRUCT_TEXT)
                        # end if
                        if (php_isset(lambda : content_["attribs"][""]["lang"])):
                            lang_ = self.sanitize(content_["attribs"][""]["lang"], SIMPLEPIE_CONSTRUCT_TEXT)
                        # end if
                        if (php_isset(lambda : content_["attribs"][""]["fileSize"])):
                            length_ = ceil(content_["attribs"][""]["fileSize"])
                        # end if
                        if (php_isset(lambda : content_["attribs"][""]["medium"])):
                            medium_ = self.sanitize(content_["attribs"][""]["medium"], SIMPLEPIE_CONSTRUCT_TEXT)
                        # end if
                        if (php_isset(lambda : content_["attribs"][""]["samplingrate"])):
                            samplingrate_ = self.sanitize(content_["attribs"][""]["samplingrate"], SIMPLEPIE_CONSTRUCT_TEXT)
                        # end if
                        if (php_isset(lambda : content_["attribs"][""]["type"])):
                            type_ = self.sanitize(content_["attribs"][""]["type"], SIMPLEPIE_CONSTRUCT_TEXT)
                        # end if
                        if (php_isset(lambda : content_["attribs"][""]["width"])):
                            width_ = self.sanitize(content_["attribs"][""]["width"], SIMPLEPIE_CONSTRUCT_TEXT)
                        # end if
                        if (php_isset(lambda : content_["attribs"][""]["url"])):
                            url_ = self.sanitize(content_["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_IRI)
                        # end if
                        #// Checking the other optional media: elements. Priority: media:content, media:group, item, channel
                        #// CAPTIONS
                        if (php_isset(lambda : content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["text"])):
                            for caption_ in content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["text"]:
                                caption_type_ = None
                                caption_lang_ = None
                                caption_startTime_ = None
                                caption_endTime_ = None
                                caption_text_ = None
                                if (php_isset(lambda : caption_["attribs"][""]["type"])):
                                    caption_type_ = self.sanitize(caption_["attribs"][""]["type"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                if (php_isset(lambda : caption_["attribs"][""]["lang"])):
                                    caption_lang_ = self.sanitize(caption_["attribs"][""]["lang"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                if (php_isset(lambda : caption_["attribs"][""]["start"])):
                                    caption_startTime_ = self.sanitize(caption_["attribs"][""]["start"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                if (php_isset(lambda : caption_["attribs"][""]["end"])):
                                    caption_endTime_ = self.sanitize(caption_["attribs"][""]["end"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                if (php_isset(lambda : caption_["data"])):
                                    caption_text_ = self.sanitize(caption_["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                captions_[-1] = self.registry.create("Caption", Array(caption_type_, caption_lang_, caption_startTime_, caption_endTime_, caption_text_))
                            # end for
                            if php_is_array(captions_):
                                captions_ = php_array_values(array_unique(captions_))
                            # end if
                        else:
                            captions_ = captions_parent_
                        # end if
                        #// CATEGORIES
                        if (php_isset(lambda : content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["category"])):
                            for category_ in content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["category"]:
                                term_ = None
                                scheme_ = None
                                label_ = None
                                if (php_isset(lambda : category_["data"])):
                                    term_ = self.sanitize(category_["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                if (php_isset(lambda : category_["attribs"][""]["scheme"])):
                                    scheme_ = self.sanitize(category_["attribs"][""]["scheme"], SIMPLEPIE_CONSTRUCT_TEXT)
                                else:
                                    scheme_ = "http://search.yahoo.com/mrss/category_schema"
                                # end if
                                if (php_isset(lambda : category_["attribs"][""]["label"])):
                                    label_ = self.sanitize(category_["attribs"][""]["label"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                categories_[-1] = self.registry.create("Category", Array(term_, scheme_, label_))
                            # end for
                        # end if
                        if php_is_array(categories_) and php_is_array(categories_parent_):
                            categories_ = php_array_values(array_unique(php_array_merge(categories_, categories_parent_)))
                        elif php_is_array(categories_):
                            categories_ = php_array_values(array_unique(categories_))
                        elif php_is_array(categories_parent_):
                            categories_ = php_array_values(array_unique(categories_parent_))
                        else:
                            categories_ = None
                        # end if
                        #// COPYRIGHTS
                        if (php_isset(lambda : content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["copyright"])):
                            copyright_url_ = None
                            copyright_label_ = None
                            if (php_isset(lambda : content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["copyright"][0]["attribs"][""]["url"])):
                                copyright_url_ = self.sanitize(content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["copyright"][0]["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_TEXT)
                            # end if
                            if (php_isset(lambda : content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["copyright"][0]["data"])):
                                copyright_label_ = self.sanitize(content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["copyright"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                            # end if
                            copyrights_ = self.registry.create("Copyright", Array(copyright_url_, copyright_label_))
                        else:
                            copyrights_ = copyrights_parent_
                        # end if
                        #// CREDITS
                        if (php_isset(lambda : content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["credit"])):
                            for credit_ in content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["credit"]:
                                credit_role_ = None
                                credit_scheme_ = None
                                credit_name_ = None
                                if (php_isset(lambda : credit_["attribs"][""]["role"])):
                                    credit_role_ = self.sanitize(credit_["attribs"][""]["role"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                if (php_isset(lambda : credit_["attribs"][""]["scheme"])):
                                    credit_scheme_ = self.sanitize(credit_["attribs"][""]["scheme"], SIMPLEPIE_CONSTRUCT_TEXT)
                                else:
                                    credit_scheme_ = "urn:ebu"
                                # end if
                                if (php_isset(lambda : credit_["data"])):
                                    credit_name_ = self.sanitize(credit_["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                credits_[-1] = self.registry.create("Credit", Array(credit_role_, credit_scheme_, credit_name_))
                            # end for
                            if php_is_array(credits_):
                                credits_ = php_array_values(array_unique(credits_))
                            # end if
                        else:
                            credits_ = credits_parent_
                        # end if
                        #// DESCRIPTION
                        if (php_isset(lambda : content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["description"])):
                            description_ = self.sanitize(content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["description"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                        else:
                            description_ = description_parent_
                        # end if
                        #// HASHES
                        if (php_isset(lambda : content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["hash"])):
                            for hash_ in content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["hash"]:
                                value_ = None
                                algo_ = None
                                if (php_isset(lambda : hash_["data"])):
                                    value_ = self.sanitize(hash_["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                if (php_isset(lambda : hash_["attribs"][""]["algo"])):
                                    algo_ = self.sanitize(hash_["attribs"][""]["algo"], SIMPLEPIE_CONSTRUCT_TEXT)
                                else:
                                    algo_ = "md5"
                                # end if
                                hashes_[-1] = algo_ + ":" + value_
                            # end for
                            if php_is_array(hashes_):
                                hashes_ = php_array_values(array_unique(hashes_))
                            # end if
                        else:
                            hashes_ = hashes_parent_
                        # end if
                        #// KEYWORDS
                        if (php_isset(lambda : content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["keywords"])):
                            if (php_isset(lambda : content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["keywords"][0]["data"])):
                                temp_ = php_explode(",", self.sanitize(content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["keywords"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT))
                                for word_ in temp_:
                                    keywords_[-1] = php_trim(word_)
                                # end for
                                temp_ = None
                            # end if
                            if php_is_array(keywords_):
                                keywords_ = php_array_values(array_unique(keywords_))
                            # end if
                        else:
                            keywords_ = keywords_parent_
                        # end if
                        #// PLAYER
                        if (php_isset(lambda : content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["player"])):
                            player_ = self.sanitize(content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["player"][0]["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_IRI)
                        else:
                            player_ = player_parent_
                        # end if
                        #// RATINGS
                        if (php_isset(lambda : content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["rating"])):
                            for rating_ in content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["rating"]:
                                rating_scheme_ = None
                                rating_value_ = None
                                if (php_isset(lambda : rating_["attribs"][""]["scheme"])):
                                    rating_scheme_ = self.sanitize(rating_["attribs"][""]["scheme"], SIMPLEPIE_CONSTRUCT_TEXT)
                                else:
                                    rating_scheme_ = "urn:simple"
                                # end if
                                if (php_isset(lambda : rating_["data"])):
                                    rating_value_ = self.sanitize(rating_["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                ratings_[-1] = self.registry.create("Rating", Array(rating_scheme_, rating_value_))
                            # end for
                            if php_is_array(ratings_):
                                ratings_ = php_array_values(array_unique(ratings_))
                            # end if
                        else:
                            ratings_ = ratings_parent_
                        # end if
                        #// RESTRICTIONS
                        if (php_isset(lambda : content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["restriction"])):
                            for restriction_ in content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["restriction"]:
                                restriction_relationship_ = None
                                restriction_type_ = None
                                restriction_value_ = None
                                if (php_isset(lambda : restriction_["attribs"][""]["relationship"])):
                                    restriction_relationship_ = self.sanitize(restriction_["attribs"][""]["relationship"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                if (php_isset(lambda : restriction_["attribs"][""]["type"])):
                                    restriction_type_ = self.sanitize(restriction_["attribs"][""]["type"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                if (php_isset(lambda : restriction_["data"])):
                                    restriction_value_ = self.sanitize(restriction_["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                                # end if
                                restrictions_[-1] = self.registry.create("Restriction", Array(restriction_relationship_, restriction_type_, restriction_value_))
                            # end for
                            if php_is_array(restrictions_):
                                restrictions_ = php_array_values(array_unique(restrictions_))
                            # end if
                        else:
                            restrictions_ = restrictions_parent_
                        # end if
                        #// THUMBNAILS
                        if (php_isset(lambda : content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["thumbnail"])):
                            for thumbnail_ in content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["thumbnail"]:
                                thumbnails_[-1] = self.sanitize(thumbnail_["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_IRI)
                            # end for
                            if php_is_array(thumbnails_):
                                thumbnails_ = php_array_values(array_unique(thumbnails_))
                            # end if
                        else:
                            thumbnails_ = thumbnails_parent_
                        # end if
                        #// TITLES
                        if (php_isset(lambda : content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["title"])):
                            title_ = self.sanitize(content_["child"][SIMPLEPIE_NAMESPACE_MEDIARSS]["title"][0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
                        else:
                            title_ = title_parent_
                        # end if
                        self.data["enclosures"][-1] = self.registry.create("Enclosure", Array(url_, type_, length_, None, bitrate_, captions_, categories_, channels_, copyrights_, credits_, description_, duration_, expression_, framerate_, hashes_, height_, keywords_, lang_, medium_, player_, ratings_, restrictions_, samplingrate_, thumbnails_, title_, width_))
                    # end if
                # end for
            # end if
            for link_ in self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "link"):
                if (php_isset(lambda : link_["attribs"][""]["href"])) and (not php_empty(lambda : link_["attribs"][""]["rel"])) and link_["attribs"][""]["rel"] == "enclosure":
                    #// Attributes
                    bitrate_ = None
                    channels_ = None
                    duration_ = None
                    expression_ = None
                    framerate_ = None
                    height_ = None
                    javascript_ = None
                    lang_ = None
                    length_ = None
                    medium_ = None
                    samplingrate_ = None
                    type_ = None
                    url_ = None
                    width_ = None
                    url_ = self.sanitize(link_["attribs"][""]["href"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(link_))
                    if (php_isset(lambda : link_["attribs"][""]["type"])):
                        type_ = self.sanitize(link_["attribs"][""]["type"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : link_["attribs"][""]["length"])):
                        length_ = ceil(link_["attribs"][""]["length"])
                    # end if
                    #// Since we don't have group or content for these, we'll just pass the '*_parent' variables directly to the constructor
                    self.data["enclosures"][-1] = self.registry.create("Enclosure", Array(url_, type_, length_, None, bitrate_, captions_parent_, categories_parent_, channels_, copyrights_parent_, credits_parent_, description_parent_, duration_parent_, expression_, framerate_, hashes_parent_, height_, keywords_parent_, lang_, medium_, player_parent_, ratings_parent_, restrictions_parent_, samplingrate_, thumbnails_parent_, title_parent_, width_))
                # end if
            # end for
            for link_ in self.get_item_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "link"):
                if (php_isset(lambda : link_["attribs"][""]["href"])) and (not php_empty(lambda : link_["attribs"][""]["rel"])) and link_["attribs"][""]["rel"] == "enclosure":
                    #// Attributes
                    bitrate_ = None
                    channels_ = None
                    duration_ = None
                    expression_ = None
                    framerate_ = None
                    height_ = None
                    javascript_ = None
                    lang_ = None
                    length_ = None
                    medium_ = None
                    samplingrate_ = None
                    type_ = None
                    url_ = None
                    width_ = None
                    url_ = self.sanitize(link_["attribs"][""]["href"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(link_))
                    if (php_isset(lambda : link_["attribs"][""]["type"])):
                        type_ = self.sanitize(link_["attribs"][""]["type"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : link_["attribs"][""]["length"])):
                        length_ = ceil(link_["attribs"][""]["length"])
                    # end if
                    #// Since we don't have group or content for these, we'll just pass the '*_parent' variables directly to the constructor
                    self.data["enclosures"][-1] = self.registry.create("Enclosure", Array(url_, type_, length_, None, bitrate_, captions_parent_, categories_parent_, channels_, copyrights_parent_, credits_parent_, description_parent_, duration_parent_, expression_, framerate_, hashes_parent_, height_, keywords_parent_, lang_, medium_, player_parent_, ratings_parent_, restrictions_parent_, samplingrate_, thumbnails_parent_, title_parent_, width_))
                # end if
            # end for
            enclosure_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_RSS_20, "enclosure")
            if enclosure_:
                if (php_isset(lambda : enclosure_[0]["attribs"][""]["url"])):
                    #// Attributes
                    bitrate_ = None
                    channels_ = None
                    duration_ = None
                    expression_ = None
                    framerate_ = None
                    height_ = None
                    javascript_ = None
                    lang_ = None
                    length_ = None
                    medium_ = None
                    samplingrate_ = None
                    type_ = None
                    url_ = None
                    width_ = None
                    url_ = self.sanitize(enclosure_[0]["attribs"][""]["url"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(enclosure_[0]))
                    if (php_isset(lambda : enclosure_[0]["attribs"][""]["type"])):
                        type_ = self.sanitize(enclosure_[0]["attribs"][""]["type"], SIMPLEPIE_CONSTRUCT_TEXT)
                    # end if
                    if (php_isset(lambda : enclosure_[0]["attribs"][""]["length"])):
                        length_ = ceil(enclosure_[0]["attribs"][""]["length"])
                    # end if
                    #// Since we don't have group or content for these, we'll just pass the '*_parent' variables directly to the constructor
                    self.data["enclosures"][-1] = self.registry.create("Enclosure", Array(url_, type_, length_, None, bitrate_, captions_parent_, categories_parent_, channels_, copyrights_parent_, credits_parent_, description_parent_, duration_parent_, expression_, framerate_, hashes_parent_, height_, keywords_parent_, lang_, medium_, player_parent_, ratings_parent_, restrictions_parent_, samplingrate_, thumbnails_parent_, title_parent_, width_))
                # end if
            # end if
            if sizeof(self.data["enclosures"]) == 0 and url_ or type_ or length_ or bitrate_ or captions_parent_ or categories_parent_ or channels_ or copyrights_parent_ or credits_parent_ or description_parent_ or duration_parent_ or expression_ or framerate_ or hashes_parent_ or height_ or keywords_parent_ or lang_ or medium_ or player_parent_ or ratings_parent_ or restrictions_parent_ or samplingrate_ or thumbnails_parent_ or title_parent_ or width_:
                #// Since we don't have group or content for these, we'll just pass the '*_parent' variables directly to the constructor
                self.data["enclosures"][-1] = self.registry.create("Enclosure", Array(url_, type_, length_, None, bitrate_, captions_parent_, categories_parent_, channels_, copyrights_parent_, credits_parent_, description_parent_, duration_parent_, expression_, framerate_, hashes_parent_, height_, keywords_parent_, lang_, medium_, player_parent_, ratings_parent_, restrictions_parent_, samplingrate_, thumbnails_parent_, title_parent_, width_))
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
            return php_float(return_[0]["data"])
        elif self.get_item_tags(SIMPLEPIE_NAMESPACE_GEORSS, "point") and php_preg_match("/^((?:-)?[0-9]+(?:\\.[0-9]+)) ((?:-)?[0-9]+(?:\\.[0-9]+))$/", php_trim(return_[0]["data"]), match_):
            return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_GEORSS, "point")
            return php_float(match_[1])
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
            return php_float(return_[0]["data"])
        elif self.get_item_tags(SIMPLEPIE_NAMESPACE_W3C_BASIC_GEO, "lon"):
            return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_W3C_BASIC_GEO, "lon")
            return php_float(return_[0]["data"])
        elif self.get_item_tags(SIMPLEPIE_NAMESPACE_GEORSS, "point") and php_preg_match("/^((?:-)?[0-9]+(?:\\.[0-9]+)) ((?:-)?[0-9]+(?:\\.[0-9]+))$/", php_trim(return_[0]["data"]), match_):
            return_ = self.get_item_tags(SIMPLEPIE_NAMESPACE_GEORSS, "point")
            return php_float(match_[2])
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
