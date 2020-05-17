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
    def __init__(self, iteration_count_log2_=None, portable_hashes_=None):
        
        
        self.itoa64 = "./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        if iteration_count_log2_ < 4 or iteration_count_log2_ > 31:
            iteration_count_log2_ = 8
        # end if
        self.iteration_count_log2 = iteration_count_log2_
        self.portable_hashes = portable_hashes_
        self.random_state = php_microtime() + php_uniqid(rand(), True)
        pass
    # end def __init__
    #// 
    #// PHP4 constructor.
    #//
    def passwordhash(self, iteration_count_log2_=None, portable_hashes_=None):
        
        
        self.__init__(iteration_count_log2_, portable_hashes_)
    # end def passwordhash
    def get_random_bytes(self, count_=None):
        
        
        output_ = ""
        fh_ = php_no_error(lambda: fopen("/dev/urandom", "rb"))
        if php_no_error(lambda: php_is_readable("/dev/urandom")) and fh_:
            output_ = fread(fh_, count_)
            php_fclose(fh_)
        # end if
        if php_strlen(output_) < count_:
            output_ = ""
            i_ = 0
            while i_ < count_:
                
                self.random_state = php_md5(php_microtime() + self.random_state)
                output_ += pack("H*", php_md5(self.random_state))
                i_ += 16
            # end while
            output_ = php_substr(output_, 0, count_)
        # end if
        return output_
    # end def get_random_bytes
    def encode64(self, input_=None, count_=None):
        
        
        output_ = ""
        i_ = 0
        while True:
            value_ = php_ord(input_[i_])
            i_ += 1
            output_ += self.itoa64[value_ & 63]
            if i_ < count_:
                value_ |= php_ord(input_[i_]) << 8
            # end if
            output_ += self.itoa64[value_ >> 6 & 63]
            i_ += 1
            if i_ >= count_:
                break
            # end if
            i_ += 1
            if i_ < count_:
                value_ |= php_ord(input_[i_]) << 16
            # end if
            output_ += self.itoa64[value_ >> 12 & 63]
            i_ += 1
            if i_ >= count_:
                break
            # end if
            i_ += 1
            output_ += self.itoa64[value_ >> 18 & 63]
            
            if i_ < count_:
                break
            # end if
        # end while
        return output_
    # end def encode64
    def gensalt_private(self, input_=None):
        
        
        output_ = "$P$"
        output_ += self.itoa64[php_min(self.iteration_count_log2 + 5 if PHP_VERSION >= "5" else 3, 30)]
        output_ += self.encode64(input_, 6)
        return output_
    # end def gensalt_private
    def crypt_private(self, password_=None, setting_=None):
        
        
        output_ = "*0"
        if php_substr(setting_, 0, 2) == output_:
            output_ = "*1"
        # end if
        id_ = php_substr(setting_, 0, 3)
        #// # We use "$P$", phpBB3 uses "$H$" for the same thing
        if id_ != "$P$" and id_ != "$H$":
            return output_
        # end if
        count_log2_ = php_strpos(self.itoa64, setting_[3])
        if count_log2_ < 7 or count_log2_ > 30:
            return output_
        # end if
        count_ = 1 << count_log2_
        salt_ = php_substr(setting_, 4, 8)
        if php_strlen(salt_) != 8:
            return output_
        # end if
        #// # We're kind of forced to use MD5 here since it's the only
        #// # cryptographic primitive available in all versions of PHP
        #// # currently in use.  To implement our own low-level crypto
        #// # in PHP would result in much worse performance and
        #// # consequently in lower iteration counts and hashes that are
        #// # quicker to crack (by non-PHP code).
        if PHP_VERSION >= "5":
            hash_ = php_md5(salt_ + password_, True)
            while True:
                hash_ = php_md5(hash_ + password_, True)
                count_ -= 1
                if count_:
                    break
                # end if
            # end while
        else:
            hash_ = pack("H*", php_md5(salt_ + password_))
            while True:
                hash_ = pack("H*", php_md5(hash_ + password_))
                count_ -= 1
                if count_:
                    break
                # end if
            # end while
        # end if
        output_ = php_substr(setting_, 0, 12)
        output_ += self.encode64(hash_, 16)
        return output_
    # end def crypt_private
    def gensalt_extended(self, input_=None):
        
        
        count_log2_ = php_min(self.iteration_count_log2 + 8, 24)
        #// # This should be odd to not reveal weak DES keys, and the
        #// # maximum valid value is (2**24 - 1) which is odd anyway.
        count_ = 1 << count_log2_ - 1
        output_ = "_"
        output_ += self.itoa64[count_ & 63]
        output_ += self.itoa64[count_ >> 6 & 63]
        output_ += self.itoa64[count_ >> 12 & 63]
        output_ += self.itoa64[count_ >> 18 & 63]
        output_ += self.encode64(input_, 3)
        return output_
    # end def gensalt_extended
    def gensalt_blowfish(self, input_=None):
        
        
        #// # This one needs to use a different order of characters and a
        #// # different encoding scheme from the one in encode64() above.
        #// # We care because the last character in our encoded string will
        #// # only represent 2 bits.  While two known implementations of
        #// # bcrypt will happily accept and correct a salt string which
        #// # has the 4 unused bits set to non-zero, we do not want to take
        #// # chances and we also do not want to waste an additional byte
        #// # of entropy.
        itoa64_ = "./ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        output_ = "$2a$"
        output_ += chr(php_ord("0") + self.iteration_count_log2 / 10)
        output_ += chr(php_ord("0") + self.iteration_count_log2 % 10)
        output_ += "$"
        i_ = 0
        while True:
            c1_ = php_ord(input_[i_])
            i_ += 1
            output_ += itoa64_[c1_ >> 2]
            c1_ = c1_ & 3 << 4
            if i_ >= 16:
                output_ += itoa64_[c1_]
                break
            # end if
            c2_ = php_ord(input_[i_])
            i_ += 1
            c1_ |= c2_ >> 4
            output_ += itoa64_[c1_]
            c1_ = c2_ & 15 << 2
            c2_ = php_ord(input_[i_])
            i_ += 1
            c1_ |= c2_ >> 6
            output_ += itoa64_[c1_]
            output_ += itoa64_[c2_ & 63]
            
            if 1:
                break
            # end if
        # end while
        return output_
    # end def gensalt_blowfish
    def hashpassword(self, password_=None):
        
        
        if php_strlen(password_) > 4096:
            return "*"
        # end if
        random_ = ""
        if CRYPT_BLOWFISH == 1 and (not self.portable_hashes):
            random_ = self.get_random_bytes(16)
            hash_ = crypt(password_, self.gensalt_blowfish(random_))
            if php_strlen(hash_) == 60:
                return hash_
            # end if
        # end if
        if CRYPT_EXT_DES == 1 and (not self.portable_hashes):
            if php_strlen(random_) < 3:
                random_ = self.get_random_bytes(3)
            # end if
            hash_ = crypt(password_, self.gensalt_extended(random_))
            if php_strlen(hash_) == 20:
                return hash_
            # end if
        # end if
        if php_strlen(random_) < 6:
            random_ = self.get_random_bytes(6)
        # end if
        hash_ = self.crypt_private(password_, self.gensalt_private(random_))
        if php_strlen(hash_) == 34:
            return hash_
        # end if
        #// # Returning '*' on error is safe here, but would _not_ be safe
        #// # in a crypt(3)-like function used _both_ for generating new
        #// # hashes and for validating passwords against existing hashes.
        return "*"
    # end def hashpassword
    def checkpassword(self, password_=None, stored_hash_=None):
        
        
        if php_strlen(password_) > 4096:
            return False
        # end if
        hash_ = self.crypt_private(password_, stored_hash_)
        if hash_[0] == "*":
            hash_ = crypt(password_, stored_hash_)
        # end if
        return hash_ == stored_hash_
    # end def checkpassword
# end class PasswordHash
