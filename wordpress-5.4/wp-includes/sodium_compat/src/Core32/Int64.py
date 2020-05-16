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
#// 
#// Class ParagonIE_Sodium_Core32_Int64
#// 
#// Encapsulates a 64-bit integer.
#// 
#// These are immutable. It always returns a new instance.
#//
class ParagonIE_Sodium_Core32_Int64():
    limbs = Array(0, 0, 0, 0)
    overflow = 0
    unsignedInt = False
    #// 
    #// ParagonIE_Sodium_Core32_Int64 constructor.
    #// @param array $array
    #// @param bool $unsignedInt
    #//
    def __init__(self, array=Array(0, 0, 0, 0), unsignedInt=False):
        
        self.limbs = Array(php_int(array[0]), php_int(array[1]), php_int(array[2]), php_int(array[3]))
        self.overflow = 0
        self.unsignedInt = unsignedInt
    # end def __init__
    #// 
    #// Adds two int64 objects
    #// 
    #// @param ParagonIE_Sodium_Core32_Int64 $addend
    #// @return ParagonIE_Sodium_Core32_Int64
    #//
    def addint64(self, addend=None):
        
        i0 = self.limbs[0]
        i1 = self.limbs[1]
        i2 = self.limbs[2]
        i3 = self.limbs[3]
        j0 = addend.limbs[0]
        j1 = addend.limbs[1]
        j2 = addend.limbs[2]
        j3 = addend.limbs[3]
        r3 = i3 + j3 & 65535
        carry = r3 >> 16
        r2 = i2 + j2 & 65535 + carry
        carry = r2 >> 16
        r1 = i1 + j1 & 65535 + carry
        carry = r1 >> 16
        r0 = i0 + j0 & 65535 + carry
        carry = r0 >> 16
        r0 &= 65535
        r1 &= 65535
        r2 &= 65535
        r3 &= 65535
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64(Array(r0, r1, r2, r3)))
        return_.overflow = carry
        return_.unsignedInt = self.unsignedInt
        return return_
    # end def addint64
    #// 
    #// Adds a normal integer to an int64 object
    #// 
    #// @param int $int
    #// @return ParagonIE_Sodium_Core32_Int64
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def addint(self, int=None):
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(int, "int", 1)
        #// @var int $int
        int = php_int(int)
        i0 = self.limbs[0]
        i1 = self.limbs[1]
        i2 = self.limbs[2]
        i3 = self.limbs[3]
        r3 = i3 + int & 65535
        carry = r3 >> 16
        r2 = i2 + int >> 16 & 65535 + carry
        carry = r2 >> 16
        r1 = i1 + carry
        carry = r1 >> 16
        r0 = i0 + carry
        carry = r0 >> 16
        r0 &= 65535
        r1 &= 65535
        r2 &= 65535
        r3 &= 65535
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64(Array(r0, r1, r2, r3)))
        return_.overflow = carry
        return_.unsignedInt = self.unsignedInt
        return return_
    # end def addint
    #// 
    #// @param int $b
    #// @return int
    #//
    def compareint(self, b=0):
        
        gt = 0
        eq = 1
        i = 4
        j = 0
        while True:
            
            if not (i > 0):
                break
            # end if
            i -= 1
            #// @var int $x1
            x1 = self.limbs[i]
            #// @var int $x2
            x2 = b >> j << 4 & 65535
            #// int
            gt |= x2 - x1 >> 8 & eq
            #// int
            eq &= x2 ^ x1 - 1 >> 8
        # end while
        return gt + gt - eq + 1
    # end def compareint
    #// 
    #// @param int $b
    #// @return bool
    #//
    def isgreaterthan(self, b=0):
        
        return self.compareint(b) > 0
    # end def isgreaterthan
    #// 
    #// @param int $b
    #// @return bool
    #//
    def islessthanint(self, b=0):
        
        return self.compareint(b) < 0
    # end def islessthanint
    #// 
    #// @param int $hi
    #// @param int $lo
    #// @return ParagonIE_Sodium_Core32_Int64
    #//
    def mask64(self, hi=0, lo=0):
        
        #// @var int $a
        a = hi >> 16 & 65535
        #// @var int $b
        b = hi & 65535
        #// @var int $c
        c = lo >> 16 & 65535
        #// @var int $d
        d = lo & 65535
        return php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64(Array(self.limbs[0] & a, self.limbs[1] & b, self.limbs[2] & c, self.limbs[3] & d), self.unsignedInt))
    # end def mask64
    #// 
    #// @param int $int
    #// @param int $size
    #// @return ParagonIE_Sodium_Core32_Int64
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedAssignment
    #//
    def mulint(self, int=0, size=0):
        
        if ParagonIE_Sodium_Compat.fastMult:
            return self.mulintfast(int)
        # end if
        ParagonIE_Sodium_Core32_Util.declarescalartype(int, "int", 1)
        ParagonIE_Sodium_Core32_Util.declarescalartype(size, "int", 2)
        #// @var int $int
        int = php_int(int)
        #// @var int $size
        size = php_int(size)
        if (not size):
            size = 63
        # end if
        a = copy.deepcopy(self)
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        return_.unsignedInt = self.unsignedInt
        #// Initialize:
        ret0 = 0
        ret1 = 0
        ret2 = 0
        ret3 = 0
        a0 = a.limbs[0]
        a1 = a.limbs[1]
        a2 = a.limbs[2]
        a3 = a.limbs[3]
        #// @var int $size
        #// @var int $i
        i = size
        while i >= 0:
            
            mask = -int & 1
            x0 = a0 & mask
            x1 = a1 & mask
            x2 = a2 & mask
            x3 = a3 & mask
            ret3 += x3
            c = ret3 >> 16
            ret2 += x2 + c
            c = ret2 >> 16
            ret1 += x1 + c
            c = ret1 >> 16
            ret0 += x0 + c
            ret0 &= 65535
            ret1 &= 65535
            ret2 &= 65535
            ret3 &= 65535
            a3 = a3 << 1
            x3 = a3 >> 16
            a2 = a2 << 1 | x3
            x2 = a2 >> 16
            a1 = a1 << 1 | x2
            x1 = a1 >> 16
            a0 = a0 << 1 | x1
            a0 &= 65535
            a1 &= 65535
            a2 &= 65535
            a3 &= 65535
            int >>= 1
            i -= 1
        # end while
        return_.limbs[0] = ret0
        return_.limbs[1] = ret1
        return_.limbs[2] = ret2
        return_.limbs[3] = ret3
        return return_
    # end def mulint
    #// 
    #// @param ParagonIE_Sodium_Core32_Int64 $A
    #// @param ParagonIE_Sodium_Core32_Int64 $B
    #// @return array<int, ParagonIE_Sodium_Core32_Int64>
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedInferredReturnType
    #//
    @classmethod
    def ctselect(self, A=None, B=None):
        
        a = copy.deepcopy(A)
        b = copy.deepcopy(B)
        #// @var int $aNeg
        aNeg = a.limbs[0] >> 15 & 1
        #// @var int $bNeg
        bNeg = b.limbs[0] >> 15 & 1
        #// @var int $m
        m = -aNeg & bNeg | 1
        #// @var int $swap
        swap = bNeg & (1 << (aNeg).bit_length()) - 1 - aNeg
        #// @var int $d
        d = -swap
        #// 
        #// if ($bNeg && !$aNeg) {
        #// $a = clone $int;
        #// $b = clone $this;
        #// } elseif($bNeg && $aNeg) {
        #// $a = $this->mulInt(-1);
        #// $b = $int->mulInt(-1);
        #// }
        #//
        x = a.xorint64(b).mask64(d, d)
        return Array(a.xorint64(x).mulint(m), b.xorint64(x).mulint(m))
    # end def ctselect
    #// 
    #// @param array<int, int> $a
    #// @param array<int, int> $b
    #// @param int $baseLog2
    #// @return array<int, int>
    #//
    def multiplylong(self, a=None, b=None, baseLog2=16):
        
        a_l = php_count(a)
        b_l = php_count(b)
        #// @var array<int, int> $r
        r = array_fill(0, a_l + b_l + 1, 0)
        base = 1 << baseLog2
        i = 0
        while i < a_l:
            
            a_i = a[i]
            j = 0
            while j < a_l:
                
                b_j = b[j]
                product = a_i * b_j + r[i + j]
                carry = product >> baseLog2 & 65535
                r[i + j] = product - php_int(carry * base) & 65535
                r[i + j + 1] += carry
                j += 1
            # end while
            i += 1
        # end while
        return php_array_slice(r, 0, 5)
    # end def multiplylong
    #// 
    #// @param int $int
    #// @return ParagonIE_Sodium_Core32_Int64
    #//
    def mulintfast(self, int=None):
        
        #// Handle negative numbers
        aNeg = self.limbs[0] >> 15 & 1
        bNeg = int >> 31 & 1
        a = array_reverse(self.limbs)
        b = Array(int & 65535, int >> 16 & 65535, -bNeg & 65535, -bNeg & 65535)
        if aNeg:
            i = 0
            while i < 4:
                
                a[i] = a[i] ^ 65535 & 65535
                i += 1
            # end while
            a[0] += 1
        # end if
        if bNeg:
            i = 0
            while i < 4:
                
                b[i] = b[i] ^ 65535 & 65535
                i += 1
            # end while
            b[0] += 1
        # end if
        #// Multiply
        res = self.multiplylong(a, b)
        #// Re-apply negation to results
        if aNeg != bNeg:
            i = 0
            while i < 4:
                
                res[i] = 65535 ^ res[i] & 65535
                i += 1
            # end while
            #// Handle integer overflow
            c = 1
            i = 0
            while i < 4:
                
                res[i] += c
                c = res[i] >> 16
                res[i] &= 65535
                i += 1
            # end while
        # end if
        #// Return our values
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        return_.limbs = Array(res[3] & 65535, res[2] & 65535, res[1] & 65535, res[0] & 65535)
        if php_count(res) > 4:
            return_.overflow = res[4] & 65535
        # end if
        return_.unsignedInt = self.unsignedInt
        return return_
    # end def mulintfast
    #// 
    #// @param ParagonIE_Sodium_Core32_Int64 $right
    #// @return ParagonIE_Sodium_Core32_Int64
    #//
    def mulint64fast(self, right=None):
        
        aNeg = self.limbs[0] >> 15 & 1
        bNeg = right.limbs[0] >> 15 & 1
        a = array_reverse(self.limbs)
        b = array_reverse(right.limbs)
        if aNeg:
            i = 0
            while i < 4:
                
                a[i] = a[i] ^ 65535 & 65535
                i += 1
            # end while
            a[0] += 1
        # end if
        if bNeg:
            i = 0
            while i < 4:
                
                b[i] = b[i] ^ 65535 & 65535
                i += 1
            # end while
            b[0] += 1
        # end if
        res = self.multiplylong(a, b)
        if aNeg != bNeg:
            if aNeg != bNeg:
                i = 0
                while i < 4:
                    
                    res[i] = res[i] ^ 65535 & 65535
                    i += 1
                # end while
                c = 1
                i = 0
                while i < 4:
                    
                    res[i] += c
                    c = res[i] >> 16
                    res[i] &= 65535
                    i += 1
                # end while
            # end if
        # end if
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        return_.limbs = Array(res[3] & 65535, res[2] & 65535, res[1] & 65535, res[0] & 65535)
        if php_count(res) > 4:
            return_.overflow = res[4]
        # end if
        return return_
    # end def mulint64fast
    #// 
    #// @param ParagonIE_Sodium_Core32_Int64 $int
    #// @param int $size
    #// @return ParagonIE_Sodium_Core32_Int64
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedAssignment
    #//
    def mulint64(self, int=None, size=0):
        
        if ParagonIE_Sodium_Compat.fastMult:
            return self.mulint64fast(int)
        # end if
        ParagonIE_Sodium_Core32_Util.declarescalartype(size, "int", 2)
        if (not size):
            size = 63
        # end if
        a, b = self.ctselect(self, int)
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        return_.unsignedInt = self.unsignedInt
        #// Initialize:
        ret0 = 0
        ret1 = 0
        ret2 = 0
        ret3 = 0
        a0 = a.limbs[0]
        a1 = a.limbs[1]
        a2 = a.limbs[2]
        a3 = a.limbs[3]
        b0 = b.limbs[0]
        b1 = b.limbs[1]
        b2 = b.limbs[2]
        b3 = b.limbs[3]
        #// @var int $size
        #// @var int $i
        i = php_int(size)
        while i >= 0:
            
            mask = -b3 & 1
            x0 = a0 & mask
            x1 = a1 & mask
            x2 = a2 & mask
            x3 = a3 & mask
            ret3 += x3
            c = ret3 >> 16
            ret2 += x2 + c
            c = ret2 >> 16
            ret1 += x1 + c
            c = ret1 >> 16
            ret0 += x0 + c
            ret0 &= 65535
            ret1 &= 65535
            ret2 &= 65535
            ret3 &= 65535
            a3 = a3 << 1
            x3 = a3 >> 16
            a2 = a2 << 1 | x3
            x2 = a2 >> 16
            a1 = a1 << 1 | x2
            x1 = a1 >> 16
            a0 = a0 << 1 | x1
            a0 &= 65535
            a1 &= 65535
            a2 &= 65535
            a3 &= 65535
            x0 = b0 & 1 << 16
            x1 = b1 & 1 << 16
            x2 = b2 & 1 << 16
            b0 = b0 >> 1
            b1 = b1 | x0 >> 1
            b2 = b2 | x1 >> 1
            b3 = b3 | x2 >> 1
            b0 &= 65535
            b1 &= 65535
            b2 &= 65535
            b3 &= 65535
            i -= 1
        # end while
        return_.limbs[0] = ret0
        return_.limbs[1] = ret1
        return_.limbs[2] = ret2
        return_.limbs[3] = ret3
        return return_
    # end def mulint64
    #// 
    #// OR this 64-bit integer with another.
    #// 
    #// @param ParagonIE_Sodium_Core32_Int64 $b
    #// @return ParagonIE_Sodium_Core32_Int64
    #//
    def orint64(self, b=None):
        
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        return_.unsignedInt = self.unsignedInt
        return_.limbs = Array(php_int(self.limbs[0] | b.limbs[0]), php_int(self.limbs[1] | b.limbs[1]), php_int(self.limbs[2] | b.limbs[2]), php_int(self.limbs[3] | b.limbs[3]))
        return return_
    # end def orint64
    #// 
    #// @param int $c
    #// @return ParagonIE_Sodium_Core32_Int64
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArrayAccess
    #//
    def rotateleft(self, c=0):
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(c, "int", 1)
        #// @var int $c
        c = php_int(c)
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        return_.unsignedInt = self.unsignedInt
        c &= 63
        if c == 0:
            #// NOP, but we want a copy.
            return_.limbs = self.limbs
        else:
            #// @var array<int, int> $limbs
            limbs = return_.limbs
            #// @var array<int, int> $myLimbs
            myLimbs = self.limbs
            #// @var int $idx_shift
            idx_shift = c >> 4 & 3
            #// @var int $sub_shift
            sub_shift = c & 15
            i = 3
            while i >= 0:
                
                #// @var int $j
                j = i + idx_shift & 3
                #// @var int $k
                k = i + idx_shift + 1 & 3
                limbs[i] = php_int(php_int(myLimbs[j]) << sub_shift | php_int(myLimbs[k]) >> 16 - sub_shift & 65535)
                i -= 1
            # end while
        # end if
        return return_
    # end def rotateleft
    #// 
    #// Rotate to the right
    #// 
    #// @param int $c
    #// @return ParagonIE_Sodium_Core32_Int64
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArrayAccess
    #//
    def rotateright(self, c=0):
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(c, "int", 1)
        #// @var int $c
        c = php_int(c)
        #// @var ParagonIE_Sodium_Core32_Int64 $return
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        return_.unsignedInt = self.unsignedInt
        c &= 63
        #// @var int $c
        if c == 0:
            #// NOP, but we want a copy.
            return_.limbs = self.limbs
        else:
            #// @var array<int, int> $limbs
            limbs = return_.limbs
            #// @var array<int, int> $myLimbs
            myLimbs = self.limbs
            #// @var int $idx_shift
            idx_shift = c >> 4 & 3
            #// @var int $sub_shift
            sub_shift = c & 15
            i = 3
            while i >= 0:
                
                #// @var int $j
                j = i - idx_shift & 3
                #// @var int $k
                k = i - idx_shift - 1 & 3
                limbs[i] = php_int(php_int(myLimbs[j]) >> php_int(sub_shift) | php_int(myLimbs[k]) << 16 - php_int(sub_shift) & 65535)
                i -= 1
            # end while
        # end if
        return return_
    # end def rotateright
    #// 
    #// @param int $c
    #// @return ParagonIE_Sodium_Core32_Int64
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def shiftleft(self, c=0):
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(c, "int", 1)
        #// @var int $c
        c = php_int(c)
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        return_.unsignedInt = self.unsignedInt
        c &= 63
        if c >= 16:
            if c >= 48:
                return_.limbs = Array(self.limbs[3], 0, 0, 0)
            elif c >= 32:
                return_.limbs = Array(self.limbs[2], self.limbs[3], 0, 0)
            else:
                return_.limbs = Array(self.limbs[1], self.limbs[2], self.limbs[3], 0)
            # end if
            return return_.shiftleft(c & 15)
        # end if
        if c == 0:
            return_.limbs = self.limbs
        elif c < 0:
            #// @var int $c
            return self.shiftright(-c)
        else:
            if (not php_is_int(c)):
                raise php_new_class("TypeError", lambda : TypeError())
            # end if
            #// @var int $carry
            carry = 0
            i = 3
            while i >= 0:
                
                #// @var int $tmp
                tmp = self.limbs[i] << c | carry & 65535
                return_.limbs[i] = php_int(tmp & 65535)
                #// @var int $carry
                carry = tmp >> 16
                i -= 1
            # end while
        # end if
        return return_
    # end def shiftleft
    #// 
    #// @param int $c
    #// @return ParagonIE_Sodium_Core32_Int64
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def shiftright(self, c=0):
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(c, "int", 1)
        c = php_int(c)
        #// @var int $c
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        return_.unsignedInt = self.unsignedInt
        c &= 63
        negative = -self.limbs[0] >> 15 & 1
        if c >= 16:
            if c >= 48:
                return_.limbs = Array(php_int(negative & 65535), php_int(negative & 65535), php_int(negative & 65535), php_int(self.limbs[0]))
            elif c >= 32:
                return_.limbs = Array(php_int(negative & 65535), php_int(negative & 65535), php_int(self.limbs[0]), php_int(self.limbs[1]))
            else:
                return_.limbs = Array(php_int(negative & 65535), php_int(self.limbs[0]), php_int(self.limbs[1]), php_int(self.limbs[2]))
            # end if
            return return_.shiftright(c & 15)
        # end if
        if c == 0:
            return_.limbs = self.limbs
        elif c < 0:
            return self.shiftleft(-c)
        else:
            if (not php_is_int(c)):
                raise php_new_class("TypeError", lambda : TypeError())
            # end if
            #// @var int $carryRight
            carryRight = negative & 65535
            mask = php_int(1 << c + 1 - 1 & 65535)
            i = 0
            while i < 4:
                
                return_.limbs[i] = php_int(self.limbs[i] >> c | carryRight << 16 - c & 65535)
                carryRight = php_int(self.limbs[i] & mask)
                i += 1
            # end while
        # end if
        return return_
    # end def shiftright
    #// 
    #// Subtract a normal integer from an int64 object.
    #// 
    #// @param int $int
    #// @return ParagonIE_Sodium_Core32_Int64
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def subint(self, int=None):
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(int, "int", 1)
        int = php_int(int)
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        return_.unsignedInt = self.unsignedInt
        #// @var int $carry
        carry = 0
        i = 3
        while i >= 0:
            
            #// @var int $tmp
            tmp = self.limbs[i] - int >> 16 & 65535 + carry
            #// @var int $carry
            carry = tmp >> 16
            return_.limbs[i] = php_int(tmp & 65535)
            i -= 1
        # end while
        return return_
    # end def subint
    #// 
    #// The difference between two Int64 objects.
    #// 
    #// @param ParagonIE_Sodium_Core32_Int64 $b
    #// @return ParagonIE_Sodium_Core32_Int64
    #//
    def subint64(self, b=None):
        
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        return_.unsignedInt = self.unsignedInt
        #// @var int $carry
        carry = 0
        i = 3
        while i >= 0:
            
            #// @var int $tmp
            tmp = self.limbs[i] - b.limbs[i] + carry
            #// @var int $carry
            carry = tmp >> 16
            return_.limbs[i] = php_int(tmp & 65535)
            i -= 1
        # end while
        return return_
    # end def subint64
    #// 
    #// XOR this 64-bit integer with another.
    #// 
    #// @param ParagonIE_Sodium_Core32_Int64 $b
    #// @return ParagonIE_Sodium_Core32_Int64
    #//
    def xorint64(self, b=None):
        
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        return_.unsignedInt = self.unsignedInt
        return_.limbs = Array(php_int(self.limbs[0] ^ b.limbs[0]), php_int(self.limbs[1] ^ b.limbs[1]), php_int(self.limbs[2] ^ b.limbs[2]), php_int(self.limbs[3] ^ b.limbs[3]))
        return return_
    # end def xorint64
    #// 
    #// @param int $low
    #// @param int $high
    #// @return self
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def fromints(self, low=None, high=None):
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(low, "int", 1)
        ParagonIE_Sodium_Core32_Util.declarescalartype(high, "int", 2)
        high = php_int(high)
        low = php_int(low)
        return php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64(Array(php_int(high >> 16 & 65535), php_int(high & 65535), php_int(low >> 16 & 65535), php_int(low & 65535))))
    # end def fromints
    #// 
    #// @param int $low
    #// @return self
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def fromint(self, low=None):
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(low, "int", 1)
        low = php_int(low)
        return php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64(Array(0, 0, php_int(low >> 16 & 65535), php_int(low & 65535))))
    # end def fromint
    #// 
    #// @return int
    #//
    def toint(self):
        
        return php_int(self.limbs[2] & 65535 << 16 | self.limbs[3] & 65535)
    # end def toint
    #// 
    #// @param string $string
    #// @return self
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def fromstring(self, string=None):
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(string, "string", 1)
        string = php_str(string)
        if ParagonIE_Sodium_Core32_Util.strlen(string) != 8:
            raise php_new_class("RangeException", lambda : RangeException("String must be 8 bytes; " + ParagonIE_Sodium_Core32_Util.strlen(string) + " given."))
        # end if
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        return_.limbs[0] = php_int(ParagonIE_Sodium_Core32_Util.chrtoint(string[0]) & 255 << 8)
        return_.limbs[0] |= ParagonIE_Sodium_Core32_Util.chrtoint(string[1]) & 255
        return_.limbs[1] = php_int(ParagonIE_Sodium_Core32_Util.chrtoint(string[2]) & 255 << 8)
        return_.limbs[1] |= ParagonIE_Sodium_Core32_Util.chrtoint(string[3]) & 255
        return_.limbs[2] = php_int(ParagonIE_Sodium_Core32_Util.chrtoint(string[4]) & 255 << 8)
        return_.limbs[2] |= ParagonIE_Sodium_Core32_Util.chrtoint(string[5]) & 255
        return_.limbs[3] = php_int(ParagonIE_Sodium_Core32_Util.chrtoint(string[6]) & 255 << 8)
        return_.limbs[3] |= ParagonIE_Sodium_Core32_Util.chrtoint(string[7]) & 255
        return return_
    # end def fromstring
    #// 
    #// @param string $string
    #// @return self
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def fromreversestring(self, string=None):
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(string, "string", 1)
        string = php_str(string)
        if ParagonIE_Sodium_Core32_Util.strlen(string) != 8:
            raise php_new_class("RangeException", lambda : RangeException("String must be 8 bytes; " + ParagonIE_Sodium_Core32_Util.strlen(string) + " given."))
        # end if
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        return_.limbs[0] = php_int(ParagonIE_Sodium_Core32_Util.chrtoint(string[7]) & 255 << 8)
        return_.limbs[0] |= ParagonIE_Sodium_Core32_Util.chrtoint(string[6]) & 255
        return_.limbs[1] = php_int(ParagonIE_Sodium_Core32_Util.chrtoint(string[5]) & 255 << 8)
        return_.limbs[1] |= ParagonIE_Sodium_Core32_Util.chrtoint(string[4]) & 255
        return_.limbs[2] = php_int(ParagonIE_Sodium_Core32_Util.chrtoint(string[3]) & 255 << 8)
        return_.limbs[2] |= ParagonIE_Sodium_Core32_Util.chrtoint(string[2]) & 255
        return_.limbs[3] = php_int(ParagonIE_Sodium_Core32_Util.chrtoint(string[1]) & 255 << 8)
        return_.limbs[3] |= ParagonIE_Sodium_Core32_Util.chrtoint(string[0]) & 255
        return return_
    # end def fromreversestring
    #// 
    #// @return array<int, int>
    #//
    def toarray(self):
        
        return Array(php_int(self.limbs[0] & 65535 << 16 | self.limbs[1] & 65535), php_int(self.limbs[2] & 65535 << 16 | self.limbs[3] & 65535))
    # end def toarray
    #// 
    #// @return ParagonIE_Sodium_Core32_Int32
    #//
    def toint32(self):
        
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
        return_.limbs[0] = php_int(self.limbs[2])
        return_.limbs[1] = php_int(self.limbs[3])
        return_.unsignedInt = self.unsignedInt
        return_.overflow = php_int(ParagonIE_Sodium_Core32_Util.abs(self.limbs[1], 16) & 65535)
        return return_
    # end def toint32
    #// 
    #// @return ParagonIE_Sodium_Core32_Int64
    #//
    def toint64(self):
        
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        return_.limbs[0] = php_int(self.limbs[0])
        return_.limbs[1] = php_int(self.limbs[1])
        return_.limbs[2] = php_int(self.limbs[2])
        return_.limbs[3] = php_int(self.limbs[3])
        return_.unsignedInt = self.unsignedInt
        return_.overflow = ParagonIE_Sodium_Core32_Util.abs(self.overflow)
        return return_
    # end def toint64
    #// 
    #// @param bool $bool
    #// @return self
    #//
    def setunsignedint(self, bool=False):
        
        self.unsignedInt = (not php_empty(lambda : bool))
        return self
    # end def setunsignedint
    #// 
    #// @return string
    #// @throws TypeError
    #//
    def tostring(self):
        
        return ParagonIE_Sodium_Core32_Util.inttochr(self.limbs[0] >> 8 & 255) + ParagonIE_Sodium_Core32_Util.inttochr(self.limbs[0] & 255) + ParagonIE_Sodium_Core32_Util.inttochr(self.limbs[1] >> 8 & 255) + ParagonIE_Sodium_Core32_Util.inttochr(self.limbs[1] & 255) + ParagonIE_Sodium_Core32_Util.inttochr(self.limbs[2] >> 8 & 255) + ParagonIE_Sodium_Core32_Util.inttochr(self.limbs[2] & 255) + ParagonIE_Sodium_Core32_Util.inttochr(self.limbs[3] >> 8 & 255) + ParagonIE_Sodium_Core32_Util.inttochr(self.limbs[3] & 255)
    # end def tostring
    #// 
    #// @return string
    #// @throws TypeError
    #//
    def toreversestring(self):
        
        return ParagonIE_Sodium_Core32_Util.inttochr(self.limbs[3] & 255) + ParagonIE_Sodium_Core32_Util.inttochr(self.limbs[3] >> 8 & 255) + ParagonIE_Sodium_Core32_Util.inttochr(self.limbs[2] & 255) + ParagonIE_Sodium_Core32_Util.inttochr(self.limbs[2] >> 8 & 255) + ParagonIE_Sodium_Core32_Util.inttochr(self.limbs[1] & 255) + ParagonIE_Sodium_Core32_Util.inttochr(self.limbs[1] >> 8 & 255) + ParagonIE_Sodium_Core32_Util.inttochr(self.limbs[0] & 255) + ParagonIE_Sodium_Core32_Util.inttochr(self.limbs[0] >> 8 & 255)
    # end def toreversestring
    #// 
    #// @return string
    #//
    def __tostring(self):
        
        try: 
            return self.tostring()
        except TypeError as ex:
            #// PHP engine can't handle exceptions from __toString()
            return ""
        # end try
    # end def __tostring
# end class ParagonIE_Sodium_Core32_Int64
