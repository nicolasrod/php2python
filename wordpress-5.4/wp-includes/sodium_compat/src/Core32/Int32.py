#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import os
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
    #// 
    #// @var array<int, int> - two 16-bit integers
    #// 
    #// 0 is the higher 16 bits
    #// 1 is the lower 16 bits
    #//
    limbs = Array(0, 0)
    #// 
    #// @var int
    #//
    overflow = 0
    #// 
    #// @var bool
    #//
    unsignedInt = False
    #// 
    #// ParagonIE_Sodium_Core32_Int32 constructor.
    #// @param array $array
    #// @param bool $unsignedInt
    #//
    def __init__(self, array_=None, unsignedInt_=None):
        if array_ is None:
            array_ = Array(0, 0)
        # end if
        if unsignedInt_ is None:
            unsignedInt_ = False
        # end if
        
        self.limbs = Array(php_int(array_[0]), php_int(array_[1]))
        self.overflow = 0
        self.unsignedInt = unsignedInt_
    # end def __init__
    #// 
    #// Adds two int32 objects
    #// 
    #// @param ParagonIE_Sodium_Core32_Int32 $addend
    #// @return ParagonIE_Sodium_Core32_Int32
    #//
    def addint32(self, addend_=None):
        
        
        i0_ = self.limbs[0]
        i1_ = self.limbs[1]
        j0_ = addend_.limbs[0]
        j1_ = addend_.limbs[1]
        r1_ = i1_ + j1_ & 65535
        carry_ = r1_ >> 16
        r0_ = i0_ + j0_ & 65535 + carry_
        carry_ = r0_ >> 16
        r0_ &= 65535
        r1_ &= 65535
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32(Array(r0_, r1_)))
        return_.overflow = carry_
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
    def addint(self, int_=None):
        
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(int_, "int", 1)
        #// @var int $int
        int_ = php_int(int_)
        int_ = php_int(int_)
        i0_ = self.limbs[0]
        i1_ = self.limbs[1]
        r1_ = i1_ + int_ & 65535
        carry_ = r1_ >> 16
        r0_ = i0_ + int_ >> 16 & 65535 + carry_
        carry_ = r0_ >> 16
        r0_ &= 65535
        r1_ &= 65535
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32(Array(r0_, r1_)))
        return_.overflow = carry_
        return_.unsignedInt = self.unsignedInt
        return return_
    # end def addint
    #// 
    #// @param int $b
    #// @return int
    #//
    def compareint(self, b_=0):
        
        
        gt_ = 0
        eq_ = 1
        i_ = 2
        j_ = 0
        while True:
            
            if not (i_ > 0):
                break
            # end if
            i_ -= 1
            #// @var int $x1
            x1_ = self.limbs[i_]
            #// @var int $x2
            x2_ = b_ >> j_ << 4 & 65535
            #// @var int $gt
            gt_ |= x2_ - x1_ >> 8 & eq_
            #// @var int $eq
            eq_ &= x2_ ^ x1_ - 1 >> 8
        # end while
        return gt_ + gt_ - eq_ + 1
    # end def compareint
    #// 
    #// @param int $m
    #// @return ParagonIE_Sodium_Core32_Int32
    #//
    def mask(self, m_=0):
        
        
        #// @var int $hi
        hi_ = m_ >> 16 & 65535
        #// @var int $lo
        lo_ = m_ & 65535
        return php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32(Array(php_int(self.limbs[0] & hi_), php_int(self.limbs[1] & lo_)), self.unsignedInt))
    # end def mask
    #// 
    #// @param array<int, int> $a
    #// @param array<int, int> $b
    #// @param int $baseLog2
    #// @return array<int, int>
    #//
    def multiplylong(self, a_=None, b_=None, baseLog2_=16):
        
        
        a_l_ = php_count(a_)
        b_l_ = php_count(b_)
        #// @var array<int, int> $r
        r_ = array_fill(0, a_l_ + b_l_ + 1, 0)
        base_ = 1 << baseLog2_
        i_ = 0
        while i_ < a_l_:
            
            a_i_ = a_[i_]
            j_ = 0
            while j_ < a_l_:
                
                b_j_ = b_[j_]
                product_ = a_i_ * b_j_ + r_[i_ + j_]
                carry_ = product_ >> baseLog2_ & 65535
                r_[i_ + j_] = product_ - php_int(carry_ * base_) & 65535
                r_[i_ + j_ + 1] += carry_
                j_ += 1
            # end while
            i_ += 1
        # end while
        return php_array_slice(r_, 0, 5)
    # end def multiplylong
    #// 
    #// @param int $int
    #// @return ParagonIE_Sodium_Core32_Int32
    #//
    def mulintfast(self, int_=None):
        
        
        #// Handle negative numbers
        aNeg_ = self.limbs[0] >> 15 & 1
        bNeg_ = int_ >> 31 & 1
        a_ = php_array_reverse(self.limbs)
        b_ = Array(int_ & 65535, int_ >> 16 & 65535)
        if aNeg_:
            i_ = 0
            while i_ < 2:
                
                a_[i_] = a_[i_] ^ 65535 & 65535
                i_ += 1
            # end while
            a_[0] += 1
        # end if
        if bNeg_:
            i_ = 0
            while i_ < 2:
                
                b_[i_] = b_[i_] ^ 65535 & 65535
                i_ += 1
            # end while
            b_[0] += 1
        # end if
        #// Multiply
        res_ = self.multiplylong(a_, b_)
        #// Re-apply negation to results
        if aNeg_ != bNeg_:
            i_ = 0
            while i_ < 2:
                
                res_[i_] = 65535 ^ res_[i_] & 65535
                i_ += 1
            # end while
            #// Handle integer overflow
            c_ = 1
            i_ = 0
            while i_ < 2:
                
                res_[i_] += c_
                c_ = res_[i_] >> 16
                res_[i_] &= 65535
                i_ += 1
            # end while
        # end if
        #// Return our values
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
        return_.limbs = Array(res_[1] & 65535, res_[0] & 65535)
        if php_count(res_) > 2:
            return_.overflow = res_[2] & 65535
        # end if
        return_.unsignedInt = self.unsignedInt
        return return_
    # end def mulintfast
    #// 
    #// @param ParagonIE_Sodium_Core32_Int32 $right
    #// @return ParagonIE_Sodium_Core32_Int32
    #//
    def mulint32fast(self, right_=None):
        
        
        aNeg_ = self.limbs[0] >> 15 & 1
        bNeg_ = right_.limbs[0] >> 15 & 1
        a_ = php_array_reverse(self.limbs)
        b_ = php_array_reverse(right_.limbs)
        if aNeg_:
            i_ = 0
            while i_ < 2:
                
                a_[i_] = a_[i_] ^ 65535 & 65535
                i_ += 1
            # end while
            a_[0] += 1
        # end if
        if bNeg_:
            i_ = 0
            while i_ < 2:
                
                b_[i_] = b_[i_] ^ 65535 & 65535
                i_ += 1
            # end while
            b_[0] += 1
        # end if
        res_ = self.multiplylong(a_, b_)
        if aNeg_ != bNeg_:
            if aNeg_ != bNeg_:
                i_ = 0
                while i_ < 2:
                    
                    res_[i_] = res_[i_] ^ 65535 & 65535
                    i_ += 1
                # end while
                c_ = 1
                i_ = 0
                while i_ < 2:
                    
                    res_[i_] += c_
                    c_ = res_[i_] >> 16
                    res_[i_] &= 65535
                    i_ += 1
                # end while
            # end if
        # end if
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
        return_.limbs = Array(res_[1] & 65535, res_[0] & 65535)
        if php_count(res_) > 2:
            return_.overflow = res_[2]
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
    def mulint(self, int_=0, size_=0):
        
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(int_, "int", 1)
        ParagonIE_Sodium_Core32_Util.declarescalartype(size_, "int", 2)
        if ParagonIE_Sodium_Compat.fastMult:
            return self.mulintfast(php_int(int_))
        # end if
        #// @var int $int
        int_ = php_int(int_)
        #// @var int $size
        size_ = php_int(size_)
        if (not size_):
            size_ = 31
        # end if
        #// @var int $size
        a_ = copy.deepcopy(self)
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
        return_.unsignedInt = self.unsignedInt
        #// Initialize:
        ret0_ = 0
        ret1_ = 0
        a0_ = a_.limbs[0]
        a1_ = a_.limbs[1]
        #// @var int $size
        #// @var int $i
        i_ = size_
        while i_ >= 0:
            
            m_ = php_int(-int_ & 1)
            x0_ = a0_ & m_
            x1_ = a1_ & m_
            ret1_ += x1_
            c_ = ret1_ >> 16
            ret0_ += x0_ + c_
            ret0_ &= 65535
            ret1_ &= 65535
            a1_ = a1_ << 1
            x1_ = a1_ >> 16
            a0_ = a0_ << 1 | x1_
            a0_ &= 65535
            a1_ &= 65535
            int_ >>= 1
            i_ -= 1
        # end while
        return_.limbs[0] = ret0_
        return_.limbs[1] = ret1_
        return return_
    # end def mulint
    #// 
    #// @param ParagonIE_Sodium_Core32_Int32 $int
    #// @param int $size
    #// @return ParagonIE_Sodium_Core32_Int32
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def mulint32(self, int_=None, size_=0):
        
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(size_, "int", 2)
        if ParagonIE_Sodium_Compat.fastMult:
            return self.mulint32fast(int_)
        # end if
        if (not size_):
            size_ = 31
        # end if
        #// @var int $size
        a_ = copy.deepcopy(self)
        b_ = copy.deepcopy(int_)
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
        return_.unsignedInt = self.unsignedInt
        #// Initialize:
        ret0_ = 0
        ret1_ = 0
        a0_ = a_.limbs[0]
        a1_ = a_.limbs[1]
        b0_ = b_.limbs[0]
        b1_ = b_.limbs[1]
        #// @var int $size
        #// @var int $i
        i_ = size_
        while i_ >= 0:
            
            m_ = php_int(-b1_ & 1)
            x0_ = a0_ & m_
            x1_ = a1_ & m_
            ret1_ += x1_
            c_ = ret1_ >> 16
            ret0_ += x0_ + c_
            ret0_ &= 65535
            ret1_ &= 65535
            a1_ = a1_ << 1
            x1_ = a1_ >> 16
            a0_ = a0_ << 1 | x1_
            a0_ &= 65535
            a1_ &= 65535
            x0_ = b0_ & 1 << 16
            b0_ = b0_ >> 1
            b1_ = b1_ | x0_ >> 1
            b0_ &= 65535
            b1_ &= 65535
            i_ -= 1
        # end while
        return_.limbs[0] = ret0_
        return_.limbs[1] = ret1_
        return return_
    # end def mulint32
    #// 
    #// OR this 32-bit integer with another.
    #// 
    #// @param ParagonIE_Sodium_Core32_Int32 $b
    #// @return ParagonIE_Sodium_Core32_Int32
    #//
    def orint32(self, b_=None):
        
        
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
        return_.unsignedInt = self.unsignedInt
        return_.limbs = Array(php_int(self.limbs[0] | b_.limbs[0]), php_int(self.limbs[1] | b_.limbs[1]))
        #// @var int overflow
        return_.overflow = self.overflow | b_.overflow
        return return_
    # end def orint32
    #// 
    #// @param int $b
    #// @return bool
    #//
    def isgreaterthan(self, b_=0):
        
        
        return self.compareint(b_) > 0
    # end def isgreaterthan
    #// 
    #// @param int $b
    #// @return bool
    #//
    def islessthanint(self, b_=0):
        
        
        return self.compareint(b_) < 0
    # end def islessthanint
    #// 
    #// @param int $c
    #// @return ParagonIE_Sodium_Core32_Int32
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArrayAccess
    #//
    def rotateleft(self, c_=0):
        
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(c_, "int", 1)
        #// @var int $c
        c_ = php_int(c_)
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
        return_.unsignedInt = self.unsignedInt
        c_ &= 31
        if c_ == 0:
            #// NOP, but we want a copy.
            return_.limbs = self.limbs
        else:
            #// @var int $c
            #// @var int $idx_shift
            idx_shift_ = c_ >> 4 & 1
            #// @var int $sub_shift
            sub_shift_ = c_ & 15
            #// @var array<int, int> $limbs
            limbs_ = return_.limbs
            #// @var array<int, int> $myLimbs
            myLimbs_ = self.limbs
            i_ = 1
            while i_ >= 0:
                
                #// @var int $j
                j_ = i_ + idx_shift_ & 1
                #// @var int $k
                k_ = i_ + idx_shift_ + 1 & 1
                limbs_[i_] = php_int(php_int(myLimbs_[j_]) << sub_shift_ | php_int(myLimbs_[k_]) >> 16 - sub_shift_ & 65535)
                i_ -= 1
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
    def rotateright(self, c_=0):
        
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(c_, "int", 1)
        #// @var int $c
        c_ = php_int(c_)
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
        return_.unsignedInt = self.unsignedInt
        c_ &= 31
        #// @var int $c
        if c_ == 0:
            #// NOP, but we want a copy.
            return_.limbs = self.limbs
        else:
            #// @var int $c
            #// @var int $idx_shift
            idx_shift_ = c_ >> 4 & 1
            #// @var int $sub_shift
            sub_shift_ = c_ & 15
            #// @var array<int, int> $limbs
            limbs_ = return_.limbs
            #// @var array<int, int> $myLimbs
            myLimbs_ = self.limbs
            i_ = 1
            while i_ >= 0:
                
                #// @var int $j
                j_ = i_ - idx_shift_ & 1
                #// @var int $k
                k_ = i_ - idx_shift_ - 1 & 1
                limbs_[i_] = php_int(php_int(myLimbs_[j_]) >> php_int(sub_shift_) | php_int(myLimbs_[k_]) << 16 - php_int(sub_shift_) & 65535)
                i_ -= 1
            # end while
        # end if
        return return_
    # end def rotateright
    #// 
    #// @param bool $bool
    #// @return self
    #//
    def setunsignedint(self, bool_=None):
        if bool_ is None:
            bool_ = False
        # end if
        
        self.unsignedInt = (not php_empty(lambda : bool_))
        return self
    # end def setunsignedint
    #// 
    #// @param int $c
    #// @return ParagonIE_Sodium_Core32_Int32
    #// @throws SodiumException
    #// @throws TypeError
    #//
    def shiftleft(self, c_=0):
        
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(c_, "int", 1)
        #// @var int $c
        c_ = php_int(c_)
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
        return_.unsignedInt = self.unsignedInt
        c_ &= 63
        #// @var int $c
        if c_ == 0:
            return_.limbs = self.limbs
        elif c_ < 0:
            #// @var int $c
            return self.shiftright(-c_)
        else:
            #// @var int $c
            #// @var int $tmp
            tmp_ = self.limbs[1] << c_
            return_.limbs[1] = php_int(tmp_ & 65535)
            #// @var int $carry
            carry_ = tmp_ >> 16
            #// @var int $tmp
            tmp_ = self.limbs[0] << c_ | carry_ & 65535
            return_.limbs[0] = php_int(tmp_ & 65535)
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
    def shiftright(self, c_=0):
        
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(c_, "int", 1)
        #// @var int $c
        c_ = php_int(c_)
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
        return_.unsignedInt = self.unsignedInt
        c_ &= 63
        #// @var int $c
        if c_ >= 16:
            return_.limbs = Array(php_int(self.overflow & 65535), php_int(self.limbs[0]))
            return_.overflow = self.overflow >> 16
            return return_.shiftright(c_ & 15)
        # end if
        if c_ == 0:
            return_.limbs = self.limbs
        elif c_ < 0:
            #// @var int $c
            return self.shiftleft(-c_)
        else:
            if (not php_is_int(c_)):
                raise php_new_class("TypeError", lambda : TypeError())
            # end if
            #// @var int $c
            #// $return->limbs[0] = (int) (($this->limbs[0] >> $c) & 0xffff);
            carryLeft_ = php_int(self.overflow & 1 << c_ + 1 - 1)
            return_.limbs[0] = php_int(self.limbs[0] >> c_ | carryLeft_ << 16 - c_ & 65535)
            carryRight_ = php_int(self.limbs[0] & 1 << c_ + 1 - 1)
            return_.limbs[1] = php_int(self.limbs[1] >> c_ | carryRight_ << 16 - c_ & 65535)
            return_.overflow >>= c_
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
    def subint(self, int_=None):
        
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(int_, "int", 1)
        #// @var int $int
        int_ = php_int(int_)
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
        return_.unsignedInt = self.unsignedInt
        #// @var int $tmp
        tmp_ = self.limbs[1] - int_ & 65535
        #// @var int $carry
        carry_ = tmp_ >> 16
        return_.limbs[1] = php_int(tmp_ & 65535)
        #// @var int $tmp
        tmp_ = self.limbs[0] - int_ >> 16 & 65535 + carry_
        return_.limbs[0] = php_int(tmp_ & 65535)
        return return_
    # end def subint
    #// 
    #// Subtract two int32 objects from each other
    #// 
    #// @param ParagonIE_Sodium_Core32_Int32 $b
    #// @return ParagonIE_Sodium_Core32_Int32
    #//
    def subint32(self, b_=None):
        
        
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
        return_.unsignedInt = self.unsignedInt
        #// @var int $tmp
        tmp_ = self.limbs[1] - b_.limbs[1] & 65535
        #// @var int $carry
        carry_ = tmp_ >> 16
        return_.limbs[1] = php_int(tmp_ & 65535)
        #// @var int $tmp
        tmp_ = self.limbs[0] - b_.limbs[0] & 65535 + carry_
        return_.limbs[0] = php_int(tmp_ & 65535)
        return return_
    # end def subint32
    #// 
    #// XOR this 32-bit integer with another.
    #// 
    #// @param ParagonIE_Sodium_Core32_Int32 $b
    #// @return ParagonIE_Sodium_Core32_Int32
    #//
    def xorint32(self, b_=None):
        
        
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
        return_.unsignedInt = self.unsignedInt
        return_.limbs = Array(php_int(self.limbs[0] ^ b_.limbs[0]), php_int(self.limbs[1] ^ b_.limbs[1]))
        return return_
    # end def xorint32
    #// 
    #// @param int $signed
    #// @return self
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def fromint(self, signed_=None):
        
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(signed_, "int", 1)
        #// @var int $signed
        signed_ = php_int(signed_)
        return php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32(Array(php_int(signed_ >> 16 & 65535), php_int(signed_ & 65535))))
    # end def fromint
    #// 
    #// @param string $string
    #// @return self
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def fromstring(self, string_=None):
        
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(string_, "string", 1)
        string_ = php_str(string_)
        if ParagonIE_Sodium_Core32_Util.strlen(string_) != 4:
            raise php_new_class("RangeException", lambda : RangeException("String must be 4 bytes; " + ParagonIE_Sodium_Core32_Util.strlen(string_) + " given."))
        # end if
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
        return_.limbs[0] = php_int(ParagonIE_Sodium_Core32_Util.chrtoint(string_[0]) & 255 << 8)
        return_.limbs[0] |= ParagonIE_Sodium_Core32_Util.chrtoint(string_[1]) & 255
        return_.limbs[1] = php_int(ParagonIE_Sodium_Core32_Util.chrtoint(string_[2]) & 255 << 8)
        return_.limbs[1] |= ParagonIE_Sodium_Core32_Util.chrtoint(string_[3]) & 255
        return return_
    # end def fromstring
    #// 
    #// @param string $string
    #// @return self
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def fromreversestring(self, string_=None):
        
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(string_, "string", 1)
        string_ = php_str(string_)
        if ParagonIE_Sodium_Core32_Util.strlen(string_) != 4:
            raise php_new_class("RangeException", lambda : RangeException("String must be 4 bytes; " + ParagonIE_Sodium_Core32_Util.strlen(string_) + " given."))
        # end if
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
        return_.limbs[0] = php_int(ParagonIE_Sodium_Core32_Util.chrtoint(string_[3]) & 255 << 8)
        return_.limbs[0] |= ParagonIE_Sodium_Core32_Util.chrtoint(string_[2]) & 255
        return_.limbs[1] = php_int(ParagonIE_Sodium_Core32_Util.chrtoint(string_[1]) & 255 << 8)
        return_.limbs[1] |= ParagonIE_Sodium_Core32_Util.chrtoint(string_[0]) & 255
        return return_
    # end def fromreversestring
    #// 
    #// @return array<int, int>
    #//
    def toarray(self):
        
        
        return Array(php_int(self.limbs[0] << 16 | self.limbs[1]))
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
        
        
        return php_int(self.limbs[0] & 65535 << 16 | self.limbs[1] & 65535)
    # end def toint
    #// 
    #// @return ParagonIE_Sodium_Core32_Int32
    #//
    def toint32(self):
        
        
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int32", lambda : ParagonIE_Sodium_Core32_Int32())
        return_.limbs[0] = php_int(self.limbs[0] & 65535)
        return_.limbs[1] = php_int(self.limbs[1] & 65535)
        return_.unsignedInt = self.unsignedInt
        return_.overflow = php_int(self.overflow & 2147483647)
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
            neg_ = -self.limbs[0] >> 15 & 1
            return_.limbs[0] = php_int(neg_ & 65535)
            return_.limbs[1] = php_int(neg_ & 65535)
        # end if
        return_.limbs[2] = php_int(self.limbs[0] & 65535)
        return_.limbs[3] = php_int(self.limbs[1] & 65535)
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
        except TypeError as ex_:
            #// PHP engine can't handle exceptions from __toString()
            return ""
        # end try
    # end def __tostring
# end class ParagonIE_Sodium_Core32_Int32
