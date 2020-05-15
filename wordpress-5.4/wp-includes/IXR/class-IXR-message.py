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
#// IXR_MESSAGE
#// 
#// @package IXR
#// @since 1.5.0
#// 
#//
class IXR_Message():
    message = False
    messageType = False
    faultCode = False
    faultString = False
    methodName = ""
    params = Array()
    _arraystructs = Array()
    _arraystructstypes = Array()
    _currentStructName = Array()
    _param = Array()
    _value = Array()
    _currentTag = Array()
    _currentTagContents = Array()
    _parser = Array()
    #// 
    #// PHP5 constructor.
    #//
    def __init__(self, message=None):
        
        self.message = message
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def ixr_message(self, message=None):
        
        self.__init__(message)
    # end def ixr_message
    def parse(self):
        
        if (not php_function_exists("xml_parser_create")):
            trigger_error(__("PHP's XML extension is not available. Please contact your hosting provider to enable PHP's XML extension."))
            return False
        # end if
        #// first remove the XML declaration
        #// merged from WP #10698 - this method avoids the RAM usage of preg_replace on very large messages
        header = php_preg_replace("/<\\?xml.*?\\?" + ">/s", "", php_substr(self.message, 0, 100), 1)
        self.message = php_trim(php_substr_replace(self.message, header, 0, 100))
        if "" == self.message:
            return False
        # end if
        #// Then remove the DOCTYPE
        header = php_preg_replace("/^<!DOCTYPE[^>]*+>/i", "", php_substr(self.message, 0, 200), 1)
        self.message = php_trim(php_substr_replace(self.message, header, 0, 200))
        if "" == self.message:
            return False
        # end if
        #// Check that the root tag is valid
        root_tag = php_substr(self.message, 0, strcspn(php_substr(self.message, 0, 20), ">  \r\n"))
        if "<!DOCTYPE" == php_strtoupper(root_tag):
            return False
        # end if
        if (not php_in_array(root_tag, Array("<methodCall", "<methodResponse", "<fault"))):
            return False
        # end if
        #// Bail if there are too many elements to parse
        element_limit = 30000
        if php_function_exists("apply_filters"):
            #// 
            #// Filters the number of elements to parse in an XML-RPC response.
            #// 
            #// @since 4.0.0
            #// 
            #// @param int $element_limit Default elements limit.
            #//
            element_limit = apply_filters("xmlrpc_element_limit", element_limit)
        # end if
        if element_limit and 2 * element_limit < php_substr_count(self.message, "<"):
            return False
        # end if
        self._parser = xml_parser_create()
        #// Set XML parser to take the case of tags in to account
        xml_parser_set_option(self._parser, XML_OPTION_CASE_FOLDING, False)
        #// Set XML parser callback functions
        xml_set_object(self._parser, self)
        xml_set_element_handler(self._parser, "tag_open", "tag_close")
        xml_set_character_data_handler(self._parser, "cdata")
        #// 256Kb, parse in chunks to avoid the RAM usage on very large messages
        chunk_size = 262144
        #// 
        #// Filters the chunk size that can be used to parse an XML-RPC response message.
        #// 
        #// @since 4.4.0
        #// 
        #// @param int $chunk_size Chunk size to parse in bytes.
        #//
        chunk_size = apply_filters("xmlrpc_chunk_parsing_size", chunk_size)
        final = False
        while True:
            if php_strlen(self.message) <= chunk_size:
                final = True
            # end if
            part = php_substr(self.message, 0, chunk_size)
            self.message = php_substr(self.message, chunk_size)
            if (not xml_parse(self._parser, part, final)):
                return False
            # end if
            if final:
                break
            # end if
            
            if True:
                break
            # end if
        # end while
        xml_parser_free(self._parser)
        #// Grab the error messages, if any
        if self.messageType == "fault":
            self.faultCode = self.params[0]["faultCode"]
            self.faultString = self.params[0]["faultString"]
        # end if
        return True
    # end def parse
    def tag_open(self, parser=None, tag=None, attr=None):
        
        self._currentTagContents = ""
        self.currentTag = tag
        for case in Switch(tag):
            if case("methodCall"):
                pass
            # end if
            if case("methodResponse"):
                pass
            # end if
            if case("fault"):
                self.messageType = tag
                break
            # end if
            if case("data"):
                #// data is to all intents and puposes more interesting than array
                self._arraystructstypes[-1] = "array"
                self._arraystructs[-1] = Array()
                break
            # end if
            if case("struct"):
                self._arraystructstypes[-1] = "struct"
                self._arraystructs[-1] = Array()
                break
            # end if
        # end for
    # end def tag_open
    def cdata(self, parser=None, cdata=None):
        
        self._currentTagContents += cdata
    # end def cdata
    def tag_close(self, parser=None, tag=None):
        
        valueFlag = False
        for case in Switch(tag):
            if case("int"):
                pass
            # end if
            if case("i4"):
                value = int(php_trim(self._currentTagContents))
                valueFlag = True
                break
            # end if
            if case("double"):
                value = float(php_trim(self._currentTagContents))
                valueFlag = True
                break
            # end if
            if case("string"):
                value = str(php_trim(self._currentTagContents))
                valueFlag = True
                break
            # end if
            if case("dateTime.iso8601"):
                value = php_new_class("IXR_Date", lambda : IXR_Date(php_trim(self._currentTagContents)))
                valueFlag = True
                break
            # end if
            if case("value"):
                #// "If no type is indicated, the type is string."
                if php_trim(self._currentTagContents) != "":
                    value = str(self._currentTagContents)
                    valueFlag = True
                # end if
                break
            # end if
            if case("boolean"):
                value = bool(php_trim(self._currentTagContents))
                valueFlag = True
                break
            # end if
            if case("base64"):
                value = php_base64_decode(self._currentTagContents)
                valueFlag = True
                break
            # end if
            if case("data"):
                pass
            # end if
            if case("struct"):
                value = php_array_pop(self._arraystructs)
                php_array_pop(self._arraystructstypes)
                valueFlag = True
                break
            # end if
            if case("member"):
                php_array_pop(self._currentStructName)
                break
            # end if
            if case("name"):
                self._currentStructName[-1] = php_trim(self._currentTagContents)
                break
            # end if
            if case("methodName"):
                self.methodName = php_trim(self._currentTagContents)
                break
            # end if
        # end for
        if valueFlag:
            if php_count(self._arraystructs) > 0:
                #// Add value to struct or array
                if self._arraystructstypes[php_count(self._arraystructstypes) - 1] == "struct":
                    #// Add to struct
                    self._arraystructs[php_count(self._arraystructs) - 1][self._currentStructName[php_count(self._currentStructName) - 1]] = value
                else:
                    #// Add to array
                    self._arraystructs[php_count(self._arraystructs) - 1][-1] = value
                # end if
            else:
                #// Just add as a parameter
                self.params[-1] = value
            # end if
        # end if
        self._currentTagContents = ""
    # end def tag_close
# end class IXR_Message
