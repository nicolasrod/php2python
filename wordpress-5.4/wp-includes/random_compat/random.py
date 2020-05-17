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
#// @version 2.0.10
#// @released 2017-03-13
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
if (not php_defined("PHP_VERSION_ID")):
    #// This constant was introduced in PHP 5.2.7
    RandomCompatversion_ = php_array_map("intval", php_explode(".", PHP_VERSION))
    php_define("PHP_VERSION_ID", RandomCompatversion_[0] * 10000 + RandomCompatversion_[1] * 100 + RandomCompatversion_[2])
    RandomCompatversion_ = None
# end if
#// 
#// PHP 7.0.0 and newer have these functions natively.
#//
if PHP_VERSION_ID >= 70000:
    sys.exit(-1)
# end if
if (not php_defined("RANDOM_COMPAT_READ_BUFFER")):
    php_define("RANDOM_COMPAT_READ_BUFFER", 8)
# end if
RandomCompatDIR_ = php_dirname(__FILE__)
php_include_file(RandomCompatDIR_ + "/byte_safe_strings.php", once=True)
php_include_file(RandomCompatDIR_ + "/cast_to_int.php", once=True)
php_include_file(RandomCompatDIR_ + "/error_polyfill.php", once=True)
if (not php_is_callable("random_bytes")):
    #// 
    #// PHP 5.2.0 - 5.6.x way to implement random_bytes()
    #// 
    #// We use conditional statements here to define the function in accordance
    #// to the operating environment. It's a micro-optimization.
    #// 
    #// In order of preference:
    #// 1. Use libsodium if available.
    #// 2. fread() /dev/urandom if available (never on Windows)
    #// 3. mcrypt_create_iv($bytes, MCRYPT_DEV_URANDOM)
    #// 4. COM('CAPICOM.Utilities.1')->GetRandom()
    #// 
    #// See RATIONALE.md for our reasoning behind this particular order
    #//
    if php_extension_loaded("libsodium"):
        #// See random_bytes_libsodium.php
        if PHP_VERSION_ID >= 50300 and php_is_callable("\\Sodium\\randombytes_buf"):
            php_include_file(RandomCompatDIR_ + "/random_bytes_libsodium.php", once=True)
        elif php_method_exists("Sodium", "randombytes_buf"):
            php_include_file(RandomCompatDIR_ + "/random_bytes_libsodium_legacy.php", once=True)
        # end if
    # end if
    #// 
    #// Reading directly from /dev/urandom:
    #//
    if DIRECTORY_SEPARATOR == "/":
        #// DIRECTORY_SEPARATOR === '/' on Unix-like OSes -- this is a fast
        #// way to exclude Windows.
        RandomCompatUrandom_ = True
        RandomCompat_basedir_ = php_ini_get("open_basedir")
        if (not php_empty(lambda : RandomCompat_basedir_)):
            RandomCompat_open_basedir_ = php_explode(PATH_SEPARATOR, php_strtolower(RandomCompat_basedir_))
            RandomCompatUrandom_ = Array() != php_array_intersect(Array("/dev", "/dev/", "/dev/urandom"), RandomCompat_open_basedir_)
            RandomCompat_open_basedir_ = None
        # end if
        if (not php_is_callable("random_bytes")) and RandomCompatUrandom_ and php_no_error(lambda: php_is_readable("/dev/urandom")):
            #// Error suppression on is_readable() in case of an open_basedir
            #// or safe_mode failure. All we care about is whether or not we
            #// can read it at this point. If the PHP environment is going to
            #// panic over trying to see if the file can be read in the first
            #// place, that is not helpful to us here.
            #// See random_bytes_dev_urandom.php
            php_include_file(RandomCompatDIR_ + "/random_bytes_dev_urandom.php", once=True)
        # end if
        #// Unset variables after use
        RandomCompat_basedir_ = None
    else:
        RandomCompatUrandom_ = False
    # end if
    #// 
    #// mcrypt_create_iv()
    #// 
    #// We only want to use mcypt_create_iv() if:
    #// 
    #// - random_bytes() hasn't already been defined
    #// - the mcrypt extensions is loaded
    #// - One of these two conditions is true:
    #// - We're on Windows (DIRECTORY_SEPARATOR !== '/')
    #// - We're not on Windows and /dev/urandom is readabale
    #// (i.e. we're not in a chroot jail)
    #// - Special case:
    #// - If we're not on Windows, but the PHP version is between
    #// 5.6.10 and 5.6.12, we don't want to use mcrypt. It will
    #// hang indefinitely. This is bad.
    #// - If we're on Windows, we want to use PHP >= 5.3.7 or else
    #// we get insufficient entropy errors.
    #//
    if (not php_is_callable("random_bytes")) and DIRECTORY_SEPARATOR == "/" or PHP_VERSION_ID >= 50307 and DIRECTORY_SEPARATOR != "/" or PHP_VERSION_ID <= 50609 or PHP_VERSION_ID >= 50613 and php_extension_loaded("mcrypt"):
        #// See random_bytes_mcrypt.php
        php_include_file(RandomCompatDIR_ + "/random_bytes_mcrypt.php", once=True)
    # end if
    RandomCompatUrandom_ = None
    #// 
    #// This is a Windows-specific fallback, for when the mcrypt extension
    #// isn't loaded.
    #//
    if (not php_is_callable("random_bytes")) and php_extension_loaded("com_dotnet") and php_class_exists("COM"):
        RandomCompat_disabled_classes_ = php_preg_split("#\\s*,\\s*#", php_strtolower(php_ini_get("disable_classes")))
        if (not php_in_array("com", RandomCompat_disabled_classes_)):
            try: 
                RandomCompatCOMtest_ = php_new_class("COM", lambda : COM("CAPICOM.Utilities.1"))
                if php_method_exists(RandomCompatCOMtest_, "GetRandom"):
                    #// See random_bytes_com_dotnet.php
                    php_include_file(RandomCompatDIR_ + "/random_bytes_com_dotnet.php", once=True)
                # end if
            except com_exception as e_:
                pass
            # end try
        # end if
        RandomCompat_disabled_classes_ = None
        RandomCompatCOMtest_ = None
    # end if
    #// 
    #// throw new Exception
    #//
    if (not php_is_callable("random_bytes")):
        #// 
        #// We don't have any more options, so let's throw an exception right now
        #// and hope the developer won't let it fail silently.
        #// 
        #// @param mixed $length
        #// @return void
        #// @throws Exception
        #//
        def random_bytes(length_=None, *_args_):
            
            
            length_ = None
            raise php_new_class("Exception", lambda : Exception("There is no suitable CSPRNG installed on your system"))
        # end def random_bytes
    # end if
# end if
if (not php_is_callable("random_int")):
    php_include_file(RandomCompatDIR_ + "/random_int.php", once=True)
# end if
RandomCompatDIR_ = None
