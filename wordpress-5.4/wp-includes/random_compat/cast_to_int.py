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
if (not php_is_callable("RandomCompat_intval")):
    #// 
    #// Cast to an integer if we can, safely.
    #// 
    #// If you pass it a float in the range (~PHP_INT_MAX, PHP_INT_MAX)
    #// (non-inclusive), it will sanely cast it to an int. If you it's equal to
    #// ~PHP_INT_MAX or PHP_INT_MAX, we let it fail as not an integer. Floats
    #// lose precision, so the <= and => operators might accidentally let a float
    #// through.
    #// 
    #// @param int|float $number    The number we want to convert to an int
    #// @param bool      $fail_open Set to true to not throw an exception
    #// 
    #// @return float|int
    #// @psalm-suppress InvalidReturnType
    #// 
    #// @throws TypeError
    #//
    def RandomCompat_intval(number=None, fail_open=False, *args_):
        
        if php_is_int(number) or php_is_float(number):
            number += 0
        elif php_is_numeric(number):
            number += 0
        # end if
        if php_is_float(number) and number > (1 << (PHP_INT_MAX).bit_length()) - 1 - PHP_INT_MAX and number < PHP_INT_MAX:
            number = int(number)
        # end if
        if php_is_int(number):
            return int(number)
        elif (not fail_open):
            raise php_new_class("TypeError", lambda : TypeError("Expected an integer."))
        # end if
        return number
    # end def RandomCompat_intval
# end if
