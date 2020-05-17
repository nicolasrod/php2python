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
#// Random_* Compatibility Library
#// for using the new PHP 7 random_* API in PHP 5 projects
#// 
#// The MIT License (MIT)
#// 
#// Copyright (c) 2015 - 2017 Paragon Initiative Enterprises
#// 
#// Permission is hereby granted, free of charge, to any person obtaining a copy
#// of this software and associated documentation files (the "Software"), to deal
#// in the Software without restriction, including without limitation the rights
#// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#// copies of the Software, and to permit persons to whom the Software is
#// furnished to do so, subject to the following conditions:
#// 
#// The above copyright notice and this permission notice shall be included in
#// all copies or substantial portions of the Software.
#// 
#// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#// SOFTWARE.
#//
if (not php_is_callable("RandomCompat_strlen")):
    if php_defined("MB_OVERLOAD_STRING") and php_ini_get("mbstring.func_overload") & MB_OVERLOAD_STRING:
        #// 
        #// strlen() implementation that isn't brittle to mbstring.func_overload
        #// 
        #// This version uses mb_strlen() in '8bit' mode to treat strings as raw
        #// binary rather than UTF-8, ISO-8859-1, etc
        #// 
        #// @param string $binary_string
        #// 
        #// @throws TypeError
        #// 
        #// @return int
        #//
        def RandomCompat_strlen(binary_string_=None, *_args_):
            
            
            if (not php_is_string(binary_string_)):
                raise php_new_class("TypeError", lambda : TypeError("RandomCompat_strlen() expects a string"))
            # end if
            return php_int(php_mb_strlen(binary_string_, "8bit"))
        # end def RandomCompat_strlen
    else:
        #// 
        #// strlen() implementation that isn't brittle to mbstring.func_overload
        #// 
        #// This version just used the default strlen()
        #// 
        #// @param string $binary_string
        #// 
        #// @throws TypeError
        #// 
        #// @return int
        #//
        def RandomCompat_strlen(binary_string_=None, *_args_):
            
            
            if (not php_is_string(binary_string_)):
                raise php_new_class("TypeError", lambda : TypeError("RandomCompat_strlen() expects a string"))
            # end if
            return php_int(php_strlen(binary_string_))
        # end def RandomCompat_strlen
    # end if
# end if
if (not php_is_callable("RandomCompat_substr")):
    if php_defined("MB_OVERLOAD_STRING") and php_ini_get("mbstring.func_overload") & MB_OVERLOAD_STRING:
        #// 
        #// substr() implementation that isn't brittle to mbstring.func_overload
        #// 
        #// This version uses mb_substr() in '8bit' mode to treat strings as raw
        #// binary rather than UTF-8, ISO-8859-1, etc
        #// 
        #// @param string $binary_string
        #// @param int $start
        #// @param int $length (optional)
        #// 
        #// @throws TypeError
        #// 
        #// @return string
        #//
        def RandomCompat_substr(binary_string_=None, start_=None, length_=None, *_args_):
            if length_ is None:
                length_ = None
            # end if
            
            if (not php_is_string(binary_string_)):
                raise php_new_class("TypeError", lambda : TypeError("RandomCompat_substr(): First argument should be a string"))
            # end if
            if (not php_is_int(start_)):
                raise php_new_class("TypeError", lambda : TypeError("RandomCompat_substr(): Second argument should be an integer"))
            # end if
            if length_ == None:
                #// 
                #// mb_substr($str, 0, NULL, '8bit') returns an empty string on
                #// PHP 5.3, so we have to find the length ourselves.
                #//
                length_ = RandomCompat_strlen(binary_string_) - start_
            elif (not php_is_int(length_)):
                raise php_new_class("TypeError", lambda : TypeError("RandomCompat_substr(): Third argument should be an integer, or omitted"))
            # end if
            #// Consistency with PHP's behavior
            if start_ == RandomCompat_strlen(binary_string_) and length_ == 0:
                return ""
            # end if
            if start_ > RandomCompat_strlen(binary_string_):
                return ""
            # end if
            return php_str(php_mb_substr(binary_string_, start_, length_, "8bit"))
        # end def RandomCompat_substr
    else:
        #// 
        #// substr() implementation that isn't brittle to mbstring.func_overload
        #// 
        #// This version just uses the default substr()
        #// 
        #// @param string $binary_string
        #// @param int $start
        #// @param int $length (optional)
        #// 
        #// @throws TypeError
        #// 
        #// @return string
        #//
        def RandomCompat_substr(binary_string_=None, start_=None, length_=None, *_args_):
            if length_ is None:
                length_ = None
            # end if
            
            if (not php_is_string(binary_string_)):
                raise php_new_class("TypeError", lambda : TypeError("RandomCompat_substr(): First argument should be a string"))
            # end if
            if (not php_is_int(start_)):
                raise php_new_class("TypeError", lambda : TypeError("RandomCompat_substr(): Second argument should be an integer"))
            # end if
            if length_ != None:
                if (not php_is_int(length_)):
                    raise php_new_class("TypeError", lambda : TypeError("RandomCompat_substr(): Third argument should be an integer, or omitted"))
                # end if
                return php_str(php_substr(binary_string_, start_, length_))
            # end if
            return php_str(php_substr(binary_string_, start_))
        # end def RandomCompat_substr
    # end if
# end if
