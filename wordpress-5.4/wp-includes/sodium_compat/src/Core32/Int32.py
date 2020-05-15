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
#// Class ParagonIE_Sodium_Core32_Int32
#// 
#// Encapsulates a 32-bit integer.
#// 
#// These are immutable. It always returns a new instance.
#//
class ParagonIE_Sodium_Core32_Int32():
    limbs = Array(0, 0)
    overflow = 0
    unsignedInt = False
    #// 
    #// ParagonIE_Sodium_Core32_Int32 constructor.
    #// @param array $array
    #// @param bool $unsignedInt
    #//
    def __init__(self, array=Array(0, 0), unsignedInt=False):
        
        self.limbs = Array(int(array[0]), int(array[1]))
        self.overflow = 0
        self.unsignedInt = unsignedInt
    # end def __init__
    #// 
    #// Adds two int32 objects
    #// 
    #// @param ParagonIE_Sodium_Core32_Int32 $addend
    #// @return ParagonIE_Sodium_Core32_Int32
    #//
    def addint32(self, addend=None):
        
        i0 = self.limbs[0]
        i1 = self.limbs[1]
        j0 = addend.limbs[0]
        j1 = addend.limbs[1]
        r1 = i1 + j1 & 65535
        carry = r1 >> 16
        r0 = i0 + j0 & 65535 + carry
        carry = r0 >> 16
        r0 &= 65535
        r1 &= 65535
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32(Array(r0, r1)))
        return_.overflow = carry
        return_.unsignedInt = self.unsignedInt
        return return_
    # end def addint32
    #// 
    #// Adds a normal integer to an int32 object
    #// 
    #// @param int $int
    #// @return ParagonIE_Sodium_Core32_Int32
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def addint(self, int=None):
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(int, "int", 1)
        #// @var int $int
        int = int(int)
        int = int(int)
        i0 = self.limbs[0]
        i1 = self.limbs[1]
        r1 = i1 + int & 65535
        carry = r1 >> 16
        r0 = i0 + int >> 16 & 65535 + carry
        carry = r0 >> 16
        r0 &= 65535
        r1 &= 65535
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32(Array(r0, r1)))
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
        i = 2
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
            #// @var int $gt
            gt |= x2 - x1 >> 8 & eq
            #// @var int $eq
            eq &= x2 ^ x1 - 1 >> 8
        # end while
        return gt + gt - eq + 1
    # end def compareint
    #// 
    #// @param int $m
    #// @return ParagonIE_Sodium_Core32_Int32
    #//
    def mask(self, m=0):
        
        #// @var int $hi
        hi = m >> 16 & 65535
        #// @var int $lo
        lo = m & 65535
        return php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32(Array(int(self.limbs[0] & hi), int(self.limbs[1] & lo)), self.unsignedInt))
    # end def mask
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
                r[i + j] = product - int(carry * base) & 65535
                r[i + j + 1] += carry
                j += 1
            # end while
            i += 1
        # end while
        return php_array_slice(r, 0, 5)
    # end def multiplylong
    #// 
    #// @param int $int
    #// @return ParagonIE_Sodium_Core32_Int32
    #//
    def mulintfast(self, int=None):
        
        #// Handle negative numbers
        aNeg = self.limbs[0] >> 15 & 1
        bNeg = int >> 31 & 1
        a = array_reverse(self.limbs)
        b = Array(int & 65535, int >> 16 & 65535)
        if aNeg:
            i = 0
            while i < 2:
                
                a[i] = a[i] ^ 65535 & 65535
                i += 1
            # end while
            a[0] += 1
        # end if
        if bNeg:
            i = 0
            while i < 2:
                
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
            while i < 2:
                
                res[i] = 65535 ^ res[i] & 65535
                i += 1
            # end while
            #// Handle integer overflow
            c = 1
            i = 0
            while i < 2:
                
                res[i] += c
                c = res[i] >> 16
                res[i] &= 65535
                i += 1
            # end while
        # end if
        #// Return our values
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
        return_.limbs = Array(res[1] & 65535, res[0] & 65535)
        if php_count(res) > 2:
            return_.overflow = res[2] & 65535
        # end if
        return_.unsignedInt = self.unsignedInt
        return return_
    # end def mulintfast
    #// 
    #// @param ParagonIE_Sodium_Core32_Int32 $right
    #// @return ParagonIE_Sodium_Core32_Int32
    #//
    def mulint32fast(self, right=None):
        
        aNeg = self.limbs[0] >> 15 & 1
        bNeg = right.limbs[0] >> 15 & 1
        a = array_reverse(self.limbs)
        b = array_reverse(right.limbs)
        if aNeg:
            i = 0
            while i < 2:
                
                a[i] = a[i] ^ 65535 & 65535
                i += 1
            # end while
            a[0] += 1
        # end if
        if bNeg:
            i = 0
            while i < 2:
                
                b[i] = b[i] ^ 65535 & 65535
                i += 1
            # end while
            b[0] += 1
        # end if
        res = self.multiplylong(a, b)
        if aNeg != bNeg:
            if aNeg != bNeg:
                i = 0
                while i < 2:
                    
                    res[i] = res[i] ^ 65535 & 65535
                    i += 1
                # end while
                c = 1
                i = 0
                while i < 2:
                    
                    res[i] += c
                    c = res[i] >> 16
                    res[i] &= 65535
                    i += 1
                # end while
            # end if
        # end if
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
        return_.limbs = Array(res[1] & 65535, res[0] & 65535)
        if php_count(res) > 2:
            return_.overflow = res[2]
        # end if
        return return_
    # end def mulint32fast
    #// 
    #// @param int $int
    #// @param int $size
    #// @return ParagonIE_Sodium_Core32_Int32
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def mulint(self, int=0, size=0):
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(int, "int", 1)
        ParagonIE_Sodium_Core32_Util.declarescalartype(size, "int", 2)
        if ParagonIE_Sodium_Compat.fastMult:
            return self.mulintfast(int(int))
        # end if
        #// @var int $int
        int = int(int)
        #// @var int $size
        size = int(size)
        if (not size):
            size = 31
        # end if
        #// @var int $size
        a = copy.deepcopy(self)
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
        return_.unsignedInt = self.unsignedInt
        #// Initialize:
        ret0 = 0
        ret1 = 0
        a0 = a.limbs[0]
        a1 = a.limbs[1]
        #// @var int $size
        #// @var int $i
        i = size
        while i >= 0:
            
            m = int(-int & 1)
            x0 = a0 & m
            x1 = a1 & m
            ret1 += x1
            c = ret1 >> 16
            ret0 += x0 + c
            ret0 &= 65535
            ret1 &= 65535
            a1 = a1 << 1
            x1 = a1 >> 16
            a0 = a0 << 1 | x1
            a0 &= 65535
            a1 &= 65535
            int >>= 1
            i -= 1
        # end while
        return_.limbs[0] = ret0
        return_.limbs[1] = ret1
        return return_
    # end def mulint
    #// 
    #// @param ParagonIE_Sodium_Core32_Int32 $int
    #// @param int $size
    #// @return ParagonIE_Sodium_Core32_Int32
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def mulint32(self, int=None, size=0):
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(size, "int", 2)
        if ParagonIE_Sodium_Compat.fastMult:
            return self.mulint32fast(int)
        # end if
        if (not size):
            size = 31
        # end if
        #// @var int $size
        a = copy.deepcopy(self)
        b = copy.deepcopy(int)
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
        return_.unsignedInt = self.unsignedInt
        #// Initialize:
        ret0 = 0
        ret1 = 0
        a0 = a.limbs[0]
        a1 = a.limbs[1]
        b0 = b.limbs[0]
        b1 = b.limbs[1]
        #// @var int $size
        #// @var int $i
        i = size
        while i >= 0:
            
            m = int(-b1 & 1)
            x0 = a0 & m
            x1 = a1 & m
            ret1 += x1
            c = ret1 >> 16
            ret0 += x0 + c
            ret0 &= 65535
            ret1 &= 65535
            a1 = a1 << 1
            x1 = a1 >> 16
            a0 = a0 << 1 | x1
            a0 &= 65535
            a1 &= 65535
            x0 = b0 & 1 << 16
            b0 = b0 >> 1
            b1 = b1 | x0 >> 1
            b0 &= 65535
            b1 &= 65535
            i -= 1
        # end while
        return_.limbs[0] = ret0
        return_.limbs[1] = ret1
        return return_
    # end def mulint32
    #// 
    #// OR this 32-bit integer with another.
    #// 
    #// @param ParagonIE_Sodium_Core32_Int32 $b
    #// @return ParagonIE_Sodium_Core32_Int32
    #//
    def orint32(self, b=None):
        
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
        return_.unsignedInt = self.unsignedInt
        return_.limbs = Array(int(self.limbs[0] | b.limbs[0]), int(self.limbs[1] | b.limbs[1]))
        #// @var int overflow
        return_.overflow = self.overflow | b.overflow
        return return_
    # end def orint32
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
    #// @param int $c
    #// @return ParagonIE_Sodium_Core32_Int32
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArrayAccess
    #//
    def rotateleft(self, c=0):
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(c, "int", 1)
        #// @var int $c
        c = int(c)
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
        return_.unsignedInt = self.unsignedInt
        c &= 31
        if c == 0:
            #// NOP, but we want a copy.
            return_.limbs = self.limbs
        else:
            #// @var int $c
            #// @var int $idx_shift
            idx_shift = c >> 4 & 1
            #// @var int $sub_shift
            sub_shift = c & 15
            #// @var array<int, int> $limbs
            limbs = return_.limbs
            #// @var array<int, int> $myLimbs
            myLimbs = self.limbs
            i = 1
            while i >= 0:
                
                #// @var int $j
                j = i + idx_shift & 1
                #// @var int $k
                k = i + idx_shift + 1 & 1
                limbs[i] = int(int(myLimbs[j]) << sub_shift | int(myLimbs[k]) >> 16 - sub_shift & 65535)
                i -= 1
            # end while
        # end if
        return return_
    # end def rotateleft
    #// 
    #// Rotate to the right
    #// 
    #// @param int $c
    #// @return ParagonIE_Sodium_Core32_Int32
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArrayAccess
    #//
    def rotateright(self, c=0):
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(c, "int", 1)
        #// @var int $c
        c = int(c)
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
        return_.unsignedInt = self.unsignedInt
        c &= 31
        #// @var int $c
        if c == 0:
            #// NOP, but we want a copy.
            return_.limbs = self.limbs
        else:
            #// @var int $c
            #// @var int $idx_shift
            idx_shift = c >> 4 & 1
            #// @var int $sub_shift
            sub_shift = c & 15
            #// @var array<int, int> $limbs
            limbs = return_.limbs
            #// @var array<int, int> $myLimbs
            myLimbs = self.limbs
            i = 1
            while i >= 0:
                
                #// @var int $j
                j = i - idx_shift & 1
                #// @var int $k
                k = i - idx_shift - 1 & 1
                limbs[i] = int(int(myLimbs[j]) >> int(sub_shift) | int(myLimbs[k]) << 16 - int(sub_shift) & 65535)
                i -= 1
            # end while
        # end if
        return return_
    # end def rotateright
    #// 
    #// @param bool $bool
    #// @return self
    #//
    def setunsignedint(self, bool=False):
        
        self.unsignedInt = (not php_empty(lambda : bool))
        return self
    # end def setunsignedint
    #// 
    #// @param int $c
    #// @return ParagonIE_Sodium_Core32_Int32
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def shiftleft(self, c=0):
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(c, "int", 1)
        #// @var int $c
        c = int(c)
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
        return_.unsignedInt = self.unsignedInt
        c &= 63
        #// @var int $c
        if c == 0:
            return_.limbs = self.limbs
        elif c < 0:
            #// @var int $c
            return self.shiftright(-c)
        else:
            #// @var int $c
            #// @var int $tmp
            tmp = self.limbs[1] << c
            return_.limbs[1] = int(tmp & 65535)
            #// @var int $carry
            carry = tmp >> 16
            #// @var int $tmp
            tmp = self.limbs[0] << c | carry & 65535
            return_.limbs[0] = int(tmp & 65535)
        # end if
        return return_
    # end def shiftleft
    #// 
    #// @param int $c
    #// @return ParagonIE_Sodium_Core32_Int32
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedAssignment
    #// @psalm-suppress MixedOperand
    #//
    def shiftright(self, c=0):
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(c, "int", 1)
        #// @var int $c
        c = int(c)
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
        return_.unsignedInt = self.unsignedInt
        c &= 63
        #// @var int $c
        if c >= 16:
            return_.limbs = Array(int(self.overflow & 65535), int(self.limbs[0]))
            return_.overflow = self.overflow >> 16
            return return_.shiftright(c & 15)
        # end if
        if c == 0:
            return_.limbs = self.limbs
        elif c < 0:
            #// @var int $c
            return self.shiftleft(-c)
        else:
            if (not php_is_int(c)):
                raise php_new_class("TypeError", lambda : TypeError())
            # end if
            #// @var int $c
            #// $return->limbs[0] = (int) (($this->limbs[0] >> $c) & 0xffff);
            carryLeft = int(self.overflow & 1 << c + 1 - 1)
            return_.limbs[0] = int(self.limbs[0] >> c | carryLeft << 16 - c & 65535)
            carryRight = int(self.limbs[0] & 1 << c + 1 - 1)
            return_.limbs[1] = int(self.limbs[1] >> c | carryRight << 16 - c & 65535)
            return_.overflow >>= c
        # end if
        return return_
    # end def shiftright
    #// 
    #// Subtract a normal integer from an int32 object.
    #// 
    #// @param int $int
    #// @return ParagonIE_Sodium_Core32_Int32
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def subint(self, int=None):
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(int, "int", 1)
        #// @var int $int
        int = int(int)
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
        return_.unsignedInt = self.unsignedInt
        #// @var int $tmp
        tmp = self.limbs[1] - int & 65535
        #// @var int $carry
        carry = tmp >> 16
        return_.limbs[1] = int(tmp & 65535)
        #// @var int $tmp
        tmp = self.limbs[0] - int >> 16 & 65535 + carry
        return_.limbs[0] = int(tmp & 65535)
        return return_
    # end def subint
    #// 
    #// Subtract two int32 objects from each other
    #// 
    #// @param ParagonIE_Sodium_Core32_Int32 $b
    #// @return ParagonIE_Sodium_Core32_Int32
    #//
    def subint32(self, b=None):
        
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
        return_.unsignedInt = self.unsignedInt
        #// @var int $tmp
        tmp = self.limbs[1] - b.limbs[1] & 65535
        #// @var int $carry
        carry = tmp >> 16
        return_.limbs[1] = int(tmp & 65535)
        #// @var int $tmp
        tmp = self.limbs[0] - b.limbs[0] & 65535 + carry
        return_.limbs[0] = int(tmp & 65535)
        return return_
    # end def subint32
    #// 
    #// XOR this 32-bit integer with another.
    #// 
    #// @param ParagonIE_Sodium_Core32_Int32 $b
    #// @return ParagonIE_Sodium_Core32_Int32
    #//
    def xorint32(self, b=None):
        
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
        return_.unsignedInt = self.unsignedInt
        return_.limbs = Array(int(self.limbs[0] ^ b.limbs[0]), int(self.limbs[1] ^ b.limbs[1]))
        return return_
    # end def xorint32
    #// 
    #// @param int $signed
    #// @return self
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def fromint(self, signed=None):
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(signed, "int", 1)
        #// @var int $signed
        signed = int(signed)
        return php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32(Array(int(signed >> 16 & 65535), int(signed & 65535))))
    # end def fromint
    #// 
    #// @param string $string
    #// @return self
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def fromstring(self, string=None):
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(string, "string", 1)
        string = str(string)
        if ParagonIE_Sodium_Core32_Util.strlen(string) != 4:
            raise php_new_class("RangeException", lambda : RangeException("String must be 4 bytes; " + ParagonIE_Sodium_Core32_Util.strlen(string) + " given."))
        # end if
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
        return_.limbs[0] = int(ParagonIE_Sodium_Core32_Util.chrtoint(string[0]) & 255 << 8)
        return_.limbs[0] |= ParagonIE_Sodium_Core32_Util.chrtoint(string[1]) & 255
        return_.limbs[1] = int(ParagonIE_Sodium_Core32_Util.chrtoint(string[2]) & 255 << 8)
        return_.limbs[1] |= ParagonIE_Sodium_Core32_Util.chrtoint(string[3]) & 255
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
        string = str(string)
        if ParagonIE_Sodium_Core32_Util.strlen(string) != 4:
            raise php_new_class("RangeException", lambda : RangeException("String must be 4 bytes; " + ParagonIE_Sodium_Core32_Util.strlen(string) + " given."))
        # end if
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
        return_.limbs[0] = int(ParagonIE_Sodium_Core32_Util.chrtoint(string[3]) & 255 << 8)
        return_.limbs[0] |= ParagonIE_Sodium_Core32_Util.chrtoint(string[2]) & 255
        return_.limbs[1] = int(ParagonIE_Sodium_Core32_Util.chrtoint(string[1]) & 255 << 8)
        return_.limbs[1] |= ParagonIE_Sodium_Core32_Util.chrtoint(string[0]) & 255
        return return_
    # end def fromreversestring
    #// 
    #// @return array<int, int>
    #//
    def toarray(self):
        
        return Array(int(self.limbs[0] << 16 | self.limbs[1]))
    # end def toarray
    #// 
    #// @return string
    #// @throws TypeError
    #//
    def tostring(self):
        
        return ParagonIE_Sodium_Core32_Util.inttochr(self.limbs[0] >> 8 & 255) + ParagonIE_Sodium_Core32_Util.inttochr(self.limbs[0] & 255) + ParagonIE_Sodium_Core32_Util.inttochr(self.limbs[1] >> 8 & 255) + ParagonIE_Sodium_Core32_Util.inttochr(self.limbs[1] & 255)
    # end def tostring
    #// 
    #// @return int
    #//
    def toint(self):
        
        return int(self.limbs[0] & 65535 << 16 | self.limbs[1] & 65535)
    # end def toint
    #// 
    #// @return ParagonIE_Sodium_Core32_Int32
    #//
    def toint32(self):
        
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
        return_.limbs[0] = int(self.limbs[0] & 65535)
        return_.limbs[1] = int(self.limbs[1] & 65535)
        return_.unsignedInt = self.unsignedInt
        return_.overflow = int(self.overflow & 2147483647)
        return return_
    # end def toint32
    #// 
    #// @return ParagonIE_Sodium_Core32_Int64
    #//
    def toint64(self):
        
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        return_.unsignedInt = self.unsignedInt
        if self.unsignedInt:
            return_.limbs[0] += self.overflow >> 16 & 65535
            return_.limbs[1] += self.overflow & 65535
        else:
            neg = -self.limbs[0] >> 15 & 1
            return_.limbs[0] = int(neg & 65535)
            return_.limbs[1] = int(neg & 65535)
        # end if
        return_.limbs[2] = int(self.limbs[0] & 65535)
        return_.limbs[3] = int(self.limbs[1] & 65535)
        return return_
    # end def toint64
    #// 
    #// @return string
    #// @throws TypeError
    #//
    def toreversestring(self):
        
        return ParagonIE_Sodium_Core32_Util.inttochr(self.limbs[1] & 255) + ParagonIE_Sodium_Core32_Util.inttochr(self.limbs[1] >> 8 & 255) + ParagonIE_Sodium_Core32_Util.inttochr(self.limbs[0] & 255) + ParagonIE_Sodium_Core32_Util.inttochr(self.limbs[0] >> 8 & 255)
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
# end class ParagonIE_Sodium_Core32_Int32
