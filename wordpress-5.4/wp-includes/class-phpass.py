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
#// Portable PHP password hashing framework.
#// @package phpass
#// @since 2.5.0
#// @version 0.3 / WordPress
#// @link https://www.openwall.com/phpass
#// 
#// #
#// # Written by Solar Designer <solar at openwall.com> in 2004-2006 and placed in
#// # the public domain.  Revised in subsequent years, still public domain.
#// #
#// # There's absolutely no warranty.
#// #
#// # Please be sure to update the Version line if you edit this file in any way.
#// # It is suggested that you leave the main version number intact, but indicate
#// # your project name (after the slash) and add your own revision information.
#// #
#// # Please do not change the "private" password hashing method implemented in
#// # here, thereby making your hashes incompatible.  However, if you must, please
#// # change the hash type identifier (the "$P$") to something different.
#// #
#// # Obviously, since this code is in the public domain, the above are not
#// # requirements (there can be none), but merely suggestions.
#// #
#// 
#// Portable PHP password hashing framework.
#// 
#// @package phpass
#// @version 0.3 / WordPress
#// @link https://www.openwall.com/phpass
#// @since 2.5.0
#//
class PasswordHash():
    itoa64 = Array()
    iteration_count_log2 = Array()
    portable_hashes = Array()
    random_state = Array()
    #// 
    #// PHP5 constructor.
    #//
    def __init__(self, iteration_count_log2=None, portable_hashes=None):
        
        self.itoa64 = "./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        if iteration_count_log2 < 4 or iteration_count_log2 > 31:
            iteration_count_log2 = 8
        # end if
        self.iteration_count_log2 = iteration_count_log2
        self.portable_hashes = portable_hashes
        self.random_state = php_microtime() + uniqid(rand(), True)
        pass
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def passwordhash(self, iteration_count_log2=None, portable_hashes=None):
        
        self.__init__(iteration_count_log2, portable_hashes)
    # end def passwordhash
    def get_random_bytes(self, count=None):
        
        output = ""
        fh = php_no_error(lambda: fopen("/dev/urandom", "rb"))
        if php_no_error(lambda: php_is_readable("/dev/urandom")) and fh:
            output = fread(fh, count)
            php_fclose(fh)
        # end if
        if php_strlen(output) < count:
            output = ""
            i = 0
            while i < count:
                
                self.random_state = php_md5(php_microtime() + self.random_state)
                output += pack("H*", php_md5(self.random_state))
                i += 16
            # end while
            output = php_substr(output, 0, count)
        # end if
        return output
    # end def get_random_bytes
    def encode64(self, input=None, count=None):
        
        output = ""
        i = 0
        while True:
            value = php_ord(input[i])
            i += 1
            output += self.itoa64[value & 63]
            if i < count:
                value |= php_ord(input[i]) << 8
            # end if
            output += self.itoa64[value >> 6 & 63]
            if i >= count:
                break
            # end if
            i += 1
            if i < count:
                value |= php_ord(input[i]) << 16
            # end if
            output += self.itoa64[value >> 12 & 63]
            if i >= count:
                break
            # end if
            i += 1
            output += self.itoa64[value >> 18 & 63]
            
            if i < count:
                break
            # end if
        # end while
        return output
    # end def encode64
    def gensalt_private(self, input=None):
        
        output = "$P$"
        output += self.itoa64[php_min(self.iteration_count_log2 + 5 if PHP_VERSION >= "5" else 3, 30)]
        output += self.encode64(input, 6)
        return output
    # end def gensalt_private
    def crypt_private(self, password=None, setting=None):
        
        output = "*0"
        if php_substr(setting, 0, 2) == output:
            output = "*1"
        # end if
        id = php_substr(setting, 0, 3)
        #// # We use "$P$", phpBB3 uses "$H$" for the same thing
        if id != "$P$" and id != "$H$":
            return output
        # end if
        count_log2 = php_strpos(self.itoa64, setting[3])
        if count_log2 < 7 or count_log2 > 30:
            return output
        # end if
        count = 1 << count_log2
        salt = php_substr(setting, 4, 8)
        if php_strlen(salt) != 8:
            return output
        # end if
        #// # We're kind of forced to use MD5 here since it's the only
        #// # cryptographic primitive available in all versions of PHP
        #// # currently in use.  To implement our own low-level crypto
        #// # in PHP would result in much worse performance and
        #// # consequently in lower iteration counts and hashes that are
        #// # quicker to crack (by non-PHP code).
        if PHP_VERSION >= "5":
            hash = php_md5(salt + password, True)
            while True:
                hash = php_md5(hash + password, True)
                
                if count -= 1:
                    break
                # end if
            # end while
        else:
            hash = pack("H*", php_md5(salt + password))
            while True:
                hash = pack("H*", php_md5(hash + password))
                
                if count -= 1:
                    break
                # end if
            # end while
        # end if
        output = php_substr(setting, 0, 12)
        output += self.encode64(hash, 16)
        return output
    # end def crypt_private
    def gensalt_extended(self, input=None):
        
        count_log2 = php_min(self.iteration_count_log2 + 8, 24)
        #// # This should be odd to not reveal weak DES keys, and the
        #// # maximum valid value is (2**24 - 1) which is odd anyway.
        count = 1 << count_log2 - 1
        output = "_"
        output += self.itoa64[count & 63]
        output += self.itoa64[count >> 6 & 63]
        output += self.itoa64[count >> 12 & 63]
        output += self.itoa64[count >> 18 & 63]
        output += self.encode64(input, 3)
        return output
    # end def gensalt_extended
    def gensalt_blowfish(self, input=None):
        
        #// # This one needs to use a different order of characters and a
        #// # different encoding scheme from the one in encode64() above.
        #// # We care because the last character in our encoded string will
        #// # only represent 2 bits.  While two known implementations of
        #// # bcrypt will happily accept and correct a salt string which
        #// # has the 4 unused bits set to non-zero, we do not want to take
        #// # chances and we also do not want to waste an additional byte
        #// # of entropy.
        itoa64 = "./ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        output = "$2a$"
        output += chr(php_ord("0") + self.iteration_count_log2 / 10)
        output += chr(php_ord("0") + self.iteration_count_log2 % 10)
        output += "$"
        i = 0
        while True:
            c1 = php_ord(input[i])
            i += 1
            output += itoa64[c1 >> 2]
            c1 = c1 & 3 << 4
            if i >= 16:
                output += itoa64[c1]
                break
            # end if
            c2 = php_ord(input[i])
            i += 1
            c1 |= c2 >> 4
            output += itoa64[c1]
            c1 = c2 & 15 << 2
            c2 = php_ord(input[i])
            i += 1
            c1 |= c2 >> 6
            output += itoa64[c1]
            output += itoa64[c2 & 63]
            
            if 1:
                break
            # end if
        # end while
        return output
    # end def gensalt_blowfish
    def hashpassword(self, password=None):
        
        if php_strlen(password) > 4096:
            return "*"
        # end if
        random = ""
        if CRYPT_BLOWFISH == 1 and (not self.portable_hashes):
            random = self.get_random_bytes(16)
            hash = crypt(password, self.gensalt_blowfish(random))
            if php_strlen(hash) == 60:
                return hash
            # end if
        # end if
        if CRYPT_EXT_DES == 1 and (not self.portable_hashes):
            if php_strlen(random) < 3:
                random = self.get_random_bytes(3)
            # end if
            hash = crypt(password, self.gensalt_extended(random))
            if php_strlen(hash) == 20:
                return hash
            # end if
        # end if
        if php_strlen(random) < 6:
            random = self.get_random_bytes(6)
        # end if
        hash = self.crypt_private(password, self.gensalt_private(random))
        if php_strlen(hash) == 34:
            return hash
        # end if
        #// # Returning '*' on error is safe here, but would _not_ be safe
        #// # in a crypt(3)-like function used _both_ for generating new
        #// # hashes and for validating passwords against existing hashes.
        return "*"
    # end def hashpassword
    def checkpassword(self, password=None, stored_hash=None):
        
        if php_strlen(password) > 4096:
            return False
        # end if
        hash = self.crypt_private(password, stored_hash)
        if hash[0] == "*":
            hash = crypt(password, stored_hash)
        # end if
        return hash == stored_hash
    # end def checkpassword
# end class PasswordHash
