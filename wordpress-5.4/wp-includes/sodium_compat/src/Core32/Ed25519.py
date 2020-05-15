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
if php_class_exists("ParagonIE_Sodium_Core32_Ed25519", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core32_Ed25519
#//
class ParagonIE_Sodium_Core32_Ed25519(ParagonIE_Sodium_Core32_Curve25519):
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
        
        seed = random_bytes(self.SEED_BYTES)
        pk = ""
        sk = ""
        self.seed_keypair(pk, sk, seed)
        return sk + pk
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
    def seed_keypair(self, pk=None, sk=None, seed=None):
        
        if self.strlen(seed) != self.SEED_BYTES:
            raise php_new_class("RangeException", lambda : RangeException("crypto_sign keypair seed must be 32 bytes long"))
        # end if
        #// @var string $pk
        pk = self.publickey_from_secretkey(seed)
        sk = seed + pk
        return sk
    # end def seed_keypair
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $keypair
    #// @return string
    #// @throws TypeError
    #//
    @classmethod
    def secretkey(self, keypair=None):
        
        if self.strlen(keypair) != self.KEYPAIR_BYTES:
            raise php_new_class("RangeException", lambda : RangeException("crypto_sign keypair must be 96 bytes long"))
        # end if
        return self.substr(keypair, 0, 64)
    # end def secretkey
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $keypair
    #// @return string
    #// @throws RangeException
    #// @throws TypeError
    #//
    @classmethod
    def publickey(self, keypair=None):
        
        if self.strlen(keypair) != self.KEYPAIR_BYTES:
            raise php_new_class("RangeException", lambda : RangeException("crypto_sign keypair must be 96 bytes long"))
        # end if
        return self.substr(keypair, 64, 32)
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
    def publickey_from_secretkey(self, sk=None):
        
        #// @var string $sk
        sk = hash("sha512", self.substr(sk, 0, 32), True)
        sk[0] = self.inttochr(self.chrtoint(sk[0]) & 248)
        sk[31] = self.inttochr(self.chrtoint(sk[31]) & 63 | 64)
        return self.sk_to_pk(sk)
    # end def publickey_from_secretkey
    #// 
    #// @param string $pk
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def pk_to_curve25519(self, pk=None):
        
        if self.small_order(pk):
            raise php_new_class("SodiumException", lambda : SodiumException("Public key is on a small order"))
        # end if
        A = self.ge_frombytes_negate_vartime(pk)
        p1 = self.ge_mul_l(A)
        if (not self.fe_isnonzero(p1.X)):
            raise php_new_class("SodiumException", lambda : SodiumException("Unexpected zero result"))
        # end if
        #// # fe_1(one_minus_y);
        #// # fe_sub(one_minus_y, one_minus_y, A.Y);
        #// # fe_invert(one_minus_y, one_minus_y);
        one_minux_y = self.fe_invert(self.fe_sub(self.fe_1(), A.Y))
        #// # fe_1(x);
        #// # fe_add(x, x, A.Y);
        #// # fe_mul(x, x, one_minus_y);
        x = self.fe_mul(self.fe_add(self.fe_1(), A.Y), one_minux_y)
        #// # fe_tobytes(curve25519_pk, x);
        return self.fe_tobytes(x)
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
    def sk_to_pk(self, sk=None):
        
        return self.ge_p3_tobytes(self.ge_scalarmult_base(self.substr(sk, 0, 32)))
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
    def sign(self, message=None, sk=None):
        
        #// @var string $signature
        signature = self.sign_detached(message, sk)
        return signature + message
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
    def sign_open(self, message=None, pk=None):
        
        #// @var string $signature
        signature = self.substr(message, 0, 64)
        #// @var string $message
        message = self.substr(message, 64)
        if self.verify_detached(signature, message, pk):
            return message
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
    def sign_detached(self, message=None, sk=None):
        
        #// # crypto_hash_sha512(az, sk, 32);
        az = hash("sha512", self.substr(sk, 0, 32), True)
        #// # az[0] &= 248;
        #// # az[31] &= 63;
        #// # az[31] |= 64;
        az[0] = self.inttochr(self.chrtoint(az[0]) & 248)
        az[31] = self.inttochr(self.chrtoint(az[31]) & 63 | 64)
        #// # crypto_hash_sha512_init(&hs);
        #// # crypto_hash_sha512_update(&hs, az + 32, 32);
        #// # crypto_hash_sha512_update(&hs, m, mlen);
        #// # crypto_hash_sha512_final(&hs, nonce);
        hs = hash_init("sha512")
        hash_update(hs, self.substr(az, 32, 32))
        hash_update(hs, message)
        nonceHash = hash_final(hs, True)
        #// # memmove(sig + 32, sk + 32, 32);
        pk = self.substr(sk, 32, 32)
        #// # sc_reduce(nonce);
        #// # ge_scalarmult_base(&R, nonce);
        #// # ge_p3_tobytes(sig, &R);
        nonce = self.sc_reduce(nonceHash) + self.substr(nonceHash, 32)
        sig = self.ge_p3_tobytes(self.ge_scalarmult_base(nonce))
        #// # crypto_hash_sha512_init(&hs);
        #// # crypto_hash_sha512_update(&hs, sig, 64);
        #// # crypto_hash_sha512_update(&hs, m, mlen);
        #// # crypto_hash_sha512_final(&hs, hram);
        hs = hash_init("sha512")
        hash_update(hs, self.substr(sig, 0, 32))
        hash_update(hs, self.substr(pk, 0, 32))
        hash_update(hs, message)
        hramHash = hash_final(hs, True)
        #// # sc_reduce(hram);
        #// # sc_muladd(sig + 32, hram, az, nonce);
        hram = self.sc_reduce(hramHash)
        sigAfter = self.sc_muladd(hram, az, nonce)
        sig = self.substr(sig, 0, 32) + self.substr(sigAfter, 0, 32)
        try: 
            ParagonIE_Sodium_Compat.memzero(az)
        except SodiumException as ex:
            az = None
        # end try
        return sig
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
    def verify_detached(self, sig=None, message=None, pk=None):
        
        if self.strlen(sig) < 64:
            raise php_new_class("SodiumException", lambda : SodiumException("Signature is too short"))
        # end if
        if self.chrtoint(sig[63]) & 240 and self.check_s_lt_l(self.substr(sig, 32, 32)):
            raise php_new_class("SodiumException", lambda : SodiumException("S < L - Invalid signature"))
        # end if
        if self.small_order(sig):
            raise php_new_class("SodiumException", lambda : SodiumException("Signature is on too small of an order"))
        # end if
        if self.chrtoint(sig[63]) & 224 != 0:
            raise php_new_class("SodiumException", lambda : SodiumException("Invalid signature"))
        # end if
        d = 0
        i = 0
        while i < 32:
            
            d |= self.chrtoint(pk[i])
            i += 1
        # end while
        if d == 0:
            raise php_new_class("SodiumException", lambda : SodiumException("All zero public key"))
        # end if
        #// @var bool The original value of ParagonIE_Sodium_Compat::$fastMult
        orig = ParagonIE_Sodium_Compat.fastMult
        #// Set ParagonIE_Sodium_Compat::$fastMult to true to speed up verification.
        ParagonIE_Sodium_Compat.fastMult = True
        #// @var ParagonIE_Sodium_Core32_Curve25519_Ge_P3 $A
        A = self.ge_frombytes_negate_vartime(pk)
        #// @var string $hDigest
        hDigest = hash("sha512", self.substr(sig, 0, 32) + self.substr(pk, 0, 32) + message, True)
        #// @var string $h
        h = self.sc_reduce(hDigest) + self.substr(hDigest, 32)
        #// @var ParagonIE_Sodium_Core32_Curve25519_Ge_P2 $R
        R = self.ge_double_scalarmult_vartime(h, A, self.substr(sig, 32))
        #// @var string $rcheck
        rcheck = self.ge_tobytes(R)
        #// Reset ParagonIE_Sodium_Compat::$fastMult to what it was before.
        ParagonIE_Sodium_Compat.fastMult = orig
        return self.verify_32(rcheck, self.substr(sig, 0, 32))
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
    def check_s_lt_l(self, S=None):
        
        if self.strlen(S) < 32:
            raise php_new_class("SodiumException", lambda : SodiumException("Signature must be 32 bytes"))
        # end if
        L = Array(237, 211, 245, 92, 26, 99, 18, 88, 214, 156, 247, 162, 222, 249, 222, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16)
        #// @var array<int, int> $L
        c = 0
        n = 1
        i = 32
        while True:
            i -= 1
            x = self.chrtoint(S[i])
            c |= x - L[i] >> 8 & n
            n &= x ^ L[i] - 1 >> 8
            
            if i != 0:
                break
            # end if
        # end while
        return c == 0
    # end def check_s_lt_l
    #// 
    #// @param string $R
    #// @return bool
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def small_order(self, R=None):
        
        blacklist = Array(Array(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), Array(1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), Array(38, 232, 149, 143, 194, 178, 39, 176, 69, 195, 244, 137, 242, 239, 152, 240, 213, 223, 172, 5, 211, 198, 51, 57, 177, 56, 2, 136, 109, 83, 252, 5), Array(199, 23, 106, 112, 61, 77, 216, 79, 186, 60, 11, 118, 13, 16, 103, 15, 42, 32, 83, 250, 44, 57, 204, 198, 78, 199, 253, 119, 146, 172, 3, 122), Array(19, 232, 149, 143, 194, 178, 39, 176, 69, 195, 244, 137, 242, 239, 152, 240, 213, 223, 172, 5, 211, 198, 51, 57, 177, 56, 2, 136, 109, 83, 252, 133), Array(180, 23, 106, 112, 61, 77, 216, 79, 186, 60, 11, 118, 13, 16, 103, 15, 42, 32, 83, 250, 44, 57, 204, 198, 78, 199, 253, 119, 146, 172, 3, 250), Array(236, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 127), Array(237, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 127), Array(238, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 127), Array(217, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255), Array(218, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255), Array(219, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255))
        #// @var array<int, array<int, int>> $blacklist
        countBlacklist = php_count(blacklist)
        i = 0
        while i < countBlacklist:
            
            c = 0
            j = 0
            while j < 32:
                
                c |= self.chrtoint(R[j]) ^ blacklist[i][j]
                j += 1
            # end while
            if c == 0:
                return True
            # end if
            i += 1
        # end while
        return False
    # end def small_order
# end class ParagonIE_Sodium_Core32_Ed25519
