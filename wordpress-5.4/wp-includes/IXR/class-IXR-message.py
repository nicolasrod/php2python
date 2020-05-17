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
#// IXR_MESSAGE
#// 
#// @package IXR
#// @since 1.5.0
#// 
#//
class IXR_Message():
    message = False
    messageType = False
    #// methodCall / methodResponse / fault
    faultCode = False
    faultString = False
    methodName = ""
    params = Array()
    #// Current variable stacks
    _arraystructs = Array()
    #// The stack used to keep track of the current array/struct
    _arraystructstypes = Array()
    #// Stack keeping track of if things are structs or array
    _currentStructName = Array()
    #// A stack as well
    _param = Array()
    _value = Array()
    _currentTag = Array()
    _currentTagContents = Array()
    #// The XML parser
    _parser = Array()
    #// 
    #// PHP5 constructor.
    #//
    def __init__(self, message_=None):
        
        
        self.message = message_
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def ixr_message(self, message_=None):
        
        
        self.__init__(message_)
    # end def ixr_message
    def parse(self):
        
        
        if (not php_function_exists("xml_parser_create")):
            trigger_error(__("PHP's XML extension is not available. Please contact your hosting provider to enable PHP's XML extension."))
            return False
        # end if
        #// first remove the XML declaration
        #// merged from WP #10698 - this method avoids the RAM usage of preg_replace on very large messages
        header_ = php_preg_replace("/<\\?xml.*?\\?" + ">/s", "", php_substr(self.message, 0, 100), 1)
        self.message = php_trim(php_substr_replace(self.message, header_, 0, 100))
        if "" == self.message:
            return False
        # end if
        #// Then remove the DOCTYPE
        header_ = php_preg_replace("/^<!DOCTYPE[^>]*+>/i", "", php_substr(self.message, 0, 200), 1)
        self.message = php_trim(php_substr_replace(self.message, header_, 0, 200))
        if "" == self.message:
            return False
        # end if
        #// Check that the root tag is valid
        root_tag_ = php_substr(self.message, 0, strcspn(php_substr(self.message, 0, 20), ">     \r\n"))
        if "<!DOCTYPE" == php_strtoupper(root_tag_):
            return False
        # end if
        if (not php_in_array(root_tag_, Array("<methodCall", "<methodResponse", "<fault"))):
            return False
        # end if
        #// Bail if there are too many elements to parse
        element_limit_ = 30000
        if php_function_exists("apply_filters"):
            #// 
            #// Filters the number of elements to parse in an XML-RPC response.
            #// 
            #// @since 4.0.0
            #// 
            #// @param int $element_limit Default elements limit.
            #//
            element_limit_ = apply_filters("xmlrpc_element_limit", element_limit_)
        # end if
        if element_limit_ and 2 * element_limit_ < php_substr_count(self.message, "<"):
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
        chunk_size_ = 262144
        #// 
        #// Filters the chunk size that can be used to parse an XML-RPC response message.
        #// 
        #// @since 4.4.0
        #// 
        #// @param int $chunk_size Chunk size to parse in bytes.
        #//
        chunk_size_ = apply_filters("xmlrpc_chunk_parsing_size", chunk_size_)
        final_ = False
        while True:
            if php_strlen(self.message) <= chunk_size_:
                final_ = True
            # end if
            part_ = php_substr(self.message, 0, chunk_size_)
            self.message = php_substr(self.message, chunk_size_)
            if (not xml_parse(self._parser, part_, final_)):
                return False
            # end if
            if final_:
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
    def tag_open(self, parser_=None, tag_=None, attr_=None):
        
        
        self._currentTagContents = ""
        self.currentTag = tag_
        for case in Switch(tag_):
            if case("methodCall"):
                pass
            # end if
            if case("methodResponse"):
                pass
            # end if
            if case("fault"):
                self.messageType = tag_
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
    def cdata(self, parser_=None, cdata_=None):
        
        
        self._currentTagContents += cdata_
    # end def cdata
    def tag_close(self, parser_=None, tag_=None):
        
        
        valueFlag_ = False
        for case in Switch(tag_):
            if case("int"):
                pass
            # end if
            if case("i4"):
                value_ = php_int(php_trim(self._currentTagContents))
                valueFlag_ = True
                break
            # end if
            if case("double"):
                value_ = php_float(php_trim(self._currentTagContents))
                valueFlag_ = True
                break
            # end if
            if case("string"):
                value_ = php_str(php_trim(self._currentTagContents))
                valueFlag_ = True
                break
            # end if
            if case("dateTime.iso8601"):
                value_ = php_new_class("IXR_Date", lambda : IXR_Date(php_trim(self._currentTagContents)))
                valueFlag_ = True
                break
            # end if
            if case("value"):
                #// "If no type is indicated, the type is string."
                if php_trim(self._currentTagContents) != "":
                    value_ = php_str(self._currentTagContents)
                    valueFlag_ = True
                # end if
                break
            # end if
            if case("boolean"):
                value_ = php_bool(php_trim(self._currentTagContents))
                valueFlag_ = True
                break
            # end if
            if case("base64"):
                value_ = php_base64_decode(self._currentTagContents)
                valueFlag_ = True
                break
            # end if
            if case("data"):
                pass
            # end if
            if case("struct"):
                value_ = php_array_pop(self._arraystructs)
                php_array_pop(self._arraystructstypes)
                valueFlag_ = True
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
        if valueFlag_:
            if php_count(self._arraystructs) > 0:
                #// Add value to struct or array
                if self._arraystructstypes[php_count(self._arraystructstypes) - 1] == "struct":
                    #// Add to struct
                    self._arraystructs[php_count(self._arraystructs) - 1][self._currentStructName[php_count(self._currentStructName) - 1]] = value_
                else:
                    #// Add to array
                    self._arraystructs[php_count(self._arraystructs) - 1][-1] = value_
                # end if
            else:
                #// Just add as a parameter
                self.params[-1] = value_
            # end if
        # end if
        self._currentTagContents = ""
    # end def tag_close
# end class IXR_Message
