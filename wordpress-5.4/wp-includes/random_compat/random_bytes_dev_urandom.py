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
    def random_bytes(bytes_=None, *_args_):
        
        
        fp_ = None
        #// 
        #// This block should only be run once
        #//
        if php_empty(lambda : fp_):
            #// 
            #// We use /dev/urandom if it is a char device.
            #// We never fall back to /dev/random
            #//
            fp_ = fopen("/dev/urandom", "rb")
            if (not php_empty(lambda : fp_)):
                st_ = fstat(fp_)
                if st_["mode"] & 61440 != 8192:
                    php_fclose(fp_)
                    fp_ = False
                # end if
            # end if
            if (not php_empty(lambda : fp_)):
                #// 
                #// stream_set_read_buffer() does not exist in HHVM
                #// 
                #// If we don't set the stream's read buffer to 0, PHP will
                #// internally buffer 8192 bytes, which can waste entropy
                #// 
                #// stream_set_read_buffer returns 0 on success
                #//
                if php_is_callable("stream_set_read_buffer"):
                    stream_set_read_buffer(fp_, RANDOM_COMPAT_READ_BUFFER)
                # end if
                if php_is_callable("stream_set_chunk_size"):
                    stream_set_chunk_size(fp_, RANDOM_COMPAT_READ_BUFFER)
                # end if
            # end if
        # end if
        try: 
            bytes_ = RandomCompat_intval(bytes_)
        except TypeError as ex_:
            raise php_new_class("TypeError", lambda : TypeError("random_bytes(): $bytes must be an integer"))
        # end try
        if bytes_ < 1:
            raise php_new_class("Error", lambda : Error("Length must be greater than 0"))
        # end if
        #// 
        #// This if() block only runs if we managed to open a file handle
        #// 
        #// It does not belong in an else {} block, because the above
        #// if (empty($fp)) line is logic that should only be run once per
        #// page load.
        #//
        if (not php_empty(lambda : fp_)):
            #// 
            #// @var int
            #//
            remaining_ = bytes_
            #// 
            #// @var string|bool
            #//
            buf_ = ""
            #// 
            #// We use fread() in a loop to protect against partial reads
            #//
            while True:
                #// 
                #// @var string|bool
                #//
                read_ = fread(fp_, remaining_)
                if (not php_is_string(read_)):
                    if read_ == False:
                        #// 
                        #// We cannot safely read from the file. Exit the
                        #// do-while loop and trigger the exception condition
                        #// 
                        #// @var string|bool
                        #//
                        buf_ = False
                        break
                    # end if
                # end if
                #// 
                #// Decrease the number of bytes returned from remaining
                #//
                remaining_ -= RandomCompat_strlen(read_)
                #// 
                #// @var string|bool
                #//
                buf_ = buf_ + read_
                
                if remaining_ > 0:
                    break
                # end if
            # end while
            #// 
            #// Is our result valid?
            #//
            if php_is_string(buf_):
                if RandomCompat_strlen(buf_) == bytes_:
                    #// 
                    #// Return our random entropy buffer here:
                    #//
                    return buf_
                # end if
            # end if
        # end if
        raise php_new_class("Exception", lambda : Exception("Error reading from source device"))
    # end def random_bytes
# end if
