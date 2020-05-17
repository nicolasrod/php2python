#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
if php_class_exists("ParagonIE_Sodium_Core_Ed25519", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core_Ed25519
#//
class ParagonIE_Sodium_Core_Ed25519(ParagonIE_Sodium_Core_Curve25519):
    KEYPAIR_BYTES = 96
    SEED_BYTES = 32
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @return string (96 bytes)
    #// @throws Exception
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def keypair(self):
        
        
        seed_ = random_bytes(self.SEED_BYTES)
        pk_ = ""
        sk_ = ""
        self.seed_keypair(pk_, sk_, seed_)
        return sk_ + pk_
    # end def keypair
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $pk
    #// @param string $sk
    #// @param string $seed
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def seed_keypair(self, pk_=None, sk_=None, seed_=None):
        
        
        if self.strlen(seed_) != self.SEED_BYTES:
            raise php_new_class("RangeException", lambda : RangeException("crypto_sign keypair seed must be 32 bytes long"))
        # end if
        #// @var string $pk
        pk_ = self.publickey_from_secretkey(seed_)
        sk_ = seed_ + pk_
        return sk_
    # end def seed_keypair
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $keypair
    #// @return string
    #// @throws TypeError
    #//
    @classmethod
    def secretkey(self, keypair_=None):
        
        
        if self.strlen(keypair_) != self.KEYPAIR_BYTES:
            raise php_new_class("RangeException", lambda : RangeException("crypto_sign keypair must be 96 bytes long"))
        # end if
        return self.substr(keypair_, 0, 64)
    # end def secretkey
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $keypair
    #// @return string
    #// @throws TypeError
    #//
    @classmethod
    def publickey(self, keypair_=None):
        
        
        if self.strlen(keypair_) != self.KEYPAIR_BYTES:
            raise php_new_class("RangeException", lambda : RangeException("crypto_sign keypair must be 96 bytes long"))
        # end if
        return self.substr(keypair_, 64, 32)
    # end def publickey
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $sk
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def publickey_from_secretkey(self, sk_=None):
        
        
        #// @var string $sk
        sk_ = hash("sha512", self.substr(sk_, 0, 32), True)
        sk_[0] = self.inttochr(self.chrtoint(sk_[0]) & 248)
        sk_[31] = self.inttochr(self.chrtoint(sk_[31]) & 63 | 64)
        return self.sk_to_pk(sk_)
    # end def publickey_from_secretkey
    #// 
    #// @param string $pk
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def pk_to_curve25519(self, pk_=None):
        
        
        if self.small_order(pk_):
            raise php_new_class("SodiumException", lambda : SodiumException("Public key is on a small order"))
        # end if
        A_ = self.ge_frombytes_negate_vartime(self.substr(pk_, 0, 32))
        p1_ = self.ge_mul_l(A_)
        if (not self.fe_isnonzero(p1_.X)):
            raise php_new_class("SodiumException", lambda : SodiumException("Unexpected zero result"))
        # end if
        #// # fe_1(one_minus_y);
        #// # fe_sub(one_minus_y, one_minus_y, A.Y);
        #// # fe_invert(one_minus_y, one_minus_y);
        one_minux_y_ = self.fe_invert(self.fe_sub(self.fe_1(), A_.Y))
        #// # fe_1(x);
        #// # fe_add(x, x, A.Y);
        #// # fe_mul(x, x, one_minus_y);
        x_ = self.fe_mul(self.fe_add(self.fe_1(), A_.Y), one_minux_y_)
        #// # fe_tobytes(curve25519_pk, x);
        return self.fe_tobytes(x_)
    # end def pk_to_curve25519
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $sk
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def sk_to_pk(self, sk_=None):
        
        
        return self.ge_p3_tobytes(self.ge_scalarmult_base(self.substr(sk_, 0, 32)))
    # end def sk_to_pk
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $message
    #// @param string $sk
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def sign(self, message_=None, sk_=None):
        
        
        #// @var string $signature
        signature_ = self.sign_detached(message_, sk_)
        return signature_ + message_
    # end def sign
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $message A signed message
    #// @param string $pk      Public key
    #// @return string         Message (without signature)
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def sign_open(self, message_=None, pk_=None):
        
        
        #// @var string $signature
        signature_ = self.substr(message_, 0, 64)
        #// @var string $message
        message_ = self.substr(message_, 64)
        if self.verify_detached(signature_, message_, pk_):
            return message_
        # end if
        raise php_new_class("SodiumException", lambda : SodiumException("Invalid signature"))
    # end def sign_open
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $message
    #// @param string $sk
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def sign_detached(self, message_=None, sk_=None):
        
        
        #// # crypto_hash_sha512(az, sk, 32);
        az_ = hash("sha512", self.substr(sk_, 0, 32), True)
        #// # az[0] &= 248;
        #// # az[31] &= 63;
        #// # az[31] |= 64;
        az_[0] = self.inttochr(self.chrtoint(az_[0]) & 248)
        az_[31] = self.inttochr(self.chrtoint(az_[31]) & 63 | 64)
        #// # crypto_hash_sha512_init(&hs);
        #// # crypto_hash_sha512_update(&hs, az + 32, 32);
        #// # crypto_hash_sha512_update(&hs, m, mlen);
        #// # crypto_hash_sha512_final(&hs, nonce);
        hs_ = hash_init("sha512")
        hash_update(hs_, self.substr(az_, 32, 32))
        hash_update(hs_, message_)
        nonceHash_ = hash_final(hs_, True)
        #// # memmove(sig + 32, sk + 32, 32);
        pk_ = self.substr(sk_, 32, 32)
        #// # sc_reduce(nonce);
        #// # ge_scalarmult_base(&R, nonce);
        #// # ge_p3_tobytes(sig, &R);
        nonce_ = self.sc_reduce(nonceHash_) + self.substr(nonceHash_, 32)
        sig_ = self.ge_p3_tobytes(self.ge_scalarmult_base(nonce_))
        #// # crypto_hash_sha512_init(&hs);
        #// # crypto_hash_sha512_update(&hs, sig, 64);
        #// # crypto_hash_sha512_update(&hs, m, mlen);
        #// # crypto_hash_sha512_final(&hs, hram);
        hs_ = hash_init("sha512")
        hash_update(hs_, self.substr(sig_, 0, 32))
        hash_update(hs_, self.substr(pk_, 0, 32))
        hash_update(hs_, message_)
        hramHash_ = hash_final(hs_, True)
        #// # sc_reduce(hram);
        #// # sc_muladd(sig + 32, hram, az, nonce);
        hram_ = self.sc_reduce(hramHash_)
        sigAfter_ = self.sc_muladd(hram_, az_, nonce_)
        sig_ = self.substr(sig_, 0, 32) + self.substr(sigAfter_, 0, 32)
        try: 
            ParagonIE_Sodium_Compat.memzero(az_)
        except SodiumException as ex_:
            az_ = None
        # end try
        return sig_
    # end def sign_detached
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $sig
    #// @param string $message
    #// @param string $pk
    #// @return bool
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def verify_detached(self, sig_=None, message_=None, pk_=None):
        
        
        if self.strlen(sig_) < 64:
            raise php_new_class("SodiumException", lambda : SodiumException("Signature is too short"))
        # end if
        if self.chrtoint(sig_[63]) & 240 and self.check_s_lt_l(self.substr(sig_, 32, 32)):
            raise php_new_class("SodiumException", lambda : SodiumException("S < L - Invalid signature"))
        # end if
        if self.small_order(sig_):
            raise php_new_class("SodiumException", lambda : SodiumException("Signature is on too small of an order"))
        # end if
        if self.chrtoint(sig_[63]) & 224 != 0:
            raise php_new_class("SodiumException", lambda : SodiumException("Invalid signature"))
        # end if
        d_ = 0
        i_ = 0
        while i_ < 32:
            
            d_ |= self.chrtoint(pk_[i_])
            i_ += 1
        # end while
        if d_ == 0:
            raise php_new_class("SodiumException", lambda : SodiumException("All zero public key"))
        # end if
        #// @var bool The original value of ParagonIE_Sodium_Compat::$fastMult
        orig_ = ParagonIE_Sodium_Compat.fastMult
        #// Set ParagonIE_Sodium_Compat::$fastMult to true to speed up verification.
        ParagonIE_Sodium_Compat.fastMult = True
        #// @var ParagonIE_Sodium_Core_Curve25519_Ge_P3 $A
        A_ = self.ge_frombytes_negate_vartime(pk_)
        #// @var string $hDigest
        hDigest_ = hash("sha512", self.substr(sig_, 0, 32) + self.substr(pk_, 0, 32) + message_, True)
        #// @var string $h
        h_ = self.sc_reduce(hDigest_) + self.substr(hDigest_, 32)
        #// @var ParagonIE_Sodium_Core_Curve25519_Ge_P2 $R
        R_ = self.ge_double_scalarmult_vartime(h_, A_, self.substr(sig_, 32))
        #// @var string $rcheck
        rcheck_ = self.ge_tobytes(R_)
        #// Reset ParagonIE_Sodium_Compat::$fastMult to what it was before.
        ParagonIE_Sodium_Compat.fastMult = orig_
        return self.verify_32(rcheck_, self.substr(sig_, 0, 32))
    # end def verify_detached
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $S
    #// @return bool
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def check_s_lt_l(self, S_=None):
        
        
        if self.strlen(S_) < 32:
            raise php_new_class("SodiumException", lambda : SodiumException("Signature must be 32 bytes"))
        # end if
        L_ = Array(237, 211, 245, 92, 26, 99, 18, 88, 214, 156, 247, 162, 222, 249, 222, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16)
        c_ = 0
        n_ = 1
        i_ = 32
        #// @var array<int, int> $L
        while True:
            i_ -= 1
            x_ = self.chrtoint(S_[i_])
            c_ |= x_ - L_[i_] >> 8 & n_
            n_ &= x_ ^ L_[i_] - 1 >> 8
            
            if i_ != 0:
                break
            # end if
        # end while
        return c_ == 0
    # end def check_s_lt_l
    #// 
    #// @param string $R
    #// @return bool
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def small_order(self, R_=None):
        
        
        #// @var array<int, array<int, int>> $blacklist
        blacklist_ = Array(Array(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), Array(1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), Array(38, 232, 149, 143, 194, 178, 39, 176, 69, 195, 244, 137, 242, 239, 152, 240, 213, 223, 172, 5, 211, 198, 51, 57, 177, 56, 2, 136, 109, 83, 252, 5), Array(199, 23, 106, 112, 61, 77, 216, 79, 186, 60, 11, 118, 13, 16, 103, 15, 42, 32, 83, 250, 44, 57, 204, 198, 78, 199, 253, 119, 146, 172, 3, 122), Array(19, 232, 149, 143, 194, 178, 39, 176, 69, 195, 244, 137, 242, 239, 152, 240, 213, 223, 172, 5, 211, 198, 51, 57, 177, 56, 2, 136, 109, 83, 252, 133), Array(180, 23, 106, 112, 61, 77, 216, 79, 186, 60, 11, 118, 13, 16, 103, 15, 42, 32, 83, 250, 44, 57, 204, 198, 78, 199, 253, 119, 146, 172, 3, 250), Array(236, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 127), Array(237, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 127), Array(238, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 127), Array(217, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255), Array(218, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255), Array(219, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255))
        #// @var int $countBlacklist
        countBlacklist_ = php_count(blacklist_)
        i_ = 0
        while i_ < countBlacklist_:
            
            c_ = 0
            j_ = 0
            while j_ < 32:
                
                c_ |= self.chrtoint(R_[j_]) ^ php_int(blacklist_[i_][j_])
                j_ += 1
            # end while
            if c_ == 0:
                return True
            # end if
            i_ += 1
        # end while
        return False
    # end def small_order
# end class ParagonIE_Sodium_Core_Ed25519
