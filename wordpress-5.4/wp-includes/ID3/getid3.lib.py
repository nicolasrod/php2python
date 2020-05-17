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
#// getID3() by James Heinrich <info@getid3.org>
#// available at https://github.com/JamesHeinrich/getID3
#// or https://www.getid3.org
#// or http://getid3.sourceforge.net
#// 
#// getid3.lib.php - part of getID3()
#// see readme.txt for more details
#// 
#//
class getid3_lib():
    #// 
    #// @param string $string
    #// @param bool   $hex
    #// @param bool   $spaces
    #// @param string $htmlencoding
    #// 
    #// @return string
    #//
    @classmethod
    def printhexbytes(self, string_=None, hex_=None, spaces_=None, htmlencoding_="UTF-8"):
        if hex_ is None:
            hex_ = True
        # end if
        if spaces_ is None:
            spaces_ = True
        # end if
        
        returnstring_ = ""
        i_ = 0
        while i_ < php_strlen(string_):
            
            if hex_:
                returnstring_ += php_str_pad(dechex(php_ord(string_[i_])), 2, "0", STR_PAD_LEFT)
            else:
                returnstring_ += " " + string_[i_] if php_preg_match("#[ -~]#", string_[i_]) else "Â¤"
            # end if
            if spaces_:
                returnstring_ += " "
            # end if
            i_ += 1
        # end while
        if (not php_empty(lambda : htmlencoding_)):
            if htmlencoding_ == True:
                htmlencoding_ = "UTF-8"
                pass
            # end if
            returnstring_ = htmlentities(returnstring_, ENT_QUOTES, htmlencoding_)
        # end if
        return returnstring_
    # end def printhexbytes
    #// 
    #// Truncates a floating-point number at the decimal point.
    #// 
    #// @param float $floatnumber
    #// 
    #// @return float|int returns int (if possible, otherwise float)
    #//
    @classmethod
    def trunc(self, floatnumber_=None):
        
        
        if floatnumber_ >= 1:
            truncatednumber_ = floor(floatnumber_)
        elif floatnumber_ <= -1:
            truncatednumber_ = ceil(floatnumber_)
        else:
            truncatednumber_ = 0
        # end if
        if self.intvaluesupported(truncatednumber_):
            truncatednumber_ = php_int(truncatednumber_)
        # end if
        return truncatednumber_
    # end def trunc
    #// 
    #// @param int|null $variable
    #// @param int      $increment
    #// 
    #// @return bool
    #//
    @classmethod
    def safe_inc(self, variable_=None, increment_=1):
        
        
        if (php_isset(lambda : variable_)):
            variable_ += increment_
        else:
            variable_ = increment_
        # end if
        return True
    # end def safe_inc
    #// 
    #// @param int|float $floatnum
    #// 
    #// @return int|float
    #//
    @classmethod
    def castasint(self, floatnum_=None):
        
        
        #// convert to float if not already
        floatnum_ = php_float(floatnum_)
        #// convert a float to type int, only if possible
        if self.trunc(floatnum_) == floatnum_:
            #// it's not floating point
            if self.intvaluesupported(floatnum_):
                #// it's within int range
                floatnum_ = php_int(floatnum_)
            # end if
        # end if
        return floatnum_
    # end def castasint
    #// 
    #// @param int $num
    #// 
    #// @return bool
    #//
    @classmethod
    def intvaluesupported(self, num_=None):
        
        
        hasINT64_ = None
        if hasINT64_ == None:
            #// 10x faster than is_null()
            hasINT64_ = php_is_int(pow(2, 31))
            #// 32-bit int are limited to (2^31)-1
            if (not hasINT64_) and (not php_defined("PHP_INT_MIN")):
                php_define("PHP_INT_MIN", (1 << (PHP_INT_MAX).bit_length()) - 1 - PHP_INT_MAX)
            # end if
        # end if
        #// if integers are 64-bit - no other check required
        if hasINT64_ or num_ <= PHP_INT_MAX and num_ >= PHP_INT_MIN:
            return True
        # end if
        return False
    # end def intvaluesupported
    #// 
    #// @param string $fraction
    #// 
    #// @return float
    #//
    @classmethod
    def decimalizefraction(self, fraction_=None):
        
        
        numerator_, denominator_ = php_explode("/", fraction_)
        return numerator_ / denominator_ if denominator_ else 1
    # end def decimalizefraction
    #// 
    #// @param string $binarynumerator
    #// 
    #// @return float
    #//
    @classmethod
    def decimalbinary2float(self, binarynumerator_=None):
        
        
        numerator_ = self.bin2dec(binarynumerator_)
        denominator_ = self.bin2dec("1" + php_str_repeat("0", php_strlen(binarynumerator_)))
        return numerator_ / denominator_
    # end def decimalbinary2float
    #// 
    #// @link http://www.scri.fsu.edu/~jac/MAD3401/Backgrnd/binary.html
    #// 
    #// @param string $binarypointnumber
    #// @param int    $maxbits
    #// 
    #// @return array
    #//
    @classmethod
    def normalizebinarypoint(self, binarypointnumber_=None, maxbits_=52):
        
        
        if php_strpos(binarypointnumber_, ".") == False:
            binarypointnumber_ = "0." + binarypointnumber_
        elif binarypointnumber_[0] == ".":
            binarypointnumber_ = "0" + binarypointnumber_
        # end if
        exponent_ = 0
        while True:
            
            if not (binarypointnumber_[0] != "1" or php_substr(binarypointnumber_, 1, 1) != "."):
                break
            # end if
            if php_substr(binarypointnumber_, 1, 1) == ".":
                exponent_ -= 1
                binarypointnumber_ = php_substr(binarypointnumber_, 2, 1) + "." + php_substr(binarypointnumber_, 3)
            else:
                pointpos_ = php_strpos(binarypointnumber_, ".")
                exponent_ += pointpos_ - 1
                binarypointnumber_ = php_str_replace(".", "", binarypointnumber_)
                binarypointnumber_ = binarypointnumber_[0] + "." + php_substr(binarypointnumber_, 1)
            # end if
        # end while
        binarypointnumber_ = php_str_pad(php_substr(binarypointnumber_, 0, maxbits_ + 2), maxbits_ + 2, "0", STR_PAD_RIGHT)
        return Array({"normalized": binarypointnumber_, "exponent": php_int(exponent_)})
    # end def normalizebinarypoint
    #// 
    #// @link http://www.scri.fsu.edu/~jac/MAD3401/Backgrnd/binary.html
    #// 
    #// @param float $floatvalue
    #// 
    #// @return string
    #//
    @classmethod
    def float2binarydecimal(self, floatvalue_=None):
        
        
        maxbits_ = 128
        #// to how many bits of precision should the calculations be taken?
        intpart_ = self.trunc(floatvalue_)
        floatpart_ = abs(floatvalue_ - intpart_)
        pointbitstring_ = ""
        while True:
            
            if not (floatpart_ != 0 and php_strlen(pointbitstring_) < maxbits_):
                break
            # end if
            floatpart_ *= 2
            pointbitstring_ += php_str(self.trunc(floatpart_))
            floatpart_ -= self.trunc(floatpart_)
        # end while
        binarypointnumber_ = decbin(intpart_) + "." + pointbitstring_
        return binarypointnumber_
    # end def float2binarydecimal
    #// 
    #// @link http://www.scri.fsu.edu/~jac/MAD3401/Backgrnd/ieee-expl.html
    #// 
    #// @param float $floatvalue
    #// @param int $bits
    #// 
    #// @return string|false
    #//
    @classmethod
    def float2string(self, floatvalue_=None, bits_=None):
        
        
        exponentbits_ = 0
        fractionbits_ = 0
        for case in Switch(bits_):
            if case(32):
                exponentbits_ = 8
                fractionbits_ = 23
                break
            # end if
            if case(64):
                exponentbits_ = 11
                fractionbits_ = 52
                break
            # end if
            if case():
                return False
                break
            # end if
        # end for
        if floatvalue_ >= 0:
            signbit_ = "0"
        else:
            signbit_ = "1"
        # end if
        normalizedbinary_ = self.normalizebinarypoint(self.float2binarydecimal(floatvalue_), fractionbits_)
        biasedexponent_ = pow(2, exponentbits_ - 1) - 1 + normalizedbinary_["exponent"]
        #// (127 or 1023) +/- exponent
        exponentbitstring_ = php_str_pad(decbin(biasedexponent_), exponentbits_, "0", STR_PAD_LEFT)
        fractionbitstring_ = php_str_pad(php_substr(normalizedbinary_["normalized"], 2), fractionbits_, "0", STR_PAD_RIGHT)
        return self.bigendian2string(self.bin2dec(signbit_ + exponentbitstring_ + fractionbitstring_), bits_ % 8, False)
    # end def float2string
    #// 
    #// @param string $byteword
    #// 
    #// @return float|false
    #//
    @classmethod
    def littleendian2float(self, byteword_=None):
        
        
        return self.bigendian2float(php_strrev(byteword_))
    # end def littleendian2float
    #// 
    #// ANSI/IEEE Standard 754-1985, Standard for Binary Floating Point Arithmetic
    #// 
    #// @link http://www.psc.edu/general/software/packages/ieee/ieee.html
    #// @link http://www.scri.fsu.edu/~jac/MAD3401/Backgrnd/ieee.html
    #// 
    #// @param string $byteword
    #// 
    #// @return float|false
    #//
    @classmethod
    def bigendian2float(self, byteword_=None):
        
        
        bitword_ = self.bigendian2bin(byteword_)
        if (not bitword_):
            return 0
        # end if
        signbit_ = bitword_[0]
        floatvalue_ = 0
        exponentbits_ = 0
        fractionbits_ = 0
        for case in Switch(php_strlen(byteword_) * 8):
            if case(32):
                exponentbits_ = 8
                fractionbits_ = 23
                break
            # end if
            if case(64):
                exponentbits_ = 11
                fractionbits_ = 52
                break
            # end if
            if case(80):
                #// 80-bit Apple SANE format
                #// http://www.mactech.com/articles/mactech/Vol.06/06.01/SANENormalized
                exponentstring_ = php_substr(bitword_, 1, 15)
                isnormalized_ = php_intval(bitword_[16])
                fractionstring_ = php_substr(bitword_, 17, 63)
                exponent_ = pow(2, self.bin2dec(exponentstring_) - 16383)
                fraction_ = isnormalized_ + self.decimalbinary2float(fractionstring_)
                floatvalue_ = exponent_ * fraction_
                if signbit_ == "1":
                    floatvalue_ *= -1
                # end if
                return floatvalue_
                break
            # end if
            if case():
                return False
                break
            # end if
        # end for
        exponentstring_ = php_substr(bitword_, 1, exponentbits_)
        fractionstring_ = php_substr(bitword_, exponentbits_ + 1, fractionbits_)
        exponent_ = self.bin2dec(exponentstring_)
        fraction_ = self.bin2dec(fractionstring_)
        if exponent_ == pow(2, exponentbits_) - 1 and fraction_ != 0:
            #// Not a Number
            floatvalue_ = False
        elif exponent_ == pow(2, exponentbits_) - 1 and fraction_ == 0:
            if signbit_ == "1":
                floatvalue_ = "-infinity"
            else:
                floatvalue_ = "+infinity"
            # end if
        elif exponent_ == 0 and fraction_ == 0:
            if signbit_ == "1":
                floatvalue_ = -0
            else:
                floatvalue_ = 0
            # end if
            floatvalue_ = 0 if signbit_ else -0
        elif exponent_ == 0 and fraction_ != 0:
            #// These are 'unnormalized' values
            floatvalue_ = pow(2, -1 * pow(2, exponentbits_ - 1) - 2) * self.decimalbinary2float(fractionstring_)
            if signbit_ == "1":
                floatvalue_ *= -1
            # end if
        elif exponent_ != 0:
            floatvalue_ = pow(2, exponent_ - pow(2, exponentbits_ - 1) - 1) * 1 + self.decimalbinary2float(fractionstring_)
            if signbit_ == "1":
                floatvalue_ *= -1
            # end if
        # end if
        return php_float(floatvalue_)
    # end def bigendian2float
    #// 
    #// @param string $byteword
    #// @param bool   $synchsafe
    #// @param bool   $signed
    #// 
    #// @return int|float|false
    #// @throws Exception
    #//
    @classmethod
    def bigendian2int(self, byteword_=None, synchsafe_=None, signed_=None):
        if synchsafe_ is None:
            synchsafe_ = False
        # end if
        if signed_ is None:
            signed_ = False
        # end if
        
        intvalue_ = 0
        bytewordlen_ = php_strlen(byteword_)
        if bytewordlen_ == 0:
            return False
        # end if
        i_ = 0
        while i_ < bytewordlen_:
            
            if synchsafe_:
                #// disregard MSB, effectively 7-bit bytes
                #// $intvalue = $intvalue | (ord($byteword{$i}) & 0x7F) << (($bytewordlen - 1 - $i) * 7); // faster, but runs into problems past 2^31 on 32-bit systems
                intvalue_ += php_ord(byteword_[i_]) & 127 * pow(2, bytewordlen_ - 1 - i_ * 7)
            else:
                intvalue_ += php_ord(byteword_[i_]) * pow(256, bytewordlen_ - 1 - i_)
            # end if
            i_ += 1
        # end while
        if signed_ and (not synchsafe_):
            #// synchsafe ints are not allowed to be signed
            if bytewordlen_ <= PHP_INT_SIZE:
                signMaskBit_ = 128 << 8 * bytewordlen_ - 1
                if intvalue_ & signMaskBit_:
                    intvalue_ = 0 - intvalue_ & signMaskBit_ - 1
                # end if
            else:
                raise php_new_class("Exception", lambda : Exception("ERROR: Cannot have signed integers larger than " + 8 * PHP_INT_SIZE + "-bits (" + php_strlen(byteword_) + ") in self::BigEndian2Int()"))
            # end if
        # end if
        return self.castasint(intvalue_)
    # end def bigendian2int
    #// 
    #// @param string $byteword
    #// @param bool   $signed
    #// 
    #// @return int|float|false
    #//
    @classmethod
    def littleendian2int(self, byteword_=None, signed_=None):
        if signed_ is None:
            signed_ = False
        # end if
        
        return self.bigendian2int(php_strrev(byteword_), False, signed_)
    # end def littleendian2int
    #// 
    #// @param string $byteword
    #// 
    #// @return string
    #//
    @classmethod
    def littleendian2bin(self, byteword_=None):
        
        
        return self.bigendian2bin(php_strrev(byteword_))
    # end def littleendian2bin
    #// 
    #// @param string $byteword
    #// 
    #// @return string
    #//
    @classmethod
    def bigendian2bin(self, byteword_=None):
        
        
        binvalue_ = ""
        bytewordlen_ = php_strlen(byteword_)
        i_ = 0
        while i_ < bytewordlen_:
            
            binvalue_ += php_str_pad(decbin(php_ord(byteword_[i_])), 8, "0", STR_PAD_LEFT)
            i_ += 1
        # end while
        return binvalue_
    # end def bigendian2bin
    #// 
    #// @param int  $number
    #// @param int  $minbytes
    #// @param bool $synchsafe
    #// @param bool $signed
    #// 
    #// @return string
    #// @throws Exception
    #//
    @classmethod
    def bigendian2string(self, number_=None, minbytes_=1, synchsafe_=None, signed_=None):
        if synchsafe_ is None:
            synchsafe_ = False
        # end if
        if signed_ is None:
            signed_ = False
        # end if
        
        if number_ < 0:
            raise php_new_class("Exception", lambda : Exception("ERROR: self::BigEndian2String() does not support negative numbers"))
        # end if
        maskbyte_ = 127 if synchsafe_ or signed_ else 255
        intstring_ = ""
        if signed_:
            if minbytes_ > PHP_INT_SIZE:
                raise php_new_class("Exception", lambda : Exception("ERROR: Cannot have signed integers larger than " + 8 * PHP_INT_SIZE + "-bits in self::BigEndian2String()"))
            # end if
            number_ = number_ & 128 << 8 * minbytes_ - 1
        # end if
        while True:
            
            if not (number_ != 0):
                break
            # end if
            quotient_ = number_ / maskbyte_ + 1
            intstring_ = chr(ceil(quotient_ - floor(quotient_) * maskbyte_)) + intstring_
            number_ = floor(quotient_)
        # end while
        return php_str_pad(intstring_, minbytes_, " ", STR_PAD_LEFT)
    # end def bigendian2string
    #// 
    #// @param int $number
    #// 
    #// @return string
    #//
    @classmethod
    def dec2bin(self, number_=None):
        
        
        while True:
            
            if not (number_ >= 256):
                break
            # end if
            bytes_[-1] = number_ / 256 - floor(number_ / 256) * 256
            number_ = floor(number_ / 256)
        # end while
        bytes_[-1] = number_
        binstring_ = ""
        i_ = 0
        while i_ < php_count(bytes_):
            
            binstring_ = decbin(bytes_[i_]) if i_ == php_count(bytes_) - 1 else php_str_pad(decbin(bytes_[i_]), 8, "0", STR_PAD_LEFT) + binstring_
            i_ += 1
        # end while
        return binstring_
    # end def dec2bin
    #// 
    #// @param string $binstring
    #// @param bool   $signed
    #// 
    #// @return int|float
    #//
    @classmethod
    def bin2dec(self, binstring_=None, signed_=None):
        if signed_ is None:
            signed_ = False
        # end if
        
        signmult_ = 1
        if signed_:
            if binstring_[0] == "1":
                signmult_ = -1
            # end if
            binstring_ = php_substr(binstring_, 1)
        # end if
        decvalue_ = 0
        i_ = 0
        while i_ < php_strlen(binstring_):
            
            decvalue_ += php_int(php_substr(binstring_, php_strlen(binstring_) - i_ - 1, 1)) * pow(2, i_)
            i_ += 1
        # end while
        return self.castasint(decvalue_ * signmult_)
    # end def bin2dec
    #// 
    #// @param string $binstring
    #// 
    #// @return string
    #//
    @classmethod
    def bin2string(self, binstring_=None):
        
        
        #// return 'hi' for input of '0110100001101001'
        string_ = ""
        binstringreversed_ = php_strrev(binstring_)
        i_ = 0
        while i_ < php_strlen(binstringreversed_):
            
            string_ = chr(self.bin2dec(php_strrev(php_substr(binstringreversed_, i_, 8)))) + string_
            i_ += 8
        # end while
        return string_
    # end def bin2string
    #// 
    #// @param int  $number
    #// @param int  $minbytes
    #// @param bool $synchsafe
    #// 
    #// @return string
    #//
    @classmethod
    def littleendian2string(self, number_=None, minbytes_=1, synchsafe_=None):
        if synchsafe_ is None:
            synchsafe_ = False
        # end if
        
        intstring_ = ""
        while True:
            
            if not (number_ > 0):
                break
            # end if
            if synchsafe_:
                intstring_ = intstring_ + chr(number_ & 127)
                number_ >>= 7
            else:
                intstring_ = intstring_ + chr(number_ & 255)
                number_ >>= 8
            # end if
        # end while
        return php_str_pad(intstring_, minbytes_, " ", STR_PAD_RIGHT)
    # end def littleendian2string
    #// 
    #// @param array $array1
    #// @param array $array2
    #// 
    #// @return array|false
    #//
    @classmethod
    def array_merge_clobber(self, array1_=None, array2_=None):
        
        
        #// written by kcØhireability*com
        #// taken from http://www.php.net/manual/en/function.array-merge-recursive.php
        if (not php_is_array(array1_)) or (not php_is_array(array2_)):
            return False
        # end if
        newarray_ = array1_
        for key_,val_ in array2_:
            if php_is_array(val_) and (php_isset(lambda : newarray_[key_])) and php_is_array(newarray_[key_]):
                newarray_[key_] = self.array_merge_clobber(newarray_[key_], val_)
            else:
                newarray_[key_] = val_
            # end if
        # end for
        return newarray_
    # end def array_merge_clobber
    #// 
    #// @param array $array1
    #// @param array $array2
    #// 
    #// @return array|false
    #//
    @classmethod
    def array_merge_noclobber(self, array1_=None, array2_=None):
        
        
        if (not php_is_array(array1_)) or (not php_is_array(array2_)):
            return False
        # end if
        newarray_ = array1_
        for key_,val_ in array2_:
            if php_is_array(val_) and (php_isset(lambda : newarray_[key_])) and php_is_array(newarray_[key_]):
                newarray_[key_] = self.array_merge_noclobber(newarray_[key_], val_)
            elif (not (php_isset(lambda : newarray_[key_]))):
                newarray_[key_] = val_
            # end if
        # end for
        return newarray_
    # end def array_merge_noclobber
    #// 
    #// @param array $array1
    #// @param array $array2
    #// 
    #// @return array|false|null
    #//
    @classmethod
    def flipped_array_merge_noclobber(self, array1_=None, array2_=None):
        
        
        if (not php_is_array(array1_)) or (not php_is_array(array2_)):
            return False
        # end if
        #// # naturally, this only works non-recursively
        newarray_ = php_array_flip(array1_)
        for key_,val_ in php_array_flip(array2_):
            if (not (php_isset(lambda : newarray_[key_]))):
                newarray_[key_] = php_count(newarray_)
            # end if
        # end for
        return php_array_flip(newarray_)
    # end def flipped_array_merge_noclobber
    #// 
    #// @param array $theArray
    #// 
    #// @return bool
    #//
    @classmethod
    def ksort_recursive(self, theArray_=None):
        
        
        ksort(theArray_)
        for key_,value_ in theArray_:
            if php_is_array(value_):
                self.ksort_recursive(theArray_[key_])
            # end if
        # end for
        return True
    # end def ksort_recursive
    #// 
    #// @param string $filename
    #// @param int    $numextensions
    #// 
    #// @return string
    #//
    @classmethod
    def fileextension(self, filename_=None, numextensions_=1):
        
        
        if php_strstr(filename_, "."):
            reversedfilename_ = php_strrev(filename_)
            offset_ = 0
            i_ = 0
            while i_ < numextensions_:
                
                offset_ = php_strpos(reversedfilename_, ".", offset_ + 1)
                if offset_ == False:
                    return ""
                # end if
                i_ += 1
            # end while
            return php_strrev(php_substr(reversedfilename_, 0, offset_))
        # end if
        return ""
    # end def fileextension
    #// 
    #// @param int $seconds
    #// 
    #// @return string
    #//
    @classmethod
    def playtimestring(self, seconds_=None):
        
        
        sign_ = "-" if seconds_ < 0 else ""
        seconds_ = round(abs(seconds_))
        H_ = php_int(floor(seconds_ / 3600))
        M_ = php_int(floor(seconds_ - 3600 * H_ / 60))
        S_ = php_int(round(seconds_ - 3600 * H_ - 60 * M_))
        return sign_ + H_ + ":" if H_ else "" + php_str_pad(M_, 2, "0", STR_PAD_LEFT) if H_ else php_intval(M_) + ":" + php_str_pad(S_, 2, 0, STR_PAD_LEFT)
    # end def playtimestring
    #// 
    #// @param int $macdate
    #// 
    #// @return int|float
    #//
    @classmethod
    def datemac2unix(self, macdate_=None):
        
        
        #// Macintosh timestamp: seconds since 00:00h January 1, 1904
        #// UNIX timestamp:      seconds since 00:00h January 1, 1970
        return self.castasint(macdate_ - 2082844800)
    # end def datemac2unix
    #// 
    #// @param string $rawdata
    #// 
    #// @return float
    #//
    @classmethod
    def fixedpoint8_8(self, rawdata_=None):
        
        
        return self.bigendian2int(php_substr(rawdata_, 0, 1)) + php_float(self.bigendian2int(php_substr(rawdata_, 1, 1)) / pow(2, 8))
    # end def fixedpoint8_8
    #// 
    #// @param string $rawdata
    #// 
    #// @return float
    #//
    @classmethod
    def fixedpoint16_16(self, rawdata_=None):
        
        
        return self.bigendian2int(php_substr(rawdata_, 0, 2)) + php_float(self.bigendian2int(php_substr(rawdata_, 2, 2)) / pow(2, 16))
    # end def fixedpoint16_16
    #// 
    #// @param string $rawdata
    #// 
    #// @return float
    #//
    @classmethod
    def fixedpoint2_30(self, rawdata_=None):
        
        
        binarystring_ = self.bigendian2bin(rawdata_)
        return self.bin2dec(php_substr(binarystring_, 0, 2)) + php_float(self.bin2dec(php_substr(binarystring_, 2, 30)) / pow(2, 30))
    # end def fixedpoint2_30
    #// 
    #// @param string $ArrayPath
    #// @param string $Separator
    #// @param mixed $Value
    #// 
    #// @return array
    #//
    @classmethod
    def createdeeparray(self, ArrayPath_=None, Separator_=None, Value_=None):
        
        
        #// assigns $Value to a nested array path:
        #// $foo = self::CreateDeepArray('/path/to/my', '/', 'file.txt')
        #// is the same as:
        #// $foo = array('path'=>array('to'=>'array('my'=>array('file.txt'))));
        #// or
        #// $foo['path']['to']['my'] = 'file.txt';
        ArrayPath_ = php_ltrim(ArrayPath_, Separator_)
        pos_ = php_strpos(ArrayPath_, Separator_)
        if pos_ != False:
            ReturnedArray_[php_substr(ArrayPath_, 0, pos_)] = self.createdeeparray(php_substr(ArrayPath_, pos_ + 1), Separator_, Value_)
        else:
            ReturnedArray_[ArrayPath_] = Value_
        # end if
        return ReturnedArray_
    # end def createdeeparray
    #// 
    #// @param array $arraydata
    #// @param bool  $returnkey
    #// 
    #// @return int|false
    #//
    @classmethod
    def array_max(self, arraydata_=None, returnkey_=None):
        if returnkey_ is None:
            returnkey_ = False
        # end if
        
        maxvalue_ = False
        maxkey_ = False
        for key_,value_ in arraydata_:
            if (not php_is_array(value_)):
                if value_ > maxvalue_:
                    maxvalue_ = value_
                    maxkey_ = key_
                # end if
            # end if
        # end for
        return maxkey_ if returnkey_ else maxvalue_
    # end def array_max
    #// 
    #// @param array $arraydata
    #// @param bool  $returnkey
    #// 
    #// @return int|false
    #//
    @classmethod
    def array_min(self, arraydata_=None, returnkey_=None):
        if returnkey_ is None:
            returnkey_ = False
        # end if
        
        minvalue_ = False
        minkey_ = False
        for key_,value_ in arraydata_:
            if (not php_is_array(value_)):
                if value_ > minvalue_:
                    minvalue_ = value_
                    minkey_ = key_
                # end if
            # end if
        # end for
        return minkey_ if returnkey_ else minvalue_
    # end def array_min
    #// 
    #// @param string $XMLstring
    #// 
    #// @return array|false
    #//
    @classmethod
    def xml2array(self, XMLstring_=None):
        
        
        if php_function_exists("simplexml_load_string") and php_function_exists("libxml_disable_entity_loader"):
            #// http://websec.io/2012/08/27/Preventing-XEE-in-PHP.html
            #// https://core.trac.wordpress.org/changeset/29378
            loader_ = libxml_disable_entity_loader(True)
            XMLobject_ = simplexml_load_string(XMLstring_, "SimpleXMLElement", LIBXML_NOENT)
            return_ = self.simplexmlelement2array(XMLobject_)
            libxml_disable_entity_loader(loader_)
            return return_
        # end if
        return False
    # end def xml2array
    #// 
    #// @param SimpleXMLElement|array $XMLobject
    #// 
    #// @return array
    #//
    @classmethod
    def simplexmlelement2array(self, XMLobject_=None):
        
        
        if (not php_is_object(XMLobject_)) and (not php_is_array(XMLobject_)):
            return XMLobject_
        # end if
        XMLarray_ = get_object_vars(XMLobject_) if type(XMLobject_).__name__ == "SimpleXMLElement" else XMLobject_
        for key_,value_ in XMLarray_:
            XMLarray_[key_] = self.simplexmlelement2array(value_)
        # end for
        return XMLarray_
    # end def simplexmlelement2array
    #// 
    #// Returns checksum for a file from starting position to absolute end position.
    #// 
    #// @param string $file
    #// @param int    $offset
    #// @param int    $end
    #// @param string $algorithm
    #// 
    #// @return string|false
    #// @throws getid3_exception
    #//
    @classmethod
    def hash_data(self, file_=None, offset_=None, end_=None, algorithm_=None):
        
        
        if (not self.intvaluesupported(end_)):
            return False
        # end if
        if (not php_in_array(algorithm_, Array("md5", "sha1"))):
            raise php_new_class("getid3_exception", lambda : getid3_exception("Invalid algorithm (" + algorithm_ + ") in self::hash_data()"))
        # end if
        size_ = end_ - offset_
        fp_ = fopen(file_, "rb")
        fseek(fp_, offset_)
        ctx_ = hash_init(algorithm_)
        while True:
            
            if not (size_ > 0):
                break
            # end if
            buffer_ = fread(fp_, php_min(size_, getID3.FREAD_BUFFER_SIZE))
            hash_update(ctx_, buffer_)
            size_ -= getID3.FREAD_BUFFER_SIZE
        # end while
        hash_ = hash_final(ctx_)
        php_fclose(fp_)
        return hash_
    # end def hash_data
    #// 
    #// @param string $filename_source
    #// @param string $filename_dest
    #// @param int    $offset
    #// @param int    $length
    #// 
    #// @return bool
    #// @throws Exception
    #// 
    #// @deprecated Unused, may be removed in future versions of getID3
    #//
    @classmethod
    def copyfileparts(self, filename_source_=None, filename_dest_=None, offset_=None, length_=None):
        
        
        if (not self.intvaluesupported(offset_ + length_)):
            raise php_new_class("Exception", lambda : Exception("cannot copy file portion, it extends beyond the " + round(PHP_INT_MAX / 1073741824) + "GB limit"))
        # end if
        fp_src_ = fopen(filename_source_, "rb")
        if php_is_readable(filename_source_) and php_is_file(filename_source_) and fp_src_:
            fp_dest_ = fopen(filename_dest_, "wb")
            if fp_dest_:
                if fseek(fp_src_, offset_) == 0:
                    byteslefttowrite_ = length_
                    while True:
                        buffer_ = fread(fp_src_, php_min(byteslefttowrite_, getID3.FREAD_BUFFER_SIZE))
                        if not (byteslefttowrite_ > 0 and buffer_):
                            break
                        # end if
                        byteswritten_ = fwrite(fp_dest_, buffer_, byteslefttowrite_)
                        byteslefttowrite_ -= byteswritten_
                    # end while
                    php_fclose(fp_dest_)
                    return True
                else:
                    php_fclose(fp_src_)
                    raise php_new_class("Exception", lambda : Exception("failed to seek to offset " + offset_ + " in " + filename_source_))
                # end if
            else:
                raise php_new_class("Exception", lambda : Exception("failed to create file for writing " + filename_dest_))
            # end if
        else:
            raise php_new_class("Exception", lambda : Exception("failed to open file for reading " + filename_source_))
        # end if
    # end def copyfileparts
    #// 
    #// @param int $charval
    #// 
    #// @return string
    #//
    @classmethod
    def iconv_fallback_int_utf8(self, charval_=None):
        
        
        if charval_ < 128:
            #// 0bbbbbbb
            newcharstring_ = chr(charval_)
        elif charval_ < 2048:
            #// 110bbbbb 10bbbbbb
            newcharstring_ = chr(charval_ >> 6 | 192)
            newcharstring_ += chr(charval_ & 63 | 128)
        elif charval_ < 65536:
            #// 1110bbbb 10bbbbbb 10bbbbbb
            newcharstring_ = chr(charval_ >> 12 | 224)
            newcharstring_ += chr(charval_ >> 6 | 192)
            newcharstring_ += chr(charval_ & 63 | 128)
        else:
            #// 11110bbb 10bbbbbb 10bbbbbb 10bbbbbb
            newcharstring_ = chr(charval_ >> 18 | 240)
            newcharstring_ += chr(charval_ >> 12 | 192)
            newcharstring_ += chr(charval_ >> 6 | 192)
            newcharstring_ += chr(charval_ & 63 | 128)
        # end if
        return newcharstring_
    # end def iconv_fallback_int_utf8
    #// 
    #// ISO-8859-1 => UTF-8
    #// 
    #// @param string $string
    #// @param bool   $bom
    #// 
    #// @return string
    #//
    @classmethod
    def iconv_fallback_iso88591_utf8(self, string_=None, bom_=None):
        if bom_ is None:
            bom_ = False
        # end if
        
        if php_function_exists("utf8_encode"):
            return utf8_encode(string_)
        # end if
        #// utf8_encode() unavailable, use getID3()'s iconv_fallback() conversions (possibly PHP is compiled without XML support)
        newcharstring_ = ""
        if bom_:
            newcharstring_ += "ï»¿"
        # end if
        i_ = 0
        while i_ < php_strlen(string_):
            
            charval_ = php_ord(string_[i_])
            newcharstring_ += self.iconv_fallback_int_utf8(charval_)
            i_ += 1
        # end while
        return newcharstring_
    # end def iconv_fallback_iso88591_utf8
    #// 
    #// ISO-8859-1 => UTF-16BE
    #// 
    #// @param string $string
    #// @param bool   $bom
    #// 
    #// @return string
    #//
    @classmethod
    def iconv_fallback_iso88591_utf16be(self, string_=None, bom_=None):
        if bom_ is None:
            bom_ = False
        # end if
        
        newcharstring_ = ""
        if bom_:
            newcharstring_ += "þÿ"
        # end if
        i_ = 0
        while i_ < php_strlen(string_):
            
            newcharstring_ += " " + string_[i_]
            i_ += 1
        # end while
        return newcharstring_
    # end def iconv_fallback_iso88591_utf16be
    #// 
    #// ISO-8859-1 => UTF-16LE
    #// 
    #// @param string $string
    #// @param bool   $bom
    #// 
    #// @return string
    #//
    @classmethod
    def iconv_fallback_iso88591_utf16le(self, string_=None, bom_=None):
        if bom_ is None:
            bom_ = False
        # end if
        
        newcharstring_ = ""
        if bom_:
            newcharstring_ += "ÿþ"
        # end if
        i_ = 0
        while i_ < php_strlen(string_):
            
            newcharstring_ += string_[i_] + " "
            i_ += 1
        # end while
        return newcharstring_
    # end def iconv_fallback_iso88591_utf16le
    #// 
    #// ISO-8859-1 => UTF-16LE (BOM)
    #// 
    #// @param string $string
    #// 
    #// @return string
    #//
    @classmethod
    def iconv_fallback_iso88591_utf16(self, string_=None):
        
        
        return self.iconv_fallback_iso88591_utf16le(string_, True)
    # end def iconv_fallback_iso88591_utf16
    #// 
    #// UTF-8 => ISO-8859-1
    #// 
    #// @param string $string
    #// 
    #// @return string
    #//
    @classmethod
    def iconv_fallback_utf8_iso88591(self, string_=None):
        
        
        if php_function_exists("utf8_decode"):
            return utf8_decode(string_)
        # end if
        #// utf8_decode() unavailable, use getID3()'s iconv_fallback() conversions (possibly PHP is compiled without XML support)
        newcharstring_ = ""
        offset_ = 0
        stringlength_ = php_strlen(string_)
        while True:
            
            if not (offset_ < stringlength_):
                break
            # end if
            if php_ord(string_[offset_]) | 7 == 247:
                #// 11110bbb 10bbbbbb 10bbbbbb 10bbbbbb
                charval_ = php_ord(string_[offset_ + 0]) & 7 << 18 & php_ord(string_[offset_ + 1]) & 63 << 12 & php_ord(string_[offset_ + 2]) & 63 << 6 & php_ord(string_[offset_ + 3]) & 63
                offset_ += 4
            elif php_ord(string_[offset_]) | 15 == 239:
                #// 1110bbbb 10bbbbbb 10bbbbbb
                charval_ = php_ord(string_[offset_ + 0]) & 15 << 12 & php_ord(string_[offset_ + 1]) & 63 << 6 & php_ord(string_[offset_ + 2]) & 63
                offset_ += 3
            elif php_ord(string_[offset_]) | 31 == 223:
                #// 110bbbbb 10bbbbbb
                charval_ = php_ord(string_[offset_ + 0]) & 31 << 6 & php_ord(string_[offset_ + 1]) & 63
                offset_ += 2
            elif php_ord(string_[offset_]) | 127 == 127:
                #// 0bbbbbbb
                charval_ = php_ord(string_[offset_])
                offset_ += 1
            else:
                #// error? throw some kind of warning here?
                charval_ = False
                offset_ += 1
            # end if
            if charval_ != False:
                newcharstring_ += chr(charval_) if charval_ < 256 else "?"
            # end if
        # end while
        return newcharstring_
    # end def iconv_fallback_utf8_iso88591
    #// 
    #// UTF-8 => UTF-16BE
    #// 
    #// @param string $string
    #// @param bool   $bom
    #// 
    #// @return string
    #//
    @classmethod
    def iconv_fallback_utf8_utf16be(self, string_=None, bom_=None):
        if bom_ is None:
            bom_ = False
        # end if
        
        newcharstring_ = ""
        if bom_:
            newcharstring_ += "þÿ"
        # end if
        offset_ = 0
        stringlength_ = php_strlen(string_)
        while True:
            
            if not (offset_ < stringlength_):
                break
            # end if
            if php_ord(string_[offset_]) | 7 == 247:
                #// 11110bbb 10bbbbbb 10bbbbbb 10bbbbbb
                charval_ = php_ord(string_[offset_ + 0]) & 7 << 18 & php_ord(string_[offset_ + 1]) & 63 << 12 & php_ord(string_[offset_ + 2]) & 63 << 6 & php_ord(string_[offset_ + 3]) & 63
                offset_ += 4
            elif php_ord(string_[offset_]) | 15 == 239:
                #// 1110bbbb 10bbbbbb 10bbbbbb
                charval_ = php_ord(string_[offset_ + 0]) & 15 << 12 & php_ord(string_[offset_ + 1]) & 63 << 6 & php_ord(string_[offset_ + 2]) & 63
                offset_ += 3
            elif php_ord(string_[offset_]) | 31 == 223:
                #// 110bbbbb 10bbbbbb
                charval_ = php_ord(string_[offset_ + 0]) & 31 << 6 & php_ord(string_[offset_ + 1]) & 63
                offset_ += 2
            elif php_ord(string_[offset_]) | 127 == 127:
                #// 0bbbbbbb
                charval_ = php_ord(string_[offset_])
                offset_ += 1
            else:
                #// error? throw some kind of warning here?
                charval_ = False
                offset_ += 1
            # end if
            if charval_ != False:
                newcharstring_ += self.bigendian2string(charval_, 2) if charval_ < 65536 else " " + "?"
            # end if
        # end while
        return newcharstring_
    # end def iconv_fallback_utf8_utf16be
    #// 
    #// UTF-8 => UTF-16LE
    #// 
    #// @param string $string
    #// @param bool   $bom
    #// 
    #// @return string
    #//
    @classmethod
    def iconv_fallback_utf8_utf16le(self, string_=None, bom_=None):
        if bom_ is None:
            bom_ = False
        # end if
        
        newcharstring_ = ""
        if bom_:
            newcharstring_ += "ÿþ"
        # end if
        offset_ = 0
        stringlength_ = php_strlen(string_)
        while True:
            
            if not (offset_ < stringlength_):
                break
            # end if
            if php_ord(string_[offset_]) | 7 == 247:
                #// 11110bbb 10bbbbbb 10bbbbbb 10bbbbbb
                charval_ = php_ord(string_[offset_ + 0]) & 7 << 18 & php_ord(string_[offset_ + 1]) & 63 << 12 & php_ord(string_[offset_ + 2]) & 63 << 6 & php_ord(string_[offset_ + 3]) & 63
                offset_ += 4
            elif php_ord(string_[offset_]) | 15 == 239:
                #// 1110bbbb 10bbbbbb 10bbbbbb
                charval_ = php_ord(string_[offset_ + 0]) & 15 << 12 & php_ord(string_[offset_ + 1]) & 63 << 6 & php_ord(string_[offset_ + 2]) & 63
                offset_ += 3
            elif php_ord(string_[offset_]) | 31 == 223:
                #// 110bbbbb 10bbbbbb
                charval_ = php_ord(string_[offset_ + 0]) & 31 << 6 & php_ord(string_[offset_ + 1]) & 63
                offset_ += 2
            elif php_ord(string_[offset_]) | 127 == 127:
                #// 0bbbbbbb
                charval_ = php_ord(string_[offset_])
                offset_ += 1
            else:
                #// error? maybe throw some warning here?
                charval_ = False
                offset_ += 1
            # end if
            if charval_ != False:
                newcharstring_ += self.littleendian2string(charval_, 2) if charval_ < 65536 else "?" + " "
            # end if
        # end while
        return newcharstring_
    # end def iconv_fallback_utf8_utf16le
    #// 
    #// UTF-8 => UTF-16LE (BOM)
    #// 
    #// @param string $string
    #// 
    #// @return string
    #//
    @classmethod
    def iconv_fallback_utf8_utf16(self, string_=None):
        
        
        return self.iconv_fallback_utf8_utf16le(string_, True)
    # end def iconv_fallback_utf8_utf16
    #// 
    #// UTF-16BE => UTF-8
    #// 
    #// @param string $string
    #// 
    #// @return string
    #//
    @classmethod
    def iconv_fallback_utf16be_utf8(self, string_=None):
        
        
        if php_substr(string_, 0, 2) == "þÿ":
            #// strip BOM
            string_ = php_substr(string_, 2)
        # end if
        newcharstring_ = ""
        i_ = 0
        while i_ < php_strlen(string_):
            
            charval_ = self.bigendian2int(php_substr(string_, i_, 2))
            newcharstring_ += self.iconv_fallback_int_utf8(charval_)
            i_ += 2
        # end while
        return newcharstring_
    # end def iconv_fallback_utf16be_utf8
    #// 
    #// UTF-16LE => UTF-8
    #// 
    #// @param string $string
    #// 
    #// @return string
    #//
    @classmethod
    def iconv_fallback_utf16le_utf8(self, string_=None):
        
        
        if php_substr(string_, 0, 2) == "ÿþ":
            #// strip BOM
            string_ = php_substr(string_, 2)
        # end if
        newcharstring_ = ""
        i_ = 0
        while i_ < php_strlen(string_):
            
            charval_ = self.littleendian2int(php_substr(string_, i_, 2))
            newcharstring_ += self.iconv_fallback_int_utf8(charval_)
            i_ += 2
        # end while
        return newcharstring_
    # end def iconv_fallback_utf16le_utf8
    #// 
    #// UTF-16BE => ISO-8859-1
    #// 
    #// @param string $string
    #// 
    #// @return string
    #//
    @classmethod
    def iconv_fallback_utf16be_iso88591(self, string_=None):
        
        
        if php_substr(string_, 0, 2) == "þÿ":
            #// strip BOM
            string_ = php_substr(string_, 2)
        # end if
        newcharstring_ = ""
        i_ = 0
        while i_ < php_strlen(string_):
            
            charval_ = self.bigendian2int(php_substr(string_, i_, 2))
            newcharstring_ += chr(charval_) if charval_ < 256 else "?"
            i_ += 2
        # end while
        return newcharstring_
    # end def iconv_fallback_utf16be_iso88591
    #// 
    #// UTF-16LE => ISO-8859-1
    #// 
    #// @param string $string
    #// 
    #// @return string
    #//
    @classmethod
    def iconv_fallback_utf16le_iso88591(self, string_=None):
        
        
        if php_substr(string_, 0, 2) == "ÿþ":
            #// strip BOM
            string_ = php_substr(string_, 2)
        # end if
        newcharstring_ = ""
        i_ = 0
        while i_ < php_strlen(string_):
            
            charval_ = self.littleendian2int(php_substr(string_, i_, 2))
            newcharstring_ += chr(charval_) if charval_ < 256 else "?"
            i_ += 2
        # end while
        return newcharstring_
    # end def iconv_fallback_utf16le_iso88591
    #// 
    #// UTF-16 (BOM) => ISO-8859-1
    #// 
    #// @param string $string
    #// 
    #// @return string
    #//
    @classmethod
    def iconv_fallback_utf16_iso88591(self, string_=None):
        
        
        bom_ = php_substr(string_, 0, 2)
        if bom_ == "þÿ":
            return self.iconv_fallback_utf16be_iso88591(php_substr(string_, 2))
        elif bom_ == "ÿþ":
            return self.iconv_fallback_utf16le_iso88591(php_substr(string_, 2))
        # end if
        return string_
    # end def iconv_fallback_utf16_iso88591
    #// 
    #// UTF-16 (BOM) => UTF-8
    #// 
    #// @param string $string
    #// 
    #// @return string
    #//
    @classmethod
    def iconv_fallback_utf16_utf8(self, string_=None):
        
        
        bom_ = php_substr(string_, 0, 2)
        if bom_ == "þÿ":
            return self.iconv_fallback_utf16be_utf8(php_substr(string_, 2))
        elif bom_ == "ÿþ":
            return self.iconv_fallback_utf16le_utf8(php_substr(string_, 2))
        # end if
        return string_
    # end def iconv_fallback_utf16_utf8
    #// 
    #// @param string $in_charset
    #// @param string $out_charset
    #// @param string $string
    #// 
    #// @return string
    #// @throws Exception
    #//
    @classmethod
    def iconv_fallback(self, in_charset_=None, out_charset_=None, string_=None):
        
        
        if in_charset_ == out_charset_:
            return string_
        # end if
        #// mb_convert_encoding() available
        if php_function_exists("mb_convert_encoding"):
            if php_strtoupper(in_charset_) == "UTF-16" and php_substr(string_, 0, 2) != "þÿ" and php_substr(string_, 0, 2) != "ÿþ":
                #// if BOM missing, mb_convert_encoding will mishandle the conversion, assume UTF-16BE and prepend appropriate BOM
                string_ = "ÿþ" + string_
            # end if
            if php_strtoupper(in_charset_) == "UTF-16" and php_strtoupper(out_charset_) == "UTF-8":
                if string_ == "ÿþ" or string_ == "þÿ":
                    #// if string consists of only BOM, mb_convert_encoding will return the BOM unmodified
                    return ""
                # end if
            # end if
            converted_string_ = php_no_error(lambda: mb_convert_encoding(string_, out_charset_, in_charset_))
            if converted_string_:
                for case in Switch(out_charset_):
                    if case("ISO-8859-1"):
                        converted_string_ = php_rtrim(converted_string_, " ")
                        break
                    # end if
                # end for
                return converted_string_
            # end if
            return string_
            pass
        elif php_function_exists("iconv"):
            converted_string_ = php_no_error(lambda: iconv(in_charset_, out_charset_ + "//TRANSLIT", string_))
            if converted_string_:
                for case in Switch(out_charset_):
                    if case("ISO-8859-1"):
                        converted_string_ = php_rtrim(converted_string_, " ")
                        break
                    # end if
                # end for
                return converted_string_
            # end if
            #// iconv() may sometimes fail with "illegal character in input string" error message
            #// and return an empty string, but returning the unconverted string is more useful
            return string_
        # end if
        ConversionFunctionList_ = Array()
        if php_empty(lambda : ConversionFunctionList_):
            ConversionFunctionList_["ISO-8859-1"]["UTF-8"] = "iconv_fallback_iso88591_utf8"
            ConversionFunctionList_["ISO-8859-1"]["UTF-16"] = "iconv_fallback_iso88591_utf16"
            ConversionFunctionList_["ISO-8859-1"]["UTF-16BE"] = "iconv_fallback_iso88591_utf16be"
            ConversionFunctionList_["ISO-8859-1"]["UTF-16LE"] = "iconv_fallback_iso88591_utf16le"
            ConversionFunctionList_["UTF-8"]["ISO-8859-1"] = "iconv_fallback_utf8_iso88591"
            ConversionFunctionList_["UTF-8"]["UTF-16"] = "iconv_fallback_utf8_utf16"
            ConversionFunctionList_["UTF-8"]["UTF-16BE"] = "iconv_fallback_utf8_utf16be"
            ConversionFunctionList_["UTF-8"]["UTF-16LE"] = "iconv_fallback_utf8_utf16le"
            ConversionFunctionList_["UTF-16"]["ISO-8859-1"] = "iconv_fallback_utf16_iso88591"
            ConversionFunctionList_["UTF-16"]["UTF-8"] = "iconv_fallback_utf16_utf8"
            ConversionFunctionList_["UTF-16LE"]["ISO-8859-1"] = "iconv_fallback_utf16le_iso88591"
            ConversionFunctionList_["UTF-16LE"]["UTF-8"] = "iconv_fallback_utf16le_utf8"
            ConversionFunctionList_["UTF-16BE"]["ISO-8859-1"] = "iconv_fallback_utf16be_iso88591"
            ConversionFunctionList_["UTF-16BE"]["UTF-8"] = "iconv_fallback_utf16be_utf8"
        # end if
        if (php_isset(lambda : ConversionFunctionList_[php_strtoupper(in_charset_)][php_strtoupper(out_charset_)])):
            ConversionFunction_ = ConversionFunctionList_[php_strtoupper(in_charset_)][php_strtoupper(out_charset_)]
            return self.conversionfunction_(string_)
        # end if
        raise php_new_class("Exception", lambda : Exception("PHP does not has mb_convert_encoding() or iconv() support - cannot convert from " + in_charset_ + " to " + out_charset_))
    # end def iconv_fallback
    #// 
    #// @param mixed  $data
    #// @param string $charset
    #// 
    #// @return mixed
    #//
    @classmethod
    def recursivemultibytecharstring2html(self, data_=None, charset_="ISO-8859-1"):
        
        
        if php_is_string(data_):
            return self.multibytecharstring2html(data_, charset_)
        elif php_is_array(data_):
            return_data_ = Array()
            for key_,value_ in data_:
                return_data_[key_] = self.recursivemultibytecharstring2html(value_, charset_)
            # end for
            return return_data_
        # end if
        #// integer, float, objects, resources, etc
        return data_
    # end def recursivemultibytecharstring2html
    #// 
    #// @param string|int|float $string
    #// @param string           $charset
    #// 
    #// @return string
    #//
    @classmethod
    def multibytecharstring2html(self, string_=None, charset_="ISO-8859-1"):
        
        
        string_ = php_str(string_)
        #// in case trying to pass a numeric (float, int) string, would otherwise return an empty string
        HTMLstring_ = ""
        for case in Switch(php_strtolower(charset_)):
            if case("1251"):
                pass
            # end if
            if case("1252"):
                pass
            # end if
            if case("866"):
                pass
            # end if
            if case("932"):
                pass
            # end if
            if case("936"):
                pass
            # end if
            if case("950"):
                pass
            # end if
            if case("big5"):
                pass
            # end if
            if case("big5-hkscs"):
                pass
            # end if
            if case("cp1251"):
                pass
            # end if
            if case("cp1252"):
                pass
            # end if
            if case("cp866"):
                pass
            # end if
            if case("euc-jp"):
                pass
            # end if
            if case("eucjp"):
                pass
            # end if
            if case("gb2312"):
                pass
            # end if
            if case("ibm866"):
                pass
            # end if
            if case("iso-8859-1"):
                pass
            # end if
            if case("iso-8859-15"):
                pass
            # end if
            if case("iso8859-1"):
                pass
            # end if
            if case("iso8859-15"):
                pass
            # end if
            if case("koi8-r"):
                pass
            # end if
            if case("koi8-ru"):
                pass
            # end if
            if case("koi8r"):
                pass
            # end if
            if case("shift_jis"):
                pass
            # end if
            if case("sjis"):
                pass
            # end if
            if case("win-1251"):
                pass
            # end if
            if case("windows-1251"):
                pass
            # end if
            if case("windows-1252"):
                HTMLstring_ = htmlentities(string_, ENT_COMPAT, charset_)
                break
            # end if
            if case("utf-8"):
                strlen_ = php_strlen(string_)
                i_ = 0
                while i_ < strlen_:
                    
                    char_ord_val_ = php_ord(string_[i_])
                    charval_ = 0
                    if char_ord_val_ < 128:
                        charval_ = char_ord_val_
                    elif char_ord_val_ & 240 >> 4 == 15 and i_ + 3 < strlen_:
                        charval_ = char_ord_val_ & 7 << 18
                        i_ += 1
                        charval_ += php_ord(string_[i_]) & 63 << 12
                        i_ += 1
                        charval_ += php_ord(string_[i_]) & 63 << 6
                        i_ += 1
                        charval_ += php_ord(string_[i_]) & 63
                    elif char_ord_val_ & 224 >> 5 == 7 and i_ + 2 < strlen_:
                        charval_ = char_ord_val_ & 15 << 12
                        i_ += 1
                        charval_ += php_ord(string_[i_]) & 63 << 6
                        i_ += 1
                        charval_ += php_ord(string_[i_]) & 63
                    elif char_ord_val_ & 192 >> 6 == 3 and i_ + 1 < strlen_:
                        charval_ = char_ord_val_ & 31 << 6
                        i_ += 1
                        charval_ += php_ord(string_[i_]) & 63
                    # end if
                    if charval_ >= 32 and charval_ <= 127:
                        HTMLstring_ += htmlentities(chr(charval_))
                    else:
                        HTMLstring_ += "&#" + charval_ + ";"
                    # end if
                    i_ += 1
                # end while
                break
            # end if
            if case("utf-16le"):
                i_ = 0
                while i_ < php_strlen(string_):
                    
                    charval_ = self.littleendian2int(php_substr(string_, i_, 2))
                    if charval_ >= 32 and charval_ <= 127:
                        HTMLstring_ += chr(charval_)
                    else:
                        HTMLstring_ += "&#" + charval_ + ";"
                    # end if
                    i_ += 2
                # end while
                break
            # end if
            if case("utf-16be"):
                i_ = 0
                while i_ < php_strlen(string_):
                    
                    charval_ = self.bigendian2int(php_substr(string_, i_, 2))
                    if charval_ >= 32 and charval_ <= 127:
                        HTMLstring_ += chr(charval_)
                    else:
                        HTMLstring_ += "&#" + charval_ + ";"
                    # end if
                    i_ += 2
                # end while
                break
            # end if
            if case():
                HTMLstring_ = "ERROR: Character set \"" + charset_ + "\" not supported in MultiByteCharString2HTML()"
                break
            # end if
        # end for
        return HTMLstring_
    # end def multibytecharstring2html
    #// 
    #// @param int $namecode
    #// 
    #// @return string
    #//
    @classmethod
    def rgadnamelookup(self, namecode_=None):
        
        
        RGADname_ = Array()
        if php_empty(lambda : RGADname_):
            RGADname_[0] = "not set"
            RGADname_[1] = "Track Gain Adjustment"
            RGADname_[2] = "Album Gain Adjustment"
        # end if
        return RGADname_[namecode_] if (php_isset(lambda : RGADname_[namecode_])) else ""
    # end def rgadnamelookup
    #// 
    #// @param int $originatorcode
    #// 
    #// @return string
    #//
    @classmethod
    def rgadoriginatorlookup(self, originatorcode_=None):
        
        
        RGADoriginator_ = Array()
        if php_empty(lambda : RGADoriginator_):
            RGADoriginator_[0] = "unspecified"
            RGADoriginator_[1] = "pre-set by artist/producer/mastering engineer"
            RGADoriginator_[2] = "set by user"
            RGADoriginator_[3] = "determined automatically"
        # end if
        return RGADoriginator_[originatorcode_] if (php_isset(lambda : RGADoriginator_[originatorcode_])) else ""
    # end def rgadoriginatorlookup
    #// 
    #// @param int $rawadjustment
    #// @param int $signbit
    #// 
    #// @return float
    #//
    @classmethod
    def rgadadjustmentlookup(self, rawadjustment_=None, signbit_=None):
        
        
        adjustment_ = php_float(rawadjustment_) / 10
        if signbit_ == 1:
            adjustment_ *= -1
        # end if
        return adjustment_
    # end def rgadadjustmentlookup
    #// 
    #// @param int $namecode
    #// @param int $originatorcode
    #// @param int $replaygain
    #// 
    #// @return string
    #//
    @classmethod
    def rgadgainstring(self, namecode_=None, originatorcode_=None, replaygain_=None):
        
        
        if replaygain_ < 0:
            signbit_ = "1"
        else:
            signbit_ = "0"
        # end if
        storedreplaygain_ = php_intval(round(replaygain_ * 10))
        gainstring_ = php_str_pad(decbin(namecode_), 3, "0", STR_PAD_LEFT)
        gainstring_ += php_str_pad(decbin(originatorcode_), 3, "0", STR_PAD_LEFT)
        gainstring_ += signbit_
        gainstring_ += php_str_pad(decbin(storedreplaygain_), 9, "0", STR_PAD_LEFT)
        return gainstring_
    # end def rgadgainstring
    #// 
    #// @param float $amplitude
    #// 
    #// @return float
    #//
    @classmethod
    def rgadamplitude2db(self, amplitude_=None):
        
        
        return 20 * log10(amplitude_)
    # end def rgadamplitude2db
    #// 
    #// @param string $imgData
    #// @param array  $imageinfo
    #// 
    #// @return array|false
    #//
    @classmethod
    def getdataimagesize(self, imgData_=None, imageinfo_=None):
        if imageinfo_ is None:
            imageinfo_ = Array()
        # end if
        
        tempdir_ = ""
        if php_empty(lambda : tempdir_):
            if php_function_exists("sys_get_temp_dir"):
                tempdir_ = php_sys_get_temp_dir()
                pass
            # end if
            #// yes this is ugly, feel free to suggest a better way
            if php_include_file(php_dirname(__FILE__) + "/getid3.php", once=False):
                getid3_temp_ = php_new_class("getID3", lambda : getID3())
                if getid3_temp_:
                    getid3_temp_tempdir_ = getid3_temp_.tempdir
                    if getid3_temp_tempdir_:
                        tempdir_ = getid3_temp_tempdir_
                    # end if
                    getid3_temp_ = None
                    getid3_temp_tempdir_ = None
                # end if
            # end if
        # end if
        GetDataImageSize_ = False
        tempfilename_ = php_tempnam(tempdir_, "gI3")
        if tempfilename_:
            tmp_ = fopen(tempfilename_, "wb")
            if php_is_writable(tempfilename_) and php_is_file(tempfilename_) and tmp_:
                fwrite(tmp_, imgData_)
                php_fclose(tmp_)
                GetDataImageSize_ = php_no_error(lambda: getimagesize(tempfilename_, imageinfo_))
                if GetDataImageSize_ == False or (not (php_isset(lambda : GetDataImageSize_[0]))) or (not (php_isset(lambda : GetDataImageSize_[1]))):
                    return False
                # end if
                GetDataImageSize_["height"] = GetDataImageSize_[0]
                GetDataImageSize_["width"] = GetDataImageSize_[1]
            # end if
            unlink(tempfilename_)
        # end if
        return GetDataImageSize_
    # end def getdataimagesize
    #// 
    #// @param string $mime_type
    #// 
    #// @return string
    #//
    @classmethod
    def imageextfrommime(self, mime_type_=None):
        
        
        #// temporary way, works OK for now, but should be reworked in the future
        return php_str_replace(Array("image/", "x-", "jpeg"), Array("", "", "jpg"), mime_type_)
    # end def imageextfrommime
    #// 
    #// @param array $ThisFileInfo
    #// 
    #// @return bool
    #//
    @classmethod
    def copytagstocomments(self, ThisFileInfo_=None):
        
        
        #// Copy all entries from ['tags'] into common ['comments']
        if (not php_empty(lambda : ThisFileInfo_["tags"])):
            for tagtype_,tagarray_ in ThisFileInfo_["tags"]:
                for tagname_,tagdata_ in tagarray_:
                    for key_,value_ in tagdata_:
                        if (not php_empty(lambda : value_)):
                            if php_empty(lambda : ThisFileInfo_["comments"][tagname_]):
                                pass
                            elif tagtype_ == "id3v1":
                                newvaluelength_ = php_strlen(php_trim(value_))
                                for existingkey_,existingvalue_ in ThisFileInfo_["comments"][tagname_]:
                                    oldvaluelength_ = php_strlen(php_trim(existingvalue_))
                                    if newvaluelength_ <= oldvaluelength_ and php_substr(existingvalue_, 0, newvaluelength_) == php_trim(value_):
                                        break
                                    # end if
                                # end for
                            elif (not php_is_array(value_)):
                                newvaluelength_ = php_strlen(php_trim(value_))
                                for existingkey_,existingvalue_ in ThisFileInfo_["comments"][tagname_]:
                                    oldvaluelength_ = php_strlen(php_trim(existingvalue_))
                                    if php_strlen(existingvalue_) > 10 and newvaluelength_ > oldvaluelength_ and php_substr(php_trim(value_), 0, php_strlen(existingvalue_)) == existingvalue_:
                                        ThisFileInfo_["comments"][tagname_][existingkey_] = php_trim(value_)
                                        break
                                    # end if
                                # end for
                            # end if
                            if php_is_array(value_) or php_empty(lambda : ThisFileInfo_["comments"][tagname_]) or (not php_in_array(php_trim(value_), ThisFileInfo_["comments"][tagname_])):
                                value_ = php_trim(value_) if php_is_string(value_) else value_
                                if (not php_is_int(key_)) and (not ctype_digit(key_)):
                                    ThisFileInfo_["comments"][tagname_][key_] = value_
                                else:
                                    if (php_isset(lambda : ThisFileInfo_["comments"][tagname_])):
                                        ThisFileInfo_["comments"][tagname_] = Array(value_)
                                    else:
                                        ThisFileInfo_["comments"][tagname_][-1] = value_
                                    # end if
                                # end if
                            # end if
                        # end if
                    # end for
                # end for
            # end for
            #// attempt to standardize spelling of returned keys
            StandardizeFieldNames_ = Array({"tracknumber": "track_number", "track": "track_number"})
            for badkey_,goodkey_ in StandardizeFieldNames_:
                if php_array_key_exists(badkey_, ThisFileInfo_["comments"]) and (not php_array_key_exists(goodkey_, ThisFileInfo_["comments"])):
                    ThisFileInfo_["comments"][goodkey_] = ThisFileInfo_["comments"][badkey_]
                    ThisFileInfo_["comments"][badkey_] = None
                # end if
            # end for
            #// Copy to ['comments_html']
            if (not php_empty(lambda : ThisFileInfo_["comments"])):
                for field_,values_ in ThisFileInfo_["comments"]:
                    if field_ == "picture":
                        continue
                    # end if
                    for index_,value_ in values_:
                        if php_is_array(value_):
                            ThisFileInfo_["comments_html"][field_][index_] = value_
                        else:
                            ThisFileInfo_["comments_html"][field_][index_] = php_str_replace("&#0;", "", self.multibytecharstring2html(value_, ThisFileInfo_["encoding"]))
                        # end if
                    # end for
                # end for
            # end if
        # end if
        return True
    # end def copytagstocomments
    #// 
    #// @param string $key
    #// @param int    $begin
    #// @param int    $end
    #// @param string $file
    #// @param string $name
    #// 
    #// @return string
    #//
    @classmethod
    def embeddedlookup(self, key_=None, begin_=None, end_=None, file_=None, name_=None):
        
        
        cache_ = None
        if (php_isset(lambda : cache_[file_][name_])):
            return cache_[file_][name_][key_] if (php_isset(lambda : cache_[file_][name_][key_])) else ""
        # end if
        #// Init
        keylength_ = php_strlen(key_)
        line_count_ = end_ - begin_ - 7
        #// Open php file
        fp_ = fopen(file_, "r")
        #// Discard $begin lines
        i_ = 0
        while i_ < begin_ + 3:
            
            php_fgets(fp_, 1024)
            i_ += 1
        # end while
        #// Loop thru line
        while True:
            
            if not (0 < line_count_):
                break
            # end if
            #// Read line
            line_ = php_ltrim(php_fgets(fp_, 1024), "    ")
            line_count_ -= 1
            #// METHOD A: only cache the matching key - less memory but slower on next lookup of not-previously-looked-up key
            #// $keycheck = substr($line, 0, $keylength);
            #// if ($key == $keycheck)  {
            #// $cache[$file][$name][$keycheck] = substr($line, $keylength + 1);
            #// break;
            #// }
            #// METHOD B: cache all keys in this lookup - more memory but faster on next lookup of not-previously-looked-up key
            #// $cache[$file][$name][substr($line, 0, $keylength)] = trim(substr($line, $keylength + 1));
            explodedLine_ = php_explode("   ", line_, 2)
            ThisKey_ = explodedLine_[0] if (php_isset(lambda : explodedLine_[0])) else ""
            ThisValue_ = explodedLine_[1] if (php_isset(lambda : explodedLine_[1])) else ""
            cache_[file_][name_][ThisKey_] = php_trim(ThisValue_)
        # end while
        #// Close and return
        php_fclose(fp_)
        return cache_[file_][name_][key_] if (php_isset(lambda : cache_[file_][name_][key_])) else ""
    # end def embeddedlookup
    #// 
    #// @param string $filename
    #// @param string $sourcefile
    #// @param bool   $DieOnFailure
    #// 
    #// @return bool
    #// @throws Exception
    #//
    @classmethod
    def includedependency(self, filename_=None, sourcefile_=None, DieOnFailure_=None):
        if DieOnFailure_ is None:
            DieOnFailure_ = False
        # end if
        
        global GETID3_ERRORARRAY_
        php_check_if_defined("GETID3_ERRORARRAY_")
        if php_file_exists(filename_):
            if php_include_file(filename_, once=False):
                return True
            else:
                diemessage_ = php_basename(sourcefile_) + " depends on " + filename_ + ", which has errors"
            # end if
        else:
            diemessage_ = php_basename(sourcefile_) + " depends on " + filename_ + ", which is missing"
        # end if
        if DieOnFailure_:
            raise php_new_class("Exception", lambda : Exception(diemessage_))
        else:
            GETID3_ERRORARRAY_[-1] = diemessage_
        # end if
        return False
    # end def includedependency
    #// 
    #// @param string $string
    #// 
    #// @return string
    #//
    @classmethod
    def trimnullbyte(self, string_=None):
        
        
        return php_trim(string_, " ")
    # end def trimnullbyte
    #// 
    #// @param string $path
    #// 
    #// @return float|bool
    #//
    @classmethod
    def getfilesizesyscall(self, path_=None):
        
        
        filesize_ = False
        if GETID3_OS_ISWINDOWS:
            if php_class_exists("COM"):
                #// From PHP 5.3.15 and 5.4.5, COM and DOTNET is no longer built into the php core.you have to add COM support in php.ini:
                filesystem_ = php_new_class("COM", lambda : COM("Scripting.FileSystemObject"))
                file_ = filesystem_.getfile(path_)
                filesize_ = file_.size()
                filesystem_ = None
                file_ = None
            else:
                commandline_ = "for %I in (" + escapeshellarg(path_) + ") do @echo %~zI"
            # end if
        else:
            commandline_ = "ls -l " + escapeshellarg(path_) + " | awk '{print $5}'"
        # end if
        if (php_isset(lambda : commandline_)):
            output_ = php_trim(os.system("commandline_"))
            if ctype_digit(output_):
                filesize_ = php_float(output_)
            # end if
        # end if
        return filesize_
    # end def getfilesizesyscall
    #// 
    #// @param string $filename
    #// 
    #// @return string|false
    #//
    @classmethod
    def truepath(self, filename_=None):
        
        
        #// 2017-11-08: this could use some improvement, patches welcome
        if php_preg_match("#^(\\\\\\\\|//)[a-z0-9]#i", filename_, matches_):
            #// PHP's built-in realpath function does not work on UNC Windows shares
            goodpath_ = Array()
            for part_ in php_explode("/", php_str_replace("\\", "/", filename_)):
                if part_ == ".":
                    continue
                # end if
                if part_ == "..":
                    if php_count(goodpath_):
                        php_array_pop(goodpath_)
                    else:
                        #// cannot step above this level, already at top level
                        return False
                    # end if
                else:
                    goodpath_[-1] = part_
                # end if
            # end for
            return php_implode(DIRECTORY_SEPARATOR, goodpath_)
        # end if
        return php_realpath(filename_)
    # end def truepath
    #// 
    #// Workaround for Bug #37268 (https://bugs.php.net/bug.php?id=37268)
    #// 
    #// @param string $path A path.
    #// @param string $suffix If the name component ends in suffix this will also be cut off.
    #// 
    #// @return string
    #//
    @classmethod
    def mb_basename(self, path_=None, suffix_=None):
        if suffix_ is None:
            suffix_ = None
        # end if
        
        splited_ = php_preg_split("#/#", php_rtrim(path_, "/ "))
        return php_substr(php_basename("X" + splited_[php_count(splited_) - 1], suffix_), 1)
    # end def mb_basename
# end class getid3_lib
