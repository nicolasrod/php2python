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
if php_class_exists("ParagonIE_Sodium_Core32_Salsa20", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core32_Salsa20
#//
class ParagonIE_Sodium_Core32_Salsa20(ParagonIE_Sodium_Core32_Util):
    ROUNDS = 20
    #// 
    #// Calculate an salsa20 hash of a single block
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $in
    #// @param string $k
    #// @param string|null $c
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def core_salsa20(self, in_=None, k=None, c=None):
        
        #// 
        #// @var ParagonIE_Sodium_Core32_Int32 $x0
        #// @var ParagonIE_Sodium_Core32_Int32 $x1
        #// @var ParagonIE_Sodium_Core32_Int32 $x2
        #// @var ParagonIE_Sodium_Core32_Int32 $x3
        #// @var ParagonIE_Sodium_Core32_Int32 $x4
        #// @var ParagonIE_Sodium_Core32_Int32 $x5
        #// @var ParagonIE_Sodium_Core32_Int32 $x6
        #// @var ParagonIE_Sodium_Core32_Int32 $x7
        #// @var ParagonIE_Sodium_Core32_Int32 $x8
        #// @var ParagonIE_Sodium_Core32_Int32 $x9
        #// @var ParagonIE_Sodium_Core32_Int32 $x10
        #// @var ParagonIE_Sodium_Core32_Int32 $x11
        #// @var ParagonIE_Sodium_Core32_Int32 $x12
        #// @var ParagonIE_Sodium_Core32_Int32 $x13
        #// @var ParagonIE_Sodium_Core32_Int32 $x14
        #// @var ParagonIE_Sodium_Core32_Int32 $x15
        #// @var ParagonIE_Sodium_Core32_Int32 $j0
        #// @var ParagonIE_Sodium_Core32_Int32 $j1
        #// @var ParagonIE_Sodium_Core32_Int32 $j2
        #// @var ParagonIE_Sodium_Core32_Int32 $j3
        #// @var ParagonIE_Sodium_Core32_Int32 $j4
        #// @var ParagonIE_Sodium_Core32_Int32 $j5
        #// @var ParagonIE_Sodium_Core32_Int32 $j6
        #// @var ParagonIE_Sodium_Core32_Int32 $j7
        #// @var ParagonIE_Sodium_Core32_Int32 $j8
        #// @var ParagonIE_Sodium_Core32_Int32 $j9
        #// @var ParagonIE_Sodium_Core32_Int32 $j10
        #// @var ParagonIE_Sodium_Core32_Int32 $j11
        #// @var ParagonIE_Sodium_Core32_Int32 $j12
        #// @var ParagonIE_Sodium_Core32_Int32 $j13
        #// @var ParagonIE_Sodium_Core32_Int32 $j14
        #// @var ParagonIE_Sodium_Core32_Int32 $j15
        #//
        if self.strlen(k) < 32:
            raise php_new_class("RangeException", lambda : RangeException("Key must be 32 bytes long"))
        # end if
        if c == None:
            x0 = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32(Array(24944, 30821)))
            x5 = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32(Array(13088, 25710)))
            x10 = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32(Array(31074, 11570)))
            x15 = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32(Array(27424, 25972)))
        else:
            x0 = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(c, 0, 4))
            x5 = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(c, 4, 4))
            x10 = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(c, 8, 4))
            x15 = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(c, 12, 4))
        # end if
        x1 = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(k, 0, 4))
        x2 = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(k, 4, 4))
        x3 = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(k, 8, 4))
        x4 = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(k, 12, 4))
        x6 = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(in_, 0, 4))
        x7 = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(in_, 4, 4))
        x8 = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(in_, 8, 4))
        x9 = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(in_, 12, 4))
        x11 = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(k, 16, 4))
        x12 = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(k, 20, 4))
        x13 = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(k, 24, 4))
        x14 = ParagonIE_Sodium_Core32_Int32.fromreversestring(self.substr(k, 28, 4))
        j0 = copy.deepcopy(x0)
        j1 = copy.deepcopy(x1)
        j2 = copy.deepcopy(x2)
        j3 = copy.deepcopy(x3)
        j4 = copy.deepcopy(x4)
        j5 = copy.deepcopy(x5)
        j6 = copy.deepcopy(x6)
        j7 = copy.deepcopy(x7)
        j8 = copy.deepcopy(x8)
        j9 = copy.deepcopy(x9)
        j10 = copy.deepcopy(x10)
        j11 = copy.deepcopy(x11)
        j12 = copy.deepcopy(x12)
        j13 = copy.deepcopy(x13)
        j14 = copy.deepcopy(x14)
        j15 = copy.deepcopy(x15)
        i = self.ROUNDS
        while i > 0:
            
            x4 = x4.xorint32(x0.addint32(x12).rotateleft(7))
            x8 = x8.xorint32(x4.addint32(x0).rotateleft(9))
            x12 = x12.xorint32(x8.addint32(x4).rotateleft(13))
            x0 = x0.xorint32(x12.addint32(x8).rotateleft(18))
            x9 = x9.xorint32(x5.addint32(x1).rotateleft(7))
            x13 = x13.xorint32(x9.addint32(x5).rotateleft(9))
            x1 = x1.xorint32(x13.addint32(x9).rotateleft(13))
            x5 = x5.xorint32(x1.addint32(x13).rotateleft(18))
            x14 = x14.xorint32(x10.addint32(x6).rotateleft(7))
            x2 = x2.xorint32(x14.addint32(x10).rotateleft(9))
            x6 = x6.xorint32(x2.addint32(x14).rotateleft(13))
            x10 = x10.xorint32(x6.addint32(x2).rotateleft(18))
            x3 = x3.xorint32(x15.addint32(x11).rotateleft(7))
            x7 = x7.xorint32(x3.addint32(x15).rotateleft(9))
            x11 = x11.xorint32(x7.addint32(x3).rotateleft(13))
            x15 = x15.xorint32(x11.addint32(x7).rotateleft(18))
            x1 = x1.xorint32(x0.addint32(x3).rotateleft(7))
            x2 = x2.xorint32(x1.addint32(x0).rotateleft(9))
            x3 = x3.xorint32(x2.addint32(x1).rotateleft(13))
            x0 = x0.xorint32(x3.addint32(x2).rotateleft(18))
            x6 = x6.xorint32(x5.addint32(x4).rotateleft(7))
            x7 = x7.xorint32(x6.addint32(x5).rotateleft(9))
            x4 = x4.xorint32(x7.addint32(x6).rotateleft(13))
            x5 = x5.xorint32(x4.addint32(x7).rotateleft(18))
            x11 = x11.xorint32(x10.addint32(x9).rotateleft(7))
            x8 = x8.xorint32(x11.addint32(x10).rotateleft(9))
            x9 = x9.xorint32(x8.addint32(x11).rotateleft(13))
            x10 = x10.xorint32(x9.addint32(x8).rotateleft(18))
            x12 = x12.xorint32(x15.addint32(x14).rotateleft(7))
            x13 = x13.xorint32(x12.addint32(x15).rotateleft(9))
            x14 = x14.xorint32(x13.addint32(x12).rotateleft(13))
            x15 = x15.xorint32(x14.addint32(x13).rotateleft(18))
            i -= 2
        # end while
        x0 = x0.addint32(j0)
        x1 = x1.addint32(j1)
        x2 = x2.addint32(j2)
        x3 = x3.addint32(j3)
        x4 = x4.addint32(j4)
        x5 = x5.addint32(j5)
        x6 = x6.addint32(j6)
        x7 = x7.addint32(j7)
        x8 = x8.addint32(j8)
        x9 = x9.addint32(j9)
        x10 = x10.addint32(j10)
        x11 = x11.addint32(j11)
        x12 = x12.addint32(j12)
        x13 = x13.addint32(j13)
        x14 = x14.addint32(j14)
        x15 = x15.addint32(j15)
        return x0.toreversestring() + x1.toreversestring() + x2.toreversestring() + x3.toreversestring() + x4.toreversestring() + x5.toreversestring() + x6.toreversestring() + x7.toreversestring() + x8.toreversestring() + x9.toreversestring() + x10.toreversestring() + x11.toreversestring() + x12.toreversestring() + x13.toreversestring() + x14.toreversestring() + x15.toreversestring()
    # end def core_salsa20
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int $len
    #// @param string $nonce
    #// @param string $key
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def salsa20(self, len=None, nonce=None, key=None):
        
        if self.strlen(key) != 32:
            raise php_new_class("RangeException", lambda : RangeException("Key must be 32 bytes long"))
        # end if
        kcopy = "" + key
        in_ = self.substr(nonce, 0, 8) + php_str_repeat(" ", 8)
        c = ""
        while True:
            
            if not (len >= 64):
                break
            # end if
            c += self.core_salsa20(in_, kcopy, None)
            u = 1
            #// Internal counter.
            i = 8
            while i < 16:
                
                u += self.chrtoint(in_[i])
                in_[i] = self.inttochr(u & 255)
                u >>= 8
                i += 1
            # end while
            len -= 64
        # end while
        if len > 0:
            c += self.substr(self.core_salsa20(in_, kcopy, None), 0, len)
        # end if
        try: 
            ParagonIE_Sodium_Compat.memzero(kcopy)
        except SodiumException as ex:
            kcopy = None
        # end try
        return c
    # end def salsa20
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $m
    #// @param string $n
    #// @param int $ic
    #// @param string $k
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def salsa20_xor_ic(self, m=None, n=None, ic=None, k=None):
        
        mlen = self.strlen(m)
        if mlen < 1:
            return ""
        # end if
        kcopy = self.substr(k, 0, 32)
        in_ = self.substr(n, 0, 8)
        #// Initialize the counter
        in_ += ParagonIE_Sodium_Core32_Util.store64_le(ic)
        c = ""
        while True:
            
            if not (mlen >= 64):
                break
            # end if
            block = self.core_salsa20(in_, kcopy, None)
            c += self.xorstrings(self.substr(m, 0, 64), self.substr(block, 0, 64))
            u = 1
            i = 8
            while i < 16:
                
                u += self.chrtoint(in_[i])
                in_[i] = self.inttochr(u & 255)
                u >>= 8
                i += 1
            # end while
            mlen -= 64
            m = self.substr(m, 64)
        # end while
        if mlen:
            block = self.core_salsa20(in_, kcopy, None)
            c += self.xorstrings(self.substr(m, 0, mlen), self.substr(block, 0, mlen))
        # end if
        try: 
            ParagonIE_Sodium_Compat.memzero(block)
            ParagonIE_Sodium_Compat.memzero(kcopy)
        except SodiumException as ex:
            block = None
            kcopy = None
        # end try
        return c
    # end def salsa20_xor_ic
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $message
    #// @param string $nonce
    #// @param string $key
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def salsa20_xor(self, message=None, nonce=None, key=None):
        
        return self.xorstrings(message, self.salsa20(self.strlen(message), nonce, key))
    # end def salsa20_xor
# end class ParagonIE_Sodium_Core32_Salsa20
