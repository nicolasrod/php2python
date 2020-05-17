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
#// Class ParagonIE_Sodium_Core32_Int64
#// 
#// Encapsulates a 64-bit integer.
#// 
#// These are immutable. It always returns a new instance.
#//
class ParagonIE_Sodium_Core32_Int64():
    #// 
    #// @var array<int, int> - four 16-bit integers
    #//
    limbs = Array(0, 0, 0, 0)
    #// 
    #// @var int
    #//
    overflow = 0
    #// 
    #// @var bool
    #//
    unsignedInt = False
    #// 
    #// ParagonIE_Sodium_Core32_Int64 constructor.
    #// @param array $array
    #// @param bool $unsignedInt
    #//
    def __init__(self, array_=None, unsignedInt_=None):
        if array_ is None:
            array_ = Array(0, 0, 0, 0)
        # end if
        if unsignedInt_ is None:
            unsignedInt_ = False
        # end if
        
        self.limbs = Array(php_int(array_[0]), php_int(array_[1]), php_int(array_[2]), php_int(array_[3]))
        self.overflow = 0
        self.unsignedInt = unsignedInt_
    # end def __init__
    #// 
    #// Adds two int64 objects
    #// 
    #// @param ParagonIE_Sodium_Core32_Int64 $addend
    #// @return ParagonIE_Sodium_Core32_Int64
    #//
    def addint64(self, addend_=None):
        
        
        i0_ = self.limbs[0]
        i1_ = self.limbs[1]
        i2_ = self.limbs[2]
        i3_ = self.limbs[3]
        j0_ = addend_.limbs[0]
        j1_ = addend_.limbs[1]
        j2_ = addend_.limbs[2]
        j3_ = addend_.limbs[3]
        r3_ = i3_ + j3_ & 65535
        carry_ = r3_ >> 16
        r2_ = i2_ + j2_ & 65535 + carry_
        carry_ = r2_ >> 16
        r1_ = i1_ + j1_ & 65535 + carry_
        carry_ = r1_ >> 16
        r0_ = i0_ + j0_ & 65535 + carry_
        carry_ = r0_ >> 16
        r0_ &= 65535
        r1_ &= 65535
        r2_ &= 65535
        r3_ &= 65535
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64(Array(r0_, r1_, r2_, r3_)))
        return_.overflow = carry_
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
    def addint(self, int_=None):
        
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(int_, "int", 1)
        #// @var int $int
        int_ = php_int(int_)
        i0_ = self.limbs[0]
        i1_ = self.limbs[1]
        i2_ = self.limbs[2]
        i3_ = self.limbs[3]
        r3_ = i3_ + int_ & 65535
        carry_ = r3_ >> 16
        r2_ = i2_ + int_ >> 16 & 65535 + carry_
        carry_ = r2_ >> 16
        r1_ = i1_ + carry_
        carry_ = r1_ >> 16
        r0_ = i0_ + carry_
        carry_ = r0_ >> 16
        r0_ &= 65535
        r1_ &= 65535
        r2_ &= 65535
        r3_ &= 65535
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64(Array(r0_, r1_, r2_, r3_)))
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
        i_ = 4
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
            #// int
            gt_ |= x2_ - x1_ >> 8 & eq_
            #// int
            eq_ &= x2_ ^ x1_ - 1 >> 8
        # end while
        return gt_ + gt_ - eq_ + 1
    # end def compareint
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
    #// @param int $hi
    #// @param int $lo
    #// @return ParagonIE_Sodium_Core32_Int64
    #//
    def mask64(self, hi_=0, lo_=0):
        
        
        #// @var int $a
        a_ = hi_ >> 16 & 65535
        #// @var int $b
        b_ = hi_ & 65535
        #// @var int $c
        c_ = lo_ >> 16 & 65535
        #// @var int $d
        d_ = lo_ & 65535
        return php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64(Array(self.limbs[0] & a_, self.limbs[1] & b_, self.limbs[2] & c_, self.limbs[3] & d_), self.unsignedInt))
    # end def mask64
    #// 
    #// @param int $int
    #// @param int $size
    #// @return ParagonIE_Sodium_Core32_Int64
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedAssignment
    #//
    def mulint(self, int_=0, size_=0):
        
        
        if ParagonIE_Sodium_Compat.fastMult:
            return self.mulintfast(int_)
        # end if
        ParagonIE_Sodium_Core32_Util.declarescalartype(int_, "int", 1)
        ParagonIE_Sodium_Core32_Util.declarescalartype(size_, "int", 2)
        #// @var int $int
        int_ = php_int(int_)
        #// @var int $size
        size_ = php_int(size_)
        if (not size_):
            size_ = 63
        # end if
        a_ = copy.deepcopy(self)
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        return_.unsignedInt = self.unsignedInt
        #// Initialize:
        ret0_ = 0
        ret1_ = 0
        ret2_ = 0
        ret3_ = 0
        a0_ = a_.limbs[0]
        a1_ = a_.limbs[1]
        a2_ = a_.limbs[2]
        a3_ = a_.limbs[3]
        #// @var int $size
        #// @var int $i
        i_ = size_
        while i_ >= 0:
            
            mask_ = -int_ & 1
            x0_ = a0_ & mask_
            x1_ = a1_ & mask_
            x2_ = a2_ & mask_
            x3_ = a3_ & mask_
            ret3_ += x3_
            c_ = ret3_ >> 16
            ret2_ += x2_ + c_
            c_ = ret2_ >> 16
            ret1_ += x1_ + c_
            c_ = ret1_ >> 16
            ret0_ += x0_ + c_
            ret0_ &= 65535
            ret1_ &= 65535
            ret2_ &= 65535
            ret3_ &= 65535
            a3_ = a3_ << 1
            x3_ = a3_ >> 16
            a2_ = a2_ << 1 | x3_
            x2_ = a2_ >> 16
            a1_ = a1_ << 1 | x2_
            x1_ = a1_ >> 16
            a0_ = a0_ << 1 | x1_
            a0_ &= 65535
            a1_ &= 65535
            a2_ &= 65535
            a3_ &= 65535
            int_ >>= 1
            i_ -= 1
        # end while
        return_.limbs[0] = ret0_
        return_.limbs[1] = ret1_
        return_.limbs[2] = ret2_
        return_.limbs[3] = ret3_
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
    def ctselect(self, A_=None, B_=None):
        
        
        a_ = copy.deepcopy(A_)
        b_ = copy.deepcopy(B_)
        #// @var int $aNeg
        aNeg_ = a_.limbs[0] >> 15 & 1
        #// @var int $bNeg
        bNeg_ = b_.limbs[0] >> 15 & 1
        #// @var int $m
        m_ = -aNeg_ & bNeg_ | 1
        #// @var int $swap
        swap_ = bNeg_ & (1 << (aNeg_).bit_length()) - 1 - aNeg_
        #// @var int $d
        d_ = -swap_
        #// 
        #// if ($bNeg && !$aNeg) {
        #// $a = clone $int;
        #// $b = clone $this;
        #// } elseif($bNeg && $aNeg) {
        #// $a = $this->mulInt(-1);
        #// $b = $int->mulInt(-1);
        #// }
        #//
        x_ = a_.xorint64(b_).mask64(d_, d_)
        return Array(a_.xorint64(x_).mulint(m_), b_.xorint64(x_).mulint(m_))
    # end def ctselect
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
    #// @return ParagonIE_Sodium_Core32_Int64
    #//
    def mulintfast(self, int_=None):
        
        
        #// Handle negative numbers
        aNeg_ = self.limbs[0] >> 15 & 1
        bNeg_ = int_ >> 31 & 1
        a_ = array_reverse(self.limbs)
        b_ = Array(int_ & 65535, int_ >> 16 & 65535, -bNeg_ & 65535, -bNeg_ & 65535)
        if aNeg_:
            i_ = 0
            while i_ < 4:
                
                a_[i_] = a_[i_] ^ 65535 & 65535
                i_ += 1
            # end while
            a_[0] += 1
        # end if
        if bNeg_:
            i_ = 0
            while i_ < 4:
                
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
            while i_ < 4:
                
                res_[i_] = 65535 ^ res_[i_] & 65535
                i_ += 1
            # end while
            #// Handle integer overflow
            c_ = 1
            i_ = 0
            while i_ < 4:
                
                res_[i_] += c_
                c_ = res_[i_] >> 16
                res_[i_] &= 65535
                i_ += 1
            # end while
        # end if
        #// Return our values
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        return_.limbs = Array(res_[3] & 65535, res_[2] & 65535, res_[1] & 65535, res_[0] & 65535)
        if php_count(res_) > 4:
            return_.overflow = res_[4] & 65535
        # end if
        return_.unsignedInt = self.unsignedInt
        return return_
    # end def mulintfast
    #// 
    #// @param ParagonIE_Sodium_Core32_Int64 $right
    #// @return ParagonIE_Sodium_Core32_Int64
    #//
    def mulint64fast(self, right_=None):
        
        
        aNeg_ = self.limbs[0] >> 15 & 1
        bNeg_ = right_.limbs[0] >> 15 & 1
        a_ = array_reverse(self.limbs)
        b_ = array_reverse(right_.limbs)
        if aNeg_:
            i_ = 0
            while i_ < 4:
                
                a_[i_] = a_[i_] ^ 65535 & 65535
                i_ += 1
            # end while
            a_[0] += 1
        # end if
        if bNeg_:
            i_ = 0
            while i_ < 4:
                
                b_[i_] = b_[i_] ^ 65535 & 65535
                i_ += 1
            # end while
            b_[0] += 1
        # end if
        res_ = self.multiplylong(a_, b_)
        if aNeg_ != bNeg_:
            if aNeg_ != bNeg_:
                i_ = 0
                while i_ < 4:
                    
                    res_[i_] = res_[i_] ^ 65535 & 65535
                    i_ += 1
                # end while
                c_ = 1
                i_ = 0
                while i_ < 4:
                    
                    res_[i_] += c_
                    c_ = res_[i_] >> 16
                    res_[i_] &= 65535
                    i_ += 1
                # end while
            # end if
        # end if
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        return_.limbs = Array(res_[3] & 65535, res_[2] & 65535, res_[1] & 65535, res_[0] & 65535)
        if php_count(res_) > 4:
            return_.overflow = res_[4]
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
    def mulint64(self, int_=None, size_=0):
        
        
        if ParagonIE_Sodium_Compat.fastMult:
            return self.mulint64fast(int_)
        # end if
        ParagonIE_Sodium_Core32_Util.declarescalartype(size_, "int", 2)
        if (not size_):
            size_ = 63
        # end if
        a_, b_ = self.ctselect(self, int_)
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        return_.unsignedInt = self.unsignedInt
        #// Initialize:
        ret0_ = 0
        ret1_ = 0
        ret2_ = 0
        ret3_ = 0
        a0_ = a_.limbs[0]
        a1_ = a_.limbs[1]
        a2_ = a_.limbs[2]
        a3_ = a_.limbs[3]
        b0_ = b_.limbs[0]
        b1_ = b_.limbs[1]
        b2_ = b_.limbs[2]
        b3_ = b_.limbs[3]
        #// @var int $size
        #// @var int $i
        i_ = php_int(size_)
        while i_ >= 0:
            
            mask_ = -b3_ & 1
            x0_ = a0_ & mask_
            x1_ = a1_ & mask_
            x2_ = a2_ & mask_
            x3_ = a3_ & mask_
            ret3_ += x3_
            c_ = ret3_ >> 16
            ret2_ += x2_ + c_
            c_ = ret2_ >> 16
            ret1_ += x1_ + c_
            c_ = ret1_ >> 16
            ret0_ += x0_ + c_
            ret0_ &= 65535
            ret1_ &= 65535
            ret2_ &= 65535
            ret3_ &= 65535
            a3_ = a3_ << 1
            x3_ = a3_ >> 16
            a2_ = a2_ << 1 | x3_
            x2_ = a2_ >> 16
            a1_ = a1_ << 1 | x2_
            x1_ = a1_ >> 16
            a0_ = a0_ << 1 | x1_
            a0_ &= 65535
            a1_ &= 65535
            a2_ &= 65535
            a3_ &= 65535
            x0_ = b0_ & 1 << 16
            x1_ = b1_ & 1 << 16
            x2_ = b2_ & 1 << 16
            b0_ = b0_ >> 1
            b1_ = b1_ | x0_ >> 1
            b2_ = b2_ | x1_ >> 1
            b3_ = b3_ | x2_ >> 1
            b0_ &= 65535
            b1_ &= 65535
            b2_ &= 65535
            b3_ &= 65535
            i_ -= 1
        # end while
        return_.limbs[0] = ret0_
        return_.limbs[1] = ret1_
        return_.limbs[2] = ret2_
        return_.limbs[3] = ret3_
        return return_
    # end def mulint64
    #// 
    #// OR this 64-bit integer with another.
    #// 
    #// @param ParagonIE_Sodium_Core32_Int64 $b
    #// @return ParagonIE_Sodium_Core32_Int64
    #//
    def orint64(self, b_=None):
        
        
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        return_.unsignedInt = self.unsignedInt
        return_.limbs = Array(php_int(self.limbs[0] | b_.limbs[0]), php_int(self.limbs[1] | b_.limbs[1]), php_int(self.limbs[2] | b_.limbs[2]), php_int(self.limbs[3] | b_.limbs[3]))
        return return_
    # end def orint64
    #// 
    #// @param int $c
    #// @return ParagonIE_Sodium_Core32_Int64
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArrayAccess
    #//
    def rotateleft(self, c_=0):
        
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(c_, "int", 1)
        #// @var int $c
        c_ = php_int(c_)
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        return_.unsignedInt = self.unsignedInt
        c_ &= 63
        if c_ == 0:
            #// NOP, but we want a copy.
            return_.limbs = self.limbs
        else:
            #// @var array<int, int> $limbs
            limbs_ = return_.limbs
            #// @var array<int, int> $myLimbs
            myLimbs_ = self.limbs
            #// @var int $idx_shift
            idx_shift_ = c_ >> 4 & 3
            #// @var int $sub_shift
            sub_shift_ = c_ & 15
            i_ = 3
            while i_ >= 0:
                
                #// @var int $j
                j_ = i_ + idx_shift_ & 3
                #// @var int $k
                k_ = i_ + idx_shift_ + 1 & 3
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
    #// @return ParagonIE_Sodium_Core32_Int64
    #// @throws SodiumException
    #// @throws TypeError
    #// @psalm-suppress MixedArrayAccess
    #//
    def rotateright(self, c_=0):
        
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(c_, "int", 1)
        #// @var int $c
        c_ = php_int(c_)
        #// @var ParagonIE_Sodium_Core32_Int64 $return
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        return_.unsignedInt = self.unsignedInt
        c_ &= 63
        #// @var int $c
        if c_ == 0:
            #// NOP, but we want a copy.
            return_.limbs = self.limbs
        else:
            #// @var array<int, int> $limbs
            limbs_ = return_.limbs
            #// @var array<int, int> $myLimbs
            myLimbs_ = self.limbs
            #// @var int $idx_shift
            idx_shift_ = c_ >> 4 & 3
            #// @var int $sub_shift
            sub_shift_ = c_ & 15
            i_ = 3
            while i_ >= 0:
                
                #// @var int $j
                j_ = i_ - idx_shift_ & 3
                #// @var int $k
                k_ = i_ - idx_shift_ - 1 & 3
                limbs_[i_] = php_int(php_int(myLimbs_[j_]) >> php_int(sub_shift_) | php_int(myLimbs_[k_]) << 16 - php_int(sub_shift_) & 65535)
                i_ -= 1
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
    def shiftleft(self, c_=0):
        
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(c_, "int", 1)
        #// @var int $c
        c_ = php_int(c_)
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        return_.unsignedInt = self.unsignedInt
        c_ &= 63
        if c_ >= 16:
            if c_ >= 48:
                return_.limbs = Array(self.limbs[3], 0, 0, 0)
            elif c_ >= 32:
                return_.limbs = Array(self.limbs[2], self.limbs[3], 0, 0)
            else:
                return_.limbs = Array(self.limbs[1], self.limbs[2], self.limbs[3], 0)
            # end if
            return return_.shiftleft(c_ & 15)
        # end if
        if c_ == 0:
            return_.limbs = self.limbs
        elif c_ < 0:
            #// @var int $c
            return self.shiftright(-c_)
        else:
            if (not php_is_int(c_)):
                raise php_new_class("TypeError", lambda : TypeError())
            # end if
            #// @var int $carry
            carry_ = 0
            i_ = 3
            while i_ >= 0:
                
                #// @var int $tmp
                tmp_ = self.limbs[i_] << c_ | carry_ & 65535
                return_.limbs[i_] = php_int(tmp_ & 65535)
                #// @var int $carry
                carry_ = tmp_ >> 16
                i_ -= 1
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
    def shiftright(self, c_=0):
        
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(c_, "int", 1)
        c_ = php_int(c_)
        #// @var int $c
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        return_.unsignedInt = self.unsignedInt
        c_ &= 63
        negative_ = -self.limbs[0] >> 15 & 1
        if c_ >= 16:
            if c_ >= 48:
                return_.limbs = Array(php_int(negative_ & 65535), php_int(negative_ & 65535), php_int(negative_ & 65535), php_int(self.limbs[0]))
            elif c_ >= 32:
                return_.limbs = Array(php_int(negative_ & 65535), php_int(negative_ & 65535), php_int(self.limbs[0]), php_int(self.limbs[1]))
            else:
                return_.limbs = Array(php_int(negative_ & 65535), php_int(self.limbs[0]), php_int(self.limbs[1]), php_int(self.limbs[2]))
            # end if
            return return_.shiftright(c_ & 15)
        # end if
        if c_ == 0:
            return_.limbs = self.limbs
        elif c_ < 0:
            return self.shiftleft(-c_)
        else:
            if (not php_is_int(c_)):
                raise php_new_class("TypeError", lambda : TypeError())
            # end if
            #// @var int $carryRight
            carryRight_ = negative_ & 65535
            mask_ = php_int(1 << c_ + 1 - 1 & 65535)
            i_ = 0
            while i_ < 4:
                
                return_.limbs[i_] = php_int(self.limbs[i_] >> c_ | carryRight_ << 16 - c_ & 65535)
                carryRight_ = php_int(self.limbs[i_] & mask_)
                i_ += 1
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
    def subint(self, int_=None):
        
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(int_, "int", 1)
        int_ = php_int(int_)
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        return_.unsignedInt = self.unsignedInt
        #// @var int $carry
        carry_ = 0
        i_ = 3
        while i_ >= 0:
            
            #// @var int $tmp
            tmp_ = self.limbs[i_] - int_ >> 16 & 65535 + carry_
            #// @var int $carry
            carry_ = tmp_ >> 16
            return_.limbs[i_] = php_int(tmp_ & 65535)
            i_ -= 1
        # end while
        return return_
    # end def subint
    #// 
    #// The difference between two Int64 objects.
    #// 
    #// @param ParagonIE_Sodium_Core32_Int64 $b
    #// @return ParagonIE_Sodium_Core32_Int64
    #//
    def subint64(self, b_=None):
        
        
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        return_.unsignedInt = self.unsignedInt
        #// @var int $carry
        carry_ = 0
        i_ = 3
        while i_ >= 0:
            
            #// @var int $tmp
            tmp_ = self.limbs[i_] - b_.limbs[i_] + carry_
            #// @var int $carry
            carry_ = tmp_ >> 16
            return_.limbs[i_] = php_int(tmp_ & 65535)
            i_ -= 1
        # end while
        return return_
    # end def subint64
    #// 
    #// XOR this 64-bit integer with another.
    #// 
    #// @param ParagonIE_Sodium_Core32_Int64 $b
    #// @return ParagonIE_Sodium_Core32_Int64
    #//
    def xorint64(self, b_=None):
        
        
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        return_.unsignedInt = self.unsignedInt
        return_.limbs = Array(php_int(self.limbs[0] ^ b_.limbs[0]), php_int(self.limbs[1] ^ b_.limbs[1]), php_int(self.limbs[2] ^ b_.limbs[2]), php_int(self.limbs[3] ^ b_.limbs[3]))
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
    def fromints(self, low_=None, high_=None):
        
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(low_, "int", 1)
        ParagonIE_Sodium_Core32_Util.declarescalartype(high_, "int", 2)
        high_ = php_int(high_)
        low_ = php_int(low_)
        return php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64(Array(php_int(high_ >> 16 & 65535), php_int(high_ & 65535), php_int(low_ >> 16 & 65535), php_int(low_ & 65535))))
    # end def fromints
    #// 
    #// @param int $low
    #// @return self
    #// @throws SodiumException
    #// @throws TypeError
    #//
    @classmethod
    def fromint(self, low_=None):
        
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(low_, "int", 1)
        low_ = php_int(low_)
        return php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64(Array(0, 0, php_int(low_ >> 16 & 65535), php_int(low_ & 65535))))
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
    def fromstring(self, string_=None):
        
        
        ParagonIE_Sodium_Core32_Util.declarescalartype(string_, "string", 1)
        string_ = php_str(string_)
        if ParagonIE_Sodium_Core32_Util.strlen(string_) != 8:
            raise php_new_class("RangeException", lambda : RangeException("String must be 8 bytes; " + ParagonIE_Sodium_Core32_Util.strlen(string_) + " given."))
        # end if
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        return_.limbs[0] = php_int(ParagonIE_Sodium_Core32_Util.chrtoint(string_[0]) & 255 << 8)
        return_.limbs[0] |= ParagonIE_Sodium_Core32_Util.chrtoint(string_[1]) & 255
        return_.limbs[1] = php_int(ParagonIE_Sodium_Core32_Util.chrtoint(string_[2]) & 255 << 8)
        return_.limbs[1] |= ParagonIE_Sodium_Core32_Util.chrtoint(string_[3]) & 255
        return_.limbs[2] = php_int(ParagonIE_Sodium_Core32_Util.chrtoint(string_[4]) & 255 << 8)
        return_.limbs[2] |= ParagonIE_Sodium_Core32_Util.chrtoint(string_[5]) & 255
        return_.limbs[3] = php_int(ParagonIE_Sodium_Core32_Util.chrtoint(string_[6]) & 255 << 8)
        return_.limbs[3] |= ParagonIE_Sodium_Core32_Util.chrtoint(string_[7]) & 255
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
        if ParagonIE_Sodium_Core32_Util.strlen(string_) != 8:
            raise php_new_class("RangeException", lambda : RangeException("String must be 8 bytes; " + ParagonIE_Sodium_Core32_Util.strlen(string_) + " given."))
        # end if
        return_ = php_new_class("ParagonIE_Sodium_Core32_Int64", lambda : ParagonIE_Sodium_Core32_Int64())
        return_.limbs[0] = php_int(ParagonIE_Sodium_Core32_Util.chrtoint(string_[7]) & 255 << 8)
        return_.limbs[0] |= ParagonIE_Sodium_Core32_Util.chrtoint(string_[6]) & 255
        return_.limbs[1] = php_int(ParagonIE_Sodium_Core32_Util.chrtoint(string_[5]) & 255 << 8)
        return_.limbs[1] |= ParagonIE_Sodium_Core32_Util.chrtoint(string_[4]) & 255
        return_.limbs[2] = php_int(ParagonIE_Sodium_Core32_Util.chrtoint(string_[3]) & 255 << 8)
        return_.limbs[2] |= ParagonIE_Sodium_Core32_Util.chrtoint(string_[2]) & 255
        return_.limbs[3] = php_int(ParagonIE_Sodium_Core32_Util.chrtoint(string_[1]) & 255 << 8)
        return_.limbs[3] |= ParagonIE_Sodium_Core32_Util.chrtoint(string_[0]) & 255
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
    def setunsignedint(self, bool_=None):
        if bool_ is None:
            bool_ = False
        # end if
        
        self.unsignedInt = (not php_empty(lambda : bool_))
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
        except TypeError as ex_:
            #// PHP engine can't handle exceptions from __toString()
            return ""
        # end try
    # end def __tostring
# end class ParagonIE_Sodium_Core32_Int64
