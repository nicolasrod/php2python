#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
_deprecated_file(php_basename(__FILE__), "5.3.0", None, "The PHP native JSON extension is now a requirement.")
if (not php_class_exists("Services_JSON")):
    #// vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4:
    #// 
    #// Converts to and from JSON format.
    #// 
    #// JSON (JavaScript Object Notation) is a lightweight data-interchange
    #// format. It is easy for humans to read and write. It is easy for machines
    #// to parse and generate. It is based on a subset of the JavaScript
    #// Programming Language, Standard ECMA-262 3rd Edition - December 1999.
    #// This feature can also be found in  Python. JSON is a text format that is
    #// completely language independent but uses conventions that are familiar
    #// to programmers of the C-family of languages, including C, C++, C#, Java,
    #// JavaScript, Perl, TCL, and many others. These properties make JSON an
    #// ideal data-interchange language.
    #// 
    #// This package provides a simple encoder and decoder for JSON notation. It
    #// is intended for use with client-side JavaScript applications that make
    #// use of HTTPRequest to perform server communication functions - data can
    #// be encoded into JSON notation for use in a client-side javaScript, or
    #// decoded from incoming JavaScript requests. JSON format is native to
    #// JavaScript, and can be directly eval()'ed with no further parsing
    #// overhead
    #// 
    #// All strings should be in ASCII or UTF-8 format!
    #// 
    #// LICENSE: Redistribution and use in source and binary forms, with or
    #// without modification, are permitted provided that the following
    #// conditions are met: Redistributions of source code must retain the
    #// above copyright notice, this list of conditions and the following
    #// disclaimer. Redistributions in binary form must reproduce the above
    #// copyright notice, this list of conditions and the following disclaimer
    #// in the documentation and/or other materials provided with the
    #// distribution.
    #// 
    #// THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED
    #// WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
    #// MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN
    #// NO EVENT SHALL CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
    #// INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
    #// BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
    #// OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
    #// ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
    #// TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
    #// USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
    #// DAMAGE.
    #// 
    #// @category
    #// @package     Services_JSON
    #// @author      Michal Migurski <mike-json@teczno.com>
    #// @author      Matt Knapp <mdknapp[at]gmail[dot]com>
    #// @author      Brett Stimmerman <brettstimmerman[at]gmail[dot]com>
    #// @copyright   2005 Michal Migurski
    #// @version     CVS: $Id: JSON.php 305040 2010-11-02 23:19:03Z alan_k $
    #// @license     http://www.opensource.org/licenses/bsd-license.php
    #// @link        http://pear.php.net/pepr/pepr-proposal-show.php?id=198
    #// 
    #// 
    #// Marker constant for Services_JSON::decode(), used to flag stack state
    #//
    php_define("SERVICES_JSON_SLICE", 1)
    #// 
    #// Marker constant for Services_JSON::decode(), used to flag stack state
    #//
    php_define("SERVICES_JSON_IN_STR", 2)
    #// 
    #// Marker constant for Services_JSON::decode(), used to flag stack state
    #//
    php_define("SERVICES_JSON_IN_ARR", 3)
    #// 
    #// Marker constant for Services_JSON::decode(), used to flag stack state
    #//
    php_define("SERVICES_JSON_IN_OBJ", 4)
    #// 
    #// Marker constant for Services_JSON::decode(), used to flag stack state
    #//
    php_define("SERVICES_JSON_IN_CMT", 5)
    #// 
    #// Behavior switch for Services_JSON::decode()
    #//
    php_define("SERVICES_JSON_LOOSE_TYPE", 16)
    #// 
    #// Behavior switch for Services_JSON::decode()
    #//
    php_define("SERVICES_JSON_SUPPRESS_ERRORS", 32)
    #// 
    #// Behavior switch for Services_JSON::decode()
    #//
    php_define("SERVICES_JSON_USE_TO_JSON", 64)
    #// 
    #// Converts to and from JSON format.
    #// 
    #// Brief example of use:
    #// 
    #// <code>
    #// create a new instance of Services_JSON
    #// $json = new Services_JSON();
    #// 
    #// convert a complex value to JSON notation, and send it to the browser
    #// $value = array('foo', 'bar', array(1, 2, 'baz'), array(3, array(4)));
    #// $output = $json->encode($value);
    #// 
    #// print($output);
    #// prints: ["foo","bar",[1,2,"baz"],[3,[4]]]
    #// 
    #// accept incoming POST data, assumed to be in JSON notation
    #// $input = file_get_contents('php://input', 1000000);
    #// $value = $json->decode($input);
    #// </code>
    #//
    class Services_JSON():
        #// 
        #// constructs a new JSON instance
        #// 
        #// @deprecated 5.3.0 Use the PHP native JSON extension instead.
        #// 
        #// @param    int     $use    object behavior flags; combine with boolean-OR
        #// 
        #// possible values:
        #// - SERVICES_JSON_LOOSE_TYPE:  loose typing.
        #// "{...}" syntax creates associative arrays
        #// instead of objects in decode().
        #// - SERVICES_JSON_SUPPRESS_ERRORS:  error suppression.
        #// Values which can't be encoded (e.g. resources)
        #// appear as NULL instead of throwing errors.
        #// By default, a deeply-nested resource will
        #// bubble up with an error, so all return values
        #// from encode() should be checked with isError()
        #// - SERVICES_JSON_USE_TO_JSON:  call toJSON when serializing objects
        #// It serializes the return value from the toJSON call rather
        #// than the object itself, toJSON can return associative arrays,
        #// strings or numbers, if you return an object, make sure it does
        #// not have a toJSON method, otherwise an error will occur.
        #//
        def __init__(self, use_=0):
            
            
            _deprecated_function(__METHOD__, "5.3.0", "The PHP native JSON extension")
            self.use = use_
            self._mb_strlen = php_function_exists("mb_strlen")
            self._mb_convert_encoding = php_function_exists("mb_convert_encoding")
            self._mb_substr = php_function_exists("mb_substr")
        # end def __init__
        #// 
        #// PHP4 constructor.
        #// 
        #// @deprecated 5.3.0 Use __construct() instead.
        #// 
        #// @see Services_JSON::__construct()
        #//
        def services_json(self, use_=0):
            
            
            _deprecated_constructor("Services_JSON", "5.3.0", get_class(self))
            self.__init__(use_)
        # end def services_json
        #// private - cache the mbstring lookup results..
        _mb_strlen = False
        _mb_substr = False
        _mb_convert_encoding = False
        #// 
        #// convert a string from one UTF-16 char to one UTF-8 char
        #// 
        #// Normally should be handled by mb_convert_encoding, but
        #// provides a slower PHP-only method for installations
        #// that lack the multibye string extension.
        #// 
        #// @deprecated 5.3.0 Use the PHP native JSON extension instead.
        #// 
        #// @param    string  $utf16  UTF-16 character
        #// @return   string  UTF-8 character
        #// @access   private
        #//
        def utf162utf8(self, utf16_=None):
            
            
            _deprecated_function(__METHOD__, "5.3.0", "The PHP native JSON extension")
            #// oh please oh please oh please oh please oh please
            if self._mb_convert_encoding:
                return mb_convert_encoding(utf16_, "UTF-8", "UTF-16")
            # end if
            bytes_ = php_ord(utf16_[0]) << 8 | php_ord(utf16_[1])
            for case in Switch(True):
                if case(127 & bytes_ == bytes_):
                    #// this case should never be reached, because we are in ASCII range
                    #// see: http://www.cl.cam.ac.uk/~mgk25/unicode.html#utf-8
                    return chr(127 & bytes_)
                # end if
                if case(2047 & bytes_ == bytes_):
                    #// return a 2-byte UTF-8 character
                    #// see: http://www.cl.cam.ac.uk/~mgk25/unicode.html#utf-8
                    return chr(192 | bytes_ >> 6 & 31) + chr(128 | bytes_ & 63)
                # end if
                if case(65535 & bytes_ == bytes_):
                    #// return a 3-byte UTF-8 character
                    #// see: http://www.cl.cam.ac.uk/~mgk25/unicode.html#utf-8
                    return chr(224 | bytes_ >> 12 & 15) + chr(128 | bytes_ >> 6 & 63) + chr(128 | bytes_ & 63)
                # end if
            # end for
            #// ignoring UTF-32 for now, sorry
            return ""
        # end def utf162utf8
        #// 
        #// convert a string from one UTF-8 char to one UTF-16 char
        #// 
        #// Normally should be handled by mb_convert_encoding, but
        #// provides a slower PHP-only method for installations
        #// that lack the multibyte string extension.
        #// 
        #// @deprecated 5.3.0 Use the PHP native JSON extension instead.
        #// 
        #// @param    string  $utf8   UTF-8 character
        #// @return   string  UTF-16 character
        #// @access   private
        #//
        def utf82utf16(self, utf8_=None):
            
            
            _deprecated_function(__METHOD__, "5.3.0", "The PHP native JSON extension")
            #// oh please oh please oh please oh please oh please
            if self._mb_convert_encoding:
                return mb_convert_encoding(utf8_, "UTF-16", "UTF-8")
            # end if
            for case in Switch(self.strlen8(utf8_)):
                if case(1):
                    #// this case should never be reached, because we are in ASCII range
                    #// see: http://www.cl.cam.ac.uk/~mgk25/unicode.html#utf-8
                    return utf8_
                # end if
                if case(2):
                    #// return a UTF-16 character from a 2-byte UTF-8 char
                    #// see: http://www.cl.cam.ac.uk/~mgk25/unicode.html#utf-8
                    return chr(7 & php_ord(utf8_[0]) >> 2) + chr(192 & php_ord(utf8_[0]) << 6 | 63 & php_ord(utf8_[1]))
                # end if
                if case(3):
                    #// return a UTF-16 character from a 3-byte UTF-8 char
                    #// see: http://www.cl.cam.ac.uk/~mgk25/unicode.html#utf-8
                    return chr(240 & php_ord(utf8_[0]) << 4 | 15 & php_ord(utf8_[1]) >> 2) + chr(192 & php_ord(utf8_[1]) << 6 | 127 & php_ord(utf8_[2]))
                # end if
            # end for
            #// ignoring UTF-32 for now, sorry
            return ""
        # end def utf82utf16
        #// 
        #// encodes an arbitrary variable into JSON format (and sends JSON Header)
        #// 
        #// @deprecated 5.3.0 Use the PHP native JSON extension instead.
        #// 
        #// @param    mixed   $var    any number, boolean, string, array, or object to be encoded.
        #// see argument 1 to Services_JSON() above for array-parsing behavior.
        #// if var is a string, note that encode() always expects it
        #// to be in ASCII or UTF-8 format!
        #// 
        #// @return   mixed   JSON string representation of input var or an error if a problem occurs
        #// @access   public
        #//
        def encode(self, var_=None):
            
            
            _deprecated_function(__METHOD__, "5.3.0", "The PHP native JSON extension")
            php_header("Content-type: application/json")
            return self.encodeunsafe(var_)
        # end def encode
        #// 
        #// encodes an arbitrary variable into JSON format without JSON Header - warning - may allow XSS!!!!)
        #// 
        #// @deprecated 5.3.0 Use the PHP native JSON extension instead.
        #// 
        #// @param    mixed   $var    any number, boolean, string, array, or object to be encoded.
        #// see argument 1 to Services_JSON() above for array-parsing behavior.
        #// if var is a string, note that encode() always expects it
        #// to be in ASCII or UTF-8 format!
        #// 
        #// @return   mixed   JSON string representation of input var or an error if a problem occurs
        #// @access   public
        #//
        def encodeunsafe(self, var_=None):
            
            
            _deprecated_function(__METHOD__, "5.3.0", "The PHP native JSON extension")
            #// see bug #16908 - regarding numeric locale printing
            lc_ = setlocale(LC_NUMERIC, 0)
            setlocale(LC_NUMERIC, "C")
            ret_ = self._encode(var_)
            setlocale(LC_NUMERIC, lc_)
            return ret_
        # end def encodeunsafe
        #// 
        #// PRIVATE CODE that does the work of encodes an arbitrary variable into JSON format
        #// 
        #// @deprecated 5.3.0 Use the PHP native JSON extension instead.
        #// 
        #// @param    mixed   $var    any number, boolean, string, array, or object to be encoded.
        #// see argument 1 to Services_JSON() above for array-parsing behavior.
        #// if var is a string, note that encode() always expects it
        #// to be in ASCII or UTF-8 format!
        #// 
        #// @return   mixed   JSON string representation of input var or an error if a problem occurs
        #// @access   public
        #//
        def _encode(self, var_=None):
            
            
            _deprecated_function(__METHOD__, "5.3.0", "The PHP native JSON extension")
            for case in Switch(gettype(var_)):
                if case("boolean"):
                    return "true" if var_ else "false"
                # end if
                if case("NULL"):
                    return "null"
                # end if
                if case("integer"):
                    return php_int(var_)
                # end if
                if case("double"):
                    pass
                # end if
                if case("float"):
                    return php_float(var_)
                # end if
                if case("string"):
                    #// STRINGS ARE EXPECTED TO BE IN ASCII OR UTF-8 FORMAT
                    ascii_ = ""
                    strlen_var_ = self.strlen8(var_)
                    #// 
                    #// Iterate over every character in the string,
                    #// escaping with a slash or encoding to UTF-8 where necessary
                    #//
                    c_ = 0
                    while c_ < strlen_var_:
                        
                        ord_var_c_ = php_ord(var_[c_])
                        for case in Switch(True):
                            if case(ord_var_c_ == 8):
                                ascii_ += "\\b"
                                break
                            # end if
                            if case(ord_var_c_ == 9):
                                ascii_ += "\\t"
                                break
                            # end if
                            if case(ord_var_c_ == 10):
                                ascii_ += "\\n"
                                break
                            # end if
                            if case(ord_var_c_ == 12):
                                ascii_ += "\\f"
                                break
                            # end if
                            if case(ord_var_c_ == 13):
                                ascii_ += "\\r"
                                break
                            # end if
                            if case(ord_var_c_ == 34):
                                pass
                            # end if
                            if case(ord_var_c_ == 47):
                                pass
                            # end if
                            if case(ord_var_c_ == 92):
                                #// double quote, slash, slosh
                                ascii_ += "\\" + var_[c_]
                                break
                            # end if
                            if case(ord_var_c_ >= 32 and ord_var_c_ <= 127):
                                #// characters U-00000000 - U-0000007F (same as ASCII)
                                ascii_ += var_[c_]
                                break
                            # end if
                            if case(ord_var_c_ & 224 == 192):
                                #// characters U-00000080 - U-000007FF, mask 110XXXXX
                                #// see http://www.cl.cam.ac.uk/~mgk25/unicode.html#utf-8
                                if c_ + 1 >= strlen_var_:
                                    c_ += 1
                                    ascii_ += "?"
                                    break
                                # end if
                                char_ = pack("C*", ord_var_c_, php_ord(var_[c_ + 1]))
                                c_ += 1
                                utf16_ = self.utf82utf16(char_)
                                ascii_ += php_sprintf("\\u%04s", bin2hex(utf16_))
                                break
                            # end if
                            if case(ord_var_c_ & 240 == 224):
                                if c_ + 2 >= strlen_var_:
                                    c_ += 2
                                    ascii_ += "?"
                                    break
                                # end if
                                #// characters U-00000800 - U-0000FFFF, mask 1110XXXX
                                #// see http://www.cl.cam.ac.uk/~mgk25/unicode.html#utf-8
                                char_ = pack("C*", ord_var_c_, php_no_error(lambda: php_ord(var_[c_ + 1])), php_no_error(lambda: php_ord(var_[c_ + 2])))
                                c_ += 2
                                utf16_ = self.utf82utf16(char_)
                                ascii_ += php_sprintf("\\u%04s", bin2hex(utf16_))
                                break
                            # end if
                            if case(ord_var_c_ & 248 == 240):
                                if c_ + 3 >= strlen_var_:
                                    c_ += 3
                                    ascii_ += "?"
                                    break
                                # end if
                                #// characters U-00010000 - U-001FFFFF, mask 11110XXX
                                #// see http://www.cl.cam.ac.uk/~mgk25/unicode.html#utf-8
                                char_ = pack("C*", ord_var_c_, php_ord(var_[c_ + 1]), php_ord(var_[c_ + 2]), php_ord(var_[c_ + 3]))
                                c_ += 3
                                utf16_ = self.utf82utf16(char_)
                                ascii_ += php_sprintf("\\u%04s", bin2hex(utf16_))
                                break
                            # end if
                            if case(ord_var_c_ & 252 == 248):
                                #// characters U-00200000 - U-03FFFFFF, mask 111110XX
                                #// see http://www.cl.cam.ac.uk/~mgk25/unicode.html#utf-8
                                if c_ + 4 >= strlen_var_:
                                    c_ += 4
                                    ascii_ += "?"
                                    break
                                # end if
                                char_ = pack("C*", ord_var_c_, php_ord(var_[c_ + 1]), php_ord(var_[c_ + 2]), php_ord(var_[c_ + 3]), php_ord(var_[c_ + 4]))
                                c_ += 4
                                utf16_ = self.utf82utf16(char_)
                                ascii_ += php_sprintf("\\u%04s", bin2hex(utf16_))
                                break
                            # end if
                            if case(ord_var_c_ & 254 == 252):
                                if c_ + 5 >= strlen_var_:
                                    c_ += 5
                                    ascii_ += "?"
                                    break
                                # end if
                                #// characters U-04000000 - U-7FFFFFFF, mask 1111110X
                                #// see http://www.cl.cam.ac.uk/~mgk25/unicode.html#utf-8
                                char_ = pack("C*", ord_var_c_, php_ord(var_[c_ + 1]), php_ord(var_[c_ + 2]), php_ord(var_[c_ + 3]), php_ord(var_[c_ + 4]), php_ord(var_[c_ + 5]))
                                c_ += 5
                                utf16_ = self.utf82utf16(char_)
                                ascii_ += php_sprintf("\\u%04s", bin2hex(utf16_))
                                break
                            # end if
                        # end for
                        c_ += 1
                    # end while
                    return "\"" + ascii_ + "\""
                # end if
                if case("array"):
                    #// 
                    #// As per JSON spec if any array key is not an integer
                    #// we must treat the whole array as an object. We
                    #// also try to catch a sparsely populated associative
                    #// array with numeric keys here because some JS engines
                    #// will create an array with empty indexes up to
                    #// max_index which can cause memory issues and because
                    #// the keys, which may be relevant, will be remapped
                    #// otherwise.
                    #// 
                    #// As per the ECMA and JSON specification an object may
                    #// have any string as a property. Unfortunately due to
                    #// a hole in the ECMA specification if the key is a
                    #// ECMA reserved word or starts with a digit the
                    #// parameter is only accessible using ECMAScript's
                    #// bracket notation.
                    #// 
                    #// treat as a JSON object
                    if php_is_array(var_) and php_count(var_) and php_array_keys(var_) != range(0, sizeof(var_) - 1):
                        properties_ = php_array_map(Array(self, "name_value"), php_array_keys(var_), php_array_values(var_))
                        for property_ in properties_:
                            if Services_JSON.iserror(property_):
                                return property_
                            # end if
                        # end for
                        return "{" + join(",", properties_) + "}"
                    # end if
                    #// treat it like a regular array
                    elements_ = php_array_map(Array(self, "_encode"), var_)
                    for element_ in elements_:
                        if Services_JSON.iserror(element_):
                            return element_
                        # end if
                    # end for
                    return "[" + join(",", elements_) + "]"
                # end if
                if case("object"):
                    #// support toJSON methods.
                    if self.use & SERVICES_JSON_USE_TO_JSON and php_method_exists(var_, "toJSON"):
                        #// this may end up allowing unlimited recursion
                        #// so we check the return value to make sure it's not got the same method.
                        recode_ = var_.tojson()
                        if php_method_exists(recode_, "toJSON"):
                            return "null" if self.use & SERVICES_JSON_SUPPRESS_ERRORS else php_new_class("Services_JSON_Error", lambda : Services_JSON_Error(get_class(var_) + " toJSON returned an object with a toJSON method."))
                        # end if
                        return self._encode(recode_)
                    # end if
                    vars_ = get_object_vars(var_)
                    properties_ = php_array_map(Array(self, "name_value"), php_array_keys(vars_), php_array_values(vars_))
                    for property_ in properties_:
                        if Services_JSON.iserror(property_):
                            return property_
                        # end if
                    # end for
                    return "{" + join(",", properties_) + "}"
                # end if
                if case():
                    return "null" if self.use & SERVICES_JSON_SUPPRESS_ERRORS else php_new_class("Services_JSON_Error", lambda : Services_JSON_Error(gettype(var_) + " can not be encoded as JSON string"))
                # end if
            # end for
        # end def _encode
        #// 
        #// array-walking function for use in generating JSON-formatted name-value pairs
        #// 
        #// @deprecated 5.3.0 Use the PHP native JSON extension instead.
        #// 
        #// @param    string  $name   name of key to use
        #// @param    mixed   $value  reference to an array element to be encoded
        #// 
        #// @return   string  JSON-formatted name-value pair, like '"name":value'
        #// @access   private
        #//
        def name_value(self, name_=None, value_=None):
            
            
            _deprecated_function(__METHOD__, "5.3.0", "The PHP native JSON extension")
            encoded_value_ = self._encode(value_)
            if Services_JSON.iserror(encoded_value_):
                return encoded_value_
            # end if
            return self._encode(php_strval(name_)) + ":" + encoded_value_
        # end def name_value
        #// 
        #// reduce a string by removing leading and trailing comments and whitespace
        #// 
        #// @deprecated 5.3.0 Use the PHP native JSON extension instead.
        #// 
        #// @param    $str    string      string value to strip of comments and whitespace
        #// 
        #// @return   string  string value stripped of comments and whitespace
        #// @access   private
        #//
        def reduce_string(self, str_=None):
            
            
            _deprecated_function(__METHOD__, "5.3.0", "The PHP native JSON extension")
            str_ = php_preg_replace(Array("#^\\s*//(.+)$#m", "#^\\s*/\\*(.+)\\*/#Us", "#/\\*(.+)\\*/\\s*$#Us"), "", str_)
            #// eliminate extraneous space
            return php_trim(str_)
        # end def reduce_string
        #// 
        #// decodes a JSON string into appropriate variable
        #// 
        #// @deprecated 5.3.0 Use the PHP native JSON extension instead.
        #// 
        #// @param    string  $str    JSON-formatted string
        #// 
        #// @return   mixed   number, boolean, string, array, or object
        #// corresponding to given JSON input string.
        #// See argument 1 to Services_JSON() above for object-output behavior.
        #// Note that decode() always returns strings
        #// in ASCII or UTF-8 format!
        #// @access   public
        #//
        def decode(self, str_=None):
            
            
            _deprecated_function(__METHOD__, "5.3.0", "The PHP native JSON extension")
            str_ = self.reduce_string(str_)
            for case in Switch(php_strtolower(str_)):
                if case("true"):
                    return True
                # end if
                if case("false"):
                    return False
                # end if
                if case("null"):
                    return None
                # end if
                if case():
                    m_ = Array()
                    if php_is_numeric(str_):
                        #// Lookie-loo, it's a number
                        #// This would work on its own, but I'm trying to be
                        #// good about returning integers where appropriate:
                        #// return (float)$str;
                        #// Return float or int, as appropriate
                        return php_int(str_) if php_float(str_) == php_int(str_) else php_float(str_)
                    elif php_preg_match("/^(\"|').*(\\1)$/s", str_, m_) and m_[1] == m_[2]:
                        #// STRINGS RETURNED IN UTF-8 FORMAT
                        delim_ = self.substr8(str_, 0, 1)
                        chrs_ = self.substr8(str_, 1, -1)
                        utf8_ = ""
                        strlen_chrs_ = self.strlen8(chrs_)
                        c_ = 0
                        while c_ < strlen_chrs_:
                            
                            substr_chrs_c_2_ = self.substr8(chrs_, c_, 2)
                            ord_chrs_c_ = php_ord(chrs_[c_])
                            for case in Switch(True):
                                if case(substr_chrs_c_2_ == "\\b"):
                                    utf8_ += chr(8)
                                    c_ += 1
                                    break
                                # end if
                                if case(substr_chrs_c_2_ == "\\t"):
                                    utf8_ += chr(9)
                                    c_ += 1
                                    break
                                # end if
                                if case(substr_chrs_c_2_ == "\\n"):
                                    utf8_ += chr(10)
                                    c_ += 1
                                    break
                                # end if
                                if case(substr_chrs_c_2_ == "\\f"):
                                    utf8_ += chr(12)
                                    c_ += 1
                                    break
                                # end if
                                if case(substr_chrs_c_2_ == "\\r"):
                                    utf8_ += chr(13)
                                    c_ += 1
                                    break
                                # end if
                                if case(substr_chrs_c_2_ == "\\\""):
                                    pass
                                # end if
                                if case(substr_chrs_c_2_ == "\\'"):
                                    pass
                                # end if
                                if case(substr_chrs_c_2_ == "\\\\"):
                                    pass
                                # end if
                                if case(substr_chrs_c_2_ == "\\/"):
                                    if delim_ == "\"" and substr_chrs_c_2_ != "\\'" or delim_ == "'" and substr_chrs_c_2_ != "\\\"":
                                        c_ += 1
                                        utf8_ += chrs_[c_]
                                    # end if
                                    break
                                # end if
                                if case(php_preg_match("/\\\\u[0-9A-F]{4}/i", self.substr8(chrs_, c_, 6))):
                                    #// single, escaped unicode character
                                    utf16_ = chr(hexdec(self.substr8(chrs_, c_ + 2, 2))) + chr(hexdec(self.substr8(chrs_, c_ + 4, 2)))
                                    utf8_ += self.utf162utf8(utf16_)
                                    c_ += 5
                                    break
                                # end if
                                if case(ord_chrs_c_ >= 32 and ord_chrs_c_ <= 127):
                                    utf8_ += chrs_[c_]
                                    break
                                # end if
                                if case(ord_chrs_c_ & 224 == 192):
                                    #// characters U-00000080 - U-000007FF, mask 110XXXXX
                                    #// see http://www.cl.cam.ac.uk/~mgk25/unicode.html#utf-8
                                    utf8_ += self.substr8(chrs_, c_, 2)
                                    c_ += 1
                                    break
                                # end if
                                if case(ord_chrs_c_ & 240 == 224):
                                    #// characters U-00000800 - U-0000FFFF, mask 1110XXXX
                                    #// see http://www.cl.cam.ac.uk/~mgk25/unicode.html#utf-8
                                    utf8_ += self.substr8(chrs_, c_, 3)
                                    c_ += 2
                                    break
                                # end if
                                if case(ord_chrs_c_ & 248 == 240):
                                    #// characters U-00010000 - U-001FFFFF, mask 11110XXX
                                    #// see http://www.cl.cam.ac.uk/~mgk25/unicode.html#utf-8
                                    utf8_ += self.substr8(chrs_, c_, 4)
                                    c_ += 3
                                    break
                                # end if
                                if case(ord_chrs_c_ & 252 == 248):
                                    #// characters U-00200000 - U-03FFFFFF, mask 111110XX
                                    #// see http://www.cl.cam.ac.uk/~mgk25/unicode.html#utf-8
                                    utf8_ += self.substr8(chrs_, c_, 5)
                                    c_ += 4
                                    break
                                # end if
                                if case(ord_chrs_c_ & 254 == 252):
                                    #// characters U-04000000 - U-7FFFFFFF, mask 1111110X
                                    #// see http://www.cl.cam.ac.uk/~mgk25/unicode.html#utf-8
                                    utf8_ += self.substr8(chrs_, c_, 6)
                                    c_ += 5
                                    break
                                # end if
                            # end for
                            c_ += 1
                        # end while
                        return utf8_
                    elif php_preg_match("/^\\[.*\\]$/s", str_) or php_preg_match("/^\\{.*\\}$/s", str_):
                        #// array, or object notation
                        if str_[0] == "[":
                            stk_ = Array(SERVICES_JSON_IN_ARR)
                            arr_ = Array()
                        else:
                            if self.use & SERVICES_JSON_LOOSE_TYPE:
                                stk_ = Array(SERVICES_JSON_IN_OBJ)
                                obj_ = Array()
                            else:
                                stk_ = Array(SERVICES_JSON_IN_OBJ)
                                obj_ = php_new_class("stdClass", lambda : stdClass())
                            # end if
                        # end if
                        php_array_push(stk_, Array({"what": SERVICES_JSON_SLICE, "where": 0, "delim": False}))
                        chrs_ = self.substr8(str_, 1, -1)
                        chrs_ = self.reduce_string(chrs_)
                        if chrs_ == "":
                            if reset(stk_) == SERVICES_JSON_IN_ARR:
                                return arr_
                            else:
                                return obj_
                            # end if
                        # end if
                        #// print("\nparsing {$chrs}\n");
                        strlen_chrs_ = self.strlen8(chrs_)
                        c_ = 0
                        while c_ <= strlen_chrs_:
                            
                            top_ = php_end(stk_)
                            substr_chrs_c_2_ = self.substr8(chrs_, c_, 2)
                            if c_ == strlen_chrs_ or chrs_[c_] == "," and top_["what"] == SERVICES_JSON_SLICE:
                                #// found a comma that is not inside a string, array, etc.,
                                #// OR we've reached the end of the character list
                                slice_ = self.substr8(chrs_, top_["where"], c_ - top_["where"])
                                php_array_push(stk_, Array({"what": SERVICES_JSON_SLICE, "where": c_ + 1, "delim": False}))
                                #// print("Found split at {$c}: ".$this->substr8($chrs, $top['where'], (1 + $c - $top['where']))."\n");
                                if reset(stk_) == SERVICES_JSON_IN_ARR:
                                    #// we are in an array, so just push an element onto the stack
                                    php_array_push(arr_, self.decode(slice_))
                                elif reset(stk_) == SERVICES_JSON_IN_OBJ:
                                    #// we are in an object, so figure
                                    #// out the property name and set an
                                    #// element in an associative array,
                                    #// for now
                                    parts_ = Array()
                                    if php_preg_match("/^\\s*([\"'].*[^\\\\][\"'])\\s*:/Uis", slice_, parts_):
                                        #// "name":value pair
                                        key_ = self.decode(parts_[1])
                                        val_ = self.decode(php_trim(php_substr(slice_, php_strlen(parts_[0])), ",   \n\r "))
                                        if self.use & SERVICES_JSON_LOOSE_TYPE:
                                            obj_[key_] = val_
                                        else:
                                            obj_.key_ = val_
                                        # end if
                                    elif php_preg_match("/^\\s*(\\w+)\\s*:/Uis", slice_, parts_):
                                        #// name:value pair, where name is unquoted
                                        key_ = parts_[1]
                                        val_ = self.decode(php_trim(php_substr(slice_, php_strlen(parts_[0])), ",   \n\r "))
                                        if self.use & SERVICES_JSON_LOOSE_TYPE:
                                            obj_[key_] = val_
                                        else:
                                            obj_.key_ = val_
                                        # end if
                                    # end if
                                # end if
                            elif chrs_[c_] == "\"" or chrs_[c_] == "'" and top_["what"] != SERVICES_JSON_IN_STR:
                                #// found a quote, and we are not inside a string
                                php_array_push(stk_, Array({"what": SERVICES_JSON_IN_STR, "where": c_, "delim": chrs_[c_]}))
                                pass
                            elif chrs_[c_] == top_["delim"] and top_["what"] == SERVICES_JSON_IN_STR and self.strlen8(self.substr8(chrs_, 0, c_)) - self.strlen8(php_rtrim(self.substr8(chrs_, 0, c_), "\\")) % 2 != 1:
                                #// found a quote, we're in a string, and it's not escaped
                                #// we know that it's not escaped because there is _not_ an
                                #// odd number of backslashes at the end of the string so far
                                php_array_pop(stk_)
                                pass
                            elif chrs_[c_] == "[" and php_in_array(top_["what"], Array(SERVICES_JSON_SLICE, SERVICES_JSON_IN_ARR, SERVICES_JSON_IN_OBJ)):
                                #// found a left-bracket, and we are in an array, object, or slice
                                php_array_push(stk_, Array({"what": SERVICES_JSON_IN_ARR, "where": c_, "delim": False}))
                                pass
                            elif chrs_[c_] == "]" and top_["what"] == SERVICES_JSON_IN_ARR:
                                #// found a right-bracket, and we're in an array
                                php_array_pop(stk_)
                                pass
                            elif chrs_[c_] == "{" and php_in_array(top_["what"], Array(SERVICES_JSON_SLICE, SERVICES_JSON_IN_ARR, SERVICES_JSON_IN_OBJ)):
                                #// found a left-brace, and we are in an array, object, or slice
                                php_array_push(stk_, Array({"what": SERVICES_JSON_IN_OBJ, "where": c_, "delim": False}))
                                pass
                            elif chrs_[c_] == "}" and top_["what"] == SERVICES_JSON_IN_OBJ:
                                #// found a right-brace, and we're in an object
                                php_array_pop(stk_)
                                pass
                            elif substr_chrs_c_2_ == "/*" and php_in_array(top_["what"], Array(SERVICES_JSON_SLICE, SERVICES_JSON_IN_ARR, SERVICES_JSON_IN_OBJ)):
                                #// found a comment start, and we are in an array, object, or slice
                                php_array_push(stk_, Array({"what": SERVICES_JSON_IN_CMT, "where": c_, "delim": False}))
                                c_ += 1
                                pass
                            elif substr_chrs_c_2_ == "*/" and top_["what"] == SERVICES_JSON_IN_CMT:
                                #// found a comment end, and we're in one now
                                php_array_pop(stk_)
                                c_ += 1
                                i_ = top_["where"]
                                while i_ <= c_:
                                    
                                    chrs_ = php_substr_replace(chrs_, " ", i_, 1)
                                    i_ += 1
                                # end while
                                pass
                            # end if
                            c_ += 1
                        # end while
                        if reset(stk_) == SERVICES_JSON_IN_ARR:
                            return arr_
                        elif reset(stk_) == SERVICES_JSON_IN_OBJ:
                            return obj_
                        # end if
                    # end if
                # end if
            # end for
        # end def decode
        #// 
        #// @deprecated 5.3.0 Use the PHP native JSON extension instead.
        #// 
        #// @todo Ultimately, this should just call PEAR::isError()
        #//
        def iserror(self, data_=None, code_=None):
            if code_ is None:
                code_ = None
            # end if
            
            _deprecated_function(__METHOD__, "5.3.0", "The PHP native JSON extension")
            if php_class_exists("pear"):
                return PEAR.iserror(data_, code_)
            elif php_is_object(data_) and get_class(data_) == "services_json_error" or is_subclass_of(data_, "services_json_error"):
                return True
            # end if
            return False
        # end def iserror
        #// 
        #// Calculates length of string in bytes
        #// 
        #// @deprecated 5.3.0 Use the PHP native JSON extension instead.
        #// 
        #// @param string
        #// @return integer length
        #//
        def strlen8(self, str_=None):
            
            
            _deprecated_function(__METHOD__, "5.3.0", "The PHP native JSON extension")
            if self._mb_strlen:
                return php_mb_strlen(str_, "8bit")
            # end if
            return php_strlen(str_)
        # end def strlen8
        #// 
        #// Returns part of a string, interpreting $start and $length as number of bytes.
        #// 
        #// @deprecated 5.3.0 Use the PHP native JSON extension instead.
        #// 
        #// @param string
        #// @param integer start
        #// @param integer length
        #// @return integer length
        #//
        def substr8(self, string_=None, start_=None, length_=None):
            if length_ is None:
                length_ = False
            # end if
            
            _deprecated_function(__METHOD__, "5.3.0", "The PHP native JSON extension")
            if length_ == False:
                length_ = self.strlen8(string_) - start_
            # end if
            if self._mb_substr:
                return php_mb_substr(string_, start_, length_, "8bit")
            # end if
            return php_substr(string_, start_, length_)
        # end def substr8
    # end class Services_JSON
    if php_class_exists("PEAR_Error"):
        class Services_JSON_Error(PEAR_Error):
            #// 
            #// PHP5 constructor.
            #// 
            #// @deprecated 5.3.0 Use the PHP native JSON extension instead.
            #//
            def __init__(self, message_="unknown error", code_=None, mode_=None, options_=None, userinfo_=None):
                if code_ is None:
                    code_ = None
                # end if
                if mode_ is None:
                    mode_ = None
                # end if
                if options_ is None:
                    options_ = None
                # end if
                if userinfo_ is None:
                    userinfo_ = None
                # end if
                
                _deprecated_function(__METHOD__, "5.3.0", "The PHP native JSON extension")
                super().pear_error(message_, code_, mode_, options_, userinfo_)
            # end def __init__
            #// 
            #// PHP4 constructor.
            #// 
            #// @deprecated 5.3.0 Use __construct() instead.
            #// 
            #// @see Services_JSON_Error::__construct()
            #//
            def services_json_error(self, message_="unknown error", code_=None, mode_=None, options_=None, userinfo_=None):
                if code_ is None:
                    code_ = None
                # end if
                if mode_ is None:
                    mode_ = None
                # end if
                if options_ is None:
                    options_ = None
                # end if
                if userinfo_ is None:
                    userinfo_ = None
                # end if
                
                _deprecated_constructor("Services_JSON_Error", "5.3.0", get_class(self))
                self.__init__(message_, code_, mode_, options_, userinfo_)
            # end def services_json_error
        # end class Services_JSON_Error
    else:
        #// 
        #// @todo Ultimately, this class shall be descended from PEAR_Error
        #//
        class Services_JSON_Error():
            #// 
            #// PHP5 constructor.
            #// 
            #// @deprecated 5.3.0 Use the PHP native JSON extension instead.
            #//
            def __init__(self, message_="unknown error", code_=None, mode_=None, options_=None, userinfo_=None):
                if code_ is None:
                    code_ = None
                # end if
                if mode_ is None:
                    mode_ = None
                # end if
                if options_ is None:
                    options_ = None
                # end if
                if userinfo_ is None:
                    userinfo_ = None
                # end if
                
                _deprecated_function(__METHOD__, "5.3.0", "The PHP native JSON extension")
            # end def __init__
            #// 
            #// PHP4 constructor.
            #// 
            #// @deprecated 5.3.0 Use __construct() instead.
            #// 
            #// @see Services_JSON_Error::__construct()
            #//
            def services_json_error(self, message_="unknown error", code_=None, mode_=None, options_=None, userinfo_=None):
                if code_ is None:
                    code_ = None
                # end if
                if mode_ is None:
                    mode_ = None
                # end if
                if options_ is None:
                    options_ = None
                # end if
                if userinfo_ is None:
                    userinfo_ = None
                # end if
                
                _deprecated_constructor("Services_JSON_Error", "5.3.0", get_class(self))
                self.__init__(message_, code_, mode_, options_, userinfo_)
            # end def services_json_error
        # end class Services_JSON_Error
    # end if
# end if
