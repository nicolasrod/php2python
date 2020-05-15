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
if (not php_is_callable("random_bytes")):
    #// 
    #// Windows with PHP < 5.3.0 will not have the function
    #// openssl_random_pseudo_bytes() available, so let's use
    #// CAPICOM to work around this deficiency.
    #// 
    #// @param int $bytes
    #// 
    #// @throws Exception
    #// 
    #// @return string
    #//
    def random_bytes(bytes=None, *args_):
        
        try: 
            bytes = RandomCompat_intval(bytes)
        except TypeError as ex:
            raise php_new_class("TypeError", lambda : TypeError("random_bytes(): $bytes must be an integer"))
        # end try
        if bytes < 1:
            raise php_new_class("Error", lambda : Error("Length must be greater than 0"))
        # end if
        buf = ""
        if (not php_class_exists("COM")):
            raise php_new_class("Error", lambda : Error("COM does not exist"))
        # end if
        util = php_new_class("COM", lambda : COM("CAPICOM.Utilities.1"))
        execCount = 0
        #// 
        #// Let's not let it loop forever. If we run N times and fail to
        #// get N bytes of random data, then CAPICOM has failed us.
        #//
        while True:
            buf += php_base64_decode(util.getrandom(bytes, 0))
            if RandomCompat_strlen(buf) >= bytes:
                #// 
                #// Return our random entropy buffer here:
                #//
                return RandomCompat_substr(buf, 0, bytes)
            # end if
            execCount += 1
            
            if execCount < bytes:
                break
            # end if
        # end while
        raise php_new_class("Exception", lambda : Exception("Could not gather sufficient random data"))
    # end def random_bytes
# end if
