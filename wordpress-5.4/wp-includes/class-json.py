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
        def __init__(self, use=0):
            
            _deprecated_function(__METHOD__, "5.3.0", "The PHP native JSON extension")
            self.use = use
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
        def services_json(self, use=0):
            
            _deprecated_constructor("Services_JSON", "5.3.0", get_class(self))
            self.__init__(use)
        # end def services_json
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
        def utf162utf8(self, utf16=None):
            
            _deprecated_function(__METHOD__, "5.3.0", "The PHP native JSON extension")
            #// oh please oh please oh please oh please oh please
            if self._mb_convert_encoding:
                return mb_convert_encoding(utf16, "UTF-8", "UTF-16")
            # end if
            bytes = php_ord(utf16[0]) << 8 | php_ord(utf16[1])
            for case in Switch(True):
                if case(127 & bytes == bytes):
                    #// this case should never be reached, because we are in ASCII range
                    #// see: http://www.cl.cam.ac.uk/~mgk25/unicode.html#utf-8
                    return chr(127 & bytes)
                # end if
                if case(2047 & bytes == bytes):
                    #// return a 2-byte UTF-8 character
                    #// see: http://www.cl.cam.ac.uk/~mgk25/unicode.html#utf-8
                    return chr(192 | bytes >> 6 & 31) + chr(128 | bytes & 63)
                # end if
                if case(65535 & bytes == bytes):
                    #// return a 3-byte UTF-8 character
                    #// see: http://www.cl.cam.ac.uk/~mgk25/unicode.html#utf-8
                    return chr(224 | bytes >> 12 & 15) + chr(128 | bytes >> 6 & 63) + chr(128 | bytes & 63)
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
        def utf82utf16(self, utf8=None):
            
            _deprecated_function(__METHOD__, "5.3.0", "The PHP native JSON extension")
            #// oh please oh please oh please oh please oh please
            if self._mb_convert_encoding:
                return mb_convert_encoding(utf8, "UTF-16", "UTF-8")
            # end if
            for case in Switch(self.strlen8(utf8)):
                if case(1):
                    #// this case should never be reached, because we are in ASCII range
                    #// see: http://www.cl.cam.ac.uk/~mgk25/unicode.html#utf-8
                    return utf8
                # end if
                if case(2):
                    #// return a UTF-16 character from a 2-byte UTF-8 char
                    #// see: http://www.cl.cam.ac.uk/~mgk25/unicode.html#utf-8
                    return chr(7 & php_ord(utf8[0]) >> 2) + chr(192 & php_ord(utf8[0]) << 6 | 63 & php_ord(utf8[1]))
                # end if
                if case(3):
                    #// return a UTF-16 character from a 3-byte UTF-8 char
                    #// see: http://www.cl.cam.ac.uk/~mgk25/unicode.html#utf-8
                    return chr(240 & php_ord(utf8[0]) << 4 | 15 & php_ord(utf8[1]) >> 2) + chr(192 & php_ord(utf8[1]) << 6 | 127 & php_ord(utf8[2]))
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
        def encode(self, var=None):
            
            _deprecated_function(__METHOD__, "5.3.0", "The PHP native JSON extension")
            php_header("Content-type: application/json")
            return self.encodeunsafe(var)
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
        def encodeunsafe(self, var=None):
            
            _deprecated_function(__METHOD__, "5.3.0", "The PHP native JSON extension")
            #// see bug #16908 - regarding numeric locale printing
            lc = setlocale(LC_NUMERIC, 0)
            setlocale(LC_NUMERIC, "C")
            ret = self._encode(var)
            setlocale(LC_NUMERIC, lc)
            return ret
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
        def _encode(self, var=None):
            
            _deprecated_function(__METHOD__, "5.3.0", "The PHP native JSON extension")
            for case in Switch(gettype(var)):
                if case("boolean"):
                    return "true" if var else "false"
                # end if
                if case("NULL"):
                    return "null"
                # end if
                if case("integer"):
                    return int(var)
                # end if
                if case("double"):
                    pass
                # end if
                if case("float"):
                    return float(var)
                # end if
                if case("string"):
                    #// STRINGS ARE EXPECTED TO BE IN ASCII OR UTF-8 FORMAT
                    ascii = ""
                    strlen_var = self.strlen8(var)
                    #// 
                    #// Iterate over every character in the string,
                    #// escaping with a slash or encoding to UTF-8 where necessary
                    #//
                    c = 0
                    while c < strlen_var:
                        
                        ord_var_c = php_ord(var[c])
                        for case in Switch(True):
                            if case(ord_var_c == 8):
                                ascii += "\\b"
                                break
                            # end if
                            if case(ord_var_c == 9):
                                ascii += "\\t"
                                break
                            # end if
                            if case(ord_var_c == 10):
                                ascii += "\\n"
                                break
                            # end if
                            if case(ord_var_c == 12):
                                ascii += "\\f"
                                break
                            # end if
                            if case(ord_var_c == 13):
                                ascii += "\\r"
                                break
                            # end if
                            if case(ord_var_c == 34):
                                pass
                            # end if
                            if case(ord_var_c == 47):
                                pass
                            # end if
                            if case(ord_var_c == 92):
                                #// double quote, slash, slosh
                                ascii += "\\" + var[c]
                                break
                            # end if
                            if case(ord_var_c >= 32 and ord_var_c <= 127):
                                #// characters U-00000000 - U-0000007F (same as ASCII)
                                ascii += var[c]
                                break
                            # end if
                            if case(ord_var_c & 224 == 192):
                                #// characters U-00000080 - U-000007FF, mask 110XXXXX
                                #// see http://www.cl.cam.ac.uk/~mgk25/unicode.html#utf-8
                                if c + 1 >= strlen_var:
                                    c += 1
                                    ascii += "?"
                                    break
                                # end if
                                char = pack("C*", ord_var_c, php_ord(var[c + 1]))
                                c += 1
                                utf16 = self.utf82utf16(char)
                                ascii += php_sprintf("\\u%04s", bin2hex(utf16))
                                break
                            # end if
                            if case(ord_var_c & 240 == 224):
                                if c + 2 >= strlen_var:
                                    c += 2
                                    ascii += "?"
                                    break
                                # end if
                                #// characters U-00000800 - U-0000FFFF, mask 1110XXXX
                                #// see http://www.cl.cam.ac.uk/~mgk25/unicode.html#utf-8
                                char = pack("C*", ord_var_c, php_no_error(lambda: php_ord(var[c + 1])), php_no_error(lambda: php_ord(var[c + 2])))
                                c += 2
                                utf16 = self.utf82utf16(char)
                                ascii += php_sprintf("\\u%04s", bin2hex(utf16))
                                break
                            # end if
                            if case(ord_var_c & 248 == 240):
                                if c + 3 >= strlen_var:
                                    c += 3
                                    ascii += "?"
                                    break
                                # end if
                                #// characters U-00010000 - U-001FFFFF, mask 11110XXX
                                #// see http://www.cl.cam.ac.uk/~mgk25/unicode.html#utf-8
                                char = pack("C*", ord_var_c, php_ord(var[c + 1]), php_ord(var[c + 2]), php_ord(var[c + 3]))
                                c += 3
                                utf16 = self.utf82utf16(char)
                                ascii += php_sprintf("\\u%04s", bin2hex(utf16))
                                break
                            # end if
                            if case(ord_var_c & 252 == 248):
                                #// characters U-00200000 - U-03FFFFFF, mask 111110XX
                                #// see http://www.cl.cam.ac.uk/~mgk25/unicode.html#utf-8
                                if c + 4 >= strlen_var:
                                    c += 4
                                    ascii += "?"
                                    break
                                # end if
                                char = pack("C*", ord_var_c, php_ord(var[c + 1]), php_ord(var[c + 2]), php_ord(var[c + 3]), php_ord(var[c + 4]))
                                c += 4
                                utf16 = self.utf82utf16(char)
                                ascii += php_sprintf("\\u%04s", bin2hex(utf16))
                                break
                            # end if
                            if case(ord_var_c & 254 == 252):
                                if c + 5 >= strlen_var:
                                    c += 5
                                    ascii += "?"
                                    break
                                # end if
                                #// characters U-04000000 - U-7FFFFFFF, mask 1111110X
                                #// see http://www.cl.cam.ac.uk/~mgk25/unicode.html#utf-8
                                char = pack("C*", ord_var_c, php_ord(var[c + 1]), php_ord(var[c + 2]), php_ord(var[c + 3]), php_ord(var[c + 4]), php_ord(var[c + 5]))
                                c += 5
                                utf16 = self.utf82utf16(char)
                                ascii += php_sprintf("\\u%04s", bin2hex(utf16))
                                break
                            # end if
                        # end for
                        c += 1
                    # end while
                    return "\"" + ascii + "\""
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
                    if php_is_array(var) and php_count(var) and php_array_keys(var) != range(0, sizeof(var) - 1):
                        properties = php_array_map(Array(self, "name_value"), php_array_keys(var), php_array_values(var))
                        for property in properties:
                            if Services_JSON.iserror(property):
                                return property
                            # end if
                        # end for
                        return "{" + join(",", properties) + "}"
                    # end if
                    #// treat it like a regular array
                    elements = php_array_map(Array(self, "_encode"), var)
                    for element in elements:
                        if Services_JSON.iserror(element):
                            return element
                        # end if
                    # end for
                    return "[" + join(",", elements) + "]"
                # end if
                if case("object"):
                    #// support toJSON methods.
                    if self.use & SERVICES_JSON_USE_TO_JSON and php_method_exists(var, "toJSON"):
                        #// this may end up allowing unlimited recursion
                        #// so we check the return value to make sure it's not got the same method.
                        recode = var.tojson()
                        if php_method_exists(recode, "toJSON"):
                            return "null" if self.use & SERVICES_JSON_SUPPRESS_ERRORS else php_new_class("Services_JSON_Error", lambda : Services_JSON_Error(get_class(var) + " toJSON returned an object with a toJSON method."))
                        # end if
                        return self._encode(recode)
                    # end if
                    vars = get_object_vars(var)
                    properties = php_array_map(Array(self, "name_value"), php_array_keys(vars), php_array_values(vars))
                    for property in properties:
                        if Services_JSON.iserror(property):
                            return property
                        # end if
                    # end for
                    return "{" + join(",", properties) + "}"
                # end if
                if case():
                    return "null" if self.use & SERVICES_JSON_SUPPRESS_ERRORS else php_new_class("Services_JSON_Error", lambda : Services_JSON_Error(gettype(var) + " can not be encoded as JSON string"))
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
        def name_value(self, name=None, value=None):
            
            _deprecated_function(__METHOD__, "5.3.0", "The PHP native JSON extension")
            encoded_value = self._encode(value)
            if Services_JSON.iserror(encoded_value):
                return encoded_value
            # end if
            return self._encode(php_strval(name)) + ":" + encoded_value
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
        def reduce_string(self, str=None):
            
            _deprecated_function(__METHOD__, "5.3.0", "The PHP native JSON extension")
            str = php_preg_replace(Array("#^\\s*//(.+)$#m", "#^\\s*/\\*(.+)\\*/#Us", "#/\\*(.+)\\*/\\s*$#Us"), "", str)
            #// eliminate extraneous space
            return php_trim(str)
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
        def decode(self, str=None):
            
            _deprecated_function(__METHOD__, "5.3.0", "The PHP native JSON extension")
            str = self.reduce_string(str)
            for case in Switch(php_strtolower(str)):
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
                    m = Array()
                    if php_is_numeric(str):
                        #// Lookie-loo, it's a number
                        #// This would work on its own, but I'm trying to be
                        #// good about returning integers where appropriate:
                        #// return (float)$str;
                        #// Return float or int, as appropriate
                        return int(str) if float(str) == int(str) else float(str)
                    elif php_preg_match("/^(\"|').*(\\1)$/s", str, m) and m[1] == m[2]:
                        #// STRINGS RETURNED IN UTF-8 FORMAT
                        delim = self.substr8(str, 0, 1)
                        chrs = self.substr8(str, 1, -1)
                        utf8 = ""
                        strlen_chrs = self.strlen8(chrs)
                        c = 0
                        while c < strlen_chrs:
                            
                            substr_chrs_c_2 = self.substr8(chrs, c, 2)
                            ord_chrs_c = php_ord(chrs[c])
                            for case in Switch(True):
                                if case(substr_chrs_c_2 == "\\b"):
                                    utf8 += chr(8)
                                    c += 1
                                    break
                                # end if
                                if case(substr_chrs_c_2 == "\\t"):
                                    utf8 += chr(9)
                                    c += 1
                                    break
                                # end if
                                if case(substr_chrs_c_2 == "\\n"):
                                    utf8 += chr(10)
                                    c += 1
                                    break
                                # end if
                                if case(substr_chrs_c_2 == "\\f"):
                                    utf8 += chr(12)
                                    c += 1
                                    break
                                # end if
                                if case(substr_chrs_c_2 == "\\r"):
                                    utf8 += chr(13)
                                    c += 1
                                    break
                                # end if
                                if case(substr_chrs_c_2 == "\\\""):
                                    pass
                                # end if
                                if case(substr_chrs_c_2 == "\\'"):
                                    pass
                                # end if
                                if case(substr_chrs_c_2 == "\\\\"):
                                    pass
                                # end if
                                if case(substr_chrs_c_2 == "\\/"):
                                    if delim == "\"" and substr_chrs_c_2 != "\\'" or delim == "'" and substr_chrs_c_2 != "\\\"":
                                        c += 1
                                        utf8 += chrs[c]
                                    # end if
                                    break
                                # end if
                                if case(php_preg_match("/\\\\u[0-9A-F]{4}/i", self.substr8(chrs, c, 6))):
                                    #// single, escaped unicode character
                                    utf16 = chr(hexdec(self.substr8(chrs, c + 2, 2))) + chr(hexdec(self.substr8(chrs, c + 4, 2)))
                                    utf8 += self.utf162utf8(utf16)
                                    c += 5
                                    break
                                # end if
                                if case(ord_chrs_c >= 32 and ord_chrs_c <= 127):
                                    utf8 += chrs[c]
                                    break
                                # end if
                                if case(ord_chrs_c & 224 == 192):
                                    #// characters U-00000080 - U-000007FF, mask 110XXXXX
                                    #// see http://www.cl.cam.ac.uk/~mgk25/unicode.html#utf-8
                                    utf8 += self.substr8(chrs, c, 2)
                                    c += 1
                                    break
                                # end if
                                if case(ord_chrs_c & 240 == 224):
                                    #// characters U-00000800 - U-0000FFFF, mask 1110XXXX
                                    #// see http://www.cl.cam.ac.uk/~mgk25/unicode.html#utf-8
                                    utf8 += self.substr8(chrs, c, 3)
                                    c += 2
                                    break
                                # end if
                                if case(ord_chrs_c & 248 == 240):
                                    #// characters U-00010000 - U-001FFFFF, mask 11110XXX
                                    #// see http://www.cl.cam.ac.uk/~mgk25/unicode.html#utf-8
                                    utf8 += self.substr8(chrs, c, 4)
                                    c += 3
                                    break
                                # end if
                                if case(ord_chrs_c & 252 == 248):
                                    #// characters U-00200000 - U-03FFFFFF, mask 111110XX
                                    #// see http://www.cl.cam.ac.uk/~mgk25/unicode.html#utf-8
                                    utf8 += self.substr8(chrs, c, 5)
                                    c += 4
                                    break
                                # end if
                                if case(ord_chrs_c & 254 == 252):
                                    #// characters U-04000000 - U-7FFFFFFF, mask 1111110X
                                    #// see http://www.cl.cam.ac.uk/~mgk25/unicode.html#utf-8
                                    utf8 += self.substr8(chrs, c, 6)
                                    c += 5
                                    break
                                # end if
                            # end for
                            c += 1
                        # end while
                        return utf8
                    elif php_preg_match("/^\\[.*\\]$/s", str) or php_preg_match("/^\\{.*\\}$/s", str):
                        #// array, or object notation
                        if str[0] == "[":
                            stk = Array(SERVICES_JSON_IN_ARR)
                            arr = Array()
                        else:
                            if self.use & SERVICES_JSON_LOOSE_TYPE:
                                stk = Array(SERVICES_JSON_IN_OBJ)
                                obj = Array()
                            else:
                                stk = Array(SERVICES_JSON_IN_OBJ)
                                obj = php_new_class("stdClass", lambda : stdClass())
                            # end if
                        # end if
                        php_array_push(stk, Array({"what": SERVICES_JSON_SLICE, "where": 0, "delim": False}))
                        chrs = self.substr8(str, 1, -1)
                        chrs = self.reduce_string(chrs)
                        if chrs == "":
                            if reset(stk) == SERVICES_JSON_IN_ARR:
                                return arr
                            else:
                                return obj
                            # end if
                        # end if
                        #// print("\nparsing {$chrs}\n");
                        strlen_chrs = self.strlen8(chrs)
                        c = 0
                        while c <= strlen_chrs:
                            
                            top = php_end(stk)
                            substr_chrs_c_2 = self.substr8(chrs, c, 2)
                            if c == strlen_chrs or chrs[c] == "," and top["what"] == SERVICES_JSON_SLICE:
                                #// found a comma that is not inside a string, array, etc.,
                                #// OR we've reached the end of the character list
                                slice = self.substr8(chrs, top["where"], c - top["where"])
                                php_array_push(stk, Array({"what": SERVICES_JSON_SLICE, "where": c + 1, "delim": False}))
                                #// print("Found split at {$c}: ".$this->substr8($chrs, $top['where'], (1 + $c - $top['where']))."\n");
                                if reset(stk) == SERVICES_JSON_IN_ARR:
                                    #// we are in an array, so just push an element onto the stack
                                    php_array_push(arr, self.decode(slice))
                                elif reset(stk) == SERVICES_JSON_IN_OBJ:
                                    #// we are in an object, so figure
                                    #// out the property name and set an
                                    #// element in an associative array,
                                    #// for now
                                    parts = Array()
                                    if php_preg_match("/^\\s*([\"'].*[^\\\\][\"'])\\s*:/Uis", slice, parts):
                                        #// "name":value pair
                                        key = self.decode(parts[1])
                                        val = self.decode(php_trim(php_substr(slice, php_strlen(parts[0])), ",  \n\r "))
                                        if self.use & SERVICES_JSON_LOOSE_TYPE:
                                            obj[key] = val
                                        else:
                                            obj.key = val
                                        # end if
                                    elif php_preg_match("/^\\s*(\\w+)\\s*:/Uis", slice, parts):
                                        #// name:value pair, where name is unquoted
                                        key = parts[1]
                                        val = self.decode(php_trim(php_substr(slice, php_strlen(parts[0])), ",  \n\r "))
                                        if self.use & SERVICES_JSON_LOOSE_TYPE:
                                            obj[key] = val
                                        else:
                                            obj.key = val
                                        # end if
                                    # end if
                                # end if
                            elif chrs[c] == "\"" or chrs[c] == "'" and top["what"] != SERVICES_JSON_IN_STR:
                                #// found a quote, and we are not inside a string
                                php_array_push(stk, Array({"what": SERVICES_JSON_IN_STR, "where": c, "delim": chrs[c]}))
                                pass
                            elif chrs[c] == top["delim"] and top["what"] == SERVICES_JSON_IN_STR and self.strlen8(self.substr8(chrs, 0, c)) - self.strlen8(php_rtrim(self.substr8(chrs, 0, c), "\\")) % 2 != 1:
                                #// found a quote, we're in a string, and it's not escaped
                                #// we know that it's not escaped because there is _not_ an
                                #// odd number of backslashes at the end of the string so far
                                php_array_pop(stk)
                                pass
                            elif chrs[c] == "[" and php_in_array(top["what"], Array(SERVICES_JSON_SLICE, SERVICES_JSON_IN_ARR, SERVICES_JSON_IN_OBJ)):
                                #// found a left-bracket, and we are in an array, object, or slice
                                php_array_push(stk, Array({"what": SERVICES_JSON_IN_ARR, "where": c, "delim": False}))
                                pass
                            elif chrs[c] == "]" and top["what"] == SERVICES_JSON_IN_ARR:
                                #// found a right-bracket, and we're in an array
                                php_array_pop(stk)
                                pass
                            elif chrs[c] == "{" and php_in_array(top["what"], Array(SERVICES_JSON_SLICE, SERVICES_JSON_IN_ARR, SERVICES_JSON_IN_OBJ)):
                                #// found a left-brace, and we are in an array, object, or slice
                                php_array_push(stk, Array({"what": SERVICES_JSON_IN_OBJ, "where": c, "delim": False}))
                                pass
                            elif chrs[c] == "}" and top["what"] == SERVICES_JSON_IN_OBJ:
                                #// found a right-brace, and we're in an object
                                php_array_pop(stk)
                                pass
                            elif substr_chrs_c_2 == "/*" and php_in_array(top["what"], Array(SERVICES_JSON_SLICE, SERVICES_JSON_IN_ARR, SERVICES_JSON_IN_OBJ)):
                                #// found a comment start, and we are in an array, object, or slice
                                php_array_push(stk, Array({"what": SERVICES_JSON_IN_CMT, "where": c, "delim": False}))
                                c += 1
                                pass
                            elif substr_chrs_c_2 == "*/" and top["what"] == SERVICES_JSON_IN_CMT:
                                #// found a comment end, and we're in one now
                                php_array_pop(stk)
                                c += 1
                                i = top["where"]
                                while i <= c:
                                    
                                    chrs = php_substr_replace(chrs, " ", i, 1)
                                    i += 1
                                # end while
                                pass
                            # end if
                            c += 1
                        # end while
                        if reset(stk) == SERVICES_JSON_IN_ARR:
                            return arr
                        elif reset(stk) == SERVICES_JSON_IN_OBJ:
                            return obj
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
        def iserror(self, data=None, code=None):
            
            _deprecated_function(__METHOD__, "5.3.0", "The PHP native JSON extension")
            if php_class_exists("pear"):
                return PEAR.iserror(data, code)
            elif php_is_object(data) and get_class(data) == "services_json_error" or is_subclass_of(data, "services_json_error"):
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
        def strlen8(self, str=None):
            
            _deprecated_function(__METHOD__, "5.3.0", "The PHP native JSON extension")
            if self._mb_strlen:
                return php_mb_strlen(str, "8bit")
            # end if
            return php_strlen(str)
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
        def substr8(self, string=None, start=None, length=False):
            
            _deprecated_function(__METHOD__, "5.3.0", "The PHP native JSON extension")
            if length == False:
                length = self.strlen8(string) - start
            # end if
            if self._mb_substr:
                return php_mb_substr(string, start, length, "8bit")
            # end if
            return php_substr(string, start, length)
        # end def substr8
    # end class Services_JSON
    if php_class_exists("PEAR_Error"):
        class Services_JSON_Error(PEAR_Error):
            #// 
            #// PHP5 constructor.
            #// 
            #// @deprecated 5.3.0 Use the PHP native JSON extension instead.
            #//
            def __init__(self, message="unknown error", code=None, mode=None, options=None, userinfo=None):
                
                _deprecated_function(__METHOD__, "5.3.0", "The PHP native JSON extension")
                super().pear_error(message, code, mode, options, userinfo)
            # end def __init__
            #// 
            #// PHP4 constructor.
            #// 
            #// @deprecated 5.3.0 Use __construct() instead.
            #// 
            #// @see Services_JSON_Error::__construct()
            #//
            def services_json_error(self, message="unknown error", code=None, mode=None, options=None, userinfo=None):
                
                _deprecated_constructor("Services_JSON_Error", "5.3.0", get_class(self))
                self.__init__(message, code, mode, options, userinfo)
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
            def __init__(self, message="unknown error", code=None, mode=None, options=None, userinfo=None):
                
                _deprecated_function(__METHOD__, "5.3.0", "The PHP native JSON extension")
            # end def __init__
            #// 
            #// PHP4 constructor.
            #// 
            #// @deprecated 5.3.0 Use __construct() instead.
            #// 
            #// @see Services_JSON_Error::__construct()
            #//
            def services_json_error(self, message="unknown error", code=None, mode=None, options=None, userinfo=None):
                
                _deprecated_constructor("Services_JSON_Error", "5.3.0", get_class(self))
                self.__init__(message, code, mode, options, userinfo)
            # end def services_json_error
        # end class Services_JSON_Error
    # end if
# end if
