#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
if php_class_exists("ParagonIE_Sodium_Core32_SipHash", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_SodiumCompat_Core32_SipHash
#// 
#// Only uses 32-bit arithmetic, while the original SipHash used 64-bit integers
#//
class ParagonIE_Sodium_Core32_SipHash(ParagonIE_Sodium_Core32_Util):
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param array<int, ParagonIE_Sodium_Core32_Int64> $v
    #// @return array<int, ParagonIE_Sodium_Core32_Int64>
    #//
    @classmethod
    def sipround(self, v_=None):
        
        
        #// # v0 += v1;
        v_[0] = v_[0].addint64(v_[1])
        #// # v1 = ROTL(v1, 13);
        v_[1] = v_[1].rotateleft(13)
        #// #  v1 ^= v0;
        v_[1] = v_[1].xorint64(v_[0])
        #// #  v0=ROTL(v0,32);
        v_[0] = v_[0].rotateleft(32)
        #// # v2 += v3;
        v_[2] = v_[2].addint64(v_[3])
        #// # v3=ROTL(v3,16);
        v_[3] = v_[3].rotateleft(16)
        #// #  v3 ^= v2;
        v_[3] = v_[3].xorint64(v_[2])
        #// # v0 += v3;
        v_[0] = v_[0].addint64(v_[3])
        #// # v3=ROTL(v3,21);
        v_[3] = v_[3].rotateleft(21)
        #// # v3 ^= v0;
        v_[3] = v_[3].xorint64(v_[0])
        #// # v2 += v1;
        v_[2] = v_[2].addint64(v_[1])
        #// # v1=ROTL(v1,17);
        v_[1] = v_[1].rotateleft(17)
        #// #  v1 ^= v2;
        v_[1] = v_[1].xorint64(v_[2])
        #// # v2=ROTL(v2,32)
        v_[2] = v_[2].rotateleft(32)
        return v_
    # end def sipround
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
        v_ = Array(php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64(Array(29551, 28005, 28787, 25973))), php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64(Array(25711, 29281, 28260, 28525))), php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64(Array(27769, 26469, 28261, 29281))), php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64(Array(29797, 25698, 31092, 25971))))
        #// # u64 k0 = LOAD64_LE( k );
        #// # u64 k1 = LOAD64_LE( k + 8 );
        k_ = Array(ParagonIE_Sodium_Core32_Int64.fromreversestring(self.substr(key_, 0, 8)), ParagonIE_Sodium_Core32_Int64.fromreversestring(self.substr(key_, 8, 8)))
        #// # b = ( ( u64 )inlen ) << 56;
        b_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64(Array(inlen_ << 8 & 65535, 0, 0, 0)))
        #// # v3 ^= k1;
        v_[3] = v_[3].xorint64(k_[1])
        #// # v2 ^= k0;
        v_[2] = v_[2].xorint64(k_[0])
        #// # v1 ^= k1;
        v_[1] = v_[1].xorint64(k_[1])
        #// # v0 ^= k0;
        v_[0] = v_[0].xorint64(k_[0])
        left_ = inlen_
        #// # for ( ; in != end; in += 8 )
        while True:
            
            if not (left_ >= 8):
                break
            # end if
            #// # m = LOAD64_LE( in );
            m_ = ParagonIE_Sodium_Core32_Int64.fromreversestring(self.substr(in_, 0, 8))
            #// # v3 ^= m;
            v_[3] = v_[3].xorint64(m_)
            #// # SIPROUND;
            #// # SIPROUND;
            v_ = self.sipround(v_)
            v_ = self.sipround(v_)
            #// # v0 ^= m;
            v_[0] = v_[0].xorint64(m_)
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
                b_ = b_.orint64(ParagonIE_Sodium_Core32_Int64.fromints(0, self.chrtoint(in_[6]) << 16))
            # end if
            if case(6):
                b_ = b_.orint64(ParagonIE_Sodium_Core32_Int64.fromints(0, self.chrtoint(in_[5]) << 8))
            # end if
            if case(5):
                b_ = b_.orint64(ParagonIE_Sodium_Core32_Int64.fromints(0, self.chrtoint(in_[4])))
            # end if
            if case(4):
                b_ = b_.orint64(ParagonIE_Sodium_Core32_Int64.fromints(self.chrtoint(in_[3]) << 24, 0))
            # end if
            if case(3):
                b_ = b_.orint64(ParagonIE_Sodium_Core32_Int64.fromints(self.chrtoint(in_[2]) << 16, 0))
            # end if
            if case(2):
                b_ = b_.orint64(ParagonIE_Sodium_Core32_Int64.fromints(self.chrtoint(in_[1]) << 8, 0))
            # end if
            if case(1):
                b_ = b_.orint64(ParagonIE_Sodium_Core32_Int64.fromints(self.chrtoint(in_[0]), 0))
            # end if
            if case(0):
                break
            # end if
        # end for
        #// # v3 ^= b;
        v_[3] = v_[3].xorint64(b_)
        #// # SIPROUND;
        #// # SIPROUND;
        v_ = self.sipround(v_)
        v_ = self.sipround(v_)
        #// # v0 ^= b;
        v_[0] = v_[0].xorint64(b_)
        #// Flip the lower 8 bits of v2 which is ($v[4], $v[5]) in our implementation
        #// # v2 ^= 0xff;
        v_[2].limbs[3] ^= 255
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
        return v_[0].xorint64(v_[1]).xorint64(v_[2]).xorint64(v_[3]).toreversestring()
    # end def siphash24
# end class ParagonIE_Sodium_Core32_SipHash
