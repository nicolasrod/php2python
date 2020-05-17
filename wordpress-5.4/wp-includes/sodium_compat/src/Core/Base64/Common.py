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
#// Class ParagonIE_Sodium_Core_Base64
#// 
#// Copyright (c) 2016 - 2018 Paragon Initiative Enterprises.
#// Copyright (c) 2014 Steve "Sc00bz" Thomas (steve at tobtu dot com)
#// 
#// We have to copy/paste the contents into the variant files because PHP 5.2
#// doesn't support late static binding, and we have no better workaround
#// available that won't break PHP 7+. Therefore, we're forced to duplicate code.
#//
class ParagonIE_Sodium_Core_Base64_Common():
    #// 
    #// Encode into Base64
    #// 
    #// Base64 character set "[A-Z][a-z][0-9]+/"
    #// 
    #// @param string $src
    #// @return string
    #// @throws TypeError
    #//
    @classmethod
    def encode(self, src_=None):
        
        
        return self.doencode(src_, True)
    # end def encode
    #// 
    #// Encode into Base64, no = padding
    #// 
    #// Base64 character set "[A-Z][a-z][0-9]+/"
    #// 
    #// @param string $src
    #// @return string
    #// @throws TypeError
    #//
    @classmethod
    def encodeunpadded(self, src_=None):
        
        
        return self.doencode(src_, False)
    # end def encodeunpadded
    #// 
    #// @param string $src
    #// @param bool $pad   Include = padding?
    #// @return string
    #// @throws TypeError
    #//
    def doencode(self, src_=None, pad_=None):
        if pad_ is None:
            pad_ = True
        # end if
        
        dest_ = ""
        srcLen_ = ParagonIE_Sodium_Core_Util.strlen(src_)
        #// Main loop (no padding):
        i_ = 0
        while i_ + 3 <= srcLen_:
            
            #// @var array<int, int> $chunk
            chunk_ = unpack("C*", ParagonIE_Sodium_Core_Util.substr(src_, i_, 3))
            b0_ = chunk_[1]
            b1_ = chunk_[2]
            b2_ = chunk_[3]
            dest_ += self.encode6bits(b0_ >> 2) + self.encode6bits(b0_ << 4 | b1_ >> 4 & 63) + self.encode6bits(b1_ << 2 | b2_ >> 6 & 63) + self.encode6bits(b2_ & 63)
            i_ += 3
        # end while
        #// The last chunk, which may have padding:
        if i_ < srcLen_:
            #// @var array<int, int> $chunk
            chunk_ = unpack("C*", ParagonIE_Sodium_Core_Util.substr(src_, i_, srcLen_ - i_))
            b0_ = chunk_[1]
            if i_ + 1 < srcLen_:
                b1_ = chunk_[2]
                dest_ += self.encode6bits(b0_ >> 2) + self.encode6bits(b0_ << 4 | b1_ >> 4 & 63) + self.encode6bits(b1_ << 2 & 63)
                if pad_:
                    dest_ += "="
                # end if
            else:
                dest_ += self.encode6bits(b0_ >> 2) + self.encode6bits(b0_ << 4 & 63)
                if pad_:
                    dest_ += "=="
                # end if
            # end if
        # end if
        return dest_
    # end def doencode
    #// 
    #// decode from base64 into binary
    #// 
    #// Base64 character set "./[A-Z][a-z][0-9]"
    #// 
    #// @param string $src
    #// @param bool $strictPadding
    #// @return string
    #// @throws RangeException
    #// @throws TypeError
    #// @psalm-suppress RedundantCondition
    #//
    @classmethod
    def decode(self, src_=None, strictPadding_=None):
        if strictPadding_ is None:
            strictPadding_ = False
        # end if
        
        #// Remove padding
        srcLen_ = ParagonIE_Sodium_Core_Util.strlen(src_)
        if srcLen_ == 0:
            return ""
        # end if
        if strictPadding_:
            if srcLen_ & 3 == 0:
                if src_[srcLen_ - 1] == "=":
                    srcLen_ -= 1
                    if src_[srcLen_ - 1] == "=":
                        srcLen_ -= 1
                    # end if
                # end if
            # end if
            if srcLen_ & 3 == 1:
                raise php_new_class("RangeException", lambda : RangeException("Incorrect padding"))
            # end if
            if src_[srcLen_ - 1] == "=":
                raise php_new_class("RangeException", lambda : RangeException("Incorrect padding"))
            # end if
        else:
            src_ = php_rtrim(src_, "=")
            srcLen_ = ParagonIE_Sodium_Core_Util.strlen(src_)
        # end if
        err_ = 0
        dest_ = ""
        #// Main loop (no padding):
        i_ = 0
        while i_ + 4 <= srcLen_:
            
            #// @var array<int, int> $chunk
            chunk_ = unpack("C*", ParagonIE_Sodium_Core_Util.substr(src_, i_, 4))
            c0_ = self.decode6bits(chunk_[1])
            c1_ = self.decode6bits(chunk_[2])
            c2_ = self.decode6bits(chunk_[3])
            c3_ = self.decode6bits(chunk_[4])
            dest_ += pack("CCC", c0_ << 2 | c1_ >> 4 & 255, c1_ << 4 | c2_ >> 2 & 255, c2_ << 6 | c3_ & 255)
            err_ |= c0_ | c1_ | c2_ | c3_ >> 8
            i_ += 4
        # end while
        #// The last chunk, which may have padding:
        if i_ < srcLen_:
            #// @var array<int, int> $chunk
            chunk_ = unpack("C*", ParagonIE_Sodium_Core_Util.substr(src_, i_, srcLen_ - i_))
            c0_ = self.decode6bits(chunk_[1])
            if i_ + 2 < srcLen_:
                c1_ = self.decode6bits(chunk_[2])
                c2_ = self.decode6bits(chunk_[3])
                dest_ += pack("CC", c0_ << 2 | c1_ >> 4 & 255, c1_ << 4 | c2_ >> 2 & 255)
                err_ |= c0_ | c1_ | c2_ >> 8
            elif i_ + 1 < srcLen_:
                c1_ = self.decode6bits(chunk_[2])
                dest_ += pack("C", c0_ << 2 | c1_ >> 4 & 255)
                err_ |= c0_ | c1_ >> 8
            elif i_ < srcLen_ and strictPadding_:
                err_ |= 1
            # end if
        # end if
        #// @var bool $check
        check_ = err_ == 0
        if (not check_):
            raise php_new_class("RangeException", lambda : RangeException("Base64::decode() only expects characters in the correct base64 alphabet"))
        # end if
        return dest_
    # end def decode
    #// 
    #// Uses bitwise operators instead of table-lookups to turn 6-bit integers
    #// into 8-bit integers.
    #// 
    #// Base64 character set:
    #// [A-Z]      [a-z]      [0-9]      +
    #// 0x41-0x5a, 0x61-0x7a, 0x30-0x39, 0x2b, 0x2f
    #// 
    #// @param int $src
    #// @return int
    #//
    def decode6bits(self, src_=None):
        
        
        pass
    # end def decode6bits
    #// 
    #// Uses bitwise operators instead of table-lookups to turn 8-bit integers
    #// into 6-bit integers.
    #// 
    #// @param int $src
    #// @return string
    #//
    def encode6bits(self, src_=None):
        
        
        pass
    # end def encode6bits
# end class ParagonIE_Sodium_Core_Base64_Common
