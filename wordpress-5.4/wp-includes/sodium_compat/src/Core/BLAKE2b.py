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
if php_class_exists("ParagonIE_Sodium_Core_BLAKE2b", False):
    sys.exit(-1)
# end if
#// 
#// Class ParagonIE_Sodium_Core_BLAKE2b
#// 
#// Based on the work of Devi Mandiri in devi/salt.
#//
class ParagonIE_Sodium_Core_BLAKE2b(ParagonIE_Sodium_Core_Util):
    iv = Array()
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
    #// @return SplFixedArray
    #// @psalm-suppress MixedAssignment
    #//
    @classmethod
    def new64(self, high=None, low=None):
        
        i64 = php_new_class("SplFixedArray", lambda : SplFixedArray(2))
        i64[0] = high & 4294967295
        i64[1] = low & 4294967295
        return i64
    # end def new64
    #// 
    #// Convert an arbitrary number into an SplFixedArray of two 32-bit integers
    #// that represents a 64-bit integer.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param int $num
    #// @return SplFixedArray
    #//
    def to64(self, num=None):
        
        hi, lo = self.numericto64bitinteger(num)
        return self.new64(hi, lo)
    # end def to64
    #// 
    #// Adds two 64-bit integers together, returning their sum as a SplFixedArray
    #// containing two 32-bit integers (representing a 64-bit integer).
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param SplFixedArray $x
    #// @param SplFixedArray $y
    #// @return SplFixedArray
    #// @psalm-suppress MixedArgument
    #// @psalm-suppress MixedAssignment
    #// @psalm-suppress MixedOperand
    #//
    def add64(self, x=None, y=None):
        
        l = x[1] + y[1] & 4294967295
        return self.new64(php_int(x[0] + y[0] + 1 if l < x[1] else 0), php_int(l))
    # end def add64
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param SplFixedArray $x
    #// @param SplFixedArray $y
    #// @param SplFixedArray $z
    #// @return SplFixedArray
    #//
    def add364(self, x=None, y=None, z=None):
        
        return self.add64(x, self.add64(y, z))
    # end def add364
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param SplFixedArray $x
    #// @param SplFixedArray $y
    #// @return SplFixedArray
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def xor64(self, x=None, y=None):
        
        if (not php_is_numeric(x[0])):
            raise php_new_class("SodiumException", lambda : SodiumException("x[0] is not an integer"))
        # end if
        if (not php_is_numeric(x[1])):
            raise php_new_class("SodiumException", lambda : SodiumException("x[1] is not an integer"))
        # end if
        if (not php_is_numeric(y[0])):
            raise php_new_class("SodiumException", lambda : SodiumException("y[0] is not an integer"))
        # end if
        if (not php_is_numeric(y[1])):
            raise php_new_class("SodiumException", lambda : SodiumException("y[1] is not an integer"))
        # end if
        return self.new64(php_int(x[0] ^ y[0] & 4294967295), php_int(x[1] ^ y[1] & 4294967295))
    # end def xor64
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param SplFixedArray $x
    #// @param int $c
    #// @return SplFixedArray
    #// @psalm-suppress MixedAssignment
    #//
    @classmethod
    def rotr64(self, x=None, c=None):
        
        if c >= 64:
            c %= 64
        # end if
        if c >= 32:
            #// @var int $tmp
            tmp = x[0]
            x[0] = x[1]
            x[1] = tmp
            c -= 32
        # end if
        if c == 0:
            return x
        # end if
        l0 = 0
        c = 64 - c
        if c < 32:
            #// @var int $h0
            h0 = php_int(x[0]) << c | php_int(x[1]) & 1 << c - 1 << 32 - c >> 32 - c
            #// @var int $l0
            l0 = php_int(x[1]) << c
        else:
            #// @var int $h0
            h0 = php_int(x[1]) << c - 32
        # end if
        h1 = 0
        c1 = 64 - c
        if c1 < 32:
            #// @var int $h1
            h1 = php_int(x[0]) >> c1
            #// @var int $l1
            l1 = php_int(x[1]) >> c1 | php_int(x[0]) & 1 << c1 - 1 << 32 - c1
        else:
            #// @var int $l1
            l1 = php_int(x[0]) >> c1 - 32
        # end if
        return self.new64(h0 | h1, l0 | l1)
    # end def rotr64
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param SplFixedArray $x
    #// @return int
    #// @psalm-suppress MixedOperand
    #//
    def flatten64(self, x=None):
        
        return php_int(x[0] * 4294967296 + x[1])
    # end def flatten64
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param SplFixedArray $x
    #// @param int $i
    #// @return SplFixedArray
    #// @psalm-suppress MixedArgument
    #// @psalm-suppress MixedArrayOffset
    #//
    def load64(self, x=None, i=None):
        
        #// @var int $l
        l = php_int(x[i]) | php_int(x[i + 1]) << 8 | php_int(x[i + 2]) << 16 | php_int(x[i + 3]) << 24
        #// @var int $h
        h = php_int(x[i + 4]) | php_int(x[i + 5]) << 8 | php_int(x[i + 6]) << 16 | php_int(x[i + 7]) << 24
        return self.new64(h, l)
    # end def load64
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param SplFixedArray $x
    #// @param int $i
    #// @param SplFixedArray $u
    #// @return void
    #// @psalm-suppress MixedAssignment
    #//
    def store64(self, x=None, i=None, u=None):
        
        maxLength = x.getsize() - 1
        j = 0
        while j < 8:
            
            #// 
            #// [0, 1, 2, 3, 4, 5, 6, 7]
            #// ... becomes ...
            #// [0, 0, 0, 0, 1, 1, 1, 1]
            #// 
            #// @var int $uIdx
            uIdx = 7 - j & 4 >> 2
            x[i] = php_int(u[uIdx]) & 255
            i += 1
            if i > maxLength:
                return
            # end if
            #// @psalm-suppress MixedOperand
            u[uIdx] >>= 8
            j += 1
        # end while
    # end def store64
    #// 
    #// This just sets the $iv static variable.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @return void
    #//
    @classmethod
    def pseudoconstructor(self):
        
        pseudoconstructor.called = False
        if pseudoconstructor.called:
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
        pseudoconstructor.called = True
    # end def pseudoconstructor
    #// 
    #// Returns a fresh BLAKE2 context.
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @return SplFixedArray
    #// @psalm-suppress MixedAssignment
    #// @psalm-suppress MixedArrayAccess
    #// @psalm-suppress MixedArrayAssignment
    #//
    def context(self):
        
        ctx = php_new_class("SplFixedArray", lambda : SplFixedArray(6))
        ctx[0] = php_new_class("SplFixedArray", lambda : SplFixedArray(8))
        #// h
        ctx[1] = php_new_class("SplFixedArray", lambda : SplFixedArray(2))
        #// t
        ctx[2] = php_new_class("SplFixedArray", lambda : SplFixedArray(2))
        #// f
        ctx[3] = php_new_class("SplFixedArray", lambda : SplFixedArray(256))
        #// buf
        ctx[4] = 0
        #// buflen
        ctx[5] = 0
        #// last_node (uint8_t)
        i = 8
        while i -= 1:
            
            ctx[0][i] = self.iv[i]
            
        # end while
        i = 256
        while i -= 1:
            
            ctx[3][i] = 0
            
        # end while
        zero = self.new64(0, 0)
        ctx[1][0] = zero
        ctx[1][1] = zero
        ctx[2][0] = zero
        ctx[2][1] = zero
        return ctx
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
    #// @psalm-suppress MixedAssignment
    #// @psalm-suppress MixedArrayAccess
    #// @psalm-suppress MixedArrayAssignment
    #// @psalm-suppress MixedArrayOffset
    #//
    def compress(self, ctx=None, buf=None):
        
        m = php_new_class("SplFixedArray", lambda : SplFixedArray(16))
        v = php_new_class("SplFixedArray", lambda : SplFixedArray(16))
        i = 16
        while i -= 1:
            
            m[i] = self.load64(buf, i << 3)
            
        # end while
        i = 8
        while i -= 1:
            
            v[i] = ctx[0][i]
            
        # end while
        v[8] = self.iv[0]
        v[9] = self.iv[1]
        v[10] = self.iv[2]
        v[11] = self.iv[3]
        v[12] = self.xor64(ctx[1][0], self.iv[4])
        v[13] = self.xor64(ctx[1][1], self.iv[5])
        v[14] = self.xor64(ctx[2][0], self.iv[6])
        v[15] = self.xor64(ctx[2][1], self.iv[7])
        r = 0
        while r < 12:
            
            v = self.g(r, 0, 0, 4, 8, 12, v, m)
            v = self.g(r, 1, 1, 5, 9, 13, v, m)
            v = self.g(r, 2, 2, 6, 10, 14, v, m)
            v = self.g(r, 3, 3, 7, 11, 15, v, m)
            v = self.g(r, 4, 0, 5, 10, 15, v, m)
            v = self.g(r, 5, 1, 6, 11, 12, v, m)
            v = self.g(r, 6, 2, 7, 8, 13, v, m)
            v = self.g(r, 7, 3, 4, 9, 14, v, m)
            r += 1
        # end while
        i = 8
        while i -= 1:
            
            ctx[0][i] = self.xor64(ctx[0][i], self.xor64(v[i], v[i + 8]))
            
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
    def g(self, r=None, i=None, a=None, b=None, c=None, d=None, v=None, m=None):
        
        v[a] = self.add364(v[a], v[b], m[self.sigma[r][i << 1]])
        v[d] = self.rotr64(self.xor64(v[d], v[a]), 32)
        v[c] = self.add64(v[c], v[d])
        v[b] = self.rotr64(self.xor64(v[b], v[c]), 24)
        v[a] = self.add364(v[a], v[b], m[self.sigma[r][i << 1 + 1]])
        v[d] = self.rotr64(self.xor64(v[d], v[a]), 16)
        v[c] = self.add64(v[c], v[d])
        v[b] = self.rotr64(self.xor64(v[b], v[c]), 63)
        return v
    # end def g
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param SplFixedArray $ctx
    #// @param int $inc
    #// @return void
    #// @throws SodiumException
    #// @psalm-suppress MixedArgument
    #// @psalm-suppress MixedArrayAccess
    #// @psalm-suppress MixedArrayAssignment
    #//
    @classmethod
    def increment_counter(self, ctx=None, inc=None):
        
        if inc < 0:
            raise php_new_class("SodiumException", lambda : SodiumException("Increasing by a negative number makes no sense."))
        # end if
        t = self.to64(inc)
        #// # S->t is $ctx[1] in our implementation
        #// # S->t[0] = ( uint64_t )( t >> 0 );
        ctx[1][0] = self.add64(ctx[1][0], t)
        #// # S->t[1] += ( S->t[0] < inc );
        if self.flatten64(ctx[1][0]) < inc:
            ctx[1][1] = self.add64(ctx[1][1], self.to64(1))
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
    #// @psalm-suppress MixedOperand
    #//
    @classmethod
    def update(self, ctx=None, p=None, plen=None):
        
        self.pseudoconstructor()
        offset = 0
        while True:
            
            if not (plen > 0):
                break
            # end if
            left = ctx[4]
            fill = 256 - left
            if plen > fill:
                #// # memcpy( S->buf + left, in, fill ); /* Fill buffer
                i = fill
                while i -= 1:
                    
                    ctx[3][i + left] = p[i + offset]
                    
                # end while
                #// # S->buflen += fill;
                ctx[4] += fill
                #// # blake2b_increment_counter( S, BLAKE2B_BLOCKBYTES );
                self.increment_counter(ctx, 128)
                #// # blake2b_compress( S, S->buf ); /* Compress
                self.compress(ctx, ctx[3])
                #// # memcpy( S->buf, S->buf + BLAKE2B_BLOCKBYTES, BLAKE2B_BLOCKBYTES ); /* Shift buffer left
                i = 128
                while i -= 1:
                    
                    ctx[3][i] = ctx[3][i + 128]
                    
                # end while
                #// # S->buflen -= BLAKE2B_BLOCKBYTES;
                ctx[4] -= 128
                #// # in += fill;
                offset += fill
                #// # inlen -= fill;
                plen -= fill
            else:
                i = plen
                while i -= 1:
                    
                    ctx[3][i + left] = p[i + offset]
                    
                # end while
                ctx[4] += plen
                offset += plen
                plen -= plen
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
    #// @psalm-suppress MixedOperand
    #//
    @classmethod
    def finish(self, ctx=None, out=None):
        
        self.pseudoconstructor()
        if ctx[4] > 128:
            self.increment_counter(ctx, 128)
            self.compress(ctx, ctx[3])
            ctx[4] -= 128
            if ctx[4] > 128:
                raise php_new_class("SodiumException", lambda : SodiumException("Failed to assert that buflen <= 128 bytes"))
            # end if
            i = ctx[4]
            while i -= 1:
                
                ctx[3][i] = ctx[3][i + 128]
                
            # end while
        # end if
        self.increment_counter(ctx, ctx[4])
        ctx[2][0] = self.new64(4294967295, 4294967295)
        i = 256 - ctx[4]
        while i -= 1:
            
            ctx[3][i + ctx[4]] = 0
            
        # end while
        self.compress(ctx, ctx[3])
        i = php_int(out.getsize() - 1 / 8)
        while i >= 0:
            
            self.store64(out, i << 3, ctx[0][i])
            i -= 1
        # end while
        return out
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
    #// @psalm-suppress MixedArrayOffset
    #//
    @classmethod
    def init(self, key=None, outlen=64, salt=None, personal=None):
        
        self.pseudoconstructor()
        klen = 0
        if key != None:
            if php_count(key) > 64:
                raise php_new_class("SodiumException", lambda : SodiumException("Invalid key size"))
            # end if
            klen = php_count(key)
        # end if
        if outlen > 64:
            raise php_new_class("SodiumException", lambda : SodiumException("Invalid output size"))
        # end if
        ctx = self.context()
        p = php_new_class("SplFixedArray", lambda : SplFixedArray(64))
        #// Zero our param buffer...
        i = 64
        while i -= 1:
            
            p[i] = 0
            
        # end while
        p[0] = outlen
        #// digest_length
        p[1] = klen
        #// key_length
        p[2] = 1
        #// fanout
        p[3] = 1
        #// depth
        if type(salt).__name__ == "SplFixedArray":
            #// salt: [32] through [47]
            i = 0
            while i < 16:
                
                p[32 + i] = php_int(salt[i])
                i += 1
            # end while
        # end if
        if type(personal).__name__ == "SplFixedArray":
            #// personal: [48] through [63]
            i = 0
            while i < 16:
                
                p[48 + i] = php_int(personal[i])
                i += 1
            # end while
        # end if
        ctx[0][0] = self.xor64(ctx[0][0], self.load64(p, 0))
        if type(salt).__name__ == "SplFixedArray" or type(personal).__name__ == "SplFixedArray":
            #// We need to do what blake2b_init_param() does:
            i = 1
            while i < 8:
                
                ctx[0][i] = self.xor64(ctx[0][i], self.load64(p, i << 3))
                i += 1
            # end while
        # end if
        if klen > 0 and type(key).__name__ == "SplFixedArray":
            block = php_new_class("SplFixedArray", lambda : SplFixedArray(128))
            i = 128
            while i -= 1:
                
                block[i] = 0
                
            # end while
            i = klen
            while i -= 1:
                
                block[i] = key[i]
                
            # end while
            self.update(ctx, block, 128)
            ctx[4] = 128
        # end if
        return ctx
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
    def stringtosplfixedarray(self, str=""):
        
        values = unpack("C*", str)
        return SplFixedArray.fromarray(php_array_values(values))
    # end def stringtosplfixedarray
    #// 
    #// Convert an SplFixedArray of integers into a string
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param SplFixedArray $a
    #// @return string
    #// @throws TypeError
    #//
    @classmethod
    def splfixedarraytostring(self, a=None):
        
        #// 
        #// @var array<int, int|string> $arr
        #//
        arr = a.toarray()
        c = a.count()
        array_unshift(arr, php_str_repeat("C", c))
        return php_str(call_user_func_array("pack", arr))
    # end def splfixedarraytostring
    #// 
    #// @internal You should not use this directly from another application
    #// 
    #// @param SplFixedArray $ctx
    #// @return string
    #// @throws TypeError
    #// @psalm-suppress MixedArgument
    #// @psalm-suppress MixedAssignment
    #// @psalm-suppress MixedArrayAccess
    #// @psalm-suppress MixedArrayAssignment
    #// @psalm-suppress MixedArrayOffset
    #// @psalm-suppress MixedMethodCall
    #//
    @classmethod
    def contexttostring(self, ctx=None):
        
        str = ""
        #// @var array<int, array<int, int>> $ctxA
        ctxA = ctx[0].toarray()
        #// # uint64_t h[8];
        i = 0
        while i < 8:
            
            str += self.store32_le(ctxA[i][1])
            str += self.store32_le(ctxA[i][0])
            i += 1
        # end while
        #// # uint64_t t[2];
        #// # uint64_t f[2];
        i = 1
        while i < 3:
            
            ctxA = ctx[i].toarray()
            str += self.store32_le(ctxA[0][1])
            str += self.store32_le(ctxA[0][0])
            str += self.store32_le(ctxA[1][1])
            str += self.store32_le(ctxA[1][0])
            i += 1
        # end while
        #// # uint8_t buf[2 * 128];
        str += self.splfixedarraytostring(ctx[3])
        #// @var int $ctx4
        ctx4 = php_int(ctx[4])
        #// # size_t buflen;
        str += php_implode("", Array(self.inttochr(ctx4 & 255), self.inttochr(ctx4 >> 8 & 255), self.inttochr(ctx4 >> 16 & 255), self.inttochr(ctx4 >> 24 & 255), self.inttochr(ctx4 >> 32 & 255), self.inttochr(ctx4 >> 40 & 255), self.inttochr(ctx4 >> 48 & 255), self.inttochr(ctx4 >> 56 & 255)))
        #// # uint8_t last_node;
        return str + self.inttochr(ctx[5]) + php_str_repeat(" ", 23)
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
    #// @psalm-suppress MixedArrayAssignment
    #//
    @classmethod
    def stringtocontext(self, string=None):
        
        ctx = self.context()
        #// # uint64_t h[8];
        i = 0
        while i < 8:
            
            ctx[0][i] = SplFixedArray.fromarray(Array(self.load_4(self.substr(string, i << 3 + 4, 4)), self.load_4(self.substr(string, i << 3 + 0, 4))))
            i += 1
        # end while
        #// # uint64_t t[2];
        #// # uint64_t f[2];
        i = 1
        while i < 3:
            
            ctx[i][1] = SplFixedArray.fromarray(Array(self.load_4(self.substr(string, 76 + i - 1 << 4, 4)), self.load_4(self.substr(string, 72 + i - 1 << 4, 4))))
            ctx[i][0] = SplFixedArray.fromarray(Array(self.load_4(self.substr(string, 68 + i - 1 << 4, 4)), self.load_4(self.substr(string, 64 + i - 1 << 4, 4))))
            i += 1
        # end while
        #// # uint8_t buf[2 * 128];
        ctx[3] = self.stringtosplfixedarray(self.substr(string, 96, 256))
        #// # uint8_t buf[2 * 128];
        int = 0
        i = 0
        while i < 8:
            
            int |= self.chrtoint(string[352 + i]) << i << 3
            i += 1
        # end while
        ctx[4] = int
        return ctx
    # end def stringtocontext
# end class ParagonIE_Sodium_Core_BLAKE2b
