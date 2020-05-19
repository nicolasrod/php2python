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
#// Used for data cleanup and post-processing
#// 
#// 
#// This class can be overloaded with {@see SimplePie::set_sanitize_class()}
#// 
#// @package SimplePie
#// @todo Move to using an actual HTML parser (this will allow tags to be properly stripped, and to switch between HTML and XHTML), this will also make it easier to shorten a string while preserving HTML tags
#//
class SimplePie_Sanitize():
    #// Private vars
    base = Array()
    #// Options
    remove_div = True
    image_handler = ""
    strip_htmltags = Array("base", "blink", "body", "doctype", "embed", "font", "form", "frame", "frameset", "html", "iframe", "input", "marquee", "meta", "noscript", "object", "param", "script", "style")
    encode_instead_of_strip = False
    strip_attributes = Array("bgsound", "class", "expr", "id", "style", "onclick", "onerror", "onfinish", "onmouseover", "onmouseout", "onfocus", "onblur", "lowsrc", "dynsrc")
    strip_comments = False
    output_encoding = "UTF-8"
    enable_cache = True
    cache_location = "./cache"
    cache_name_function = "md5"
    timeout = 10
    useragent = ""
    force_fsockopen = False
    replace_url_attributes = None
    def __init__(self):
        
        
        #// Set defaults
        self.set_url_replacements(None)
    # end def __init__
    def remove_div(self, enable_=None):
        if enable_ is None:
            enable_ = True
        # end if
        
        self.remove_div = php_bool(enable_)
    # end def remove_div
    def set_image_handler(self, page_=None):
        if page_ is None:
            page_ = False
        # end if
        
        if page_:
            self.image_handler = php_str(page_)
        else:
            self.image_handler = False
        # end if
    # end def set_image_handler
    def set_registry(self, registry_=None):
        
        
        self.registry = registry_
    # end def set_registry
    def pass_cache_data(self, enable_cache_=None, cache_location_="./cache", cache_name_function_="md5", cache_class_="SimplePie_Cache"):
        if enable_cache_ is None:
            enable_cache_ = True
        # end if
        
        if (php_isset(lambda : enable_cache_)):
            self.enable_cache = php_bool(enable_cache_)
        # end if
        if cache_location_:
            self.cache_location = php_str(cache_location_)
        # end if
        if cache_name_function_:
            self.cache_name_function = php_str(cache_name_function_)
        # end if
    # end def pass_cache_data
    def pass_file_data(self, file_class_="SimplePie_File", timeout_=10, useragent_="", force_fsockopen_=None):
        if force_fsockopen_ is None:
            force_fsockopen_ = False
        # end if
        
        if timeout_:
            self.timeout = php_str(timeout_)
        # end if
        if useragent_:
            self.useragent = php_str(useragent_)
        # end if
        if force_fsockopen_:
            self.force_fsockopen = php_str(force_fsockopen_)
        # end if
    # end def pass_file_data
    def strip_htmltags(self, tags_=None):
        if tags_ is None:
            tags_ = Array("base", "blink", "body", "doctype", "embed", "font", "form", "frame", "frameset", "html", "iframe", "input", "marquee", "meta", "noscript", "object", "param", "script", "style")
        # end if
        
        if tags_:
            if php_is_array(tags_):
                self.strip_htmltags = tags_
            else:
                self.strip_htmltags = php_explode(",", tags_)
            # end if
        else:
            self.strip_htmltags = False
        # end if
    # end def strip_htmltags
    def encode_instead_of_strip(self, encode_=None):
        if encode_ is None:
            encode_ = False
        # end if
        
        self.encode_instead_of_strip = php_bool(encode_)
    # end def encode_instead_of_strip
    def strip_attributes(self, attribs_=None):
        if attribs_ is None:
            attribs_ = Array("bgsound", "class", "expr", "id", "style", "onclick", "onerror", "onfinish", "onmouseover", "onmouseout", "onfocus", "onblur", "lowsrc", "dynsrc")
        # end if
        
        if attribs_:
            if php_is_array(attribs_):
                self.strip_attributes = attribs_
            else:
                self.strip_attributes = php_explode(",", attribs_)
            # end if
        else:
            self.strip_attributes = False
        # end if
    # end def strip_attributes
    def strip_comments(self, strip_=None):
        if strip_ is None:
            strip_ = False
        # end if
        
        self.strip_comments = php_bool(strip_)
    # end def strip_comments
    def set_output_encoding(self, encoding_="UTF-8"):
        
        
        self.output_encoding = php_str(encoding_)
    # end def set_output_encoding
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
        if element_attribute_ is None:
            element_attribute_ = None
        # end if
        
        if element_attribute_ == None:
            element_attribute_ = Array({"a": "href", "area": "href", "blockquote": "cite", "del": "cite", "form": "action", "img": Array("longdesc", "src"), "input": "src", "ins": "cite", "q": "cite"})
        # end if
        self.replace_url_attributes = element_attribute_
    # end def set_url_replacements
    def sanitize(self, data_=None, type_=None, base_=""):
        
        
        data_ = php_trim(data_)
        if data_ != "" or type_ & SIMPLEPIE_CONSTRUCT_IRI:
            if type_ & SIMPLEPIE_CONSTRUCT_MAYBE_HTML:
                if php_preg_match("/(&(#(x[0-9a-fA-F]+|[0-9]+)|[a-zA-Z0-9]+)|<\\/[A-Za-z][^\\x09\\x0A\\x0B\\x0C\\x0D\\x20\\x2F\\x3E]*" + SIMPLEPIE_PCRE_HTML_ATTRIBUTE + ">)/", data_):
                    type_ |= SIMPLEPIE_CONSTRUCT_HTML
                else:
                    type_ |= SIMPLEPIE_CONSTRUCT_TEXT
                # end if
            # end if
            if type_ & SIMPLEPIE_CONSTRUCT_BASE64:
                data_ = php_base64_decode(data_)
            # end if
            if type_ & SIMPLEPIE_CONSTRUCT_HTML | SIMPLEPIE_CONSTRUCT_XHTML:
                if (not php_class_exists("DOMDocument")):
                    self.registry.call("Misc", "error", Array("DOMDocument not found, unable to use sanitizer", E_USER_WARNING, __FILE__, inspect.currentframe().f_lineno))
                    return ""
                # end if
                document_ = php_new_class("DOMDocument", lambda : DOMDocument())
                document_.encoding = "UTF-8"
                data_ = self.preprocess(data_, type_)
                set_error_handler(Array("SimplePie_Misc", "silence_errors"))
                document_.loadhtml(data_)
                restore_error_handler()
                #// Strip comments
                if self.strip_comments:
                    xpath_ = php_new_class("DOMXPath", lambda : DOMXPath(document_))
                    comments_ = xpath_.query("//comment()")
                    for comment_ in comments_:
                        comment_.parentNode.removechild(comment_)
                    # end for
                # end if
                #// Strip out HTML tags and attributes that might cause various security problems.
                #// Based on recommendations by Mark Pilgrim at:
                #// http://diveintomark.org/archives/2003/06/12/how_to_consume_rss_safely
                if self.strip_htmltags:
                    for tag_ in self.strip_htmltags:
                        self.strip_tag(tag_, document_, type_)
                    # end for
                # end if
                if self.strip_attributes:
                    for attrib_ in self.strip_attributes:
                        self.strip_attr(attrib_, document_)
                    # end for
                # end if
                #// Replace relative URLs
                self.base = base_
                for element_,attributes_ in self.replace_url_attributes.items():
                    self.replace_urls(document_, element_, attributes_)
                # end for
                #// If image handling (caching, etc.) is enabled, cache and rewrite all the image tags.
                if (php_isset(lambda : self.image_handler)) and php_str(self.image_handler) != "" and self.enable_cache:
                    images_ = document_.getelementsbytagname("img")
                    for img_ in images_:
                        if img_.hasattribute("src"):
                            image_url_ = php_call_user_func(self.cache_name_function, img_.getattribute("src"))
                            cache_ = self.registry.call("Cache", "get_handler", Array(self.cache_location, image_url_, "spi"))
                            if cache_.load():
                                img_.setattribute("src", self.image_handler + image_url_)
                            else:
                                file_ = self.registry.create("File", Array(img_.getattribute("src"), self.timeout, 5, Array({"X-FORWARDED-FOR": PHP_SERVER["REMOTE_ADDR"]}), self.useragent, self.force_fsockopen))
                                headers_ = file_.headers
                                if file_.success and file_.method & SIMPLEPIE_FILE_SOURCE_REMOTE == 0 or file_.status_code == 200 or file_.status_code > 206 and file_.status_code < 300:
                                    if cache_.save(Array({"headers": file_.headers, "body": file_.body})):
                                        img_.setattribute("src", self.image_handler + image_url_)
                                    else:
                                        trigger_error(str(self.cache_location) + str(" is not writeable. Make sure you've set the correct relative or absolute path, and that the location is server-writable."), E_USER_WARNING)
                                    # end if
                                # end if
                            # end if
                        # end if
                    # end for
                # end if
                #// Remove the DOCTYPE
                #// Seems to cause segfaulting if we don't do this
                if type(document_.firstChild).__name__ == "DOMDocumentType":
                    document_.removechild(document_.firstChild)
                # end if
                #// Move everything from the body to the root
                real_body_ = document_.getelementsbytagname("body").item(0).childNodes.item(0)
                document_.replacechild(real_body_, document_.firstChild)
                #// Finally, convert to a HTML string
                data_ = php_trim(document_.savehtml())
                if self.remove_div:
                    data_ = php_preg_replace("/^<div" + SIMPLEPIE_PCRE_XML_ATTRIBUTE + ">/", "", data_)
                    data_ = php_preg_replace("/<\\/div>$/", "", data_)
                else:
                    data_ = php_preg_replace("/^<div" + SIMPLEPIE_PCRE_XML_ATTRIBUTE + ">/", "<div>", data_)
                # end if
            # end if
            if type_ & SIMPLEPIE_CONSTRUCT_IRI:
                absolute_ = self.registry.call("Misc", "absolutize_url", Array(data_, base_))
                if absolute_ != False:
                    data_ = absolute_
                # end if
            # end if
            if type_ & SIMPLEPIE_CONSTRUCT_TEXT | SIMPLEPIE_CONSTRUCT_IRI:
                data_ = php_htmlspecialchars(data_, ENT_COMPAT, "UTF-8")
            # end if
            if self.output_encoding != "UTF-8":
                data_ = self.registry.call("Misc", "change_encoding", Array(data_, "UTF-8", self.output_encoding))
            # end if
        # end if
        return data_
    # end def sanitize
    def preprocess(self, html_=None, type_=None):
        
        
        ret_ = ""
        if type_ & (1 << (SIMPLEPIE_CONSTRUCT_XHTML).bit_length()) - 1 - SIMPLEPIE_CONSTRUCT_XHTML:
            #// Atom XHTML constructs are wrapped with a div by default
            #// Note: No protection if $html contains a stray </div>!
            html_ = "<div>" + html_ + "</div>"
            ret_ += "<!DOCTYPE html>"
            content_type_ = "text/html"
        else:
            ret_ += "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">"
            content_type_ = "application/xhtml+xml"
        # end if
        ret_ += "<html><head>"
        ret_ += "<meta http-equiv=\"Content-Type\" content=\"" + content_type_ + "; charset=utf-8\" />"
        ret_ += "</head><body>" + html_ + "</body></html>"
        return ret_
    # end def preprocess
    def replace_urls(self, document_=None, tag_=None, attributes_=None):
        
        
        if (not php_is_array(attributes_)):
            attributes_ = Array(attributes_)
        # end if
        if (not php_is_array(self.strip_htmltags)) or (not php_in_array(tag_, self.strip_htmltags)):
            elements_ = document_.getelementsbytagname(tag_)
            for element_ in elements_:
                for attribute_ in attributes_:
                    if element_.hasattribute(attribute_):
                        value_ = self.registry.call("Misc", "absolutize_url", Array(element_.getattribute(attribute_), self.base))
                        if value_ != False:
                            element_.setattribute(attribute_, value_)
                        # end if
                    # end if
                # end for
            # end for
        # end if
    # end def replace_urls
    def do_strip_htmltags(self, match_=None):
        
        
        if self.encode_instead_of_strip:
            if (php_isset(lambda : match_[4])) and (not php_in_array(php_strtolower(match_[1]), Array("script", "style"))):
                match_[1] = php_htmlspecialchars(match_[1], ENT_COMPAT, "UTF-8")
                match_[2] = php_htmlspecialchars(match_[2], ENT_COMPAT, "UTF-8")
                return str("&lt;") + str(match_[1]) + str(match_[2]) + str("&gt;") + str(match_[3]) + str("&lt;/") + str(match_[1]) + str("&gt;")
            else:
                return php_htmlspecialchars(match_[0], ENT_COMPAT, "UTF-8")
            # end if
        elif (php_isset(lambda : match_[4])) and (not php_in_array(php_strtolower(match_[1]), Array("script", "style"))):
            return match_[4]
        else:
            return ""
        # end if
    # end def do_strip_htmltags
    def strip_tag(self, tag_=None, document_=None, type_=None):
        
        
        xpath_ = php_new_class("DOMXPath", lambda : DOMXPath(document_))
        elements_ = xpath_.query("body//" + tag_)
        if self.encode_instead_of_strip:
            for element_ in elements_:
                fragment_ = document_.createdocumentfragment()
                #// For elements which aren't script or style, include the tag itself
                if (not php_in_array(tag_, Array("script", "style"))):
                    text_ = "<" + tag_
                    if element_.hasattributes():
                        attrs_ = Array()
                        for name_,attr_ in element_.attributes.items():
                            value_ = attr_.value
                            #// In XHTML, empty values should never exist, so we repeat the value
                            if php_empty(lambda : value_) and type_ & SIMPLEPIE_CONSTRUCT_XHTML:
                                value_ = name_
                                #// For HTML, empty is fine
                            elif php_empty(lambda : value_) and type_ & SIMPLEPIE_CONSTRUCT_HTML:
                                attrs_[-1] = name_
                                continue
                            # end if
                            #// Standard attribute text
                            attrs_[-1] = name_ + "=\"" + attr_.value + "\""
                        # end for
                        text_ += " " + php_implode(" ", attrs_)
                    # end if
                    text_ += ">"
                    fragment_.appendchild(php_new_class("DOMText", lambda : DOMText(text_)))
                # end if
                number_ = element_.childNodes.length
                i_ = number_
                while i_ > 0:
                    
                    child_ = element_.childNodes.item(0)
                    fragment_.appendchild(child_)
                    i_ -= 1
                # end while
                if (not php_in_array(tag_, Array("script", "style"))):
                    fragment_.appendchild(php_new_class("DOMText", lambda : DOMText("</" + tag_ + ">")))
                # end if
                element_.parentNode.replacechild(fragment_, element_)
            # end for
            return
        elif php_in_array(tag_, Array("script", "style")):
            for element_ in elements_:
                element_.parentNode.removechild(element_)
            # end for
            return
        else:
            for element_ in elements_:
                fragment_ = document_.createdocumentfragment()
                number_ = element_.childNodes.length
                i_ = number_
                while i_ > 0:
                    
                    child_ = element_.childNodes.item(0)
                    fragment_.appendchild(child_)
                    i_ -= 1
                # end while
                element_.parentNode.replacechild(fragment_, element_)
            # end for
        # end if
    # end def strip_tag
    def strip_attr(self, attrib_=None, document_=None):
        
        
        xpath_ = php_new_class("DOMXPath", lambda : DOMXPath(document_))
        elements_ = xpath_.query("//*[@" + attrib_ + "]")
        for element_ in elements_:
            element_.removeattribute(attrib_)
        # end for
    # end def strip_attr
# end class SimplePie_Sanitize
