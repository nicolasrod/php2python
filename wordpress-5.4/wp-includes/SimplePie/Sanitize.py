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
#// Used for data cleanup and post-processing
#// 
#// 
#// This class can be overloaded with {@see SimplePie::set_sanitize_class()}
#// 
#// @package SimplePie
#// @todo Move to using an actual HTML parser (this will allow tags to be properly stripped, and to switch between HTML and XHTML), this will also make it easier to shorten a string while preserving HTML tags
#//
class SimplePie_Sanitize():
    base = Array()
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
    def remove_div(self, enable=True):
        
        self.remove_div = php_bool(enable)
    # end def remove_div
    def set_image_handler(self, page=False):
        
        if page:
            self.image_handler = php_str(page)
        else:
            self.image_handler = False
        # end if
    # end def set_image_handler
    def set_registry(self, registry=None):
        
        self.registry = registry
    # end def set_registry
    def pass_cache_data(self, enable_cache=True, cache_location="./cache", cache_name_function="md5", cache_class="SimplePie_Cache"):
        
        if (php_isset(lambda : enable_cache)):
            self.enable_cache = php_bool(enable_cache)
        # end if
        if cache_location:
            self.cache_location = php_str(cache_location)
        # end if
        if cache_name_function:
            self.cache_name_function = php_str(cache_name_function)
        # end if
    # end def pass_cache_data
    def pass_file_data(self, file_class="SimplePie_File", timeout=10, useragent="", force_fsockopen=False):
        
        if timeout:
            self.timeout = php_str(timeout)
        # end if
        if useragent:
            self.useragent = php_str(useragent)
        # end if
        if force_fsockopen:
            self.force_fsockopen = php_str(force_fsockopen)
        # end if
    # end def pass_file_data
    def strip_htmltags(self, tags=Array("base", "blink", "body", "doctype", "embed", "font", "form", "frame", "frameset", "html", "iframe", "input", "marquee", "meta", "noscript", "object", "param", "script", "style")):
        
        if tags:
            if php_is_array(tags):
                self.strip_htmltags = tags
            else:
                self.strip_htmltags = php_explode(",", tags)
            # end if
        else:
            self.strip_htmltags = False
        # end if
    # end def strip_htmltags
    def encode_instead_of_strip(self, encode=False):
        
        self.encode_instead_of_strip = php_bool(encode)
    # end def encode_instead_of_strip
    def strip_attributes(self, attribs=Array("bgsound", "class", "expr", "id", "style", "onclick", "onerror", "onfinish", "onmouseover", "onmouseout", "onfocus", "onblur", "lowsrc", "dynsrc")):
        
        if attribs:
            if php_is_array(attribs):
                self.strip_attributes = attribs
            else:
                self.strip_attributes = php_explode(",", attribs)
            # end if
        else:
            self.strip_attributes = False
        # end if
    # end def strip_attributes
    def strip_comments(self, strip=False):
        
        self.strip_comments = php_bool(strip)
    # end def strip_comments
    def set_output_encoding(self, encoding="UTF-8"):
        
        self.output_encoding = php_str(encoding)
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
    def set_url_replacements(self, element_attribute=None):
        
        if element_attribute == None:
            element_attribute = Array({"a": "href", "area": "href", "blockquote": "cite", "del": "cite", "form": "action", "img": Array("longdesc", "src"), "input": "src", "ins": "cite", "q": "cite"})
        # end if
        self.replace_url_attributes = element_attribute
    # end def set_url_replacements
    def sanitize(self, data=None, type=None, base=""):
        
        data = php_trim(data)
        if data != "" or type & SIMPLEPIE_CONSTRUCT_IRI:
            if type & SIMPLEPIE_CONSTRUCT_MAYBE_HTML:
                if php_preg_match("/(&(#(x[0-9a-fA-F]+|[0-9]+)|[a-zA-Z0-9]+)|<\\/[A-Za-z][^\\x09\\x0A\\x0B\\x0C\\x0D\\x20\\x2F\\x3E]*" + SIMPLEPIE_PCRE_HTML_ATTRIBUTE + ">)/", data):
                    type |= SIMPLEPIE_CONSTRUCT_HTML
                else:
                    type |= SIMPLEPIE_CONSTRUCT_TEXT
                # end if
            # end if
            if type & SIMPLEPIE_CONSTRUCT_BASE64:
                data = php_base64_decode(data)
            # end if
            if type & SIMPLEPIE_CONSTRUCT_HTML | SIMPLEPIE_CONSTRUCT_XHTML:
                if (not php_class_exists("DOMDocument")):
                    self.registry.call("Misc", "error", Array("DOMDocument not found, unable to use sanitizer", E_USER_WARNING, __FILE__, 0))
                    return ""
                # end if
                document = php_new_class("DOMDocument", lambda : DOMDocument())
                document.encoding = "UTF-8"
                data = self.preprocess(data, type)
                set_error_handler(Array("SimplePie_Misc", "silence_errors"))
                document.loadhtml(data)
                restore_error_handler()
                #// Strip comments
                if self.strip_comments:
                    xpath = php_new_class("DOMXPath", lambda : DOMXPath(document))
                    comments = xpath.query("//comment()")
                    for comment in comments:
                        comment.parentNode.removechild(comment)
                    # end for
                # end if
                #// Strip out HTML tags and attributes that might cause various security problems.
                #// Based on recommendations by Mark Pilgrim at:
                #// http://diveintomark.org/archives/2003/06/12/how_to_consume_rss_safely
                if self.strip_htmltags:
                    for tag in self.strip_htmltags:
                        self.strip_tag(tag, document, type)
                    # end for
                # end if
                if self.strip_attributes:
                    for attrib in self.strip_attributes:
                        self.strip_attr(attrib, document)
                    # end for
                # end if
                #// Replace relative URLs
                self.base = base
                for element,attributes in self.replace_url_attributes:
                    self.replace_urls(document, element, attributes)
                # end for
                #// If image handling (caching, etc.) is enabled, cache and rewrite all the image tags.
                if (php_isset(lambda : self.image_handler)) and php_str(self.image_handler) != "" and self.enable_cache:
                    images = document.getelementsbytagname("img")
                    for img in images:
                        if img.hasattribute("src"):
                            image_url = php_call_user_func(self.cache_name_function, img.getattribute("src"))
                            cache = self.registry.call("Cache", "get_handler", Array(self.cache_location, image_url, "spi"))
                            if cache.load():
                                img.setattribute("src", self.image_handler + image_url)
                            else:
                                file = self.registry.create("File", Array(img.getattribute("src"), self.timeout, 5, Array({"X-FORWARDED-FOR": PHP_SERVER["REMOTE_ADDR"]}), self.useragent, self.force_fsockopen))
                                headers = file.headers
                                if file.success and file.method & SIMPLEPIE_FILE_SOURCE_REMOTE == 0 or file.status_code == 200 or file.status_code > 206 and file.status_code < 300:
                                    if cache.save(Array({"headers": file.headers, "body": file.body})):
                                        img.setattribute("src", self.image_handler + image_url)
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
                if type(document.firstChild).__name__ == "DOMDocumentType":
                    document.removechild(document.firstChild)
                # end if
                #// Move everything from the body to the root
                real_body = document.getelementsbytagname("body").item(0).childNodes.item(0)
                document.replacechild(real_body, document.firstChild)
                #// Finally, convert to a HTML string
                data = php_trim(document.savehtml())
                if self.remove_div:
                    data = php_preg_replace("/^<div" + SIMPLEPIE_PCRE_XML_ATTRIBUTE + ">/", "", data)
                    data = php_preg_replace("/<\\/div>$/", "", data)
                else:
                    data = php_preg_replace("/^<div" + SIMPLEPIE_PCRE_XML_ATTRIBUTE + ">/", "<div>", data)
                # end if
            # end if
            if type & SIMPLEPIE_CONSTRUCT_IRI:
                absolute = self.registry.call("Misc", "absolutize_url", Array(data, base))
                if absolute != False:
                    data = absolute
                # end if
            # end if
            if type & SIMPLEPIE_CONSTRUCT_TEXT | SIMPLEPIE_CONSTRUCT_IRI:
                data = htmlspecialchars(data, ENT_COMPAT, "UTF-8")
            # end if
            if self.output_encoding != "UTF-8":
                data = self.registry.call("Misc", "change_encoding", Array(data, "UTF-8", self.output_encoding))
            # end if
        # end if
        return data
    # end def sanitize
    def preprocess(self, html=None, type=None):
        
        ret = ""
        if type & (1 << (SIMPLEPIE_CONSTRUCT_XHTML).bit_length()) - 1 - SIMPLEPIE_CONSTRUCT_XHTML:
            #// Atom XHTML constructs are wrapped with a div by default
            #// Note: No protection if $html contains a stray </div>!
            html = "<div>" + html + "</div>"
            ret += "<!DOCTYPE html>"
            content_type = "text/html"
        else:
            ret += "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">"
            content_type = "application/xhtml+xml"
        # end if
        ret += "<html><head>"
        ret += "<meta http-equiv=\"Content-Type\" content=\"" + content_type + "; charset=utf-8\" />"
        ret += "</head><body>" + html + "</body></html>"
        return ret
    # end def preprocess
    def replace_urls(self, document=None, tag=None, attributes=None):
        
        if (not php_is_array(attributes)):
            attributes = Array(attributes)
        # end if
        if (not php_is_array(self.strip_htmltags)) or (not php_in_array(tag, self.strip_htmltags)):
            elements = document.getelementsbytagname(tag)
            for element in elements:
                for attribute in attributes:
                    if element.hasattribute(attribute):
                        value = self.registry.call("Misc", "absolutize_url", Array(element.getattribute(attribute), self.base))
                        if value != False:
                            element.setattribute(attribute, value)
                        # end if
                    # end if
                # end for
            # end for
        # end if
    # end def replace_urls
    def do_strip_htmltags(self, match=None):
        
        if self.encode_instead_of_strip:
            if (php_isset(lambda : match[4])) and (not php_in_array(php_strtolower(match[1]), Array("script", "style"))):
                match[1] = htmlspecialchars(match[1], ENT_COMPAT, "UTF-8")
                match[2] = htmlspecialchars(match[2], ENT_COMPAT, "UTF-8")
                return str("&lt;") + str(match[1]) + str(match[2]) + str("&gt;") + str(match[3]) + str("&lt;/") + str(match[1]) + str("&gt;")
            else:
                return htmlspecialchars(match[0], ENT_COMPAT, "UTF-8")
            # end if
        elif (php_isset(lambda : match[4])) and (not php_in_array(php_strtolower(match[1]), Array("script", "style"))):
            return match[4]
        else:
            return ""
        # end if
    # end def do_strip_htmltags
    def strip_tag(self, tag=None, document=None, type=None):
        
        xpath = php_new_class("DOMXPath", lambda : DOMXPath(document))
        elements = xpath.query("body//" + tag)
        if self.encode_instead_of_strip:
            for element in elements:
                fragment = document.createdocumentfragment()
                #// For elements which aren't script or style, include the tag itself
                if (not php_in_array(tag, Array("script", "style"))):
                    text = "<" + tag
                    if element.hasattributes():
                        attrs = Array()
                        for name,attr in element.attributes:
                            value = attr.value
                            #// In XHTML, empty values should never exist, so we repeat the value
                            if php_empty(lambda : value) and type & SIMPLEPIE_CONSTRUCT_XHTML:
                                value = name
                                #// For HTML, empty is fine
                            elif php_empty(lambda : value) and type & SIMPLEPIE_CONSTRUCT_HTML:
                                attrs[-1] = name
                                continue
                            # end if
                            #// Standard attribute text
                            attrs[-1] = name + "=\"" + attr.value + "\""
                        # end for
                        text += " " + php_implode(" ", attrs)
                    # end if
                    text += ">"
                    fragment.appendchild(php_new_class("DOMText", lambda : DOMText(text)))
                # end if
                number = element.childNodes.length
                i = number
                while i > 0:
                    
                    child = element.childNodes.item(0)
                    fragment.appendchild(child)
                    i -= 1
                # end while
                if (not php_in_array(tag, Array("script", "style"))):
                    fragment.appendchild(php_new_class("DOMText", lambda : DOMText("</" + tag + ">")))
                # end if
                element.parentNode.replacechild(fragment, element)
            # end for
            return
        elif php_in_array(tag, Array("script", "style")):
            for element in elements:
                element.parentNode.removechild(element)
            # end for
            return
        else:
            for element in elements:
                fragment = document.createdocumentfragment()
                number = element.childNodes.length
                i = number
                while i > 0:
                    
                    child = element.childNodes.item(0)
                    fragment.appendchild(child)
                    i -= 1
                # end while
                element.parentNode.replacechild(fragment, element)
            # end for
        # end if
    # end def strip_tag
    def strip_attr(self, attrib=None, document=None):
        
        xpath = php_new_class("DOMXPath", lambda : DOMXPath(document))
        elements = xpath.query("//*[@" + attrib + "]")
        for element in elements:
            element.removeattribute(attrib)
        # end for
    # end def strip_attr
# end class SimplePie_Sanitize
