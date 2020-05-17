#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
if php_class_exists("ParagonIE_Sodium_Core_SipHash", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_SodiumCompat_Core_SipHash
#// 
#// Only uses 32-bit arithmetic, while the original SipHash used 64-bit integers
#//
class ParagonIE_Sodium_Core_SipHash(ParagonIE_Sodium_Core_Util):
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int[] $v
    #// @return int[]
    #//
    @classmethod
    def sipround(self, v_=None):
        
        
        #// # v0 += v1;
        v_[0], v_[1] = self.add(Array(v_[0], v_[1]), Array(v_[2], v_[3]))
        #// #  v1=ROTL(v1,13);
        v_[2], v_[3] = self.rotl_64(v_[2], v_[3], 13)
        #// #  v1 ^= v0;
        v_[2] ^= v_[0]
        v_[3] ^= v_[1]
        #// #  v0=ROTL(v0,32);
        v_[0], v_[1] = self.rotl_64(php_int(v_[0]), php_int(v_[1]), 32)
        #// # v2 += v3;
        v_[4], v_[5] = self.add(Array(v_[4], v_[5]), Array(v_[6], v_[7]))
        #// # v3=ROTL(v3,16);
        v_[6], v_[7] = self.rotl_64(v_[6], v_[7], 16)
        #// #  v3 ^= v2;
        v_[6] ^= v_[4]
        v_[7] ^= v_[5]
        #// # v0 += v3;
        v_[0], v_[1] = self.add(Array(php_int(v_[0]), php_int(v_[1])), Array(php_int(v_[6]), php_int(v_[7])))
        #// # v3=ROTL(v3,21);
        v_[6], v_[7] = self.rotl_64(php_int(v_[6]), php_int(v_[7]), 21)
        #// # v3 ^= v0;
        v_[6] ^= v_[0]
        v_[7] ^= v_[1]
        #// # v2 += v1;
        v_[4], v_[5] = self.add(Array(php_int(v_[4]), php_int(v_[5])), Array(php_int(v_[2]), php_int(v_[3])))
        #// # v1=ROTL(v1,17);
        v_[2], v_[3] = self.rotl_64(php_int(v_[2]), php_int(v_[3]), 17)
        #// #  v1 ^= v2;;
        v_[2] ^= v_[4]
        v_[3] ^= v_[5]
        #// # v2=ROTL(v2,32)
        v_[4], v_[5] = self.rotl_64(php_int(v_[4]), php_int(v_[5]), 32)
        return v_
    # end def sipround
    #// 
    #// Add two 32 bit integers representing a 64-bit integer.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int[] $a
    #// @param int[] $b
    #// @return array<int, mixed>
    #//
    @classmethod
    def add(self, a_=None, b_=None):
        
        
        #// @var int $x1
        x1_ = a_[1] + b_[1]
        #// @var int $c
        c_ = x1_ >> 32
        #// Carry if ($a + $b) > 0xffffffff
        #// @var int $x0
        x0_ = a_[0] + b_[0] + c_
        return Array(x0_ & 4294967295, x1_ & 4294967295)
    # end def add
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int $int0
    #// @param int $int1
    #// @param int $c
    #// @return array<int, mixed>
    #//
    @classmethod
    def rotl_64(self, int0_=None, int1_=None, c_=None):
        
        
        int0_ &= 4294967295
        int1_ &= 4294967295
        c_ &= 63
        if c_ == 32:
            return Array(int1_, int0_)
        # end if
        if c_ > 31:
            tmp_ = int1_
            int1_ = int0_
            int0_ = tmp_
            c_ &= 31
        # end if
        if c_ == 0:
            return Array(int0_, int1_)
        # end if
        return Array(4294967295 & int0_ << c_ | int1_ >> 32 - c_, 4294967295 & int1_ << c_ | int0_ >> 32 - c_)
    # end def rotl_64
    #// 
    #// Implements Siphash-2-4 using only 32-bit numbers.
    #// 
    #// When we split an int into two, the higher bits go to the lower index.
    #// e.g. 0xDEADBEEFAB10C92D becomes [
    #// 0 => 0xDEADBEEF,
    #// 1 => 0xAB10C92D
    #// ].
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $in
    #// @param string $key
    #// @return string
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def siphash24(self, in_=None, key_=None):
        
        
        inlen_ = self.strlen(in_)
        #// # /* "somepseudorandomlygeneratedbytes"
        #// # u64 v0 = 0x736f6d6570736575ULL;
        #// # u64 v1 = 0x646f72616e646f6dULL;
        #// # u64 v2 = 0x6c7967656e657261ULL;
        #// # u64 v3 = 0x7465646279746573ULL;
        v_ = Array(1936682341, 1886610805, 1685025377, 1852075885, 1819895653, 1852142177, 1952801890, 2037671283)
        #// v0 => $v[0], $v[1]
        #// v1 => $v[2], $v[3]
        #// v2 => $v[4], $v[5]
        #// v3 => $v[6], $v[7]
        #// # u64 k0 = LOAD64_LE( k );
        #// # u64 k1 = LOAD64_LE( k + 8 );
        k_ = Array(self.load_4(self.substr(key_, 4, 4)), self.load_4(self.substr(key_, 0, 4)), self.load_4(self.substr(key_, 12, 4)), self.load_4(self.substr(key_, 8, 4)))
        #// k0 => $k[0], $k[1]
        #// k1 => $k[2], $k[3]
        #// # b = ( ( u64 )inlen ) << 56;
        b_ = Array(inlen_ << 24, 0)
        #// See docblock for why the 0th index gets the higher bits.
        #// # v3 ^= k1;
        v_[6] ^= k_[2]
        v_[7] ^= k_[3]
        #// # v2 ^= k0;
        v_[4] ^= k_[0]
        v_[5] ^= k_[1]
        #// # v1 ^= k1;
        v_[2] ^= k_[2]
        v_[3] ^= k_[3]
        #// # v0 ^= k0;
        v_[0] ^= k_[0]
        v_[1] ^= k_[1]
        left_ = inlen_
        #// # for ( ; in != end; in += 8 )
        while True:
            
            if not (left_ >= 8):
                break
            # end if
            #// # m = LOAD64_LE( in );
            m_ = Array(self.load_4(self.substr(in_, 4, 4)), self.load_4(self.substr(in_, 0, 4)))
            #// # v3 ^= m;
            v_[6] ^= m_[0]
            v_[7] ^= m_[1]
            #// # SIPROUND;
            #// # SIPROUND;
            v_ = self.sipround(v_)
            v_ = self.sipround(v_)
            #// # v0 ^= m;
            v_[0] ^= m_[0]
            v_[1] ^= m_[1]
            in_ = self.substr(in_, 8)
            left_ -= 8
        # end while
        #// # switch( left )
        #// #  {
        #// #     case 7: b |= ( ( u64 )in[ 6] )  << 48;
        #// #     case 6: b |= ( ( u64 )in[ 5] )  << 40;
        #// #     case 5: b |= ( ( u64 )in[ 4] )  << 32;
        #// #     case 4: b |= ( ( u64 )in[ 3] )  << 24;
        #// #     case 3: b |= ( ( u64 )in[ 2] )  << 16;
        #// #     case 2: b |= ( ( u64 )in[ 1] )  <<  8;
        #// #     case 1: b |= ( ( u64 )in[ 0] ); break;
        #// #     case 0: break;
        #// # }
        for case in Switch(left_):
            if case(7):
                b_[0] |= self.chrtoint(in_[6]) << 16
            # end if
            if case(6):
                b_[0] |= self.chrtoint(in_[5]) << 8
            # end if
            if case(5):
                b_[0] |= self.chrtoint(in_[4])
            # end if
            if case(4):
                b_[1] |= self.chrtoint(in_[3]) << 24
            # end if
            if case(3):
                b_[1] |= self.chrtoint(in_[2]) << 16
            # end if
            if case(2):
                b_[1] |= self.chrtoint(in_[1]) << 8
            # end if
            if case(1):
                b_[1] |= self.chrtoint(in_[0])
            # end if
            if case(0):
                break
            # end if
        # end for
        #// See docblock for why the 0th index gets the higher bits.
        #// # v3 ^= b;
        v_[6] ^= b_[0]
        v_[7] ^= b_[1]
        #// # SIPROUND;
        #// # SIPROUND;
        v_ = self.sipround(v_)
        v_ = self.sipround(v_)
        #// # v0 ^= b;
        v_[0] ^= b_[0]
        v_[1] ^= b_[1]
        #// Flip the lower 8 bits of v2 which is ($v[4], $v[5]) in our implementation
        #// # v2 ^= 0xff;
        v_[5] ^= 255
        #// # SIPROUND;
        #// # SIPROUND;
        #// # SIPROUND;
        #// # SIPROUND;
        v_ = self.sipround(v_)
        v_ = self.sipround(v_)
        v_ = self.sipround(v_)
        v_ = self.sipround(v_)
        #// # b = v0 ^ v1 ^ v2 ^ v3;
        #// # STORE64_LE( out, b );
        return self.store32_le(v_[1] ^ v_[3] ^ v_[5] ^ v_[7]) + self.store32_le(v_[0] ^ v_[2] ^ v_[4] ^ v_[6])
    # end def siphash24
# end class ParagonIE_Sodium_Core_SipHash
