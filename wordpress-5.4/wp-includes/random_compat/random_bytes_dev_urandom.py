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
if (not php_defined("RANDOM_COMPAT_READ_BUFFER")):
    php_define("RANDOM_COMPAT_READ_BUFFER", 8)
# end if
if (not php_is_callable("random_bytes")):
    #// 
    #// Unless open_basedir is enabled, use /dev/urandom for
    #// random numbers in accordance with best practices
    #// 
    #// Why we use /dev/urandom and not /dev/random
    #// @ref http://sockpuppet.org/blog/2014/02/25/safely-generate-random-numbers
    #// 
    #// @param int $bytes
    #// 
    #// @throws Exception
    #// 
    #// @return string
    #//
    def random_bytes(bytes=None, *args_):
        
        fp = None
        #// 
        #// This block should only be run once
        #//
        if php_empty(lambda : fp):
            #// 
            #// We use /dev/urandom if it is a char device.
            #// We never fall back to /dev/random
            #//
            fp = fopen("/dev/urandom", "rb")
            if (not php_empty(lambda : fp)):
                st = fstat(fp)
                if st["mode"] & 61440 != 8192:
                    php_fclose(fp)
                    fp = False
                # end if
            # end if
            if (not php_empty(lambda : fp)):
                #// 
                #// stream_set_read_buffer() does not exist in HHVM
                #// 
                #// If we don't set the stream's read buffer to 0, PHP will
                #// internally buffer 8192 bytes, which can waste entropy
                #// 
                #// stream_set_read_buffer returns 0 on success
                #//
                if php_is_callable("stream_set_read_buffer"):
                    stream_set_read_buffer(fp, RANDOM_COMPAT_READ_BUFFER)
                # end if
                if php_is_callable("stream_set_chunk_size"):
                    stream_set_chunk_size(fp, RANDOM_COMPAT_READ_BUFFER)
                # end if
            # end if
        # end if
        try: 
            bytes = RandomCompat_intval(bytes)
        except TypeError as ex:
            raise php_new_class("TypeError", lambda : TypeError("random_bytes(): $bytes must be an integer"))
        # end try
        if bytes < 1:
            raise php_new_class("Error", lambda : Error("Length must be greater than 0"))
        # end if
        #// 
        #// This if() block only runs if we managed to open a file handle
        #// 
        #// It does not belong in an else {} block, because the above
        #// if (empty($fp)) line is logic that should only be run once per
        #// page load.
        #//
        if (not php_empty(lambda : fp)):
            #// 
            #// @var int
            #//
            remaining = bytes
            #// 
            #// @var string|bool
            #//
            buf = ""
            #// 
            #// We use fread() in a loop to protect against partial reads
            #//
            while True:
                #// 
                #// @var string|bool
                #//
                read = fread(fp, remaining)
                if (not php_is_string(read)):
                    if read == False:
                        #// 
                        #// We cannot safely read from the file. Exit the
                        #// do-while loop and trigger the exception condition
                        #// 
                        #// @var string|bool
                        #//
                        buf = False
                        break
                    # end if
                # end if
                #// 
                #// Decrease the number of bytes returned from remaining
                #//
                remaining -= RandomCompat_strlen(read)
                #// 
                #// @var string|bool
                #//
                buf = buf + read
                
                if remaining > 0:
                    break
                # end if
            # end while
            #// 
            #// Is our result valid?
            #//
            if php_is_string(buf):
                if RandomCompat_strlen(buf) == bytes:
                    #// 
                    #// Return our random entropy buffer here:
                    #//
                    return buf
                # end if
            # end if
        # end if
        raise php_new_class("Exception", lambda : Exception("Error reading from source device"))
    # end def random_bytes
# end if
