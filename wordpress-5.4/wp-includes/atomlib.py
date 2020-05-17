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
    #// 
    #// Stores Links
    #// @var array
    #// @access public
    #//
    links = Array()
    #// 
    #// Stores Categories
    #// @var array
    #// @access public
    #//
    categories = Array()
    #// 
    #// Stores Entries
    #// 
    #// @var array
    #// @access public
    #//
    entries = Array()
# end class AtomFeed
#// 
#// Structure that store Atom Entry Properties
#// 
#// @package AtomLib
#//
class AtomEntry():
    #// 
    #// Stores Links
    #// @var array
    #// @access public
    #//
    links = Array()
    #// 
    #// Stores Categories
    #// @var array
    #// @access public
    #//
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
    FILE_ = "php://input"
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
    def map_attrs(self, k_=None, v_=None):
        
        
        return str(k_) + str("=\"") + str(v_) + str("\"")
    # end def map_attrs
    #// 
    #// Map XML namespace to string.
    #// 
    #// @param indexish $p XML Namespace element index
    #// @param array $n Two-element array pair. [ 0 => {namespace}, 1 => {url} ]
    #// @return string 'xmlns="{url}"' or 'xmlns:{namespace}="{url}"'
    #//
    @classmethod
    def map_xmlns(self, p_=None, n_=None):
        
        
        xd_ = "xmlns"
        if 0 < php_strlen(n_[0]):
            xd_ += str(":") + str(n_[0])
        # end if
        return str(xd_) + str("=\"") + str(n_[1]) + str("\"")
    # end def map_xmlns
    def _p(self, msg_=None):
        
        
        if self.debug:
            php_print(php_str_repeat(" ", self.depth * self.indent) + msg_ + "\n")
        # end if
    # end def _p
    def error_handler(self, log_level_=None, log_text_=None, error_file_=None, error_line_=None):
        
        
        self.error = log_text_
    # end def error_handler
    def parse(self):
        
        
        set_error_handler(Array(self, "error_handler"))
        array_unshift(self.ns_contexts, Array())
        if (not php_function_exists("xml_parser_create_ns")):
            trigger_error(__("PHP's XML extension is not available. Please contact your hosting provider to enable PHP's XML extension."))
            return False
        # end if
        parser_ = xml_parser_create_ns()
        xml_set_object(parser_, self)
        xml_set_element_handler(parser_, "start_element", "end_element")
        xml_parser_set_option(parser_, XML_OPTION_CASE_FOLDING, 0)
        xml_parser_set_option(parser_, XML_OPTION_SKIP_WHITE, 0)
        xml_set_character_data_handler(parser_, "cdata")
        xml_set_default_handler(parser_, "_default")
        xml_set_start_namespace_decl_handler(parser_, "start_ns")
        xml_set_end_namespace_decl_handler(parser_, "end_ns")
        self.content = ""
        ret_ = True
        fp_ = fopen(self.FILE_, "r")
        while True:
            data_ = fread(fp_, 4096)
            if not (data_):
                break
            # end if
            if self.debug:
                self.content += data_
            # end if
            if (not xml_parse(parser_, data_, php_feof(fp_))):
                #// translators: 1: Error message, 2: Line number.
                trigger_error(php_sprintf(__("XML Error: %1$s at line %2$s") + "\n", xml_error_string(xml_get_error_code(parser_)), xml_get_current_line_number(parser_)))
                ret_ = False
                break
            # end if
        # end while
        php_fclose(fp_)
        xml_parser_free(parser_)
        restore_error_handler()
        return ret_
    # end def parse
    def start_element(self, parser_=None, name_=None, attrs_=None):
        
        
        tag_ = php_array_pop(php_explode(":", name_))
        for case in Switch(name_):
            if case(self.NS + ":feed"):
                self.current = self.feed
                break
            # end if
            if case(self.NS + ":entry"):
                self.current = php_new_class("AtomEntry", lambda : AtomEntry())
                break
            # end if
        # end for
        self._p(str("start_element('") + str(name_) + str("')"))
        #// #$this->_p(print_r($this->ns_contexts,true));
        #// #$this->_p('current(' . $this->current . ')');
        array_unshift(self.ns_contexts, self.ns_decls)
        self.depth += 1
        if (not php_empty(lambda : self.in_content)):
            self.content_ns_decls = Array()
            if self.is_html or self.is_text:
                trigger_error("Invalid content in element found. Content must not be of type text or html if it contains markup.")
            # end if
            attrs_prefix_ = Array()
            #// resolve prefixes for attributes
            for key_,value_ in attrs_:
                with_prefix_ = self.ns_to_prefix(key_, True)
                attrs_prefix_[with_prefix_[1]] = self.xml_escape(value_)
            # end for
            attrs_str_ = join(" ", php_array_map(self.map_attrs_func, php_array_keys(attrs_prefix_), php_array_values(attrs_prefix_)))
            if php_strlen(attrs_str_) > 0:
                attrs_str_ = " " + attrs_str_
            # end if
            with_prefix_ = self.ns_to_prefix(name_)
            if (not self.is_declared_content_ns(with_prefix_[0])):
                php_array_push(self.content_ns_decls, with_prefix_[0])
            # end if
            xmlns_str_ = ""
            if php_count(self.content_ns_decls) > 0:
                array_unshift(self.content_ns_contexts, self.content_ns_decls)
                xmlns_str_ += join(" ", php_array_map(self.map_xmlns_func, php_array_keys(self.content_ns_contexts[0]), php_array_values(self.content_ns_contexts[0])))
                if php_strlen(xmlns_str_) > 0:
                    xmlns_str_ = " " + xmlns_str_
                # end if
            # end if
            php_array_push(self.in_content, Array(tag_, self.depth, "<" + with_prefix_[1] + str(xmlns_str_) + str(attrs_str_) + ">"))
        else:
            if php_in_array(tag_, self.ATOM_CONTENT_ELEMENTS) or php_in_array(tag_, self.ATOM_SIMPLE_ELEMENTS):
                self.in_content = Array()
                self.is_xhtml = attrs_["type"] == "xhtml"
                self.is_html = attrs_["type"] == "html" or attrs_["type"] == "text/html"
                self.is_text = (not php_in_array("type", php_array_keys(attrs_))) or attrs_["type"] == "text"
                type_ = "XHTML" if self.is_xhtml else "HTML" if self.is_html else "TEXT" if self.is_text else attrs_["type"]
                if php_in_array("src", php_array_keys(attrs_)):
                    self.current.tag_ = attrs_
                else:
                    php_array_push(self.in_content, Array(tag_, self.depth, type_))
                # end if
            else:
                if tag_ == "link":
                    php_array_push(self.current.links, attrs_)
                else:
                    if tag_ == "category":
                        php_array_push(self.current.categories, attrs_)
                    # end if
                # end if
            # end if
        # end if
        self.ns_decls = Array()
    # end def start_element
    def end_element(self, parser_=None, name_=None):
        
        
        tag_ = php_array_pop(php_explode(":", name_))
        ccount_ = php_count(self.in_content)
        #// # if we are *in* content, then let's proceed to serialize it
        if (not php_empty(lambda : self.in_content)):
            #// # if we are ending the original content element
            #// # then let's finalize the content
            if self.in_content[0][0] == tag_ and self.in_content[0][1] == self.depth:
                origtype_ = self.in_content[0][2]
                php_array_shift(self.in_content)
                newcontent_ = Array()
                for c_ in self.in_content:
                    if php_count(c_) == 3:
                        php_array_push(newcontent_, c_[2])
                    else:
                        if self.is_xhtml or self.is_text:
                            php_array_push(newcontent_, self.xml_escape(c_))
                        else:
                            php_array_push(newcontent_, c_)
                        # end if
                    # end if
                # end for
                if php_in_array(tag_, self.ATOM_CONTENT_ELEMENTS):
                    self.current.tag_ = Array(origtype_, join("", newcontent_))
                else:
                    self.current.tag_ = join("", newcontent_)
                # end if
                self.in_content = Array()
            else:
                if self.in_content[ccount_ - 1][0] == tag_ and self.in_content[ccount_ - 1][1] == self.depth:
                    self.in_content[ccount_ - 1][2] = php_substr(self.in_content[ccount_ - 1][2], 0, -1) + "/>"
                else:
                    #// # else, just finalize the current element's content
                    endtag_ = self.ns_to_prefix(name_)
                    php_array_push(self.in_content, Array(tag_, self.depth, str("</") + str(endtag_[1]) + str(">")))
                # end if
            # end if
        # end if
        php_array_shift(self.ns_contexts)
        self.depth -= 1
        if name_ == self.NS + ":entry":
            php_array_push(self.feed.entries, self.current)
            self.current = None
        # end if
        self._p(str("end_element('") + str(name_) + str("')"))
    # end def end_element
    def start_ns(self, parser_=None, prefix_=None, uri_=None):
        
        
        self._p("starting: " + prefix_ + ":" + uri_)
        php_array_push(self.ns_decls, Array(prefix_, uri_))
    # end def start_ns
    def end_ns(self, parser_=None, prefix_=None):
        
        
        self._p("ending: #" + prefix_ + "#")
    # end def end_ns
    def cdata(self, parser_=None, data_=None):
        
        
        self._p("data: #" + php_str_replace(Array("\n"), Array("\\n"), php_trim(data_)) + "#")
        if (not php_empty(lambda : self.in_content)):
            php_array_push(self.in_content, data_)
        # end if
    # end def cdata
    def _default(self, parser_=None, data_=None):
        
        
        pass
    # end def _default
    def ns_to_prefix(self, qname_=None, attr_=None):
        if attr_ is None:
            attr_ = False
        # end if
        
        #// # split 'http://www.w3.org/1999/xhtml:div' into ('http','//www.w3.org/1999/xhtml','div')
        components_ = php_explode(":", qname_)
        #// # grab the last one (e.g 'div')
        name_ = php_array_pop(components_)
        if (not php_empty(lambda : components_)):
            #// # re-join back the namespace component
            ns_ = join(":", components_)
            for context_ in self.ns_contexts:
                for mapping_ in context_:
                    if mapping_[1] == ns_ and php_strlen(mapping_[0]) > 0:
                        return Array(mapping_, str(mapping_[0]) + str(":") + str(name_))
                    # end if
                # end for
            # end for
        # end if
        if attr_:
            return Array(None, name_)
        else:
            for context_ in self.ns_contexts:
                for mapping_ in context_:
                    if php_strlen(mapping_[0]) == 0:
                        return Array(mapping_, name_)
                    # end if
                # end for
            # end for
        # end if
    # end def ns_to_prefix
    def is_declared_content_ns(self, new_mapping_=None):
        
        
        for context_ in self.content_ns_contexts:
            for mapping_ in context_:
                if new_mapping_ == mapping_:
                    return True
                # end if
            # end for
        # end for
        return False
    # end def is_declared_content_ns
    def xml_escape(self, string_=None):
        
        
        return php_str_replace(Array("&", "\"", "'", "<", ">"), Array("&amp;", "&quot;", "&apos;", "&lt;", "&gt;"), string_)
    # end def xml_escape
# end class AtomParser
