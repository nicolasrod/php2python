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
#// Class ParagonIE_Sodium_Core_Base64UrlSafe
#// 
#// Copyright (c) 2016 - 2018 Paragon Initiative Enterprises.
#// Copyright (c) 2014 Steve "Sc00bz" Thomas (steve at tobtu dot com)
#//
class ParagonIE_Sodium_Core_Base64_UrlSafe():
    #// COPY ParagonIE_Sodium_Core_Base64_Common STARTING HERE
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
    #// COPY ParagonIE_Sodium_Core_Base64_Common ENDING HERE
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
        
        
        ret_ = -1
        #// if ($src > 0x40 && $src < 0x5b) $ret += $src - 0x41 + 1; // -64
        ret_ += 64 - src_ & src_ - 91 >> 8 & src_ - 64
        #// if ($src > 0x60 && $src < 0x7b) $ret += $src - 0x61 + 26 + 1; // -70
        ret_ += 96 - src_ & src_ - 123 >> 8 & src_ - 70
        #// if ($src > 0x2f && $src < 0x3a) $ret += $src - 0x30 + 52 + 1; // 5
        ret_ += 47 - src_ & src_ - 58 >> 8 & src_ + 5
        #// if ($src == 0x2c) $ret += 62 + 1;
        ret_ += 44 - src_ & src_ - 46 >> 8 & 63
        #// if ($src == 0x5f) ret += 63 + 1;
        ret_ += 94 - src_ & src_ - 96 >> 8 & 64
        return ret_
    # end def decode6bits
    #// 
    #// Uses bitwise operators instead of table-lookups to turn 8-bit integers
    #// into 6-bit integers.
    #// 
    #// @param int $src
    #// @return string
    #//
    def encode6bits(self, src_=None):
        
        
        diff_ = 65
        #// if ($src > 25) $diff += 0x61 - 0x41 - 26; // 6
        diff_ += 25 - src_ >> 8 & 6
        #// if ($src > 51) $diff += 0x30 - 0x61 - 26; // -75
        diff_ -= 51 - src_ >> 8 & 75
        #// if ($src > 61) $diff += 0x2d - 0x30 - 10; // -13
        diff_ -= 61 - src_ >> 8 & 13
        #// if ($src > 62) $diff += 0x5f - 0x2b - 1; // 3
        diff_ += 62 - src_ >> 8 & 49
        return pack("C", src_ + diff_)
    # end def encode6bits
# end class ParagonIE_Sodium_Core_Base64_UrlSafe
