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
if php_class_exists("ParagonIE_Sodium_Core32_Curve25519", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core32_Curve25519
#// 
#// Implements Curve25519 core functions
#// 
#// Based on the ref10 curve25519 code provided by libsodium
#// 
#// @ref https://github.com/jedisct1/libsodium/blob/master/src/libsodium/crypto_core/curve25519/ref10/curve25519_ref10.c
#//
class ParagonIE_Sodium_Core32_Curve25519(ParagonIE_Sodium_Core32_Curve25519_H):
    #// 
    #// Get a field element of size 10 with a value of 0
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @return ParagonIE_Sodium_Core32_Curve25519_Fe
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def fe_0(self):
        
        return ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(Array(php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32()), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32()), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32()), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32()), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32()), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32()), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32()), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32()), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32()), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())))
    # end def fe_0
    #// 
    #// Get a field element of size 10 with a value of 1
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @return ParagonIE_Sodium_Core32_Curve25519_Fe
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def fe_1(self):
        
        return ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(Array(ParagonIE_Sodium_Core32_Int32.fromint(1), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32()), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32()), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32()), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32()), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32()), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32()), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32()), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32()), php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())))
    # end def fe_1
    #// 
    #// Add two field elements.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $f
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $g
    #// @return ParagonIE_Sodium_Core32_Curve25519_Fe
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedAssignment
    #// @psalm-suppress MixedMethodCall
    #//
    @classmethod
    def fe_add(self, f=None, g=None):
        
        arr = Array()
        i = 0
        while i < 10:
            
            arr[i] = f[i].addint32(g[i])
            i += 1
        # end while
        #// @var array<int, ParagonIE_Sodium_Core32_Int32> $arr
        return ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(arr)
    # end def fe_add
    #// 
    #// Constant-time conditional move.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $f
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $g
    #// @param int $b
    #// @return ParagonIE_Sodium_Core32_Curve25519_Fe
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedAssignment
    #// @psalm-suppress MixedMethodCall
    #//
    @classmethod
    def fe_cmov(self, f=None, g=None, b=0):
        
        #// @var array<int, ParagonIE_Sodium_Core32_Int32> $h
        h = Array()
        i = 0
        while i < 10:
            
            if (not type(f[i]).__name__ == "ParagonIE_Sodium_Core32_Int32"):
                raise php_new_class("TypeError", lambda : TypeError("Expected Int32"))
            # end if
            if (not type(g[i]).__name__ == "ParagonIE_Sodium_Core32_Int32"):
                raise php_new_class("TypeError", lambda : TypeError("Expected Int32"))
            # end if
            h[i] = f[i].xorint32(f[i].xorint32(g[i]).mask(b))
            i += 1
        # end while
        #// @var array<int, ParagonIE_Sodium_Core32_Int32> $h
        return ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(h)
    # end def fe_cmov
    #// 
    #// Create a copy of a field element.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $f
    #// @return ParagonIE_Sodium_Core32_Curve25519_Fe
    #//
    @classmethod
    def fe_copy(self, f=None):
        
        h = copy.deepcopy(f)
        return h
    # end def fe_copy
    #// 
    #// Give: 32-byte string.
    #// Receive: A field element object to use for internal calculations.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $s
    #// @return ParagonIE_Sodium_Core32_Curve25519_Fe
    #// @throws RangeException
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedMethodCall
    #//
    @classmethod
    def fe_frombytes(self, s=None):
        
        if self.strlen(s) != 32:
            raise php_new_class("RangeException", lambda : RangeException("Expected a 32-byte string."))
        # end if
        #// @var ParagonIE_Sodium_Core32_Int32 $h0
        h0 = ParagonIE_Sodium_Core32_Int32.fromint(self.load_4(s))
        #// @var ParagonIE_Sodium_Core32_Int32 $h1
        h1 = ParagonIE_Sodium_Core32_Int32.fromint(self.load_3(self.substr(s, 4, 3)) << 6)
        #// @var ParagonIE_Sodium_Core32_Int32 $h2
        h2 = ParagonIE_Sodium_Core32_Int32.fromint(self.load_3(self.substr(s, 7, 3)) << 5)
        #// @var ParagonIE_Sodium_Core32_Int32 $h3
        h3 = ParagonIE_Sodium_Core32_Int32.fromint(self.load_3(self.substr(s, 10, 3)) << 3)
        #// @var ParagonIE_Sodium_Core32_Int32 $h4
        h4 = ParagonIE_Sodium_Core32_Int32.fromint(self.load_3(self.substr(s, 13, 3)) << 2)
        #// @var ParagonIE_Sodium_Core32_Int32 $h5
        h5 = ParagonIE_Sodium_Core32_Int32.fromint(self.load_4(self.substr(s, 16, 4)))
        #// @var ParagonIE_Sodium_Core32_Int32 $h6
        h6 = ParagonIE_Sodium_Core32_Int32.fromint(self.load_3(self.substr(s, 20, 3)) << 7)
        #// @var ParagonIE_Sodium_Core32_Int32 $h7
        h7 = ParagonIE_Sodium_Core32_Int32.fromint(self.load_3(self.substr(s, 23, 3)) << 5)
        #// @var ParagonIE_Sodium_Core32_Int32 $h8
        h8 = ParagonIE_Sodium_Core32_Int32.fromint(self.load_3(self.substr(s, 26, 3)) << 4)
        #// @var ParagonIE_Sodium_Core32_Int32 $h9
        h9 = ParagonIE_Sodium_Core32_Int32.fromint(self.load_3(self.substr(s, 29, 3)) & 8388607 << 2)
        carry9 = h9.addint(1 << 24).shiftright(25)
        h0 = h0.addint32(carry9.mulint(19, 5))
        h9 = h9.subint32(carry9.shiftleft(25))
        carry1 = h1.addint(1 << 24).shiftright(25)
        h2 = h2.addint32(carry1)
        h1 = h1.subint32(carry1.shiftleft(25))
        carry3 = h3.addint(1 << 24).shiftright(25)
        h4 = h4.addint32(carry3)
        h3 = h3.subint32(carry3.shiftleft(25))
        carry5 = h5.addint(1 << 24).shiftright(25)
        h6 = h6.addint32(carry5)
        h5 = h5.subint32(carry5.shiftleft(25))
        carry7 = h7.addint(1 << 24).shiftright(25)
        h8 = h8.addint32(carry7)
        h7 = h7.subint32(carry7.shiftleft(25))
        carry0 = h0.addint(1 << 25).shiftright(26)
        h1 = h1.addint32(carry0)
        h0 = h0.subint32(carry0.shiftleft(26))
        carry2 = h2.addint(1 << 25).shiftright(26)
        h3 = h3.addint32(carry2)
        h2 = h2.subint32(carry2.shiftleft(26))
        carry4 = h4.addint(1 << 25).shiftright(26)
        h5 = h5.addint32(carry4)
        h4 = h4.subint32(carry4.shiftleft(26))
        carry6 = h6.addint(1 << 25).shiftright(26)
        h7 = h7.addint32(carry6)
        h6 = h6.subint32(carry6.shiftleft(26))
        carry8 = h8.addint(1 << 25).shiftright(26)
        h9 = h9.addint32(carry8)
        h8 = h8.subint32(carry8.shiftleft(26))
        return ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(Array(h0, h1, h2, h3, h4, h5, h6, h7, h8, h9))
    # end def fe_frombytes
    #// 
    #// Convert a field element to a byte string.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $h
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedAssignment
    #// @psalm-suppress MixedMethodCall
    #//
    @classmethod
    def fe_tobytes(self, h=None):
        
        #// 
        #// @var ParagonIE_Sodium_Core32_Int64[] $f
        #// @var ParagonIE_Sodium_Core32_Int64 $q
        #//
        f = Array()
        i = 0
        while i < 10:
            
            f[i] = h[i].toint64()
            i += 1
        # end while
        q = f[9].mulint(19, 5).addint(1 << 14).shiftright(25).addint64(f[0]).shiftright(26).addint64(f[1]).shiftright(25).addint64(f[2]).shiftright(26).addint64(f[3]).shiftright(25).addint64(f[4]).shiftright(26).addint64(f[5]).shiftright(25).addint64(f[6]).shiftright(26).addint64(f[7]).shiftright(25).addint64(f[8]).shiftright(26).addint64(f[9]).shiftright(25)
        f[0] = f[0].addint64(q.mulint(19, 5))
        carry0 = f[0].shiftright(26)
        f[1] = f[1].addint64(carry0)
        f[0] = f[0].subint64(carry0.shiftleft(26))
        carry1 = f[1].shiftright(25)
        f[2] = f[2].addint64(carry1)
        f[1] = f[1].subint64(carry1.shiftleft(25))
        carry2 = f[2].shiftright(26)
        f[3] = f[3].addint64(carry2)
        f[2] = f[2].subint64(carry2.shiftleft(26))
        carry3 = f[3].shiftright(25)
        f[4] = f[4].addint64(carry3)
        f[3] = f[3].subint64(carry3.shiftleft(25))
        carry4 = f[4].shiftright(26)
        f[5] = f[5].addint64(carry4)
        f[4] = f[4].subint64(carry4.shiftleft(26))
        carry5 = f[5].shiftright(25)
        f[6] = f[6].addint64(carry5)
        f[5] = f[5].subint64(carry5.shiftleft(25))
        carry6 = f[6].shiftright(26)
        f[7] = f[7].addint64(carry6)
        f[6] = f[6].subint64(carry6.shiftleft(26))
        carry7 = f[7].shiftright(25)
        f[8] = f[8].addint64(carry7)
        f[7] = f[7].subint64(carry7.shiftleft(25))
        carry8 = f[8].shiftright(26)
        f[9] = f[9].addint64(carry8)
        f[8] = f[8].subint64(carry8.shiftleft(26))
        carry9 = f[9].shiftright(25)
        f[9] = f[9].subint64(carry9.shiftleft(25))
        #// @var int $h0
        h0 = f[0].toint32().toint()
        #// @var int $h1
        h1 = f[1].toint32().toint()
        #// @var int $h2
        h2 = f[2].toint32().toint()
        #// @var int $h3
        h3 = f[3].toint32().toint()
        #// @var int $h4
        h4 = f[4].toint32().toint()
        #// @var int $h5
        h5 = f[5].toint32().toint()
        #// @var int $h6
        h6 = f[6].toint32().toint()
        #// @var int $h7
        h7 = f[7].toint32().toint()
        #// @var int $h8
        h8 = f[8].toint32().toint()
        #// @var int $h9
        h9 = f[9].toint32().toint()
        #// 
        #// @var array<int, int>
        #//
        s = Array(php_int(h0 >> 0 & 255), php_int(h0 >> 8 & 255), php_int(h0 >> 16 & 255), php_int(h0 >> 24 | h1 << 2 & 255), php_int(h1 >> 6 & 255), php_int(h1 >> 14 & 255), php_int(h1 >> 22 | h2 << 3 & 255), php_int(h2 >> 5 & 255), php_int(h2 >> 13 & 255), php_int(h2 >> 21 | h3 << 5 & 255), php_int(h3 >> 3 & 255), php_int(h3 >> 11 & 255), php_int(h3 >> 19 | h4 << 6 & 255), php_int(h4 >> 2 & 255), php_int(h4 >> 10 & 255), php_int(h4 >> 18 & 255), php_int(h5 >> 0 & 255), php_int(h5 >> 8 & 255), php_int(h5 >> 16 & 255), php_int(h5 >> 24 | h6 << 1 & 255), php_int(h6 >> 7 & 255), php_int(h6 >> 15 & 255), php_int(h6 >> 23 | h7 << 3 & 255), php_int(h7 >> 5 & 255), php_int(h7 >> 13 & 255), php_int(h7 >> 21 | h8 << 4 & 255), php_int(h8 >> 4 & 255), php_int(h8 >> 12 & 255), php_int(h8 >> 20 | h9 << 6 & 255), php_int(h9 >> 2 & 255), php_int(h9 >> 10 & 255), php_int(h9 >> 18 & 255))
        return self.intarraytostring(s)
    # end def fe_tobytes
    #// 
    #// Is a field element negative? (1 = yes, 0 = no. Used in calculations.)
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $f
    #// @return int
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def fe_isnegative(self, f=None):
        
        str = self.fe_tobytes(f)
        return php_int(self.chrtoint(str[0]) & 1)
    # end def fe_isnegative
    #// 
    #// Returns 0 if this field element results in all NUL bytes.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $f
    #// @return bool
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def fe_isnonzero(self, f=None):
        
        fe_isnonzero.zero = None
        if fe_isnonzero.zero == None:
            fe_isnonzero.zero = php_str_repeat(" ", 32)
        # end if
        #// @var string $str
        str = self.fe_tobytes(f)
        #// @var string $zero
        return (not self.verify_32(str, fe_isnonzero.zero))
    # end def fe_isnonzero
    #// 
    #// Multiply two field elements
    #// 
    #// h = f * g
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @security Is multiplication a source of timing leaks? If so, can we do
    #// anything to prevent that from happening?
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $f
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $g
    #// @return ParagonIE_Sodium_Core32_Curve25519_Fe
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def fe_mul(self, f=None, g=None):
        
        #// 
        #// @var ParagonIE_Sodium_Core32_Int32[] $f
        #// @var ParagonIE_Sodium_Core32_Int32[] $g
        #// @var ParagonIE_Sodium_Core32_Int64 $f0
        #// @var ParagonIE_Sodium_Core32_Int64 $f1
        #// @var ParagonIE_Sodium_Core32_Int64 $f2
        #// @var ParagonIE_Sodium_Core32_Int64 $f3
        #// @var ParagonIE_Sodium_Core32_Int64 $f4
        #// @var ParagonIE_Sodium_Core32_Int64 $f5
        #// @var ParagonIE_Sodium_Core32_Int64 $f6
        #// @var ParagonIE_Sodium_Core32_Int64 $f7
        #// @var ParagonIE_Sodium_Core32_Int64 $f8
        #// @var ParagonIE_Sodium_Core32_Int64 $f9
        #// @var ParagonIE_Sodium_Core32_Int64 $g0
        #// @var ParagonIE_Sodium_Core32_Int64 $g1
        #// @var ParagonIE_Sodium_Core32_Int64 $g2
        #// @var ParagonIE_Sodium_Core32_Int64 $g3
        #// @var ParagonIE_Sodium_Core32_Int64 $g4
        #// @var ParagonIE_Sodium_Core32_Int64 $g5
        #// @var ParagonIE_Sodium_Core32_Int64 $g6
        #// @var ParagonIE_Sodium_Core32_Int64 $g7
        #// @var ParagonIE_Sodium_Core32_Int64 $g8
        #// @var ParagonIE_Sodium_Core32_Int64 $g9
        #//
        f0 = f[0].toint64()
        f1 = f[1].toint64()
        f2 = f[2].toint64()
        f3 = f[3].toint64()
        f4 = f[4].toint64()
        f5 = f[5].toint64()
        f6 = f[6].toint64()
        f7 = f[7].toint64()
        f8 = f[8].toint64()
        f9 = f[9].toint64()
        g0 = g[0].toint64()
        g1 = g[1].toint64()
        g2 = g[2].toint64()
        g3 = g[3].toint64()
        g4 = g[4].toint64()
        g5 = g[5].toint64()
        g6 = g[6].toint64()
        g7 = g[7].toint64()
        g8 = g[8].toint64()
        g9 = g[9].toint64()
        g1_19 = g1.mulint(19, 5)
        #// 2^4 <= 19 <= 2^5, but we only want 5 bits
        g2_19 = g2.mulint(19, 5)
        g3_19 = g3.mulint(19, 5)
        g4_19 = g4.mulint(19, 5)
        g5_19 = g5.mulint(19, 5)
        g6_19 = g6.mulint(19, 5)
        g7_19 = g7.mulint(19, 5)
        g8_19 = g8.mulint(19, 5)
        g9_19 = g9.mulint(19, 5)
        #// @var ParagonIE_Sodium_Core32_Int64 $f1_2
        f1_2 = f1.shiftleft(1)
        #// @var ParagonIE_Sodium_Core32_Int64 $f3_2
        f3_2 = f3.shiftleft(1)
        #// @var ParagonIE_Sodium_Core32_Int64 $f5_2
        f5_2 = f5.shiftleft(1)
        #// @var ParagonIE_Sodium_Core32_Int64 $f7_2
        f7_2 = f7.shiftleft(1)
        #// @var ParagonIE_Sodium_Core32_Int64 $f9_2
        f9_2 = f9.shiftleft(1)
        f0g0 = f0.mulint64(g0, 27)
        f0g1 = f0.mulint64(g1, 27)
        f0g2 = f0.mulint64(g2, 27)
        f0g3 = f0.mulint64(g3, 27)
        f0g4 = f0.mulint64(g4, 27)
        f0g5 = f0.mulint64(g5, 27)
        f0g6 = f0.mulint64(g6, 27)
        f0g7 = f0.mulint64(g7, 27)
        f0g8 = f0.mulint64(g8, 27)
        f0g9 = f0.mulint64(g9, 27)
        f1g0 = f1.mulint64(g0, 27)
        f1g1_2 = f1_2.mulint64(g1, 27)
        f1g2 = f1.mulint64(g2, 27)
        f1g3_2 = f1_2.mulint64(g3, 27)
        f1g4 = f1.mulint64(g4, 30)
        f1g5_2 = f1_2.mulint64(g5, 30)
        f1g6 = f1.mulint64(g6, 30)
        f1g7_2 = f1_2.mulint64(g7, 30)
        f1g8 = f1.mulint64(g8, 30)
        f1g9_38 = g9_19.mulint64(f1_2, 30)
        f2g0 = f2.mulint64(g0, 30)
        f2g1 = f2.mulint64(g1, 29)
        f2g2 = f2.mulint64(g2, 30)
        f2g3 = f2.mulint64(g3, 29)
        f2g4 = f2.mulint64(g4, 30)
        f2g5 = f2.mulint64(g5, 29)
        f2g6 = f2.mulint64(g6, 30)
        f2g7 = f2.mulint64(g7, 29)
        f2g8_19 = g8_19.mulint64(f2, 30)
        f2g9_19 = g9_19.mulint64(f2, 30)
        f3g0 = f3.mulint64(g0, 30)
        f3g1_2 = f3_2.mulint64(g1, 30)
        f3g2 = f3.mulint64(g2, 30)
        f3g3_2 = f3_2.mulint64(g3, 30)
        f3g4 = f3.mulint64(g4, 30)
        f3g5_2 = f3_2.mulint64(g5, 30)
        f3g6 = f3.mulint64(g6, 30)
        f3g7_38 = g7_19.mulint64(f3_2, 30)
        f3g8_19 = g8_19.mulint64(f3, 30)
        f3g9_38 = g9_19.mulint64(f3_2, 30)
        f4g0 = f4.mulint64(g0, 30)
        f4g1 = f4.mulint64(g1, 30)
        f4g2 = f4.mulint64(g2, 30)
        f4g3 = f4.mulint64(g3, 30)
        f4g4 = f4.mulint64(g4, 30)
        f4g5 = f4.mulint64(g5, 30)
        f4g6_19 = g6_19.mulint64(f4, 30)
        f4g7_19 = g7_19.mulint64(f4, 30)
        f4g8_19 = g8_19.mulint64(f4, 30)
        f4g9_19 = g9_19.mulint64(f4, 30)
        f5g0 = f5.mulint64(g0, 30)
        f5g1_2 = f5_2.mulint64(g1, 30)
        f5g2 = f5.mulint64(g2, 30)
        f5g3_2 = f5_2.mulint64(g3, 30)
        f5g4 = f5.mulint64(g4, 30)
        f5g5_38 = g5_19.mulint64(f5_2, 30)
        f5g6_19 = g6_19.mulint64(f5, 30)
        f5g7_38 = g7_19.mulint64(f5_2, 30)
        f5g8_19 = g8_19.mulint64(f5, 30)
        f5g9_38 = g9_19.mulint64(f5_2, 30)
        f6g0 = f6.mulint64(g0, 30)
        f6g1 = f6.mulint64(g1, 30)
        f6g2 = f6.mulint64(g2, 30)
        f6g3 = f6.mulint64(g3, 30)
        f6g4_19 = g4_19.mulint64(f6, 30)
        f6g5_19 = g5_19.mulint64(f6, 30)
        f6g6_19 = g6_19.mulint64(f6, 30)
        f6g7_19 = g7_19.mulint64(f6, 30)
        f6g8_19 = g8_19.mulint64(f6, 30)
        f6g9_19 = g9_19.mulint64(f6, 30)
        f7g0 = f7.mulint64(g0, 30)
        f7g1_2 = g1.mulint64(f7_2, 30)
        f7g2 = f7.mulint64(g2, 30)
        f7g3_38 = g3_19.mulint64(f7_2, 30)
        f7g4_19 = g4_19.mulint64(f7, 30)
        f7g5_38 = g5_19.mulint64(f7_2, 30)
        f7g6_19 = g6_19.mulint64(f7, 30)
        f7g7_38 = g7_19.mulint64(f7_2, 30)
        f7g8_19 = g8_19.mulint64(f7, 30)
        f7g9_38 = g9_19.mulint64(f7_2, 30)
        f8g0 = f8.mulint64(g0, 30)
        f8g1 = f8.mulint64(g1, 29)
        f8g2_19 = g2_19.mulint64(f8, 30)
        f8g3_19 = g3_19.mulint64(f8, 30)
        f8g4_19 = g4_19.mulint64(f8, 30)
        f8g5_19 = g5_19.mulint64(f8, 30)
        f8g6_19 = g6_19.mulint64(f8, 30)
        f8g7_19 = g7_19.mulint64(f8, 30)
        f8g8_19 = g8_19.mulint64(f8, 30)
        f8g9_19 = g9_19.mulint64(f8, 30)
        f9g0 = f9.mulint64(g0, 30)
        f9g1_38 = g1_19.mulint64(f9_2, 30)
        f9g2_19 = g2_19.mulint64(f9, 30)
        f9g3_38 = g3_19.mulint64(f9_2, 30)
        f9g4_19 = g4_19.mulint64(f9, 30)
        f9g5_38 = g5_19.mulint64(f9_2, 30)
        f9g6_19 = g6_19.mulint64(f9, 30)
        f9g7_38 = g7_19.mulint64(f9_2, 30)
        f9g8_19 = g8_19.mulint64(f9, 30)
        f9g9_38 = g9_19.mulint64(f9_2, 30)
        #// $h0 = $f0g0 + $f1g9_38 + $f2g8_19 + $f3g7_38 + $f4g6_19 + $f5g5_38 + $f6g4_19 + $f7g3_38 + $f8g2_19 + $f9g1_38;
        h0 = f0g0.addint64(f1g9_38).addint64(f2g8_19).addint64(f3g7_38).addint64(f4g6_19).addint64(f5g5_38).addint64(f6g4_19).addint64(f7g3_38).addint64(f8g2_19).addint64(f9g1_38)
        #// $h1 = $f0g1 + $f1g0    + $f2g9_19 + $f3g8_19 + $f4g7_19 + $f5g6_19 + $f6g5_19 + $f7g4_19 + $f8g3_19 + $f9g2_19;
        h1 = f0g1.addint64(f1g0).addint64(f2g9_19).addint64(f3g8_19).addint64(f4g7_19).addint64(f5g6_19).addint64(f6g5_19).addint64(f7g4_19).addint64(f8g3_19).addint64(f9g2_19)
        #// $h2 = $f0g2 + $f1g1_2  + $f2g0    + $f3g9_38 + $f4g8_19 + $f5g7_38 + $f6g6_19 + $f7g5_38 + $f8g4_19 + $f9g3_38;
        h2 = f0g2.addint64(f1g1_2).addint64(f2g0).addint64(f3g9_38).addint64(f4g8_19).addint64(f5g7_38).addint64(f6g6_19).addint64(f7g5_38).addint64(f8g4_19).addint64(f9g3_38)
        #// $h3 = $f0g3 + $f1g2    + $f2g1    + $f3g0    + $f4g9_19 + $f5g8_19 + $f6g7_19 + $f7g6_19 + $f8g5_19 + $f9g4_19;
        h3 = f0g3.addint64(f1g2).addint64(f2g1).addint64(f3g0).addint64(f4g9_19).addint64(f5g8_19).addint64(f6g7_19).addint64(f7g6_19).addint64(f8g5_19).addint64(f9g4_19)
        #// $h4 = $f0g4 + $f1g3_2  + $f2g2    + $f3g1_2  + $f4g0    + $f5g9_38 + $f6g8_19 + $f7g7_38 + $f8g6_19 + $f9g5_38;
        h4 = f0g4.addint64(f1g3_2).addint64(f2g2).addint64(f3g1_2).addint64(f4g0).addint64(f5g9_38).addint64(f6g8_19).addint64(f7g7_38).addint64(f8g6_19).addint64(f9g5_38)
        #// $h5 = $f0g5 + $f1g4    + $f2g3    + $f3g2    + $f4g1    + $f5g0    + $f6g9_19 + $f7g8_19 + $f8g7_19 + $f9g6_19;
        h5 = f0g5.addint64(f1g4).addint64(f2g3).addint64(f3g2).addint64(f4g1).addint64(f5g0).addint64(f6g9_19).addint64(f7g8_19).addint64(f8g7_19).addint64(f9g6_19)
        #// $h6 = $f0g6 + $f1g5_2  + $f2g4    + $f3g3_2  + $f4g2    + $f5g1_2  + $f6g0    + $f7g9_38 + $f8g8_19 + $f9g7_38;
        h6 = f0g6.addint64(f1g5_2).addint64(f2g4).addint64(f3g3_2).addint64(f4g2).addint64(f5g1_2).addint64(f6g0).addint64(f7g9_38).addint64(f8g8_19).addint64(f9g7_38)
        #// $h7 = $f0g7 + $f1g6    + $f2g5    + $f3g4    + $f4g3    + $f5g2    + $f6g1    + $f7g0    + $f8g9_19 + $f9g8_19;
        h7 = f0g7.addint64(f1g6).addint64(f2g5).addint64(f3g4).addint64(f4g3).addint64(f5g2).addint64(f6g1).addint64(f7g0).addint64(f8g9_19).addint64(f9g8_19)
        #// $h8 = $f0g8 + $f1g7_2  + $f2g6    + $f3g5_2  + $f4g4    + $f5g3_2  + $f6g2    + $f7g1_2  + $f8g0    + $f9g9_38;
        h8 = f0g8.addint64(f1g7_2).addint64(f2g6).addint64(f3g5_2).addint64(f4g4).addint64(f5g3_2).addint64(f6g2).addint64(f7g1_2).addint64(f8g0).addint64(f9g9_38)
        #// $h9 = $f0g9 + $f1g8    + $f2g7    + $f3g6    + $f4g5    + $f5g4    + $f6g3    + $f7g2    + $f8g1    + $f9g0   ;
        h9 = f0g9.addint64(f1g8).addint64(f2g7).addint64(f3g6).addint64(f4g5).addint64(f5g4).addint64(f6g3).addint64(f7g2).addint64(f8g1).addint64(f9g0)
        #// 
        #// @var ParagonIE_Sodium_Core32_Int64 $h0
        #// @var ParagonIE_Sodium_Core32_Int64 $h1
        #// @var ParagonIE_Sodium_Core32_Int64 $h2
        #// @var ParagonIE_Sodium_Core32_Int64 $h3
        #// @var ParagonIE_Sodium_Core32_Int64 $h4
        #// @var ParagonIE_Sodium_Core32_Int64 $h5
        #// @var ParagonIE_Sodium_Core32_Int64 $h6
        #// @var ParagonIE_Sodium_Core32_Int64 $h7
        #// @var ParagonIE_Sodium_Core32_Int64 $h8
        #// @var ParagonIE_Sodium_Core32_Int64 $h9
        #// @var ParagonIE_Sodium_Core32_Int64 $carry0
        #// @var ParagonIE_Sodium_Core32_Int64 $carry1
        #// @var ParagonIE_Sodium_Core32_Int64 $carry2
        #// @var ParagonIE_Sodium_Core32_Int64 $carry3
        #// @var ParagonIE_Sodium_Core32_Int64 $carry4
        #// @var ParagonIE_Sodium_Core32_Int64 $carry5
        #// @var ParagonIE_Sodium_Core32_Int64 $carry6
        #// @var ParagonIE_Sodium_Core32_Int64 $carry7
        #// @var ParagonIE_Sodium_Core32_Int64 $carry8
        #// @var ParagonIE_Sodium_Core32_Int64 $carry9
        #//
        carry0 = h0.addint(1 << 25).shiftright(26)
        h1 = h1.addint64(carry0)
        h0 = h0.subint64(carry0.shiftleft(26))
        carry4 = h4.addint(1 << 25).shiftright(26)
        h5 = h5.addint64(carry4)
        h4 = h4.subint64(carry4.shiftleft(26))
        carry1 = h1.addint(1 << 24).shiftright(25)
        h2 = h2.addint64(carry1)
        h1 = h1.subint64(carry1.shiftleft(25))
        carry5 = h5.addint(1 << 24).shiftright(25)
        h6 = h6.addint64(carry5)
        h5 = h5.subint64(carry5.shiftleft(25))
        carry2 = h2.addint(1 << 25).shiftright(26)
        h3 = h3.addint64(carry2)
        h2 = h2.subint64(carry2.shiftleft(26))
        carry6 = h6.addint(1 << 25).shiftright(26)
        h7 = h7.addint64(carry6)
        h6 = h6.subint64(carry6.shiftleft(26))
        carry3 = h3.addint(1 << 24).shiftright(25)
        h4 = h4.addint64(carry3)
        h3 = h3.subint64(carry3.shiftleft(25))
        carry7 = h7.addint(1 << 24).shiftright(25)
        h8 = h8.addint64(carry7)
        h7 = h7.subint64(carry7.shiftleft(25))
        carry4 = h4.addint(1 << 25).shiftright(26)
        h5 = h5.addint64(carry4)
        h4 = h4.subint64(carry4.shiftleft(26))
        carry8 = h8.addint(1 << 25).shiftright(26)
        h9 = h9.addint64(carry8)
        h8 = h8.subint64(carry8.shiftleft(26))
        carry9 = h9.addint(1 << 24).shiftright(25)
        h0 = h0.addint64(carry9.mulint(19, 5))
        h9 = h9.subint64(carry9.shiftleft(25))
        carry0 = h0.addint(1 << 25).shiftright(26)
        h1 = h1.addint64(carry0)
        h0 = h0.subint64(carry0.shiftleft(26))
        return ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(Array(h0.toint32(), h1.toint32(), h2.toint32(), h3.toint32(), h4.toint32(), h5.toint32(), h6.toint32(), h7.toint32(), h8.toint32(), h9.toint32()))
    # end def fe_mul
    #// 
    #// Get the negative values for each piece of the field element.
    #// 
    #// h = -f
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $f
    #// @return ParagonIE_Sodium_Core32_Curve25519_Fe
    #// @psalm-suppress MixedAssignment
    #// @psalm-suppress MixedMethodCall
    #//
    @classmethod
    def fe_neg(self, f=None):
        
        h = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Fe", lambda : ParagonIE_Sodium_Core32_Curve25519_Fe())
        i = 0
        while i < 10:
            
            h[i] = h[i].subint32(f[i])
            i += 1
        # end while
        return h
    # end def fe_neg
    #// 
    #// Square a field element
    #// 
    #// h = f * f
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $f
    #// @return ParagonIE_Sodium_Core32_Curve25519_Fe
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedMethodCall
    #//
    @classmethod
    def fe_sq(self, f=None):
        
        #// @var ParagonIE_Sodium_Core32_Int64 $f0
        f0 = f[0].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f1
        f1 = f[1].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f2
        f2 = f[2].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f3
        f3 = f[3].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f4
        f4 = f[4].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f5
        f5 = f[5].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f6
        f6 = f[6].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f7
        f7 = f[7].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f8
        f8 = f[8].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f9
        f9 = f[9].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f0_2
        f0_2 = f0.shiftleft(1)
        f1_2 = f1.shiftleft(1)
        f2_2 = f2.shiftleft(1)
        f3_2 = f3.shiftleft(1)
        f4_2 = f4.shiftleft(1)
        f5_2 = f5.shiftleft(1)
        f6_2 = f6.shiftleft(1)
        f7_2 = f7.shiftleft(1)
        f5_38 = f5.mulint(38, 6)
        f6_19 = f6.mulint(19, 5)
        f7_38 = f7.mulint(38, 6)
        f8_19 = f8.mulint(19, 5)
        f9_38 = f9.mulint(38, 6)
        #// @var ParagonIE_Sodium_Core32_Int64 $f0f0
        f0f0 = f0.mulint64(f0, 28)
        f0f1_2 = f0_2.mulint64(f1, 28)
        f0f2_2 = f0_2.mulint64(f2, 28)
        f0f3_2 = f0_2.mulint64(f3, 28)
        f0f4_2 = f0_2.mulint64(f4, 28)
        f0f5_2 = f0_2.mulint64(f5, 28)
        f0f6_2 = f0_2.mulint64(f6, 28)
        f0f7_2 = f0_2.mulint64(f7, 28)
        f0f8_2 = f0_2.mulint64(f8, 28)
        f0f9_2 = f0_2.mulint64(f9, 28)
        f1f1_2 = f1_2.mulint64(f1, 28)
        f1f2_2 = f1_2.mulint64(f2, 28)
        f1f3_4 = f1_2.mulint64(f3_2, 28)
        f1f4_2 = f1_2.mulint64(f4, 28)
        f1f5_4 = f1_2.mulint64(f5_2, 30)
        f1f6_2 = f1_2.mulint64(f6, 28)
        f1f7_4 = f1_2.mulint64(f7_2, 28)
        f1f8_2 = f1_2.mulint64(f8, 28)
        f1f9_76 = f9_38.mulint64(f1_2, 30)
        f2f2 = f2.mulint64(f2, 28)
        f2f3_2 = f2_2.mulint64(f3, 28)
        f2f4_2 = f2_2.mulint64(f4, 28)
        f2f5_2 = f2_2.mulint64(f5, 28)
        f2f6_2 = f2_2.mulint64(f6, 28)
        f2f7_2 = f2_2.mulint64(f7, 28)
        f2f8_38 = f8_19.mulint64(f2_2, 30)
        f2f9_38 = f9_38.mulint64(f2, 30)
        f3f3_2 = f3_2.mulint64(f3, 28)
        f3f4_2 = f3_2.mulint64(f4, 28)
        f3f5_4 = f3_2.mulint64(f5_2, 30)
        f3f6_2 = f3_2.mulint64(f6, 28)
        f3f7_76 = f7_38.mulint64(f3_2, 30)
        f3f8_38 = f8_19.mulint64(f3_2, 30)
        f3f9_76 = f9_38.mulint64(f3_2, 30)
        f4f4 = f4.mulint64(f4, 28)
        f4f5_2 = f4_2.mulint64(f5, 28)
        f4f6_38 = f6_19.mulint64(f4_2, 30)
        f4f7_38 = f7_38.mulint64(f4, 30)
        f4f8_38 = f8_19.mulint64(f4_2, 30)
        f4f9_38 = f9_38.mulint64(f4, 30)
        f5f5_38 = f5_38.mulint64(f5, 30)
        f5f6_38 = f6_19.mulint64(f5_2, 30)
        f5f7_76 = f7_38.mulint64(f5_2, 30)
        f5f8_38 = f8_19.mulint64(f5_2, 30)
        f5f9_76 = f9_38.mulint64(f5_2, 30)
        f6f6_19 = f6_19.mulint64(f6, 30)
        f6f7_38 = f7_38.mulint64(f6, 30)
        f6f8_38 = f8_19.mulint64(f6_2, 30)
        f6f9_38 = f9_38.mulint64(f6, 30)
        f7f7_38 = f7_38.mulint64(f7, 28)
        f7f8_38 = f8_19.mulint64(f7_2, 30)
        f7f9_76 = f9_38.mulint64(f7_2, 30)
        f8f8_19 = f8_19.mulint64(f8, 30)
        f8f9_38 = f9_38.mulint64(f8, 30)
        f9f9_38 = f9_38.mulint64(f9, 28)
        h0 = f0f0.addint64(f1f9_76).addint64(f2f8_38).addint64(f3f7_76).addint64(f4f6_38).addint64(f5f5_38)
        h1 = f0f1_2.addint64(f2f9_38).addint64(f3f8_38).addint64(f4f7_38).addint64(f5f6_38)
        h2 = f0f2_2.addint64(f1f1_2).addint64(f3f9_76).addint64(f4f8_38).addint64(f5f7_76).addint64(f6f6_19)
        h3 = f0f3_2.addint64(f1f2_2).addint64(f4f9_38).addint64(f5f8_38).addint64(f6f7_38)
        h4 = f0f4_2.addint64(f1f3_4).addint64(f2f2).addint64(f5f9_76).addint64(f6f8_38).addint64(f7f7_38)
        h5 = f0f5_2.addint64(f1f4_2).addint64(f2f3_2).addint64(f6f9_38).addint64(f7f8_38)
        h6 = f0f6_2.addint64(f1f5_4).addint64(f2f4_2).addint64(f3f3_2).addint64(f7f9_76).addint64(f8f8_19)
        h7 = f0f7_2.addint64(f1f6_2).addint64(f2f5_2).addint64(f3f4_2).addint64(f8f9_38)
        h8 = f0f8_2.addint64(f1f7_4).addint64(f2f6_2).addint64(f3f5_4).addint64(f4f4).addint64(f9f9_38)
        h9 = f0f9_2.addint64(f1f8_2).addint64(f2f7_2).addint64(f3f6_2).addint64(f4f5_2)
        #// 
        #// @var ParagonIE_Sodium_Core32_Int64 $h0
        #// @var ParagonIE_Sodium_Core32_Int64 $h1
        #// @var ParagonIE_Sodium_Core32_Int64 $h2
        #// @var ParagonIE_Sodium_Core32_Int64 $h3
        #// @var ParagonIE_Sodium_Core32_Int64 $h4
        #// @var ParagonIE_Sodium_Core32_Int64 $h5
        #// @var ParagonIE_Sodium_Core32_Int64 $h6
        #// @var ParagonIE_Sodium_Core32_Int64 $h7
        #// @var ParagonIE_Sodium_Core32_Int64 $h8
        #// @var ParagonIE_Sodium_Core32_Int64 $h9
        #//
        carry0 = h0.addint(1 << 25).shiftright(26)
        h1 = h1.addint64(carry0)
        h0 = h0.subint64(carry0.shiftleft(26))
        carry4 = h4.addint(1 << 25).shiftright(26)
        h5 = h5.addint64(carry4)
        h4 = h4.subint64(carry4.shiftleft(26))
        carry1 = h1.addint(1 << 24).shiftright(25)
        h2 = h2.addint64(carry1)
        h1 = h1.subint64(carry1.shiftleft(25))
        carry5 = h5.addint(1 << 24).shiftright(25)
        h6 = h6.addint64(carry5)
        h5 = h5.subint64(carry5.shiftleft(25))
        carry2 = h2.addint(1 << 25).shiftright(26)
        h3 = h3.addint64(carry2)
        h2 = h2.subint64(carry2.shiftleft(26))
        carry6 = h6.addint(1 << 25).shiftright(26)
        h7 = h7.addint64(carry6)
        h6 = h6.subint64(carry6.shiftleft(26))
        carry3 = h3.addint(1 << 24).shiftright(25)
        h4 = h4.addint64(carry3)
        h3 = h3.subint64(carry3.shiftleft(25))
        carry7 = h7.addint(1 << 24).shiftright(25)
        h8 = h8.addint64(carry7)
        h7 = h7.subint64(carry7.shiftleft(25))
        carry4 = h4.addint(1 << 25).shiftright(26)
        h5 = h5.addint64(carry4)
        h4 = h4.subint64(carry4.shiftleft(26))
        carry8 = h8.addint(1 << 25).shiftright(26)
        h9 = h9.addint64(carry8)
        h8 = h8.subint64(carry8.shiftleft(26))
        carry9 = h9.addint(1 << 24).shiftright(25)
        h0 = h0.addint64(carry9.mulint(19, 5))
        h9 = h9.subint64(carry9.shiftleft(25))
        carry0 = h0.addint(1 << 25).shiftright(26)
        h1 = h1.addint64(carry0)
        h0 = h0.subint64(carry0.shiftleft(26))
        return ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(Array(h0.toint32(), h1.toint32(), h2.toint32(), h3.toint32(), h4.toint32(), h5.toint32(), h6.toint32(), h7.toint32(), h8.toint32(), h9.toint32()))
    # end def fe_sq
    #// 
    #// Square and double a field element
    #// 
    #// h = 2 * f * f
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $f
    #// @return ParagonIE_Sodium_Core32_Curve25519_Fe
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedMethodCall
    #//
    @classmethod
    def fe_sq2(self, f=None):
        
        #// @var ParagonIE_Sodium_Core32_Int64 $f0
        f0 = f[0].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f1
        f1 = f[1].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f2
        f2 = f[2].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f3
        f3 = f[3].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f4
        f4 = f[4].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f5
        f5 = f[5].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f6
        f6 = f[6].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f7
        f7 = f[7].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f8
        f8 = f[8].toint64()
        #// @var ParagonIE_Sodium_Core32_Int64 $f9
        f9 = f[9].toint64()
        f0_2 = f0.shiftleft(1)
        f1_2 = f1.shiftleft(1)
        f2_2 = f2.shiftleft(1)
        f3_2 = f3.shiftleft(1)
        f4_2 = f4.shiftleft(1)
        f5_2 = f5.shiftleft(1)
        f6_2 = f6.shiftleft(1)
        f7_2 = f7.shiftleft(1)
        f5_38 = f5.mulint(38, 6)
        #// 1.959375*2^30
        f6_19 = f6.mulint(19, 5)
        #// 1.959375*2^30
        f7_38 = f7.mulint(38, 6)
        #// 1.959375*2^30
        f8_19 = f8.mulint(19, 5)
        #// 1.959375*2^30
        f9_38 = f9.mulint(38, 6)
        #// 1.959375*2^30
        f0f0 = f0.mulint64(f0, 28)
        f0f1_2 = f0_2.mulint64(f1, 28)
        f0f2_2 = f0_2.mulint64(f2, 28)
        f0f3_2 = f0_2.mulint64(f3, 28)
        f0f4_2 = f0_2.mulint64(f4, 28)
        f0f5_2 = f0_2.mulint64(f5, 28)
        f0f6_2 = f0_2.mulint64(f6, 28)
        f0f7_2 = f0_2.mulint64(f7, 28)
        f0f8_2 = f0_2.mulint64(f8, 28)
        f0f9_2 = f0_2.mulint64(f9, 28)
        f1f1_2 = f1_2.mulint64(f1, 28)
        f1f2_2 = f1_2.mulint64(f2, 28)
        f1f3_4 = f1_2.mulint64(f3_2, 29)
        f1f4_2 = f1_2.mulint64(f4, 28)
        f1f5_4 = f1_2.mulint64(f5_2, 29)
        f1f6_2 = f1_2.mulint64(f6, 28)
        f1f7_4 = f1_2.mulint64(f7_2, 29)
        f1f8_2 = f1_2.mulint64(f8, 28)
        f1f9_76 = f9_38.mulint64(f1_2, 29)
        f2f2 = f2.mulint64(f2, 28)
        f2f3_2 = f2_2.mulint64(f3, 28)
        f2f4_2 = f2_2.mulint64(f4, 28)
        f2f5_2 = f2_2.mulint64(f5, 28)
        f2f6_2 = f2_2.mulint64(f6, 28)
        f2f7_2 = f2_2.mulint64(f7, 28)
        f2f8_38 = f8_19.mulint64(f2_2, 29)
        f2f9_38 = f9_38.mulint64(f2, 29)
        f3f3_2 = f3_2.mulint64(f3, 28)
        f3f4_2 = f3_2.mulint64(f4, 28)
        f3f5_4 = f3_2.mulint64(f5_2, 28)
        f3f6_2 = f3_2.mulint64(f6, 28)
        f3f7_76 = f7_38.mulint64(f3_2, 29)
        f3f8_38 = f8_19.mulint64(f3_2, 29)
        f3f9_76 = f9_38.mulint64(f3_2, 29)
        f4f4 = f4.mulint64(f4, 28)
        f4f5_2 = f4_2.mulint64(f5, 28)
        f4f6_38 = f6_19.mulint64(f4_2, 29)
        f4f7_38 = f7_38.mulint64(f4, 29)
        f4f8_38 = f8_19.mulint64(f4_2, 29)
        f4f9_38 = f9_38.mulint64(f4, 29)
        f5f5_38 = f5_38.mulint64(f5, 29)
        f5f6_38 = f6_19.mulint64(f5_2, 29)
        f5f7_76 = f7_38.mulint64(f5_2, 29)
        f5f8_38 = f8_19.mulint64(f5_2, 29)
        f5f9_76 = f9_38.mulint64(f5_2, 29)
        f6f6_19 = f6_19.mulint64(f6, 29)
        f6f7_38 = f7_38.mulint64(f6, 29)
        f6f8_38 = f8_19.mulint64(f6_2, 29)
        f6f9_38 = f9_38.mulint64(f6, 29)
        f7f7_38 = f7_38.mulint64(f7, 29)
        f7f8_38 = f8_19.mulint64(f7_2, 29)
        f7f9_76 = f9_38.mulint64(f7_2, 29)
        f8f8_19 = f8_19.mulint64(f8, 29)
        f8f9_38 = f9_38.mulint64(f8, 29)
        f9f9_38 = f9_38.mulint64(f9, 29)
        h0 = f0f0.addint64(f1f9_76).addint64(f2f8_38).addint64(f3f7_76).addint64(f4f6_38).addint64(f5f5_38)
        h1 = f0f1_2.addint64(f2f9_38).addint64(f3f8_38).addint64(f4f7_38).addint64(f5f6_38)
        h2 = f0f2_2.addint64(f1f1_2).addint64(f3f9_76).addint64(f4f8_38).addint64(f5f7_76).addint64(f6f6_19)
        h3 = f0f3_2.addint64(f1f2_2).addint64(f4f9_38).addint64(f5f8_38).addint64(f6f7_38)
        h4 = f0f4_2.addint64(f1f3_4).addint64(f2f2).addint64(f5f9_76).addint64(f6f8_38).addint64(f7f7_38)
        h5 = f0f5_2.addint64(f1f4_2).addint64(f2f3_2).addint64(f6f9_38).addint64(f7f8_38)
        h6 = f0f6_2.addint64(f1f5_4).addint64(f2f4_2).addint64(f3f3_2).addint64(f7f9_76).addint64(f8f8_19)
        h7 = f0f7_2.addint64(f1f6_2).addint64(f2f5_2).addint64(f3f4_2).addint64(f8f9_38)
        h8 = f0f8_2.addint64(f1f7_4).addint64(f2f6_2).addint64(f3f5_4).addint64(f4f4).addint64(f9f9_38)
        h9 = f0f9_2.addint64(f1f8_2).addint64(f2f7_2).addint64(f3f6_2).addint64(f4f5_2)
        #// 
        #// @var ParagonIE_Sodium_Core32_Int64 $h0
        #// @var ParagonIE_Sodium_Core32_Int64 $h1
        #// @var ParagonIE_Sodium_Core32_Int64 $h2
        #// @var ParagonIE_Sodium_Core32_Int64 $h3
        #// @var ParagonIE_Sodium_Core32_Int64 $h4
        #// @var ParagonIE_Sodium_Core32_Int64 $h5
        #// @var ParagonIE_Sodium_Core32_Int64 $h6
        #// @var ParagonIE_Sodium_Core32_Int64 $h7
        #// @var ParagonIE_Sodium_Core32_Int64 $h8
        #// @var ParagonIE_Sodium_Core32_Int64 $h9
        #//
        h0 = h0.shiftleft(1)
        h1 = h1.shiftleft(1)
        h2 = h2.shiftleft(1)
        h3 = h3.shiftleft(1)
        h4 = h4.shiftleft(1)
        h5 = h5.shiftleft(1)
        h6 = h6.shiftleft(1)
        h7 = h7.shiftleft(1)
        h8 = h8.shiftleft(1)
        h9 = h9.shiftleft(1)
        carry0 = h0.addint(1 << 25).shiftright(26)
        h1 = h1.addint64(carry0)
        h0 = h0.subint64(carry0.shiftleft(26))
        carry4 = h4.addint(1 << 25).shiftright(26)
        h5 = h5.addint64(carry4)
        h4 = h4.subint64(carry4.shiftleft(26))
        carry1 = h1.addint(1 << 24).shiftright(25)
        h2 = h2.addint64(carry1)
        h1 = h1.subint64(carry1.shiftleft(25))
        carry5 = h5.addint(1 << 24).shiftright(25)
        h6 = h6.addint64(carry5)
        h5 = h5.subint64(carry5.shiftleft(25))
        carry2 = h2.addint(1 << 25).shiftright(26)
        h3 = h3.addint64(carry2)
        h2 = h2.subint64(carry2.shiftleft(26))
        carry6 = h6.addint(1 << 25).shiftright(26)
        h7 = h7.addint64(carry6)
        h6 = h6.subint64(carry6.shiftleft(26))
        carry3 = h3.addint(1 << 24).shiftright(25)
        h4 = h4.addint64(carry3)
        h3 = h3.subint64(carry3.shiftleft(25))
        carry7 = h7.addint(1 << 24).shiftright(25)
        h8 = h8.addint64(carry7)
        h7 = h7.subint64(carry7.shiftleft(25))
        carry4 = h4.addint(1 << 25).shiftright(26)
        h5 = h5.addint64(carry4)
        h4 = h4.subint64(carry4.shiftleft(26))
        carry8 = h8.addint(1 << 25).shiftright(26)
        h9 = h9.addint64(carry8)
        h8 = h8.subint64(carry8.shiftleft(26))
        carry9 = h9.addint(1 << 24).shiftright(25)
        h0 = h0.addint64(carry9.mulint(19, 5))
        h9 = h9.subint64(carry9.shiftleft(25))
        carry0 = h0.addint(1 << 25).shiftright(26)
        h1 = h1.addint64(carry0)
        h0 = h0.subint64(carry0.shiftleft(26))
        return ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(Array(h0.toint32(), h1.toint32(), h2.toint32(), h3.toint32(), h4.toint32(), h5.toint32(), h6.toint32(), h7.toint32(), h8.toint32(), h9.toint32()))
    # end def fe_sq2
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $Z
    #// @return ParagonIE_Sodium_Core32_Curve25519_Fe
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def fe_invert(self, Z=None):
        
        z = copy.deepcopy(Z)
        t0 = self.fe_sq(z)
        t1 = self.fe_sq(t0)
        t1 = self.fe_sq(t1)
        t1 = self.fe_mul(z, t1)
        t0 = self.fe_mul(t0, t1)
        t2 = self.fe_sq(t0)
        t1 = self.fe_mul(t1, t2)
        t2 = self.fe_sq(t1)
        i = 1
        while i < 5:
            
            t2 = self.fe_sq(t2)
            i += 1
        # end while
        t1 = self.fe_mul(t2, t1)
        t2 = self.fe_sq(t1)
        i = 1
        while i < 10:
            
            t2 = self.fe_sq(t2)
            i += 1
        # end while
        t2 = self.fe_mul(t2, t1)
        t3 = self.fe_sq(t2)
        i = 1
        while i < 20:
            
            t3 = self.fe_sq(t3)
            i += 1
        # end while
        t2 = self.fe_mul(t3, t2)
        t2 = self.fe_sq(t2)
        i = 1
        while i < 10:
            
            t2 = self.fe_sq(t2)
            i += 1
        # end while
        t1 = self.fe_mul(t2, t1)
        t2 = self.fe_sq(t1)
        i = 1
        while i < 50:
            
            t2 = self.fe_sq(t2)
            i += 1
        # end while
        t2 = self.fe_mul(t2, t1)
        t3 = self.fe_sq(t2)
        i = 1
        while i < 100:
            
            t3 = self.fe_sq(t3)
            i += 1
        # end while
        t2 = self.fe_mul(t3, t2)
        t2 = self.fe_sq(t2)
        i = 1
        while i < 50:
            
            t2 = self.fe_sq(t2)
            i += 1
        # end while
        t1 = self.fe_mul(t2, t1)
        t1 = self.fe_sq(t1)
        i = 1
        while i < 5:
            
            t1 = self.fe_sq(t1)
            i += 1
        # end while
        return self.fe_mul(t1, t0)
    # end def fe_invert
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @ref https://github.com/jedisct1/libsodium/blob/68564326e1e9dc57ef03746f85734232d20ca6fb/src/libsodium/crypto_core/curve25519/ref10/curve25519_ref10.c#L1054-L1106
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $z
    #// @return ParagonIE_Sodium_Core32_Curve25519_Fe
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def fe_pow22523(self, z=None):
        
        #// # fe_sq(t0, z);
        #// # fe_sq(t1, t0);
        #// # fe_sq(t1, t1);
        #// # fe_mul(t1, z, t1);
        #// # fe_mul(t0, t0, t1);
        #// # fe_sq(t0, t0);
        #// # fe_mul(t0, t1, t0);
        #// # fe_sq(t1, t0);
        t0 = self.fe_sq(z)
        t1 = self.fe_sq(t0)
        t1 = self.fe_sq(t1)
        t1 = self.fe_mul(z, t1)
        t0 = self.fe_mul(t0, t1)
        t0 = self.fe_sq(t0)
        t0 = self.fe_mul(t1, t0)
        t1 = self.fe_sq(t0)
        #// # for (i = 1; i < 5; ++i) {
        #// #     fe_sq(t1, t1);
        #// # }
        i = 1
        while i < 5:
            
            t1 = self.fe_sq(t1)
            i += 1
        # end while
        #// # fe_mul(t0, t1, t0);
        #// # fe_sq(t1, t0);
        t0 = self.fe_mul(t1, t0)
        t1 = self.fe_sq(t0)
        #// # for (i = 1; i < 10; ++i) {
        #// #     fe_sq(t1, t1);
        #// # }
        i = 1
        while i < 10:
            
            t1 = self.fe_sq(t1)
            i += 1
        # end while
        #// # fe_mul(t1, t1, t0);
        #// # fe_sq(t2, t1);
        t1 = self.fe_mul(t1, t0)
        t2 = self.fe_sq(t1)
        #// # for (i = 1; i < 20; ++i) {
        #// #     fe_sq(t2, t2);
        #// # }
        i = 1
        while i < 20:
            
            t2 = self.fe_sq(t2)
            i += 1
        # end while
        #// # fe_mul(t1, t2, t1);
        #// # fe_sq(t1, t1);
        t1 = self.fe_mul(t2, t1)
        t1 = self.fe_sq(t1)
        #// # for (i = 1; i < 10; ++i) {
        #// #     fe_sq(t1, t1);
        #// # }
        i = 1
        while i < 10:
            
            t1 = self.fe_sq(t1)
            i += 1
        # end while
        #// # fe_mul(t0, t1, t0);
        #// # fe_sq(t1, t0);
        t0 = self.fe_mul(t1, t0)
        t1 = self.fe_sq(t0)
        #// # for (i = 1; i < 50; ++i) {
        #// #     fe_sq(t1, t1);
        #// # }
        i = 1
        while i < 50:
            
            t1 = self.fe_sq(t1)
            i += 1
        # end while
        #// # fe_mul(t1, t1, t0);
        #// # fe_sq(t2, t1);
        t1 = self.fe_mul(t1, t0)
        t2 = self.fe_sq(t1)
        #// # for (i = 1; i < 100; ++i) {
        #// #     fe_sq(t2, t2);
        #// # }
        i = 1
        while i < 100:
            
            t2 = self.fe_sq(t2)
            i += 1
        # end while
        #// # fe_mul(t1, t2, t1);
        #// # fe_sq(t1, t1);
        t1 = self.fe_mul(t2, t1)
        t1 = self.fe_sq(t1)
        #// # for (i = 1; i < 50; ++i) {
        #// #     fe_sq(t1, t1);
        #// # }
        i = 1
        while i < 50:
            
            t1 = self.fe_sq(t1)
            i += 1
        # end while
        #// # fe_mul(t0, t1, t0);
        #// # fe_sq(t0, t0);
        #// # fe_sq(t0, t0);
        #// # fe_mul(out, t0, z);
        t0 = self.fe_mul(t1, t0)
        t0 = self.fe_sq(t0)
        t0 = self.fe_sq(t0)
        return self.fe_mul(t0, z)
    # end def fe_pow22523
    #// 
    #// Subtract two field elements.
    #// 
    #// h = f - g
    #// 
    #// Preconditions:
    #// |f| bounded by 1.1*2^25,1.1*2^24,1.1*2^25,1.1*2^24,etc.
    #// |g| bounded by 1.1*2^25,1.1*2^24,1.1*2^25,1.1*2^24,etc.
    #// 
    #// Postconditions:
    #// |h| bounded by 1.1*2^26,1.1*2^25,1.1*2^26,1.1*2^25,etc.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $f
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $g
    #// @return ParagonIE_Sodium_Core32_Curve25519_Fe
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedMethodCall
    #// @psalm-suppress MixedTypeCoercion
    #//
    @classmethod
    def fe_sub(self, f=None, g=None):
        
        return ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(Array(f[0].subint32(g[0]), f[1].subint32(g[1]), f[2].subint32(g[2]), f[3].subint32(g[3]), f[4].subint32(g[4]), f[5].subint32(g[5]), f[6].subint32(g[6]), f[7].subint32(g[7]), f[8].subint32(g[8]), f[9].subint32(g[9])))
    # end def fe_sub
    #// 
    #// Add two group elements.
    #// 
    #// r = p + q
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_P3 $p
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_Cached $q
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_add(self, p=None, q=None):
        
        r = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1", lambda : ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1())
        r.X = self.fe_add(p.Y, p.X)
        r.Y = self.fe_sub(p.Y, p.X)
        r.Z = self.fe_mul(r.X, q.YplusX)
        r.Y = self.fe_mul(r.Y, q.YminusX)
        r.T = self.fe_mul(q.T2d, p.T)
        r.X = self.fe_mul(p.Z, q.Z)
        t0 = self.fe_add(r.X, r.X)
        r.X = self.fe_sub(r.Z, r.Y)
        r.Y = self.fe_add(r.Z, r.Y)
        r.Z = self.fe_add(t0, r.T)
        r.T = self.fe_sub(t0, r.T)
        return r
    # end def ge_add
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @ref https://github.com/jedisct1/libsodium/blob/157c4a80c13b117608aeae12178b2d38825f9f8f/src/libsodium/crypto_core/curve25519/ref10/curve25519_ref10.c#L1185-L1215
    #// @param string $a
    #// @return array<int, mixed>
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArrayOffset
    #//
    @classmethod
    def slide(self, a=None):
        
        if self.strlen(a) < 256:
            if self.strlen(a) < 16:
                a = php_str_pad(a, 256, "0", STR_PAD_RIGHT)
            # end if
        # end if
        #// @var array<int, int> $r
        r = Array()
        i = 0
        while i < 256:
            
            r[i] = php_int(1 & self.chrtoint(a[i >> 3]) >> i & 7)
            i += 1
        # end while
        i = 0
        while i < 256:
            
            if r[i]:
                b = 1
                while b <= 6 and i + b < 256:
                    
                    if r[i + b]:
                        if r[i] + r[i + b] << b <= 15:
                            r[i] += r[i + b] << b
                            r[i + b] = 0
                        elif r[i] - r[i + b] << b >= -15:
                            r[i] -= r[i + b] << b
                            k = i + b
                            while k < 256:
                                
                                if (not r[k]):
                                    r[k] = 1
                                    break
                                # end if
                                r[k] = 0
                                k += 1
                            # end while
                        else:
                            break
                        # end if
                    # end if
                    b += 1
                # end while
            # end if
            i += 1
        # end while
        return r
    # end def slide
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $s
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_P3
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_frombytes_negate_vartime(self, s=None):
        
        ge_frombytes_negate_vartime.d = None
        if (not ge_frombytes_negate_vartime.d):
            #// @var ParagonIE_Sodium_Core32_Curve25519_Fe $d
            ge_frombytes_negate_vartime.d = ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(Array(ParagonIE_Sodium_Core32_Int32.fromint(self.ge_frombytes_negate_vartime.d[0]), ParagonIE_Sodium_Core32_Int32.fromint(self.ge_frombytes_negate_vartime.d[1]), ParagonIE_Sodium_Core32_Int32.fromint(self.ge_frombytes_negate_vartime.d[2]), ParagonIE_Sodium_Core32_Int32.fromint(self.ge_frombytes_negate_vartime.d[3]), ParagonIE_Sodium_Core32_Int32.fromint(self.ge_frombytes_negate_vartime.d[4]), ParagonIE_Sodium_Core32_Int32.fromint(self.ge_frombytes_negate_vartime.d[5]), ParagonIE_Sodium_Core32_Int32.fromint(self.ge_frombytes_negate_vartime.d[6]), ParagonIE_Sodium_Core32_Int32.fromint(self.ge_frombytes_negate_vartime.d[7]), ParagonIE_Sodium_Core32_Int32.fromint(self.ge_frombytes_negate_vartime.d[8]), ParagonIE_Sodium_Core32_Int32.fromint(self.ge_frombytes_negate_vartime.d[9])))
        # end if
        #// # fe_frombytes(h->Y,s);
        #// # fe_1(h->Z);
        h = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Ge_P3", lambda : ParagonIE_Sodium_Core32_Curve25519_Ge_P3(self.fe_0(), self.fe_frombytes(s), self.fe_1()))
        #// # fe_sq(u,h->Y);
        #// # fe_mul(v,u,d);
        #// # fe_sub(u,u,h->Z);       /* u = y^2-1
        #// # fe_add(v,v,h->Z);       /* v = dy^2+1
        u = self.fe_sq(h.Y)
        #// @var ParagonIE_Sodium_Core32_Curve25519_Fe $d
        v = self.fe_mul(u, ge_frombytes_negate_vartime.d)
        u = self.fe_sub(u, h.Z)
        #// u =  y^2 - 1
        v = self.fe_add(v, h.Z)
        #// v = dy^2 + 1
        #// # fe_sq(v3,v);
        #// # fe_mul(v3,v3,v);        /* v3 = v^3
        #// # fe_sq(h->X,v3);
        #// # fe_mul(h->X,h->X,v);
        #// # fe_mul(h->X,h->X,u);    /* x = uv^7
        v3 = self.fe_sq(v)
        v3 = self.fe_mul(v3, v)
        #// v3 = v^3
        h.X = self.fe_sq(v3)
        h.X = self.fe_mul(h.X, v)
        h.X = self.fe_mul(h.X, u)
        #// x = uv^7
        #// # fe_pow22523(h->X,h->X); /* x = (uv^7)^((q-5)/8)
        #// # fe_mul(h->X,h->X,v3);
        #// # fe_mul(h->X,h->X,u);    /* x = uv^3(uv^7)^((q-5)/8)
        h.X = self.fe_pow22523(h.X)
        #// x = (uv^7)^((q-5)/8)
        h.X = self.fe_mul(h.X, v3)
        h.X = self.fe_mul(h.X, u)
        #// x = uv^3(uv^7)^((q-5)/8)
        #// # fe_sq(vxx,h->X);
        #// # fe_mul(vxx,vxx,v);
        #// # fe_sub(check,vxx,u);    /* vx^2-u
        vxx = self.fe_sq(h.X)
        vxx = self.fe_mul(vxx, v)
        check = self.fe_sub(vxx, u)
        #// vx^2 - u
        #// # if (fe_isnonzero(check)) {
        #// #     fe_add(check,vxx,u);  /* vx^2+u
        #// #     if (fe_isnonzero(check)) {
        #// #         return -1;
        #// #     }
        #// #     fe_mul(h->X,h->X,sqrtm1);
        #// # }
        if self.fe_isnonzero(check):
            check = self.fe_add(vxx, u)
            #// vx^2 + u
            if self.fe_isnonzero(check):
                raise php_new_class("RangeException", lambda : RangeException("Internal check failed."))
            # end if
            h.X = self.fe_mul(h.X, ParagonIE_Sodium_Core32_Curve25519_Fe.fromintarray(self.sqrtm1))
        # end if
        #// # if (fe_isnegative(h->X) == (s[31] >> 7)) {
        #// #     fe_neg(h->X,h->X);
        #// # }
        i = self.chrtoint(s[31])
        if self.fe_isnegative(h.X) == i >> 7:
            h.X = self.fe_neg(h.X)
        # end if
        #// # fe_mul(h->T,h->X,h->Y);
        h.T = self.fe_mul(h.X, h.Y)
        return h
    # end def ge_frombytes_negate_vartime
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1 $R
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_P3 $p
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp $q
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_madd(self, R=None, p=None, q=None):
        
        r = copy.deepcopy(R)
        r.X = self.fe_add(p.Y, p.X)
        r.Y = self.fe_sub(p.Y, p.X)
        r.Z = self.fe_mul(r.X, q.yplusx)
        r.Y = self.fe_mul(r.Y, q.yminusx)
        r.T = self.fe_mul(q.xy2d, p.T)
        t0 = self.fe_add(copy.deepcopy(p.Z), copy.deepcopy(p.Z))
        r.X = self.fe_sub(r.Z, r.Y)
        r.Y = self.fe_add(r.Z, r.Y)
        r.Z = self.fe_add(t0, r.T)
        r.T = self.fe_sub(t0, r.T)
        return r
    # end def ge_madd
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1 $R
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_P3 $p
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp $q
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_msub(self, R=None, p=None, q=None):
        
        r = copy.deepcopy(R)
        r.X = self.fe_add(p.Y, p.X)
        r.Y = self.fe_sub(p.Y, p.X)
        r.Z = self.fe_mul(r.X, q.yminusx)
        r.Y = self.fe_mul(r.Y, q.yplusx)
        r.T = self.fe_mul(q.xy2d, p.T)
        t0 = self.fe_add(p.Z, p.Z)
        r.X = self.fe_sub(r.Z, r.Y)
        r.Y = self.fe_add(r.Z, r.Y)
        r.Z = self.fe_sub(t0, r.T)
        r.T = self.fe_add(t0, r.T)
        return r
    # end def ge_msub
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1 $p
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_P2
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_p1p1_to_p2(self, p=None):
        
        r = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Ge_P2", lambda : ParagonIE_Sodium_Core32_Curve25519_Ge_P2())
        r.X = self.fe_mul(p.X, p.T)
        r.Y = self.fe_mul(p.Y, p.Z)
        r.Z = self.fe_mul(p.Z, p.T)
        return r
    # end def ge_p1p1_to_p2
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1 $p
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_P3
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_p1p1_to_p3(self, p=None):
        
        r = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Ge_P3", lambda : ParagonIE_Sodium_Core32_Curve25519_Ge_P3())
        r.X = self.fe_mul(p.X, p.T)
        r.Y = self.fe_mul(p.Y, p.Z)
        r.Z = self.fe_mul(p.Z, p.T)
        r.T = self.fe_mul(p.X, p.Y)
        return r
    # end def ge_p1p1_to_p3
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_P2
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_p2_0(self):
        
        return php_new_class("ParagonIE_Sodium_Core32_Curve25519_Ge_P2", lambda : ParagonIE_Sodium_Core32_Curve25519_Ge_P2(self.fe_0(), self.fe_1(), self.fe_1()))
    # end def ge_p2_0
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_P2 $p
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_p2_dbl(self, p=None):
        
        r = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1", lambda : ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1())
        r.X = self.fe_sq(p.X)
        r.Z = self.fe_sq(p.Y)
        r.T = self.fe_sq2(p.Z)
        r.Y = self.fe_add(p.X, p.Y)
        t0 = self.fe_sq(r.Y)
        r.Y = self.fe_add(r.Z, r.X)
        r.Z = self.fe_sub(r.Z, r.X)
        r.X = self.fe_sub(t0, r.Y)
        r.T = self.fe_sub(r.T, r.Z)
        return r
    # end def ge_p2_dbl
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_P3
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_p3_0(self):
        
        return php_new_class("ParagonIE_Sodium_Core32_Curve25519_Ge_P3", lambda : ParagonIE_Sodium_Core32_Curve25519_Ge_P3(self.fe_0(), self.fe_1(), self.fe_1(), self.fe_0()))
    # end def ge_p3_0
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_P3 $p
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_Cached
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_p3_to_cached(self, p=None):
        
        ge_p3_to_cached.d2 = None
        if ge_p3_to_cached.d2 == None:
            ge_p3_to_cached.d2 = ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(Array(ParagonIE_Sodium_Core32_Int32.fromint(self.ge_p3_to_cached.d2[0]), ParagonIE_Sodium_Core32_Int32.fromint(self.ge_p3_to_cached.d2[1]), ParagonIE_Sodium_Core32_Int32.fromint(self.ge_p3_to_cached.d2[2]), ParagonIE_Sodium_Core32_Int32.fromint(self.ge_p3_to_cached.d2[3]), ParagonIE_Sodium_Core32_Int32.fromint(self.ge_p3_to_cached.d2[4]), ParagonIE_Sodium_Core32_Int32.fromint(self.ge_p3_to_cached.d2[5]), ParagonIE_Sodium_Core32_Int32.fromint(self.ge_p3_to_cached.d2[6]), ParagonIE_Sodium_Core32_Int32.fromint(self.ge_p3_to_cached.d2[7]), ParagonIE_Sodium_Core32_Int32.fromint(self.ge_p3_to_cached.d2[8]), ParagonIE_Sodium_Core32_Int32.fromint(self.ge_p3_to_cached.d2[9])))
        # end if
        #// @var ParagonIE_Sodium_Core32_Curve25519_Fe $d2
        r = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Ge_Cached", lambda : ParagonIE_Sodium_Core32_Curve25519_Ge_Cached())
        r.YplusX = self.fe_add(p.Y, p.X)
        r.YminusX = self.fe_sub(p.Y, p.X)
        r.Z = self.fe_copy(p.Z)
        r.T2d = self.fe_mul(p.T, ge_p3_to_cached.d2)
        return r
    # end def ge_p3_to_cached
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_P3 $p
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_P2
    #//
    @classmethod
    def ge_p3_to_p2(self, p=None):
        
        return php_new_class("ParagonIE_Sodium_Core32_Curve25519_Ge_P2", lambda : ParagonIE_Sodium_Core32_Curve25519_Ge_P2(p.X, p.Y, p.Z))
    # end def ge_p3_to_p2
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_P3 $h
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_p3_tobytes(self, h=None):
        
        recip = self.fe_invert(h.Z)
        x = self.fe_mul(h.X, recip)
        y = self.fe_mul(h.Y, recip)
        s = self.fe_tobytes(y)
        s[31] = self.inttochr(self.chrtoint(s[31]) ^ self.fe_isnegative(x) << 7)
        return s
    # end def ge_p3_tobytes
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_P3 $p
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_p3_dbl(self, p=None):
        
        q = self.ge_p3_to_p2(p)
        return self.ge_p2_dbl(q)
    # end def ge_p3_dbl
    #// 
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_precomp_0(self):
        
        return php_new_class("ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp", lambda : ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp(self.fe_1(), self.fe_1(), self.fe_0()))
    # end def ge_precomp_0
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int $b
    #// @param int $c
    #// @return int
    #// @psalm-suppress MixedReturnStatement
    #//
    @classmethod
    def equal(self, b=None, c=None):
        
        return php_int(b ^ c - 1 & 4294967295 >> 31)
    # end def equal
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string|int $char
    #// @return int (1 = yes, 0 = no)
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def negative(self, char=None):
        
        if php_is_int(char):
            return 1 if char < 0 else 0
        # end if
        #// @var string $char
        #// @var int $x
        x = self.chrtoint(self.substr(char, 0, 1))
        return php_int(x >> 31)
    # end def negative
    #// 
    #// Conditional move
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp $t
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp $u
    #// @param int $b
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def cmov(self, t=None, u=None, b=None):
        
        if (not php_is_int(b)):
            raise php_new_class("InvalidArgumentException", lambda : InvalidArgumentException("Expected an integer."))
        # end if
        return php_new_class("ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp", lambda : ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp(self.fe_cmov(t.yplusx, u.yplusx, b), self.fe_cmov(t.yminusx, u.yminusx, b), self.fe_cmov(t.xy2d, u.xy2d, b)))
    # end def cmov
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int $pos
    #// @param int $b
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArrayAccess
    #// @psalm-suppress MixedArrayOffset
    #// @psalm-suppress MixedArgument
    #//
    @classmethod
    def ge_select(self, pos=0, b=0):
        
        ge_select.base = None
        if ge_select.base == None:
            ge_select.base = Array()
            for i,bas in self.ge_select.base:
                j = 0
                while j < 8:
                    
                    ge_select.base[i][j] = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp", lambda : ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp(ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(Array(ParagonIE_Sodium_Core32_Int32.fromint(bas[j][0][0]), ParagonIE_Sodium_Core32_Int32.fromint(bas[j][0][1]), ParagonIE_Sodium_Core32_Int32.fromint(bas[j][0][2]), ParagonIE_Sodium_Core32_Int32.fromint(bas[j][0][3]), ParagonIE_Sodium_Core32_Int32.fromint(bas[j][0][4]), ParagonIE_Sodium_Core32_Int32.fromint(bas[j][0][5]), ParagonIE_Sodium_Core32_Int32.fromint(bas[j][0][6]), ParagonIE_Sodium_Core32_Int32.fromint(bas[j][0][7]), ParagonIE_Sodium_Core32_Int32.fromint(bas[j][0][8]), ParagonIE_Sodium_Core32_Int32.fromint(bas[j][0][9]))), ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(Array(ParagonIE_Sodium_Core32_Int32.fromint(bas[j][1][0]), ParagonIE_Sodium_Core32_Int32.fromint(bas[j][1][1]), ParagonIE_Sodium_Core32_Int32.fromint(bas[j][1][2]), ParagonIE_Sodium_Core32_Int32.fromint(bas[j][1][3]), ParagonIE_Sodium_Core32_Int32.fromint(bas[j][1][4]), ParagonIE_Sodium_Core32_Int32.fromint(bas[j][1][5]), ParagonIE_Sodium_Core32_Int32.fromint(bas[j][1][6]), ParagonIE_Sodium_Core32_Int32.fromint(bas[j][1][7]), ParagonIE_Sodium_Core32_Int32.fromint(bas[j][1][8]), ParagonIE_Sodium_Core32_Int32.fromint(bas[j][1][9]))), ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(Array(ParagonIE_Sodium_Core32_Int32.fromint(bas[j][2][0]), ParagonIE_Sodium_Core32_Int32.fromint(bas[j][2][1]), ParagonIE_Sodium_Core32_Int32.fromint(bas[j][2][2]), ParagonIE_Sodium_Core32_Int32.fromint(bas[j][2][3]), ParagonIE_Sodium_Core32_Int32.fromint(bas[j][2][4]), ParagonIE_Sodium_Core32_Int32.fromint(bas[j][2][5]), ParagonIE_Sodium_Core32_Int32.fromint(bas[j][2][6]), ParagonIE_Sodium_Core32_Int32.fromint(bas[j][2][7]), ParagonIE_Sodium_Core32_Int32.fromint(bas[j][2][8]), ParagonIE_Sodium_Core32_Int32.fromint(bas[j][2][9])))))
                    j += 1
                # end while
            # end for
        # end if
        if (not php_is_int(pos)):
            raise php_new_class("InvalidArgumentException", lambda : InvalidArgumentException("Position must be an integer"))
        # end if
        if pos < 0 or pos > 31:
            raise php_new_class("RangeException", lambda : RangeException("Position is out of range [0, 31]"))
        # end if
        bnegative = self.negative(b)
        #// @var int $babs
        babs = b - -bnegative & b << 1
        t = self.ge_precomp_0()
        i = 0
        while i < 8:
            
            t = self.cmov(t, ge_select.base[pos][i], self.equal(babs, i + 1))
            i += 1
        # end while
        minusT = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp", lambda : ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp(self.fe_copy(t.yminusx), self.fe_copy(t.yplusx), self.fe_neg(t.xy2d)))
        return self.cmov(t, minusT, -bnegative)
    # end def ge_select
    #// 
    #// Subtract two group elements.
    #// 
    #// r = p - q
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_P3 $p
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_Cached $q
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_sub(self, p=None, q=None):
        
        r = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1", lambda : ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1())
        r.X = self.fe_add(p.Y, p.X)
        r.Y = self.fe_sub(p.Y, p.X)
        r.Z = self.fe_mul(r.X, q.YminusX)
        r.Y = self.fe_mul(r.Y, q.YplusX)
        r.T = self.fe_mul(q.T2d, p.T)
        r.X = self.fe_mul(p.Z, q.Z)
        t0 = self.fe_add(r.X, r.X)
        r.X = self.fe_sub(r.Z, r.Y)
        r.Y = self.fe_add(r.Z, r.Y)
        r.Z = self.fe_sub(t0, r.T)
        r.T = self.fe_add(t0, r.T)
        return r
    # end def ge_sub
    #// 
    #// Convert a group element to a byte string.
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_P2 $h
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_tobytes(self, h=None):
        
        recip = self.fe_invert(h.Z)
        x = self.fe_mul(h.X, recip)
        y = self.fe_mul(h.Y, recip)
        s = self.fe_tobytes(y)
        s[31] = self.inttochr(self.chrtoint(s[31]) ^ self.fe_isnegative(x) << 7)
        return s
    # end def ge_tobytes
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $a
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_P3 $A
    #// @param string $b
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_P2
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArrayAccess
    #//
    @classmethod
    def ge_double_scalarmult_vartime(self, a=None, A=None, b=None):
        
        #// @var array<int, ParagonIE_Sodium_Core32_Curve25519_Ge_Cached> $Ai
        Ai = Array()
        ge_double_scalarmult_vartime.Bi = Array()
        #// @var array<int, ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp> $Bi
        if (not ge_double_scalarmult_vartime.Bi):
            i = 0
            while i < 8:
                
                ge_double_scalarmult_vartime.Bi[i] = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp", lambda : ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp(ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(Array(ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i][0][0]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i][0][1]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i][0][2]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i][0][3]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i][0][4]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i][0][5]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i][0][6]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i][0][7]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i][0][8]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i][0][9]))), ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(Array(ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i][1][0]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i][1][1]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i][1][2]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i][1][3]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i][1][4]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i][1][5]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i][1][6]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i][1][7]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i][1][8]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i][1][9]))), ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(Array(ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i][2][0]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i][2][1]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i][2][2]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i][2][3]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i][2][4]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i][2][5]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i][2][6]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i][2][7]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i][2][8]), ParagonIE_Sodium_Core32_Int32.fromint(self.base2[i][2][9])))))
                i += 1
            # end while
        # end if
        i = 0
        while i < 8:
            
            Ai[i] = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Ge_Cached", lambda : ParagonIE_Sodium_Core32_Curve25519_Ge_Cached(self.fe_0(), self.fe_0(), self.fe_0(), self.fe_0()))
            i += 1
        # end while
        #// @var array<int, ParagonIE_Sodium_Core32_Curve25519_Ge_Cached> $Ai
        #// # slide(aslide,a);
        #// # slide(bslide,b);
        #// @var array<int, int> $aslide
        aslide = self.slide(a)
        #// @var array<int, int> $bslide
        bslide = self.slide(b)
        #// # ge_p3_to_cached(&Ai[0],A);
        #// # ge_p3_dbl(&t,A); ge_p1p1_to_p3(&A2,&t);
        Ai[0] = self.ge_p3_to_cached(A)
        t = self.ge_p3_dbl(A)
        A2 = self.ge_p1p1_to_p3(t)
        #// # ge_add(&t,&A2,&Ai[0]); ge_p1p1_to_p3(&u,&t); ge_p3_to_cached(&Ai[1],&u);
        #// # ge_add(&t,&A2,&Ai[1]); ge_p1p1_to_p3(&u,&t); ge_p3_to_cached(&Ai[2],&u);
        #// # ge_add(&t,&A2,&Ai[2]); ge_p1p1_to_p3(&u,&t); ge_p3_to_cached(&Ai[3],&u);
        #// # ge_add(&t,&A2,&Ai[3]); ge_p1p1_to_p3(&u,&t); ge_p3_to_cached(&Ai[4],&u);
        #// # ge_add(&t,&A2,&Ai[4]); ge_p1p1_to_p3(&u,&t); ge_p3_to_cached(&Ai[5],&u);
        #// # ge_add(&t,&A2,&Ai[5]); ge_p1p1_to_p3(&u,&t); ge_p3_to_cached(&Ai[6],&u);
        #// # ge_add(&t,&A2,&Ai[6]); ge_p1p1_to_p3(&u,&t); ge_p3_to_cached(&Ai[7],&u);
        i = 0
        while i < 7:
            
            t = self.ge_add(A2, Ai[i])
            u = self.ge_p1p1_to_p3(t)
            Ai[i + 1] = self.ge_p3_to_cached(u)
            i += 1
        # end while
        #// # ge_p2_0(r);
        r = self.ge_p2_0()
        #// # for (i = 255;i >= 0;--i) {
        #// #     if (aslide[i] || bslide[i]) break;
        #// # }
        i = 255
        while i >= 0:
            
            if aslide[i] or bslide[i]:
                break
            # end if
            i -= 1
        # end while
        #// # for (;i >= 0;--i) {
        while i >= 0:
            
            #// # ge_p2_dbl(&t,r);
            t = self.ge_p2_dbl(r)
            #// # if (aslide[i] > 0) {
            if aslide[i] > 0:
                #// # ge_p1p1_to_p3(&u,&t);
                #// # ge_add(&t,&u,&Ai[aslide[i]/2]);
                u = self.ge_p1p1_to_p3(t)
                t = self.ge_add(u, Ai[php_int(floor(aslide[i] / 2))])
                pass
            elif aslide[i] < 0:
                #// # ge_p1p1_to_p3(&u,&t);
                #// # ge_sub(&t,&u,&Ai[(-aslide[i])/2]);
                u = self.ge_p1p1_to_p3(t)
                t = self.ge_sub(u, Ai[php_int(floor(-aslide[i] / 2))])
            # end if
            #// @var array<int, ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp> $Bi
            #// # if (bslide[i] > 0) {
            if bslide[i] > 0:
                #// # ge_p1p1_to_p3(&u,&t);
                #// # ge_madd(&t,&u,&Bi[bslide[i]/2]);
                u = self.ge_p1p1_to_p3(t)
                #// @var int $index
                index = php_int(floor(bslide[i] / 2))
                #// @var ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp $thisB
                thisB = ge_double_scalarmult_vartime.Bi[index]
                t = self.ge_madd(t, u, thisB)
                pass
            elif bslide[i] < 0:
                #// # ge_p1p1_to_p3(&u,&t);
                #// # ge_msub(&t,&u,&Bi[(-bslide[i])/2]);
                u = self.ge_p1p1_to_p3(t)
                #// @var int $index
                index = php_int(floor(-bslide[i] / 2))
                #// @var ParagonIE_Sodium_Core32_Curve25519_Ge_Precomp $thisB
                thisB = ge_double_scalarmult_vartime.Bi[index]
                t = self.ge_msub(t, u, thisB)
            # end if
            #// # ge_p1p1_to_p2(r,&t);
            r = self.ge_p1p1_to_p2(t)
            i -= 1
        # end while
        return r
    # end def ge_double_scalarmult_vartime
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $a
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_P3
    #// @psalm-suppress MixedAssignment
    #// @psalm-suppress MixedOperand
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_scalarmult_base(self, a=None):
        
        #// @var array<int, int> $e
        e = Array()
        r = php_new_class("ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1", lambda : ParagonIE_Sodium_Core32_Curve25519_Ge_P1p1())
        i = 0
        while i < 32:
            
            #// @var int $dbl
            dbl = php_int(i) << 1
            e[dbl] = php_int(self.chrtoint(a[i])) & 15
            e[dbl + 1] = php_int(self.chrtoint(a[i]) >> 4) & 15
            i += 1
        # end while
        #// @var int $carry
        carry = 0
        i = 0
        while i < 63:
            
            e[i] += carry
            #// @var int $carry
            carry = e[i] + 8
            #// @var int $carry
            carry >>= 4
            e[i] -= carry << 4
            i += 1
        # end while
        #// @var array<int, int> $e
        e[63] += php_int(carry)
        h = self.ge_p3_0()
        i = 1
        while i < 64:
            
            t = self.ge_select(php_int(floor(i / 2)), php_int(e[i]))
            r = self.ge_madd(r, h, t)
            h = self.ge_p1p1_to_p3(r)
            i += 2
        # end while
        r = self.ge_p3_dbl(h)
        s = self.ge_p1p1_to_p2(r)
        r = self.ge_p2_dbl(s)
        s = self.ge_p1p1_to_p2(r)
        r = self.ge_p2_dbl(s)
        s = self.ge_p1p1_to_p2(r)
        r = self.ge_p2_dbl(s)
        h = self.ge_p1p1_to_p3(r)
        i = 0
        while i < 64:
            
            t = self.ge_select(i >> 1, php_int(e[i]))
            r = self.ge_madd(r, h, t)
            h = self.ge_p1p1_to_p3(r)
            i += 2
        # end while
        return h
    # end def ge_scalarmult_base
    #// 
    #// Calculates (ab + c) mod l
    #// where l = 2^252 + 27742317777372353535851937790883648493
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $a
    #// @param string $b
    #// @param string $c
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def sc_muladd(self, a=None, b=None, c=None):
        
        a0 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(a, 0, 3)))
        a1 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(a, 2, 4)) >> 5)
        a2 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(a, 5, 3)) >> 2)
        a3 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(a, 7, 4)) >> 7)
        a4 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(a, 10, 4)) >> 4)
        a5 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(a, 13, 3)) >> 1)
        a6 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(a, 15, 4)) >> 6)
        a7 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(a, 18, 3)) >> 3)
        a8 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(a, 21, 3)))
        a9 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(a, 23, 4)) >> 5)
        a10 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(a, 26, 3)) >> 2)
        a11 = ParagonIE_Sodium_Core32_Int64.fromint(536870911 & self.load_4(self.substr(a, 28, 4)) >> 7)
        b0 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(b, 0, 3)))
        b1 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(b, 2, 4)) >> 5)
        b2 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(b, 5, 3)) >> 2)
        b3 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(b, 7, 4)) >> 7)
        b4 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(b, 10, 4)) >> 4)
        b5 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(b, 13, 3)) >> 1)
        b6 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(b, 15, 4)) >> 6)
        b7 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(b, 18, 3)) >> 3)
        b8 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(b, 21, 3)))
        b9 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(b, 23, 4)) >> 5)
        b10 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(b, 26, 3)) >> 2)
        b11 = ParagonIE_Sodium_Core32_Int64.fromint(536870911 & self.load_4(self.substr(b, 28, 4)) >> 7)
        c0 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(c, 0, 3)))
        c1 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(c, 2, 4)) >> 5)
        c2 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(c, 5, 3)) >> 2)
        c3 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(c, 7, 4)) >> 7)
        c4 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(c, 10, 4)) >> 4)
        c5 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(c, 13, 3)) >> 1)
        c6 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(c, 15, 4)) >> 6)
        c7 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(c, 18, 3)) >> 3)
        c8 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(c, 21, 3)))
        c9 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(c, 23, 4)) >> 5)
        c10 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(c, 26, 3)) >> 2)
        c11 = ParagonIE_Sodium_Core32_Int64.fromint(536870911 & self.load_4(self.substr(c, 28, 4)) >> 7)
        #// Can't really avoid the pyramid here:
        #// 
        #// @var ParagonIE_Sodium_Core32_Int64 $s0
        #// @var ParagonIE_Sodium_Core32_Int64 $s1
        #// @var ParagonIE_Sodium_Core32_Int64 $s2
        #// @var ParagonIE_Sodium_Core32_Int64 $s3
        #// @var ParagonIE_Sodium_Core32_Int64 $s4
        #// @var ParagonIE_Sodium_Core32_Int64 $s5
        #// @var ParagonIE_Sodium_Core32_Int64 $s6
        #// @var ParagonIE_Sodium_Core32_Int64 $s7
        #// @var ParagonIE_Sodium_Core32_Int64 $s8
        #// @var ParagonIE_Sodium_Core32_Int64 $s9
        #// @var ParagonIE_Sodium_Core32_Int64 $s10
        #// @var ParagonIE_Sodium_Core32_Int64 $s11
        #// @var ParagonIE_Sodium_Core32_Int64 $s12
        #// @var ParagonIE_Sodium_Core32_Int64 $s13
        #// @var ParagonIE_Sodium_Core32_Int64 $s14
        #// @var ParagonIE_Sodium_Core32_Int64 $s15
        #// @var ParagonIE_Sodium_Core32_Int64 $s16
        #// @var ParagonIE_Sodium_Core32_Int64 $s17
        #// @var ParagonIE_Sodium_Core32_Int64 $s18
        #// @var ParagonIE_Sodium_Core32_Int64 $s19
        #// @var ParagonIE_Sodium_Core32_Int64 $s20
        #// @var ParagonIE_Sodium_Core32_Int64 $s21
        #// @var ParagonIE_Sodium_Core32_Int64 $s22
        #// @var ParagonIE_Sodium_Core32_Int64 $s23
        #//
        s0 = c0.addint64(a0.mulint64(b0, 24))
        s1 = c1.addint64(a0.mulint64(b1, 24)).addint64(a1.mulint64(b0, 24))
        s2 = c2.addint64(a0.mulint64(b2, 24)).addint64(a1.mulint64(b1, 24)).addint64(a2.mulint64(b0, 24))
        s3 = c3.addint64(a0.mulint64(b3, 24)).addint64(a1.mulint64(b2, 24)).addint64(a2.mulint64(b1, 24)).addint64(a3.mulint64(b0, 24))
        s4 = c4.addint64(a0.mulint64(b4, 24)).addint64(a1.mulint64(b3, 24)).addint64(a2.mulint64(b2, 24)).addint64(a3.mulint64(b1, 24)).addint64(a4.mulint64(b0, 24))
        s5 = c5.addint64(a0.mulint64(b5, 24)).addint64(a1.mulint64(b4, 24)).addint64(a2.mulint64(b3, 24)).addint64(a3.mulint64(b2, 24)).addint64(a4.mulint64(b1, 24)).addint64(a5.mulint64(b0, 24))
        s6 = c6.addint64(a0.mulint64(b6, 24)).addint64(a1.mulint64(b5, 24)).addint64(a2.mulint64(b4, 24)).addint64(a3.mulint64(b3, 24)).addint64(a4.mulint64(b2, 24)).addint64(a5.mulint64(b1, 24)).addint64(a6.mulint64(b0, 24))
        s7 = c7.addint64(a0.mulint64(b7, 24)).addint64(a1.mulint64(b6, 24)).addint64(a2.mulint64(b5, 24)).addint64(a3.mulint64(b4, 24)).addint64(a4.mulint64(b3, 24)).addint64(a5.mulint64(b2, 24)).addint64(a6.mulint64(b1, 24)).addint64(a7.mulint64(b0, 24))
        s8 = c8.addint64(a0.mulint64(b8, 24)).addint64(a1.mulint64(b7, 24)).addint64(a2.mulint64(b6, 24)).addint64(a3.mulint64(b5, 24)).addint64(a4.mulint64(b4, 24)).addint64(a5.mulint64(b3, 24)).addint64(a6.mulint64(b2, 24)).addint64(a7.mulint64(b1, 24)).addint64(a8.mulint64(b0, 24))
        s9 = c9.addint64(a0.mulint64(b9, 24)).addint64(a1.mulint64(b8, 24)).addint64(a2.mulint64(b7, 24)).addint64(a3.mulint64(b6, 24)).addint64(a4.mulint64(b5, 24)).addint64(a5.mulint64(b4, 24)).addint64(a6.mulint64(b3, 24)).addint64(a7.mulint64(b2, 24)).addint64(a8.mulint64(b1, 24)).addint64(a9.mulint64(b0, 24))
        s10 = c10.addint64(a0.mulint64(b10, 24)).addint64(a1.mulint64(b9, 24)).addint64(a2.mulint64(b8, 24)).addint64(a3.mulint64(b7, 24)).addint64(a4.mulint64(b6, 24)).addint64(a5.mulint64(b5, 24)).addint64(a6.mulint64(b4, 24)).addint64(a7.mulint64(b3, 24)).addint64(a8.mulint64(b2, 24)).addint64(a9.mulint64(b1, 24)).addint64(a10.mulint64(b0, 24))
        s11 = c11.addint64(a0.mulint64(b11, 24)).addint64(a1.mulint64(b10, 24)).addint64(a2.mulint64(b9, 24)).addint64(a3.mulint64(b8, 24)).addint64(a4.mulint64(b7, 24)).addint64(a5.mulint64(b6, 24)).addint64(a6.mulint64(b5, 24)).addint64(a7.mulint64(b4, 24)).addint64(a8.mulint64(b3, 24)).addint64(a9.mulint64(b2, 24)).addint64(a10.mulint64(b1, 24)).addint64(a11.mulint64(b0, 24))
        s12 = a1.mulint64(b11, 24).addint64(a2.mulint64(b10, 24)).addint64(a3.mulint64(b9, 24)).addint64(a4.mulint64(b8, 24)).addint64(a5.mulint64(b7, 24)).addint64(a6.mulint64(b6, 24)).addint64(a7.mulint64(b5, 24)).addint64(a8.mulint64(b4, 24)).addint64(a9.mulint64(b3, 24)).addint64(a10.mulint64(b2, 24)).addint64(a11.mulint64(b1, 24))
        s13 = a2.mulint64(b11, 24).addint64(a3.mulint64(b10, 24)).addint64(a4.mulint64(b9, 24)).addint64(a5.mulint64(b8, 24)).addint64(a6.mulint64(b7, 24)).addint64(a7.mulint64(b6, 24)).addint64(a8.mulint64(b5, 24)).addint64(a9.mulint64(b4, 24)).addint64(a10.mulint64(b3, 24)).addint64(a11.mulint64(b2, 24))
        s14 = a3.mulint64(b11, 24).addint64(a4.mulint64(b10, 24)).addint64(a5.mulint64(b9, 24)).addint64(a6.mulint64(b8, 24)).addint64(a7.mulint64(b7, 24)).addint64(a8.mulint64(b6, 24)).addint64(a9.mulint64(b5, 24)).addint64(a10.mulint64(b4, 24)).addint64(a11.mulint64(b3, 24))
        s15 = a4.mulint64(b11, 24).addint64(a5.mulint64(b10, 24)).addint64(a6.mulint64(b9, 24)).addint64(a7.mulint64(b8, 24)).addint64(a8.mulint64(b7, 24)).addint64(a9.mulint64(b6, 24)).addint64(a10.mulint64(b5, 24)).addint64(a11.mulint64(b4, 24))
        s16 = a5.mulint64(b11, 24).addint64(a6.mulint64(b10, 24)).addint64(a7.mulint64(b9, 24)).addint64(a8.mulint64(b8, 24)).addint64(a9.mulint64(b7, 24)).addint64(a10.mulint64(b6, 24)).addint64(a11.mulint64(b5, 24))
        s17 = a6.mulint64(b11, 24).addint64(a7.mulint64(b10, 24)).addint64(a8.mulint64(b9, 24)).addint64(a9.mulint64(b8, 24)).addint64(a10.mulint64(b7, 24)).addint64(a11.mulint64(b6, 24))
        s18 = a7.mulint64(b11, 24).addint64(a8.mulint64(b10, 24)).addint64(a9.mulint64(b9, 24)).addint64(a10.mulint64(b8, 24)).addint64(a11.mulint64(b7, 24))
        s19 = a8.mulint64(b11, 24).addint64(a9.mulint64(b10, 24)).addint64(a10.mulint64(b9, 24)).addint64(a11.mulint64(b8, 24))
        s20 = a9.mulint64(b11, 24).addint64(a10.mulint64(b10, 24)).addint64(a11.mulint64(b9, 24))
        s21 = a10.mulint64(b11, 24).addint64(a11.mulint64(b10, 24))
        s22 = a11.mulint64(b11, 24)
        s23 = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        carry0 = s0.addint(1 << 20).shiftright(21)
        s1 = s1.addint64(carry0)
        s0 = s0.subint64(carry0.shiftleft(21))
        carry2 = s2.addint(1 << 20).shiftright(21)
        s3 = s3.addint64(carry2)
        s2 = s2.subint64(carry2.shiftleft(21))
        carry4 = s4.addint(1 << 20).shiftright(21)
        s5 = s5.addint64(carry4)
        s4 = s4.subint64(carry4.shiftleft(21))
        carry6 = s6.addint(1 << 20).shiftright(21)
        s7 = s7.addint64(carry6)
        s6 = s6.subint64(carry6.shiftleft(21))
        carry8 = s8.addint(1 << 20).shiftright(21)
        s9 = s9.addint64(carry8)
        s8 = s8.subint64(carry8.shiftleft(21))
        carry10 = s10.addint(1 << 20).shiftright(21)
        s11 = s11.addint64(carry10)
        s10 = s10.subint64(carry10.shiftleft(21))
        carry12 = s12.addint(1 << 20).shiftright(21)
        s13 = s13.addint64(carry12)
        s12 = s12.subint64(carry12.shiftleft(21))
        carry14 = s14.addint(1 << 20).shiftright(21)
        s15 = s15.addint64(carry14)
        s14 = s14.subint64(carry14.shiftleft(21))
        carry16 = s16.addint(1 << 20).shiftright(21)
        s17 = s17.addint64(carry16)
        s16 = s16.subint64(carry16.shiftleft(21))
        carry18 = s18.addint(1 << 20).shiftright(21)
        s19 = s19.addint64(carry18)
        s18 = s18.subint64(carry18.shiftleft(21))
        carry20 = s20.addint(1 << 20).shiftright(21)
        s21 = s21.addint64(carry20)
        s20 = s20.subint64(carry20.shiftleft(21))
        carry22 = s22.addint(1 << 20).shiftright(21)
        s23 = s23.addint64(carry22)
        s22 = s22.subint64(carry22.shiftleft(21))
        carry1 = s1.addint(1 << 20).shiftright(21)
        s2 = s2.addint64(carry1)
        s1 = s1.subint64(carry1.shiftleft(21))
        carry3 = s3.addint(1 << 20).shiftright(21)
        s4 = s4.addint64(carry3)
        s3 = s3.subint64(carry3.shiftleft(21))
        carry5 = s5.addint(1 << 20).shiftright(21)
        s6 = s6.addint64(carry5)
        s5 = s5.subint64(carry5.shiftleft(21))
        carry7 = s7.addint(1 << 20).shiftright(21)
        s8 = s8.addint64(carry7)
        s7 = s7.subint64(carry7.shiftleft(21))
        carry9 = s9.addint(1 << 20).shiftright(21)
        s10 = s10.addint64(carry9)
        s9 = s9.subint64(carry9.shiftleft(21))
        carry11 = s11.addint(1 << 20).shiftright(21)
        s12 = s12.addint64(carry11)
        s11 = s11.subint64(carry11.shiftleft(21))
        carry13 = s13.addint(1 << 20).shiftright(21)
        s14 = s14.addint64(carry13)
        s13 = s13.subint64(carry13.shiftleft(21))
        carry15 = s15.addint(1 << 20).shiftright(21)
        s16 = s16.addint64(carry15)
        s15 = s15.subint64(carry15.shiftleft(21))
        carry17 = s17.addint(1 << 20).shiftright(21)
        s18 = s18.addint64(carry17)
        s17 = s17.subint64(carry17.shiftleft(21))
        carry19 = s19.addint(1 << 20).shiftright(21)
        s20 = s20.addint64(carry19)
        s19 = s19.subint64(carry19.shiftleft(21))
        carry21 = s21.addint(1 << 20).shiftright(21)
        s22 = s22.addint64(carry21)
        s21 = s21.subint64(carry21.shiftleft(21))
        s11 = s11.addint64(s23.mulint(666643, 20))
        s12 = s12.addint64(s23.mulint(470296, 19))
        s13 = s13.addint64(s23.mulint(654183, 20))
        s14 = s14.subint64(s23.mulint(997805, 20))
        s15 = s15.addint64(s23.mulint(136657, 18))
        s16 = s16.subint64(s23.mulint(683901, 20))
        s10 = s10.addint64(s22.mulint(666643, 20))
        s11 = s11.addint64(s22.mulint(470296, 19))
        s12 = s12.addint64(s22.mulint(654183, 20))
        s13 = s13.subint64(s22.mulint(997805, 20))
        s14 = s14.addint64(s22.mulint(136657, 18))
        s15 = s15.subint64(s22.mulint(683901, 20))
        s9 = s9.addint64(s21.mulint(666643, 20))
        s10 = s10.addint64(s21.mulint(470296, 19))
        s11 = s11.addint64(s21.mulint(654183, 20))
        s12 = s12.subint64(s21.mulint(997805, 20))
        s13 = s13.addint64(s21.mulint(136657, 18))
        s14 = s14.subint64(s21.mulint(683901, 20))
        s8 = s8.addint64(s20.mulint(666643, 20))
        s9 = s9.addint64(s20.mulint(470296, 19))
        s10 = s10.addint64(s20.mulint(654183, 20))
        s11 = s11.subint64(s20.mulint(997805, 20))
        s12 = s12.addint64(s20.mulint(136657, 18))
        s13 = s13.subint64(s20.mulint(683901, 20))
        s7 = s7.addint64(s19.mulint(666643, 20))
        s8 = s8.addint64(s19.mulint(470296, 19))
        s9 = s9.addint64(s19.mulint(654183, 20))
        s10 = s10.subint64(s19.mulint(997805, 20))
        s11 = s11.addint64(s19.mulint(136657, 18))
        s12 = s12.subint64(s19.mulint(683901, 20))
        s6 = s6.addint64(s18.mulint(666643, 20))
        s7 = s7.addint64(s18.mulint(470296, 19))
        s8 = s8.addint64(s18.mulint(654183, 20))
        s9 = s9.subint64(s18.mulint(997805, 20))
        s10 = s10.addint64(s18.mulint(136657, 18))
        s11 = s11.subint64(s18.mulint(683901, 20))
        carry6 = s6.addint(1 << 20).shiftright(21)
        s7 = s7.addint64(carry6)
        s6 = s6.subint64(carry6.shiftleft(21))
        carry8 = s8.addint(1 << 20).shiftright(21)
        s9 = s9.addint64(carry8)
        s8 = s8.subint64(carry8.shiftleft(21))
        carry10 = s10.addint(1 << 20).shiftright(21)
        s11 = s11.addint64(carry10)
        s10 = s10.subint64(carry10.shiftleft(21))
        carry12 = s12.addint(1 << 20).shiftright(21)
        s13 = s13.addint64(carry12)
        s12 = s12.subint64(carry12.shiftleft(21))
        carry14 = s14.addint(1 << 20).shiftright(21)
        s15 = s15.addint64(carry14)
        s14 = s14.subint64(carry14.shiftleft(21))
        carry16 = s16.addint(1 << 20).shiftright(21)
        s17 = s17.addint64(carry16)
        s16 = s16.subint64(carry16.shiftleft(21))
        carry7 = s7.addint(1 << 20).shiftright(21)
        s8 = s8.addint64(carry7)
        s7 = s7.subint64(carry7.shiftleft(21))
        carry9 = s9.addint(1 << 20).shiftright(21)
        s10 = s10.addint64(carry9)
        s9 = s9.subint64(carry9.shiftleft(21))
        carry11 = s11.addint(1 << 20).shiftright(21)
        s12 = s12.addint64(carry11)
        s11 = s11.subint64(carry11.shiftleft(21))
        carry13 = s13.addint(1 << 20).shiftright(21)
        s14 = s14.addint64(carry13)
        s13 = s13.subint64(carry13.shiftleft(21))
        carry15 = s15.addint(1 << 20).shiftright(21)
        s16 = s16.addint64(carry15)
        s15 = s15.subint64(carry15.shiftleft(21))
        s5 = s5.addint64(s17.mulint(666643, 20))
        s6 = s6.addint64(s17.mulint(470296, 19))
        s7 = s7.addint64(s17.mulint(654183, 20))
        s8 = s8.subint64(s17.mulint(997805, 20))
        s9 = s9.addint64(s17.mulint(136657, 18))
        s10 = s10.subint64(s17.mulint(683901, 20))
        s4 = s4.addint64(s16.mulint(666643, 20))
        s5 = s5.addint64(s16.mulint(470296, 19))
        s6 = s6.addint64(s16.mulint(654183, 20))
        s7 = s7.subint64(s16.mulint(997805, 20))
        s8 = s8.addint64(s16.mulint(136657, 18))
        s9 = s9.subint64(s16.mulint(683901, 20))
        s3 = s3.addint64(s15.mulint(666643, 20))
        s4 = s4.addint64(s15.mulint(470296, 19))
        s5 = s5.addint64(s15.mulint(654183, 20))
        s6 = s6.subint64(s15.mulint(997805, 20))
        s7 = s7.addint64(s15.mulint(136657, 18))
        s8 = s8.subint64(s15.mulint(683901, 20))
        s2 = s2.addint64(s14.mulint(666643, 20))
        s3 = s3.addint64(s14.mulint(470296, 19))
        s4 = s4.addint64(s14.mulint(654183, 20))
        s5 = s5.subint64(s14.mulint(997805, 20))
        s6 = s6.addint64(s14.mulint(136657, 18))
        s7 = s7.subint64(s14.mulint(683901, 20))
        s1 = s1.addint64(s13.mulint(666643, 20))
        s2 = s2.addint64(s13.mulint(470296, 19))
        s3 = s3.addint64(s13.mulint(654183, 20))
        s4 = s4.subint64(s13.mulint(997805, 20))
        s5 = s5.addint64(s13.mulint(136657, 18))
        s6 = s6.subint64(s13.mulint(683901, 20))
        s0 = s0.addint64(s12.mulint(666643, 20))
        s1 = s1.addint64(s12.mulint(470296, 19))
        s2 = s2.addint64(s12.mulint(654183, 20))
        s3 = s3.subint64(s12.mulint(997805, 20))
        s4 = s4.addint64(s12.mulint(136657, 18))
        s5 = s5.subint64(s12.mulint(683901, 20))
        s12 = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        carry0 = s0.addint(1 << 20).shiftright(21)
        s1 = s1.addint64(carry0)
        s0 = s0.subint64(carry0.shiftleft(21))
        carry2 = s2.addint(1 << 20).shiftright(21)
        s3 = s3.addint64(carry2)
        s2 = s2.subint64(carry2.shiftleft(21))
        carry4 = s4.addint(1 << 20).shiftright(21)
        s5 = s5.addint64(carry4)
        s4 = s4.subint64(carry4.shiftleft(21))
        carry6 = s6.addint(1 << 20).shiftright(21)
        s7 = s7.addint64(carry6)
        s6 = s6.subint64(carry6.shiftleft(21))
        carry8 = s8.addint(1 << 20).shiftright(21)
        s9 = s9.addint64(carry8)
        s8 = s8.subint64(carry8.shiftleft(21))
        carry10 = s10.addint(1 << 20).shiftright(21)
        s11 = s11.addint64(carry10)
        s10 = s10.subint64(carry10.shiftleft(21))
        carry1 = s1.addint(1 << 20).shiftright(21)
        s2 = s2.addint64(carry1)
        s1 = s1.subint64(carry1.shiftleft(21))
        carry3 = s3.addint(1 << 20).shiftright(21)
        s4 = s4.addint64(carry3)
        s3 = s3.subint64(carry3.shiftleft(21))
        carry5 = s5.addint(1 << 20).shiftright(21)
        s6 = s6.addint64(carry5)
        s5 = s5.subint64(carry5.shiftleft(21))
        carry7 = s7.addint(1 << 20).shiftright(21)
        s8 = s8.addint64(carry7)
        s7 = s7.subint64(carry7.shiftleft(21))
        carry9 = s9.addint(1 << 20).shiftright(21)
        s10 = s10.addint64(carry9)
        s9 = s9.subint64(carry9.shiftleft(21))
        carry11 = s11.addint(1 << 20).shiftright(21)
        s12 = s12.addint64(carry11)
        s11 = s11.subint64(carry11.shiftleft(21))
        s0 = s0.addint64(s12.mulint(666643, 20))
        s1 = s1.addint64(s12.mulint(470296, 19))
        s2 = s2.addint64(s12.mulint(654183, 20))
        s3 = s3.subint64(s12.mulint(997805, 20))
        s4 = s4.addint64(s12.mulint(136657, 18))
        s5 = s5.subint64(s12.mulint(683901, 20))
        s12 = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        carry0 = s0.shiftright(21)
        s1 = s1.addint64(carry0)
        s0 = s0.subint64(carry0.shiftleft(21))
        carry1 = s1.shiftright(21)
        s2 = s2.addint64(carry1)
        s1 = s1.subint64(carry1.shiftleft(21))
        carry2 = s2.shiftright(21)
        s3 = s3.addint64(carry2)
        s2 = s2.subint64(carry2.shiftleft(21))
        carry3 = s3.shiftright(21)
        s4 = s4.addint64(carry3)
        s3 = s3.subint64(carry3.shiftleft(21))
        carry4 = s4.shiftright(21)
        s5 = s5.addint64(carry4)
        s4 = s4.subint64(carry4.shiftleft(21))
        carry5 = s5.shiftright(21)
        s6 = s6.addint64(carry5)
        s5 = s5.subint64(carry5.shiftleft(21))
        carry6 = s6.shiftright(21)
        s7 = s7.addint64(carry6)
        s6 = s6.subint64(carry6.shiftleft(21))
        carry7 = s7.shiftright(21)
        s8 = s8.addint64(carry7)
        s7 = s7.subint64(carry7.shiftleft(21))
        carry8 = s8.shiftright(21)
        s9 = s9.addint64(carry8)
        s8 = s8.subint64(carry8.shiftleft(21))
        carry9 = s9.shiftright(21)
        s10 = s10.addint64(carry9)
        s9 = s9.subint64(carry9.shiftleft(21))
        carry10 = s10.shiftright(21)
        s11 = s11.addint64(carry10)
        s10 = s10.subint64(carry10.shiftleft(21))
        carry11 = s11.shiftright(21)
        s12 = s12.addint64(carry11)
        s11 = s11.subint64(carry11.shiftleft(21))
        s0 = s0.addint64(s12.mulint(666643, 20))
        s1 = s1.addint64(s12.mulint(470296, 19))
        s2 = s2.addint64(s12.mulint(654183, 20))
        s3 = s3.subint64(s12.mulint(997805, 20))
        s4 = s4.addint64(s12.mulint(136657, 18))
        s5 = s5.subint64(s12.mulint(683901, 20))
        carry0 = s0.shiftright(21)
        s1 = s1.addint64(carry0)
        s0 = s0.subint64(carry0.shiftleft(21))
        carry1 = s1.shiftright(21)
        s2 = s2.addint64(carry1)
        s1 = s1.subint64(carry1.shiftleft(21))
        carry2 = s2.shiftright(21)
        s3 = s3.addint64(carry2)
        s2 = s2.subint64(carry2.shiftleft(21))
        carry3 = s3.shiftright(21)
        s4 = s4.addint64(carry3)
        s3 = s3.subint64(carry3.shiftleft(21))
        carry4 = s4.shiftright(21)
        s5 = s5.addint64(carry4)
        s4 = s4.subint64(carry4.shiftleft(21))
        carry5 = s5.shiftright(21)
        s6 = s6.addint64(carry5)
        s5 = s5.subint64(carry5.shiftleft(21))
        carry6 = s6.shiftright(21)
        s7 = s7.addint64(carry6)
        s6 = s6.subint64(carry6.shiftleft(21))
        carry7 = s7.shiftright(21)
        s8 = s8.addint64(carry7)
        s7 = s7.subint64(carry7.shiftleft(21))
        carry8 = s10.shiftright(21)
        s9 = s9.addint64(carry8)
        s8 = s8.subint64(carry8.shiftleft(21))
        carry9 = s9.shiftright(21)
        s10 = s10.addint64(carry9)
        s9 = s9.subint64(carry9.shiftleft(21))
        carry10 = s10.shiftright(21)
        s11 = s11.addint64(carry10)
        s10 = s10.subint64(carry10.shiftleft(21))
        S0 = s0.toint()
        S1 = s1.toint()
        S2 = s2.toint()
        S3 = s3.toint()
        S4 = s4.toint()
        S5 = s5.toint()
        S6 = s6.toint()
        S7 = s7.toint()
        S8 = s8.toint()
        S9 = s9.toint()
        S10 = s10.toint()
        S11 = s11.toint()
        #// 
        #// @var array<int, int>
        #//
        arr = Array(php_int(255 & S0 >> 0), php_int(255 & S0 >> 8), php_int(255 & S0 >> 16 | S1 << 5), php_int(255 & S1 >> 3), php_int(255 & S1 >> 11), php_int(255 & S1 >> 19 | S2 << 2), php_int(255 & S2 >> 6), php_int(255 & S2 >> 14 | S3 << 7), php_int(255 & S3 >> 1), php_int(255 & S3 >> 9), php_int(255 & S3 >> 17 | S4 << 4), php_int(255 & S4 >> 4), php_int(255 & S4 >> 12), php_int(255 & S4 >> 20 | S5 << 1), php_int(255 & S5 >> 7), php_int(255 & S5 >> 15 | S6 << 6), php_int(255 & S6 >> 2), php_int(255 & S6 >> 10), php_int(255 & S6 >> 18 | S7 << 3), php_int(255 & S7 >> 5), php_int(255 & S7 >> 13), php_int(255 & S8 >> 0), php_int(255 & S8 >> 8), php_int(255 & S8 >> 16 | S9 << 5), php_int(255 & S9 >> 3), php_int(255 & S9 >> 11), php_int(255 & S9 >> 19 | S10 << 2), php_int(255 & S10 >> 6), php_int(255 & S10 >> 14 | S11 << 7), php_int(255 & S11 >> 1), php_int(255 & S11 >> 9), php_int(255 & S11 >> 17))
        return self.intarraytostring(arr)
    # end def sc_muladd
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $s
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def sc_reduce(self, s=None):
        
        #// 
        #// @var ParagonIE_Sodium_Core32_Int64 $s0
        #// @var ParagonIE_Sodium_Core32_Int64 $s1
        #// @var ParagonIE_Sodium_Core32_Int64 $s2
        #// @var ParagonIE_Sodium_Core32_Int64 $s3
        #// @var ParagonIE_Sodium_Core32_Int64 $s4
        #// @var ParagonIE_Sodium_Core32_Int64 $s5
        #// @var ParagonIE_Sodium_Core32_Int64 $s6
        #// @var ParagonIE_Sodium_Core32_Int64 $s7
        #// @var ParagonIE_Sodium_Core32_Int64 $s8
        #// @var ParagonIE_Sodium_Core32_Int64 $s9
        #// @var ParagonIE_Sodium_Core32_Int64 $s10
        #// @var ParagonIE_Sodium_Core32_Int64 $s11
        #// @var ParagonIE_Sodium_Core32_Int64 $s12
        #// @var ParagonIE_Sodium_Core32_Int64 $s13
        #// @var ParagonIE_Sodium_Core32_Int64 $s14
        #// @var ParagonIE_Sodium_Core32_Int64 $s15
        #// @var ParagonIE_Sodium_Core32_Int64 $s16
        #// @var ParagonIE_Sodium_Core32_Int64 $s17
        #// @var ParagonIE_Sodium_Core32_Int64 $s18
        #// @var ParagonIE_Sodium_Core32_Int64 $s19
        #// @var ParagonIE_Sodium_Core32_Int64 $s20
        #// @var ParagonIE_Sodium_Core32_Int64 $s21
        #// @var ParagonIE_Sodium_Core32_Int64 $s22
        #// @var ParagonIE_Sodium_Core32_Int64 $s23
        #//
        s0 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(s, 0, 3)))
        s1 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(s, 2, 4)) >> 5)
        s2 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(s, 5, 3)) >> 2)
        s3 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(s, 7, 4)) >> 7)
        s4 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(s, 10, 4)) >> 4)
        s5 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(s, 13, 3)) >> 1)
        s6 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(s, 15, 4)) >> 6)
        s7 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(s, 18, 4)) >> 3)
        s8 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(s, 21, 3)))
        s9 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(s, 23, 4)) >> 5)
        s10 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(s, 26, 3)) >> 2)
        s11 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(s, 28, 4)) >> 7)
        s12 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(s, 31, 4)) >> 4)
        s13 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(s, 34, 3)) >> 1)
        s14 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(s, 36, 4)) >> 6)
        s15 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(s, 39, 4)) >> 3)
        s16 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(s, 42, 3)))
        s17 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(s, 44, 4)) >> 5)
        s18 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(s, 47, 3)) >> 2)
        s19 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(s, 49, 4)) >> 7)
        s20 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(s, 52, 4)) >> 4)
        s21 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_3(self.substr(s, 55, 3)) >> 1)
        s22 = ParagonIE_Sodium_Core32_Int64.fromint(2097151 & self.load_4(self.substr(s, 57, 4)) >> 6)
        s23 = ParagonIE_Sodium_Core32_Int64.fromint(536870911 & self.load_4(self.substr(s, 60, 4)) >> 3)
        s11 = s11.addint64(s23.mulint(666643, 20))
        s12 = s12.addint64(s23.mulint(470296, 19))
        s13 = s13.addint64(s23.mulint(654183, 20))
        s14 = s14.subint64(s23.mulint(997805, 20))
        s15 = s15.addint64(s23.mulint(136657, 18))
        s16 = s16.subint64(s23.mulint(683901, 20))
        s10 = s10.addint64(s22.mulint(666643, 20))
        s11 = s11.addint64(s22.mulint(470296, 19))
        s12 = s12.addint64(s22.mulint(654183, 20))
        s13 = s13.subint64(s22.mulint(997805, 20))
        s14 = s14.addint64(s22.mulint(136657, 18))
        s15 = s15.subint64(s22.mulint(683901, 20))
        s9 = s9.addint64(s21.mulint(666643, 20))
        s10 = s10.addint64(s21.mulint(470296, 19))
        s11 = s11.addint64(s21.mulint(654183, 20))
        s12 = s12.subint64(s21.mulint(997805, 20))
        s13 = s13.addint64(s21.mulint(136657, 18))
        s14 = s14.subint64(s21.mulint(683901, 20))
        s8 = s8.addint64(s20.mulint(666643, 20))
        s9 = s9.addint64(s20.mulint(470296, 19))
        s10 = s10.addint64(s20.mulint(654183, 20))
        s11 = s11.subint64(s20.mulint(997805, 20))
        s12 = s12.addint64(s20.mulint(136657, 18))
        s13 = s13.subint64(s20.mulint(683901, 20))
        s7 = s7.addint64(s19.mulint(666643, 20))
        s8 = s8.addint64(s19.mulint(470296, 19))
        s9 = s9.addint64(s19.mulint(654183, 20))
        s10 = s10.subint64(s19.mulint(997805, 20))
        s11 = s11.addint64(s19.mulint(136657, 18))
        s12 = s12.subint64(s19.mulint(683901, 20))
        s6 = s6.addint64(s18.mulint(666643, 20))
        s7 = s7.addint64(s18.mulint(470296, 19))
        s8 = s8.addint64(s18.mulint(654183, 20))
        s9 = s9.subint64(s18.mulint(997805, 20))
        s10 = s10.addint64(s18.mulint(136657, 18))
        s11 = s11.subint64(s18.mulint(683901, 20))
        carry6 = s6.addint(1 << 20).shiftright(21)
        s7 = s7.addint64(carry6)
        s6 = s6.subint64(carry6.shiftleft(21))
        carry8 = s8.addint(1 << 20).shiftright(21)
        s9 = s9.addint64(carry8)
        s8 = s8.subint64(carry8.shiftleft(21))
        carry10 = s10.addint(1 << 20).shiftright(21)
        s11 = s11.addint64(carry10)
        s10 = s10.subint64(carry10.shiftleft(21))
        carry12 = s12.addint(1 << 20).shiftright(21)
        s13 = s13.addint64(carry12)
        s12 = s12.subint64(carry12.shiftleft(21))
        carry14 = s14.addint(1 << 20).shiftright(21)
        s15 = s15.addint64(carry14)
        s14 = s14.subint64(carry14.shiftleft(21))
        carry16 = s16.addint(1 << 20).shiftright(21)
        s17 = s17.addint64(carry16)
        s16 = s16.subint64(carry16.shiftleft(21))
        carry7 = s7.addint(1 << 20).shiftright(21)
        s8 = s8.addint64(carry7)
        s7 = s7.subint64(carry7.shiftleft(21))
        carry9 = s9.addint(1 << 20).shiftright(21)
        s10 = s10.addint64(carry9)
        s9 = s9.subint64(carry9.shiftleft(21))
        carry11 = s11.addint(1 << 20).shiftright(21)
        s12 = s12.addint64(carry11)
        s11 = s11.subint64(carry11.shiftleft(21))
        carry13 = s13.addint(1 << 20).shiftright(21)
        s14 = s14.addint64(carry13)
        s13 = s13.subint64(carry13.shiftleft(21))
        carry15 = s15.addint(1 << 20).shiftright(21)
        s16 = s16.addint64(carry15)
        s15 = s15.subint64(carry15.shiftleft(21))
        s5 = s5.addint64(s17.mulint(666643, 20))
        s6 = s6.addint64(s17.mulint(470296, 19))
        s7 = s7.addint64(s17.mulint(654183, 20))
        s8 = s8.subint64(s17.mulint(997805, 20))
        s9 = s9.addint64(s17.mulint(136657, 18))
        s10 = s10.subint64(s17.mulint(683901, 20))
        s4 = s4.addint64(s16.mulint(666643, 20))
        s5 = s5.addint64(s16.mulint(470296, 19))
        s6 = s6.addint64(s16.mulint(654183, 20))
        s7 = s7.subint64(s16.mulint(997805, 20))
        s8 = s8.addint64(s16.mulint(136657, 18))
        s9 = s9.subint64(s16.mulint(683901, 20))
        s3 = s3.addint64(s15.mulint(666643, 20))
        s4 = s4.addint64(s15.mulint(470296, 19))
        s5 = s5.addint64(s15.mulint(654183, 20))
        s6 = s6.subint64(s15.mulint(997805, 20))
        s7 = s7.addint64(s15.mulint(136657, 18))
        s8 = s8.subint64(s15.mulint(683901, 20))
        s2 = s2.addint64(s14.mulint(666643, 20))
        s3 = s3.addint64(s14.mulint(470296, 19))
        s4 = s4.addint64(s14.mulint(654183, 20))
        s5 = s5.subint64(s14.mulint(997805, 20))
        s6 = s6.addint64(s14.mulint(136657, 18))
        s7 = s7.subint64(s14.mulint(683901, 20))
        s1 = s1.addint64(s13.mulint(666643, 20))
        s2 = s2.addint64(s13.mulint(470296, 19))
        s3 = s3.addint64(s13.mulint(654183, 20))
        s4 = s4.subint64(s13.mulint(997805, 20))
        s5 = s5.addint64(s13.mulint(136657, 18))
        s6 = s6.subint64(s13.mulint(683901, 20))
        s0 = s0.addint64(s12.mulint(666643, 20))
        s1 = s1.addint64(s12.mulint(470296, 19))
        s2 = s2.addint64(s12.mulint(654183, 20))
        s3 = s3.subint64(s12.mulint(997805, 20))
        s4 = s4.addint64(s12.mulint(136657, 18))
        s5 = s5.subint64(s12.mulint(683901, 20))
        s12 = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        carry0 = s0.addint(1 << 20).shiftright(21)
        s1 = s1.addint64(carry0)
        s0 = s0.subint64(carry0.shiftleft(21))
        carry2 = s2.addint(1 << 20).shiftright(21)
        s3 = s3.addint64(carry2)
        s2 = s2.subint64(carry2.shiftleft(21))
        carry4 = s4.addint(1 << 20).shiftright(21)
        s5 = s5.addint64(carry4)
        s4 = s4.subint64(carry4.shiftleft(21))
        carry6 = s6.addint(1 << 20).shiftright(21)
        s7 = s7.addint64(carry6)
        s6 = s6.subint64(carry6.shiftleft(21))
        carry8 = s8.addint(1 << 20).shiftright(21)
        s9 = s9.addint64(carry8)
        s8 = s8.subint64(carry8.shiftleft(21))
        carry10 = s10.addint(1 << 20).shiftright(21)
        s11 = s11.addint64(carry10)
        s10 = s10.subint64(carry10.shiftleft(21))
        carry1 = s1.addint(1 << 20).shiftright(21)
        s2 = s2.addint64(carry1)
        s1 = s1.subint64(carry1.shiftleft(21))
        carry3 = s3.addint(1 << 20).shiftright(21)
        s4 = s4.addint64(carry3)
        s3 = s3.subint64(carry3.shiftleft(21))
        carry5 = s5.addint(1 << 20).shiftright(21)
        s6 = s6.addint64(carry5)
        s5 = s5.subint64(carry5.shiftleft(21))
        carry7 = s7.addint(1 << 20).shiftright(21)
        s8 = s8.addint64(carry7)
        s7 = s7.subint64(carry7.shiftleft(21))
        carry9 = s9.addint(1 << 20).shiftright(21)
        s10 = s10.addint64(carry9)
        s9 = s9.subint64(carry9.shiftleft(21))
        carry11 = s11.addint(1 << 20).shiftright(21)
        s12 = s12.addint64(carry11)
        s11 = s11.subint64(carry11.shiftleft(21))
        s0 = s0.addint64(s12.mulint(666643, 20))
        s1 = s1.addint64(s12.mulint(470296, 19))
        s2 = s2.addint64(s12.mulint(654183, 20))
        s3 = s3.subint64(s12.mulint(997805, 20))
        s4 = s4.addint64(s12.mulint(136657, 18))
        s5 = s5.subint64(s12.mulint(683901, 20))
        s12 = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        carry0 = s0.shiftright(21)
        s1 = s1.addint64(carry0)
        s0 = s0.subint64(carry0.shiftleft(21))
        carry1 = s1.shiftright(21)
        s2 = s2.addint64(carry1)
        s1 = s1.subint64(carry1.shiftleft(21))
        carry2 = s2.shiftright(21)
        s3 = s3.addint64(carry2)
        s2 = s2.subint64(carry2.shiftleft(21))
        carry3 = s3.shiftright(21)
        s4 = s4.addint64(carry3)
        s3 = s3.subint64(carry3.shiftleft(21))
        carry4 = s4.shiftright(21)
        s5 = s5.addint64(carry4)
        s4 = s4.subint64(carry4.shiftleft(21))
        carry5 = s5.shiftright(21)
        s6 = s6.addint64(carry5)
        s5 = s5.subint64(carry5.shiftleft(21))
        carry6 = s6.shiftright(21)
        s7 = s7.addint64(carry6)
        s6 = s6.subint64(carry6.shiftleft(21))
        carry7 = s7.shiftright(21)
        s8 = s8.addint64(carry7)
        s7 = s7.subint64(carry7.shiftleft(21))
        carry8 = s8.shiftright(21)
        s9 = s9.addint64(carry8)
        s8 = s8.subint64(carry8.shiftleft(21))
        carry9 = s9.shiftright(21)
        s10 = s10.addint64(carry9)
        s9 = s9.subint64(carry9.shiftleft(21))
        carry10 = s10.shiftright(21)
        s11 = s11.addint64(carry10)
        s10 = s10.subint64(carry10.shiftleft(21))
        carry11 = s11.shiftright(21)
        s12 = s12.addint64(carry11)
        s11 = s11.subint64(carry11.shiftleft(21))
        s0 = s0.addint64(s12.mulint(666643, 20))
        s1 = s1.addint64(s12.mulint(470296, 19))
        s2 = s2.addint64(s12.mulint(654183, 20))
        s3 = s3.subint64(s12.mulint(997805, 20))
        s4 = s4.addint64(s12.mulint(136657, 18))
        s5 = s5.subint64(s12.mulint(683901, 20))
        carry0 = s0.shiftright(21)
        s1 = s1.addint64(carry0)
        s0 = s0.subint64(carry0.shiftleft(21))
        carry1 = s1.shiftright(21)
        s2 = s2.addint64(carry1)
        s1 = s1.subint64(carry1.shiftleft(21))
        carry2 = s2.shiftright(21)
        s3 = s3.addint64(carry2)
        s2 = s2.subint64(carry2.shiftleft(21))
        carry3 = s3.shiftright(21)
        s4 = s4.addint64(carry3)
        s3 = s3.subint64(carry3.shiftleft(21))
        carry4 = s4.shiftright(21)
        s5 = s5.addint64(carry4)
        s4 = s4.subint64(carry4.shiftleft(21))
        carry5 = s5.shiftright(21)
        s6 = s6.addint64(carry5)
        s5 = s5.subint64(carry5.shiftleft(21))
        carry6 = s6.shiftright(21)
        s7 = s7.addint64(carry6)
        s6 = s6.subint64(carry6.shiftleft(21))
        carry7 = s7.shiftright(21)
        s8 = s8.addint64(carry7)
        s7 = s7.subint64(carry7.shiftleft(21))
        carry8 = s8.shiftright(21)
        s9 = s9.addint64(carry8)
        s8 = s8.subint64(carry8.shiftleft(21))
        carry9 = s9.shiftright(21)
        s10 = s10.addint64(carry9)
        s9 = s9.subint64(carry9.shiftleft(21))
        carry10 = s10.shiftright(21)
        s11 = s11.addint64(carry10)
        s10 = s10.subint64(carry10.shiftleft(21))
        S0 = s0.toint32().toint()
        S1 = s1.toint32().toint()
        S2 = s2.toint32().toint()
        S3 = s3.toint32().toint()
        S4 = s4.toint32().toint()
        S5 = s5.toint32().toint()
        S6 = s6.toint32().toint()
        S7 = s7.toint32().toint()
        S8 = s8.toint32().toint()
        S9 = s9.toint32().toint()
        S10 = s10.toint32().toint()
        S11 = s11.toint32().toint()
        #// 
        #// @var array<int, int>
        #//
        arr = Array(php_int(S0 >> 0), php_int(S0 >> 8), php_int(S0 >> 16 | S1 << 5), php_int(S1 >> 3), php_int(S1 >> 11), php_int(S1 >> 19 | S2 << 2), php_int(S2 >> 6), php_int(S2 >> 14 | S3 << 7), php_int(S3 >> 1), php_int(S3 >> 9), php_int(S3 >> 17 | S4 << 4), php_int(S4 >> 4), php_int(S4 >> 12), php_int(S4 >> 20 | S5 << 1), php_int(S5 >> 7), php_int(S5 >> 15 | S6 << 6), php_int(S6 >> 2), php_int(S6 >> 10), php_int(S6 >> 18 | S7 << 3), php_int(S7 >> 5), php_int(S7 >> 13), php_int(S8 >> 0), php_int(S8 >> 8), php_int(S8 >> 16 | S9 << 5), php_int(S9 >> 3), php_int(S9 >> 11), php_int(S9 >> 19 | S10 << 2), php_int(S10 >> 6), php_int(S10 >> 14 | S11 << 7), php_int(S11 >> 1), php_int(S11 >> 9), php_int(S11) >> 17)
        return self.intarraytostring(arr)
    # end def sc_reduce
    #// 
    #// multiply by the order of the main subgroup l = 2^252+27742317777372353535851937790883648493
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Ge_P3 $A
    #// @return ParagonIE_Sodium_Core32_Curve25519_Ge_P3
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_mul_l(self, A=None):
        
        #// @var array<int, int> $aslide
        aslide = Array(13, 0, 0, 0, 0, -1, 0, 0, 0, 0, -11, 0, 0, 0, 0, 0, 0, -5, 0, 0, 0, 0, 0, 0, -3, 0, 0, 0, 0, -13, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, -13, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 11, 0, 0, 0, 0, 0, 11, 0, 0, 0, 0, -13, 0, 0, 0, 0, 0, 0, -3, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 3, 0, 0, 0, 0, -11, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)
        #// @var array<int, ParagonIE_Sodium_Core32_Curve25519_Ge_Cached> $Ai size 8
        Ai = Array()
        #// # ge_p3_to_cached(&Ai[0], A);
        Ai[0] = self.ge_p3_to_cached(A)
        #// # ge_p3_dbl(&t, A);
        t = self.ge_p3_dbl(A)
        #// # ge_p1p1_to_p3(&A2, &t);
        A2 = self.ge_p1p1_to_p3(t)
        i = 1
        while i < 8:
            
            #// # ge_add(&t, &A2, &Ai[0]);
            t = self.ge_add(A2, Ai[i - 1])
            #// # ge_p1p1_to_p3(&u, &t);
            u = self.ge_p1p1_to_p3(t)
            #// # ge_p3_to_cached(&Ai[i], &u);
            Ai[i] = self.ge_p3_to_cached(u)
            i += 1
        # end while
        r = self.ge_p3_0()
        i = 252
        while i >= 0:
            
            t = self.ge_p3_dbl(r)
            if aslide[i] > 0:
                #// # ge_p1p1_to_p3(&u, &t);
                u = self.ge_p1p1_to_p3(t)
                #// # ge_add(&t, &u, &Ai[aslide[i] / 2]);
                t = self.ge_add(u, Ai[php_int(aslide[i] / 2)])
            elif aslide[i] < 0:
                #// # ge_p1p1_to_p3(&u, &t);
                u = self.ge_p1p1_to_p3(t)
                #// # ge_sub(&t, &u, &Ai[(-aslide[i]) / 2]);
                t = self.ge_sub(u, Ai[php_int(-aslide[i] / 2)])
            # end if
            i -= 1
        # end while
        #// # ge_p1p1_to_p3(r, &t);
        return self.ge_p1p1_to_p3(t)
    # end def ge_mul_l
# end class ParagonIE_Sodium_Core32_Curve25519
