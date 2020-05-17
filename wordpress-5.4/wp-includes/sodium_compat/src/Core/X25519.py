#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
if php_class_exists("ParagonIE_Sodium_Core_X25519", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core_X25519
#//
class ParagonIE_Sodium_Core_X25519(ParagonIE_Sodium_Core_Curve25519):
    #// 
    #// Alters the objects passed to this method in place.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $f
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $g
    #// @param int $b
    #// @return void
    #// @psalm-suppress MixedAssignment
    #//
    @classmethod
    def fe_cswap(self, f_=None, g_=None, b_=0):
        
        
        f0_ = php_int(f_[0])
        f1_ = php_int(f_[1])
        f2_ = php_int(f_[2])
        f3_ = php_int(f_[3])
        f4_ = php_int(f_[4])
        f5_ = php_int(f_[5])
        f6_ = php_int(f_[6])
        f7_ = php_int(f_[7])
        f8_ = php_int(f_[8])
        f9_ = php_int(f_[9])
        g0_ = php_int(g_[0])
        g1_ = php_int(g_[1])
        g2_ = php_int(g_[2])
        g3_ = php_int(g_[3])
        g4_ = php_int(g_[4])
        g5_ = php_int(g_[5])
        g6_ = php_int(g_[6])
        g7_ = php_int(g_[7])
        g8_ = php_int(g_[8])
        g9_ = php_int(g_[9])
        b_ = -b_
        x0_ = f0_ ^ g0_ & b_
        x1_ = f1_ ^ g1_ & b_
        x2_ = f2_ ^ g2_ & b_
        x3_ = f3_ ^ g3_ & b_
        x4_ = f4_ ^ g4_ & b_
        x5_ = f5_ ^ g5_ & b_
        x6_ = f6_ ^ g6_ & b_
        x7_ = f7_ ^ g7_ & b_
        x8_ = f8_ ^ g8_ & b_
        x9_ = f9_ ^ g9_ & b_
        f_[0] = f0_ ^ x0_
        f_[1] = f1_ ^ x1_
        f_[2] = f2_ ^ x2_
        f_[3] = f3_ ^ x3_
        f_[4] = f4_ ^ x4_
        f_[5] = f5_ ^ x5_
        f_[6] = f6_ ^ x6_
        f_[7] = f7_ ^ x7_
        f_[8] = f8_ ^ x8_
        f_[9] = f9_ ^ x9_
        g_[0] = g0_ ^ x0_
        g_[1] = g1_ ^ x1_
        g_[2] = g2_ ^ x2_
        g_[3] = g3_ ^ x3_
        g_[4] = g4_ ^ x4_
        g_[5] = g5_ ^ x5_
        g_[6] = g6_ ^ x6_
        g_[7] = g7_ ^ x7_
        g_[8] = g8_ ^ x8_
        g_[9] = g9_ ^ x9_
    # end def fe_cswap
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $f
    #// @return ParagonIE_Sodium_Core_Curve25519_Fe
    #//
    @classmethod
    def fe_mul121666(self, f_=None):
        
        
        h_ = Array(self.mul(php_int(f_[0]), 121666, 17), self.mul(php_int(f_[1]), 121666, 17), self.mul(php_int(f_[2]), 121666, 17), self.mul(php_int(f_[3]), 121666, 17), self.mul(php_int(f_[4]), 121666, 17), self.mul(php_int(f_[5]), 121666, 17), self.mul(php_int(f_[6]), 121666, 17), self.mul(php_int(f_[7]), 121666, 17), self.mul(php_int(f_[8]), 121666, 17), self.mul(php_int(f_[9]), 121666, 17))
        #// @var int $carry9
        carry9_ = h_[9] + 1 << 24 >> 25
        h_[0] += self.mul(carry9_, 19, 5)
        h_[9] -= carry9_ << 25
        #// @var int $carry1
        carry1_ = h_[1] + 1 << 24 >> 25
        h_[2] += carry1_
        h_[1] -= carry1_ << 25
        #// @var int $carry3
        carry3_ = h_[3] + 1 << 24 >> 25
        h_[4] += carry3_
        h_[3] -= carry3_ << 25
        #// @var int $carry5
        carry5_ = h_[5] + 1 << 24 >> 25
        h_[6] += carry5_
        h_[5] -= carry5_ << 25
        #// @var int $carry7
        carry7_ = h_[7] + 1 << 24 >> 25
        h_[8] += carry7_
        h_[7] -= carry7_ << 25
        #// @var int $carry0
        carry0_ = h_[0] + 1 << 25 >> 26
        h_[1] += carry0_
        h_[0] -= carry0_ << 26
        #// @var int $carry2
        carry2_ = h_[2] + 1 << 25 >> 26
        h_[3] += carry2_
        h_[2] -= carry2_ << 26
        #// @var int $carry4
        carry4_ = h_[4] + 1 << 25 >> 26
        h_[5] += carry4_
        h_[4] -= carry4_ << 26
        #// @var int $carry6
        carry6_ = h_[6] + 1 << 25 >> 26
        h_[7] += carry6_
        h_[6] -= carry6_ << 26
        #// @var int $carry8
        carry8_ = h_[8] + 1 << 25 >> 26
        h_[9] += carry8_
        h_[8] -= carry8_ << 26
        for i_,value_ in h_:
            h_[i_] = php_int(value_)
        # end for
        return ParagonIE_Sodium_Core_Curve25519_Fe.fromarray(h_)
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
        return self.fe_tobytes(x2_)
    # end def crypto_scalarmult_curve25519_ref10
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $edwardsY
    #// @param ParagonIE_Sodium_Core_Curve25519_Fe $edwardsZ
    #// @return ParagonIE_Sodium_Core_Curve25519_Fe
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
        if (not type(A_.Y).__name__ == "ParagonIE_Sodium_Core_Curve25519_Fe") or (not type(A_.Z).__name__ == "ParagonIE_Sodium_Core_Curve25519_Fe"):
            raise php_new_class("TypeError", lambda : TypeError("Null points encountered"))
        # end if
        pk_ = self.edwards_to_montgomery(A_.Y, A_.Z)
        return self.fe_tobytes(pk_)
    # end def crypto_scalarmult_curve25519_ref10_base
# end class ParagonIE_Sodium_Core_X25519
