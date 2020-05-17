#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
if php_class_exists("ParagonIE_Sodium_Core_BLAKE2b", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core_BLAKE2b
#// 
#// Based on the work of Devi Mandiri in devi/salt.
#//
class ParagonIE_Sodium_Core32_BLAKE2b(ParagonIE_Sodium_Core_Util):
    #// 
    #// @var SplFixedArray
    #//
    iv = Array()
    #// 
    #// @var array<int, array<int, int>>
    #//
    sigma = Array(Array(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15), Array(14, 10, 4, 8, 9, 15, 13, 6, 1, 12, 0, 2, 11, 7, 5, 3), Array(11, 8, 12, 0, 5, 2, 15, 13, 10, 14, 3, 6, 7, 1, 9, 4), Array(7, 9, 3, 1, 13, 12, 11, 14, 2, 6, 5, 10, 4, 0, 15, 8), Array(9, 0, 5, 7, 2, 4, 10, 15, 14, 1, 11, 12, 6, 8, 3, 13), Array(2, 12, 6, 10, 0, 11, 8, 3, 4, 13, 7, 5, 15, 14, 1, 9), Array(12, 5, 1, 15, 14, 13, 4, 10, 0, 7, 6, 3, 9, 2, 8, 11), Array(13, 11, 7, 14, 12, 1, 3, 9, 5, 0, 15, 4, 8, 6, 2, 10), Array(6, 15, 14, 9, 11, 3, 0, 8, 12, 2, 13, 7, 1, 4, 10, 5), Array(10, 2, 8, 4, 7, 6, 1, 5, 15, 11, 9, 14, 3, 12, 13, 0), Array(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15), Array(14, 10, 4, 8, 9, 15, 13, 6, 1, 12, 0, 2, 11, 7, 5, 3))
    BLOCKBYTES = 128
    OUTBYTES = 64
    KEYBYTES = 64
    #// 
    #// Turn two 32-bit integers into a fixed array representing a 64-bit integer.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int $high
    #// @param int $low
    #// @return ParagonIE_Sodium_Core32_Int64
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def new64(self, high_=None, low_=None):
        
        
        return ParagonIE_Sodium_Core32_Int64.fromints(low_, high_)
    # end def new64
    #// 
    #// Convert an arbitrary number into an SplFixedArray of two 32-bit integers
    #// that represents a 64-bit integer.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int $num
    #// @return ParagonIE_Sodium_Core32_Int64
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def to64(self, num_=None):
        
        
        hi_, lo_ = self.numericto64bitinteger(num_)
        return self.new64(hi_, lo_)
    # end def to64
    #// 
    #// Adds two 64-bit integers together, returning their sum as a SplFixedArray
    #// containing two 32-bit integers (representing a 64-bit integer).
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Int64 $x
    #// @param ParagonIE_Sodium_Core32_Int64 $y
    #// @return ParagonIE_Sodium_Core32_Int64
    #//
    def add64(self, x_=None, y_=None):
        
        
        return x_.addint64(y_)
    # end def add64
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Int64 $x
    #// @param ParagonIE_Sodium_Core32_Int64 $y
    #// @param ParagonIE_Sodium_Core32_Int64 $z
    #// @return ParagonIE_Sodium_Core32_Int64
    #//
    @classmethod
    def add364(self, x_=None, y_=None, z_=None):
        
        
        return x_.addint64(y_).addint64(z_)
    # end def add364
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Int64 $x
    #// @param ParagonIE_Sodium_Core32_Int64 $y
    #// @return ParagonIE_Sodium_Core32_Int64
    #// @throws TypeError
    #//
    @classmethod
    def xor64(self, x_=None, y_=None):
        
        
        return x_.xorint64(y_)
    # end def xor64
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param ParagonIE_Sodium_Core32_Int64 $x
    #// @param int $c
    #// @return ParagonIE_Sodium_Core32_Int64
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def rotr64(self, x_=None, c_=None):
        
        
        return x_.rotateright(c_)
    # end def rotr64
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param SplFixedArray $x
    #// @param int $i
    #// @return ParagonIE_Sodium_Core32_Int64
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def load64(self, x_=None, i_=None):
        
        
        #// @var int $l
        l_ = php_int(x_[i_]) | php_int(x_[i_ + 1]) << 8 | php_int(x_[i_ + 2]) << 16 | php_int(x_[i_ + 3]) << 24
        #// @var int $h
        h_ = php_int(x_[i_ + 4]) | php_int(x_[i_ + 5]) << 8 | php_int(x_[i_ + 6]) << 16 | php_int(x_[i_ + 7]) << 24
        return self.new64(h_, l_)
    # end def load64
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param SplFixedArray $x
    #// @param int $i
    #// @param ParagonIE_Sodium_Core32_Int64 $u
    #// @return void
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #// @psalm-suppress MixedAssignment
    #// @psalm-suppress MixedArrayAccess
    #// @psalm-suppress MixedArrayAssignment
    #// @psalm-suppress MixedArrayOffset
    #//
    @classmethod
    def store64(self, x_=None, i_=None, u_=None):
        
        
        v_ = copy.deepcopy(u_)
        maxLength_ = x_.getsize() - 1
        j_ = 0
        while j_ < 8:
            
            k_ = 3 - j_ >> 1
            x_[i_] = v_.limbs[k_] & 255
            i_ += 1
            i_ += 1
            if i_ > maxLength_:
                return
            # end if
            v_.limbs[k_] >>= 8
            j_ += 1
        # end while
    # end def store64
    #// 
    #// This just sets the $iv static variable.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @return void
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def pseudoconstructor(self):
        
        
        called_ = False
        if called_:
            return
        # end if
        self.iv = php_new_class("SplFixedArray", lambda : SplFixedArray(8))
        self.iv[0] = self.new64(1779033703, 4089235720)
        self.iv[1] = self.new64(3144134277, 2227873595)
        self.iv[2] = self.new64(1013904242, 4271175723)
        self.iv[3] = self.new64(2773480762, 1595750129)
        self.iv[4] = self.new64(1359893119, 2917565137)
        self.iv[5] = self.new64(2600822924, 725511199)
        self.iv[6] = self.new64(528734635, 4215389547)
        self.iv[7] = self.new64(1541459225, 327033209)
        called_ = True
    # end def pseudoconstructor
    #// 
    #// Returns a fresh BLAKE2 context.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @return SplFixedArray
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #// @psalm-suppress MixedAssignment
    #// @psalm-suppress MixedArrayAccess
    #// @psalm-suppress MixedArrayAssignment
    #// @psalm-suppress MixedArrayOffset
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def context(self):
        
        
        ctx_ = php_new_class("SplFixedArray", lambda : SplFixedArray(6))
        ctx_[0] = php_new_class("SplFixedArray", lambda : SplFixedArray(8))
        #// h
        ctx_[1] = php_new_class("SplFixedArray", lambda : SplFixedArray(2))
        #// t
        ctx_[2] = php_new_class("SplFixedArray", lambda : SplFixedArray(2))
        #// f
        ctx_[3] = php_new_class("SplFixedArray", lambda : SplFixedArray(256))
        #// buf
        ctx_[4] = 0
        #// buflen
        ctx_[5] = 0
        #// last_node (uint8_t)
        i_ = 8
        while i_ -= 1:
            
            ctx_[0][i_] = self.iv[i_]
            
        # end while
        i_ = 256
        while i_ -= 1:
            
            ctx_[3][i_] = 0
            
        # end while
        zero_ = self.new64(0, 0)
        ctx_[1][0] = zero_
        ctx_[1][1] = zero_
        ctx_[2][0] = zero_
        ctx_[2][1] = zero_
        return ctx_
    # end def context
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param SplFixedArray $ctx
    #// @param SplFixedArray $buf
    #// @return void
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #// @psalm-suppress MixedArrayAccess
    #// @psalm-suppress MixedArrayAssignment
    #// @psalm-suppress MixedAssignment
    #//
    def compress(self, ctx_=None, buf_=None):
        
        
        m_ = php_new_class("SplFixedArray", lambda : SplFixedArray(16))
        v_ = php_new_class("SplFixedArray", lambda : SplFixedArray(16))
        i_ = 16
        while i_ -= 1:
            
            m_[i_] = self.load64(buf_, i_ << 3)
            
        # end while
        i_ = 8
        while i_ -= 1:
            
            v_[i_] = ctx_[0][i_]
            
        # end while
        v_[8] = self.iv[0]
        v_[9] = self.iv[1]
        v_[10] = self.iv[2]
        v_[11] = self.iv[3]
        v_[12] = self.xor64(ctx_[1][0], self.iv[4])
        v_[13] = self.xor64(ctx_[1][1], self.iv[5])
        v_[14] = self.xor64(ctx_[2][0], self.iv[6])
        v_[15] = self.xor64(ctx_[2][1], self.iv[7])
        r_ = 0
        while r_ < 12:
            
            v_ = self.g(r_, 0, 0, 4, 8, 12, v_, m_)
            v_ = self.g(r_, 1, 1, 5, 9, 13, v_, m_)
            v_ = self.g(r_, 2, 2, 6, 10, 14, v_, m_)
            v_ = self.g(r_, 3, 3, 7, 11, 15, v_, m_)
            v_ = self.g(r_, 4, 0, 5, 10, 15, v_, m_)
            v_ = self.g(r_, 5, 1, 6, 11, 12, v_, m_)
            v_ = self.g(r_, 6, 2, 7, 8, 13, v_, m_)
            v_ = self.g(r_, 7, 3, 4, 9, 14, v_, m_)
            r_ += 1
        # end while
        i_ = 8
        while i_ -= 1:
            
            ctx_[0][i_] = self.xor64(ctx_[0][i_], self.xor64(v_[i_], v_[i_ + 8]))
            
        # end while
    # end def compress
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int $r
    #// @param int $i
    #// @param int $a
    #// @param int $b
    #// @param int $c
    #// @param int $d
    #// @param SplFixedArray $v
    #// @param SplFixedArray $m
    #// @return SplFixedArray
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #// @psalm-suppress MixedArrayOffset
    #//
    @classmethod
    def g(self, r_=None, i_=None, a_=None, b_=None, c_=None, d_=None, v_=None, m_=None):
        
        
        v_[a_] = self.add364(v_[a_], v_[b_], m_[self.sigma[r_][i_ << 1]])
        v_[d_] = self.rotr64(self.xor64(v_[d_], v_[a_]), 32)
        v_[c_] = self.add64(v_[c_], v_[d_])
        v_[b_] = self.rotr64(self.xor64(v_[b_], v_[c_]), 24)
        v_[a_] = self.add364(v_[a_], v_[b_], m_[self.sigma[r_][i_ << 1 + 1]])
        v_[d_] = self.rotr64(self.xor64(v_[d_], v_[a_]), 16)
        v_[c_] = self.add64(v_[c_], v_[d_])
        v_[b_] = self.rotr64(self.xor64(v_[b_], v_[c_]), 63)
        return v_
    # end def g
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param SplFixedArray $ctx
    #// @param int $inc
    #// @return void
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #// @psalm-suppress MixedArrayAccess
    #// @psalm-suppress MixedArrayAssignment
    #//
    @classmethod
    def increment_counter(self, ctx_=None, inc_=None):
        
        
        if inc_ < 0:
            raise php_new_class("SodiumException", lambda : SodiumException("Increasing by a negative number makes no sense."))
        # end if
        t_ = self.to64(inc_)
        #// # S->t is $ctx[1] in our implementation
        #// # S->t[0] = ( uint64_t )( t >> 0 );
        ctx_[1][0] = self.add64(ctx_[1][0], t_)
        #// # S->t[1] += ( S->t[0] < inc );
        if (not type(ctx_[1][0]).__name__ == "ParagonIE_Sodium_Core32_Int64"):
            raise php_new_class("TypeError", lambda : TypeError("Not an int64"))
        # end if
        #// @var ParagonIE_Sodium_Core32_Int64 $c
        c_ = ctx_[1][0]
        if c_.islessthanint(inc_):
            ctx_[1][1] = self.add64(ctx_[1][1], self.to64(1))
        # end if
    # end def increment_counter
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param SplFixedArray $ctx
    #// @param SplFixedArray $p
    #// @param int $plen
    #// @return void
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #// @psalm-suppress MixedAssignment
    #// @psalm-suppress MixedArrayAccess
    #// @psalm-suppress MixedArrayAssignment
    #// @psalm-suppress MixedArrayOffset
    #// @psalm-suppress MixedMethodCall
    #// @psalm-suppress MixedOperand
    #//
    @classmethod
    def update(self, ctx_=None, p_=None, plen_=None):
        
        
        self.pseudoconstructor()
        offset_ = 0
        while True:
            
            if not (plen_ > 0):
                break
            # end if
            left_ = ctx_[4]
            fill_ = 256 - left_
            if plen_ > fill_:
                #// # memcpy( S->buf + left, in, fill ); /* Fill buffer
                i_ = fill_
                while i_ -= 1:
                    
                    ctx_[3][i_ + left_] = p_[i_ + offset_]
                    
                # end while
                #// # S->buflen += fill;
                ctx_[4] += fill_
                #// # blake2b_increment_counter( S, BLAKE2B_BLOCKBYTES );
                self.increment_counter(ctx_, 128)
                #// # blake2b_compress( S, S->buf ); /* Compress
                self.compress(ctx_, ctx_[3])
                #// # memcpy( S->buf, S->buf + BLAKE2B_BLOCKBYTES, BLAKE2B_BLOCKBYTES ); /* Shift buffer left
                i_ = 128
                while i_ -= 1:
                    
                    ctx_[3][i_] = ctx_[3][i_ + 128]
                    
                # end while
                #// # S->buflen -= BLAKE2B_BLOCKBYTES;
                ctx_[4] -= 128
                #// # in += fill;
                offset_ += fill_
                #// # inlen -= fill;
                plen_ -= fill_
            else:
                i_ = plen_
                while i_ -= 1:
                    
                    ctx_[3][i_ + left_] = p_[i_ + offset_]
                    
                # end while
                ctx_[4] += plen_
                offset_ += plen_
                plen_ -= plen_
            # end if
        # end while
    # end def update
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param SplFixedArray $ctx
    #// @param SplFixedArray $out
    #// @return SplFixedArray
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #// @psalm-suppress MixedAssignment
    #// @psalm-suppress MixedArrayAccess
    #// @psalm-suppress MixedArrayAssignment
    #// @psalm-suppress MixedArrayOffset
    #// @psalm-suppress MixedMethodCall
    #// @psalm-suppress MixedOperand
    #//
    @classmethod
    def finish(self, ctx_=None, out_=None):
        
        
        self.pseudoconstructor()
        if ctx_[4] > 128:
            self.increment_counter(ctx_, 128)
            self.compress(ctx_, ctx_[3])
            ctx_[4] -= 128
            if ctx_[4] > 128:
                raise php_new_class("SodiumException", lambda : SodiumException("Failed to assert that buflen <= 128 bytes"))
            # end if
            i_ = ctx_[4]
            while i_ -= 1:
                
                ctx_[3][i_] = ctx_[3][i_ + 128]
                
            # end while
        # end if
        self.increment_counter(ctx_, ctx_[4])
        ctx_[2][0] = self.new64(4294967295, 4294967295)
        i_ = 256 - ctx_[4]
        while i_ -= 1:
            
            #// @var int $i
            ctx_[3][i_ + ctx_[4]] = 0
            
        # end while
        self.compress(ctx_, ctx_[3])
        i_ = php_int(out_.getsize() - 1 / 8)
        while i_ >= 0:
            
            self.store64(out_, i_ << 3, ctx_[0][i_])
            i_ -= 1
        # end while
        return out_
    # end def finish
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param SplFixedArray|null $key
    #// @param int $outlen
    #// @param SplFixedArray|null $salt
    #// @param SplFixedArray|null $personal
    #// @return SplFixedArray
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #// @psalm-suppress MixedAssignment
    #// @psalm-suppress MixedArrayAccess
    #// @psalm-suppress MixedArrayAssignment
    #// @psalm-suppress MixedMethodCall
    #//
    @classmethod
    def init(self, key_=None, outlen_=64, salt_=None, personal_=None):
        if key_ is None:
            key_ = None
        # end if
        if salt_ is None:
            salt_ = None
        # end if
        if personal_ is None:
            personal_ = None
        # end if
        
        self.pseudoconstructor()
        klen_ = 0
        if key_ != None:
            if php_count(key_) > 64:
                raise php_new_class("SodiumException", lambda : SodiumException("Invalid key size"))
            # end if
            klen_ = php_count(key_)
        # end if
        if outlen_ > 64:
            raise php_new_class("SodiumException", lambda : SodiumException("Invalid output size"))
        # end if
        ctx_ = self.context()
        p_ = php_new_class("SplFixedArray", lambda : SplFixedArray(64))
        #// Zero our param buffer...
        i_ = 64
        while i_:
            i_ -= 1
            p_[i_] = 0
            
        # end while
        p_[0] = outlen_
        #// digest_length
        p_[1] = klen_
        #// key_length
        p_[2] = 1
        #// fanout
        p_[3] = 1
        #// depth
        if type(salt_).__name__ == "SplFixedArray":
            #// salt: [32] through [47]
            i_ = 0
            while i_ < 16:
                
                p_[32 + i_] = php_int(salt_[i_])
                i_ += 1
            # end while
        # end if
        if type(personal_).__name__ == "SplFixedArray":
            #// personal: [48] through [63]
            i_ = 0
            while i_ < 16:
                
                p_[48 + i_] = php_int(personal_[i_])
                i_ += 1
            # end while
        # end if
        ctx_[0][0] = self.xor64(ctx_[0][0], self.load64(p_, 0))
        if type(salt_).__name__ == "SplFixedArray" or type(personal_).__name__ == "SplFixedArray":
            #// We need to do what blake2b_init_param() does:
            i_ = 1
            while i_ < 8:
                
                ctx_[0][i_] = self.xor64(ctx_[0][i_], self.load64(p_, i_ << 3))
                i_ += 1
            # end while
        # end if
        if klen_ > 0 and type(key_).__name__ == "SplFixedArray":
            block_ = php_new_class("SplFixedArray", lambda : SplFixedArray(128))
            i_ = 128
            while i_ -= 1:
                
                block_[i_] = 0
                
            # end while
            i_ = klen_
            while i_ -= 1:
                
                block_[i_] = key_[i_]
                
            # end while
            self.update(ctx_, block_, 128)
            ctx_[4] = 128
        # end if
        return ctx_
    # end def init
    #// 
    #// Convert a string into an SplFixedArray of integers
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $str
    #// @return SplFixedArray
    #//
    @classmethod
    def stringtosplfixedarray(self, str_=""):
        
        
        values_ = unpack("C*", str_)
        return SplFixedArray.fromarray(php_array_values(values_))
    # end def stringtosplfixedarray
    #// 
    #// Convert an SplFixedArray of integers into a string
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param SplFixedArray $a
    #// @return string
    #//
    @classmethod
    def splfixedarraytostring(self, a_=None):
        
        
        #// 
        #// @var array<int, string|int>
        #//
        arr_ = a_.toarray()
        c_ = a_.count()
        array_unshift(arr_, php_str_repeat("C", c_))
        return php_str(call_user_func_array("pack", arr_))
    # end def splfixedarraytostring
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param SplFixedArray $ctx
    #// @return string
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #// @psalm-suppress MixedArrayAccess
    #// @psalm-suppress MixedArrayAssignment
    #// @psalm-suppress MixedMethodCall
    #//
    @classmethod
    def contexttostring(self, ctx_=None):
        
        
        str_ = ""
        #// @var array<int, ParagonIE_Sodium_Core32_Int64> $ctxA
        ctxA_ = ctx_[0].toarray()
        #// # uint64_t h[8];
        i_ = 0
        while i_ < 8:
            
            if (not type(ctxA_[i_]).__name__ == "ParagonIE_Sodium_Core32_Int64"):
                raise php_new_class("TypeError", lambda : TypeError("Not an instance of Int64"))
            # end if
            #// @var ParagonIE_Sodium_Core32_Int64 $ctxAi
            ctxAi_ = ctxA_[i_]
            str_ += ctxAi_.toreversestring()
            i_ += 1
        # end while
        #// # uint64_t t[2];
        #// # uint64_t f[2];
        i_ = 1
        while i_ < 3:
            
            #// @var array<int, ParagonIE_Sodium_Core32_Int64> $ctxA
            ctxA_ = ctx_[i_].toarray()
            #// @var ParagonIE_Sodium_Core32_Int64 $ctxA1
            ctxA1_ = ctxA_[0]
            #// @var ParagonIE_Sodium_Core32_Int64 $ctxA2
            ctxA2_ = ctxA_[1]
            str_ += ctxA1_.toreversestring()
            str_ += ctxA2_.toreversestring()
            i_ += 1
        # end while
        #// # uint8_t buf[2 * 128];
        str_ += self.splfixedarraytostring(ctx_[3])
        #// @var int $ctx4
        ctx4_ = ctx_[4]
        #// # size_t buflen;
        str_ += php_implode("", Array(self.inttochr(ctx4_ & 255), self.inttochr(ctx4_ >> 8 & 255), self.inttochr(ctx4_ >> 16 & 255), self.inttochr(ctx4_ >> 24 & 255), "    "))
        #// # uint8_t last_node;
        return str_ + self.inttochr(ctx_[5]) + php_str_repeat(" ", 23)
    # end def contexttostring
    #// 
    #// Creates an SplFixedArray containing other SplFixedArray elements, from
    #// a string (compatible with \Sodium\crypto_generichash_{init, update, final})
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param string $string
    #// @return SplFixedArray
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArrayAccess
    #// @psalm-suppress MixedArrayAssignment
    #//
    @classmethod
    def stringtocontext(self, string_=None):
        
        
        ctx_ = self.context()
        #// # uint64_t h[8];
        i_ = 0
        while i_ < 8:
            
            ctx_[0][i_] = ParagonIE_Sodium_Core32_Int64.fromreversestring(self.substr(string_, i_ << 3 + 0, 8))
            i_ += 1
        # end while
        #// # uint64_t t[2];
        #// # uint64_t f[2];
        i_ = 1
        while i_ < 3:
            
            ctx_[i_][1] = ParagonIE_Sodium_Core32_Int64.fromreversestring(self.substr(string_, 72 + i_ - 1 << 4, 8))
            ctx_[i_][0] = ParagonIE_Sodium_Core32_Int64.fromreversestring(self.substr(string_, 64 + i_ - 1 << 4, 8))
            i_ += 1
        # end while
        #// # uint8_t buf[2 * 128];
        ctx_[3] = self.stringtosplfixedarray(self.substr(string_, 96, 256))
        #// # uint8_t buf[2 * 128];
        int_ = 0
        i_ = 0
        while i_ < 8:
            
            int_ |= self.chrtoint(string_[352 + i_]) << i_ << 3
            i_ += 1
        # end while
        ctx_[4] = int_
        return ctx_
    # end def stringtocontext
# end class ParagonIE_Sodium_Core32_BLAKE2b
