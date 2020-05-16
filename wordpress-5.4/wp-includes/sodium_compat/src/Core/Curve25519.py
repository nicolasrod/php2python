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
if php_class_exists("ParagonIE_Sodium_Core_Curve25519", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core_Curve25519
#// 
#// Implements Curve25519 core functions
#// 
#// Based on the ref10 curve25519 code provided by libsodium
#// 
#// @ref https://github.com/jedisct1/libsodium/blob/master/src/libsodium/crypto_core/curve25519/ref10/curve25519_ref10.c
#//
class ParagonIE_Sodium_Core_Curve25519(ParagonIE_Sodium_Core_Curve25519_H):
    #// 
    #// Get a field element of size 10 with a value of 0
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @return ParagonIE_Sodium_Core_Curve25519_Fe
    #//
    @classmethod
    def fe_0(self):
        
        return ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(Array(0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
    # end def fe_0
    #// 
    #// Get a field element of size 10 with a value of 1
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @return ParagonIE_Sodium_Core_Curve25519_Fe
    #//
    @classmethod
    def fe_1(self):
        
        return ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(Array(1, 0, 0, 0, 0, 0, 0, 0, 0, 0))
    # end def fe_1
    #// 
    #// Add two field elements.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $f
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $g
    #// @return ParagonIE_Sodium_Core_Curve25519_Fe
    #// @psalm-suppress MixedAssignment
    #// @psalm-suppress MixedOperand
    #//
    @classmethod
    def fe_add(self, f=None, g=None):
        
        #// @var array<int, int> $arr
        arr = Array()
        i = 0
        while i < 10:
            
            arr[i] = php_int(f[i] + g[i])
            i += 1
        # end while
        return ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(arr)
    # end def fe_add
    #// 
    #// Constant-time conditional move.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $f
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $g
    #// @param int $b
    #// @return ParagonIE_Sodium_Core_Curve25519_Fe
    #// @psalm-suppress MixedAssignment
    #//
    @classmethod
    def fe_cmov(self, f=None, g=None, b=0):
        
        #// @var array<int, int> $h
        h = Array()
        b *= -1
        i = 0
        while i < 10:
            
            #// @var int $x
            x = f[i] ^ g[i] & b
            h[i] = php_int(php_int(f[i]) ^ x)
            i += 1
        # end while
        return ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(h)
    # end def fe_cmov
    #// 
    #// Create a copy of a field element.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $f
    #// @return ParagonIE_Sodium_Core_Curve25519_Fe
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
    #// @return ParagonIE_Sodium_Core_Curve25519_Fe
    #// @throws RangeException
    #// @throws TypeError
    #//
    @classmethod
    def fe_frombytes(self, s=None):
        
        if self.strlen(s) != 32:
            raise php_new_class("RangeException", lambda : RangeException("Expected a 32-byte string."))
        # end if
        #// @var int $h0
        h0 = self.load_4(s)
        #// @var int $h1
        h1 = self.load_3(self.substr(s, 4, 3)) << 6
        #// @var int $h2
        h2 = self.load_3(self.substr(s, 7, 3)) << 5
        #// @var int $h3
        h3 = self.load_3(self.substr(s, 10, 3)) << 3
        #// @var int $h4
        h4 = self.load_3(self.substr(s, 13, 3)) << 2
        #// @var int $h5
        h5 = self.load_4(self.substr(s, 16, 4))
        #// @var int $h6
        h6 = self.load_3(self.substr(s, 20, 3)) << 7
        #// @var int $h7
        h7 = self.load_3(self.substr(s, 23, 3)) << 5
        #// @var int $h8
        h8 = self.load_3(self.substr(s, 26, 3)) << 4
        #// @var int $h9
        h9 = self.load_3(self.substr(s, 29, 3)) & 8388607 << 2
        #// @var int $carry9
        carry9 = h9 + 1 << 24 >> 25
        h0 += self.mul(carry9, 19, 5)
        h9 -= carry9 << 25
        #// @var int $carry1
        carry1 = h1 + 1 << 24 >> 25
        h2 += carry1
        h1 -= carry1 << 25
        #// @var int $carry3
        carry3 = h3 + 1 << 24 >> 25
        h4 += carry3
        h3 -= carry3 << 25
        #// @var int $carry5
        carry5 = h5 + 1 << 24 >> 25
        h6 += carry5
        h5 -= carry5 << 25
        #// @var int $carry7
        carry7 = h7 + 1 << 24 >> 25
        h8 += carry7
        h7 -= carry7 << 25
        #// @var int $carry0
        carry0 = h0 + 1 << 25 >> 26
        h1 += carry0
        h0 -= carry0 << 26
        #// @var int $carry2
        carry2 = h2 + 1 << 25 >> 26
        h3 += carry2
        h2 -= carry2 << 26
        #// @var int $carry4
        carry4 = h4 + 1 << 25 >> 26
        h5 += carry4
        h4 -= carry4 << 26
        #// @var int $carry6
        carry6 = h6 + 1 << 25 >> 26
        h7 += carry6
        h6 -= carry6 << 26
        #// @var int $carry8
        carry8 = h8 + 1 << 25 >> 26
        h9 += carry8
        h8 -= carry8 << 26
        return ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(Array(php_int(h0), php_int(h1), php_int(h2), php_int(h3), php_int(h4), php_int(h5), php_int(h6), php_int(h7), php_int(h8), php_int(h9)))
    # end def fe_frombytes
    #// 
    #// Convert a field element to a byte string.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $h
    #// @return string
    #//
    @classmethod
    def fe_tobytes(self, h=None):
        
        #// @var int $h0
        h0 = php_int(h[0])
        #// @var int $h1
        h1 = php_int(h[1])
        #// @var int $h2
        h2 = php_int(h[2])
        #// @var int $h3
        h3 = php_int(h[3])
        #// @var int $h4
        h4 = php_int(h[4])
        #// @var int $h5
        h5 = php_int(h[5])
        #// @var int $h6
        h6 = php_int(h[6])
        #// @var int $h7
        h7 = php_int(h[7])
        #// @var int $h8
        h8 = php_int(h[8])
        #// @var int $h9
        h9 = php_int(h[9])
        #// @var int $q
        q = self.mul(h9, 19, 5) + 1 << 24 >> 25
        #// @var int $q
        q = h0 + q >> 26
        #// @var int $q
        q = h1 + q >> 25
        #// @var int $q
        q = h2 + q >> 26
        #// @var int $q
        q = h3 + q >> 25
        #// @var int $q
        q = h4 + q >> 26
        #// @var int $q
        q = h5 + q >> 25
        #// @var int $q
        q = h6 + q >> 26
        #// @var int $q
        q = h7 + q >> 25
        #// @var int $q
        q = h8 + q >> 26
        #// @var int $q
        q = h9 + q >> 25
        h0 += self.mul(q, 19, 5)
        #// @var int $carry0
        carry0 = h0 >> 26
        h1 += carry0
        h0 -= carry0 << 26
        #// @var int $carry1
        carry1 = h1 >> 25
        h2 += carry1
        h1 -= carry1 << 25
        #// @var int $carry2
        carry2 = h2 >> 26
        h3 += carry2
        h2 -= carry2 << 26
        #// @var int $carry3
        carry3 = h3 >> 25
        h4 += carry3
        h3 -= carry3 << 25
        #// @var int $carry4
        carry4 = h4 >> 26
        h5 += carry4
        h4 -= carry4 << 26
        #// @var int $carry5
        carry5 = h5 >> 25
        h6 += carry5
        h5 -= carry5 << 25
        #// @var int $carry6
        carry6 = h6 >> 26
        h7 += carry6
        h6 -= carry6 << 26
        #// @var int $carry7
        carry7 = h7 >> 25
        h8 += carry7
        h7 -= carry7 << 25
        #// @var int $carry8
        carry8 = h8 >> 26
        h9 += carry8
        h8 -= carry8 << 26
        #// @var int $carry9
        carry9 = h9 >> 25
        h9 -= carry9 << 25
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
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $f
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
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $f
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
        #// @var string $zero
        #// @var string $str
        str = self.fe_tobytes(f)
        return (not self.verify_32(str, php_str(fe_isnonzero.zero)))
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
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $f
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $g
    #// @return ParagonIE_Sodium_Core_Curve25519_Fe
    #//
    @classmethod
    def fe_mul(self, f=None, g=None):
        
        #// @var int $f0
        f0 = f[0]
        #// @var int $f1
        f1 = f[1]
        #// @var int $f2
        f2 = f[2]
        #// @var int $f3
        f3 = f[3]
        #// @var int $f4
        f4 = f[4]
        #// @var int $f5
        f5 = f[5]
        #// @var int $f6
        f6 = f[6]
        #// @var int $f7
        f7 = f[7]
        #// @var int $f8
        f8 = f[8]
        #// @var int $f9
        f9 = f[9]
        #// @var int $g0
        g0 = g[0]
        #// @var int $g1
        g1 = g[1]
        #// @var int $g2
        g2 = g[2]
        #// @var int $g3
        g3 = g[3]
        #// @var int $g4
        g4 = g[4]
        #// @var int $g5
        g5 = g[5]
        #// @var int $g6
        g6 = g[6]
        #// @var int $g7
        g7 = g[7]
        #// @var int $g8
        g8 = g[8]
        #// @var int $g9
        g9 = g[9]
        g1_19 = self.mul(g1, 19, 5)
        g2_19 = self.mul(g2, 19, 5)
        g3_19 = self.mul(g3, 19, 5)
        g4_19 = self.mul(g4, 19, 5)
        g5_19 = self.mul(g5, 19, 5)
        g6_19 = self.mul(g6, 19, 5)
        g7_19 = self.mul(g7, 19, 5)
        g8_19 = self.mul(g8, 19, 5)
        g9_19 = self.mul(g9, 19, 5)
        #// @var int $f1_2
        f1_2 = f1 << 1
        #// @var int $f3_2
        f3_2 = f3 << 1
        #// @var int $f5_2
        f5_2 = f5 << 1
        #// @var int $f7_2
        f7_2 = f7 << 1
        #// @var int $f9_2
        f9_2 = f9 << 1
        f0g0 = self.mul(f0, g0, 26)
        f0g1 = self.mul(f0, g1, 25)
        f0g2 = self.mul(f0, g2, 26)
        f0g3 = self.mul(f0, g3, 25)
        f0g4 = self.mul(f0, g4, 26)
        f0g5 = self.mul(f0, g5, 25)
        f0g6 = self.mul(f0, g6, 26)
        f0g7 = self.mul(f0, g7, 25)
        f0g8 = self.mul(f0, g8, 26)
        f0g9 = self.mul(f0, g9, 26)
        f1g0 = self.mul(f1, g0, 26)
        f1g1_2 = self.mul(f1_2, g1, 25)
        f1g2 = self.mul(f1, g2, 26)
        f1g3_2 = self.mul(f1_2, g3, 25)
        f1g4 = self.mul(f1, g4, 26)
        f1g5_2 = self.mul(f1_2, g5, 25)
        f1g6 = self.mul(f1, g6, 26)
        f1g7_2 = self.mul(f1_2, g7, 25)
        f1g8 = self.mul(f1, g8, 26)
        f1g9_38 = self.mul(g9_19, f1_2, 26)
        f2g0 = self.mul(f2, g0, 26)
        f2g1 = self.mul(f2, g1, 25)
        f2g2 = self.mul(f2, g2, 26)
        f2g3 = self.mul(f2, g3, 25)
        f2g4 = self.mul(f2, g4, 26)
        f2g5 = self.mul(f2, g5, 25)
        f2g6 = self.mul(f2, g6, 26)
        f2g7 = self.mul(f2, g7, 25)
        f2g8_19 = self.mul(g8_19, f2, 26)
        f2g9_19 = self.mul(g9_19, f2, 26)
        f3g0 = self.mul(f3, g0, 26)
        f3g1_2 = self.mul(f3_2, g1, 25)
        f3g2 = self.mul(f3, g2, 26)
        f3g3_2 = self.mul(f3_2, g3, 25)
        f3g4 = self.mul(f3, g4, 26)
        f3g5_2 = self.mul(f3_2, g5, 25)
        f3g6 = self.mul(f3, g6, 26)
        f3g7_38 = self.mul(g7_19, f3_2, 26)
        f3g8_19 = self.mul(g8_19, f3, 25)
        f3g9_38 = self.mul(g9_19, f3_2, 26)
        f4g0 = self.mul(f4, g0, 26)
        f4g1 = self.mul(f4, g1, 25)
        f4g2 = self.mul(f4, g2, 26)
        f4g3 = self.mul(f4, g3, 25)
        f4g4 = self.mul(f4, g4, 26)
        f4g5 = self.mul(f4, g5, 25)
        f4g6_19 = self.mul(g6_19, f4, 26)
        f4g7_19 = self.mul(g7_19, f4, 26)
        f4g8_19 = self.mul(g8_19, f4, 26)
        f4g9_19 = self.mul(g9_19, f4, 26)
        f5g0 = self.mul(f5, g0, 26)
        f5g1_2 = self.mul(f5_2, g1, 25)
        f5g2 = self.mul(f5, g2, 26)
        f5g3_2 = self.mul(f5_2, g3, 25)
        f5g4 = self.mul(f5, g4, 26)
        f5g5_38 = self.mul(g5_19, f5_2, 26)
        f5g6_19 = self.mul(g6_19, f5, 25)
        f5g7_38 = self.mul(g7_19, f5_2, 26)
        f5g8_19 = self.mul(g8_19, f5, 25)
        f5g9_38 = self.mul(g9_19, f5_2, 26)
        f6g0 = self.mul(f6, g0, 26)
        f6g1 = self.mul(f6, g1, 25)
        f6g2 = self.mul(f6, g2, 26)
        f6g3 = self.mul(f6, g3, 25)
        f6g4_19 = self.mul(g4_19, f6, 26)
        f6g5_19 = self.mul(g5_19, f6, 26)
        f6g6_19 = self.mul(g6_19, f6, 26)
        f6g7_19 = self.mul(g7_19, f6, 26)
        f6g8_19 = self.mul(g8_19, f6, 26)
        f6g9_19 = self.mul(g9_19, f6, 26)
        f7g0 = self.mul(f7, g0, 26)
        f7g1_2 = self.mul(f7_2, g1, 25)
        f7g2 = self.mul(f7, g2, 26)
        f7g3_38 = self.mul(g3_19, f7_2, 26)
        f7g4_19 = self.mul(g4_19, f7, 26)
        f7g5_38 = self.mul(g5_19, f7_2, 26)
        f7g6_19 = self.mul(g6_19, f7, 25)
        f7g7_38 = self.mul(g7_19, f7_2, 26)
        f7g8_19 = self.mul(g8_19, f7, 25)
        f7g9_38 = self.mul(g9_19, f7_2, 26)
        f8g0 = self.mul(f8, g0, 26)
        f8g1 = self.mul(f8, g1, 25)
        f8g2_19 = self.mul(g2_19, f8, 26)
        f8g3_19 = self.mul(g3_19, f8, 26)
        f8g4_19 = self.mul(g4_19, f8, 26)
        f8g5_19 = self.mul(g5_19, f8, 26)
        f8g6_19 = self.mul(g6_19, f8, 26)
        f8g7_19 = self.mul(g7_19, f8, 26)
        f8g8_19 = self.mul(g8_19, f8, 26)
        f8g9_19 = self.mul(g9_19, f8, 26)
        f9g0 = self.mul(f9, g0, 26)
        f9g1_38 = self.mul(g1_19, f9_2, 26)
        f9g2_19 = self.mul(g2_19, f9, 25)
        f9g3_38 = self.mul(g3_19, f9_2, 26)
        f9g4_19 = self.mul(g4_19, f9, 25)
        f9g5_38 = self.mul(g5_19, f9_2, 26)
        f9g6_19 = self.mul(g6_19, f9, 25)
        f9g7_38 = self.mul(g7_19, f9_2, 26)
        f9g8_19 = self.mul(g8_19, f9, 25)
        f9g9_38 = self.mul(g9_19, f9_2, 26)
        h0 = f0g0 + f1g9_38 + f2g8_19 + f3g7_38 + f4g6_19 + f5g5_38 + f6g4_19 + f7g3_38 + f8g2_19 + f9g1_38
        h1 = f0g1 + f1g0 + f2g9_19 + f3g8_19 + f4g7_19 + f5g6_19 + f6g5_19 + f7g4_19 + f8g3_19 + f9g2_19
        h2 = f0g2 + f1g1_2 + f2g0 + f3g9_38 + f4g8_19 + f5g7_38 + f6g6_19 + f7g5_38 + f8g4_19 + f9g3_38
        h3 = f0g3 + f1g2 + f2g1 + f3g0 + f4g9_19 + f5g8_19 + f6g7_19 + f7g6_19 + f8g5_19 + f9g4_19
        h4 = f0g4 + f1g3_2 + f2g2 + f3g1_2 + f4g0 + f5g9_38 + f6g8_19 + f7g7_38 + f8g6_19 + f9g5_38
        h5 = f0g5 + f1g4 + f2g3 + f3g2 + f4g1 + f5g0 + f6g9_19 + f7g8_19 + f8g7_19 + f9g6_19
        h6 = f0g6 + f1g5_2 + f2g4 + f3g3_2 + f4g2 + f5g1_2 + f6g0 + f7g9_38 + f8g8_19 + f9g7_38
        h7 = f0g7 + f1g6 + f2g5 + f3g4 + f4g3 + f5g2 + f6g1 + f7g0 + f8g9_19 + f9g8_19
        h8 = f0g8 + f1g7_2 + f2g6 + f3g5_2 + f4g4 + f5g3_2 + f6g2 + f7g1_2 + f8g0 + f9g9_38
        h9 = f0g9 + f1g8 + f2g7 + f3g6 + f4g5 + f5g4 + f6g3 + f7g2 + f8g1 + f9g0
        #// @var int $carry0
        carry0 = h0 + 1 << 25 >> 26
        h1 += carry0
        h0 -= carry0 << 26
        #// @var int $carry4
        carry4 = h4 + 1 << 25 >> 26
        h5 += carry4
        h4 -= carry4 << 26
        #// @var int $carry1
        carry1 = h1 + 1 << 24 >> 25
        h2 += carry1
        h1 -= carry1 << 25
        #// @var int $carry5
        carry5 = h5 + 1 << 24 >> 25
        h6 += carry5
        h5 -= carry5 << 25
        #// @var int $carry2
        carry2 = h2 + 1 << 25 >> 26
        h3 += carry2
        h2 -= carry2 << 26
        #// @var int $carry6
        carry6 = h6 + 1 << 25 >> 26
        h7 += carry6
        h6 -= carry6 << 26
        #// @var int $carry3
        carry3 = h3 + 1 << 24 >> 25
        h4 += carry3
        h3 -= carry3 << 25
        #// @var int $carry7
        carry7 = h7 + 1 << 24 >> 25
        h8 += carry7
        h7 -= carry7 << 25
        #// @var int $carry4
        carry4 = h4 + 1 << 25 >> 26
        h5 += carry4
        h4 -= carry4 << 26
        #// @var int $carry8
        carry8 = h8 + 1 << 25 >> 26
        h9 += carry8
        h8 -= carry8 << 26
        #// @var int $carry9
        carry9 = h9 + 1 << 24 >> 25
        h0 += self.mul(carry9, 19, 5)
        h9 -= carry9 << 25
        #// @var int $carry0
        carry0 = h0 + 1 << 25 >> 26
        h1 += carry0
        h0 -= carry0 << 26
        return ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(Array(php_int(h0), php_int(h1), php_int(h2), php_int(h3), php_int(h4), php_int(h5), php_int(h6), php_int(h7), php_int(h8), php_int(h9)))
    # end def fe_mul
    #// 
    #// Get the negative values for each piece of the field element.
    #// 
    #// h = -f
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $f
    #// @return ParagonIE_Sodium_Core_Curve25519_Fe
    #// @psalm-suppress MixedAssignment
    #//
    @classmethod
    def fe_neg(self, f=None):
        
        h = php_new_class("ParagonIE_Sodium_Core_Curve25519_Fe", lambda : ParagonIE_Sodium_Core_Curve25519_Fe())
        i = 0
        while i < 10:
            
            h[i] = -f[i]
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
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $f
    #// @return ParagonIE_Sodium_Core_Curve25519_Fe
    #//
    @classmethod
    def fe_sq(self, f=None):
        
        f0 = php_int(f[0])
        f1 = php_int(f[1])
        f2 = php_int(f[2])
        f3 = php_int(f[3])
        f4 = php_int(f[4])
        f5 = php_int(f[5])
        f6 = php_int(f[6])
        f7 = php_int(f[7])
        f8 = php_int(f[8])
        f9 = php_int(f[9])
        #// @var int $f0_2
        f0_2 = f0 << 1
        #// @var int $f1_2
        f1_2 = f1 << 1
        #// @var int $f2_2
        f2_2 = f2 << 1
        #// @var int $f3_2
        f3_2 = f3 << 1
        #// @var int $f4_2
        f4_2 = f4 << 1
        #// @var int $f5_2
        f5_2 = f5 << 1
        #// @var int $f6_2
        f6_2 = f6 << 1
        #// @var int $f7_2
        f7_2 = f7 << 1
        f5_38 = self.mul(f5, 38, 6)
        f6_19 = self.mul(f6, 19, 5)
        f7_38 = self.mul(f7, 38, 6)
        f8_19 = self.mul(f8, 19, 5)
        f9_38 = self.mul(f9, 38, 6)
        f0f0 = self.mul(f0, f0, 25)
        f0f1_2 = self.mul(f0_2, f1, 24)
        f0f2_2 = self.mul(f0_2, f2, 25)
        f0f3_2 = self.mul(f0_2, f3, 24)
        f0f4_2 = self.mul(f0_2, f4, 25)
        f0f5_2 = self.mul(f0_2, f5, 25)
        f0f6_2 = self.mul(f0_2, f6, 25)
        f0f7_2 = self.mul(f0_2, f7, 24)
        f0f8_2 = self.mul(f0_2, f8, 25)
        f0f9_2 = self.mul(f0_2, f9, 25)
        f1f1_2 = self.mul(f1_2, f1, 24)
        f1f2_2 = self.mul(f1_2, f2, 25)
        f1f3_4 = self.mul(f1_2, f3_2, 25)
        f1f4_2 = self.mul(f1_2, f4, 25)
        f1f5_4 = self.mul(f1_2, f5_2, 26)
        f1f6_2 = self.mul(f1_2, f6, 25)
        f1f7_4 = self.mul(f1_2, f7_2, 25)
        f1f8_2 = self.mul(f1_2, f8, 25)
        f1f9_76 = self.mul(f9_38, f1_2, 25)
        f2f2 = self.mul(f2, f2, 25)
        f2f3_2 = self.mul(f2_2, f3, 24)
        f2f4_2 = self.mul(f2_2, f4, 25)
        f2f5_2 = self.mul(f2_2, f5, 25)
        f2f6_2 = self.mul(f2_2, f6, 25)
        f2f7_2 = self.mul(f2_2, f7, 24)
        f2f8_38 = self.mul(f8_19, f2_2, 26)
        f2f9_38 = self.mul(f9_38, f2, 25)
        f3f3_2 = self.mul(f3_2, f3, 24)
        f3f4_2 = self.mul(f3_2, f4, 25)
        f3f5_4 = self.mul(f3_2, f5_2, 26)
        f3f6_2 = self.mul(f3_2, f6, 25)
        f3f7_76 = self.mul(f7_38, f3_2, 25)
        f3f8_38 = self.mul(f8_19, f3_2, 25)
        f3f9_76 = self.mul(f9_38, f3_2, 25)
        f4f4 = self.mul(f4, f4, 25)
        f4f5_2 = self.mul(f4_2, f5, 25)
        f4f6_38 = self.mul(f6_19, f4_2, 26)
        f4f7_38 = self.mul(f7_38, f4, 25)
        f4f8_38 = self.mul(f8_19, f4_2, 26)
        f4f9_38 = self.mul(f9_38, f4, 25)
        f5f5_38 = self.mul(f5_38, f5, 25)
        f5f6_38 = self.mul(f6_19, f5_2, 26)
        f5f7_76 = self.mul(f7_38, f5_2, 26)
        f5f8_38 = self.mul(f8_19, f5_2, 26)
        f5f9_76 = self.mul(f9_38, f5_2, 26)
        f6f6_19 = self.mul(f6_19, f6, 25)
        f6f7_38 = self.mul(f7_38, f6, 25)
        f6f8_38 = self.mul(f8_19, f6_2, 26)
        f6f9_38 = self.mul(f9_38, f6, 25)
        f7f7_38 = self.mul(f7_38, f7, 24)
        f7f8_38 = self.mul(f8_19, f7_2, 25)
        f7f9_76 = self.mul(f9_38, f7_2, 25)
        f8f8_19 = self.mul(f8_19, f8, 25)
        f8f9_38 = self.mul(f9_38, f8, 25)
        f9f9_38 = self.mul(f9_38, f9, 25)
        h0 = f0f0 + f1f9_76 + f2f8_38 + f3f7_76 + f4f6_38 + f5f5_38
        h1 = f0f1_2 + f2f9_38 + f3f8_38 + f4f7_38 + f5f6_38
        h2 = f0f2_2 + f1f1_2 + f3f9_76 + f4f8_38 + f5f7_76 + f6f6_19
        h3 = f0f3_2 + f1f2_2 + f4f9_38 + f5f8_38 + f6f7_38
        h4 = f0f4_2 + f1f3_4 + f2f2 + f5f9_76 + f6f8_38 + f7f7_38
        h5 = f0f5_2 + f1f4_2 + f2f3_2 + f6f9_38 + f7f8_38
        h6 = f0f6_2 + f1f5_4 + f2f4_2 + f3f3_2 + f7f9_76 + f8f8_19
        h7 = f0f7_2 + f1f6_2 + f2f5_2 + f3f4_2 + f8f9_38
        h8 = f0f8_2 + f1f7_4 + f2f6_2 + f3f5_4 + f4f4 + f9f9_38
        h9 = f0f9_2 + f1f8_2 + f2f7_2 + f3f6_2 + f4f5_2
        #// @var int $carry0
        carry0 = h0 + 1 << 25 >> 26
        h1 += carry0
        h0 -= carry0 << 26
        #// @var int $carry4
        carry4 = h4 + 1 << 25 >> 26
        h5 += carry4
        h4 -= carry4 << 26
        #// @var int $carry1
        carry1 = h1 + 1 << 24 >> 25
        h2 += carry1
        h1 -= carry1 << 25
        #// @var int $carry5
        carry5 = h5 + 1 << 24 >> 25
        h6 += carry5
        h5 -= carry5 << 25
        #// @var int $carry2
        carry2 = h2 + 1 << 25 >> 26
        h3 += carry2
        h2 -= carry2 << 26
        #// @var int $carry6
        carry6 = h6 + 1 << 25 >> 26
        h7 += carry6
        h6 -= carry6 << 26
        #// @var int $carry3
        carry3 = h3 + 1 << 24 >> 25
        h4 += carry3
        h3 -= carry3 << 25
        #// @var int $carry7
        carry7 = h7 + 1 << 24 >> 25
        h8 += carry7
        h7 -= carry7 << 25
        #// @var int $carry4
        carry4 = h4 + 1 << 25 >> 26
        h5 += carry4
        h4 -= carry4 << 26
        #// @var int $carry8
        carry8 = h8 + 1 << 25 >> 26
        h9 += carry8
        h8 -= carry8 << 26
        #// @var int $carry9
        carry9 = h9 + 1 << 24 >> 25
        h0 += self.mul(carry9, 19, 5)
        h9 -= carry9 << 25
        #// @var int $carry0
        carry0 = h0 + 1 << 25 >> 26
        h1 += carry0
        h0 -= carry0 << 26
        return ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(Array(php_int(h0), php_int(h1), php_int(h2), php_int(h3), php_int(h4), php_int(h5), php_int(h6), php_int(h7), php_int(h8), php_int(h9)))
    # end def fe_sq
    #// 
    #// Square and double a field element
    #// 
    #// h = 2 * f * f
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $f
    #// @return ParagonIE_Sodium_Core_Curve25519_Fe
    #//
    @classmethod
    def fe_sq2(self, f=None):
        
        f0 = php_int(f[0])
        f1 = php_int(f[1])
        f2 = php_int(f[2])
        f3 = php_int(f[3])
        f4 = php_int(f[4])
        f5 = php_int(f[5])
        f6 = php_int(f[6])
        f7 = php_int(f[7])
        f8 = php_int(f[8])
        f9 = php_int(f[9])
        #// @var int $f0_2
        f0_2 = f0 << 1
        #// @var int $f1_2
        f1_2 = f1 << 1
        #// @var int $f2_2
        f2_2 = f2 << 1
        #// @var int $f3_2
        f3_2 = f3 << 1
        #// @var int $f4_2
        f4_2 = f4 << 1
        #// @var int $f5_2
        f5_2 = f5 << 1
        #// @var int $f6_2
        f6_2 = f6 << 1
        #// @var int $f7_2
        f7_2 = f7 << 1
        f5_38 = self.mul(f5, 38, 6)
        #// 1.959375*2^30
        f6_19 = self.mul(f6, 19, 5)
        #// 1.959375*2^30
        f7_38 = self.mul(f7, 38, 6)
        #// 1.959375*2^30
        f8_19 = self.mul(f8, 19, 5)
        #// 1.959375*2^30
        f9_38 = self.mul(f9, 38, 6)
        #// 1.959375*2^30
        f0f0 = self.mul(f0, f0, 24)
        f0f1_2 = self.mul(f0_2, f1, 24)
        f0f2_2 = self.mul(f0_2, f2, 24)
        f0f3_2 = self.mul(f0_2, f3, 24)
        f0f4_2 = self.mul(f0_2, f4, 24)
        f0f5_2 = self.mul(f0_2, f5, 24)
        f0f6_2 = self.mul(f0_2, f6, 24)
        f0f7_2 = self.mul(f0_2, f7, 24)
        f0f8_2 = self.mul(f0_2, f8, 24)
        f0f9_2 = self.mul(f0_2, f9, 24)
        f1f1_2 = self.mul(f1_2, f1, 24)
        f1f2_2 = self.mul(f1_2, f2, 24)
        f1f3_4 = self.mul(f1_2, f3_2, 24)
        f1f4_2 = self.mul(f1_2, f4, 24)
        f1f5_4 = self.mul(f1_2, f5_2, 24)
        f1f6_2 = self.mul(f1_2, f6, 24)
        f1f7_4 = self.mul(f1_2, f7_2, 24)
        f1f8_2 = self.mul(f1_2, f8, 24)
        f1f9_76 = self.mul(f9_38, f1_2, 24)
        f2f2 = self.mul(f2, f2, 24)
        f2f3_2 = self.mul(f2_2, f3, 24)
        f2f4_2 = self.mul(f2_2, f4, 24)
        f2f5_2 = self.mul(f2_2, f5, 24)
        f2f6_2 = self.mul(f2_2, f6, 24)
        f2f7_2 = self.mul(f2_2, f7, 24)
        f2f8_38 = self.mul(f8_19, f2_2, 25)
        f2f9_38 = self.mul(f9_38, f2, 24)
        f3f3_2 = self.mul(f3_2, f3, 24)
        f3f4_2 = self.mul(f3_2, f4, 24)
        f3f5_4 = self.mul(f3_2, f5_2, 24)
        f3f6_2 = self.mul(f3_2, f6, 24)
        f3f7_76 = self.mul(f7_38, f3_2, 24)
        f3f8_38 = self.mul(f8_19, f3_2, 24)
        f3f9_76 = self.mul(f9_38, f3_2, 24)
        f4f4 = self.mul(f4, f4, 24)
        f4f5_2 = self.mul(f4_2, f5, 24)
        f4f6_38 = self.mul(f6_19, f4_2, 25)
        f4f7_38 = self.mul(f7_38, f4, 24)
        f4f8_38 = self.mul(f8_19, f4_2, 25)
        f4f9_38 = self.mul(f9_38, f4, 24)
        f5f5_38 = self.mul(f5_38, f5, 24)
        f5f6_38 = self.mul(f6_19, f5_2, 24)
        f5f7_76 = self.mul(f7_38, f5_2, 24)
        f5f8_38 = self.mul(f8_19, f5_2, 24)
        f5f9_76 = self.mul(f9_38, f5_2, 24)
        f6f6_19 = self.mul(f6_19, f6, 24)
        f6f7_38 = self.mul(f7_38, f6, 24)
        f6f8_38 = self.mul(f8_19, f6_2, 25)
        f6f9_38 = self.mul(f9_38, f6, 24)
        f7f7_38 = self.mul(f7_38, f7, 24)
        f7f8_38 = self.mul(f8_19, f7_2, 24)
        f7f9_76 = self.mul(f9_38, f7_2, 24)
        f8f8_19 = self.mul(f8_19, f8, 24)
        f8f9_38 = self.mul(f9_38, f8, 24)
        f9f9_38 = self.mul(f9_38, f9, 24)
        #// @var int $h0
        h0 = php_int(f0f0 + f1f9_76 + f2f8_38 + f3f7_76 + f4f6_38 + f5f5_38) << 1
        #// @var int $h1
        h1 = php_int(f0f1_2 + f2f9_38 + f3f8_38 + f4f7_38 + f5f6_38) << 1
        #// @var int $h2
        h2 = php_int(f0f2_2 + f1f1_2 + f3f9_76 + f4f8_38 + f5f7_76 + f6f6_19) << 1
        #// @var int $h3
        h3 = php_int(f0f3_2 + f1f2_2 + f4f9_38 + f5f8_38 + f6f7_38) << 1
        #// @var int $h4
        h4 = php_int(f0f4_2 + f1f3_4 + f2f2 + f5f9_76 + f6f8_38 + f7f7_38) << 1
        #// @var int $h5
        h5 = php_int(f0f5_2 + f1f4_2 + f2f3_2 + f6f9_38 + f7f8_38) << 1
        #// @var int $h6
        h6 = php_int(f0f6_2 + f1f5_4 + f2f4_2 + f3f3_2 + f7f9_76 + f8f8_19) << 1
        #// @var int $h7
        h7 = php_int(f0f7_2 + f1f6_2 + f2f5_2 + f3f4_2 + f8f9_38) << 1
        #// @var int $h8
        h8 = php_int(f0f8_2 + f1f7_4 + f2f6_2 + f3f5_4 + f4f4 + f9f9_38) << 1
        #// @var int $h9
        h9 = php_int(f0f9_2 + f1f8_2 + f2f7_2 + f3f6_2 + f4f5_2) << 1
        #// @var int $carry0
        carry0 = h0 + 1 << 25 >> 26
        h1 += carry0
        h0 -= carry0 << 26
        #// @var int $carry4
        carry4 = h4 + 1 << 25 >> 26
        h5 += carry4
        h4 -= carry4 << 26
        #// @var int $carry1
        carry1 = h1 + 1 << 24 >> 25
        h2 += carry1
        h1 -= carry1 << 25
        #// @var int $carry5
        carry5 = h5 + 1 << 24 >> 25
        h6 += carry5
        h5 -= carry5 << 25
        #// @var int $carry2
        carry2 = h2 + 1 << 25 >> 26
        h3 += carry2
        h2 -= carry2 << 26
        #// @var int $carry6
        carry6 = h6 + 1 << 25 >> 26
        h7 += carry6
        h6 -= carry6 << 26
        #// @var int $carry3
        carry3 = h3 + 1 << 24 >> 25
        h4 += carry3
        h3 -= carry3 << 25
        #// @var int $carry7
        carry7 = h7 + 1 << 24 >> 25
        h8 += carry7
        h7 -= carry7 << 25
        #// @var int $carry4
        carry4 = h4 + 1 << 25 >> 26
        h5 += carry4
        h4 -= carry4 << 26
        #// @var int $carry8
        carry8 = h8 + 1 << 25 >> 26
        h9 += carry8
        h8 -= carry8 << 26
        #// @var int $carry9
        carry9 = h9 + 1 << 24 >> 25
        h0 += self.mul(carry9, 19, 5)
        h9 -= carry9 << 25
        #// @var int $carry0
        carry0 = h0 + 1 << 25 >> 26
        h1 += carry0
        h0 -= carry0 << 26
        return ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(Array(php_int(h0), php_int(h1), php_int(h2), php_int(h3), php_int(h4), php_int(h5), php_int(h6), php_int(h7), php_int(h8), php_int(h9)))
    # end def fe_sq2
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $Z
    #// @return ParagonIE_Sodium_Core_Curve25519_Fe
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
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $z
    #// @return ParagonIE_Sodium_Core_Curve25519_Fe
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
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $f
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $g
    #// @return ParagonIE_Sodium_Core_Curve25519_Fe
    #// @psalm-suppress MixedOperand
    #//
    @classmethod
    def fe_sub(self, f=None, g=None):
        
        return ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(Array(php_int(f[0] - g[0]), php_int(f[1] - g[1]), php_int(f[2] - g[2]), php_int(f[3] - g[3]), php_int(f[4] - g[4]), php_int(f[5] - g[5]), php_int(f[6] - g[6]), php_int(f[7] - g[7]), php_int(f[8] - g[8]), php_int(f[9] - g[9])))
    # end def fe_sub
    #// 
    #// Add two group elements.
    #// 
    #// r = p + q
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_P3 $p
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_Cached $q
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_P1p1
    #//
    @classmethod
    def ge_add(self, p=None, q=None):
        
        r = php_new_class("ParagonIE_Sodium_Core_Curve25519_Ge_P1p1", lambda : ParagonIE_Sodium_Core_Curve25519_Ge_P1p1())
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
        #// @var int $i
        i = 0
        while i < 256:
            
            r[i] = php_int(1 & self.chrtoint(a[php_int(i >> 3)]) >> i & 7)
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
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_P3
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def ge_frombytes_negate_vartime(self, s=None):
        
        ge_frombytes_negate_vartime.d = None
        if (not ge_frombytes_negate_vartime.d):
            ge_frombytes_negate_vartime.d = ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(self.ge_frombytes_negate_vartime.d)
        # end if
        #// # fe_frombytes(h->Y,s);
        #// # fe_1(h->Z);
        h = php_new_class("ParagonIE_Sodium_Core_Curve25519_Ge_P3", lambda : ParagonIE_Sodium_Core_Curve25519_Ge_P3(self.fe_0(), self.fe_frombytes(s), self.fe_1()))
        #// # fe_sq(u,h->Y);
        #// # fe_mul(v,u,d);
        #// # fe_sub(u,u,h->Z);       /* u = y^2-1
        #// # fe_add(v,v,h->Z);       /* v = dy^2+1
        u = self.fe_sq(h.Y)
        #// @var ParagonIE_Sodium_Core_Curve25519_Fe $d
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
            h.X = self.fe_mul(h.X, ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(self.sqrtm1))
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
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_P1p1 $R
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_P3 $p
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_Precomp $q
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_P1p1
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
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_P1p1 $R
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_P3 $p
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_Precomp $q
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_P1p1
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
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_P1p1 $p
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_P2
    #//
    @classmethod
    def ge_p1p1_to_p2(self, p=None):
        
        r = php_new_class("ParagonIE_Sodium_Core_Curve25519_Ge_P2", lambda : ParagonIE_Sodium_Core_Curve25519_Ge_P2())
        r.X = self.fe_mul(p.X, p.T)
        r.Y = self.fe_mul(p.Y, p.Z)
        r.Z = self.fe_mul(p.Z, p.T)
        return r
    # end def ge_p1p1_to_p2
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_P1p1 $p
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_P3
    #//
    @classmethod
    def ge_p1p1_to_p3(self, p=None):
        
        r = php_new_class("ParagonIE_Sodium_Core_Curve25519_Ge_P3", lambda : ParagonIE_Sodium_Core_Curve25519_Ge_P3())
        r.X = self.fe_mul(p.X, p.T)
        r.Y = self.fe_mul(p.Y, p.Z)
        r.Z = self.fe_mul(p.Z, p.T)
        r.T = self.fe_mul(p.X, p.Y)
        return r
    # end def ge_p1p1_to_p3
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_P2
    #//
    @classmethod
    def ge_p2_0(self):
        
        return php_new_class("ParagonIE_Sodium_Core_Curve25519_Ge_P2", lambda : ParagonIE_Sodium_Core_Curve25519_Ge_P2(self.fe_0(), self.fe_1(), self.fe_1()))
    # end def ge_p2_0
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_P2 $p
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_P1p1
    #//
    @classmethod
    def ge_p2_dbl(self, p=None):
        
        r = php_new_class("ParagonIE_Sodium_Core_Curve25519_Ge_P1p1", lambda : ParagonIE_Sodium_Core_Curve25519_Ge_P1p1())
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
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_P3
    #//
    @classmethod
    def ge_p3_0(self):
        
        return php_new_class("ParagonIE_Sodium_Core_Curve25519_Ge_P3", lambda : ParagonIE_Sodium_Core_Curve25519_Ge_P3(self.fe_0(), self.fe_1(), self.fe_1(), self.fe_0()))
    # end def ge_p3_0
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_P3 $p
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_Cached
    #//
    @classmethod
    def ge_p3_to_cached(self, p=None):
        
        ge_p3_to_cached.d2 = None
        if ge_p3_to_cached.d2 == None:
            ge_p3_to_cached.d2 = ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(self.ge_p3_to_cached.d2)
        # end if
        #// @var ParagonIE_Sodium_Core_Curve25519_Fe $d2
        r = php_new_class("ParagonIE_Sodium_Core_Curve25519_Ge_Cached", lambda : ParagonIE_Sodium_Core_Curve25519_Ge_Cached())
        r.YplusX = self.fe_add(p.Y, p.X)
        r.YminusX = self.fe_sub(p.Y, p.X)
        r.Z = self.fe_copy(p.Z)
        r.T2d = self.fe_mul(p.T, ge_p3_to_cached.d2)
        return r
    # end def ge_p3_to_cached
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_P3 $p
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_P2
    #//
    @classmethod
    def ge_p3_to_p2(self, p=None):
        
        return php_new_class("ParagonIE_Sodium_Core_Curve25519_Ge_P2", lambda : ParagonIE_Sodium_Core_Curve25519_Ge_P2(p.X, p.Y, p.Z))
    # end def ge_p3_to_p2
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_P3 $h
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
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_P3 $p
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_P1p1
    #//
    @classmethod
    def ge_p3_dbl(self, p=None):
        
        q = self.ge_p3_to_p2(p)
        return self.ge_p2_dbl(q)
    # end def ge_p3_dbl
    #// 
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_Precomp
    #//
    @classmethod
    def ge_precomp_0(self):
        
        return php_new_class("ParagonIE_Sodium_Core_Curve25519_Ge_Precomp", lambda : ParagonIE_Sodium_Core_Curve25519_Ge_Precomp(self.fe_1(), self.fe_1(), self.fe_0()))
    # end def ge_precomp_0
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int $b
    #// @param int $c
    #// @return int
    #//
    @classmethod
    def equal(self, b=None, c=None):
        
        return php_int(b ^ c - 1 & 4294967295 >> 31)
    # end def equal
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int|string $char
    #// @return int (1 = yes, 0 = no)
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def negative(self, char=None):
        
        if php_is_int(char):
            return 1 if char < 0 else 0
        # end if
        x = self.chrtoint(self.substr(char, 0, 1))
        return php_int(x >> 63)
    # end def negative
    #// 
    #// Conditional move
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_Precomp $t
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_Precomp $u
    #// @param int $b
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_Precomp
    #//
    @classmethod
    def cmov(self, t=None, u=None, b=None):
        
        if (not php_is_int(b)):
            raise php_new_class("InvalidArgumentException", lambda : InvalidArgumentException("Expected an integer."))
        # end if
        return php_new_class("ParagonIE_Sodium_Core_Curve25519_Ge_Precomp", lambda : ParagonIE_Sodium_Core_Curve25519_Ge_Precomp(self.fe_cmov(t.yplusx, u.yplusx, b), self.fe_cmov(t.yminusx, u.yminusx, b), self.fe_cmov(t.xy2d, u.xy2d, b)))
    # end def cmov
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int $pos
    #// @param int $b
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_Precomp
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #// @psalm-suppress MixedArrayAccess
    #// @psalm-suppress MixedArrayOffset
    #//
    @classmethod
    def ge_select(self, pos=0, b=0):
        
        ge_select.base = None
        if ge_select.base == None:
            ge_select.base = Array()
            #// @var int $i
            for i,bas in self.ge_select.base:
                j = 0
                while j < 8:
                    
                    ge_select.base[i][j] = php_new_class("ParagonIE_Sodium_Core_Curve25519_Ge_Precomp", lambda : ParagonIE_Sodium_Core_Curve25519_Ge_Precomp(ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(bas[j][0]), ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(bas[j][1]), ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(bas[j][2])))
                    j += 1
                # end while
            # end for
        # end if
        #// @var array<int, array<int, ParagonIE_Sodium_Core_Curve25519_Ge_Precomp>> $base
        if (not php_is_int(pos)):
            raise php_new_class("InvalidArgumentException", lambda : InvalidArgumentException("Position must be an integer"))
        # end if
        if pos < 0 or pos > 31:
            raise php_new_class("RangeException", lambda : RangeException("Position is out of range [0, 31]"))
        # end if
        #// @var int $bnegative
        bnegative = self.negative(b)
        #// @var int $babs
        babs = b - -bnegative & b << 1
        t = self.ge_precomp_0()
        i = 0
        while i < 8:
            
            t = self.cmov(t, ge_select.base[pos][i], self.equal(babs, i + 1))
            i += 1
        # end while
        minusT = php_new_class("ParagonIE_Sodium_Core_Curve25519_Ge_Precomp", lambda : ParagonIE_Sodium_Core_Curve25519_Ge_Precomp(self.fe_copy(t.yminusx), self.fe_copy(t.yplusx), self.fe_neg(t.xy2d)))
        return self.cmov(t, minusT, bnegative)
    # end def ge_select
    #// 
    #// Subtract two group elements.
    #// 
    #// r = p - q
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_P3 $p
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_Cached $q
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_P1p1
    #//
    @classmethod
    def ge_sub(self, p=None, q=None):
        
        r = php_new_class("ParagonIE_Sodium_Core_Curve25519_Ge_P1p1", lambda : ParagonIE_Sodium_Core_Curve25519_Ge_P1p1())
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
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_P2 $h
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
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_P3 $A
    #// @param string $b
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_P2
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #// @psalm-suppress MixedArrayAccess
    #//
    @classmethod
    def ge_double_scalarmult_vartime(self, a=None, A=None, b=None):
        
        #// @var array<int, ParagonIE_Sodium_Core_Curve25519_Ge_Cached> $Ai
        Ai = Array()
        ge_double_scalarmult_vartime.Bi = Array()
        if (not ge_double_scalarmult_vartime.Bi):
            i = 0
            while i < 8:
                
                ge_double_scalarmult_vartime.Bi[i] = php_new_class("ParagonIE_Sodium_Core_Curve25519_Ge_Precomp", lambda : ParagonIE_Sodium_Core_Curve25519_Ge_Precomp(ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(self.base2[i][0]), ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(self.base2[i][1]), ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(self.base2[i][2])))
                i += 1
            # end while
        # end if
        i = 0
        while i < 8:
            
            Ai[i] = php_new_class("ParagonIE_Sodium_Core_Curve25519_Ge_Cached", lambda : ParagonIE_Sodium_Core_Curve25519_Ge_Cached(self.fe_0(), self.fe_0(), self.fe_0(), self.fe_0()))
            i += 1
        # end while
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
            #// # if (bslide[i] > 0) {
            if bslide[i] > 0:
                #// @var int $index
                index = php_int(floor(bslide[i] / 2))
                #// # ge_p1p1_to_p3(&u,&t);
                #// # ge_madd(&t,&u,&Bi[bslide[i]/2]);
                u = self.ge_p1p1_to_p3(t)
                t = self.ge_madd(t, u, ge_double_scalarmult_vartime.Bi[index])
                pass
            elif bslide[i] < 0:
                #// @var int $index
                index = php_int(floor(-bslide[i] / 2))
                #// # ge_p1p1_to_p3(&u,&t);
                #// # ge_msub(&t,&u,&Bi[(-bslide[i])/2]);
                u = self.ge_p1p1_to_p3(t)
                t = self.ge_msub(t, u, ge_double_scalarmult_vartime.Bi[index])
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
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_P3
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedAssignment
    #// @psalm-suppress MixedOperand
    #//
    @classmethod
    def ge_scalarmult_base(self, a=None):
        
        #// @var array<int, int> $e
        e = Array()
        r = php_new_class("ParagonIE_Sodium_Core_Curve25519_Ge_P1p1", lambda : ParagonIE_Sodium_Core_Curve25519_Ge_P1p1())
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
    #// @throws TypeError
    #//
    @classmethod
    def sc_muladd(self, a=None, b=None, c=None):
        
        #// @var int $a0
        a0 = 2097151 & self.load_3(self.substr(a, 0, 3))
        #// @var int $a1
        a1 = 2097151 & self.load_4(self.substr(a, 2, 4)) >> 5
        #// @var int $a2
        a2 = 2097151 & self.load_3(self.substr(a, 5, 3)) >> 2
        #// @var int $a3
        a3 = 2097151 & self.load_4(self.substr(a, 7, 4)) >> 7
        #// @var int $a4
        a4 = 2097151 & self.load_4(self.substr(a, 10, 4)) >> 4
        #// @var int $a5
        a5 = 2097151 & self.load_3(self.substr(a, 13, 3)) >> 1
        #// @var int $a6
        a6 = 2097151 & self.load_4(self.substr(a, 15, 4)) >> 6
        #// @var int $a7
        a7 = 2097151 & self.load_3(self.substr(a, 18, 3)) >> 3
        #// @var int $a8
        a8 = 2097151 & self.load_3(self.substr(a, 21, 3))
        #// @var int $a9
        a9 = 2097151 & self.load_4(self.substr(a, 23, 4)) >> 5
        #// @var int $a10
        a10 = 2097151 & self.load_3(self.substr(a, 26, 3)) >> 2
        #// @var int $a11
        a11 = self.load_4(self.substr(a, 28, 4)) >> 7
        #// @var int $b0
        b0 = 2097151 & self.load_3(self.substr(b, 0, 3))
        #// @var int $b1
        b1 = 2097151 & self.load_4(self.substr(b, 2, 4)) >> 5
        #// @var int $b2
        b2 = 2097151 & self.load_3(self.substr(b, 5, 3)) >> 2
        #// @var int $b3
        b3 = 2097151 & self.load_4(self.substr(b, 7, 4)) >> 7
        #// @var int $b4
        b4 = 2097151 & self.load_4(self.substr(b, 10, 4)) >> 4
        #// @var int $b5
        b5 = 2097151 & self.load_3(self.substr(b, 13, 3)) >> 1
        #// @var int $b6
        b6 = 2097151 & self.load_4(self.substr(b, 15, 4)) >> 6
        #// @var int $b7
        b7 = 2097151 & self.load_3(self.substr(b, 18, 3)) >> 3
        #// @var int $b8
        b8 = 2097151 & self.load_3(self.substr(b, 21, 3))
        #// @var int $b9
        b9 = 2097151 & self.load_4(self.substr(b, 23, 4)) >> 5
        #// @var int $b10
        b10 = 2097151 & self.load_3(self.substr(b, 26, 3)) >> 2
        #// @var int $b11
        b11 = self.load_4(self.substr(b, 28, 4)) >> 7
        #// @var int $c0
        c0 = 2097151 & self.load_3(self.substr(c, 0, 3))
        #// @var int $c1
        c1 = 2097151 & self.load_4(self.substr(c, 2, 4)) >> 5
        #// @var int $c2
        c2 = 2097151 & self.load_3(self.substr(c, 5, 3)) >> 2
        #// @var int $c3
        c3 = 2097151 & self.load_4(self.substr(c, 7, 4)) >> 7
        #// @var int $c4
        c4 = 2097151 & self.load_4(self.substr(c, 10, 4)) >> 4
        #// @var int $c5
        c5 = 2097151 & self.load_3(self.substr(c, 13, 3)) >> 1
        #// @var int $c6
        c6 = 2097151 & self.load_4(self.substr(c, 15, 4)) >> 6
        #// @var int $c7
        c7 = 2097151 & self.load_3(self.substr(c, 18, 3)) >> 3
        #// @var int $c8
        c8 = 2097151 & self.load_3(self.substr(c, 21, 3))
        #// @var int $c9
        c9 = 2097151 & self.load_4(self.substr(c, 23, 4)) >> 5
        #// @var int $c10
        c10 = 2097151 & self.load_3(self.substr(c, 26, 3)) >> 2
        #// @var int $c11
        c11 = self.load_4(self.substr(c, 28, 4)) >> 7
        #// Can't really avoid the pyramid here:
        s0 = c0 + self.mul(a0, b0, 24)
        s1 = c1 + self.mul(a0, b1, 24) + self.mul(a1, b0, 24)
        s2 = c2 + self.mul(a0, b2, 24) + self.mul(a1, b1, 24) + self.mul(a2, b0, 24)
        s3 = c3 + self.mul(a0, b3, 24) + self.mul(a1, b2, 24) + self.mul(a2, b1, 24) + self.mul(a3, b0, 24)
        s4 = c4 + self.mul(a0, b4, 24) + self.mul(a1, b3, 24) + self.mul(a2, b2, 24) + self.mul(a3, b1, 24) + self.mul(a4, b0, 24)
        s5 = c5 + self.mul(a0, b5, 24) + self.mul(a1, b4, 24) + self.mul(a2, b3, 24) + self.mul(a3, b2, 24) + self.mul(a4, b1, 24) + self.mul(a5, b0, 24)
        s6 = c6 + self.mul(a0, b6, 24) + self.mul(a1, b5, 24) + self.mul(a2, b4, 24) + self.mul(a3, b3, 24) + self.mul(a4, b2, 24) + self.mul(a5, b1, 24) + self.mul(a6, b0, 24)
        s7 = c7 + self.mul(a0, b7, 24) + self.mul(a1, b6, 24) + self.mul(a2, b5, 24) + self.mul(a3, b4, 24) + self.mul(a4, b3, 24) + self.mul(a5, b2, 24) + self.mul(a6, b1, 24) + self.mul(a7, b0, 24)
        s8 = c8 + self.mul(a0, b8, 24) + self.mul(a1, b7, 24) + self.mul(a2, b6, 24) + self.mul(a3, b5, 24) + self.mul(a4, b4, 24) + self.mul(a5, b3, 24) + self.mul(a6, b2, 24) + self.mul(a7, b1, 24) + self.mul(a8, b0, 24)
        s9 = c9 + self.mul(a0, b9, 24) + self.mul(a1, b8, 24) + self.mul(a2, b7, 24) + self.mul(a3, b6, 24) + self.mul(a4, b5, 24) + self.mul(a5, b4, 24) + self.mul(a6, b3, 24) + self.mul(a7, b2, 24) + self.mul(a8, b1, 24) + self.mul(a9, b0, 24)
        s10 = c10 + self.mul(a0, b10, 24) + self.mul(a1, b9, 24) + self.mul(a2, b8, 24) + self.mul(a3, b7, 24) + self.mul(a4, b6, 24) + self.mul(a5, b5, 24) + self.mul(a6, b4, 24) + self.mul(a7, b3, 24) + self.mul(a8, b2, 24) + self.mul(a9, b1, 24) + self.mul(a10, b0, 24)
        s11 = c11 + self.mul(a0, b11, 24) + self.mul(a1, b10, 24) + self.mul(a2, b9, 24) + self.mul(a3, b8, 24) + self.mul(a4, b7, 24) + self.mul(a5, b6, 24) + self.mul(a6, b5, 24) + self.mul(a7, b4, 24) + self.mul(a8, b3, 24) + self.mul(a9, b2, 24) + self.mul(a10, b1, 24) + self.mul(a11, b0, 24)
        s12 = self.mul(a1, b11, 24) + self.mul(a2, b10, 24) + self.mul(a3, b9, 24) + self.mul(a4, b8, 24) + self.mul(a5, b7, 24) + self.mul(a6, b6, 24) + self.mul(a7, b5, 24) + self.mul(a8, b4, 24) + self.mul(a9, b3, 24) + self.mul(a10, b2, 24) + self.mul(a11, b1, 24)
        s13 = self.mul(a2, b11, 24) + self.mul(a3, b10, 24) + self.mul(a4, b9, 24) + self.mul(a5, b8, 24) + self.mul(a6, b7, 24) + self.mul(a7, b6, 24) + self.mul(a8, b5, 24) + self.mul(a9, b4, 24) + self.mul(a10, b3, 24) + self.mul(a11, b2, 24)
        s14 = self.mul(a3, b11, 24) + self.mul(a4, b10, 24) + self.mul(a5, b9, 24) + self.mul(a6, b8, 24) + self.mul(a7, b7, 24) + self.mul(a8, b6, 24) + self.mul(a9, b5, 24) + self.mul(a10, b4, 24) + self.mul(a11, b3, 24)
        s15 = self.mul(a4, b11, 24) + self.mul(a5, b10, 24) + self.mul(a6, b9, 24) + self.mul(a7, b8, 24) + self.mul(a8, b7, 24) + self.mul(a9, b6, 24) + self.mul(a10, b5, 24) + self.mul(a11, b4, 24)
        s16 = self.mul(a5, b11, 24) + self.mul(a6, b10, 24) + self.mul(a7, b9, 24) + self.mul(a8, b8, 24) + self.mul(a9, b7, 24) + self.mul(a10, b6, 24) + self.mul(a11, b5, 24)
        s17 = self.mul(a6, b11, 24) + self.mul(a7, b10, 24) + self.mul(a8, b9, 24) + self.mul(a9, b8, 24) + self.mul(a10, b7, 24) + self.mul(a11, b6, 24)
        s18 = self.mul(a7, b11, 24) + self.mul(a8, b10, 24) + self.mul(a9, b9, 24) + self.mul(a10, b8, 24) + self.mul(a11, b7, 24)
        s19 = self.mul(a8, b11, 24) + self.mul(a9, b10, 24) + self.mul(a10, b9, 24) + self.mul(a11, b8, 24)
        s20 = self.mul(a9, b11, 24) + self.mul(a10, b10, 24) + self.mul(a11, b9, 24)
        s21 = self.mul(a10, b11, 24) + self.mul(a11, b10, 24)
        s22 = self.mul(a11, b11, 24)
        s23 = 0
        #// @var int $carry0
        carry0 = s0 + 1 << 20 >> 21
        s1 += carry0
        s0 -= carry0 << 21
        #// @var int $carry2
        carry2 = s2 + 1 << 20 >> 21
        s3 += carry2
        s2 -= carry2 << 21
        #// @var int $carry4
        carry4 = s4 + 1 << 20 >> 21
        s5 += carry4
        s4 -= carry4 << 21
        #// @var int $carry6
        carry6 = s6 + 1 << 20 >> 21
        s7 += carry6
        s6 -= carry6 << 21
        #// @var int $carry8
        carry8 = s8 + 1 << 20 >> 21
        s9 += carry8
        s8 -= carry8 << 21
        #// @var int $carry10
        carry10 = s10 + 1 << 20 >> 21
        s11 += carry10
        s10 -= carry10 << 21
        #// @var int $carry12
        carry12 = s12 + 1 << 20 >> 21
        s13 += carry12
        s12 -= carry12 << 21
        #// @var int $carry14
        carry14 = s14 + 1 << 20 >> 21
        s15 += carry14
        s14 -= carry14 << 21
        #// @var int $carry16
        carry16 = s16 + 1 << 20 >> 21
        s17 += carry16
        s16 -= carry16 << 21
        #// @var int $carry18
        carry18 = s18 + 1 << 20 >> 21
        s19 += carry18
        s18 -= carry18 << 21
        #// @var int $carry20
        carry20 = s20 + 1 << 20 >> 21
        s21 += carry20
        s20 -= carry20 << 21
        #// @var int $carry22
        carry22 = s22 + 1 << 20 >> 21
        s23 += carry22
        s22 -= carry22 << 21
        #// @var int $carry1
        carry1 = s1 + 1 << 20 >> 21
        s2 += carry1
        s1 -= carry1 << 21
        #// @var int $carry3
        carry3 = s3 + 1 << 20 >> 21
        s4 += carry3
        s3 -= carry3 << 21
        #// @var int $carry5
        carry5 = s5 + 1 << 20 >> 21
        s6 += carry5
        s5 -= carry5 << 21
        #// @var int $carry7
        carry7 = s7 + 1 << 20 >> 21
        s8 += carry7
        s7 -= carry7 << 21
        #// @var int $carry9
        carry9 = s9 + 1 << 20 >> 21
        s10 += carry9
        s9 -= carry9 << 21
        #// @var int $carry11
        carry11 = s11 + 1 << 20 >> 21
        s12 += carry11
        s11 -= carry11 << 21
        #// @var int $carry13
        carry13 = s13 + 1 << 20 >> 21
        s14 += carry13
        s13 -= carry13 << 21
        #// @var int $carry15
        carry15 = s15 + 1 << 20 >> 21
        s16 += carry15
        s15 -= carry15 << 21
        #// @var int $carry17
        carry17 = s17 + 1 << 20 >> 21
        s18 += carry17
        s17 -= carry17 << 21
        #// @var int $carry19
        carry19 = s19 + 1 << 20 >> 21
        s20 += carry19
        s19 -= carry19 << 21
        #// @var int $carry21
        carry21 = s21 + 1 << 20 >> 21
        s22 += carry21
        s21 -= carry21 << 21
        s11 += self.mul(s23, 666643, 20)
        s12 += self.mul(s23, 470296, 19)
        s13 += self.mul(s23, 654183, 20)
        s14 -= self.mul(s23, 997805, 20)
        s15 += self.mul(s23, 136657, 18)
        s16 -= self.mul(s23, 683901, 20)
        s10 += self.mul(s22, 666643, 20)
        s11 += self.mul(s22, 470296, 19)
        s12 += self.mul(s22, 654183, 20)
        s13 -= self.mul(s22, 997805, 20)
        s14 += self.mul(s22, 136657, 18)
        s15 -= self.mul(s22, 683901, 20)
        s9 += self.mul(s21, 666643, 20)
        s10 += self.mul(s21, 470296, 19)
        s11 += self.mul(s21, 654183, 20)
        s12 -= self.mul(s21, 997805, 20)
        s13 += self.mul(s21, 136657, 18)
        s14 -= self.mul(s21, 683901, 20)
        s8 += self.mul(s20, 666643, 20)
        s9 += self.mul(s20, 470296, 19)
        s10 += self.mul(s20, 654183, 20)
        s11 -= self.mul(s20, 997805, 20)
        s12 += self.mul(s20, 136657, 18)
        s13 -= self.mul(s20, 683901, 20)
        s7 += self.mul(s19, 666643, 20)
        s8 += self.mul(s19, 470296, 19)
        s9 += self.mul(s19, 654183, 20)
        s10 -= self.mul(s19, 997805, 20)
        s11 += self.mul(s19, 136657, 18)
        s12 -= self.mul(s19, 683901, 20)
        s6 += self.mul(s18, 666643, 20)
        s7 += self.mul(s18, 470296, 19)
        s8 += self.mul(s18, 654183, 20)
        s9 -= self.mul(s18, 997805, 20)
        s10 += self.mul(s18, 136657, 18)
        s11 -= self.mul(s18, 683901, 20)
        #// @var int $carry6
        carry6 = s6 + 1 << 20 >> 21
        s7 += carry6
        s6 -= carry6 << 21
        #// @var int $carry8
        carry8 = s8 + 1 << 20 >> 21
        s9 += carry8
        s8 -= carry8 << 21
        #// @var int $carry10
        carry10 = s10 + 1 << 20 >> 21
        s11 += carry10
        s10 -= carry10 << 21
        #// @var int $carry12
        carry12 = s12 + 1 << 20 >> 21
        s13 += carry12
        s12 -= carry12 << 21
        #// @var int $carry14
        carry14 = s14 + 1 << 20 >> 21
        s15 += carry14
        s14 -= carry14 << 21
        #// @var int $carry16
        carry16 = s16 + 1 << 20 >> 21
        s17 += carry16
        s16 -= carry16 << 21
        #// @var int $carry7
        carry7 = s7 + 1 << 20 >> 21
        s8 += carry7
        s7 -= carry7 << 21
        #// @var int $carry9
        carry9 = s9 + 1 << 20 >> 21
        s10 += carry9
        s9 -= carry9 << 21
        #// @var int $carry11
        carry11 = s11 + 1 << 20 >> 21
        s12 += carry11
        s11 -= carry11 << 21
        #// @var int $carry13
        carry13 = s13 + 1 << 20 >> 21
        s14 += carry13
        s13 -= carry13 << 21
        #// @var int $carry15
        carry15 = s15 + 1 << 20 >> 21
        s16 += carry15
        s15 -= carry15 << 21
        s5 += self.mul(s17, 666643, 20)
        s6 += self.mul(s17, 470296, 19)
        s7 += self.mul(s17, 654183, 20)
        s8 -= self.mul(s17, 997805, 20)
        s9 += self.mul(s17, 136657, 18)
        s10 -= self.mul(s17, 683901, 20)
        s4 += self.mul(s16, 666643, 20)
        s5 += self.mul(s16, 470296, 19)
        s6 += self.mul(s16, 654183, 20)
        s7 -= self.mul(s16, 997805, 20)
        s8 += self.mul(s16, 136657, 18)
        s9 -= self.mul(s16, 683901, 20)
        s3 += self.mul(s15, 666643, 20)
        s4 += self.mul(s15, 470296, 19)
        s5 += self.mul(s15, 654183, 20)
        s6 -= self.mul(s15, 997805, 20)
        s7 += self.mul(s15, 136657, 18)
        s8 -= self.mul(s15, 683901, 20)
        s2 += self.mul(s14, 666643, 20)
        s3 += self.mul(s14, 470296, 19)
        s4 += self.mul(s14, 654183, 20)
        s5 -= self.mul(s14, 997805, 20)
        s6 += self.mul(s14, 136657, 18)
        s7 -= self.mul(s14, 683901, 20)
        s1 += self.mul(s13, 666643, 20)
        s2 += self.mul(s13, 470296, 19)
        s3 += self.mul(s13, 654183, 20)
        s4 -= self.mul(s13, 997805, 20)
        s5 += self.mul(s13, 136657, 18)
        s6 -= self.mul(s13, 683901, 20)
        s0 += self.mul(s12, 666643, 20)
        s1 += self.mul(s12, 470296, 19)
        s2 += self.mul(s12, 654183, 20)
        s3 -= self.mul(s12, 997805, 20)
        s4 += self.mul(s12, 136657, 18)
        s5 -= self.mul(s12, 683901, 20)
        s12 = 0
        #// @var int $carry0
        carry0 = s0 + 1 << 20 >> 21
        s1 += carry0
        s0 -= carry0 << 21
        #// @var int $carry2
        carry2 = s2 + 1 << 20 >> 21
        s3 += carry2
        s2 -= carry2 << 21
        #// @var int $carry4
        carry4 = s4 + 1 << 20 >> 21
        s5 += carry4
        s4 -= carry4 << 21
        #// @var int $carry6
        carry6 = s6 + 1 << 20 >> 21
        s7 += carry6
        s6 -= carry6 << 21
        #// @var int $carry8
        carry8 = s8 + 1 << 20 >> 21
        s9 += carry8
        s8 -= carry8 << 21
        #// @var int $carry10
        carry10 = s10 + 1 << 20 >> 21
        s11 += carry10
        s10 -= carry10 << 21
        #// @var int $carry1
        carry1 = s1 + 1 << 20 >> 21
        s2 += carry1
        s1 -= carry1 << 21
        #// @var int $carry3
        carry3 = s3 + 1 << 20 >> 21
        s4 += carry3
        s3 -= carry3 << 21
        #// @var int $carry5
        carry5 = s5 + 1 << 20 >> 21
        s6 += carry5
        s5 -= carry5 << 21
        #// @var int $carry7
        carry7 = s7 + 1 << 20 >> 21
        s8 += carry7
        s7 -= carry7 << 21
        #// @var int $carry9
        carry9 = s9 + 1 << 20 >> 21
        s10 += carry9
        s9 -= carry9 << 21
        #// @var int $carry11
        carry11 = s11 + 1 << 20 >> 21
        s12 += carry11
        s11 -= carry11 << 21
        s0 += self.mul(s12, 666643, 20)
        s1 += self.mul(s12, 470296, 19)
        s2 += self.mul(s12, 654183, 20)
        s3 -= self.mul(s12, 997805, 20)
        s4 += self.mul(s12, 136657, 18)
        s5 -= self.mul(s12, 683901, 20)
        s12 = 0
        #// @var int $carry0
        carry0 = s0 >> 21
        s1 += carry0
        s0 -= carry0 << 21
        #// @var int $carry1
        carry1 = s1 >> 21
        s2 += carry1
        s1 -= carry1 << 21
        #// @var int $carry2
        carry2 = s2 >> 21
        s3 += carry2
        s2 -= carry2 << 21
        #// @var int $carry3
        carry3 = s3 >> 21
        s4 += carry3
        s3 -= carry3 << 21
        #// @var int $carry4
        carry4 = s4 >> 21
        s5 += carry4
        s4 -= carry4 << 21
        #// @var int $carry5
        carry5 = s5 >> 21
        s6 += carry5
        s5 -= carry5 << 21
        #// @var int $carry6
        carry6 = s6 >> 21
        s7 += carry6
        s6 -= carry6 << 21
        #// @var int $carry7
        carry7 = s7 >> 21
        s8 += carry7
        s7 -= carry7 << 21
        #// @var int $carry8
        carry8 = s8 >> 21
        s9 += carry8
        s8 -= carry8 << 21
        #// @var int $carry9
        carry9 = s9 >> 21
        s10 += carry9
        s9 -= carry9 << 21
        #// @var int $carry10
        carry10 = s10 >> 21
        s11 += carry10
        s10 -= carry10 << 21
        #// @var int $carry11
        carry11 = s11 >> 21
        s12 += carry11
        s11 -= carry11 << 21
        s0 += self.mul(s12, 666643, 20)
        s1 += self.mul(s12, 470296, 19)
        s2 += self.mul(s12, 654183, 20)
        s3 -= self.mul(s12, 997805, 20)
        s4 += self.mul(s12, 136657, 18)
        s5 -= self.mul(s12, 683901, 20)
        #// @var int $carry0
        carry0 = s0 >> 21
        s1 += carry0
        s0 -= carry0 << 21
        #// @var int $carry1
        carry1 = s1 >> 21
        s2 += carry1
        s1 -= carry1 << 21
        #// @var int $carry2
        carry2 = s2 >> 21
        s3 += carry2
        s2 -= carry2 << 21
        #// @var int $carry3
        carry3 = s3 >> 21
        s4 += carry3
        s3 -= carry3 << 21
        #// @var int $carry4
        carry4 = s4 >> 21
        s5 += carry4
        s4 -= carry4 << 21
        #// @var int $carry5
        carry5 = s5 >> 21
        s6 += carry5
        s5 -= carry5 << 21
        #// @var int $carry6
        carry6 = s6 >> 21
        s7 += carry6
        s6 -= carry6 << 21
        #// @var int $carry7
        carry7 = s7 >> 21
        s8 += carry7
        s7 -= carry7 << 21
        #// @var int $carry8
        carry8 = s8 >> 21
        s9 += carry8
        s8 -= carry8 << 21
        #// @var int $carry9
        carry9 = s9 >> 21
        s10 += carry9
        s9 -= carry9 << 21
        #// @var int $carry10
        carry10 = s10 >> 21
        s11 += carry10
        s10 -= carry10 << 21
        #// 
        #// @var array<int, int>
        #//
        arr = Array(php_int(255 & s0 >> 0), php_int(255 & s0 >> 8), php_int(255 & s0 >> 16 | s1 << 5), php_int(255 & s1 >> 3), php_int(255 & s1 >> 11), php_int(255 & s1 >> 19 | s2 << 2), php_int(255 & s2 >> 6), php_int(255 & s2 >> 14 | s3 << 7), php_int(255 & s3 >> 1), php_int(255 & s3 >> 9), php_int(255 & s3 >> 17 | s4 << 4), php_int(255 & s4 >> 4), php_int(255 & s4 >> 12), php_int(255 & s4 >> 20 | s5 << 1), php_int(255 & s5 >> 7), php_int(255 & s5 >> 15 | s6 << 6), php_int(255 & s6 >> 2), php_int(255 & s6 >> 10), php_int(255 & s6 >> 18 | s7 << 3), php_int(255 & s7 >> 5), php_int(255 & s7 >> 13), php_int(255 & s8 >> 0), php_int(255 & s8 >> 8), php_int(255 & s8 >> 16 | s9 << 5), php_int(255 & s9 >> 3), php_int(255 & s9 >> 11), php_int(255 & s9 >> 19 | s10 << 2), php_int(255 & s10 >> 6), php_int(255 & s10 >> 14 | s11 << 7), php_int(255 & s11 >> 1), php_int(255 & s11 >> 9), 255 & s11 >> 17)
        return self.intarraytostring(arr)
    # end def sc_muladd
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $s
    #// @return string
    #// @throws TypeError
    #//
    @classmethod
    def sc_reduce(self, s=None):
        
        #// @var int $s0
        s0 = 2097151 & self.load_3(self.substr(s, 0, 3))
        #// @var int $s1
        s1 = 2097151 & self.load_4(self.substr(s, 2, 4)) >> 5
        #// @var int $s2
        s2 = 2097151 & self.load_3(self.substr(s, 5, 3)) >> 2
        #// @var int $s3
        s3 = 2097151 & self.load_4(self.substr(s, 7, 4)) >> 7
        #// @var int $s4
        s4 = 2097151 & self.load_4(self.substr(s, 10, 4)) >> 4
        #// @var int $s5
        s5 = 2097151 & self.load_3(self.substr(s, 13, 3)) >> 1
        #// @var int $s6
        s6 = 2097151 & self.load_4(self.substr(s, 15, 4)) >> 6
        #// @var int $s7
        s7 = 2097151 & self.load_3(self.substr(s, 18, 4)) >> 3
        #// @var int $s8
        s8 = 2097151 & self.load_3(self.substr(s, 21, 3))
        #// @var int $s9
        s9 = 2097151 & self.load_4(self.substr(s, 23, 4)) >> 5
        #// @var int $s10
        s10 = 2097151 & self.load_3(self.substr(s, 26, 3)) >> 2
        #// @var int $s11
        s11 = 2097151 & self.load_4(self.substr(s, 28, 4)) >> 7
        #// @var int $s12
        s12 = 2097151 & self.load_4(self.substr(s, 31, 4)) >> 4
        #// @var int $s13
        s13 = 2097151 & self.load_3(self.substr(s, 34, 3)) >> 1
        #// @var int $s14
        s14 = 2097151 & self.load_4(self.substr(s, 36, 4)) >> 6
        #// @var int $s15
        s15 = 2097151 & self.load_3(self.substr(s, 39, 4)) >> 3
        #// @var int $s16
        s16 = 2097151 & self.load_3(self.substr(s, 42, 3))
        #// @var int $s17
        s17 = 2097151 & self.load_4(self.substr(s, 44, 4)) >> 5
        #// @var int $s18
        s18 = 2097151 & self.load_3(self.substr(s, 47, 3)) >> 2
        #// @var int $s19
        s19 = 2097151 & self.load_4(self.substr(s, 49, 4)) >> 7
        #// @var int $s20
        s20 = 2097151 & self.load_4(self.substr(s, 52, 4)) >> 4
        #// @var int $s21
        s21 = 2097151 & self.load_3(self.substr(s, 55, 3)) >> 1
        #// @var int $s22
        s22 = 2097151 & self.load_4(self.substr(s, 57, 4)) >> 6
        #// @var int $s23
        s23 = self.load_4(self.substr(s, 60, 4)) >> 3
        s11 += self.mul(s23, 666643, 20)
        s12 += self.mul(s23, 470296, 19)
        s13 += self.mul(s23, 654183, 20)
        s14 -= self.mul(s23, 997805, 20)
        s15 += self.mul(s23, 136657, 18)
        s16 -= self.mul(s23, 683901, 20)
        s10 += self.mul(s22, 666643, 20)
        s11 += self.mul(s22, 470296, 19)
        s12 += self.mul(s22, 654183, 20)
        s13 -= self.mul(s22, 997805, 20)
        s14 += self.mul(s22, 136657, 18)
        s15 -= self.mul(s22, 683901, 20)
        s9 += self.mul(s21, 666643, 20)
        s10 += self.mul(s21, 470296, 19)
        s11 += self.mul(s21, 654183, 20)
        s12 -= self.mul(s21, 997805, 20)
        s13 += self.mul(s21, 136657, 18)
        s14 -= self.mul(s21, 683901, 20)
        s8 += self.mul(s20, 666643, 20)
        s9 += self.mul(s20, 470296, 19)
        s10 += self.mul(s20, 654183, 20)
        s11 -= self.mul(s20, 997805, 20)
        s12 += self.mul(s20, 136657, 18)
        s13 -= self.mul(s20, 683901, 20)
        s7 += self.mul(s19, 666643, 20)
        s8 += self.mul(s19, 470296, 19)
        s9 += self.mul(s19, 654183, 20)
        s10 -= self.mul(s19, 997805, 20)
        s11 += self.mul(s19, 136657, 18)
        s12 -= self.mul(s19, 683901, 20)
        s6 += self.mul(s18, 666643, 20)
        s7 += self.mul(s18, 470296, 19)
        s8 += self.mul(s18, 654183, 20)
        s9 -= self.mul(s18, 997805, 20)
        s10 += self.mul(s18, 136657, 18)
        s11 -= self.mul(s18, 683901, 20)
        #// @var int $carry6
        carry6 = s6 + 1 << 20 >> 21
        s7 += carry6
        s6 -= carry6 << 21
        #// @var int $carry8
        carry8 = s8 + 1 << 20 >> 21
        s9 += carry8
        s8 -= carry8 << 21
        #// @var int $carry10
        carry10 = s10 + 1 << 20 >> 21
        s11 += carry10
        s10 -= carry10 << 21
        #// @var int $carry12
        carry12 = s12 + 1 << 20 >> 21
        s13 += carry12
        s12 -= carry12 << 21
        #// @var int $carry14
        carry14 = s14 + 1 << 20 >> 21
        s15 += carry14
        s14 -= carry14 << 21
        #// @var int $carry16
        carry16 = s16 + 1 << 20 >> 21
        s17 += carry16
        s16 -= carry16 << 21
        #// @var int $carry7
        carry7 = s7 + 1 << 20 >> 21
        s8 += carry7
        s7 -= carry7 << 21
        #// @var int $carry9
        carry9 = s9 + 1 << 20 >> 21
        s10 += carry9
        s9 -= carry9 << 21
        #// @var int $carry11
        carry11 = s11 + 1 << 20 >> 21
        s12 += carry11
        s11 -= carry11 << 21
        #// @var int $carry13
        carry13 = s13 + 1 << 20 >> 21
        s14 += carry13
        s13 -= carry13 << 21
        #// @var int $carry15
        carry15 = s15 + 1 << 20 >> 21
        s16 += carry15
        s15 -= carry15 << 21
        s5 += self.mul(s17, 666643, 20)
        s6 += self.mul(s17, 470296, 19)
        s7 += self.mul(s17, 654183, 20)
        s8 -= self.mul(s17, 997805, 20)
        s9 += self.mul(s17, 136657, 18)
        s10 -= self.mul(s17, 683901, 20)
        s4 += self.mul(s16, 666643, 20)
        s5 += self.mul(s16, 470296, 19)
        s6 += self.mul(s16, 654183, 20)
        s7 -= self.mul(s16, 997805, 20)
        s8 += self.mul(s16, 136657, 18)
        s9 -= self.mul(s16, 683901, 20)
        s3 += self.mul(s15, 666643, 20)
        s4 += self.mul(s15, 470296, 19)
        s5 += self.mul(s15, 654183, 20)
        s6 -= self.mul(s15, 997805, 20)
        s7 += self.mul(s15, 136657, 18)
        s8 -= self.mul(s15, 683901, 20)
        s2 += self.mul(s14, 666643, 20)
        s3 += self.mul(s14, 470296, 19)
        s4 += self.mul(s14, 654183, 20)
        s5 -= self.mul(s14, 997805, 20)
        s6 += self.mul(s14, 136657, 18)
        s7 -= self.mul(s14, 683901, 20)
        s1 += self.mul(s13, 666643, 20)
        s2 += self.mul(s13, 470296, 19)
        s3 += self.mul(s13, 654183, 20)
        s4 -= self.mul(s13, 997805, 20)
        s5 += self.mul(s13, 136657, 18)
        s6 -= self.mul(s13, 683901, 20)
        s0 += self.mul(s12, 666643, 20)
        s1 += self.mul(s12, 470296, 19)
        s2 += self.mul(s12, 654183, 20)
        s3 -= self.mul(s12, 997805, 20)
        s4 += self.mul(s12, 136657, 18)
        s5 -= self.mul(s12, 683901, 20)
        s12 = 0
        #// @var int $carry0
        carry0 = s0 + 1 << 20 >> 21
        s1 += carry0
        s0 -= carry0 << 21
        #// @var int $carry2
        carry2 = s2 + 1 << 20 >> 21
        s3 += carry2
        s2 -= carry2 << 21
        #// @var int $carry4
        carry4 = s4 + 1 << 20 >> 21
        s5 += carry4
        s4 -= carry4 << 21
        #// @var int $carry6
        carry6 = s6 + 1 << 20 >> 21
        s7 += carry6
        s6 -= carry6 << 21
        #// @var int $carry8
        carry8 = s8 + 1 << 20 >> 21
        s9 += carry8
        s8 -= carry8 << 21
        #// @var int $carry10
        carry10 = s10 + 1 << 20 >> 21
        s11 += carry10
        s10 -= carry10 << 21
        #// @var int $carry1
        carry1 = s1 + 1 << 20 >> 21
        s2 += carry1
        s1 -= carry1 << 21
        #// @var int $carry3
        carry3 = s3 + 1 << 20 >> 21
        s4 += carry3
        s3 -= carry3 << 21
        #// @var int $carry5
        carry5 = s5 + 1 << 20 >> 21
        s6 += carry5
        s5 -= carry5 << 21
        #// @var int $carry7
        carry7 = s7 + 1 << 20 >> 21
        s8 += carry7
        s7 -= carry7 << 21
        #// @var int $carry9
        carry9 = s9 + 1 << 20 >> 21
        s10 += carry9
        s9 -= carry9 << 21
        #// @var int $carry11
        carry11 = s11 + 1 << 20 >> 21
        s12 += carry11
        s11 -= carry11 << 21
        s0 += self.mul(s12, 666643, 20)
        s1 += self.mul(s12, 470296, 19)
        s2 += self.mul(s12, 654183, 20)
        s3 -= self.mul(s12, 997805, 20)
        s4 += self.mul(s12, 136657, 18)
        s5 -= self.mul(s12, 683901, 20)
        s12 = 0
        #// @var int $carry0
        carry0 = s0 >> 21
        s1 += carry0
        s0 -= carry0 << 21
        #// @var int $carry1
        carry1 = s1 >> 21
        s2 += carry1
        s1 -= carry1 << 21
        #// @var int $carry2
        carry2 = s2 >> 21
        s3 += carry2
        s2 -= carry2 << 21
        #// @var int $carry3
        carry3 = s3 >> 21
        s4 += carry3
        s3 -= carry3 << 21
        #// @var int $carry4
        carry4 = s4 >> 21
        s5 += carry4
        s4 -= carry4 << 21
        #// @var int $carry5
        carry5 = s5 >> 21
        s6 += carry5
        s5 -= carry5 << 21
        #// @var int $carry6
        carry6 = s6 >> 21
        s7 += carry6
        s6 -= carry6 << 21
        #// @var int $carry7
        carry7 = s7 >> 21
        s8 += carry7
        s7 -= carry7 << 21
        #// @var int $carry8
        carry8 = s8 >> 21
        s9 += carry8
        s8 -= carry8 << 21
        #// @var int $carry9
        carry9 = s9 >> 21
        s10 += carry9
        s9 -= carry9 << 21
        #// @var int $carry10
        carry10 = s10 >> 21
        s11 += carry10
        s10 -= carry10 << 21
        #// @var int $carry11
        carry11 = s11 >> 21
        s12 += carry11
        s11 -= carry11 << 21
        s0 += self.mul(s12, 666643, 20)
        s1 += self.mul(s12, 470296, 19)
        s2 += self.mul(s12, 654183, 20)
        s3 -= self.mul(s12, 997805, 20)
        s4 += self.mul(s12, 136657, 18)
        s5 -= self.mul(s12, 683901, 20)
        #// @var int $carry0
        carry0 = s0 >> 21
        s1 += carry0
        s0 -= carry0 << 21
        #// @var int $carry1
        carry1 = s1 >> 21
        s2 += carry1
        s1 -= carry1 << 21
        #// @var int $carry2
        carry2 = s2 >> 21
        s3 += carry2
        s2 -= carry2 << 21
        #// @var int $carry3
        carry3 = s3 >> 21
        s4 += carry3
        s3 -= carry3 << 21
        #// @var int $carry4
        carry4 = s4 >> 21
        s5 += carry4
        s4 -= carry4 << 21
        #// @var int $carry5
        carry5 = s5 >> 21
        s6 += carry5
        s5 -= carry5 << 21
        #// @var int $carry6
        carry6 = s6 >> 21
        s7 += carry6
        s6 -= carry6 << 21
        #// @var int $carry7
        carry7 = s7 >> 21
        s8 += carry7
        s7 -= carry7 << 21
        #// @var int $carry8
        carry8 = s8 >> 21
        s9 += carry8
        s8 -= carry8 << 21
        #// @var int $carry9
        carry9 = s9 >> 21
        s10 += carry9
        s9 -= carry9 << 21
        #// @var int $carry10
        carry10 = s10 >> 21
        s11 += carry10
        s10 -= carry10 << 21
        #// 
        #// @var array<int, int>
        #//
        arr = Array(php_int(s0 >> 0), php_int(s0 >> 8), php_int(s0 >> 16 | s1 << 5), php_int(s1 >> 3), php_int(s1 >> 11), php_int(s1 >> 19 | s2 << 2), php_int(s2 >> 6), php_int(s2 >> 14 | s3 << 7), php_int(s3 >> 1), php_int(s3 >> 9), php_int(s3 >> 17 | s4 << 4), php_int(s4 >> 4), php_int(s4 >> 12), php_int(s4 >> 20 | s5 << 1), php_int(s5 >> 7), php_int(s5 >> 15 | s6 << 6), php_int(s6 >> 2), php_int(s6 >> 10), php_int(s6 >> 18 | s7 << 3), php_int(s7 >> 5), php_int(s7 >> 13), php_int(s8 >> 0), php_int(s8 >> 8), php_int(s8 >> 16 | s9 << 5), php_int(s9 >> 3), php_int(s9 >> 11), php_int(s9 >> 19 | s10 << 2), php_int(s10 >> 6), php_int(s10 >> 14 | s11 << 7), php_int(s11 >> 1), php_int(s11 >> 9), php_int(s11) >> 17)
        return self.intarraytostring(arr)
    # end def sc_reduce
    #// 
    #// multiply by the order of the main subgroup l = 2^252+27742317777372353535851937790883648493
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Ge_P3 $A
    #// @return ParagonIE_Sodium_Core_Curve25519_Ge_P3
    #//
    @classmethod
    def ge_mul_l(self, A=None):
        
        #// @var array<int, int> $aslide
        aslide = Array(13, 0, 0, 0, 0, -1, 0, 0, 0, 0, -11, 0, 0, 0, 0, 0, 0, -5, 0, 0, 0, 0, 0, 0, -3, 0, 0, 0, 0, -13, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, -13, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 11, 0, 0, 0, 0, 0, 11, 0, 0, 0, 0, -13, 0, 0, 0, 0, 0, 0, -3, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 3, 0, 0, 0, 0, -11, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)
        #// @var array<int, ParagonIE_Sodium_Core_Curve25519_Ge_Cached> $Ai size 8
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
# end class ParagonIE_Sodium_Core_Curve25519
