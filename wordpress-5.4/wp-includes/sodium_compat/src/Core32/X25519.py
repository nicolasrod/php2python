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
if php_class_exists("ParagonIE_Sodium_Core32_X25519", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core32_X25519
#//
class ParagonIE_Sodium_Core32_X25519(ParagonIE_Sodium_Core32_Curve25519):
    #// 
    #// Alters the objects passed to this method in place.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $f
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $g
    #// @param int $b
    #// @return void
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedMethodCall
    #//
    @classmethod
    def fe_cswap(self, f=None, g=None, b=0):
        
        f0 = int(f[0].toint())
        f1 = int(f[1].toint())
        f2 = int(f[2].toint())
        f3 = int(f[3].toint())
        f4 = int(f[4].toint())
        f5 = int(f[5].toint())
        f6 = int(f[6].toint())
        f7 = int(f[7].toint())
        f8 = int(f[8].toint())
        f9 = int(f[9].toint())
        g0 = int(g[0].toint())
        g1 = int(g[1].toint())
        g2 = int(g[2].toint())
        g3 = int(g[3].toint())
        g4 = int(g[4].toint())
        g5 = int(g[5].toint())
        g6 = int(g[6].toint())
        g7 = int(g[7].toint())
        g8 = int(g[8].toint())
        g9 = int(g[9].toint())
        b = -b
        #// @var int $x0
        x0 = f0 ^ g0 & b
        #// @var int $x1
        x1 = f1 ^ g1 & b
        #// @var int $x2
        x2 = f2 ^ g2 & b
        #// @var int $x3
        x3 = f3 ^ g3 & b
        #// @var int $x4
        x4 = f4 ^ g4 & b
        #// @var int $x5
        x5 = f5 ^ g5 & b
        #// @var int $x6
        x6 = f6 ^ g6 & b
        #// @var int $x7
        x7 = f7 ^ g7 & b
        #// @var int $x8
        x8 = f8 ^ g8 & b
        #// @var int $x9
        x9 = f9 ^ g9 & b
        f[0] = ParagonIE_Sodium_Core32_Int32.fromint(f0 ^ x0)
        f[1] = ParagonIE_Sodium_Core32_Int32.fromint(f1 ^ x1)
        f[2] = ParagonIE_Sodium_Core32_Int32.fromint(f2 ^ x2)
        f[3] = ParagonIE_Sodium_Core32_Int32.fromint(f3 ^ x3)
        f[4] = ParagonIE_Sodium_Core32_Int32.fromint(f4 ^ x4)
        f[5] = ParagonIE_Sodium_Core32_Int32.fromint(f5 ^ x5)
        f[6] = ParagonIE_Sodium_Core32_Int32.fromint(f6 ^ x6)
        f[7] = ParagonIE_Sodium_Core32_Int32.fromint(f7 ^ x7)
        f[8] = ParagonIE_Sodium_Core32_Int32.fromint(f8 ^ x8)
        f[9] = ParagonIE_Sodium_Core32_Int32.fromint(f9 ^ x9)
        g[0] = ParagonIE_Sodium_Core32_Int32.fromint(g0 ^ x0)
        g[1] = ParagonIE_Sodium_Core32_Int32.fromint(g1 ^ x1)
        g[2] = ParagonIE_Sodium_Core32_Int32.fromint(g2 ^ x2)
        g[3] = ParagonIE_Sodium_Core32_Int32.fromint(g3 ^ x3)
        g[4] = ParagonIE_Sodium_Core32_Int32.fromint(g4 ^ x4)
        g[5] = ParagonIE_Sodium_Core32_Int32.fromint(g5 ^ x5)
        g[6] = ParagonIE_Sodium_Core32_Int32.fromint(g6 ^ x6)
        g[7] = ParagonIE_Sodium_Core32_Int32.fromint(g7 ^ x7)
        g[8] = ParagonIE_Sodium_Core32_Int32.fromint(g8 ^ x8)
        g[9] = ParagonIE_Sodium_Core32_Int32.fromint(g9 ^ x9)
    # end def fe_cswap
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $f
    #// @return ParagonIE_Sodium_Core32_Curve25519_Fe
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedAssignment
    #// @psalm-suppress MixedMethodCall
    #//
    @classmethod
    def fe_mul121666(self, f=None):
        
        #// @var array<int, ParagonIE_Sodium_Core32_Int64> $h
        h = Array()
        i = 0
        while i < 10:
            
            h[i] = f[i].toint64().mulint(121666, 17)
            i += 1
        # end while
        carry9 = h[9].addint(1 << 24).shiftright(25)
        h[0] = h[0].addint64(carry9.mulint(19, 5))
        h[9] = h[9].subint64(carry9.shiftleft(25))
        carry1 = h[1].addint(1 << 24).shiftright(25)
        h[2] = h[2].addint64(carry1)
        h[1] = h[1].subint64(carry1.shiftleft(25))
        carry3 = h[3].addint(1 << 24).shiftright(25)
        h[4] = h[4].addint64(carry3)
        h[3] = h[3].subint64(carry3.shiftleft(25))
        carry5 = h[5].addint(1 << 24).shiftright(25)
        h[6] = h[6].addint64(carry5)
        h[5] = h[5].subint64(carry5.shiftleft(25))
        carry7 = h[7].addint(1 << 24).shiftright(25)
        h[8] = h[8].addint64(carry7)
        h[7] = h[7].subint64(carry7.shiftleft(25))
        carry0 = h[0].addint(1 << 25).shiftright(26)
        h[1] = h[1].addint64(carry0)
        h[0] = h[0].subint64(carry0.shiftleft(26))
        carry2 = h[2].addint(1 << 25).shiftright(26)
        h[3] = h[3].addint64(carry2)
        h[2] = h[2].subint64(carry2.shiftleft(26))
        carry4 = h[4].addint(1 << 25).shiftright(26)
        h[5] = h[5].addint64(carry4)
        h[4] = h[4].subint64(carry4.shiftleft(26))
        carry6 = h[6].addint(1 << 25).shiftright(26)
        h[7] = h[7].addint64(carry6)
        h[6] = h[6].subint64(carry6.shiftleft(26))
        carry8 = h[8].addint(1 << 25).shiftright(26)
        h[9] = h[9].addint64(carry8)
        h[8] = h[8].subint64(carry8.shiftleft(26))
        i = 0
        while i < 10:
            
            h[i] = h[i].toint32()
            i += 1
        # end while
        #// @var array<int, ParagonIE_Sodium_Core32_Int32> $h2
        h2 = h
        return ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(h2)
    # end def fe_mul121666
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// Inline comments preceded by # are from libsodium's ref10 code.
    #// 
    #// @param string $n
    #// @param string $p
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def crypto_scalarmult_curve25519_ref10(self, n=None, p=None):
        
        #// # for (i = 0;i < 32;++i) e[i] = n[i];
        e = "" + n
        #// # e[0] &= 248;
        e[0] = self.inttochr(self.chrtoint(e[0]) & 248)
        #// # e[31] &= 127;
        #// # e[31] |= 64;
        e[31] = self.inttochr(self.chrtoint(e[31]) & 127 | 64)
        #// # fe_frombytes(x1,p);
        x1 = self.fe_frombytes(p)
        #// # fe_1(x2);
        x2 = self.fe_1()
        #// # fe_0(z2);
        z2 = self.fe_0()
        #// # fe_copy(x3,x1);
        x3 = self.fe_copy(x1)
        #// # fe_1(z3);
        z3 = self.fe_1()
        #// # swap = 0;
        #// @var int $swap
        swap = 0
        #// # for (pos = 254;pos >= 0;--pos) {
        pos = 254
        while pos >= 0:
            
            #// # b = e[pos / 8] >> (pos & 7);
            #// @var int $b
            b = self.chrtoint(e[int(floor(pos / 8))]) >> pos & 7
            #// # b &= 1;
            b &= 1
            #// # swap ^= b;
            swap ^= b
            #// # fe_cswap(x2,x3,swap);
            self.fe_cswap(x2, x3, swap)
            #// # fe_cswap(z2,z3,swap);
            self.fe_cswap(z2, z3, swap)
            #// # swap = b;
            #// @var int $swap
            swap = b
            #// # fe_sub(tmp0,x3,z3);
            tmp0 = self.fe_sub(x3, z3)
            #// # fe_sub(tmp1,x2,z2);
            tmp1 = self.fe_sub(x2, z2)
            #// # fe_add(x2,x2,z2);
            x2 = self.fe_add(x2, z2)
            #// # fe_add(z2,x3,z3);
            z2 = self.fe_add(x3, z3)
            #// # fe_mul(z3,tmp0,x2);
            z3 = self.fe_mul(tmp0, x2)
            #// # fe_mul(z2,z2,tmp1);
            z2 = self.fe_mul(z2, tmp1)
            #// # fe_sq(tmp0,tmp1);
            tmp0 = self.fe_sq(tmp1)
            #// # fe_sq(tmp1,x2);
            tmp1 = self.fe_sq(x2)
            #// # fe_add(x3,z3,z2);
            x3 = self.fe_add(z3, z2)
            #// # fe_sub(z2,z3,z2);
            z2 = self.fe_sub(z3, z2)
            #// # fe_mul(x2,tmp1,tmp0);
            x2 = self.fe_mul(tmp1, tmp0)
            #// # fe_sub(tmp1,tmp1,tmp0);
            tmp1 = self.fe_sub(tmp1, tmp0)
            #// # fe_sq(z2,z2);
            z2 = self.fe_sq(z2)
            #// # fe_mul121666(z3,tmp1);
            z3 = self.fe_mul121666(tmp1)
            #// # fe_sq(x3,x3);
            x3 = self.fe_sq(x3)
            #// # fe_add(tmp0,tmp0,z3);
            tmp0 = self.fe_add(tmp0, z3)
            #// # fe_mul(z3,x1,z2);
            z3 = self.fe_mul(x1, z2)
            #// # fe_mul(z2,tmp1,tmp0);
            z2 = self.fe_mul(tmp1, tmp0)
            pos -= 1
        # end while
        #// # fe_cswap(x2,x3,swap);
        self.fe_cswap(x2, x3, swap)
        #// # fe_cswap(z2,z3,swap);
        self.fe_cswap(z2, z3, swap)
        #// # fe_invert(z2,z2);
        z2 = self.fe_invert(z2)
        #// # fe_mul(x2,x2,z2);
        x2 = self.fe_mul(x2, z2)
        #// # fe_tobytes(q,x2);
        return str(self.fe_tobytes(x2))
    # end def crypto_scalarmult_curve25519_ref10
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $edwardsY
    #// @param ParagonIE_Sodium_Core32_Curve25519_Fe $edwardsZ
    #// @return ParagonIE_Sodium_Core32_Curve25519_Fe
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def edwards_to_montgomery(self, edwardsY=None, edwardsZ=None):
        
        tempX = self.fe_add(edwardsZ, edwardsY)
        tempZ = self.fe_sub(edwardsZ, edwardsY)
        tempZ = self.fe_invert(tempZ)
        return self.fe_mul(tempX, tempZ)
    # end def edwards_to_montgomery
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $n
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def crypto_scalarmult_curve25519_ref10_base(self, n=None):
        
        #// # for (i = 0;i < 32;++i) e[i] = n[i];
        e = "" + n
        #// # e[0] &= 248;
        e[0] = self.inttochr(self.chrtoint(e[0]) & 248)
        #// # e[31] &= 127;
        #// # e[31] |= 64;
        e[31] = self.inttochr(self.chrtoint(e[31]) & 127 | 64)
        A = self.ge_scalarmult_base(e)
        if (not type(A.Y).__name__ == "ParagonIE_Sodium_Core32_Curve25519_Fe") or (not type(A.Z).__name__ == "ParagonIE_Sodium_Core32_Curve25519_Fe"):
            raise php_new_class("TypeError", lambda : TypeError("Null points encountered"))
        # end if
        pk = self.edwards_to_montgomery(A.Y, A.Z)
        return self.fe_tobytes(pk)
    # end def crypto_scalarmult_curve25519_ref10_base
# end class ParagonIE_Sodium_Core32_X25519
