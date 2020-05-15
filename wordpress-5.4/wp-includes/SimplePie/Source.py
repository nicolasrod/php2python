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
    def __init__(self, item=None, data=None):
        
        self.item = item
        self.data = data
    # end def __init__
    def set_registry(self, registry=None):
        
        self.registry = registry
    # end def set_registry
    def __tostring(self):
        
        return php_md5(serialize(self.data))
    # end def __tostring
    def get_source_tags(self, namespace=None, tag=None):
        
        if (php_isset(lambda : self.data["child"][namespace][tag])):
            return self.data["child"][namespace][tag]
        else:
            return None
        # end if
    # end def get_source_tags
    def get_base(self, element=Array()):
        
        return self.item.get_base(element)
    # end def get_base
    def sanitize(self, data=None, type=None, base=""):
        
        return self.item.sanitize(data, type, base)
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
    def get_category(self, key=0):
        
        categories = self.get_categories()
        if (php_isset(lambda : categories[key])):
            return categories[key]
        else:
            return None
        # end if
    # end def get_category
    def get_categories(self):
        
        categories = Array()
        for category in self.get_source_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "category"):
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
        for category in self.get_source_tags(SIMPLEPIE_NAMESPACE_RSS_20, "category"):
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
        for category in self.get_source_tags(SIMPLEPIE_NAMESPACE_DC_11, "subject"):
            categories[-1] = self.registry.create("Category", Array(self.sanitize(category["data"], SIMPLEPIE_CONSTRUCT_TEXT), None, None))
        # end for
        for category in self.get_source_tags(SIMPLEPIE_NAMESPACE_DC_10, "subject"):
            categories[-1] = self.registry.create("Category", Array(self.sanitize(category["data"], SIMPLEPIE_CONSTRUCT_TEXT), None, None))
        # end for
        if (not php_empty(lambda : categories)):
            return array_unique(categories)
        else:
            return None
        # end if
    # end def get_categories
    def get_author(self, key=0):
        
        authors = self.get_authors()
        if (php_isset(lambda : authors[key])):
            return authors[key]
        else:
            return None
        # end if
    # end def get_author
    def get_authors(self):
        
        authors = Array()
        for author in self.get_source_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "author"):
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
        author = self.get_source_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "author")
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
        for author in self.get_source_tags(SIMPLEPIE_NAMESPACE_DC_11, "creator"):
            authors[-1] = self.registry.create("Author", Array(self.sanitize(author["data"], SIMPLEPIE_CONSTRUCT_TEXT), None, None))
        # end for
        for author in self.get_source_tags(SIMPLEPIE_NAMESPACE_DC_10, "creator"):
            authors[-1] = self.registry.create("Author", Array(self.sanitize(author["data"], SIMPLEPIE_CONSTRUCT_TEXT), None, None))
        # end for
        for author in self.get_source_tags(SIMPLEPIE_NAMESPACE_ITUNES, "author"):
            authors[-1] = self.registry.create("Author", Array(self.sanitize(author["data"], SIMPLEPIE_CONSTRUCT_TEXT), None, None))
        # end for
        if (not php_empty(lambda : authors)):
            return array_unique(authors)
        else:
            return None
        # end if
    # end def get_authors
    def get_contributor(self, key=0):
        
        contributors = self.get_contributors()
        if (php_isset(lambda : contributors[key])):
            return contributors[key]
        else:
            return None
        # end if
    # end def get_contributor
    def get_contributors(self):
        
        contributors = Array()
        for contributor in self.get_source_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "contributor"):
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
        for contributor in self.get_source_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "contributor"):
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
    def get_link(self, key=0, rel="alternate"):
        
        links = self.get_links(rel)
        if (php_isset(lambda : links[key])):
            return links[key]
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
    def get_links(self, rel="alternate"):
        
        if (not (php_isset(lambda : self.data["links"]))):
            self.data["links"] = Array()
            links = self.get_source_tags(SIMPLEPIE_NAMESPACE_ATOM_10, "link")
            if links:
                for link in links:
                    if (php_isset(lambda : link["attribs"][""]["href"])):
                        link_rel = link["attribs"][""]["rel"] if (php_isset(lambda : link["attribs"][""]["rel"])) else "alternate"
                        self.data["links"][link_rel][-1] = self.sanitize(link["attribs"][""]["href"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(link))
                    # end if
                # end for
            # end if
            links = self.get_source_tags(SIMPLEPIE_NAMESPACE_ATOM_03, "link")
            if links:
                for link in links:
                    if (php_isset(lambda : link["attribs"][""]["href"])):
                        link_rel = link["attribs"][""]["rel"] if (php_isset(lambda : link["attribs"][""]["rel"])) else "alternate"
                        self.data["links"][link_rel][-1] = self.sanitize(link["attribs"][""]["href"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(link))
                    # end if
                # end for
            # end if
            links = self.get_source_tags(SIMPLEPIE_NAMESPACE_RSS_10, "link")
            if links:
                self.data["links"]["alternate"][-1] = self.sanitize(links[0]["data"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(links[0]))
            # end if
            links = self.get_source_tags(SIMPLEPIE_NAMESPACE_RSS_090, "link")
            if links:
                self.data["links"]["alternate"][-1] = self.sanitize(links[0]["data"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(links[0]))
            # end if
            links = self.get_source_tags(SIMPLEPIE_NAMESPACE_RSS_20, "link")
            if links:
                self.data["links"]["alternate"][-1] = self.sanitize(links[0]["data"], SIMPLEPIE_CONSTRUCT_IRI, self.get_base(links[0]))
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
            return float(return_[0]["data"])
        elif self.get_source_tags(SIMPLEPIE_NAMESPACE_GEORSS, "point") and php_preg_match("/^((?:-)?[0-9]+(?:\\.[0-9]+)) ((?:-)?[0-9]+(?:\\.[0-9]+))$/", php_trim(return_[0]["data"]), match):
            return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_GEORSS, "point")
            return float(match[1])
        else:
            return None
        # end if
    # end def get_latitude
    def get_longitude(self):
        
        return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_W3C_BASIC_GEO, "long")
        if return_:
            return float(return_[0]["data"])
        elif self.get_source_tags(SIMPLEPIE_NAMESPACE_W3C_BASIC_GEO, "lon"):
            return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_W3C_BASIC_GEO, "lon")
            return float(return_[0]["data"])
        elif self.get_source_tags(SIMPLEPIE_NAMESPACE_GEORSS, "point") and php_preg_match("/^((?:-)?[0-9]+(?:\\.[0-9]+)) ((?:-)?[0-9]+(?:\\.[0-9]+))$/", php_trim(return_[0]["data"]), match):
            return_ = self.get_source_tags(SIMPLEPIE_NAMESPACE_GEORSS, "point")
            return float(match[2])
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
