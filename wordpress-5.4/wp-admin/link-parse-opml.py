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
global opml
php_check_if_defined("opml")
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
def startElement(parser=None, tagName=None, attrs=None, *args_):
    
    #// phpcs:ignore WordPress.NamingConventions.ValidFunctionName.FunctionNameInvalid
    global names,urls,targets,descriptions,feeds
    php_check_if_defined("names","urls","targets","descriptions","feeds")
    if "OUTLINE" == tagName:
        name = ""
        if (php_isset(lambda : attrs["TEXT"])):
            name = attrs["TEXT"]
        # end if
        if (php_isset(lambda : attrs["TITLE"])):
            name = attrs["TITLE"]
        # end if
        url = ""
        if (php_isset(lambda : attrs["URL"])):
            url = attrs["URL"]
        # end if
        if (php_isset(lambda : attrs["HTMLURL"])):
            url = attrs["HTMLURL"]
        # end if
        #// Save the data away.
        names[-1] = name
        urls[-1] = url
        targets[-1] = attrs["TARGET"] if (php_isset(lambda : attrs["TARGET"])) else ""
        feeds[-1] = attrs["XMLURL"] if (php_isset(lambda : attrs["XMLURL"])) else ""
        descriptions[-1] = attrs["DESCRIPTION"] if (php_isset(lambda : attrs["DESCRIPTION"])) else ""
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
def endElement(parser=None, tagName=None, *args_):
    
    pass
# end def endElement
#// Create an XML parser.
if (not php_function_exists("xml_parser_create")):
    trigger_error(__("PHP's XML extension is not available. Please contact your hosting provider to enable PHP's XML extension."))
    wp_die(__("PHP's XML extension is not available. Please contact your hosting provider to enable PHP's XML extension."))
# end if
xml_parser = xml_parser_create()
#// Set the functions to handle opening and closing tags.
xml_set_element_handler(xml_parser, "startElement", "endElement")
if (not xml_parse(xml_parser, opml, True)):
    printf(__("XML Error: %1$s at line %2$s"), xml_error_string(xml_get_error_code(xml_parser)), xml_get_current_line_number(xml_parser))
# end if
#// Free up memory used by the XML parser.
xml_parser_free(xml_parser)
