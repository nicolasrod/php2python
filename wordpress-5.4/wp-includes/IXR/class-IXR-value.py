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
#// IXR_Value
#// 
#// @package IXR
#// @since 1.5.0
#//
class IXR_Value():
    data = Array()
    type = Array()
    #// 
    #// PHP5 constructor.
    #//
    def __init__(self, data_=None, type_=None):
        if type_ is None:
            type_ = False
        # end if
        
        self.data = data_
        if (not type_):
            type_ = self.calculatetype()
        # end if
        self.type = type_
        if type_ == "struct":
            #// Turn all the values in the array in to new IXR_Value objects
            for key_,value_ in self.data:
                self.data[key_] = php_new_class("IXR_Value", lambda : IXR_Value(value_))
            # end for
        # end if
        if type_ == "array":
            i_ = 0
            j_ = php_count(self.data)
            while i_ < j_:
                
                self.data[i_] = php_new_class("IXR_Value", lambda : IXR_Value(self.data[i_]))
                i_ += 1
            # end while
        # end if
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def ixr_value(self, data_=None, type_=None):
        if type_ is None:
            type_ = False
        # end if
        
        self.__init__(data_, type_)
    # end def ixr_value
    def calculatetype(self):
        
        
        if self.data == True or self.data == False:
            return "boolean"
        # end if
        if is_integer(self.data):
            return "int"
        # end if
        if is_double(self.data):
            return "double"
        # end if
        #// Deal with IXR object types base64 and date
        if php_is_object(self.data) and php_is_a(self.data, "IXR_Date"):
            return "date"
        # end if
        if php_is_object(self.data) and php_is_a(self.data, "IXR_Base64"):
            return "base64"
        # end if
        #// If it is a normal PHP object convert it in to a struct
        if php_is_object(self.data):
            self.data = get_object_vars(self.data)
            return "struct"
        # end if
        if (not php_is_array(self.data)):
            return "string"
        # end if
        #// We have an array - is it an array or a struct?
        if self.isstruct(self.data):
            return "struct"
        else:
            return "array"
        # end if
    # end def calculatetype
    def getxml(self):
        
        
        #// Return XML for this value
        for case in Switch(self.type):
            if case("boolean"):
                return "<boolean>" + "1" if self.data else "0" + "</boolean>"
                break
            # end if
            if case("int"):
                return "<int>" + self.data + "</int>"
                break
            # end if
            if case("double"):
                return "<double>" + self.data + "</double>"
                break
            # end if
            if case("string"):
                return "<string>" + htmlspecialchars(self.data) + "</string>"
                break
            # end if
            if case("array"):
                return_ = "<array><data>" + "\n"
                for item_ in self.data:
                    return_ += "  <value>" + item_.getxml() + "</value>\n"
                # end for
                return_ += "</data></array>"
                return return_
                break
            # end if
            if case("struct"):
                return_ = "<struct>" + "\n"
                for name_,value_ in self.data:
                    name_ = htmlspecialchars(name_)
                    return_ += str("  <member><name>") + str(name_) + str("</name><value>")
                    return_ += value_.getxml() + "</value></member>\n"
                # end for
                return_ += "</struct>"
                return return_
                break
            # end if
            if case("date"):
                pass
            # end if
            if case("base64"):
                return self.data.getxml()
                break
            # end if
        # end for
        return False
    # end def getxml
    #// 
    #// Checks whether or not the supplied array is a struct or not
    #// 
    #// @param array $array
    #// @return bool
    #//
    def isstruct(self, array_=None):
        
        
        expected_ = 0
        for key_,value_ in array_:
            if php_str(key_) != php_str(expected_):
                return True
            # end if
            expected_ += 1
        # end for
        return False
    # end def isstruct
# end class IXR_Value
