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
#// Handles `<atom:source>`
#// 
#// Used by {@see SimplePie_Item::get_source()}
#// 
#// This class can be overloaded with {@see SimplePie::set_source_class()}
#// 
#// @package SimplePie
#// @subpackage API
#//
class SimplePie_Source():
    item = Array()
    data = Array()
    registry = Array()
    def __init__(self, item_=None, data_=None):
        
        
        self.item = item_
        self.data = data_
    # end def __init__
    def set_registry(self, registry_=None):
        
        
        self.registry = registry_
    # end def set_registry
    def __tostring(self):
        
        
        return php_md5(serialize(self.data))
    # end def __tostring
    def get_source_tags(self, namespace_=None, tag_=None):
        
        
        if (php_isset(lambda : self.data["child"][namespace_][tag_])):
            return self.data["child"][namespace_][tag_]
        else:
            return None
        # end if
    # end def get_source_tags
    def get_base(self, element_=None):
        if element_ is None:
            element_ = Array()
        # end if
        
        return self.item.get_base(element_)
    # end def get_base
    def sanitize(self, data_=None, type_=None, base_=""):
        
        
        return self.item.sanitize(data_, type_, base_)
    # end def sanitize
    def get_item(self):
        
        
        return self.item
    # end def get_item
    def get_title(self):
        
        
        return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "title")
        if return_:
            return self.sanitize(return_[0]["data"], self.registry.call("Misc", "atom_10_construct_type", Array(return_[0]["attribs"])), self.get_base(return_[0]))
        elif self.get_source_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "title"):
            return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "title")
            return self.sanitize(return_[0]["data"], self.registry.call("Misc", "atom_03_construct_type", Array(return_[0]["attribs"])), self.get_base(return_[0]))
        elif self.get_source_tags(SIMPLEPIE_NAMESPACE_RSS_10, "title"):
            return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_RSS_10, "title")
            return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_MAYBE_HTML, self.get_base(return_[0]))
        elif self.get_source_tags(SIMPLEPIE_NAMESPACE_RSS_090, "title"):
            return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_RSS_090, "title")
            return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_MAYBE_HTML, self.get_base(return_[0]))
        elif self.get_source_tags(SIMPLEPIE_NAMESPACE_RSS_20, "title"):
            return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_RSS_20, "title")
            return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_MAYBE_HTML, self.get_base(return_[0]))
        elif self.get_source_tags(SIMPLEPIE_NAMESPACE_DC_11, "title"):
            return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_DC_11, "title")
            return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
        elif self.get_source_tags(SIMPLEPIE_NAMESPACE_DC_10, "title"):
            return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_DC_10, "title")
            return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
        else:
            return None
        # end if
    # end def get_title
    def get_category(self, key_=0):
        
        
        categories_ = self.get_categories()
        if (php_isset(lambda : categories_[key_])):
            return categories_[key_]
        else:
            return None
        # end if
    # end def get_category
    def get_categories(self):
        
        
        categories_ = Array()
        for category_ in self.get_source_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "category"):
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
        for category_ in self.get_source_tags(SIMPLEPIE_NAMESPACE_RSS_20, "category"):
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
        for category_ in self.get_source_tags(SIMPLEPIE_NAMESPACE_DC_11, "subject"):
            categories_[-1] = self.registry.create("Category", Array(self.sanitize(category_["data"], SIMPLEPIE_CONSTRUCT_TEXT), None, None))
        # end for
        for category_ in self.get_source_tags(SIMPLEPIE_NAMESPACE_DC_10, "subject"):
            categories_[-1] = self.registry.create("Category", Array(self.sanitize(category_["data"], SIMPLEPIE_CONSTRUCT_TEXT), None, None))
        # end for
        if (not php_empty(lambda : categories_)):
            return array_unique(categories_)
        else:
            return None
        # end if
    # end def get_categories
    def get_author(self, key_=0):
        
        
        authors_ = self.get_authors()
        if (php_isset(lambda : authors_[key_])):
            return authors_[key_]
        else:
            return None
        # end if
    # end def get_author
    def get_authors(self):
        
        
        authors_ = Array()
        for author_ in self.get_source_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "author"):
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
        author_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "author")
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
        for author_ in self.get_source_tags(SIMPLEPIE_NAMESPACE_DC_11, "creator"):
            authors_[-1] = self.registry.create("Author", Array(self.sanitize(author_["data"], SIMPLEPIE_CONSTRUCT_TEXT), None, None))
        # end for
        for author_ in self.get_source_tags(SIMPLEPIE_NAMESPACE_DC_10, "creator"):
            authors_[-1] = self.registry.create("Author", Array(self.sanitize(author_["data"], SIMPLEPIE_CONSTRUCT_TEXT), None, None))
        # end for
        for author_ in self.get_source_tags(SIMPLEPIE_NAMESPACE_ITUNES, "author"):
            authors_[-1] = self.registry.create("Author", Array(self.sanitize(author_["data"], SIMPLEPIE_CONSTRUCT_TEXT), None, None))
        # end for
        if (not php_empty(lambda : authors_)):
            return array_unique(authors_)
        else:
            return None
        # end if
    # end def get_authors
    def get_contributor(self, key_=0):
        
        
        contributors_ = self.get_contributors()
        if (php_isset(lambda : contributors_[key_])):
            return contributors_[key_]
        else:
            return None
        # end if
    # end def get_contributor
    def get_contributors(self):
        
        
        contributors_ = Array()
        for contributor_ in self.get_source_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "contributor"):
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
        for contributor_ in self.get_source_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "contributor"):
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
    def get_link(self, key_=0, rel_="alternate"):
        
        
        links_ = self.get_links(rel_)
        if (php_isset(lambda : links_[key_])):
            return links_[key_]
        else:
            return None
        # end if
    # end def get_link
    #// 
    #// Added for parity between the parent-level and the item/entry-level.
    #//
    def get_permalink(self):
        
        
        return self.get_link(0)
    # end def get_permalink
    def get_links(self, rel_="alternate"):
        
        
        if (not (php_isset(lambda : self.data["links"]))):
            self.data["links"] = Array()
            links_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "link")
            if links_:
                for link_ in links_:
                    if (php_isset(lambda : link_["attribs"][""]["href"])):
                        link_rel_ = link_["attribs"][""]["rel"] if (php_isset(lambda : link_["attribs"][""]["rel"])) else "alternate"
                        self.data["links"][link_rel_][-1] = self.sanitize(link_["attribs"][""]["href"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(link_))
                    # end if
                # end for
            # end if
            links_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "link")
            if links_:
                for link_ in links_:
                    if (php_isset(lambda : link_["attribs"][""]["href"])):
                        link_rel_ = link_["attribs"][""]["rel"] if (php_isset(lambda : link_["attribs"][""]["rel"])) else "alternate"
                        self.data["links"][link_rel_][-1] = self.sanitize(link_["attribs"][""]["href"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(link_))
                    # end if
                # end for
            # end if
            links_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_RSS_10, "link")
            if links_:
                self.data["links"]["alternate"][-1] = self.sanitize(links_[0]["data"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(links_[0]))
            # end if
            links_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_RSS_090, "link")
            if links_:
                self.data["links"]["alternate"][-1] = self.sanitize(links_[0]["data"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(links_[0]))
            # end if
            links_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_RSS_20, "link")
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
    def get_description(self):
        
        
        return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "subtitle")
        if return_:
            return self.sanitize(return_[0]["data"], self.registry.call("Misc", "atom_10_construct_type", Array(return_[0]["attribs"])), self.get_base(return_[0]))
        elif self.get_source_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "tagline"):
            return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "tagline")
            return self.sanitize(return_[0]["data"], self.registry.call("Misc", "atom_03_construct_type", Array(return_[0]["attribs"])), self.get_base(return_[0]))
        elif self.get_source_tags(SIMPLEPIE_NAMESPACE_RSS_10, "description"):
            return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_RSS_10, "description")
            return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_MAYBE_HTML, self.get_base(return_[0]))
        elif self.get_source_tags(SIMPLEPIE_NAMESPACE_RSS_090, "description"):
            return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_RSS_090, "description")
            return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_MAYBE_HTML, self.get_base(return_[0]))
        elif self.get_source_tags(SIMPLEPIE_NAMESPACE_RSS_20, "description"):
            return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_RSS_20, "description")
            return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_MAYBE_HTML, self.get_base(return_[0]))
        elif self.get_source_tags(SIMPLEPIE_NAMESPACE_DC_11, "description"):
            return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_DC_11, "description")
            return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
        elif self.get_source_tags(SIMPLEPIE_NAMESPACE_DC_10, "description"):
            return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_DC_10, "description")
            return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
        elif self.get_source_tags(SIMPLEPIE_NAMESPACE_ITUNES, "summary"):
            return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_ITUNES, "summary")
            return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_HTML, self.get_base(return_[0]))
        elif self.get_source_tags(SIMPLEPIE_NAMESPACE_ITUNES, "subtitle"):
            return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_ITUNES, "subtitle")
            return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_HTML, self.get_base(return_[0]))
        else:
            return None
        # end if
    # end def get_description
    def get_copyright(self):
        
        
        return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "rights")
        if return_:
            return self.sanitize(return_[0]["data"], self.registry.call("Misc", "atom_10_construct_type", Array(return_[0]["attribs"])), self.get_base(return_[0]))
        elif self.get_source_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "copyright"):
            return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "copyright")
            return self.sanitize(return_[0]["data"], self.registry.call("Misc", "atom_03_construct_type", Array(return_[0]["attribs"])), self.get_base(return_[0]))
        elif self.get_source_tags(SIMPLEPIE_NAMESPACE_RSS_20, "copyright"):
            return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_RSS_20, "copyright")
            return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
        elif self.get_source_tags(SIMPLEPIE_NAMESPACE_DC_11, "rights"):
            return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_DC_11, "rights")
            return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
        elif self.get_source_tags(SIMPLEPIE_NAMESPACE_DC_10, "rights"):
            return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_DC_10, "rights")
            return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
        else:
            return None
        # end if
    # end def get_copyright
    def get_language(self):
        
        
        return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_RSS_20, "language")
        if return_:
            return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
        elif self.get_source_tags(SIMPLEPIE_NAMESPACE_DC_11, "language"):
            return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_DC_11, "language")
            return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
        elif self.get_source_tags(SIMPLEPIE_NAMESPACE_DC_10, "language"):
            return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_DC_10, "language")
            return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_TEXT)
        elif (php_isset(lambda : self.data["xml_lang"])):
            return self.sanitize(self.data["xml_lang"], SIMPLEPIE_CONSTRUCT_TEXT)
        else:
            return None
        # end if
    # end def get_language
    def get_latitude(self):
        
        
        return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_W3C_BASIC_GEO, "lat")
        if return_:
            return php_float(return_[0]["data"])
        elif self.get_source_tags(SIMPLEPIE_NAMESPACE_GEORSS, "point") and php_preg_match("/^((?:-)?[0-9]+(?:\\.[0-9]+)) ((?:-)?[0-9]+(?:\\.[0-9]+))$/", php_trim(return_[0]["data"]), match_):
            return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_GEORSS, "point")
            return php_float(match_[1])
        else:
            return None
        # end if
    # end def get_latitude
    def get_longitude(self):
        
        
        return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_W3C_BASIC_GEO, "long")
        if return_:
            return php_float(return_[0]["data"])
        elif self.get_source_tags(SIMPLEPIE_NAMESPACE_W3C_BASIC_GEO, "lon"):
            return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_W3C_BASIC_GEO, "lon")
            return php_float(return_[0]["data"])
        elif self.get_source_tags(SIMPLEPIE_NAMESPACE_GEORSS, "point") and php_preg_match("/^((?:-)?[0-9]+(?:\\.[0-9]+)) ((?:-)?[0-9]+(?:\\.[0-9]+))$/", php_trim(return_[0]["data"]), match_):
            return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_GEORSS, "point")
            return php_float(match_[2])
        else:
            return None
        # end if
    # end def get_longitude
    def get_image_url(self):
        
        
        return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_ITUNES, "image")
        if return_:
            return self.sanitize(return_[0]["attribs"][""]["href"], SIMPLEPIE_CONSTRUCT_IRI)
        elif self.get_source_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "logo"):
            return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "logo")
            return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(return_[0]))
        elif self.get_source_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "icon"):
            return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "icon")
            return self.sanitize(return_[0]["data"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(return_[0]))
        else:
            return None
        # end if
    # end def get_image_url
# end class SimplePie_Source
