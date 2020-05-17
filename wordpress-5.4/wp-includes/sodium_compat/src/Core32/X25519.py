#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
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
    def fe_cswap(self, f_=None, g_=None, b_=0):
        
        
        f0_ = php_int(f_[0].toint())
        f1_ = php_int(f_[1].toint())
        f2_ = php_int(f_[2].toint())
        f3_ = php_int(f_[3].toint())
        f4_ = php_int(f_[4].toint())
        f5_ = php_int(f_[5].toint())
        f6_ = php_int(f_[6].toint())
        f7_ = php_int(f_[7].toint())
        f8_ = php_int(f_[8].toint())
        f9_ = php_int(f_[9].toint())
        g0_ = php_int(g_[0].toint())
        g1_ = php_int(g_[1].toint())
        g2_ = php_int(g_[2].toint())
        g3_ = php_int(g_[3].toint())
        g4_ = php_int(g_[4].toint())
        g5_ = php_int(g_[5].toint())
        g6_ = php_int(g_[6].toint())
        g7_ = php_int(g_[7].toint())
        g8_ = php_int(g_[8].toint())
        g9_ = php_int(g_[9].toint())
        b_ = -b_
        #// @var int $x0
        x0_ = f0_ ^ g0_ & b_
        #// @var int $x1
        x1_ = f1_ ^ g1_ & b_
        #// @var int $x2
        x2_ = f2_ ^ g2_ & b_
        #// @var int $x3
        x3_ = f3_ ^ g3_ & b_
        #// @var int $x4
        x4_ = f4_ ^ g4_ & b_
        #// @var int $x5
        x5_ = f5_ ^ g5_ & b_
        #// @var int $x6
        x6_ = f6_ ^ g6_ & b_
        #// @var int $x7
        x7_ = f7_ ^ g7_ & b_
        #// @var int $x8
        x8_ = f8_ ^ g8_ & b_
        #// @var int $x9
        x9_ = f9_ ^ g9_ & b_
        f_[0] = ParagonIE_Sodium_Core32_Int32.fromint(f0_ ^ x0_)
        f_[1] = ParagonIE_Sodium_Core32_Int32.fromint(f1_ ^ x1_)
        f_[2] = ParagonIE_Sodium_Core32_Int32.fromint(f2_ ^ x2_)
        f_[3] = ParagonIE_Sodium_Core32_Int32.fromint(f3_ ^ x3_)
        f_[4] = ParagonIE_Sodium_Core32_Int32.fromint(f4_ ^ x4_)
        f_[5] = ParagonIE_Sodium_Core32_Int32.fromint(f5_ ^ x5_)
        f_[6] = ParagonIE_Sodium_Core32_Int32.fromint(f6_ ^ x6_)
        f_[7] = ParagonIE_Sodium_Core32_Int32.fromint(f7_ ^ x7_)
        f_[8] = ParagonIE_Sodium_Core32_Int32.fromint(f8_ ^ x8_)
        f_[9] = ParagonIE_Sodium_Core32_Int32.fromint(f9_ ^ x9_)
        g_[0] = ParagonIE_Sodium_Core32_Int32.fromint(g0_ ^ x0_)
        g_[1] = ParagonIE_Sodium_Core32_Int32.fromint(g1_ ^ x1_)
        g_[2] = ParagonIE_Sodium_Core32_Int32.fromint(g2_ ^ x2_)
        g_[3] = ParagonIE_Sodium_Core32_Int32.fromint(g3_ ^ x3_)
        g_[4] = ParagonIE_Sodium_Core32_Int32.fromint(g4_ ^ x4_)
        g_[5] = ParagonIE_Sodium_Core32_Int32.fromint(g5_ ^ x5_)
        g_[6] = ParagonIE_Sodium_Core32_Int32.fromint(g6_ ^ x6_)
        g_[7] = ParagonIE_Sodium_Core32_Int32.fromint(g7_ ^ x7_)
        g_[8] = ParagonIE_Sodium_Core32_Int32.fromint(g8_ ^ x8_)
        g_[9] = ParagonIE_Sodium_Core32_Int32.fromint(g9_ ^ x9_)
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
    def fe_mul121666(self, f_=None):
        
        
        #// @var array<int, ParagonIE_Sodium_Core32_Int64> $h
        h_ = Array()
        i_ = 0
        while i_ < 10:
            
            h_[i_] = f_[i_].toint64().mulint(121666, 17)
            i_ += 1
        # end while
        carry9_ = h_[9].addint(1 << 24).shiftright(25)
        h_[0] = h_[0].addint64(carry9_.mulint(19, 5))
        h_[9] = h_[9].subint64(carry9_.shiftleft(25))
        carry1_ = h_[1].addint(1 << 24).shiftright(25)
        h_[2] = h_[2].addint64(carry1_)
        h_[1] = h_[1].subint64(carry1_.shiftleft(25))
        carry3_ = h_[3].addint(1 << 24).shiftright(25)
        h_[4] = h_[4].addint64(carry3_)
        h_[3] = h_[3].subint64(carry3_.shiftleft(25))
        carry5_ = h_[5].addint(1 << 24).shiftright(25)
        h_[6] = h_[6].addint64(carry5_)
        h_[5] = h_[5].subint64(carry5_.shiftleft(25))
        carry7_ = h_[7].addint(1 << 24).shiftright(25)
        h_[8] = h_[8].addint64(carry7_)
        h_[7] = h_[7].subint64(carry7_.shiftleft(25))
        carry0_ = h_[0].addint(1 << 25).shiftright(26)
        h_[1] = h_[1].addint64(carry0_)
        h_[0] = h_[0].subint64(carry0_.shiftleft(26))
        carry2_ = h_[2].addint(1 << 25).shiftright(26)
        h_[3] = h_[3].addint64(carry2_)
        h_[2] = h_[2].subint64(carry2_.shiftleft(26))
        carry4_ = h_[4].addint(1 << 25).shiftright(26)
        h_[5] = h_[5].addint64(carry4_)
        h_[4] = h_[4].subint64(carry4_.shiftleft(26))
        carry6_ = h_[6].addint(1 << 25).shiftright(26)
        h_[7] = h_[7].addint64(carry6_)
        h_[6] = h_[6].subint64(carry6_.shiftleft(26))
        carry8_ = h_[8].addint(1 << 25).shiftright(26)
        h_[9] = h_[9].addint64(carry8_)
        h_[8] = h_[8].subint64(carry8_.shiftleft(26))
        i_ = 0
        while i_ < 10:
            
            h_[i_] = h_[i_].toint32()
            i_ += 1
        # end while
        #// @var array<int, ParagonIE_Sodium_Core32_Int32> $h2
        h2_ = h_
        return ParagonIE_Sodium_Core32_Curve25519_Fe.fromarray(h2_)
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
    def crypto_scalarmult_curve25519_ref10(self, n_=None, p_=None):
        
        
        #// # for (i = 0;i < 32;++i) e[i] = n[i];
        e_ = "" + n_
        #// # e[0] &= 248;
        e_[0] = self.inttochr(self.chrtoint(e_[0]) & 248)
        #// # e[31] &= 127;
        #// # e[31] |= 64;
        e_[31] = self.inttochr(self.chrtoint(e_[31]) & 127 | 64)
        #// # fe_frombytes(x1,p);
        x1_ = self.fe_frombytes(p_)
        #// # fe_1(x2);
        x2_ = self.fe_1()
        #// # fe_0(z2);
        z2_ = self.fe_0()
        #// # fe_copy(x3,x1);
        x3_ = self.fe_copy(x1_)
        #// # fe_1(z3);
        z3_ = self.fe_1()
        #// # swap = 0;
        #// @var int $swap
        swap_ = 0
        #// # for (pos = 254;pos >= 0;--pos) {
        pos_ = 254
        while pos_ >= 0:
            
            #// # b = e[pos / 8] >> (pos & 7);
            #// @var int $b
            b_ = self.chrtoint(e_[php_int(floor(pos_ / 8))]) >> pos_ & 7
            #// # b &= 1;
            b_ &= 1
            #// # swap ^= b;
            swap_ ^= b_
            #// # fe_cswap(x2,x3,swap);
            self.fe_cswap(x2_, x3_, swap_)
            #// # fe_cswap(z2,z3,swap);
            self.fe_cswap(z2_, z3_, swap_)
            #// # swap = b;
            #// @var int $swap
            swap_ = b_
            #// # fe_sub(tmp0,x3,z3);
            tmp0_ = self.fe_sub(x3_, z3_)
            #// # fe_sub(tmp1,x2,z2);
            tmp1_ = self.fe_sub(x2_, z2_)
            #// # fe_add(x2,x2,z2);
            x2_ = self.fe_add(x2_, z2_)
            #// # fe_add(z2,x3,z3);
            z2_ = self.fe_add(x3_, z3_)
            #// # fe_mul(z3,tmp0,x2);
            z3_ = self.fe_mul(tmp0_, x2_)
            #// # fe_mul(z2,z2,tmp1);
            z2_ = self.fe_mul(z2_, tmp1_)
            #// # fe_sq(tmp0,tmp1);
            tmp0_ = self.fe_sq(tmp1_)
            #// # fe_sq(tmp1,x2);
            tmp1_ = self.fe_sq(x2_)
            #// # fe_add(x3,z3,z2);
            x3_ = self.fe_add(z3_, z2_)
            #// # fe_sub(z2,z3,z2);
            z2_ = self.fe_sub(z3_, z2_)
            #// # fe_mul(x2,tmp1,tmp0);
            x2_ = self.fe_mul(tmp1_, tmp0_)
            #// # fe_sub(tmp1,tmp1,tmp0);
            tmp1_ = self.fe_sub(tmp1_, tmp0_)
            #// # fe_sq(z2,z2);
            z2_ = self.fe_sq(z2_)
            #// # fe_mul121666(z3,tmp1);
            z3_ = self.fe_mul121666(tmp1_)
            #// # fe_sq(x3,x3);
            x3_ = self.fe_sq(x3_)
            #// # fe_add(tmp0,tmp0,z3);
            tmp0_ = self.fe_add(tmp0_, z3_)
            #// # fe_mul(z3,x1,z2);
            z3_ = self.fe_mul(x1_, z2_)
            #// # fe_mul(z2,tmp1,tmp0);
            z2_ = self.fe_mul(tmp1_, tmp0_)
            pos_ -= 1
        # end while
        #// # fe_cswap(x2,x3,swap);
        self.fe_cswap(x2_, x3_, swap_)
        #// # fe_cswap(z2,z3,swap);
        self.fe_cswap(z2_, z3_, swap_)
        #// # fe_invert(z2,z2);
        z2_ = self.fe_invert(z2_)
        #// # fe_mul(x2,x2,z2);
        x2_ = self.fe_mul(x2_, z2_)
        #// # fe_tobytes(q,x2);
        return php_str(self.fe_tobytes(x2_))
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
    def edwards_to_montgomery(self, edwardsY_=None, edwardsZ_=None):
        
        
        tempX_ = self.fe_add(edwardsZ_, edwardsY_)
        tempZ_ = self.fe_sub(edwardsZ_, edwardsY_)
        tempZ_ = self.fe_invert(tempZ_)
        return self.fe_mul(tempX_, tempZ_)
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
    def crypto_scalarmult_curve25519_ref10_base(self, n_=None):
        
        
        #// # for (i = 0;i < 32;++i) e[i] = n[i];
        e_ = "" + n_
        #// # e[0] &= 248;
        e_[0] = self.inttochr(self.chrtoint(e_[0]) & 248)
        #// # e[31] &= 127;
        #// # e[31] |= 64;
        e_[31] = self.inttochr(self.chrtoint(e_[31]) & 127 | 64)
        A_ = self.ge_scalarmult_base(e_)
        if (not type(A_.Y).__name__ == "ParagonIE_Sodium_Core32_Curve25519_Fe") or (not type(A_.Z).__name__ == "ParagonIE_Sodium_Core32_Curve25519_Fe"):
            raise php_new_class("TypeError", lambda : TypeError("Null points encountered"))
        # end if
        pk_ = self.edwards_to_montgomery(A_.Y, A_.Z)
        return self.fe_tobytes(pk_)
    # end def crypto_scalarmult_curve25519_ref10_base
# end class ParagonIE_Sodium_Core32_X25519
