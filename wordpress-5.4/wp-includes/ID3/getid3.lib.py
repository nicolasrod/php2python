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
    def printhexbytes(self, string=None, hex=True, spaces=True, htmlencoding="UTF-8"):
        
        returnstring = ""
        i = 0
        while i < php_strlen(string):
            
            if hex:
                returnstring += php_str_pad(dechex(php_ord(string[i])), 2, "0", STR_PAD_LEFT)
            else:
                returnstring += " " + string[i] if php_preg_match("#[ -~]#", string[i]) else "Â¤"
            # end if
            if spaces:
                returnstring += " "
            # end if
            i += 1
        # end while
        if (not php_empty(lambda : htmlencoding)):
            if htmlencoding == True:
                htmlencoding = "UTF-8"
                pass
            # end if
            returnstring = htmlentities(returnstring, ENT_QUOTES, htmlencoding)
        # end if
        return returnstring
    # end def printhexbytes
    #// 
    #// Truncates a floating-point number at the decimal point.
    #// 
    #// @param float $floatnumber
    #// 
    #// @return float|int returns int (if possible, otherwise float)
    #//
    @classmethod
    def trunc(self, floatnumber=None):
        
        if floatnumber >= 1:
            truncatednumber = floor(floatnumber)
        elif floatnumber <= -1:
            truncatednumber = ceil(floatnumber)
        else:
            truncatednumber = 0
        # end if
        if self.intvaluesupported(truncatednumber):
            truncatednumber = php_int(truncatednumber)
        # end if
        return truncatednumber
    # end def trunc
    #// 
    #// @param int|null $variable
    #// @param int      $increment
    #// 
    #// @return bool
    #//
    @classmethod
    def safe_inc(self, variable=None, increment=1):
        
        if (php_isset(lambda : variable)):
            variable += increment
        else:
            variable = increment
        # end if
        return True
    # end def safe_inc
    #// 
    #// @param int|float $floatnum
    #// 
    #// @return int|float
    #//
    @classmethod
    def castasint(self, floatnum=None):
        
        #// convert to float if not already
        floatnum = php_float(floatnum)
        #// convert a float to type int, only if possible
        if self.trunc(floatnum) == floatnum:
            #// it's not floating point
            if self.intvaluesupported(floatnum):
                #// it's within int range
                floatnum = php_int(floatnum)
            # end if
        # end if
        return floatnum
    # end def castasint
    #// 
    #// @param int $num
    #// 
    #// @return bool
    #//
    @classmethod
    def intvaluesupported(self, num=None):
        
        intvaluesupported.hasINT64 = None
        if intvaluesupported.hasINT64 == None:
            #// 10x faster than is_null()
            intvaluesupported.hasINT64 = php_is_int(pow(2, 31))
            #// 32-bit int are limited to (2^31)-1
            if (not intvaluesupported.hasINT64) and (not php_defined("PHP_INT_MIN")):
                php_define("PHP_INT_MIN", (1 << (PHP_INT_MAX).bit_length()) - 1 - PHP_INT_MAX)
            # end if
        # end if
        #// if integers are 64-bit - no other check required
        if intvaluesupported.hasINT64 or num <= PHP_INT_MAX and num >= PHP_INT_MIN:
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
    def decimalizefraction(self, fraction=None):
        
        numerator, denominator = php_explode("/", fraction)
        return numerator / denominator if denominator else 1
    # end def decimalizefraction
    #// 
    #// @param string $binarynumerator
    #// 
    #// @return float
    #//
    @classmethod
    def decimalbinary2float(self, binarynumerator=None):
        
        numerator = self.bin2dec(binarynumerator)
        denominator = self.bin2dec("1" + php_str_repeat("0", php_strlen(binarynumerator)))
        return numerator / denominator
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
    def normalizebinarypoint(self, binarypointnumber=None, maxbits=52):
        
        if php_strpos(binarypointnumber, ".") == False:
            binarypointnumber = "0." + binarypointnumber
        elif binarypointnumber[0] == ".":
            binarypointnumber = "0" + binarypointnumber
        # end if
        exponent = 0
        while True:
            
            if not (binarypointnumber[0] != "1" or php_substr(binarypointnumber, 1, 1) != "."):
                break
            # end if
            if php_substr(binarypointnumber, 1, 1) == ".":
                exponent -= 1
                binarypointnumber = php_substr(binarypointnumber, 2, 1) + "." + php_substr(binarypointnumber, 3)
            else:
                pointpos = php_strpos(binarypointnumber, ".")
                exponent += pointpos - 1
                binarypointnumber = php_str_replace(".", "", binarypointnumber)
                binarypointnumber = binarypointnumber[0] + "." + php_substr(binarypointnumber, 1)
            # end if
        # end while
        binarypointnumber = php_str_pad(php_substr(binarypointnumber, 0, maxbits + 2), maxbits + 2, "0", STR_PAD_RIGHT)
        return Array({"normalized": binarypointnumber, "exponent": php_int(exponent)})
    # end def normalizebinarypoint
    #// 
    #// @link http://www.scri.fsu.edu/~jac/MAD3401/Backgrnd/binary.html
    #// 
    #// @param float $floatvalue
    #// 
    #// @return string
    #//
    @classmethod
    def float2binarydecimal(self, floatvalue=None):
        
        maxbits = 128
        #// to how many bits of precision should the calculations be taken?
        intpart = self.trunc(floatvalue)
        floatpart = abs(floatvalue - intpart)
        pointbitstring = ""
        while True:
            
            if not (floatpart != 0 and php_strlen(pointbitstring) < maxbits):
                break
            # end if
            floatpart *= 2
            pointbitstring += php_str(self.trunc(floatpart))
            floatpart -= self.trunc(floatpart)
        # end while
        binarypointnumber = decbin(intpart) + "." + pointbitstring
        return binarypointnumber
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
    def float2string(self, floatvalue=None, bits=None):
        
        exponentbits = 0
        fractionbits = 0
        for case in Switch(bits):
            if case(32):
                exponentbits = 8
                fractionbits = 23
                break
            # end if
            if case(64):
                exponentbits = 11
                fractionbits = 52
                break
            # end if
            if case():
                return False
                break
            # end if
        # end for
        if floatvalue >= 0:
            signbit = "0"
        else:
            signbit = "1"
        # end if
        normalizedbinary = self.normalizebinarypoint(self.float2binarydecimal(floatvalue), fractionbits)
        biasedexponent = pow(2, exponentbits - 1) - 1 + normalizedbinary["exponent"]
        #// (127 or 1023) +/- exponent
        exponentbitstring = php_str_pad(decbin(biasedexponent), exponentbits, "0", STR_PAD_LEFT)
        fractionbitstring = php_str_pad(php_substr(normalizedbinary["normalized"], 2), fractionbits, "0", STR_PAD_RIGHT)
        return self.bigendian2string(self.bin2dec(signbit + exponentbitstring + fractionbitstring), bits % 8, False)
    # end def float2string
    #// 
    #// @param string $byteword
    #// 
    #// @return float|false
    #//
    @classmethod
    def littleendian2float(self, byteword=None):
        
        return self.bigendian2float(php_strrev(byteword))
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
    def bigendian2float(self, byteword=None):
        
        bitword = self.bigendian2bin(byteword)
        if (not bitword):
            return 0
        # end if
        signbit = bitword[0]
        floatvalue = 0
        exponentbits = 0
        fractionbits = 0
        for case in Switch(php_strlen(byteword) * 8):
            if case(32):
                exponentbits = 8
                fractionbits = 23
                break
            # end if
            if case(64):
                exponentbits = 11
                fractionbits = 52
                break
            # end if
            if case(80):
                #// 80-bit Apple SANE format
                #// http://www.mactech.com/articles/mactech/Vol.06/06.01/SANENormalized
                exponentstring = php_substr(bitword, 1, 15)
                isnormalized = php_intval(bitword[16])
                fractionstring = php_substr(bitword, 17, 63)
                exponent = pow(2, self.bin2dec(exponentstring) - 16383)
                fraction = isnormalized + self.decimalbinary2float(fractionstring)
                floatvalue = exponent * fraction
                if signbit == "1":
                    floatvalue *= -1
                # end if
                return floatvalue
                break
            # end if
            if case():
                return False
                break
            # end if
        # end for
        exponentstring = php_substr(bitword, 1, exponentbits)
        fractionstring = php_substr(bitword, exponentbits + 1, fractionbits)
        exponent = self.bin2dec(exponentstring)
        fraction = self.bin2dec(fractionstring)
        if exponent == pow(2, exponentbits) - 1 and fraction != 0:
            #// Not a Number
            floatvalue = False
        elif exponent == pow(2, exponentbits) - 1 and fraction == 0:
            if signbit == "1":
                floatvalue = "-infinity"
            else:
                floatvalue = "+infinity"
            # end if
        elif exponent == 0 and fraction == 0:
            if signbit == "1":
                floatvalue = -0
            else:
                floatvalue = 0
            # end if
            floatvalue = 0 if signbit else -0
        elif exponent == 0 and fraction != 0:
            #// These are 'unnormalized' values
            floatvalue = pow(2, -1 * pow(2, exponentbits - 1) - 2) * self.decimalbinary2float(fractionstring)
            if signbit == "1":
                floatvalue *= -1
            # end if
        elif exponent != 0:
            floatvalue = pow(2, exponent - pow(2, exponentbits - 1) - 1) * 1 + self.decimalbinary2float(fractionstring)
            if signbit == "1":
                floatvalue *= -1
            # end if
        # end if
        return php_float(floatvalue)
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
    def bigendian2int(self, byteword=None, synchsafe=False, signed=False):
        
        intvalue = 0
        bytewordlen = php_strlen(byteword)
        if bytewordlen == 0:
            return False
        # end if
        i = 0
        while i < bytewordlen:
            
            if synchsafe:
                #// disregard MSB, effectively 7-bit bytes
                #// $intvalue = $intvalue | (ord($byteword{$i}) & 0x7F) << (($bytewordlen - 1 - $i) * 7); // faster, but runs into problems past 2^31 on 32-bit systems
                intvalue += php_ord(byteword[i]) & 127 * pow(2, bytewordlen - 1 - i * 7)
            else:
                intvalue += php_ord(byteword[i]) * pow(256, bytewordlen - 1 - i)
            # end if
            i += 1
        # end while
        if signed and (not synchsafe):
            #// synchsafe ints are not allowed to be signed
            if bytewordlen <= PHP_INT_SIZE:
                signMaskBit = 128 << 8 * bytewordlen - 1
                if intvalue & signMaskBit:
                    intvalue = 0 - intvalue & signMaskBit - 1
                # end if
            else:
                raise php_new_class("Exception", lambda : Exception("ERROR: Cannot have signed integers larger than " + 8 * PHP_INT_SIZE + "-bits (" + php_strlen(byteword) + ") in self::BigEndian2Int()"))
            # end if
        # end if
        return self.castasint(intvalue)
    # end def bigendian2int
    #// 
    #// @param string $byteword
    #// @param bool   $signed
    #// 
    #// @return int|float|false
    #//
    @classmethod
    def littleendian2int(self, byteword=None, signed=False):
        
        return self.bigendian2int(php_strrev(byteword), False, signed)
    # end def littleendian2int
    #// 
    #// @param string $byteword
    #// 
    #// @return string
    #//
    @classmethod
    def littleendian2bin(self, byteword=None):
        
        return self.bigendian2bin(php_strrev(byteword))
    # end def littleendian2bin
    #// 
    #// @param string $byteword
    #// 
    #// @return string
    #//
    @classmethod
    def bigendian2bin(self, byteword=None):
        
        binvalue = ""
        bytewordlen = php_strlen(byteword)
        i = 0
        while i < bytewordlen:
            
            binvalue += php_str_pad(decbin(php_ord(byteword[i])), 8, "0", STR_PAD_LEFT)
            i += 1
        # end while
        return binvalue
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
    def bigendian2string(self, number=None, minbytes=1, synchsafe=False, signed=False):
        
        if number < 0:
            raise php_new_class("Exception", lambda : Exception("ERROR: self::BigEndian2String() does not support negative numbers"))
        # end if
        maskbyte = 127 if synchsafe or signed else 255
        intstring = ""
        if signed:
            if minbytes > PHP_INT_SIZE:
                raise php_new_class("Exception", lambda : Exception("ERROR: Cannot have signed integers larger than " + 8 * PHP_INT_SIZE + "-bits in self::BigEndian2String()"))
            # end if
            number = number & 128 << 8 * minbytes - 1
        # end if
        while True:
            
            if not (number != 0):
                break
            # end if
            quotient = number / maskbyte + 1
            intstring = chr(ceil(quotient - floor(quotient) * maskbyte)) + intstring
            number = floor(quotient)
        # end while
        return php_str_pad(intstring, minbytes, " ", STR_PAD_LEFT)
    # end def bigendian2string
    #// 
    #// @param int $number
    #// 
    #// @return string
    #//
    @classmethod
    def dec2bin(self, number=None):
        
        while True:
            
            if not (number >= 256):
                break
            # end if
            bytes[-1] = number / 256 - floor(number / 256) * 256
            number = floor(number / 256)
        # end while
        bytes[-1] = number
        binstring = ""
        i = 0
        while i < php_count(bytes):
            
            binstring = decbin(bytes[i]) if i == php_count(bytes) - 1 else php_str_pad(decbin(bytes[i]), 8, "0", STR_PAD_LEFT) + binstring
            i += 1
        # end while
        return binstring
    # end def dec2bin
    #// 
    #// @param string $binstring
    #// @param bool   $signed
    #// 
    #// @return int|float
    #//
    @classmethod
    def bin2dec(self, binstring=None, signed=False):
        
        signmult = 1
        if signed:
            if binstring[0] == "1":
                signmult = -1
            # end if
            binstring = php_substr(binstring, 1)
        # end if
        decvalue = 0
        i = 0
        while i < php_strlen(binstring):
            
            decvalue += php_int(php_substr(binstring, php_strlen(binstring) - i - 1, 1)) * pow(2, i)
            i += 1
        # end while
        return self.castasint(decvalue * signmult)
    # end def bin2dec
    #// 
    #// @param string $binstring
    #// 
    #// @return string
    #//
    @classmethod
    def bin2string(self, binstring=None):
        
        #// return 'hi' for input of '0110100001101001'
        string = ""
        binstringreversed = php_strrev(binstring)
        i = 0
        while i < php_strlen(binstringreversed):
            
            string = chr(self.bin2dec(php_strrev(php_substr(binstringreversed, i, 8)))) + string
            i += 8
        # end while
        return string
    # end def bin2string
    #// 
    #// @param int  $number
    #// @param int  $minbytes
    #// @param bool $synchsafe
    #// 
    #// @return string
    #//
    @classmethod
    def littleendian2string(self, number=None, minbytes=1, synchsafe=False):
        
        intstring = ""
        while True:
            
            if not (number > 0):
                break
            # end if
            if synchsafe:
                intstring = intstring + chr(number & 127)
                number >>= 7
            else:
                intstring = intstring + chr(number & 255)
                number >>= 8
            # end if
        # end while
        return php_str_pad(intstring, minbytes, " ", STR_PAD_RIGHT)
    # end def littleendian2string
    #// 
    #// @param array $array1
    #// @param array $array2
    #// 
    #// @return array|false
    #//
    @classmethod
    def array_merge_clobber(self, array1=None, array2=None):
        
        #// written by kcØhireability*com
        #// taken from http://www.php.net/manual/en/function.array-merge-recursive.php
        if (not php_is_array(array1)) or (not php_is_array(array2)):
            return False
        # end if
        newarray = array1
        for key,val in array2:
            if php_is_array(val) and (php_isset(lambda : newarray[key])) and php_is_array(newarray[key]):
                newarray[key] = self.array_merge_clobber(newarray[key], val)
            else:
                newarray[key] = val
            # end if
        # end for
        return newarray
    # end def array_merge_clobber
    #// 
    #// @param array $array1
    #// @param array $array2
    #// 
    #// @return array|false
    #//
    @classmethod
    def array_merge_noclobber(self, array1=None, array2=None):
        
        if (not php_is_array(array1)) or (not php_is_array(array2)):
            return False
        # end if
        newarray = array1
        for key,val in array2:
            if php_is_array(val) and (php_isset(lambda : newarray[key])) and php_is_array(newarray[key]):
                newarray[key] = self.array_merge_noclobber(newarray[key], val)
            elif (not (php_isset(lambda : newarray[key]))):
                newarray[key] = val
            # end if
        # end for
        return newarray
    # end def array_merge_noclobber
    #// 
    #// @param array $array1
    #// @param array $array2
    #// 
    #// @return array|false|null
    #//
    @classmethod
    def flipped_array_merge_noclobber(self, array1=None, array2=None):
        
        if (not php_is_array(array1)) or (not php_is_array(array2)):
            return False
        # end if
        #// # naturally, this only works non-recursively
        newarray = php_array_flip(array1)
        for key,val in php_array_flip(array2):
            if (not (php_isset(lambda : newarray[key]))):
                newarray[key] = php_count(newarray)
            # end if
        # end for
        return php_array_flip(newarray)
    # end def flipped_array_merge_noclobber
    #// 
    #// @param array $theArray
    #// 
    #// @return bool
    #//
    @classmethod
    def ksort_recursive(self, theArray=None):
        
        ksort(theArray)
        for key,value in theArray:
            if php_is_array(value):
                self.ksort_recursive(theArray[key])
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
    def fileextension(self, filename=None, numextensions=1):
        
        if php_strstr(filename, "."):
            reversedfilename = php_strrev(filename)
            offset = 0
            i = 0
            while i < numextensions:
                
                offset = php_strpos(reversedfilename, ".", offset + 1)
                if offset == False:
                    return ""
                # end if
                i += 1
            # end while
            return php_strrev(php_substr(reversedfilename, 0, offset))
        # end if
        return ""
    # end def fileextension
    #// 
    #// @param int $seconds
    #// 
    #// @return string
    #//
    @classmethod
    def playtimestring(self, seconds=None):
        
        sign = "-" if seconds < 0 else ""
        seconds = round(abs(seconds))
        H = php_int(floor(seconds / 3600))
        M = php_int(floor(seconds - 3600 * H / 60))
        S = php_int(round(seconds - 3600 * H - 60 * M))
        return sign + H + ":" if H else "" + php_str_pad(M, 2, "0", STR_PAD_LEFT) if H else php_intval(M) + ":" + php_str_pad(S, 2, 0, STR_PAD_LEFT)
    # end def playtimestring
    #// 
    #// @param int $macdate
    #// 
    #// @return int|float
    #//
    @classmethod
    def datemac2unix(self, macdate=None):
        
        #// Macintosh timestamp: seconds since 00:00h January 1, 1904
        #// UNIX timestamp:      seconds since 00:00h January 1, 1970
        return self.castasint(macdate - 2082844800)
    # end def datemac2unix
    #// 
    #// @param string $rawdata
    #// 
    #// @return float
    #//
    @classmethod
    def fixedpoint8_8(self, rawdata=None):
        
        return self.bigendian2int(php_substr(rawdata, 0, 1)) + php_float(self.bigendian2int(php_substr(rawdata, 1, 1)) / pow(2, 8))
    # end def fixedpoint8_8
    #// 
    #// @param string $rawdata
    #// 
    #// @return float
    #//
    @classmethod
    def fixedpoint16_16(self, rawdata=None):
        
        return self.bigendian2int(php_substr(rawdata, 0, 2)) + php_float(self.bigendian2int(php_substr(rawdata, 2, 2)) / pow(2, 16))
    # end def fixedpoint16_16
    #// 
    #// @param string $rawdata
    #// 
    #// @return float
    #//
    @classmethod
    def fixedpoint2_30(self, rawdata=None):
        
        binarystring = self.bigendian2bin(rawdata)
        return self.bin2dec(php_substr(binarystring, 0, 2)) + php_float(self.bin2dec(php_substr(binarystring, 2, 30)) / pow(2, 30))
    # end def fixedpoint2_30
    #// 
    #// @param string $ArrayPath
    #// @param string $Separator
    #// @param mixed $Value
    #// 
    #// @return array
    #//
    @classmethod
    def createdeeparray(self, ArrayPath=None, Separator=None, Value=None):
        
        #// assigns $Value to a nested array path:
        #// $foo = self::CreateDeepArray('/path/to/my', '/', 'file.txt')
        #// is the same as:
        #// $foo = array('path'=>array('to'=>'array('my'=>array('file.txt'))));
        #// or
        #// $foo['path']['to']['my'] = 'file.txt';
        ArrayPath = php_ltrim(ArrayPath, Separator)
        pos = php_strpos(ArrayPath, Separator)
        if pos != False:
            ReturnedArray[php_substr(ArrayPath, 0, pos)] = self.createdeeparray(php_substr(ArrayPath, pos + 1), Separator, Value)
        else:
            ReturnedArray[ArrayPath] = Value
        # end if
        return ReturnedArray
    # end def createdeeparray
    #// 
    #// @param array $arraydata
    #// @param bool  $returnkey
    #// 
    #// @return int|false
    #//
    @classmethod
    def array_max(self, arraydata=None, returnkey=False):
        
        maxvalue = False
        maxkey = False
        for key,value in arraydata:
            if (not php_is_array(value)):
                if value > maxvalue:
                    maxvalue = value
                    maxkey = key
                # end if
            # end if
        # end for
        return maxkey if returnkey else maxvalue
    # end def array_max
    #// 
    #// @param array $arraydata
    #// @param bool  $returnkey
    #// 
    #// @return int|false
    #//
    @classmethod
    def array_min(self, arraydata=None, returnkey=False):
        
        minvalue = False
        minkey = False
        for key,value in arraydata:
            if (not php_is_array(value)):
                if value > minvalue:
                    minvalue = value
                    minkey = key
                # end if
            # end if
        # end for
        return minkey if returnkey else minvalue
    # end def array_min
    #// 
    #// @param string $XMLstring
    #// 
    #// @return array|false
    #//
    @classmethod
    def xml2array(self, XMLstring=None):
        
        if php_function_exists("simplexml_load_string") and php_function_exists("libxml_disable_entity_loader"):
            #// http://websec.io/2012/08/27/Preventing-XEE-in-PHP.html
            #// https://core.trac.wordpress.org/changeset/29378
            loader = libxml_disable_entity_loader(True)
            XMLobject = simplexml_load_string(XMLstring, "SimpleXMLElement", LIBXML_NOENT)
            return_ = self.simplexmlelement2array(XMLobject)
            libxml_disable_entity_loader(loader)
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
    def simplexmlelement2array(self, XMLobject=None):
        
        if (not php_is_object(XMLobject)) and (not php_is_array(XMLobject)):
            return XMLobject
        # end if
        XMLarray = get_object_vars(XMLobject) if type(XMLobject).__name__ == "SimpleXMLElement" else XMLobject
        for key,value in XMLarray:
            XMLarray[key] = self.simplexmlelement2array(value)
        # end for
        return XMLarray
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
    def hash_data(self, file=None, offset=None, end_=None, algorithm=None):
        
        if (not self.intvaluesupported(end_)):
            return False
        # end if
        if (not php_in_array(algorithm, Array("md5", "sha1"))):
            raise php_new_class("getid3_exception", lambda : getid3_exception("Invalid algorithm (" + algorithm + ") in self::hash_data()"))
        # end if
        size = end_ - offset
        fp = fopen(file, "rb")
        fseek(fp, offset)
        ctx = hash_init(algorithm)
        while True:
            
            if not (size > 0):
                break
            # end if
            buffer = fread(fp, php_min(size, getID3.FREAD_BUFFER_SIZE))
            hash_update(ctx, buffer)
            size -= getID3.FREAD_BUFFER_SIZE
        # end while
        hash = hash_final(ctx)
        php_fclose(fp)
        return hash
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
    def copyfileparts(self, filename_source=None, filename_dest=None, offset=None, length=None):
        
        if (not self.intvaluesupported(offset + length)):
            raise php_new_class("Exception", lambda : Exception("cannot copy file portion, it extends beyond the " + round(PHP_INT_MAX / 1073741824) + "GB limit"))
        # end if
        fp_src = fopen(filename_source, "rb")
        if php_is_readable(filename_source) and php_is_file(filename_source) and fp_src:
            fp_dest = fopen(filename_dest, "wb")
            if fp_dest:
                if fseek(fp_src, offset) == 0:
                    byteslefttowrite = length
                    while True:
                        buffer = fread(fp_src, php_min(byteslefttowrite, getID3.FREAD_BUFFER_SIZE))
                        if not (byteslefttowrite > 0 and buffer):
                            break
                        # end if
                        byteswritten = fwrite(fp_dest, buffer, byteslefttowrite)
                        byteslefttowrite -= byteswritten
                    # end while
                    php_fclose(fp_dest)
                    return True
                else:
                    php_fclose(fp_src)
                    raise php_new_class("Exception", lambda : Exception("failed to seek to offset " + offset + " in " + filename_source))
                # end if
            else:
                raise php_new_class("Exception", lambda : Exception("failed to create file for writing " + filename_dest))
            # end if
        else:
            raise php_new_class("Exception", lambda : Exception("failed to open file for reading " + filename_source))
        # end if
    # end def copyfileparts
    #// 
    #// @param int $charval
    #// 
    #// @return string
    #//
    @classmethod
    def iconv_fallback_int_utf8(self, charval=None):
        
        if charval < 128:
            #// 0bbbbbbb
            newcharstring = chr(charval)
        elif charval < 2048:
            #// 110bbbbb 10bbbbbb
            newcharstring = chr(charval >> 6 | 192)
            newcharstring += chr(charval & 63 | 128)
        elif charval < 65536:
            #// 1110bbbb 10bbbbbb 10bbbbbb
            newcharstring = chr(charval >> 12 | 224)
            newcharstring += chr(charval >> 6 | 192)
            newcharstring += chr(charval & 63 | 128)
        else:
            #// 11110bbb 10bbbbbb 10bbbbbb 10bbbbbb
            newcharstring = chr(charval >> 18 | 240)
            newcharstring += chr(charval >> 12 | 192)
            newcharstring += chr(charval >> 6 | 192)
            newcharstring += chr(charval & 63 | 128)
        # end if
        return newcharstring
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
    def iconv_fallback_iso88591_utf8(self, string=None, bom=False):
        
        if php_function_exists("utf8_encode"):
            return utf8_encode(string)
        # end if
        #// utf8_encode() unavailable, use getID3()'s iconv_fallback() conversions (possibly PHP is compiled without XML support)
        newcharstring = ""
        if bom:
            newcharstring += "ï»¿"
        # end if
        i = 0
        while i < php_strlen(string):
            
            charval = php_ord(string[i])
            newcharstring += self.iconv_fallback_int_utf8(charval)
            i += 1
        # end while
        return newcharstring
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
    def iconv_fallback_iso88591_utf16be(self, string=None, bom=False):
        
        newcharstring = ""
        if bom:
            newcharstring += "þÿ"
        # end if
        i = 0
        while i < php_strlen(string):
            
            newcharstring += " " + string[i]
            i += 1
        # end while
        return newcharstring
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
    def iconv_fallback_iso88591_utf16le(self, string=None, bom=False):
        
        newcharstring = ""
        if bom:
            newcharstring += "ÿþ"
        # end if
        i = 0
        while i < php_strlen(string):
            
            newcharstring += string[i] + " "
            i += 1
        # end while
        return newcharstring
    # end def iconv_fallback_iso88591_utf16le
    #// 
    #// ISO-8859-1 => UTF-16LE (BOM)
    #// 
    #// @param string $string
    #// 
    #// @return string
    #//
    @classmethod
    def iconv_fallback_iso88591_utf16(self, string=None):
        
        return self.iconv_fallback_iso88591_utf16le(string, True)
    # end def iconv_fallback_iso88591_utf16
    #// 
    #// UTF-8 => ISO-8859-1
    #// 
    #// @param string $string
    #// 
    #// @return string
    #//
    @classmethod
    def iconv_fallback_utf8_iso88591(self, string=None):
        
        if php_function_exists("utf8_decode"):
            return utf8_decode(string)
        # end if
        #// utf8_decode() unavailable, use getID3()'s iconv_fallback() conversions (possibly PHP is compiled without XML support)
        newcharstring = ""
        offset = 0
        stringlength = php_strlen(string)
        while True:
            
            if not (offset < stringlength):
                break
            # end if
            if php_ord(string[offset]) | 7 == 247:
                #// 11110bbb 10bbbbbb 10bbbbbb 10bbbbbb
                charval = php_ord(string[offset + 0]) & 7 << 18 & php_ord(string[offset + 1]) & 63 << 12 & php_ord(string[offset + 2]) & 63 << 6 & php_ord(string[offset + 3]) & 63
                offset += 4
            elif php_ord(string[offset]) | 15 == 239:
                #// 1110bbbb 10bbbbbb 10bbbbbb
                charval = php_ord(string[offset + 0]) & 15 << 12 & php_ord(string[offset + 1]) & 63 << 6 & php_ord(string[offset + 2]) & 63
                offset += 3
            elif php_ord(string[offset]) | 31 == 223:
                #// 110bbbbb 10bbbbbb
                charval = php_ord(string[offset + 0]) & 31 << 6 & php_ord(string[offset + 1]) & 63
                offset += 2
            elif php_ord(string[offset]) | 127 == 127:
                #// 0bbbbbbb
                charval = php_ord(string[offset])
                offset += 1
            else:
                #// error? throw some kind of warning here?
                charval = False
                offset += 1
            # end if
            if charval != False:
                newcharstring += chr(charval) if charval < 256 else "?"
            # end if
        # end while
        return newcharstring
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
    def iconv_fallback_utf8_utf16be(self, string=None, bom=False):
        
        newcharstring = ""
        if bom:
            newcharstring += "þÿ"
        # end if
        offset = 0
        stringlength = php_strlen(string)
        while True:
            
            if not (offset < stringlength):
                break
            # end if
            if php_ord(string[offset]) | 7 == 247:
                #// 11110bbb 10bbbbbb 10bbbbbb 10bbbbbb
                charval = php_ord(string[offset + 0]) & 7 << 18 & php_ord(string[offset + 1]) & 63 << 12 & php_ord(string[offset + 2]) & 63 << 6 & php_ord(string[offset + 3]) & 63
                offset += 4
            elif php_ord(string[offset]) | 15 == 239:
                #// 1110bbbb 10bbbbbb 10bbbbbb
                charval = php_ord(string[offset + 0]) & 15 << 12 & php_ord(string[offset + 1]) & 63 << 6 & php_ord(string[offset + 2]) & 63
                offset += 3
            elif php_ord(string[offset]) | 31 == 223:
                #// 110bbbbb 10bbbbbb
                charval = php_ord(string[offset + 0]) & 31 << 6 & php_ord(string[offset + 1]) & 63
                offset += 2
            elif php_ord(string[offset]) | 127 == 127:
                #// 0bbbbbbb
                charval = php_ord(string[offset])
                offset += 1
            else:
                #// error? throw some kind of warning here?
                charval = False
                offset += 1
            # end if
            if charval != False:
                newcharstring += self.bigendian2string(charval, 2) if charval < 65536 else " " + "?"
            # end if
        # end while
        return newcharstring
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
    def iconv_fallback_utf8_utf16le(self, string=None, bom=False):
        
        newcharstring = ""
        if bom:
            newcharstring += "ÿþ"
        # end if
        offset = 0
        stringlength = php_strlen(string)
        while True:
            
            if not (offset < stringlength):
                break
            # end if
            if php_ord(string[offset]) | 7 == 247:
                #// 11110bbb 10bbbbbb 10bbbbbb 10bbbbbb
                charval = php_ord(string[offset + 0]) & 7 << 18 & php_ord(string[offset + 1]) & 63 << 12 & php_ord(string[offset + 2]) & 63 << 6 & php_ord(string[offset + 3]) & 63
                offset += 4
            elif php_ord(string[offset]) | 15 == 239:
                #// 1110bbbb 10bbbbbb 10bbbbbb
                charval = php_ord(string[offset + 0]) & 15 << 12 & php_ord(string[offset + 1]) & 63 << 6 & php_ord(string[offset + 2]) & 63
                offset += 3
            elif php_ord(string[offset]) | 31 == 223:
                #// 110bbbbb 10bbbbbb
                charval = php_ord(string[offset + 0]) & 31 << 6 & php_ord(string[offset + 1]) & 63
                offset += 2
            elif php_ord(string[offset]) | 127 == 127:
                #// 0bbbbbbb
                charval = php_ord(string[offset])
                offset += 1
            else:
                #// error? maybe throw some warning here?
                charval = False
                offset += 1
            # end if
            if charval != False:
                newcharstring += self.littleendian2string(charval, 2) if charval < 65536 else "?" + " "
            # end if
        # end while
        return newcharstring
    # end def iconv_fallback_utf8_utf16le
    #// 
    #// UTF-8 => UTF-16LE (BOM)
    #// 
    #// @param string $string
    #// 
    #// @return string
    #//
    @classmethod
    def iconv_fallback_utf8_utf16(self, string=None):
        
        return self.iconv_fallback_utf8_utf16le(string, True)
    # end def iconv_fallback_utf8_utf16
    #// 
    #// UTF-16BE => UTF-8
    #// 
    #// @param string $string
    #// 
    #// @return string
    #//
    @classmethod
    def iconv_fallback_utf16be_utf8(self, string=None):
        
        if php_substr(string, 0, 2) == "þÿ":
            #// strip BOM
            string = php_substr(string, 2)
        # end if
        newcharstring = ""
        i = 0
        while i < php_strlen(string):
            
            charval = self.bigendian2int(php_substr(string, i, 2))
            newcharstring += self.iconv_fallback_int_utf8(charval)
            i += 2
        # end while
        return newcharstring
    # end def iconv_fallback_utf16be_utf8
    #// 
    #// UTF-16LE => UTF-8
    #// 
    #// @param string $string
    #// 
    #// @return string
    #//
    @classmethod
    def iconv_fallback_utf16le_utf8(self, string=None):
        
        if php_substr(string, 0, 2) == "ÿþ":
            #// strip BOM
            string = php_substr(string, 2)
        # end if
        newcharstring = ""
        i = 0
        while i < php_strlen(string):
            
            charval = self.littleendian2int(php_substr(string, i, 2))
            newcharstring += self.iconv_fallback_int_utf8(charval)
            i += 2
        # end while
        return newcharstring
    # end def iconv_fallback_utf16le_utf8
    #// 
    #// UTF-16BE => ISO-8859-1
    #// 
    #// @param string $string
    #// 
    #// @return string
    #//
    @classmethod
    def iconv_fallback_utf16be_iso88591(self, string=None):
        
        if php_substr(string, 0, 2) == "þÿ":
            #// strip BOM
            string = php_substr(string, 2)
        # end if
        newcharstring = ""
        i = 0
        while i < php_strlen(string):
            
            charval = self.bigendian2int(php_substr(string, i, 2))
            newcharstring += chr(charval) if charval < 256 else "?"
            i += 2
        # end while
        return newcharstring
    # end def iconv_fallback_utf16be_iso88591
    #// 
    #// UTF-16LE => ISO-8859-1
    #// 
    #// @param string $string
    #// 
    #// @return string
    #//
    @classmethod
    def iconv_fallback_utf16le_iso88591(self, string=None):
        
        if php_substr(string, 0, 2) == "ÿþ":
            #// strip BOM
            string = php_substr(string, 2)
        # end if
        newcharstring = ""
        i = 0
        while i < php_strlen(string):
            
            charval = self.littleendian2int(php_substr(string, i, 2))
            newcharstring += chr(charval) if charval < 256 else "?"
            i += 2
        # end while
        return newcharstring
    # end def iconv_fallback_utf16le_iso88591
    #// 
    #// UTF-16 (BOM) => ISO-8859-1
    #// 
    #// @param string $string
    #// 
    #// @return string
    #//
    @classmethod
    def iconv_fallback_utf16_iso88591(self, string=None):
        
        bom = php_substr(string, 0, 2)
        if bom == "þÿ":
            return self.iconv_fallback_utf16be_iso88591(php_substr(string, 2))
        elif bom == "ÿþ":
            return self.iconv_fallback_utf16le_iso88591(php_substr(string, 2))
        # end if
        return string
    # end def iconv_fallback_utf16_iso88591
    #// 
    #// UTF-16 (BOM) => UTF-8
    #// 
    #// @param string $string
    #// 
    #// @return string
    #//
    @classmethod
    def iconv_fallback_utf16_utf8(self, string=None):
        
        bom = php_substr(string, 0, 2)
        if bom == "þÿ":
            return self.iconv_fallback_utf16be_utf8(php_substr(string, 2))
        elif bom == "ÿþ":
            return self.iconv_fallback_utf16le_utf8(php_substr(string, 2))
        # end if
        return string
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
    def iconv_fallback(self, in_charset=None, out_charset=None, string=None):
        
        if in_charset == out_charset:
            return string
        # end if
        #// mb_convert_encoding() available
        if php_function_exists("mb_convert_encoding"):
            if php_strtoupper(in_charset) == "UTF-16" and php_substr(string, 0, 2) != "þÿ" and php_substr(string, 0, 2) != "ÿþ":
                #// if BOM missing, mb_convert_encoding will mishandle the conversion, assume UTF-16BE and prepend appropriate BOM
                string = "ÿþ" + string
            # end if
            if php_strtoupper(in_charset) == "UTF-16" and php_strtoupper(out_charset) == "UTF-8":
                if string == "ÿþ" or string == "þÿ":
                    #// if string consists of only BOM, mb_convert_encoding will return the BOM unmodified
                    return ""
                # end if
            # end if
            converted_string = php_no_error(lambda: mb_convert_encoding(string, out_charset, in_charset))
            if converted_string:
                for case in Switch(out_charset):
                    if case("ISO-8859-1"):
                        converted_string = php_rtrim(converted_string, " ")
                        break
                    # end if
                # end for
                return converted_string
            # end if
            return string
            pass
        elif php_function_exists("iconv"):
            converted_string = php_no_error(lambda: iconv(in_charset, out_charset + "//TRANSLIT", string))
            if converted_string:
                for case in Switch(out_charset):
                    if case("ISO-8859-1"):
                        converted_string = php_rtrim(converted_string, " ")
                        break
                    # end if
                # end for
                return converted_string
            # end if
            #// iconv() may sometimes fail with "illegal character in input string" error message
            #// and return an empty string, but returning the unconverted string is more useful
            return string
        # end if
        iconv_fallback.ConversionFunctionList = Array()
        if php_empty(lambda : iconv_fallback.ConversionFunctionList):
            iconv_fallback.ConversionFunctionList["ISO-8859-1"]["UTF-8"] = "iconv_fallback_iso88591_utf8"
            iconv_fallback.ConversionFunctionList["ISO-8859-1"]["UTF-16"] = "iconv_fallback_iso88591_utf16"
            iconv_fallback.ConversionFunctionList["ISO-8859-1"]["UTF-16BE"] = "iconv_fallback_iso88591_utf16be"
            iconv_fallback.ConversionFunctionList["ISO-8859-1"]["UTF-16LE"] = "iconv_fallback_iso88591_utf16le"
            iconv_fallback.ConversionFunctionList["UTF-8"]["ISO-8859-1"] = "iconv_fallback_utf8_iso88591"
            iconv_fallback.ConversionFunctionList["UTF-8"]["UTF-16"] = "iconv_fallback_utf8_utf16"
            iconv_fallback.ConversionFunctionList["UTF-8"]["UTF-16BE"] = "iconv_fallback_utf8_utf16be"
            iconv_fallback.ConversionFunctionList["UTF-8"]["UTF-16LE"] = "iconv_fallback_utf8_utf16le"
            iconv_fallback.ConversionFunctionList["UTF-16"]["ISO-8859-1"] = "iconv_fallback_utf16_iso88591"
            iconv_fallback.ConversionFunctionList["UTF-16"]["UTF-8"] = "iconv_fallback_utf16_utf8"
            iconv_fallback.ConversionFunctionList["UTF-16LE"]["ISO-8859-1"] = "iconv_fallback_utf16le_iso88591"
            iconv_fallback.ConversionFunctionList["UTF-16LE"]["UTF-8"] = "iconv_fallback_utf16le_utf8"
            iconv_fallback.ConversionFunctionList["UTF-16BE"]["ISO-8859-1"] = "iconv_fallback_utf16be_iso88591"
            iconv_fallback.ConversionFunctionList["UTF-16BE"]["UTF-8"] = "iconv_fallback_utf16be_utf8"
        # end if
        if (php_isset(lambda : iconv_fallback.ConversionFunctionList[php_strtoupper(in_charset)][php_strtoupper(out_charset)])):
            ConversionFunction = iconv_fallback.ConversionFunctionList[php_strtoupper(in_charset)][php_strtoupper(out_charset)]
            return self.conversionfunction(string)
        # end if
        raise php_new_class("Exception", lambda : Exception("PHP does not has mb_convert_encoding() or iconv() support - cannot convert from " + in_charset + " to " + out_charset))
    # end def iconv_fallback
    #// 
    #// @param mixed  $data
    #// @param string $charset
    #// 
    #// @return mixed
    #//
    @classmethod
    def recursivemultibytecharstring2html(self, data=None, charset="ISO-8859-1"):
        
        if php_is_string(data):
            return self.multibytecharstring2html(data, charset)
        elif php_is_array(data):
            return_data = Array()
            for key,value in data:
                return_data[key] = self.recursivemultibytecharstring2html(value, charset)
            # end for
            return return_data
        # end if
        #// integer, float, objects, resources, etc
        return data
    # end def recursivemultibytecharstring2html
    #// 
    #// @param string|int|float $string
    #// @param string           $charset
    #// 
    #// @return string
    #//
    @classmethod
    def multibytecharstring2html(self, string=None, charset="ISO-8859-1"):
        
        string = php_str(string)
        #// in case trying to pass a numeric (float, int) string, would otherwise return an empty string
        HTMLstring = ""
        for case in Switch(php_strtolower(charset)):
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
                HTMLstring = htmlentities(string, ENT_COMPAT, charset)
                break
            # end if
            if case("utf-8"):
                strlen = php_strlen(string)
                i = 0
                while i < strlen:
                    
                    char_ord_val = php_ord(string[i])
                    charval = 0
                    if char_ord_val < 128:
                        charval = char_ord_val
                    elif char_ord_val & 240 >> 4 == 15 and i + 3 < strlen:
                        charval = char_ord_val & 7 << 18
                        i += 1
                        charval += php_ord(string[i]) & 63 << 12
                        i += 1
                        charval += php_ord(string[i]) & 63 << 6
                        i += 1
                        charval += php_ord(string[i]) & 63
                    elif char_ord_val & 224 >> 5 == 7 and i + 2 < strlen:
                        charval = char_ord_val & 15 << 12
                        i += 1
                        charval += php_ord(string[i]) & 63 << 6
                        i += 1
                        charval += php_ord(string[i]) & 63
                    elif char_ord_val & 192 >> 6 == 3 and i + 1 < strlen:
                        charval = char_ord_val & 31 << 6
                        i += 1
                        charval += php_ord(string[i]) & 63
                    # end if
                    if charval >= 32 and charval <= 127:
                        HTMLstring += htmlentities(chr(charval))
                    else:
                        HTMLstring += "&#" + charval + ";"
                    # end if
                    i += 1
                # end while
                break
            # end if
            if case("utf-16le"):
                i = 0
                while i < php_strlen(string):
                    
                    charval = self.littleendian2int(php_substr(string, i, 2))
                    if charval >= 32 and charval <= 127:
                        HTMLstring += chr(charval)
                    else:
                        HTMLstring += "&#" + charval + ";"
                    # end if
                    i += 2
                # end while
                break
            # end if
            if case("utf-16be"):
                i = 0
                while i < php_strlen(string):
                    
                    charval = self.bigendian2int(php_substr(string, i, 2))
                    if charval >= 32 and charval <= 127:
                        HTMLstring += chr(charval)
                    else:
                        HTMLstring += "&#" + charval + ";"
                    # end if
                    i += 2
                # end while
                break
            # end if
            if case():
                HTMLstring = "ERROR: Character set \"" + charset + "\" not supported in MultiByteCharString2HTML()"
                break
            # end if
        # end for
        return HTMLstring
    # end def multibytecharstring2html
    #// 
    #// @param int $namecode
    #// 
    #// @return string
    #//
    @classmethod
    def rgadnamelookup(self, namecode=None):
        
        rgadnamelookup.RGADname = Array()
        if php_empty(lambda : rgadnamelookup.RGADname):
            rgadnamelookup.RGADname[0] = "not set"
            rgadnamelookup.RGADname[1] = "Track Gain Adjustment"
            rgadnamelookup.RGADname[2] = "Album Gain Adjustment"
        # end if
        return rgadnamelookup.RGADname[namecode] if (php_isset(lambda : rgadnamelookup.RGADname[namecode])) else ""
    # end def rgadnamelookup
    #// 
    #// @param int $originatorcode
    #// 
    #// @return string
    #//
    @classmethod
    def rgadoriginatorlookup(self, originatorcode=None):
        
        rgadoriginatorlookup.RGADoriginator = Array()
        if php_empty(lambda : rgadoriginatorlookup.RGADoriginator):
            rgadoriginatorlookup.RGADoriginator[0] = "unspecified"
            rgadoriginatorlookup.RGADoriginator[1] = "pre-set by artist/producer/mastering engineer"
            rgadoriginatorlookup.RGADoriginator[2] = "set by user"
            rgadoriginatorlookup.RGADoriginator[3] = "determined automatically"
        # end if
        return rgadoriginatorlookup.RGADoriginator[originatorcode] if (php_isset(lambda : rgadoriginatorlookup.RGADoriginator[originatorcode])) else ""
    # end def rgadoriginatorlookup
    #// 
    #// @param int $rawadjustment
    #// @param int $signbit
    #// 
    #// @return float
    #//
    @classmethod
    def rgadadjustmentlookup(self, rawadjustment=None, signbit=None):
        
        adjustment = php_float(rawadjustment) / 10
        if signbit == 1:
            adjustment *= -1
        # end if
        return adjustment
    # end def rgadadjustmentlookup
    #// 
    #// @param int $namecode
    #// @param int $originatorcode
    #// @param int $replaygain
    #// 
    #// @return string
    #//
    @classmethod
    def rgadgainstring(self, namecode=None, originatorcode=None, replaygain=None):
        
        if replaygain < 0:
            signbit = "1"
        else:
            signbit = "0"
        # end if
        storedreplaygain = php_intval(round(replaygain * 10))
        gainstring = php_str_pad(decbin(namecode), 3, "0", STR_PAD_LEFT)
        gainstring += php_str_pad(decbin(originatorcode), 3, "0", STR_PAD_LEFT)
        gainstring += signbit
        gainstring += php_str_pad(decbin(storedreplaygain), 9, "0", STR_PAD_LEFT)
        return gainstring
    # end def rgadgainstring
    #// 
    #// @param float $amplitude
    #// 
    #// @return float
    #//
    @classmethod
    def rgadamplitude2db(self, amplitude=None):
        
        return 20 * log10(amplitude)
    # end def rgadamplitude2db
    #// 
    #// @param string $imgData
    #// @param array  $imageinfo
    #// 
    #// @return array|false
    #//
    @classmethod
    def getdataimagesize(self, imgData=None, imageinfo=Array()):
        
        getdataimagesize.tempdir = ""
        if php_empty(lambda : getdataimagesize.tempdir):
            if php_function_exists("sys_get_temp_dir"):
                getdataimagesize.tempdir = php_sys_get_temp_dir()
                pass
            # end if
            #// yes this is ugly, feel free to suggest a better way
            if php_include_file(php_dirname(__FILE__) + "/getid3.php", once=False):
                getid3_temp = php_new_class("getID3", lambda : getID3())
                if getid3_temp:
                    getid3_temp_tempdir = getid3_temp.getdataimagesize.tempdir
                    if getid3_temp_tempdir:
                        getdataimagesize.tempdir = getid3_temp_tempdir
                    # end if
                    getid3_temp = None
                    getid3_temp_tempdir = None
                # end if
            # end if
        # end if
        GetDataImageSize = False
        tempfilename = php_tempnam(getdataimagesize.tempdir, "gI3")
        if tempfilename:
            tmp = fopen(tempfilename, "wb")
            if php_is_writable(tempfilename) and php_is_file(tempfilename) and tmp:
                fwrite(tmp, imgData)
                php_fclose(tmp)
                GetDataImageSize = php_no_error(lambda: getimagesize(tempfilename, imageinfo))
                if GetDataImageSize == False or (not (php_isset(lambda : GetDataImageSize[0]))) or (not (php_isset(lambda : GetDataImageSize[1]))):
                    return False
                # end if
                GetDataImageSize["height"] = GetDataImageSize[0]
                GetDataImageSize["width"] = GetDataImageSize[1]
            # end if
            unlink(tempfilename)
        # end if
        return GetDataImageSize
    # end def getdataimagesize
    #// 
    #// @param string $mime_type
    #// 
    #// @return string
    #//
    @classmethod
    def imageextfrommime(self, mime_type=None):
        
        #// temporary way, works OK for now, but should be reworked in the future
        return php_str_replace(Array("image/", "x-", "jpeg"), Array("", "", "jpg"), mime_type)
    # end def imageextfrommime
    #// 
    #// @param array $ThisFileInfo
    #// 
    #// @return bool
    #//
    @classmethod
    def copytagstocomments(self, ThisFileInfo=None):
        
        #// Copy all entries from ['tags'] into common ['comments']
        if (not php_empty(lambda : ThisFileInfo["tags"])):
            for tagtype,tagarray in ThisFileInfo["tags"]:
                for tagname,tagdata in tagarray:
                    for key,value in tagdata:
                        if (not php_empty(lambda : value)):
                            if php_empty(lambda : ThisFileInfo["comments"][tagname]):
                                pass
                            elif tagtype == "id3v1":
                                newvaluelength = php_strlen(php_trim(value))
                                for existingkey,existingvalue in ThisFileInfo["comments"][tagname]:
                                    oldvaluelength = php_strlen(php_trim(existingvalue))
                                    if newvaluelength <= oldvaluelength and php_substr(existingvalue, 0, newvaluelength) == php_trim(value):
                                        break
                                    # end if
                                # end for
                            elif (not php_is_array(value)):
                                newvaluelength = php_strlen(php_trim(value))
                                for existingkey,existingvalue in ThisFileInfo["comments"][tagname]:
                                    oldvaluelength = php_strlen(php_trim(existingvalue))
                                    if php_strlen(existingvalue) > 10 and newvaluelength > oldvaluelength and php_substr(php_trim(value), 0, php_strlen(existingvalue)) == existingvalue:
                                        ThisFileInfo["comments"][tagname][existingkey] = php_trim(value)
                                        break
                                    # end if
                                # end for
                            # end if
                            if php_is_array(value) or php_empty(lambda : ThisFileInfo["comments"][tagname]) or (not php_in_array(php_trim(value), ThisFileInfo["comments"][tagname])):
                                value = php_trim(value) if php_is_string(value) else value
                                if (not php_is_int(key)) and (not ctype_digit(key)):
                                    ThisFileInfo["comments"][tagname][key] = value
                                else:
                                    if (php_isset(lambda : ThisFileInfo["comments"][tagname])):
                                        ThisFileInfo["comments"][tagname] = Array(value)
                                    else:
                                        ThisFileInfo["comments"][tagname][-1] = value
                                    # end if
                                # end if
                            # end if
                        # end if
                    # end for
                # end for
            # end for
            #// attempt to standardize spelling of returned keys
            StandardizeFieldNames = Array({"tracknumber": "track_number", "track": "track_number"})
            for badkey,goodkey in StandardizeFieldNames:
                if php_array_key_exists(badkey, ThisFileInfo["comments"]) and (not php_array_key_exists(goodkey, ThisFileInfo["comments"])):
                    ThisFileInfo["comments"][goodkey] = ThisFileInfo["comments"][badkey]
                    ThisFileInfo["comments"][badkey] = None
                # end if
            # end for
            #// Copy to ['comments_html']
            if (not php_empty(lambda : ThisFileInfo["comments"])):
                for field,values in ThisFileInfo["comments"]:
                    if field == "picture":
                        continue
                    # end if
                    for index,value in values:
                        if php_is_array(value):
                            ThisFileInfo["comments_html"][field][index] = value
                        else:
                            ThisFileInfo["comments_html"][field][index] = php_str_replace("&#0;", "", self.multibytecharstring2html(value, ThisFileInfo["encoding"]))
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
    def embeddedlookup(self, key=None, begin=None, end_=None, file=None, name=None):
        
        embeddedlookup.cache = None
        if (php_isset(lambda : embeddedlookup.cache[file][name])):
            return embeddedlookup.cache[file][name][key] if (php_isset(lambda : embeddedlookup.cache[file][name][key])) else ""
        # end if
        #// Init
        keylength = php_strlen(key)
        line_count = end_ - begin - 7
        #// Open php file
        fp = fopen(file, "r")
        #// Discard $begin lines
        i = 0
        while i < begin + 3:
            
            php_fgets(fp, 1024)
            i += 1
        # end while
        #// Loop thru line
        while True:
            
            if not (0 < line_count):
                break
            # end if
            #// Read line
            line = php_ltrim(php_fgets(fp, 1024), "  ")
            line_count -= 1
            #// METHOD A: only cache the matching key - less memory but slower on next lookup of not-previously-looked-up key
            #// $keycheck = substr($line, 0, $keylength);
            #// if ($key == $keycheck)  {
            #// $cache[$file][$name][$keycheck] = substr($line, $keylength + 1);
            #// break;
            #// }
            #// METHOD B: cache all keys in this lookup - more memory but faster on next lookup of not-previously-looked-up key
            #// $cache[$file][$name][substr($line, 0, $keylength)] = trim(substr($line, $keylength + 1));
            explodedLine = php_explode("    ", line, 2)
            ThisKey = explodedLine[0] if (php_isset(lambda : explodedLine[0])) else ""
            ThisValue = explodedLine[1] if (php_isset(lambda : explodedLine[1])) else ""
            embeddedlookup.cache[file][name][ThisKey] = php_trim(ThisValue)
        # end while
        #// Close and return
        php_fclose(fp)
        return embeddedlookup.cache[file][name][key] if (php_isset(lambda : embeddedlookup.cache[file][name][key])) else ""
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
    def includedependency(self, filename=None, sourcefile=None, DieOnFailure=False):
        
        global GETID3_ERRORARRAY
        php_check_if_defined("GETID3_ERRORARRAY")
        if php_file_exists(filename):
            if php_include_file(filename, once=False):
                return True
            else:
                diemessage = php_basename(sourcefile) + " depends on " + filename + ", which has errors"
            # end if
        else:
            diemessage = php_basename(sourcefile) + " depends on " + filename + ", which is missing"
        # end if
        if DieOnFailure:
            raise php_new_class("Exception", lambda : Exception(diemessage))
        else:
            GETID3_ERRORARRAY[-1] = diemessage
        # end if
        return False
    # end def includedependency
    #// 
    #// @param string $string
    #// 
    #// @return string
    #//
    @classmethod
    def trimnullbyte(self, string=None):
        
        return php_trim(string, " ")
    # end def trimnullbyte
    #// 
    #// @param string $path
    #// 
    #// @return float|bool
    #//
    @classmethod
    def getfilesizesyscall(self, path=None):
        
        filesize = False
        if GETID3_OS_ISWINDOWS:
            if php_class_exists("COM"):
                #// From PHP 5.3.15 and 5.4.5, COM and DOTNET is no longer built into the php core.you have to add COM support in php.ini:
                filesystem = php_new_class("COM", lambda : COM("Scripting.FileSystemObject"))
                file = filesystem.getfile(path)
                filesize = file.size()
                filesystem = None
                file = None
            else:
                commandline = "for %I in (" + escapeshellarg(path) + ") do @echo %~zI"
            # end if
        else:
            commandline = "ls -l " + escapeshellarg(path) + " | awk '{print $5}'"
        # end if
        if (php_isset(lambda : commandline)):
            output = php_trim(os.system("commandline"))
            if ctype_digit(output):
                filesize = php_float(output)
            # end if
        # end if
        return filesize
    # end def getfilesizesyscall
    #// 
    #// @param string $filename
    #// 
    #// @return string|false
    #//
    @classmethod
    def truepath(self, filename=None):
        
        #// 2017-11-08: this could use some improvement, patches welcome
        if php_preg_match("#^(\\\\\\\\|//)[a-z0-9]#i", filename, matches):
            #// PHP's built-in realpath function does not work on UNC Windows shares
            goodpath = Array()
            for part in php_explode("/", php_str_replace("\\", "/", filename)):
                if part == ".":
                    continue
                # end if
                if part == "..":
                    if php_count(goodpath):
                        php_array_pop(goodpath)
                    else:
                        #// cannot step above this level, already at top level
                        return False
                    # end if
                else:
                    goodpath[-1] = part
                # end if
            # end for
            return php_implode(DIRECTORY_SEPARATOR, goodpath)
        # end if
        return php_realpath(filename)
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
    def mb_basename(self, path=None, suffix=None):
        
        splited = php_preg_split("#/#", php_rtrim(path, "/ "))
        return php_substr(php_basename("X" + splited[php_count(splited) - 1], suffix), 1)
    # end def mb_basename
# end class getid3_lib
