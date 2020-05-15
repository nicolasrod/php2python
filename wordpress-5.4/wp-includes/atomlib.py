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
#// Atom Syndication Format PHP Library
#// 
#// @package AtomLib
#// @link http://code.google.com/p/phpatomlib
#// 
#// @author Elias Torres <elias@torrez.us>
#// @version 0.4
#// @since 2.3.0
#// 
#// 
#// Structure that store common Atom Feed Properties
#// 
#// @package AtomLib
#//
class AtomFeed():
    links = Array()
    categories = Array()
    entries = Array()
# end class AtomFeed
#// 
#// Structure that store Atom Entry Properties
#// 
#// @package AtomLib
#//
class AtomEntry():
    links = Array()
    categories = Array()
# end class AtomEntry
#// 
#// AtomLib Atom Parser API
#// 
#// @package AtomLib
#//
class AtomParser():
    NS = "http://www.w3.org/2005/Atom"
    ATOM_CONTENT_ELEMENTS = Array("content", "summary", "title", "subtitle", "rights")
    ATOM_SIMPLE_ELEMENTS = Array("id", "updated", "published", "draft")
    debug = False
    depth = 0
    indent = 2
    in_content = Array()
    ns_contexts = Array()
    ns_decls = Array()
    content_ns_decls = Array()
    content_ns_contexts = Array()
    is_xhtml = False
    is_html = False
    is_text = True
    skipped_div = False
    FILE = "php://input"
    feed = Array()
    current = Array()
    #// 
    #// PHP5 constructor.
    #//
    def __init__(self):
        
        self.feed = php_new_class("AtomFeed", lambda : AtomFeed())
        self.current = None
        self.map_attrs_func = Array(__CLASS__, "map_attrs")
        self.map_xmlns_func = Array(__CLASS__, "map_xmlns")
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def atomparser(self):
        
        self.__init__()
    # end def atomparser
    #// 
    #// Map attributes to key="val"
    #// 
    #// @param string $k Key
    #// @param string $v Value
    #// @return string
    #//
    @classmethod
    def map_attrs(self, k=None, v=None):
        
        return str(k) + str("=\"") + str(v) + str("\"")
    # end def map_attrs
    #// 
    #// Map XML namespace to string.
    #// 
    #// @param indexish $p XML Namespace element index
    #// @param array $n Two-element array pair. [ 0 => {namespace}, 1 => {url} ]
    #// @return string 'xmlns="{url}"' or 'xmlns:{namespace}="{url}"'
    #//
    @classmethod
    def map_xmlns(self, p=None, n=None):
        
        xd = "xmlns"
        if 0 < php_strlen(n[0]):
            xd += str(":") + str(n[0])
        # end if
        return str(xd) + str("=\"") + str(n[1]) + str("\"")
    # end def map_xmlns
    def _p(self, msg=None):
        
        if self.debug:
            php_print(php_str_repeat(" ", self.depth * self.indent) + msg + "\n")
        # end if
    # end def _p
    def error_handler(self, log_level=None, log_text=None, error_file=None, error_line=None):
        
        self.error = log_text
    # end def error_handler
    def parse(self):
        
        set_error_handler(Array(self, "error_handler"))
        array_unshift(self.ns_contexts, Array())
        if (not php_function_exists("xml_parser_create_ns")):
            trigger_error(__("PHP's XML extension is not available. Please contact your hosting provider to enable PHP's XML extension."))
            return False
        # end if
        parser = xml_parser_create_ns()
        xml_set_object(parser, self)
        xml_set_element_handler(parser, "start_element", "end_element")
        xml_parser_set_option(parser, XML_OPTION_CASE_FOLDING, 0)
        xml_parser_set_option(parser, XML_OPTION_SKIP_WHITE, 0)
        xml_set_character_data_handler(parser, "cdata")
        xml_set_default_handler(parser, "_default")
        xml_set_start_namespace_decl_handler(parser, "start_ns")
        xml_set_end_namespace_decl_handler(parser, "end_ns")
        self.content = ""
        ret = True
        fp = fopen(self.FILE, "r")
        while True:
            data = fread(fp, 4096)
            if not (data):
                break
            # end if
            if self.debug:
                self.content += data
            # end if
            if (not xml_parse(parser, data, php_feof(fp))):
                #// translators: 1: Error message, 2: Line number.
                trigger_error(php_sprintf(__("XML Error: %1$s at line %2$s") + "\n", xml_error_string(xml_get_error_code(parser)), xml_get_current_line_number(parser)))
                ret = False
                break
            # end if
        # end while
        php_fclose(fp)
        xml_parser_free(parser)
        restore_error_handler()
        return ret
    # end def parse
    def start_element(self, parser=None, name=None, attrs=None):
        
        tag = php_array_pop(php_explode(":", name))
        for case in Switch(name):
            if case(self.NS + ":feed"):
                self.current = self.feed
                break
            # end if
            if case(self.NS + ":entry"):
                self.current = php_new_class("AtomEntry", lambda : AtomEntry())
                break
            # end if
        # end for
        self._p(str("start_element('") + str(name) + str("')"))
        #// #$this->_p(print_r($this->ns_contexts,true));
        #// #$this->_p('current(' . $this->current . ')');
        array_unshift(self.ns_contexts, self.ns_decls)
        self.depth += 1
        if (not php_empty(lambda : self.in_content)):
            self.content_ns_decls = Array()
            if self.is_html or self.is_text:
                trigger_error("Invalid content in element found. Content must not be of type text or html if it contains markup.")
            # end if
            attrs_prefix = Array()
            #// resolve prefixes for attributes
            for key,value in attrs:
                with_prefix = self.ns_to_prefix(key, True)
                attrs_prefix[with_prefix[1]] = self.xml_escape(value)
            # end for
            attrs_str = join(" ", php_array_map(self.map_attrs_func, php_array_keys(attrs_prefix), php_array_values(attrs_prefix)))
            if php_strlen(attrs_str) > 0:
                attrs_str = " " + attrs_str
            # end if
            with_prefix = self.ns_to_prefix(name)
            if (not self.is_declared_content_ns(with_prefix[0])):
                php_array_push(self.content_ns_decls, with_prefix[0])
            # end if
            xmlns_str = ""
            if php_count(self.content_ns_decls) > 0:
                array_unshift(self.content_ns_contexts, self.content_ns_decls)
                xmlns_str += join(" ", php_array_map(self.map_xmlns_func, php_array_keys(self.content_ns_contexts[0]), php_array_values(self.content_ns_contexts[0])))
                if php_strlen(xmlns_str) > 0:
                    xmlns_str = " " + xmlns_str
                # end if
            # end if
            php_array_push(self.in_content, Array(tag, self.depth, "<" + with_prefix[1] + str(xmlns_str) + str(attrs_str) + ">"))
        else:
            if php_in_array(tag, self.ATOM_CONTENT_ELEMENTS) or php_in_array(tag, self.ATOM_SIMPLE_ELEMENTS):
                self.in_content = Array()
                self.is_xhtml = attrs["type"] == "xhtml"
                self.is_html = attrs["type"] == "html" or attrs["type"] == "text/html"
                self.is_text = (not php_in_array("type", php_array_keys(attrs))) or attrs["type"] == "text"
                type = "XHTML" if self.is_xhtml else "HTML" if self.is_html else "TEXT" if self.is_text else attrs["type"]
                if php_in_array("src", php_array_keys(attrs)):
                    self.current.tag = attrs
                else:
                    php_array_push(self.in_content, Array(tag, self.depth, type))
                # end if
            else:
                if tag == "link":
                    php_array_push(self.current.links, attrs)
                else:
                    if tag == "category":
                        php_array_push(self.current.categories, attrs)
                    # end if
                # end if
            # end if
        # end if
        self.ns_decls = Array()
    # end def start_element
    def end_element(self, parser=None, name=None):
        
        tag = php_array_pop(php_explode(":", name))
        ccount = php_count(self.in_content)
        #// # if we are *in* content, then let's proceed to serialize it
        if (not php_empty(lambda : self.in_content)):
            #// # if we are ending the original content element
            #// # then let's finalize the content
            if self.in_content[0][0] == tag and self.in_content[0][1] == self.depth:
                origtype = self.in_content[0][2]
                php_array_shift(self.in_content)
                newcontent = Array()
                for c in self.in_content:
                    if php_count(c) == 3:
                        php_array_push(newcontent, c[2])
                    else:
                        if self.is_xhtml or self.is_text:
                            php_array_push(newcontent, self.xml_escape(c))
                        else:
                            php_array_push(newcontent, c)
                        # end if
                    # end if
                # end for
                if php_in_array(tag, self.ATOM_CONTENT_ELEMENTS):
                    self.current.tag = Array(origtype, join("", newcontent))
                else:
                    self.current.tag = join("", newcontent)
                # end if
                self.in_content = Array()
            else:
                if self.in_content[ccount - 1][0] == tag and self.in_content[ccount - 1][1] == self.depth:
                    self.in_content[ccount - 1][2] = php_substr(self.in_content[ccount - 1][2], 0, -1) + "/>"
                else:
                    #// # else, just finalize the current element's content
                    endtag = self.ns_to_prefix(name)
                    php_array_push(self.in_content, Array(tag, self.depth, str("</") + str(endtag[1]) + str(">")))
                # end if
            # end if
        # end if
        php_array_shift(self.ns_contexts)
        self.depth -= 1
        if name == self.NS + ":entry":
            php_array_push(self.feed.entries, self.current)
            self.current = None
        # end if
        self._p(str("end_element('") + str(name) + str("')"))
    # end def end_element
    def start_ns(self, parser=None, prefix=None, uri=None):
        
        self._p("starting: " + prefix + ":" + uri)
        php_array_push(self.ns_decls, Array(prefix, uri))
    # end def start_ns
    def end_ns(self, parser=None, prefix=None):
        
        self._p("ending: #" + prefix + "#")
    # end def end_ns
    def cdata(self, parser=None, data=None):
        
        self._p("data: #" + php_str_replace(Array("\n"), Array("\\n"), php_trim(data)) + "#")
        if (not php_empty(lambda : self.in_content)):
            php_array_push(self.in_content, data)
        # end if
    # end def cdata
    def _default(self, parser=None, data=None):
        
        pass
    # end def _default
    def ns_to_prefix(self, qname=None, attr=False):
        
        #// # split 'http://www.w3.org/1999/xhtml:div' into ('http','//www.w3.org/1999/xhtml','div')
        components = php_explode(":", qname)
        #// # grab the last one (e.g 'div')
        name = php_array_pop(components)
        if (not php_empty(lambda : components)):
            #// # re-join back the namespace component
            ns = join(":", components)
            for context in self.ns_contexts:
                for mapping in context:
                    if mapping[1] == ns and php_strlen(mapping[0]) > 0:
                        return Array(mapping, str(mapping[0]) + str(":") + str(name))
                    # end if
                # end for
            # end for
        # end if
        if attr:
            return Array(None, name)
        else:
            for context in self.ns_contexts:
                for mapping in context:
                    if php_strlen(mapping[0]) == 0:
                        return Array(mapping, name)
                    # end if
                # end for
            # end for
        # end if
    # end def ns_to_prefix
    def is_declared_content_ns(self, new_mapping=None):
        
        for context in self.content_ns_contexts:
            for mapping in context:
                if new_mapping == mapping:
                    return True
                # end if
            # end for
        # end for
        return False
    # end def is_declared_content_ns
    def xml_escape(self, string=None):
        
        return php_str_replace(Array("&", "\"", "'", "<", ">"), Array("&amp;", "&quot;", "&apos;", "&lt;", "&gt;"), string)
    # end def xml_escape
# end class AtomParser
