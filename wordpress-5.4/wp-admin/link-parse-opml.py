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
#// Parse OPML XML files and store in globals.
#// 
#// @package WordPress
#// @subpackage Administration
#//
if (not php_defined("ABSPATH")):
    php_exit(0)
# end if
#// 
#// @global string $opml
#//
global opml_
php_check_if_defined("opml_")
#// 
#// XML callback function for the start of a new XML tag.
#// 
#// @since 0.71
#// @access private
#// 
#// @global array $names
#// @global array $urls
#// @global array $targets
#// @global array $descriptions
#// @global array $feeds
#// 
#// @param resource $parser XML Parser resource.
#// @param string $tagName XML element name.
#// @param array $attrs XML element attributes.
#//
def startElement(parser_=None, tagName_=None, attrs_=None, *_args_):
    
    
    #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.FunctionNameInvalid
    global names_
    global urls_
    global targets_
    global descriptions_
    global feeds_
    php_check_if_defined("names_","urls_","targets_","descriptions_","feeds_")
    if "OUTLINE" == tagName_:
        name_ = ""
        if (php_isset(lambda : attrs_["TEXT"])):
            name_ = attrs_["TEXT"]
        # end if
        if (php_isset(lambda : attrs_["TITLE"])):
            name_ = attrs_["TITLE"]
        # end if
        url_ = ""
        if (php_isset(lambda : attrs_["URL"])):
            url_ = attrs_["URL"]
        # end if
        if (php_isset(lambda : attrs_["HTMLURL"])):
            url_ = attrs_["HTMLURL"]
        # end if
        #// Save the data away.
        names_[-1] = name_
        urls_[-1] = url_
        targets_[-1] = attrs_["TARGET"] if (php_isset(lambda : attrs_["TARGET"])) else ""
        feeds_[-1] = attrs_["XMLURL"] if (php_isset(lambda : attrs_["XMLURL"])) else ""
        descriptions_[-1] = attrs_["DESCRIPTION"] if (php_isset(lambda : attrs_["DESCRIPTION"])) else ""
    # end if
    pass
# end def startElement
#// 
#// XML callback function that is called at the end of a XML tag.
#// 
#// @since 0.71
#// @access private
#// 
#// @param resource $parser XML Parser resource.
#// @param string $tagName XML tag name.
#//
def endElement(parser_=None, tagName_=None, *_args_):
    
    
    pass
# end def endElement
#// Create an XML parser.
if (not php_function_exists("xml_parser_create")):
    trigger_error(__("PHP's XML extension is not available. Please contact your hosting provider to enable PHP's XML extension."))
    wp_die(__("PHP's XML extension is not available. Please contact your hosting provider to enable PHP's XML extension."))
# end if
xml_parser_ = xml_parser_create()
#// Set the functions to handle opening and closing tags.
xml_set_element_handler(xml_parser_, "startElement", "endElement")
if (not xml_parse(xml_parser_, opml_, True)):
    printf(__("XML Error: %1$s at line %2$s"), xml_error_string(xml_get_error_code(xml_parser_)), xml_get_current_line_number(xml_parser_))
# end if
#// Free up memory used by the XML parser.
xml_parser_free(xml_parser_)
