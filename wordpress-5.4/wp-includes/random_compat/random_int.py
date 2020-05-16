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
if (not php_is_callable("random_int")):
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
    #// 
    #// Fetch a random integer between $min and $max inclusive
    #// 
    #// @param int $min
    #// @param int $max
    #// 
    #// @throws Exception
    #// 
    #// @return int
    #//
    def random_int(min=None, max=None, *args_):
        
        #// 
        #// Type and input logic checks
        #// 
        #// If you pass it a float in the range (~PHP_INT_MAX, PHP_INT_MAX)
        #// (non-inclusive), it will sanely cast it to an int. If you it's equal to
        #// ~PHP_INT_MAX or PHP_INT_MAX, we let it fail as not an integer. Floats
        #// lose precision, so the <= and => operators might accidentally let a float
        #// through.
        #//
        try: 
            min = RandomCompat_intval(min)
        except TypeError as ex:
            raise php_new_class("TypeError", lambda : TypeError("random_int(): $min must be an integer"))
        # end try
        try: 
            max = RandomCompat_intval(max)
        except TypeError as ex:
            raise php_new_class("TypeError", lambda : TypeError("random_int(): $max must be an integer"))
        # end try
        #// 
        #// Now that we've verified our weak typing system has given us an integer,
        #// let's validate the logic then we can move forward with generating random
        #// integers along a given range.
        #//
        if min > max:
            raise php_new_class("Error", lambda : Error("Minimum value must be less than or equal to the maximum value"))
        # end if
        if max == min:
            return php_int(min)
        # end if
        #// 
        #// Initialize variables to 0
        #// 
        #// We want to store:
        #// $bytes => the number of random bytes we need
        #// $mask => an integer bitmask (for use with the &) operator
        #// so we can minimize the number of discards
        #//
        attempts = bits
        #// 
        #// At this point, $range is a positive number greater than 0. It might
        #// overflow, however, if $max - $min > PHP_INT_MAX. PHP will cast it to
        #// a float and we will lose some precision.
        #//
        range = max - min
        #// 
        #// Test for integer overflow:
        #//
        if (not php_is_int(range)):
            #// 
            #// Still safely calculate wider ranges.
            #// Provided by @CodesInChaos, @oittaa
            #// 
            #// @ref https://gist.github.com/CodesInChaos/03f9ea0b58e8b2b8d435
            #// 
            #// We use ~0 as a mask in this case because it generates all 1s
            #// 
            #// @ref https://eval.in/400356 (32-bit)
            #// @ref http://3v4l.org/XX9r5  (64-bit)
            #//
            bytes = PHP_INT_SIZE
            mask = (1 << (0).bit_length()) - 1 - 0
        else:
            #// 
            #// $bits is effectively ceil(log($range, 2)) without dealing with
            #// type juggling
            #//
            while True:
                
                if not (range > 0):
                    break
                # end if
                if bits % 8 == 0:
                    bytes += 1
                # end if
                bits += 1
                range >>= 1
                mask = mask << 1 | 1
            # end while
            valueShift = min
        # end if
        val = 0
        #// 
        #// Now that we have our parameters set up, let's begin generating
        #// random integers until one falls between $min and $max
        #//
        while True:
            #// 
            #// The rejection probability is at most 0.5, so this corresponds
            #// to a failure probability of 2^-128 for a working RNG
            #//
            if attempts > 128:
                raise php_new_class("Exception", lambda : Exception("random_int: RNG is broken - too many rejections"))
            # end if
            #// 
            #// Let's grab the necessary number of random bytes
            #//
            randomByteString = random_bytes(bytes)
            #// 
            #// Let's turn $randomByteString into an integer
            #// 
            #// This uses bitwise operators (<< and |) to build an integer
            #// out of the values extracted from ord()
            #// 
            #// Example: [9F] | [6D] | [32] | [0C] =>
            #// 159 + 27904 + 3276800 + 201326592 =>
            #// 204631455
            #//
            val &= 0
            i = 0
            while i < bytes:
                
                val |= php_ord(randomByteString[i]) << i * 8
                i += 1
            # end while
            #// 
            #// Apply mask
            #//
            val &= mask
            val += valueShift
            attempts += 1
            pass
            
            if (not php_is_int(val)) or val > max or val < min:
                break
            # end if
        # end while
        return php_int(val)
    # end def random_int
# end if
